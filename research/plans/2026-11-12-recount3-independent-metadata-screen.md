# Proposed bounded recount3 independent-source screen

Date: 12 November 2026. Base: merged main `1557bffd03e29a4d565b20e35964b2a42181a31f` (PR #63). **Plan for review only; execution has not started.** No SRA/GEO/recount3 discovery request, candidate inspection, new count download or source-effect calculation preceded this plan. Historical project results informed the question; it is not a blind hypothesis.

## Question, expected result and scope

Can a previously unexamined public human-neuronal TDP-43 depletion experiment provide accessible whole-transcriptome junction counts, documented depletion efficacy and at least three independent genetic backgrounds per condition, with enough directly observed UNC13A cryptic-junction coverage to nominate a separate design review?

Working expectation: **zero of at most three selected projects will meet all criteria**. This is a prospective expectation, not an estimated probability or an established claim about typical datasets. One qualifying project refutes it. Zero means failure of this finite source screen, not proof that public RNA-seq cannot answer the question. No inference about functional recovery, therapeutic rescue or clinical benefit is sought.

Only plan drafting is performed now. Stage A metadata discovery requires Luis's explicit scope decision on this plan. Stage B count inspection additionally requires a concrete Stage A manifest and explicit authorization for its byte-bounded downloads. Opening/merging a plan PR alone does not silently launch either stage. Issue #37 remains closed; its earlier suspension of the 20-read acceptance criterion is not silently reversed. A positive screen nominates design review, not an analysis or issue reopening.

## Existing criteria versus proposed amendments

| Element | Provenance and rule in this proposal |
|---|---|
| Whole-transcriptome assay; documented depletion efficacy | Retained from the sharpened source requirements in STATE and the fraction-discrepancy report. A measured RNA or protein reduction must be attributable to the functional assay's condition, dose and sampling interval, with modality/source recorded. Induction alone is insufficient. No new favorable percentage cutoff; no estimation from amplicon counts. |
| Approximately 200 canonical reads | **Historical conditional scenario, not a sealed unconditional threshold.** STATE says approximately 200 *if* the fraction is near 0.10; the fraction audit did not establish a true fraction or a calibrated depth requirement. Preserve the example as context; do not turn it into a hard exclusion or combine it with 20 as two established gates. A canonical maximum of 66 does not prove no alternative fraction could yield 20 cryptic reads. No PSI or fraction is calculated in this screen. |
| At least three independent units per arm | Historical wording allowed independently generated cultures from HUES3 while acknowledging one genotype. **New proposed restriction:** at least three distinct donor/genetic backgrounds, each represented in both KD and control. This narrows the target to cross-background reproducibility; it does not mean separate cultures are never independent experimental replicates. Single-background projects are rejected for this proposed design even if deep. Multiple clones, wells or differentiations from one background do not satisfy the genetic-background count. |
| Cryptic coverage of 20 | Preserve the existing assay diagnostic on each individual sealed junction and library. The probe's legacy `gate_met` only needs one qualifying sample; it is not an inferential design gate. **New proposed nomination rule:** the same cryptic junction must reach at least 20 in the metadata-selected KD library from each of at least three backgrounds, with linked controls and canonical measurement in every selected library. This stricter rule is declared before candidate selection; it changes no legacy output or threshold. |

## Frozen measurement inputs

Reuse `research/references/unc13a_targets_sealed.json` and `scripts/recount3_junction_probe.py` unchanged. SHA256 respectively:

- `e35f6e05016b30eab89f8d3aacc2d4ec101840e24e2b6f07159e6c5235d0bc3a`
- `0b5fbaf72d331298e820236d2ecdbf58bc359c6eb9be9ab5685da01440ff4f15`

GRCh38, chr19, minus strand, intronic 0-based half-open targets: canonical `[17641556,17642844)`, cryptic-left `[17641556,17642413)`, cryptic-right `[17642541,17642844)`. The existing conversion is `[start0+1,end0]` in 1-based inclusive intron coordinates; retain its `length == end-start+1` guard. Do not rederive, shift, accept nearest coordinates or filter by `annotated`. Stop on source-hash or convention mismatch; no replacement target.

The sealed file's historical `project` label is provenance, not a new candidate identity; a future adapter must label each new output by the manifest's actual project without editing the sealed measurements or misreporting a new project as SRP166282. No adapter is implemented by this plan.

## Prior-work exclusion

Explicitly exclude **SRP166282/GSE121569 (Klim)** and **SRP334561/GSE182976 (Ma amplicon)**: already measured, not new validation. Exclude previously inspected Brown/Liu deposits and reused accessions, closed Humphrey/GSE296714 pilot/processed routes, RiMOD/NYGC/TARGET_ALS/ANSWER_ALS patient cohorts, and previously audited functional sources as new families. Compare candidates against [the prior-source inventory](../../reports/source-gate-issue37-20261103/prior_sources.tsv), [PR #63 exclusions](../../reports/independent-postdeficit-screen-20261112/prior_work.tsv) and current STATE before selection. A new accession/version/name is insufficient evidence of new experimental observations. Unknown overlap remains pending, not independent.

## Stage A — finite metadata-only selection

After explicit authorization, use at most three discovery query groups, each with at most two fixed queries; at most 30 distinct study records and **10 MB total** metadata/text transfers. Proposed groups: (1) human neuronal TARDBP/TDP-43 knockdown or depletion SRA/GEO; (2) induced cortical/i3Neuron TDP-43 loss with RNA-seq; (3) motor-neuron TDP-43 depletion with RNA-seq. Write exact query strings/filters before the first request. No fourth group or expanding the budget after negative results.

Record all discovered records and deduplicate by experiment lineage. Select at most three eligible projects before any junction counts. Eligibility: actual human neuronal depletion/control contrast, whole-transcriptome short-read RNA-seq rather than targeted/iCLIP/Riboseq/single-cell gene matrix, documented efficacy, explicit background/differentiation/library mapping, matched backgrounds across arms, no complete condition/batch confounding, no unresolved reuse, and concrete recount3 processed-file availability. A library-strategy label or title alone cannot establish these facts.

For multiple libraries per background/condition, freeze one by documented assay/QC compatibility first, then highest comparable total read count, then accession lexical order for ties, **before inspecting junction counts**. Record omitted technical libraries. Unknown donor/clonal ancestry, efficacy, pairing or batch structure is pending; it does not count as eligible. Published claims of replication without a usable map are insufficient.

Among eligible projects, rank by complete unit/efficacy metadata, then comparable per-library depth and read length (missing/incomparable values last), then project accession. These are priority variables, not a claim that depth uniquely causes prior failures. Do not reject ordinary projects as mathematically unable to pass from a generic depth/read-length cutoff. A hard numerical impossibility exclusion needs an independently verified upper bound on supporting reads in compatible units below 20; otherwise label it prioritization/unknown. Do not impute missing values.

Stage A output is a complete discovery/rejection table plus at most three frozen manifest entries: accession/aliases/version, assay/perturbation, efficacy modality/value/time/source, background and differentiation identities, condition/batch map, declared total reads/read length and units, known reuse, exact recount3 URLs/sizes, and decision with locators. If zero are eligible, close without count downloads. If some qualify, stop at this manifest for the Stage B decision.

## Stage B — conditional availability/coverage inspection

Only after specific authorization of the manifest: at most the three fixed projects, **200 MB cumulative compressed transfer budget including Stage A**, no FASTQ/BAM, raw imaging, genome alignment or paid access. Check declared sizes before each transfer; enforce a streamed byte cap when size is absent/unreliable and include partial/error transfers in the budget. Stop rather than replace an oversized, blocked or negative project. No disabling TLS verification, mirror chase or new contact.

Hash actual input bytes, use isolated per-project directories, and run the existing probe with exact targets and `--min-coverage 20`. Record all canonical and individual cryptic counts for the fixed selected libraries, including zeros and low counts. Do not sum cryptic-left/right, pool donors/libraries, average to pass a threshold or select a different library after seeing coverage. Canonical detection is a measurement control, not proof of unbiased cryptic detection or valid design. A cryptic zero is an observed zero count, not proof of biological absence; below-threshold observations are ineligible for this proposed inference-readiness criterion.

Reject/pending/nominate are separate: pending metadata is not acceptance; failure of the new three-background coverage rule is a bounded nomination failure, not proof that another question is impossible. Controls with zero cryptic reads remain retained. Assay-shape flags trigger primary-source verification; they cannot certify assay identity. No source is nominated automatically from the probe's boolean.

## Deliverables and stop

English report, all discovery decisions, at most three fixed candidate rows, source locators/versions, sizes/hashes and request/error log; if authorized, per-junction coverage and the separately computed proposed nomination status. No PSI, effect, model, significance test, power calculation, simulation, clinical interpretation or coordinate change.

Stop at the query/record/byte caps, inaccessible required source, failed convention/hash guard, zero Stage A eligibility, or completed adjudication of the selected projects. No substitutions after results. If none qualify, close and retain negatives; if one qualifies, write a separate prospective effect design only after its scope is authorized. No automatic merge, #37 reopening, outreach, access request, expense or watcher modification.

## Plan-only verification

At drafting: main and merged PR baseline checked; frozen source hashes/coordinates and probe diagnostic semantics inspected locally; links and distinction between old rules and new proposed restrictions checked. No candidate or count file queried. The plan changes no scripts, inputs or historical results. This document is proposed for review before execution, not evidence that either stage has been approved.
