#!/usr/bin/env python3
"""Build the input of a batch transform job: one rerank request per line (JSON Lines), the same body the hammer sends to an
endpoint ({"model", "query", "documents"}), so both containers get the request format of the endpoint benchmarks.

    python3 build_input.py --prepared <hammer>/data/prepared --size 4b --shape short20 --count 1800 --out DIR

- short20: the hammer's `short20` pool (beir-scifact, beir-fiqa, beir-arguana: 20 documents per request, about 5K to 12K
  tokens). long32k: the hammer's `long32k` pool (ladder1-32768 and 100 requests of each natural-* set, about 31K tokens).
- The pool is shuffled with SEED and repeated until COUNT requests; every query gets a nonce " #xxxxxxxx" like the hammer's
  speed modes, so no request repeats another and nothing is answered from a prefix cache. The nonces come from SEED, so the
  same arguments give the same file byte for byte, and both engines get identical input.
- Writes DIR/input/requests.jsonl (the job's input), DIR/index.jsonl (per line: set, id, labelled-relevant document
  positions, estimated tokens) and DIR/input.json (counts, estimated tokens, SHA-256 of the input).
The request sets come from the hammer's prepare.py (pinned sources, checked by SHA-256): ../../hammer/README.md.
"""
import argparse
import hashlib
import json
import random
from pathlib import Path

POOLS = {
    "short20": [("beir-scifact", None), ("beir-fiqa", None), ("beir-arguana", None)],
    "long32k": [("ladder1-32768", None), ("natural-2wikimqa", 100), ("natural-summ_screen_fd", 100), ("natural-qmsum", 100)],
}


def load(prepared: Path, name: str, limit):
    rows = []
    with open(prepared / f"{name}.jsonl") as f:
        for line in f:
            if limit is not None and len(rows) >= limit:
                break
            rows.append(json.loads(line))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prepared", type=Path, required=True)
    ap.add_argument("--size", choices=["0.6b", "4b", "8b"], required=True)
    ap.add_argument("--shape", choices=list(POOLS), default="short20")
    ap.add_argument("--count", type=int, required=True)
    ap.add_argument("--seed", type=int, default=20261119)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()

    pool = [r for name, limit in POOLS[a.shape] for r in load(a.prepared, name, limit)]
    rng = random.Random(a.seed)
    (a.out / "input").mkdir(parents=True, exist_ok=True)
    sha = hashlib.sha256()
    est = 0
    with open(a.out / "input" / "requests.jsonl", "w") as f, open(a.out / "index.jsonl", "w") as ix:
        order = []
        while len(order) < a.count:
            p = list(range(len(pool)))
            rng.shuffle(p)
            order += p
        for line, i in enumerate(order[: a.count]):
            r = pool[i]
            body = {"model": f"qwen3-reranker-{a.size}", "query": r["query"] + f" #{rng.getrandbits(32):08x}",
                    "documents": r["documents"]}
            s = json.dumps(body, ensure_ascii=False) + "\n"
            assert s.count("\n") == 1
            f.write(s)
            sha.update(s.encode())
            est += r.get("est_api_tokens", 0)
            ix.write(json.dumps({"line": line, "set": r["set"], "id": r["id"], "relevant": r.get("relevant", []),
                                 "docs": len(r["documents"]), "est_tokens": r.get("est_api_tokens", 0)}) + "\n")
    meta = {"size": a.size, "shape": a.shape, "count": a.count, "seed": a.seed, "pool": len(pool),
            "est_tokens": est, "sha256": sha.hexdigest(),
            "bytes": (a.out / "input" / "requests.jsonl").stat().st_size}
    (a.out / "input.json").write_text(json.dumps(meta, indent=1) + "\n")
    print(json.dumps(meta))


if __name__ == "__main__":
    main()
