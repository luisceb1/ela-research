# UNC13A: originality, methods comparison, and next experiment gate
Date: 2026-11-01. Status: comparative desk review, not a new scientific discovery.

## Findings and precedence

| Work | Prior result in scope | Implication for our project |
|---|---|---|
| Ma et al., Nature (2022), doi:10.1038/s41586-022-04424-7 | UNC13A cryptic exon associated with TDP-43 dysfunction; NYGC interrogation of 1,151 tissues / 413 individuals, multiple tissues/person, and orthogonal FTLD material. Included negative controls, genotype groups and brain regional comparisons. | Our NYGC nonzero splice-junction count and ALS-TDP/control comparison are **not novel**. Do not equate our larger reprocessed cohort with an independent external cohort. |
| Brown et al., bioRxiv preprint (2025), doi:10.1101/2025.11.23.689722 | TDP-43 cryptic exon responsiveness, degradation and regional burden; released NYGC/RiMOD LeafCutter parquets at Zenodo record 15977268 and code at frattalab/cryptic_biology. | This is the direct source of both our numeric matrices and primary metadata. Reprocessing them adds no biological independence. |
| NYGC consortium resource and related analyses | More RNA-seq datasets, multi-tissue and donor heterogeneity; specific thresholding can determine whether an event is called. | Quantify a precise method effect only after identifying and quoting its exact source/filters; otherwise a hypothetical comparison, **not** a published disagreement. |

Sources:
- https://www.nature.com/articles/s41586-022-04424-7
- https://pmc.ncbi.nlm.nih.gov/articles/PMC8891019/
- https://pmc.ncbi.nlm.nih.gov/articles/PMC12667841/
- https://zenodo.org/records/15977268
- https://github.com/frattalab/cryptic_biology

## Cross-check of local project evidence (user-executed; not rerun here)

RiMOD 47 samples, UNC13A cluster clu_46643_-: canonical 7074 counts, novel_donor 80, novel_acceptor 53, alternate long 23; control+MAPT 27/27 no >0 cryptic, C9orf72+GRN 16/20 donor-junction positive. NYGC aggregate: 2476 sample IDs with target records in 3548 parquet archive; 153 donor-junction positive, 129 acceptor-junction positive. NYGC metadata: 2551 rows, 2421 distinct sample IDs; 130 redundant rows with consistent critical fields, 313 parquet sample IDs without metadata match, 637 nonempty unique subject IDs among matched samples across tissues. NYGC motor-cortex donor-dedup maximum local depth: 313 ALS-TDP donors, 48 controls; at local depth>=100 26/244 ALS-TDP and 0/38 control donors positive for donor-junction. These are *descriptive results from user's local execution*, not independently verified here.

## Scientific originality assessment

1. Novel UNC13A-TDP43 molecular association? **NO** (Ma 2022).
2. Novel appearance in NYGC ALS-TDP? **NO** (Ma 2022).
3. Novel interpretation of Brown NYGC/RiMOD junction catalogue? **NO**, source-derived data.
4. Reproducible donor-aware targeted extraction and explicit negative/missingness accounting? **Potential technical deliverable**, but originality relative to prior methods unverified.
5. Claimed discrepancy with other NYGC studies? **NOT ESTABLISHED** until exact cohort, library processing, junction definitions, threshold and denominator harmonized.

## Locked prospective next experiment / go-no-go

**Question**: How much of targeted UNC13A novel_donor detection in NYGC motor cortex depends on single-donor sampling and prespecified local-depth/read-count thresholds?

- Eligible units: motor-cortex donor IDs with exactly one selected sample per subject; phenotypes ALS-TDP vs Control as metadata *labels*, not proof of tissue pathology.
- Select representative sample by highest `cluster_count` at UNC13A among available motor-cortex libraries (tie: lexical sample ID), blinded to cryptic outcome. Explicit selection-bias limitation.
- Primary endpoint: proportion of donor representatives with `junction_count>=1` at `chr19:17641556-17642414`, restrict to cluster depth>=100. Report numerator/denominator plus Wilson 95% confidence interval as descriptive sampling uncertainty, NOT clinical diagnostic sensitivity or specificity.
- Secondary/sensitivity: junction_count>=3 and >=5; novel_acceptor separately; cluster depth>=50; RIN categories (<6.5, 6.5-<7.5, >=7.5, missing), check library size and batch. Treat all as exploratory, avoid selective p-value fishing.
- Missingness gate: enumerate 313 unmatched Parquet sample IDs by prefix/source *only after privacy/metadata requirements*; do not impute case/control.
- Nonindependence gate: verify unique physical donors across RiMOD and NYGC and reused libraries across papers. If overlap cannot be resolved, label dataset relationships unknown.
- Literature methods comparison: record exact sample count, tissue subset, junction/reference, CE detection rule, depth and number of donors used by Ma and Brown; cite original figure/supplement, distinguish reported vs not specified.
- Decision: if technical thresholds fully explain the event detection variation and prior literature has not examined exact combination, write methods note; otherwise mark this reproduction complete and prioritize genuinely independent biological dataset / causal intervention with STMN2+UNC13A.

## Review/merge recommendation

Do NOT merge PR #30 as a validated new scientific result. Keep reproducibility scripts and tests in a distinct branch, add a source-pinned reference inventory, then peer-review code and data provenance. If merged later, title as "exploratory public-dataset reproduction" and clearly flag untested clinical interpretation. No publication/claims of novelty until external methodological review.
