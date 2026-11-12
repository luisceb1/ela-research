# Question A detection measurement — SRP069787, 12 November 2026

**Interpretation correction — 12 November 2026:** reviewed against committed outputs; see the [correction record](../nov12-interpretation-review-20261112/REPORT.md). Counts and executed prospective rules are preserved; the stronger original interpretations are superseded below.

**Not detected. Question A closes for this deposit without sufficient cryptic support, not as evidence of biological absence.** Low canonical counts provide a coverage warning; they do not identify the sole cause of non-detection.

Executed under the [amendment committed before any count was downloaded](../../research/plans/2026-11-12-questionA-amendment-detection-floor.md), `daf9d24`, which fixed every outcome reading in advance.

## Result

Sealed targets verified unchanged first (`e35f6e05…bc3a`). Probe run with `--project-id SRP069787`. 16 libraries, `assay_shape` not flagged as targeted.

| Junction | Max reads | Libraries with any read | At or above 20 | Present in recount3 |
|---|---|---|---|---|
| canonical (positive control) | 26 | **16 / 16** | 3 | yes |
| cryptic_left | **0** | 0 / 16 | 0 | **absent — no row** |
| cryptic_right | **0** | 0 / 16 | 0 | **absent — no row** |

`gate_met` is false. Both sealed cryptic junctions are absent from the project's junction catalogue entirely, which is what zero supporting reads across all 16 libraries looks like.

Per-library canonical counts, with the deposit's own declared labels:

| Run | Declared label | Canonical |
|---|---|---|
| SRR3153259 | **TDP43 Knockdown Rep1** | **9** |
| SRR3153260 | **TDP43 Knockdown Rep2** | **2** |
| SRR3153255 | Scramble Knockdown Rep1 | 5 |
| SRR3153256 | Scramble Knockdown Rep2 | 7 |
| SRR3153251 | FUS Knockdown Rep1 | 26 |
| SRR3153252 | FUS Knockdown Rep2 | 23 |
| SRR3153257 | TAF15 Knockdown Rep1 | 22 |
| SRR3153258 | TAF15 Knockdown Rep2 | 17 |
| SRR3153265 | WT Sibling Control Rep 2 | 19 |
| SRR3153263 | FUS R521G Rep 3 | 16 |
| SRR3153254 | FUS and TAF15 Knockdown Rep2 | 12 |
| SRR3153266 | WT Sibling Control Rep 2 scramble shRNA treated | 8 |
| SRR3153253 | FUS and TAF15 Knockdown Rep1 | 7 |
| SRR3153262 | FUS R521G Rep 2 | 7 |
| SRR3153255 / SRR3153264 | Scramble Rep1 / WT Sibling Control Rep 1 | 5 / 5 |
| SRR3153261 | FUS R521G Rep 1 | 4 |

The non-TDP-43 arms are listed only to show the canonical control across the project. They are not a comparison group and no comparison was made.

## Reading, fixed in advance

The amendment's table maps this outcome to one conclusion and no other: canonical measured in every library, cryptic zero everywhere → **missing data at this depth, never a biological zero.** Question A closes for this deposit. No PSI, fraction, effect, interval, p-value or knockdown-versus-scramble comparison was computed, and none will be.

## What the numbers add beyond that

The two TDP-43 knockdown libraries carry **9 and 2 canonical reads**, while both cryptic counts are zero. Canonical and cryptic junctions are alternative paths; the observed canonical count is not an upper bound on the cryptic count, and a cryptic fraction relative to their combined counts can exceed one half. The earlier claim that 20 cryptic reads were impossible at any plausible fraction is withdrawn. No fraction or required sequencing depth is estimated here.

Relaxing the replicate floor did not produce an eligible measurement: the observed cryptic counts still fail the fixed support requirement. Replicate count remains a separate design constraint; this result does not show that it was irrelevant or that sequencing depth uniquely caused the negative. Depletion efficacy, assay, mapping and biology remain unresolved alternatives.

For scale: SRP166282 reached a canonical maximum of 66 and a cryptic maximum of 5, and was rejected on coverage. SRP069787's canonical maximum is **26**. It is shallower at this locus than the deposit already rejected.

## Incidental verification of the PR #66 fix

The result file reports `"project": "SRP069787"` with `"targets_provenance_project": "SRP166282"` in its own field. Run against the pre-fix probe, this file would have claimed to be SRP166282 — the already-rejected Klim dataset — while containing SRP069787's counts. The fix is doing exactly what it was written for, on the first new project measured after it.

## Provenance

Five recount3 files, 21 MB against a 150 MB cap, from `duffel.rail.bio/recount3/human/data_sources/sra/`:

| File | Bytes | SHA256 |
|---|---|---|
| sra.junctions.SRP069787.ALL.RR.gz | 9,590,063 | `fcf742763994c1752910b10f3221680596e98bc5d446235ec3723e2a9e71d539` |
| sra.junctions.SRP069787.ALL.MM.gz | 11,533,110 | `40efbb358c5057838eb11f8e2e8a39180a8e964ec5c8d77049e69ec6a1829f8d` |
| sra.junctions.SRP069787.ALL.ID.gz | 85 | `890f64cf5b2721156fbdd8f7425f70e6ef97705943b6bb9fb1dd295ee533acd7` |
| sra.recount_project.SRP069787.MD.gz | 250 | `61b06ffbedbe00677aa2ef7652af82a930964c1eff08dac03e229cadb8a63963` |
| sra.sra.SRP069787.MD.gz | 2,766 | `f40dea58d4897e2750881f7ee3a9b0b8812bc852e87b7f9ed64035d1f4e1f824` |

Full output in [results_SRP069787.json](results_SRP069787.json).

## Boundaries

One bounded detection measurement on one deposit. Not biological replication, not independent validation in the cross-background sense, and no evidence about functional recovery, therapeutic rescue or clinical benefit. The 20-read minimum was applied as written and is not lowered now that the result is known. The three-background question from PR #64 is untouched. Issue #37 stays closed; nothing here nominates a design review. No contact, access request, cost or personal data.
