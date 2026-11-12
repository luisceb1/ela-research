# Numerical reproduction

Install `research/requirements-stmn2-within-region.txt` in an isolated environment, then run the command in REPORT.md using the pinned source hashes. NumPy 2.3.4 matches the full offline CI dependency. Exact floating-point bytes can differ across BLAS/platform versions; compare coefficients with tolerance 1e-10, while donor counts, eligibility and hashes must match exactly.

Unadjusted Spearman values were separately checked with SciPy: absolute discrepancies 2.78e-17 (cortex) and 1.39e-17 (cervical), recorded in validation.json. SciPy is only a cross-check dependency, not required by the analysis script. Synthetic tests validate numerical controls; they do not validate the biological interpretation.
