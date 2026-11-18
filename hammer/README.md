# The hammer

The load and quality client behind every number in this repository. It sends prepared reranking requests to an endpoint and records each answer, its latency and its scores.

Written by Renaldas Zioma (`rz`); support for SageMaker endpoints (AWS-signed requests, per-request log) was added in its last commit. This folder is a cleaned snapshot of the hammer's private repository at that commit, `195a09c` (2026-11-05), which every run in [`../reports/`](../reports/) used. [CHANGES.md](CHANGES.md) lists every difference from that commit; none changes a request, the load pattern or a measurement.

## Prepare the request sets

1. Install [uv](https://docs.astral.sh/uv/).
2. `uv run scripts/prepare.py` downloads the pinned sources (about 130 MB) from exact Hugging Face commits, checks their SHA-256, builds the request sets into `data/prepared/` (about 176 MB) and checks those against [`checksums/prepared.sha256`](checksums/prepared.sha256). A mismatch stops the script, so a clean checkout reproduces the same requests byte for byte.

`data/` is not in the repository: it holds the datasets' text, which their authors publish under their own terms. `reference/qwen3-reranker-0.6b/` (request ids and scores only, no dataset text) is committed: the vanilla 0.6B model's scores from `scripts/reference.py`, which `quality` compares with.

### Pinned sources ([`scripts/sources.py`](scripts/sources.py))

| Source | Commit | Used for |
|---|---|---|
| `BeIR/scifact`, `BeIR/scifact-qrels` | `b3b53356`, `2938d17d` | `beir-scifact` |
| `BeIR/fiqa`, `BeIR/fiqa-qrels` | `979c07a7`, `252958f2` | `beir-fiqa` |
| `BeIR/arguana`, `BeIR/arguana-qrels` | `9bcf8fc0`, `ae5468c6` | `beir-arguana` |
| `dwzhu/LongEmbed` (needle, 2wikimqa, summ_screen_fd, qmsum) | `10039a58` | `ladder*`, `natural-*` |
| `Qwen/Qwen3-Reranker-0.6B` (tokenizer only) | `e61197ed` | token counts |

### The request sets (`data/prepared/`)

| Set | Requests | Documents per request | Tokens per request | What it is |
|---|---|---|---|---|
| `beir-scifact` | 300 | 20 | about 8.9K | Scientific claims against abstracts |
| `beir-fiqa` | 300 | 20 | about 5.5K | Finance questions against forum answers |
| `beir-arguana` | 300 | 20 | about 11.9K | Arguments against counter-arguments |
| `ladder-{256,…,32768}` | 50 each | 100 down to 1 | about 28–32K | Documents of one length, packed to about 32K tokens |
| `ladder1-{256,…,32768}` | 50 each | 1 | 0.3K up to 32K | One document per request |
| `natural-{2wikimqa,summ_screen_fd,qmsum}` | 300 each | 1 to 5 | about 31K | Real long documents |

The `beir-*` candidates are every labelled-relevant document plus BM25 hard negatives from the same corpus. The `ladder*` sets come from LongEmbed's *needle* task: one essay text at eight lengths, a sentence planted in one document, and a question only that sentence answers. Documents are shuffled per request with a fixed seed. Requests are budgeted with a character-based token estimate (`*_api_tokens`, `est_api_tokens`); the real Qwen token counts are kept as `query_tokens` and `doc_tokens`.

## Run

```bash
export RERANKER_API_URL=https://runtime.sagemaker.eu-west-3.amazonaws.com/endpoints/<endpoint>/invocations
export RERANKER_MODEL=qwen3-reranker-4b RERANKER_REFERENCE=qwen3-reranker-4b   # 4B and 8B only; the 0.6B uses the defaults
uv run --with botocore scripts/hammer.py quality --timeout 75 --out <folder> --no-docs
```

SageMaker endpoints get AWS-signed requests with credentials from the usual AWS chain. Any other URL gets plain requests with the same body: `{"model", "query", "documents"}`, answered with `{"results": [{"index", "relevance_score"}], "usage": {"total_tokens"}}`.

| Mode | Load | What it measures |
|---|---|---|
| `quality` | Up to 300 requests per set (100 per `natural-*` set) at 4 in flight (`--concurrency 2` for the 4B and 8B) | nDCG@10 and MRR against the labels, and every score per document |
| `meticulous` | One request at a time | Latency against document length (one document, 256 to 32K tokens), number of documents, cold against cached, then `short20` at 1 to 32 in flight |
| `speed` | Closed loop, 25 s per cell | Tokens a second for five request shapes at 1, 4 and 16 in flight |
| `normal` | Open loop, Poisson arrivals (`--rate`, `--duration`) | Latency percentiles of mixed traffic: 60% `short20`, 10% each `many100`, `mid1k`, `mid4k`, 5% each `long8k`, `long32k` |
| `hammer32k` | Closed loop, 2 in flight, 45 minutes | Tokens a second and latency on about 32K-token requests |
| `smoke`, `burst` | | Sanity checks and bursts of simultaneous requests; not used in this repository's tables |

Request shapes in `speed`: `short20` (the three BEIR sets, 20 documents), `many100` (100 documents of 256 tokens), `long8k` (one 8K document), `pack32k` (about 30K tokens in 3 to 55 documents), `long32k` (about 31K tokens in 1 to 5 documents). Speed modes add a random nonce to every query so that no answer comes from a prefix cache. "API tok/s" is the server's own token count (`usage.total_tokens`) of the answered requests over wall time.

Each mode writes `<mode>.md` (tables), `<mode>.requests.jsonl` (one record per request, written as it finishes), `<mode>.json` (the same records) and PNG charts. Exit status 1 means the mode's checks failed: more than 5% of requests failed (`--max-error-rate`), or `quality` fell more than 0.05 nDCG@10 below the reference (`--max-ndcg-drop`).

## Reference answers

`uv run --extra reference scripts/reference.py` scores every request with the pinned vanilla Qwen3-Reranker on a local NVIDIA GPU, using the prompt from the model card, and writes `reference/<model>/<set>.jsonl`. The runs in this repository compare endpoints with each other, not with these files, so the tables do not depend on them.
