# recount3 availability check for the Question A candidates — 12 November 2026

**All three candidates are absent from recount3. Question A closes for them on data availability, before any coverage question is reached.** This is a catalogue lookup, not a measurement: no junction counts were downloaded and no coverage was measured.

Required by the [Question A plan](../../research/plans/2026-11-12-questionA-measurement-reproducibility.md), which recorded recount3 availability as unverified for all three.

## Method

recount3's human SRA project index was downloaded once and read locally:

- URL: `https://duffel.rail.bio/recount3/human/data_sources/sra/metadata/sra.recount_project.MD.gz`, redirecting to `recount-opendata.s3.amazonaws.com`
- 2,890,522 bytes, SHA256 `f28cbb775b5037c91250c353b2c422c046fc43426d33a8191c71a81705e55b01`
- One row per sequencing run: `rail_id, external_id, study, project, organism, file_source, metadata_source, date_processed`

GEO series were mapped to SRA study accessions through NCBI E-utilities (`esearch`/`elink`/`esummary`), then looked up in that index.

## Result

| GEO series | SRA study | Runs in recount3 | Status |
|---|---|---|---|
| GSE252892 | SRP482832 | **0** | Absent |
| GSE299341 | SRP590954 | **0** | Absent |
| GSE298758 | SRP589302 | **0** | Absent |
| SRP166282 (Klim, already measured) | — | 18 | Present, `date_processed` 2019-10-01 |
| SRP334561 (Ma, already measured) | — | 12 | Present, `date_processed` 2023-08-16 |

The two controls are the projects this repository has already measured. Their run counts, 18 and 12, match `n_samples` in the two recorded result files exactly. That is the positive control for the lookup: the method finds projects that are genuinely there.

## Why they are absent, and the limit this exposes

Absence is not explained by accession recency alone. recount3's human SRA compilation holds **8,103 distinct SRP projects**, and only **16** of them carry an accession above SRP482832 — one above SRP589302 and SRP590954. By `date_processed` the compilation is overwhelmingly its original build:

| Year processed | Projects |
|---|---|
| 2019 | 8,677 |
| 2021 | 19 |
| 2022 | 6 |
| 2023 | 57 |
| 2024 | 28 |
| 2025 | 15 |

(Counts are of project rows in this index; the distinct-project total differs slightly.)

So recount3 is, in practice, a 2019 snapshot with a thin trickle of later additions — about 125 projects across six years. It is **not** frozen: 15 projects were processed in 2025, and the latest `date_processed` is 2025-09-26. But a deposit from 2025 or 2026 is very unlikely to be present, and these three are not.

This qualifies, without retracting, the earlier statement that recount3 solves issue #37's measurement blocker as a capability. The capability is real — junction counts without FASTQ or alignment — but its **catalogue is nearly static**, so it reaches recent deposits only by exception. No claim is made here about recount3's future updates, about other recount3 collections (`gtex`, `tcga`, `ANSWER_ALS`, `TARGET_ALS`, `ega`, `LIBD`), or about availability of these studies through any other route.

## Consequence for the screening order

Stage A spent its metadata budget selecting candidates from GEO that recount3 could never have measured. The check performed here costs one file and one lookup, and would have excluded all four focal candidates before any GEO inspection.

**The order was backwards.** Any future recount3-based screen should intersect with this project index *first*, and only then inspect design, efficacy and background metadata for the projects that survive. That is a process correction; it does not invalidate the Stage A records, whose design observations stand.

## What this does and does not establish

Question A is closed for these three candidates on availability. It is **not** answered: no cryptic-junction coverage was measured in any new deposit, so whether the UNC13A cryptic junction is observable at adequate depth in an unexamined experiment remains open. The 20-read minimum was neither applied nor relaxed. Question B's negative result in PR #64 is unaffected. Issue #37 stays closed, and nothing here nominates a design review.

No contact, access request, cost or personal data was involved. Downloads: one index file, 2.89 MB.
