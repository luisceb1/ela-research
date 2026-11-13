# Prospective retained-block continuation — 13 November 2026

Parent runtime: `69a33bcc7bb61311b717a5634b642a8245d29d5f`, PR #78. Commit this amendment before implementation and any further live request. This is a new proposal/root, never a mutation or rerun of consumed v1/v2. Luis's standing local download/CPU authorization applies; no cloud spending, contact or merge.

## Evidence and prediction

User-supplied v2 receipts summary: 60 finished attempts, 50 complete (1 MiB overlap plus 49 x 32 MiB blocks), 10 failed; 1,645,215,744 bytes in complete attempts. A range at 1,962,540,462–1,996,094,893 exhausted three attempts (0, 29,407,660, 0 bytes); other requests were subsequently cancelled. Observed v2 body bytes 1,759,157,246; prior v1 351,927,726; cumulative charged total 2,111,084,972, active requests none, cleanup_error null. No fastp/alignment or biological result. HTTP range support and initial prefix overlap succeeded; underlying truncation cause remains unknown.

Prediction: valid complete blocks can reduce repeated transfer, but continued network failures may still prevent completion. Check receipt identity, coverage and every on-disk block hash before counting anything as reusable. Reject altered/missing evidence; do not infer that every received byte is usable.

## Fixed change

New schema v3, root and single-use proposal. Bind exact consumed v2 plan SHA `98a89d95c199fb13e90ac5f68c2b33cec1251daf62313d83ec4b4b1fe649af6d`, its claim/accepted/supervision/failure/aggregate ledger, all 60 attempt receipts and unchanged v1 lineage. Only complete 32 MiB block receipts for the fixed first file may supply assembly pieces. Exclude the overlap probe as an assembly piece. Require unique expected intervals, exact observed/charged lengths, no uncertain tails, hashes, regular files confined to the old range directory, and no overlapping pieces. Verify all original bytes again at preparation/worker use/assembly. Failed partials remain evidence and are not reused.

Acquire a fresh last-1-MiB overlap against the unchanged v1 prefix. Combine that prefix, validated retained complete blocks and newly downloaded missing intervals by exact byte offset. Never remove/write old blocks, old prefix, receipts or claims. Verify original whole-file MD5/length before any biological processing.

For missing intervals and subsequent files use 8 MiB blocks, **two** connections, 120 s socket timeout, **five** attempts, backoffs 2/10/30/60 s; numeric Retry-After <=120 s is honored if longer, other forms stop. The smaller block and reduced concurrency are prospective transport choices, not proven remedies. Strict 206/exact range/length, no redirects/mirrors/full-file fallback, validator/integrity/TLS/budget stops remain. These settings do not change the assay.

Keep 14,000,000,000 body bytes **including all 2,111,084,972 already charged**. Count retries, new overlap, uncertain tails and in-flight reservations. Fresh 48 h window, same two CPU affinity/8 GiB per-process AS/6 GiB sampled group RSS/100 GiB across all three roots/50 GiB actual C: reserve. No automatic restart; any later continuation requires a new explicit prospective record and proposal.

## Unchanged question and stop

Same two libraries/four fixed URLs/MD5/reference/targets/commands/filters/anchor/count units; control first and KD only if canonical >0. No effects, PSI, p-values, donor generalization or functional recovery. Source-hash regression pins original scientific functions. Fixtures must cover retained hash/path/interval tampering, holes/order, immutable old files, cumulative accounting and no full-file promotion after incomplete/incorrect assembly. No agent-side raw retrieval. Stop on first fatal failure, exhausted retry/budget/window, failed canonical control or both completed libraries. Report test success separately from live execution.
