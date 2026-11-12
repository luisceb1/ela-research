# UNC13A intervention timing: the target-specific documentation gap persists under both rule readings

> English translation prepared on 11 November 2026 from the [Spanish original](REPORT.md) at `c7d8f7e92e7eb02e3fb619f6e8984f075ef84784`. Source/translation hashes and review scope: [English guide](../../docs/ENGLISH_GUIDE.md#translation-policy-and-review). This is a dated report, not a new analysis or publication-status check.
> Earlier proposed next steps are historical; for completed STMN2 work and current stop rules, use the [closing report](../stmn2-within-region-20261111/REPORT.en.md) and [current findings](../../docs/CURRENT_FINDINGS.md).

**Date:** 2026-11-10. **Baseline:** main `3916b77ec0546e9d327e6d54e4dacd90d1a51ce4`, plan fixed in `research/plans/2026-11-10-unc13a-intervention-timing-matrix.md` (commit `626c259`, **before** retrieving texts).
**Evidence label:** exploratory documentary audit. Initial pass and curation performed **by the same agent**; no independent review of the classifications. See [CURATION (Spanish)](CURATION.md).

Authorization: on 10 November 2026 Luis confirmed that the K26 file **had not** arrived and AD Workbench **had not** granted access, and instructed continuation with the remaining work. #37 and #44 remained blocked and unchanged. Luis subsequently supplied the Mallika/Cao PDFs, completing the matrix to 6/6 sources.

## Prespecified question and prediction

Does any accessible primary experiment correcting or preventing UNC13A/Unc13a cryptic-exon inclusion under TDP-43 loss start intervention **after** documenting a baseline functional deficit in the same system and endpoint?

Prespecified prediction: none meets this criterion for a functional endpoint.

## Result

**14 experiments across 6 sources.** All quotations checked literally against primary text: 14/14 PASS with `scripts/verify_matrix_quotes.py`.

The prediction's status depends on a rule judgment, so the matrix records **two readings** in separate countable columns:

| Reading | Definition | Post-deficit | Prediction |
|---|---|---:|---|
| `strict_rule_verdict` | Literal prespecified criterion, **excluding** a parallel arm as baseline evidence | **0 of 14** | **not refuted** |
| `classification` | Substantive reading: documented symptoms at dosing, framed by authors as “after onset of symptoms” | **1 of 14** | refuted |

The sole discrepant experiment is **Mallika M-a**: AAV-PHP.eB-CTR at 6 weeks, “when fine tremors are already apparent”, with large reported grip-strength/survival benefit, survival from approximately 47 to **≥110 weeks** (n=20 per group). Under the strict criterion this is insufficient because predosing documentation concerns tremors (qualitative, not the measured endpoint), while the grip-strength deficit is evidenced in the **parallel GFP arm**. Both readings are reported rather than silently selecting one.

**The central result does not depend on that choice.** Target scope, verified row by row:

| Scope | Experiments | Post-deficit (strict) | Post-deficit (substantive) |
|---|---:|---:|---:|
| **`unc13a_only`** | **6** | **0** | **0** |
| `mixed` (single/combined ASOs) | 2 | 0 | 0 |
| `multi_target` | 5 | 0 | 1 |
| `stmn2_focused` | 1 | 0 | 0 |

**For none of the 6 UNC13A-specific interventions could dosing after a documented functional deficit be established, under either reading.**

> **Correction of 11 November 2026.** The original added “all are preventive by construction”. **That does not follow.** Germline cryptic-exon deletions are preventive by design. For the others, particularly **K-c** (Keuss, SH-SY5Y), where knockdown was established **5 days** before dosing, **not measuring a prior deficit does not establish that none existed**. The matrix establishes **absence of documentation**, not absence of deficit. Reversing these turns absence of evidence into evidence of absence.

Complete matrix: [`matrix.tsv`](matrix.tsv), 14 rows, 16 fields. Provenance/SHA256: [`sources.json`](sources.json). Errors found/corrected during curation: [`CURATION.md` (Spanish)](CURATION.md).

## Evidence by source

| Source | Access | Experiments | Strict / substantive reading |
|---|---|---:|---|
| S1 Keuss 2024 | full text (Europe PMC) | 3 | 3 prevention / same |
| S2 Guo 2025 | full text (Europe PMC) | 2 | 2 prevention / same |
| S3 Mallika 2026 | **PDF supplied by Luis** | 2 | 2 prevention / **1 post-deficit (M-a, multi-target)** + 1 prevention |
| S4 Cao 2026 | **PDF supplied by Luis** | 2 | 2 prevention / same |
| S5 Mehta 2025 | full text (Europe PMC) | 2 | 2 prevention / same |
| S6 Gomberg 2025 | full text (Europe PMC) | 3 | 3 prevention / same |

Chronologies determining classification, with literal source wording where quoted:

- **Keuss, ASO arm:** “ASO treatments were started **at the same time as** PROTAC treatment”. Concurrent with TDP-43 degradation.
- **Guo:** first dose **precedes** knockdown in both designs — ASO days 3 and 10 with shRNA on day 5, and ASO days 20 and 27 with shRNA on day **21**. Authors place their measurement “prior to any cell loss”.
- **Mehta:** tU7 expressed from stable lines selected before doxycycline induction.
- **Gomberg:** anti-TDP-43 ASO day 30, lentivirus day 32, axotomy day **42**; intervention precedes the functional challenge, and the functional endpoint is attributed to STMN2.
- **Mallika, Unc13a-specific arm:** approximately 44 bp germline CE deletion crossed into the cKO model. Result: “could not maintain the normal grip strength and body weight … **indistinguishable** from those observed in ChAT-Cre;Tardbpf/f mice”, and authors' conclusion: “**preventing cryptic splicing of Unc13a is insufficient to attenuate motor neuron disease**”.
- **Cao, Unc13a-specific arm:** germline deletion, tamoxifen at 2 months; preserves novel-object recognition. Title: “**Prevention** of Unc13a cryptic splicing is sufficient to preserve memory”.
- **Cao, CTR arm:** “Tamoxifen was administered at 5 months of age to deplete TDP-43, followed by ICV injection of AAV-PHP.eB-CTR … **2 weeks later**”. No predose behavioral measurement is reported, so this does not establish post-deficit intervention.

## Interpretation

Three readings, in order of strength:

1. **Isolated UNC13A correction after a measured deficit is not documented in the inspected experiments.** In the **6** accessible `unc13a_only` interventions, dosing after a documented deficit is not established under either reading; **only germline deletions are preventive by construction** (see correction above). The literature supports prevention of cryptic-exon inclusion preserving function when intervention precedes or coincides with TDP-43 loss, rather than correction restoring already lost function, the scenario relevant to a diagnosed patient. The closest experimental template is **K-c** (Keuss, SH-SY5Y): dosing after established knockdown following 5 days of doxycycline, but without predose measurement of the defect.

2. **Multi-target restoration after symptoms benefits function in a mouse model under the substantive reading.** Mallika M-a shows a large survival effect. This is not evidence against the UNC13A hypothesis: it suggests the post-deficit window **is not intrinsically intractable** in this model, making the UNC13A-specific question more pertinent. Under the strict reading, even this is not established because baseline evidence comes from the parallel arm.

3. **UNC13A alone differs by endpoint, not study quality.** Preventively, it fails for motor-neuron disease (Mallika) and preserves memory (Cao). This is compatible with H1's neuronal-type-dependence hypothesis and the observational Ikegami finding below of coordinated target dysregulation. These are different endpoints/populations, not a contradiction.

This reinforces the criterion already applied to #44, where the selected intervention is also concurrent with TDP-43 depletion.

## Limitations

- **One reader, without independent review.** The same agent performed the first pass and curation. Curation catches transcription/rule-application failures — four were found, including a verifier bug and three quotations incorrectly joined with ellipses — but **cannot provide an independent assessment of the agent's systematic bias or an ill-conceived criterion**. See [CURATION (Spanish)](CURATION.md). `extract_intervention_timing.py` only locates sentences; `verify_matrix_quotes.py` only checks transcription. Neither classifies experiments.
- **M-a is the discrepant row and most needs independent review.** The rule requires the deficit *of the same endpoint* measured *in the same animals* before dosing and explicitly excludes the parallel arm. In M-a, predose documentation concerns **fine tremors** (qualitative, not the measured endpoint); grip-strength deficit comes from the GFP arm. Whether this is too strict for a mouse model with characterized age-related progression is a judgment the rule's author **cannot independently assess**.
- **Count corrected during curation:** the initial “9 specific / 5 multi-target” was an unsupported hand count. The verified row distribution is 6 `unc13a_only`, 2 `mixed`, 5 `multi_target`, 1 `stmn2_focused`.
- **S3 and S4 are not independent of one another:** same corresponding author (Philip C. Wong, Johns Hopkins) and **6 shared authors** among S3's 10 and S4's 18. They may share animals, constructs and cohorts. They are not counted as independent replications.
- **All 6 inspected source versions are preprints**, subject to revision/correction. The Nature 2026 Keuss version **was not inspected**; its chronology is attributed only to the 2024 preprint.
- **Mouse extrapolation:** the mouse *Unc13a* cryptic exon lies in **intron 1**, whereas the human exon lies in **intron 20** (confirmed in Mallika's discussion). The interventions are not equated mechanistically. AAV-PHP.eB crosses the mouse blood–brain barrier; that does not establish human applicability.
- CTR's effect **cannot assign improvement to each target separately**: there is no factorial control.
- No project effect was quantified, no model fitted and no cross-system magnitude comparison made. Splicing correction ≠ molecular rescue ≠ neuronal function ≠ clinical benefit. Nothing here supports a clinical recommendation.
- S4 license: “All rights reserved. No reuse allowed without permission”. Only hashes and short audit quotations are committed; the PDF is not redistributed.

## Collateral source-gate check (#37)

**PMID 42983891** (Ikegami/Koike 2026, *Acta Neuropathologica Communications* 14:229, peer-reviewed, open access) was evaluated as a possible new #37 source.

**Decision: REJECTED as a technical source for #37.** Reasons checked in full text (SHA256 in `sources.json` C1):

1. **No junction counts.** Quantification is qRT-PCR/ddPCR, not RNA-seq. Full-text occurrences: `RNA-seq` 0, `sequencing` 0, `GEO` 0, `BAM` 0, `FASTQ` 0. There is no junction matrix or alignment to apply the ≥20-coverage criterion to.
2. **Insufficient availability:** “available from the corresponding author on reasonable request”. Source data in Additional file 3 (XLSX, 29 KB), not downloaded in this cycle.
3. **Post-mortem tissue, not culture.** Sporadic ALS motor cortex (Type 1 n=12, Type 2a n=12, Type 2b n=11). This does not replace or equate to the i3N culture contrast.

Retained **context**: subtype 2b shows significantly higher UNC13A cryptic RNA and truncated STMN2 RNA, positively correlated (Spearman ρ = 0.58). Observational coordinated dysregulation, not rescue or causality.

#37 remains blocked on its specified input: a concrete Seddighi–AD Workbench manifest. This review **does not** open a fourth candidate.

## Next discriminating experiment

1. The precise documented gap is **no UNC13A-specific correction shown after a measured functional deficit** (0 of 6 under both readings). This supplies documentary justification for #18 in its specific form and **does not authorize an experiment**: it would still require a measured deficit before first dose, verifiable independent units and specific authorization.
2. Before any design, check whether peer-reviewed Mallika/Cao versions change chronologies or group sizes.

### Independent review: no-cost routes

The same agent performed curation, so independence remains pending. Free routes, ordered by Luis's effort:

- **Wait for peer-reviewed versions.** The source report records Keuss's Nature acceptance and Mallika/Cao as under review. Peer reviewers could assess M-a's chronology with field expertise. Cost: zero; timeframe: months. This is a proposed route, not a guarantee that reviewers will resolve this particular question.
- **Public bioRxiv comment.** A concrete courteous question asking whether baseline grip strength was measured before injection at 6 weeks could resolve the issue. **Explicit authorization is required**, because `AGENTS.md` prohibits unauthorized external communications, and Luis would sign it rather than the agent.
- **ALS research communities.** Open academic forums/lists where a methodological question may receive expert response without cost. The same authorization requirement applies.
- **Paid statistical/methodological review services.** These exist, but the report does not recommend them here: the pending question concerns design criteria rather than statistics, and peer review is a possible free route. Pricing would need to be provided before any expense.

**Abandonment criterion:** if external review identifies an already published *UNC13A-specific* post-deficit intervention, this documentation gap closes and #18 loses the justification described here.

No contacts, costs, personal data, laboratory work or external publication were executed in this cycle. Framework: [AGENTS](../../AGENTS.md), [PROTOCOL](../../research/PROTOCOL.md), [STATE](../../research/STATE.md).
