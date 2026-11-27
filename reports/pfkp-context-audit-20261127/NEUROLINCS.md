<!-- Working record from the completed 27 November cycle, authorized for public archival release. Statements about no publication/repository changes describe the original analysis step. Only aggregate results and reproducibility details are included. -->

# PFKP RNA/protein concordance in a C9orf72 ALS iPSC-derived neuronal cohort

27 November 2026 — internal working record, not published. This is a numerical extraction of author-reported aggregate effects, not a new fitted model or individual-level multimodal correlation.

## Question

Do PFKP RNA and protein abundance estimates have concordant direction in a study that measures both modalities in the same experimental cohort? This discriminates an assumption of obligatory RNA--protein discordance from study-specific/context-specific effects, without purporting to resolve Guise's postmortem motor-neuron protein observation.

## Source selection and access

NeuroLINCS et al., iScience 24:103221 (2021), [DOI](https://doi.org/10.1016/j.isci.2021.103221), [PMC8554488](https://pmc.ncbi.nlm.nih.gov/articles/PMC8554488). The study describes parallel neuronal cultures, with RNA-seq and proteomics measured on material from the same donor-derived cultures. The independent replication cohort consists of six C9orf72 ALS patients and seven controls, distinct from the original cohort according to the article. Its diMN cultures were assessed at day 18; composition is not pure MN and one motor-neuron marker's proportion differed between groups. A cohort labelled replication by the authors is not automatically a replication of PFKP; original cohort PFKP protein contrast not identified in the inspected complete source summaries.

The official supplementary package at https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8554488/supplementaryFiles was retrieved after direct publisher delivery returned 403 and PMC direct downloads returned HTML. Extracted only the two relevant aggregate workbooks, no individual expression/genetic data inspected. Files:

| File | Bytes | SHA-256 |
|---|---:|---|
| mmc2.xlsx, Table S9 | 12,500,936 | 41a0f1f6ab2d4e6725563f249f103c208ac472b6653095d5e5d1deb4b5127b22 |
| mmc3.xlsx, Table S10 | 339,767 | 9fff0b7ff0391c6736794b3c5f3df921beeff44c3bcf3d70e87cb59c916d9945 |

Hashes are local; no publisher digest comparison claimed. Table S9 contains three distinct side-by-side RNA effects (original iMN, human cervical tissue, day-18 diMN replication). Table S10 includes enrichment outputs and one full replication protein table. No original discovery or cervical RNA block was interpreted as a paired contrast.

## Fixed scope before inspecting target values

Plan SHA-256 `d77a7b1e017389e1561b242d83789e3b1a06d5e2094b995adc130fe4e982546a`:

> NeuroLINCS iScience 2021 (10.1016/j.isci.2021.103221). Question: do author-reported total RNA and protein PFKP ALS/control effect estimates have concordant direction in the same day-18 replication cohort? Fixed source scope: mmc2.xlsx Table S9 columns 19–26 (diMN day18 replication cohort DEGs), exact unique PFKP gene symbol; mmc3.xlsx Table S10 tab 'g) replication cohort', exact UniProt Q01813 (check protein name). All source statistics retained. No original/discovery or cervical RNA block interpreted as paired; original protein table not present as full contrast in inspected S10. Report log2FC, relative percent 100*(2^log2FC-1), raw author p/padj and protein FDR/score/log_oddsDE; missing/ambiguous rows stop rather than substitute. No formal difference of effects, no within-unit correlation, no pooling, no new significance test or re-modeling. Both RNA and protein timing/culture and sample-level match must be stated as authors' study design, not independently verified unit mapping. Does not answer postmortem spinal MN protein question; model evidence only.

## Results

Exactly one row matched each target. The RNA contrast is from the day-18 replication block; the protein table explicitly labels contrast C9ALS/CTR.

| Endpoint | Author log2 fold change | Relative change vs control | Source adjusted statistic |
|---|---:|---:|---:|
| PFKP RNA | +0.589353566822211 | +50.4572437563% | padj 0.841479198074537 |
| PFKP protein | +0.480931 | +39.5644012843% | FDR 0.0000450387 |

RNA workbook sheet `Table S2 - RNA DEGs DEseq unfil`, Excel row 7993, columns S–Z: ENSG00000067057, PFKP, baseMean 1191.11078118109, log2FC 0.589353566822211, lfcSE 0.583682296188159, stat 1.00971636568573, pvalue 0.312631199329441, padj 0.841479198074537. Protein workbook sheet `g) replication cohort`, Excel row 351: Q01813, PFKAP_HUMAN, log2FC 0.480931, score 0.99866, FDR 4.50387e-05, log_oddsDE 6.61344.

The RNA point estimate is positive and imprecise, not statistically established; protein estimate is also positive with the reported source FDR very low. Direction is concordant at point-estimate level. No statistical evidence is calculated for a difference between RNA and protein, and the RNA point estimate does not prove a common magnitude. The source protein FDR is not re-estimated or verified against independent biological units; the exact per-analyte contributing sample map, missingness, normalization and author model remain unverified. Group-level paired-cohort contrasts are distinct from individual matched RNA–protein correlation.

## Interpretation

The result is opposite to Guise's −68.1% protein observation in postmortem human spinal motor neurons. It supports preservation of context-specific opposite directions rather than assuming ubiquitous PFKP reduction or obligatory RNA-to-protein discordance. It does not formally contradict Guise: hereditary C9orf72 iPSC cultures differ from postmortem ALS tissue in genotype, differentiation, composition, disease state and measurement. Prior Manzo positive RNA, Takeuchi weak negative MN RNA, and Krach exploratory partial-cohort negative RNA remain on record. No mechanistic inference, glycolytic flux, therapeutic target or clinical result. Do not combine these effects statistically.

## Additional human-tissue candidate, not yet admitted

Caldi Gomes et al., Nature Communications 15:4893 (2024), https://doi.org/10.1038/s41467-024-49196-y, and Hausmann et al., GigaScience (2024), https://doi.org/10.1093/gigascience/giae100 are reports of the same MAXOMOD PFC multiomics resource (51 sporadic ALS and 50 control subjects). The original study reports RNA and protein analysis in the same samples stratified by sex. It is bulk cortex, not motor neurons; raw human RNA is restricted. The author [public supplementary ZIP](https://pmc.ncbi.nlm.nih.gov/articles/instance/11161513/bin/41467_2024_49196_MOESM4_ESM.zip) contains Data 1–16; Data 3 is the human sex-stratified differential RNA result and Data 11 is the protein differential result (also includes other contrasts). Direct publisher retrieval returned HTTP 503; contents not inspected. GigaDB DOI 10.5524/102597 gives associated resource; file-level manifest could not be verified. No restricted-data requests or claims of paired donor access. Distinct next input: public author summary Data 3/11, with both sexes retained and exact contrast verification before target extraction; a within-donor analysis would still need valid accessible paired measurements and coverage metadata.

## Reproduction

```python
import openpyxl
w = openpyxl.load_workbook("mmc2.xlsx", data_only=True, read_only=True)
s = w.active
rows = [(i, r) for i,r in enumerate(s.iter_rows(min_row=3,
        min_col=19,max_col=26,values_only=True),3) if r[1]=="PFKP"]
assert len(rows)==1
i,r=rows[0]
print(i,r,100*(2**float(r[3])-1))
w = openpyxl.load_workbook("mmc3.xlsx",data_only=True,read_only=True)
s = w["g) replication cohort"]
rows = [(i,r) for i,r in enumerate(s.iter_rows(min_row=3,
        values_only=True),3) if r[0]=="Q01813"]
assert len(rows)==1
i,r=rows[0]
print(i,r,100*(2**float(r[2])-1))
```

No remote compute, expense, contact, public distribution or repository modification. No new statistics beyond relative percent conversion.
