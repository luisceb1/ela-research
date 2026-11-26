# Cross-study proteomic evidence audit: STMN2, UNC13A and PFKP

**26 November 2026 — Independent ALS research project — Documentary evidence audit**

## Updated conclusion — five-study comparison (26 November 2026)

The five-study audit now shows **mixed PFKP direction**: Guise reports −68.1% relative abundance in human spinal motor neurons; Feneberg and Chan have smaller negative estimates, but Spiteri has positive estimates in three of four bulk tissue regions and Aly has small positive synaptic-pool ratios. Spiteri's STMN2 and UNC13A estimates are negative across four regions, none significant after correction. Aly has positive STMN2 ratios and lower UNC13A in pooled synaptic material (−48.72% sporadic ALS, −29.27% C9orf72 ALS); the sporadic source q=0.040951 is not donor-level significance. Different endpoints and units; no independent quantitative replication or clinical inference.

The additional [Spiteri and Aly supplementary-table audit](SPITERI_ALY.md) records exact source rows, native contrast estimates, adjusted p-values, source hashes and the corrected Aly workbook. The new evidence supersedes any suggestion of uniform PFKP direction beyond the original three-study comparison. No additional computation on raw samples or independent biological experiment was conducted.

| Study | PFKP | STMN2 | UNC13A |
|---|---|---|---|
| Guise 2024 | −68.1%, author BH flag true | Lower detection; BH flags false | Not identified in inspected target rows |
| Feneberg 2025 | Four negative estimates, none FDR-significant | Not located | Mixed estimates, none FDR-significant |
| Chan 2026 | −4.4%, descriptive | −56.1%, source q=0.0003472, cellular model | −17.1%, descriptive |
| Spiteri 2025 | Three positive regional diff estimates; one slightly negative; all adjusted p>0.05 | Four negative regional estimates, all adjusted p>0.05 | Four negative regional estimates, all adjusted p>0.05 |
| Aly 2023 | +2.89% sALS, +1.63% C9, median-corrected pool ratios | +16.35%, +8.97%, pooled | −48.72%, −29.27%, pooled; sALS source q=0.040951 |

Spiteri's combined source contrast equals the sum of four regional contrasts in these target rows; neither the combined nor regional native diff is converted into a percentage. Four regions are repeated observations of 15 donors, not 60 independent donors. Aly has one pooled sample per condition (10 donors per pool) with two technical replicates. Its reported source q is not a test across independent donors. The three-study audit below is retained in its original scope, including its historical decision and source provenance; this update and the linked supplement take precedence for the broader comparison.

---

## Original three-study audit (historical scope)

## Executive conclusion

The three audited publications support different levels of evidence, not a single replicated result. PFKP has a marked author-reported reduction in postmortem spinal motor neurons in Guise et al.; point estimates in Feneberg et al. and Chan et al. are also lower than their respective controls, but considerably smaller and without confirmed differential significance in the inspected tables. STMN2 has a strong published protein-level result in the Chan cellular model and lower detection in Guise's ALS neurons, but the latter does not establish a quantitative reduction. UNC13A remains unresolved across these proteomic datasets. None of these observations constitutes clinical validation.

This synthesis uses the completed supplementary-table audits only. No new raw-data processing, inferential model, pooled estimate or biological experiment was performed. The date is the project's reference date.

## 1. Evidence by study

| Study | Design and biological unit | PFKP | STMN2 | UNC13A |
|---|---|---|---|---|
| Guise (2024), PXD042799 | Laser-captured postmortem spinal motor neurons; cells nested within a small number of donors | ALS/control author log2 FC −1.647, BH significance flag true | Lower detection in ALS; author contrast BH flags false | Not identified among inspected target rows |
| Feneberg (2025), PXD067060 | Postmortem bulk spinal cord and cerebral cortex; soluble and insoluble fractions | Four negative effect estimates (−6.9% to −15.7%); none FDR-significant | Not located among contrast rows | Three estimable contrasts, mixed signs, none FDR-significant; fourth unavailable |
| Chan (2026), PXD062725 | Published human iPSC-derived motor neuron model; three independent cell vials per group, not three unrelated donors | −4.4% descriptive mean signal; not a selected differential protein | −56.1%; matches reciprocal published figure ratio; source q=0.0003472 | −17.1% descriptive mean signal; no author differential p/q located |

These percentages refer to different normalized signals and comparisons. They are not interchangeable estimates of a population effect. The four Feneberg compartments are not four independent cohorts; Guise's pilot and stratified tables share donor labels. Cross-study donor overlap in human tissue was not independently established.

## 2. PFKP: directional agreement without quantitative replication

Accession Q01813; some source tables use the symbol PFKAP.

| Source and contrast | Relative change vs reference | Statistical status |
|---|---:|---|
| Guise ALS vs control | −68.1% | Author BH flag true; nominal source P=8.65×10⁻⁸ |
| Guise no overt inclusions vs control | −63.3% | BH flag true; P=0.001385; below the publication's additional absolute log2 FC cutoff of 1.5 |
| Guise MLD/MOD/SEV vs control | −69.5% | BH flag true; P≈1.08×10⁻⁷ |
| Feneberg spinal cord soluble | −8.55% | FDR 0.448450 |
| Feneberg spinal cord insoluble | −7.73% | FDR 0.937215 |
| Feneberg cortex soluble | −6.86% | FDR 0.747636 |
| Feneberg cortex insoluble | −15.74% | FDR 0.478633 (nominal P=0.033045) |
| Chan model vs WT | −4.40% | Descriptive ratio; differential p/q unavailable in inspected selected figure table |

The principal comparison is ALS versus controls (Guise and Feneberg) or model versus WT (Chan). The extra Guise contrasts provide within-study context, not independent confirmation.

**Human motor-neuron evidence:** Guise's pilot contained 18 ALS and 18 control neurons (three donors per group). Its stratified table contained 75 ALS and 25 control neurons (three and two donors respectively). Positive PFKP abundance was available in 18/18 vs 16/18 pilot cells and 73/75 vs 25/25 stratified cells. Supplement 6, FoldChange_TDP43pseudotime, row 1826, reports log2 FC −1.646721925 for ALS vs control. Its BH field is a boolean flag, not a numeric adjusted p-value; we did not reproduce the authors' fitted model.

**Important negative result:** Guise's adjacent ALS-only inclusion stage comparisons have false BH flags. A descriptive Spearman coefficient including controls is −0.4322246 (98 observed pairs); restricted to ALS it is +0.0606838 (73 pairs). The coefficients agree with the source, but their nominal p-values do not exactly reproduce. The combined correlation sheet has mismatched accession/gene labels (PFKP-labelled row 758 lists P52815; Q01813 is paired with MBP elsewhere). The ALS-only adjusted p field exceeds 1 as stored. Donor-specific reported pair counts (48/45/47) exceed the 25 sampled ALS neurons per donor; definitions were not reconciled. These issues preclude a claim of donor-specific replication or a monotonic relationship to ALS inclusion stage. No overt inclusions does not establish intact nuclear TDP-43 function. The strata are cross-sectional, not elapsed time.

**Independent-study context:** Feneberg supplement 3 rows 2344, 646, 420 and 203 in the four tissue/fraction worksheets respectively contain the negative PFKP estimates. None meets the authors' FDR threshold, including cortex insoluble despite the nominal P<0.05. Additional ALS vs pooled non-ALS, AD and PD comparisons do not establish corrected significance for PFKP. Bulk composition, tissue region, protein extraction and model differences may be relevant explanations for the smaller estimates; the available aggregate data cannot distinguish these explanations. Chan supplement data 2 (processed proteomics), row 5990, has all six positive measurements; means are 133374.9063 vs 139508.9375, ratio 0.956031. This is below the published Figure 3 effect selection threshold, and absence from that selected table does not prove a null result.

**Assessment:** PFKP remains an exploratory molecular comparator. The Guise result is the strongest observed human protein-level association in these sources. The other studies provide descriptive directional concordance, not replication of its magnitude or statistical evidence. No PFKP-specific metabolic mechanism, diagnostic utility or treatment effect has been established. The absence of corrected significance is not evidence of equivalence.

## 3. STMN2: model-level protein evidence and limited human detection

Guise's Q93045 positive abundance detection was 0/18 ALS vs 3/18 controls in the pilot and 4/75 ALS vs 11/25 controls in the stratified material. Missingness is substantial, missing is not zero and a reported signal need not be direct peptide confirmation in the individual cell. Author supplement 6 flags are false for all inspected STMN2 contrasts; their log2 FC estimates are +0.68067, −0.52128 and +0.70669. No quantitative human protein loss can be established from those tables. Feneberg did not supply an identifiable STMN2 contrast row in the inspected tables.

Chan's processed proteomics row 8227 yields mean model signal 300898.0209 vs WT 685535.9792 (ratio 0.438924). All six measurements are positive. Figure 3a source row 632 reports the reverse WT/model log2 FC +1.1879577619, source p=0.0001738960 and q=0.0003472049. The reciprocal mean ratio matches the published fold change, a numerical reconciliation of an existing study, not a replay of its paired test (pairing was unverified).

**Assessment:** The Chan result provides published protein-level evidence in a cellular model consistent with the project's existing STMN2 RNA observations. It does not independently validate human protein abundance, quantify a clinical effect, or establish therapeutic benefit.

## 4. UNC13A: unresolved protein evidence

Guise's inspected tables did not identify Q9UPW8. Feneberg soluble spinal cord, soluble cortex and insoluble cortex show author log2 FC +0.143999, +0.118937 and −0.092598 respectively (FDR 0.844505, 0.897553 and 0.884157); insoluble spinal cord entries are NA. Source supplement 3 rows 1174, 2254, 967 and 1305 index these observations. Chan processed proteomics row 9204 has six positive values, means 22282.1908 vs 26867.3040 (ratio 0.829342); no author differential p/q was available in the selected table. The protein group is not an isoform-specific measurement, and the published lack of demonstrable baseline aberrant UNC13A splicing in that model does not prove normal protein abundance.

**Assessment:** Heterogeneous descriptive endpoints and insufficient corrected statistical evidence. No claim of a confirmed protein reduction or of preserved protein function. Retain the project's existing insufficient UNC13A junction evidence and discrepancy with Alessandrini separately; protein measurements cannot settle that RNA discrepancy.

## 5. Metabolic observations are context, not PFKP functional evidence

Chan's published processed co-culture metabolomic signals produced the following descriptive model/WT mean ratios: lysate fructose-6-phosphate 1.064, fructose-1,6-bisphosphate 0.720, sodium lactate 0.788; supernatant fructose-1,6-bisphosphate 0.173 and sodium lactate 1.453. The measurements are not matched per sample to the proteome; the opposite lactate direction between compartments illustrates the risk of collapsing them. They establish neither glycolytic flux nor PFKP enzyme activity nor causal attribution. No inference about absolute concentrations or relative quantities across analytes is made.

## 6. Relationship to the project's closed RNA work

| Level | What is supported | What is not supported |
|---|---|---|
| Computational reproducibility | Existing STMN2 local technical reproduction of six original libraries and one independent-host pilot; selected source-table arithmetic reconciliations in Guise and Chan | Full replay of Guise or Chan statistical models; independent biological validation from the same original samples |
| Biological evidence | Published human tissue PFKP association; published STMN2 protein change in a cellular model; weaker descriptive observations elsewhere | A common quantitative effect across all three studies; definitive UNC13A protein loss; independently confirmed PFKP causal mechanism |
| Clinical evidence | None established by this audit | Clinical biomarker validation, prognosis, treatment efficacy, or patient-specific conclusions |

The project's exploratory GSE304550 PFKP splicing contrast was qualitatively concordant with Alessandrini, but it used original-study libraries and unresolved pairing; RNA junction usage and protein abundance are different endpoints. It is not valid to use a protein abundance observation as direct replication of a junction result. UNC13A negative or insufficient evidence remains on record. The previous partial Keuss statistical reproduction is unchanged.

## 7. Decision and priorities

1. **Close the three present supplementary-table audits.** No reason to refit these same aggregate tables or seek a different threshold merely to obtain significance.
2. **Prioritize compatible, genuinely distinct human evidence.** In a future documentary review, look for published cell-specific protein measurements, clear donor-level units and reported uncertainty; distinguish independent donors from repeated cells and document cohort provenance. The outstanding question is whether the marked PFKP observation in Guise generalizes beyond that dataset, not whether another nominally negative number can be found.
3. **Retain STMN2 as the best-supported anchor within this project and keep UNC13A explicitly unresolved.** For pending data-access and author clarifications, do not treat unavailable data as a negative biological finding.

Public summary: “Three published proteomics datasets were audited. PFKP estimates were directionally concordant but differed substantially in magnitude and statistical support; STMN2 showed a published protein-level change in a cellular model; UNC13A protein evidence was inconclusive. This analysis does not establish clinical or therapeutic findings.”

No new biological analysis, researcher communication, spending or remote computation was undertaken for this audit.

## 8. Sources and provenance

Primary studies:
- Guise et al. (2024), *Cell Reports*. [DOI 10.1016/j.celrep.2023.113636](https://doi.org/10.1016/j.celrep.2023.113636), PXD042799.
- Feneberg et al. (2025), *Acta Neuropathologica Communications*. [DOI 10.1186/s40478-025-02084-y](https://doi.org/10.1186/s40478-025-02084-y), PXD067060.
- Chan et al. (2026), *Communications Biology*, article in press at reference date. [DOI 10.1038/s42003-026-10832-6](https://doi.org/10.1038/s42003-026-10832-6), PXD062725.
- Project [integrated evidence audit, 26 November 2026](https://github.com/luisceb1/ela-research/blob/main/reports/integrated-evidence-audit-20261126/REPORT.md).

This synthesis relies on the following same-date component audit records (working notes; source worksheets and hashes are identified here):
- Guise_proteomics_audit_2026-11-26.md
- Guise_PFKP_author_statistics_audit_2026-11-26.md
- Feneberg_PFKP_proteomics_audit_2026-11-26.md
- Chan_proteomics_metabolomics_audit_2026-11-26.md

Key supplementary files and SHA-256 provenance (as recorded in the component audits, no rehash asserted):

**Guise_proteomics_audit_2026-11-26.md**

- NIHMS1961509-supplement-2.xlsx: SHA-256 5a95bad26b56efa621285be41c799ebe8b8f55601b02a9bfb57c079718583bec. Sheet MasterProteins_5%FDR_1unique: normalized abundance columns 67–102, header rows 3–7; sheet DEPsLFC>=1.5,p-adj<0.05 is an already filtered author table. The workbook labels the sheets S2A/S2B; the final paper refers to the pilot as Table S1. Preserve exact filename and sheet names.
- NIHMS1961509-supplement-3.xlsx: SHA-256 cf9dae8aa456369956b36a25542352a13f68c2309c38c6e172d7877010d94bcf. Sheet HCMP_1unique_NormAbund, columns 4–103, headers 1–7; the DEPs sheet contains no non-empty values. The six metadata rows distinguish diagnosis, donor and pathology stratum. Strip trailing whitespace from stage labels only; one MLD label has an extra space.

**Guise_PFKP_author_statistics_audit_2026-11-26.md**

- supplement-4 SHA-256 e94073c99bc5041422cfca8aa732e4aab9f23299e29d010bfcf1a5feba10f0c9
- supplement-5 SHA-256 f4d1be86acef2f5c60e9e9585a0b8fb78dac4c33ce61c492978f6d8639689b67
- supplement-6 SHA-256 1a0d8f75ff2c6bdbc6853077ba95c667adbbc85dc0ccda470afc81c98aef5aca
- supplement-7 SHA-256 50fb033250a2d40ce8ef4594ad890d9c255ed333a75024ce6daf7352954c0e3d
- previously supplied supplement-3 SHA-256 cf9dae8aa456369956b36a25542352a13f68c2309c38c6e172d7877010d94bcf

**Feneberg_PFKP_proteomics_audit_2026-11-26.md**

- 40478_2025_2084_MOESM3_ESM.xlsx SHA-256 3e8dc47f19ab33c00d67222bdfa6d26284360634f0d4b12ea1286eef3b7546fd.
- 40478_2025_2084_MOESM4_ESM.xlsx SHA-256 1fd5eb94a07376963f8972a949925488cc5eec345c06e648fef9b706d4cc39fe.
- 40478_2025_2084_MOESM5_ESM.xls SHA-256 fe0d8e47bd5b9ac27c66bbdc2056bce8311f2b27701d48e4c4c5fd770c97fa0e.

**Chan_proteomics_metabolomics_audit_2026-11-26.md**

- 42003_2026_10832_MOESM3_ESM.xlsx (source figures), SHA-256 65841277c4f8f3164487d7c13902dbbeec717f7fe7cac90d24c83f6112800281
- 42003_2026_10832_MOESM4_ESM.xlsx (processed proteomics), SHA-256 7fc472663a01ef72d0484631e1c236fb962ee3458382c7ed9c0b5973900fd85d
- 42003_2026_10832_MOESM5_ESM.xlsx (processed metabolomics), SHA-256 6cc9d7426e370bdd37b08d5b014b1cd3641a0ad40f1377942d8fe3cee31b5534
