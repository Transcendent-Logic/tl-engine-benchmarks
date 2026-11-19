#!/usr/bin/env python3
"""fetch_log.py GROUP STREAM: print every event of one CloudWatch log stream as JSON lines {"t": ms, "ingest": ms, "m": text},
oldest first, using the AWS CLI (profile and region from the environment)."""
import json
import subprocess
import sys

group, stream = sys.argv[1:3]
token = None
while True:
    cmd = ["aws", "logs", "get-log-events", "--log-group-name", group, "--log-stream-name", stream, "--start-from-head",
           "--output", "json"]
    if token:
        cmd += ["--next-token", token]
    d = json.loads(subprocess.run(cmd, check=True, capture_output=True, text=True).stdout)
    for e in d["events"]:
        print(json.dumps({"t": e["timestamp"], "ingest": e.get("ingestionTime"), "m": e["message"]}, ensure_ascii=False))
    if not d["events"] or d.get("nextForwardToken") == token:
        break
    token = d["nextForwardToken"]
