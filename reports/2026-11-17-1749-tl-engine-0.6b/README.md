# TL Engine · Qwen3-Reranker-0.6B · 2026-11-17 17:49 UTC

One run of the benchmark. It feeds these tables in the [repository README](../../README.md): peak throughput. Only three-run means are published there; this folder holds this run's own results.

| | |
|---|---|
| Configuration | TL Engine: our inference engine for the NVIDIA L4 (proprietary, not in this repository) |
| Model | Hugging Face `Qwen/Qwen3-Reranker-0.6B` revision `e61197ed45024b0ed8a2d74b80b4d909f1255473`, packed as `model.tar.gz` (checked file by file against that revision on 2026-11-17). |
| Image | Ours, in our private registry (digest `sha256:8a7ad8697abaec24f176435b0d3131aca184c2b76a7d94773a3de0bc2747b9c5`). The listing's image is this one plus an OS update and `STEP_TOKENS=4096` set in the image (see the repository README). |
| Container environment | `COMPILE=1`, `VLLM_DISABLE_COMPILE_CACHE=1`, `VLLM_USE_AOT_COMPILE=0`, `STEP_TOKENS=4096`, `SM_VLLM_MAX_NUM_SEQS=64`, `SM_VLLM_MAX_MODEL_LEN=33000`, `SM_VLLM_ASYNC_SCHEDULING=` ([endpoint/container.json](endpoint/container.json)) |
| Endpoint | 1 × ml.g6.xlarge (one NVIDIA L4), eu-west-3 (Paris), network isolation on, SageMaker's default host image, start-up and download timeouts 1,800 s ([endpoint/variants.json](endpoint/variants.json)) |
| Client | c7i.xlarge in eu-west-3, second client (runs of 2026-11-17 and 18), Amazon Linux 2023; the hammer at `195a09c` ([../../hammer/](../../hammer/)) |
| Time (UTC) | 2026-11-17T17:49:16Z to 2026-11-17T18:39:24Z |

## Modes

| Mode | Arguments | Start (UTC) | End (UTC) | Exit status | Requests | Failed |
|---|---|---|---|---|---|---|
| [`normal`](normal.md) | `--timeout 75` | 17:49:17 | 17:54:19 | 0 | 436 | 0 |
| [`hammer32k`](hammer32k.md) | `--timeout 75` | 17:54:20 | 18:39:23 | 0 | 2,742 | 0 |

Exit status 1 means more than 5% of a mode's requests failed. Mode arguments are as the client's [status](status) file records them (`(none)`: the hammer's defaults, with its 60-second request timeout).

## Notes

- The container log is not published: it describes the proprietary engine's internals.

## Files

- `<mode>.md`: the hammer's report of that mode; `<mode>.requests.jsonl`: one record per request (send time, latency, scores, error); `<mode>.png`: its charts.
- `status`: the client's log of the run: modes with their arguments and times, and single probe requests between modes, which no table uses.
- `client-vmstat.log`: the client's CPU and memory, every 10 seconds.
- `endpoint/`: the container definition and production variant the endpoint was created with, and the creation log with two sanity requests ([`scripts/req_short.json`](../../scripts/req_short.json), [`req_long.json`](../../scripts/req_long.json)). Our AWS account IDs, bucket and registry names are replaced by placeholders.
- `run.json`: this page as data; [`scripts/tables.py`](../../scripts/tables.py) reads it.
