# GSE299341 published-artifact inspection — 15 November 2026

## Decision and scope

**Raw execution remains unselected; this artifact inspection is closed.** It resolves sample-name linkage and documents the authors' prior exclusion of the tiny library. It partially resolves technical processing intent but does not establish RNA culture independence, deposited-run equivalence or exact molecular deduplication. No gene/junction-count matrix, FASTQ or BAM was acquired and no author code was executed.

[Prospective protocol](../../research/plans/2026-11-15-gse299341-artifact-inspection.md) was committed at621bd008b1d55de78f7667c62d82e8e431e4c46f before artifact requests.10connector requests,8files,36,419decoded source bytes, within12requests/8files/2MB. Repository pinned to [a84e7ec](https://github.com/NIH-CARD/Neurite-WT-RBP-KD/tree/a84e7ec16c5f8db3a47901365085f9de80b6a709). [Manifest](manifest.json) records SHA256 and8/8matching Git blob hashes/lengths; [full tree metadata](repository-tree.json) is not content acquisition. Connector-decoded text is retained under source/. These are payload bytes, not metered origin HTTP bytes. Administrative commit author details are not copied.

## Evidence and limits

| Gate | Inspected artifact / finding | Implication |
|---|---|---|
| Tiny library identity | GEO library TDP43.20 maps through rna-metadata.csv to JR-7961-20, sg200 Soma5, KD; [ten-library linkage](sample-linkage.tsv) preserves all selected GSMs. | Prior tiny ENA record and author sample identity agree. No missing sample is invented or replaced. |
| Prior QC exclusion | RNA/README.md explicitly excludes TDP-43.20 for low depth and PC1 separation; DESeq2.R22,63–65 uses exact TDP43.20 exclusion. RNA-metrics-wide.csv reports7genes detected for this sample; other selected soma rows report23,967–28,027. | A prior author exclusion now explains its analysis status. It does not isolate a sequencing/library/submission failure cause and is not a new target-coverage measurement. Preserve the excluded record; do not inherit this exclusion silently in a future protocol. |
| Technical concatenation | align-and-count.sh selects matching original sample-prefix files separately for R1/R2 and concatenates each before preprocessing. | Multiple files per original sample are intended as technical inputs. The script has no SRR identifiers/lane manifest and no explicit sorted mate-list comparison, so it does not prove the two SRA runs are disjoint or identify iSeq versus main runs. Never infer two biological replicates. |
| UMI implementation | fastp/0.24 module; non-WT branch passes -U, --umi_loc=read2, --umi_len=8, followed by a second call with --trim_front2 6; adapter trimming disabled in both calls. | Confirms extraction/trim option sequence. **The non-WT branch does not explicitly pass --dedup**, although the comment says collapse by UMI. No claim of validated UMI-aware molecular dedup follows from that comment. No fastp semantics test was run here. |
| Later duplicates | STAR2.7.11b BAM then GATK read groups and MarkDuplicates with --REMOVE_DUPLICATES; featureCounts ignores duplicates. | Duplicate handling is present, but explicit UMI-aware matching parameters are not shown. Published article's optical-marking description and this remove-duplicates command are not assumed identical executions. |
| Independent RNA units | Metadata Replicate field is parsed from Long_Name labels, e.g.sg100 Soma1, not an independently recorded differentiation identifier. No culture/date/batch field in inspected RNA metadata. | Five labels per arm remain nominal libraries, not certified independent differentiations/donors; same replicate number across arms is not a proven paired culture. |
| QC versus independence | tdp43.txt has RIN, concentrations and UMI IDs; sample20 soma RIN9.3. | More metadata available, but good RNA integrity does not establish library success or independence. UMI ID labels are not unique molecule sequences and their coding is not inferred. |
| Author expression design | DESeq2.R uses ~Contrast, with prior sample20 exclusion. | Documents their expression pipeline, not a new approved design or proof of biological independence. No effect estimate was inspected/recomputed. |

Exact local sources: [README](source/RNA/README.md), [alignment script](source/RNA/scripts/align-and-count.sh), [metadata organizer](source/RNA/scripts/organize-metadata.R), [RNA metadata](source/RNA/metadata/rna-metadata.csv), [sample list](source/RNA/metadata/rna-samples.txt), [original TDP43 sheet](source/RNA/metadata/tdp43.txt), [QC](source/RNA/RNA_QC/RNA-metrics-wide.csv), [expression script](source/RNA/scripts/DESeq2.R). Remote paths use the pinned repository commit above.

## Concrete processed-artifact lead — inventory only

The pinned nontruncated tree lists **figure3/data/tdp_kd_whole_cell_junctions.tsv**,85,922,421bytes, its exact Git blob SHA is retained in repository-tree.json. **Contents were not downloaded or inspected**: schema, sample columns, coordinate convention, target inclusion, per-library counts versus aggregate/PSI, missing-event handling and original QC/filtering are unknown. Filename alone does not demonstrate eligibility or independent validation.

This is a concrete lower-transfer lead than86.56GB of raw FASTQs. A separately prospective **schema/provenance inspection of that one exact processed artifact** is the recommended next decision; verify the actual file/schema before defining any sealed-target measurement. Do not assume rows contain raw counts or permit original20paired-group diagnostic. Preserve the historical0.585773 and all closed cycles; no effect/ratio/PSI computation follows here.

The author's STAR job requests100GB memory,16CPUs and400GB scratch. This published allocation is not measured minimum resource need, but it exceeds Luis's current machine envelope if copied literally. No cloud purchase or raw runner is proposed. A processed-table route may avoid that pipeline, subject to schema acceptance.

## Closure

No automatic source expansion, count download, author contact or scientific execution. This inspection closes with a new prior-exclusion finding, a processing discrepancy and a concrete processed-file lead. Raw processing remains gated; unsupported claims of UMI deduplication, RNA biological independence and deposited-run provenance remain withheld. ADWB access and author replies unchanged. PR80 remains for human review.

