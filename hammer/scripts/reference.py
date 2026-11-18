"""Score every prepared request with a vanilla Qwen3-Reranker run locally: the reference answers.

    uv run --extra reference scripts/reference.py                       # Qwen3-Reranker-0.6B, bf16, all sets
    uv run --extra reference scripts/reference.py --variant fp8         # fp8 linear layers (weights + activations)
    uv run --extra reference scripts/reference.py --variant fp8-kv      # bf16 model, K/V stored as scaled fp8
    uv run --extra reference scripts/reference.py --variant yarn        # bf16 model with static YaRN rope scaling x4
    uv run --extra reference scripts/reference.py --variant w4          # fp16, fp8-attn, w8, w4: see Reranker
    uv run --extra reference scripts/reference.py --model 4b --sets beir-scifact ladder1-32768

Needs an NVIDIA GPU. Writes reference/<model>[-<variant>]/<set>.jsonl, one line per request:

    {"id": "<set>/<query_id>", "scores": [P(yes) per document, in the request's document order]}

which is the same quantity a reranking endpoint returns as relevance_score. Prompt format, instruction and
yes/no scoring follow the model card (https://huggingface.co/Qwen/Qwen3-Reranker-0.6B), with no
length truncation. Also prints and saves nDCG@10 / MRR against the ground-truth labels.

The output is committed to the repository: hammer.py quality compares an endpoint's scores with it,
with no GPU. Only reference/qwen3-reranker-0.6b/ (bf16) is included here. Scores are computed in bfloat16, so they can drift
in the last digits between GPUs and library versions; `git diff --stat reference/` shows what changed.
"""

import argparse
import json
import math
import time

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

import download
from checksums import ROOT
from report import reference_metrics

PREPARED = ROOT / "data" / "prepared"
OUT = ROOT / "reference"

PREFIX = ('<|im_start|>system\nJudge whether the Document meets the requirements based on the Query '
          'and the Instruct provided. Note that the answer can only be "yes" or "no".<|im_end|>\n'
          '<|im_start|>user\n')
SUFFIX = "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
INSTRUCTION = "Given a web search query, retrieve relevant passages that answer the query"


# Variant -> suffix of the output directory. Ordered from mildest to strongest precision reduction.
VARIANTS = {"bf16": "", "fp16": "-fp16", "fp8-kv": "-fp8kv", "fp8-attn": "-fp8attn", "fp8": "-fp8",
            "w8": "-w8", "w4": "-w4", "yarn": "-yarn"}


def fp8_roundtrip(t: torch.Tensor) -> torch.Tensor:
    """Round through fp8 e4m3 with one scale per tensor, as fp8 caches/kernels store activations."""
    scale = t.abs().amax().clamp(min=1e-6) / 448.0  # e4m3 max
    return (t / scale).to(torch.float8_e4m3fn).to(t.dtype) * scale


def fake_quant_weights(model, bits: int, group: int | None) -> None:
    """Weight-only symmetric integer quantisation, dequantised back in place: exactly the numerics
    of an int8 (per output channel) or int4 (per group of `group` inputs) weight-only deployment."""
    qmax = 2 ** (bits - 1) - 1
    for name, mod in model.named_modules():
        if isinstance(mod, torch.nn.Linear) and "lm_head" not in name:
            w = mod.weight.data.float()
            shape = w.shape
            if group:
                w = w.view(shape[0], -1, group)
            scale = w.abs().amax(-1, keepdim=True).clamp(min=1e-8) / qmax
            w = ((w / scale).round().clamp(-qmax, qmax) * scale).view(shape)
            mod.weight.data = w.to(mod.weight.dtype)


class Reranker:
    """bf16: weights, activations and SDPA attention in bf16 (fp32 softmax inside the kernel).
    fp16: the same in float16.
    fp8-kv: bf16, but K and V pass through scaled fp8 e4m3 before attention (an fp8 KV cache).
    fp8-attn: bf16, but Q, K and V all pass through scaled fp8 before attention.
    fp8: the 196 linear layers get fp8 e4m3 weights (128x128 block scales) and per-token-group fp8
    activations (W8A8); attention, norms and lm_head stay bf16.
    w8 / w4: int8 per-channel / int4 group-128 weight-only quantisation (dequantised, so exact
    numerics without special kernels); everything else bf16.
    yarn: bf16 with static YaRN rope scaling (factor 4, original 32768), as a server might enable
    for long contexts; Qwen warns it affects shorter inputs."""

    def __init__(self, model_dir, batch_tokens: int, compile: bool = True, variant: str = "bf16"):
        self.tok = AutoTokenizer.from_pretrained(model_dir, padding_side="left")
        kwargs = dict(dtype=torch.float16 if variant == "fp16" else torch.bfloat16, attn_implementation="sdpa")
        if variant == "fp8":
            from transformers import FineGrainedFP8Config
            kwargs.update(quantization_config=FineGrainedFP8Config(), device_map="cuda")
        elif variant in ("fp8-kv", "fp8-attn"):
            from transformers import AttentionInterface, AttentionMaskInterface
            from transformers.integrations.sdpa_attention import sdpa_attention_forward
            from transformers.masking_utils import sdpa_mask

            def attn(module, query, key, value, *args, **kw):
                if variant == "fp8-attn":
                    query = fp8_roundtrip(query)
                return sdpa_attention_forward(module, query, fp8_roundtrip(key), fp8_roundtrip(value), *args, **kw)

            AttentionInterface.register("sdpa_" + variant, attn)
            AttentionMaskInterface.register("sdpa_" + variant, sdpa_mask)  # else the causal mask is not built
            kwargs["attn_implementation"] = "sdpa_" + variant
        elif variant == "yarn":
            from transformers import AutoConfig
            cfg = AutoConfig.from_pretrained(model_dir)
            yarn = {"rope_type": "yarn", "factor": 4.0, "original_max_position_embeddings": 32768}
            if getattr(cfg, "rope_parameters", None) is not None:  # transformers >= 5
                cfg.rope_parameters = {**cfg.rope_parameters, **yarn}
            else:
                cfg.rope_scaling = yarn
            kwargs["config"] = cfg
        self.model = AutoModelForCausalLM.from_pretrained(model_dir, **kwargs).cuda().eval()
        if variant in ("w8", "w4"):
            fake_quant_weights(self.model, bits=8 if variant == "w8" else 4, group=None if variant == "w8" else 128)
        if compile and variant != "fp8":  # fuses memory-bound elementwise ops: ~1.8x short, ~1.3x at 32K
            self.model = torch.compile(self.model, dynamic=True)
        self.prefix = self.tok.encode(PREFIX, add_special_tokens=False)
        self.suffix = self.tok.encode(SUFFIX, add_special_tokens=False)
        self.yes, self.no = self.tok.convert_tokens_to_ids("yes"), self.tok.convert_tokens_to_ids("no")
        self.batch_tokens = batch_tokens

    def encode(self, query: str, docs: list[str]) -> list[list[int]]:
        texts = [f"<Instruct>: {INSTRUCTION}\n<Query>: {query}\n<Document>: {d}" for d in docs]
        return [self.prefix + ids + self.suffix
                for ids in self.tok(texts, add_special_tokens=False)["input_ids"]]

    @torch.inference_mode()
    def score_ids(self, ids: list[list[int]]) -> list[float]:
        """Score pre-encoded pairs; batches by padded token count, longest first."""
        order = sorted(range(len(ids)), key=lambda i: -len(ids[i]))
        scores = [0.0] * len(ids)
        i = 0
        while i < len(order):
            longest = len(ids[order[i]])
            n = max(1, min(len(order) - i, self.batch_tokens // longest))
            batch = [ids[j] for j in order[i:i + n]]
            pad = [[self.tok.pad_token_id] * (longest - len(b)) + b for b in batch]
            input_ids = torch.tensor(pad, device="cuda")
            kwargs = {}
            if n > 1:  # a single unpadded sequence needs no mask (and gets the fast attention kernel)
                kwargs["attention_mask"] = torch.tensor(
                    [[0] * (longest - len(b)) + [1] * len(b) for b in batch], device="cuda")
            logits = self.model(input_ids=input_ids, logits_to_keep=1, **kwargs).logits[:, -1, :]
            probs = torch.softmax(logits[:, [self.no, self.yes]].float(), dim=-1)[:, 1].tolist()
            for j, p in zip(order[i:i + n], probs):
                scores[j] = p
            i += n
        return scores


def metrics(scores: list[float], relevant: list[int]) -> tuple[float, float]:
    """nDCG@10 and reciprocal rank of the first relevant document."""
    ranked = sorted(range(len(scores)), key=lambda i: -scores[i])
    rel = set(relevant)
    dcg = sum(1 / math.log2(r + 2) for r, i in enumerate(ranked[:10]) if i in rel)
    idcg = sum(1 / math.log2(r + 2) for r in range(min(len(rel), 10)))
    rr = next((1 / (r + 1) for r, i in enumerate(ranked) if i in rel), 0.0)
    return dcg / idcg if idcg else 0.0, rr


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default="0.6b", choices=["0.6b", "4b", "8b"])
    ap.add_argument("--variant", default="bf16", choices=list(VARIANTS))
    ap.add_argument("--sets", nargs="*", help="only these sets (default: every data/prepared/*.jsonl)")
    ap.add_argument("--batch-tokens", type=int, default=65536, help="padded tokens per forward pass")
    ap.add_argument("--no-compile", action="store_true", help="skip torch.compile (slower, no warm-up)")
    args = ap.parse_args()

    model_dir = download.ensure_model(args.model)
    reranker = Reranker(model_dir, args.batch_tokens, compile=not args.no_compile, variant=args.variant)
    out_dir = OUT / f"qwen3-reranker-{args.model}{VARIANTS[args.variant]}"
    out_dir.mkdir(parents=True, exist_ok=True)

    summary = {}
    for path in sorted(PREPARED.glob("*.jsonl")):
        set_name = path.stem
        if args.sets and set_name not in args.sets:
            continue
        out, nd, rr, pairs, tokens, t0 = out_dir / path.name, [], [], 0, 0, time.time()
        with open(path) as f, open(out, "w") as g:
            for line in f:
                req = json.loads(line)
                ids = reranker.encode(req["query"], req["documents"])
                scores = reranker.score_ids(ids)
                g.write(json.dumps({"id": req["id"], "scores": [round(s, 6) for s in scores]}) + "\n")
                n, r = metrics(scores, req["relevant"])
                nd.append(n)
                rr.append(r)
                pairs += len(ids)
                tokens += sum(map(len, ids))
        dt = time.time() - t0
        summary[set_name] = {"requests": len(nd), "ndcg@10": sum(nd) / len(nd), "mrr": sum(rr) / len(rr)}
        print(f"{set_name:24} {len(nd):5} req  nDCG@10={summary[set_name]['ndcg@10']:.3f}  "
              f"MRR={summary[set_name]['mrr']:.3f}  {pairs / dt:6.1f} pairs/s  {tokens / dt / 1e3:7.1f}K tok/s")

    reference_metrics(out_dir, PREPARED)  # from every set file on disk, so partial runs stay consistent
    print(f"wrote {out_dir.relative_to(ROOT)}/ — review with `git diff --stat reference/` and commit it")


if __name__ == "__main__":
    main()
