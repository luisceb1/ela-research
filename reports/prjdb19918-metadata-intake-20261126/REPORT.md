# PRJDB19918 public metadata intake — 26 November 2026

See the [prospective plan](../../research/plans/2026-11-26-tanaka-source-intake.md). Metadata retrieval only; no new molecular measurements.

## Evidence

A standard public GitHub runner retrieved the official ENA read-run file report successfully: [run 45809243690](https://github.com/luisceb1/ela-research/actions/runs/45809243690), execution commit `60a9dd26f7ba702f7599131af62aab643279936f`, 8 s total. The runner reported 6,338 bytes and SHA-256 `7b0b9c2ed6a74054aba2efa3fe3d031b80ed97e386de0d209e5317ddeb4c7cbb`; [parsed rows and receipt](metadata.json) preserve the logged metadata, not a byte-identical copy of the TSV.

| Assay | Group | Runs | Compressed FASTQ bytes advertised |
|---|---|---:|---:|
| Illumina paired | motor neuron scramble | 4 | 24,817,781,006 |
| Illumina paired | motor neuron TDP-43 KD | 5 | 26,945,071,719 |
| Illumina paired | untreated motor neurons | 5 | 34,453,733,601 |
| Illumina paired | untreated iPSC | 3 | 20,243,676,132 |
| Nanopore single | motor neuron scramble | 4 | 53,701,329,166 |
| Nanopore single | motor neuron TDP-43 KD | 5 | 64,002,519,524 |

There are 26 unique run IDs and 17 unique BioSample IDs. In particular, all 9 Nanopore runs share BioSample IDs with the 9 treated motor-neuron Illumina runs. Do not count these assays as separate biological replicates. The source article [Tanaka et al. 2025](https://pubmed.ncbi.nlm.nih.gov/40670663/) identifies the same 4/5 short-read group sizes; its [full article](https://doi.org/10.1038/s42003-025-08463-4) describes using the same samples for long-read sequencing. All samples derive from the 771-3G line. The sample titles label replicate numbers; independent cultures/differentiations and pairing across conditions have not yet been mapped.

The nine short-read treated libraries alone advertise 51,762,852,725 compressed bytes. Total catalogue size is 224,164,111,148 bytes. No cost estimate for execution is yet authorized; transfer size is not disk or runtime prediction. Untreated and iPSC libraries are not added to the comparison by default.

## Decision: promising, pending admission

The study cites a junction supplement (Supplementary Data 1). Next inspect its schema and the documented independent-unit map before deciding whether raw reads are needed. Publication-level claims or sample labels alone cannot establish per-library support, independence or a new replication of the prior GSE304550 factorial contrast. No UPF1 arm is present. No target counts were read, no FASTQ was transferred, and no Hetzner resources were created.

If eligible after the schema/design gate, fix the event, controls, estimator and scope in a separate prospective plan and obtain a specific budget authorization before starting a disposable VM. Otherwise retain the pending/rejection reason without expanding the search or repeating existing analyses.
