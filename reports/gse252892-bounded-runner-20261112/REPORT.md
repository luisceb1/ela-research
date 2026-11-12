# Bounded GSE252892 local executor — 12 November 2026

## Evidence and scope

Luis's [terminal evidence](user-software-setup.json) confirms fastp 0.23.4 installation, in addition to previously reported Python 3.12.3/PySAM 0.23.3 and HISAT2 2.2.3. The prior disabled base descriptor was prepared on his host, SHA256 `97a578839d72088bab1403b0c9ef6bd9b8e3ff064bbe3008314fb34545b6af26`; its full bytes have not been read on the agent host. The new preparer reads/rechecks that exact file on Luis's computer. No direct computer access, FASTQ acquisition or biological counting occurred on the agent host.

Prospective specification: [plan](../../research/plans/2026-11-12-gse252892-bounded-execution.md), committed as `bc4b041cce0c94d0f45a6bde3bb2eecb992b98bd` before executor implementation/raw acquisition. This is a separately reviewable extension stacked on unmerged PR #76. It does not merge or reopen #37/#44/STMN2.

## Implemented sequence and limits

The new executor has separate **prepare** and **execute** actions. Preparation verifies the exact base descriptor, selected inputs, clean code commit, current index sizes/hashes, Python/PySAM, tool hashes and required CLI options, sealed targets, exact command construction and actual Windows C: free bytes through WSL interop. It writes a new execution proposal outside the checkout and transfers no raw data. No descriptor/root is overwritten.

Execution requires the explicit accepted proposal SHA256 and **14,000,000,000** transfer-byte cap, plus a new root and one-time claim. A separate process-group supervisor applies:

| Resource | Proposed bound / mechanism |
|---|---|
| Raw inputs | Four pinned FASTQs advertise **12,826,593,031 bytes**; **14 GB** cap for application-read response bodies, no retry/redirect/mirror/resume |
| CPU | Inherited affinity to at most two logical CPUs; fastp/HISAT2 two threads |
| Memory | Per-process 8 GiB address-space limit; process-group RSS sampled at 6 GiB maximum |
| Disk | New run-root sampled at 100 GiB maximum; physical Windows C: free reserve 50 GiB |
| Wall clock | 12 hours of supervised worker execution, then group termination |
| Failures | Partial files, raw inputs, logs, claim and receipts retained; known successful plain intermediates removed after counting |

The control library GSM8009878/SRR27477544 is acquired/preprocessed/aligned first. KD GSM8009881/SRR27477541 is acquired only if control canonical support is >0. A control failure, failed MD5/size/gzip signature, processing error or resource violation stops the attempt. Successful control measurement does not guarantee KD support or assay specificity. Completed individual library counts are separate; no replacement or analysis expansion follows a failure.

Transfer receipts distinguish observed application-read bytes from a conservative in-flight read reservation, so forced termination need not be misreported as an exact zero-byte remainder. The cap is not a packet/TCP/TLS overhead measurement. RSS/disk are sampled and can overshoot between checks; they are not hard aggregate kernel quotas. Hardware shutdown, supervisor death, process escape and uninterruptible I/O are not claimed fully controllable. No retry/new window is automatic; a consumed descriptor cannot be reused as a resume token.

## Processing and count interpretation

GEO RNA-seq processing describes fastp adapter removal followed by STAR/ENCODE mapping; the 3'-end assay is excluded. This pipeline uses paired adapter detection with fastp 0.23.4 and its fixed-version filtering defaults, with duplication evaluation disabled but no molecular deduplication. Exact author fastp arguments are unknown. HISAT2 native 2.2.3 replaces STAR using the prospective genome-wide command, without target-directed mapping or assumed library strandness. CLI option names were checked against the pinned [fastp source](https://github.com/OpenGene/fastp/blob/v0.23.4/src/main.cpp); installed CLI help is also checked before any raw transfer. Differences from the author pipeline remain explicit.

The primary count is a **contiguous paired query group/event/library**, not RNA molecules, donors or a calibrated splicing fraction. Both unique primary/proper mates must meet fixed NH/MAPQ/mate-link checks; exact CIGAR N intervals match the unchanged sealed hg38 targets, with XS minus and adjacent aligned anchors >=15. Eligible mates are unioned per group/event, preventing double-counting both mates on one junction. Ambiguous groups are excluded/tallied; marked duplicates are counted, not claimed independent. The SAM chr19 reference length is checked before parsing support. --reorder does not establish global query-name uniqueness or PCR/UMI deduplication.

Canonical support >0 is the measurement-control rule. The separately labelled >=20-group support diagnostic is not silently equated to recount3 read support or an inferential gate; canonical counts do not bound cryptic counts. No cryptic sum, PSI, KD/control effect, p-value, biological independence, functional recovery or clinical benefit is calculated. A partial execution has no completed overall coverage verdict. Neither lower support nor process failure proves biological absence or isolates sequencing depth as cause.

## Software validation and remaining evidence

[Focused tests](focused-tests.json): **37/37 pass, no skips**, Python 3.12.14/PySAM 0.23.3 on agent host. Coverage includes accepted-file checksums/charges, error/partial-body accounting, overflow/header rejection, no retry/overwrite/redirect, anchor/strand/NH/MAPQ/mate criteria, paired-support deduplication, PySAM half-open intron agreement, low canonical/high cryptic possibility, physical-reserve/symlink/acceptance guards, actual fixture process-group stopping/wall timeout and control-failure suppression of KD. [Artifact hashes](artifact-hashes.json) bind the executor and unchanged measurement inputs. Python compilation and Markdown/diff checks are performed. Full offline CI must be read at the final head; an earlier green run is not attributed to this code.

All reads, responses and subprocesses used in these tests are software fixtures. There is **no positive full human-index/fastp/HISAT2 execution, measured local performance or biological reproduction** here. This executor is reviewed/tested software for an explicitly bounded attempt, not validated experimental evidence. Live ENA availability/raw checksums, actual resource use, query-name assumptions and the complete processing path will only be assessed if the concrete proposal is approved and run. The failure ledger is a result to retain, not a reason to loosen the envelope.

## Next step and stopping boundary

Follow the [preparation-only runbook](../../research/runbooks/2026-11-12-gse252892-bounded-execution.md) at the exact reviewed commit, and report the resulting proposal hash/resource summary. It uses the existing environment; no new packages or FASTQ are acquired by preparation. Review the concrete proposal before accepting its SHA/14 GB cap. No execute invocation or transfer authorization is inferred from installing fastp, preparing either descriptor, passing tests or this PR. Do not reuse the old pilot or edit its ledger/descriptor. No contact, cost, auto merge or public experimental claim is authorized.
