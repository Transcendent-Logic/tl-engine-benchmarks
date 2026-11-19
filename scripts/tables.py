"""tables.py [--runs | --check | --write]: the README's tables, recomputed from the run folders in ../reports/ (Python 3.9+,
standard library only). With no option it prints them; --runs adds every run's own value in brackets; --check exits 1 if a table
in ../README.md differs from what the data gives; --write rewrites those tables (between <!-- table:NAME --> markers).

Every number is a mean over the runs of one configuration (three per configuration and size, except where a row says
otherwise), computed from the hammer's own report tables (<mode>.md) and per-request records (quality.requests.jsonl):
  - throughput: `speed` cells at 4 in flight and one request at a time (25 seconds each), and `hammer32k` (45 minutes at 2 in
    flight), as "API tok/s": the server's token count of the answered requests over wall time;
  - latency: `meticulous`, one 32K-token document sent alone (30 requests), and `speed`, 20 documents one at a time (25
    seconds of requests), each as the median time (from <mode>.md) and the mean time (from <mode>.requests.jsonl);
    `normal` and `hammer32k` percentiles;
  - quality: nDCG@10 per BEIR set from the per-request records, and agreement with each 16-bit run (see agreement()).
Which run feeds which table is in each folder's run.json ("used_in").
"""
import json
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reports")
SIZES = ["0.6B", "4B", "8B"]
CONFIGS = ["vllm-bf16", "vllm-fp8", "vllm-int8", "tl-engine"]
LABEL = {"vllm-bf16": "vLLM 16-bit", "vllm-fp8": "vLLM fp8", "vllm-int8": "vLLM int8", "tl-engine": "TL Engine"}
SHOW_RUNS = "--runs" in sys.argv


def md_tables(path):
    """Every Markdown table in a hammer report, with the ### section it sits in."""
    tables, section, cur = [], "", None
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if line.startswith("### "):
            section = line[4:].strip()
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cur is None:
                cur = {"section": section, "header": cells, "rows": []}
                tables.append(cur)
            elif not set("".join(cells)) <= set("-: "):
                cur["rows"].append(cells)
        else:
            cur = None
    return tables


def cell(run, mode, row, col, section=None):
    """One value from a mode's tables, as the hammer printed it, as a number (None if absent)."""
    path = os.path.join(ROOT, run["run"], f"{mode}.md")
    if not os.path.exists(path):
        return None
    for t in md_tables(path):
        if section and not t["section"].startswith(section):
            continue
        if col in t["header"]:
            j = t["header"].index(col)
            for r in t["rows"]:
                if r[0] == row and j < len(r):
                    m = re.match(r"[-\d,.]+", r[j])
                    return float(m.group(0).replace(",", "")) if m else None
    return None


def scores(run):
    """id -> (set, scores, ndcg) from quality.requests.jsonl, answered requests only."""
    out = {}
    for line in open(os.path.join(ROOT, run["run"], "quality.requests.jsonl"), encoding="utf-8"):
        q = json.loads(line)
        if q.get("scores"):
            out[q["id"]] = (q["set"], q["scores"], q.get("ndcg"))
    return out


def agreement(base, other):
    """Agreement of one run with one 16-bit run, as the mean of two shares: FiQA queries (300, 20 documents each) whose top
    document is the same, and hidden-passage requests (`ladder1-32768`: 50 single documents of about 32K tokens, a planted
    sentence in each) whose score is within 0.2. Over the requests both runs answered."""
    am = lambda s: max(range(len(s)), key=s.__getitem__)
    fq = [i for i in base if base[i][0] == "beir-fiqa" and i in other]
    nd = [i for i in base if base[i][0] == "ladder1-32768" and i in other]
    top = 100 * sum(am(base[i][1]) == am(other[i][1]) for i in fq) / len(fq)
    near = 100 * sum(all(abs(x - y) <= 0.2 for x, y in zip(base[i][1], other[i][1])) for i in nd) / len(nd)
    return (top + near) / 2


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def load_runs():
    runs = []
    for d in sorted(os.listdir(ROOT)):
        p = os.path.join(ROOT, d, "run.json")
        if os.path.exists(p):
            runs.append(json.load(open(p)))
    return runs


def mean_time(run, mode, cls):
    """Mean time of the answered requests of one request class (the hammer's `cls`) in a mode's per-request records."""
    ls = [d["latency"] for d in map(json.loads, open(os.path.join(ROOT, run["run"], f"{mode}.requests.jsonl"), encoding="utf-8"))
          if d["cls"] == cls and not d.get("error")]
    return sum(ls) / len(ls) if ls else None


def pick(runs, size, config, use, mode):
    return [r for r in runs if r["size"] == size and r["configuration"] == config and use in r.get("used_in", [])
            and os.path.exists(os.path.join(ROOT, r["run"], f"{mode}.md"))]


def fmt(v, kind):
    return "–" if v is None else f"${v:.4f}" if kind == "$" else f"{v:,.0f}" if kind == "t" else f"{v:.3f}" if kind == "s" else f"{v:.1f}%" if kind == "%" else f"{v:.3f}"


def values(rs, f, kind):
    vs = [f(r) for r in rs]
    m = mean(vs)
    return m, (fmt(m, kind) + (f" ({' / '.join(fmt(v, kind) for v in vs)})" if SHOW_RUNS else ""))


THROUGHPUT = [  # (label, mode, row, column)
    ("20 documents per request (`short20`), 4 in flight", "speed", "short20 ×4", "API tok/s"),
    ("100 documents of 256 tokens (`many100`), 4 in flight", "speed", "many100 ×4", "API tok/s"),
    ("One 8K-token document (`long8k`), 4 in flight", "speed", "long8k ×4", "API tok/s"),
    ("About 30K tokens in 3 to 55 documents (`pack32k`), 4 in flight", "speed", "pack32k ×4", "API tok/s"),
    ("About 31K tokens in 1 to 5 documents (`long32k`), 4 in flight", "speed", "long32k ×4", "API tok/s"),
    ("32K-token requests for 45 minutes (`hammer32k`), 2 in flight", "hammer32k", "all", "API tok/s"),
]
EXTRA = [  # not in the README's headline tables
    ("`hammer32k` median (s)", "hammer32k", "all", "p50 s", "s"),
    ("`hammer32k` 99th percentile (s)", "hammer32k", "all", "p99 s", "s"),
    ("`normal` mixed traffic, median (s)", "normal", "all", "p50 s", "s"),
    ("`normal` mixed traffic, 90th percentile (s)", "normal", "all", "p90 s", "s"),
    ("`normal` mixed traffic, 99th percentile (s)", "normal", "all", "p99 s", "s"),
]


def throughput(runs, size):
    out = ["| Request shape | vLLM 16-bit (tok/s) | TL Engine (tok/s) | TL Engine ÷ vLLM |", "|---|---|---|---|"]
    for label, mode, row, col in THROUGHPUT:
        a, at = values(pick(runs, size, "vllm-bf16", "throughput", mode), lambda r: cell(r, mode, row, col), "t")
        b, bt = values(pick(runs, size, "tl-engine", "throughput", mode), lambda r: cell(r, mode, row, col), "t")
        out.append(f"| {label} | {at} | {bt} | {b / a:.2f}× |")
    return out


def single(runs, size):
    out = ["| Request, sent alone | vLLM 16-bit (s) | TL Engine (s) | Faster by |", "|---|---|---|---|"]
    t32 = lambda r: cell(r, "meticulous", "32,768", "p50 s", "Single document")
    t20 = lambda r: cell(r, "speed", "short20 ×1", "p50 s")
    rows = [("One document of 32K tokens (`meticulous`, 30 requests): median time", "quality", "meticulous", t32),
            ("The same: mean time", "quality", "meticulous", lambda r: mean_time(r, "meticulous", "ladder1-32768")),
            ("20 documents per request (`speed` `short20 ×1`, 25 seconds of requests): median time", "throughput", "speed", t20),
            ("The same: mean time", "throughput", "speed", lambda r: mean_time(r, "speed", "short20 x1"))]
    for label, use, mode, f in rows:
        a, at = values(pick(runs, size, "vllm-bf16", use, mode), f, "s")
        b, bt = values(pick(runs, size, "tl-engine", use, mode), f, "s")
        out.append(f"| {label} | {at} | {bt} | {a / b:.2f}× |")
    return out


def quality(runs, size):
    base = [(r, scores(r)) for r in pick(runs, size, "vllm-bf16", "quality", "quality")]
    t32 = lambda r: cell(r, "meticulous", "32,768", "p50 s", "Single document")
    b32 = mean([t32(r) for r, _ in base])
    out = ["| Configuration | nDCG@10 FiQA | nDCG@10 SciFact | nDCG@10 ArguAna | Agreement with 16-bit | One 32K document (s) | Faster than 16-bit by |",
           "|---|---|---|---|---|---|---|"]
    for c in CONFIGS:
        rs = pick(runs, size, c, "quality", "quality")
        sc = {r["run"]: scores(r) for r in rs}
        nd = []
        for s in ("beir-fiqa", "beir-scifact", "beir-arguana"):
            nd.append(values(rs, lambda r: mean([v[2] for v in sc[r["run"]].values() if v[0] == s]), "n")[1])
        ag = [agreement(q, sc[r["run"]]) for r in rs for b, q in base if b["run"] != r["run"]]
        agt = fmt(mean(ag), "%") + (" (16-bit against itself)" if c == "vllm-bf16" else "")
        m32, t32t = values(rs, t32, "s")
        out.append(f"| {LABEL[c]} | " + " | ".join(nd) + f" | {agt} | {t32t} | {b32 / m32:.2f}× |")
    return out


def extra(runs, size):
    out = ["| Measure | vLLM 16-bit | TL Engine |", "|---|---|---|"]
    for label, mode, row, col, kind in EXTRA:
        a = values(pick(runs, size, "vllm-bf16", "throughput", mode), lambda r: cell(r, mode, row, col), kind)[1]
        b = values(pick(runs, size, "tl-engine", "throughput", mode), lambda r: cell(r, mode, row, col), kind)[1]
        out.append(f"| {label} | {a} | {b} |")
    return out


# Batch transform jobs (run.json "kind": "batch", measures in batch.json from scripts/batch/analyze.py). Prices: ml.g6.xlarge
# batch transform in eu-west-3 (Paris), $1.43024 an hour (AWS Price List API, read 2026-11-19); TL Engine's software fee on its
# AWS Marketplace listings, $0.30 an hour. Cost per million tokens is over the billed job (TransformStartTime to TransformEndTime).
BATCH_PRICE, BATCH_FEE = 1.43024, 0.30


def batch_runs(runs, size, config, conc):
    out = [r for r in runs if r.get("kind") == "batch" and r["size"] == size and r["configuration"] == config
           and r["max_concurrent_transforms"] == conc]
    for r in out:
        r.setdefault("_b", json.load(open(os.path.join(ROOT, r["run"], "batch.json"))))
    return out


def batch(runs, size):
    usd = lambda fee: (lambda r: (BATCH_PRICE + fee) * r["_b"]["job_s"] / 3600 / r["_b"]["tokens"] * 1e6)
    out = ["| MaxConcurrentTransforms | vLLM 16-bit (tok/s) | TL Engine (tok/s) | TL Engine ÷ vLLM | Billed job, vLLM 16-bit (s) "
           "| Billed job, TL Engine (s) | Finishes sooner by | $ per million tokens, vLLM 16-bit | $ per million tokens, TL Engine with its fee "
           "| TL Engine costs less by |", "|---|---|---|---|---|---|---|---|---|---|"]
    for conc, label in ((1, "1 (SageMaker's default)"), (4, "4")):
        va, vb = batch_runs(runs, size, "vllm-bf16", conc), batch_runs(runs, size, "tl-engine", conc)
        if not va or not vb:
            continue
        a, at = values(va, lambda r: r["_b"]["tok_s_processing"], "t")
        b, bt = values(vb, lambda r: r["_b"]["tok_s_processing"], "t")
        ja, jat = values(va, lambda r: r["_b"]["job_s"], "t")
        jb, jbt = values(vb, lambda r: r["_b"]["job_s"], "t")
        ca, cat = values(va, usd(0), "$")
        cb, cbt = values(vb, usd(BATCH_FEE), "$")
        out.append(f"| {label} | {at} | {bt} | {b / a:.2f}× | {jat} | {jbt} | {ja / jb:.2f}× | {cat} | {cbt} | {(1 - cb / ca) * 100:.1f}% |")
    return out


TABLES = [("throughput", "Peak throughput", throughput), ("single", "One request at a time", single), ("quality", "Quality", quality),
          ("load", "More load measures", extra), ("batch", "Batch transform jobs", batch)]


def main():
    runs = load_runs()
    if "--check" in sys.argv or "--write" in sys.argv:
        path = os.path.join(ROOT, "..", "README.md")
        text = open(path, encoding="utf-8").read()
        funcs = {name: f for name, _, f in TABLES}

        def fill(m):
            return m.group(1) + "\n" + "\n".join(funcs[m.group(2)](runs, m.group(3))) + "\n" + m.group(4)

        new = re.sub(r"(<!-- table:(\w+)-([\d.]+B) -->)(?s:.*?)(<!-- end -->)", fill, text)
        if "--write" in sys.argv:
            open(path, "w", encoding="utf-8").write(new)
            print("README.md tables written")
        else:
            print("README.md tables match the data" if new == text else "README.md tables DIFFER from the data")
            sys.exit(0 if new == text else 1)
        return
    for _, title, f in TABLES:
        print(f"## {title}\n")
        for size in SIZES:
            print(f"### {size}\n")
            print("\n".join(f(runs, size)) + "\n")


if __name__ == "__main__":
    main()
