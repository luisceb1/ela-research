# K26 Fig.4d conditional replay: positive ASO contrast, block sensitivity and unmatched star band

11 November 2026; review clarification added 12 November 2026. **Conditional computational reproduction using the same published observations, not independent biological replication.** The user authorized the narrower published-block replay after the strict v1 limitations were explained. [Plan amendment](../../research/plans/2026-11-11-k26-fig4d-conditional-v2.md) was committed at **`55f84fe26f77d631d417f382bff176ca4528b1f3` before model fitting and group/effect summaries**. Published direction and individual values had already been seen. The original FR-K26-4d v1 contract remains unchanged and disabled; no human independence approval is fabricated.

## Evidence

Exact input: Keuss et al., [Nature DOI 10.1038/s41586-026-11256-2](https://doi.org/10.1038/s41586-026-11256-2), public Source Data Fig.4, worksheet 4d, 89 observations (34 Control, 30 KD, 25 KD+21-6), three explicitly labelled source blocks. Original SHA-256 `7a01e468d3eaf89a2af9bd0c3fb16434f815e3020033df771d9872799cba3eb7`. The [source/design review](../k26-published-source-20261111/DESIGN_REVIEW.md) pins the workbook, final axis and Reporting Summary. Original positive numerical amplitudes are retained in **nA**, the displayed source scale. Source worksheet coordinates are observation provenance, not lab-origin biological cell IDs. Values were not converted to pA, rectified, rounded, imputed or selected by outcome.

Actual R was used: R **4.5.0**, lme4 **1.1-37**, lmerTest **3.1-3**, Matrix **1.7-3**. This is **not** the exact publication environment: Methods states R 4.4.1; Reporting Summary lists 4.2.2. Installed versions and the actual run are recorded in `sessionInfo.txt`, `execution_provenance.txt` and `execution.log`.

### Prespecified primary model

REML, KD reference: `log1p(value_nA) ~ condition + (1 | source_batch)`, Gaussian LMM with Satterthwaite t inference. Pointwise 95% intervals below are model-conditional, not independent-differentiation validation.

| Contrast | Estimate, log1p scale | Pointwise 95% interval | Nominal p | Holm p, two fixed contrasts |
|---|---:|---|---:|---:|
| KD_ASO − KD, primary | **+0.474402** | **+0.132939 to +0.815865** | **0.007036** | **0.007036** |
| Control − KD, secondary | +0.716123 | +0.400305 to +1.031940 | 0.00002085 | 0.00004170 |

The primary fit converged with default nloptwrap (optimizer code 0), was nonsingular, and emitted no warnings. Batch-intercept variance was 0.043987 and residual SD 0.631276. Residual Shapiro–Wilk W=0.988594, p=0.635274, with a visually near-linear Q–Q plot. This does not prove all Gaussian, variance or independence assumptions; it only reports the specified checks. [Residual diagnostics](residual_diagnostics.png).

### Comparison with the publication: direction agrees, the ASO star band does not

The final Fig.4d image displays **three stars for KD versus KD+M21-6**, with the caption defining that band as p<0.001; Control versus KD displays four stars (p<0.0001). Our fixed nA/log1p model gives **p=0.007036** for ASO versus KD, corresponding to **two stars**, and p=0.00002085 for Control versus KD, compatible with four stars.

**Therefore, this is not an exact numerical reproduction of the displayed ASO significance band.** Both contrast directions agree and the ASO contrast remains positive with a pointwise interval above zero in the full model. The exact author coefficients/p-values or a panel-specific executed model output were not recovered. Source identity, unit choice, reference group and the public R formula were checked; the actual R implementation, rather than its mismatched Python/factorial README, guided this replay. The cause of the remaining discrepancy is **unresolved**. Software versions differ; unreported preprocessing or unit/model choices are possibilities, not established explanations. No rescaling, alternative transformation or optimizer was chosen to match a star.

### Fixed leave-one-block-out sensitivity

All three reduced fits converged without warnings and were nonsingular. Each contains only **two source blocks**; these are influence checks, not three replications.

| Omitted source block | ASO−KD estimate, log1p scale | Pointwise 95% interval | Nominal p |
|---|---:|---|---:|
| Batch 1 | +0.376607 | −0.041659 to +0.794872 | 0.076625 |
| Batch 2 | +0.611197 | +0.218328 to +1.004067 | 0.002868 |
| Batch 3 | +0.418454 | −0.026618 to +0.863526 | 0.064829 |

The **direction remains positive in all three**, but two intervals include zero. This does not prove those subsets have no effect. It shows that precision/significance depends on retaining all three blocks, with both sample-size reduction and block composition changing together; the analysis cannot attribute that change solely to one exceptional experiment.

### Original-scale descriptive block summaries

All entries below use equal block weights, regardless of cell count.

| Source block | Mean ASO−KD, nA | Mean Control−KD, nA | Block ratio | Weight in aggregate ratio |
|---|---:|---:|---:|---:|
| Batch 1 | +2.696427 | +7.874400 | **0.342430** | **0.691906** |
| Batch 2 | +0.716321 | +0.683519 | **1.047990** | **0.060059** |
| Batch 3 | +3.253776 | +2.822815 | **1.152671** | **0.248035** |

Equal-block condition means remain KD **1.489972 nA**, Control **5.283550 nA**, KD_ASO **3.712147 nA**; equal-block ASO−KD is **+2.222175 nA**. The prespecified ratio of those mean differences remains **0.585773** (numerator 2.222175, denominator 3.793578). It is a valid, explicitly defined aggregate estimand; it is **not** the mean or median of within-block ratios.

**Review clarification, 12 November:** ratios are heterogeneous, **0.342430–1.152671**, and the point estimates straddle 1. The unweighted mean of block ratios is **0.847697** and their median **1.047990**; these are post-hoc descriptive summaries, not replacements selected to declare a more favorable outcome. If A_b=ASO−KD and D_b=Control−KD, then sum(A_b)/sum(D_b)=sum[w_b*(A_b/D_b)], where w_b=D_b/sum(D_b). Thus the original aggregate implicitly gives the largest deficit, Batch 1, **69.19% of ratio weight**, even though the condition means use equal block weights. The script verifies this identity.

The earlier shorthand “roughly 59% of the mean amplitude deficit” is removed to prevent reading this aggregate as a stable or typical recovery fraction. Two within-block point ratios exceed 1, which only describes their observed means; **it does not establish complete recovery or equivalence**. No block-ratio confidence interval or clinical recovery interpretation is claimed with these three blocks.

The fixed raw-scale Gaussian LMM gives ASO−KD **+2.180178 nA**, pointwise 95% interval +0.223202 to +4.137154, nominal/Holm p=0.029435. Its residual W=0.836974, p≈1.73×10⁻⁸ flags a poor Gaussian residual approximation, visible in its Q–Q plot. It is retained as a limited sensitivity, not selected instead of the primary model. No extra Gamma model or transformation was added after observing this result.


### Post-hoc ASO–Control clarification, requested during review

[Review scope](../../research/plans/2026-11-12-k26-review-clarification.md) was recorded in commit `94f3af13a2b18e7c8bcec403e6838c99ab32bb59` before the added contrast test. This contrast is **post-hoc and exploratory**, not a third prespecified confirmatory contrast. The original primary/secondary estimates and two-contrast Holm family remain unchanged.

Actual R/lmerTest `contest1D` uses the same full-data models and fixed-effect covariance, with Satterthwaite degrees of freedom. Both refits first reproduce the original coefficients and batch variance. Nominal p-values and pointwise intervals are shown without a claim of confirmatory family control across this later addition.

| Model | ASO−Control estimate | Pointwise 95% interval | Exploratory nominal p |
|---|---:|---|---:|
| Primary log1p(nA) | **−0.241721** | **−0.574500 to +0.091059** | **0.152344** |
| Raw nA sensitivity | **−1.525701 nA** | **−3.433091 to +0.381688 nA** | **0.115450** |

These are the p-values for the declared R models, not the external review's untraced 0.52/0.30 values. A different test/unit of analysis may give other results, but its method must be stated before comparing them. The raw model retains its poor residual diagnostic. Both intervals include zero; this **does not prove equality, full rescue or that a meaningful residual deficit is absent**. No equivalence margin was prespecified and no equivalence test was performed.

### What the external specification scan can and cannot establish

The external review reports 18 specifications without p<0.001. That scan was not independently reproduced in this follow-up; even if every reported result is correct, it only describes the procedures actually tested. It **does not exhaust all preprocessing, versions, contrasts or covariance choices** and does not prove that a different analysis n is the only explanation. A star annotation error is also an unexcluded possibility, not a finding. The final ASO star-band cause therefore remains **unresolved**. Asking which observations/n, input scale, preprocessing and panel-specific code/output produced the annotation is appropriate as an open question; selecting a single explanation by elimination from 18 tests is not justified. No additional email was sent for this review.

## Interpretation

The bounded result is **a positive ASO-associated amplitude contrast under the authors' published-block model**, with preserved direction but limited precision in two-block sensitivities. It reproduces the qualitative direction, not the displayed ASO p-value band or the exact software environment. The analysis is of the same source data and therefore adds computational scrutiny, not an independent efficacy experiment.

The three labels are used as source blocks under the explicitly authorized assumption; the full differentiation/culture/coverslip/repeat hierarchy remains unverified. The model's residual degrees of freedom (approximately 84) do not turn 89 observations into 89 independent biological experiments. Those model-based intervals/p-values can change if the missing nesting requires a different covariance structure.

## Limitations and next discriminating input

- Only three source blocks; missing nested identities, cell-repeat mapping and per-record timing/QC. Author Reporting Summary supports independent differentiations and parallel intervention wells, but does not supply the complete mapping demanded by strict v1.
- Nonrandomized treatment allocation as reported; no independent replication, causal generalization or clinical interpretation. Positive magnitudes and recorded surviving/recordable cells do not establish recovery of every lost function.
- Unit preservation is essential because log1p is not scale-invariant. The source axis is nA; this run does not establish what numerical scale entered the authors' unpublished execution.
- The ASO star-band discrepancy must remain visible. Confirmation of the input numerical scale and panel-specific model output would discriminate among possible causes; no further email was sent for this replay. The previously authorized metadata follow-up is already recorded.
- The current source and code support a batch-conditional replay, not a claim that the original strict gate has been met. Its disabled contract is preserved.

Stop this fixed replay here. Next input is author clarification of the source-block mapping/nesting and, for exact reproduction, the panel-specific execution/scale. An independent functional experiment would still be needed for independent validation. No new endpoint, STMN2 refit, source fishing or post-deficit efficacy claim is opened.

## Reproduction and verification

From the repository root with the pinned original workbook downloaded outside git:

```sh
python scripts/adapt_k26_conditional_source.py --source /path/to/41586_2026_11256_MOESM7_ESM.xlsx --contract reports/k26-conditional-replay-20261111/conditional_contract.json --output-dir /tmp/k26-replay --plan-commit 55f84fe26f77d631d417f382bff176ca4528b1f3
Rscript --vanilla scripts/replay_k26_conditional.R /tmp/k26-replay/observations.csv /tmp/k26-replay
Rscript --vanilla scripts/check_k26_replay_outputs.R /tmp/k26-replay
# Later, explicitly post-hoc review clarification:
Rscript --vanilla scripts/review_k26_outputs.R /tmp/k26-replay
python -m unittest discover -s tests -p test_adapt_k26_conditional_source.py -v
```

The local environment lacked system R; official Debian trixie packages were downloaded and extracted to an isolated prefix without changing the system. The actual invocation used the native R executable with `--vanilla --slave --file=... --args ...`, equivalent script execution rather than a Python replacement. Exact R/package versions and native BLAS/LAPACK are in sessionInfo; a normally installed compatible R can use the Rscript commands above. The implementation requires `sha256sum` on PATH. Dependency versions are recorded, not asserted to reproduce the authors' environment.

Eight new artificial adapter tests check units, source coordinates, blanks/counts, negative/nonfinite refusal, batch identity/order, missing block labels, header/extra-row drift, source-hash refusal and no strict-gate substitution. Real-source hash/schema/count checks passed. An independent base-R GLS reconstruction from the fitted covariance reproduced coefficients and standard errors; t-tail, interval, Holm and equal-block arithmetic checks passed. These are software/arithmetic checks, not biological validation.

`review_k26_outputs.R` adds only the dated review clarification, first checking that unchanged-model refits reproduce the stored primary coefficients/variance. Its `contest1D` estimate/SE were checked against the fixed-effect covariance and its aggregate-ratio identity against the original result. `review_*` outputs keep that later analysis separate. `results.json` consolidates the numerical outputs without changing the original contrasts; `output_manifest.json` hashes deposited outputs. `observations.csv` retains original source-cell coordinates, raw numeric text and unchanged nA values; the adaptation is attributed to Keuss et al. under the article's CC BY 4.0 terms, with the original DOI/source URL above. The cached XLSX is not redistributed here.
