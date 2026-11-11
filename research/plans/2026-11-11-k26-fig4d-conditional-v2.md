# FR-K26-4d conditional published-block replay v2

11 November 2026. User explicitly authorized this narrower replay after being told that strict v1 remains unmet. Source/design branch baseline: `e6633b6ef9ffe585a401d332a6e7af35f6814953`. This amendment must be committed before fitting or computing group summaries/effects. Individual source values, published direction and cell counts were already inspected; this is not an independent prospective biological experiment or an unbiased new-hypothesis test.

## Question and boundary

Can we reproduce the reported Fig.4d ASO-versus-KD pattern with the published numerical values and batch random-intercept model, and how much does the estimate depend on each published block?

Strict FR-K26-4d v1 is NOT passed or enabled by this amendment. Its cell/culture/coverslip hierarchy and per-cell recording-day requirements remain unresolved; author follow-up has been sent. This v2 permits a conditional computational replay under the explicit assumption that the three original source labels are the blocks described by the authors. It does not certify biological independence, complete nesting, distinct-cell identity or a clinical/causal conclusion. No inferred culture/cell IDs or exact recording dates are generated.

## Fixed input and unit correction

- Final Nature DOI `10.1038/s41586-026-11256-2`, Fig.4d only. Do not select a different endpoint.
- Original Fig.4 workbook: `https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-026-11256-2/MediaObjects/41586_2026_11256_MOESM7_ESM.xlsx`.
- SHA-256 `7a01e468d3eaf89a2af9bd0c3fb16434f815e3020033df771d9872799cba3eb7`, 126052 bytes. Use exact sheet `4d`, condition headers in row 3, and explicit Batch 1/2/3 labels in column A. Carry each label only through its declared block. Read all 89 numerical observations: Control 34, KD 30, KD_ASO 25. Preserve source-sheet/cell coordinates as observation provenance, not biological identities.
- Preserve positive amplitude values as supplied in **nA**, the final Fig.4d axis unit. Do not convert to pA before `log1p`; the historical v1 pA contract was wrong for the published scale. No absolute-value operation, imputation, extra exclusion or rounding before fitting. All source hash/schema/count/batch checks must pass; refuse unexpected inputs.
- Author code: `peteharley95/Log1pGaussianLMM`, commit `ae3f1b1548121e085897871292a363ed08c26d60`, R-file Git blob `249e4f59d6f2bdada2d9245628d8ec48b4206d95`. Read the R implementation, not the mismatched README. Adapt only source-sheet/header ingestion and deterministic output; do not execute its interactive file chooser.

## Primary model and contrasts

Use actual R, lme4 and lmerTest, with package/R versions and sessionInfo recorded. The publication states R 4.4.1; if unavailable, disclose the exact available R/package versions rather than claim an exact environment match. No Python OLS/mixed-model replacement.

Fit by REML with KD as reference:

`lmerTest::lmer(log1p(value_nA) ~ condition + (1 | source_batch), REML = TRUE)`.

Use the default optimizer as the primary fit. Extract fixed coefficients, standard errors, Satterthwaite degrees of freedom, two-sided p-values and pointwise 95% t intervals. Primary contrast KD_ASO−KD; secondary Control−KD. Report both nominal p-values and Holm adjustments across these two fixed contrasts. Neither threshold crossing nor overlapping/nonoverlapping intervals is a new biological validation. Do not convert transformed coefficients into an unconditional raw-nA difference or interpret `expm1(beta)` as a percentage of deficit restored.

Record model warnings/convergence, singularity, batch variance, residual SD, Shapiro–Wilk residual test, fitted/residual vectors, R/package versions and a Q–Q diagnostic. Three blocks limit variance estimation and uncertainty; missing nested metadata is not corrected by including batch.

If the primary fit is nonconvergent, retain the failure and permit one prespecified `bobyqa` refit only as a diagnostic. Do not choose an optimizer by favorable significance. A singular fit is reported, not silently removed. If residual W<0.90, explicitly flag deviation from the publication's Gaussian assumptions; no ad hoc transformation or Gamma fit is added in this bounded replay.

## Fixed sensitivities and descriptive summaries

1. Raw-scale Gaussian random-intercept model, same rows/groups/blocks and REML, as in the public R file. Retain warnings/singularity; use it as a scale sensitivity, not a replacement selected by p-value.
2. Leave each of the three source blocks out in turn and fit the primary log1p model on the remaining two. Report the primary coefficient, interval, nominal p and diagnostics without treating these as independent replications or adding multiplicity-adjusted confirmatory tests. If a two-block fit fails, report failure instead of manufacturing an estimate.
3. Export n, mean, median and SD per source batch/condition in original nA. Compute ASO−KD and Control−KD mean differences per batch and their equal-batch-weight mean; report all three directions. Do not weight a block more because it has more recorded cells.
4. The original plan's descriptive recovery ratio may be reported as `(equal_batch_mean_ASO - equal_batch_mean_KD) / (equal_batch_mean_Control - equal_batch_mean_KD)` only if the equal-weight denominator and each individual block's Control−KD difference are positive; otherwise mark undefined/unstable. Report numerator/denominator and unbounded ratio, no clipping, CI or claim of full recovery/equivalence. This ratio is a descriptive summary under the block assumption, not a clinical recovery rate.

No bootstrap, threshold search, new covariates, RNA/function correlation, cross-study pooling or subgroup selection.

## Comparison, falsifiability and stopping

The published panel displays positive Control−KD and ASO−KD directions and significance stars. Compare direction and the explicitly defined star bands with the replayed two-sided nominal contrasts; do not invent exact author coefficients/p-values that are not available. An agreement is a limited computational reproduction, not independent replication. A discrepancy must be retained and traced to source/unit/model/software versions; do not tune the analysis to match a star.

The directional expectation is ASO−KD>0, already informed by the publication. If nonpositive, record failure to reproduce that direction. If positive but uncertain or strongly block-dependent, report that qualification. No fixed success threshold is invented from the observed estimates. Stop after these fixed outputs and a source/implementation review, regardless of result. Future author metadata may justify a separately dated design amendment, not silent changes to these results.

## Deliverables

- Exact-source adapter exporting condition/source-batch/nA/source-cell provenance, with no invented biological IDs.
- Executed R script and complete machine-readable results, sessionInfo, logs and diagnostic artifacts.
- Report with Evidence / Interpretation / Limitations / Next discriminating input.
- Meaningful adapter/guard tests and appropriate software checks; no synthetic result presented as biological evidence.
- Updated STATE/BACKLOG/current findings, preserving strict v1 disabled status and the pending author clarification.
