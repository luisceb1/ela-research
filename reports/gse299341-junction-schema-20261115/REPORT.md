# Processed-junction schema decision — 15 November 2026

**Rejected for per-library count reproduction.** The exact candidate's header exposes condition-level PSI/dPSI/probability fields, not per-library numerical read support. Stop at this decisive gate; no target-specific rows were searched, no effect/ratio/PSI was computed, and the remaining85.86MB was not fetched. Rejection is for this count question, not every possible scientific use of the table or all GSE299341 data.

[Prospective protocol](../../research/plans/2026-11-15-gse299341-junction-schema.md), committed fc22ffbf27d3b4866c527c52547e1d9b584ddfb3 before content access. Candidate pinned to author commit a84e7ec16c5f8db3a47901365085f9de80b6a709 and Git blob983b0b7e9d21eb4b3007e61dabaf27e5e7d767f7, indexed85,922,421bytes.

## Actual acquisition

GitHub connector rejected the oversized file. One direct HTTP fallback returned206, Content-Range bytes0-65535/85922421: **65,536body bytes**, prefix SHA2564dfa9edbba23e5fe2ea63cf2fe7b18771f0a0ce26a10474cca4149b9c05adff4. [Transport receipt](transport.json). Whole-file integrity is **not verified** by a prefix hash/ETag. Connector internal origin traffic is not exposed; its failed retrieval is not zero-byte metered evidence. Direct fallback consumed65,536observed bytes under100MB cap; no retry/full-file acquisition. One additional author Rmd17136bytes was read statically, not executed. No FASTQ/BAM or unrelated data table.

[Exact header and preamble](header.txt), [machine-readable schema decision](schema.json). Header is line8 after7comment lines; the first line is not the TSV field header. The prefix necessarily includes leading unrelated data rows, but no target scan or biological analysis was made. Only header/preamble is copied here; the transport receipt hashes the larger received prefix. Source Rmd is retained separately.

## Schema/provenance gates

| Gate | Direct evidence | Decision |
|---|---|---|
| Per-library support |20header fields; condition fields ctrlSoma_median_psi, KDSoma_median_psi, KDSoma-ctrlSoma_median_dpsi and changing/nonchanging probabilities. No read-count or GSM/SRR/library columns in this schema. | Fails per-library count gate. Do not convert PSI into reads or apply20paired-group diagnostic. No denominator reconstruction. |
| Representation | Module/gene/LSV/event identifiers, junction name/coordinates, event/junction changing flags; not a simple unique-junction/library matrix. | Cannot infer one row per unique intron or independent observation. |
| Embedded processing | Preamble command voila modulize, version2.4.dev4+gdd43612, --show-all, --changing-between-group-dpsi0.05; changing/nonchanging/probability thresholds recorded. | Preserve exact command; --show-all does not establish complete raw catalogue or absence semantics. No comparison/retuning of author effects. |
| Upstream identity | Embedded splicegraph/delta-PSI paths include /SAN/neuroscience/NYGC_Jan2023/pipeline_tdp/ and ctrlSoma-KDSoma.deltapsi.voila. | This string does not establish NYGC donor origin, but it also does not certify linkage to the10selected GSE299341 libraries. Source identity remains unresolved; do not claim independent cohort or matching GSMs. |
| Genome/convention | seqid,strand,junction_coord columns. Cached primary methods mention GRCh38, but the table preamble has no explicit coordinate origin/boundary definition or sample manifest. | Do not silently assign0/1-based convention or apply sealed coordinates. No conversion needed after schema rejection. |
| Missing events | No raw support/denominator or explicit zero/missing code definition in inspected header. | Missing row cannot be interpreted as biological absence, count0 or failed support threshold. |
| Extra author notebook | [utr_and_splicing_analysis.Rmd](source/utr_and_splicing_analysis.Rmd) covers WT isoform/APA/UPF1/motif work; literal filename and MAJIQ/junction-import strings were not found in its inspected text. | Does not resolve this table's generating pipeline or GSM linkage; absence of those strings in one notebook is not absence of another pipeline. |

The general paper's MAJIQ description and genotype names are contextual only; this task does not validate their execution against the deposited file. Earlier raw-processing and biological-unit uncertainties from [artifact inspection](../gse299341-artifact-inspection-20261115/REPORT.md) remain.

## Recommendation and closure

Close this processed-count route for the exact artifact. **Do not download the remaining table for the current count-reproduction question and do not buy CPU for it.** A future use as an author-processed splicing summary would be a different question and still require upstream/sample/coordinate provenance; no such analysis is scheduled.

Next discriminating input would be a library-linked raw junction count matrix/STAR junction files with their coordinate/filter definitions, or source clarification that resolves those fields and experimental units. No contact is sent. AD/author waiting status unchanged; no automatic raw alignment, second-table substitution, extra marker, threshold change, merge or reopening of #37/#44/donor cycles.

This finite negative schema result neither proves that all processed GSE299341 files are unsuitable nor excludes alternative mechanisms for the prior UNC13A low-support observations.

