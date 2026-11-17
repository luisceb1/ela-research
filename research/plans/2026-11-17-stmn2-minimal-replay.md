# Minimal STMN2 technical replay — 17 November 2026

Luis authorized preparation of a portable six-library reproduction entry point and
an updated README. This is research software work, not a new biological analysis.

## Question and decision

Can a clean Linux checkout, without historical host paths, consumed descriptors or
failed-run directories, reproduce the archived GSE252892 STMN2 measurement?
Exact count and QC agreement would support technical transferability only.
Disagreement identifies a reproducibility defect to investigate; incomplete inputs
or failed processing are inconclusive. No outcome permits a donor-level or
functional-rescue claim, and no threshold/target/filter will be tuned to match.

## Fixed scope

Use GSM8009878–GSM8009883, in accession order. The first three are declared
controls; the last three are declared KD. Preserve all six, including controls
with cryptic counts 3, 5 and 0. Expected canonical/cryptic counts are respectively
1945/3, 2806/5, 2438/0, 253/727, 173/551 and 140/556, from the two original
deposited STMN2 result cycles. These are known comparison targets, not holdouts.

Bind the twelve compressed FASTQs by published length/MD5 and archived SHA256;
bind the eight original hg38 index shards by length/SHA256. Keep the existing
STMN2 target seal and counter byte-for-byte. Require fastp 0.23.4, native
hisat2-align-s 2.2.3 and PySAM 0.23.3; record binary digests and distinguish a
different build from the historical build. Keep preprocessing/alignment options
identical except paths. No new downloads or external package installation by the
replay command. Existing local file paths are supplied explicitly, not searched.

## Preparation and acceptance

Provide a human-readable source manifest, local path-map template, offline
comparison CLI and a single sequential replay entry point. Preparation hashes
inputs/index/tools and emits a separate immutable plan; it does not align data.
Replay accepts its exact SHA, revalidates bindings in a clean checkout, uses a
fresh output directory and retains failures. It streams SAM through the original
counter and writes all six count/QC records before comparison; no result-driven
early stop. Compare exact counts and the original five QC totals, sample/gene/
project identity, completeness and count units. Fail on missing/duplicate/extra
libraries, changed counts/QC or invalid records. A JSON comparison alone cannot
prove FASTQ execution, so label it separately from supervised replay provenance.

## Resources and stop rules

Preparation only in this session; no real FASTQ replay has been started or
scheduled. For a later replay: zero raw transfer, sequential six libraries,
96 hours wall, two CPU affinity slots, 8 GiB per-process address-space limit,
6 GiB sampled group RSS, 100 GiB sampled new output, and 50 GiB filesystem free
reserve. Require 150 GiB free at prepare/run admission. Monitor every 0.5 seconds;
sampled limits are not kernel aggregate quotas. On WSL, guest free space does
not certify physical host space; require native Linux for this portable entry
point. Historical WSL executors remain unchanged. Never delete source data or
old roots; delete only this replay's successful-library trimmed intermediates.
No automatic retry/resume, model sweep or further dataset on failure.

## Validation and completion

Test malformed/missing/duplicate inputs, provenance/hash refusals, fixed-command
equivalence, exact archived six-library comparison and deliberately perturbed
results. Test orchestration with software fixtures explicitly labelled as such.
Run the repository offline suite and report omissions. Deliver a reviewable PR,
guide, machine-readable comparison and an honest pending real-replay status.
No #83 execution, contact, cloud spend or new scientific finding is authorized.
