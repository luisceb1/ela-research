# PFKP context-specific evidence audit — cycle closure

**27 November 2026.** Independent ALS research project directed by Luis Cebrián Fraile. Public-source documentary audit, target-blind source admission and one exploratory historical-matrix calculation. Not peer reviewed; no independent biological or clinical validation. This report supersedes neither the original study results nor the 26 November five-study proteomics audit.

## Question and decision

Does PFKP exhibit a reproducible selective reduction in human spinal motor neurons, and is an RNA–protein discrepancy measurable within a common experimental context? The results do **not** establish a uniform direction, a selective decline, an obligatory RNA–protein discrepancy, or the mechanism of Guise's large protein estimate. The current cycle is closed; further work requires a genuinely discriminating, admissible input. No additional runs, contact or spending are scheduled.

## Evidence table

Percentages are source-specific relative contrasts or explicitly labelled arithmetic estimates, not interchangeable effects.

| Source | Endpoint / cohort | PFKP result | Evidence limit |
|---|---|---|---|
| Manzo 2019, [eLife](https://doi.org/10.7554/eLife.45114) | Human bulk spinal cord RNA; iPSC-derived motor-neuron RNA | +80% (9 ALS, 8 controls; source p<0.001); +58% (3 differentiations; source p=0.010) | Published qPCR; differentiations not distinct donors; no source replay |
| GSE330130, [Barretto preprint](https://doi.org/10.64898/2026.07.24.740361) | Target-blind lumbar nucleus coverage | 91 ALS / 347 control motor-neuron nuclei among 121,881 total; 95.1% of control MN nuclei from one donor; only 4 ALS / 1 control donors pass ≥10 nuclei in both neuronal classes plus summed author n_counts ≥10,000 in both | 11 ALS / 9 control donors in total; primary interaction not admitted; no PFKP extraction; not biological cell loss |
| GSE287257, [Zelic](https://doi.org/10.1016/j.immuni.2025.02.024) | Cervical snRNA-seq catalogue | 12 gene-by-barcode H5 matrices, no separate author annotation in the archive | MN-specific annotation and coverage unverified; no target extraction |
| [Takeuchi](https://doi.org/10.1093/brain/awaf426), 2026 | Human spinal snRNA author pseudobulk tables | MN −3.51%, padj 0.99994; excitatory and inhibitory near-zero positive estimates; MN_1 −3.70%, padj 0.76695 | Shrunken estimates; no formal diagnosis-by-cell-type interaction; contributing donor coverage unverified; MN_1 not independent |
| [Krach](https://doi.org/10.1007/s00401-018-1870-7), GSE76220 | LCM-enriched human spinal MN RNA, exploratory common-subset calculation | −14.73% arithmetic mean RPKM ratio; difference −0.2690 RPKM, unadjusted Welch 95% interval [−0.4884, −0.0497] | 12 ALS / 8 controls matched to GEO; historical file includes withdrawn control and omits one deposited ALS sample; no full-cohort or DESeq2 replay; mixture and survivorship limits |
| [NeuroLINCS](https://doi.org/10.1016/j.isci.2021.103221), 2021 | Day-18 C9orf72 ALS iPSC-derived MN culture replication cohort, 6 ALS / 7 controls | RNA +50.46%, padj 0.84148; protein +39.56%, source FDR 0.0000450387 | Concordant point estimates in same described culture cohort; RNA not significant; no per-analyte donor-pair map or individual correlation verified; not PFKP replication of original cohort or postmortem tissue |
| [MAXOMOD](https://doi.org/10.1038/s41467-024-49196-y), 2024 | Human bulk BA6 PFC, 51 ALS / 50 controls, sex-stratified | Protein male −0.56% (padj 0.97706), female −1.67% (padj 0.96366); RNA PFKP unavailable from filtered table | No RNA–protein comparison possible; non-significant protein estimates not equivalence; exact analyte-level overlap unverified; no sex interaction |
| [Guise](https://doi.org/10.1016/j.celrep.2023.113636), 2024 | Isolated human spinal MN protein | −68.1%, source BH flag true | Prior audited result; small donor cohort, no new model, independent magnitude replication unresolved |

The 26 November audit also retains Feneberg and Chan smaller negative PFKP protein estimates, Spiteri mostly positive regional estimates and Aly small positive pooled synaptic ratios. These do not resolve the differences across contexts. Cross-study donor overlap remains unverified. Neither near-zero estimates nor insufficient support imply absence.

## Provenance and reproducibility

The appendices preserve the pre-target plans, source hashes, fields, calculated values and actual code or equivalent aggregate-only audit logic. No individual-level rows, raw matrices, sequence reads or clinical identifiers are included. Earlier statements about no publication describe the analysis step before authorization of this archival release.

- [Initial intake and Manzo prior evidence](INTAKE.md)
- [Target-blind donor and annotation audit of GSE330130](GSE330130.md)
- [Takeuchi source-statistics audit](TAKEUCHI.md)
- [Krach historical-matrix audit and exploratory calculation](KRACH.md)
- [NeuroLINCS common-cohort RNA/protein source audit](NEUROLINCS.md)
- [MAXOMOD source audit](MAXOMOD.md)
- [26 November five-study proteomics audit](../cross-study-proteomics-audit-20261126/REPORT.md)

The new source checks were conducted on public files only. RNA percentages, protein percentages, nuclear versus whole-cell measurements, cohorts, disease genotypes and assay normalization are not quantitatively pooled.

## Closure and next discriminating inputs

- GSE330130 lumbar interaction route closed before target inspection; GSE287257 pending annotation, not a negative biological result.
- Krach subset closed; only a corrected full-cohort matrix or authoritative full source statistics could clarify the missing sample and permit a separate review.
- NeuroLINCS source audit closed; matched donor-level anatomic or cellular evidence with adequate measurement and consistent units would be needed for a formal RNA/protein association.
- MAXOMOD source audit closed; only a verified full human RNA DE table or compatible, authorized paired measurements could fill the gap.
- Resume UNC13A priority only when compatible independent human event-level RNA and protein data, unit maps or substantive pending author/access inputs are available. No automatic reopening of closed analyses.

No mechanism, enzyme activity, neuronal function, prognosis or clinical efficacy conclusion is justified. This is an archival closure of a bounded research cycle, not a discovery of a therapeutic target.
