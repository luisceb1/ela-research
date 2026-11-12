# Amendment to the Question A plan — replicate floor relaxed for detection only

Date: 12 November 2026. Base: merged main `ae832eff1e68d481f74fa9d384b6842a1fc439bd`.
**Committed before any junction count is downloaded or any coverage measured.**

## What is being changed, and the honest circumstance

The [Question A plan](2026-11-12-questionA-measurement-reproducibility.md) required at least three replicate libraries per arm. The [index-first screen](../../reports/recount3-index-first-20261112/REPORT.md) found that this floor is the **only** thing excluding SRP069787, and Luis then authorised relaxing it.

That sequence is exactly the circumstance in which a relaxed threshold is least trustworthy: the obstacle was identified first, the rule changed second. Nothing can undo that ordering. What can be done, and is done here, is to **fix every outcome criterion now, before any count is seen**, so that the result cannot be shaped after the fact. This amendment is written to be falsifiable against itself: if the numbers come back and any rule below is then altered, the alteration is visible in the diff.

## Scope of the relaxation

**Relaxed:** the replicate floor drops from three to **two libraries per arm**, for **SRP069787 only**, and for the **detection question only**.

**Rationale, stated in advance.** Question A asks whether the UNC13A cryptic junction is *observable at adequate coverage* in an independent neuronal TDP-43 depletion deposit. Detection at depth is a property of a single library; it is not an inferential contrast, and it does not require replication to be meaningful. The three-replicate floor was introduced for a coverage *table*, which is a different purpose.

**Not relaxed, and not relitigated by this amendment:**

- The **20-read minimum** on each sealed cryptic junction. It is not lowered, and it is not lowered later if the result lands just below it.
- The three-genetic-background question from PR #64, which remains closed negative over inspected sources.
- Issue #37, which stays closed.
- The sealed targets and their coordinates.

## Prespecified outcome interpretation

Fixed before measurement. Each outcome maps to one conclusion and no other:

| Observation | Conclusion, fixed in advance |
|---|---|
| Canonical junction **not** measured in every selected library | The measurement failed at this locus. **Nothing is concluded** about the cryptic junctions, in either direction |
| A sealed cryptic junction reaches **≥20 reads** in at least one TDP-43 knockdown library, with canonical measured throughout | **Detected at threshold.** Licenses one thing: a separate prospective design review. Not an effect, not validation, not replication |
| Cryptic maximum **>0 but <20** | Below threshold. **Missing data at this depth**, never a biological zero. Question A closes for this deposit |
| Cryptic **0 in all libraries**, canonical measured | Same reading: missing data at this depth, not evidence of absence. Question A closes for this deposit |

## Explicitly forbidden in this cycle

No PSI, fraction, ratio, normalisation, effect size, confidence interval, p-value or model. **No knockdown-versus-scramble comparison of any kind** — with two libraries per arm that would be exactly the inference this relaxation does not buy. No pooling with SRP166282 or any other project. No substituting a different junction if the sealed ones are absent. No second pass with a lowered threshold. No extension to a further project on the strength of this one.

The scramble libraries are downloaded and reported **only** so the canonical positive control and the deposit's own declared labels can be read across the whole project. They are not a comparison group here.

## Execution parameters

- Project: **SRP069787**, 16 runs in recount3, declared `TDP43 Knockdown` ×2 and `Scramble Knockdown` ×2 among other arms (FUS, TAF15, FUS R521G, WT sibling controls) which are not part of this question.
- Files: the five recount3 files the probe requires. Cap 150 MB; stop and report if exceeded.
- Probe invoked with `--project-id SRP069787`, per the fix merged in PR #66. The sealed targets file is used unchanged and its hash verified first; stop on mismatch.
- Record SHA256 and byte size of every downloaded file.
- Report per-junction maximum, samples with any read, samples at or above 20, the canonical control, `assay_shape`, and the deposit's declared labels. Nothing else.

## Boundaries

This is a single bounded detection measurement on one deposit. It is not biological replication, not independent validation in the cross-background sense, and not evidence about functional recovery, therapeutic rescue or clinical benefit. Two libraries per arm cannot support any inferential claim and none will be made. No contact, access request, cost or personal data.
