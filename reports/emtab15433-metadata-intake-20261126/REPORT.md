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
