<!-- Working record from the completed 27 November cycle, authorized for public archival release. Statements about no publication/repository changes describe the original analysis step. Only aggregate results and reproducibility details are included. -->

# PFKP in human spinal neuronal populations — Takeuchi source-statistics audit

**27 November 2026** — internal scientific working record; not a publication.
Question: Does independent human spinal neuronal RNA evidence support the proposed selective decline in PFKP? This is a documentary/numerical extraction of published group-level statistics, not a new donor-level fit or reproduction of the paper's statistical model.

## 1. GSE287257 admission decision

GSE287257 (Zelic et al., Immunity 2025, DOI 10.1016/j.immuni.2025.02.024; PRJNA1211983) reports cervical spinal cords from 8 ALS donors and 4 controls. The official [supplement directory](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE287nnn/GSE287257/suppl/) and [file list](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE287nnn/GSE287257/suppl/filelist.txt) were accessed. The deposited TAR is 480,081,920 bytes and lists exactly 12 filtered feature-by-barcode H5 matrices, one per sample. No separate author annotation file is listed in that archive. The existence of a public Sanofi/BioTuring exploratory browser was reported by the study authors, but export of labels and motor-neuron coverage are not verified. Therefore GSE287257 remains pending; do not infer that the dataset lacks motor neurons or that labels cannot be obtained elsewhere. No TAR or raw sequences downloaded. Do not substitute a broad neuron cluster for motor neurons.

## 2. Alternative, genuinely distinct publication

Takeuchi et al., [Brain 149:2480–2494 (2026)](https://doi.org/10.1093/brain/awaf426), first online 11 Nov 2025, describes single-nucleus multiome profiling in motor cortex and lumbar spinal cord of six sporadic ALS and six control donors. The paper reports 62,711 spinal nuclei and explicitly acknowledges low motor-neuron yield. The paper reports DESeq2 pseudobulk analysis with age and sex as covariates; its reported differential selection criterion is adjusted p<0.2. The [public code](https://github.com/ertakeuchi/ALS_project/blob/main/code/analysis/DESeq2.R) aggregates raw RNA counts by fine cluster and SubjectID, sets HC as reference, uses age, sex and group in a DESeq2 design, and calls lfcShrink. Exact executed code, coefficient/SE relationship and number of contributing donors for each aggregate table have not been independently verified. Do not infer that 6+6 subjects contribute to every cell type.

[Author data deposit](https://doi.org/10.6084/m9.figshare.29628653), version 1, CC BY 4.0. This provides full published differential results per class. The source distinguishes published aggregate Wald CSVs from multi-gigabyte RDS objects and controlled raw reads. Only four aggregate CSVs were retrieved. No person-level information accessed for the new source. Non-overlap with prior tissue cohorts remains unverified.

## 3. Fixed scope before reading PFKP rows

Plan written before extracting any target values, SHA-256:
`d4a921a10d0a8a9a3b7f41b35b2a5fd68c3cab7b8dbfb6ed328f740c3f70827c`.

> Scope: author aggregate DESeq2 ALS vs HC Wald tables, figshare v1 29628653. Extract PFKP exact gene symbol only, all three broad spinal neuronal populations (MN, EX, INH), plus MN_1 subtype as same-cohort descriptive reconciliation, not independent replication. No other targets, no model fitting, no new thresholds. Verify file lengths and MD5 against figshare, inspect schema, exact unique row, report original baseMean/log2FC/SE/stat/p/padj when available and transform log2FC to relative ratio descriptively. If no exact match retain missing; no substitution by alias without identifier cross-check. Compare directions descriptively only; no formal cell-type interaction, donor coverage not verified. Author padj threshold 0.2 retained as source reporting criterion and exact adjusted p-values shown. No conversion to protein effects or clinical inference.

## 4. Extracted results

All four files have exactly one PFKP gene-symbol match. Headers: gene, baseMean, log2FoldChange, lfcSE, pvalue, padj. No stat column. Relative change is arithmetic only: 100 × (2^log2FoldChange − 1).

| Author source class | baseMean | log2FoldChange | lfcSE | pvalue | padj | Relative change |
|---|---:|---:|---:|---:|---:|---:|
| spinalcord_MN_neurons | 17.3180272723 | −0.0515598012 | 0.2658147020 | 0.5322163274 | 0.9999373234 | −3.510745% |
| spinalcord_EX_neurons | 131.4879403495 | +0.0000062016 | 0.0014426762 | 0.1520798557 | 0.9998368089 | +0.000429862% |
| spinalcord_INH_neurons | 62.0566419443 | +0.0000052962 | 0.0014426720 | 0.2379286734 | 0.9998846026 | +0.000367102% |
| sc_MN_1 (same cohort) | 17.3180272723 | −0.0544469896 | 0.2731400378 | 0.5319897787 | 0.7669546519 | −3.703651% |

The estimated contrast is slightly more negative in MN compared with the other two broad neuronal groups, whose exported shrunken estimates are near zero. Both MN tables have the same baseMean and similar estimates; do not count them as two confirmations. None meets even the source's relatively permissive adjusted-p criterion (0.2). Author code calls shrinkage; exported effect/SE and p-value may refer to different inferential stages, so no confidence interval, Wald reconstruction, equivalence claim or test of contrasts between cell types is computed from these summary values. No assumption that near-zero estimates imply normal biological expression.

## 5. Reconciliation with project evidence

- Guise reported −68.1% protein in human isolated spinal MNs. Takeuchi's −3.51% estimate is nuclear RNA in a separate study, not quantitative protein replication.
- Manzo reported positive RNA estimates in bulk spinal cord (+80%) and iPSC-derived MNs (+58%). Takeuchi's small negative point estimate does not support a large, consistent direction/magnitude across different RNA contexts.
- Previous GSE330130 analysis was closed without target inspection because 95.1% of its captured control MNs came from one donor. Takeuchi admits an **aggregate source-statistics audit** only; it does not remove the donor-coverage gate for a new cell-type interaction analysis.

**Decision:** current human spinal MN RNA summary evidence does not establish a selective PFKP reduction. The weak negative point estimate is recorded without claiming an absence of effect or mechanism. A formal disease-by-cell-type interaction needs comparable donor-level expression, coverage and independent-unit verification. The Guise protein association remains unresolved rather than refuted.

## 6. Reproducible provenance

All four files downloaded from author deposit; sizes and MD5 verified against figshare API v2 entry 29628653 (version 1), SHA-256 calculated locally on original bytes.

| Filename | Figshare file ID | Bytes | MD5 | SHA-256 |
|---|---:|---:|---|---|
| sc_MN_1_ALS_vs_HC_Wald_all_genes.csv | 56556602 | 1829838 | ec4a8ed5959157b73b21ccf22ec81c04 | fe08714464b2bbf6d416594579460e06a37e61ecb916ff271dde089f76b456d4 |
| spinalcord_MN_neurons_ALS_vs_HC_Wald_all_genes.csv | 56556680 | 2510853 | 613bd696f6aff69aa4c68203e34b89cb | 5eab96f9d0d6e760dce8db21fcb3bd103f61acecfdcdcf2cb181123570c837d0 |
| spinalcord_INH_neurons_ALS_vs_HC_Wald_all_genes.csv | 56556698 | 3180417 | 511448c1b98b03b2bd37fe5d12f3a9e9 | 3937b84f20fd6896fc310526047b91924b55f9f0a194e35a3d4b2c13e28ad5ee |
| spinalcord_EX_neurons_ALS_vs_HC_Wald_all_genes.csv | 56556701 | 3198941 | 698634c9501324542ea9f9388fc66f4d | 89cabd61b742645b1eed1b0822fea069b0756d85f2a09414eb3ce7a380a36b12 |

Sum: 10,720,049 bytes. Row counts: 22,542 fine MN; 31,944 each broad population. File download endpoints as provided by figshare: https://ndownloader.figshare.com/files/{file_id}. Python/pandas extraction:

```python
import pandas as pd
from pathlib import Path

names = [
    "spinalcord_MN_neurons_ALS_vs_HC_Wald_all_genes.csv",
    "spinalcord_EX_neurons_ALS_vs_HC_Wald_all_genes.csv",
    "spinalcord_INH_neurons_ALS_vs_HC_Wald_all_genes.csv",
    "sc_MN_1_ALS_vs_HC_Wald_all_genes.csv",
]
for name in names:
    df = pd.read_csv(Path(name), keep_default_na=True)
    assert {"gene", "baseMean", "log2FoldChange", "lfcSE",
            "pvalue", "padj"} <= set(df.columns)
    row = df[df.gene.eq("PFKP")]
    assert len(row) == 1
    v = row.iloc[0]
    print(name, len(df), v.to_json(),
          100*(2**v.log2FoldChange-1))
```

## 7. Next discriminating route

A separate RNA-abundance question could be assessed using directly laser-captured human spinal motor neurons (Krach et al., GSE76220 / PRJNA306659; paper DOI and sample-level mapping to be verified). GEO describes 13 sporadic ALS and 9 controls, but deposits 21 samples; the discrepancy requires reconciliation. This dataset cannot by itself establish a within-donor cell-type-specific interaction if it contains only motor neurons. No target values or new donor files were accessed. Do not reopen previous failed junction-count cycles merely because an accession is available.

No expenditures, cloud execution, contact, public repository modifications, or new biological inference beyond the source comparisons.
