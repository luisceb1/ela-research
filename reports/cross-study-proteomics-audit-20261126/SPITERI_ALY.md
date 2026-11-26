# Spiteri and Aly: follow-up human ALS proteomics audit
26 November 2026 — documentary and numerical audit of supplied publisher tables.

## Question and scope
Do two additional human proteomics studies support the direction and magnitude of the previously audited PFKP association? Preserve all target contrasts for PFKP (Q01813), STMN2 (Q93045) and UNC13A (Q9UPW8), including opposing and non-significant results. This is extraction and arithmetic reconciliation of published summary data, not a new biological experiment, model fit or raw mass-spectrometry replay.

## Sources and provenance

- Spiteri et al., 2025, Scientific Reports 15:33959, https://doi.org/10.1038/s41598-025-11466-0, PXD062542. Publisher Supplementary Information 1, `41598_2025_11466_MOESM1_ESM.xlsx`, SHA-256 `9ab482d1c10a4b8464fff924318ad9a287b4790193ab3f72c3eeebe7b9e336cb`.
- Aly, Laszlo et al., 2023, Acta Neuropathologica 146:451–475, https://doi.org/10.1007/s00401-023-02611-y, PXD042617. **Corrected** workbook published with https://doi.org/10.1007/s00401-023-02630-9, `401_2023_2630_MOESM2_ESM.xlsx`, SHA-256 `e62a5e1eef95393a31bb78413b49cc929d1d72e8629a3782b3f7398295285bbe`.
- Workbooks read without modification via openpyxl (read-only, cached values). Exact accession and gene agreement checked for target rows; human tissue only. No missing value imputation or statistical testing was performed by the project.

## 1. Spiteri: donor-level bulk human tissue contrasts
The study describes 10 sporadic ALS and 5 control donors, each contributing cervical, lumbar and thoracic spinal cord and motor cortex; the four regions represent repeated measurements of the same 15 individuals. The study reports adjusted limma models and a combined analysis accounting for repeated donor and tissue effects. The source supplement also contains mouse results; they are excluded. Cross-study donor overlap is unverified; the human samples came from the Victorian Brain Bank.

In `Human limma results` all three target proteins are reported as high-confidence master proteins with zero missing values and imputed=False; unique peptide counts are 25 (PFKP), 3 (STMN2), and 23 (UNC13A). Protein identification q-values are not differential q-values. All 15 target contrast significance flags and each target's overall significant flag are False. The authors describe a 1.5-fold effect selection cutoff plus BH adjusted p<0.05. The table below retains native source `diff` and interval fields; no transformation to percent abundance is assumed.

| Protein (Excel row) | Contrast | Author diff | Author CI.L | Author CI.R | Nominal p | Adjusted p | Significant |
|---|---|---:|---:|---:|---:|---:|---|
| PFKP (4414) | Combined | +0.471719 | -0.630291 | 1.573728 | 0.393667 | 0.672442 | False |
| PFKP | Cervical | +0.242527 | -0.067551 | 0.552604 | 0.122363 | 0.683692 | False |
| PFKP | Lumbar | +0.168010 | -0.142068 | 0.478087 | 0.281373 | 0.569023 | False |
| PFKP | Motor cortex | -0.023775 | -0.333852 | 0.286303 | 0.878115 | 0.939936 | False |
| PFKP | Thoracic | +0.084957 | -0.225120 | 0.395035 | 0.584232 | 0.786533 | False |
| STMN2 (6068) | Combined | -0.937241 | -2.403140 | 0.528658 | 0.204751 | 0.499169 | False |
| STMN2 | Cervical | -0.317028 | -0.729495 | 0.095438 | 0.128802 | 0.690916 | False |
| STMN2 | Lumbar | -0.248152 | -0.660618 | 0.164315 | 0.232306 | 0.522280 | False |
| STMN2 | Motor cortex | -0.053648 | -0.466114 | 0.358819 | 0.794796 | 0.894635 | False |
| STMN2 | Thoracic | -0.318413 | -0.730880 | 0.094053 | 0.127179 | 0.388910 | False |
| UNC13A (6758) | Combined | -1.761581 | -3.838113 | 0.314952 | 0.094523 | 0.347339 | False |
| UNC13A | Cervical | -0.090609 | -0.674893 | 0.493674 | 0.756516 | 0.984460 | False |
| UNC13A | Lumbar | -0.402441 | -0.986725 | 0.181842 | 0.172471 | 0.452961 | False |
| UNC13A | Motor cortex | -0.589462 | -1.173745 | -0.005178 | 0.048082 | 0.196939 | False |
| UNC13A | Thoracic | -0.679068 | -1.263351 | -0.094785 | 0.023674 | 0.170793 | False |

**Scale check:** for each of these three rows the combined diff equals the sum of the four region-specific differences within rounding (PFKP +0.47171855864037, STMN2 -0.937241023681167, UNC13A -1.76158054507654). Thus do not read the combined diff as a mean region effect or directly transform it into a percentage reduction. Exact model contrast and normalization details were not replayed. Regional contrasts also remain on the source scale, which is not assumed interchangeable with the earlier audit.

PFKP is positive in three of four tissue regions and slightly negative in cortex. All four source intervals contain zero. STMN2 and UNC13A point estimates are negative in all four regions. UNC13A cortex and thoracic nominal p values fall below 0.05 but do not survive BH adjustment. They are not corrected significant findings. No evidence of equivalence or a null biological effect follows from the non-significant results.

## 2. Aly: pooled human spinal cord synaptic fractions

The corrected workbook's cover page identifies the postmortem dataset as technical replicate reporter signals. The article's discovery sample design pools 10 control donors, 10 sporadic ALS donors with TDP-43 pathology, and 10 C9orf72 ALS donors into one sample per group, with two technical replicates. Therefore donor-level inference is not supported by those six measurements. Between-donor variability cannot be reconstructed. This is a synapse-enriched cervical spinal cord fraction, not isolated motor-neuron whole-cell abundance.

`Normalized` sheet author columns M–P provide uncorrected group-mean ratios and median-corrected ratios. All three targets have positive reporter intensities in all six measurements. The source ratios are tabulated without pooling genotypes.

| Target (row in RAW and Normalized) | Raw sALS/control | Raw C9/control | Median-corrected sALS/control | Median-corrected C9/control | Median-corrected changes |
|---|---:|---:|---:|---:|---|
| PFKP (3431) | 1.068599 | 1.006562 | 1.028851 | 1.016310 | +2.89%, +1.63% |
| STMN2 (4747) | 1.208449 | 1.079225 | 1.163499 | 1.089676 | +16.35%, +8.97% |
| UNC13A (5270) | 0.532591 | 0.700511 | 0.512781 | 0.707296 | -48.72%, -29.27% |

Raw group intensities (two technical measurements per pool):
- PFKP: control 13,173,000 / 11,361,000; sALS 12,876,000 / 13,341,000; C9 12,186,000 / 12,509,000.
- STMN2: control 100,140 / 101,060; sALS 120,920 / 122,220; C9 102,770 / 114,370.
- UNC13A: control 711,680 / 799,930; sALS 375,660 / 429,410; C9 520,390 / 538,510.

The `Vulcano plot ` worksheet lists separate source log FC, p and q values. Exact gene labels are reconciled to the verified target rows in RAW/Normalized; columns A–D for sALS and I–L for C9.

| Target | sALS row | Log FC | p | q | C9 row | Log FC | p | q |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| PFKP | 2498 | +0.088963 | 0.344791 | 0.391110 | 2575 | +0.016833 | 0.840938 | 0.865338 |
| STMN2 | 1588 | +0.262676 | 0.066452 | 0.098275 | 2014 | +0.111523 | 0.173600 | 0.228461 |
| UNC13A | 5247 | -0.920135 | 0.020024 | 0.040951 | 4992 | -0.507694 | 0.060229 | 0.101823 |

The source sALS UNC13A q is below 0.05; the C9 value is not. **These are reported source statistics derived from pooled material and technical measurements; the sALS q cannot establish donor-level significance.** They are not newly calculated q-values. The source cover describes median-normalized log2 transformed data, but the volcano log FC is not numerically identical to log2 of the normalized sheet ratios; do not silently equate these endpoints or reconstruct the model. UNC13A appears in `TDP43_synapticinteractors` row 755 with z-scores -1.694372 and -1.137117; this is a re-expression of the same pooled dataset and not an additional result. Other workbook alignment sheets are not additional independent human postmortem evidence.

## 3. Integration with the prior three-study audit

| Target | Previous evidence | New evidence | Updated assessment |
|---|---|---|---|
| PFKP | Guise strong negative author contrast; Feneberg smaller negative non-significant estimates; Chan small descriptive decrease | Spiteri mostly positive estimates, all non-significant; Aly small positive pool ratios | Direction is **not consistently negative across studies**. Large Guise human cell-specific observation is not generalized by these bulk or synaptic measures. No new cell-specific replication. |
| STMN2 | Chan model reduction with author q<0.05; lower human detection in Guise | Spiteri uniformly negative non-significant effects; Aly positive pool ratios | Published model result remains; tissue/fraction heterogeneity prevents a general human abundance conclusion. |
| UNC13A | Guise missing; Feneberg mixed non-significant; Chan descriptive decline | Spiteri negative in four regions (no corrected significance); Aly lower pooled synaptic ratios, especially sALS | Additional directional human-tissue evidence; pooled significance not donor-level proof. No direct confirmation of the project's specific RNA-junction measurements. |

No pooled quantitative estimate, no clinical biomarker or treatment claim, and no mechanistic attribution are justified. The three previous audits remain valid in their original scope; broad statements of directional PFKP agreement across **all** studies must now be revised. Differing tissue composition and measurement context are possible explanations, not demonstrated mechanisms. Close both supplementary-table audits. Further generalization requires comparable independent cell-specific human evidence, not another reinterpretation of the same tables.

No new cloud execution, expense or researcher communication was undertaken. This is a documentary audit of previously published results.
