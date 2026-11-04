# Bounded ELK1 RNA-FISH replay plan — 2026-11-04

User-authorized exploratory extension; independent of #37/#44 and PAPA TPM replay. Base main: f1ce8470905296390261432d78fd6a69991168c2. Source frattalab/tdp43-apa pinned e0d54b6f60a094c79f05f57ab4c88e451127bcbb.

Question: can image counts reproduce the three replicate-level ELK1 probe-count and localization ratios deposited with the public wet-lab scripts? No new treatment/rescue or biological novelty is claimed.

Inputs: wet/data/fish_counts_cleaned.tsv and two tiny deposited ratio tables; inspect fish_process_counts.R, fish_plot.R, fish_stats.R, README and version metadata. Verify original byte size/Git blob/SHA256, do not republish originals or download images/large archives. Establish article/preprint version before attributing panels.

Method: reproduce R-specified pivot and aggregate operations in Python with exact rational arithmetic. Treat images as nested observations, not biological replicates; preserve the three source replicate labels without inferring donor/culture identities. Normalize KD to CTRL within replicate and probe. Compare to all deposited ratios at 1e-8 tolerance (rounded CSVs). Audit numerator/denominator accounting: pivoting regions repeats each image nucleus count, so retain source arithmetic separately from once-per-image normalization. Prediction: any constant factor shared by arms cancels in fold changes, but changes absolute per-nucleus values. Failure: source mismatch, missing/ambiguous pairing, malformed counts or mismatched derived values must be reported, not repaired by inferred IDs.

Sensitivity: compare pooled foci/pooled nuclei with equal-image averages and leave-one-replicate-out means; label sensitivity descriptive. No p-values by default: independence is not certified from labels, and public scripts contain different testing/ratio conventions requiring version adjudication. No claims of actual R execution, automated image recount, final-paper figure replication or functional efficacy without direct evidence.

Deliverables: one bounded script, meaningful denominator/identity tests, replicate tables, provenance, discrepancy report and a reviewable PR. Stop after this dataset; do not automatically expand ELK1 into a therapeutic program, or repeat searches/access requests. Keep #37/#44 blocked and unchanged. If final article omits FISH, label this specifically a preprint-era experiment.
