# Non-ALS spinal cord source for the cervical control

Date: 12 November 2026. Base: merged main `06705591e8fa548b873c7bb3ef7ef0644910fda9`.
**Committed before any discovery query or download.**

## Correction that reframes the question

I stated after the [gtex BRAIN control](../../reports/gtex-brain-negative-control-20261112/REPORT.md) that the published cervical measurement "has no non-ALS baseline". **That is wrong.** The [cervical report](../../reports/target-als-cervical-20261111/REPORT.md) already carries **13 non-neurological controls per tissue**, from the same cohort and the same pipeline:

| Tissue | Group | n | Canonical median | Canonical per million | Detection |
|---|---|---|---|---|---|
| Motor cortex | ALS Spectrum MND | 84 | 102 | 2.530 | 0.190 |
| Motor cortex | Non-neurological control | 13 | 148 | 2.845 | 0.000 |
| Cervical cord | ALS Spectrum MND | 95 | 5 | 0.113 | 0.053 |
| Cervical cord | Non-neurological control | 13 | 8 | 0.174 | 0.000 |

A same-cohort control is **stronger** than any external one, because it avoids exactly the cross-study weakness that makes the GTEx comparison weak. The existing control is limited by **n and depth**, not missing.

So the question is not "is there a baseline" but: **is there a non-ALS spinal cord source with enough UNC13A coverage to improve on 13 controls at canonical median 8?**

## Prediction, refutable

**No public non-ALS spinal cord RNA-seq source will have materially better UNC13A coverage**, because the limitation is a property of the tissue, not of the cohort. UNC13A canonical coverage is about 22× lower in cervical cord than motor cortex in TARGET_ALS, and GTEx independently shows cervical median canonical 1.0 against cortex 15.0. Two independent cohorts agree. Standard-depth bulk RNA-seq of spinal cord will not clear the 20-read bar at this locus.

**Refuted by** any non-ALS spinal cord project with a median canonical count at or above 20, or with a substantial share of libraries in the 102–148 window used for the cortex control.

## Method, index-first

1. Enumerate spinal cord holdings already known: GTEx `Brain - Spinal cord (cervical c-1)` (171, measured: median canonical 1.0, max 21) and TARGET_ALS cervical / lumbar / thoracic (164 / 147 / 75, ALS cohort with 13 controls).
2. At most **four** E-utilities queries for human spinal cord RNA-seq, resolved to study accessions, intersected with the recount3 SRA project index before anything else.
3. For survivors, read declared tissue and disease status from the deposit's own recount3 metadata.
4. Measure canonical coverage **only** for a survivor that is non-ALS spinal cord and plausibly deep, and only to test the prediction above. Cap 1.5 GB.

## Boundaries

No effect, PSI, ratio, p-value or model. No ALS-versus-control test. The 20-read minimum stands. A negative result closes this as a tissue-level coverage limit, **not** as proof that no such deposit exists. Issue #37 and the three-background question are untouched. No contact, access request, cost or personal data.
