<!-- Working record from the completed 27 November cycle, authorized for public archival release. Statements about no publication/repository changes describe the original analysis step. Only aggregate results and reproducibility details are included. -->

# PFKP in human cortex — MAXOMOD sex-stratified RNA/protein source audit

**27 November 2026 — internal working record.** No new fitted model, biological validation or public release.

## Question and source

Do author-reported PFKP RNA and protein disease contrasts have concordant direction within each sex in postmortem human bulk cortical tissue? This is contextual evidence; it cannot resolve the motor-neuron-specific protein association observed by Guise.

- Caldi Gomes et al., Nature Communications 15:4893 (2024), DOI [10.1038/s41467-024-49196-y](https://doi.org/10.1038/s41467-024-49196-y), [PMC11161513](https://pmc.ncbi.nlm.nih.gov/articles/PMC11161513/).
- Hausmann et al., GigaScience (2024), DOI 10.1093/gigascience/giae100 is the associated MAXOMOD data note, not an independent cohort.
- Human BA6 PFC material: 51 ALS and 50 controls. Article Table 1: 31.4% female among ALS (approximately 16/51), 56% female among controls (28/50); nominal cohort counts therefore ~35/16 ALS male/female, 22/28 control male/female. Actual target-specific assay counts and overlap are not verified. Age and brain-bank origin differ between diagnostics. The original article reports one C9orf72 expansion and one pathogenic NEK1 variant; do not describe entire cohort as strictly sporadic. Authors describe the two modalities on the same samples and stratify by sex. Bulk PFC is not isolated motor neurons; cell composition and assay differences remain relevant.

## Source access and fixed target scope

The official [Europe PMC supplemental package](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11161513/supplementaryFiles) was obtained successfully, unlike earlier failed direct publisher downloads. Inner archive `41467_2024_49196_MOESM4_ESM.zip`, 28,413,530 bytes, SHA-256 `d4a9b7c306164508635e332290ddcb9a0f268876e9f0cce68d9ef5c987f94e3c`. Only Supplemental Data 3, 11 and the legends were extracted/inspected. No donor-level genetic, phenotype or raw-data tables read. No restricted EGA access attempted.

Before target inspection plan SHA-256 `8c67a19e1c0d7c6ab99b92b5c62273fef78ecdd6eabb1930a3c60d1bc8373c7d`:

> MAXOMOD Nature Communications 2024 10.1038/s41467-024-49196-y. Question: do author-reported PFKP RNA and protein ALS/control contrast estimates have concordant direction within each sex in postmortem human bulk prefrontal cortex? Fixed scope: human sex-specific group contrasts only, Supplementary Data 3 (RNA) and 11 (protein), all available male and female results. Exact PFKP or stable gene ID ENSG00000067057 and exact protein Q01813/PFKAP_HUMAN, require unique reconciled row or report all ambiguous entries without selecting, preserve missing. Verify schema, comparison direction, scale and source p/adjusted p; convert log2FC only if documented to 100*(2^log2FC-1). No new model, no comparison of significance between modalities or sexes as evidence of interaction; no sex pooling, no mouse data, no individual correlation, no RNA-protein conversion. Report donor matching only as study design; analyte-level unit overlap not independently verified. No mechanistic or clinical inference. If tables are filtered, absence is missing, not a null effect.

## Findings

### RNA: source table filtered

Supplemental Data 3 describes selected differential expression results from DESeq2 with BH adjustment. Human sheets have fields gene_id, gene_name, baseMean, log2FoldChange, lfcSE, stat, pvalue, padj, regulation. The male sheet has 113 data rows, female 4. Neither has an exact PFKP or ENSG00000067057 match. The relation between those row totals and the article's reported DEG counts was not reconstructed. No fold change or p-value may be inferred from nonappearance. Source-data ZIP manifest contains animal/cell experiments, Figure 6 statistics and immunoblot image, not a full human gene-level DE table. GigaDB 10.5524/102597 was identified earlier but exact full human RNA contrast files not verified. The human RNA arm remains missing for the intended comparison.

### Protein: two measured author contrasts

Supplemental Data 11 has 2,363 rows in each human sex sheet, fields UniProtName, baseMean, log2FoldChange, stat, pvalue, padj. Both contain exactly one PFKAP_HUMAN row. Limma two-sided test; source BH correction. The author figure defines positive effect as ALS high and negative as ALS low. Percent conversion is arithmetic only.

| Sex / endpoint | Native log2FC | Relative change | Nominal p | BH adjusted p |
|---|---:|---:|---:|---:|
| Male PFKP RNA | unavailable | unavailable | unavailable | unavailable |
| Female PFKP RNA | unavailable | unavailable | unavailable | unavailable |
| Male PFKP protein | −0.008144323963695 | −0.5629310907% | 0.865213877116939 | 0.977057209306943 |
| Female PFKP protein | −0.0243060759778903 | −1.6706559414% | 0.665738182348847 | 0.963655988153304 |

Exact source rows: `human-male` Excel row 2093, baseMean 29.9365766348551, stat −0.170486605412017. `human-female` Excel row 1622, baseMean 29.8813000281005, stat −0.434958252503525. BaseMean is retained on source scale, not converted into concentration. No source SE/CI in protein tables; no new intervals estimated. Neither protein contrast is significant; near-zero estimates do not establish equivalence or no biological effect. Sex-specific contrasts are not a formal sex interaction.

## Decision

The intended within-cohort RNA/protein comparison is **unresolved** because the full RNA PFKP estimates are unavailable in the inspected source. The two new PFC protein estimates (approximately −0.56% and −1.67%) are independent contextual point estimates, subject to unverified cross-study donor overlap. They do not reproduce Guise's motor-neuron protein magnitude and do not refute that cell-specific association. Preserve context-dependent positive NeuroLINCS C9 iPSC protein effect +39.56%, Guise −68.1%, prior heterogeneous tissue proteomes, weak negative Takeuchi neuronal RNA and exploratory Krach matched-subset RNA. No statistical pooling of these non-equivalent endpoints. No RNA-protein correlation, causal mechanism, enzyme activity, clinical inference or effect of sex established.

Do not reprocess the restricted RNA or refit models to obtain PFKP. The next enabling input for this particular question is a verified unfiltered human RNA DE table (both sexes) or authorized paired donor-level data with analytically valid matching. Source table absence is not grounds for adding further model variants.

## Provenance

| File | Bytes | SHA-256 |
|---|---:|---|
| Supplemental Data 3 - DE results transcriptomics.xlsx | 12,025,333 | f500d3e16b01ae4e828e967ef79233fb22efc7b85fb9580e1aa61186964c444b |
| Supplemental Data 11 - Proteomics.xlsx | 1,831,526 | 54748e57787d4845d8d2a2ce592b0f943dc816cbd700adf212831914e864d2d3 |
| Supplementary Data - legends.docx | 15,832 | a560ca75e6ba515659fa3f9188e35f304ea3005003936bec61f163a0eeff4b2f |

Hashes locally computed, no publisher digest comparison. Workbooks opened with openpyxl read_only=True, data_only=True. Reproduction (source files as above; no other sheets queried):

```python
import openpyxl
sources = [
    ("Supplemental Data 3 - DE results transcriptomics.xlsx",
        ["human_male","human_female"], "RNA"),
    ("Supplemental Data 11 - Proteomics.xlsx",
        ["human-male","human-female"], "protein")
]
for file, sheets, mode in sources:
    w = openpyxl.load_workbook(file, read_only=True, data_only=True)
    for name in sheets:
        it = w[name].values
        h = next(it)
        hits = []
        n = 0
        for i, row in enumerate(it, 2):
            n += 1
            match = (row[1]=="PFKP" or str(row[0]).split(".")[0]=="ENSG00000067057") if mode=="RNA" else row[0] in {"Q01813","PFKAP_HUMAN","PFKP"}
            if match:
                hits.append((i,row))
        print(name, n, len(hits))
        for i,row in hits:
            print(i,dict(zip(h,row)),100*(2**row[h.index("log2FoldChange")]-1))
```

No expenditure, remote execution, external contact, public repository modification or individual-data export.
