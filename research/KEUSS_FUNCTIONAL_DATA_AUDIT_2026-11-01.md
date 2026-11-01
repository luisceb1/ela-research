# Keuss UNC13A functional-rescue data-access audit
Date: 2026-11-01. Status: initial source-level audit; no numerical replication.

## Evidence confirmed
- Keuss et al., accepted Nature 2026-10-06, manuscript repository at https://kclpure.kcl.ac.uk/portal/en/publications/unc13a-splice-correction-rescues-synaptic-dysfunction-induced-by-/ . Author accepted manuscript is linked as CC BY (6.13 MB); abstract reports restoration of spontaneous and evoked synaptic release, single-synapse release probability and network synchrony in human neuronal models. **This is a manuscript, NOT a verified spreadsheet of biological replicate measurements.**
- Earlier Keuss et al. 2024 bioRxiv, doi:10.1101/2024.06.20.599684, open article https://pmc.ncbi.nlm.nih.gov/articles/PMC11230273/ . Data availability says 'Source data is provided with this paper'; visible supplementary material is a PDF (3.1 MB). MATLAB electrophysiology code is available from JB, rather than a publicly verified GitHub archive.
- In 2024 article Fig. 3, RNA/splicing rescue, protein rescue and electrophysiology are compared across biological conditions, but **not shown as verified paired per-differentiation RNA and mEPSC measurements**. Fig. 3d reports n=17,22,15,28 neurons by condition pooled from 3 experiments, and network synchrony n=24 wells from 4 experiments; neurons and wells are nested, not equivalent to n independent differentiations.
- ASO treatments reported >90% splicing rescue, protein restoration approx. 30-50% (some >50% formulations); synaptic mEPSC frequency rescue documented. These are **group-level published results**, not individual observation-level pairs. Fig. 4 and extended figures require direct source-data inspection before extracting effect sizes.
- Mehta et al. 2025 tU7 splice intervention https://pmc.ncbi.nlm.nih.gov/articles/PMC12697360/: RNA/protein n=3 biological replicates, mEPSC frequency measured from 17 and 22 cells pooled from 3 experiments; published paper does not itself establish paired differentiation-level RNA/function records.

## Source access inventory
| Resource | Available verified? | Quantitative raw table linked? | Decision |
|---|---|---|---|
| Keuss Nature 2026 accepted author manuscript | Yes, linked on KCL repository | **Not verified** | Read methods, figure labels and source-data links |
| Keuss 2024 manuscript full text | Yes, PMC open | **Not verified** | Define condition/replicate key for matched datasets |
| Keuss 2024 Supplement 1 PDF (3.1 MB) | Yes, linked from PMC | **No machine-readable per-biological-replicate data verified** | Extract methodology only; do not digitize panels as biological pairs |
| MATLAB electrophysiology analysis code | Authors state available from JB | No public repository verified | Request code/data only with explicit user authorization |
| Mehta tU7 2025 | Yes, PMC open | Paired molecular/function by biological replicate **not verified** | Secondary fallback after data access gate |

## Falsifiable analysis requirement
The estimand **cannot** be a numerical correlation between RNA correction and synaptic function unless both measurements are linked to the same independent biological differentiation/repeat with condition, dose, timing and batch identifiers. A plot's cell-level n does not make paired replicate data available. If unavailable, limit analysis to reproducibility of authors' group-level outcomes with appropriate caveats, and report missing data explicitly.

## Next executable steps
1. Download the published accepted manuscript, preprint supplement and any source-data attachment (if present); hash, index filenames and check access/licence. Do not commit large third-party files to git.
2. Build a figure-to-assay-to-unit matrix: RNA assay, protein assay, release, mEPSC, network synchrony, each with biological n, technical n, controls, interventions and time points.
3. Inspect whether any attachment contains machine-readable per-differentiation measurements with join keys. Mark YES only after reading the data columns; otherwise NO/UNKNOWN.
4. If joinable, pre-specify one endpoint (e.g. change in mEPSC frequency per differentiation) and a design-aware analysis. If not, stop the correlation project and prepare a precise data-request draft **without sending**.
5. Contrast accepted 2026 manuscript versus 2024 preprint for newly added evoked release and spinal motor-neuron experiments; do not conflate versions.

## Claims explicitly not supported
- Quantitative restoration percentage per dose across independently matched biological replicates.
- A lead/lag relationship between molecular and functional rescue.
- In vivo efficacy in ALS patients or translation to a clinical therapy.
- Original discovery of UNC13A splice-based synaptic rescue.
