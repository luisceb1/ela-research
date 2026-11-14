# Prospective transport recovery amendment — 13 November 2026

Parent: `66eb85865719bde68397fa48bc7cfbb26cda5fbc` / PR #77. Luis authorized substantial local transfers/CPU within host capacity. This is a new, separately sealed attempt, not a mutation/resume of the consumed v1 proposal. No cloud spending, contact or merge is authorized. Commit before any new live range request; agent-side validation uses fixtures only.

## Recorded failure and unchanged science

The user ledger reports HTTP 200 followed by EOF after 351,927,726 of 2,772,553,416 advertised bytes in the first control FASTQ. Prefix SHA256 ee7762da8dc57e0ab9878fbf449cb7f933fd7f95c6a32c4e93be5dc2c3c5d2aa. The failure is an incomplete response; its underlying network/server cause is unknown. At 2,098.952 s the worker failed, peak sampled RSS 38,105,088 bytes; no fastp/alignment or biological result was reached. Preserve all failed roots, claims, receipts and bytes, including this negative outcome.

Same two libraries, four URLs, published lengths/MD5, reference/targets, fastp/HISAT2 commands, fragment/event unit, anchor 15, filters and diagnostics as the prior specification. Control first and KD only if control canonical >0. No new effect, PSI, p-value, replacement sample or reinterpretation of low coverage.

## Fixed transport

Use exact-origin HTTPS single byte-range requests (RFC 9110), 32 MiB blocks, at most four simultaneous connections per file, 120 s socket timeout, at most three attempts per block with 2/10 s backoff. Retry only short/failed network reads, transient connection errors and HTTP 408/429/500/502/503/504. No retry for changed object metadata, wrong ranges, ignored Range (200), TLS certificate failures, corrupt prefix, full MD5 mismatch, local I/O or resource limits. No redirects, mirrors or full-file fallback. Require HTTP 206, exact Content-Range endpoints/total and exact Content-Length for every requested block. Record validators and use a strong ETag/If-Range if supplied; changed validators fail. Actual support by ENA is unknown until user-host execution; do not infer it from this specification.

Reuse the old prefix only after matching the prior consumed proposal SHA911c5be6f8a470d085ab57279ee8d3ce40bb31edcb990a3064238d9c4b9d9a9f, failed-cleanup receipts, ledger URL/length, on-disk prefix length and SHA256. Verify a remote overlap of the last 1 MiB (or whole shorter prefix) before requesting the suffix. Preserve the old file; assemble into a new root. If no old prefix applies, obtain the first block serially before parallel requests. Assembly order is fixed by byte offset; verify each block's local digest/size again and the complete FASTQ's original MD5/length/gzip signature before promotion. Only after that may fastp read it. No partial prefix/chunk becomes a biological input. A failed range attempt is retained; a successful full-file promotion may remove its successful temporary chunks, retaining receipts and full compressed input.

## Budgets and accounting

Keep the **14,000,000,000-byte lineage cap including the 351,927,726 bytes already consumed**. Retries and the overlap consume the same remaining budget; no resetting old charges. Distinguish observed bytes from conservative charges/in-flight reservations under a thread-safe ledger; reserve before reads, charge unknown read tails conservatively. Each attempt has its own receipt and digest; a bounded-size aggregate ledger exposes current totals for supervision. Protocol headers/TLS overhead are not represented as raw-body bytes. Fail on cap exhaustion and retain the incomplete result.

New fixed wall window **48 h** for this new attempt, selected prospectively after measured slow transport, not after biological results. Same two CPU affinity, per-process AS 8 GiB, sampled process-group RSS 6 GiB, 100 GiB combined old/new roots and real C: reserve 50 GiB. Preserve sampled-quota/uninterruptible-I/O limitations. No automatic continuation beyond the new window or restart after the new descriptor is consumed. No performance promise; four connections need not improve throughput.

## Acceptance and stop

Prepare a new proposal without HTTP, binding current code/tools, original disabled base descriptor, old plan/root/receipt hashes, validated prefix, fixed transport settings/caps and a new root/output. Live execution requires the new proposal SHA acceptance; prior local-resource permission persists. Test range/header/status, overlap, ordering, MD5, retries, concurrent-budget reservations/unknown tails, old-prefix immutability and unchanged scientific operations with fixtures. Report live failure separately from software-test success. Stop at first fatal integrity/design/resource failure, exhausted retry allowance, failed control or both complete libraries. No additional candidates or clinical claims.
