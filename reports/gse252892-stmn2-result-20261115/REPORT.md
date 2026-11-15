# STMN2 orthogonal control result — 15 November 2026

## Reported evidence

Luis supplied [result JSON](user-reported-result.json), [supervision](user-reported-supervision.json) and both [HISAT2 summaries](alignment-summary.tsv) as terminal text. These files transcribe that text; original STMN2 host metadata have not yet been uploaded/hashed by the agent. Completed proposal SHA2568379c7e56c0546623fac80c732935f29113f17e048b8625d85e1163e3f61b557, pinned runtimeacff06335ca1283b079c35ab0830a284e6d23258. Prior six-run UNC13A archive was audited separately; that does not audit these new output bytes.

The [selection](../../research/plans/2026-11-14-gse252892-orthogonal-control-selection.md) and [execution](../../research/plans/2026-11-14-gse252892-stmn2-execution.md) preceded counts. Sole selected marker, sealed chr8/plus junctions, unchanged paired-group filters and20-group descriptive diagnostic. No endpoint, threshold, estimator or alignment change after results.

| Library | Condition | Canonical | Cryptic | Cryptic support >=20 |
|---|---|---:|---:|---|
| GSM8009878 | Control | 1,945 | 3 | No |
| GSM8009881 | TDP-43 KD | 253 | 727 | Yes |

[Exportable table](counts.tsv). Counts are eligible paired query-groups per exact event/library, anchor15; not independent molecules, transcript percentages or biological replicates. Both canonical operational controls passed. Preserve the three control cryptic groups; do not call the control biologically negative. The generic raw output `interpretation` string warns about below-diagnostic support; it is a conditional warning, **not the current KD verdict**. The explicit per-event flag is true for KD727 and false for control3. Original output wording is retained unchanged.

## Interpretation fixed by the protocol

**The KD library shows supported STMN2 cryptic splice response compatible with the expected downstream consequence of TDP-43 loss.** This meets the prospective descriptive prediction for the sole marker. It does not measure nuclear TDP-43 concentration, quantify protein knockdown efficiency, establish intervention specificity, causality or a statistically estimated effect. One library per condition and one genetic background remain; unequal library size prevents treating raw count differences as a normalized effect. No fold change, ratio, PSI, interval or p-value is computed. Lower canonical count is not a calibrated expression estimate.

The same-library [UNC13A result](../gse252892-local-result-20261114/REPORT.md) remains106/0/0 control and41/0/3 KD. Those exact data and their bounded closure are unchanged. A supported orthogonal response shows the KD library is not devoid of all expected transcriptomic response under this workflow. It **does not isolate why UNC13A support was low** or prove that locus depth, depletion strength, RNA processing/stability, assay design, genotype or alignment/filter sensitivity is the cause. No cross-gene pooling, sum, correlation or substitution of STMN2 for UNC13A.

This is orthogonal-marker support within the same experiment/FASTQs, not independent biological validation, a new cohort, functional recovery or clinical evidence. The earlier45-donor STMN2 cycle is not reopened. Primary/assay sensitivity limitations from [selection](../gse252892-orthogonal-control-20261114/SELECTION.md) remain; the new positive observation does not retroactively validate negative observations.

## Technical consistency and resources

New QC group totals match the prior same-library UNC13A output exactly. Global mapping92.29%/91.59%; paired inputs70,948,578/89,969,380. [Consistency checks](consistency-check.json) pass. This is strong workflow consistency of supplied outputs, not an independent replay by the agent.

Supervision completed, failure/cleanup_error null, elapsed6,110.122 s (~1 h42 min), network_bytes0, sampled peak RSS4,792,123,392 and seven-root disk101,472,799,651 bytes, within fixed6 GiB/100 GiB/48 h caps. Sampled/non-kernel and uninterruptible-I/O limitations remain. Ctrl+C was shown after completed status and PowerShell prompt, not as an interruption of this completed run. No extra sequencing transfer or agent-side raw processing.

## Closure and next step

Close this sole-marker control with supported KD STMN2 junction response and all limits above. No additional marker, library, model, threshold or source expansion is scheduled. Archive the original new descriptor/claim, final result/supervision, per-library counts, fastp QC and HISAT2 logs to confirm original metadata bytes before treating this as fully audited. Keep raw inputs/index and earlier archive until retention/cleanup is explicitly decided. New local cleanup may inventory old plain intermediates first; no deletion is performed here. Existing AD/author waiting status is unchanged; no contact, cloud spend or merge is authorized by receiving results.
