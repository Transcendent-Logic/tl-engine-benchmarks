"""Read, write and verify `sha256sum`-compatible checksum files.

Paths inside the files are relative to the repo root, so `sha256sum -c checksums/raw.sha256`
works from there too."""

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load(sumfile: Path) -> dict[str, str]:
    if not sumfile.exists():
        return {}
    out = {}
    for line in sumfile.read_text().splitlines():
        digest, rel = line.split(maxsplit=1)
        out[rel.lstrip("*")] = digest
    return out


def write(sumfile: Path, paths: list[Path]) -> None:
    lines = [f"{sha256(p)}  {p.relative_to(ROOT).as_posix()}" for p in sorted(paths)]
    sumfile.write_text("\n".join(lines) + "\n")
    print(f"wrote {len(lines)} checksums to {sumfile.relative_to(ROOT)}")


def verify(sumfile: Path, paths: list[Path]) -> None:
    """Exit non-zero if any path is missing from, or disagrees with, the checksum file."""
    expected = load(sumfile)
    if not expected:
        sys.exit(f"{sumfile.relative_to(ROOT)} not found; run with --write-checksums to create it")
    bad = 0
    for p in sorted(paths):
        rel = p.relative_to(ROOT).as_posix()
        got = sha256(p)
        if expected.get(rel) != got:
            print(f"MISMATCH {rel}: expected {expected.get(rel)}, got {got}")
            bad += 1
    extra = set(expected) - {p.relative_to(ROOT).as_posix() for p in paths}
    for rel in sorted(extra):
        print(f"MISSING {rel}")
        bad += 1
    if bad:
        sys.exit(f"{bad} checksum problem(s) against {sumfile.relative_to(ROOT)}")
    print(f"OK: {len(paths)} files match {sumfile.relative_to(ROOT)}")
