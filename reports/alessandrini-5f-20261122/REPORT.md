# GSE304550 junction reanalysis of the Figure 5F contrast

Exploratory, descriptive reanalysis of eight libraries from the Alessandrini study. The question is whether adding UPF1 knockdown to TDP-43 knockdown shifts the observable UNC13A cryptic fraction in both recorded batches. PFKP is a response comparator.

## Evidence

| Gene | Batch | TDP-43 KD (%) | Double KD (%) | Change (percentage points) |
|---|---|---:|---:|---:|
| UNC13A | M85 | 38.51 | 55.16 | +16.64 |
| UNC13A | M86 | 23.00 | 26.81 | +3.81 |
| PFKP | M85 | 21.93 | 41.92 | +20.00 |
| PFKP | M86 | 23.54 | 32.43 | +8.89 |

[Counts and accession map](counts.csv) transcribe the user-supplied terminal output. Run `python3 summarize.py` with Python 3.11 or newer to recompute means and edge-specific sensitivities. Each condition mean gives equal weight to its two libraries. For each library with skipping support S and cryptic supports A and B, the symmetric measure is (A+B)/(2S+A+B). UNC13A uses the shared edge for A and the sum of short and long alternative edges for B. PFKP uses its two cryptic edges. The script also reports A/(S+A) and B/(S+B).

HISAT2 2.2.3 aligned compressed paired FASTQs directly to hg38 with `--reorder -p 2`. The counter used primary mapped records with NH=1, compatible XS when present, and at least 15 aligned bases on each side of the intron. Each contiguous query group contributed at most once per edge. Zero-based half-open introns, in CSV count column order: UNC13A chr19 minus (17641556,17642844), (17641556,17642413), (17642541,17642844), (17642591,17642844); PFKP chr10 plus (3099352,3101364), (3099352,3099556), (3099819,3101364). User reported FASTQ MD5 checks against ENA for all 16 mates. Complete per-run logs and local binary/index digests were not provided. The first library reported 97.65% overall alignment. Repeated terminal excerpts for it were counted once.

## Interpretation and limits

Both edge definitions give a positive UNC13A delta in both batches, +16.66 to +16.82 points in M85 and +3.22 to +4.40 points in M86. In M85 the conditions separate across the two observed libraries per group. In M86 UNC13A overlaps across conditions. PFKP rises in both batches and has the larger symmetric delta in each. The relative long-edge share among short and long supports does not change in a consistent direction across batches.

These are the original study libraries reprocessed using an alternative aligner and counting rule. The study used Cutadapt and STAR and displayed cryptic reads relative to all transcript reads. The local junction fraction and the published denominator may differ. A/B labels do not establish paired or independently differentiated cultures. No statistical inference or separate UPF1-by-TDP-43 interaction is estimated here. Steady-state junction support does not identify an RNA decay mechanism.

## Next experiment

Recover the study's per-library differentiation map and junction inputs where accessible. The strongest next question within GSE304550 is the within-batch difference of differences: compare the effect of UPF1 KD in the TDP-43 KD background against its effect in the scramble background. GEO records both missing arms in each batch with two libraries per arm. Check the metadata and inexpensive junction sources before committing to a transfer. Apply the same locked counter to all arms if needed. Report per-library coverage and both edges. Follow any reproducible contrast with a different dataset and verified biological units.

## Sources

- [GSE304550 sample records](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE304550) and [ENA project](https://www.ebi.ac.uk/ena/browser/view/PRJNA1301730).
- [Alessandrini et al., Figure 5 and Methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC12704819/).
- [Brown et al. candidate junction resources](https://github.com/frattalab/unc13a_cryptic_splicing/tree/e05e8723e3d18e64c6c559db18de423282511c91/data).
