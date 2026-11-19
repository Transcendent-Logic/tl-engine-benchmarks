# vLLM 16-bit · Qwen3-Reranker-8B · batch transform, MaxConcurrentTransforms 4 · 2026-11-19 15:50 UTC

One batch transform job. It feeds the tables in the [repository README](../../README.md), section "Batch transform jobs"; only means over three runs are published there. This folder holds this job's own results.

| | |
|---|---|
| Configuration | vLLM 16-bit: AWS's SageMaker vLLM 0.31.0 container, 16-bit, with the endpoint runs' environment plus `SM_VLLM_GPU_MEMORY_UTILIZATION=0.925` (see Notes) ([model-container.json](model-container.json)) |
| Model | Hugging Face `Qwen/Qwen3-Reranker-8B` revision `77d193c791ed757ca307ee72715aa132723da912`, packed as `model.tar.gz` ([../../scripts/batch/pack_vllm_weights.sh](../../scripts/batch/pack_vllm_weights.sh)) |
| Job | 1 × ml.g6.xlarge (one NVIDIA L4), eu-west-3 (Paris), network isolation on, SageMaker's default batch host; `BatchStrategy` SingleRecord, `SplitType` Line, `MaxConcurrentTransforms` 4 ([transform-input.json](transform-input.json)) |
| Input | `short20-8b-900`: 900 requests, one per line, SHA-256 `bbd98c8e5655b61e34624edbf8382eed9a86e0e1baddae70bad1f1ec4613c37e`, from [../../scripts/batch/build_input.py](../../scripts/batch/build_input.py) with seed 20261119 |
| Time (UTC) | created 2026-11-19T15:50:35Z, started 2026-11-19T15:55:30Z, ended 2026-11-19T16:30:38Z, Completed |

## Results

| Measure | Value |
|---|---|
| Requests answered | 900 of 900; 0 not a ranking |
| Tokens (sum of `usage.total_tokens`) | 7,713,006 |
| Job, start to end (billed) | 2,108.0 s |
| Start-up, job start to first request | 626.1 s |
| Processing, first to last request | 1,480.5 s |
| Tokens a second, processing | 5,210 |
| Tokens a second, whole job | 3,659 |
| nDCG@10 per set | beir-arguana 0.697, beir-fiqa 0.785, beir-scifact 0.848 |

## Notes

- vLLM 8B runs with `SM_VLLM_GPU_MEMORY_UTILIZATION=0.925` instead of vLLM's default 0.92, the one setting that differs from the endpoint runs: on the batch host's NVIDIA driver 535 the L4 reports 21.96 GiB (22.03 GiB on the endpoints' driver-580 host image), and at 0.92 every start found 5.45 GiB of KV cache against the 5.49 GiB that 40,000 tokens need. 0.925 gives about 5.57 GiB, close to the endpoints' 5.52 GiB: more memory for vLLM, not less. See the repository README, "Batch transform jobs".
- The container log has 895 `POST /invocations` lines for 900 requests; the output has all 900 responses, none an error, with their tokens counted. The 5 missing access-log lines fall inside the run, not at its ends: the first and last request lines (16:05:56 and 16:30:37 UTC) agree with vLLM's own throughput lines (non-zero from 16:06:04 to 16:30:45), so the processing window is unaffected. Cause not known; the only run of the series with fewer log lines than responses.

## Files

- `run.json`: this page as data; [`scripts/tables.py`](../../scripts/tables.py) reads it, with `batch.json`.
- `batch.json`: the measures, by [`scripts/batch/analyze.py`](../../scripts/batch/analyze.py) from the files below.
- `per-request.jsonl`: per request, in input order: set, id, tokens, every document's score, top document, nDCG@10. The job's own output also echoes every document's text and is not published.
- `job.json`, `transform-input.json`, `model-container.json`: the job's description after it ended, the `CreateTransformJob` request and the model's container. Our AWS account ID, bucket and registry are replaced by placeholders.
- `logs/data-log.jsonl`: SageMaker's data log. `logs/container.jsonl`: the container log, one JSON line per CloudWatch event with its timestamp.
