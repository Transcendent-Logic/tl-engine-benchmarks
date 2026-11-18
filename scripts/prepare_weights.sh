#!/usr/bin/env bash
# prepare_weights.sh SIZE S3_PREFIX: the weights folder AWS's vLLM container mounts at /opt/ml/model: Qwen3-Reranker-SIZE at the
# Hugging Face revision the runs used, plus the prompt template qwen3_reranker.jinja, uploaded uncompressed to S3_PREFIX
# (s3://<your bucket>/<path>/, ending in /). Needs the Hugging Face CLI (`hf`, from huggingface_hub) and the AWS CLI.
set -euo pipefail
SIZE=${1:?SIZE (0.6b, 4b or 8b)}; DEST=${2:?S3_PREFIX}
case $SIZE in
  0.6b) REPO=Qwen/Qwen3-Reranker-0.6B REV=e61197ed45024b0ed8a2d74b80b4d909f1255473 ;;
  4b)   REPO=Qwen/Qwen3-Reranker-4B   REV=22e683669bc0f0bd69640a1354a6d0aebcfeede5 ;;
  8b)   REPO=Qwen/Qwen3-Reranker-8B   REV=77d193c791ed757ca307ee72715aa132723da912 ;;
  *) echo "SIZE must be 0.6b, 4b or 8b"; exit 1 ;;
esac
W=$(mktemp -d); trap 'rm -rf "$W"' EXIT
hf download "$REPO" --revision "$REV" --local-dir "$W/m"
rm -rf "$W/m/.cache"
cp "$(dirname "$0")/qwen3_reranker.jinja" "$W/m/qwen3_reranker.jinja"   # MD5 60e2181d9eafc05c7fabf125abd6910a, as in the runs
ls -la "$W/m"
aws s3 sync --only-show-errors "$W/m/" "$DEST"
echo "uploaded $REPO@$REV to $DEST"
