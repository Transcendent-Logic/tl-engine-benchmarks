# TL Engine · Qwen3-Reranker-8B · batch transform, MaxConcurrentTransforms 4 · 2026-11-22 21:14 UTC

One batch transform job. It feeds the tables in the [repository README](../../README.md), section "Batch transform jobs"; only means over three runs are published there. This folder holds this job's own results.

| | |
|---|---|
| Configuration | TL Engine: our inference engine for the NVIDIA L4 (proprietary): our image and `model.tar.gz`, with no environment ([model-container.json](model-container.json)) |
| Model | Hugging Face `Qwen/Qwen3-Reranker-8B` revision `77d193c791ed757ca307ee72715aa132723da912`, in the engine's own file format, packed as `model.tar.gz` |
| Job | 1 × ml.g6.xlarge (one NVIDIA L4), eu-west-3 (Paris), network isolation on, SageMaker's default batch host; `BatchStrategy` SingleRecord, `SplitType` Line, `MaxConcurrentTransforms` 4 ([transform-input.json](transform-input.json)) |
| Input | `short20-8b-900`: 900 requests, one per line, SHA-256 `bbd98c8e5655b61e34624edbf8382eed9a86e0e1baddae70bad1f1ec4613c37e`, from [../../scripts/batch/build_input.py](../../scripts/batch/build_input.py) with seed 20261119 |
| Time (UTC) | created 2026-11-22T21:14:34Z, started 2026-11-22T21:21:33Z, ended 2026-11-22T21:38:58Z, Completed |

## Results

| Measure | Value |
|---|---|
| Requests answered | 900 of 900; 0 not a ranking |
| Tokens (sum of `usage.total_tokens`) | 7,713,006 |
| Job, start to end (billed) | 1,044.6 s |
| Start-up, job start to first request | 178.4 s |
| Processing, first to last request | 864.2 s |
| Tokens a second, processing | 8,925 |
| Tokens a second, whole job | 7,384 |
| nDCG@10 per set | beir-arguana 0.691, beir-fiqa 0.782, beir-scifact 0.847 |

## Files

- `run.json`: this page as data; [`scripts/tables.py`](../../scripts/tables.py) reads it, with `batch.json`.
- `batch.json`: the measures, by [`scripts/batch/analyze.py`](../../scripts/batch/analyze.py) from the files below.
- `per-request.jsonl`: per request, in input order: set, id, tokens, every document's score, top document, nDCG@10. The job's own output also echoes every document's text and is not published.
- `job.json`, `transform-input.json`, `model-container.json`: the job's description after it ended, the `CreateTransformJob` request and the model's container. Our AWS account ID, bucket and registry are replaced by placeholders, and our internal name for the engine by `tl`.
- `logs/data-log.jsonl`: SageMaker's data log. `logs/container.jsonl`: the container log's access lines only (`POST /invocations`), with their CloudWatch timestamps; the rest of the log describes the proprietary engine and is not published.
