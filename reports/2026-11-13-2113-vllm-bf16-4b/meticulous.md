## meticulous — 2026-11-13 22:31 UTC

**PASS** · 1270 s · 832 requests · 1 (0.1%) errors · 0 rate-limited · 9,449,536 tokens billed

Sequential requests (one in flight) unless stated; every query carries a nonce so nothing is served from the API's prefix cache.


### Single document: latency vs length

| rung | Qwen tokens | billed | errors | p50 s | p90 s | max s | API tok/s |
|---|---|---|---|---|---|---|---|
| 256 | 229 | 323 | 0 (0.0%) | 0.070 | 0.072 | 0.102 | 4,544 |
| 512 | 457 | 551 | 0 (0.0%) | 0.105 | 0.110 | 0.115 | 5,184 |
| 1,024 | 911 | 1,005 | 0 (0.0%) | 0.169 | 0.172 | 0.172 | 5,943 |
| 2,048 | 1,872 | 1,966 | 0 (0.0%) | 0.333 | 0.337 | 0.338 | 5,897 |
| 4,096 | 3,707 | 3,800 | 0 (0.0%) | 0.668 | 0.677 | 0.680 | 5,678 |
| 8,192 | 7,545 | 7,640 | 0 (0.0%) | 1.508 | 1.521 | 1.531 | 5,062 |
| 16,384 | 15,274 | 15,368 | 0 (0.0%) | 3.703 | 3.710 | 3.712 | 4,150 |
| 32,768 | 25,438 | 25,536 | 0 (0.0%) | 7.678 | 7.700 | 7.726 | 3,327 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Single document: latency vs length"
    x-axis "document length (designed tokens)" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "s" 0 --> 8.47
    line [0.06972, 0.1054, 0.169, 0.3326, 0.6678, 1.508, 3.703, 7.678]
    line [0.07247, 0.1098, 0.1717, 0.3367, 0.6774, 1.521, 3.71, 7.7]
```

*Single document: latency vs length: p50, p90*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Single document: throughput vs length"
    x-axis "document length (designed tokens)" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "" 0 --> 6.537
    line [4.544, 5.184, 5.943, 5.897, 5.678, 5.062, 4.15, 3.327]
```

*Single document: throughput vs length: API tokens/s ÷ 1000*


### ~30K tokens per request: latency vs document length (fewer, longer documents)

| rung | docs/request | billed | errors | p50 s | p90 s | max s | API tok/s |
|---|---|---|---|---|---|---|---|
| 256 | 100 | 32,413 | 1 (6.7%) | 2.533 | 2.553 | 2.570 | 12,799 |
| 512 | 55 | 30,264 | 0 (0.0%) | 2.368 | 2.499 | 2.680 | 12,683 |
| 1,024 | 28 | 28,178 | 0 (0.0%) | 2.490 | 2.724 | 2.789 | 11,378 |
| 2,048 | 13 | 25,570 | 0 (0.0%) | 2.509 | 2.754 | 2.924 | 10,517 |
| 4,096 | 6 | 22,808 | 0 (0.0%) | 2.722 | 3.018 | 3.219 | 8,529 |
| 8,192 | 3 | 22,921 | 0 (0.0%) | 3.259 | 3.807 | 4.181 | 7,246 |
| 16,384 | 1 | 15,366 | 0 (0.0%) | 3.705 | 3.712 | 3.731 | 4,146 |
| 32,768 | 1 | 25,541 | 0 (0.0%) | 7.680 | 7.693 | 7.730 | 3,327 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "~30K tokens: latency vs document length"
    x-axis "document length" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "s" 0 --> 8.463
    line [2.533, 2.368, 2.49, 2.509, 2.722, 3.259, 3.705, 7.68]
    line [2.553, 2.499, 2.724, 2.754, 3.018, 3.807, 3.712, 7.693]
```

*~30K tokens: latency vs document length: p50, p90*


### Latency vs number of documents

| documents | billed | errors | p50 s | p90 s | max s | MRR |
|---|---|---|---|---|---|---|
| 1 tiny | 91.3 | 0 (0.0%) | 0.043 | 0.044 | 0.045 | 1.000 |
| 10 tiny | 917 | 0 (0.0%) | 0.097 | 0.106 | 0.107 | 1.000 |
| 100 tiny | 9,289 | 0 (0.0%) | 0.523 | 0.534 | 0.535 | 1.000 |
| 1000 tiny | 94,189 | 0 (0.0%) | 2.860 | 4.896 | 4.920 | 1.000 |
| 1×256 | 323 | 0 (0.0%) | 0.070 | 0.073 | 0.074 | 1.000 |
| 10×256 | 3,230 | 0 (0.0%) | 0.334 | 0.360 | 0.382 | 1.000 |
| 50×256 | 16,125 | 0 (0.0%) | 1.313 | 1.386 | 1.404 | 1.000 |
| 100×256 | 32,379 | 0 (0.0%) | 2.513 | 2.522 | 2.531 | 0.950 |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Latency vs number of documents"
    x-axis "documents per request" ["1 tiny", "10 tiny", "100 tiny", "1000 tiny", "1×256", "10×256", "50×256", "100×256"]
    y-axis "s" 0 --> 5.386
    line [0.04306, 0.09672, 0.5227, 2.86, 0.06959, 0.3344, 1.313, 2.513]
    line [0.04405, 0.1058, 0.5341, 4.896, 0.07305, 0.36, 1.386, 2.522]
```

*Latency vs number of documents: p50, p90*


### Cold vs cached: the same single-document request sent twice in a row

The API caches prompt prefixes, so a repeated (query, document) pair skips most of the compute. Cold = fresh nonce in the query; cached = the identical request again immediately after.

| rung | pairs | cold p50 s | cached p50 s | speed-up × | cold max s | cached max s | errors |
|---|---|---|---|---|---|---|---|
| 256 | 10 | 0.063 | 0.043 | 1.470 | 0.078 | 0.044 |  |
| 512 | 10 | 0.097 | 0.044 | 2.200 | 0.099 | 0.045 |  |
| 1,024 | 10 | 0.164 | 0.045 | 3.630 | 0.167 | 0.047 |  |
| 2,048 | 10 | 0.329 | 0.048 | 6.794 | 0.331 | 0.050 |  |
| 4,096 | 10 | 0.660 | 0.056 | 11.8 | 0.668 | 0.057 |  |
| 8,192 | 10 | 1.510 | 0.070 | 21.6 | 1.519 | 0.072 |  |
| 16,384 | 10 | 3.643 | 0.096 | 38.0 | 3.699 | 0.098 |  |
| 32,768 | 10 | 7.558 | 0.129 | 58.7 | 7.655 | 0.131 |  |

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "Cold vs cached latency vs document length"
    x-axis "document length (designed tokens)" ["256", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    y-axis "s" 0 --> 8.314
    line [0.06282, 0.09657, 0.1643, 0.3286, 0.6599, 1.51, 3.643, 7.558]
    line [0.04273, 0.0439, 0.04526, 0.04836, 0.05607, 0.07003, 0.09587, 0.1288]
```

*Cold vs cached latency vs document length: cold p50, cached p50*


### short20: latency and throughput vs concurrency

|  | requests | errors | 429s | p50 s | p90 s | p99 s | max s | req/s | API tok/s | MRR |
|---|---|---|---|---|---|---|---|---|---|---|
| ×1 | 27 | 0 (0.0%) | 0 | 0.833 | 1.287 | 1.611 | 1.641 | 1.074 | 9,474 | 0.665 |
| ×2 | 31 | 0 (0.0%) | 0 | 1.909 | 1.988 | 2.564 | 2.564 | 1.172 | 10,661 | 0.670 |
| ×4 | 32 | 0 (0.0%) | 0 | 3.514 | 4.437 | 4.508 | 4.508 | 1.176 | 10,572 | 0.656 |
| ×8 | 37 | 0 (0.0%) | 0 | 6.703 | 8.118 | 8.328 | 8.330 | 1.155 | 10,212 | 0.701 |
| ×16 | 44 | 0 (0.0%) | 0 | 13.4 | 14.1 | 14.3 | 14.4 | 1.173 | 10,109 | 0.715 |
| ×32 | 61 | 0 (0.0%) | 0 | 26.7 | 28.4 | 29.1 | 29.1 | 1.161 | 10,410 | 0.672 |

No 429s up to concurrency ×32.

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "short20: latency vs concurrency"
    x-axis "concurrency" ["×1", "×2", "×4", "×8", "×16", "×32"]
    y-axis "s" 0 --> 31.28
    line [0.8327, 1.909, 3.514, 6.703, 13.4, 26.68]
    line [1.287, 1.988, 4.437, 8.118, 14.09, 28.44]
```

*short20: latency vs concurrency: p50, p90*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "short20: throughput vs concurrency"
    x-axis "concurrency" ["×1", "×2", "×4", "×8", "×16", "×32"]
    y-axis "" 0 --> 11.73
    line [1.074, 1.172, 1.176, 1.155, 1.173, 1.161]
    line [9.474, 10.66, 10.57, 10.21, 10.11, 10.41]
```

*short20: throughput vs concurrency: req/s, API tokens/s ÷ 1000*

```mermaid
%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#1f77b4, #ff7f0e, #9467bd, #8c564b, #e377c2, #7f7f7f, #bcbd22, #17becf, #d62728, #aec7e8, #ffbb78, #c5b0d5, #c49c94, #f7b6d2, #c7c7c7, #dbdb8d, #9edae5, #ff9896, #98df8a"}}}}%%
xychart-beta
    title "short20: 429s per second vs concurrency"
    x-axis "concurrency" ["×1", "×2", "×4", "×8", "×16", "×32"]
    y-axis "429 responses/s" 0 --> 1.1
    line [0, 0, 0, 0, 0, 0]
```

*short20: 429s per second vs concurrency: 429/s*

| error | count | example | response |
|---|---|---|---|
| http 424 ModelError container 0 | 1 | ladder-256 ladder-256/ctx256_query50 | {"ErrorCode":"INTERNAL_FAILURE_FROM_MODEL","LogStreamArn":"arn:aws:logs:eu-west-3:<account-id>:log-group:/aws/sagemaker/Endpoints/reranker-aws031-4b-bf16-3","Message":"Received server error (0) from primary with message \"Connection reset by peer for the reranker-aws031-4b-bf16-3 endpoint. Please re |

832 requests, 9,449,536 tokens billed.
