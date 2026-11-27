<!-- Working record from the completed 27 November cycle, authorized for public archival release. Statements about no publication/repository changes describe the original analysis step. Only aggregate results and reproducibility details are included. -->

# PFKP in laser-captured human spinal motor-neuron-enriched RNA — GSE76220

**27 November 2026 — private working record.** Target-blind admission check followed by a prospectively limited exploratory calculation. Not a publication, not a replay of the source DESeq2 model.

## Question and prior evidence

Does total PFKP RNA abundance decrease in human ALS lumbar motor-neuron-enriched samples? This is a separate abundance question, not the disease-by-cell-type interaction originally proposed. Prior independent source Takeuchi reports a shrunken MN RNA estimate −3.51%, adjusted p=0.999937; Guise reports −68.1% protein (different molecular level and cohort); Manzo reports positive RNA contrasts in bulk spinal cord and an iPSC-derived model. Preserve discrepant results.

## Source and design

Krach et al., Acta Neuropathologica 136:405–423 (2018), [DOI 10.1007/s00401-018-1870-7](https://doi.org/10.1007/s00401-018-1870-7), [PMID 29881994](https://pubmed.ncbi.nlm.nih.gov/29881994/), [full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC6215775/), [GEO GSE76220](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE76220), PRJNA306659.

The source describes lumbar LCM-enriched surviving motor neurons from 13 sporadic ALS and nine control donors; one control was withdrawn after initial expression profiling because of prior spinal radiation. Samples are neuronal-enriched, not pure isolated neurons; authors acknowledge adjacent glia, with selected ALS cases of rostral onset and caudal progression. The design is cross-sectional and survivor-biased. The paper uses DESeq2 on count-derived expression comparisons. RPKM is not raw counts and cannot validly be supplied to DESeq2 as counts.

## Provenance gate, before target inspection

Direct official metadata and matrix header reconciliation (numeric coded identifiers in GEO sample titles vs matrix columns, group suffix a/c):

| Item | ALS | Control | Total |
|---|---:|---:|---:|
| GEO deposited sample titles | 13 | 8 | 21 |
| Historical RPKM matrix columns | 12 | 9 | 21 |
| Exact common coded IDs, group concordant | 12 | 8 | 20 |
| GEO-only | 1 | 0 | 1 |
| Matrix-only | 0 | 1 | 1 |

All 20 common IDs have matching group labels. The matrix-only control is the withdrawn radiation-treated control documented in the paper. The reason the remaining GEO ALS sample does not appear in the matrix is unresolved. No individual codes or measurements exported. This proves the matrix is not the final 21-sample set. Deposited sample unit is one donor's pooled LCM material, not individual neurons. The original all-21 descriptive estimand is blocked; no imputation and no silent inclusion of the withdrawn control.

The author aggregate DESeq2 comparison is described in Online Resource 2, Data S1a. Attempted publisher workbook delivery returned HTTP 503; PMC endpoint returned HTML, not XLSX. No values or fields from that workbook were read. It remains unresolved whether it contains a full unfiltered PFKP contrast with inferential fields. The other GEO processed text (MPR) has ratio/z-score annotation fields, not the required sample-level general expression matrix; not used for this analysis.

## Protocol chronology

Before target inspection, initial plan written: SHA-256 `0747df8417bd5b687c8e5022575b5336ebcba0a8b6439a2b6e41e3dbaa19aac7`. The initial primary author statistics route and complete 21-sample secondary route are both blocked. A target-blind amendment was written before extracting the gene row, SHA-256 `d3c2126d1ebaffc482b69ae366f787b92501188db441eb2db0b1540dd1162c87`:

> Target-blind design check: GEO titles map 13 sALS and 8 controls; RPKM file has 12 a-suffix and 9 c-suffix. Common coded IDs: 20 (12 ALS, 8 controls), zero group conflicts. The sole matrix-only control is the withdrawn radiation-treated control documented by Krach; one GEO ALS is missing from the matrix. The original all-21 secondary estimand is therefore blocked. Primary author workbook retrieval failed (publisher 503, PMC returned HTML not XLSX). Permit a distinct, explicitly exploratory descriptive complete-match subset result only: 12 ALS and 8 controls, no imputation of missing ALS and no inclusion of withdrawn control. All matched donors, exact unique gene row, mean/median RPKM, arithmetic ratio and Welch 95% interval for raw-scale mean difference; geometric ratio if all positive. No p-value or new DESeq2 inference, no claim of original-cohort reproduction, no individual values or coded IDs exported. If nonunique gene or nonnumeric/missing target values, stop and preserve limitation.

## New exploratory calculation

Matrix has 25,856 rows, exactly one PFKP symbol match. All values in 20 common units numeric, finite, positive. No covariate adjustment, no other target tested, no significance-based inclusion.

| Group | n | Mean RPKM | Median RPKM | Sample SD |
|---|---:|---:|---:|---:|
| Sporadic ALS | 12 | 1.5573547856 | 1.5124340010 | 0.3035940885 |
| Controls | 8 | 1.8264000881 | 1.8365539415 | 0.1588429215 |

- Arithmetic mean ratio ALS/control: 0.8526909277, or **−14.7309072%** relative.
- Mean difference (ALS − control): −0.2690453025 RPKM; unadjusted Welch 95% interval [−0.4883621885, −0.0497284166] RPKM, effective df 17.30362749.
- Geometric mean ratio (all values positive): 0.8400009965, or approximately −16.0%, distinct descriptive estimand.

The interval excludes zero conditionally under the ordinary independent-donor raw-scale Welch assumptions. It is not the paper's adjusted p-value, is not valid evidence of the missing donor's influence, does not correct disease-related selection or covariates, and is not a confirmatory result from the original full analysis. Direction compares descriptively with Takeuchi; the effect sizes are not directly pooled because assay, units, selection, model and shrinkage differ.

## Evidence decision

We now have a modest negative RNA point estimate in two distinct reports (Takeuchi and the historical matched subset of Krach), without confirmed donor-level cohort nonoverlap. This is not evidence of a uniform or large selective PFKP decrease. The Krach dataset cannot estimate a within-donor cell-type interaction (only MN-enriched samples in inspected matrix). No RNA-to-protein extrapolation, causal, glycolytic flux, functional or clinical inference. The large Guise protein effect remains unresolved. The next enabling evidence is the authoritative full-cohort gene-level source table or corrected processed matrix; absence of target from a filtered author table would not be evidence of no change. Do not re-fit additional models on this subset merely to change significance.

## Files, integrity and computation

Official supplementary directory https://ftp.ncbi.nlm.nih.gov/geo/series/GSE76nnn/GSE76220/suppl/; gzip integrity tests passed. SHA-256 locally calculated, no publisher digest verified.

| Filename | Bytes | SHA-256 |
|---|---:|---|
| GSE76220_ALS_LCM_RPKM.txt.gz | 3673192 | 0ed60c73c1739d3638abffbc09a3a9ea317160714ad9a51fa9df5b05f4e81103 |
| GSE76220_ALS_LCM_MPR_gene_expression.txt.gz | 699587 | 6bab464cdbbc15e0fa6774eeada2567a196dd37b774f2e210fec129abdef53c4 |

Python 3.12.14, pandas 2.2.3, NumPy 2.3.5, SciPy 1.17.0. Reproducibility code (aggregate outputs only; input is the GEO series family metadata and matrix; use authorized minimal coded linkage):

```python
import re, urllib.request, collections
import numpy as np
import pandas as pd
from scipy.stats import t

url = "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE76220&targ=all&form=text&view=quick"
with urllib.request.urlopen(url, timeout=20) as r:
    geo = dict(re.findall(r"^!Sample_title = (\d+)_(Control|sALS)\s*$",
                          r.read().decode(), re.M))
df = pd.read_csv("GSE76220_ALS_LCM_RPKM.txt.gz", sep="\t", low_memory=False)
matrix = {m.group(1): (x, {"a":"sALS","c":"Control"}[m.group(2)])
          for x in df.columns if (m := re.fullmatch(r"(\d+)([ac])", x))}
assert collections.Counter(geo.values()) == {"sALS":13, "Control":8}
assert len(matrix.keys() & geo.keys()) == 20
assert all(matrix[k][1] == geo[k] for k in matrix.keys() & geo.keys())
row = df[df.Gene_symbol.eq("PFKP")]
assert len(row) == 1
a = {}
for gr in ["sALS", "Control"]:
    cols = [v[0] for k,v in matrix.items() if k in geo and geo[k] == gr]
    a[gr] = pd.to_numeric(row.iloc[0][cols], errors="raise").to_numpy(float)
    assert np.isfinite(a[gr]).all() and (a[gr] >= 0).all()
    v = a[gr]
    print(gr, len(v), v.mean(), np.median(v), v.std(ddof=1))
x, y = a["sALS"], a["Control"]
vx, vy = x.var(ddof=1)/len(x), y.var(ddof=1)/len(y)
delta = x.mean()-y.mean()
dfw = (vx+vy)**2/(vx*vx/(len(x)-1)+vy*vy/(len(y)-1))
half = t.ppf(.975, dfw)*np.sqrt(vx+vy)
print(x.mean()/y.mean(), delta, delta-half, delta+half)
if (x>0).all() and (y>0).all():
    print(np.exp(np.log(x).mean()-np.log(y).mean()))
```

No new cloud execution, expenditure, contact, publication or individual-data export. No public repo modification.
