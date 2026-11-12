# Cervical cord versus motor cortex: about 22 times lower UNC13A coverage

> English translation prepared on 11 November 2026 from the [Spanish original](REPORT.md) at `c7d8f7e92e7eb02e3fb619f6e8984f075ef84784`. Source/translation hashes and review scope: [English guide](../../docs/ENGLISH_GUIDE.md#translation-policy-and-review). This is a dated report, not a new analysis or publication-status check.
> Earlier proposed next steps are historical; for completed STMN2 work and current stop rules, use the [closing report](../stmn2-within-region-20261111/REPORT.en.md) and [current findings](../../docs/CURRENT_FINDINGS.md).

**Date:** 2026-11-11. **Prespecified plan:** [`research/plans/2026-11-11-target-als-cervical-cord.md`](../../research/plans/2026-11-11-target-als-cervical-cord.md), commit `9816f9d`, **before downloading cord junctions**. The design incorporates five external-review corrections from the preceding cycle.
**Evidence label:** exploratory descriptive analysis in post-mortem tissue, **unpaired tissue comparison**. No between-tissue p-values, effect estimates or clinical interpretation.

> ## Correction history of the central figure
>
> This figure was published three times and **the first two versions were not defensible**. The history is retained because readers are entitled to know how often and why it was corrected.
>
> | Version | Figure | What was wrong |
> |---|---|---|
> | 1 (morning) | **20.9×**; “canonical per million” 2.30 and 0.11 | Divided the **group median** by a **single** median depth of 44.4 M applied to both tissues. This is a **ratio of medians**, not per-library normalization. The report also called that field “reads assigned to exons”: **it is not.** It is `exon_fc_count_all.total`, reads *submitted* to featureCounts. Actually assigned reads differ between tissues (20.3 M versus 23.9 M), so the “identical” depth claim held only for the field that was not named. The report also said this “eliminates the confounder”: matching one median eliminates nothing |
> | 2 (afternoon) | **22.3×**; 2.530 and 0.113 | **The arithmetic was correct; no procedure had been deposited.** Announced without deposited code and with a wrongly named denominator, it could not be reproduced by an external reader: `.assigned` gives 0.2055 and input reads give 0.1150, neither 0.113. A correct but irreproducible figure is not an acceptable state for a published report |
> | **3 (this version)** | **22.34×** | Calculated by [`scripts/normalize_tissue_coverage.py`](../../scripts/normalize_tissue_coverage.py), naming the QC field, input hashes, per-library ranges, **five** candidate denominators and eight tests: one distinguishes the median of ratios from the ratio of medians, and two check that quotients use **full precision**, because a fourth review found that the script divided already rounded medians, moving the figure by 0.01 (22.33 instead of 22.34). Full output: [`depth_normalisation.json`](depth_normalisation.json), now depositing the exact median alongside the rounded one and marking the rounded quotient as not for use |
>
> Direction and order of magnitude persisted across all three. The method did not.

## What makes this comparison relatively clean, and its limits

**In favor:** same consortium, quantification pipeline, group criteria and sealed coordinates.

**Depth, precisely:** the whole-tissue-set medians of `exon_fc_count_all.total` nearly coincide (44.387 M and 44.389 M), but **group medians do not**: controls are deeper than ALS in both tissues (50.4 M versus 42.7 M in cortex; 49.5 M versus 43.2 M in cord). Each library is therefore normalized by its own depth; matching overall medians was not a control.

**Declared limitation:** this compares **different, unpaired sample sets**. The recount3 metadata do not expose subject identity.

The project does have a donor map establishing **45 cortex–cord pairs**, validated against NYGC ST3 by exact RNA key. **Correction of 11 November 2026:** an earlier version attributed this map to ST7. **That was wrong:** the map already existed and was validated; ST7 later supplied composition estimates for the 90 libraries of those same pairs.

More importantly, **those 45 pairs do not serve the purpose this report implied**. They are **ALS donors in both tissues**, also selected on **STMN2** coverage (C+K≥20 in both regions). Thus:

- they could pair the **tissue comparison** by donor, not the **ALS-versus-control** comparison, which they do not contain;
- selection is based on another gene's coverage, so applying them to UNC13A introduces a different selection that must be declared.

**That pairing is not used here**, and this report cannot claim it as support.

Cord assembly checks passed: not apparently targeted (2,695,965 junctions, 4.8% on chr19, 119 chromosomes); all three sealed junctions match exactly; expected annotation pattern. Downloaded 213 MB against the 400 MB budget.

## Tissue table: the deliverable

Full table: [`tissue_comparison.tsv`](tissue_comparison.tsv), including per-library ranges, the alternative denominator and withdrawn ratio of medians, so the published column can be checked against the two not selected.

| Tissue | Group | n | Median depth | Canonical median | **Canonical per million** (median of per-library ratios) | Per-library range | Detection [Wilson 95%] | ≥20 |
|---|---|---:|---:|---:|---:|---|---|---:|
| Motor cortex | ALS Spectrum MND | 84 | 42.7 M | 102 | **2.530** | 0.139–4.240 | 0.190 [0.121–0.287] | 0 |
| Motor cortex | Non-neurological control | 13 | 50.4 M | 148 | **2.845** | 0.750–5.819 | 0.000 [0.000–0.228] | 0 |
| Cervical cord | ALS Spectrum MND | 95 | 43.2 M | 5 | **0.113** | 0.000–0.763 | 0.053 [0.023–0.117] | 0 |
| Cervical cord | Non-neurological control | 13 | 49.5 M | 8 | **0.174** | 0.000–0.442 | 0.000 [0.000–0.228] | 0 |

Denominator: `exon_fc_count_all.total`. **The denominator choice moves the figure**, so all choices are published: 22.34× with this field, 25.55× with `exon_fc_count_all.assigned`, 23.57× with input reads, 22.85× with mapped reads and 22.16× with uniquely mapped reads. **The finding's direction/order of magnitude holds across these choices**; the exact value within approximately 22–26 depends on the denominator.

## The three prespecified predictions

| | Prediction | Result |
|---|---|---|
| **P1** | Normalized canonical coverage **lower** in cervical cord | **CONFIRMED. 22.34× lower** (2.530 versus 0.113 per million in ALS), approximately 22.2×–25.6× under the five denominators |
| **P2** | Lower proportion of ALS samples with any cryptic read in cord | **CONFIRMED for the observed proportion:** 0.053 versus 0.190. Wilson intervals do not overlap, but **only by 0.004** (0.117 versus 0.121), which **does not constitute an interpretable separation**; the prediction itself is weakly informative because lower detection is expected with 22× less coverage without requiring different biology |
| **P3** | No cord sample reaches 20 reads on one cryptic junction | **CONFIRMED.** Maximum 2 |

## Interpretation

### Main finding: a large, now reproducible tissue coverage difference

After normalizing each library by its own depth, **UNC13A has about 22 times less coverage in cervical cord than motor cortex**. Depth is not claimed to be “controlled”: it is normalized, the comparison remains **unpaired**, and unmeasured confounders include cell composition. This checks, within one cohort/pipeline, the observation that Ikegami 2026 and Mallika 2026's GTEx panel made across studies.

It offers a plausible explanation for the project's failures: **the closed pilot and Klim dataset used spinal motor neurons**, where this locus is much less covered. This is a retrospective coverage explanation, **not a demonstration that coverage was the sole cause** of those failures; “the wrong tissue” is not claimed, because that would presume coverage explains everything that failed.

### Lower cord detection does NOT require different biology

Detection is lower in cord (5.3% versus 19.0%), but **that direction is expected from 22× less coverage alone**. Without reads, cryptic reads cannot be observed. This comparison **does not** provide evidence that cryptic inclusion differs between tissues and is not presented as such.

### In cord, the ratio is not interpretable in the great majority of libraries

> **Correction of 11 November 2026.** The previous version said “no ratio is interpretable”. **Too absolute.** Under the same 20-canonical-read criterion, **5 of 95 ALS libraries** (20, 23, 27, 36 and 37) and **2 of 13 controls** (20 and 29) do have a usable denominator. A median of 5 does not describe every sample. These are also **different requirements**: sufficient denominator is not 20 **cryptic** reads, which **remains unmet** throughout cord (maximum 2).

With median canonical coverage **5** in cervical ALS, ratios in the remainder are not informative under that criterion: the mixed group's “maximum PSI” of 0.33 is **one cryptic read over two canonical reads**. It is sampling noise rather than signal. Column `ratio_interpretable` marks `no` for the group, describing the median and **not** the 7 libraries with adequate denominators; of those 5 ALS libraries, **only 1 has any cryptic read**.

The methodological lesson is that **a ratio without a minimum denominator is not an adequate measure**, and reporting PSI at single-digit coverage creates seemingly informative values that are not informative.

### A collateral observation not pursued

In both tissues, normalized canonical coverage is **lower in ALS than controls** (2.530 versus 2.845; 0.113 versus 0.174). This is the direction one might expect if TDP-43 loss reduced canonical splicing, but with **13 controls**, no pairing and no prespecified contrast, it **is neither tested nor interpreted**. It is recorded as an observation, **without a proposed route**: the 45 pairs cannot address this because all are ALS donors.

### The question concerned tissues and is answered at tissue level

Tissue contains multiple cell types. This comparison **does not identify neuronal-type dependence** and is not used to support H1. It only says these junctions are much less covered in cervical cord than motor cortex.

## Bounded conclusion, fixed in advance

Of the five examined datasets, **none reaches 20 reads on one cryptic junction**. **This search closes for insufficient precision with the data examined.**

It is not concluded that the threshold is unattainable across all public RNA-seq. What the evidence establishes is **where coverage is poorer**: cord, by approximately 22 times.

> **Correction of 11 November 2026.** The previous version added that “more samples would not suffice” and “the route is not more n or more depth”. **That is not demonstrated.** These data support closing **the search performed** for insufficient coverage. Ruling out greater depth would require estimating the necessary depth, and **no validated estimate is available**. Scenarios conditional on assumed cryptic fractions can be calculated; evidence to choose one is missing because Klim's and Ma's figures are not comparable and gate #37 could not establish the real fraction.

Two **reasonable routes, not established as the only ones**: **cell enrichment**, such as nuclei sorted by TDP-43 presence/absence in GSE126543, or a targeted assay. That dataset has no reachable SRA records in the documented search, so a different access route would be needed.

## Limitations

- **Unpaired comparison.** The project has 45 donor pairs, **not used here** and **not applicable** to an ALS–control comparison: these are ALS cortex–cord pairs selected on STMN2 coverage.
- **Bulk tissue**; cell composition is unmeasured and can confound the magnitude throughout.
- **13 controls per tissue.** Their 0/13 is compatible with rates up to 22.8%, so cortical controls **cannot be distinguished from ALS** solely by detection proportion on this basis. The earlier cycle's clean separation remains a pattern, not a statistical contrast.
- **Wilson nonoverlap in P2 is 0.004** and is not used to support a claim.
- **The central figure varies with denominator** between approximately 22.2× and 25.6×. The full range is reported, calculated at full precision: rounding medians before division moved the headline by 0.01.
- **Greater depth is not ruled out.** No **validated estimate** of required depth is available: scenarios conditional on an assumed cryptic fraction can be calculated, but evidence for choosing it is absent (#37).
- **No between-tissue p-values**: different sample sets, unpaired, with unmeasured confounders.
- **STMN2 was not analyzed in this cycle**: sealed hg38 coordinates were unavailable at the time; they are now available.
- **No novelty claimed**: the consortium has published on these data.
- **Lumbar/thoracic data were not downloaded**, as planned.
- **Personal data:** **only** the group column and, for normalization, `rail_id` and numeric QC columns were read; sex, ethnicity, ages and onset site **were not read**; no individual clinical row appears in output; the metadata file is not committed.

## Reproduce the central figure

```
python -I scripts/normalize_tissue_coverage.py \
  --tissue 'Cortex_Motor_Lateral:reports/target-als-cortex-20261111/results.json:<qc.MD.gz>' \
  --tissue 'Spinal_Cord_Cervical:reports/target-als-cervical-20261111/results.json:<qc_cerv.MD.gz>' \
  --json reports/target-als-cervical-20261111/depth_normalisation.json
```

Both `qc*.MD.gz` files come from `recount3`, TARGET_ALS; SHA256 values are in `depth_normalisation.json`. They are not committed because they contain the consortium's complete QC table.

## Next step

Do not propose another whole-transcriptome dataset for this question. Meaningful continuations recorded by this report are:

1. **A paired contrast on the 45 pairs**, with one prespecified comparison, which this report did not perform.
2. **Cell enrichment**, requiring an access route to sorted-nuclei data.
3. Bring the tissue-coverage and chronology observations to a laboratory group.

No contacts, costs, laboratory work or external publication were executed in this cycle. Framework: [AGENTS](../../AGENTS.md), [PROTOCOL](../../research/PROTOCOL.md), [STATE](../../research/STATE.md).
