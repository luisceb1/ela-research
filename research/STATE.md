# Current research state — 2026-11-04

## Local disabled descriptor prepared on user host — 12 November 2026

Luis supplied a successful terminal summary from the pinned `4fa5346` preparer: 9 index members, 4 input-file entries and zero raw bytes downloaded; descriptor SHA256 `97a578839d72088bab1403b0c9ef6bd9b8e3ff064bbe3008314fb34545b6af26`. [Receipt and limits](../reports/local-raw-feasibility-20261112/user-prepared-summary.json). Full descriptor bytes have not been inspected by the agent. Resource/assay/runner gates remain unresolved. GEO documents fastp adapter trimming followed by STAR; a future HISAT2 count workflow must document its differences and processing parameters. Local fastp installation/version confirmation is the next setup step. No sequencing transfer or old-pilot activation is authorized by this receipt.

## Local index hash check and disabled preparation — 12 November 2026

Luis's nine reported index hashes match the historical record (8 HISAT2 members plus make script). An [offline preparer/runbook](runbooks/2026-11-12-gse252892-offline-preparation.md) rechecks current local files and writes a disabled descriptor for four fixed GSE252892 FASTQs; no raw execution path or transfer is implemented. Existing tool versions are user-reported. See [comparison and limits](../reports/local-raw-feasibility-20261112/user-index-check.json). Full successful host preparation, resource benchmark, assay/reference review and bounded runner remain pending. No old pilot is reactivated.

## Local raw-data feasibility inventory — 12 November 2026

Luis selected a local-computer route and supplied WSL tool/version evidence. A prospectively bounded [inventory](../reports/local-raw-feasibility-20261112/REPORT.md) prefers previously known **GSE252892 for preparation only**: six total-RNA libraries advertise 12 FASTQs / 40,589,186,698 compressed bytes. The provisional first control/KD inputs advertise four files / 12,826,593,031 bytes; no transfer is authorized/executed by the inventory. GSE299341 advertises 40 files / 86,561,386,307 bytes; unresolved processing/efficacy and one 358,774-byte library remain recorded. Two ENA metadata requests used 36,284 bytes; zero raw/count transfers. This is not independent-donor validation, a KD effect or a reopened #37/#44/STMN2 cycle. A separate hash-locked runner and resource/transfer/stop budget must precede any approved raw execution. Current index integrity, primary-to-library depletion linkage and peak local resources remain unverified. AD workspace/dataset access and author replies are unchanged.

## PR #53 integrated for review — 12 November 2026

The historical subtype-conditioned Ikegami cycle is now included: pooled rho 0.57367, adjusted rank rho 0.31669, stratified two-sided permutation p=0.07825 and marginal bootstrap 95% interval [-0.02342, 0.62758], using the same 35 cases. The fixed prediction was not met; absence of association, subtype heterogeneity and mechanism are not established. This is internal reproduction, not independent validation. No new fit or raw-data acquisition was performed during integration. [Result](../reports/ikegami-subtype-conditioning-20261110/REPORT.md), [integration/validation](../reports/pr53-integration-20261112/REPORT.md).

The fixed three-source paired-marker screen admitted no new source. The authorized Quadros request was recorded as sent on 11 November; no reply/data receipt is verified in this integration. Earlier unsent wording below is historical and superseded by its communication log. No reminder or fourth candidate is scheduled.

The early 11 November Keuss publication check below is historical: final source data and the conditional replay were subsequently integrated through #60–#62. #44 and #37 are closed; strict v1 and biological-unit clarification remain unresolved. No source search, model sweep or equivalent replay is reopened. The prior seven report translations retain their pinned scope; current English findings now include this result.

PR #51 is closed unmerged as not currently planned, with its branch retained. Reconsider agent infrastructure only for a concrete accepted task and separately authorized execution/budget; no live API workflow is integrated here.

## Interpretation review and access update — 12 November 2026

The [bounded review](../reports/nov12-interpretation-review-20261112/REPORT.md) corrects the GTEx window rationale, withdraws the canonical-count upper-bound claim and limits the spinal/laser-capture conclusions to the inspected observations. Numerical outputs, thresholds and prospective plans are retained. This is a documentation/committed-output check, not a re-run of the original sequencing inputs.

**AD Workbench:** Luis supplied a support reply headed “Fwd: New Workspace Request received.” Support states that the request was received and is under review. This is user-reported correspondence, not a mailbox/portal verification; approval, active workspace and dataset access remain unconfirmed. The reply's timestamp was not supplied. No duplicate request or reminder is scheduled. Luis reports no other updates; no new Fratta/Wong reply is claimed.

**Next step:** await a concrete author clarification or verified workspace/dataset inventory before a new prospective data task. The old `codex/unc13a-single-background-A-20261112` protocol branch is superseded by the integrated availability/detection work; no merge or deletion is needed for this review. Closed cycles remain closed.

## Two loose ends closed — 12 November 2026

[Verification report](../reports/loose-ends-resolved-20261112/REPORT.md). No new biological measurement.

**SRP166282 re-run done with the real bytes.** All five recount3 inputs re-fetched and both SHA256 and byte size reproduce the values recorded in November, so the earlier result rests on inputs still reproducible exactly. Re-running the fixed probe over them gives output in which **every field shared with the committed result is identical** — `per_junction`, `verdict`, `samples`, `matrix_header`, `assay_shape`, `inputs`, `n_samples` and `project` — with the single added key `targets_provenance_project`, the documented schema change. PR #66's deferred equivalence check is closed against real data rather than a fixture.

**SRP334561 label resolved as far as the repository allows.** The sealed targets file has exactly two commits, `afa84bb` and `83cf23a`, and **both carry `SRP166282`**; no second UNC13A targets file was ever committed. The label therefore came from an uncommitted artifact — an ad-hoc targets file or a manual edit — and **which cannot be determined**, so the uncertainty stands rather than being resolved by assumption. Three things can be stated: the **committed seal was never broken**, so the earlier suggestion that it was is withdrawn; the measurement is unaffected, since the probe never read `project` for measurement and the recorded input hashes are SRP334561's own files; and it cannot recur, because the label now comes from a required `--project-id` with a regression test. The residual item is a documentation gap in that November cycle, not a data-integrity problem.

## Non-ALS spinal cord search: baseline already existed, new source fails its control — 12 November 2026

[Search and measurement](../reports/nonals-spinal-source-20261112/REPORT.md), under the [plan committed before any query](plans/2026-11-12-nonals-spinal-cord-source.md) at `6906a58`.

**Correction:** after the gtex cycle I said the published cervical measurement had no non-ALS baseline. Wrong. The [cervical report](../reports/target-als-cervical-20261111/REPORT.md) already carries **13 non-neurological controls per tissue, same cohort and pipeline** — cervical controls canonical median 8, detection 0/13 — which is *stronger* than the external GTEx comparison because it avoids the cross-study weakness. Its limitation is n and depth, not absence.

Index-first search: three queries, 107 human SRA studies, **24 held by recount3**, of which exactly **one** is non-ALS post-mortem spinal cord tissue. SRP097615 (laser-captured motor neurons from control subjects: 12 spinal, 20 oculomotor, 7 Onuf's) is not prior work and is biologically ideal, since laser capture enriches the cell type at issue.

**It fails its positive control.** The canonical junction is absent in all 39 libraries. No conclusion about cryptic absence follows. Catalogue size differs across studies and sample counts; it neither measures standardized library complexity nor isolates laser capture as the cause. See the corrected source report.

Prediction not refuted, and exceeded in the unfavourable direction: median canonical 0 in all three neuron populations.

**What remains:** TARGET_ALS supplies a same-cohort cervical control, with the reported n/depth limits. No better source was identified in the finite search. The failures in the examined deposits do not establish a universal public-data or tissue limit; deeper sequencing, other preparation or another source remain possible routes, not proven solutions.

## Non-ALS background measured: cryptic junctions absent in the fixed window — 12 November 2026

[gtex BRAIN control](../reports/gtex-brain-negative-control-20261112/REPORT.md), under the [plan committed before any download](plans/2026-11-12-gtex-brain-negative-control.md) at `b2ff4f2`, which fixed the comparability window in advance. 2,931 libraries, 9,484,210 junctions, 2.8 GB.

**In the 26 libraries with canonical coverage in the prespecified canonical window (102–148), both sealed cryptic junctions carry zero reads.** Fifteen of the 26 are cortical. Across all 2,931 libraries cryptic reads appear in 7, maximum 2 reads, all outside the window. Canonical control measured in 2,655/2,931, maximum 286.

The fixed GTEx subset has zero cryptic counts. The original table interpreted this as ALS counts above background, but the 102–148 window uses two group medians rather than the ALS per-library range. That label does not establish matched coverage or an ALS-versus-background difference. The counts and window are preserved; the stronger interpretation is withdrawn.

**GTEx supplies no cervical library in the fixed window.** This does not remove the existing TARGET_ALS same-cohort cervical control. The earlier statement that no non-ALS baseline existed is withdrawn.

**Within GTEx:** cervical median canonical coverage is 1.0 versus cortex 15.0. This repeats the direction outside TARGET_ALS but does not isolate a tissue-intrinsic cause or rule out composition, preparation and mapping differences.

No p-value, no ALS-versus-GTEx test, no pooling. #37, the 20-read minimum and the three-background question are untouched.

## recount3 non-SRA collections inventoried; the gap is a control, not a source — 12 November 2026

[Catalogue inventory](../reports/recount3-collections-inventory-20261112/REPORT.md), listing only: no junction counts, no coverage, no new candidate accepted.

**Correction:** a previous session summary called `TARGET_ALS` uninspected. It is not — two prespecified cycles already used it via recount3 ([motor cortex](../reports/target-als-cortex-20261111/REPORT.md), [cervical](../reports/target-als-cervical-20261111/REPORT.md)). `ANSWER_ALS` is genuinely uninspected and was already an open backlog item.

Holdings: ANSWER_ALS 2,229 samples / 4 releases; TARGET_ALS 683 across 5 tissues, of which motor medial 148, lumbar 147 and thoracic 75 are untouched; gtex 19,214 (BRAIN 2,931); tcga 11,348 (irrelevant); ega 8,783 including SPORADIC_ALS_EGAD00001006022 at 19; LIBD 1,203 brain.

**The useful gap is a missing control, not a new source.** The project has counted UNC13A cryptic reads in ALS cortex (1–4 per positive sample) but has **never measured that locus in non-ALS brain at comparable depth**, so those counts cannot be distinguished from assay background. gtex BRAIN and LIBD are that baseline and are reachable by the existing probe. This would qualify a result already held; it is not a source for #37 and must not be presented as one.

Unverified and required before any plan: per-collection junction file sizes (TARGET_ALS cortex was 194 MB for 149 samples, so gtex BRAIN likely needs a subset), and access terms for ANSWER_ALS and the EGA set. TARGET_ALS's three remaining tissues are the weakest lead: donor identity is not exposed in that cohort, so more samples are not independent donors.

#37, the 20-read minimum and the three-background question are untouched.

## Question A detection measurement: no sufficient cryptic support — 12 November 2026

[Measurement on SRP069787](../reports/questionA-detection-SRP069787-20261112/REPORT.md), under the [amendment committed before any count was downloaded](plans/2026-11-12-questionA-amendment-detection-floor.md) at `daf9d24`, which fixed every outcome reading in advance. Luis authorised relaxing the replicate floor from three to two, for this deposit and for detection only.

**Both sealed cryptic junctions are absent from the project's junction catalogue: zero reads in all 16 libraries.** The canonical positive control is measured in 16/16, maximum 26. Per the prespecified table this reads as **missing data at this depth, never a biological zero**; Question A closes for this deposit. No PSI, fraction, effect, interval, p-value or knockdown-versus-scramble comparison was computed.

**After the authorized replicate-floor amendment**, the KD libraries have canonical counts 9 and 2 and zero cryptic counts. The fixed cryptic support gate remains unmet. Canonical counts are not an upper bound on cryptic counts; the previous impossibility claim is withdrawn. Low coverage is a warning, not an identified sole cause, and replicate count remains a separate design limitation.

Incidentally, this is the first new project measured since PR #66: the output reports `project: SRP069787` with provenance `SRP166282` in its own field, where the pre-fix probe would have mislabelled the whole file as the rejected Klim dataset.

The 20-read minimum was applied as written and is not lowered now the result is known. #64's three-background result is untouched. #37 stays closed; nothing nominates a design review.

## Index-first search finds no eligible source; the constraint moves to replicates — 12 November 2026

[Index-first screen](../reports/recount3-index-first-20261112/REPORT.md), plan committed at `6318d6d` before the first query. Three queries gave 42 SRA studies; **12 are held by recount3; zero are unaudited neuronal TDP-43 depletion experiments with three or more replicates per arm.** Only two of the twelve are prior work: the other ten were never eligible, so the earlier source gate did not miss accessible material.

Three screens have now failed for three different reasons — genetic background (PR #64), recount3 holdings (PR #67), and now **replicate count**. The two projects with the right model and contrast, SRP069787 (iPSC motor neurons, declared TDP43 Knockdown vs Scramble) and SRP169127 (SH-SY5Y shRNA), have **two** biological replicates per arm, a 2016-era norm in a catalogue built in 2019. Depth was never tested in this screen.

**Historical decision, subsequently taken:** Luis authorized the detection-only amendment for SRP069787, now measured and closed as recorded above. This is no longer a pending scope decision; no inference from two libraries or new source is authorized.

No coverage measured, 20-read minimum neither applied nor relaxed, three-background question untouched. Not a claim that no public junction counts can answer Question A, nor about other recount3 collections or non-recount3 routes. #37 stays closed; nothing nominates a design review.

## recount3 availability closes Question A candidates — 12 November 2026

[Availability check](../reports/recount3-availability-check-20261112/REPORT.md): **GSE252892 (SRP482832), GSE299341 (SRP590954) and GSE298758 (SRP589302) are all absent from recount3**, so Question A closes for them before any coverage question. The two already-measured projects are present with run counts matching their recorded results exactly, which is the lookup's positive control.

recount3's human SRA index holds 8,103 distinct projects and is overwhelmingly its 2019 build: about 125 projects were added across 2021-2025, latest `date_processed` 2025-09-26. The capability recorded earlier stands — junction counts without FASTQ or alignment — but its **catalogue is nearly static**, so recent deposits are reached only by exception. Not a claim about future updates, other recount3 collections or other access routes.

**Process correction:** the Stage A screen selected candidates from GEO that recount3 could never have measured. Any future recount3-based screen must intersect the project index **first**, then inspect design and efficacy metadata for survivors. Stage A's design observations are unaffected.

Question A is closed for these candidates on availability, **not answered**: no cryptic coverage was measured in any new deposit. The 20-read minimum was neither applied nor relaxed. Question B's negative result stands as recorded. #37 remains closed; nothing here nominates a design review.

## recount3 Stage A completed — 12 November 2026

Luis authorized the metadata-only stage after PR #64's prospective plan. [Query lock](plans/2026-11-12-recount3-stageA-query-lock.md) committed at `3bbc9326a926a77e6224600a8250e189d5c679b3` before discovery. [Completed report](../reports/recount3-metadata-stageA-20261112/REPORT.md): five queries reached the 30-series cap, 39 successful metadata/text responses, 636,037 received body bytes. Zero sources nominated under the proposed three-genetic-background rule. WA01/WTC11 sources fail that rule; DCPS remains unresolved for exact RNA-seq background linkage and is archived without active follow-up. Full decisions, 26 culture-library metadata records and empty Stage B manifest are deposited.

Stage A is closed; no sixth query or additional source expansion. No junction counts, coverage measurement, PSI, effects or models. recount3 availability itself was not established for rejected sources; earlier design gates failed. The zero nomination result does not establish biological absence or test the coverage expectation. Stage B remains unauthorized; #37/#44 and the closed STMN2 cycle are unchanged. The prior “proposal only” wording below records chronology, not a current instruction to restart selection.

**Interpretive review — 12 November:** zero meets the new three-background criterion; zero sources were rejected on measured depth. In the four focal neuronal depletion records, GSE252892 (WA01), GSE307054 (WTC-11) and GSE299341 (WTC11) fail that rule, while GSE298758 has unresolved background linkage. **A: single-background measurement reproduction in separate experimental observations is untested; B: cross-background reproducibility lacks an accepted source in this finite screen.** A single background need not disqualify A, but culture independence, efficacy, batch and recount3 linkage still need review. Neither A nor B is selected or launched; B is not proven permanently inaccessible. [Scope distinction](../reports/recount3-metadata-stageA-20261112/INTERPRETATION_REVIEW.md).

## Bounded independent post-deficit source screen — 12 November 2026

[Completed documentary screen](../reports/independent-postdeficit-screen-20261112/REPORT.md), prospectively committed at `bac77055aa0e7eaaab9cced0513ef1cbb19819d5` from verified main `d09203c8546f3cca7bfeb54911eb322d3451404a`: three screened primary records, not three independent validation families; four original query groups; zero accepted for a validation-analysis protocol. Walker 2015 and Huang 2012 are relevant TDP-43 transgene-suppression recovery experiments, not isolated STMN2/UNC13A correction; numeric longitudinal unit/control linkage remains unverified. Matson 2026 v1 is discarded at abstract triage: the complete API abstract describes depletion/stress recovery rather than an eligible restorative intervention. The API is accessible and was omitted initially; full methods remain uninspected. Walker/Huang are archived prior art, not active waiting leads. Hur 2022 is a related-family check, not another independent candidate. [Traceable table](../reports/independent-postdeficit-screen-20261112/candidates.tsv).

This finite search is closed, not a claim that no suitable experiment exists. No effects, new tests of biological hypotheses, contacts or mass downloads. Reconsider only upon a concrete eligible artifact; do not pursue a fourth candidate. #37/#44 and the 45-donor STMN2 cycle are unchanged. Luis reports no active AD Workbench workspace; no new portal or mailbox check is claimed. Existing Wong/Fratta communications remain awaiting substantive clarification, without automatic follow-up.

## Authorized closure and Wong contact — 12 November 2026

Luis authorized both the Wong email and closure of this computational cycle. PRs #60 and #61 are merged; the reviewed scientific baseline is `f312d3cf41fe6f2ace004f4a05fc893e6bc5abed`.

**K26 Fig.4d conditional replay is closed.** The favorable ASO−KD direction is reproduced under the stated source-block assumptions; the published ASO star band remains unmatched, its cause unresolved. Block heterogeneity and the post-hoc ASO−Control comparison do not establish complete rescue or equivalence. This is reuse of the same observations, not independent biological validation. Strict v1 remains disabled. No further transformations, model sweeps or thresholds on these observations are scheduled.

Reopen only for concrete author clarification of biological nesting/panel execution, a corrected primary source, or an independently eligible dataset after a new prospective design review. Issue #44 may close as completion of this bounded computational task, not satisfaction of strict v1 or resolution of the star discrepancy. The separate STMN2 cycle remains closed.

**Wong email sent:** the approved version-2 text was sent on 12 November 2026 at 09:45 Europe/Madrid to the corresponding address verified in [Mallika et al.](https://www.biorxiv.org/content/10.64898/2026.09.11.751082v1.full), corroborated by the Johns Hopkins directory. Gmail SENT and the stored message body were checked; this does not establish delivery, reading or a reply. No attachments, tissue-coverage claims or extra recipients were added. [Exact approved text and historical draft](drafts/2026-11-11-mensaje-wong-borrador.md). No automatic follow-up is authorized.

**Next decision:** review substantive author replies when received; confirm actual AD Workbench access/file inventory before reopening #37. A bounded Gmail search on 12 November found no new Fratta message after 10 November and no matching AD Workbench/Seddighi notification after 3 November; absence of matching mail does not establish portal access status. No new source search or download was performed. #37's selection cycle is already closed and remains conditional on a concrete usable manifest. New studies require a separate question, eligible data and prospective controls; no fourth candidate is opened by this closure.


This replaces earlier planning snapshots. Historical reports and commits remain evidence, not automatic instructions to rerun work. This consolidated state accompanies integration of PRs #46–#49. Review details and exact checked commits are preserved in [INTEGRATION_REVIEW](../reports/integration-20261104/REVIEW.md).



## K26 review clarification — 12 November 2026

[Updated report](../reports/k26-conditional-replay-20261111/REPORT.md) retains the prespecified aggregate ratio 0.585773 and adds heterogeneous block ratios 0.342430/1.047990/1.152671 plus their implicit weights. The mean/median of block ratios answer different questions and are labelled post-hoc descriptive, not replacements for the original estimand. Two point ratios exceed 1; this does not establish complete rescue/equivalence.

The explicitly post-hoc ASO−Control R contrast gives log1p estimate −0.241721, pointwise 95% interval −0.574500 to +0.091059, nominal exploratory p=0.152344; raw p=0.115450 with the existing residual limitation. Original primary contrasts/Holm family are unchanged. Non-rejection does not establish equivalence. The external 18-specification scan cannot exclude all alternative inputs/preprocessing/model choices or prove that a different n uniquely explains the stars; cause remains unresolved. Scope was recorded before the added contrast in `94f3af13a2b18e7c8bcec403e6838c99ab32bb59`. No new communication or model search; strict v1 remains disabled.


## K26 conditional replay completed — 11 November 2026

[Conditional replay report](../reports/k26-conditional-replay-20261111/REPORT.md), with v2 plan committed at `55f84fe26f77d631d417f382bff176ca4528b1f3` before fitting. User explicitly authorized using the three published source blocks and original nA scale under a narrower assumption. Strict v1 remains unchanged/disabled; its full nested biological-identity requirements are not declared satisfied. Earlier no-fit statements below describe the preceding strict-gate review.

Actual R/lme4/lmerTest REML log1p fit: ASO−KD +0.474402, pointwise 95% interval +0.132939 to +0.815865, nominal/Holm-two-contrasts p=0.007036. Default fit converged and was nonsingular. Direction remains positive in all three leave-one-block-out fits; two intervals include zero. Equal-block original-scale difference is +2.222175 nA; prespecified aggregate ratio 0.585773 is heterogeneous across blocks (0.342430/1.047990/1.152671); Batch 1 carries 69.19% of its implicit deficit weight. It is not a stable recovery fraction, clinical recovery or equivalence. Raw-scale Gaussian residuals violate the prespecified W<0.90 check. The final figure's ASO three-star band (p<0.001) is **not reproduced**; this run corresponds to two stars. Cause unresolved, no tuning/rescaling performed. R 4.5.0 differs from the Methods' 4.4.1.

This is conditional computational scrutiny of the same data, not independent biological replication. Stop this fixed replay. Next discriminating input: author block/nesting clarification and panel-specific execution/scale for the star-band discrepancy. No new contact is authorized by this entry; the previously approved follow-up is already recorded. #37 and the closed STMN2 cycle remain unchanged.


## K26 public source found — 11 November 2026

Follow-up [design review](../reports/k26-published-source-20261111/DESIGN_REVIEW.md) completed before fitting: the final Fig.4d axis is **nA**, while the historical v1 contract hard-codes pA. Reporting Summary supports independent differentiations and parallel intervention wells; the workbook still lacks the full cell/culture/coverslip/repeat mapping and exact per-cell days required by strict v1. No IDs, dates or human approval were fabricated. The existing contract remains disabled; no effect/model was calculated. A focused Fratta metadata follow-up was [sent with Luis’s explicit authorization](../reports/k26-published-source-20261111/COMMUNICATION_LOG.md) on 11 November 2026 in the existing thread; no further message is authorized. A unit/version amendment is needed before any eventual fit; batch-only conditional replay would require a prospectively explicit narrower assumption. This dated review supersedes the availability inspection's remaining-check list, not its original counts.

The final Nature article is published today, DOI `10.1038/s41586-026-11256-2`. Its public Source Data Fig.4 workbook was downloaded and hash-pinned. Panel 4d contains explicit Batch 1/2/3 blocks and 34 control, 30 KD, 25 KD+21-6 numerical observations, matching the final legend. [Bounded inspection and reproduction script](../reports/k26-published-source-20261111/REPORT.md). This is a new reopening input for #44; older statements that the numerical file is unavailable are superseded. No effect was estimated and the input contract remains disabled. Next: reconcile units, batch-to-differentiation/culture structure, identities/exclusions/QC and the now reachable actual R model against the existing FR-K26-4d v1 plan before inference. This does not unblock #37 or reopen STMN2.


## English documentation entry — 11 November 2026

PR #58 is merged at `c7d8f7e92e7eb02e3fb619f6e8984f075ef84784`; the corrected UNC13A coverage calculation and its limitations are integrated. The [current findings page](../docs/CURRENT_FINDINGS.md) and [English evidence/reproduction guide](../docs/ENGLISH_GUIDE.md) provide the public reading route, with seven source-pinned report translations. Spanish originals and dated sections below remain preserved. No new biological analysis, data-access check or contact was performed for this documentation update. The language policy applies to new scientific/public documentation and new code comments/docstrings; it does not reopen closed scientific cycles.


## Current integrated status — 11 November 2026

The six Claude commits ending at 5ef8825 and the closed STMN2 #57 analysis are reconciled in [INTEGRATION REVIEW](../reports/integration-20261111/REVIEW.md). Plans and original counts are preserved, the audit table has an explicit integration-review column, and unsupported inferential wording is corrected at its source (including the Ikegami report relied on by the audit). No new biological analysis or broad historical audit was opened.

The current scientific balance is the [closing report](../reports/stmn2-within-region-20261111/REPORT.md): exploratory paired tissue pattern, quality sensitivities and unresolved composition/batch/selection. P1 is below its fixed threshold; P3 directions are descriptive. Stop further fits on the same 45 donors. Older dated sections below preserve chronology and do not reopen completed tasks or override this status. Pre-10-November review remains pending, prioritized only if a current conclusion relies on it. No functional, causal or independent-replication claim. #37/#44 remain unchanged.

## STMN2 cycle closed — 11 November 2026

[Integrated closing report](../reports/stmn2-within-region-20261111/REPORT.md). Final fixed within-region analysis, same 45 donors, no new p-values or corrected tissue effect: cortical Spearman −0.229 / partial rank correlation −0.299; cervical −0.093 / −0.105, accounting for RIN, total junction coverage and preparation within each region. Leave-one-donor-out ranges remain negative; these are influence checks, not confidence intervals. The existing 19-pair RIN sensitivity gives unadjusted −0.285 / −0.117. **22/45 cervical neuronal estimates are zero** (10/19 in RIN subset), limiting this composition probe. Composition is not ruled out; inverse associations do not identify mechanism.

All previously pending within-region/RIN/ST7 tasks below are now complete. **Stop this cycle on the same donors**: no more cutoffs, correlations or models by inertia. Supported result is exploratory paired tissue pattern, partially resistant to measured quality restrictions, with composition/batch/selection unresolved. P1 ≥10× is not met; P2's four covered cases do not establish that UNC13A failed solely because of the locus; original P3 frequencies are descriptive. No functional, causal, clinical or independent-discovery claim.

Next enabling input is a genuinely discriminating composition/QC measurement or independent paired cohort with target junction coverage and verified design, not another analysis of these 45 donors. PR #57 is consolidated for human review. Claude's historical prediction-label audit is separate and not marked complete here. #37 UNC13A and #44 K26 gates remain unchanged.

## ST7 composition gate completed — 11 November 2026

[Report](../reports/stmn2-composition-20261111/REPORT.md): ST7 supplies exact valid composition vectors for all 90 libraries of the 45 original pairs. 16,985 rows, 1,724 valid sample/reference vectors, finite simplex values and complete observed taxonomies. Technical linkage accepted; no new adjusted tissue effect fitted.

Cortex (8 classes, MuSiC GSE140231 reference) and spinal cord (11 classes, GSE190442 reference) use different taxonomies. Cross-reference calibration and exact raw/transformed ST7 provenance are not established by the worksheet. Do not subtract/divide these fractions or claim a common-scale composition correction without a defensible measurement/model protocol. Shared algorithm and sum-one alone do not establish comparability.

The earlier ST7 inspection task is complete. Cheapest next concrete task: fix a within-region-only STMN2/neuronal-estimate association protocol, handling coverage/RIN and keeping cortical and spinal reference scales separate. This can probe an alternative explanation but cannot be labelled correction of the paired tissue effect. A common-scale tissue adjustment instead requires harmonized/calibrated composition estimates and provenance. No extra cohort search or new p-value executed here; #37/#44 unchanged.

## STMN2 RIN sensitivity completed — 11 November 2026

[RIN report](../reports/stmn2-rin-20261111/REPORT.md), fixed protocol c444b5443b671f0aa8436109eb05a600f1fb0b86. All original 45 pairs reproduce and agree with ST3 on donor/region/preparation; valid RIN in all 90 libraries. Main restriction (RIN≥6 both, absolute difference≤1) leaves **19 pairs: 10 cervical-higher / 8 ties / 1 lower**, median paired local-ratio difference **+0.002551**. Stricter RIN≥7 leaves **9 pairs, 4/4/1, median zero** and fails the fixed ≥10-pair interpretation gate. No additional p-values or regression. This is descriptive sensitivity, not full QC adjustment or independent replication; do not claim uniform robustness to RIN.

The earlier pending RIN task is complete. Next concrete input is ST7 NYGC composition estimates: fix inspection scope, verify per-library granularity/exact keys and method, then define one analysis before inspecting effects. Do not search further RIN thresholds. Composition, true extraction/sequencing batch, selection and unequal depth remain unresolved. #37 UNC13A and #44 K26 unchanged.

## Source gate completed — 11 November 2026

[Three-source availability review](../reports/paired-stmn2-source-gate-20261111/REPORT.md): no independent replication source accepted yet. **New executable QC input found:** NYGC ST3 metadata, Zenodo 20090702, exact rna_id matches for 308/313 original libraries (147 cortex, 161 cervical), all with valid RIN and preparation. This is demonstrated overlap with the original cohort, not independent validation. No new effect was fitted.

Next actionable task: fix an RIN/QC sensitivity protocol for the original 45 pairs and validate donor/region/preparation compatibility before modelling. Composition lead is NYGC ST7 (32.7MB expression workbook, not downloaded); per-library granularity and exact key remain unverified. EGA EGAD00001009686 has the relevant paired bulk/nuclear design but requires controlled access and independence checks. GSE330130 provides lumbar/cortex multiome matrices; donor pairing, independence and STMN2-junction suitability are unresolved. Do not treat matrices of gene counts or different accession names as replication. No request/contact or new biological contrast executed; #37/#44 unchanged.

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

Completed instead, as bounded documentary work: an intervention-chronology matrix over the six UNC13A intervention preprints, completed to 6/6 when Luis supplied the Mallika and Cao PDFs that neither Europe PMC nor bioRxiv would serve. **14 experiments. Historical pre-curation labels were 1 post-deficit recovery / 12 prevention / 1 indeterminate; the curated substantive column now has 1 / 13 / 0, while the strict column has zero post-deficit classifications. These labels describe the recorded rule, not proof that an undocumented deficit was absent.**

**Under the symptom-based substantive reading, the prediction is refuted; under the strict same-endpoint baseline rule it is not**, as explained by the curation below. Mallika's AAV-PHP.eB-CTR arm was delivered at 6 weeks "when fine tremors are already apparent", at what the authors call a symptomatic stage. The study reports maintained grip strength and extended survival from ~47 to ≥110 weeks (n=20 per group). CTR is a chimeric TDP-43 splicing repressor acting on many targets, **not a UNC13A-specific intervention**.

In the inspected matrix, **0 of 6 UNC13A-specific experiments** establish treatment after a documented functional deficit. **Correction — 12 November 2026:** the nine-experiment denominator here was a pre-curation hand count already corrected in the 10 November curation, but not propagated to this paragraph. The phrase claiming all were preventive by construction is withdrawn: lack of documentation does not establish absence of a deficit; only germline interventions necessarily precede the induced deficit. The UNC13A-specific arms also diverge by endpoint, failing for motor neuron disease ("preventing cryptic splicing of Unc13a is insufficient to attenuate motor neuron disease", Mallika) while preserving memory (Cao). The post-deficit window is therefore not intrinsically intractable in these models, which makes the UNC13A-specific question more pointed, not less.

A curation pass re-derived every row against the prespecified rule and verified all 14 locator quotations verbatim against the primary text (14/14, `scripts/verify_matrix_quotes.py`). It found and fixed four defects, including a bug in the verifier itself and three quotations I had joined with ellipses into sentences no author wrote, and corrected a hand count of target specificity. Because the prediction's fate turns on a judgement rather than a datum, the matrix now records both readings in separate countable columns: under the letter of the rule, which excludes a parallel untreated arm as baseline evidence, **0 of 14** are post-deficit and the prediction is **not** refuted; under the substantive reading, 1 of 14 is. Either way, **treatment after a documented functional deficit was not established for any of the 6 UNC13A-specific experiments** in the inspected matrix.

The curation is not independent review: the same agent did both passes, so it cannot detect a systematic bias of its own or a criterion that was ill-conceived from the start. That need stays open, with free routes recorded (peer review of Mallika/Cao; a bioRxiv comment, which would need Luis's express authorization). Mallika and Cao share a corresponding author and six authors, so they are not independent replications of each other. [Matrix and report](../reports/unc13a-intervention-timing-20261110/REPORT.md), [plan](plans/2026-11-10-unc13a-intervention-timing-matrix.md).

PMID 42983891 (Ikegami/Koike 2026, peer reviewed) was checked against the #37 gate and **rejected as a technical source**: qRT-PCR/ddPCR on post-mortem motor cortex, no junction counts, no RNA-seq/GEO/BAM, data by author request. Kept as context only: pathological subtype 2b shows higher UNC13A cryptic and truncated STMN2 RNA, correlated at Spearman ρ = 0.58. This does not open a fourth candidate.

The daily watcher's `long_reads` query searched all fields including reference lists (11,040 hits, unrelated papers); it is now restricted to TITLE_ABS (42 hits), with tests. This is a scope fix, not a quality filter.

## New bounded result — Ikegami source-data replay, 10 November

The deposited source data of Ikegami/Koike 2026 (*Acta Neuropathol Commun* 14:229, **peer reviewed**, open access) **reproduce their published statistics**. Group sizes match exactly (12/12/11, n=35); Spearman between UNC13A cryptic RNA and truncated STMN2 RNA reproduces at **rho 0.5737** against a published 0.58, inside the prespecified tolerance; subtype differences reproduce in direction and significance, Type 2b above Types 1 and 2a for both measures while Types 1 and 2a do not differ. A label-permutation control destroys the effect and marginal disease-duration correlations are non-significant (rho -0.24 and -0.26). These same-data calculations neither exclude duration as a contributor nor constitute independent replication. The ddPCR/qRT-PCR concordance the paper calls "strong" is quantified here for the first time: rho 0.859 and 0.870 on 26 cases. [Report](../reports/ikegami-source-replay-20261110/REPORT.md).

A second bounded cycle screened the confounders with Table S1/S2 (35 cases). **No significant differences in RIN, post-mortem interval or semiquantitative neuronal loss were detected between subtypes**. This same-data screening does not establish equivalence or exclude confounding. **Disease duration does differ** strongly and in the expected direction (medians 32 / 19 / 11 months), so the subtype with most cryptic RNA has the shortest course; that is compatible with the paper, whose support is a non-significant duration-marker correlation, but with n=35 it is absence of evidence rather than evidence of absence. Age at onset differs nominally (Type 2b about ten years older) and does not survive Holm correction across the six covariates, so the paper's age-comparability claim is not contradicted at a corrected level. The discriminating test for H2 is **not executable from this deposit**: it carries no per-case pTDP-43 burden. Per-case covariate joins were refused because disease duration is not a unique key within Types 2a and 2b, the plan forbidding row-position joins.

This is internal reproducibility, not replication: same subjects, same measurements, same laboratory. It carries **no junction counts**, so **#37 stays blocked and this source stays rejected for that gate**. Post-mortem tissue is still not equated with i3N culture. The rho ~0.57 correlation across 35 human cases is internal observational evidence compatible with hypothesis **H2**, pending separation of between-subtype and within-subtype association, and it agrees in direction with Mallika's experimental finding that correcting one target alone was insufficient. Correlation of two markers in the same tissue is not mechanism, causality or patient benefit.

The watcher extension found that **Guo's preprint is now peer reviewed** in *Science Translational Medicine* (PMID 42234776, DOI 10.1126/scitranslmed.aeb8517, 2026-06-03). It is paywalled with no PMC record, so its methods were **not** inspected: the two Guo rows of the timing matrix remain attributed to the 2025 preprint and may differ from the published version.

## Strategic routes — 11 November

Three routes were set out and acted on. **Snaptron/recount3**, the one route that could unblock #37 without money or third-party permission, was attempted and is **blocked by TLS**: the CONNECT tunnel succeeds once the host is allowed, but the server's certificate chain does not verify even with the proxy CA supplied, and verification was not disabled. The feasibility question is therefore **unanswered, not refuted**, and the prespecified stop rule forbade chasing alternatives inside that cycle. Opening a cycle on the recount3 file store instead needs its own scope decision and plan. [Report](../reports/snaptron-unc13a-feasibility-20261111/REPORT.md).

A **laboratory collaboration message** and the **structure of a commentary** are drafted and deliberately **not executed**: both are external and irreversible, both would carry Luis's name, and the commentary should wait for the independent review of row M-a that the watcher will surface for free. [Drafts](drafts/2026-11-11-borradores-pendientes-de-autorizacion.md).

Honest ceiling, recorded so it is not forgotten: with no laboratory, no budget and the raw-data pilot already closed at coverage [1,0,0], this project's realistic contribution is verification and synthesis of published work, not new biological measurement. Nothing here helps a patient today and nothing here supports any clinical decision.

## recount3 breakthrough and its limit — 11 November

**Issue #37's measurement blocker is solved as a capability.** All four candidate families were rejected for want of accessible junction counts; recount3 publishes them already quantified. For 24.5 MB and no cost, the project now holds exon-exon junction counts for a TDP-43 depletion experiment in human neurons, with conditions **declared by the deposit** rather than inferred, and no FASTQ or alignment involved. The probe is written and tested, so applying the same route to another project costs minutes and a few megabytes. [Report](../reports/recount3-unc13a-20261111/REPORT.md).

**The dataset inspected does not pass the gate.** SRP166282 is Klim 2019, whose data #37 had rejected through Irwin for lacking linkable junction counts; recount3 supplies them. Design reconstructed from declared metadata: 6 TDP-43 knockdown against 12 controls, both batches containing both conditions, **but a single cell line (HUES3)**, so replicates are independent cultures and not genetically independent donors. All three sealed target junctions match **exactly**, the coordinate-convention guard passes, and the annotation pattern is as the biology predicts: canonical annotated, both cryptic not.

Coverage decides it. The canonical positive control is measured in 18/18 samples at up to 66 reads, so measurement is not the failure, yet the cryptic junctions reach a maximum of **5 reads against the prospective minimum of 20**, and `gate_met` is false with the positive control excluded from the gate. **Rejected on observed cryptic-junction coverage**. Correction — 12 November 2026: the earlier claim isolating the cause to locus depth is withdrawn. Accessible counts and a detected canonical junction do not isolate total sequencing depth from depletion efficacy, assay, mapping/read-length or biological alternatives, nor certify all design requirements.

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

## Integrated Claude coordinate and prediction review — 11 November

The six Claude commits ending at 5ef8825 are incorporated with [integration review](../reports/integration-20261111/REVIEW.md). Coordinate plans and the 16-row prediction audit remain traceable. P1 is not met: 6.6x raw, 8.085x normalized. P2 is observed in four covered samples, not proof of a locus-only explanation; P3 remains descriptive. Nondetection of an outgoing junction is not proof of terminality/completeness. Three splice donors are not three biological donors. The 484/9 comparison refers only to unannotated alternatives.

The prediction audit's 14/1/1 classification describes its original narrow rule, not 14 validated scientific conclusions. Its table now distinguishes descriptive directions, a test never performed as written, and inference unsupported by Wilson-overlap or p>0.05. The numerical 11 / qualitative five split is explicit. Earlier pre-10-November cycles are not certified; review them only where a current conclusion relies on them.

## Correction — the cervical coverage ratio was a ratio of medians

A third external review of the day, on the draft message for Wong, pointed out that the table it cited does not support a claim that depth was controlled between tissues. Checking that, I found a methodological error in the merged cervical report.

The column reading "canonical per million" was computed as a **ratio of medians** — a group median count divided by a single project median depth of 44.4 M applied to both tissues — which is not per-library normalisation. That field was also **named wrongly**: it is `exon_fc_count_all.total`, the reads submitted to featureCounts, not the reads assigned to exons, which differ between tissues (20.3 M against 23.9 M). So the claim that depth was "identical" held only for the field the report did not name.

**The correction then needed correcting.** A fourth external review could not reproduce the replacement figure of 2.530 / 0.113 (22.3-fold): trying `.assigned` gives 0.2055 and input reads give 0.1150 for the cervical ALS group. The arithmetic was in fact right — it reproduces exactly against `exon_fc_count_all.total` — but it had been announced with **no procedure committed and the denominator named wrongly**, which is not an acceptable state for a published figure. It is now deposited in [`scripts/normalize_tissue_coverage.py`](../scripts/normalize_tissue_coverage.py) with six tests, input hashes, per-library ranges and **all five candidate denominators**: **22.34-fold**, and between 22.2 and 25.6 depending on the field. A fifth review then reproduced the deposit against the input hashes and found one residual defect: the script divided medians that had already been rounded, which moved the headline by 0.01. It now keeps full-precision medians and marks the rounded quotient as not for use. The report now carries the full three-version history of the figure, the table and TSV are regenerated, and a standing rule is recorded: no central figure is published or corrected without a deposited script, a named data field, input hashes and a test.

Two overstatements in the same report are also corrected. It said sequencing depth "is identical" and that this "eliminates the confounder". Matching medians does neither: per-library distributions differ, and equal medians only make it unlikely that depth explains a twentyfold gap. The comparison remains unpaired with unmeasured confounders.

A collateral observation is recorded without being exploited: normalised canonical coverage is **lower in ALS than in controls in both tissues** (2.530 against 2.845; 0.113 against 0.174), the direction expected if TDP-43 loss reduced canonical splicing, but with 13 controls, unpaired and with no prespecified contrast it is **not tested or interpreted**.

Three further points from the same review are accepted; two are fixed in the draft, and the third is now carried into the reports that held it: the draft's claim of no donor pairing was outdated, since a validated map of 45 cortex-cord pairs exists (**corrected again**: that map pre-existed table ST7 and was validated against NYGC ST3; ST7 later added composition estimates for the same 90 libraries, and it did not originate the pairing. Those pairs are also **ALS donors in both tissues**, selected on STMN2 coverage, so they can pair the tissue contrast but **cannot** resolve an ALS-versus-control one); "the limitation appears to be gene-specific" overreaches from two genes; and **failing to document a deficit before dosing does not demonstrate that an intervention was preventive**, which held for the germline deletions but not for the row where knockdown had run five days. The message now says only that we could not establish treatment began after a documented deficit, and the phrase "preventive by construction" has been **withdrawn from the timing report and its curation record** as well, since the matrix establishes absence of documentation, not absence of deficit.

One further item is open and deliberately not resolved by downloading more data: the cortical report's normalised 1.8-fold against Klim compares 44.4 M with 21.8 M **without it being established that both come from the same QC field**. It is flagged in that report and supports nothing.

Three further overstatements in the cervical report are withdrawn after the fifth review. "No ratio in cord is interpretable" was too absolute: 5 of 95 ALS libraries and 2 of 13 controls do reach 20 canonical reads, which is a different requirement from the 20 **cryptic** reads that remain unmet everywhere in cord. The description of the 45 pairs is corrected as above, and the correction is now carried into the collateral paragraph too, which had gone on proposing those pairs as the route to examine an ALS-versus-control difference they cannot address. That observation is left recorded with **no route proposed**. And the conclusion no longer says more depth would not help: closing **the search performed** for insufficient coverage is supported, but ruling out depth would need an estimate of the depth required, and **no validated estimate is available**. Scenarios conditioned on an assumed cryptic fraction can be computed; what is missing is evidence for choosing one, since Klim's figure and Ma's are not comparable and #37 could not fix the real fraction. Calling any such calculation "circular" was itself too absolute and is withdrawn. Cell enrichment and targeted assays are described as reasonable, not as the only routes.

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


## Subtype-conditioned Ikegami result — 10 November 2026

The prespecified exploratory test does not support the prediction beyond subtype: pooled rho 0.57367 falls to adjusted rank rho **0.31669**, stratified two-sided permutation **p=0.07825**, marginal bootstrap 95% interval **[-0.02342, 0.62758]**. Removing Type 2b gives pooled rho 0.14957 and adjusted rho 0.19087. Within-subtype estimates vary (Type 1 -0.15385; 2a 0.65734; 2b 0.86364), but no difference-between-correlations test was prespecified or performed. H2 remains uncertain; neither absence nor a uniform mechanism is established. Prior confounder-exclusion and Spearman-variance claims are corrected without changing historical statistics. [Protocol](plans/2026-11-10-ikegami-subtype-conditioning.md), [report](../reports/ikegami-subtype-conditioning-20261110/REPORT.md). This bounded cycle is closed; #37/#44 remain blocked. Proposed next evidence is an independent, identifiable-unit source with both markers and justified TDP-43 function measures, not another equivalent replay.


## Independent paired-marker source screen — 10 November 2026

Luis authorized a bounded independent-source search after the subtype-conditioned result. Fixed candidate list and admission rules were committed at `2b23019` before inspecting the source workbook. **0/3 admitted for a new paired-marker/pathology association**: Quadros 2024 is the best targeted source request (both cryptic markers and pTDP-43 burden, but original paired values by author request); Gittings 2023 did not detect UNC13A cryptic junctions; Ramsey 2026 provides a verified public workbook but no biological-unit map or PCR-to-pathology keys. Ramsey's 18/27 human PCR entries are not 45 subjects; its pathology block has 8 entries per group. Its organoids lack detectable cryptic retention according to the paper despite astroglial pTDP-43 pathology. No new biological correlations were calculated. [Report](../reports/independent-marker-source-screen-20261110/REPORT.md), [decisions](../reports/independent-marker-source-screen-20261110/candidate-decisions.json). Cycle closed; #37/#44 are now closed under their later dispositions. The Quadros request was subsequently authorized and recorded as sent; see the communication log below. No new contact is authorized. No participant demographics, raw sequencing or expression matrices were downloaded. Neither AD nor FTLD organoid evidence is labelled ALS replication.


## Authorized communication and Keuss publication check — 11 November 2026

Luis explicitly authorized the prepared Quadros source-data request. Sent to corresponding author Clotilde Lagier-Tourenne on 11 November at 08:21 Europe/Madrid; Gmail SENT confirmation ID `1a1c97ba8ab9cf9d`. This supersedes the earlier unsent status; no response or data delivery is claimed. [Communication log](../reports/publication-access-check-20261111/COMMUNICATION_LOG.md).

**Historical early check, later superseded by #60–#62:** the separately authorized one-time Keuss/Fratta publication check did **not at that time** establish final publication or new source data. KCL still displays Accepted/In press (6 October 2026) and an accepted-manuscript PDF; its direct PDF route returns 403. Crossref title query (8 hits), Europe PMC Keuss AND UNC13A (16 hits) and bioRxiv details (2024 v1, published=NA) did not identify the final K26 article/source table. These are bounded retrieval results, not proof of global absence. Gmail search/read found only Fratta's 4 November reply anticipating availability the following week, with no file or new reply in the inspected query. #44 remains blocked on original Fig.4d eEPSC values and cell→culture/differentiation map; no effect estimated and no follow-up sent to Fratta. [Report](../reports/publication-access-check-20261111/REPORT.md).
