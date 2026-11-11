# Fig.4d design review: original values available, strict v1 gate not yet met

11 November 2026. Scope: complete the planned source/unit/design inspection before any model fit. [Original prospective plan](../functional-rescue-20261103/REPRODUCTION_PLAN.md). No effect, group mean, recovery fraction or p-value was calculated. The original disabled contract and validator remain unchanged.

## Verified evidence

- Final Fig.4d's vertical axis is **Amplitude (nA)**. The published source entries are positive magnitudes on that displayed scale. The figure was inspected visually; its URL/hash is in `design_review.json`.
- The final legend reports **34 control / 30 KD / 25 KD+M21-6 neurons from three independent differentiations**. Methods, *Autaptic cultures and recordings (Leibniz-FMP-Berlin)*, say data came from three cultures and recordings were made at DIV60–70.
- The public XLSX has three explicit batch blocks and all three conditions in each, as recorded by the deposited inspector. A row coordinate identifies a source entry, not an original cell/culture identity.
- Reporting Summary pp2–3 declares independent differentiations, treatments applied to parallel wells of a differentiation, no sample randomization, and blinded spinal motor neuron electrophysiology. It declares all data included; a per-record QC/exclusion ledger is not supplied in this panel.
- The actual R implementation is a REML Gaussian LMM on log1p values with group and a batch random intercept. The public workbook has title/header rows and multiple sheets; the author's interactive script does not directly select the 4d sheet/header without adaptation. The README describes a different workflow and cannot substitute for inspecting the R file.

## A real discrepancy in our contract: pA versus nA

The historical FR-K26-4d v1 contract hard-codes `pA_magnitude`. The final figure uses **nA**. This is a project-input discrepancy, not an accusation of a paper error.

Unit conversion before `log1p` is not innocuous: `log(1+1000*x)` is not `log(1+x)` plus a constant. The planned primary reproduction must preserve the source numerical scale used by the authors. Merely multiplying these values by 1000 to make an old pA validator pass could change fitted coefficients and uncertainty. A prospective unit/version amendment is required before fitting. No conversion or fit was performed here, and the original contract is not silently rewritten as if it had always specified nA.

## Why the strict gate remains closed

The scientific reporting supports three declared independent differentiations and the batch layout is consistent with that design. It does **not** supply the complete exact key map required by our strict v1 schema: individual cell, culture and coverslip identifiers, multiplicity/repeat mapping and exact recording day per cell. Neither counts nor three generic labels verify that full hierarchy. No lab-origin IDs or exact dates are fabricated from worksheet positions, and no AI review is labelled a human independence approval.

This is a limitation of the inspected metadata **relative to our specified contract**, not a demonstration of pseudoreplication or invalidity of the published study. A conditional replay treating the three published labels as the reported experimental blocks is computationally possible. It would require an explicit prospective amendment defining that assumption and its narrower interpretation; it must not be presented as satisfying the original full metadata gate. That alternative was not executed in this review.

## The smallest useful next input

An author clarification should establish whether Batch 1–3 correspond one-to-one to the declared independent differentiations, whether each numeric entry represents a distinct neuron, and whether shared cultures/coverslips or repeat recordings add nesting. An existing technical mapping and any available recording-day/QC information are welcome; no custom schema or new experiment is requested.

The follow-up is [drafted](../../research/drafts/2026-11-11-fratta-published-fig4d-metadata.md), not sent. It acknowledges the now-public values and asks only about remaining design information. Its authorization is separate from the already approved source review.

## Reproduction and limits of this review

`inspection.json` and `scripts/inspect_k26_fig4_source.py` reproduce workbook identity and count checks. `design_review.json` pins the visual/source documents and records manual locators. `strict_v1_status.json` distinguishes file availability from strict-contract readiness. Re-running the original validator on the still-disabled original contract returns the expected blocked decision; its historical reason predates publication and is superseded by this dated review.

No R model was installed or executed because the strict prerequisite was not met. Software tests do not fill missing design metadata. The remaining clarification is bounded; it does not reopen STMN2 or another UNC13A endpoint.
