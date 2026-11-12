# Independent paired-marker source screen after Ikegami

Date: 2026-11-10. Luis authorized proceeding to an independent source after the subtype-conditioned analysis. This is a new bounded source-feasibility cycle, not a continuation of the closed #37 candidate search.

## Question and known information
Can one of three selected primary studies supply explicitly paired STMN2 truncation/cryptic and UNC13A cryptic measurements, biological-unit identifiers, and an independently measured TDP-43 phenotype? Titles, abstracts, availability statements and main-text summaries are already inspected. No source-data workbook for these candidates has been inspected; no new association is estimated.

## Fixed candidates
1. Agra Almeida Quadros et al. 2024, DOI 10.1007/s00401-023-02655-0, PMID 38175301: AD tissue, both markers and pTDP-43; different disease and brain regions, not ALS replication.
2. Gittings et al. 2023, DOI 10.1007/s00401-023-02599-5, PMID 37466726: C9ORF72 ALS/FTD snRNA-seq; inspect whether UNC13A cryptic event is actually measurable, rather than substituting gene expression or another target.
3. Ramsey et al. 2026, DOI 10.1172/JCI190035, PMID 42302828: GRN organoids and FTLD-GRN tissue; publicly linked Supporting Data Values. Main text already reports no detectable cryptic exon retention in the organoids; do not treat the paper as a positive association source by title alone.

## Admission and stop rules
- Inspect primary methods/availability and small source-data/index files only. Download at most 25 MB total of source workbooks or technical manifests; no raw FASTQ/BAM, gene-expression matrices or mass data retrieval. Hash exact files and record URLs, size, status and retrieval date.
- Do not download participant demographic tables, identify participants or change access permissions. Public molecular observations in an explicitly labelled source workbook may be inspected, without joining demographics. No accounts, access requests, contacts, spending or laboratory work.
- Require within-source explicit pairing (a shared sample key or a source scatter plot's documented pair), cryptic-marker specificity, sufficient observable range, biological-unit/culture/batch provenance, and a route to link the TDP-43 measure. Row order alone is not a key. Many nuclei, images or technical replicates do not establish biological replication.
- Distinguish direct nuclear TDP-43 loss from aggregate/phosphorylation burden. Distinguish abundance by PCR from junction inclusion. External AD/FTD or organoid evidence cannot be called independent ALS replication.
- Independently verify accessions and whether samples are reused. Unverified overlap stays unknown. An independent source family is not automatically an accepted dataset.
- If an admissible paired source exists, register a separate analysis protocol before any inferential calculation; this screen does not authorize searching for a significant result. If no source qualifies, report the exact missing inputs and close this cycle. No fourth candidate by inertia, no digitizing figures, no simulation as evidence.

## Deliverables
A three-row decision table with primary locators, a hashed file inventory and source-layout inspection if available; report with Evidence / Interpretation / Limitations / Next experiment; update STATE and BACKLOG through the current review branch. Preserve #37/#44 gates and the previous results. No new tests for a documentation-only screen. Existing CI is assessed on the final commit if it runs.
