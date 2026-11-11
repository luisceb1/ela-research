# Paired STMN2: 45 usable donors and a higher cervical ratio

> English translation prepared on 11 November 2026 from the [Spanish original](REPORT.md) at `c7d8f7e92e7eb02e3fb619f6e8984f075ef84784`. Source/translation hashes and review scope: [English guide](../../docs/ENGLISH_GUIDE.md#translation-policy-and-review). This is a dated report, not a new analysis or publication-status check.
> Earlier proposed next steps are historical; for completed STMN2 work and current stop rules, use the [closing report](../stmn2-within-region-20261111/REPORT.en.md) and [current findings](../../docs/CURRENT_FINDINGS.md).

11 November 2026. **Exploratory evidence**, same previously inspected cohort; not independent replication. [Protocol](../../research/plans/2026-11-11-paired-stmn2.md), commit `60b1246c44b0ff1f8e7cb7a6579a2a0ee0340fb0`, fixed before counting eligible pairs or calculating differences. Prior marginal results were already known and motivated the question.

## Evidence

Only existing counts and the technical sources pinned in the [audit](../stmn2-map-audit-20261111/REPORT.en.md) were used. Requirements were concordant exact links through both metadata routes, declared donor, compatible region/project, a single library per region, and a known identical preparation method. Groups come from the original JSON. No new clinical columns were used and no donor rows were exported.

The joint route has 104 donors shared between tissues, a subset of the 128 linked by the primary source. Of those 104, 29 are not pure ALS in both regions, one has discordant preparation, and 29 do not reach C+K≥20 in both tissues: **45 pairs** remain. There are 25 Manual KAPA Total and 20 Automated KAPA Total pairs. There are no multiplicities among these 104; the previously detected cervical duplicate does not contribute an accepted pair in this subset. Independence is not inferred by selecting a better-covered library.

Endpoint: within-donor difference, cervical minus cortex, in the local ratio K/(C+K). C=canonical junction, K=entry to cryptic terminal exon 2a. K zeros are included when the denominator is adequate.

| C+K threshold in both tissues | ALS pairs | Cervical higher | Ties | Cervical lower | Median difference |
|---|---:|---:|---:|---:|---:|
| ≥20, primary | 45 | 24 | 14 | 7 | +0.003676 (0.368 percentage points) |
| ≥50, descriptive sensitivity | 32 | 20 | 8 | 4 | +0.010665 (1.066 percentage points) |
| ≥100, descriptive sensitivity | 22 | 14 | 7 | 1 | +0.010007 (1.001 percentage points) |

The prespecified gate (≥10 pairs and ≥5 nonzero differences) passes: 45 pairs, 31 nonzero differences. The sole primary comparison, a two-sided exact sign test, gives **nominal p=0.0033268929** (24 versus 7). No additional tests were performed on the sensitivities. The directional prediction of a positive median is observed in this subset; it is not presented as external confirmation.

Median total junction counts are **845 in cortex and 89 in cervical cord** among the 45 pairs; median canonical counts are 844 and 80. Pairing does not equalize depth or precision. The sensitivities retain the direction but retain different subsets and do not replace an adjustment for assay bias.

The descriptive control leaves **4 control pairs** at threshold 20 (one cervical higher, three ties; median zero). Thresholds 50 and 100 leave three and two pairs. ALS is not compared with controls and disease specificity is not claimed at these sizes.

## Interpretation

The prior marginal pattern does not disappear when paired donors and compatible preparation are used: in this subset, the local STMN2 ratio is usually higher in cervical cord. The analysis reduces confounding by differences between people and by the recorded preparation method. The median primary local effect is small and does not represent a percentage of affected neurons or an amount of functional protein.

## Limitations and alternatives

- **Extraction/sequencing batches**, RIN, pTDP-43 burden and cell composition are unknown in this analysis. The same preparation method does not mean the same batch. Absence of technical confounding has not been demonstrated.
- Coverage, RNA stability, neuronal loss and glial proportion can affect detection and the ratio. The C+K threshold selects on a variable dependent on expression/quality and can induce bias.
- The exact sign test assumes probability 1/2 for each direction under its null and independent donors. Unequal depth and discrete zeros can affect that symmetry even without differences in a latent molecular fraction. Its p-value is **nominal for the observed differences**, not evidence that measurement biases or all confounders have been eliminated.
- There is no new cohort: choosing this question after seeing the marginal difference limits any confirmatory interpretation. Both metadata routes concern the same cohort.
- The junctions do not distinguish alternative polyadenylation endpoints or measure molecular rescue, neuronal function or clinical benefit. Neuronal-type dependence has not been tested.
- The 45 pairs are not 90 biological replicates or the 128 potential pairs in the broader map. The audit's 20 missing links were not filled by inference.

## Next discriminating test and stopping rule

This cycle ends with the single fixed comparison. The next question is whether the pattern persists with **cell composition and RNA quality characterized**, ideally in an independent paired cohort. Before new analyses, inspect a concrete manifest providing those fields and coverage; do not launch a broad search or repeat filters until another p-value is obtained. Without that input, the result remains an exploratory tissue association. This does not change UNC13A #37 or functional K26 #44 gates, and does not require reinterpreting the signal as a discovery.

## Reproduction

```sh
python scripts/paired_stmn2.py --source-root /ruta/temporal/stmn2-audit-work --output /ruta/temporal/paired.json
python -m unittest discover -s tests -p test_paired_stmn2.py -v
```

The source directory contains the exact files in `reports/stmn2-map-audit-20261111/sources.json` and a `repo` subdirectory with the historical JSONs at their original paths. `results.json` records SHA-256 of every input and the Python version. Six new tests verify exact tails, ties, zeros, multiplicity before filtering, preparation compatibility and both stopping conditions. They also run in the complete CI suite. Only aggregates are exported.
