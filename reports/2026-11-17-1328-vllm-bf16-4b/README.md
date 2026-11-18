# vLLM 16-bit · Qwen3-Reranker-4B · 2026-11-17 13:28 UTC

One run of the benchmark. It feeds these tables in the [repository README](../../README.md): peak throughput, one request at a time. Only three-run means are published there; this folder holds this run's own results.

| | |
|---|---|
| Configuration | vLLM 16-bit: AWS's SageMaker vLLM 0.31.0 container, unmodified, 16-bit (BF16) |
| Model | Hugging Face `Qwen/Qwen3-Reranker-4B` revision `22e683669bc0f0bd69640a1354a6d0aebcfeede5` (checked file by file against that revision), as an uncompressed folder with [`qwen3_reranker.jinja`](../../scripts/qwen3_reranker.jinja) added. |
| Image | `763104351884.dkr.ecr.eu-west-3.amazonaws.com/vllm:0.31.0-gpu-py312-cu130-ubuntu24.04-sagemaker` (digest `sha256:da4fd31c78d04b5ec659c7fed354dd33a28b83d88cf74a6a0539630a92a93690`, AWS's) |
| Container environment | `SM_VLLM_MODEL=/opt/ml/model`, `SM_VLLM_RUNNER=pooling`, `SM_VLLM_DTYPE=bfloat16`, `SM_VLLM_SERVED_MODEL_NAME=qwen3-reranker-4b`, `SM_VLLM_CHAT_TEMPLATE=/opt/ml/model/qwen3_reranker.jinja`, `SM_VLLM_HF_OVERRIDES={"architectures":["Qwen3ForSequenceClassification"],"classifier_from_token":["no","yes"],"is_original_qwen3_reranker":true}`, `HF_HUB_OFFLINE=1` ([endpoint/container.json](endpoint/container.json)) |
| Endpoint | 1 × ml.g6.xlarge (one NVIDIA L4), eu-west-3 (Paris), network isolation on, host image `al2023-ami-sagemaker-inference-gpu-4-1`, start-up and download timeouts 1,800 s ([endpoint/variants.json](endpoint/variants.json)) |
| Client | c7i.xlarge in eu-west-3, second client (runs of 2026-11-17 and 18), Amazon Linux 2023; the hammer at `195a09c` ([../../hammer/](../../hammer/)) |
| Time (UTC) | 2026-11-17T13:28:10Z to 2026-11-17T14:42:18Z |

## Modes

| Mode | Arguments | Start (UTC) | End (UTC) | Exit status | Requests | Failed |
|---|---|---|---|---|---|---|
| [`normal`](normal.md) | `--timeout 75 --rate 0.25 --duration 900` | 13:28:15 | 13:43:34 | 0 | 216 | 0 |
| [`speed`](speed.md) | `--timeout 75` | 13:43:36 | 13:54:02 | 0 | 306 | 7 |
| [`hammer32k`](hammer32k.md) | `--timeout 75` | 13:57:05 | 14:42:16 | 0 | 419 | 0 |

Exit status 1 means more than 5% of a mode's requests failed. Mode arguments are as the client's [status](status) file records them (`(none)`: the hammer's defaults, with its 60-second request timeout).

Failed requests (every one is in the mode's `requests.jsonl`, with SageMaker's response):

- `speed`: 7 × SageMaker ended the invocation at its 60-second limit (HTTP 424).

## Files

- `<mode>.md`: the hammer's report of that mode; `<mode>.requests.jsonl`: one record per request (send time, latency, scores, error); `<mode>.png`: its charts.
- `status`: the client's log of the run: modes with their arguments and times, and single probe requests between modes, which no table uses.
- `client-vmstat.log`: the client's CPU and memory, every 10 seconds.
- `container.log`: the endpoint's log, from CloudWatch.
- `endpoint/`: the container definition and production variant the endpoint was created with, and the creation log with two sanity requests ([`scripts/req_short.json`](../../scripts/req_short.json), [`req_long.json`](../../scripts/req_long.json)). Our AWS account IDs, bucket and registry names are replaced by placeholders.
- `run.json`: this page as data; [`scripts/tables.py`](../../scripts/tables.py) reads it.
