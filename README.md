# ALS — reproducible computational research

[Español](README.es.md) · [Current findings](docs/CURRENT_FINDINGS.md) · [English evidence and reproduction guide](docs/ENGLISH_GUIDE.md)

Independent, AI-assisted research on the transcriptomic consequences of nuclear TDP-43 loss of function, focusing on **STMN2** and **UNC13A**. The project is directed by Luis Cebrián Fraile and uses public sources. It contains technical reproductions, exploratory analyses, source audits and experimental proposals. It has not demonstrated a new therapeutic target, neuronal rescue or clinical benefit.

## Start with the current evidence

[Integrated evidence review and critical audit (26 November 2026)](reports/integrated-evidence-audit-20261126/REPORT.md) compares existing results with the primary literature, including the UNC13A measurement discrepancy in GSE304550 and the partial Keuss reproduction.

Current status: **26 November 2026**, including the completed local six-library STMN2 FASTQ replay audit and the fixed independent-host pilot for one library. Read [STATE](research/STATE.md) for the concise evidence and limits. Older reports preserve the work and its errors; later corrections take precedence. This is not a certification of the entire historical archive.

| Question | Supported result | Main limitation |
|---|---|---|
| Does the measured STMN2 event have support in GSE252892 KD libraries? | Canonical/cryptic counts: controls 1945/3, 2806/5, 2438/0; KD 253/727, 173/551, 140/556 | One WA01/H1 background; culture/differentiation independence and protein efficacy unverified; no donor-level validation or functional recovery |
| Can public junction counts measure the documented STMN2 event? | The retained junction is supported by literature and genome-chain checks; four cervical ALS libraries with ≥20 cryptic reads map to four donors | A local junction-use proxy, not a calibrated molecular fraction or functional assay |
| Does STMN2 differ between tissues from the same donor? | In 45 eligible ALS donor pairs: cervical higher/tied/lower in 24/14/7; median local-ratio difference +0.368 percentage points | Exploratory, same cohort; composition, batch, selection and unequal coverage remain unresolved |
| Is UNC13A coverage sufficient in the examined data? | Canonical junction coverage is about 22–26 times lower in cervical cord than motor cortex under five library-depth denominators | Unpaired descriptive comparison; the cryptic-read threshold was not reached; this does not exclude all public RNA-seq or greater depth |
| Does the published Keuss Fig.4d block model reproduce? | A [conditional R replay](reports/k26-conditional-replay-20261111/REPORT.md) gives a positive ASO contrast, p≈0.007 | Same data; two reduced-fit intervals include zero; published ASO star band not reproduced; strict metadata gate remains unmet |
| Was isolated UNC13A correction tested after a measured functional deficit? | In the six UNC13A-specific experiments inspected, treatment after a documented baseline deficit could not be established | Bounded documentary review; absent documentation does not establish absent deficit; multi-target row M-a has two rule readings |

Read [Current findings](docs/CURRENT_FINDINGS.md) for the qualifications, source links and closed/open boundaries. The [English guide](docs/ENGLISH_GUIDE.md) links seven translated reports, their original Spanish texts, scripts, outputs and source manifests.

## Minimal STMN2 replay

The [six-library reproduction guide](reproduction/stmn2-six-libraries/README.md) provides exact local FASTQ/index identities, a path-map template, an offline count/QC comparator and a supervised replay entry point for native Linux or verified C:-backed WSL2. It does not require historical host paths or failed-run directories. **Local FASTQ replay completed with exact agreement in 12 event counts and 30 QC fields**, according to the [audited supplied host records](reports/stmn2-real-replay-20261118/REPORT.md). The fresh worktree/environment reused the same PC and original inputs. A subsequent [independent-host technical pilot](reports/stmn2-hetzner-pilot-20261126/REPORT.md) reproduced all seven fixed fields for one control library on Hetzner, with verified cleanup. Portability of the other five libraries and independent biological replication remain untested. Checking archived JSON alone is not raw-data reproduction.

## Reproduce the software checks

From the repository root, using Python 3.11 or 3.12:

```sh
python -m pip install -r research/requirements-ci.txt
python scripts/run_offline_tests.py --fail-on-skip --report test-results/offline.json
python -m compileall -q scripts tests
```

CI runs the complete offline suite on both Python versions with pinned dependencies, requires zero skips, and uploads test/dependency reports. Inspect checks for the exact commit. **Passing software tests does not rerun every real-data analysis or establish biological validity.**

For real-data reproduction, follow the selected report's commands, exact input URLs/hashes, source-directory layout and analysis-specific dependencies. Large originals and mixed metadata workbooks are not committed. The [English guide](docs/ENGLISH_GUIDE.md#reproduction) explains the entry points and remaining prerequisites; the [script lifecycle inventory](research/SCRIPT_LIFECYCLE.md) remains in Spanish.

## Scope and next enabling inputs

The STMN2 cycle on these 45 donors is closed. More fits on the same donors are not independent replication. Further progress requires discriminating composition/QC evidence or an independent cohort with verified design and usable event coverage.

Issues [#37](https://github.com/luisceb1/ela-research/issues/37) and [#44](https://github.com/luisceb1/ela-research/issues/44) are closed; the underlying scientific questions remain conditional on usable independent data or design metadata. [#83](https://github.com/luisceb1/ela-research/pull/83) remains draft and paused. AD Workbench access is unverified and author inputs remain pending. See [Current findings](docs/CURRENT_FINDINGS.md#what-would-enable-further-work). No fresh external-access or mailbox check is implied by this documentation update.

## Documentation and provenance

New scientific documentation, public-facing documentation and new code comments/docstrings are written in English. Spanish originals, internal working material and the historical archive remain available. The English reports are dated translations with pinned source hashes, not new analyses; [language policy and translation review](docs/ENGLISH_GUIDE.md#translation-policy-and-review) explains their status and how corrections propagate.

For agent operations, read [AGENTS](AGENTS.md), [STATE](research/STATE.md), [BACKLOG](research/BACKLOG.md), [PROTOCOL](research/PROTOCOL.md) and [MASTER_EVIDENCE](research/MASTER_EVIDENCE.md). These operational/historical files may contain superseded dated sections; the current findings page identifies the reviewed scientific baseline. New communications, spending, personal-data handling, laboratory work and clinical instructions require the applicable explicit authorization.
