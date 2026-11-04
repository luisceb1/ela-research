# Molecular Dox experiment: provenance audit — 2026-11-04

## A. Primary literature

Brown et al. (2022), *TDP-43 loss and ALS-risk SNPs drive mis-splicing and depletion of UNC13A*, Nature 603:131–137, published 23 February 2022, DOI [10.1038/s41586-022-04436-3](https://doi.org/10.1038/s41586-022-04436-3), [full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC8891020/).

Figure 2c reports RNA/protein dose-response measurements in SH-SY5Y cells with doxycycline-inducible TDP-43 shRNA, declaring three biological replicates and mean ± SEM. Methods describe clonal expansion and concentrations 12.5, 18.75, 21, 25 and 75 ng/ml. The general depletion protocol lasts three days followed by seven days in neuronal medium. RT-qPCR uses ΔΔCt; Western intensities use ImageJ. Extended Data 3f includes tubulin controls. Supplementary Figure 1 describes UNC13A on a separate membrane from UNC13B, TDP-43 and tubulin.

The [18 June 2024 Author Correction](https://doi.org/10.1038/s41586-024-07577-9), Nature 631:E7, corrects another cell-line designation from SK-N-DZ to SK-N-BE(2). It does not identify the Dox-table join problem or change SH-SY5Y to that other model.

## B. Traceability assessment by our project

| Item | Evidence and status | Consequence |
|---|---|---|
| Panel attribution | Public Rmd heading at L3779 and series match the subject of Fig.2c; final Figure 2 image inspected | Strong contextual attribution; exact numeric equivalence to editorial source data remains unverified |
| Perturbation | Induced TDP-43 knockdown, rather than a corrective intervention | Neither prevention nor recovery is tested by this CSV |
| Dox labels | CSV has NT and Dox-1…5; Rmd specifies order but no numeric dose key | Do not assign the five listed concentrations to individual labels |
| Timing | General method available; no per-row schedule | Do not certify ten days for each CSV observation |
| Normalization | NT is approximately 100; exact per-series denominator and construction of “Correct RNA” not recovered | Retain original relative scale; no absolute concentrations or reconstructed ΔΔCt |
| Independent units | Caption declares n=3; no experiment/culture/replicate identifiers in CSV | Three rows do not establish three independent units by themselves |
| Count discrepancy | UNC13B protein has five rows per condition; other series have three | Unresolved mismatch with caption; retain all rows, no arbitrary trimming |
| RNA/protein pairing | No shared sample IDs or blot identifiers | No paired tests or row-order correlations; membrane information does not resolve sample pairing |
| Exact duplicates | 16 excess identical-value rows retained | Cannot distinguish legitimate repeated values from duplicate records |
| Functional endpoint | No electrophysiology, synaptic assay or rescue arm in this table | No inference about restoration of neuronal function or clinical benefit |

The issue is incomplete metadata, not demonstrated pseudoreplication. The missing identifiers prevent adjudicating independence. Other CSVs inspected by header belong to different experiments and cannot supply these identifiers.

## Actual R execution

[Run 41874295175](https://github.com/luisceb1/ela-research/actions/runs/41874295175), job 126729394580, succeeded using R 4.4.3/dplyr 1.1.4. The original data-preparation sequence and a join-before-renaming comparator were executed; both match the Python means and row-based SEMs within 1e-12. Original sequence: six missing SEMs out of 36 plot groups. Comparator: zero; means unchanged. This verifies the pinned public code behavior, not which code generated the final editorial figure. No full Rmd, ggplot rendering or author-era environment was reproduced.

`r-output/` preserves all five downloaded artifact files, including sessionInfo, beyond the seven-day Actions retention. ZIP SHA256 and run identity are recorded in `r-validation.json`. The temporary workflow is removed after execution; its exact configuration remains in commit 3721432cc2817bb9bef8971e0d9467947b9af62f. To repeat from project root, install R 4.4.3 and dplyr 1.1.4 (Posit snapshot 2025-06-01), fetch the hash-verified original CSV, then run:

```bash
Rscript scripts/check_fratta_dox_join.R /path/Protein_RNA_Corr_3.csv /path/output
```

## Unavailable source data and failed access

Figure 2 advertises `41586_2022_4436_MOESM16_ESM.xlsx` (~2.2 MB). No valid workbook was retrieved. PMC returned an HTML challenge; encoded and unencoded Springer CDN requests returned HTTP 503; Europe PMC returned 403. Requests were bounded to 3 MiB. Thus no workbook hash, sheet inspection, dose key or exact published-value comparison is claimed. The source URL is in `sources.json`.

Local R was unavailable and apt failed on UID/GID permissions; no escalation was attempted. Scite required a paid plan/trial and returned no usable evidence; no purchase was made. Primary text, figure and code were used directly. These access failures do not imply that the data do not exist.

## C. Decision and stopping rule

Close this bounded molecular replay as a technical/descriptive result. It supplies no new biological mechanism and no justified therapeutic threshold. Resume the single functional target K26 Fig.4d only when original numeric data and cell/differentiation identifiers are available. If Source Data 2 later becomes accessible, resolve label/count/normalization discrepancies before any inferential use. No new contact, access request, clinical claim or independent experimental replication is authorized by this audit.
