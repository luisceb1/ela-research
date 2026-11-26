# Integrated evidence review and critical audit — 26 November 2026

## Scope and status

Documentary review of the ALS research project's existing public-source results against selected primary publications and deposited study descriptions. Baseline: main commit `674c01c478bbe362411b26f3109e0e6b49250862`. No new biological measurements, models, thresholds or cloud execution. This is a targeted, AI-assisted critical review, not a systematic literature review, peer review, independent biological replication or clinical assessment. Some publisher/full-text pages were inaccessible; available article records and the project's previously documented source reviews were used where necessary.

## Evidence and decisions

| Work | Recorded finding | Critical interpretation |
|---|---|---|
| GSE252892 STMN2 | Six libraries: control canonical/cryptic 1945/3, 2806/5, 2438/0; KD 253/727, 173/551, 140/556. Local replay: 12/12 event counts, 30/30 QC fields. | Descriptive repetition within one background and technical reproducibility of existing inputs; compatible with known STMN2 biology, not a novel mechanism. |
| Independent-host STMN2 | One control library, 7/7 fields matched; cleanup verified. | Technical portability for that library only. |
| GSE252892 UNC13A | Control canonical/left/right 106/0/0; KD 41/0/3. | Below fixed 20-group cryptic-support diagnostic; not evidence of biological absence. |
| PRJDB19918 UNC13A | Control 79/0/0; KD 56/2/0; both pilots completed with independent cleanup. | Insufficient local support; no verified independent culture map. Not a negative biological replication. |
| GSE304550 | Descriptive factorial contrasts M85/M86: UNC13A +16.64/+3.81 pp; PFKP +20.13/+8.70 pp. | Within-study exploratory result, direction repeated across recorded blocks. UNC13A differs qualitatively from the original Fig. 5F account; metrics are not equivalent. |
| Keuss Fig. 4d | Conditional replay of 89 original observations: ASO–KD direction positive, nominal p=0.007036; 2/3 leave-one-block-out intervals include zero; three-star band not reproduced. | Partial statistical reproduction of one panel, not a rejection of the paper or independent efficacy evidence. |
| Donor data | 45 previously examined ALS pairs: 24 cervical higher, 14 ties, 7 lower; median local-ratio difference +0.368 pp; nominal exploratory sign-test p=0.0033. | Same cohort, selection by coverage, tissue composition and unequal depth; no external confirmation. |
| Ikegami | Same 35 cases; adjusted rank rho 0.31669, exploratory p=0.07825, interval [-0.02342, 0.62758]; fixed prediction not met. | Retain the negative prediction outcome; no evidence of absence of association. |
| E-MTAB-15433 | Candidate source; technical catalogue and SDRF reconciled in a separate pending intake, with no admitted independent-unit map or junction counts. | No new result; 16 libraries are not automatically 16 independent biological replicates. |

## Comparison with primary literature

**STMN2.** [Klim et al. (2019)](https://doi.org/10.1038/s41593-018-0300-4) and [Melamed et al. (2019)](https://doi.org/10.1038/s41593-018-0293-z) already establish the association of TDP-43 depletion with STMN2 RNA processing and expression changes. [Zeng et al. (2025)](https://doi.org/10.1038/s41593-025-02049-3) and [GEO GSE252892](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE252892) identify the underlying cortical-neuron study. GEO lists six RNA-seq libraries and six separate 3'-end-seq libraries. The project's contribution is an audited computational reproduction, not discovery of the molecular phenomenon. The report describes independent replications at study level; the exact library-to-preparation map and protein efficacy are not independently verified by this project. Raw counts are not calibrated RNA abundance or functional rescue.

**UNC13A.** [Brown et al. (2022)](https://doi.org/10.1038/s41586-022-04436-3) and [Ma et al. (2022)](https://doi.org/10.1038/s41586-022-04424-7) provide biological evidence for cryptic splicing and reduced UNC13A protein following loss of TDP-43 function. Brown's [2024 correction](https://doi.org/10.1038/s41586-024-07577-9) clarifies a cell-line identity; use the corrected version. Our low-support results neither contradict nor independently confirm this literature. [Tanaka et al. (2025)](https://doi.org/10.1038/s42003-025-08463-4) studied cryptic splicing in motor neurons using complementary sequencing assays; the assays sharing BioSamples are not additional biological replicates. The [NYGC ALS resource preprint (2026)](https://doi.org/10.64898/2026.04.29.26350889) describes inadequate UNC13A spliced-read support under its cross-tissue criteria. This is contextual support for measurement limitations, not proof of the cause of our observations or independent confirmation; dataset overlap is unresolved.

**GSE304550.** [Alessandrini et al. (2026)](https://doi.org/10.1016/j.neuron.2025.11.001), Fig. 5F, describes an increase for PFKP but not UNC13A under its transcript-read measure. Our UNC13A directional result differs, while PFKP agrees qualitatively. The local fraction of junction support is not the paper's ratio of cryptic-containing reads to all transcript reads; the contrasts also differ in scope. This discrepancy is not a formal contradiction or refutation of the original study. The 16 libraries are the original dataset, not a new replication. The recorded 112 counts and 16 logs reconcile; original FASTQ byte identities and executed counter/downloader remain unresolved. A biological pairing map is not established. No mechanism, RNA stability or novel therapeutic target is concluded.

**Keuss.** [Keuss et al. (2026)](https://doi.org/10.1038/s41586-026-11256-2) reports preclinical synaptic outcomes; some phenotypes were not restored. Our conditional reanalysis concerns only Fig. 4d; the published significance band was not reproduced, and nesting and exact author model output remain unresolved. Positive direction is not equivalence to control or complete neuronal recovery. The paper discloses relevant commercial and patent interests; this is not a reason to dismiss its findings. Neither the paper's preclinical observations nor this replay establish clinical efficacy.

**Donors.** [Ikegami et al. (2026)](https://doi.org/10.1186/s40478-026-02400-0) reports pathological subtype heterogeneity in retrospective motor-cortex samples. Our subtype-conditioned analysis uses the same observations, and its fixed prediction was not met. The paired-region analysis uses a separate previously examined cohort; its nominal significance does not resolve cell composition, RNA quality, batch, unequal precision or selection and is not evidence of a distinct causal mechanism.

## Alternative explanations and review decision

Local measurement support, biological context, RNA processing, and methodological differences are non-exclusive possibilities. Current results do not determine their relative contributions. Preserve measured zeros, failed predictions and discrepant results. Do not combine non-equivalent endpoints or magnitudes into a pooled estimate. The material next inputs are documented experimental unit maps, source measurement definitions and independent comparable observational evidence. Access to restricted platforms remains unverified; no new data acquisition or author communication follows this review.

## Conclusion suitable for public communication

The project documents computational reproducibility of selected known TDP-43-associated RNA-processing observations, especially STMN2, and identifies limitations of local measurements, differences between transcriptomic metrics, and incomplete statistical reproduction of a published functional panel. The work is a reproducibility and methodological contribution. It does not establish a new biological mechanism, independently validate a therapeutic target, demonstrate complete neuronal recovery or establish clinical benefit.

## Project records

- [Current state](../../research/STATE.md)
- [STMN2 six-library result](../stmn2-remaining-result-20261116/REPORT.md), [local replay](../stmn2-real-replay-20261118/REPORT.md), [cloud pilot](../stmn2-hetzner-pilot-20261126/REPORT.md)
- [GSE252892 UNC13A audit](../gse252892-audit-verification-20261114/REPORT.md), [Tanaka closure](../prjdb19918-metadata-intake-20261126/PILOT_CLOSURE.md)
- [GSE304550 factorial report](../gse304550-factorial-20261126/REPORT.md)
- [Keuss conditional replay](../k26-conditional-replay-20261111/REPORT.md)
- [Paired donor report](../paired-stmn2-20261111/REPORT.en.md), [Ikegami review](../pr53-integration-20261112/REPORT.md)
- [E-MTAB-15433 pending intake PR](https://github.com/luisceb1/ela-research/pull/98) (not part of this publication or merge).

Publication of this documentary review does not reopen any closed pilot or authorize new compute, transfers, clinical work or outreach.
