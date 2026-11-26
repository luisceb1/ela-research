# GSE304550 four-arm factorial contrast — 26 November 2026

Evidence level: exploratory descriptive reanalysis of the original study libraries.

## Evidence

The [pre-outcome analysis decision](../alessandrini-5f-20261122/FACTORIAL_INPUT_AUDIT.md) specified the within-batch difference of differences on the percentage-point scale. The eight missing control and UPF1-only libraries have now been processed and transcribed from the user's terminal output, alongside the [eight previously reported libraries](../alessandrini-5f-20261122/counts.csv). All 16 libraries (1,184,350,515 reported query groups) have positive skipping support at both loci. GEO accession mapping follows the prior audit. There are two libraries per arm in each of two recorded blocks; biological pairing remains unresolved.

| Gene | Block | Scramble (%) | UPF1 KD (%) | TDP-43 KD (%) | Double KD (%) | Factorial contrast (pp) |
|---|---|---:|---:|---:|---:|---:|
| UNC13A | M85 | 0.00 | 0.00 | 38.51 | 55.16 | +16.64 |
| UNC13A | M86 | 0.00 | 0.00 | 23.00 | 26.81 | +3.81 |
| PFKP | M85 | 0.13 | 0.00 | 21.93 | 41.92 | +20.13 |
| PFKP | M86 | 0.05 | 0.24 | 23.54 | 32.43 | +8.70 |

Per-library symmetric fraction: 100(A+B)/(2S+A+B), with S skipping support; UNC13A A is the shared edge and B the sum of short and long edges; PFKP A and B are the left and right edges. Equal-weight library means are used within each arm. The contrast is (double KD − TDP-43 KD) − (UPF1 KD − scramble). Edge-specific fractions 100A/(S+A) and 100B/(S+B) are reported separately. All twelve contrasts are positive. UNC13A edge-specific contrasts range from +16.66 to +16.82 pp in M85 and +3.22 to +4.40 pp in M86. PFKP ranges from +15.84 to +24.26 and +8.44 to +8.90 pp, respectively.

[Counts](counts.csv) · [Computed contrasts](contrasts.csv) · [Recompute](summarize.py) with Python 3.11+. The recomputed output matched contrasts.csv exactly in the agent environment.

## Provenance and limitations

The original eight libraries and new SRR34876671, SRR34876670 and SRR34876665 were reported as ENA MD5-verified paired FASTQs. Five new libraries (SRR34876664, SRR34876663, SRR34876662, SRR34876657, SRR34876656) were recovered from NCBI SRA Normalized Format with full quality scores using SRA Toolkit 3.0.3 after repeated ENA transfer/checksum failures. The user reported successful SRA validation, paired FASTQ extraction/identifier checks and matching query-group totals. Validation emitted an unrecognized Illumina database-type warning while reporting consistency. ENA failed copies are excluded. The SRA-derived FASTQs have different serialization and ENA file digests cannot be applied to them.

HISAT2 2.2.3 with hg38, --reorder -p 2 and the same counter definitions as the [original report](../alessandrini-5f-20261122/REPORT.md) were used. The terminal excerpts show completion but full logs, command records, local input/index/binary digests and source files have not been received for independent audit. Source channel differs across libraries; no same-run comparison of the source channels was performed. No paired statistical test or claim about independent differentiations is made. The local denominator is a junction-support proxy and differs from the publication's transcript-read ratio. Zero observed support is limited to the selected edges and filters.

## Interpretation

All eight additional libraries have zero UNC13A cryptic-edge support and positive skipping support. The four-arm results preserve the positive descriptive contrast in each recorded block, with a larger magnitude in M85. PFKP has sparse nonzero baseline support in some libraries. The observations are consistent with the prior prediction within the selected measure. They do not establish RNA degradation kinetics, a causal interaction, protein recovery or clinical benefit. This is a reanalysis of the same biological dataset, not independent replication. M86 library-level overlap remains as reported previously.

## Next discriminating evidence

Retain raw inputs pending an evidence-retention decision. Obtain full local logs and source records before technical closure. The outstanding scientific gates are the differentiation/pairing map and comparison with the publication's per-library denominator. Independent material with verified units, conditions and compatible junction evidence is needed before claiming reproducibility across datasets. A directionally concordant independent result would support extending the descriptive observation; discordance or inadequate coverage would restrict the conclusion to the original material. No further raw download or cloud spend is scheduled by this report.

Sources: [GEO GSE304550](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE304550), [Alessandrini et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC12704819/), [prior accession audit](../alessandrini-5f-20261122/FACTORIAL_INPUT_AUDIT.md).
