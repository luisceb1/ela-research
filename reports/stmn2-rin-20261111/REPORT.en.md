# STMN2 and RNA quality: a positive pattern in 19 pairs, a limit under the strictest filter

> English translation prepared on 11 November 2026 from the [Spanish original](REPORT.md) at `c7d8f7e92e7eb02e3fb619f6e8984f075ef84784`. Source/translation hashes and review scope: [English guide](../../docs/ENGLISH_GUIDE.md#translation-policy-and-review). This is a dated report, not a new analysis or publication-status check.
> Earlier proposed next steps are historical; for completed STMN2 work and current stop rules, use the [closing report](../stmn2-within-region-20261111/REPORT.en.md) and [current findings](../../docs/CURRENT_FINDINGS.md).

11 November 2026. **Exploratory sensitivity in the same cohort**, without independent replication or new p-values. [Protocol](../../research/plans/2026-11-11-paired-stmn2-rin.md) fixed at `c444b5443b671f0aa8436109eb05a600f1fb0b86` before joining quality to STMN2 differences. The original result and general availability of RIN were already known.

## Evidence

The **45 original pairs** were reproduced using exactly the previous rules: pure ALS in both tissues, one library per donor/region, compatible preparation and C+K≥20 in both. The 90 libraries link to NYGC ST3 through an exact unique RNA key; **all 45 pairs agree on donor, region and preparation and have valid RIN**. There was no fuzzy recoding or exclusion for identity discrepancies. The mixed workbook remains temporary, without adding donor rows to the repository.

The primary rule was **RIN≥6 in both tissues and absolute RIN difference≤1**. The secondary descriptive rule raised the minimum to 7. These are operational rules fixed for this sensitivity, not universally validated assay thresholds. No further cutoffs were searched and the minimum of ten pairs for interpreting the prediction was not relaxed.

| Set | Pairs | Cervical higher | Ties | Cervical lower | Median cervical−cortex |
|---|---:|---:|---:|---:|---:|
| Original, no RIN filter | 45 | 24 | 14 | 7 | +0.003676 (0.368 percentage points) |
| RIN≥6 both and difference≤1, primary | **19** | **10** | **8** | **1** | **+0.002551 (0.255 percentage points)** |
| RIN≥7 both and difference≤1, secondary | **9** | **4** | **4** | **1** | **0** |

The primary filter retains the positive direction with 19 pairs; the stricter one leaves nine, below the fixed gate, with an observed median of zero. **This does not support uniform robustness to RNA quality.** Nor does it demonstrate that improving RIN removes the effect: these are different small subsets, not an intervention on quality.

In the 19 primary pairs, median RIN is 6.9 in cortex and 7.2 in cervical cord, with median absolute difference 0.5. Median C+K denominators remain very different: **1150 versus 120**. In the nine strict pairs they are 921 versus 53. Comparable RIN does not equalize depth or eliminate discrete detection bias.

### Exclusions and selection

The primary filter excludes 26 compatible pairs. Their directions are 14 cervical higher / 6 ties / 6 cervical lower, with median difference +0.011059. The strict filter excludes 36 pairs, with 20/10/6 and median +0.010007. Nonexclusive reasons (low RIN in at least one tissue and RIN difference>1) are quantified in `results.json`; a pair can fail both rules. Excluded pairs are neither imputed nor added to the selected set.

Original results are not changed or replaced by the most favorable sensitivity. No adjusted regression, additional significance test, control comparison or endpoint change was performed. K=0 remains eligible if its denominator is sufficient.

## Interpretation and limitations

The cervical/cortex difference **does not disappear descriptively** under the primary quality restriction; this supplies a concrete check on an alternative explanation. Its median magnitude is smaller than in the original 45 pairs, but comparing these medians across subsets does not quantify a causal RIN effect.

The strict sensitivity supplies a material limitation: median zero and only nine pairs. The appropriate statement is descriptive persistence under the primary filter, with an inconclusive strict-filter result, not a fully quality-adjusted association. Thresholds were fixed after the marginal pattern was known, so they are not external prospective confirmation either.

Unmeasured cell composition, unknown actual extraction/sequencing batch, coverage/RIN selection, RNA stability and unequal depth remain. Whole-tissue RIN may not reflect each transcript's or cell's integrity equally. Neither this check nor the previous one establishes neuronal-type dependence, TDP-43 burden, function or rescue. UNC13A #37 and K26 #44 gates do not change.

## Next discriminating test

The RIN task is complete. The next concrete input is the already located **NYGC ST7 table of estimated cell composition**. Before using it, fix an inspection/extraction protocol and confirm per-library granularity, exact keys and estimation method. If it is aggregate-only or does not link to our pairs, it cannot adjust this comparison. If usable, then fix a single appropriate model/sensitivity before calculating its effect. Do not add RIN cutoffs until another conclusion is obtained or treat the same donors as independent replication.

## Reproduction and verification

```sh
python scripts/stmn2_rin_sensitivity.py --source-root /ruta/temporal/stmn2-audit-work --output /ruta/temporal/rin.json
python -m unittest discover -s tests -p test_stmn2_rin_sensitivity.py -v
```

ST3 source: workbook `NYGC_Flagship_ST_1_3_Metadata.xlsx`, [Zenodo 20090702](https://zenodo.org/records/20090702), SHA-256 `c1bf21493c4a2773e27ff787e60267fc2e1304ce11e84e644c03c700cc68f048`. The script requires that hash and locates ST3 by name and workbook relationships. The source/count directory retains the previous analysis layout; no other clinical worksheets are used.

`results.json` records hashes of all inputs and aggregates only. Five new tests verify inclusive boundaries, missing/nonfinite/out-of-range RIN, incorrect donor/region/preparation, duplicate keys, cryptic zeros, the 45-pair guard and the minimum of ten for directional interpretation. No randomness or new downloads. PR CI runs compilation and the complete offline suite.
