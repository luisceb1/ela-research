# ELK1 RNA-FISH: bounded molecular replay — 2026-11-04

## Result

**Final-paper reconciliation completed:** the linked Zenodo archive confirms identical inputs and all 240 long-table rows/84 aggregate numeric fields. The two older replicate-1 ratio discrepancies persist. Fig.3g-style extranuclear counts are reconstructed separately; see [final comparison](FINAL_ARTICLE_COMPARISON.md). This does not certify editorial point identity.

We processed the 60 deposited image-count rows into 12 replicate/condition/probe summaries. There are three source replicate labels, two arms and ten images per arm/replicate. Images are nested observations, not 60 biological replicates. The authors describe biological replicates; the table does not identify donors, differentiation batches, cultures or coverslips, so their independence cannot be independently verified from this file.

Seven of nine deposited ratio values match an equal-image calculation within 1e-8. Two count ratios for replicate 1 do not match. No values or identities were changed to make them agree. This is an executed computational reproduction with unresolved discrepancies, not an independent experimental validation, rescue experiment or new biological discovery.

## A. Literature and version attribution

Bryce-Smith et al., preprint v1, 23 January 2024, *TDP-43 loss induces extensive cryptic polyadenylation in ALS/FTD*, DOI [10.1101/2024.01.22.576625](https://doi.org/10.1101/2024.01.22.576625), Fig.3F–H. Final article: *TDP-43 loss induces cryptic polyadenylation in ALS/FTD*, Nature Neuroscience 28:2190–2200, 21 October 2025, DOI [10.1038/s41593-025-02050-w](https://doi.org/10.1038/s41593-025-02050-w), [full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC12586162/).

The experiment uses cortical-like i3Neurons, control versus TDP-43 depletion, fixed on day 9. Proximal/shared and distal/extension-specific probes detect ELK1 RNA; the proximal probe is not exclusive to the canonical isoform. Methods describe ten images per arm per biological replicate, image-level normalization to nuclei, and log-ratio t-tests with BH correction. The final Fig.3g instead presents extranuclear foci; final Fig.3h is a separate SH-SY5Y fractionation experiment, not the preprint localization ratio. The final article states that FISH analysis was blinded and no data were excluded.

The public GitHub snapshot is preprint-era. We do not certify identity to the final editorial source workbook or reproduce its reported P values. We do not transfer the distinct Halo-PROTAC protein experiment's timing to this FISH assay; exact knockdown schedule and culture lineage per replicate remain unresolved here.

## B. Executed project results

Immutable source: `frattalab/tdp43-apa` commit `e0d54b6f60a094c79f05f57ab4c88e451127bcbb`. The plan was committed before numerical analysis; see `sources.json`. Counts, two ratio tables and relevant R scripts were inspected. Exact source bytes are verified by SHA256 and Git blob; originals are linked rather than republished.

| Source replicate | Total/shared probe: computed KD/CTRL | Deposited | Extension probe: computed KD/CTRL | Deposited |
|---|---:|---:|---:|---:|
| 1 | 2.178250 | 2.352952 | 5.294080 | 5.389317 |
| 2 | 3.249458 | 3.249458 | 8.943165 | 8.943165 |
| 3 | 2.328862 | 2.328862 | 7.385818 | 7.385818 |

These are ratios of equally weighted image-level foci/nucleus means, using all ten images. All three deposited proximal nuclear:extranuclear ratio changes match (0.389665, 0.734701, 0.395139). `deposited-comparison.csv` retains full precision. Color/probe and replicate mapping follows source code and numeric labels, not invented culture identities.

Three discrepancies in conventions must remain separate:

1. **Repeated nucleus denominator.** `fish_process_counts.R` pivots each image into nuclear and extranuclear rows per probe, then sums `n_nuclei` across both. Its `mean_cell` is total foci/(2×total nuclei). Once-per-image normalization gives exactly twice that absolute value. The factor cancels in KD/CTRL fold changes; it cannot explain the two deposited mismatches.
2. **Unequal weighting.** That R script pools foci and nuclei, whereas written methods average image-level ratios. Pooled KD/CTRL folds are 2.049315/3.236662/2.357078 (shared) and 5.411308/8.770349/7.368320 (extension). Both estimands are retained. They answer different questions; neither is chosen because it favors a conclusion. The two unmatched deposited values remain unmatched to the corresponding pooled and equal-image calculations.
3. **Localization and statistics.** `fish_plot.R` uses pooled extranuclear:nuclear ratios; the tiny deposited table and methods use averaged nuclear:extranuclear ratios. Averaging and division do not commute. Distal-probe localization is undefined for some image-level controls because extranuclear counts are zero; no pseudocount or selective omission is used. `fish_stats.R` contains both raw-scale Bonferroni and log-scale BH tests, while the plotting script selects a particular three-test family. No new P values are estimated without adjudicating versions and independent units.

All three source replicates show increased total/shared and extension-probe foci per nucleus under both aggregation choices. Equal-image mean folds are 2.585523 and 7.207688. Leaving out one replicate gives mean ranges 2.253556–2.789160 and 6.339949–8.164491. These are descriptive fragility checks, not confidence intervals or extra replicates. Foci counts are not calibrated molecule counts or single-cell distributions, and density/segmentation differences could affect these summaries.

## Reproducibility and quality

Python standard library, exact rational aggregation; no package installation. `scripts/reproduce_elk1_fish.py` validates source hashes, count syntax, image identity, zero denominators and the pinned grid; parses the same verified bytes used for hashes; exports summaries, folds, comparisons, sensitivity and a run receipt. Six artificial transformation controls test the denominator, weighting, missing arms, zero compartment counts, identity and row-order invariance. They are not simulated neuronal evidence.

```bash
python scripts/reproduce_elk1_fish.py --source-dir /path/original-files --output /path/replay
python -m unittest discover -s tests -p 'test_elk1_fish.py' -v
```

Fetch only the three data files from the immutable URLs in `sources.json`. Inspection of original R was static; no R execution or image re-segmentation is claimed. The source lock records R4.3.2, dplyr1.1.4, tidyr1.3.0 and readr2.1.4; our executed Python version is in `run.json`. Validation/hashes and exact differences are preserved. The initial attempt to move a nonexistent new branch ref returned HTTP422; creating the branch explicitly succeeded. No data were altered in response.

## C. Interpretation, originality and stopping rule

This adds a reproducible image-to-replicate molecular analysis and an auditable metadata/code discrepancy report. It is distinct from TPM/PPAU and the UNC13A Dox replay, but it does not establish new ELK1 biology, causal toxicity or a therapeutic strategy. Increased ELK1 RNA after TDP-43 loss does not demonstrate that correcting UNC13A requires correcting ELK1, or that lowering ELK1 would help patients.

Conclude this bounded replay without opening a new ELK1 intervention program. A future reconciliation would require the final figure's numeric source and the source-to-summary processing history, including explanation of the two replicate-1 values and biological lineage. No new contacts are made. Functional K26 Fig.4d (#44) and Seddighi/AD Workbench (#37) remain separate and blocked on their specified data; no endpoint is substituted into those protocols.
