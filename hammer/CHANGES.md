# Changes from commit `195a09c`

The hammer was first written to test a hosted reranking API with its own keys, rate limits and error codes. The runs in this repository all used commit `195a09c` against SageMaker endpoints. For publication, the parts that belong to that API were removed. Nothing here changes a request, the request sets (`checksums/prepared.sha256` is unchanged), the load pattern or how a measurement is computed.

## `scripts/hammer.py`

- `RERANKER_API_URL` is required; it had the hosted API's address as its default.
- No API key: the `RERANKER_API_KEY` bearer token is gone. SageMaker URLs are signed as before (AWS SigV4); other URLs get plain requests.
- No 429 handling. The hosted API answered over-limit requests with HTTP 429 and `Retry-After`; the hammer retried them in `quality` and counted them apart from other errors. Removed: the retry, the `retry_after` field, the "429s" columns and chart, and the `hard_err_pct` measure (now every failure counts in `err_pct`). None of the 158,449 requests in `../reports/` got a 429, so the published numbers are the same either way.
- `smoke`: removed the three checks of the hosted API's own refusals (unknown model name → 404 `MODEL_NOT_FOUND`, 1,001 documents → 400, over-long input → 400 `INPUT_TOO_LONG`). A SageMaker container makes none of these refusals, so `smoke` failed on every endpoint.
- Removed the step that refreshed the hosted API's documentation after each run (`scripts/update_docs.py`); `--no-docs` is still accepted and does nothing.
- Docstring, report wording and the User-Agent no longer name the hosted API.

## Other files

- `scripts/prepare.py`, `scripts/reference.py`, `scripts/report.py`: comments and one chart label reworded; no code change.
- `scripts/sources.py`: the two community GGUF quantisations of the 0.6B are gone (they served a script not included here).
- `pyproject.toml`, `uv.lock`: project renamed to `tl-engine-benchmarks-hammer`; dependencies unchanged.
- Not included: `README.md` (it reported on the hosted API; replaced), the GitHub Actions workflows (they ran against the hosted API with its key), `scripts/update_docs.py`, `scripts/compare_variants.py`, `scripts/reference_vllm.py`, `scripts/reference_gguf.py`, the `docs/` charts, the GGUF checksums, and every `reference/` folder except `qwen3-reranker-0.6b/` (scores of other local precision variants).
