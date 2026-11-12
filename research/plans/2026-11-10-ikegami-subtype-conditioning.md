# UNC13A–STMN2 association conditional on pathological subtype

Date: 2026-11-10. Authorized by Luis after the review of commit a286232.
This protocol is recorded before downloading or inspecting individual source values in this session. The published pooled rho and group sizes are already known. This is a new exploratory analysis of an already analysed cohort, not an independent confirmatory study.

## Question and competing explanation

Does the positive association between cryptic UNC13A RNA and truncated STMN2 RNA extend beyond differences between pathological subtypes? The alternative is that pooling subtypes with different levels generates much of the observed rho=0.5737.

## Source and admission gate

Use only Fig. 2c of Ikegami/Koike Additional file 3, DOI 10.1186/s40478-026-02400-0. Require original XLSX SHA256 d72b8ebc18c1b71be8bc4c26ffde1edd6f5da65541a7711c686073f4a36ad385 and explicit paired measurements and subtype labels in that sheet. Require 12/12/11 pairs and reproduction of pooled rho within 1e-10 of 0.5736694677871148. Record headers, cells used, missing values, source URL, bytes, versions and hashes. Reject nonfinite values, ambiguous groups or incomplete numeric pairs. Do not join sheets by row order. If the verified file cannot be recovered, stop and record the access failure, without reconstructing observations from aggregate statistics. Original source values are not redistributed.

## Primary estimand and test

Rank each marker globally using average ranks for ties. Subtract each subtype's mean rank separately from each ranked marker. Pearson correlation between these residuals is the subtype-adjusted rank correlation (partial Spearman controlling subtype indicators). This estimates association after removing group mean ranks, not a causal effect.

Primary null test: permute one marker's ranks only within subtype, re-centre, and recompute the statistic. Two-sided absolute-statistic tail, 99,999 permutations, seed 20261110, p=(extreme+1)/(B+1), alpha=0.05. This preserves subtype-level distributions and requires within-subtype exchangeability under the null. It does not require identical distributions across subtypes. Report Monte Carlo standard error. One primary test, no selection between methods based on significance.

## Secondary estimates and uncertainty

- Spearman rho in each subtype; descriptive, no separate significance decisions.
- Pooled rho and subtype-adjusted rank correlation after removing Type 2b, as sensitivity estimates only.
- Paired nonparametric bootstrap, 10,000 resamples, seed 20261111: resample complete pairs within each subtype at original group sizes, recomputing ranks and adjustment in each draw. Report marginal 95% percentile intervals for pooled, adjusted, within-subtype and no-2b coefficients. Do not interpret intervals as simultaneous or as accounting for unmeasured confounders. Record undefined replicates. More than 1% undefined makes that interval unavailable.
- Leave-one-pair-out range of the primary coefficient. Report absolute change from pooled rho, without calling it explained variance.

## Prediction, failure and interpretation

Working prediction: adjusted coefficient remains positive and the primary permutation p<0.05. If not, this cohort does not support the prediction beyond subtype; do not equate nonsignificance with no association. A substantial reduction is descriptive, with no post-hoc attenuation threshold. Broad intervals make the estimate uncertain even if a test crosses alpha.

Persistence cannot establish a shared mechanism or rule out RNA quality, normalization, cellular composition, disease duration, age or TDP-43 dysfunction as common causes. Attenuation cannot establish subtype as a causal confounder either; its position in the causal process is unknown. pTDP-43 aggregate burden is not interchangeable with nuclear TDP-43 function. This cohort remains internal, observational evidence, with no junction counts, independent replication, functional rescue or patient benefit.

## Software checks and output

Before real-data execution, test a constructed grouping-only association (adjustment removes it), a genuine within-group association, agreement with residualization by least squares, permutation reproducibility/invariance of subtype marginals, ties and invalid pairing. Test data are software fixtures only, never biological evidence.

Deliver a standalone script, tests, aggregate results JSON, figure and report. Correct prior interpretations in REPORT, STATE and BACKLOG: p>=0.05 does not exclude confounding, Spearman squared is not raw-expression variance explained, and adjusting for measured pathology does not identify mechanism. Preserve original numerical results. Record a protocol commit before analysis and close this cycle after one run. No new contacts, spending, patient data, laboratory work or external dissemination beyond the authorized repository PR. #37 and #44 remain blocked.
