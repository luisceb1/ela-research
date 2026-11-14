Current status: the original user metadata ZIP has now been received and verified; see [executed audit](../gse252892-audit-verification-20261114/REPORT.md). Earlier pending-archive statements below describe the prior stage. No raw-data replay was performed.

# GSE252892 complete local measurement — 14 November 2026

## Evidence and provenance

Luis supplied completed run06 [result JSON](user-reported-result.json), [supervision](user-reported-supervision.json) and both [HISAT2 summaries](alignment-summary.tsv) as terminal text. These JSON artifacts are transcriptions of that supplied text, not original host-file bytes or an independent raw-data replay. The agent did not process the FASTQs. Host proposal SHA256 is `61c5f2c73e762ed23d9c940ce7db2b3043713169311e4594d8f87e51d0332369`; runtime commit `49afddbe0071f5552860cb474a1544e027646ea5`. Original host plan/receipt bytes and final transfer ledger remain to be packaged for archival verification. Current main was checked at `bff46c6488abe3358df730139276e657b0d443db` before this documentation update.

Question/method fixed in the [original specification](../../research/plans/2026-11-12-gse252892-bounded-execution.md); subsequent amendments only addressed transport/supervision/interruption and retained original scientific function source. Public GSE252892 / SRP482832, fixed control GSM8009878/SRR27477544 and KD GSM8009881/SRR27477541. One nominal library per condition, one WA01/H1 genetic background; not matched cultures, donor replication or a new functional experiment. Source selection came from the earlier inventory; it is not newly discovered literature.

## Exact descriptive result

| Library | Condition | Canonical | Cryptic left | Cryptic right |
|---|---|---:|---:|---:|
| GSM8009878 | Control | 106 | 0 | 0 |
| GSM8009881 | TDP-43 KD | 41 | 0 | 3 |

[Exportable counts](counts.tsv). Unit: one eligible contiguous paired query-name group per sealed event/library, union of mates, adjacent aligned anchors >=15, fixed unique/proper/primary/MAPQ/NH/strand filters. This is not molecular/UMI deduplication or recount3 read support. Do not sum the two cryptic counts or treat them as a completed isoform measurement.

Canonical >0 in the control passed the operational gate, permitting KD acquisition; KD canonical is also positive. Neither cryptic event in either library reaches the historical **20-group support diagnostic**. This was explicitly a diagnostic, **not an inference gate or a newly fitted acceptance threshold**. The two-example design never authorized an effect/ratio/PSI/interval/p-value. Three right-junction groups are detected in KD; this preserves a low-support observation, not a robust quantitative or causal result. Left zero in KD and both control zeros are observed non-detections, not evidence of biological absence. Lower canonical support in KD is not proof of UNC13A repression, a count ceiling, equivalent sampling or an explanation of cryptic support.

## Technical checks and resources

Control: 70,948,578 pairs, unique concordant 61,077,456, multiple concordant 4,401,096, global alignment 92.29%. KD: 89,969,380 pairs, unique 76,494,020, multiple 5,913,263, global alignment 91.59%. Global mapping does not establish junction-level sensitivity, adequate depletion, or biological equivalence. Supplied eligible/rejected group counts match these unique/multiple summaries; [consistency checks](consistency-check.json) pass. No new effect analysis or model was run.

Final supervision completed with failure/cleanup_error null, elapsed 16,577.237 s (~4 h 36 min), peak group RSS 4,850,765,824 bytes, peak combined disk 101,471,660,394 bytes; below declared sampled limits (6 GiB/100 GiB), within 48 h. Sampling/uninterruptible-I/O limitations remain. Last displayed lineage transfer upper bound was 13,007,068,985 / 14,000,000,000 bytes; the final ledger itself is not yet supplied, so this is a screenshot value rather than independently verified final accounting. Retain all failed-attempt receipts and conservative reservations.

## Interpretation and closure

**Technical execution succeeded; cryptic support remains below the fixed descriptive diagnostic in these two libraries.** This does not establish general absence, lack of TDP-43 biology, failure of all GSE252892 samples, a depth-only cause, or invalidity of the targets. Depletion efficacy/library linkage, assay/preparation, alignment/reference/anchor filters and biology remain possible contributors. No alternative estimator, target, alignment rule, threshold or library is selected after seeing the counts.

This is an additional experiment/deposit relative to prior donor/cohort work under the recorded inventory, not donor-level validation; another accession alone does not prove every independence claim. Results do not generalize across backgrounds and cannot be pooled with tissue/recount3 or interpreted as recovery/clinical benefit. #37/#44 and prior STMN2 cycles remain closed.

Close this bounded two-library measurement with its exact low-support outcome. Next authorized task is preserving a small provenance package (actual plan, final ledger, verified-input receipts, counts and QC logs) for audit, not more sequencing/parameter searches. Further libraries or a new assay question need a separate prospective decision; this result does not justify automatically expanding the cycle. No contact, cloud spend or merge.
