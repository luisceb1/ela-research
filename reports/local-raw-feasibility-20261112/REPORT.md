# Local raw-RNA-seq feasibility inventory — 12 November 2026

## Decision

**Prefer GSE252892 for preparation of a bounded local measurement workflow, conditionally.** It has the simpler inspected total-RNA assay and a smaller fixed input set. This is not acceptance for a KD effect, independent-donor validation or raw execution. No FASTQ was downloaded. GSE299341 remains unselected: processing/efficacy details are less resolved and one selected library has unexpectedly tiny published files. Do not silently discard it, replace it or reinterpret it as a biological zero.

Protocol committed before the new metadata requests: `05703d659fb7e51a29bc1276efcbb91f126b9dd8`, [plan](../../research/plans/2026-11-12-local-raw-feasibility.md). This re-examines previously known candidates through a different access route, not a new discovery screen. The earlier recount3 unavailability result stands.

## Exact input costs and source decisions

| Source | Fixed selected subset | Nominal design | ENA FASTQ metadata | Decision/limits |
|---|---|---|---|---|
| GSE252892 / SRP482832 / PRJNA1063175 | Six total-RNA libraries, GSM8009878–GSM8009883; exclude 3'-end assay | WA01/H1, NGN2 neurons; shControl 3, shTDP-43 3 | 6 runs, **12 files**, **40,589,186,698 compressed bytes** (40.59 GB decimal) | Preferred for preparation. Primary methods specify stranded total RNA, 75-bp paired-end; Fig.1c documents an assay-level western-blot KD check, n=3 per arm. No numeric depletion efficacy linked to each sequenced library or independently verified culture/differentiation nesting established. One genetic background, not three donors. |
| GSE299341 / SRP590954 / PRJNA1273942 | Ten fixed soma libraries; exclude neurites/other RBP arms | WTC11, CRISPRi; nominal control 5, KD 5 | 20 runs, **40 files**, **86,561,386,307 compressed bytes** (86.56 GB decimal) | Not selected. Two run accessions per GSM are not independent cultures and do not themselves identify the technical relationship. UMI processing and numeric efficacy remain uncertified because primary full methods were not successfully read in the prior cycle. |

These are archive-advertised compressed sizes/checksums, not bytes independently downloaded and hashed by us. [FASTQ manifest](fastq-manifest.tsv) includes each exact file URL, MD5, size, run/SRX/GSM and declared treatment title; [summary](summary.json) aggregates these fields only. No whole-project data from unrelated arms is included in those totals. FASTQ URLs were not probed or downloaded; future accessibility and raw checksum agreement remain untested.

**GSE299341 anomaly:** GSM9037617 maps to SRX29112933, runs SRR33905369/370. ENA reports read_count fields of 1,791 and 1,728 and four FASTQ files totalling **358,774 compressed bytes**, much smaller than the other selected libraries. These are metadata values, not new measured read counts. No cause is assigned and no inference about target coverage follows.

## Provenance and independence

All 16 GSM-to-SRX links were rechecked offline against the original cached Stage A GEO response bytes; their SHA256 values match the committed inventory. [Linkage evidence](geo-linkage.json) records source URLs/hashes. Fresh ENA metadata supplies the associated run/files. Two response bodies and [receipts](retrievals.json) are preserved: **36,284 bytes**, within 2 MB and four-attempt caps; no failed attempts, count downloads, FASTQ transfer, contact or cost.

The earlier primary XML cache for [PMC12586192](https://pmc.ncbi.nlm.nih.gov/articles/PMC12586192/) was read at the methods/Fig.1c/data-availability locators; [source hash and limits](primary-review.json) distinguish that reuse from this cycle's two fresh ENA requests. The paper includes reused external datasets too; only its new in-house GSE252892 observations are considered here. Separate experiment/accession is not sufficient proof of independent biological units or all upstream sample non-overlap. Previous single-background/donor and assay restrictions are not reclassified as satisfied.

## User-reported host readiness

Ubuntu-24.04 WSL2: Python 3.12.3, HISAT2 align/inspect 2.2.3 execute; PySAM 0.23.3 is installed. The historical checkout has detached HEAD and no listed changes. Eight hg38 index members plus make script are present, about 4.4 GiB. This confirms reported presence/version behaviour, not current index integrity or reference compatibility. No remote access to Luis's filesystem is claimed.

Windows: 15.8 GiB physical RAM, 564.9 GiB free C:, i5-12400 6 cores/12 threads. WSL sees 7.6 GiB RAM and about 7 GiB available with 2 GiB swap. Its displayed virtual disk capacity does not increase physical free C: capacity. No runtime, peak RAM or achievable junction coverage is benchmarked here.

## Concrete next preparation, without execution

Use GSE252892's first declared control and first declared KD as the provisional two-library input for a technical/resource demonstration: **GSM8009878/SRR27477544** and **GSM8009881/SRR27477541**. They are selected by the existing replicate label order, not observed coverage. They are not asserted to be matched biological cultures. The four advertised paired FASTQs total **12,826,593,031 bytes** (12.83 GB decimal). This is a transfer-size proposal, **not authorization or an executable download plan**; no more libraries are nominated automatically.

Before any transfer: seal exact index/target/tool hashes and current checkout; review strand/adapter/assay handling; build a separate runner with explicit transfer, disk and wall-clock budgets, cleanup and retained failure receipts. A runtime/memory trial would need a fixed bounded subset after raw execution approval; it cannot establish full-library coverage. Existing old CTRL-4/TDP-5 plans are not reused. The full six-library experiment would cost 40.59 GB of compressed inputs, excluding any temporary/index/output space; a full inferential analysis remains outside this task.

The proposed endpoint is each sealed UNC13A junction count separately, with canonical control; no PSI, KD/control effect, p-value or pooling. No guarantee of cryptic support follows from library-wide read metadata, and the canonical count is not a cryptic upper bound. Maintain #37/#44/STMN2 closures, no restored functional-recovery claim, and no widening after failure.

## Reproduction and validation

```sh
# Derive from the committed ENA responses; no network by default.
python reports/local-raw-feasibility-20261112/inventory.py
```

The opt-in metadata acquisition mode refuses an existing ledger; it is not a FASTQ downloader. [Validation](VALIDATION.json) checks response sizes/hashes, 16 source links, 52 distinct file URLs and checksums, source totals and the proposed two-library sum. No raw checksum, biological effect or local performance was validated. Stop this inventory after the two fixed decisions; no third source or new primary route is pursued.


## Subsequent offline preparation — user hash check

Luis supplied SHA256 values for all eight index members and the build script; **9/9 match** the historical verified-index record. [Recorded comparison](user-index-check.json) is user-reported terminal evidence, not direct host inspection. The files need not be restored on the strength of this result.

A new standard-library-only preparer, `scripts/prepare_gse252892_local.py`, validates the four fixed manifest entries, clean checkout, index sizes/hashes, local binary versions/hashes, existing PySAM 0.23.3 and sealed target hash before writing a new descriptor outside the checkout. It refuses overwrites and has no network/download/alignment or execute path. Output explicitly remains `prepared_disabled`; the old pilot cannot be enabled with this descriptor. Seven [focused controls](preparer-tests.json) pass; tests use software fixtures and do not run a human index/alignment on the agent host. Full positive host preparation remains pending Luis's run. This does not implement or validate the eventual raw runner/resource controls.


## Host preparation completed; preprocessing prerequisite

Luis ran the pinned preparer at `4fa5346` successfully on Ubuntu-24.04, using the existing Python 3.12.3/PySAM environment. The [user-supplied terminal summary](user-prepared-summary.json) reports `prepared_disabled`, 9 index members verified, 4 FASTQ entries, zero raw bytes transferred and descriptor SHA256 `97a578839d72088bab1403b0c9ef6bd9b8e3ff064bbe3008314fb34545b6af26`. The agent has not read the full descriptor bytes or independently rehashed it. This supersedes the pending-positive-preparation statement above, not any resource/assay/runner gate.

The cached primary GEO GSM8009878 processing record (hash in geo-linkage.json) says RNA-seq adapters were removed with fastp, then STAR/ENCODE mapping and uniquely mapped properly paired reads were used for splicing. It separately describes the 3'-end assay, which remains excluded. Exact author fastp parameters/version are not recovered from that record; defaults must not be silently called equivalent. A subsequent HISAT2 measurement would differ from the author STAR pipeline. Adapter preprocessing and explicit read/junction filtering require a prospective execution specification before raw processing.

Ubuntu's official Noble package record lists fastp 0.23.4+dfsg-1: https://packages.ubuntu.com/en/noble/fastp (checked 12 November 2026). The next local setup step is installing/recording that package, not downloading FASTQ. No installation or performance on Luis's computer is claimed yet.
