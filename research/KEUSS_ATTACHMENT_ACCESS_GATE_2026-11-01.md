# Keuss primary attachment access verification — 2026-11-01

**Disposition:** no analyzable paired raw data verified. Source files are reachable as *links* but their contents have NOT been examined in this run. No molecular/functional correlation may be computed.

## Checked links and observed access
- Keuss 2024 preprint (PMC11230273): https://pmc.ncbi.nlm.nih.gov/articles/PMC11230273/ . Associated Data lists **Supplement 1, media-1.pdf, 3.1 MB**, at https://pmc.ncbi.nlm.nih.gov/articles/instance/11230273/bin/media-1.pdf . Browser-retrieval attempt returned a browser/reCAPTCHA gate; NOT proof that the PDF is unavailable to a human browser.
- Keuss 2026 accepted Nature author manuscript, KCL repository: https://kclpure.kcl.ac.uk/portal/en/publications/unc13a-splice-correction-rescues-synaptic-dysfunction-induced-by-/ . Attachment link https://kclpure.kcl.ac.uk/portal/files/391373721/LossOfTDP_Keuss_GreenAAM.pdf (6.13 MB, CC BY). Automated fetch returned HTTP 403; not inspected.
- 2024 preprint 'Data availability': "Source data is provided with this paper." Public PMC listing only exposes PDF supplement; no Excel/CSV data attachment was verified through this listing.
- 2024 preprint 'Code availability': authors state MATLAB electrophysiology analysis code available from JB; this is NOT a verified publicly downloadable package.

## Replication units in accessible text
- Keuss 2024 Fig 3d mEPSC: n=17, 22, 15 and 28 individual iNeurons in the four conditions **pooled from 3 experiments**.
- Fig 3f network synchrony: 24 wells **from 4 experiments**.
- Fig 3b UNC13A synaptic intensity: 71,71,66,75 synapses **from 3 experiments**.
- These are cells/synapses/wells nested in independent experiment batches; do not take per-neuron n as independent biological n.
- Fig 4 ASOs rescue UNC13A splicing and protein, and mEPSC frequency; no verified *per-differentiation join key* between RNA rescue, protein rescue and electrophysiological output.

## Explicitly unresolved
1. Does the accepted 2026 manuscript provide electronic source data separate from manuscript PDF?
2. Does the 2024 supplement contain numeric source data or only supplement figures/methods?
3. Are RNA and electrophysiological measurements **paired by experiment, dose and time**?
4. Biological replicate definition, original recordings, units and uncertainty model.
5. Conditions used in later accepted manuscript versus earlier 2024 preprint.

## Local retrieval path (do not commit copyrighted source binaries)
Download each PDF in a normal browser if permitted, store under ignored `data/external/keuss/`, generate SHA256 via PowerShell `Get-FileHash`; share filenames or attach PDFs to chat for content audit. Only then label contents VERIFIED. If paired data are unavailable, prepare a *draft* data request to corresponding authors; do not send without user approval.

**Interpretation:** already published functional rescue is meaningful biological evidence, but available webpage text is not sufficient to reconstruct a new quantitative molecular-to-function effect relationship. No original inference or independent rescue experiment completed.
