# vLLM fp8 · Qwen3-Reranker-4B · 2026-11-13 20:10 UTC

One run of the benchmark. It feeds these tables in the [repository README](../../README.md): quality. Only three-run means are published there; this folder holds this run's own results.

| | |
|---|---|
| Configuration | vLLM fp8: AWS's SageMaker vLLM 0.31.0 container, unmodified, with vLLM's online fp8 quantization |
| Model | AWS JumpStart's copy of Qwen3-Reranker-4B (`inference-prepack/v1.0.0`) with `qwen3_reranker.jinja` added; not compared file by file with a Hugging Face revision. |
| Image | `763104351884.dkr.ecr.eu-west-3.amazonaws.com/vllm:0.31.0-gpu-py312-cu130-ubuntu24.04-sagemaker` (digest `sha256:da4fd31c78d04b5ec659c7fed354dd33a28b83d88cf74a6a0539630a92a93690`, AWS's) |
| Container environment | `SM_VLLM_MODEL=/opt/ml/model`, `SM_VLLM_RUNNER=pooling`, `SM_VLLM_DTYPE=bfloat16`, `SM_VLLM_SERVED_MODEL_NAME=qwen3-reranker-4b`, `SM_VLLM_CHAT_TEMPLATE=/opt/ml/model/qwen3_reranker.jinja`, `SM_VLLM_HF_OVERRIDES={"architectures":["Qwen3ForSequenceClassification"],"classifier_from_token":["no","yes"],"is_original_qwen3_reranker":true}`, `HF_HUB_OFFLINE=1`, `SM_VLLM_QUANTIZATION=fp8` ([endpoint/container.json](endpoint/container.json)) |
| Endpoint | 1 × ml.g6.xlarge (one NVIDIA L4), eu-west-3 (Paris), network isolation on, host image `al2023-ami-sagemaker-inference-gpu-4-1`, start-up and download timeouts 1,800 s ([endpoint/variants.json](endpoint/variants.json)) |
| Client | c7i.xlarge in eu-west-3, first client (runs of 2026-11-10 to 16); its instance type is from our notes of 2026-11-06, not from the run's files; the hammer at `195a09c` ([../../hammer/](../../hammer/)) |
| Time (UTC) | 2026-11-13T20:10:05Z to 2026-11-13T21:32:00Z |

## Modes

| Mode | Arguments | Start (UTC) | End (UTC) | Exit status | Requests | Failed |
|---|---|---|---|---|---|---|
| [`quality`](quality.md) | `--timeout 75 --concurrency 2` | 20:10:09 | 21:13:52 | 0 | 2,000 | 0 |
| [`meticulous`](meticulous.md) | `--timeout 75` | 21:13:54 | 21:31:58 | 0 | 883 | 0 |

Exit status 1 means more than 5% of a mode's requests failed. Mode arguments are as the client's [status](status) file records them (`(none)`: the hammer's defaults, with its 60-second request timeout).

## Files

- `<mode>.md`: the hammer's report of that mode; `<mode>.requests.jsonl`: one record per request (send time, latency, scores, error); `<mode>.png`: its charts.
- `status`: the client's log of the run: modes with their arguments and times, and single probe requests between modes, which no table uses.
- `client-vmstat.log`: the client's CPU and memory, every 10 seconds.
- `container.log`: the endpoint's log, from CloudWatch.
- `endpoint/`: the container definition and production variant the endpoint was created with, and the creation log with two sanity requests ([`scripts/req_short.json`](../../scripts/req_short.json), [`req_long.json`](../../scripts/req_long.json)). Our AWS account IDs, bucket and registry names are replaced by placeholders.
- `run.json`: this page as data; [`scripts/tables.py`](../../scripts/tables.py) reads it.
