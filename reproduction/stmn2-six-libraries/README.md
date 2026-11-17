# Minimal six-library STMN2 technical replay

**Prepared, not yet replayed on real FASTQs in a clean environment.** This entry
point measures exactly the existing GSE252892 STMN2 targets with the original
counter. It does not need historical run directories, consumed proposals,
transport ledgers or the original user's home directory.

The question is technical transferability of a known result, not new biological
replication. All six libraries share one WA01/H1 background; independent
cultures/differentiations and protein efficacy remain unverified. No normalized
effect, PSI, statistical test or functional recovery is calculated.

## Fixed inputs and expected measurements

| GSM | Run | Declared condition | Canonical | Cryptic |
|---|---|---|---:|---:|
| GSM8009878 | SRR27477544 | Control | 1945 | 3 |
| GSM8009879 | SRR27477543 | Control | 2806 | 5 |
| GSM8009880 | SRR27477542 | Control | 2438 | 0 |
| GSM8009881 | SRR27477541 | KD | 253 | 727 |
| GSM8009882 | SRR27477540 | KD | 173 | 551 |
| GSM8009883 | SRR27477539 | KD | 140 | 556 |

Units: contiguous eligible paired query groups per event per library, minimum
15 aligned anchor bases. A zero is an observed count, not biological absence.
The 20-group diagnostic is descriptive. The comparison targets are already known.

The [manifest](manifest.json) pins twelve compressed FASTQs, source URLs,
published lengths/MD5s, archived host-reported SHA256s, eight index shards, original
result/QC records, and source-document hashes. Total compressed input is
**40,589,186,698 bytes**. Those files are not included or downloaded by this
package. This preparation did not rehash the actual FASTQs.

## Immediate offline check — no raw inputs needed

From the repository root, with Python 3.11/3.12:

```sh
python scripts/replay_stmn2_minimal.py compare \
  --results reports/gse252892-stmn2-result-20261115/original/result.json \
            reports/stmn2-remaining-result-20261116/original/result.json \
  --output /tmp/stmn2-archived-comparison.json
```

Use a new output filename on each invocation. Expected status: `records_match`,
`raw_replay_verified: false`. This validates all six result identities, units,
completion flags, canonical/cryptic counts and five QC totals against the pinned
reference. It is a check of supplied JSON, **not a FASTQ reproduction**. Supplied
per-library `stmn2-counts.json` files are accepted too. Missing libraries or changed
records return exit 1; malformed, duplicate, unexpected or invalid records return
exit 2. Output is never overwritten. A standalone matching JSON cannot establish
whether the caller actually ran the pipeline.

## Later real-data replay prerequisites

Real replay has not been started or scheduled by this preparation. Use a clean
checkout of the reviewed PR commit and a dedicated environment:

- Native Linux, Python 3.11 or 3.12, PySAM **0.23.3** (the existing
  [pinned requirement](../../research/requirements-pe-contract.txt)).
- **fastp 0.23.4** and the native **hisat2-align-s 2.2.3** binary, rather than the
  `hisat2` wrapper. A different build with the same version is recorded as
  `historical_build_match: false`; it is not called an identical tool binary.
- All twelve original compressed FASTQs already available locally. Sources and
  checksums are in the manifest; obtaining them is a separate resource decision.
- The original hg38 **genome.1.ht2–genome.8.ht2** files already extracted into one
  directory. The [index source record](../../reports/hisat2-index-inspection-20261031/verified_index.json)
  supplies the versioned archive URL and checksum. Exact shard digests are
  mandatory; a same-named or rebuilt index is not accepted.
- An existing output parent filesystem with at least **150 GiB free**, including
  space for this replay's output and a **50 GiB reserve**. Inputs/index remain
  outside the new output root. Extra free RAM is needed for the OS and other apps;
  the worker's sampled RSS limit is 6 GiB and each process's AS limit is 8 GiB.

**This portable entry point rejects WSL.** Guest free space does not establish
physical host drive capacity. The historical WSL executors remain preserved;
this guide does not claim that a portable replay can already run on Luis's WSL
machine or introduce a host-space assumption to make it pass.

Copy [paths.example.json](paths.example.json) outside the checkout and replace
the twelve values with absolute local paths. The files may live in different
directories; they are read in place, never copied, moved or deleted. The map must
contain exactly the fixed filenames and distinct source files.

## Prepare without alignment

The following are **path placeholders**, not a command to run unchanged:

```sh
python scripts/replay_stmn2_minimal.py prepare \
  --paths /absolute/path/stmn2-paths.json \
  --index-dir /absolute/path/hg38 \
  --fastp /absolute/path/fastp \
  --aligner /absolute/path/hisat2-align-s \
  --run-root /absolute/path/stmn2-replay-01 \
  --output /absolute/path/stmn2-replay-plan.json
```

Preparation reads/hashes about 40.6 GB of FASTQs plus the index and can take
minutes. It checks exact raw lengths/MD5/SHA256, index digests, versions, tool
digests, code/target/source bindings and filesystem capacity. It emits a new
plan, its SHA256, all command arguments and `prepared_not_executed`. It performs
no trimming, alignment or raw download. Keep the checkout clean and unchanged
between prepare and run; put maps, proposals and outputs outside it.

## Explicit supervised execution

Once a real replay is separately selected with the required local inputs and
resources, substitute the exact SHA returned by prepare:

```sh
python scripts/replay_stmn2_minimal.py run \
  --plan /absolute/path/stmn2-replay-plan.json \
  --accept-plan-sha256 SHA256_RETURNED_BY_PREPARE
```

The single-use plan is claimed before execution. The worker rehashes sources and
index, then processes all six libraries sequentially, with the original fastp/
HISAT2 option order (paths substituted) and unchanged STMN2 counter. SAM is
streamed; no BAM is stored. Successful-library plain trimmed intermediates are
removed only inside this new output root. A failed library's files/logs remain.
No count-based early stop, automatic retry/resume or modification of references
is allowed. Repeating a consumed plan is refused, even after failure.

The supervisor enforces 96 h wall and two CPU affinity slots with an 8 GiB
per-process AS limit. It samples group RSS (6 GiB), new output size (100 GiB)
and free filesystem reserve (50 GiB) every 0.5 s. Sampling is not an aggregate
kernel quota, external disk use can change capacity, and uninterruptible I/O can
prevent timely termination. A cleanup error fails the replay explicitly.
No network transfer is implemented; this is **not OS network isolation or measured
zero network traffic**. Dependencies/tools must already be installed.

## Inspect the outcome

Retain the plan/claim, `accepted.json`, per-library fastp/HISAT logs and count JSON,
`worker.log`, `result.json`, `comparison.json` and `supervision.json`. Retain
`worker-failure.json` if present. A successful local report needs all six matching
count/QC records plus successful supervision without a cleanup error. These are
unsigned local records, not independent host attestation. Different tool builds
remain visible in the plan even if all outputs agree.

On discrepancy or failed/incomplete processing, preserve all evidence and stop;
do not change filters, counts, targets or expected values to obtain a match.
Even perfect agreement supports technical reproducibility only. It adds no
independent donor, experiment, functional recovery or clinical claim.

[Prospective scope and stop rules](../../research/plans/2026-11-17-stmn2-minimal-replay.md)
· [Preparation evidence](../../reports/stmn2-minimal-replay-20261117/REPORT.md)
