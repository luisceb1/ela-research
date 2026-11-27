<!-- Working record from the completed 27 November cycle, authorized for public archival release. Statements about no publication/repository changes describe the original analysis step. Only aggregate results and reproducibility details are included. -->

# PFKP cell-specificity — source admission and prospective analysis draft

Reference date: 27 November 2026. Internal working document; not a publication.
Repository baseline: `47b7ee619210a0fcc568ec06855393d7f10ee2e0`. The five-study proteomic audit remains closed. This document contains source-level verification and a prospective draft, not a fitted result.

## 1. Decision-changing question

In adult postmortem human spinal cord, is the ALS-associated difference in PFKP **nuclear RNA abundance** more negative in surviving annotated motor neurons than in other spinal neurons? A positive result would provide evidence for RNA-level cell-context specificity; it would not replicate Guise's protein effect, establish cell loss as its cause, establish PFKP enzyme activity or imply therapeutic or clinical benefit. A negative or positive nonselective effect would narrow the proposed explanation of the discordant proteomic results. Other reasons (measurement technology, compartment, donor heterogeneity and RNA–protein discordance) remain possible.

Primary protein finding retained: Guise, Cell Reports (2024), DOI 10.1016/j.celrep.2023.113636, author ALS/control protein contrast −68.1%. Feneberg and Chan smaller negative estimates; Spiteri mostly positive regional estimates; Aly small positive pooled ratios. Do not reinterpret or quantitatively pool these endpoints.

### Newly identified prior evidence: opposite direction in RNA

Manzo et al., eLife (2019), DOI [10.7554/eLife.45114](https://doi.org/10.7554/eLife.45114), reported PFKP RNA +80% in human bulk spinal cord (9 ALS, 8 controls; reported p<0.001), and +58% in an ALS-associated TDP-43 mutant patient-derived iPSC motor-neuron comparison (three differentiations, reported p=0.010). These are author-reported qPCR results, not newly calculated or replicated. Differentiations are not independent donors. Fig. 2 and public source archive: [10.7554/eLife.45114.006](https://doi.org/10.7554/eLife.45114.006), [10.7554/eLife.45114.007](https://doi.org/10.7554/eLife.45114.007). Cohort overlap, assay equivalence and effect intervals not verified. No individual-level source archive downloaded.

This prior result is important counterevidence against a default assumption that PFKP RNA necessarily decreases in ALS. It does not contradict Guise directly: different molecular level, tissue/cell context and cohorts. The proposed novelty is the direct within-donor, between-cell-type **disease-by-cell-type interaction**, not the discovery that PFKP or glycolysis is altered in ALS. A bounded literature check does not certify novelty.

## 2. Source admission (metadata only; no PFKP values inspected in candidate atlases)

| Source | Verified evidence | Decision |
|---|---|---|
| Barretto et al. 2026, preprint DOI 10.64898/2026.07.24.740361; GEO GSE330130 | The paper design section reports 20 lumbar spinal cord donors (11 ALS, 9 controls), 24 motor cortex donors (16 ALS, 8 controls) in single-nucleus multiome. 121,881 QC-passing lumbar nuclei, ten broad classes including annotated motor neurons, other excitatory and inhibitory neurons, glia. Data availability assigns single-nucleus RNA and ATAC to GSE330130. | **Primary candidate, pending.** Need original processed RNA matrix and annotations, non-identifying donor linkage and per-class QC/coverage, licensing, and independent-unit audit. Exact file names, sizes, internal schema and cohort overlap unverified; GEO direct page inaccessible. Preprint is not peer reviewed. |
| Barretto et al., GSE330224 / PRJNA1463185 | Separate spatial assay: 320 Visium libraries, 35 lumbar spinal cord donors and 50 motor cortex donors. GEO lists LSC_VISIUM_COUNTS.h5ad (1.2 GB), MTC_VISIUM_COUNTS.h5ad (3.1 GB) and RAW.tar (9.7 GB). | **Excluded from direct cell-specific primary contrast.** A spot is not an isolated motor neuron; multiple sections are repeated observations. Optional contextual evidence only, not independent from GSE330130 without overlap verification. |
| Zelic et al. 2025, Immunity 58:961–979.e8, DOI 10.1016/j.immuni.2025.02.024; GSE287257 / PRJNA1211983 | Single-nucleus cervical spinal cord: 8 ALS (6 sporadic, 2 familial) and 4 controls, 12 deposited libraries; NCBI lists ~458 MB supplementary data and raw sequencing ~0.27 TB. GEO sample records describe filtered gene-by-barcode H5 matrices. | **Conditional external candidate.** Confirm author cell-type labels (especially motor neurons, not broad neurons), capture adequacy, donor pairing and group map. No raw download or annotation reconstruction. Small cohort may yield imprecise results; poor coverage is not a biological negative. |
| Zelic et al., GSE287256 / PRJNA1211982 | Bulk cervical spinal cord, identical study design (8 ALS and 4 controls), ~2 MB supplementary data. | **Context only**; likely linked cohort, do not count as independent replication. Bulk expression cannot resolve motor-neuron selectivity. |

Cross-source donor overlap is not proven absent. Barretto acknowledges Target ALS/ALS Consortium tissue procurement; Zelic reports NIH brain biobank. Do not conflate different brain banks or accessions with verified independence. No participant identifiers or clinical metadata copied into this report.

Sources (accessed 2026-11-27):
- Barretto et al. preprint, v1 [article](https://www.biorxiv.org/content/10.64898/2026.07.24.740361v1.full), [PubMed](https://pubmed.ncbi.nlm.nih.gov/42619860/). Indexed abstract, design and availability excerpts accessible; direct full-text fetch returned 403 and PMC only archives abstract.
- [GSE330130](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE330130), direct fetch unsuccessful; primary paper identifies accession.
- [GSE330224](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE330224), [BioProject](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1463185), indexed source record and catalogue.
- [GSE287257 BioProject](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1211983), [Zelic article](https://pubmed.ncbi.nlm.nih.gov/40132594/).
- [GSE287256 BioProject](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1211982).
- [Guise article](https://pubmed.ncbi.nlm.nih.gov/38183652/).
- Repository [five-study audit](https://github.com/luisceb1/ela-research/blob/47b7ee619210a0fcc568ec06855393d7f10ee2e0/reports/cross-study-proteomics-audit-20261126/REPORT.md).

## 3. Prospective analysis draft (disabled pending admission)

Primary cohort: GSE330130 lumbar snRNA-seq only. The independent biological unit is the donor, not nuclei, sections, libraries or assay modalities. Source-defined motor-neuron labels must be validated independently of PFKP; other spinal neurons (source excitatory and inhibitory, excluding MN) form the prespecified primary comparator. Glial classes are secondary descriptive comparisons, not alternative primary targets. Cervical GSE287257 is a distinct regional replication attempt only if eligibility and nonoverlap are established; estimate separately.

Primary prediction: ALS/control PFKP expression is lower in MNs and the ALS-control effect is more negative in MNs than other neurons. Primary estimand is the difference between the two diagnosis effects on log2 normalized donor-level RNA expression (interaction). Aggregate counts within donor and class; use one documented method for donor-level library normalization. Retain legitimate zero counts; no imputation of unobserved classes. Never treat nuclei as replicates. Report both component effects and their uncertainty (not merely two separate significance tests). Any covariate adjustment, exact count model, QC thresholds, exclusions, inference procedure and practically relevant effect margin must be fixed in a versioned plan after inspecting schema and target-blind design/precision, before looking at target values. Do not use protein fold change as an RNA threshold. No outcome-dependent changes.

Admission checks, before analysis:
1. Public terms permit use; no personal-data access/storage, controlled access or redistribution without specific authorization. Use a non-identifying, permitted data representation.
2. Verify source version, file sizes/hashes and provenance. Raw RNA counts, source cell annotations, diagnosis class and stable anonymous unit linkage must be documented. Do not use ATAC counts or spatial spots as RNA counts.
3. Inspect numbers of donors with both classes and per-class nuclei/QC counts, independent of PFKP. Verify donor/technical-replicate mapping, pathology grouping, region and cohort overlap. Do not infer pathological TDP-43 loss from ALS diagnosis alone.
4. Establish adequate measurement precision without inspecting the target effect; predefine all minimum donor/class coverage and inclusion rules. No replacement of an unavailable specificity comparison by a bulk comparison.
5. Freeze estimator, normalization, uncertainty method, comparator definitions and stop conditions before extracting target values. Record all exclusions; no threshold chasing.

Decision logic:
- Negative MN effect and negative MN-versus-other-neurons disease interaction with adequate precision and independent regional corroboration: evidence supporting RNA cell-type specificity.
- Negative effects across both MN and other neuronal classes with a sufficiently precise absence of a meaningful interaction: weakens selectivity explanation; cannot infer equivalent protein effects.
- Positive MN RNA effect or sufficiently precise estimate excluding the prespecified meaningful MN RNA decrease: disconfirms directional RNA prediction in tested material.
- Wide intervals, poor recovery of MNs, missing labels, unmatched units or unverified overlap: insufficient for definitive resolution. Preserve null and discrepant estimates.
- Protein-specific answer remains conditional on an independent comparable cell-specific donor-level protein dataset; no RNA-to-protein conversion or inference of metabolic flux.

Survivorship/capture bias, neuronal subtype composition, library normalization, RNA quality and regional difference are explicit limitations. Gene-level nuclear RNA abundance is not cryptic junction usage. No inference of mechanism, enzyme activity, neuronal functional response or clinical outcome.

## 4. Current conclusion and bounded stop

The two candidate atlases are not yet admissible for execution. The strongest enabling input is the original GSE330130 processed RNA/annotation manifest or an author-supplied non-identifying donor-by-cell-type count representation; for GSE287257, recover the original annotation and motor-neuron support documentation. No target count or effect has been extracted from these atlases. The published Manzo RNA finding changes the context and must remain visible, regardless of eventual result.

No new cloud execution, paid acquisition, personal-data collection, communications or public repository/website changes. No quantitative biological analysis was performed. This is a private admission record and prospective draft, not a registered analysis plan or a scientific discovery.
