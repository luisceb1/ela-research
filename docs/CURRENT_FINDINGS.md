# Current findings and limits

**Reviewed scientific baseline: 11 November 2026, source commit `c7d8f7e92e7eb02e3fb619f6e8984f075ef84784` (PR #58 merged).** This page summarizes selected current conclusions; it does not certify every historical report. No new biological analysis was performed for the English documentation. [Evidence/reproduction guide](ENGLISH_GUIDE.md) · [Spanish project entry](../README.es.md).

## STMN2: a measured junction and an exploratory paired tissue pattern

The retained GRCh38 positive-strand introns are canonical **chr8:[79611214,79636801)** and cryptic **chr8:[79611214,79616821)**, in 0-based half-open coordinates. Direct hg38 literature and UCSC chain checks support the cryptic acceptor at exon start **79616822**, 1-based. A one-base difference in published terminal exon counting endpoints does not change this junction. The assay pools transcripts sharing that junction and does not resolve alternative polyadenylation endpoints.

The outcome **K/(C+K)** uses cryptic-entry count K and canonical count C. It is a local junction-read ratio, not a calibrated molecular fraction, protein measurement or fraction of affected neurons. Four pure-ALS cervical samples with K≥20 map to four declared donors. P1's fixed ≥10× canonical-coverage prediction versus UNC13A was **not met**: 6.6× from raw medians and 8.085× after per-library input-read normalization. P2's covered cases do not prove that the earlier UNC13A limitation had a single cause. P3 frequencies are descriptive; Wilson-interval overlap is not an inferential test. [Measurement and unit audit](../reports/stmn2-map-audit-20261111/REPORT.en.md).

After exact technical mapping, pure-ALS status in both regions, matching preparation, one library per region and C+K≥20 in both, **45 donor pairs** remain. Cervical higher/tied/lower: **24/14/7**; median paired local-ratio difference **+0.003676**, or approximately **+0.368 percentage points**. The one prespecified two-sided exact sign test has **nominal p=0.0033268929**, conditional on independent donors and sign symmetry. Unequal coverage and discrete zeros can affect that symmetry. The question was informed by previously observed marginal results. Only four eligible control pairs remain; no ALS-versus-control test was performed. [Paired analysis](../reports/paired-stmn2-20261111/REPORT.en.md).

The prespecified main RNA-integrity restriction leaves **19 pairs**, with directions **10/8/1** and median difference **+0.002551**. The stricter restriction leaves **nine pairs**, median zero, below the fixed minimum of ten for interpretation. This does not establish uniform robustness to RNA quality. [RIN sensitivity](../reports/stmn2-rin-20261111/REPORT.en.md).

NYGC ST7 supplies composition vectors for all 90 libraries. Cortex and spinal cord use different MuSiC reference taxonomies, so a shared-scale composition correction was not established. Within-region Spearman/partial-rank correlations are **−0.229/−0.299** in cortex and **−0.093/−0.105** in cervical cord. **22/45 cervical neuronal estimates are zero.** These associations do not rule out composition confounding or establish a mechanism; no new p-values or corrected tissue effect were computed. [Composition gate](../reports/stmn2-composition-20261111/REPORT.en.md) · [Closing report](../reports/stmn2-within-region-20261111/REPORT.en.md).

**Status:** this cycle on the same 45 donors is closed. No causal, functional, clinical or independent-discovery conclusion is supported.

## UNC13A: a coverage limitation in the examined data

In TARGET_ALS, the median of per-library canonical-count/depth ratios is **2.5304 per million in motor cortex** and **0.1133 in cervical cord** for the pure ALS-spectrum groups, using **`exon_fc_count_all.total`**, reads submitted to featureCounts. This is not the count assigned to exons. The full-precision median ratio is **22.34**; the five named denominator choices yield **22.34, 25.55, 23.57, 22.85 and 22.16**. The rounded range 22–26 describes denominator sensitivity, not a confidence interval.

This comparison uses different, **unpaired** sample sets (84 cortical and 95 cervical ALS-spectrum libraries). Library-depth normalization does not eliminate composition, batch or other confounding, and does not establish tissue-specific cryptic splicing. The separately recovered 45 STMN2 pairs are ALS tissue pairs selected on STMN2 coverage, not ALS–control pairs; they were not used here.

No examined cervical library reaches 20 reads on a single cryptic UNC13A junction (maximum two). This differs from having a sufficient canonical denominator: **five of 95 ALS libraries and two of 13 controls have ≥20 canonical reads**. The search performed was closed for insufficient cryptic coverage. That does not establish that every public RNA-seq dataset is inadequate or that greater depth cannot help. No validated required-depth estimate is available; conditional scenarios are possible but require an assumed cryptic fraction. [Corrected coverage report](../reports/target-als-cervical-20261111/REPORT.en.md), including all prior corrections and reproduction commands.

## Intervention timing: a bounded documentation gap

The six-source, 14-experiment matrix contains **six UNC13A-specific experiments**. In none could treatment after a documented functional baseline deficit be established under either recorded reading of the rule. **This is absence of documentation in the inspected material, not proof that no deficit existed, and not an exhaustive claim about all literature.**

Multi-target Mallika row M-a differs between readings: zero of 14 experiments qualify under the strict same-endpoint baseline rule, versus one of 14 under a symptom-based substantive reading. Fine tremors were documented at dosing; the grip-strength deficit is evidenced by the parallel GFP arm rather than a same-endpoint pretreatment measurement in the CTR animals. The row and the suitability of the rule still need independent methodological review. Multi-target benefit cannot be assigned to isolated UNC13A correction. [Timing report](../reports/unc13a-intervention-timing-20261110/REPORT.en.md). The reviewed source versions and access limitations are stated there; this translation is not a new publication-status search.

## Conditional functional-data replay — 11 November 2026

After explicit user authorization of a narrower published-block analysis, [Keuss Fig.4d was replayed in R](../reports/k26-conditional-replay-20261111/REPORT.md) under a plan committed before fitting. The same 89 source observations were kept in nA with three author-labelled blocks; the original strict metadata gate remains unmet. The REML log1p model gives ASO−KD +0.474402, pointwise 95% interval +0.132939 to +0.815865, nominal/Holm p=0.007036. Direction is positive in all three leave-one-block-out fits, but two intervals include zero. The raw-scale Gaussian residual check is poor.

The qualitative direction is reproduced; the published ASO three-star band (p<0.001) is **not**: this fixed replay gives a two-star band. Cause remains unresolved; no scale/model was selected to match it. R/package versions and full outputs are recorded. This is computational reproduction under stated block assumptions on the **same data**, not independent biological replication, post-deficit reversal or clinical benefit. The cycle is closed pending discriminating author metadata/panel-execution information.


## Source-availability update — 11 November 2026

**Subsequent design review:** [validated source details and remaining gate](../reports/k26-published-source-20261111/DESIGN_REVIEW.md). The final amplitude axis is nA, whereas the old contract assumed pA; the unit/version needs amendment before log1p modelling. The authors document independent differentiations/parallel wells, but the source does not provide every nested per-cell key and exact recording day required by strict v1. The original contract remains disabled and no model/effect was fitted. The metadata clarification was sent with explicit authorization on 11 November 2026; see the [communication record](../reports/k26-published-source-20261111/COMMUNICATION_LOG.md).

The final Keuss Nature article (`10.1038/s41586-026-11256-2`) is now published and its public Fig.4 source workbook has been downloaded. The exact 4d sheet supplies 34/30/25 observations in three explicit batch blocks, matching the legend. [Source inspection](../reports/k26-published-source-20261111/REPORT.md). This changes file availability for #44, not the current scientific conclusions: units, batch/differentiation identity, nested structure and exclusions/QC still need reconciliation, and no new model or effect has been calculated. Older dated statements of missing source values are superseded; the inference contract remains disabled.


## What would enable further work

- **STMN2:** a discriminating, traceable composition/QC measurement; external validation requires a genuinely independent cohort with the event counts, donor structure and technical design verified. Another model on the same donors is not replication.
- **UNC13A #37:** an accepted concrete file/manifest with usable event measurements and independently verifiable condition/unit/batch structure, under the documented coverage/design criteria. Whole-transcriptome and targeted-amplicon fractions cannot simply be pooled.
- **Functional #44:** the numerical workbook is now available (update above). Validate its units, explicit batch→differentiation/culture map, cell/repeat identity, exclusions and chronology against the existing plan. Cells alone do not establish independent biological replication.

Access and communication records are dated evidence, not proof that files have now arrived. No new contact or follow-up was sent for this documentation work. None of these findings supports treatment advice or a clinical decision.
