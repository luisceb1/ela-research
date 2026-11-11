# Closing the STMN2 cycle: exploratory tissue association and unresolved composition

> English translation prepared on 11 November 2026 from the [Spanish original](REPORT.md) at `c7d8f7e92e7eb02e3fb619f6e8984f075ef84784`. Source/translation hashes and review scope: [English guide](../../docs/ENGLISH_GUIDE.md#translation-policy-and-review). This is a dated report, not a new analysis or publication-status check.

11 November 2026. Final within-region analysis, without new p-values or correction of the tissue effect. [Protocol](../../research/plans/2026-11-11-stmn2-within-region.md) fixed at `3a43db16981ab7dd5d0d887fb46099db74ee45d1` before calculating these associations. Earlier results were already known; this is not external prospective confirmation.

## Evidence from the final analysis

The **45 pure-ALS donors** were retained, with one library per region, compatible preparation, C+K≥20 in both tissues, valid RIN and exact technical links. Cortex and cervical cord were analyzed **separately**, without mixing their MuSiC references.

- Cortical neuronal indicator: Excitatory+Inhibitory sum from reference GSE140231.
- Cervical neuronal indicator: Neurons from GSE190442.
- Outcome: local STMN2 junction-read ratio K/(C+K), not protein or a fraction of diseased neurons.
- Spearman: correlation of average ranks, allowing ties. Partial correlation: outcome and indicator ranks separately residualized against an intercept, RIN ranks, log1p(C+K) ranks and binary preparation; correlation of the two residuals.

Both covariate matrices passed checks for size, distinct values, full rank, numerical condition and residual variation. These are computational checks, not a guarantee of power or causal identification.

| Region | Donors | Spearman | Partial rank correlation | Range when leaving out one donor at a time |
|---|---:|---:|---:|---|
| Cortex | 45 | −0.229 | **−0.299** | −0.364 to −0.247 |
| Cervical | 45 | −0.093 | **−0.105** | −0.185 to −0.054 |

There were 45/45 valid leave-one-donor-out estimates in each region; all retained a negative sign. This is an individual-influence check, **not a confidence interval or replication**. Coefficients are not formally compared between regions, which share donors and use different references.

In the prespecified RIN subset (RIN≥6 both and difference≤1, **19 pairs**), only associations without multivariable adjustment were calculated: Spearman −0.285 in cortex and −0.117 in cervical cord. No cutoffs or variables were added after seeing results.

### A material limitation of the cervical indicator

In cord, **22/45 neuronal estimates are exactly zero** (10/19 in the RIN subset); there are only 24 distinct neuronal values. Cortex has no neuronal zeros and 45 distinct values. A deconvolution zero does not demonstrate histological absence of neurons: it is an estimate from the method and reference. This accumulation of zeros limits the cervical composition probe.

The STMN2 outcome also has ties: ratio zero in 29/45 cortical and 21/45 cervical libraries. A near-zero cervical correlation **does not rule out composition confounding**, estimation error or nonmonotonic relationships. The inverse cortical relationship does not identify a mechanism either: pathology-linked neuronal loss, cell-type mixtures, quality or shared expression between indicator and outcome may contribute.

## Integrated balance of the cycle

| Question | Supported result | What it does not establish |
|---|---|---|
| Is the documented STMN2 event measured? | Sealed junction supported by hg38 literature and genome chain; four cervical ALS samples with K≥20 correspond to four donors | Complete assay validation, function or the cause of UNC13A's limitation |
| Is P1, ≥10× coverage versus UNC13A, met? | **No**: 6.6× raw; 8.085× after input-read normalization | The threshold is not changed to declare success |
| Is there a descriptive tissue difference within donor? | In 45 pairs, cervical higher/tied/lower: 24/14/7; median +0.368 percentage points | Independence from composition, quality or batch; external discovery |
| Does it survive an RIN restriction? | In 19 primary pairs: 10/8/1; median +0.255 percentage points | Uniform robustness: the strictest filter leaves nine pairs and median zero |
| Is composition ruled out? | **No.** Inverse within-region associations and many zeros in the cervical indicator | Correction of the tissue effect or causal neuronal-type dependence |
| Was P3 inferentially confirmed? | No; its original frequencies are descriptive | Confirmation from overlap/nonoverlap of Wilson intervals |

Coverage normalization, medians of ratios and their populations remain distinct. Original counts are unchanged. P2's prediction of obtaining sufficient reads is met in those samples, but does not demonstrate that the previous UNC13A problem was exclusively due to the locus.

## Interpretation and stopping rule

**Final result: an exploratory tissue pattern reproducible within this cohort, partially resistant to quality restrictions, without resolving the composition explanation.** Causality, functional rescue, biological novelty and clinical utility have not been demonstrated. Analyses of the same cohort, even with new tables, are not independent replications.

This cycle is **closed**. No further correlation, RIN threshold or adjustment on these 45 donors is proposed. Further progress requires discriminating input: composition estimates with verified provenance/calibration and, for external validation, an independent cohort with event counts and traceable design/QC. The previously identified EGA collection remains conditional on access and an independence check; nobody was contacted and no controlled data were downloaded.

PR #57 brings together protocols, derivation, maps, quality controls, positive/negative results and limitations for human review. The systematic historical-claim review proposed by Claude is a separate task: it is not duplicated or declared complete here. UNC13A #37 and K26 #44 gates do not change.

## Reproduction and verification

```sh
python scripts/stmn2_within_region.py --source-root /ruta/temporal/stmn2-audit-work --output /ruta/temporal/within.json
python -m unittest discover -s tests -p test_stmn2_within_region.py -v
```

Already pinned sources are used, without additional downloads or clinical columns. The temporary structure follows the preceding steps; `results.json` retains hashes of counts, maps, ST3/ST7 and Python/NumPy versions. Only aggregates are exported, not identifiable donor rows or plots. The algorithm is deterministic and needs no seed.

Eight new tests verify tied ranks, constants, minimum sizes, singular design, removal of synthetic confounding, known residual correlation, absence of residual variation, and failure for missing linkage/reference. Synthetic tests validate the calculation; **they are not biological data or evidence for the hypothesis**. PR CI runs compilation and the complete offline suite with pinned dependencies.
