# Prospective continuation after supervisor race — 13 November 2026

Parent fix `97d58ecb51c4f3f8d08b2bbbd017fe2f6c5619f3`. Commit before implementation and new live requests. Standing local-resource authorization persists; no cloud purchase, contact or merge. All scientific methods, libraries, source URLs/MD5, reference/targets, count units and control-first/KD gate stay fixed.

## Observed state

The user supplied final v3 supervision (failed, cleanup_error null), proposal SHA `e131b017001b8f8f5b877c2aeb1aa4589609f9639f1c5b4093af9de359fac1ca`, ledger and verified-file/receipt summary. First control FASTQ is complete, 2,772,553,416 bytes, MD5 ab0a84e544fa6e2fc1e8c901d0c55675, SHA256 ddd42a540b6d01ca2405692cd6bf65ae35485c8b5e66f8eda2aec5fc62086bb6. 232 durable attempt receipts: 217 complete, 15 failed, complete body bytes 1,809,305,882. First-file complete attempt bytes include 777,507,098 newly completed bytes/probe; the remaining 1,031,798,784 bytes imply 123 full 8 MiB second-file blocks. Validate actual receipts/bytes before reuse; do not treat this arithmetic as host inspection.

Ledger: prior 2,111,084,972; new observed/charged 1,851,407,187; actual 3,962,492,159; conservative upper **3,963,540,735**. 233 started, 231 aggregate-completed, active IDs 232/233. ID232 has a durable complete receipt written before aggregate finalization (8 MiB already observed, no reservation); count it once. ID233 has 4 MiB observed and 1 MiB reserved; do not reuse its partial. Worker-failure receipt absent after supervisor termination. No fastp/alignment/biological result.

## Fixed recovery

New v4 proposal/root binds consumed v3 proposal/claim, final supervision/ledger, all 232 durable receipts, verified-first-file receipt, inherited v1/v2 lineage and absence of worker-failure receipt. Reconcile each request ID once against aggregate and active entries; carry the 1 MiB uncertain in-flight reservation as spent, never reset it. Reject missing/changed evidence or inconsistent identities/totals.

Revalidate first FASTQ full published MD5/length and recorded SHA256, then copy read-only source into a new root with streaming digest verification and atomic promotion. Original remains untouched; no HTTP for this file. Completed first-file temporary pieces were removed legitimately after promotion; do not require or reconstruct them. The full file supersedes those pieces.

Only complete second-file 8 MiB receipts may supply retained pieces, including durable ID232 if valid despite stale aggregate status. Validate exact URL/total/interval/filename/size/SHA256 and non-overlap. Probe first 1 MiB remotely against the retained first block; download uncovered intervals with existing 8 MiB/two-connection/five-attempt/2-10-30-60 s policy. Strict HTTP206/range/length/validator/TLS/no-redirect/no-fallback and full-file MD5 policies persist. Keep all old roots/claims/bytes immutable. No automatic continuation of consumed proposals.

14 GB lineage cap includes **3,963,540,735** conservative prior bytes. With 123 valid second-file blocks, minimum new body transfer for remaining inputs including fresh overlap is **9,023,289,407**; minimum cumulative 12,986,830,142 leaves 1,013,169,858 for retries/reservations. New 48 h window; two CPU affinity, 8 GiB per-process AS, 6 GiB sampled group RSS, **100 GiB across four roots**, real Windows C: reserve 50 GiB. The corrected sampler tolerates atomic leaf renames; sampled/quota/I/O limitations remain.

## Controls and stop

Fixture tests: stale aggregate/durable receipt deduplication, unknown reserved-tail retention, changed evidence/source/full-file or block hashes, missing/duplicate intervals, read-only source preservation, copy promotion only after full digest, probe/holes and original scientific-source equality. No agent-side live raw transfer. Prediction: verified bytes can avoid repeating their transfer; completion is not guaranteed. Stop on fatal integrity/resource/evidence failure, exhausted bounded attempts/budget/window, failed canonical control or both libraries complete. No effects/PSI/inference, donor generalization or functional recovery claim. Report software checks separately from host success.
