# Local raw-RNA-seq feasibility inventory — 12 November 2026

Base: `bff46c6488abe3358df730139276e657b0d443db`. Luis chose a local-computer route after the processed-count availability closures. This is a new access/resource inventory, not a new experiment or a reopening of #37, #44 or the closed STMN2 cycle.

## Fixed question and sources

Can one of the two already-screened experiments support a bounded local UNC13A measurement workflow, using existing WSL/HISAT2 infrastructure? Reuse the original six whole-transcriptome GSE252892 libraries GSM8009878–GSM8009883, and the ten GSE299341 soma libraries GSM9037603–GSM9037607/GSM9037613–GSM9037617. These are previously known candidates, not new independent sources. Exclude 3'-end libraries, neurites and other RBP arms. Runs are technical accessions and do not establish independent biological units.

## Prospective method and stopping rule

Reuse committed GEO sample mapping and the earlier cached primary/mapping material with explicit provenance. Obtain ENA read_run metadata only for PRJNA1063175 and PRJNA1273942, retaining exact selected SRX links, paired FASTQ URLs, compressed bytes and MD5. Maximum four HTTP attempts, 2,000,000 response-body bytes total, each at most 1,000,000; verified TLS, no automatic retry. Up to two optional primary full-text metadata routes fit within the same caps if needed; no broad search or third candidate. Stop after both fixed decisions or cap/access failure. Do not request raw FASTQ/BAM, make model calls or contact authors. Missing metadata stays unknown; neither counts nor coverage are measured.

Check whole-transcriptome assay, treatment labels, depletion-efficacy evidence and technical/biological nesting from the existing material. Prefer a route only if its assay/processing is sufficiently understood; total compressed bytes alone cannot decide scientific eligibility. Report exact file totals and unknowns without declaring nominal replicates to be donors. No effect, PSI, estimator change or threshold tuning. The existing ~200 canonical scenario is not a hard gate; canonical counts are not an upper bound on cryptic counts.

## Host and eventual execution gates

User-reported Windows: i5-12400, 6 cores/12 threads, 15.8 GiB RAM, 564.9 GiB free C:, D: nearly full. Ubuntu-24.04 WSL2 sees 7.6 GiB RAM/~7 GiB available, 2 GiB swap; Linux virtual disk capacity is not proof of physical free space. Python 3.12.3, HISAT2 align/inspect 2.2.3 and PySAM 0.23.3 are reported runnable. Eight hg38 index members and make script exist under the historical path; current hashes/reference compatibility and peak resources remain unverified. This is user-provided terminal evidence, not remote host inspection.

Prediction: an accession-level compressed-size manifest can be made, but resource feasibility and biological readiness may remain conditional. Failure is unmapped/missing file metadata or unresolved assay/perturbation design, not an inferred biological zero. No runtime or RAM benchmark is predicted from presence/version checks.

A later execution plan must lock one source, exact input files/checksums, index/reference/target hashes, processing (including any UMI handling), measured pilot resources, disk/transfer/time limits, and stop behaviour before any raw acquisition. Do not reuse or reactivate old CTRL-4/TDP-5 plans. Small prefixes can test software/resources, not refute full-library coverage. No costs or mass transfer are authorized by this inventory; leave any proposed raw budget unexecuted for review.
