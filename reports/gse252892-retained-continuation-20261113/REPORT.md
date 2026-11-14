# Retained-block continuation — 13 November 2026

Current status: the v3 host run subsequently stopped on a supervisor disk-sampling race. See the [race diagnosis and fix](../gse252892-disk-sampling-fix-20261113/REPORT.md). Earlier counts below describe software tests and prospective transfer, not successful live completion.

## Evidence

The [user-supplied v2 failure record](user-v2-failure.json) establishes a short range body after bounded retries, not inadequate biological coverage. Of 60 completed attempts, 50 were complete: the 1 MiB overlap and 49 full 32 MiB blocks (1,644,167,168 bytes excluding the probe). Ten failed attempts include peer cancellations after one range exhausted three attempts. Total actual/conservative lineage charge is 2,111,084,972 bytes with no outstanding requests. Cleanup completed. No fastp/alignment ran; the underlying network/server cause is unknown. Original host files have not been fetched by the agent.

The [amendment](../../research/plans/2026-11-13-gse252892-retained-blocks.md) was committed at `a20f5384790036b48a288377b31332f523192b2e` before implementation or new live requests. The old v1/v2 proposals remain consumed and unchanged. This continuation is in the existing unmerged PR #78; the earlier v2 result remains in history.

## Method and controls

Offline preparation of schema v3 binds the exact consumed v2 proposal SHA, claim/accepted/supervision/failure/ledger, all 60 attempt receipts and inherited v1 evidence. A complete block must have the expected original interval, URL, length, observed/charged bytes, no uncertainty, exact filename and regular-file location in the old range directory; its size/SHA256 are rechecked. Exclude the overlap probe from assembly coverage. Refuse missing or changed evidence rather than lowering the expected count. The original prefix is also rechecked. Failed partials are retained but never reused as assembly pieces.

Worker validation repeats these checks. A fresh remote overlap is charged and compared; only uncovered intervals are requested, in 8 MiB blocks with two simultaneous connections, five attempts and 2/10/30/60 s backoffs. Existing exact-range/length, validator, TLS, numeric Retry-After <=120 s and no-redirect/mirror/full-file-fallback policies persist. Smaller requests/reduced concurrency are prospective transport choices with no performance or success guarantee. Each assembly block is verified again; only the complete original file length/MD5 permits biological processing. Preserve all old bytes/receipts; successful new temporary blocks may be removed after promotion. There is no automatic cross-run resume or retry beyond the new proposal.

The **14 GB cap includes 2,111,084,972 old bytes**. Conditional reuse covers 351,927,726 prefix bytes plus 1,644,167,168 block bytes. Minimum new transfer for all four inputs, including the fresh 1 MiB overlap, is **10,831,546,713 bytes**, before retries. Minimum cumulative charge is 12,942,631,685, leaving 1,057,368,315 bytes for retries/conservative charges. Observed body bytes, uncertain-tail charges and in-flight reservations remain distinct; protocol overhead is outside this metric.

Fresh 48 h window, two CPU affinity, per-process AS 8 GiB, sampled group RSS 6 GiB, **100 GiB across all three roots**, real Windows C: reserve 50 GiB. Sampled limits and uninterruptible-I/O limitations remain. Present evidence gives no reason to buy cloud capacity.

## Unchanged science

Same libraries GSM8009878/SRR27477544 and GSM8009881/SRR27477541, same four fixed URLs/MD5, reference/targets, fastp/HISAT2 commands, filters, anchor 15 and paired query-group/event unit. Control first; KD only if canonical >0. The historical [scientific-source hashes](../gse252892-range-recovery-20261113/scientific-functions-66eb858.json) still match exactly. No effect, PSI, p-value, independent-donor validation, functional recovery or reopened #37/#44/STMN2 cycle.

## Validation and next step

[Focused controls](focused-tests.json): 86 passed, no failures/errors/skips, including 16 new controls for retained evidence, cumulative charges, source/path/interval/hash tampering, gaps, whole-file MD5, old-file immutability and smaller-block coverage. Python compilation and diff checks pass. Only fixture bodies were used; no new live raw requests were made by the agent. Host evidence validation and live success remain pending.

Fetch/check out the final reviewed PR commit in the existing local worktree. Prepare with the same base and fastp but `--prior-plan /home/luisceb/ela-gse252892-range-execution-20261113.json`, new `--run-root /home/luisceb/ela-gse252892-retained-run-03` and `--output /home/luisceb/ela-gse252892-retained-execution-20261113.json`. Preparation performs no HTTP. Execute only a successful actual new proposal SHA, accepting the same 14,000,000,000-byte cumulative cap. Luis's standing local-resource authorization covers this bounded continuation; no further permission loop is needed. Stop at fatal error, retry/cap/window exhaustion, failed canonical control or both complete libraries.
