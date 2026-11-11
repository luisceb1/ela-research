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

Completed instead, as bounded documentary work: an intervention-chronology matrix over the six UNC13A intervention preprints, completed to 6/6 when Luis supplied the Mallika and Cao PDFs that neither Europe PMC nor bioRxiv would serve. **14 experiments; 1 post-deficit recovery; 12 prevention; 1 indeterminate.**

**The prespecified prediction is refuted**, by Mallika's AAV-PHP.eB-CTR arm: delivered at 6 weeks "when fine tremors are already apparent", at what the authors call a symptomatic stage, it maintained grip strength and extended survival from ~47 to ≥110 weeks (n=20 per group). CTR is a chimeric TDP-43 splicing repressor acting on many targets, **not a UNC13A-specific intervention**.

Split by specificity, the gap persists and sharpens: of **9 UNC13A-specific** experiments, **0** act after a measured deficit — all are preventive by construction. The UNC13A-specific arms also diverge by endpoint, failing for motor neuron disease ("preventing cryptic splicing of Unc13a is insufficient to attenuate motor neuron disease", Mallika) while preserving memory (Cao). The post-deficit window is therefore not intrinsically intractable in these models, which makes the UNC13A-specific question more pointed, not less.

A curation pass re-derived every row against the prespecified rule and verified all 14 locator quotations verbatim against the primary text (14/14, `scripts/verify_matrix_quotes.py`). It found and fixed four defects, including a bug in the verifier itself and three quotations I had joined with ellipses into sentences no author wrote, and corrected a hand count of target specificity. Because the prediction's fate turns on a judgement rather than a datum, the matrix now records both readings in separate countable columns: under the letter of the rule, which excludes a parallel untreated arm as baseline evidence, **0 of 14** are post-deficit and the prediction is **not** refuted; under the substantive reading, 1 of 14 is. Either way **0 of the 6 UNC13A-specific experiments** act after a measured deficit.

The curation is not independent review: the same agent did both passes, so it cannot detect a systematic bias of its own or a criterion that was ill-conceived from the start. That need stays open, with free routes recorded (peer review of Mallika/Cao; a bioRxiv comment, which would need Luis's express authorization). Mallika and Cao share a corresponding author and six authors, so they are not independent replications of each other. [Matrix and report](../reports/unc13a-intervention-timing-20261110/REPORT.md), [plan](plans/2026-11-10-unc13a-intervention-timing-matrix.md).

PMID 42983891 (Ikegami/Koike 2026, peer reviewed) was checked against the #37 gate and **rejected as a technical source**: qRT-PCR/ddPCR on post-mortem motor cortex, no junction counts, no RNA-seq/GEO/BAM, data by author request. Kept as context only: pathological subtype 2b shows higher UNC13A cryptic and truncated STMN2 RNA, correlated at Spearman ρ = 0.58. This does not open a fourth candidate.

The daily watcher's `long_reads` query searched all fields including reference lists (11,040 hits, unrelated papers); it is now restricted to TITLE_ABS (42 hits), with tests. This is a scope fix, not a quality filter.

## New bounded result — Ikegami source-data replay, 10 November

The deposited source data of Ikegami/Koike 2026 (*Acta Neuropathol Commun* 14:229, **peer reviewed**, open access) **reproduce their published statistics**. Group sizes match exactly (12/12/11, n=35); Spearman between UNC13A cryptic RNA and truncated STMN2 RNA reproduces at **rho 0.5737** against a published 0.58, inside the prespecified tolerance; subtype differences reproduce in direction and significance, Type 2b above Types 1 and 2a for both measures while Types 1 and 2a do not differ. A label-permutation control destroys the effect and disease duration does not account for it (rho -0.24 and -0.26, both non-significant), independently confirming the paper's own claim. The ddPCR/qRT-PCR concordance the paper calls "strong" is quantified here for the first time: rho 0.859 and 0.870 on 26 cases. [Report](../reports/ikegami-source-replay-20261110/REPORT.md).

A second bounded cycle screened the confounders with Table S1/S2 (35 cases). **RIN, post-mortem interval and semiquantitative neuronal loss do not differ between subtypes**, independently confirming two of the paper's own claims. **Disease duration does differ** strongly and in the expected direction (medians 32 / 19 / 11 months), so the subtype with most cryptic RNA has the shortest course; that is compatible with the paper, whose support is a non-significant duration-marker correlation, but with n=35 it is absence of evidence rather than evidence of absence. Age at onset differs nominally (Type 2b about ten years older) and does not survive Holm correction across the six covariates, so the paper's age-comparability claim is not contradicted at a corrected level. The discriminating test for H2 is **not executable from this deposit**: it carries no per-case pTDP-43 burden. Per-case covariate joins were refused because disease duration is not a unique key within Types 2a and 2b, the plan forbidding row-position joins.

This is internal reproducibility, not replication: same subjects, same measurements, same laboratory. It carries **no junction counts**, so **#37 stays blocked and this source stays rejected for that gate**. Post-mortem tissue is still not equated with i3N culture. The rho ~0.57 correlation across 35 human cases is the strongest observational support we hold for hypothesis **H2** (coordinated dysregulation across TDP-43 targets), and it agrees in direction with Mallika's experimental finding that correcting one target alone was insufficient. Correlation of two markers in the same tissue is not mechanism, causality or patient benefit.

The watcher extension found that **Guo's preprint is now peer reviewed** in *Science Translational Medicine* (PMID 42234776, DOI 10.1126/scitranslmed.aeb8517, 2026-06-03). It is paywalled with no PMC record, so its methods were **not** inspected: the two Guo rows of the timing matrix remain attributed to the 2025 preprint and may differ from the published version.

## Strategic routes — 11 November

Three routes were set out and acted on. **Snaptron/recount3**, the one route that could unblock #37 without money or third-party permission, was attempted and is **blocked by TLS**: the CONNECT tunnel succeeds once the host is allowed, but the server's certificate chain does not verify even with the proxy CA supplied, and verification was not disabled. The feasibility question is therefore **unanswered, not refuted**, and the prespecified stop rule forbade chasing alternatives inside that cycle. Opening a cycle on the recount3 file store instead needs its own scope decision and plan. [Report](../reports/snaptron-unc13a-feasibility-20261111/REPORT.md).

A **laboratory collaboration message** and the **structure of a commentary** are drafted and deliberately **not executed**: both are external and irreversible, both would carry Luis's name, and the commentary should wait for the independent review of row M-a that the watcher will surface for free. [Drafts](drafts/2026-11-11-borradores-pendientes-de-autorizacion.md).

Honest ceiling, recorded so it is not forgotten: with no laboratory, no budget and the raw-data pilot already closed at coverage [1,0,0], this project's realistic contribution is verification and synthesis of published work, not new biological measurement. Nothing here helps a patient today and nothing here supports any clinical decision.

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
