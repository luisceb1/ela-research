# E-MTAB-15433 metadata intake — 26 November 2026

[Prospective scope](../../research/plans/2026-11-26-emtab15433-metadata.md). The [official BioStudies study](https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-15433) is cited by Brown et al. ([article](https://pmc.ncbi.nlm.nih.gov/articles/PMC12667841/)) and was reused in [the September 2026 circular RNA article](https://pmc.ncbi.nlm.nih.gov/articles/PMC13596441/). These citations do not add independent samples.

The bounded [metadata job](https://github.com/luisceb1/ela-research/actions/runs/45845146376) retrieved the study JSON (17,183 bytes, SHA-256 `cfe2bac1213466d94f6517e0601163d8d5e0ab67f65e1a3c333370723ab72752`). The [file catalogue receipt](metadata.json) identifies 16 gene-level quantification files, eight labelled control and eight labelled TDP43 KD, plus IDF and SDRF. The gene-quant filenames are grouped as A/B and C/D, but these labels cannot establish biological cultures, pairing or batch. No junction-count file was identified in this study catalogue. The author repository tree was inspected separately (tree `80fa3d70418a4665a85d414e33c7c470a9312086`); no unambiguous i3LMN-specific per-library junction filename was identified. No target values or clinical files were opened.

| Item | Status |
|---|---|
| Official study metadata | Retrieved |
| Gene quantification files | 8 control, 8 KD; filenames only |
| Technical SDRF | Listed, 21,932 bytes; two bounded file requests returned URLError |
| Independent experimental unit / batch map | Not verified |
| Compatible per-library splice-junction evidence | Not verified |

**Decision: pending, not admitted.** The smallest useful next input is the public SDRF and accompanying design/assay documentation, or an identifiable compatible per-library junction table. [SDRF file link](https://www.ebi.ac.uk/biostudies/files/E-MTAB-15433/E-MTAB-15433.sdrf.txt). No raw data, new analysis, Hetzner resources, contact or additional cost. This source is promising only at the catalogue stage; its availability does not repair the Tanaka coverage gap or imply independent replication.

## User-supplied public SDRF — 26 November 2026

The user supplied the listed SDRF in a ZIP (22,072 bytes; SHA-256 `9aaf50651992a0bb9a395bb49ccdcf61313ae039478bae6ea658240a9dda1270`). Archive integrity passed; the single SDRF member is exactly 21,932 bytes, consistent with the official catalogue, SHA-256 `42d89abbb3ad6dc4de0ba5eb4623ce7a598c0eb93911a8c85e581ee0873a5fde`. The [parsed audit](sdrf_audit.json) preserves the technical sample mapping without raw sequence data or personal identifiers. The original user-supplied archive remains privately retained.

All 32 rows have 39 columns. They resolve to 16 unique source, extract and assay names, 16 distinct ENA runs/experiments and 16 BioSamples; each source has two distinct mate URIs and one consistent run, condition and derived gene file. All 16 derived filenames reconcile with the official catalogue. The manifest identifies paired-end, second-strand libraries in WTC-11 lower motor neurons, with eight control and eight TDP-43 KD libraries. The declared culture condition is shared.

| Label group | Condition | Libraries |
|---|---|---:|
| A | control | 4 |
| B | control | 4 |
| C | TDP-43 KD | 4 |
| D | TDP-43 KD | 4 |

There is no explicit culture/differentiation/batch or replicate field. These condition-exclusive letter codes cannot establish experimental independence, pairing or batch equivalence. If they correspond to independent preparations or condition-confounded batches, those possibilities entail different interpretations; neither is inferred from names. A BioSample or file is not automatically a biological replicate.

**Decision:** technical manifest recovered and reconciled; scientific admission still pending. No per-library junction counts identified, no raw acquisition or inference authorized. The remaining concrete questions are the meaning of A/B/C/D, the biological preparation map, and availability of per-library splice-junction counts with reference/count convention. The user reports effective AD Workbench and Target ALS access remains unavailable. No data transfers, communications or additional expense.

## Authorized source clarification request — 26 November 2026

The user explicitly authorized one request to the corresponding author Anna-Leigh Brown, whose professional address is listed in the [author record](https://www.biorxiv.org/content/10.1101/2025.11.23.689722v1). Sending was confirmed in the user's mailbox. The two requested inputs are the interpretation of A/B/C/D and the library-to-culture/differentiation/batch map, and availability of per-library junction counts or a compatible sample-linked count matrix. No raw reads, private data or attachments were requested. Await substantive reply; no reminder, additional contact or analysis scheduled. No claim of data availability follows from sending this request.
