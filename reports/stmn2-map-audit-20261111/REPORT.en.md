# STMN2: junction validated and partial donor map recovered

> English translation prepared on 11 November 2026 from the [Spanish original](REPORT.md) at `c7d8f7e92e7eb02e3fb619f6e8984f075ef84784`. Source/translation hashes and review scope: [English guide](../../docs/ENGLISH_GUIDE.md#translation-policy-and-review). This is a dated report, not a new analysis or publication-status check.
> Earlier proposed next steps are historical; for completed STMN2 work and current stop rules, use the [closing report](../stmn2-within-region-20261111/REPORT.en.md) and [current findings](../../docs/CURRENT_FINDINGS.md).

Date: 11 November 2026. Count baseline: `ad96ec5e3e5ebb40a12324c0802a4979916f5c4d`.
Scope fixed before the new joins at commit `7f9b04c613fc7ad80032ff0bc25fa0377392a6af`, [plan](../../research/plans/2026-11-11-stmn2-map-audit.md).
Original counts and claims were already known: this is a retrospective measurement/design audit, not prospective validation or a biological discovery.

## Evidence

### The probe measures entry to the documented terminal exon 2a

The sealed intronic, 0-based half-open, positive-strand GRCh38 junctions are unchanged:

| Event | Sealed interval | 1-based inclusive intron |
|---|---|---|
| Canonical exon 1→2 | chr8:[79611214,79636801) | 79611215–79636801 |
| Cryptic exon 1→2a | chr8:[79611214,79616821) | 79611215–79616821 |

The acceptor starts the cryptic exon at **79616822 (1-based)**. Melamed 2019 provides this start directly in hg38. The UCSC hg19→hg38 chain uniquely confirms the eight nucleotides checked around canonical/cryptic boundaries, without extrapolating an offset between blocks. Base-by-base results are in `results.json`.

The two earlier RefSeq anchors agreed but did not by themselves demonstrate alignment of the intervening region. This chain check and the directly published hg38 coordinate resolve that limitation.

**One-nucleotide precision:** Melamed describes the 227 nt terminal transcript at 79616822–79617048. The 228 nt counting interval used by Quadros, mapped through the chain, ends at 79617049. Both share the start; equivalence of their counting and cleavage endpoints is not established. This difference does not alter the junction we count.

### What the measure may miss

Screening was restricted to the four fixed source families, main text and relevant methods; it is not an exhaustive inventory of supplements or all human isoforms.

| Primary source and locator | Documented event or alternative | Consequence for our probe |
|---|---|---|
| [Klim 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC7153761/), Fig.3f–g and cryptic-exon section | Junction from exon 1 to the cryptic exon, without observed exit to downstream exons | Compatible with a terminal-entry junction |
| [Melamed 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6348009/), Fig.3c–e and 227-base paragraph | Terminal exon 2a with premature polyadenylation; no 2a→2 junction detected. Another alternative annotation between exons 4 and 5 is mentioned, not detected in their cells | The probe does not count all downstream isoforms or verify terminal cleavage |
| [Baughn 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10148063/), Fig.1H–I and cryptic-site-disruption section | After experimental inactivation of the proximal PAS, polyadenylated 1→2a RNAs persist; authors propose distal sites, without resolving individual use here | One acceptor can end at different sites; the probe pools them. Do not turn the paper's 61 candidate motifs into 61 observed isoforms |
| [Quadros 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC10766724/), STMN2 RNA-seq quantification | Exonic interval used to quantify truncated RNA | A published exon count does not directly equal our junction count |

No second validated cryptic acceptor requiring inclusion was identified within the screened text/methods. This does not prove its absence. The five regional `annotated=0` candidates do not acquire biological identity from their annotation flag. The probe also does not measure unspliced intron retention, stability, protein or axonal repair. **K/(C+K) is a local junction-read ratio**, not a calibrated molecular fraction; this terminal event does not require dividing K by two.

### Technical map: 293/313 samples, with 128 shared donors

Exact route: **(recount3 project region, rail_id) → external_id → original library key → declared donor + region + project**. `rail_id` is reused between regions: it is not a global key. The first join without region scope detected 245 apparent collisions; key scope was corrected and a specific check added before accepting the result. Conflicting keys within a region are rejected. All suffixes, including `-2`, are preserved; people are not inferred from prefixes.

Sources: Fratta author metadata (`cryptic_biology`, commit `80fa3d70418a4665a85d414e33c7c470a9312086`) and Table S1 of the GEO curation by [Jung 2026](https://www.mdpi.com/1422-0067/27/18/8011), repository `chaeyunjung/pd-als-transcriptomics`, commit `8e57756b7b875e0e4b326ecb900ee43d14e49c9b`. Accepted projects are respectively `Target ALS` and `Target ALS PM core`. These are two metadata routes for the same cohort; agreement **is not** independent biological replication.

| Check | Lateral motor cortex | Cervical cord |
|---|---:|---:|
| Samples in original counts | 149 | 164 |
| Exact linkage in Fratta metadata | 140 | 153 |
| Distinct declared donors in that linkage | 140 | 152 |
| Samples without accepted linkage | 9 | 11 |
| Linkage through Jung GEO curation | 117 | 129 |
| Samples common to both routes / matching donor keys | 117/117 | 129/129 |
| Donors with >1 sample in that region | 0 | 1 (two samples) |
| Pure ALS: linked / original samples | 81/84 | 92/95 |
| Controls: linked / original samples | 13/13 | 12/13 |

Fratta provides **128 donors in both regions**, out of 164 distinct donors in the union of linked regions. The Jung route confirms 104 shared donors in its subset. The 128 include all original groups, not just ALS/controls or sufficiently covered libraries. They are not yet an eligible contrast's sample size.

The four pure-ALS cervical samples with K≥20 link to **four different donors**. The eight with K≥20 across all groups link to eight donors; do not confuse these totals. The cervical duplicate is in the mixed group and must not become two independent replicates. Whether these are technical replicates or two extractions has not been determined: multiplicity is recorded and a rule is required before analysis.

Four original GEO records were also checked: first GSM per region/preparation stratum among exact links, without signal-based selection. **4/4** contain the same sample key, donor and region. Receipts are in `geo_spotcheck.json`; this is a bounded check, not an exhaustive rereading of GEO. The 20 unlinked samples remain excluded from the accepted map, without inferred keys.

### Corrections to the STMN2 report

Original counts are unchanged. The cervical ALS median with C+K≥20 remains 0.005684; the previous error concerned summary labels/population, not a numerical change in that median.

| Tissue / group | Total n | n with C+K>0 | n with C+K≥20 | Median / maximum, C+K≥20 | Maximum over all denominators >0 |
|---|---:|---:|---:|---|---:|
| Cortex / pure ALS | 84 | 84 | 82 | 0 / 0.029106 | 0.029106 |
| Cortex / control | 13 | 13 | 12 | 0 / 0.008547 | 0.008547 |
| Cervical / pure ALS | 95 | 92 | 58 | 0.005684 / 0.543860 | 1 |
| Cervical / control | 13 | 13 | 8 | 0 / 0.001027 | 0.001027 |

**P1 is not met:** normalizing each library first by `star.number_of_input_reads_both`, canonical medians are 0.929460 STMN2 and 0.114960 UNC13A per million; ratio **8.085**, below 10. Sensitivities using uniquely mapped and exon-assigned reads: 7.782 and 7.769. The ratio of raw medians, 33/5=6.6, also failed the criterion. The original prediction is not changed retrospectively.

**P2 is observed:** four pure-ALS samples with K≥20. This demonstrates capacity to obtain event reads in some libraries; it neither fully validates the assay nor identifies the cause of low UNC13A coverage.

**P3 describes sample frequencies only:** 48/95 versus 1/13 in cervical cord and 31/84 versus 1/13 in cortex. An inferential difference is not confirmed by overlap of Wilson intervals. Tissues share donors and coverage/composition differs; confounding by these routes is not excluded. Statements dismissing a coverage explanation or assigning causality to the locus are withdrawn.

## Interpretation and limits

The unit-identity blocker is **partially resolved** for an explicit subset, and a concrete paired-comparison route exists. No pTDP-43 burden data or functional result were recovered; UNC13A #37 and K26 #44 retain their original conditions. Independence between people does not replace information about tissue selection, extraction, batch, quality and cell composition.

No effect, p-value or disease contrast was fitted. Requiring K≥20 in controls would artificially select positive controls; a future design must fix eligibility by total information or measurement precision, allow K=0 when C is informative, and not redefine the existing UNC13A gate to declare STMN2 success.

Only technical keys, region, project and preparation were used. Age, sex, mutation, onset and progression columns were not used. Aggregates and hashes are exported; mixed tables or individual donor/disease rows are not committed. No contacts, costs, RNA download or new tissue. The GEO series response exceeded the 7 MB read limit and was discarded; Klim/Baughn XML failed or timed out and their primary text was consulted in PMC. Large downloads were not pursued.

## Next experiment

Write a single protocol for **STMN2 comparison between cortex and cord from the same donor**, conditional on verifying preparation/batch, C+K eligibility and usable pair count. Before the contrast, fix multiplicity aggregation, exclusions, endpoint and depth handling; stop if too few pairs remain or tissue and preparation cannot be separated by the design. This question's selection is informed by current results and requires external replication to support novelty. Do not start another cohort search by inertia.

## Reproduction and validation

Standard Python, without additional dependencies. From the repository root, with the exact manifest source files downloaded into a temporary directory:

```sh
python scripts/audit_stmn2_units.py --source-root /ruta/temporal/fuentes --cortex reports/stmn2-derivation-20261111/results_corteza.json --cervical reports/stmn2-derivation-20261111/results_cervical.json --unc13a-cervical reports/target-als-cervical-20261111/results.json --output /ruta/temporal/recheck.json
python -m unittest discover -s tests -p test_audit_stmn2_units.py -v
```

`sources.json` pins URLs, versions and SHA-256; the result also records historical-count hashes. Tests cover suffixes, inter-/intra-region collisions, conflicts, missing donors, wrong tissue, duplicates, aggregation without exporting keys, chain gaps/strand and normalization before the median. The GEO check has separate receipts. The complete suite is checked by PR CI; the bounded local test is not presented as local execution of the entire suite.
