# GSE252892 transport recovery — 13 November 2026

Current status: the v2 host attempt subsequently failed on a short range after bounded retries. See the [retained-block continuation](../gse252892-retained-continuation-20261113/REPORT.md). Earlier test results and commands below describe v2, not a successful live completion.

## Evidence

The [user terminal record](user-failed-run.json) reports HTTP 200 followed by premature EOF in the first control FASTQ: 351,927,726 of 2,772,553,416 expected bytes. The old run stopped after 2,098.952 seconds with a raw length/MD5 mismatch, cleanup_error null and peak sampled group RSS 38,105,088 bytes. No fastp or alignment ran. The agent has inspected supplied terminal text, not the original host files. Preparation must recheck those files.

The prospective [amendment](../../research/plans/2026-11-13-gse252892-range-transport.md) was committed at `9438011817f47e3734051002bd177ee0b2323520` before implementation and before any new live range request. Agent validation uses synthetic transport fixtures only; no raw sequencing bytes have been fetched by this recovery work.

## Interpretation

An incomplete transfer is demonstrated; its underlying network/server cause is unknown. Neither RAM/CPU exhaustion nor inadequate biological coverage is established. Keep the old failed attempt intact; do not rerun its consumed proposal or delete its claim.

The new transport requires exact-origin HTTP 206, exact range endpoints, total and length. There is no ignored-Range HTTP 200 fallback, redirect or mirror. Each block is 32 MiB; at most four connections per file, three attempts per block and 120 seconds per socket. Retry backoffs are 2/10 seconds. A numeric server Retry-After up to 120 seconds is honored if longer; larger or date-form hints stop for review. TLS certificate failures, local I/O, changed validators, integrity and budget failures are fatal. Strong ETag/If-Range is used when provided; the complete original MD5 remains mandatory even without a strong validator.

Old-prefix reuse binds the old proposal, consumed claim, accepted receipt, supervision, failure and ledger hashes; exact local size/SHA256 and gzip signature are checked. A remote overlap of the last 1 MiB must match before the suffix. Assembly checks offsets, block size/digests and the full original MD5/length before promotion. The old partial is read-only. Failed pieces and attempt receipts remain; successful temporary pieces may be removed only after full verification.

## Budgets and unchanged science

The 14,000,000,000-byte lineage cap includes 351,927,726 bytes already charged. Four complete advertised inputs total 12,826,593,031 bytes. Conditional reuse requires at least **12,475,713,881 new body bytes**, including the 1 MiB overlap, before retries. Observed bytes, conservative unknown-tail charges and in-flight reservations are distinct. Reservations are persisted under a lock before reads. A bounded aggregate ledger plus separate per-attempt receipts avoids an ever-growing heartbeat payload. HTTP/TLS overhead is outside the body-byte metric.

The new 48 h window is prospectively longer than v1's 12 h because transport was slow. CPU affinity remains two logical CPUs, per-process address space 8 GiB, sampled process-group RSS 6 GiB, **combined old/new roots** 100 GiB, and actual Windows C: reserve 50 GiB. These are sampled guards, not kernel-enforced aggregate quotas; uninterruptible I/O and sampling gaps remain limitations. No cloud purchase is needed on the present evidence or authorized by this change. Four connections need not improve throughput.

The same two single-background libraries, four URLs/MD5s, sealed coordinates, fastp/HISAT2 commands, paired query-group/event unit, anchor 15 and filters remain. Control first; KD only if control canonical >0. [Source hashes](scientific-functions-66eb858.json) and a regression test pin the exact original commands/events/pair_hits/count_records source. This is measurement reproducibility in a single genetic background, not independent-donor validation, an effect estimate, PSI or functional recovery. No #37/#44/STMN2 cycle is reopened.

## Validation and limitations

[Focused tests](focused-tests.json): 70 executed/passed, no failures/errors/skips. Fixtures cover strict range handling, premature EOF/retries, immutable prefix and remote overlap, block ordering and complete MD5, concurrent cap reservations and uncertain tails, old charge/claim binding, resource settings, scientific-source equality and prior runner/preparer controls. Test success does not establish ENA range support or live end-to-end success. No biological result exists from either attempt yet.

## Next user-host step

Fetch the reviewed recovery commit and check it out in `/home/luisceb/proyectos/ela-local-20261112`. Run the following preparation command from PowerShell. This performs local validation and writes a new proposal without HTTP:

```powershell
wsl -d Ubuntu-24.04 -- /home/luisceb/proyectos/ela-research-piloto/.venv/bin/python /home/luisceb/proyectos/ela-local-20261112/scripts/run_gse252892_local.py prepare --base-descriptor /home/luisceb/ela-gse252892-prepared-20261112.json --fastp /usr/bin/fastp --prior-plan /home/luisceb/ela-gse252892-execution-20261112.json --run-root /home/luisceb/ela-gse252892-range-run-02 --output /home/luisceb/ela-gse252892-range-execution-20261113.json
```

Then accept the new actual proposal SHA with `execute --plan ... --accept-plan-sha256 ... --accept-transfer-bytes 14000000000`. The old proposal must remain consumed. Stop at first fatal failure, retry/cap/window exhaustion, failed control or completion of both libraries; no automatic cross-run resume. Substantial local-resource authorization already persists; paid cloud, contacts and merging need their separate authority.
