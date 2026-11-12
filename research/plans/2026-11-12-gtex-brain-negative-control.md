# Non-ALS background for the UNC13A cryptic junctions — gtex BRAIN

Date: 12 November 2026. Base: merged main `06c5b94fa27d6774329ba1edfdadb7a4b1cb772b`.
**Committed before any junction file is downloaded.** Only the file sizes and the collection index were checked beforehand, and those checks are recorded below.

## Question

This project has published cryptic UNC13A read counts in ALS post-mortem tissue — [motor cortex](../../reports/target-als-cortex-20261111/REPORT.md) reports canonical coverage 102–148 and **1–4 reads per positive sample**, per-junction cryptic ratio maximum 0.0414 — without ever measuring what that locus produces in brain **without** TDP-43 pathology at comparable local coverage.

**Question: in non-ALS brain, at comparable canonical UNC13A coverage, do the sealed cryptic junctions carry reads at all?**

This is a control for a number already in the repository. It is **not** a new source for issue #37 and does not address the depletion question.

## The weakness of this design, stated before execution

GTEx and TARGET_ALS are **different studies**, with different donors, tissue handling, library preparation and sequencing. By this project's own established standard — correction #1 in the cortex report, which demoted a 1.8× cross-study claim to "weak evidence" — a comparison between them is weak whatever it shows. A clean zero in GTEx would be **consistent with** the ALS counts being real signal; it would not demonstrate it, because processing differences alone can suppress or create low-count junction detection.

Recording this now means the conclusion cannot be upgraded later on the strength of a favourable result.

## Depth comparability, fixed in advance

**Comparability is judged on the canonical UNC13A junction itself, not on library-wide depth.** Library depth fields caused three successive published corrections in this project (`exon_fc_count_all.total` repeatedly misdescribed as reads assigned to exons, and ratio-of-medians confused with median-of-ratios). The canonical junction is the direct local measure at the locus in question and needs no such field.

A GTEx library counts as **depth-comparable to the published cortex measurement** if its canonical count falls within **102–148**, the observed TARGET_ALS cortex range. The full canonical distribution is reported regardless of how many libraries qualify.

Cryptic burden is reported with the **per-junction** estimator only — each sealed cryptic junction separately — never the summed `(cL+cR)/(cL+cR+canonical)` form, which correction #2 in the cortex report established inflates roughly twofold at low values.

Libraries are stratified by the deposit's own tissue label, keeping cortical regions and cervical spinal cord separate, because the project's two published measurements are those tissues. Labels are taken from GTEx metadata, never inferred from ordering.

## Prespecified outcome table

Fixed before any count is seen. Each outcome maps to one conclusion and no other.

| Observation | Conclusion |
|---|---|
| No GTEx cortical library reaches canonical 102–148 | **Not depth-comparable. Inconclusive**; report the distributions and stop. No background claim in either direction |
| Among depth-comparable cortical libraries, both cryptic junctions are **0** throughout | The published ALS cortical cryptic reads are **above the non-ALS background at comparable local coverage**. Weak between-study evidence, consistent with real signal, not a demonstration of it. No causality, mechanism or clinical meaning |
| Cryptic reads present at a rate **similar** to the ALS cortex measurement | The published 1–4 reads are **not distinguishable from background**, and the TARGET_ALS cortex report's central observation requires correction. This outcome is to be reported as prominently as the favourable one |
| Cryptic reads present but clearly rarer | Report both distributions descriptively. **No threshold separating them may be declared after seeing the numbers** |

## Forbidden in this cycle

No p-value, no inferential ALS-versus-GTEx test, no effect size, no interval, no model, no PSI beyond the per-junction descriptive ratio already defined, no pooling of GTEx with TARGET_ALS libraries, no substitution of a different junction, and no post-hoc change to the 102–148 comparability window.

## Execution parameters

- Collection `gtex`, project `BRAIN`: 2,931 samples. Checked before this plan: `MM.gz` is **2,819,422,875 bytes** and `RR.gz` is **112,590,478 bytes**; 30 GB of writable disk were free. Cap for this cycle **3.5 GB**; stop and report if exceeded.
- Files: `RR`, `MM`, `ID`, the `recount_project` index and the GTEx sample metadata, so tissue labels come from the deposit.
- Sealed targets `research/references/unc13a_targets_sealed.json` used unchanged, hash `e35f6e05…bc3a` verified first; stop on mismatch. The probe is invoked with `--project-id BRAIN` per the PR #66 fix, and its coordinate-convention guard must pass.
- Record SHA256 and byte size of every file. Report per-junction maxima, libraries with any read, libraries at or above 20, the canonical distribution overall and per tissue label, `assay_shape`, and the per-junction cryptic ratios.

## Boundaries

A descriptive background measurement in non-diseased tissue. Not biological replication, not validation of any ALS result, not evidence about TDP-43 depletion, functional recovery, therapeutic rescue or clinical benefit. Issue #37, the 20-read minimum and the three-background question are untouched. No contact, access request, cost or personal data.
