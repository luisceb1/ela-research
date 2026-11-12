# Question A — UNC13A cryptic-junction measurement reproducibility in a single genetic background

Date: 12 November 2026. Base: merged main `1557bffd03e29a4d565b20e35964b2a42181a31f`.
**Plan for review only. No execution has started.** No recount3 file was downloaded, no coverage was measured and no candidate was accepted when this plan was written.

## Why this plan exists

The Stage A metadata screen (PR #64, not yet merged) closed with zero eligible projects. All four focal candidates failed on the **three-genetic-background** requirement; none failed on depth, assay type or data availability. That requirement was introduced for this project in PR #64's plan, and it answers a cross-background reproducibility question.

Two questions had been conflated. This plan separates them and addresses only the first:

- **Question A, addressed here.** In a previously unexamined public deposit, is the UNC13A cryptic junction directly observable at adequate coverage in a TDP-43 depletion experiment, in a *single* genetic background? This is measurement reproducibility at the locus in a different experiment.
- **Question B, not addressed here.** Does the effect reproduce across independent human genetic backgrounds? PR #64 found no source meeting its fixed requirement. That is a negative result over the inspected sources only. It is not evidence that no such deposit exists, and no claim is made here about what the field does or does not produce.

A positive Question A result is **not** independent validation in the Question B sense, not a biological replication, and not a reopening of issue #37. It would license one thing: a separate prospective design review.

## Question, prediction and failure criterion

**Question.** Using recount3 junction counts and the existing sealed targets, do any of the pre-identified candidate projects measure the canonical UNC13A junction in every selected library *and* reach at least 20 reads on a sealed cryptic junction in at least one knockdown library?

**Refutable working expectation.** At least one candidate exceeds SRP166282's observed canonical maximum of 66 reads. Whether any cryptic junction reaches 20 is genuinely uncertain and is not predicted in either direction. Recording this asymmetry is deliberate: the canonical prediction is checkable and can be wrong; the cryptic outcome is the open question.

**Failure criterion.** If no candidate reaches 20 on a cryptic junction in any knockdown library, Question A closes for these candidates with a published coverage table. The 20-read minimum is **not** relaxed, no fourth candidate is opened, and no PSI, fraction, effect or test is computed to compensate. A below-threshold count is missing data at that depth, never a biological zero.

**Explicitly not a gate.** The "approximately 200 canonical reads" figure in `research/STATE.md` is a *conditional* illustration — about 200 *if* the cryptic fraction is near 0.10. The fraction was never established. It is retained as context for prioritisation and must not be used as a hard exclusion, nor combined with the 20-read minimum as if both were sealed thresholds.

## Candidates

Carried over from PR #64's Stage A inventory. **No new discovery queries, no new search budget, no fourth candidate.** Execution of this plan requires PR #64 to be merged first, so that the records these rows cite are on `main`.

| Candidate | Declared design | Background | Status for Question A |
|---|---|---|---|
| GSE252892 | 3 scrambled vs 3 TDP-43 shRNA, whole RNA-seq, day 7; SMARTer stranded total RNA-seq | WA01, single | Eligible to inspect |
| GSE299341 | 5 non-targeting vs 5 TDP-43 KD soma libraries, day 17; total RNA-seq, UMI protocol | WTC11, single | Eligible to inspect |
| GSE298758 | 3 control vs 3 TDP-43 shRNA standard RNA-seq, day 14 | i3Neurons, background map unresolved | Eligible to inspect; the unresolved map does not disqualify under Question A, and single-background status is **not** asserted |
| GSE307054 | 2 KD libraries only | WTC-11, single | **Excluded**: fewer than three replicate libraries per arm |

Three replicate libraries per arm is required here as a *technical* replication floor for a coverage table, not as a claim of biological or genetic independence. These are cultures or differentiations within one background, and every output must say so.

Each candidate's recount3 processed-file availability is **unverified**. Stage A inspected GEO metadata, not recount3 holdings. A candidate whose counts are not published by recount3 is recorded as unavailable and dropped; no alternative route, FASTQ download or realignment is authorised by this plan.

## Frozen measurement inputs

Reuse unchanged, verified by hash before each run:

- `research/references/unc13a_targets_sealed.json` — `e35f6e05016b30eab89f8d3aacc2d4ec101840e24e2b6f07159e6c5235d0bc3a`
- `scripts/recount3_junction_probe.py` — `0b5fbaf72d331298e820236d2ecdbf58bc359c6eb9be9ab5685da01440ff4f15`

GRCh38, chr19, minus strand, intronic 0-based half-open: canonical `[17641556, 17642844)`, cryptic-left `[17641556, 17642413)`, cryptic-right `[17642541, 17642844)`. The probe converts to `[start0+1, end0]` 1-based inclusive and enforces `length == end - start + 1`. Do not re-derive, shift, accept nearest coordinates or filter on the `annotated` flag — that flag is already recorded as inconsistent between UNC13A and STMN2. **Stop on any hash or convention mismatch; there is no replacement target.**

## Defect to fix before execution: project mislabelling

`scripts/recount3_junction_probe.py:236` sets the output project from the **targets file**:

```python
"project": spec.get("project", ""),
```

`unc13a_targets_sealed.json` carries `"project": "SRP166282"` as provenance. The probe never reads that field for measurement — targets come from `spec["junctions"]` and `spec["chromosome"]` — but it copies it into the result. **Run unchanged against a new project, the output JSON would claim `"project": "SRP166282"`**, silently relabelling new counts as the already-rejected Klim dataset.

The existing `reports/recount3-unc13a-20261111/results_SRP334561.json` nevertheless reports `"project": "SRP334561"`, which the current sealed file cannot produce. How that run was labelled is unexplained and must be established before reuse; if the sealed file was edited in place for that run, its hash seal was broken at that moment.

Required fix, before any new run:

1. Add an explicit `--project-id` argument, required, and use it for the output `project` field. Do **not** edit `unc13a_targets_sealed.json`; its hash must stay as sealed above.
2. Fail loudly if `--project-id` is absent rather than falling back to the targets file.
3. Extend `tests/test_recount3_junction_probe.py` with a regression test asserting that a run labelled with a new project id does not emit `SRP166282`.
4. Re-run the existing SRP166282 inputs and confirm byte-identical measurement output apart from the project label, so the fix is shown not to disturb any recorded result.
5. Record the probe's new hash in the execution report; this plan's sealed hash above then refers to the pre-fix version and is superseded only for the probe, never for the targets.

This is a labelling defect, not a measurement defect. No recorded count, threshold or gate outcome changes.

## Execution budget and stop rule

- At most the three eligible candidates. No fourth, no replacement after a negative result.
- Download only the five recount3 files per project the probe requires (`RR`, `MM`, `ID`, project `MD`, sra `MD`). Hard cap **150 MB total**; stop and report if exceeded.
- Record SHA256 and byte size of every downloaded file, as the two existing result files already do.
- Per project, report per-junction maximum, samples with any read, samples at or above 20, the canonical positive-control result, `assay_shape`, and the deposit's own declared condition labels. Nothing else.
- **No effect, PSI, fraction, ratio, model, p-value, normalisation or cross-project pooling.** Counts and the coverage table only.
- Stop after the three candidates are reported, whatever the outcome.

## Authorisations and boundaries

This plan authorises nothing by being merged. Execution requires Luis's explicit scope decision, and PR #64 merged first. No author contact, access request, paid resource, personal data or clinical inference is involved or permitted. Issue #37 stays closed; a positive result nominates a design review, not an analysis and not a reopening. Question B's negative result stands as recorded in PR #64, scoped to the sources inspected.

Outputs: a plan commit before execution, then a coverage table, execution report and source manifest on a branch, in a reviewable PR, unmerged.
