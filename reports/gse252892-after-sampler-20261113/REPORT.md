# Continuation after sampler failure — 13 November 2026

Current status: v4 completed control transfer/fastp but stopped on Windows interop during disk checking. See [final v4 evidence and drvfs continuation](../gse252892-drvfs-continuation-20261113/REPORT.md). Earlier pending-host statements describe that earlier stage.

## Evidence

The [user terminal record](user-final-v3.json) now supplies final v3 supervision/ledger and verified-file/receipt summaries. Cleanup_error is null after the supervisor race. The first control FASTQ is reported complete: 2,772,553,416 bytes, published MD5 ab0a84e544fa6e2fc1e8c901d0c55675 and recorded SHA256 ddd42a540b6d01ca2405692cd6bf65ae35485c8b5e66f8eda2aec5fc62086bb6. Agent inspection is of terminal text; actual host bytes must be independently rechecked during preparation/worker/copy.

233 requests started, aggregate completed 231; 232 durable receipts (217 complete, 15 failed), 1,809,305,882 complete body bytes. ID232 has a durable complete receipt but remains active in the aggregate snapshot, consistent with interruption between receipt promotion and aggregate update. Count it once. ID233 has 4 MiB observed and 1 MiB in flight. Actual observed cumulative bytes are 3,962,492,159; carry the conservative **3,963,540,735** as spent. Do not equate the last heartbeat with final accounting or discard the reservation.

Arithmetic after the first-file attempts implies **123 second-file blocks / 1,031,798,784 bytes**. Host preparation requires every actual block/receipt to match; this is a conditional reuse inventory, not an agent measurement of host files. No fastp/alignment or biological result is demonstrated.

## Method

The [prospective amendment](../../research/plans/2026-11-13-gse252892-after-sampler.md) was committed at `0df81e7374a474c726928de3899e4e32c0ed4b7b` before implementation/new live requests. A separate v4 proposal/root binds consumed v3 identity/claim, supervision/ledger, all 232 durable receipts, verified-file receipt, inherited v1/v2 evidence and absent worker-failure receipt. Per-ID reconciliation merges the durable/active ID232 without double counting and charges ID233's 1 MiB reserved tail. New ledgers distinguish prior observed bytes from unobserved bytes charged; actual body totals no longer include that reservation as if observed.

Validate the first complete input's published length/MD5 and recorded SHA256, then copy into the new root while hashing the stream again. No hard link, HTTP, alteration or deletion of the old file. Original first-file temporary pieces removed after successful promotion need not exist; the complete verified file supersedes them.

Recheck all 123 second-file block identities/intervals/filenames/location/size/SHA256, including ID232 if its durable receipt is valid. Failed/pending partials remain evidence and are not imported. Probe the first 1 MiB remotely against the retained first block, then request only uncovered ranges with unchanged 8 MiB blocks, two connections, five attempts and 2/10/30/60 s backoffs. Keep strict 206/range/length/validator/TLS, numeric Retry-After <=120 s, no redirect/mirror/full fallback and original full-file MD5 promotion rules. Complete old blocks remain read-only. No automatic cross-run continuation.

## Budgets and scientific scope

14 GB cumulative cap including **3,963,540,735 prior charged bytes**. Conditional minimum new body transfer is 9,023,289,407 (including fresh overlap); cumulative minimum 12,986,830,142 leaves 1,013,169,858 for retries/reservations. Transfer-body accounting excludes protocol overhead. A new 48 h window, two CPU affinity/8 GiB per-process AS/6 GiB sampled group RSS/**100 GiB across four roots**/50 GiB actual C: reserve remain. The corrected sampler handles atomic leaf renames; sampled-quota and uninterruptible-I/O limitations persist. No cloud purchase is justified by this failure or authorized here.

Same fixed libraries/four URLs/MD5/reference/targets/commands/filters/anchor 15/paired query-group-event count unit. Original scientific-function source hashes still match. Control first, KD only if canonical >0. No effects/PSI/p-values, independent-donor generalization, functional recovery or reopened #37/#44/STMN2 cycle.

## Validation and next step

[Focused tests](focused-tests.json): **107 passed**, no errors/failures/skips. Fifteen new controls include stale aggregate/durable deduplication, reserved-tail retention and observed-vs-charged labels, missing/changed source evidence, whole-file copy without source mutation/linking, digest failure without promotion, retained-only first-block probe and missing-range/full-MD5 assembly. Six sampler regressions and prior scientific controls also pass. Compilation/diff/link checks pass. No agent-side live raw requests. Fixture success is not host success; prepare/worker must validate actual files.

Fetch/check out the reviewed PR commit. Prepare with original base/fastp and `--prior-plan /home/luisceb/ela-gse252892-retained-execution-20261113.json`, new `--run-root /home/luisceb/ela-gse252892-after-sampler-run-04`, `--output /home/luisceb/ela-gse252892-after-sampler-execution-20261113.json`. Preparation performs no HTTP. Under standing local authorization, execute only the actual successful new proposal SHA with the same cumulative 14,000,000,000-byte acceptance. Retain all prior roots/proposals. Stop on fatal evidence/integrity/resource failure, exhausted retry/budget/window, failed canonical control or both libraries complete. No merge/contact/spending.
