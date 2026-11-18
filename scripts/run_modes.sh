#!/usr/bin/env bash
# run_modes.sh ENDPOINT OUT SIZE: run the hammer's modes in $MODES against one SageMaker endpoint, one after another, with the
# per-size arguments of the benchmark runs, writing every mode's files and a `status` file to OUT. Run it on the client machine
# (the runs used a c7i.xlarge with Amazon Linux 2023 in the endpoint's region) from anywhere; it changes into ../hammer.
#   MODES='quality meticulous speed'   the runs behind the quality and single-request tables (and TL Engine's speed cells)
#   MODES='normal speed hammer32k'     vLLM 16-bit's load runs; TL Engine's load runs ran MODES='normal hammer32k'
# SIZE is 0.6b, 4b or 8b. Needs uv and AWS credentials allowed to invoke the endpoint (sagemaker:InvokeEndpoint).
#
# Made from the clients' wrapper scripts of 2026-11-16/17, without their probe requests between
# modes (single requests that checked the endpoint was idle; their results are the `probe` lines in each run's `status`, and
# they enter no table) and without their copying to S3. The wrappers of 2026-11-10 to 15 were not kept; what they ran (modes,
# arguments, order, times) is in each run's `status`, and the arguments below reproduce it, with one difference: the 0.6B runs
# on the first client (2026-11-10 to 13) passed no --timeout, so they ran with the hammer's default of 60 s instead of 75 s; their
# slowest request took 25 s, and SageMaker itself ends every invocation at 60 s. The full runs of 2026-11-10/11 (MODES unset)
# also ran `smoke` first and `burst` after `normal`; neither enters a table, so they are left out here.
set -euo pipefail
EP=${1:?ENDPOINT}; OUT=$(mkdir -p "${2:?OUT}" && cd "$2" && pwd); SIZE=${3:?SIZE}; REGION=${REGION:-eu-west-3}
export AWS_DEFAULT_REGION=$REGION
export RERANKER_API_URL=https://runtime.sagemaker.$REGION.amazonaws.com/endpoints/$EP/invocations
case $SIZE in
  # The 4B and 8B: model name and reference folder of their size; quality at 2 in flight (four 30K-token requests at once
  # take longer than SageMaker's 60-second limit on vLLM 16-bit); normal at 0.25 requests a second for 15 minutes.
  8b|4b) export RERANKER_MODEL=qwen3-reranker-$SIZE RERANKER_REFERENCE=qwen3-reranker-$SIZE; QC="--concurrency 2"
         NORMAL="--rate 0.25 --duration 900" ;;
  # The 0.6B: the hammer's defaults (model qwen3-reranker-0.6b, quality at 4 in flight, normal at 1.5 requests a second for 5 minutes)
  0.6b)  unset RERANKER_MODEL RERANKER_REFERENCE; QC=""; NORMAL="" ;;
  *) echo "SIZE must be 0.6b, 4b or 8b"; exit 1 ;;
esac
cd "$(dirname "$0")/../hammer"
echo "start $(date -u +%FT%TZ) endpoint=$EP hammer=195a09c+cleanup modes=${MODES:-default} model=${RERANKER_MODEL:-default} size=$SIZE" >> "$OUT/status"
vmstat -t 10 > "$OUT/client-vmstat.log" 2>/dev/null & VM=$!
for mode in ${MODES:-quality normal speed meticulous hammer32k}; do
  case $mode in quality) ARGS="$QC" ;; normal) ARGS="$NORMAL" ;; *) ARGS="" ;; esac
  echo "$mode start $(date -u +%FT%TZ) args: --timeout 75 $ARGS" >> "$OUT/status"
  set +e; uv run --with botocore scripts/hammer.py $mode --timeout 75 $ARGS --out "$OUT" --no-docs > "$OUT/$mode.stdout" 2>&1
  echo "$mode exit $? $(date -u +%FT%TZ)" >> "$OUT/status"; set -e
  [ $mode = speed ] && sleep 180   # the runs paused 3 minutes after speed, whose largest cells can leave the server busy
done
kill $VM 2>/dev/null || true
echo "done $(date -u +%FT%TZ)" >> "$OUT/status"
