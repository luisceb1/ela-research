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

HISAT2 2.2.3 with hg38, --reorder -p 2 and the same counter definitions as the [original report](../alessandrini-5f-20261122/REPORT.md) were used. The subsequent host archive audit below verifies the supplied logs, command records and NCBI source notes; raw input/index/binary digests and the local script files were not part of that archive. See the subsequent current-host provenance audit below. Source channel differs across libraries; no same-run comparison of the source channels was performed. No paired statistical test or claim about independent differentiations is made. The local denominator is a junction-support proxy and differs from the publication's transcript-read ratio. Zero observed support is limited to the selected edges and filters.

## Interpretation

All eight additional libraries have zero UNC13A cryptic-edge support and positive skipping support. The four-arm results preserve the positive descriptive contrast in each recorded block, with a larger magnitude in M85. PFKP has sparse nonzero baseline support in some libraries. The observations are consistent with the prior prediction within the selected measure. They do not establish RNA degradation kinetics, a causal interaction, protein recovery or clinical benefit. This is a reanalysis of the same biological dataset, not independent replication. M86 library-level overlap remains as reported previously.

## Host evidence audit — 26 November 2026

User-supplied archive `ELA_5F_evidencias.tar.gz`, SHA-256 `4c012361df2051e695b41c301ce8988b0d9bef8a2298eb5a0ae38b77b26df382`, contains 54 files: 16 per-library junction tables, 16 HISAT2 logs, 16 command/version records, five NCBI source records and one consolidated eight-library table. Python read the archive directly without extracting or executing its contents.

All 112 per-library counts and coordinates/strands match the fixed records, all 16 log pair counts match counts.csv (1,184,350,515 total), and the consolidated 56 rows match their eight individual tables. Concordant and discordant pair counts and residual mate counts reconcile arithmetically in every log; the alignment percentages recompute within reported rounding. Each command records HISAT2 2.2.3, --reorder -p 2, the hg38 index path and matching run. The five NCBI records match the corresponding pair totals and run accessions. Alignment rates range from 96.82% to 97.75%. [Log QC and hashes](alignment_qc.csv).

The supplied archive is retained privately; the public summary contains only run IDs, aggregate QC and hashes. The archive does not contain the local counter/downloader scripts, raw input bytes, index/binary hashes or complete transfer receipts. Recorded commands and counts establish host evidence coherence, with no independent raw replay or cryptographic verification of input origin. Results and scientific limits above remain unchanged.

## Current-host provenance audit — 26 November 2026

The user ran a read-only collection on the original Ubuntu 24.04 WSL host. The full receipt records 69 SHA-256 candidates and is retained privately (receipt SHA-256 `db0d46905a9064969a0ae6fef525fe027a024c2da3834910a7d96c63a5174886`). [Sanitized digest receipt](current_host_provenance.json) excludes local paths and records only file names, run IDs, byte totals and digests. All 56 earlier small-file digests remain unchanged between inventory and hash collection; all 69 paths, sizes and recorded modification times are stable.

| Evidence | Current-host result | Verification limit |
|---|---|---|
| HISAT2 logs | 15/15 recovered log digests match the archived QC table; 16th run SRR34876669 remains documented in the earlier archive | Collector did not identify a current log for that run; its prefixed pilot directory may not be recognized |
| Index hg38 | All 8 shards, 4,664,041,946 bytes, match both sizes and SHA-256 in the [sealed reference](../../reproduction/stmn2-six-libraries/manifest.json) | Current file identities, not a separate raw replay |
| HISAT2 aligner | `hisat2-align-s` SHA-256 matches historical reference; wrapper and build/inspect utilities also fingerprinted | No historical hash comparison for other executables |
| NCBI SRA | Five retained files (SRR34876656/57/62/63/64), 37,716,180,855 bytes; all current SHA-256 recorded, all five accessions match the documented NCBI channel | No earlier SRA digests or direct source-byte verification; not evidence of unchanged bytes since execution |
| Other receipts | 15 command files, 15 junction tables, five NCBI source records, current digests | Only log digests were compared directly to prior public archive hashes |
| FASTQ / original scripts | None located within scanned roots | Not proof of global absence or deletion; original executed code and FASTQ byte provenance remain unresolved |

The six scan notes concern the depth limit in nonessential HISAT2 source/documentation subdirectories, not a reported failure to hash the identified files. Current SRA Toolkit candidates are fingerprinted but this does not establish the exact historical invoked payload. All 69 entries report hashed status. No raw files or scripts were executed, no downloads or alignments were launched, and no new scientific results were produced.

**Decision:** close this bounded current-host audit with explicit remaining gaps. Do not require further local scanning or repeat computation solely to fill missing provenance. Retain existing files pending a separate retention decision. The original 112 counts and all scientific limitations remain unchanged; full raw-data reproduction of this reanalysis is not certified.

## Next discriminating evidence

Retain the five SRA files and supplied host archive pending an evidence-retention decision. The current-host index and aligner match their sealed reference; SRA fingerprints are now recorded. The historical original counter/downloader and FASTQ byte identities remain unresolved, and should be incorporated only if concrete original materials become available. The outstanding scientific gates are the differentiation/pairing map and comparison with the publication's per-library denominator. Independent material with verified units, conditions and compatible junction evidence is needed before claiming reproducibility across datasets. A directionally concordant independent result would support extending the descriptive observation; discordance or inadequate coverage would restrict the conclusion to the original material. No further raw download or cloud spend is scheduled by this report.

Sources: [GEO GSE304550](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE304550), [Alessandrini et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC12704819/), [prior accession audit](../alessandrini-5f-20261122/FACTORIAL_INPUT_AUDIT.md).
