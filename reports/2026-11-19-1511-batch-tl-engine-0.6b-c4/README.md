# TL Engine · Qwen3-Reranker-0.6B · batch transform, MaxConcurrentTransforms 4 · 2026-11-19 15:11 UTC

One batch transform job. It feeds the tables in the [repository README](../../README.md), section "Batch transform jobs"; only means over three runs are published there. This folder holds this job's own results.

| | |
|---|---|
| Configuration | TL Engine: our inference engine for the NVIDIA L4 (proprietary), from the AWS Marketplace listing's model package with no environment ([model-container.json](model-container.json)) |
| Model | Hugging Face `Qwen/Qwen3-Reranker-0.6B` revision `e61197ed45024b0ed8a2d74b80b4d909f1255473`, inside the model package |
| Job | 1 × ml.g6.xlarge (one NVIDIA L4), eu-west-3 (Paris), network isolation on, SageMaker's default batch host; `BatchStrategy` SingleRecord, `SplitType` Line, `MaxConcurrentTransforms` 4 ([transform-input.json](transform-input.json)) |
| Input | `short20-06b-7200`: 7,200 requests, one per line, SHA-256 `2b09d94f3b022bc3ad46124015ca0012cbc8b2bfe02a3257ab67df7bab1ced77`, from [../../scripts/batch/build_input.py](../../scripts/batch/build_input.py) with seed 20261119 |
| Time (UTC) | created 2026-11-19T15:11:26Z, started 2026-11-19T15:18:32Z, ended 2026-11-19T15:30:43Z, Completed |

## Results

| Measure | Value |
|---|---|
| Requests answered | 7,200 of 7,200; 0 not a ranking |
| Tokens (sum of `usage.total_tokens`) | 61,704,368 |
| Job, start to end (billed) | 731.3 s |
| Start-up, job start to first request | 157.3 s |
| Processing, first to last request | 573.4 s |
| Tokens a second, processing | 107,611 |
| Tokens a second, whole job | 84,373 |
| nDCG@10 per set | beir-arguana 0.575, beir-fiqa 0.673, beir-scifact 0.824 |

## Files

- `run.json`: this page as data; [`scripts/tables.py`](../../scripts/tables.py) reads it, with `batch.json`.
- `batch.json`: the measures, by [`scripts/batch/analyze.py`](../../scripts/batch/analyze.py) from the files below.
- `per-request.jsonl`: per request, in input order: set, id, tokens, every document's score, top document, nDCG@10. The job's own output also echoes every document's text and is not published.
- `job.json`, `transform-input.json`, `model-container.json`: the job's description after it ended, the `CreateTransformJob` request and the model's container. Our AWS account ID, bucket and registry are replaced by placeholders.
- `logs/data-log.jsonl`: SageMaker's data log. `logs/container.jsonl`: the container log's access lines only (`POST /invocations`), with their CloudWatch timestamps; the rest of the log describes the proprietary engine and is not published.
