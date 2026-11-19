# vLLM 16-bit · Qwen3-Reranker-4B · batch transform, MaxConcurrentTransforms 1 · 2026-11-19 12:36 UTC

One batch transform job. It feeds the tables in the [repository README](../../README.md), section "Batch transform jobs"; only means over three runs are published there. This folder holds this job's own results.

| | |
|---|---|
| Configuration | vLLM 16-bit: AWS's SageMaker vLLM 0.31.0 container, 16-bit, with the endpoint runs' environment ([model-container.json](model-container.json)) |
| Model | Hugging Face `Qwen/Qwen3-Reranker-4B` revision `22e683669bc0f0bd69640a1354a6d0aebcfeede5`, packed as `model.tar.gz` ([../../scripts/batch/pack_vllm_weights.sh](../../scripts/batch/pack_vllm_weights.sh)) |
| Job | 1 × ml.g6.xlarge (one NVIDIA L4), eu-west-3 (Paris), network isolation on, SageMaker's default batch host; `BatchStrategy` SingleRecord, `SplitType` Line, `MaxConcurrentTransforms` not set (SageMaker's data log: `MaxConcurrentTransforms=1`) ([transform-input.json](transform-input.json)) |
| Input | `short20-4b-1800`: 1,800 requests, one per line, SHA-256 `745a5252e388101c6ba1ad5e1c7fd9ba240c0282641c9dff29047f32e66f2065`, from [../../scripts/batch/build_input.py](../../scripts/batch/build_input.py) with seed 20261119 |
| Time (UTC) | created 2026-11-19T12:36:32Z, started 2026-11-19T12:41:25Z, ended 2026-11-19T13:15:46Z, Completed |

## Results

| Measure | Value |
|---|---|
| Requests answered | 1,800 of 1,800; 0 not a ranking |
| Tokens (sum of `usage.total_tokens`) | 15,426,632 |
| Job, start to end (billed) | 2,061.2 s |
| Start-up, job start to first request | 413.1 s |
| Processing, first to last request | 1,646.6 s |
| Tokens a second, processing | 9,369 |
| Tokens a second, whole job | 7,484 |
| nDCG@10 per set | beir-arguana 0.594, beir-fiqa 0.773, beir-scifact 0.838 |

## Files

- `run.json`: this page as data; [`scripts/tables.py`](../../scripts/tables.py) reads it, with `batch.json`.
- `batch.json`: the measures, by [`scripts/batch/analyze.py`](../../scripts/batch/analyze.py) from the files below.
- `per-request.jsonl`: per request, in input order: set, id, tokens, every document's score, top document, nDCG@10. The job's own output also echoes every document's text and is not published.
- `job.json`, `transform-input.json`, `model-container.json`: the job's description after it ended, the `CreateTransformJob` request and the model's container. Our AWS account ID, bucket and registry are replaced by placeholders.
- `logs/data-log.jsonl`: SageMaker's data log. `logs/container.jsonl`: the container log, one JSON line per CloudWatch event with its timestamp.
