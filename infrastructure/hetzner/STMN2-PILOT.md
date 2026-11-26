# One-library independent-host technical replay

Prospective decision, 26 November 2026. The GSE304550 original counter
could not be located; the SRA file is retained locally. For the first real
cloud test, select the pre-existing, fully documented control GSM8009878
(SRR27477544) from GSE252892. The previously recorded counts and five QC
fields are the locked reference in reproduction/stmn2-six-libraries/manifest.json.
Use the smallest compressed input pair in that manifest (5.69 GB).

Question: does the original procedure reproduce all seven numerical fields
on an independent Ubuntu 24.04 host using identical input and index hashes?
If it does, the original workflow is technically portable on this host.
If it does not, retain the discrepancy without tuning thresholds or tools.
An incomplete transfer, hash mismatch, timeout or insufficient resources is
a failed execution, not a biological result. No new biological contrast.

The pilot reuses the original commands and single-library measurement
function without modifying the six-library local executor or its manifest.
The native HISAT2 2.2.3 source archive and hg38 archive must match their
recorded source hashes; fastp 0.23.4 and PySAM 0.23.3 are fixed and actual
binary hashes are recorded. A different build is identified as such.
Use the original two CPU slots and 8 GiB per-process address-space limit.
Do not run another library or change thresholds if the comparison fails.

The original input files are retained locally. The transient cloud copies
are discarded with the disposable server after recovering the evidence.
Only public-source aggregate counts, QC, commands and logs are included
in the GitHub artifact; no raw reads, individual-level source records,
BAMs, or credentials are uploaded.

Resource decision: one CCX33 at Nuremberg, gross rate plus IPv4 about
EUR 0.269/hour. Three-hour expiry, controller timeout 140 minutes and
workflow timeout 155 minutes, leaving room for retrieval and cleanup.
Expected maximum three-hour compute cost about EUR 0.81, excluding
unexpected provider/scheduler delays. The independent expiry check is
best effort rather than a provider-enforced monetary cap. No automatic
retry or next library. Verify no resources remain in Hetzner.

This is a technical replay of known measurements, not independent biological
replication, a functional experiment, or new clinical evidence.
