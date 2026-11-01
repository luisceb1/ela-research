# Keuss source-data gate and multi-target prior art — 2026-11-01

Status: source literature checked, no raw paired data available from supplied PDF artifacts. No quantitative reanalysis performed.

## Keuss source-data search
- KCL accepted/in-press record: https://kclpure.kcl.ac.uk/portal/en/publications/unc13a-splice-correction-rescues-synaptic-dysfunction-induced-by-/ . Record offers a 6.13MB accepted author manuscript, not confirmed separate electronic source-data tables.
- Original preprint: https://pmc.ncbi.nlm.nih.gov/articles/PMC11230273/ ; companion supplement (11pp PDF), provided by user. The previous direct inspection of uploaded PDFs confirmed no embedded source-data attachment or joined replicate-level data table.
- 63pp accepted manuscript author declaration: "Source data is provided with this paper"; stated availability of MATLAB code from JB, LMM R code from PH, ImageJ code from REJ, and an iGluSNFR3 image-analysis pipeline at https://github.com/f-hamidlab/iGluSNFR3 .
- The missing artifact remains **condition-, batch-, dose-, time- and replicate-keyed numerical RNA/protein/function values**. Do not claim impossible access, only not verified in the reviewed publicly available artifacts.
- Crucially Fig. 4 reports nested cells/synapses from 3 experiments and MEA from 4; do not correlate cell-level points with group-level RNA restoration percentages.

## Critical new originality gate
2026 article, DOI 10.1126/scitranslmed.aeb8517, https://pubmed.ncbi.nlm.nih.gov/42234776/ , 'Cryptic splicing in synaptic and membrane excitability genes links TDP-43 loss to neuronal dysfunction' reports KALRN, RAP1GAP, SYT7, KCNQ2 mis-splicing and functional consequences; individual splice-modifying ASOs partly rescue, combined targeting nearly fully rescues synaptic deficits. These results **preempt broad originality claims about multi-target synaptic rescue**. Do not infer that tested combinations include UNC13A or STMN2 without explicit source verification.

## Current falsifiable opportunity / choices
A. Reanalyse one independent dataset with paired transcript or protein and electrophysiological readout **at biological replicate level**; source must contain numeric tables, identifiers and time of intervention.
B. Compare recovery across domains (transmission vs synapse density vs excitability) with distinct endpoints and intervention design; literature mapping first, to avoid rediscovery of published observations.
C. If original paired data cannot be located, send no outreach without user approval. Prepare a narrowly scoped request for per-differentiation RNA/UNC13A protein plus mEPSC/MEA data and accompanying metadata/codes; no patient information sought.

## Next planned source check
- Retrieve full methods/supplement for DOI 10.1126/scitranslmed.aeb8517, inspect explicit combinations used and deposited data.
- Check accession and deposited supplemental files before opening a new analysis branch. Set an explicit no-go if no replication keys.
- Keep PR #30 as exploratory reproduction, and do not merge experimental hypothesis as validated result.

Evidence status: preliminary source-audit only. No new rescue effect estimated.
