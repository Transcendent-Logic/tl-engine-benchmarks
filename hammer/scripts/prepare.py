"""Build benchmark request sets in data/prepared/ from the raw downloads.

    uv run scripts/prepare.py                     # build all sets, verify against checksums/prepared.sha256
    uv run scripts/prepare.py --write-checksums   # (maintainers) record new checksums
    uv run scripts/prepare.py --sets beir-scifact ladder-32768

Every output line is one request plus its ground truth:

    {"set", "id", "query_id", "query", "documents": [...], "relevant": [doc indices],
     "doc_ids": [...], "query_tokens", "doc_tokens": [...], "query_api_tokens", "doc_api_tokens": [...],
     "est_api_tokens", "truncated": [doc indices]}

query_tokens / doc_tokens are real Qwen3-Reranker tokenizer counts; *_api_tokens are a character-based
estimate (see API_CHARS_PER_TOKEN), used only to keep every request within a 32,768-token budget.

Sets (document length is the main axis):

    beir-{scifact,fiqa,arguana}  realistic short documents (~100-300 tokens): 1 query + CANDIDATES
                                 documents = every relevant document + BM25 hard negatives.
    ladder-{256..32768}          LongEmbed needle documents of one designed length: the relevant
                                 document + same-length distractors, packed up to the request budget.
                                 Total tokens per request stay ~constant while document length varies.
                                 The 32768 rung exceeds the 32,768-token budget on its own and is cut down to it,
                                 keeping the end of the document that contains the planted fact.
    ladder1-{256..32768}         same, but exactly one document per request (latency vs length).
    natural-{2wikimqa,summ_screen_fd,qmsum}
                                 real 1.5K-35K-token documents: the relevant document (cut to the
                                 budget if needed) + distractors from the same corpus while they fit.

Everything is deterministic: inputs are pinned, orderings are sorted, shuffles are seeded per query.
"""

import argparse
import collections
import json
import math
import random
import re

import pyarrow.parquet as pq
from tokenizers import Tokenizer

import download
from checksums import ROOT, verify, write

RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "prepared"
SUMS = ROOT / "checksums" / "prepared.sha256"

# Requests are budgeted with a character-based token estimate: chars/3.75 per text, plus a few tokens per
# (query, document) pair, independent of the real Qwen tokenization (the hosted API this hammer was first
# written for counted tokens this way). The real Qwen token counts are kept in the output because those
# are what the model actually processes. Changing these constants changes the request sets.
API_MAX_TOKENS = 32768
API_MAX_DOCS = 1000
API_CHARS_PER_TOKEN = 3.75
API_PAIR_OVERHEAD = 4
BUDGET = 32000
CANDIDATES = 20  # documents per request in the beir-* sets
LADDER = [256, 512, 1024, 2048, 4096, 8192, 16384, 32768]

_tok = None


def tokenizer() -> Tokenizer:
    """The pinned Qwen3-Reranker tokenizer, loaded on first use (after download.ensure_datasets())."""
    global _tok
    if _tok is None:
        _tok = Tokenizer.from_file(str(RAW / "Qwen/Qwen3-Reranker-0.6B/tokenizer.json"))
    return _tok


def ntok(texts: list[str]) -> list[int]:
    return [len(e.ids) for e in tokenizer().encode_batch(texts, add_special_tokens=False)]


def api_tokens(text: str) -> int:
    return math.ceil(len(text) / API_CHARS_PER_TOKEN)


def pair_cost(query: str, doc: str) -> int:
    return api_tokens(doc) + api_tokens(query) + API_PAIR_OVERHEAD


def max_doc_chars(query: str) -> int:
    """Longest document (in characters) that fits a request on its own."""
    return int((BUDGET - api_tokens(query) - API_PAIR_OVERHEAD) * API_CHARS_PER_TOKEN)


def rng(*key) -> random.Random:
    return random.Random(":".join(map(str, key)))


# --- BM25 for hard negatives -------------------------------------------------------------

WORD = re.compile(r"\w+")


def words(text: str) -> list[str]:
    return WORD.findall(text.lower())


class BM25:
    def __init__(self, ids: list[str], texts: list[str], k1=1.2, b=0.75):
        self.ids, self.k1, self.b = ids, k1, b
        self.postings: dict[str, list[tuple[int, int]]] = collections.defaultdict(list)
        self.dl = []
        for i, text in enumerate(texts):
            w = words(text)
            self.dl.append(len(w))
            for term, tf in collections.Counter(w).items():
                self.postings[term].append((i, tf))
        self.n = len(texts)
        self.avgdl = sum(self.dl) / self.n

    def top(self, query: str, n: int, exclude: set[str]) -> list[str]:
        # Only the rarest 20 query terms matter for the score and they keep this fast enough in pure Python.
        terms = [t for t in set(words(query)) if t in self.postings and len(self.postings[t]) < 0.1 * self.n]
        terms = sorted(terms, key=lambda t: (len(self.postings[t]), t))[:20]
        scores: dict[int, float] = collections.defaultdict(float)
        for t in terms:
            plist = self.postings[t]
            idf = math.log(1 + (self.n - len(plist) + 0.5) / (len(plist) + 0.5))
            for i, tf in plist:
                norm = 1 - self.b + self.b * self.dl[i] / self.avgdl
                scores[i] += idf * tf * (self.k1 + 1) / (tf + self.k1 * norm)
        ranked = sorted(scores, key=lambda i: (-scores[i], self.ids[i]))
        return [self.ids[i] for i in ranked if self.ids[i] not in exclude][:n]


# --- loaders ------------------------------------------------------------------------------


def load_beir(name: str):
    corpus = {r["_id"]: f"{r['title']} {r['text']}".strip()
              for r in pq.read_table(RAW / f"BeIR/{name}/corpus/corpus-00000-of-00001.parquet").to_pylist()}
    queries = {r["_id"]: r["text"]
               for r in pq.read_table(RAW / f"BeIR/{name}/queries/queries-00000-of-00001.parquet").to_pylist()}
    qrels = collections.defaultdict(set)
    with open(RAW / f"BeIR/{name}-qrels/test.tsv") as f:
        next(f)  # header: query-id corpus-id score
        for line in f:
            qid, did, score = line.rstrip("\n").split("\t")
            if int(score) > 0 and did in corpus:
                qrels[qid].add(did)
    return corpus, queries, qrels


def numeric_id(s: str) -> int:
    """LongEmbed ids look like 'query34' / 'doc_12'; sort them by their number."""
    return int(re.search(r"\d+", s).group())


def load_longembed(name: str):
    def rows(kind):
        with open(RAW / f"dwzhu/LongEmbed/{name}/{kind}.jsonl") as f:
            return [json.loads(line) for line in f]
    corpus = {r["doc_id"]: r for r in rows("corpus")}
    queries = {r["qid"]: r["text"] for r in rows("queries")}
    qrels = collections.defaultdict(set)
    for r in rows("qrels"):
        qrels[r["qid"]].add(r["doc_id"])
    return corpus, queries, qrels


# --- set builders: each yields request dicts ------------------------------------------------


def request(set_name, qid, query, doc_ids, texts, relevant_ids, truncated_ids=()):
    """Assemble one request, shuffling documents so relevant ones are not always first."""
    order = list(range(len(doc_ids)))
    rng(set_name, qid).shuffle(order)
    doc_ids = [doc_ids[i] for i in order]
    texts = [texts[i] for i in order]
    qt, dt = ntok([query])[0], ntok(texts)
    est = sum(pair_cost(query, t) for t in texts)
    assert est <= API_MAX_TOKENS and len(texts) <= API_MAX_DOCS, (set_name, qid, est, len(texts))
    return {
        "set": set_name, "id": f"{set_name}/{qid}", "query_id": qid, "query": query,
        "documents": texts, "relevant": [i for i, d in enumerate(doc_ids) if d in relevant_ids],
        "doc_ids": doc_ids,
        "query_tokens": qt, "doc_tokens": dt,  # real Qwen tokenizer counts
        "query_api_tokens": api_tokens(query), "doc_api_tokens": [api_tokens(t) for t in texts],
        "est_api_tokens": est,  # the character-based estimate: sum over pairs incl. per-pair overhead
        "truncated": [i for i, d in enumerate(doc_ids) if d in truncated_ids],
    }


def build_beir(name: str, max_queries: int):
    set_name = f"beir-{name}"
    corpus, queries, qrels = load_beir(name)
    ids = sorted(corpus)
    bm25 = BM25(ids, [corpus[i] for i in ids])
    for qid in sorted(qrels, key=str)[:max_queries]:
        relevant = sorted(qrels[qid])[: CANDIDATES // 2]
        negatives = bm25.top(queries[qid], CANDIDATES - len(relevant), set(relevant))
        while len(relevant) + len(negatives) < CANDIDATES:  # BM25 found too few: pad randomly
            d = rng(set_name, qid, "pad", len(negatives)).choice(ids)
            if d not in relevant and d not in negatives:
                negatives.append(d)
        doc_ids = relevant + negatives
        yield request(set_name, qid, queries[qid], doc_ids, [corpus[d] for d in doc_ids], set(relevant))


def needle_span(text: str, others: list[str]) -> tuple[int, int]:
    """Character span of the one sentence planted in a needle document (absent from its siblings)."""
    norm = text.replace("\n", " ")
    seen = {s for o in others for s in o.replace("\n", " ").split(". ")}
    for s in norm.split(". "):
        if len(s) > 10 and s not in seen:
            start = norm.index(s)
            return start, start + len(s)
    raise ValueError("needle not found")


def build_ladder(length: int, single: bool):
    set_name = f"{'ladder1' if single else 'ladder'}-{length}"
    corpus, queries, qrels = load_longembed("needle")
    docs = sorted(d for d, r in corpus.items() if r["context_length"] == length)
    texts = {d: corpus[d]["text"] for d in docs}
    for qid in sorted(qrels, key=numeric_id):
        (rel,) = qrels[qid]
        if rel not in texts:
            continue
        query = queries[qid]
        limit = max_doc_chars(query)
        cut = {}
        if len(texts[rel]) > limit:
            # Too long for one request (the 32768 rung): keep the end that contains the planted fact.
            _, end = needle_span(texts[rel], [texts[d] for d in docs if d != rel])
            cut[rel] = texts[rel][:limit] if end <= limit else texts[rel][-limit:]
        if single:
            doc_ids = [rel]
        else:
            per_doc = max(pair_cost(query, t[:limit]) for t in texts.values())
            n = min(API_MAX_DOCS, len(docs), BUDGET // per_doc)
            others = [d for d in docs if d != rel]
            doc_ids = [rel] + rng(set_name, qid, "distractors").sample(others, n - 1)
        yield request(set_name, qid, query, doc_ids, [cut.get(d, texts[d]) for d in doc_ids], {rel}, set(cut))


def build_natural(name: str, max_queries: int):
    set_name = f"natural-{name}"
    corpus, queries, qrels = load_longembed(name)
    docs = sorted(corpus)
    for qid in sorted(qrels, key=numeric_id)[:max_queries]:
        query = queries[qid]
        relevant = sorted(qrels[qid])
        texts, doc_ids, truncated, used = [], [], set(), 0
        for d in relevant + rng(set_name, qid, "distractors").sample(docs, len(docs)):
            if d in doc_ids:
                continue
            text = corpus[d]["text"]
            cost = pair_cost(query, text)
            if used + cost > BUDGET:
                if d not in relevant or used:  # only a lone relevant document gets cut to fit
                    continue
                text = text[: max_doc_chars(query)]
                cost = pair_cost(query, text)
                truncated.add(d)
            doc_ids.append(d)
            texts.append(text)
            used += cost
        yield request(set_name, qid, query, doc_ids, texts, set(relevant), truncated)


def builders(max_queries: int):
    for name in ("scifact", "fiqa", "arguana"):
        yield f"beir-{name}", lambda name=name: build_beir(name, max_queries)
    for length in LADDER:
        yield f"ladder-{length}", lambda length=length: build_ladder(length, single=False)
        yield f"ladder1-{length}", lambda length=length: build_ladder(length, single=True)
    for name in ("2wikimqa", "summ_screen_fd", "qmsum"):
        yield f"natural-{name}", lambda name=name: build_natural(name, max_queries)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sets", nargs="*", help="only build these sets (default: all)")
    ap.add_argument("--max-queries", type=int, default=300, help="cap per beir-*/natural-* set")
    ap.add_argument("--write-checksums", action="store_true")
    args = ap.parse_args()

    download.ensure_datasets()
    OUT.mkdir(parents=True, exist_ok=True)
    paths = []
    for set_name, build in builders(args.max_queries):
        if args.sets and set_name not in args.sets:
            continue
        path = OUT / f"{set_name}.jsonl"
        n, tokens, docs = 0, 0, 0
        with open(path, "w") as f:
            for req in build():
                f.write(json.dumps(req, ensure_ascii=False, sort_keys=True) + "\n")
                n, tokens, docs = n + 1, tokens + req["est_api_tokens"], docs + len(req["documents"])
        print(f"{set_name:24} {n:5} requests  {docs / max(n, 1):7.1f} docs/req  {tokens / max(n, 1):9.0f} api-tokens/req")
        paths.append(path)

    if args.sets:
        print("partial build: checksums not checked")
    else:
        (write if args.write_checksums else verify)(SUMS, paths)


if __name__ == "__main__":
    main()
