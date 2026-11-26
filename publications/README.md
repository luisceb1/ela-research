# Public findings catalog

`catalog.json` is the editorial source for the bilingual ELA Research website at https://www.cebr.xyz/ela/hallazgos and https://www.cebr.xyz/ela/en/findings.

Only add findings explicitly cleared for public distribution and documented in a reviewed report. A completed run or a merged research report alone does not constitute publication approval. Include limitations, negative findings, and later corrections, and keep the two language versions equivalent. A catalog entry is a public summary, not a new analysis or independent review.

The catalog uses version 1. Each entry has a unique stable URL slug (`id`, lowercase ASCII letters, digits and hyphens), ISO date, `status` (`reproduced`, `partial`, `refuted`, `pending`), bilingual `title`, `question`, `result` and `limitations` objects with `es` and `en` strings, relative report path (`report` beginning `reports/` or `docs/`), and HTTPS primary source (`source`). Optional `visual` is `datos` for the existing STMN2 visualization. Keep existing slugs stable when correcting a finding. The website reads the public catalog from main, validates it, and caches it for an hour. Failed or malformed updates fall back to the previous valid catalog where available, or to the embedded initial snapshot.
