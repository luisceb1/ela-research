# Keuss: direct uploaded PDF attachment audit (2026-11-01)

## Source identification and integrity
User supplied manuscript `LossOfTDP_Keuss_GreenAAM(1).pdf` (63 pages, 6,365,279 bytes, SHA-256 `4c0c9e6c0a532dbf62f9630a47f7fb4730c069d7990ccb81a9fd9d1dfa562ef8`) and older preprint supplement `media-1(1).pdf` (11 pages, 3,272,060 bytes, SHA-256 `b5319cef383db704843c17fc4f62c6c95557d663eed08a7b512fdc21a14ae283`). Both inspected via PyMuPDF. The two PDFs have **zero embedded-file attachments**, and neither constitutes a machine-readable per-replicate source-data release.

The 63-page peer-reviewed accepted manuscript contains Fig 1–4, extended figures, methods, ASO tables 1–7 (including Table 6 on page 62). The 11-page older supplement contains extended figures 1–7 and tables 1–4; its contents/version differ from the accepted paper. **Do not join figure numbers across versions**.

## Direct manuscript evidence (PDF pages)
- pp. 7–8 (Fig 2): CRISPR cryptic-exon deletion largely restored mEPSC frequency (~80% recovery stated); synapse density deficit was **not rescued** and mEPSC amplitude had a residual deficit. Fig 2 legend p. 43: mEPSC group sizes 17/22/15/28 cells over 3 experiments, RNA/protein 6 biological measurements over 3 experiments.
- pp. 8–9 (Fig 3): 21nt and 18nt MOE ASOs yielded >90% correction of correct splicing, protein rescued ~30–50% or >50% depending formulation and cell model; Figure 3 readouts RNA/protein usually 5–6 biological replicates over 3 experiments. In reporter mice, spinal cord splicing is partially corrected; **not animal behavioral rescue**.
- pp. 9–10 (Fig 4): M18-17 and M21-4 rescued spontaneous mEPSC frequency; evoked eEPSC response partly rescued in cortical-like neurons and spinal motor neurons; remaining synapses increased release probability, while active synapse count and synapse density failed rescue. Early DIV14 and late DIV33 depletion show different network synchrony rescue; this is not a longitudinal treatment delay randomized at clinical symptom onset.
- Fig 4 legend PDF p. 45: mEPSC 19/19 and 17/18 cells, evoked cortical 11/6/6 cells, spinal motor 34/30/25 cells, synaptic release probability 285/71/66 synapses, each from 3 experiments; MEA network synchrony from 4 experiments. Cells/synapses are nested technical units; not independent biological replicate totals.
- Statistical Methods manuscript p. 35: per-batch mixed-effect models with batch random intercept, log1p transformation; confirm model diagnostics and inference before attempting numerical reconstruction.
- Manuscript p. 36: "Source data is provided with this paper"; code availability specifies MATLAB electrophysiology JB, R LMM PH, ImageJ REJ, iGluSNFR3 pipeline https://github.com/f-hamidlab/iGluSNFR3 .
- Supplement older 11pp: supplementary figures and tables only; no per-experiment molecular/function matchable table found.

## Critical interpretations and limitations
1. Author experiments provide strong proof-of-principle that UNC13A cryptic splicing contributes to presynaptic dysfunction after TDP-43 depletion in induced neuronal models; **not evidence of clinical therapeutic efficacy**.
2. The authors show dissociation between functional restoration of remaining synapses and restoration of synapse density. This is a **published finding**, not our original discovery.
3. Evidence for a precise protein threshold (~30%) is **suggestive, not established dose-response threshold**; distinct ASOs / assays are not matched quantitative replicate pairs.
4. No verified joined RNA/protein/mEPSC/eEPSC observations by experiment/batch/dose/time in the provided PDFs. A correlation, mediation or lag analysis would be pseudoreplication or ecological inference.
5. Some newer experiments (eEPSC, iGluSNFR3, adult-stage DIV33 synchrony) are absent from the older supplement; maintain strict versioning.
6. The KCL accepted manuscript contains licensing/usage notes: keep uploaded PDFs private, don't commit them to GitHub. Store only document hash, manually authored summaries and links.

## Next gate: explicit search for electronic source data
- Check definitive published Nature article page and online source-data files/figures; verify whether Excel/CSV individual source data actually exist.
- Obtain replicate-, assay-, condition-, batch-, time- and dose-keyed table before promising molecular-to-function regression. If not open, prepare data availability request, **do not send without user's specific permission**.
- If unavailable, choose an independent, publicly downloadable assay dataset where molecular and function readouts share experimental replicate IDs; avoid extending repeated postmortem observational analysis.
