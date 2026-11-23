# TL Engine · Qwen3-Reranker-4B · 2026-11-23 09:07 UTC

One run of the benchmark. It feeds these tables in the [repository README](../../README.md): peak throughput. Only three-run means are published there; this folder holds this run's own results.

| | |
|---|---|
| Configuration | TL Engine: our inference engine for the NVIDIA L4 (proprietary, not in this repository) |
| Model | Hugging Face `Qwen/Qwen3-Reranker-4B` revision `22e683669bc0f0bd69640a1354a6d0aebcfeede5`, in the engine's own file format, packed as `model.tar.gz` (made from the same revision's files, checked file by file against it on 2026-11-17). |
| Image | Ours, in our private registry (digest `sha256:81e43230efce898a28416ffabe09fccbe9f26ac36cc60e7badfa2c4d1b8140bd`). |
| Container environment | None: the image's own settings, as an endpoint from the listing runs ([endpoint/container.json](endpoint/container.json)) |
| Endpoint | 1 × ml.g6.xlarge (one NVIDIA L4), eu-west-3 (Paris), network isolation on, SageMaker's default host image, start-up and download timeouts 1,800 s ([endpoint/variants.json](endpoint/variants.json)) |
| Client | c7i.xlarge in eu-west-3, second client (the one of the runs of 2026-11-17 and 18), Amazon Linux 2023; the hammer at `195a09c` ([../../hammer/](../../hammer/)) |
| Time (UTC) | 2026-11-23T09:07:17Z to 2026-11-23T10:07:49Z |

## Modes

| Mode | Arguments | Start (UTC) | End (UTC) | Exit status | Requests | Failed |
|---|---|---|---|---|---|---|
| [`normal`](normal.md) | `--timeout 75 --rate 0.25 --duration 900` | 09:07:20 | 09:22:38 | 0 | 216 | 0 |
| [`hammer32k`](hammer32k.md) | `--timeout 75` | 09:22:39 | 10:07:48 | 0 | 667 | 0 |

Exit status 1 means more than 5% of a mode's requests failed. Mode arguments are as the client's [status](status) file records them (`(none)`: the hammer's defaults, with its 60-second request timeout).

## Notes

- The container log is not published: it describes the proprietary engine's internals.

## Files

- `<mode>.md`: the hammer's report of that mode; `<mode>.requests.jsonl`: one record per request (send time, latency, scores, error); `<mode>.png`: its charts.
- `status`: the client's log of the run: modes with their arguments and times, and single probe requests between modes, which no table uses.
- `client-vmstat.log`: the client's CPU and memory, every 10 seconds.
- `endpoint/`: the container definition and production variant the endpoint was created with, and the creation log with two sanity requests ([`scripts/req_short.json`](../../scripts/req_short.json), [`req_long.json`](../../scripts/req_long.json)). Our AWS account IDs, bucket and registry names are replaced by placeholders, and our internal name for the engine by `tl`.
- `run.json`: this page as data; [`scripts/tables.py`](../../scripts/tables.py) reads it.
