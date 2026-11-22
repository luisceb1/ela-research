# GSE304550 factorial contrast: input and experimental-unit audit

## Decision

GEO establishes four treatment arms in both M85 and M86, with two RNA-seq libraries per arm and batch. The public sample matrix supplies batch and replicate number but no field linking each library to a specific differentiation, culture or cross-treatment pair. Figure 5F reports four biological replicates from two independent differentiations and a paired test. The methods describe using differentiation as a covariate for gene and transcript analyses. Neither statement identifies the actual pairs in the deposited libraries. SRX and SAMN identifiers establish accession identity and cannot resolve experimental pairing.

| Batch | Scramble GEO / run | UPF1-only GEO / run | Compressed FASTQ total |
|---|---|---|---:|
| M85 | GSM9152768 / SRR34876671, GSM9152769 / SRR34876670 | GSM9152774 / SRR34876665, GSM9152775 / SRR34876664 | 45,655,221,934 bytes |
| M86 | GSM9152776 / SRR34876663, GSM9152777 / SRR34876662 | GSM9152782 / SRR34876657, GSM9152783 / SRR34876656 | 43,128,446,884 bytes |

The eight missing libraries total **88,783,668,818 bytes** compressed. The public GEO series has a processed gene-expression table, with no sample supplements listed for any of the 16 libraries. ENA lists 16 runs with paired FASTQs and blank submitted-file fields. The analysis file report returned headers only. No sample-level junction counts or indexed alignments were found through these records or in the paper's linked data availability. External recount3/Snaptron endpoints did not return usable records in this check, so their coverage of SRP606829 remains unverified.

## Analysis decision before observing the missing arms

For each batch, take equal-weight means of the per-library local junction fraction. Estimate `(double KD - TDP-43 KD) - (UPF1 KD - scramble)` on the percentage-point scale. The observed first terms for UNC13A are +16.64 and +3.81 points in M85 and M86. The unmeasured second term only needs to exceed +3.81 points in M86 to reverse the sign there. The same decision thresholds for PFKP are +20.00 and +8.89 points.

Keep the symmetric junction fraction, both edge-specific checks, and sample-level coverage. A measured zero with skipping support is distinct from a zero denominator. Use the same alignment and counting workflow for every arm if an author-provided junction matrix cannot be applied consistently to all 16 libraries. Without a verified pairing map any estimates remain descriptive within the recorded blocks. A common sign across the two batches would motivate a test on independent material. Discordant signs or sparse denominators warrant reporting batch results separately. These are steady-state RNA measurements.

The smallest input that resolves the bottleneck is a table mapping GEO accessions to differentiation and cross-treatment pairs plus library-level UNC13A/PFKP splice-junction support across all four arms. Prioritize obtaining that input before additional FASTQ transfer.

## Sources

- [GEO GSE304550](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE304550), [GEO series matrix](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE304nnn/GSE304550/matrix/GSE304550_series_matrix.txt.gz), SHA-256 `517e18f1627c0e88f4c1ec36a15fc7a734045ec1db74bb564e7d3c0fae24235e`.
- [ENA read-run file report](https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJNA1301730&result=read_run&fields=run_accession,experiment_accession,sample_accession,fastq_bytes,submitted_format,submitted_ftp&format=tsv), SHA-256 `1d71b605952e811431c6a95bb42e48b112a3ab67766c31e5389000378d6cd740`.
- [ENA analysis file report](https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJNA1301730&result=analysis&fields=analysis_accession,analysis_type&format=tsv).
- [Alessandrini et al., Figure 5 statistics and Methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC12704819/).
