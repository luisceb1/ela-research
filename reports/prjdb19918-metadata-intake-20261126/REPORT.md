# PRJDB19918 public metadata intake — 26 November 2026

See the [prospective plan](../../research/plans/2026-11-26-tanaka-source-intake.md). Metadata retrieval only; no new molecular measurements.

## Technical pilot closed — 26 November 2026

See [pilot closure](PILOT_CLOSURE.md). Subsequently authorized two-library cloud run completed successfully with verified cleanup and insufficient cryptic support in both libraries. The seven remaining libraries are not scheduled; independent-unit and source gates remain unresolved. Earlier status statements below are historical.

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

## Supplement schema attempt — 26 November 2026

A second bounded standard-runner job attempted to retrieve the article XML from Europe PMC, with the goal of resolving the author junction supplement filename and inspecting only its headers. [Run 45809694928](https://github.com/luisceb1/ela-research/actions/runs/45809694928), job 139874012335, execution commit `17fc048475b877d2aff34ebeab2450830c66ccad`. The request timed out before an article receipt or supplement header was returned. The job completed with the explicit log marker `SCHEMA_PENDING TimeoutError`; this is **not** a successful content inspection. No supplement schema, event support, or sample-unit map has been verified. The bounded attempt is closed without automatic retry; no raw transfer or VM is justified yet.

## Fixed inputs and follow-up admission — 26 November 2026

The [input manifest](input_manifest.json) records all **18 paired FASTQ files** for the fixed nine Illumina runs (51,762,852,725 compressed bytes), with official ENA paths, advertised byte lengths and published MD5 digests. The [metadata retrieval](https://github.com/luisceb1/ela-research/actions/runs/45810760349) succeeded, reporting a 6,363-byte ENA response and its SHA-256. This establishes expected input identities, not acquired or validated bytes. No reads were transferred.

All nine technical BioSample records were retrieved twice; their reported SHA-256 identities agree between attempts. Neither parser returned selected attributes establishing culture/differentiation, pairing or batch. The author article describes biological replicates and the same nine samples across assays, but their independent preparation map remains unresolved. A distinct BioSample is not by itself proof of independent biological replication.

The [publisher follow-up](https://github.com/luisceb1/ela-research/actions/runs/45811037613) retrieved the HTML successfully, but its bounded link inspection did not resolve a unique downloadable junction supplement or reporting-summary file. This is not proof of absence. No supplement schema or event counts were obtained. [Admission receipt](admission_followup.json) records the positive checks and explicit pending outcomes.

The user's EUR 10 objective budget is authorized for the proposed phased execution subject to the scientific and technical gates. **Paid execution remains pending**, because the independent-unit and supplement admission checks did not pass. The provisional two-library technical-only alternative is described in [PILOT_DECISION.md](PILOT_DECISION.md); it would answer a coverage/portability question, not establish biological replication. No further routine source retry, cloud dispatch or automatic extension to all nine is authorized by this admission result.
