Subsequent authorized artifact review: [updated evidence and limits](../gse299341-artifact-inspection-20261115/REPORT.md). Earlier unresolved-status statements below are historical and superseded only where explicitly resolved.

# GSE299341 bounded design review — 15 November 2026

## Decision

**Pending; not selected for raw execution or inference.** Six web-tool calls exhausted the prospective cap. The full primary methods are now readable and remove the earlier full-text-access obstacle. UMI layout and study-level depletion validation are documented; run relationship, RNA-library biological-unit mapping and the anomalous library remain unresolved. No FASTQ, junction/count matrix, effect analysis, contact, spend or merge was performed. No new candidate was added.

Protocol committed before new queries: 3684579603826d8022ef3a94d39889024e7ae281, [selection rule](../../research/plans/2026-11-15-gse299341-design-review.md). Base main3fbbac9. This is a reappraisal of an inventoried source under the authorized local-route question, not a new dataset discovery. Earlier cross-background and recount3-availability rejections stand.

## Traceable assessment

| Question | Evidence and locator | Decision / remaining uncertainty |
|---|---|---|
| Intervention / specificity | Dargan et al., doi10.1093/nar/gkaf709, PMC12309387, Methods iPSC maintenance/differentiation, lines252–258: lentiviral TARDBP sgRNA with dCas9-KRAB; nontargeting guide; selection before differentiation. | Targeted transcriptional depletion, not restorative STMN2/UNC13A treatment. A targeting guide does not establish complete specificity. |
| Model / timing | Same methods249–257 and GEO series: WTC11 i3Neurons, Boyden chamber; day3 replating, day17 collection. | Single background. Not measured post-deficit restoration or clinical evidence. |
| UMI and linker | Primary Data analysis328–329 and GEO GSM9037617 processing: RBP-KD experiment uses8-nt UMI at start of R2, then6-nt linker removal, fastp; STAR2.7.11b/GENCODE45 and Picard3.2.0. | Layout is documented. This differs from GSE252892's ordinary paired-read processing; its executor cannot be reused unchanged. Exact fastp flags/dedup implementation and cross-run dedup scope were not recovered. |
| Which controls | GEO series distinguishes WT/no-sgRNA experiment from TDP43 experiment NT controls. Selected NT GSM9037603–607 and KD GSM9037613–617 are the same TDP43 experiment. | Do not mix WT v2-kit controls with NT controls or assume v2/v3 kit confounding solely from condition names. Primary labels WT versus RBP KD experiments, not necessarily every NT versus KD library. |
| Depletion evidence | Primary Results424–425: western and IF confirm depletion (Supplementary Fig.S4A–D), with decreased protein abundance in fractionated proteomics. | Study-level orthogonal validation now documented. Supplement images/numbers and exact RNA-library linkage not inspected; no numeric per-library efficiency certified. RNA expression changes are not protein efficacy. |
| Units / n | Ten selected GEO soma GSMs have sample labels,5NT/5KD. Primary FISH/FUNCAT methods313,321 explicitly describe3independent differentiations for those assays. | Do not transfer the imaging differentiation count to RNA-seq. Exact RNA culture/differentiation/batch mapping remains unresolved. Proteomics5-versus5 in Fig5D is a different assay. Runs/fractions are not independent cultures or donors. |
| Two runs per library | Prior manifest binds20runs to10SRX/GSMs. New SRA experiment open failed; exact-run search gave no resolving record. | Shared SRX supports one nominal experiment/library grouping, not two biological replicates. Lanes, resequencing, split submissions or duplicates cannot be distinguished from inspected evidence. Do not concatenate/deduplicate across runs by guesswork. |
| Tiny GSM9037617 | Prior ENA inventory: SRX29112933, SRR33905369/370, read_count1791/1728,4files totalling358774bytes. New GEO record identifies TDP43.20, KD sample5 soma, same SRX. | Identity confirmed; cause unresolved. Do not silently exclude, replace or label a biological zero. No new read/canonical coverage measurement. |
| Independence | Different declared WTC11 experiment from WA01/H1 GSE252892. Authors include Fratta/Keuss; UPF1 sibling GSE296063 shares this publication. | Another accession/background is not sufficient proof of independent culture history or upstream non-overlap. Not independent-donor validation; sibling UPF1 is not a second TDP43 source. |

## Accessible artifacts and restrictions

Primary [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC12309387/) is accessible; it is a US Government work. Methods RNA sequencing261–262 report Takara total-RNA v2/v3 preparations and main sequencing2x100bp, about50M/sample; pooled libraries were checked by iSeq before main sequencing. This does **not** establish that the two deposited runs represent iSeq/main sequencing. The UPF1 paragraph's polyA/2x150 protocol belongs to another experiment and must not be substituted.

[GEO series](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE299341) advertises a3MB gene-feature count CSV; it was not downloaded and gene counts are not sealed junction counts. Article Data availability540–542 links ADWB, [author GitHub](https://github.com/NIH-CARD/Neurite-WT-RBP-KD), Zenodo15298524 and PRIDE PXD054548. GitHub root is readable with RNA/Proteomics folders; the RNA directory retrieval failed. No code contents or supplements were recovered from that route. No claim that the code is absent or permanently inaccessible. ADWB access remains unverified; public deposition is not an active workspace.

Prior ENA metadata total remains86,561,386,307 compressed bytes for40files; not newly measured, refreshed or downloaded here. See [manifest/inventory](../local-raw-feasibility-20261112/REPORT.md). No origin byte metering is available from web search; retrieval log stores tool-returned text, not original server response bytes.

## Stop and recommendation

Close this finite documentary review **pending exact artifacts**, without scheduling raw execution. The blocker is provenance/processing specification, not demonstrated lack of target depth or a shortage of CPU. A new bounded artifact-inspection task could inspect the published RNA processing scripts and sample sheet for exact UMI/run and culture/batch relationships; it would need its own prospective scope. If those artifacts do not resolve the tiny library, preserve it as an explicit input limitation and define any future handling before counts, rather than remove it after results.

No automatic download, marker panel, effect estimate or parameter change follows. Sealed targets and20-group descriptive diagnostic unchanged; ~200canonical remains a conditional scenario, never a hard gate. GSE252892, #37/#44 and earlier donor cycles stay closed. Retain negative results and unresolved questions.
