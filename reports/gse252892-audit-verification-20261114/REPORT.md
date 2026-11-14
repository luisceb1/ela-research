# Original metadata archive verification — 14 November 2026

## Evidence verified

Received user attachment `ela-auditoria-run06.zip`: **1,091,994 bytes**, SHA256 **c8751b9610512791ba40a613449ad332833ff557e8c371f96e118636361e4617**, matching the host-generated summary. Persistent user attachment ID: libfile_1f3753ca54d08191b8f826b6702a91c4. No raw sequencing files were uploaded. Archive contains 1,463 metadata members plus MANIFEST.json, metadata payload 1,959,447 bytes. Every member length/SHA256 matches the manifest, names are unique/safe, ZIP CRC checks pass on read and no raw/trimmed FASTQ, SAM/BAM, index or partial input member is included.

The [executed verification script](../../scripts/verify_gse252892_audit.py) produced the [full verification record](verification.json). It verifies seven actual proposal/base descriptors, consumed claims, 41 recorded runtime code hashes against their exact repository commits, and 557 distinct embedded original-file bindings. All pass. This is computational inspection of original supplied metadata, not a third-party review or a second biological experiment.

Across six attempts, per-request observations/charges reconcile with aggregate ledgers and prior charges. The interrupted run03 durable ID232 is deduplicated against its stale active snapshot; ID233's 1 MiB reservation remains charged. Run05 interruption has zero new transfer. Run06 has 863/863 settled requests, zero active. Final **13,006,020,409 observed versus 13,007,068,985 conservative charged bytes**, below 14 GB; difference 1,048,576 is retained uncertainty, not newly observed data. Earlier failures remain in the archive and verification record.

## Counts and QC confirmed from original files

Original archive result equals the previously transcribed result exactly; original supervision also equals the prior transcription. Per-library count JSON agrees with aggregate. Original fastp passed-filter counts equal twice the paired-read totals in HISAT2 summaries; eligible+rejected groups equal alignment groups. Four complete-input receipts match the fixed input manifest's published lengths/MD5 and include recorded SHA256s. These input hashes were **not recomputed on FASTQs by the agent**; archive verification does not prove the current integrity of raw files on the user host.

| Library | Canonical | Cryptic left | Cryptic right |
|---|---:|---:|---:|
| Control GSM8009878 | 106 | 0 | 0 |
| TDP-43 KD GSM8009881 | 41 | 0 | 3 |

Counts are eligible paired query-groups/event, anchor15. No count changes, new models/ratios/PSI, threshold changes or raw re-analysis. Neither cryptic event meets the fixed 20-group descriptive diagnostic. Preserve three KD right-junction groups; observed zero is not biological absence. One library/condition/single background cannot establish an inferential KD effect, donor generalization, functional recovery or clinical benefit. The [bounded measurement closure](../gse252892-local-result-20261114/REPORT.md) stands.

## Archival and cleanup boundary

The archival-verification task is complete for the supplied metadata. Selected exact original result/supervision/ledger/library-count/mapping files are retained in [original/](original/); all original metadata remain in the uploaded ZIP identified by SHA256 above. Do not equate these preserved bytes with the historical user transcriptions; equality was explicitly checked. The archive and report preserve runtime commits/input URLs and hashes needed for a future independently authorized replay.

No user-host files were deleted, moved or modified. Keep the ZIP and its SHA256 in a separate backup, and keep original compressed FASTQs/reference index unless a separate retention decision is made. Before cleanup, inspect actual host file sizes; candidate disposable intermediates are interrupted run04/run05 plain trimmed FASTQs, never count/QC logs, plans/claims, the ZIP, compressed raw inputs or the reference index. No deletion command is authorized or executed here. No cloud spend, contacts, merge or reopened scientific cycle.
