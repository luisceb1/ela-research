# Functional rescue data gate — UNC13A versus STMN2
Date: 2026-11-01
Status: SOURCE AUDIT; public preprint XML retrieved, no numerical functional dataset or effect analysis. See reports/functional-source-access-20261101.

## Central falsifiable question
In human TDP-43-deficient neurons, to what extent does molecular rescue of UNC13A or STMN2 precede and predict functional recovery, after controlling for intervention timing and independent biological replicate?

**IMPORTANT: The literature already demonstrates rescue, so do not claim that rescue itself is novel.** A novel contribution would require newly testable *quantitative generalization*, such as timing, lag, dose-response coupling or joint impact of distinct interventions. This is a proposed question, NOT established novelty.

## Initial source matrix (verify primary figure and supplemental files)
| Study | Intervention / model | Reported functional endpoint | Data access finding | Gate |
|---|---|---|---|---|
| Keuss et al., accepted Nature 6 Oct 2026, https://kclpure.kcl.ac.uk/portal/en/publications/unc13a-splice-correction-rescues-synaptic-dysfunction-induced-by-/ | Splice-switching ASO correction of UNC13A in TDP-43 depleted human cortical and motor neurons, humanized mouse | Spontaneous/evoked vesicle release, synaptic release probability, network synchrony | Accepted author manuscript linked publicly. A matched per-biological-replicate splicing/function table **not yet verified** | First-choice source audit |
| Keuss et al., bioRxiv 2024, doi:10.1101/2024.06.20.599684, https://pmc.ncbi.nlm.nih.gov/articles/PMC11230273/ | UNC13A splice-switching rescue | Synaptic transmission and network synchrony | Paper reports source data, MATLAB electrophysiology code available *from author*; do not assume underlying paired raw data is public | Search source data/figure supplements |
| Baughn et al., Science 2023, doi:10.1126/science.abq5622, https://pmc.ncbi.nlm.nih.gov/articles/PMC10148063/ | dCasRx/ASO STMN2 correction in TDP-43-deficient human motor neurons | Axon regeneration; lysosomal trafficking | Manuscript full text public, paired raw measurements/accessions not verified | Reference arm, not direct comparability assumption |
| Mehta et al., bioRxiv 2025, doi:10.1101/2025.11.26.690143, https://pmc.ncbi.nlm.nih.gov/articles/PMC12697360/ | tU7 splice-switching UNC13A/STMN2 in neurons | mEPSC and protein/synaptic localization rescue; RNA correction | Supplemental PDF available; paper gives biological n=3 for RNA/protein and cell-level electrophysiology counts but paired per-differentiation raw data not verified | Secondary candidate; avoid cell-level pseudoreplication |

## Go / no-go criteria for quantitative functional reanalysis
1. For separate functional-outcome reproduction: source data must include intervention group, TDP-43 status, experimental unit/batch, dosing/timing, functional value and units. Molecular measurements and an explicit cross-assay link are additionally required only for molecular–functional coupling; sister cultures may be eligible if the design documents the relationship.
2. **Linkage**: RNA and function must be paired at appropriate biological replicate level to infer cross-readout coupling. If only aggregate graphs are published, can reproduce descriptive plotted effects but must NOT claim molecular-to-functional correlation or time ordering.
3. Controls must include no TDP-43 depletion, TDP-43 depletion plus non-targeting treatment, and TDP-43 depletion plus active correction, or state explicitly which is missing.
4. Source data must enable proper design-aware uncertainty intervals; cells/synapses nested within differentiations are not independent n.
5. Predefine outcome measure and comparison *before* examining raw arrays. For UNC13A choose evoked vesicle release probability (if matched data exist) or mEPSC frequency when available; for STMN2 choose axonal regeneration endpoint. **Different endpoints cannot be numerically equated without explicit bridge model.**
6. If missing matched data, do not digitize plots as though values were raw pairs; document blockage and request access through a separately authorized communication.
7. Reuse source manifests, stable DOI, version, SHA-256, processing code and no patient-level private data in Git.

## Immediate execution plan
- Read Keuss accepted manuscript, specific figures and supplementary/source data availability; locate any machine-readable individual replicate data and report links, file sizes, licences.
- Compare Mehta and Baughn source-data material on whether paired molecular + functional observations are present.
- Only then choose ONE public dataset, build data dictionary, frozen protocol, and replication scripts/tests.
- If no open paired material exists, next approved deliverable is a transparent missing-data access matrix, not invented effect estimates.

## Relationship to merged PR #30
This research question is a **new independent intervention-analysis workstream**. Keep PR #30 (RiMOD+NYGC targeted observational splicing) scoped to original claims, provenance and QC. Avoid reusing observational bulk-tissue effects as intervention outcomes.


## Current access decision — 01/11/2026
PR #30 merged in 39e0479. The bounded two-family access audit is closed: reports/functional-source-access-20261101. No numeric source accepted; no molecular/function correlation or post-deficit treatment effect estimated. Review the existing unsent request specification; do not repeat completed index/PDF searches without a concrete new source. This is an access limitation, not evidence that biological replicates are dependent or source files do not exist.
