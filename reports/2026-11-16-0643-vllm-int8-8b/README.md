# vLLM int8 · Qwen3-Reranker-8B · 2026-11-16 06:43 UTC

One run of the benchmark. It feeds these tables in the [repository README](../../README.md): quality. Only three-run means are published there; this folder holds this run's own results.

| | |
|---|---|
| Configuration | vLLM int8: AWS's SageMaker vLLM 0.31.0 container, unmodified, serving an int8 W8A8 checkpoint |
| Model | An int8 W8A8 SmoothQuant checkpoint (compressed-tensors) built on 2026-11-13 by [`scripts/w8a8_sq_msmarco.py`](../../scripts/w8a8_sq_msmarco.py), calibrated on 128 MS MARCO queries, from the 16-bit weights: Hugging Face `Qwen/Qwen3-Reranker-8B` revision `77d193c791ed757ca307ee72715aa132723da912`. |
| Image | `763104351884.dkr.ecr.eu-west-3.amazonaws.com/vllm:0.31.0-gpu-py312-cu130-ubuntu24.04-sagemaker` (digest `sha256:da4fd31c78d04b5ec659c7fed354dd33a28b83d88cf74a6a0539630a92a93690`, AWS's) |
| Container environment | `SM_VLLM_MODEL=/opt/ml/model`, `SM_VLLM_RUNNER=pooling`, `SM_VLLM_DTYPE=bfloat16`, `SM_VLLM_SERVED_MODEL_NAME=qwen3-reranker-8b`, `SM_VLLM_CHAT_TEMPLATE=/opt/ml/model/qwen3_reranker.jinja`, `SM_VLLM_HF_OVERRIDES={"architectures":["Qwen3ForSequenceClassification"],"classifier_from_token":["no","yes"],"is_original_qwen3_reranker":true}`, `HF_HUB_OFFLINE=1`, `SM_VLLM_MAX_MODEL_LEN=40000` ([endpoint/container.json](endpoint/container.json)) |
| Endpoint | 1 × ml.g6.xlarge (one NVIDIA L4), eu-west-3 (Paris), network isolation on, host image `al2023-ami-sagemaker-inference-gpu-4-1`, start-up and download timeouts 1,800 s ([endpoint/variants.json](endpoint/variants.json)) |
| Client | c7i.xlarge in eu-west-3, first client (runs of 2026-11-10 to 16); its instance type is from our notes of 2026-11-06, not from the run's files; the hammer at `195a09c` ([../../hammer/](../../hammer/)) |
| Time (UTC) | 2026-11-16T06:43:46Z to 2026-11-16T08:38:53Z |

## Modes

| Mode | Arguments | Start (UTC) | End (UTC) | Exit status | Requests | Failed |
|---|---|---|---|---|---|---|
| [`quality`](quality.md) | `--timeout 75 --concurrency 2` | 06:43:52 | 08:14:51 | 0 | 2,000 | 0 |
| [`meticulous`](meticulous.md) | `--timeout 75` | 08:14:53 | 08:38:51 | 0 | 803 | 1 |

Exit status 1 means more than 5% of a mode's requests failed. Mode arguments are as the client's [status](status) file records them (`(none)`: the hammer's defaults, with its 60-second request timeout).

Failed requests (every one is in the mode's `requests.jsonl`, with SageMaker's response):

- `meticulous`: 1 × SageMaker got no answer from the container (HTTP 424, "container 0"), within milliseconds of sending.

## Files

- `<mode>.md`: the hammer's report of that mode; `<mode>.requests.jsonl`: one record per request (send time, latency, scores, error); `<mode>.png`: its charts.
- `status`: the client's log of the run: modes with their arguments and times, and single probe requests between modes, which no table uses.
- `client-vmstat.log`: the client's CPU and memory, every 10 seconds.
- `container.log`: the endpoint's log, from CloudWatch.
- `endpoint/`: the container definition and production variant the endpoint was created with, and the creation log with two sanity requests ([`scripts/req_short.json`](../../scripts/req_short.json), [`req_long.json`](../../scripts/req_long.json)). Our AWS account IDs, bucket and registry names are replaced by placeholders.
- `run.json`: this page as data; [`scripts/tables.py`](../../scripts/tables.py) reads it.
