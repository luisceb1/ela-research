# Physical C: measurement and complete-control continuation — 13 November 2026

## Evidence

[User final v4 record](user-final-v4.json): both control FASTQs are reported verified (2,772,553,416 + 2,913,274,103 bytes, published MD5 and recorded SHA256), fastp completed in 246 seconds with 70,948,578 pairs. Alignment started but no final summary/count receipt exists. The supervisor stopped on WSL Windows-executable interop while checking C: availability; cleanup_error null. Peak sampled RSS 4,801,024,000 and sampled combined disk use 42,411,417,295 bytes did not cross existing caps. No memory/disk shortage or biological failure is established.

Final ledger is settled (233/233 attempts, no active requests): 5,858,614,698 observed versus **5,859,663,274 charged**, retaining the original 1 MiB reservation. The user showed `/mnt/c` mounted via 9p, decoded source C:\, aname=drvfs, path=C:\; statvfs reported 563,055,382,528 available bytes. This proves the reported mount identity, not an independently observed Windows Get-PSDrive equality test. No host bytes were fetched by the agent.

## Correction and prospective method

The [amendment](../../research/plans/2026-11-13-gse252892-drvfs-continuation.md) was committed at `7cd35333709d4962ce67b5d7c3b56f4cc353b63e` before implementation/new raw transfer. `physical_free` now uses statvfs only on an exact mountinfo-verified C: drvfs mapping at /mnt/c. Require 9p, decoded source C:\, aname=drvfs, path=C:\, a unique matching mount and sane filesystem availability fields. Another drive, virtual/Linux filesystem, ambiguous or malformed mapping fails. Original PowerShell method remains fallback only if no /mnt/c entry. No WSL-root free-space substitution; physical reserve remains 50 GiB. Repeated Windows process startup is avoided on this verified user mapping.

A new v5 proposal/root binds consumed v4/claim, final supervision/ledger and all 233 settled per-request receipts, both verified-file receipts, fastp log/JSON hashes and inherited evidence. Reject unexpected worker/result/count receipts pending review. Both full files must match published length/MD5 and recorded SHA256, then are copied read-only with streaming digest verification into the new root; no control HTTP. Unsealed old trimmed files/partial alignments are not reused. Identical fastp and complete alignment/count rerun from the beginning. KD transfer is still conditional on control canonical >0.

## Budgets, science and limits

Same 14 GB cumulative cap including **5,859,663,274** charged bytes; expected KD inputs 7,140,765,512 bytes. Minimum cumulative charge 13,000,428,786 leaves 999,571,214 for retries/reservations. No network for reusing control inputs. New 48 h window, same two CPU affinity/8 GiB per-process AS/6 GiB sampled group RSS/**100 GiB across five roots**/50 GiB real C: reserve. All previous roots/claims retained. Sampled guards, concurrent file changes and uninterruptible-I/O limits remain; mount identity can be rechecked on each call. Removing interop calls addresses this observed failure but does not guarantee completion. No cloud purchase/contact/merge.

Fixed libraries/URLs/MD5/reference/targets/fastp and HISAT2 commands/anchor/filter/count units unchanged, verified by original scientific-source regression. No effects/PSI/p-values, independent-donor validation, functional recovery, biological count or reopened closed cycle.

## Validation and next step

[125 focused controls](focused-tests.json) passed with no failures/errors/skips, including ten exact-drive/availability/fallback/reserve tests and eight settled-lineage/full-input integrity tests. Earlier read-only-copy/whole-MD5, sampler-race and scientific-source controls also pass. Compile/diff/link checks pass; full CI must be verified for the final commit. Fixture success is not host execution. No agent-side raw transfer.

Fetch/check out final reviewed commit. Prepare with original base/fastp, prior `/home/luisceb/ela-gse252892-after-sampler-execution-20261113.json`, new root `/home/luisceb/ela-gse252892-drvfs-run-05` and output `/home/luisceb/ela-gse252892-drvfs-execution-20261113.json`. Preparation performs local rehashing, not HTTP. Under standing local authorization, execute only the successful new proposal SHA with 14,000,000,000 cumulative-byte acceptance. Stop on fatal integrity/resource/evidence failure, retry/budget/window exhaustion, failed canonical control or both complete libraries. No automatic restart.
