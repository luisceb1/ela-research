# Bounded interpretation review — 12 November 2026

Base: `f6e66099103986507b9ad52c34fc5fc39c478fe3`. Luis authorized this review after the merged recount3 cycles. Scope: inspect deposited outputs and their interpretation; no new source search, sequencing transfer, count extraction, effect, model or inference. This is an AI-assisted consistency review, not independent biological validation or a raw-input reproduction.

## Evidence and corrections

| Item | Deposited evidence | Correction |
|---|---|---|
| GTEx window rationale | [TARGET_ALS cortical table](../target-als-cortex-20261111/REPORT.md): canonical **median** 102 in 84 ALS libraries and 148 in 13 non-neurological controls | 102–148 is a fixed window between two group medians, not the observed per-library range. Keep the executed window, counts and original plan; correct its description, including the JSON metadata field. |
| GTEx result | [Summary](../gtex-brain-negative-control-20261112/summary_BRAIN.json): 26 libraries in the window, including 15 cortical; zero cryptic counts in that subset | This descriptive zero does not establish an ALS-versus-background difference. Individual ALS positive libraries were not matched here; studies and preparations differ. Outside-window libraries include those above the upper bound and cannot all be classified as insufficiently covered. No donor-level rate bound is established from 15 libraries. |
| SRP069787 | [Recorded output](../questionA-detection-SRP069787-20261112/results_SRP069787.json): KD canonical counts 9 and 2; cryptic counts zero throughout 16 libraries | Canonical support is a warning, not a mathematical ceiling on alternative cryptic junction counts. Withdraw impossibility and sole-cause claims; observed cryptic support fails the fixed gate. Replicate count, depletion, assay, mapping and biology remain separate considerations. |
| SRP097615 | [Recorded output](../nonals-spinal-source-20261112/results_SRP097615.json): canonical absent in all 39 libraries; 121,078 catalogue junction rows | Control failure limits conclusions at this locus. Distinct catalogue rows across different sample counts/assays do not establish per-library complexity or a causal cost of laser capture. Preserve the spinal/oculomotor/Onuf distinction. Do not generalize to all public spinal RNA-seq. |
| Current status | A availability, selection and detection cycles are already integrated | Remove stale “A not started / scope decision pending” language from current summaries and backlog. The old A protocol branch is superseded; no duplicate execution or merge is proposed. |
| AD Workbench | Luis supplied the support reply “New Workspace Request received”; request received and under review | User-reported correspondence only. Approval, active workspace and dataset access remain unconfirmed; no timestamp, independent mailbox check or new Fratta/Wong response inferred. |

The original prospective plans remain byte-for-byte intact as historical records, including the inaccurate window rationale and outcome interpretation. Prespecification records a decision; it does not validate its premise. These corrections supersede those interpretations without adjusting endpoints or rerunning a more favourable selection. Source reports, STATE and CURRENT_FINDINGS carry the corrected conclusions; BACKLOG carries actual completed scope and conditional next steps. No translated source report is changed by this review.

## Validation and limits

Run from the repository root:

```sh
python reports/nov12-interpretation-review-20261112/verify_committed_outputs.py
```

[Recorded validation](VALIDATION.json) checks the cited GTEx totals and subset, both project result files, source group medians, and unchanged numerical GTEx fields. It verifies that the two project outputs, all existing 12 November prospective plans, sealed targets and junction probe are unchanged from the base. SHA256 values identify the inspected derived files. The original multi-gigabyte inputs were not reacquired or reprocessed; input hashes recorded in those outputs are not freshly verified by this review.

This is deliberately limited to claims supporting today's conclusions. It does not certify every historical report, resolve biological nesting, establish disease-specificity, validate a causal mechanism, or establish functional/clinical recovery. Negative counts, failed predictions, support threshold and closed #37/#44/STMN2 cycles are retained.

## Next discriminating input and stop

Close this review after the stated checks and propagation. No further recount3 candidate or cohort is scheduled. A verified active workspace plus actual dataset/file inventory, or substantive author clarification, can justify a separate prospective task. Receipt of the workspace request alone cannot. No duplicate workspace request, reminder, branch deletion, merge or new contact is performed.
