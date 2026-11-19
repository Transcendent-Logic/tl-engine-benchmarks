#!/usr/bin/env python3
"""analyze.py RUN_DIR INDEX: measure one batch transform job from the files run_job.sh fetched in RUN_DIR, and write
RUN_DIR/batch.json (the measures) and RUN_DIR/per-request.jsonl (per request: set, id, tokens, every document's score, top
document, nDCG@10). INDEX is the index.jsonl that build_input.py wrote with the job's input. Prints a summary line.

From job.json (DescribeTransformJob): CreationTime, TransformStartTime, TransformEndTime.
From the container log (logs/<instance>.jsonl, CloudWatch timestamps): the processing window, from the first to the last
"POST /invocations" access-log line, and the status of every invocation.
From the data log (logs/data-log.jsonl): SageMaker's own settings line (MaxConcurrentTransforms, MaxPayloadInMB, BatchStrategy)
and any error lines.
From the output (output/*.out, one response per input line, in input order): tokens (sum of usage.total_tokens), responses that
are not a ranking, and per request the top document and nDCG@10 against the labels in the input's index.jsonl.
CloudWatch stamps the access-log lines as the agent ships them (about once a second), so the window is good to about 1 s.
"""
import json
import math
import re
import sys
from datetime import datetime
from pathlib import Path

PRICE = 1.43024  # USD per hour, SageMaker batch transform ml.g6.xlarge, eu-west-3 (AWS Price List API, read 2026-11-19)
FEE = 0.30       # USD per hour, TL Engine's software fee on its AWS Marketplace listings
ACCESS = re.compile(r'"POST /invocations HTTP/1\.1" (\d{3})')


def ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()


def ndcg10(scores, relevant):
    order = sorted(range(len(scores)), key=lambda i: -scores[i])[:10]
    dcg = sum(1 / math.log2(r + 2) for r, i in enumerate(order) if i in relevant)
    idcg = sum(1 / math.log2(r + 2) for r in range(min(10, len(relevant))))
    return dcg / idcg if idcg else 0.0


def analyze(run: Path, index_file: Path):
    job = json.loads((run / "job.json").read_text())
    created, start, end = (ts(job[k]) for k in ("CreationTime", "TransformStartTime", "TransformEndTime"))
    container = [p for p in (run / "logs").glob("*.jsonl") if p.name != "data-log.jsonl"]
    inv, statuses = [], {}
    for p in container:
        for line in p.open():
            e = json.loads(line)
            m = ACCESS.search(e["m"])
            if m:
                inv.append(e["t"] / 1000)
                statuses[m[1]] = statuses.get(m[1], 0) + 1
    settings, data_errors = None, []
    dl = run / "logs" / "data-log.jsonl"
    if dl.exists():
        for line in dl.open():
            m = json.loads(line)["m"]
            if "MaxConcurrentTransforms=" in m:
                settings = m.split("]: ", 1)[-1].strip()
            elif re.search(r"error|fail|exception", m, re.I):
                data_errors.append(m.strip()[:300])
    index = [json.loads(l) for l in index_file.open()]
    outs = sorted((run / "output").glob("*.out"))
    responses = [l for p in outs for l in p.open() if l.strip()]
    tokens, bad, per = 0, 0, []
    for i, l in enumerate(responses):
        try:
            d = json.loads(l)
            res = d["results"]
            tok = d["usage"]["total_tokens"]
            tokens += tok
        except Exception:
            bad += 1
            continue
        scores = [0.0] * len(res)
        for r in res:
            scores[r["index"]] = r["relevance_score"]
        ix = index[i] if i < len(index) else {}
        per.append({"line": i, "set": ix.get("set"), "id": ix.get("id"), "tokens": tok, "top": res[0]["index"],
                    "ndcg": ndcg10(scores, set(ix.get("relevant", []))), "scores": scores})
    window = (max(inv) - min(inv)) if inv else None
    job_s = end - start
    out = {
        "job": job["TransformJobName"], "status": job["TransformJobStatus"],
        "max_concurrent": job.get("MaxConcurrentTransforms"), "settings_line": settings,
        "created": job["CreationTime"], "start": job["TransformStartTime"], "end": job["TransformEndTime"],
        "create_to_end_s": round(end - created, 1), "job_s": round(job_s, 1),
        "first_invocation": datetime.utcfromtimestamp(min(inv)).isoformat() + "Z" if inv else None,
        "last_invocation": datetime.utcfromtimestamp(max(inv)).isoformat() + "Z" if inv else None,
        "processing_s": round(window, 1) if window else None,
        "startup_s": round(min(inv) - start, 1) if inv else None,
        "invocations": len(inv), "invocation_status": statuses, "input_lines": len(index),
        "responses": len(responses), "bad_responses": bad, "data_log_errors": data_errors[:20],
        "tokens": tokens,
        "tok_s_processing": round(tokens / window, 1) if window else None,
        "tok_s_job": round(tokens / job_s, 1),
        "usd_per_m_tokens_job": round(PRICE * job_s / 3600 / tokens * 1e6, 5) if tokens else None,
        "usd_per_m_tokens_job_with_fee": round((PRICE + FEE) * job_s / 3600 / tokens * 1e6, 5) if tokens else None,
        "ndcg10": {s: round(sum(p["ndcg"] for p in per if p["set"] == s) / max(1, sum(p["set"] == s for p in per)), 4)
                   for s in sorted({p["set"] for p in per if p["set"]})},
    }
    (run / "batch.json").write_text(json.dumps(out, indent=1) + "\n")
    with open(run / "per-request.jsonl", "w") as f:
        for p in per:
            f.write(json.dumps(p) + "\n")
    return out


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    if True:
        o = analyze(Path(sys.argv[1]), Path(sys.argv[2]))
        print(json.dumps({k: o[k] for k in ("job", "status", "settings_line", "job_s", "startup_s", "processing_s",
                                             "invocations", "invocation_status", "responses", "bad_responses", "tokens",
                                             "tok_s_processing", "tok_s_job", "ndcg10")}))
