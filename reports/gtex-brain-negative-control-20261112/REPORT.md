# Non-ALS background for the UNC13A cryptic junctions — gtex BRAIN, 12 November 2026

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

Depth comparability was fixed in advance on the canonical junction itself — not on library depth fields, which caused three successive published corrections in this project. The window is **canonical 102–148**, the observed TARGET_ALS cortex range.

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

Fifteen cortical libraries reach the window, so the "not depth-comparable, inconclusive" branch does not apply. Both cryptic junctions are zero throughout the window, which is the branch reading: **the published ALS cortical cryptic reads are above the non-ALS background at comparable local coverage.**

The plan's own qualification stands and is not softened now the result is favourable. GTEx and TARGET_ALS are different studies with different donors, handling, library preparation and sequencing. By the standard this project set when it demoted a 1.8× cross-study claim to weak evidence, this comparison is weak whatever it shows. It is **consistent with** the ALS counts being real signal; it does not demonstrate it, because processing differences alone can suppress low-count junction detection.

Two further limits belong next to the result:

**n = 15 cortical libraries is small.** Zero cryptic reads in 15 libraries is compatible with a background rate of a few percent. This bounds the background loosely, not tightly.

**Only 0.9 % of GTEx brain is depth-comparable at all.** Median canonical coverage runs from 1 to 35.5 by tissue, against TARGET_ALS cortex's 102–148. For the other 2,905 libraries the zeros are **missing data at that depth**, not biological zeros, exactly as in every previous cycle — and they are not evidence of background absence.

## One thing this could not control, and one it corroborates

**The cervical measurement cannot be controlled from GTEx.** `Brain - Spinal cord (cervical c-1)` has median canonical 1.0 and maximum 21, so **no library reaches the window**. The published [cervical cord result](../target-als-cervical-20261111/REPORT.md) has no non-ALS baseline here, and this cycle does not provide one.

**The tissue asymmetry reproduces in non-diseased tissue.** Within GTEx alone — same study, same processing, so not a cross-study comparison — cervical spinal cord has median canonical 1.0 against cortex's 15.0, the same direction as the cortex-over-cervical coverage difference this project reported in ALS tissue, and the same direction as the GTEx expression panels cited by Ikegami and Mallika. No ratio is formed between these medians: ratio-of-medians versus median-of-ratios was the subject of two published corrections here, and forming one from a descriptive side observation would repeat that error. The observation is that the direction holds in tissue without TDP-43 pathology, which argues the asymmetry is a property of the tissue rather than of disease or of the TARGET_ALS cohort.

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
