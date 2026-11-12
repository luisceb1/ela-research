# English evidence and reproduction guide

[README](../README.md) · [Current findings](CURRENT_FINDINGS.md)

## Reading route

These seven complete report translations cover the evidence chain behind the current findings. Each retains its original scope, numerical results, corrections and limitations. A dated proposed next step in an earlier report may already be completed by a later one; the closing report and current findings take precedence. The operational history and plans remain in their original language unless separately identified.

| Evidence | English report | Spanish original | Executable entry point | Deposited output |
|---|---|---|---|---|
| STMN2 junction and technical units | [Audit](../reports/stmn2-map-audit-20261111/REPORT.en.md) | [Original](../reports/stmn2-map-audit-20261111/REPORT.md) | [audit_stmn2_units.py](../scripts/audit_stmn2_units.py) | [Results](../reports/stmn2-map-audit-20261111/results.json) |
| Paired STMN2 tissue comparison | [Paired analysis](../reports/paired-stmn2-20261111/REPORT.en.md) | [Original](../reports/paired-stmn2-20261111/REPORT.md) | [paired_stmn2.py](../scripts/paired_stmn2.py) | [Results](../reports/paired-stmn2-20261111/results.json) |
| RNA-integrity sensitivity | [RIN](../reports/stmn2-rin-20261111/REPORT.en.md) | [Original](../reports/stmn2-rin-20261111/REPORT.md) | [stmn2_rin_sensitivity.py](../scripts/stmn2_rin_sensitivity.py) | [Results](../reports/stmn2-rin-20261111/results.json) |
| Composition linkage and comparability | [Composition gate](../reports/stmn2-composition-20261111/REPORT.en.md) | [Original](../reports/stmn2-composition-20261111/REPORT.md) | [stmn2_composition_gate.py](../scripts/stmn2_composition_gate.py) | [Results](../reports/stmn2-composition-20261111/gate.json) |
| Final within-region associations and closure | [Closing report](../reports/stmn2-within-region-20261111/REPORT.en.md) | [Original](../reports/stmn2-within-region-20261111/REPORT.md) | [stmn2_within_region.py](../scripts/stmn2_within_region.py) | [Results](../reports/stmn2-within-region-20261111/results.json) |
| Corrected UNC13A coverage normalization | [Coverage](../reports/target-als-cervical-20261111/REPORT.en.md) | [Original](../reports/target-als-cervical-20261111/REPORT.md) | [normalize_tissue_coverage.py](../scripts/normalize_tissue_coverage.py) | [Normalization](../reports/target-als-cervical-20261111/depth_normalisation.json) |
| Intervention chronology and rule ambiguity | [Timing](../reports/unc13a-intervention-timing-20261110/REPORT.en.md) | [Original](../reports/unc13a-intervention-timing-20261110/REPORT.md) | [verify_matrix_quotes.py](../scripts/verify_matrix_quotes.py) | [Matrix](../reports/unc13a-intervention-timing-20261110/matrix.tsv) |

## Reproduction

Run commands from the repository root. Install [pinned CI requirements](../research/requirements-ci.txt) for the offline suite; analysis dependencies and inputs are described in each report. The translated command blocks retain the original paths, flags and filenames, including Spanish filenames. Replace temporary-directory placeholders with your own paths.

For STMN2, the [audit source manifest](../reports/stmn2-map-audit-20261111/sources.json) pins URLs and hashes. The source root used by subsequent scripts contains these source files and a `repo/` subtree with the original deposited count JSONs at their repository paths. The RIN/composition/within-region reports specify the additional `source-gate/` workbooks and hashes. Outputs record source/count hashes and aggregate results. Input workbooks are not committed; scripts' exact layout/hash checks must pass before reproduction is claimed.

For UNC13A normalization, obtain the two TARGET_ALS recount3 QC tables, verify their hashes in [depth_normalisation.json](../reports/target-als-cervical-20261111/depth_normalisation.json), and supply their paths alongside the committed count JSONs. The report names all five QC denominator fields. Missing QC linkage leads to refusal, not a silent subset estimate.

For timing, [sources.json](../reports/unc13a-intervention-timing-20261110/sources.json) pins the inspected sources and [matrix.tsv](../reports/unc13a-intervention-timing-20261110/matrix.tsv) contains the classifications and locators. The quote-checking command needs a source-ID→text map and the corresponding legally obtained source files. The two supplied PDFs are not redistributed. The quote verifier checks text, not experimental classification or design adequacy; some local inputs are therefore needed beyond cloning the repository.

```sh
python -I scripts/verify_matrix_quotes.py \
  reports/unc13a-intervention-timing-20261110/matrix.tsv \
  --sources <source-map>.json --base <source-directory>
```

`<source-map>.json` maps each `source_id` to its source text; use the pinned inputs and documented extraction/normalization rules. Placeholder paths are not runnable without those files.


The documentation update does not claim fresh downloads or end-to-end replay of every analysis. Source hashes, commands and scientific limitations remain visible even where an external access/input prerequisite remains.

## Translation policy and review

English is the default for new scientific/public documentation and new code comments/docstrings. Luis's internal working material and the historical archive may remain in Spanish. Existing code identifiers, data columns, JSON keys, source quotes, coordinates and filenames are not renamed for language consistency.

Each `REPORT.en.md` is a dated translation of the Spanish report at **`c7d8f7e92e7eb02e3fb619f6e8984f075ef84784`**, not a fresh analysis. [translation_manifest.json](translation_manifest.json) records SHA-256 of both texts, scope and review checks. Spanish report bodies are preserved byte-for-byte; each original adds only an English companion link after its title. The manifest distinguishes the pinned source hash from the current file hash including that navigation line. Links between translated reports follow the English route where available; original plans, curation and other untranslated documents are explicitly part of the source record.

Review includes numerical tables and thresholds, source/commit identifiers, links, reproduction command blocks, negative statements and uncertainty. Numerical locale changes only presentation: for example, Spanish `0,003676` becomes English `0.003676`. Command blocks and source identifiers retain their original bytes. Interpretive labels such as `prevention` remain recorded labels, not proof that a functional deficit was absent.

This is an AI-assisted translation and comparison, not independent expert scientific validation. It preserves dated statements, including explicitly superseded next steps; it does not silently update publication/access status. A source correction requires updating the affected English report, this manifest and the current findings together. A later source hash mismatch means the translation needs review, not that the Spanish file should be overwritten. When versions disagree, consult the pinned source and correction history; neither language grants permission to strengthen a claim.

## Corrections and contributions

A useful correction identifies the report, exact statement, source locator or count output, and the proposed bounded change. Separate software correctness, arithmetic reproducibility, biological replication and interpretation. Keep failed predictions and negative results visible. Before proposing a new contrast, read the existing stop rules and define the design and failure criterion before calculating the result.
