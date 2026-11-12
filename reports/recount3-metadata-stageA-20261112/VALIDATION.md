# Stage A verification — 12 November 2026

Executed documentary/data-integrity checks:

- Query lock is committed at `3bbc9326a926a77e6224600a8250e189d5c679b3`, after the unchanged prospective plan `55ab5a8777887d855c19e8b3d725517deeb67473` and before all scientific response timestamps.
- Five executed locked queries; sixth omitted at the 30-distinct-series cap. Thirty unique GEO series IDs; no 31st series opened. All 30 records classified and no eligible/nominated project.
- Catalogue decisions: 12 prior/sibling exclusions, 14 scope rejections, three design rejections, one unresolved metadata case archived as closed. Same publication/other assay not counted as independent replication.
- Twenty-six culture-only library metadata rows: six DCPS, six APA whole-transcriptome, four simple-KD/guide-control NMD, ten local-transport soma. The WA01 and WTC11/WTC-11 assignments are source fields; no clinical sample rows are exported.
- All 39 body lengths and SHA256 hashes recomputed from raw response cache; 636,037 total bytes, largest 304,899, all HTTP200 and no retry/error/truncation. No count/raw experimental file URL in the request manifest. Exact cache-body/hash linkage checked.
- Stage B manifest empty, coverage not measured, Stage B not authorized. No legacy diagnostic boolean promoted to inferential readiness; no threshold-200 exclusion.
- Frozen coordinate JSON and probe source SHA256 match the plan. They, the prior intervention matrix and original recount3 result JSONs remain byte-identical to plan base. Only this metadata-screen work and dated status entries are changed.
- JSON/TSV parse, required fields, local Markdown links and `git diff --check` checked before publication of the result commit.

This is not a full scientific-software suite run, independent methodological review, biological replication or validation of uninspected fields. New production analysis code is not introduced; scripts in `execution_snapshot` are historical acquisition snapshots with the original paths. Software CI must be read on the actual PR head; no passing CI is claimed here. Header/TLS overhead and server-side work are not counted as measured payload bytes. No live acquisition is repeated for verification.

Verified timing: remote query-lock committer timestamp 2026-11-12T09:54:34Z; first scientific acquisition request 2026-11-12T09:55:23.615554Z. Offline checks passed for 30 unique series, five locked queries, 26 mapped culture libraries, all 39 source-body hashes/lengths, empty Stage B manifest, unchanged frozen measurement/prior-result bytes and 13 local report/plan links.
