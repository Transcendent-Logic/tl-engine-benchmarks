#!/usr/bin/env bash
# pack_vllm_weights.sh SIZE S3_URI: the weights of the vLLM 16-bit batch jobs as one model.tar.gz: Qwen3-Reranker-SIZE at the
# Hugging Face revision the runs used, plus the prompt template qwen3_reranker.jinja, the same files as the endpoint runs'
# uncompressed folder (../prepare_weights.sh). A batch job needs a tarball: SageMaker refuses a model whose container uses
# ModelDataSource ("SageMaker Batch currently doesn't support Model entity with container definitions which use
# ModelDataSource attribute"). S3_URI is the object to write, e.g. s3://<your bucket>/models/qwen3-reranker-4b/model.tar.gz.
# Needs the Hugging Face CLI (`hf`, from huggingface_hub), the AWS CLI and room for the model twice on local disk.
set -euo pipefail
SIZE=${1:?SIZE (0.6b, 4b or 8b)}; DEST=${2:?S3_URI}
case $SIZE in
  0.6b) REPO=Qwen/Qwen3-Reranker-0.6B REV=e61197ed45024b0ed8a2d74b80b4d909f1255473 ;;
  4b)   REPO=Qwen/Qwen3-Reranker-4B   REV=22e683669bc0f0bd69640a1354a6d0aebcfeede5 ;;
  8b)   REPO=Qwen/Qwen3-Reranker-8B   REV=77d193c791ed757ca307ee72715aa132723da912 ;;
  *) echo "SIZE must be 0.6b, 4b or 8b"; exit 1 ;;
esac
W=$(mktemp -d); trap 'rm -rf "$W"' EXIT
hf download "$REPO" --revision "$REV" --local-dir "$W/m"
rm -rf "$W/m/.cache"
cp "$(dirname "$0")/../qwen3_reranker.jinja" "$W/m/qwen3_reranker.jinja"
( cd "$W/m" && sha256sum * 2>/dev/null || shasum -a 256 * )   # each file's SHA-256, to compare with the run's
tar -C "$W/m" -czf "$W/model.tar.gz" .
aws s3 cp --only-show-errors "$W/model.tar.gz" "$DEST"
echo "uploaded $REPO@$REV as $DEST ($(wc -c < "$W/model.tar.gz") bytes)"
