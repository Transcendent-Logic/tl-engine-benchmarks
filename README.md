# TL Engine benchmarks

The benchmark behind the numbers we publish for TL Engine, including our AWS Marketplace listings: Qwen3-Reranker 0.6B, 4B and 8B served by **TL Engine**, our inference engine for the NVIDIA L4, against the same models served by **vLLM 16-bit**. vLLM fp8 and int8 are in the quality table as well.

This repository holds everything needed to see and repeat it: the load client, every run's raw results, the scripts that created the endpoints and ran the client, and the script that computes the tables below from those results.

- **Same model, same hardware.** Each configuration ran on its own Amazon SageMaker real-time endpoint: one ml.g6.xlarge (one NVIDIA L4, 24 GB) in eu-west-3 (Paris), network isolation on.
- **The baseline is vLLM as AWS ships it.** AWS's SageMaker vLLM 0.31.0 container, unmodified, with vLLM's defaults and only the settings a reranker needs.
- **Batch transform jobs too.** The same models as SageMaker batch transform jobs, TL Engine against vLLM 16-bit, three jobs per configuration (2026-11-19 and 22): [Batch transform jobs](#batch-transform-jobs).
- **Three runs of each configuration.** Every number below is the mean of three runs on three separate endpoints, run between 2026-11-10 and 2026-11-23. We publish only these means; each run's own values are in its folder under [`reports/`](reports/), and `python3 scripts/tables.py --runs` prints them next to the means.

## What was compared

| Configuration | Server | Weights | Precision |
|---|---|---|---|
| **vLLM 16-bit** | AWS's SageMaker vLLM 0.31.0 container | Qwen's, unmodified | BF16 |
| **vLLM fp8** | The same container with `SM_VLLM_QUANTIZATION=fp8` | Qwen's, quantized by vLLM when it loads them | fp8 weights and activations (per tensor) |
| **vLLM int8** | The same container | An int8 W8A8 SmoothQuant checkpoint made with llm-compressor ([`scripts/w8a8_sq_msmarco.py`](scripts/w8a8_sq_msmarco.py)) | int8 weights and activations |
| **TL Engine** | Our engine, in the image of our AWS Marketplace listing | Qwen's, in the engine's own file format | Mixed precision, on its own kernels for the L4 |

The engine itself is proprietary and is not in this repository; you can run it through the AWS Marketplace listing (see [Repeat it](#repeat-it)).

## Results

All numbers are means of three runs. Tokens a second count the server's own token count (`usage.total_tokens`) of the requests it answered, over wall time.

### Peak throughput

Tokens a second for one instance, by request shape: each `speed` cell is 25 seconds of requests at 4 in flight, where both servers reach their peak (16 in flight adds nothing, and at 16 SageMaker's 60-second limit cut off some 4B and 8B requests of both). `hammer32k` sends 32K-token requests for 45 minutes, 2 in flight.

**0.6B**

<!-- table:throughput-0.6B -->
| Request shape | vLLM 16-bit (tok/s) | TL Engine (tok/s) | TL Engine ÷ vLLM |
|---|---|---|---|
| 20 documents per request (`short20`), 4 in flight | 57,066 | 106,795 | 1.87× |
| 100 documents of 256 tokens (`many100`), 4 in flight | 74,056 | 143,076 | 1.93× |
| One 8K-token document (`long8k`), 4 in flight | 23,116 | 39,156 | 1.69× |
| About 30K tokens in 3 to 55 documents (`pack32k`), 4 in flight | 49,823 | 86,800 | 1.74× |
| About 31K tokens in 1 to 5 documents (`long32k`), 4 in flight | 18,952 | 31,451 | 1.66× |
| 32K-token requests for 45 minutes (`hammer32k`), 2 in flight | 18,596 | 30,569 | 1.64× |
<!-- end -->

**4B**

<!-- table:throughput-4B -->
| Request shape | vLLM 16-bit (tok/s) | TL Engine (tok/s) | TL Engine ÷ vLLM |
|---|---|---|---|
| 20 documents per request (`short20`), 4 in flight | 10,633 | 16,711 | 1.57× |
| 100 documents of 256 tokens (`many100`), 4 in flight | 13,390 | 21,377 | 1.60× |
| One 8K-token document (`long8k`), 4 in flight | 5,202 | 8,465 | 1.63× |
| About 30K tokens in 3 to 55 documents (`pack32k`), 4 in flight | 10,413 | 16,342 | 1.57× |
| About 31K tokens in 1 to 5 documents (`long32k`), 4 in flight | 4,538 | 7,448 | 1.64× |
| 32K-token requests for 45 minutes (`hammer32k`), 2 in flight | 4,569 | 7,303 | 1.60× |
<!-- end -->

**8B**

<!-- table:throughput-8B -->
| Request shape | vLLM 16-bit (tok/s) | TL Engine (tok/s) | TL Engine ÷ vLLM |
|---|---|---|---|
| 20 documents per request (`short20`), 4 in flight | 5,357 | 8,604 | 1.61× |
| 100 documents of 256 tokens (`many100`), 4 in flight | 7,108 | 11,247 | 1.58× |
| One 8K-token document (`long8k`), 4 in flight | 2,980 | 5,002 | 1.68× |
| About 30K tokens in 3 to 55 documents (`pack32k`), 4 in flight | 5,821 | 9,664 | 1.66× |
| About 31K tokens in 1 to 5 documents (`long32k`), 4 in flight | 2,905 | 4,682 | 1.61× |
| 32K-token requests for 45 minutes (`hammer32k`), 2 in flight | 2,819 | 4,578 | 1.62× |
<!-- end -->

### One request at a time

How long a single request takes when it has the endpoint to itself. One 32K-token document: 30 requests sent one after another (`meticulous`). 20 documents (the three BEIR sets, about 5K to 12K tokens a request): 25 seconds of requests one after another (`speed`, `short20 ×1`). Each is given as the median time (the typical request) and the mean time (the average over every answered request).

**0.6B**

<!-- table:single-0.6B -->
| Request, sent alone | vLLM 16-bit (s) | TL Engine (s) | Faster by |
|---|---|---|---|
| One document of 32K tokens (`meticulous`, 30 requests): median time | 2.221 | 1.306 | 1.70× |
| The same: mean time | 2.218 | 1.306 | 1.70× |
| 20 documents per request (`speed` `short20 ×1`, 25 seconds of requests): median time | 0.178 | 0.088 | 2.03× |
| The same: mean time | 0.184 | 0.091 | 2.01× |
<!-- end -->

**4B**

<!-- table:single-4B -->
| Request, sent alone | vLLM 16-bit (s) | TL Engine (s) | Faster by |
|---|---|---|---|
| One document of 32K tokens (`meticulous`, 30 requests): median time | 7.701 | 4.634 | 1.66× |
| The same: mean time | 7.697 | 4.635 | 1.66× |
| 20 documents per request (`speed` `short20 ×1`, 25 seconds of requests): median time | 0.805 | 0.500 | 1.61× |
| The same: mean time | 0.890 | 0.540 | 1.65× |
<!-- end -->

**8B**

<!-- table:single-8B -->
| Request, sent alone | vLLM 16-bit (s) | TL Engine (s) | Faster by |
|---|---|---|---|
| One document of 32K tokens (`meticulous`, 30 requests): median time | 11.100 | 6.720 | 1.65× |
| The same: mean time | 11.063 | 6.722 | 1.65× |
| 20 documents per request (`speed` `short20 ×1`, 25 seconds of requests): median time | 1.565 | 0.963 | 1.62× |
| The same: mean time | 1.678 | 1.045 | 1.61× |
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
| TL Engine | 0.670 | 0.817 | 0.583 | 96.3% | 1.306 | 1.70× |
<!-- end -->

**4B**

<!-- table:quality-4B -->
| Configuration | nDCG@10 FiQA | nDCG@10 SciFact | nDCG@10 ArguAna | Agreement with 16-bit | One 32K document (s) | Faster than 16-bit by |
|---|---|---|---|---|---|---|
| vLLM 16-bit | 0.771 | 0.844 | 0.598 | 99.7% (16-bit against itself) | 7.701 | 1.00× |
| vLLM fp8 | 0.765 | 0.843 | 0.604 | 94.6% | 6.713 | 1.15× |
| vLLM int8 | 0.762 | 0.836 | 0.615 | 94.5% | 6.543 | 1.18× |
| TL Engine | 0.767 | 0.847 | 0.599 | 98.7% | 4.634 | 1.66× |
<!-- end -->

**8B**

<!-- table:quality-8B -->
| Configuration | nDCG@10 FiQA | nDCG@10 SciFact | nDCG@10 ArguAna | Agreement with 16-bit | One 32K document (s) | Faster than 16-bit by |
|---|---|---|---|---|---|---|
| vLLM 16-bit | 0.780 | 0.849 | 0.695 | 99.3% (16-bit against itself) | 11.100 | 1.00× |
| vLLM fp8 | 0.781 | 0.848 | 0.685 | 96.5% | 8.764 | 1.27× |
| vLLM int8 | 0.780 | 0.845 | 0.693 | 92.1% | 8.424 | 1.32× |
| TL Engine | 0.780 | 0.847 | 0.691 | 98.2% | 6.720 | 1.65× |
<!-- end -->

### Batch transform jobs

The same comparison as SageMaker batch transform jobs (vLLM 16-bit on 2026-11-19, TL Engine on 2026-11-22): each job on one ml.g6.xlarge in eu-west-3, network isolation on, and the same input file for both engines per size. The input is the `short20` requests (20 documents per request, the three BEIR sets), one per line, each query with a nonce: 7,200 requests for the 0.6B (61.7 million tokens), 1,800 for the 4B (15.4 million), 900 for the 8B (7.7 million). `MaxConcurrentTransforms` was left unset, SageMaker's default (it asks the container's `/execution-parameters`, which neither container has, and then sends one request at a time), or set to 4. Three jobs per configuration.

- **Tokens a second:** the tokens of all responses (`usage.total_tokens`) over the time from the first to the last request in the container log.
- **Billed job:** `TransformStartTime` to `TransformEndTime`, container start-up and processing. Not counted: the few minutes before, while AWS finds the instance, the same for both engines. "Finishes sooner by" is vLLM's billed job time divided by TL Engine's.
- **$ per million tokens:** ml.g6.xlarge batch transform in Paris at $1.43024 an hour (AWS Price List API, read 2026-11-19), over the billed job. TL Engine's row adds its $0.30 an hour software fee.

**0.6B**

<!-- table:batch-0.6B -->
| MaxConcurrentTransforms | vLLM 16-bit (tok/s) | TL Engine (tok/s) | TL Engine ÷ vLLM | Billed job, vLLM 16-bit (s) | Billed job, TL Engine (s) | Finishes sooner by | $ per million tokens, vLLM 16-bit | $ per million tokens, TL Engine with its fee | TL Engine costs less by |
|---|---|---|---|---|---|---|---|---|---|
| 1 (SageMaker's default) | 51,329 | 99,249 | 1.93× | 1,527 | 735 | 2.08× | $0.0098 | $0.0057 | 41.8% |
| 4 | 57,203 | 105,983 | 1.85× | 1,405 | 696 | 2.02× | $0.0090 | $0.0054 | 40.1% |
<!-- end -->

**4B**

<!-- table:batch-4B -->
| MaxConcurrentTransforms | vLLM 16-bit (tok/s) | TL Engine (tok/s) | TL Engine ÷ vLLM | Billed job, vLLM 16-bit (s) | Billed job, TL Engine (s) | Finishes sooner by | $ per million tokens, vLLM 16-bit | $ per million tokens, TL Engine with its fee | TL Engine costs less by |
|---|---|---|---|---|---|---|---|---|---|
| 1 (SageMaker's default) | 9,426 | 15,898 | 1.69× | 2,050 | 1,114 | 1.84× | $0.0528 | $0.0347 | 34.2% |
| 4 | 10,047 | 16,010 | 1.59× | 1,954 | 1,108 | 1.76× | $0.0503 | $0.0345 | 31.4% |
<!-- end -->

**8B**

<!-- table:batch-8B -->
| MaxConcurrentTransforms | vLLM 16-bit (tok/s) | TL Engine (tok/s) | TL Engine ÷ vLLM | Billed job, vLLM 16-bit (s) | Billed job, TL Engine (s) | Finishes sooner by | $ per million tokens, vLLM 16-bit | $ per million tokens, TL Engine with its fee | TL Engine costs less by |
|---|---|---|---|---|---|---|---|---|---|
| 1 (SageMaker's default) | 5,129 | 8,634 | 1.68× | 2,141 | 1,072 | 2.00× | $0.1103 | $0.0668 | 39.4% |
| 4 | 5,376 | 8,703 | 1.62× | 2,071 | 1,068 | 1.94× | $0.1067 | $0.0665 | 37.6% |
<!-- end -->

- **Batch matches the endpoint benchmark.** At `MaxConcurrentTransforms` 4, vLLM 16-bit reaches 100% (0.6B), 94% (4B) and 100% (8B) of its peak on the endpoints (`short20`, 4 in flight, above), TL Engine 99%, 96% and 101%.
- **SageMaker's default costs the most on the 0.6B.** Left at 1, the 0.6B runs at 94% of its speed at 4 on TL Engine (90% on vLLM 16-bit), because each request takes so little GPU time that the gaps between requests show. On the 4B and 8B one 20-document request already fills the L4: both engines keep 94 to 99% of their speed. Set `MaxConcurrentTransforms` to 4 for batch jobs.
- **Same rankings.** On the same input, TL Engine's top document is vLLM 16-bit's in 96.2% (0.6B), 98.6% (4B) and 97.4% (8B) of requests, and in 99.6 to 99.8% counting a different top document whose vLLM score is within 0.01 of the best; vLLM 16-bit's own jobs agree with each other in 99.0 to 99.6%.
- **Start-up** (job start to first request) is 110 to 180 seconds for TL Engine and 310 to 640 seconds for vLLM 16-bit; it is inside the billed job. Before it, AWS takes a few minutes to provide the instance, the same for both, so on these job sizes the whole wait from the create call to the finished job is shorter by less than the billed job.

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

- Image used in the runs: ours, digest `sha256:81e43230efce898a28416ffabe09fccbe9f26ac36cc60e7badfa2c4d1b8140bd`, with no environment (the image's own settings), and the weights in the engine's own file format as a `model.tar.gz`.
- **To run it yourself, subscribe to the listing** (Qwen3-Reranker-0.6B, 4B or 8B on TL Engine; links in [transcendent-logic/tl-engine-aws](https://github.com/transcendent-logic/tl-engine-aws)) and create an endpoint from its model package with no environment (`scripts/create_endpoint.sh tl-engine <size> <name>` with `MODEL_PACKAGE_ARN`). The listing's model package carries the benchmarked image and the same `model.tar.gz`, so a listing endpoint runs exactly what the runs ran.

### Models

| Size | Hugging Face model | Revision |
|---|---|---|
| 0.6B | [Qwen/Qwen3-Reranker-0.6B](https://huggingface.co/Qwen/Qwen3-Reranker-0.6B) | `e61197ed45024b0ed8a2d74b80b4d909f1255473` |
| 4B | [Qwen/Qwen3-Reranker-4B](https://huggingface.co/Qwen/Qwen3-Reranker-4B) | `22e683669bc0f0bd69640a1354a6d0aebcfeede5` |
| 8B | [Qwen/Qwen3-Reranker-8B](https://huggingface.co/Qwen/Qwen3-Reranker-8B) | `77d193c791ed757ca307ee72715aa132723da912` |

One exception: vLLM's 4B runs of 2026-11-11 to 15 (16-bit, fp8, and the base of the int8 checkpoint) used AWS JumpStart's copy of the 4B (`inference-prepack/v1.0.0`), which we did not compare file by file with a Hugging Face revision. vLLM's 4B load runs of 2026-11-17 used revision `22e68366`, checked file by file, and came within 4% of the earlier 16-bit run in every throughput cell (each run's folder says which weights it used).

### Client and load

- The client: [`hammer/`](hammer/), commit `195a09c`, on a c7i.xlarge in the same region as the endpoint, sending AWS-signed requests to the endpoint's public SageMaker runtime URL. Two clients were used: one for the runs of 2026-11-10 to 16 (its instance type is from our notes, not from the run files), and one with Amazon Linux 2023 for the runs of 2026-11-17 to 23. On 2026-11-13 to 23 one client sometimes tested two or three endpoints at once, each run against its own endpoint; each run's `client-vmstat.log` shows the client's CPU and memory.
- The requests: built by `hammer/scripts/prepare.py` from BEIR (SciFact, FiQA, ArguAna) and LongEmbed, downloaded from pinned Hugging Face commits and checked by SHA-256, so every run sent the same requests. See [`hammer/README.md`](hammer/README.md).
- The modes and their arguments, per run: [`scripts/run_modes.sh`](scripts/run_modes.sh) runs them as the runs did. The 4B and 8B ran `quality` at 2 in flight and `normal` at 0.25 requests a second for 15 minutes; the 0.6B ran the hammer's defaults (`quality` at 4 in flight, `normal` at 1.5 a second for 5 minutes). Every `speed` and `meticulous` query carries a random nonce, so no answer comes from a prefix cache.
- The runs behind the quality table ran `quality` and `meticulous` (TL Engine also `speed`); the load runs ran `normal`, `speed` and `hammer32k` (vLLM 16-bit) or `normal` and `hammer32k` (TL Engine, whose `speed` comes from its quality runs). The first 16-bit run of each size was a full run of every mode.

### Batch transform jobs

Each run folder named `<date>-<time>-batch-<configuration>-<size>-c<1|4>` under [`reports/`](reports/) holds what its job was created with (`transform-input.json`, `model-container.json`), how it ended (`job.json`), SageMaker's data log, the measures (`batch.json`) and per request the scores and tokens (`per-request.jsonl`). The scripts are in [`scripts/batch/`](scripts/batch/):

1. **Input:** `python3 scripts/batch/build_input.py --prepared hammer/data/prepared --size 4b --count 1800 --out in-4b` (after the hammer's `prepare.py`; 7,200 requests for the 0.6B, 900 for the 8B). It writes `in-4b/input/requests.jsonl`, byte for byte the runs' input: its SHA-256 is in each run's `run.json`. Copy it to S3.
2. **vLLM 16-bit weights:** `scripts/batch/pack_vllm_weights.sh 4b s3://<your bucket>/models/qwen3-reranker-4b/model.tar.gz`: the Hugging Face revision of the endpoint runs plus [`scripts/qwen3_reranker.jinja`](scripts/qwen3_reranker.jinja), packed as one `model.tar.gz`.
3. **A job:** `ROLE_ARN=… OUTPUT_S3=s3://<your bucket>/batch/ VLLM_WEIGHTS=s3://…/model.tar.gz scripts/batch/run_job.sh vllm-bf16 4b 4 <job name> s3://<your bucket>/in-4b/ out/<job name>`; for TL Engine, `MODEL_PACKAGE_ARN=<the ARN your subscription gives you> … run_job.sh tl-engine 4b 4 …`. `default` instead of `4` leaves `MaxConcurrentTransforms` unset.
4. **The measures:** `python3 scripts/batch/analyze.py out/<job name> in-4b/index.jsonl` writes `batch.json` and `per-request.jsonl`.

How the batch jobs differ from the endpoint runs:

- **vLLM's weights are a `model.tar.gz`** of the same files as the endpoints' uncompressed folder: a batch job refuses a model whose container uses `ModelDataSource`.
- **The host.** Both engines ran on SageMaker's default batch host, with NVIDIA driver 535. The vLLM endpoints ran on `al2023-ami-sagemaker-inference-gpu-4-1` (driver 580), which batch transform does not offer: `TransformAmiVersion` has only `al2-ami-sagemaker-batch-gpu-470` and `-535`. AWS's CUDA 13 vLLM container starts and runs there.
- **vLLM 8B adds `SM_VLLM_GPU_MEMORY_UTILIZATION=0.925`** (vLLM's default is 0.92). With driver 535 the L4 reports 21.96 GiB instead of 22.03 GiB, and at 0.92 every start of vLLM 8B found 5.45 GiB of KV cache against the 5.49 GiB that 40,000 tokens need (`ValueError: To serve at least one request with the model's max seq len (40000), (5.49 GiB KV cache is needed, which is larger than the available KV cache memory (5.45 GiB)`), so the job failed its health check. On the endpoints the same check passed with 5.52 GiB. 0.925 gives about 5.57 GiB: more memory for vLLM, not less. The 0.6B and 4B run with the endpoints' settings unchanged.
- **TL Engine ran from our image and `model.tar.gz`** with no environment, as on the endpoints: what the listing's model package carries (see [TL Engine](#tl-engine)).

### What is not here

- The engine, and our engine's container logs, which describe its internals. vLLM's container logs are in each vLLM run's folder.
- The client wrapper scripts of 2026-11-10 to 15 were not kept. What they ran is in each run's `status` file: modes, arguments, order and times. `scripts/run_modes.sh`, made from the wrappers of 2026-11-16/17, reproduces those arguments; the only difference is noted in it (the 0.6B runs of 2026-11-10 to 13 used the hammer's default 60-second request timeout instead of 75 seconds, with no request slower than 25 seconds).
- The small probe requests the wrappers sent between modes (their results are the `probe` lines in `status`; no table uses them).
- The datasets' text. `hammer/scripts/prepare.py` downloads it; the run records hold only request ids, scores, latencies and errors.
- Batch jobs: their raw output, which echoes every document's text (`per-request.jsonl` keeps every score and token count), and TL Engine's container log apart from its access lines (`POST /invocations`), which give the processing window.

## Layout

| Folder | What it holds |
|---|---|
| [`hammer/`](hammer/) | The load and quality client, with its request-set builder and checksums |
| [`reports/`](reports/) | One folder per run, named `<date>-<time UTC>-<configuration>-<size>`: the hammer's reports and per-request records, the client's status file, the endpoint's definition, vLLM's container log, and a README; batch jobs as `<date>-<time UTC>-batch-<configuration>-<size>-c<1|4>` |
| [`scripts/`](scripts/) | Creating endpoints, preparing weights, the int8 checkpoint, running the modes, and `tables.py`, which computes the tables above |
| [`scripts/batch/`](scripts/batch/) | The batch transform jobs: building the input, packing vLLM's weights, running a job, measuring it |

In the run folders our AWS account IDs, S3 bucket names and private registry are replaced by placeholders, and in TL Engine's endpoint, job and file names our internal name for the engine by `tl`; nothing else was changed. Each run folder keeps only the modes this benchmark uses.

## Data and model licences

The benchmark downloads its data at run time and redistributes none of it. Each dataset has its own terms (BEIR's SciFact, FiQA and ArguAna; LongEmbed; MS MARCO, used only to calibrate the vLLM int8 checkpoint); check them before you use the data. The Qwen3-Reranker models are Apache-2.0.

## Credits

The hammer was written by Renaldas Zioma (`rz`); see [`hammer/README.md`](hammer/README.md) for its source commit and what was changed for publication.

## Licence

Apache-2.0 ([LICENSE](LICENSE)); see [NOTICE](NOTICE) for the hammer, the models and the datasets. TL Engine is not part of this repository.
