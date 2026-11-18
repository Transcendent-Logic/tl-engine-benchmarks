"""Download pinned raw sources into data/raw/ and verify them against checksums/.

    uv run scripts/download.py                     # datasets (~130 MB); verify against checksums/raw.sha256
    uv run scripts/download.py --model 0.6b        # also one reranker's weights (checksums/model-0.6b.sha256)
    uv run scripts/download.py --write-checksums   # (maintainers) record new checksums instead of verifying

scripts/prepare.py and scripts/reference.py call this themselves, so running it by hand is optional.
"""

import argparse
import shutil
import urllib.request

import sources
from checksums import ROOT, verify, write

RAW = ROOT / "data" / "raw"
SUMS = ROOT / "checksums"


def fetch(url: str, dest) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + ".part")
    print(f"GET {url}")
    with urllib.request.urlopen(url) as r, open(tmp, "wb") as f:
        shutil.copyfileobj(r, f, 1 << 20)
    tmp.rename(dest)


def ensure(entries, sumfile, write_checksums=False) -> None:
    """Fetch whatever is missing, then verify (or record) checksums of the whole group."""
    paths = []
    for url, rel in entries:
        dest = RAW / rel
        if not dest.exists():
            fetch(url, dest)
        paths.append(dest)
    (write if write_checksums else verify)(sumfile, paths)


def ensure_datasets(write_checksums=False) -> None:
    ensure(sources.files(), SUMS / "raw.sha256", write_checksums)


def ensure_model(size: str, write_checksums=False):
    """Returns the local directory holding the model."""
    ensure(sources.model_files(size), SUMS / f"model-{size}.sha256", write_checksums)
    return RAW / sources.MODELS[size][0]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", action="append", choices=sorted(sources.MODELS), default=[])
    ap.add_argument("--write-checksums", action="store_true")
    args = ap.parse_args()
    ensure_datasets(args.write_checksums)
    for size in args.model:
        ensure_model(size, args.write_checksums)


if __name__ == "__main__":
    main()
