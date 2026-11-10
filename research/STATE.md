# Current research state — 2026-11-04

This replaces earlier planning snapshots. Historical reports and commits remain evidence, not automatic instructions to rerun work. This consolidated state accompanies integration of PRs #46–#49. Review details and exact checked commits are preserved in [INTEGRATION_REVIEW](../reports/integration-20261104/REVIEW.md).

## Active scientific priorities

| Priority | Status | Only input enabling analysis |
|---|---|---|
| #37: independent UNC13A source | No accepted new technical source | Concrete Seddighi/AD Workbench file or manifest with junction counts or indexed alignments, condition→independent unit→batch map and access terms |
| #44: K26 Fig.4d functional reproduction | FR-K26-4d v1 ready; contract disabled | Original eEPSC values/units, groups, cell→culture→differentiation map, exclusions and chronology |

Keep target junction coverage ≥20 and at least three independent biological units per condition before an inferential contrast for #37. Do not reopen rejected candidates or the closed pilot by default. [Source gate](../reports/source-gate-issue37-20261103/REPORT.md).

K26 Fig.4d reports 34/30/25 cells across three experiments; cells do not establish biological replication. The selected ASO intervention is concurrent with TDP-43 depletion, not treatment after demonstrating a prior functional deficit. No effect is estimated. [Plan](../reports/functional-rescue-20261103/REPRODUCTION_PLAN.md).

## Update — 10 November 2026

Luis confirmed on 10 November that the K26 file has **not** arrived (Fratta indicated publication "this week") and that AD Workbench has **not** granted access. Both #37 and #44 therefore remain blocked on exactly the inputs already recorded; no follow-up contact is authorized.

Completed instead, as bounded documentary work: an intervention-chronology matrix over the six accessible UNC13A intervention preprints. **12 experiments; 0 post-deficit recovery; 10 prevention; 2 indeterminate.** Every published UNC13A intervention we can inspect acts before or concurrently with TDP-43 loss, so correcting UNC13A after a measured functional deficit remains untested in the accessible literature. Single-reader audit: it requires second human curation, and 2 of 6 sources (Mallika, Cao) expose only abstracts, leaving the matrix at its prespecified minimum. Both public routes to those two methods were exhausted the same day; verified in passing that those two preprints share a laboratory and six authors, so they are not independent replications of each other. [Matrix and report](../reports/unc13a-intervention-timing-20261110/REPORT.md), [plan](plans/2026-11-10-unc13a-intervention-timing-matrix.md).

PMID 42983891 (Ikegami/Koike 2026, peer reviewed) was checked against the #37 gate and **rejected as a technical source**: qRT-PCR/ddPCR on post-mortem motor cortex, no junction counts, no RNA-seq/GEO/BAM, data by author request. Kept as context only: pathological subtype 2b shows higher UNC13A cryptic and truncated STMN2 RNA, correlated at Spearman ρ = 0.58. This does not open a fourth candidate.

The daily watcher's `long_reads` query searched all fields including reference lists (11,040 hits, unrelated papers); it is now restricted to TITLE_ABS (42 hits), with tests. This is a scope fix, not a quality filter.

## Access and communications: dated evidence only

The 04 November administrative audit records AD Workbench dataset-approval wording followed by review wording, and a pending workspace. Neither establishes effective access or a technical manifest. [Audit](../reports/continuity-20261104/REPORT.md). The expanded public K26 search found no attributable source table in the checked routes; this is not universal proof of absence. [Search](../reports/fig4d-source-search-20261104/REPORT.md).

K26 data request was sent with authorization on 03 November. Luis later supplied Fratta's reply anticipating availability the following week; that is not data delivery. No fresh mailbox inspection is claimed by this integration. A separate authorized A25 support message was sent on 04 November; culture identifiers remain unverified in the inspected files. [K26 communication](../reports/functional-rescue-20261103/COMMUNICATION_LOG.md), [A25 communication](../reports/asadollahi-fig3s-audit-20261104/COMMUNICATION_LOG.md). No automatic contact follow-up is authorized.

Broad research continuity stays paused. The separately requested one-time publication/data check for 09 November is not blanket authority for recurring searches, access requests or analysis.

## Completed bounded results

| Work | Project finding | Limit |
|---|---|---|
| A25 Fig.3s | 73 deposited observations reproduce 2/2 published means within prospective rounding tolerances: WT24.209923pC; R202H15.009117pC | Missing observation→culture/exclusions map; no inferential analysis, new biological replication or ALS rescue |
| ELK1 RNA-FISH | 60 image rows; 7/9 older summary ratios match; final-paper-linked archive confirms 240 intermediate rows and 84 numeric fields; extranuclear endpoint reconstructed | Two old ratios unresolved; no independent culture map or editorial point-identity certification; no functional rescue |
| UNC13A Dox | 138 rows, 42 groups; Python and actual R reproduce six missing SEMs from renamed join keys; key-preserving join changes no means | No biological pairing; UNC13B five-row versus declared n3 discrepancy; editorial numeric identity unverified |

[A25 report](../reports/fig3s-descriptive-20261104/REPORT.md), [UNC13A Dox report](../reports/fratta-dox-replay-20261104/REPORT.md). The experiments and models are not pooled or treated as directly comparable. [ELK1 final comparison](../reports/elk1-fish-replay-20261104/FINAL_ARTICLE_COMPARISON.md). All three bounded replays are closed computational results; do not rerun them as new tasks.

## Earlier closed results and deferred work

- UNC13A CTRL-4 pilot: completed, insufficient target coverage [1,0,0] against20; no control expansion/TDP run by default. [Closure](../reports/unc13a-control-annotation-20261103/CLOSURE.md).
- Regional annotation inventory:31/33 junctions; RefSeq clarifies a previously unannotated singleton, without new coverage or biological validation. [Comparison](../reports/source-gate-issue37-20261103/refseq-comparison/comparison.json).
- STMN2/PAPA: descriptive TPM→PPAU reproduced for12/12 libraries, not direct junction PSI or function.
- GEO/ENSG mapping and historical parser corrected; 1,901 support keys are not discoveries.
- GSE126542/GSE121569 aggregate/QC complete; audited DEXSeq bins do not directly measure the target cryptic regions; refit blocked.
- GSE122069 two controls complete; library→culture/batch/pairing map missing. Do not process remaining runs by automatic continuity.

GSE310723 has one library per condition; GSE315972 heterogeneous tissue is not i3Neuron replication. Do not halve uniqueCounts by assumption. SH-SY5Y alias/strand issues remain source-dependent. AGRN, CAMK2B, synthetic MEA and UNC13A post-deficit v0.4 stay deferred under [BACKLOG](BACKLOG.md). No neuronal rescue or clinical benefit has been demonstrated by our project.

## Operation

Preserve original source hashes, historical executors, reports and failures. CI must be read by exact commit and tested merge context; passing software controls does not reproduce every real-data analysis or establish biological validity. See [PROTOCOL](PROTOCOL.md), [MASTER_EVIDENCE](MASTER_EVIDENCE.md), [SCRIPT_LIFECYCLE](SCRIPT_LIFECYCLE.md) and [history](history/README.md).

No new contacts, costs, personal data, laboratory work, clinical instructions or external publication without specific authorization. No new equivalent molecular replay is scheduled.
