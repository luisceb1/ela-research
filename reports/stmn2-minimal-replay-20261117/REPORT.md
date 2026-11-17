# Minimal STMN2 technical replay preparation — 17 November 2026

## Evidence

Luis authorized this bounded software contribution after AD Workbench and author
inputs remained unavailable. The [scope/stop rules](../../research/plans/2026-11-17-stmn2-minimal-replay.md)
were committed locally at `86116af` before implementation and deposited as the
[parent protocol commit](https://github.com/luisceb1/ela-research/commit/2994248d814d2d27b2ed33b9d77841027f1b040d). No new biological
question, target measurement or raw execution was started.

The [guide](../../reproduction/stmn2-six-libraries/README.md) now provides one
entry point for six fixed GSE252892 libraries, independent of historical host
paths and consumed proposals. The [manifest](../../reproduction/stmn2-six-libraries/manifest.json)
contains twelve FASTQ identities (40,589,186,698 compressed bytes), eight original
index shard hashes, source bindings, expected count/QC records and historical
tool digests. Raw SHA256s are preserved host-reported digests; this preparation
did not read or rehash the actual FASTQs. New raw transfer: none performed.

The standalone comparator was executed against the two deposited original
aggregate result files: [archived-comparison.json](archived-comparison.json).
All six library identities, units, completion/control flags, counts and five QC
totals match. The controls' cryptic counts **3, 5 and 0** remain visible; KD counts
remain **727, 551 and 556**. The comparison explicitly reports
`raw_replay_verified: false`. It is metadata agreement, not a raw-data replay.

The [new script](../../scripts/replay_stmn2_minimal.py) prepares an immutable
local-input plan without alignment, then exposes a separately invoked,
single-use supervised replay. It imports the existing STMN2 counter unchanged;
the target seal is also unchanged. A regression compares all six command
argument sequences with the historical implementation, substituting paths only.
Per-library processing is not stopped by a low or zero canonical count.

## Validation

[Focused controls](focused-tests.json): **21 executed, 21 passed, zero skips** on
Python 3.12.14 with PySAM 0.23.3. Controls cover malformed/duplicate/missing
inputs, same-size raw corruption, index corruption, changed plan bindings,
single-use claims, version/WSL refusals, exact command equivalence, altered
counts/QC, completion/units/flags, process resource-cap failure metadata and
all-six software orchestration. One test actually launches tiny stand-in tools
and streams synthetic SAM through PySAM and the original counter; its output is
a software fixture, not biological evidence. Other orchestration controls use
mocks and are labelled accordingly in the test source.

The first full-suite run used a 4.9 GiB `/tmp` tmpfs (about 4.5 GiB available).
Pre-existing pilot tests enforce larger disk reserves: **1375 executed, 1339
passed, 3 failures and 33 errors, zero skips**. The [failed run record](initial-suite-environment-failure.json)
is retained. No historical guard, script or test was relaxed. The same suite was
rerun with `TMPDIR` on the workspace filesystem, which had about 59 GiB free;
**1375 executed and passed, zero failures/errors/skips**. The final record is [full-suite.json](full-suite.json).

Compilation and `git diff --check` pass. [Artifact hashes](artifact-hashes.json)
identify the new script, manifest/template/test and the unchanged original
counter/target seal. Installation of the existing pinned CI dependencies was
confined to a scratch virtual environment; the replay command installs nothing.

## Interpretation

The deliverable removes historical execution-chain prerequisites from a future
technical replay and makes count/QC discrepancy detectable. It does not yet
establish that real FASTQs reproduce on another machine. No new independent
library, donor, culture, functional measurement or therapeutic inference is added.

## Limitations

- **Actual clean-environment FASTQ replay remains pending.** No real-input
  prepare descriptor, installed-tool/index rehash or supervision result exists
  for the new portable entry point. Existing archived results are the reference.
- Execution currently requires **native Linux**. It refuses WSL rather than
  infer physical Windows free space from guest capacity. It is not advertised
  as immediately runnable on Luis's WSL host.
- Different builds of the required tool versions are permitted but their
  digests and historical-build mismatch are explicit. Version agreement alone
  is not binary identity or proof of output equivalence.
- Local execution receipts are unsigned, not independent host attestation.
  RSS/disk are sampled, not aggregate kernel quotas; external use and
  uninterruptible I/O can defeat timely resource termination. The command has
  no transfer implementation but does not enforce OS network isolation or
  independently measure network bytes.
- Biological independence and protein efficacy remain unresolved. The original
  measurement cycles stay closed; #83 stays paused.

## Next discriminating check

Only if a suitable native-Linux environment, all fixed local inputs and resources
are selected, prepare/inspect the descriptor and then run the single-use replay.
Compare all six count/QC records and supervision without changing expected values
on disagreement. No download, real replay, cloud spend, contact or merge is
scheduled by this preparation.
