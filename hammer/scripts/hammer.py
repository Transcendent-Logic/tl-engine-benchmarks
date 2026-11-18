"""Load-test and validate a reranking endpoint with the prepared request sets.

    export RERANKER_API_URL=https://runtime.sagemaker.<region>.amazonaws.com/endpoints/<name>/invocations
    # correctness
    uv run --with botocore scripts/hammer.py smoke         # < 1 min   alive, answers correctly, no timeouts
    # quality
    uv run --with botocore scripts/hammer.py quality       # < 15 min  ranking quality vs labels and the vanilla model
    # reliability
    uv run --with botocore scripts/hammer.py normal        # 5 min     realistic mixed traffic at a steady rate
    uv run --with botocore scripts/hammer.py burst         # < 10 min  bursts of simultaneous requests, latency
    uv run --with botocore scripts/hammer.py hammer32k     # < 1 h     continuous 32K-token requests
    # speed
    uv run --with botocore scripts/hammer.py speed         # < 15 min  throughput per request class x concurrency
    uv run --with botocore scripts/hammer.py meticulous    # < 25 min  latency/speed vs length, doc count, concurrency, cache
    uv run --with botocore scripts/hammer.py all           # everything, in that order

Each mode writes <out>/<mode>.md (+ .json per-request records, .png charts) and appends the
markdown to $GITHUB_STEP_SUMMARY under GitHub Actions. Exit status 1 when the mode's checks fail.
Every request is also appended to <out>/<mode>.requests.jsonl the moment it finishes (with its
send time and, if it failed, the response body), so a run that dies half-way keeps every
finished request.

RERANKER_API_URL (required) is where every request goes: {"model", "query", "documents"} as JSON,
answered with {"results": [{"index", "relevance_score"}, ...], "usage": {"total_tokens"}}. A SageMaker
endpoint (https://runtime.sagemaker.<region>.amazonaws.com/endpoints/<name>/invocations) gets
AWS-signed requests, with credentials from the usual AWS chain; that needs botocore, hence
`uv run --with botocore`. Any other URL gets plain unauthenticated requests.
RERANKER_MODEL sets the "model" field ("" omits it) and RERANKER_REFERENCE the folder under
reference/ that `quality` compares with (default qwen3-reranker-0.6b for both).

A server may cache prompt prefixes, so that a repeated (query, document) answers much faster
whatever its length. Speed modes therefore append a random nonce to every query (--no-nonce to
disable); `meticulous` measures cold vs cached explicitly.

The column "API tok/s" is the server's own token count (usage.total_tokens, recorded per request as
"billed") over successful requests, divided by wall time.
"""

import argparse
import asyncio
import collections
import itertools
import json
import math
import os
import random
import re
import statistics
import sys
import time
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path

import httpx

from report import Report, pct, ranking_metrics

ROOT = Path(__file__).resolve().parent.parent
PREPARED = ROOT / "data" / "prepared"
REFERENCE = ROOT / "reference" / os.environ.get("RERANKER_REFERENCE", "qwen3-reranker-0.6b")
API_URL = os.environ.get("RERANKER_API_URL") or sys.exit("RERANKER_API_URL is not set (see the docstring)")
MODEL = os.environ.get("RERANKER_MODEL", "qwen3-reranker-0.6b")  # "" leaves "model" out of the requests
# A SageMaker endpoint takes AWS-signed requests instead of an API key (group 1: the region).
SAGEMAKER = re.match(r"https://runtime\.sagemaker\.([a-z0-9-]+)\.amazonaws\.com/", API_URL)
LOG = None  # open file, set in main(): one JSON line per request, written the moment it finishes
LADDER = [256, 512, 1024, 2048, 4096, 8192, 16384, 32768]

# Request classes: pools drawn from the prepared sets as (set, max requests to load).
CLASSES = {
    "short20": [("beir-scifact", None), ("beir-fiqa", None), ("beir-arguana", None)],  # 20 docs, 4-14K tokens
    "many100": [("ladder-256", None)],  # 100 x 256-token docs, ~29K tokens
    "mid1k": [("ladder1-1024", None)],
    "mid4k": [("ladder1-4096", None)],
    "long8k": [("ladder1-8192", None)],
    "pack32k": [(f"ladder-{n}", None) for n in (512, 1024, 2048, 4096, 8192)],  # ~30K tokens in 3-55 docs
    "long32k": [("ladder1-32768", None), ("natural-2wikimqa", 100),
                ("natural-summ_screen_fd", 100), ("natural-qmsum", 100)],  # ~31K tokens in 1-5 docs
}

_sets: dict = {}


def load_set(name: str, limit: int | None = None) -> list[dict]:
    if (name, limit) not in _sets:
        rows = []
        with open(PREPARED / f"{name}.jsonl") as f:
            for line in f:
                if limit is not None and len(rows) >= limit:
                    break
                rows.append(json.loads(line))
        _sets[name, limit] = rows
    return _sets[name, limit]


def pool(cls: str, rng: random.Random | None = None) -> list[dict]:
    reqs = [r for name, limit in CLASSES[cls] for r in load_set(name, limit)]
    if rng:
        rng.shuffle(reqs)
    return reqs


# --- client ---------------------------------------------------------------------------------


@dataclass
class Result:
    cls: str
    set: str
    id: str
    docs: int
    est_tokens: int
    start: float  # seconds since the client was created
    latency: float
    status: int | None = None
    error: str | None = None
    billed: int | None = None
    rank: int | None = None  # 1-based rank of the first relevant document
    ndcg: float | None = None
    top_score: float | None = None
    scores: list | None = None
    ts: float | None = None  # wall clock (Unix seconds) when the request was sent, to match server logs
    detail: str | None = None  # a failed request's response body (first 2000 characters)
    request_id: str | None = None  # a failed request's x-amzn-RequestId, if any

    @property
    def ok(self) -> bool:
        return self.error is None


def validate(data, n_docs: int) -> str | None:
    if not isinstance(data, dict) or not isinstance(data.get("results"), list):
        return "no results list"
    results = data["results"]
    if len(results) != n_docs:
        return f"{len(results)} results for {n_docs} documents"
    try:
        idx = [r["index"] for r in results]
        scores = [r["relevance_score"] for r in results]
    except (KeyError, TypeError):
        return "malformed result entry"
    if sorted(idx) != list(range(n_docs)):
        return "indices are not a permutation of the documents"
    if not all(isinstance(s, (int, float)) and 0 <= s <= 1 for s in scores):
        return "score outside [0, 1]"
    if any(scores[i] < scores[i + 1] for i in range(len(scores) - 1)):
        return "results not sorted by score"
    if not isinstance(data.get("usage", {}).get("total_tokens"), int):
        return "no usage.total_tokens"
    return None


class SigV4(httpx.Auth):
    """Signs every request for SageMaker with credentials from the usual AWS chain (instance role,
    profile, environment). Needs botocore: `uv run --with botocore scripts/hammer.py ...`."""
    requires_request_body = True
    _creds = None  # looked up once, shared by every Client; botocore refreshes them itself

    def __init__(self, region: str):
        import botocore.session
        from botocore.auth import SigV4Auth
        from botocore.awsrequest import AWSRequest
        if SigV4._creds is None:
            SigV4._creds = botocore.session.Session().get_credentials() or sys.exit("no AWS credentials found")
        self.region, self.signer, self.request = region, SigV4Auth, AWSRequest

    def auth_flow(self, request):
        aws = self.request(method=request.method, url=str(request.url), data=request.content,
                           headers={"Content-Type": request.headers["content-type"]})
        self.signer(SigV4._creds.get_frozen_credentials(), "sagemaker", self.region).add_auth(aws)
        request.headers.update(dict(aws.headers))
        yield request


def error_label(status: int, data, headers) -> str:
    """Short name of a failed answer, as grouped in the error tables. SageMaker wraps every failure
    of the container in a 424, so say which kind it was: its own 60 s cut-off, or the container's
    status (400 for an over-long input, 5xx for a crash)."""
    label = f"http {status}"
    if isinstance(data, dict) and isinstance(data.get("error"), dict) and data["error"].get("code"):
        label += f" {data['error']['code']}"
    if kind := (headers or {}).get("x-amzn-errortype", "").split(":")[0]:
        label += f" {kind}"
    if isinstance(data, dict) and "timed out" in str(data.get("Message", "")):
        label += " timed out at SageMaker"
    elif isinstance(data, dict) and data.get("OriginalStatusCode") is not None:
        label += f" container {data['OriginalStatusCode']}"
    return label


class Client:
    def __init__(self, concurrency: int = 8, timeout: float = 60.0, nonce: bool = False, keep_scores=False):
        headers = {"Content-Type": "application/json", "User-Agent": "tl-engine-benchmarks-hammer/0.1"}
        self.http = httpx.AsyncClient(
            headers=headers, auth=SigV4(SAGEMAKER[1]) if SAGEMAKER else None,
            timeout=httpx.Timeout(timeout, connect=10.0),
            limits=httpx.Limits(max_connections=concurrency + 8, max_keepalive_connections=concurrency + 8))
        self.t0 = time.perf_counter()
        self.nonce, self.keep_scores = nonce, keep_scores

    async def close(self):
        await self.http.aclose()

    async def raw(self, body: dict) -> tuple[int | None, object, float]:
        """POST anything; returns (status, parsed JSON or error name, latency)."""
        return (await self.post(body))[:3]

    async def post(self, body: dict) -> tuple:
        """As raw(), plus the response text and headers when the answer is not a 200 (else None)."""
        t = time.perf_counter()
        try:
            r = await self.http.post(API_URL, json=body)
        except httpx.TimeoutException:
            return None, "timeout", time.perf_counter() - t, None, None
        except httpx.HTTPError as e:
            return None, type(e).__name__, time.perf_counter() - t, None, None
        latency = time.perf_counter() - t
        try:
            data = r.json()
        except ValueError:
            data = None
        failed = r.status_code != 200
        return (r.status_code, data, latency,
                r.text[:2000] if failed else None, dict(r.headers) if failed else None)

    async def send(self, req: dict, cls: str = "") -> Result:
        res = await self._send(req, cls)
        if LOG:  # on disk before anything else can go wrong; the report is only written when a mode ends
            LOG.write(json.dumps(asdict(res)) + "\n")
            LOG.flush()
        return res

    async def _send(self, req: dict, cls: str = "") -> Result:
        query = req["query"] + (f" #{uuid.uuid4().hex[:8]}" if self.nonce else "")
        res = Result(cls=cls, set=req.get("set", ""), id=req.get("id", ""), docs=len(req["documents"]),
                     est_tokens=req.get("est_api_tokens", 0), start=time.perf_counter() - self.t0, latency=0.0,
                     ts=time.time())
        status, data, res.latency, res.detail, headers = await self.post(
            {**({"model": MODEL} if MODEL else {}), "query": query, "documents": req["documents"]})
        res.status = status
        if status is None:
            res.error = data
            return res
        if status != 200:
            res.error, res.request_id = error_label(status, data, headers), headers.get("x-amzn-requestid")
            return res
        if err := validate(data, res.docs):
            res.error = "invalid: " + err
            return res
        res.billed = data["usage"]["total_tokens"]
        scores = [0.0] * res.docs
        for r in data["results"]:
            scores[r["index"]] = r["relevance_score"]
        res.top_score = max(scores)
        if req.get("relevant"):
            res.ndcg, rr = ranking_metrics(scores, req["relevant"])
            res.rank = round(1 / rr) if rr else None
        if self.keep_scores:
            res.scores = scores
        return res


# --- load patterns --------------------------------------------------------------------------


async def closed_loop(client, reqs, concurrency, duration=None, cls="") -> list[Result]:
    """`concurrency` workers each always have one request in flight. Runs through `reqs` once, or
    cycles through them for `duration` seconds."""
    it = itertools.cycle(reqs) if duration else iter(reqs)
    deadline = time.perf_counter() + duration if duration else math.inf
    results = []

    async def worker():
        while time.perf_counter() < deadline and (req := next(it, None)) is not None:
            results.append(await client.send(req, cls))

    await asyncio.gather(*[worker() for _ in range(concurrency)])
    return results


async def open_loop(client, sample, rate, duration, max_inflight=64) -> tuple[list[Result], int]:
    """Poisson arrivals at `rate`/s for `duration` seconds; `sample()` yields (request, class).
    Arrivals beyond `max_inflight` in-flight requests are shed and counted instead of queued."""
    results, tasks, shed = [], set(), 0
    rng = random.Random(0)
    deadline = time.perf_counter() + duration

    async def one(req, cls):
        results.append(await client.send(req, cls))

    while time.perf_counter() < deadline:
        await asyncio.sleep(rng.expovariate(rate))
        if len(tasks) >= max_inflight:
            shed += 1
            continue
        task = asyncio.create_task(one(*sample()))
        tasks.add(task)
        task.add_done_callback(tasks.discard)
    await asyncio.gather(*tasks)
    return results, shed


async def burst(client, reqs, cls="") -> list[Result]:
    return list(await asyncio.gather(*[client.send(r, cls) for r in reqs]))


# --- summaries ------------------------------------------------------------------------------

SUMMARY_COLS = ["", "requests", "errors", "p50 s", "p90 s", "p99 s", "max s", "req/s", "API tok/s", "MRR"]


def summarize(results: list[Result], wall: float | None = None) -> dict:
    """Percentiles are over successful requests; `err_pct` counts every failure."""
    ok = [r for r in results if r.ok]
    lat = [r.latency for r in ok]
    if wall is None:
        wall = max((r.start + r.latency for r in results), default=0) - min((r.start for r in results), default=0)
    labelled = [r for r in ok if r.ndcg is not None]
    n_err = len(results) - len(ok)
    return {
        "n": len(results), "ok": len(ok), "err_pct": 100 * n_err / max(1, len(results)),
        "errors": f"{n_err} ({100 * n_err / max(1, len(results)):.1f}%)",
        "p50": pct(lat, 50), "p90": pct(lat, 90), "p99": pct(lat, 99), "max": max(lat, default=math.nan),
        "mean": statistics.fmean(lat) if lat else math.nan,
        "rps": len(ok) / wall if wall else math.nan,
        "tps": sum(r.billed for r in ok) / wall if wall else math.nan,
        "billed": sum(r.billed for r in ok),
        "mrr": statistics.fmean(1 / r.rank if r.rank else 0 for r in labelled) if labelled else math.nan,
        "ndcg": statistics.fmean(r.ndcg for r in labelled) if labelled else math.nan,
    }


def summary_row(label: str, s: dict) -> list:
    return [label, s["n"], s["errors"], s["p50"], s["p90"], s["p99"], s["max"], s["rps"], s["tps"], s["mrr"]]


def errors(rep: Report, results: list[Result]):
    counts = collections.Counter(r.error for r in results if not r.ok)
    if counts:
        def first(e):  # the first request that failed this way, and what the server said
            r = next(r for r in results if r.error == e)
            return [f"{r.set} {r.id}", " ".join((r.detail or "").replace("|", "/").split())[:300]]
        rep.table(["error", "count", "example", "response"], [[e, n, *first(e)] for e, n in counts.most_common()])


def timeline(rep: Report, results: list[Result], bucket: float, title: str):
    """Latency percentiles and throughput per time bucket."""
    buckets = collections.defaultdict(list)
    for r in results:
        buckets[int(r.start // bucket)].append(r)
    keys = sorted(buckets)
    stats = [summarize(buckets[k], bucket) for k in keys]
    x = [f"{k * bucket / 60:g}" for k in keys]
    rep.chart(title, x, [("p50", [s["p50"] for s in stats]), ("p90", [s["p90"] for s in stats]),
                         ("max", [s["max"] for s in stats])], "latency s", x_label="minute")
    rep.chart(title.replace("Latency", "Throughput"), x,
              [("API tokens/s ÷ 1000", [s["tps"] / 1000 for s in stats]), ("errors", [s["n"] - s["ok"] for s in stats])],
              "", x_label="minute")


# --- modes ----------------------------------------------------------------------------------


# One request per set for the smoke check, chosen (by index into the deterministic prepared set) so
# that the vanilla model ranks the labelled document first by a wide margin: the first SciFact request
# is one the model cannot answer at all (every score ~0.001), so its rank is noise.
SMOKE_REQUESTS = {"beir-scifact": 12, "ladder1-256": 0, "ladder-256": 0, "ladder1-32768": 0, "natural-qmsum": 0}


async def mode_smoke(args, rep):
    client = Client(concurrency=4, timeout=min(args.timeout, 15))
    rows, passed = [], True

    def check(name, ok, latency, detail=""):
        nonlocal passed
        passed &= bool(ok)
        rows.append([name, bool(ok), latency, detail])

    sanity = {"query": "What is the capital of France?", "relevant": [0], "set": "sanity", "id": "france",
              "documents": ["Paris is the capital of France.", "Berlin is the capital of Germany.",
                            "London is the capital of the United Kingdom."]}
    r = await client.send(sanity, "sanity")
    check("sanity: Paris first with score > 0.9", r.ok and r.rank == 1 and r.top_score > 0.9, r.latency,
          r.error or f"top score {r.top_score:.4f}")
    results = [r]
    for name, idx in SMOKE_REQUESTS.items():
        r = await client.send(load_set(name, idx + 1)[idx], name)
        results.append(r)
        check(f"{name}: {r.docs} docs, {r.est_tokens:,} tokens → valid, relevant doc in top 3",
              r.ok and r.rank is not None and r.rank <= 3, r.latency, r.error or f"rank {r.rank}, billed {r.billed:,}")
    slowest = max(row[2] for row in rows)
    check("every response under 10 s", slowest < 10, slowest, f"slowest {slowest:.2f} s")
    rep.table(["check", "ok", "latency s", "detail"], rows)
    await client.close()
    return passed, results


async def mode_normal(args, rep):
    duration, rate = args.duration or 300, args.rate
    mix = [("short20", 60), ("many100", 10), ("mid1k", 10), ("mid4k", 10), ("long8k", 5), ("long32k", 5)]
    rng = random.Random(args.seed)
    pools = {c: pool(c) for c, _ in mix}

    def sample():
        c = rng.choices([c for c, _ in mix], [w for _, w in mix])[0]
        return rng.choice(pools[c]), c

    client = Client(concurrency=64, timeout=args.timeout, nonce=not args.no_nonce)
    results, shed = await open_loop(client, sample, rate, duration)
    await client.close()
    s = summarize(results, duration)
    rep.p(f"{duration / 60:g} min of Poisson traffic at {rate:g} req/s; mix "
          + ", ".join(f"{c} {w}%" for c, w in mix) + f". Billed {s['billed']:,} tokens."
          + (f" **{shed} arrivals shed** (64 already in flight)." if shed else ""))
    rep.table(SUMMARY_COLS, [summary_row("all", s)]
              + [summary_row(c, summarize([r for r in results if r.cls == c], duration)) for c, _ in mix])
    errors(rep, results)
    timeline(rep, results, 30, "Latency over time")
    return s["err_pct"] <= args.max_error_rate and not shed, results


async def mode_speed(args, rep):
    classes, levels = ["short20", "many100", "long8k", "pack32k", "long32k"], [1, 4, 16]
    rows, cells, results = [], {}, []
    for c in classes:
        reqs = pool(c, random.Random(args.seed))
        for n in levels:
            client = Client(concurrency=n, timeout=args.timeout, nonce=not args.no_nonce)
            t = time.perf_counter()
            res = await closed_loop(client, reqs, n, duration=args.cell_seconds, cls=f"{c} x{n}")
            await client.close()
            cells[c, n] = s = summarize(res, time.perf_counter() - t)
            rows.append(summary_row(f"{c} ×{n}", s))
            results += res
            await asyncio.sleep(2)
    s = summarize(results)
    rep.p(f"Closed loop, {args.cell_seconds:g} s per cell, {len(classes)} request classes × concurrency {levels}. "
          f"{s['n']} requests, {s['billed']:,} tokens billed.")
    rep.table(SUMMARY_COLS, rows)
    errors(rep, results)
    x = [f"×{n}" for n in levels]
    rep.chart("Throughput vs concurrency", x, [(c, [cells[c, n]["tps"] / 1000 for n in levels]) for c in classes],
              "API tokens/s ÷ 1000", x_label="concurrency")
    rep.chart("Requests/s vs concurrency", x, [(c, [cells[c, n]["rps"] for n in levels]) for c in classes],
              "req/s", x_label="concurrency")
    rep.chart("p50 latency vs concurrency", x, [(c, [cells[c, n]["p50"] for n in levels]) for c in classes],
              "s", x_label="concurrency")
    return s["err_pct"] <= args.max_error_rate, results


async def mode_burst(args, rep):
    plan = [("short20", [10, 25, 50, 100, 200]), ("long32k", [4, 8, 16, 32])]
    rows, per_class, results = [], {}, []
    for c, sizes in plan:
        reqs, pos = pool(c, random.Random(args.seed)), 0
        for n in sizes:
            batch = [reqs[(pos + i) % len(reqs)] for i in range(n)]
            pos += n
            client = Client(concurrency=n, timeout=args.timeout, nonce=not args.no_nonce)
            t = time.perf_counter()
            res = await burst(client, batch, f"{c} burst {n}")
            wall = time.perf_counter() - t
            await client.close()
            s = summarize(res, wall)
            per_class.setdefault(c, []).append((n, s, res))
            rows.append([f"{c} burst {n}", n, s["ok"], s["errors"], wall, s["p50"], s["p90"], s["max"], s["tps"]])
            results += res
            await asyncio.sleep(5)
    s = summarize(results)
    rep.p(f"Each burst fires all its requests at once and waits for every answer (5 s pause between bursts). "
          f"{s['n']} requests, {s['billed']:,} tokens billed. Latencies are over served requests.")
    rep.table(["burst", "requests", "served", "errors", "all done s", "p50 s", "p90 s", "max s", "API tok/s"], rows)
    errors(rep, results)
    for c, items in per_class.items():
        rep.chart(f"{c}: latency vs burst size", [n for n, _, _ in items],
                  [(k, [s[k] for _, s, _ in items]) for k in ("p50", "p90", "max")], "s",
                  x_label="simultaneous requests")
    n, _, res = per_class["short20"][-1]
    done = sorted((r for r in res if r.ok), key=lambda r: r.start + r.latency)
    step = max(1, len(done) // 50)
    rep.chart(f"short20 burst of {n}: latency by completion order", [i + 1 for i in range(0, len(done), step)],
              [("latency", [r.latency for r in done[::step]])], "s", x_label="completed request #")
    rep.chart("Served and failed per burst", [row[0] for row in rows],
              [("served", [row[2] for row in rows]), ("errors", [int(row[3].split()[0]) for row in rows])],
              "requests", kind="bar")
    return s["err_pct"] <= args.max_error_rate, results


async def mode_meticulous(args, rep):
    client = Client(concurrency=1, timeout=args.timeout, nonce=True)
    results = []
    rep.p("Sequential requests (one in flight) unless stated; every query carries a nonce so nothing is served "
          "from a prefix cache.")

    rep.h("Single document: latency vs length")
    rows, stats = [], []
    for n in LADDER:
        reqs = load_set(f"ladder1-{n}")[:args.per_rung]
        res = await closed_loop(client, reqs, 1, cls=f"ladder1-{n}")
        results += res
        s = summarize(res)
        stats.append(s)
        rows.append([n, int(statistics.median(r["doc_tokens"][0] for r in reqs)), s["billed"] / max(1, s["ok"]),
                     s["errors"], s["p50"], s["p90"], s["max"], s["tps"]])
    rep.table(["rung", "Qwen tokens", "billed", "errors", "p50 s", "p90 s", "max s", "API tok/s"], rows)
    rep.chart("Single document: latency vs length", LADDER, [("p50", [s["p50"] for s in stats]), ("p90", [s["p90"] for s in stats])],
              "s", x_label="document length (designed tokens)")
    rep.chart("Single document: throughput vs length", LADDER, [("API tokens/s ÷ 1000", [s["tps"] / 1000 for s in stats])],
              "", x_label="document length (designed tokens)")

    rep.h("~30K tokens per request: latency vs document length (fewer, longer documents)")
    rows, stats = [], []
    for n in LADDER:
        reqs = load_set(f"ladder-{n}")[:max(5, args.per_rung // 2)]
        res = await closed_loop(client, reqs, 1, cls=f"ladder-{n}")
        results += res
        s = summarize(res)
        stats.append(s)
        rows.append([n, res[0].docs, s["billed"] / max(1, s["ok"]), s["errors"], s["p50"], s["p90"], s["max"], s["tps"]])
    rep.table(["rung", "docs/request", "billed", "errors", "p50 s", "p90 s", "max s", "API tok/s"], rows)
    rep.chart("~30K tokens: latency vs document length", LADDER,
              [("p50", [s["p50"] for s in stats]), ("p90", [s["p90"] for s in stats])], "s", x_label="document length")

    rep.h("Latency vs number of documents")

    def tiny(n, i):
        hit = i % n
        return {"query": "Which document mentions Paris?", "relevant": [hit], "set": "tiny", "id": f"tiny{n}/{i}",
                "documents": [f"Document {j} mentions {'Paris' if j == hit else 'a city'}." for j in range(n)]}

    def subset(req, n, i):
        rel = req["relevant"][0]
        rng = random.Random(i)
        idx = [rel] + rng.sample([j for j in range(len(req["documents"])) if j != rel], n - 1)
        rng.shuffle(idx)
        return {"query": req["query"], "relevant": [idx.index(rel)], "set": req["set"], "id": f"{req['id']}/{n}",
                "documents": [req["documents"][j] for j in idx]}

    base = load_set("ladder-256")
    scan = [(f"{n} tiny", [tiny(n, i) for i in range(10)]) for n in (1, 10, 100, 1000)]
    scan += [(f"{n}×256", [subset(base[i], n, i) for i in range(10)]) for n in (1, 10, 50, 100)]
    rows, stats = [], []
    for label, reqs in scan:
        res = await closed_loop(client, reqs, 1, cls=f"docs {label}")
        results += res
        s = summarize(res)
        stats.append(s)
        rows.append([label, s["billed"] / max(1, s["ok"]), s["errors"], s["p50"], s["p90"], s["max"], s["mrr"]])
    rep.table(["documents", "billed", "errors", "p50 s", "p90 s", "max s", "MRR"], rows)
    rep.chart("Latency vs number of documents", [l for l, _ in scan],
              [("p50", [s["p50"] for s in stats]), ("p90", [s["p90"] for s in stats])], "s", x_label="documents per request")

    rep.h("Cold vs cached: the same single-document request sent twice in a row")
    rep.p("A server that caches prompt prefixes skips most of the compute for a repeated (query, document) pair. "
          "Cold = fresh nonce in the query; cached = the identical request again immediately after.")
    plain = Client(concurrency=1, timeout=args.timeout)
    rows, cold_s, warm_s = [], [], []
    for n in LADDER:
        cold, warm = [], []
        for req in load_set(f"ladder1-{n}")[:max(5, args.per_rung // 3)]:
            q = dict(req, query=req["query"] + f" #{uuid.uuid4().hex[:8]}")
            cold.append(await plain.send(q, f"cold {n}"))
            warm.append(await plain.send(q, f"cached {n}"))
        results += cold + warm
        sc, sw = summarize(cold), summarize(warm)
        cold_s.append(sc)
        warm_s.append(sw)
        rows.append([n, len(cold), sc["p50"], sw["p50"], sc["p50"] / sw["p50"] if sw["p50"] else math.nan,
                     sc["max"], sw["max"], sc["errors"] if sc["n"] - sc["ok"] or sw["n"] - sw["ok"] else ""])
    await plain.close()
    rep.table(["rung", "pairs", "cold p50 s", "cached p50 s", "speed-up ×", "cold max s", "cached max s", "errors"], rows)
    rep.chart("Cold vs cached latency vs document length", LADDER,
              [("cold p50", [s["p50"] for s in cold_s]), ("cached p50", [s["p50"] for s in warm_s])], "s",
              x_label="document length (designed tokens)")

    rep.h("short20: latency and throughput vs concurrency")
    levels = [1, 2, 4, 8, 16, 32]
    reqs = pool("short20", random.Random(args.seed))
    rows, stats = [], []
    for n in levels:
        c = Client(concurrency=n, timeout=args.timeout, nonce=True)
        t = time.perf_counter()
        res = await closed_loop(c, reqs, n, duration=args.cell_seconds, cls=f"short20 x{n}")
        await c.close()
        results += res
        s = summarize(res, time.perf_counter() - t)
        stats.append(s)
        rows.append(summary_row(f"×{n}", s))
        await asyncio.sleep(2)
    rep.table(SUMMARY_COLS, rows)
    rep.chart("short20: latency vs concurrency", [f"×{n}" for n in levels],
              [("p50", [s["p50"] for s in stats]), ("p90", [s["p90"] for s in stats])], "s", x_label="concurrency")
    rep.chart("short20: throughput vs concurrency", [f"×{n}" for n in levels],
              [("req/s", [s["rps"] for s in stats]), ("API tokens/s ÷ 1000", [s["tps"] / 1000 for s in stats])], "",
              x_label="concurrency")
    await client.close()
    errors(rep, results)
    s = summarize(results)
    rep.p(f"{s['n']} requests, {s['billed']:,} tokens billed.")
    return s["err_pct"] <= args.max_error_rate, results


async def mode_hammer32k(args, rep):
    duration, n = args.duration or 45 * 60, args.concurrency or 2
    reqs = pool("long32k", random.Random(args.seed))
    client = Client(concurrency=n, timeout=max(args.timeout, 120), nonce=not args.no_nonce)
    results = await closed_loop(client, reqs, n, duration=duration, cls="long32k")
    await client.close()
    s = summarize(results, duration)
    rep.p(f"{duration / 60:g} min closed loop with {n} concurrent ~32K-token requests ({len(reqs)} distinct). "
          f"{s['n']} requests, {s['billed']:,} tokens billed.")
    window = 300
    rows = [summary_row("all", s)]
    for k in range(math.ceil(duration / window)):
        chunk = [r for r in results if k * window <= r.start < (k + 1) * window]
        if chunk:
            wall = min(window, duration - k * window)  # the last window may be partial
            rows.append(summary_row(f"min {k * window // 60}–{(k + 1) * window // 60}", summarize(chunk, wall)))
    rep.table(SUMMARY_COLS, rows)
    errors(rep, results)
    timeline(rep, results, 60, "Latency per minute")
    return s["err_pct"] <= args.max_error_rate, results


async def mode_quality(args, rep):
    sets = sorted(p.stem for p in PREPARED.glob("*.jsonl") if not args.sets or p.stem in args.sets)
    conc = args.concurrency or 4
    client = Client(concurrency=conc, timeout=args.timeout, keep_scores=True)
    # Local reference variants from scripts/reference.py: reference/qwen3-reranker-0.6b[-fp8|-fp8kv]/
    variants = {d.name.removeprefix(REFERENCE.name).lstrip("-") or "bf16": d
                for d in sorted(REFERENCE.parent.glob(REFERENCE.name + "*")) if (d / "metrics.json").exists()}
    rows, results, api_nd, ref_nd = [], [], [], {v: {} for v in variants}
    delta, agree = {v: [] for v in variants}, {v: [] for v in variants}
    for name in sets:
        reqs = load_set(name, args.per_set_natural if name.startswith("natural-") else args.per_set)
        relevant = {q["id"]: q["relevant"] for q in reqs}
        res = await closed_loop(client, reqs, conc, cls=name)
        results += res
        ok = [r for r in res if r.ok]
        s = summarize(res)
        row = [name, s["n"], s["errors"], s["ndcg"], s["mrr"], s["p50"]]
        for v, d in variants.items():
            mad = top1 = nd = math.nan
            ref_path = d / f"{name}.jsonl"
            if ref_path.exists() and ok:
                ref = {json.loads(l)["id"]: json.loads(l)["scores"] for l in open(ref_path)}
                pairs = [(r.scores, ref[r.id], relevant[r.id]) for r in ok if r.id in ref]
                if pairs:  # every reference metric over exactly the requests the API answered
                    mad = statistics.fmean(abs(x - y) for a, b, _ in pairs for x, y in zip(a, b))
                    top1 = 100 * statistics.fmean(a.index(max(a)) == b.index(max(b)) for a, b, _ in pairs)
                    nd = statistics.fmean(ranking_metrics(b, rel)[0] for _, b, rel in pairs)
                    ref_nd[v][name] = nd
            row += [nd, mad, top1]
            delta[v].append(mad)
            agree[v].append(top1)
        api_nd.append(s["ndcg"])
        rows.append(row)
    await client.close()
    s = summarize(results)
    rep.p(f"Up to {args.per_set} requests per set ({args.per_set_natural} for natural-*) at {conc} in flight; "
          f"{s['n']} requests, {s['billed']:,} tokens billed. nDCG@10 / MRR are against the "
          "ground-truth labels; every reference column is computed over the same requests. Local reference "
          "variants of Qwen3-Reranker-0.6B (scripts/reference.py): "
          + (", ".join(variants) if variants else "**none available here** — run scripts/reference.py on a GPU")
          + ". |Δ| is the mean absolute score difference per document; top-1 is the share of requests where the "
          "API and the reference pick the same best document.")
    rep.table(["set", "requests", "errors", "nDCG@10 API", "MRR API", "p50 s"]
              + [h for v in variants for h in (f"nDCG {v}", f"|Δ| {v}", f"top-1 % {v}")], rows)
    errors(rep, results)
    rep.chart("nDCG@10 per set (bars: API; lines: local reference variants)", sets,
              [("API", api_nd)] + [(v, [ref_nd[v].get(n, math.nan) for n in sets]) for v in variants],
              "nDCG@10", kind="bar")
    if variants:
        rep.chart("Mean |score difference| between API and reference, per set", sets,
                  [(v, delta[v]) for v in variants], "mean |Δ score|")
        rep.chart("Top-1 agreement between API and reference, % of requests", sets,
                  [(v, agree[v]) for v in variants], "%")
    base = ref_nd.get("bf16", {})
    drops = [a < base[n] - args.max_ndcg_drop for a, n in zip(api_nd, sets) if n in base]
    return s["err_pct"] <= args.max_error_rate and not any(drops), results


# `all` runs in this order: correctness, quality, reliability, speed.
MODES = {"smoke": mode_smoke, "quality": mode_quality,
         "normal": mode_normal, "burst": mode_burst, "hammer32k": mode_hammer32k,
         "speed": mode_speed, "meticulous": mode_meticulous}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=[*MODES, "all"])
    ap.add_argument("--duration", type=float, help="seconds (normal: 300, hammer32k: 2700)")
    ap.add_argument("--rate", type=float, default=1.5, help="normal: mean requests per second")
    ap.add_argument("--concurrency", type=int, help="hammer32k: 2, quality: 4")
    ap.add_argument("--cell-seconds", type=float, default=25, help="speed/meticulous: seconds per concurrency cell")
    ap.add_argument("--per-rung", type=int, default=30, help="meticulous: requests per ladder rung")
    ap.add_argument("--per-set", type=int, default=300, help="quality: requests per set (ladder sets have 50)")
    ap.add_argument("--per-set-natural", type=int, default=100, help="quality: requests per natural-* set (~32K tokens each)")
    ap.add_argument("--sets", nargs="*", help="quality: only these prepared sets (default: all)")
    ap.add_argument("--timeout", type=float, default=60, help="per-request timeout, seconds")
    ap.add_argument("--max-error-rate", type=float, default=5.0, help="%% of failed requests that still passes")
    ap.add_argument("--max-ndcg-drop", type=float, default=0.05, help="quality: tolerated nDCG@10 gap vs vanilla")
    ap.add_argument("--no-nonce", action="store_true", help="let identical queries hit the server's prefix cache")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", type=Path, default=ROOT / "reports")
    ap.add_argument("--no-docs", action="store_true", help="accepted for compatibility; does nothing")
    args = ap.parse_args()

    global LOG
    all_ok = True
    args.out.mkdir(parents=True, exist_ok=True)
    for mode in (MODES if args.mode == "all" else [args.mode]):
        LOG = open(args.out / f"{mode}.requests.jsonl", "a")  # appended to, so a rerun never erases a run
        rep = Report(f"{mode} — {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}")
        t = time.perf_counter()
        ok, results = asyncio.run(MODES[mode](args, rep))
        s = summarize(results)
        rep.parts.insert(1, f"**{'PASS' if ok else 'FAIL'}** · {time.perf_counter() - t:.0f} s · {s['n']} requests · "
                            f"{s['errors']} errors · {s['billed']:,} tokens billed\n")
        rep.write(args.out / f"{mode}.md", [asdict(r) for r in results])
        all_ok &= ok
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
