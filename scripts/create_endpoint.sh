#!/usr/bin/env bash
# create_endpoint.sh KIND SIZE NAME: one ml.g6.xlarge SageMaker endpoint set up as in the benchmark runs, then wait until it is
# in service. KIND is one of
#   vllm-bf16   AWS's SageMaker vLLM 0.31.0 container, 16-bit (vLLM's defaults apart from the variables below)
#   vllm-fp8    the same with vLLM's online fp8 quantization (SM_VLLM_QUANTIZATION=fp8)
#   vllm-int8   the same container serving an int8 W8A8 SmoothQuant checkpoint (w8a8_sq_msmarco.py)
#   tl-engine   TL Engine from its AWS Marketplace model package
# SIZE is 0.6b, 4b or 8b. Needs the AWS CLI with credentials for the account that pays for the endpoint.
#
# Environment:
#   ROLE_ARN           SageMaker execution role (needs S3 read on WEIGHTS and, for vllm-*, ECR pull on AWS's vllm repository)
#   WEIGHTS            vllm-*: S3 prefix (ending in /) with the model and qwen3_reranker.jinja, from prepare_weights.sh
#                      (vllm-int8: the checkpoint written by w8a8_sq_msmarco.py, which copies the template next to it)
#   MODEL_PACKAGE_ARN  tl-engine: the model package ARN your subscription to the listing gives you
#   REGION             default eu-west-3 (Paris), where every run was made
#
# The benchmark runs created TL Engine endpoints from the image directly, with the weights as a model.tar.gz and the
# environment in TL_ENV below; the listing's model package carries the same engine and weights and sets STEP_TOKENS=4096 in its
# image, so a buyer's endpoint runs the benchmarked settings with no environment at all (see ../README.md, "TL Engine").
set -euo pipefail
KIND=${1:?KIND}; SIZE=${2:?SIZE}; NAME=${3:?NAME}; REGION=${REGION:-eu-west-3}
ROLE_ARN=${ROLE_ARN:?set ROLE_ARN}
VLLM_IMAGE=763104351884.dkr.ecr.$REGION.amazonaws.com/vllm:0.31.0-gpu-py312-cu130-ubuntu24.04-sagemaker
# digest on 2026-11-13 to 18, as read from ECR: sha256:da4fd31c78d04b5ec659c7fed354dd33a28b83d88cf74a6a0539630a92a93690
case $SIZE in 0.6b|4b|8b) ;; *) echo "SIZE must be 0.6b, 4b or 8b"; exit 1;; esac
W=$(mktemp -d); trap 'rm -rf "$W"' EXIT

case $KIND in
vllm-*)
  WEIGHTS=${WEIGHTS:?set WEIGHTS to the S3 prefix of the weights}
  python3 - "$SIZE" "$KIND" "$WEIGHTS" "$VLLM_IMAGE" > "$W/container.json" <<'PY'
import json, sys
size, kind, weights, image = sys.argv[1:]
env = {"SM_VLLM_MODEL": "/opt/ml/model", "SM_VLLM_RUNNER": "pooling", "SM_VLLM_DTYPE": "bfloat16",
       "SM_VLLM_SERVED_MODEL_NAME": f"qwen3-reranker-{size}",
       "SM_VLLM_CHAT_TEMPLATE": "/opt/ml/model/qwen3_reranker.jinja",
       "SM_VLLM_HF_OVERRIDES": json.dumps({"architectures": ["Qwen3ForSequenceClassification"],
                                           "classifier_from_token": ["no", "yes"], "is_original_qwen3_reranker": True},
                                          separators=(",", ":")),
       "HF_HUB_OFFLINE": "1"}
if size == "8b":
    env["SM_VLLM_MAX_MODEL_LEN"] = "40000"  # the one setting added for the 8B
if kind == "vllm-fp8":
    env["SM_VLLM_QUANTIZATION"] = "fp8"
print(json.dumps({"Image": image, "Environment": env,
                  "ModelDataSource": {"S3DataSource": {"S3Uri": weights, "S3DataType": "S3Prefix", "CompressionType": "None"}}}))
PY
  # AWS's CUDA 13 container needs a host with a newer driver than SageMaker's default
  echo '[{"VariantName":"AllTraffic","ModelName":"'$NAME'","InitialInstanceCount":1,"InstanceType":"ml.g6.xlarge","InferenceAmiVersion":"al2023-ami-sagemaker-inference-gpu-4-1","ContainerStartupHealthCheckTimeoutInSeconds":1800,"ModelDataDownloadTimeoutInSeconds":1800}]' > "$W/variants.json"
  ;;
tl-engine)
  MODEL_PACKAGE_ARN=${MODEL_PACKAGE_ARN:?set MODEL_PACKAGE_ARN}
  echo '{"ModelPackageName":"'$MODEL_PACKAGE_ARN'"}' > "$W/container.json"
  # What the benchmark runs set instead (the benchmarked image, with the weights as model.tar.gz):
  #   TL_ENV='{"COMPILE":"1","VLLM_DISABLE_COMPILE_CACHE":"1","VLLM_USE_AOT_COMPILE":"0","STEP_TOKENS":"4096",
  #            "SM_VLLM_MAX_NUM_SEQS":"64","SM_VLLM_MAX_MODEL_LEN":"33000","SM_VLLM_ASYNC_SCHEDULING":""}'
  # SageMaker's default host image, as in the runs; the 1,800 s timeouts are not needed (it starts in 5 to 7 minutes)
  echo '[{"VariantName":"AllTraffic","ModelName":"'$NAME'","InitialInstanceCount":1,"InstanceType":"ml.g6.xlarge","ContainerStartupHealthCheckTimeoutInSeconds":1800,"ModelDataDownloadTimeoutInSeconds":1800}]' > "$W/variants.json"
  ;;
*) echo "KIND must be vllm-bf16, vllm-fp8, vllm-int8 or tl-engine"; exit 1;;
esac

A="aws --region $REGION"
cat "$W/container.json"; echo
$A sagemaker create-model --model-name "$NAME" --execution-role-arn "$ROLE_ARN" --enable-network-isolation \
  --primary-container "file://$W/container.json" --query ModelArn --output text
$A sagemaker create-endpoint-config --endpoint-config-name "$NAME" --production-variants "file://$W/variants.json" \
  --query EndpointConfigArn --output text
$A sagemaker create-endpoint --endpoint-name "$NAME" --endpoint-config-name "$NAME" --query EndpointArn --output text
T0=$(date +%s)
$A sagemaker wait endpoint-in-service --endpoint-name "$NAME"
echo "$NAME in service after $(( $(date +%s) - T0 )) s"

# Sanity checks, as before each run: three short documents, and one planted sentence among two documents of about 24,000 tokens
for f in req_short req_long; do
  $A sagemaker-runtime invoke-endpoint --endpoint-name "$NAME" --content-type application/json \
    --cli-binary-format raw-in-base64-out --body "file://$(dirname "$0")/$f.json" "$W/out.json" > /dev/null
  python3 -c 'import sys,json; d=json.load(open(sys.argv[1])); print(sys.argv[2], d["usage"]["total_tokens"], [(r["index"], round(r["relevance_score"], 6)) for r in d["results"]])' "$W/out.json" $f
done
echo "Delete when done: $A sagemaker delete-endpoint --endpoint-name $NAME; $A sagemaker delete-endpoint-config --endpoint-config-name $NAME; $A sagemaker delete-model --model-name $NAME"
