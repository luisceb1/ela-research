# Non-ALS background for the UNC13A cryptic junctions — gtex BRAIN, 12 November 2026

**Interpretation correction — 12 November 2026:** reviewed against committed outputs; see the [correction record](../nov12-interpretation-review-20261112/REPORT.md). Counts and executed prospective rules are preserved; the stronger original interpretations are superseded below.

**In the 26 non-ALS brain libraries with canonical coverage comparable to the published ALS cortex measurement, both sealed cryptic junctions carry zero reads.** Across all 2,931 libraries, cryptic reads appear in 7 of them at a maximum of 2 reads. By this project's own standard a cross-study comparison is weak evidence, so this is consistent with the published ALS counts being signal — it does not demonstrate it.

Executed under the [plan committed before any junction file was downloaded](../../research/plans/2026-11-12-gtex-brain-negative-control.md), `b2ff4f2`, which fixed the comparability window and every outcome reading in advance.

## Assembly controls

Sealed targets verified unchanged first (`e35f6e05…bc3a`). Probe run with `--project-id BRAIN`; coordinate-convention guard passed; all three sealed junctions located exactly, no endpoint shifted.

| Control | Result |
|---|---|
| Targeted assay? | **No** — 9,484,210 junctions × 2,931 libraries, 699,368,828 non-zeros |
| Canonical positive control | Measured in **2,655 / 2,931** libraries, maximum 286, 895 at or above 20 |
| `gate_met` | False — neither cryptic junction reaches 20 in any library |

## Result

| Junction | Max | Libraries with any read | ≥20 |
|---|---|---|---|
| canonical (control) | 286 | 2,655 / 2,931 | 895 |
| cryptic_left | **2** | **5 / 2,931** | 0 |
| cryptic_right | **1** | **4 / 2,931** | 0 |

### The comparability window

Depth comparability was fixed in advance on the canonical junction itself — not on library depth fields, which caused three successive published corrections in this project. The window is **canonical 102–148**, bounded by the TARGET_ALS ALS-group median (102) and non-neurological-control median (148), not the observed per-library range.

**26 libraries of 2,931 fall in that window. In all 26, both cryptic junctions are zero.** Fifteen of the 26 are cortical: Frontal Cortex BA9 (8), Anterior cingulate BA24 (5), Cortex (2).

### Per tissue

| Tissue | n | Canonical median | Canonical max | In window | cL>0 | cR>0 |
|---|---|---|---|---|---|---|
| Brain - Cortex | 286 | 15.0 | 137 | 2 | 0 | 0 |
| Brain - Cerebellum | 285 | 27.0 | 141 | 2 | 1 | 1 |
| Brain - Caudate | 273 | 5.0 | 82 | 0 | 0 | 0 |
| Brain - Nucleus accumbens | 262 | 9.5 | 121 | 1 | 0 | 1 |
| Brain - Cerebellar Hemisphere | 250 | 35.5 | 205 | 4 | 0 | 0 |
| Brain - Frontal Cortex (BA9) | 224 | 23.0 | 286 | 8 | 1 | 1 |
| Brain - Hypothalamus | 221 | 6.0 | 104 | 1 | 1 | 1 |
| Brain - Putamen | 221 | 4.0 | 38 | 0 | 1 | 0 |
| Brain - Hippocampus | 220 | 5.0 | 122 | 3 | 0 | 0 |
| Brain - Anterior cingulate (BA24) | 201 | 12.0 | 127 | 5 | 0 | 0 |
| **Brain - Spinal cord (cervical c-1)** | **171** | **1.0** | **21** | **0** | 0 | 0 |
| Brain - Amygdala | 163 | 5.0 | 83 | 0 | 1 | 0 |
| Brain - Substantia nigra | 154 | 2.0 | 49 | 0 | 0 | 0 |

### The seven libraries with any cryptic read

All sit **outside** the comparability window, at canonical 3–56.

| Sample | Tissue | Canonical | cL | cR |
|---|---|---|---|---|
| GTEX-13X6K-0011-R10a-SM-5P9JR | Frontal Cortex (BA9) | 56 | 0 | 1 |
| GTEX-13N2G-0011-R10a-SM-5MR34 | Frontal Cortex (BA9) | 10 | 1 | 0 |
| GTEX-11EQ8-2826-SM-5N9C1 | Cerebellum | 24 | 2 | 1 |
| GTEX-13X6K-0011-R8b-SM-5PNZ4 | Hypothalamus | 20 | 1 | 1 |
| GTEX-13X6K-0011-R7b-SM-5P9K7 | Putamen | 12 | 1 | 0 |
| GTEX-13OW5-0011-R6b-SM-5O9BW | Nucleus accumbens | 11 | 0 | 1 |
| GTEX-X4EP-0011-R4B-SM-3P627 | Amygdala | 3 | 1 | 0 |

Three of the seven share the donor prefix `GTEX-13X6K` across three tissues. That is recorded descriptively; with seven observations at 1–2 reads, no donor-level pattern is claimed or tested.

## Reading, per the prespecified table

Fifteen cortical libraries meet the fixed 102–148 window and both cryptic counts are zero in them. The prespecified outcome table labelled this as ALS counts above background, but that interpretation overreaches: the window was derived from two group medians, not the ALS per-library range, and the ALS positive libraries were not matched individually to these controls. The retained result is the descriptive zero in this fixed GTEx subset. It does not establish an ALS-versus-background difference.

The plan's own qualification stands and is not softened now the result is favourable. GTEx and TARGET_ALS are different studies with different donors, handling, library preparation and sequencing. By the standard this project set when it demoted a 1.8× cross-study claim to weak evidence, this comparison is weak whatever it shows. It is **consistent with** the ALS counts being real signal; it does not demonstrate it, because processing differences alone can suppress low-count junction detection.

Two further limits belong next to the result:

**n = 15 cortical libraries is a small descriptive subset.** Libraries are not automatically independent donors; no donor-level background-rate bound or interval is established here.

**Only 0.9 % of GTEx brain meets the prespecified window.** The other 2,905 libraries lie outside this selection, including libraries above its upper bound; that does not make all their zeros missing data or establish insufficient coverage in each. No new window or coverage classification is substituted after seeing the results.

## One thing this could not control, and one it corroborates

**The cervical measurement cannot be controlled from GTEx.** `Brain - Spinal cord (cervical c-1)` has median canonical 1.0 and maximum 21, so **no library reaches the window**. The published [cervical cord result](../target-als-cervical-20261111/REPORT.md) has no non-ALS baseline here, and this cycle does not provide one.

**The coverage direction also occurs in GTEx.** Cervical median canonical coverage is 1.0 versus 15.0 in cortex within GTEx. This shows that this direction can occur outside the ALS cohort; it does not isolate tissue biology from composition, preparation, mapping or other differences, nor verify absence of TDP-43 pathology per donor.

## Provenance

Five files, 2.8 GB against a 3.5 GB cap, from `duffel.rail.bio/recount3/human/data_sources/gtex/`. Probe runtime 6m56s.

| File | Bytes | SHA256 |
|---|---|---|
| gtex.junctions.BRAIN.ALL.MM.gz | 2,819,422,875 | `93da00d3de042aea218c6fe1183f053ea3ca7eefe70460f044eb8f4be243a0a1` |
| gtex.junctions.BRAIN.ALL.RR.gz | 112,590,478 | `0f2807de027777c65d22865db801c58ea15950633f014f8613fd1a127b0f7091` |
| gtex.gtex.BRAIN.MD.gz | 475,816 | `4cdc75aad388ca432d7f9b9fb84c3b4fc07973559b72b92378c81b25fc41b189` |
| gtex.recount_project.BRAIN.MD.gz | 33,279 | `546ab0c809dc31253f5d7bc0d89dd6e5a7814d7b5f3e4b93af358c12296d2f3e` |
| gtex.junctions.BRAIN.ALL.ID.gz | 6,423 | `6d2bca353542a783fcf041adfa3420d830d79f644956f300cf92ae2d6efd7c22` |

Tissue labels are the deposit's own `SMTSD`, joined on `SAMPID`; all 2,931 libraries resolved. Per-tissue and per-library detail in [summary_BRAIN.json](summary_BRAIN.json). The full 1.2 MB per-sample output is not committed; it is reproducible from the hashed inputs with the recorded command.

## Boundaries

A descriptive background measurement in non-diseased tissue. No p-value, no ALS-versus-GTEx test, no effect, no interval, no model, no pooling of GTEx with TARGET_ALS libraries. The 102–148 window was not changed after seeing the counts. Not biological replication, not validation of any ALS result, and no evidence about TDP-43 depletion, functional recovery, therapeutic rescue or clinical benefit. Issue #37, the 20-read minimum and the three-background question are untouched.
