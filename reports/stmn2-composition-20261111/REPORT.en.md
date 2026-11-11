# ST7 links to all 45 pairs; a common tissue adjustment is not yet justified

> English translation prepared on 11 November 2026 from the [Spanish original](REPORT.md) at `c7d8f7e92e7eb02e3fb619f6e8984f075ef84784`. Source/translation hashes and review scope: [English guide](../../docs/ENGLISH_GUIDE.md#translation-policy-and-review). This is a dated report, not a new analysis or publication-status check.
> Earlier proposed next steps are historical; for completed STMN2 work and current stop rules, use the [closing report](../stmn2-within-region-20261111/REPORT.en.md) and [current findings](../../docs/CURRENT_FINDINGS.md).

11 November 2026. Technical and comparability review, without a new biological contrast. [Scope fixed](../../research/plans/2026-11-11-stmn2-composition-gate.md) before reading ST7. Previous STMN2 and RIN results were already known.

## Evidence

Only the expression-tables workbook from [Zenodo 20090702](https://zenodo.org/records/20090702) was downloaded: 32,702,280 bytes, MD5 `d49eca47d62502c5b89627c96dae4d75`, matching the manifest; SHA-256 `6b24edc4279eebb0d8560ef277573745fa0110e1e8d1a07009621d020cd2abfc`. No RNA matrices, FASTQ or BAM were downloaded. The workbook remains temporary; the repository contains only schema, aggregates and hashes.

ST7 contains **16,985 estimate rows**, with columns `Sample`, `cell type`, `estimate`, `tissue`. There are **1,724 valid sample/reference vectors**: no duplicated cell-type keys within a vector, finite numerical values between 0 and 1, sum one within tolerance 10⁻⁶, and all categories observed in the reference. Cell-type rows are not confused with biological replicates.

| Check on the frozen analysis | Cortex | Cervical |
|---|---:|---:|
| Libraries from the 45 original pairs | 45 | 45 |
| Exact Sample key with one valid vector | 45 | 45 |
| Compatible reference label | Cortex: 45 | Spinal Cord: 45 |
| Categories per vector | 8 | 11 |

Thus **45/45 pairs have both estimates**; there is no sample loss from ST7 linkage. The donor/region/preparation map is the previously validated one; the new link is by exact library, without inferring individuals from prefixes. A donor's cortical and cervical vectors are not independent donor replicates.

## Method and comparability

The [NYGC source study](https://www.medrxiv.org/content/10.64898/2026.04.29.26350889v1.full), *Cell-type deconvolution*, describes **MuSiC 1.0.0** with controls as references: GSE140231 for cortex, GSE190442 for spinal cord and GSE246183 for cerebellum. These are estimates derived from bulk expression, not histological counts. The authors' code, `jackhump/NYGC_ALS_Flagship`, tree `bed82ad63b0d959237f9368561e1145230463ecb`, separates proportion files by reference in `scripts/Deconvolution_scatters.Rmd`; effects/statistics are in another script. The method mentions residual-based adjustments for comparing composition between groups. ST7 does not label a transformation per row, so the exact status as raw versus transformed estimates is not established by the column name alone; the vectors pass proportion checks.

Categories differ:

- Cortex: Astrocytes, Endothelial, Excitatory, Inhibitory, Microglia, Oligodendrocytes, Opc and Pericytes.
- Spinal cord: Astrocytes, Endothelial, Ependymal.Cells, Lymphocytes, Meninges, Microglia, Neurons, OPC, Oligodendrocytes, Pericytes and Schwann.

The cortical Excitatory+Inhibitory sum is a plausible neuronal aggregation within that reference, but **does not itself verify calibration against Neurons in the spinal reference**. Different reference genes, included populations and efficiencies can change an estimated proportion's scale. Sharing an algorithm and summing to one are necessary file checks, not proof that the two estimates are interchangeable or unbiased physical cell percentages.

## Decision

**Technical linkage accepted for all 45 pairs. A single cortex−cord effect adjustment treating cell fractions as a common scale is not enabled by the reviewed evidence.** No new “composition-corrected” effect was calculated, neuronal percentages from different references were not subtracted, and the STMN2 ratio was not divided by a neuronal fraction. This does not claim these estimates cannot be analyzed or that different references invalidate every model; the limitation concerns interpreting a common tissue correction that has not yet been validated.

The original result remains an exploratory tissue association, with a positive primary RIN sensitivity in 19 pairs and a strict nine-pair subset with median zero. Composition linkage does not supply external replication or remove those limits. Quality, depth, composition and pathology variation can coexist; causality is not assigned to one route.

## Next concrete experiment

There are two different questions and a bounded route for each:

1. **Measurement compatibility for adjusting the tissue comparison:** obtain ST7's exact provenance (raw table or transformation) and an estimate of broad cell classes with a harmonized reference or calibration of both references. If deconvolution is recomputed, use the same libraries and fix markers, classes and controls first; this would require expression data and was not started in this cycle.
2. **Feasible analysis without assuming a common scale between tissues:** separately within cortex and cervical cord, examine the relationship between the STMN2 measure and the neuronal estimate from its reference. This requires a single protocol before calculating associations, with coverage/RIN control and without presenting two correlations as correction of the tissue effect. It can probe an alternative explanation within each region but cannot demonstrate independence from composition across regions.

The least costly technical priority is the second route, using already linked data. It is not executed here because the fixed scope was acceptance of the covariate, not a new search for associations. No cohort expansion is needed to formulate it. UNC13A #37 and K26 #44 remain unchanged.

## Verification and reproduction

`python scripts/stmn2_composition_gate.py --source-root /ruta/temporal/stmn2-audit-work --output /ruta/temporal/gate.json` reproduces the aggregate; the temporary workbook is at `source-gate/nygc-expression-tables.xlsx`, and sources/counts retain the previously used structure. The script verifies the hash and locates ST7 through workbook relationships, without relying on worksheet number. `gate.json` contains no sample or donor keys.

Five new tests cover valid vectors with zeros, duplicate keys, nonfinite/out-of-range values, incorrect sum, incomplete categories and separation of taxonomies. Per-library coverage was checked on real data. No new models or biological tests were created; PR CI verifies the complete offline suite and compilation.
