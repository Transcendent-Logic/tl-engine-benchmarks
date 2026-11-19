#!/usr/bin/env bash
# run_job.sh KIND SIZE CONC JOB INPUT_S3 OUT: one SageMaker batch transform job on one ml.g6.xlarge, set up as in the batch
# runs, then its files in OUT. KIND is
#   vllm-bf16   AWS's SageMaker vLLM 0.31.0 container, 16-bit, with the endpoint runs' environment (../create_endpoint.sh)
#   tl-engine   TL Engine from its AWS Marketplace model package, with no environment, as a buyer creates it
# SIZE is 0.6b, 4b or 8b. CONC is MaxConcurrentTransforms: "default" leaves it unset (SageMaker then asks the container's
# /execution-parameters; neither container has one, so it uses 1), or a number (the runs used 4). JOB names the model and the
# transform job. INPUT_S3 is the S3 prefix holding the input from build_input.py (requests.jsonl, one request per line).
# OUT gets job.json (DescribeTransformJob), transform-input.json (the CreateTransformJob request), model-container.json,
# output/ (the .out file, one response per input line) and logs/ (every CloudWatch stream of the job). The model is deleted
# afterwards; the job's output stays in S3 under OUTPUT_S3/JOB/.
#
# Environment:
#   ROLE_ARN           SageMaker execution role (reads INPUT_S3 and the weights, writes OUTPUT_S3, pulls AWS's vLLM image)
#   OUTPUT_S3          S3 prefix for the jobs' output, e.g. s3://<your bucket>/batch/ (ending in /)
#   VLLM_WEIGHTS       vllm-bf16: the model.tar.gz from pack_vllm_weights.sh for this SIZE
#   MODEL_PACKAGE_ARN  tl-engine: the model package ARN your subscription to the listing gives you, for this SIZE
#   REGION             default eu-west-3 (Paris), where every run was made
# Needs the AWS CLI and python3.
set -euo pipefail
KIND=${1:?KIND}; SIZE=${2:?SIZE}; CONC=${3:?CONC}; JOB=${4:?JOB}; INPUT=${5:?INPUT_S3}; OUT=${6:?OUT}
REGION=${REGION:-eu-west-3}; ROLE_ARN=${ROLE_ARN:?set ROLE_ARN}; OUTPUT_S3=${OUTPUT_S3:?set OUTPUT_S3}
export AWS_DEFAULT_REGION=$REGION
VLLM_IMAGE=763104351884.dkr.ecr.$REGION.amazonaws.com/vllm:0.31.0-gpu-py312-cu130-ubuntu24.04-sagemaker
case $SIZE in 0.6b|4b|8b) ;; *) echo "SIZE must be 0.6b, 4b or 8b"; exit 1;; esac
mkdir -p "$OUT/output" "$OUT/logs"
log() { echo "$1 $(date -u +%FT%TZ) ${2:-}" | tee -a "$OUT/status"; }

case $KIND in
vllm-bf16)
  VLLM_WEIGHTS=${VLLM_WEIGHTS:?set VLLM_WEIGHTS}
  python3 - "$SIZE" "$VLLM_WEIGHTS" "$VLLM_IMAGE" > "$OUT/model-container.json" <<'PY'
import json, sys
size, weights, image = sys.argv[1:]
env = {"SM_VLLM_MODEL": "/opt/ml/model", "SM_VLLM_RUNNER": "pooling", "SM_VLLM_DTYPE": "bfloat16",
       "SM_VLLM_SERVED_MODEL_NAME": f"qwen3-reranker-{size}",
       "SM_VLLM_CHAT_TEMPLATE": "/opt/ml/model/qwen3_reranker.jinja",
       "SM_VLLM_HF_OVERRIDES": json.dumps({"architectures": ["Qwen3ForSequenceClassification"],
                                           "classifier_from_token": ["no", "yes"], "is_original_qwen3_reranker": True},
                                          separators=(",", ":")),
       "HF_HUB_OFFLINE": "1"}
if size == "8b":
    env["SM_VLLM_MAX_MODEL_LEN"] = "40000"  # as on the endpoints
    # Batch only: batch hosts run NVIDIA driver 535 (TransformAmiVersion offers 470 and 535), where the L4 reports 21.96 GiB
    # (22.03 GiB on the endpoints' driver-580 host image). At vLLM's default 0.92 every start then finds 5.45 GiB of KV cache
    # against the 5.49 GiB that 40,000 tokens need, and the job fails its ping check. 0.925 gives about 5.57 GiB, close to the
    # endpoints' 5.52 GiB: more memory for vLLM, not less. See the README, "Batch transform jobs".
    env["SM_VLLM_GPU_MEMORY_UTILIZATION"] = "0.925"
print(json.dumps({"Image": image, "Environment": env, "ModelDataUrl": weights}))
PY
  ;;
tl-engine)
  MODEL_PACKAGE_ARN=${MODEL_PACKAGE_ARN:?set MODEL_PACKAGE_ARN}
  echo "{\"ModelPackageName\":\"$MODEL_PACKAGE_ARN\"}" > "$OUT/model-container.json" ;;
*) echo "KIND must be vllm-bf16 or tl-engine"; exit 1 ;;
esac

python3 - "$JOB" "$INPUT" "${OUTPUT_S3%/}/$JOB/output/" "$CONC" > "$OUT/transform-input.json" <<'PY'
import json, sys
job, inp, out, conc = sys.argv[1:]
d = {"TransformJobName": job, "ModelName": job, "BatchStrategy": "SingleRecord",
     "TransformInput": {"DataSource": {"S3DataSource": {"S3DataType": "S3Prefix", "S3Uri": inp}},
                        "ContentType": "application/json", "SplitType": "Line"},
     "TransformOutput": {"S3OutputPath": out, "Accept": "application/json", "AssembleWith": "Line"},
     "TransformResources": {"InstanceType": "ml.g6.xlarge", "InstanceCount": 1}}
if conc != "default":
    d["MaxConcurrentTransforms"] = int(conc)
print(json.dumps(d))
PY

log create-model "$KIND $SIZE"
aws sagemaker create-model --model-name "$JOB" --execution-role-arn "$ROLE_ARN" --enable-network-isolation \
  --primary-container "file://$OUT/model-container.json" --query ModelArn --output text >> "$OUT/status"
log create-transform-job "conc=$CONC"
aws sagemaker create-transform-job --cli-input-json "file://$OUT/transform-input.json" --query TransformJobArn --output text >> "$OUT/status"
aws sagemaker wait transform-job-completed-or-stopped --transform-job-name "$JOB" || true   # the waiter gives up after 1 hour
while ST=$(aws sagemaker describe-transform-job --transform-job-name "$JOB" --query TransformJobStatus --output text) \
      && [ "$ST" = InProgress -o "$ST" = Stopping ]; do sleep 60; done
log "job-$ST"
aws sagemaker describe-transform-job --transform-job-name "$JOB" > "$OUT/job.json"
for i in 1 2 3 4 5; do
  aws s3 cp --recursive --only-show-errors "${OUTPUT_S3%/}/$JOB/output/" "$OUT/output/" && break
  log retry "output download, attempt $i failed"; sleep 30
done
for s in $(aws logs describe-log-streams --log-group-name /aws/sagemaker/TransformJobs --log-stream-name-prefix "$JOB/" \
            --query 'logStreams[].logStreamName' --output text); do
  python3 "$(dirname "$0")/fetch_log.py" /aws/sagemaker/TransformJobs "$s" > "$OUT/logs/$(basename "$s").jsonl"
done
aws sagemaker delete-model --model-name "$JOB" && log model-deleted
[ "$ST" = Completed ] && log done || log FAILED "job $ST"
