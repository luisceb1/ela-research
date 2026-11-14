# Orthogonal STMN2 splice-response control — 14 November 2026

## Outcome of this preparation cycle

**One candidate selected and a zero-network local executor implemented/tested; no new biological counts yet.** The source selection plan was committed at `15ebbbdf51103434c903de0e2b296762ef8a8b81` before primary review; the [execution specification](../../research/plans/2026-11-14-gse252892-stmn2-execution.md) and [source decision](SELECTION.md) were committed at `b26969174bce9d0aad2cff562935135ba354972d` before implementation/counts. Base main `ebebf945c3d00662748c2047a12dcc65b4f5e0d8`. Prior UNC13A outcome and prior donor/STMN2 cycles remain closed.

This follows Luis's authorization to assess an orthogonal molecular control in the two existing GSE252892 libraries. It is a new response-control question, not a new source/cohort, restoration test or independent biological replication. Reading an existing study again for a different endpoint is explicitly recorded as reuse, not a new discovery.

## Source/assay decision

See [selection evidence](SELECTION.md). STMN2 exon1-to-cryptic-terminal-exon is biologically supported as a TDP-43-loss response, with existing audited hg38 coordinates. This admits descriptive splice-junction measurement in the selected total-RNA libraries in principle. It does not calibrate sensitivity, verify per-library nuclear protein depletion or predict quantitative support. The study-specific standard-RNA/3'-end distinction is retained: polyadenylation visibility and exact splice-junction sensitivity are different endpoints. Failure or low support cannot establish that KD failed. A supported KD junction is only compatible with the known downstream response; control observations are reported without an inferential comparison.

Four primary/search-service calls, two works reviewed, no further marker or sequencing retrieval. The failed reference click returned a recaptcha page. Original target seal retained byte-for-byte; old target/annotation/ratio limitations are not silently removed. No sensitivity/alternative-marker/threshold search after counts.

## Implemented local workflow

[Runner](../../scripts/run_gse252892_stmn2_control.py) has separate prepare/execute actions with exact proposal acceptance, a new root and consumed claim. It binds the completed source proposal (`61c5f2c7…`), original archived result/supervision/ledger bytes and recorded input identities from the verified archive. All four original FASTQs are locally rehashed against published length/MD5 and recorded SHA256; tool binaries and the original index are rechecked. Pinned clean code and the STMN2 target seal are mandatory. No raw copying, deletion or HTTP/download code path is added.

Exact old fastp/HISAT2 option sequences are reused, replacing raw source/output paths only. New [counter](../../scripts/stmn2_paired_control_counts.py) changes only the old chromosome/XS strand to chr8/plus and the two-cryptic label list to a single cryptic event; mate/filter/CIGAR/query-group rules are source-equivalent. No ratio, PSI, p-value, effect or polyA-site count. Genome-wide alignment streams directly into counting; no target list is fed to the aligner and no SAM/BAM file is written. Canonical/cryptic support is reported for both libraries regardless of the first STMN2 count because no new acquisition is involved.

Prepare performs local hash checks, records the current six-root disk baseline and inventories old plain trimmed files without deleting them. It refuses an already full combined allowance. The new run is the seventh root; 48 h, two CPU affinity, per-process AS 8 GiB, sampled group RSS 6 GiB, all-seven-root 100 GiB and actual C: reserve 50 GiB are fixed. Reuse the previously tested drvfs/sampler/process-group controls; they remain sampled checks, not kernel quotas, and uninterruptible-I/O limits persist. New transfer is explicitly zero, accepted as zero in the descriptor; this is an implementation policy, not a network sandbox. Historical transfer charges are preserved in source metadata, not relabelled as zero.

Plain trimmed outputs are temporary new-run files and removed only after that library's successful count. Original compressed inputs, all old roots and metadata remain read-only. Failure is retained; no automatic restart/replacement. Rerun after a technical failure requires separate accounting/descriptor handling. No user-host executor run is claimed here.

## Verification

[Focused checks](focused-tests.json): **42 executed/passed, no skips**, including 20 new event/source/command/claim/zero-network-path controls and 22 prior lineage/drive/sampler controls. Fixtures test chr8/plus specificity, exact intron and 15-vs-14 anchors, union of mates once, ambiguity/reciprocity rejection, exact old filter source equivalence, digest/proposal/metadata failures, fixed options, direct-worker refusal and consumed-claim rejection. All sequencing-looking bytes in tests are software fixtures, not evidence. Compilation, diff and report-link checks pass. Full CI is checked on the actual final head separately.

## Host execution and stop

Fetch the reviewed PR commit in the existing `/home/luisceb/proyectos/ela-local-20261112` worktree. Use the original Python/PySAM environment; prepare with source `/home/luisceb/ela-gse252892-interrupt-execution-20261113.json`, a new `/home/luisceb/ela-gse252892-stmn2-control-01` root and `/home/luisceb/ela-gse252892-stmn2-control-20261114.json` proposal. Preparation can take minutes to rehash the existing 12.83 GB of raw files and index. It does not download them.

Only a successful new proposal SHA can be executed with `--accept-network-bytes 0`. Standing authorization already covers local CPU use; no additional permission loop. Preserve the printed proposal summary, cleanup inventory, actual result and supervision. No cleanup is included. Stop at fatal validation/process/resource failure, exhausted window or both completed libraries. Interpret no outcome until actual host counts/QC are supplied; do not automatically substitute another marker.
