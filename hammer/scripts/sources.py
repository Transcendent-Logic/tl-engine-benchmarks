"""Pinned upstream sources. Every file is fetched from an exact Hugging Face commit,
so the bytes never change; checksums/*.sha256 record what those bytes are."""

HF = "https://huggingface.co"

# (repo type, repo id, commit sha, files)
SOURCES = [
    ("datasets", "BeIR/scifact", "b3b5335604bf5ee3c4447671af975ea25143d4f5",
     ["corpus/corpus-00000-of-00001.parquet", "queries/queries-00000-of-00001.parquet"]),
    ("datasets", "BeIR/scifact-qrels", "2938d17dc3b09882fdb8c12bbbe2e2dc0e75a029", ["test.tsv"]),
    ("datasets", "BeIR/fiqa", "979c07a7cb5ccc6ca009792241fa1250b98055dd",
     ["corpus/corpus-00000-of-00001.parquet", "queries/queries-00000-of-00001.parquet"]),
    ("datasets", "BeIR/fiqa-qrels", "252958f2d646e22cab6d0c72dd3f0d5de6d0655a", ["test.tsv"]),
    ("datasets", "BeIR/arguana", "9bcf8fc0320c4e3860e25b8b85fa205fcdd7078f",
     ["corpus/corpus-00000-of-00001.parquet", "queries/queries-00000-of-00001.parquet"]),
    ("datasets", "BeIR/arguana-qrels", "ae5468c6f1c198109a8af5f0d4dc58bd18b6fea7", ["test.tsv"]),
    # Long documents. needle: essays with a planted fact, 100 docs at each designed length
    # 256..32768 tokens. 2wikimqa / summ_screen_fd / qmsum: natural 1.5K-35K-token documents
    # (wiki bundles, TV scripts, meeting transcripts).
    ("datasets", "dwzhu/LongEmbed", "10039a580487dacecf79db69166e17ace3ede392",
     [f"{c}/{f}.jsonl" for c in ("needle", "2wikimqa", "summ_screen_fd", "qmsum")
      for f in ("corpus", "queries", "qrels")]),
    # Tokenizer only (not the weights): used to count documents in real Qwen tokens.
    ("models", "Qwen/Qwen3-Reranker-0.6B", "e61197ed45024b0ed8a2d74b80b4d909f1255473",
     ["tokenizer.json"]),
]

_TOKENIZER_FILES = ["config.json", "generation_config.json", "merges.txt", "tokenizer.json",
                    "tokenizer_config.json", "vocab.json"]

# Reranker weights for scripts/reference.py, keyed by size. Only fetched on demand.
MODELS = {
    "0.6b": ("Qwen/Qwen3-Reranker-0.6B", "e61197ed45024b0ed8a2d74b80b4d909f1255473",
             _TOKENIZER_FILES + ["model.safetensors"]),
    "4b": ("Qwen/Qwen3-Reranker-4B", "22e683669bc0f0bd69640a1354a6d0aebcfeede5",
           _TOKENIZER_FILES + ["model.safetensors.index.json"]
           + [f"model-0000{i}-of-00002.safetensors" for i in (1, 2)]),
    "8b": ("Qwen/Qwen3-Reranker-8B", "77d193c791ed757ca307ee72715aa132723da912",
           _TOKENIZER_FILES + ["model.safetensors.index.json"]
           + [f"model-0000{i}-of-00005.safetensors" for i in range(1, 6)]),
}


def _entries(kind, repo, sha, paths):
    prefix = "" if kind == "models" else "datasets/"
    for p in paths:
        yield f"{HF}/{prefix}{repo}/resolve/{sha}/{p}", f"{repo}/{p}"


def files():
    """Yield (url, local path relative to data/raw) for every dataset source."""
    for kind, repo, sha, paths in SOURCES:
        yield from _entries(kind, repo, sha, paths)


def model_files(size: str):
    """Yield (url, local path relative to data/raw) for one reranker's weights."""
    repo, sha, paths = MODELS[size]
    yield from _entries("models", repo, sha, paths)
