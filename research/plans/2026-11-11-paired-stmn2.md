# Paired STMN2 cortex/cervical analysis — 2026-11-11
Exploratory protocol fixed before counting eligible pairs or fitting a paired effect. Previous marginal counts and tissue pattern are known; this is not independent confirmation or a preregistration made before seeing all outcomes.

Question: among exactly linked pure-ALS donors with comparable library preparation and informative coverage in both regions, is the local cryptic junction ratio higher in cervical cord?
Prediction: median paired difference (cervical minus cortex) is positive; a nonpositive median refutes this directional prediction in the retained subset.

Sources: historical STMN2 cortex/cervical count JSON, recount project metadata, pinned Fratta technical map and Jung GEO curation and hashes from reports/stmn2-map-audit-20261111/sources.json. No new downloads or clinical columns. Only anonymous technical keys are used transiently; export aggregate results, never individual donor rows.

Eligibility, in this order:
1. Exact region-scoped recount key and sample alias joins in BOTH metadata routes; donor key must agree. Correct project required. Groups come exclusively from original count JSON.
2. Group must be exactly ALS Spectrum MND in both regions. No mixed, unknown or control samples enter the primary effect. Apply the same technical pipeline separately to controls as a descriptive feasibility check only.
3. Exactly one library per declared donor per region, counted before coverage filtering; exclude multiplicities rather than choose the library with the best response or sum possible extractions.
4. Known library preparation in both regions from Jung, exactly matching (Manual KAPA Total or Automated KAPA Total). This is preparation compatibility, not proof of identical sequencing/extraction batch: those batch fields are unavailable. Count mismatches and exclude them.
5. C+K>=20 in EACH region, including K=0. No requirement for positive cryptic reads. No imputation. At least 10 eligible pure-ALS donor pairs and at least 5 nonzero paired differences required to execute the primary test. Otherwise report insufficient feasibility and stop; do not relax thresholds.
Endpoint: local junction ratio K/(C+K), same frozen junctions. Unit: declared donor, paired across tissue.
Primary summary: median within-donor difference, number cervical>cortex / ties / cervical<cortex. One exact two-sided paired sign test (binomial among nonzero differences, p=min(1,2*lower tail)). No pooled-read test, covariate fishing or disease-vs-control test.
Sensitivity: repeat aggregate median and direction counts at total denominator >=50 and >=100 in both tissues, no additional p-values. These thresholds do not amend primary eligibility.
Assay/design control: describe matched preparation strata and canonical/total read medians in each tissue among eligible pairs. Local total coverage differs by biology and quality; thresholding can select donors unevenly and cannot remove composition or RNA-quality confounding. Conditioning on total reads is not a measurement of neuronal fraction.
Interpretation: this exploratory paired association can address between-person confounding and documented library-preparation mismatch only. It cannot establish neuron-type dependence, TDP-43 burden, causality, function, novelty or therapeutic rescue. No result changes UNC13A #37 or K26 #44 gates.
Stopping: one primary contrast if gate passes, otherwise feasibility-only. No new cohort, no lab/contact/spending. Next discriminating evidence would be an independent, composition/QC-characterized paired cohort; do not call reanalysis of these same donors replication.
Validation: synthetic tests for exact sign-tail arithmetic, ties, zero cryptic counts, per-region multiplicity before coverage, preparation mismatch and gate enforcement; full offline suite in PR CI. Record source/script hashes and runtime.
