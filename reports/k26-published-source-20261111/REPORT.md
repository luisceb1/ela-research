# K26 is published: public Fig.4 source values and explicit batch blocks found

> Follow-up completed: [design/unit review and strict-gate decision](DESIGN_REVIEW.md). Source counts below are unchanged; the later review establishes nA as the published scale and identifies the remaining strict-v1 metadata gap. No effect fitted.

**11 November 2026. Bounded source-availability inspection under the existing FR-K26-4d v1 plan, not an effect analysis.** Repository baseline: `8257b71335ef39b0f8ccadfd899d68f577c99738`. No new endpoint, fitted model, p-value, threshold change or contact.

## New primary source

Keuss et al., *UNC13A splice correction rescues synaptic dysfunction induced by TDP-43 loss*, Nature, published **11 November 2026**, DOI [10.1038/s41586-026-11256-2](https://doi.org/10.1038/s41586-026-11256-2). The live publisher HTML was retrieved successfully after a normal cookie-authorization redirect; the web retrieval service separately failed on that redirect. The publisher labels the article open access, CC BY 4.0. Its source-data section directly links **Source Data Fig. 4**, an XLSX file, rather than only a plotted figure or a summary PDF.

Original source URL: <https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-026-11256-2/MediaObjects/41586_2026_11256_MOESM7_ESM.xlsx>.

Downloaded 126,052 bytes; SHA-256 `7a01e468d3eaf89a2af9bd0c3fb16434f815e3020033df771d9872799cba3eb7`. The original workbook remains in a temporary source cache; the repository records its URL/hash and aggregate inspection. No amplitudes are inferred from a figure image.

## Panel identity and structural check

The workbook has sheets `4a`, `4b`, `4c`, `4d`, `4e`, `4g`. Worksheet `4d` is titled `Figure 4d, Measurement of evoked EPSCs in spinal motor neuron`. Row 3 names the three conditions; column A explicitly labels `Batch 1`, `Batch 2`, `Batch 3`. The labels are carried forward only within their declared blocks, following the source layout; no biological identifiers are manufactured from row order.

| Explicit source block | Control | TDP-43 KD | TDP-43 KD +21-6 |
|---|---:|---:|---:|
| Batch 1 | 10 | 10 | 11 |
| Batch 2 | 13 | 8 | 7 |
| Batch 3 | 11 | 12 | 7 |
| Total | **34** | **30** | **25** |

There are **89 numerical observations** in this panel; values are finite/nonnegative and the selected panel contains no formulas. The published Fig.4d legend still reports 34/30/25 neurons and three independent differentiations. The count agreement verifies panel identity and completeness against that particular declared count; it does not independently establish biological independence, unreported exclusions or unit meaning.

## Code is now reachable

The article links [peteharley95/Log1pGaussianLMM](https://github.com/peteharley95/Log1pGaussianLMM), inspected at commit `ae3f1b1548121e085897871292a363ed08c26d60`. The R file `Log1p and gaussian GLMM FINAL.R` (Git blob `249e4f59d6f2bdada2d9245628d8ec48b4206d95`) reads explicit batch blocks and fits `log1p_value ~ group + (1|batch)` using lme4/lmerTest and REML, as well as a raw-scale model. It has not been executed here. Its README describes a different Python/factorial workflow, so the actual R file and published methods must govern any reconciliation; a repository title alone is not a verified implementation.

The article also links [jburrone/Keuss-Harley-Ryadnov-Jackson-et-al.-Nature-2026](https://github.com/jburrone/Keuss-Harley-Ryadnov-Jackson-et-al.-Nature-2026); its inspected root exposes synapse-density material. It is not substituted for the spinal eEPSC analysis.

## Gate decision and next action

**A previously missing public numerical source now exists and has been downloaded.** The earlier blanket statement that only an author delivery can supply the values is outdated. This is a concrete reopening input for issue #44, under its existing plan.

**This inspection does not open the inference gate.** Next, validate amplitude unit/sign/processing against the final figure/methods; reconcile the three explicit batch labels with the declared independent differentiations and any nested culture/coverslip structure; review cell identity/repeated measurements, exclusions and QC; reconcile the actual R code with FR-K26-4d v1. Adapt the original layout transparently only after that review. The existing disabled input contract is unchanged. Do not treat 89 cells as 89 biological replicates or silently declare the three batch labels to be verified differentiation IDs.

If the available source/methods resolve those checks, proceed to the already approved conditional reproduction. If a precise missing mapping remains, a focused request to Fratta would then be justified; this inspection sends no message. No broad new dataset search, STMN2 refit or endpoint substitution is proposed. This does not resolve the separate AD Workbench gate for #37.

## Reproduce this inspection

Download the exact publisher XLSX using the source URL above and preserve the original bytes. From the repository root:

```sh
python scripts/inspect_k26_fig4_source.py --input /path/to/41586_2026_11256_MOESM7_ESM.xlsx --output /tmp/k26-inspection.json
```

The script refuses a changed source hash or unexpected panel/header/block/count/formula structure and exports aggregates only. It performs no hypothesis test, group mean or rescue estimate. `inspection.json` is the deposited output. This new source check is separate from passing the repository's offline software suite.
