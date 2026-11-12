# Non-ALS spinal cord source for the cervical control — 12 November 2026

**Interpretation correction — 12 November 2026:** reviewed against committed outputs; see the [correction record](../nov12-interpretation-review-20261112/REPORT.md). Counts and executed prospective rules are preserved; the stronger original interpretations are superseded below.

**Two results. The baseline I said was missing already exists, and the one genuinely new source that is biologically ideal fails its positive control.**

Executed under the [plan committed before any discovery query](../../research/plans/2026-11-12-nonals-spinal-cord-source.md), `6906a58`. Transfers: 2.9 MB index plus 3.1 MB of junction data.

## 1. Correction: the cervical baseline was never missing

After the gtex cycle I said the published cervical measurement "has no non-ALS baseline". **Wrong.** The [cervical report](../target-als-cervical-20261111/REPORT.md) already carries **13 non-neurological controls per tissue**, from the same cohort and the same quantification pipeline:

| Tissue | Group | n | Canonical median | Canonical per million | Detection |
|---|---|---|---|---|---|
| Motor cortex | ALS Spectrum MND | 84 | 102 | 2.530 | 0.190 |
| Motor cortex | Non-neurological control | 13 | 148 | 2.845 | 0.000 |
| Cervical cord | ALS Spectrum MND | 95 | 5 | 0.113 | 0.053 |
| Cervical cord | Non-neurological control | 13 | 8 | 0.174 | 0.000 |

A same-cohort control is **stronger** than the external one this project built in GTEx, because it avoids exactly the cross-study weakness that made that comparison weak. What the cervical control actually suffers from is **n and depth** — 13 libraries at canonical median 8, of which the earlier report records only 2 reaching 20 canonical reads — not absence.

That reframes the task: not "find a baseline" but "find one better than 13 controls at canonical median 8".

## 2. The search

Index-first, as established in PR #68. The recount3 SRA project index was re-fetched and its hash reproduced (`f28cbb77…55b01`). Three E-utilities queries gave **107 distinct human SRA studies**; **24** are held by recount3. Full adjudication in [candidates.tsv](candidates.tsv).

Only **one** is non-ALS post-mortem spinal cord tissue. The rest are ALS cohorts, hPSC-derived cultures, embryonic material, astrocyte derivations, reference-epigenome mixtures or the wrong assay. `SRP270799` is large (2,256 runs) and concerns truncated STMN2, but it is an FTD/TDP-43-pathology brain cohort, not spinal cord.

## 3. SRP097615 — the right material, measured, and it fails

[GSE-linked deposit](candidates.tsv): laser-captured motor neurons from **control** subjects — 12 spinal (lumbar/cervical), 20 oculomotor, 7 Onuf's nucleus. Not prior work in this repository. Biologically this is better than bulk cord: laser capture enriches the cell type whose UNC13A signal is at issue.

Sealed targets verified unchanged first. Probe run with `--project-id SRP097615`.

| Junction | Max | Libraries with any read | Present in catalogue |
|---|---|---|---|
| **canonical (positive control)** | **0** | **0 / 39** | **absent** |
| cryptic_left | 0 | 0 / 39 | absent |
| cryptic_right | 0 | 0 / 39 | absent |

**The positive control is absent.** Per the prespecified rule carried from the Question A amendment, that means the measurement failed at this locus and **nothing is concluded** about the cryptic junctions in either direction. These zeros are not a background measurement.

The project catalogue contains **121,078 distinct junction rows** across 39 libraries, versus 9,484,210 across 2,931 GTEx libraries and 2,678,581 across 149 TARGET_ALS cortical libraries. Only 19 rows lie in the inspected 100 kb around UNC13A. These are catalogue observations across different sample counts and assays, not a standardized measure of library complexity or proof of its cause. Low input, RNA quality, preparation, sequencing and mapping remain possible explanations.

Cell-type enrichment did not yield a measurable canonical junction in this deposit. There is no matched enriched-versus-bulk experiment here, so the failure cannot be causally assigned to laser capture.

## 4. The prediction

The plan predicted that no public non-ALS spinal cord source would have materially better UNC13A coverage, under the hypothesis that tissue-associated coverage limits recur across cohorts (a hypothesis, not an established cause), and set the refutation condition as median canonical ≥20 or a substantial share of libraries in the 102–148 window.

**Not refuted.** SRP097615's median canonical is 0, in every one of its three neuron populations. The result goes further than predicted in the unfavourable direction: the one source with ideal biology is worse, not better, than bulk cord.

## 5. What this leaves

The cervical control that exists is the TARGET_ALS same-cohort one, with its stated weakness: 0 of 13 is compatible with background rates up to 22.8 % by the Wilson interval the earlier report already recorded. **This cycle does not improve it**, and no public source found here would.

No better cervical control was identified in this finite search. TARGET_ALS and GTEx show low cervical canonical coverage, and SRP097615 fails the canonical control in all 39 libraries; its libraries include spinal, oculomotor and Onuf populations, not 39 equivalent cervical samples. These observations do not exclude other cohorts, library preparations or public sources. Deeper or targeted sequencing are possible routes, not established necessities or the only options.

## Provenance

| File | Bytes | SHA256 |
|---|---|---|
| sra.junctions.SRP097615.ALL.RR.gz | 1,957,224 | `e2550f3986bfa340b2bd4567bf55565e0e7a3eea42c40c20508c9aa63190b41a` |
| sra.junctions.SRP097615.ALL.MM.gz | 1,116,418 | `d07896d09f57f0aff0520cdcdbd2527fb8a503659cf0d5648c5e04e7299813df` |
| sra.junctions.SRP097615.ALL.ID.gz | 142 | `6e17e918983d5a0c3ab4595f13eb3084975c94fdadbc675f4bd0b9ec58ecb94a` |
| sra.recount_project.SRP097615.MD.gz | 391 | `53ff895295d8b15e6a977ea13c04604508abfdc8119778e77069fb3f8d7f8bc2` |
| sra.sra.SRP097615.MD.gz | 4,506 | `01efe46316012a8d447ab3cf01929db788423219fa2da63d316c83aaed979f0c` |

Full probe output in [results_SRP097615.json](results_SRP097615.json). Group labels are the deposit's own `sample_title` and `tissue` attributes.

## Boundaries

No effect, PSI, ratio, p-value or model. No ALS-versus-control test was performed, and the existing 13-control comparison is not reinterpreted here. The 20-read minimum stands. A negative search closes this as a tissue-level coverage limit over the sources inspected, **not** as proof that no such deposit exists anywhere. Issue #37 and the three-background question are untouched. No contact, access request, cost or personal data.
