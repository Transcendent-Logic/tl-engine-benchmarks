# /// script
# requires-python = "==3.13.*"
# dependencies = [
#     "llmcompressor==0.14.0",
#     "compressed-tensors==0.19.0",
#     "torch==2.14.0",
#     "transformers==5.17.0",
#     "accelerate==1.15.0",
#     "datasets==5.0.1",
#     "pyarrow==25.0.1",
# ]
# ///
"""SmoothQuant + int8 W8A8 (per-channel weights, dynamic per-token activations) of a Qwen3-Reranker with llm-compressor, for
AWS's vLLM container: the "vLLM int8" checkpoints of the benchmark. SmoothQuant strength 0.8, then W8A8 on every Linear except
lm_head, 128 calibration samples, max length 1,024, saved compressed (compressed-tensors).

Calibrated on MS MARCO, not on SciFact, FiQA or ArguAna, which are the hammer's quality sets. Calibration pairs: MS MARCO v1.1
validation (microsoft/ms_marco @ a47ee7aa), rows in file order, each query with its first passage marked is_selected, rendered
with the endpoint's own template (MODEL_DIR/qwen3_reranker.jinja).

    hf download microsoft/ms_marco v1.1/validation-00000-of-00001.parquet --repo-type dataset \
        --revision a47ee7aae8d7d466ba15f9f0bfac3b3681087b3a --local-dir msmarco
    uv run w8a8_sq_msmarco.py MODEL_DIR msmarco/v1.1/validation-00000-of-00001.parquet OUT_DIR [N=128] [ALPHA=0.8]

MODEL_DIR is the 16-bit weights folder with qwen3_reranker.jinja (prepare_weights.sh builds one). Needs an NVIDIA GPU: the runs'
checkpoints were made on one NVIDIA L4 (a SageMaker training job on ml.g6.xlarge, 2026-11-13) with these library versions,
which the pins above repeat; the script is the one that job ran, with only this header added.
"""
import json
import shutil
import sys
from pathlib import Path

import pyarrow.parquet as pq
from datasets import Dataset
from llmcompressor import oneshot
from llmcompressor.modifiers.quantization import QuantizationModifier
from llmcompressor.modifiers.smoothquant import SmoothQuantModifier
from transformers import AutoModelForCausalLM, AutoTokenizer

model_dir, parquet, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
n = int(sys.argv[4]) if len(sys.argv) > 4 else 128
alpha = float(sys.argv[5]) if len(sys.argv) > 5 else 0.8
tpl = (model_dir / "qwen3_reranker.jinja").read_text()
pairs = []
for row in pq.read_table(parquet, columns=["query_id", "query", "passages"]).to_pylist():
    p = row["passages"]
    sel = [t for s, t in zip(p["is_selected"], p["passage_text"]) if s == 1]
    if sel:
        pairs.append((row["query_id"], row["query"], sel[0]))
    if len(pairs) == n:
        break
tok = AutoTokenizer.from_pretrained(model_dir)
texts = [tok.apply_chat_template([{"role": "query", "content": q}, {"role": "document", "content": d}], tokenize=False, chat_template=tpl)
         for _, q, d in pairs]
print("example calibration text:\n" + texts[0])
ds = Dataset.from_dict({"text": texts})
model = AutoModelForCausalLM.from_pretrained(model_dir, dtype="bfloat16", device_map="cuda")
oneshot(model=model, dataset=ds, recipe=[SmoothQuantModifier(smoothing_strength=alpha), QuantizationModifier(targets="Linear", scheme="W8A8", ignore=["lm_head"])],
        max_seq_length=1024, num_calibration_samples=len(texts))
model.save_pretrained(out, save_compressed=True)
tok.save_pretrained(out)
shutil.copy(model_dir / "qwen3_reranker.jinja", out / "qwen3_reranker.jinja")
(out / "calibration.json").write_text(json.dumps({"source": "microsoft/ms_marco v1.1 validation @ a47ee7aae8d7d466ba15f9f0bfac3b3681087b3a",
    "samples": len(texts), "alpha": alpha, "max_seq_length": 1024, "query_ids": [q for q, _, _ in pairs]}, indent=1))
print("saved", out, "calibration samples", len(texts))
