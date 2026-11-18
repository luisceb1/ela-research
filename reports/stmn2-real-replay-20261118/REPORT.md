# Six-library STMN2 local FASTQ replay — evidence audit, 18 November 2026

## Evidence

The supplied host bundle records successful replay of all six fixed GSE252892
libraries with the new entry point, on the same PC and WSL2 distribution holding
the historical inputs. It used a fresh code worktree and dedicated Python
environment, while reusing original FASTQs, index and native tool builds.

Execution commit: `b72c877acf02b62fc34ef6a170e7142a9889de69` (PR #86).
Accepted plan SHA256:
`423ccc524120b098c6ed1e7f8b98b76522487c369048d952509e78f0cecb9dd4`.
Supplied archive SHA256:
`8a86442368c7e2db37bc579d98b279545085dcc695ce16b509a6e16aae1e0532`.
Result SHA256:
`74621ab7f15ef565118a2a494467b1a340e06924165c5870edbd877db93bce1a`.

| Library | Declared condition | Canonical | Cryptic |
|---|---|---:|---:|
| GSM8009878 | Control | 1945 | 3 |
| GSM8009879 | Control | 2806 | 5 |
| GSM8009880 | Control | 2438 | 0 |
| GSM8009881 | KD | 253 | 727 |
| GSM8009882 | KD | 173 | 551 |
| GSM8009883 | KD | 140 | 556 |

Units remain contiguous eligible paired query groups/event/library with minimum
15 aligned anchor bases. All **12 event counts and 30 QC fields** match the
prefixed reference exactly. The controls with 3, 5 and 0 cryptic groups remain
included. See [original result](original/result.json), [table](results.tsv), and
[machine-readable audit](audit.json).

The agent audited the 43 files in the received bundle, without extracting or
executing its contents. Checks include the plan bytes/hash, execution-commit code
hashes, twelve declared FASTQ identities and historical tool digests, fixed
commands, plan/claim/acceptance/supervision links, six per-library versus aggregate
records, and a fresh offline comparison against the repository reference.
For each library, fastp's after-filter total reads equal twice HISAT2's input
pairs; HISAT2's unique/multiple concordant pairs reconcile with the counter QC.
The supplied HISAT2 logs and summaries are identical.

| Recorded supervision quantity | Value |
|---|---:|
| Elapsed wall time | 25,314.577 s (7 h 1 min 54.577 s) |
| Peak sampled worker-group RSS | 4,797,501,440 bytes (4.47 GiB) |
| Peak sampled new output | 44,068,567,914 bytes (41.04 GiB) |
| Minimum sampled physical C: availability | 457,662,414,848 bytes (426.23 GiB) |
| Failure / cleanup error | null / null |
| Supervisor raw execution reported | true |

The original archive remains with the user. Host registry GUIDs, absolute paths,
full plan and HTML reports are not republished in this derived audit; member
digests bind the supplied originals. The result JSON is retained byte-for-byte.

## Interpretation

The supplied records support **successful local technical replay** using the new
entry point, with exact count/QC agreement and no recorded supervisor failure.
This closes the practical question of whether that entry point can reproduce
these six known measurements on this configured host without the old execution
descriptors. No thresholds, targets or expected results were changed.

`comparison.json` correctly retains `raw_replay_verified: false`: the comparator
only evaluates supplied JSON. The separate supervisor reports
`raw_execution_reported: true`. Neither field authenticates the host; preserve
both meanings rather than promoting the comparator flag to a stronger claim.

## Limitations

These are unsigned user-supplied files, not independent host attestation. Raw
FASTQs, installed binaries and index shards are not in the received bundle, so
the agent did not independently rehash them; their checking is reported by the
hash-bound execution code and plan. The historical data, operator and PC are
reused. This is not reproduction on an unrelated machine or an independent
donor/culture experiment. One WA01/H1 background remains; culture/differentiation
independence and protein efficacy remain unverified. No normalized effect, PSI,
statistical test, neuronal rescue or clinical benefit is established.

Sampled limits are observations, not kernel aggregate quotas or network telemetry.
Source retention remains undecided; no deletion or new execution follows closure.

## Validation and next discriminating step

The bundle audit passed; twelve altered/unsafe evidence cases were refused,
including changed counts/QC, altered receipts, failed/exceeded supervision,
changed preprocessing commands/pairs, missing logs and unsafe archive paths.
[Mutation results](mutation-checks.json). Software checks are not experiments.

Re-run the record audit, with the original bundle outside the checkout, using:

```sh
python scripts/audit_stmn2_replay_bundle.py \
  --bundle /absolute/path/stmn2-replay-evidence-20261118.tar.gz \
  --output /absolute/path/new-audit.json
```

Negative controls can be repeated with a new output filename:

```sh
python scripts/check_stmn2_replay_audit_mutations.py \
  --bundle /absolute/path/stmn2-replay-evidence-20261118.tar.gz \
  --output /absolute/path/new-negative-checks.json
```

The 23 existing minimal-replay tests and script compilation also passed after
adding this record-audit tooling; the prior WSL preparation's full suite remains
reported separately in its dated validation record.

The execution commit must exist in local git history. No alignment, source
download or external host access is performed by this audit.

Do not replay these libraries again merely to accumulate confirmations. A future
portability test would require an independently configured host/operator; further
biological progress requires qualifying independent data or design metadata.
PR #83 remains paused; existing ADWB/author input gates are unchanged.
