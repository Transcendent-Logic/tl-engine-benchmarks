# TL Engine benchmarks

The benchmark behind the numbers we publish for TL Engine, including our AWS Marketplace listings: Qwen3-Reranker 0.6B, 4B and 8B served by **TL Engine**, our inference engine for the NVIDIA L4, against the same models served by **vLLM 16-bit**. vLLM fp8 and int8 are in the quality table as well.

This repository holds everything needed to see and repeat it: the load client, every run's raw results, the scripts that created the endpoints and ran the client, and the script that computes the tables below from those results.

- **Same model, same hardware.** Each configuration ran on its own Amazon SageMaker real-time endpoint: one ml.g6.xlarge (one NVIDIA L4, 24 GB) in eu-west-3 (Paris), network isolation on.
- **The baseline is vLLM as AWS ships it.** AWS's SageMaker vLLM 0.31.0 container, unmodified, with vLLM's defaults and only the settings a reranker needs.
- **Three runs of each configuration.** Every number below is the mean of three runs on three separate endpoints, run between 2026-11-10 and 2026-11-18. We publish only these means; each run's own values are in its folder under [`reports/`](reports/), and `python3 scripts/tables.py --runs` prints them next to the means.

## What was compared

| Configuration | Server | Weights | Precision |
|---|---|---|---|
| **vLLM 16-bit** | AWS's SageMaker vLLM 0.31.0 container | Qwen's, unmodified | BF16 |
| **vLLM fp8** | The same container with `SM_VLLM_QUANTIZATION=fp8` | Qwen's, quantized by vLLM when it loads them | fp8 weights and activations (per tensor) |
| **vLLM int8** | The same container | An int8 W8A8 SmoothQuant checkpoint made with llm-compressor ([`scripts/w8a8_sq_msmarco.py`](scripts/w8a8_sq_msmarco.py)) | int8 weights and activations |
| **TL Engine** | Our engine, in the image of our AWS Marketplace listing | Qwen's, unmodified | Computes in 8-bit integers on its own L4 kernels |

The engine itself is proprietary and is not in this repository; you can run it through the AWS Marketplace listing (see [Repeat it](#repeat-it)).

## Results

All numbers are means of three runs. Tokens a second count the server's own token count (`usage.total_tokens`) of the requests it answered, over wall time.

### Peak throughput

Tokens a second for one instance, by request shape: each `speed` cell is 25 seconds of requests at 4 in flight, where both servers reach their peak (16 in flight adds nothing, and at 16 SageMaker's 60-second limit cut off some of vLLM's 4B and 8B requests). `hammer32k` sends 32K-token requests for 45 minutes, 2 in flight.

**0.6B**

<!-- table:throughput-0.6B -->
| Request shape | vLLM 16-bit (tok/s) | TL Engine (tok/s) | TL Engine ÷ vLLM |
|---|---|---|---|
| 20 documents per request (`short20`), 4 in flight | 57,066 | 105,673 | 1.85× |
| 100 documents of 256 tokens (`many100`), 4 in flight | 74,056 | 140,217 | 1.89× |
| One 8K-token document (`long8k`), 4 in flight | 23,116 | 37,899 | 1.64× |
| About 30K tokens in 3 to 55 documents (`pack32k`), 4 in flight | 49,823 | 85,287 | 1.71× |
| About 31K tokens in 1 to 5 documents (`long32k`), 4 in flight | 18,952 | 30,534 | 1.61× |
| 32K-token requests for 45 minutes (`hammer32k`), 2 in flight | 18,596 | 29,791 | 1.60× |
<!-- end -->

**4B**

<!-- table:throughput-4B -->
| Request shape | vLLM 16-bit (tok/s) | TL Engine (tok/s) | TL Engine ÷ vLLM |
|---|---|---|---|
| 20 documents per request (`short20`), 4 in flight | 10,633 | 15,266 | 1.44× |
| 100 documents of 256 tokens (`many100`), 4 in flight | 13,390 | 19,856 | 1.48× |
| One 8K-token document (`long8k`), 4 in flight | 5,202 | 8,019 | 1.54× |
| About 30K tokens in 3 to 55 documents (`pack32k`), 4 in flight | 10,413 | 15,432 | 1.48× |
| About 31K tokens in 1 to 5 documents (`long32k`), 4 in flight | 4,538 | 7,031 | 1.55× |
| 32K-token requests for 45 minutes (`hammer32k`), 2 in flight | 4,569 | 7,020 | 1.54× |
<!-- end -->

**8B**

<!-- table:throughput-8B -->
| Request shape | vLLM 16-bit (tok/s) | TL Engine (tok/s) | TL Engine ÷ vLLM |
|---|---|---|---|
| 20 documents per request (`short20`), 4 in flight | 5,357 | 8,667 | 1.62× |
| 100 documents of 256 tokens (`many100`), 4 in flight | 7,108 | 11,313 | 1.59× |
| One 8K-token document (`long8k`), 4 in flight | 2,980 | 5,057 | 1.70× |
| About 30K tokens in 3 to 55 documents (`pack32k`), 4 in flight | 5,821 | 9,751 | 1.68× |
| About 31K tokens in 1 to 5 documents (`long32k`), 4 in flight | 2,905 | 4,677 | 1.61× |
| 32K-token requests for 45 minutes (`hammer32k`), 2 in flight | 2,819 | 4,635 | 1.64× |
<!-- end -->

### One request at a time

How long a single request takes when it has the endpoint to itself. One 32K-token document: 30 requests sent one after another (`meticulous`). 20 documents (the three BEIR sets, about 5K to 12K tokens a request): 25 seconds of requests one after another (`speed`, `short20 ×1`). Each is given as the median time (the typical request) and the mean time (the average over every answered request).

**0.6B**

<!-- table:single-0.6B -->
| Request, sent alone | vLLM 16-bit (s) | TL Engine (s) | Faster by |
|---|---|---|---|
| One document of 32K tokens (`meticulous`, 30 requests): median time | 2.221 | 1.376 | 1.61× |
| The same: mean time | 2.218 | 1.377 | 1.61× |
| 20 documents per request (`speed` `short20 ×1`, 25 seconds of requests): median time | 0.178 | 0.117 | 1.52× |
| The same: mean time | 0.184 | 0.119 | 1.55× |
<!-- end -->

**4B**

<!-- table:single-4B -->
| Request, sent alone | vLLM 16-bit (s) | TL Engine (s) | Faster by |
|---|---|---|---|
| One document of 32K tokens (`meticulous`, 30 requests): median time | 7.701 | 4.886 | 1.58× |
| The same: mean time | 7.697 | 4.888 | 1.57× |
| 20 documents per request (`speed` `short20 ×1`, 25 seconds of requests): median time | 0.805 | 0.558 | 1.44× |
| The same: mean time | 0.890 | 0.604 | 1.47× |
<!-- end -->

**8B**

<!-- table:single-8B -->
| Request, sent alone | vLLM 16-bit (s) | TL Engine (s) | Faster by |
|---|---|---|---|
| One document of 32K tokens (`meticulous`, 30 requests): median time | 11.100 | 6.731 | 1.65× |
| The same: mean time | 11.063 | 6.732 | 1.64× |
| 20 documents per request (`speed` `short20 ×1`, 25 seconds of requests): median time | 1.565 | 0.959 | 1.63× |
| The same: mean time | 1.678 | 1.051 | 1.60× |
<!-- end -->

### Quality

Ranking quality on three BEIR sets (300 queries each, 20 candidate documents per query: every relevant document plus BM25 hard negatives), and how closely each configuration agrees with vLLM 16-bit.

- **nDCG@10** against the datasets' relevance labels.
- **Agreement with 16-bit:** each run compared with each vLLM 16-bit run, then averaged. It is the mean of two shares: FiQA queries whose top document is the same as 16-bit's, and long-document requests (`ladder1-32768`: 50 single documents of about 32K tokens, each with one planted sentence) whose score is within 0.2 of 16-bit's. For the 16-bit row, each 16-bit run is compared with the other two: this is how much 16-bit agrees with itself from run to run (99.8%, 99.7% and 99.3%), the ceiling for the others.
- **One 32K document:** the median time from the table above, for every configuration.

**0.6B**

<!-- table:quality-0.6B -->
| Configuration | nDCG@10 FiQA | nDCG@10 SciFact | nDCG@10 ArguAna | Agreement with 16-bit | One 32K document (s) | Faster than 16-bit by |
|---|---|---|---|---|---|---|
| vLLM 16-bit | 0.675 | 0.821 | 0.580 | 99.8% (16-bit against itself) | 2.221 | 1.00× |
| vLLM fp8 | 0.672 | 0.823 | 0.571 | 92.5% | 2.132 | 1.04× |
| vLLM int8 | 0.670 | 0.824 | 0.590 | 95.1% | 2.114 | 1.05× |
| TL Engine | 0.676 | 0.827 | 0.578 | 96.4% | 1.376 | 1.61× |
<!-- end -->

**4B**

<!-- table:quality-4B -->
| Configuration | nDCG@10 FiQA | nDCG@10 SciFact | nDCG@10 ArguAna | Agreement with 16-bit | One 32K document (s) | Faster than 16-bit by |
|---|---|---|---|---|---|---|
| vLLM 16-bit | 0.771 | 0.844 | 0.598 | 99.7% (16-bit against itself) | 7.701 | 1.00× |
| vLLM fp8 | 0.765 | 0.843 | 0.604 | 94.6% | 6.713 | 1.15× |
| vLLM int8 | 0.762 | 0.836 | 0.615 | 94.5% | 6.543 | 1.18× |
| TL Engine | 0.769 | 0.846 | 0.597 | 98.3% | 4.886 | 1.58× |
<!-- end -->

**8B**

<!-- table:quality-8B -->
| Configuration | nDCG@10 FiQA | nDCG@10 SciFact | nDCG@10 ArguAna | Agreement with 16-bit | One 32K document (s) | Faster than 16-bit by |
|---|---|---|---|---|---|---|
| vLLM 16-bit | 0.780 | 0.849 | 0.695 | 99.3% (16-bit against itself) | 11.100 | 1.00× |
| vLLM fp8 | 0.781 | 0.848 | 0.685 | 96.5% | 8.764 | 1.27× |
| vLLM int8 | 0.780 | 0.845 | 0.693 | 92.1% | 8.424 | 1.32× |
| TL Engine | 0.782 | 0.847 | 0.692 | 98.7% | 6.731 | 1.65× |
<!-- end -->

`python3 scripts/tables.py` prints these tables from the run folders, plus `normal` (mixed traffic at a steady rate) and `hammer32k` latency percentiles; `--check` confirms the tables above match the data.

## Repeat it

### Region, instance, endpoint

- Region eu-west-3 (Paris). Instance ml.g6.xlarge, one per endpoint. Network isolation on. Start-up health-check and model download timeouts 1,800 s (not needed, but set in every run).
- vLLM endpoints ran on the host image `al2023-ami-sagemaker-inference-gpu-4-1`, which AWS's CUDA 13 container needs; TL Engine endpoints on SageMaker's default host image.
- [`scripts/create_endpoint.sh`](scripts/create_endpoint.sh) creates an endpoint of any configuration exactly as the runs did and sends the two sanity requests the runs sent before each test.

### vLLM 16-bit, fp8 and int8

- Image: `763104351884.dkr.ecr.eu-west-3.amazonaws.com/vllm:0.31.0-gpu-py312-cu130-ubuntu24.04-sagemaker`, AWS's, digest `sha256:da4fd31c78d04b5ec659c7fed354dd33a28b83d88cf74a6a0539630a92a93690` (read from ECR on 2026-11-13, 16, 17 and 18; pushed by AWS on 2026-10-15). The endpoints were created by tag.
- Container environment, every vLLM run: `SM_VLLM_MODEL=/opt/ml/model`, `SM_VLLM_RUNNER=pooling`, `SM_VLLM_DTYPE=bfloat16`, `SM_VLLM_SERVED_MODEL_NAME=qwen3-reranker-<size>`, `SM_VLLM_CHAT_TEMPLATE=/opt/ml/model/qwen3_reranker.jinja`, `SM_VLLM_HF_OVERRIDES={"architectures":["Qwen3ForSequenceClassification"],"classifier_from_token":["no","yes"],"is_original_qwen3_reranker":true}`, `HF_HUB_OFFLINE=1`. The 8B adds `SM_VLLM_MAX_MODEL_LEN=40000`; fp8 adds `SM_VLLM_QUANTIZATION=fp8`. The container turns each `SM_VLLM_X` into vLLM's `--x` flag; none of them is a tuning flag, so batching, compilation and attention are vLLM's defaults.
- Weights: an uncompressed S3 folder mounted at `/opt/ml/model`, with the prompt template [`scripts/qwen3_reranker.jinja`](scripts/qwen3_reranker.jinja) added ([`scripts/prepare_weights.sh`](scripts/prepare_weights.sh)).
- int8: [`scripts/w8a8_sq_msmarco.py`](scripts/w8a8_sq_msmarco.py) (llm-compressor 0.14.0; SmoothQuant strength 0.8, then W8A8 on every linear layer except `lm_head`), calibrated on 128 MS MARCO queries so that no quality set is used for calibration. Built on 2026-11-13 on one L4.

### TL Engine

- Image used in the runs: ours, digest `sha256:8a7ad8697abaec24f176435b0d3131aca184c2b76a7d94773a3de0bc2747b9c5`, with the environment `COMPILE=1`, `STEP_TOKENS=4096`, `SM_VLLM_MAX_NUM_SEQS=64`, `SM_VLLM_MAX_MODEL_LEN=33000`, `SM_VLLM_ASYNC_SCHEDULING=` (empty: the bare flag), `VLLM_DISABLE_COMPILE_CACHE=1` and `VLLM_USE_AOT_COMPILE=0` (these two concern start-up only), and the weights as a `model.tar.gz`.
- **To run it yourself, subscribe to the listing** (Qwen3-Reranker-0.6B, 4B or 8B on TL Engine; links in [transcendent-logic/tl-engine-aws](https://github.com/transcendent-logic/tl-engine-aws)) and create an endpoint from its model package with no environment (`scripts/create_endpoint.sh tl-engine <size> <name>` with `MODEL_PACKAGE_ARN`). The listing's image (digest `sha256:884402ba4f8e9ca95ee83d64613ae4dfd8cb16bdc62347a29aa1c1b614fa3ffc`) is the benchmarked image plus one layer: an OS update (glibc and perl-base only) and `STEP_TOKENS=4096` set in the image, because AWS Marketplace model packages take no environment. Every engine file is the same. With no environment, a listing endpoint runs with the settings above, apart from `VLLM_DISABLE_COMPILE_CACHE` and `VLLM_USE_AOT_COMPILE`, which are not set and affect start-up only.

### Models

| Size | Hugging Face model | Revision |
|---|---|---|
| 0.6B | [Qwen/Qwen3-Reranker-0.6B](https://huggingface.co/Qwen/Qwen3-Reranker-0.6B) | `e61197ed45024b0ed8a2d74b80b4d909f1255473` |
| 4B | [Qwen/Qwen3-Reranker-4B](https://huggingface.co/Qwen/Qwen3-Reranker-4B) | `22e683669bc0f0bd69640a1354a6d0aebcfeede5` |
| 8B | [Qwen/Qwen3-Reranker-8B](https://huggingface.co/Qwen/Qwen3-Reranker-8B) | `77d193c791ed757ca307ee72715aa132723da912` |

One exception: vLLM's 4B runs of 2026-11-11 to 15 (16-bit, fp8, and the base of the int8 checkpoint) used AWS JumpStart's copy of the 4B (`inference-prepack/v1.0.0`), which we did not compare file by file with a Hugging Face revision. vLLM's 4B load runs of 2026-11-17 used revision `22e68366`, checked file by file, and came within 4% of the earlier 16-bit run in every throughput cell (each run's folder says which weights it used).

### Client and load

- The client: [`hammer/`](hammer/), commit `195a09c`, on a c7i.xlarge in the same region as the endpoint, sending AWS-signed requests to the endpoint's public SageMaker runtime URL. Two clients were used: one for the runs of 2026-11-10 to 16 (its instance type is from our notes, not from the run files), and one with Amazon Linux 2023 for the runs of 2026-11-17 and 18. On 2026-11-13 to 18 one client sometimes tested two or three endpoints at once, each run against its own endpoint; each run's `client-vmstat.log` shows the client's CPU and memory.
- The requests: built by `hammer/scripts/prepare.py` from BEIR (SciFact, FiQA, ArguAna) and LongEmbed, downloaded from pinned Hugging Face commits and checked by SHA-256, so every run sent the same requests. See [`hammer/README.md`](hammer/README.md).
- The modes and their arguments, per run: [`scripts/run_modes.sh`](scripts/run_modes.sh) runs them as the runs did. The 4B and 8B ran `quality` at 2 in flight and `normal` at 0.25 requests a second for 15 minutes; the 0.6B ran the hammer's defaults (`quality` at 4 in flight, `normal` at 1.5 a second for 5 minutes). Every `speed` and `meticulous` query carries a random nonce, so no answer comes from a prefix cache.
- The runs behind the quality table ran `quality` and `meticulous` (TL Engine also `speed`); the load runs ran `normal`, `speed` and `hammer32k` (vLLM 16-bit) or `normal` and `hammer32k` (TL Engine, whose `speed` comes from its quality runs). The first 16-bit run of each size was a full run of every mode.

### What is not here

- The engine, and our engine's container logs, which describe its internals. vLLM's container logs are in each vLLM run's folder.
- The client wrapper scripts of 2026-11-10 to 15 were not kept. What they ran is in each run's `status` file: modes, arguments, order and times. `scripts/run_modes.sh`, made from the wrappers of 2026-11-16/17, reproduces those arguments; the only difference is noted in it (the 0.6B runs of 2026-11-10 to 13 used the hammer's default 60-second request timeout instead of 75 seconds, with no request slower than 25 seconds).
- The small probe requests the wrappers sent between modes (their results are the `probe` lines in `status`; no table uses them).
- The datasets' text. `hammer/scripts/prepare.py` downloads it; the run records hold only request ids, scores, latencies and errors.

## Layout

| Folder | What it holds |
|---|---|
| [`hammer/`](hammer/) | The load and quality client, with its request-set builder and checksums |
| [`reports/`](reports/) | One folder per run, named `<date>-<time UTC>-<configuration>-<size>`: the hammer's reports and per-request records, the client's status file, the endpoint's definition, vLLM's container log, and a README |
| [`scripts/`](scripts/) | Creating endpoints, preparing weights, the int8 checkpoint, running the modes, and `tables.py`, which computes the tables above |

In the run folders our AWS account IDs, S3 bucket names and private registry are replaced by placeholders; nothing else was changed. Each run folder keeps only the modes this benchmark uses.

## Data and model licences

The benchmark downloads its data at run time and redistributes none of it. Each dataset has its own terms (BEIR's SciFact, FiQA and ArguAna; LongEmbed; MS MARCO, used only to calibrate the vLLM int8 checkpoint); check them before you use the data. The Qwen3-Reranker models are Apache-2.0.

## Credits

The hammer was written by Renaldas Zioma (`rz`); see [`hammer/README.md`](hammer/README.md) for its source commit and what was changed for publication.

## Licence

Apache-2.0 ([LICENSE](LICENSE)); see [NOTICE](NOTICE) for the hammer, the models and the datasets. TL Engine is not part of this repository.
