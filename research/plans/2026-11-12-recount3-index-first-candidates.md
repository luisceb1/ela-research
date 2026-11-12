# Index-first candidate search for Question A

Date: 12 November 2026. Base: merged main `f10e685c2888d2e1f7c644dd42035dadf8970c67`.
**Plan committed before any discovery query.** Authorised by Luis as a new scope decision; the Question A plan's "no fourth candidate" rule applied to its own three candidates and is superseded for this search only.

## Why the order is reversed

PR #67 established that all three previous candidates were absent from recount3, and that the human SRA compilation is overwhelmingly its 2019 build — 8,103 distinct projects, about 125 added across 2021-2025. Selecting candidates from GEO first wasted a metadata budget on studies recount3 could never measure.

This search therefore starts from what recount3 actually holds and works outwards.

## Question, prediction and failure criterion

**Question.** Which human SRA projects *held by recount3* are TDP-43 depletion or loss-of-function experiments in neuronal material that this project has not already audited?

**Prediction, refutable.** The intersection will be dominated by families already audited and rejected. recount3's catalogue is essentially pre-2020, and the pre-2020 TDP-43 depletion deposits are exactly the ones issue #37 already worked through — Klim, Melamed, Humphrey, Ma, Brown/Liu and the rest of the 15-family inventory. **Expected: zero to two unaudited survivors.** Three or more refutes the prediction and would mean the earlier source gate missed accessible material.

**Failure criterion.** Zero unaudited survivors closes the recount3 route for Question A, recorded as a dead end with its table, not as proof that no public junction counts exist anywhere. One or more survivors are reported with their declared metadata only; whether any is worth measuring is a separate decision.

## Method

1. Reuse the recount3 human SRA project index already retrieved and hashed in PR #67: `sra.recount_project.MD.gz`, SHA256 `f28cbb775b5037c91250c353b2c422c046fc43426d33a8191c71a81705e55b01`. Re-download only if the hash cannot be reproduced; stop on mismatch.
2. Query NCBI E-utilities for human RNA-seq studies perturbing TARDBP / TDP-43, collecting SRA study accessions. At most **six queries**, exact strings recorded before execution.
3. Intersect those accessions with the recount3 index. Only the intersection proceeds.
4. Exclude prior families against `reports/source-gate-issue37-20261103/prior_sources.tsv`, `reports/independent-postdeficit-screen-20261112/prior_work.tsv` and current STATE. A new accession or title is not a new experiment.
5. For survivors, record declared organism, sample count, `date_processed`, study title and the deposit's own condition labels. Nothing inferred from titles or ordering.

## Boundaries

**No junction counts are downloaded and no coverage is measured in this step.** Measuring a survivor requires a separate scope decision, and the 20-read minimum and the three-background question both remain exactly as recorded — this search does not relitigate either. Transfer cap 10 MB beyond the cached index. No author contact, access request, cost or personal data. Issue #37 stays closed; a survivor nominates nothing by itself.

Output: a table of the intersection with exclusion reasons, on a branch, in a reviewable PR, unmerged.
