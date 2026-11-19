# vLLM 16-bit · Qwen3-Reranker-0.6B · batch transform, MaxConcurrentTransforms 1 · 2026-11-19 11:14 UTC

One batch transform job. It feeds the tables in the [repository README](../../README.md), section "Batch transform jobs"; only means over three runs are published there. This folder holds this job's own results.

| | |
|---|---|
| Configuration | vLLM 16-bit: AWS's SageMaker vLLM 0.31.0 container, 16-bit, with the endpoint runs' environment ([model-container.json](model-container.json)) |
| Model | Hugging Face `Qwen/Qwen3-Reranker-0.6B` revision `e61197ed45024b0ed8a2d74b80b4d909f1255473`, packed as `model.tar.gz` ([../../scripts/batch/pack_vllm_weights.sh](../../scripts/batch/pack_vllm_weights.sh)) |
| Job | 1 × ml.g6.xlarge (one NVIDIA L4), eu-west-3 (Paris), network isolation on, SageMaker's default batch host; `BatchStrategy` SingleRecord, `SplitType` Line, `MaxConcurrentTransforms` not set (SageMaker's data log: `MaxConcurrentTransforms=1`) ([transform-input.json](transform-input.json)) |
| Input | `short20-06b-7200`: 7,200 requests, one per line, SHA-256 `2b09d94f3b022bc3ad46124015ca0012cbc8b2bfe02a3257ab67df7bab1ced77`, from [../../scripts/batch/build_input.py](../../scripts/batch/build_input.py) with seed 20261119 |
| Time (UTC) | created 2026-11-19T11:14:53Z, started 2026-11-19T11:19:35Z, ended 2026-11-19T11:45:09Z, Completed |

## Results

| Measure | Value |
|---|---|
| Requests answered | 7,200 of 7,200; 0 not a ranking |
| Tokens (sum of `usage.total_tokens`) | 61,704,368 |
| Job, start to end (billed) | 1,534.9 s |
| Start-up, job start to first request | 320.8 s |
| Processing, first to last request | 1,212.7 s |
| Tokens a second, processing | 50,884 |
| Tokens a second, whole job | 40,201 |
| nDCG@10 per set | beir-arguana 0.577, beir-fiqa 0.677, beir-scifact 0.825 |

## Files

- `run.json`: this page as data; [`scripts/tables.py`](../../scripts/tables.py) reads it, with `batch.json`.
- `batch.json`: the measures, by [`scripts/batch/analyze.py`](../../scripts/batch/analyze.py) from the files below.
- `per-request.jsonl`: per request, in input order: set, id, tokens, every document's score, top document, nDCG@10. The job's own output also echoes every document's text and is not published.
- `job.json`, `transform-input.json`, `model-container.json`: the job's description after it ended, the `CreateTransformJob` request and the model's container. Our AWS account ID, bucket and registry are replaced by placeholders.
- `logs/data-log.jsonl`: SageMaker's data log. `logs/container.jsonl`: the container log, one JSON line per CloudWatch event with its timestamp.
