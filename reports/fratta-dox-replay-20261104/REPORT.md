# Fratta molecular Dox replay — 2026-11-04

## Result and scope

We reconstructed 42 molecular groups from 138 deposited observations. The pinned public R data-preparation sequence loses six standard errors when its group label is changed before joining tables. Joining on original keys before changing the label preserves all six, without changing means. Actual execution in R 4.4.3/dplyr 1.1.4 confirms the Python reconstruction within 1e-12; see `r-validation.json`, `r-output/` and `EXPERIMENT_TRACE.md`.

This is a computational replay of existing molecular measurements. It is not an independent biological replication, functional rescue, therapeutic threshold or clinical result. The whole Rmd and editorial figure generation were not reproduced. The public code issue does not establish an error in the published figure or its biological conclusions.

The experiment is contextually traced to Brown et al. (2022), Figure 2c, DOI [10.1038/s41586-022-04436-3](https://doi.org/10.1038/s41586-022-04436-3). Exact equivalence to the final Source Data 2 workbook remains unverified because no valid workbook was retrieved. The trace separates documented methods from unresolved CSV-level metadata and records the 2024 correction.

## Provenance and analysis

The source repository is `frattalab/unc13a_cryptic_splicing`, pinned commit `e05e8723e3d18e64c6c559db18de423282511c91`. Only the molecular CSV and figure Rmd were materialized; their sizes, SHA256 and Git blobs were verified. Immutable links are in `sources.json`. The prior plan was committed as `9d61c4da691ab5c4aac34a036a4b8608f190f744`, before calculation; the R trace plan is in commit `3721432cc2817bb9bef8971e0d9467947b9af62f` before R execution.

Grouping uses Treatment/Gene/Line_Group/Color_Group. Means, sample SD and sd/sqrt(row count) reproduce the specified arithmetic. All 42 means were independently checked using rational fractions; a seeded row permutation and second execution preserve outputs. Five transformation tests passed. The original Python-stage receipts `qc.json` and `validation.json` are historical; `trace-validation.json` records current file hashes and `r-validation.json` records the later R execution.

## A. Deposited observations; B. our calculated summaries

The observations belong to the authors. Our calculations give these UNC13A means on the original relative scale:

| Condition | Total RNA | Correct RNA | Protein |
|---|---:|---:|---:|
| NT | 101.00 | 100.33 | 100.03 |
| Dox-1 | 95.00 | 94.00 | 80.53 |
| Dox-2 | 59.33 | 55.33 | 33.17 |
| Dox-3 | 50.33 | 45.33 | 14.33 |
| Dox-4 | 42.33 | 30.67 | 8.03 |
| Dox-5 | 25.33 | 10.00 | 4.30 |

`unc13a-molecular.svg` shows 54 observations and means without inferential intervals. It is a new descriptive plot of published data, not an exact reproduction of the author plot, which omits total UNC13A RNA and includes UNC13B/TDP-43 series. The measurements are not interchangeable; this table alone cannot explain their differences or establish temporal order or significance.

## Join behavior and safeguards

The source removes `13A-RNA`, renames `Correct_RNA` to `RNA` in the means table, then performs an implicit common-column left join with a SEM table retaining `Correct_RNA`. All six correct-RNA groups fail to match. `source-order-join.csv` preserves that behavior; `key-preserving-join.csv` joins before renaming. Actual R results are also preserved separately.

Thirty-six source groups have three rows; six UNC13B protein groups have five. All 16 excess exact-value duplicate rows are retained because identities are unknown. Row-based SEMs are computational summaries, not validated biological uncertainty. No values are deduplicated, paired by row order, divided by zero TDP-43 values, or used for hypothesis tests. Missing experiment/culture identifiers and the mismatch with the declared n remain explicit limitations.

## Reproduction

Fetch only the two immutable originals listed in `sources.json`; the Python script checks their SHA256. From project root:

```bash
python scripts/reproduce_fratta_dox.py --source-csv /path/Protein_RNA_Corr_3.csv --source-rmd /path/paper_figures.Rmd --output /path/replay --plot
python -m unittest discover -s tests -p 'test_fratta_dox_replay.py' -v
Rscript scripts/check_fratta_dox_join.R /path/Protein_RNA_Corr_3.csv /path/r-output
```

Python 3.12.14, standard library for tables, optional Matplotlib 3.10.8/Agg for plotting. R requirements and full session information are preserved in the trace and `r-output/sessionInfo.txt`. No author-era package environment is claimed.

## C. Recommendation

Conclude this molecular replay with a reproducible technical finding and no claim of biological novelty. Keep K26 Fig.4d as the single functional reproduction target, conditional on original numerical data with independent-unit identifiers. Do not expand this CSV into a new inferential project. No merge, external contact, access request or paid service was undertaken. STATE/BACKLOG and parallel work #37/#44/#46/#47 remain untouched.
