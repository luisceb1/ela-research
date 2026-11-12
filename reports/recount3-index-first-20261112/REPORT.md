# Index-first candidate search — 12 November 2026

**Zero new eligible candidates. The prediction holds, and the binding constraint has moved.** Twelve recount3-held projects perturb TDP-43 in human material; none is an unaudited neuronal depletion experiment with three or more replicates per arm. No junction counts were downloaded and no coverage was measured.

Executed against the [plan committed before the first query](../../research/plans/2026-11-12-recount3-index-first-candidates.md), `6318d6d`.

## Method and budget

The recount3 human SRA project index was reused from cache, hash reproduced: `f28cbb775b5037c91250c353b2c422c046fc43426d33a8191c71a81705e55b01`. Three NCBI E-utilities queries against `db=sra` (TARDBP whole-transcriptome; TDP-43 or TARDBP with knockdown/knockout/depletion; TARDBP with shRNA/siRNA/CRISPR), resolved to study accessions through `efetch rettype=runinfo`, giving **42 distinct SRA studies**. Three of the six permitted queries were used.

Intersecting those 42 with recount3's holdings leaves **12**. For six of them the deposit's own per-project metadata was then read from recount3 (`sra.sra.<project>.MD.gz`, 1.8–7.2 KB each), so model and contrast below are the deposits' declared labels, never inferred from titles or run order.

Transfers beyond the cached index: about 2.1 MB, against a 10 MB cap.

## The intersection

Full fields in [candidates.tsv](candidates.tsv); raw intersection in [intersection.json](intersection.json).

| Project | recount3 runs | Declared contrast | TDP-43 depletion arm | Decision |
|---|---|---|---|---|
| SRP166282 | 18 | TDP-43 KD vs control, iPSC motor neurons | 6 | **Prior work** — Klim 2019, already measured and rejected on cryptic coverage |
| SRP069787 | 16 | TDP43 Knockdown vs Scramble, iPSC motor neurons | **2** | **Near miss** — right model and contrast, too few replicates |
| SRP169127 | 6 | TARDBP shRNA vs two control hairpins, SH-SY5Y | **2** | Near miss — neuroblastoma line, 2 KD libraries |
| SRP219885 | 6 | TDP-43 KO vs **rescued** KO, HeLa M | 3 | Rejected: non-neuronal |
| SRP496259 | 32 | TDP-43ΔNLS:YFP **overexpression** vs YFP, iPSC motor neurons, line 11a | 0 | Rejected: overexpression of mislocalised TDP-43, not depletion |
| SRP358326 | 15 | TARDBP K263E vs wild-type, iPSC neurons and NPC | 0 | Rejected: point mutation |
| SRP254044 | 10 | TARDBP M337V patient lines, iPSC motor neurons | 0 | Rejected: patient mutation |
| SRP069789 | 18 | FUS and TAF15 KD time course, NPC | 0 | Rejected: no TDP-43 arm |
| SRP399239 | 47 | VCP ATPase inhibition, ALS motor neurons | 0 | Rejected: not TDP-43 depletion |
| SRP576070 | 12 | TDP-43 aggregate exposure, immune cells | 0 | Rejected: non-neuronal |
| SRP013565 | 2212 | ENCODE RIP-seq | 0 | Rejected: wrong assay |
| SRP057819 | 2 | TDP-43 knockdown, HeLa | 1 | Prior work, non-neuronal |

## The prediction, and what it got right and wrong

The plan predicted the intersection would be **dominated by already-audited families**, with zero to two unaudited survivors. Zero survivors is the outcome, so the prediction is not refuted.

It was wrong about the mechanism, and that matters more than the count. Only two of the twelve are prior work. The other ten are genuinely new to this project — they were simply never eligible. The earlier source gate did not miss accessible material; the material that exists does not answer this question.

## The constraint has moved

Three screens have now failed for three different reasons, and the sequence is the useful result:

- Stage A (PR #64): failed on **genetic background** — every candidate was a single isogenic line.
- Availability (PR #67): failed on **recount3 holdings** — all three candidates absent.
- This screen: fails on **replicate count** — the two projects with the right model and the right contrast have **two** biological replicates per arm.

Two replicates per arm is a 2016-era design norm, which is exactly what a catalogue built in 2019 is full of. Depth was never the limiting factor in this screen, and it was not tested.

## One judgement that belongs to Luis, not to me

**SRP069787 is the sharpest near miss and should not be dismissed quietly.** It is iPSC-derived motor neurons, the deposit itself declares `TDP43 Knockdown` against `Scramble Knockdown`, recount3 holds its junction counts, and it is not prior work. It fails only the three-replicates-per-arm floor.

That floor was my own addition in the Question A plan, introduced for a coverage *table*. Question A's actual question is narrower: *is the UNC13A cryptic junction observable at adequate depth in an independent neuronal TDP-43 depletion deposit?* Two knockdown libraries can answer that, because detection at depth is not an inferential contrast. They cannot support any effect, fraction or test, and nothing here proposes one.

So the choice is real and it is not mine: either the floor stands and this screen closes at zero, or the floor is explicitly relaxed **for the detection question only**, in a separate amendment that says so in advance and forbids any inference from two libraries. Relaxing it after seeing that it is the only thing in the way is precisely the threshold-tuning this project guards against — which is why it is recorded here as an open decision rather than taken.

SRP219885 is noted for one reason only: it is the single **KO-plus-rescue** design the search surfaced. It is HeLa, so it is not a candidate for this question, and it is recorded so that the design is not forgotten if the question ever changes.

## What this does and does not establish

No eligible new source was found for Question A, under the criteria as written. This is a closed finite screen over three queries and twelve intersected projects — **not** proof that no public junction counts can answer the question, and not a statement about recount3's future updates, its other collections (`gtex`, `tcga`, `ANSWER_ALS`, `TARGET_ALS`, `ega`, `LIBD`) or non-recount3 routes.

No coverage was measured. The 20-read minimum was neither applied nor relaxed. The three-background question from PR #64 is untouched. Issue #37 stays closed and nothing here nominates a design review. No contact, access request, cost or personal data.
