# recount3 non-SRA collections — inventory — 12 November 2026

**Catalogue listing only. Nothing was measured and no junction file was downloaded.** Six project indexes, 631 KB total.

## Correction first

In the previous session summary I suggested `TARGET_ALS` and `ANSWER_ALS` as collections that "were never inspected". **That was wrong about TARGET_ALS**, and one grep would have caught it before I said it.

TARGET_ALS has already been worked through this project via recount3, in two full prespecified cycles with their own correction histories: [motor cortex, 149 samples](../target-als-cortex-20261111/REPORT.md) and [cervical cord vs cortex, 22.34×](../target-als-cervical-20261111/REPORT.md). It is not a new route. ANSWER_ALS is genuinely uninspected, and `research/BACKLOG.md:172` already recorded it as an open item requiring a new plan because it answers a different question.

## What the six collections hold

| Collection | Samples | Projects | Content | Status for this project |
|---|---|---|---|---|
| **ANSWER_ALS** | 2,229 | 4 (V5 1117, V3 640, V2 306, base 166) | ALS patient cohort | **Uninspected.** Open backlog item; patient cohort, not a depletion experiment |
| **TARGET_ALS** | 683 | 5 tissues | ALS post-mortem tissue | **Prior work** for cortex motor lateral (149) and cervical (164). Three tissues untouched: motor medial 148, lumbar 147, thoracic 75 |
| **gtex** | 19,214 | 32 | Non-diseased tissue; BRAIN 2,931, NERVE 659 | **Uninspected.** Candidate *negative control*, not a candidate source |
| **tcga** | 11,348 | 33 | Cancer | Irrelevant to this question |
| **ega** | 8,783 | 3 | YOUNG_MICROGLIA_SC 8,662; BULK 102; **SPORADIC_ALS_EGAD00001006022 19** | Uninspected; the ALS set is 19 samples |
| **LIBD** | 1,203 | 3 | DLPFC 409 + 398, hippocampus 396 | **Uninspected.** Candidate *negative control* |

## The gap worth naming

The most useful thing in this inventory is not a new candidate source. It is a **control that was never measured**.

This project has counted UNC13A cryptic-junction reads in ALS post-mortem cortex — the TARGET_ALS cycle reports 1–4 reads per positive sample — but it has **never established what that locus looks like in non-ALS brain at comparable depth**. Without a baseline, "1–4 reads in ALS tissue" cannot be told apart from whatever the assay produces in tissue with no TDP-43 pathology. `gtex` BRAIN (2,931 samples) and `LIBD` DLPFC/hippocampus (1,203) are exactly that baseline, and both are in recount3 with junction counts, reachable by the probe already in this repository.

That is a control for existing published numbers, not a new source for issue #37, and it should not be sold as one. It would qualify or strengthen a result the project already holds, which is a different and more honest kind of progress than another candidate hunt.

**Practical constraint, unverified:** the TARGET_ALS cortex download was 194 MB for 149 samples. Scaled naively, gtex BRAIN would be well into the gigabytes. A baseline cycle would need either a tissue subset or a different byte strategy, and that must be settled in a plan before anything is fetched — the per-collection junction file sizes were **not** checked here.

## The other three, assessed honestly

**ANSWER_ALS** is the largest uninspected set and is genuinely open. It is a patient cohort, so it cannot answer the depletion question that issue #37 asks. Whether its material is patient-derived iPSC lines or tissue, and whether recount3 serves its junction counts without controlled-access terms, are **unverified here** and would have to be established before any plan, not assumed from the collection's presence in the index.

**ega SPORADIC_ALS_EGAD00001006022** is 19 samples. Small, directly ALS, and uninspected. Access terms unverified.

**TARGET_ALS's three remaining tissues** are the weakest lead despite looking like free data. The existing cycle established that this cohort's metadata **does not expose donor identity**, so motor medial cortex cannot be shown to be different donors from motor lateral. More samples from the same cohort are not independent observations.

## Boundaries

Catalogue listing from each collection's `recount_project` index. No junction counts, no coverage, no effects, no new candidate accepted. Sample and project counts are the indexes' own; tissue and content descriptions come from project names and are not independent verification of what each deposit contains. Access terms were not checked for any collection. The 20-read minimum, the three-background question and issue #37 are all untouched. No contact, cost or personal data.
