Current status: the original user metadata ZIP has now been received and verified; see [executed audit](../gse252892-audit-verification-20261114/REPORT.md). Earlier pending-archive statements below describe the prior stage. No raw-data replay was performed.

# Metadata audit package — 14 November 2026

The bounded two-library measurement is closed with [106/0/0 and 41/0/3](../gse252892-local-result-20261114/REPORT.md). Luis authorized preserving the original audit metadata before cleanup. No new analysis, transfer, raw-data replay, cleanup or merge.

The new offline `scripts/package_gse252892_audit.py` requires the exact completed host proposal SHA61c5f2c73e762ed23d9c940ce7db2b3043713169311e4594d8f87e51d0332369, completed clean supervision, final transfer accounting <=14 GB/no active requests and actual result/per-library JSON agreement with the transcribed result. It follows the recorded lineage for the six roots and consumed plans/claims; all source proposal SHAs, base descriptor hash and claims are checked.

Explicit metadata allowlist only: source plans/claims/base descriptor, accepted/supervision/ledger/progress/result/failure receipts, worker/index logs, per-library fastp JSON/log and HISAT2 logs/summaries/counts, recorded verified-input JSON and transport JSON receipts from all six attempts. No recursive sequencing-file sweep and no FASTQ, trimmed FASTQ, SAM/BAM, index, range/partial input, or HTML inclusion. Original inputs are neither opened nor rehashed by this packaging script. Recorded input hashes are provenance claims, not fresh FASTQ verification.

Per-file metadata cap5 MiB; combined payload50 MiB and <10,000 members. Refuse source symlinks, missing required root receipts, oversized metadata, changed counts/claims/plans or existing archive/partial output. In-memory payload is bounded. Archive MANIFEST lists original absolute source paths, ZIP member paths, byte sizes and SHA256. ZIP is verified by reading all members against the manifest, published without overwriting an existing output, and verified again. An interrupted/failed archive is not labelled successful; partial evidence is retained. No source deletion/mutation. Archive source-path metadata is expected to identify Luis's local run locations.

[Tests](focused-tests.json): ten packaging regressions and six prior lineage/scientific-function controls pass, no failures/errors/skips. Checks cover raw/alignment exclusion, exact metadata/source preservation, digest verification/corruption, inconsistent result/claim rejection, symlinks, size caps and no overwrite. Python compile/diff/link checks pass. Full CI is checked separately on the published head. This is software-fixture verification, not an archive actually generated from the user host.

## User-host step

Fetch/check out the reviewed commit; no runtime or plan execution is involved. Run:

```powershell
wsl -d Ubuntu-24.04 -- /home/luisceb/proyectos/ela-research-piloto/.venv/bin/python /home/luisceb/proyectos/ela-local-20261112/scripts/package_gse252892_audit.py --plan /home/luisceb/ela-gse252892-interrupt-execution-20261113.json --output /mnt/c/Users/Luis/ela-auditoria-run06.zip
```

Output is `C:\Users\Luis\ela-auditoria-run06.zip`. A successful summary reports metadata_archive_verified, ZIP size/SHA256, member count, zero raw inputs/source deletions, and the actual final transfer ledger. Upload that ZIP for independent inspection of the original metadata bytes. Until received, the original-host archive remains pending; do not clean up the raw files or claim the agent has verified them. No publication/contact/cost/merge.
