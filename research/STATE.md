# Current research state — 2026-11-04

This replaces earlier planning snapshots. Historical reports and commits remain evidence, not automatic instructions to rerun work. This consolidated state accompanies integration of PRs #46–#49. Review details and exact checked commits are preserved in [INTEGRATION_REVIEW](../reports/integration-20261104/REVIEW.md).


## Paired STMN2 completed — 11 November 2026

[Paired exploratory report](../reports/paired-stmn2-20261111/REPORT.md), protocol committed before pair counting and effect calculation (marginal outcomes were already known). The dual-source technical subset has 104 shared donors; after pure-ALS status, matching preparation, unique library and C+K≥20 in both regions, **45 donor pairs** remain. Cervical higher/tied/lower: **24/14/7**; median paired local-ratio difference **+0.003676**; one prespecified exact two-sided sign-test nominal p=0.0033269. Direction persists descriptively at denominators ≥50 (32 pairs) and ≥100 (22 pairs). Only four eligible control pairs: no disease-vs-control test.

The paired-design task previously listed below is now **completed**, not a pending instruction to rerun. This reduces between-person and recorded preparation mismatch, but does not resolve extraction/sequencing batch, RNA quality, composition, discrete-depth bias or selection on denominator. It is neither independent replication nor proof of neuron-type dependence. Next enabling input: a concrete independent paired manifest with composition/QC/batch information and usable junction coverage. Stop this cycle rather than add contrasts on the same donors. UNC13A #37 and K26 #44 gates remain unchanged.

## Current override — STMN2 measurement and technical units, 11 November 2026

[Completed bounded audit](../reports/stmn2-map-audit-20261111/REPORT.md) supersedes older STMN2 claims below about unavailable donor identity, P1 confirmation, inference from Wilson overlap, and coverage ruling out confounding. No original counts were changed.

- The sealed exon-1→2a junction is retained: direct hg38 literature and UCSC chain support the acceptor. A one-base difference at the terminal exon counting endpoint does not change the junction. The assay is a local junction-use proxy and cannot resolve alternative polyadenylation endpoints.
- Exact region-scoped recount keys recover 293/313 library→declared-donor links: cortex 140/149, cervical 153/164. There are 128 shared donors across regions (all groups), 164 unique donors in the mapped union, and one cervical donor with two samples. The four pure-ALS cervical K≥20 samples are four declared donors. Two metadata routes agree on all 246 overlapping library links; four original GEO spot checks agree. This is partial technical design recovery, not independent cohort replication.
- P1 ≥10x canonical coverage is **not met**: per-input-read normalized median ratio 8.085 (sensitivities 7.782/7.769), raw ratio 6.6. The cervical ALS C+K≥20 ratio summary is n=58, median 0.005684, max 0.543860; including all nonzero denominators gives n=92 and max 1.0. No new inferential biological test was performed.
- Next bounded scientific task: fix a single paired STMN2 cortex/cervical protocol, verify library-preparation/batch compatibility, define coverage-based eligibility and multiplicity handling, then count eligible pairs before any effect. K=0 controls remain eligible if their total denominator is adequate. This task is distinct from the unchanged UNC13A #37 gate and functional K26 #44 request.

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

## recount3 breakthrough and its limit — 11 November

**Issue #37's measurement blocker is solved as a capability.** All four candidate families were rejected for want of accessible junction counts; recount3 publishes them already quantified. For 24.5 MB and no cost, the project now holds exon-exon junction counts for a TDP-43 depletion experiment in human neurons, with conditions **declared by the deposit** rather than inferred, and no FASTQ or alignment involved. The probe is written and tested, so applying the same route to another project costs minutes and a few megabytes. [Report](../reports/recount3-unc13a-20261111/REPORT.md).

**The dataset inspected does not pass the gate.** SRP166282 is Klim 2019, whose data #37 had rejected through Irwin for lacking linkable junction counts; recount3 supplies them. Design reconstructed from declared metadata: 6 TDP-43 knockdown against 12 controls, both batches containing both conditions, **but a single cell line (HUES3)**, so replicates are independent cultures and not genetically independent donors. All three sealed target junctions match **exactly**, the coordinate-convention guard passes, and the annotation pattern is as the biology predicts: canonical annotated, both cryptic not.

Coverage decides it. The canonical positive control is measured in 18/18 samples at up to 66 reads, so measurement is not the failure, yet the cryptic junctions reach a maximum of **5 reads against the prospective minimum of 20**, and `gate_met` is false with the positive control excluded from the gate. **Rejected on coverage**, cause isolated to depth at the locus.

Recorded as an observation strictly below threshold and carrying no inference: every cryptic read seen is in a knockdown sample, none in the 12 controls. At a maximum of 5 reads those zeros are **missing data at this depth, not biological zeros**; no PSI, p-value or effect is computed, and the minimum of 20 is not relaxed.

Next discriminating step: UNC13A is expressed lower in spinal cord than cortex (Ikegami 2026, Mallika's GTEx panel), and these are spinal motor neurons, so a cortical or i3Neuron depletion dataset is the natural candidate. ANSWER_ALS and TARGET_ALS are in recount3 but are **patient cohorts, not depletion experiments**, so using them would answer a different question and needs its own plan; the endpoint is not switched to dodge this rejection.

## Second recount3 candidate — amplicon, not eligible

SRP334561 (GSE182976) is Ma 2022's own dataset for the UNC13A cryptic-exon paper, fixed as the candidate **before any count was extracted**. Its design is better than Klim's: `shTDP-43` against `shScramble` across **three donor lines**, so three genetically independent units per condition, which SRP166282 lacked. Coverage clears the threshold enormously, up to 57,709 reads on a cryptic junction, with complete separation — cryptic fraction 0.000–0.002 in six controls against 0.390–0.690 in six knockdowns, consistent across all three lines.

**The gate still is not passed, and the prespecified rule is why.** The plan fixed in advance that clearing the threshold in a targeted assay does not demonstrate transcriptome-wide detectability, and required verifying the assay against the publication first. Ma 2022 states the deposit is **amplicon sequencing**, by RT-PCR from UNC13A exon 19 to exon 21, while SRA metadata labels it `library_strategy: RNA-Seq`. So this is depth at one locus, not coverage: not comparable with the closed pilot or SRP166282, and it does not enable #37's inferential contrast. What it does establish is an independent reproduction of the published qualitative finding from deposited counts.

The probe now detects this trap itself: 43 junctions with 76.7% on chr19 across 6 chromosomes flags as targeted, against 599,768 junctions and 5.7% across 77 chromosomes for real RNA-seq. A heuristic that forces verification, not a substitute for it.

**The cortical hypothesis remains untested** — both datasets are motor neurons. And a reusable caution is recorded: SRA's library_strategy field can misdescribe a targeted assay.

## Brown 2022 ruled out, and an open discrepancy that reframes #37

Brown 2022 was ruled out **from its own data statement**, before touching any data. Everything it deposited is targeted or another assay entirely — Riboseq, targeted RNA-seq, two iCLIP sets, targeted nanopore — and of what it reused, the only whole-transcriptome source is GSE121569, which resolves to SRP166282, the Klim dataset already rejected on coverage. Its cortical candidate, GSE126543, has no SRA records at all. So Brown cannot test the cortical-depth hypothesis, which **remains untested** across all three candidates examined. This was not an exhaustive search of recount3: specific accessions from the two defining papers were checked, and no claim is made that no suitable dataset exists.

Worth noting: both papers that **established** the UNC13A cryptic exon deposited targeted assays, consistent with the junction being hard to see in whole-transcriptome RNA-seq at ordinary depth.

**The finding that matters most is a discrepancy between the two sources.** In knockdown samples the cryptic fraction is **0.000–0.145** by Klim's whole-transcriptome RNA-seq and **0.390–0.690** by Ma's amplicon — four to five fold apart. A fraction is depth-independent, so coverage does not explain it. Candidate explanations, none tested here: knockdown efficiency (siRNA against shRNA), amplification bias in the amplicon assay, cell line or type, recount3's junction filters, or read length and mappability in 2013-era data. It is recorded as an open inconsistency and is not averaged away.

This reframes the gate. At Klim's fraction (~0.10) and canonical coverage (~60), reaching 20 cryptic reads would need roughly **200** reads on the canonical junction; at Ma's fraction (~0.5), about **40** would do. So whether the threshold of 20 is reachable in public RNA-seq **depends on which fraction is real**, which is exactly what is unknown. The prior question is no longer "is there a deeper dataset" but "what is the true cryptic inclusion level". Whether to reorient #37 towards resolving that is a **scope decision for Luis**; the agent does not change the threshold or the question on its own.

## #37 reoriented, and the discrepancy is bounded rather than resolved

Luis reoriented #37 on 11 November towards arbitrating the cryptic-fraction disagreement. The threshold of 20 is **not changed**; its use as a source-acceptance criterion is suspended until the disagreement is arbitrated. [Report](../reports/unc13a-fraction-discrepancy-20261111/REPORT.md).

**The main finding is that the two measurements are not comparable as PSI estimates.** The amplicon nature of SRP334561 is now confirmed by a second, independent route: at gene level its twelve samples detect only 8 to 17 genes, **one gene carries 100% of the counts**, and the modal fragment is 1,508 bp, the size of the exon 19 to 21 PCR product. Klim's project, by contrast, detects 29,646 to 36,965 genes with a top-gene share of 1.6%. So one figure is a junction fraction over a transcriptome and the other a proportion of products within one amplicon; the "discrepancy" is in large part an artefact of comparing two non-equivalent assays.

**Knockdown efficiency is measured on one side only.** In Klim's deposited gene counts TARDBP falls 58.8% (CPM 132 to 54), so **roughly 41% of TARDBP remains** — a partial knockdown, compatible with low cryptic inclusion without demonstrating it. For Ma the script **refuses** to read a knockdown level off an amplicon library, as the plan required, and the paper does not state one in its accessible text, which the plan required to be recorded as unavailable rather than estimated. The prespecified prediction, that Klim's knockdown would prove substantially weaker than Ma's, is therefore **not testable** and is neither confirmed nor refuted.

By-product verification: STMN2 falls 51.8% in the same counts, independently reproducing Klim 2019's headline finding, which was not this cycle's aim.

No explanation is ruled out or demonstrated. What the cycle does yield is a sharper entry requirement for #37: whole-transcriptome RNA-seq, with **documented depletion efficiency**, deep enough at UNC13A (of the order of 200 canonical reads if the fraction is near 0.10), and with at least three independent biological units per condition. The second criterion is new, and without it a low fraction cannot be told apart from a weak knockdown.

## TARGET_ALS motor cortex: the cleanest empirical result so far, and why the gate is unreachable

A fourth cycle, on patient tissue rather than culture: TARGET_ALS motor cortex via recount3, **149 samples**, 194 MB against a 400 MB budget. Every setup control passes — not a targeted assay (2.7M junctions across 127 chromosomes), the convention guard holds, all three sealed junctions match exactly, annotation pattern as predicted. [Report](../reports/target-als-cortex-20261111/REPORT.md).

**The cortical expression hypothesis is supported:** canonical coverage runs at a median of 102–148 reads per sample against 7–66 in Klim's spinal motor neurons, so UNC13A is two to three times better covered in motor cortex.

**Clean qualitative separation: 23 of 109 ALS-spectrum samples (21%) carry cryptic reads; 0 of 17 non-ALS samples carry any** — and the controls have *better* canonical coverage (median 148), so their zero is not a depth artefact.

Of the three prespecified predictions, **P1 is refuted** (0 of 149 samples reach 20 cryptic reads) while P2 (median fraction below 0.10) and P3 (higher in ALS) are confirmed.

**The arithmetic explains the repeated failures and is the cycle's main contribution.** Depth is no longer the limit; the *fraction* is. At a fraction of 0.08 reaching 20 cryptic reads needs about 250 canonical reads, and at 0.02 about 1,000 — two to ten times the locus depth of one of the largest ALS cohorts in existence. The cause is biological dilution: bulk tissue is mostly cells without nuclear TDP-43 loss. More samples cannot fix it; cell enrichment or a targeted assay could.

**Third datapoint on the discrepancy: the amplicon is the lone outlier.** Two whole-transcriptome measurements now agree in order of magnitude — Klim's culture at 0.000–0.145 and patient cortex at 0.000–0.0796 — across different labs, decades and systems, against the amplicon's 0.390–0.690. This does not prove the amplicon biased, since each transcriptome source has its own downward-bias explanation, but it shifts the burden of proof onto the single high figure.

No novelty is claimed: the consortium has published on these data and Ma 2022 carries a supplementary table on UNC13A and STMN2 variants in the NYGC cohort. Personal data: only the subject-group column was read; sex, ethnicity, ages and site of onset were not read, no individual clinical row is in the output, and the metadata file is not versioned.

## Cervical cord against motor cortex: 21x less UNC13A coverage at identical depth

The cortex report was corrected the same day after **the project's first independent review**, which Luis obtained from a second reader. It flagged four overstatements; I checked all four and all four were right. Library depth explained most of the coverage difference I had called evidence of cortical expression. The ratio double-counted inclusion, because a transcript carrying the cryptic exon offers two junctions a read can span while one without it offers one, so the maximum fell from 0.0796 to 0.0414 and the per-junction maximum is **four reads**. Cell dilution is now stated as the most plausible explanation rather than a demonstrated cause, and the closing claim is narrowed to the datasets examined. Verification also established that **the metadata exposes no donor identity**, so tissue comparisons cannot be paired.

The cervical cycle then ran with that corrected design. [Report](../reports/target-als-cervical-20261111/REPORT.md), table in `tissue_comparison.tsv`.

**Sequencing depth is identical between tissues** — median 44.4M exon-assigned reads in both, ratio 1.00 — which removes the confounder that invalidated the earlier cross-study comparison. With depth matched, **UNC13A canonical coverage is about 21 times lower in cervical cord than in motor cortex** (0.11 against 2.30 per million in ALS). All three predictions are confirmed: lower normalised coverage, lower detection (0.053 against 0.190, Wilson intervals just failing to overlap), and no sample reaching twenty reads on a single cryptic junction.

This retrospectively explains the project's failures: **the closed pilot and the Klim dataset were spinal motor neurons**, the tissue where this locus is worst covered. Not bad luck — the wrong tissue for the locus.

Two things it does **not** show. The lower detection in cord needs no difference in biology, since it is what 21-fold less coverage produces on its own. And in cord no ratio is interpretable at all: with a canonical median of 5 reads, the apparent high PSI values are one cryptic read over two canonical, which is sampling noise.

**Conclusion, as prespecified:** of the five datasets examined none reaches the threshold, so **this search closes for lack of precision with the data examined**. No claim is made about all public RNA-seq. What is established is where not to look, and that the route to the threshold is cell enrichment or a targeted assay rather than more samples or more depth.

## STMN2 passes the coverage threshold: the failure was the locus, not the method

The coverage search had closed for UNC13A. This cycle changed gene rather than reopening it, on a measured basis: in Klim's motor neurons STMN2 runs at CPM 2,145.6 against UNC13A's 178.5, twelve times higher. [Report](../reports/stmn2-derivation-20261111/REPORT.md).

**Coordinates were derived, not improvised.** Two independent features of NM_007029.4 — the exon 1 end and the exon 2 start, read from UCSC's ncbiRefSeq in both assemblies — give the **same** offset of 912,235, which places the published hg19 cryptic-exon interval at hg38 79,616,822–79,617,049. The observed junction chr8:79,611,215–79,616,821 puts its acceptor exon start at exactly 79,616,822, and the canonical junction matches the transcript's exon boundaries exactly. Sealed in `research/references/stmn2_targets_sealed.json`.

**My own prespecified criterion was wrong and the cross-check caught it.** The plan required `annotated=0` for the cryptic junction; the true junction is flagged `annotated=1` in recount3's reference set, so the criterion would have excluded it. Five `annotated=0` candidates did pass every structural check and none is the published event. Stopping before measuring, as the plan required with more than one candidate, is what prevented measuring an arbitrary junction and calling it STMN2's cryptic exon.

**The threshold is passed for the first time in this project.** In cervical cord, 4 ALS samples reach 20 or more cryptic reads (21–52 reads, PSI 0.148–0.544 on solid denominators), and detection is 48 of 95 against 1 of 13 controls, with Wilson intervals that do not overlap. So the repeated failure with UNC13A was **the locus, not the method or the access**.

**The signal sits where the biology predicts, and it mirrors UNC13A.** Motor cortex holds 19 times more canonical STMN2 coverage than cervical cord and still shows fewer cryptic junctions (31 of 84) and far lower PSI (max 0.029 against 0.544), which a coverage difference cannot explain. **No discovery is claimed**: STMN2 truncation in ALS cord is among the field's most replicated findings, and this is reproduction with adequate coverage.

No effect is computed: 4 samples above threshold in ALS and none in controls, with no donor identity, so an inferential contrast needs its own prospective design. Ratios were read only where cryptic plus canonical reached 20, since 25 of 95 cord samples have canonical below 10 and their apparent PSI of 1.0 is two cryptic reads over zero canonical.

Next: UNC13A's own sealed coordinates came from an earlier derivation and **should face the same double-anchor cross-check**, since its `annotated=0` assumption may have been wrong too.

## UNC13A's coordinates audited and confirmed: 88 of 88 boundaries agree

Because the STMN2 cycle showed a prespecified criterion of mine could exclude the published event, UNC13A's sealed coordinates were put through the same double-anchor cross-check they had never faced. [Report](../reports/unc13a-coordinate-audit-20261111/REPORT.md).

All **88** exon boundaries of NM_001080421.3 give a single offset, 110,809, with no exception, so the region lifted between assemblies without structural change. Applying it to the published hg19 cryptic-exon interval yields **17,642,414–17,642,541**, exactly what the sealed junctions imply, and the canonical intron begins one base after a real hg38 exon end and finishes at a real exon start. The offset was written into the plan **before** querying UCSC, so this was a checked prediction rather than a fitted adjustment.

**Coordinates unchanged; none was needed. No measurement from this week is affected** — the recount3 reports, the fraction discrepancy, motor cortex and cervical cord all measured the right junctions, and the coverage closure for UNC13A stands on locus coverage rather than a coordinate error.

One methodological lesson does change practice: UNC13A's cryptic junctions are flagged `annotated=0` in recount3 while STMN2's is flagged `annotated=1`, so **that flag is inconsistent across genes and unreliable in either direction**. Using it to include would have failed for UNC13A; using it to exclude did fail for STMN2. What worked in both cases was cross-checking a published interval through a double anchor, and the note is recorded in the sealed files so no future cycle leans on the flag again.

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
