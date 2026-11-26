# PRJDB19918 two-library technical pilot closure — 26 November 2026

**Technical execution succeeded; descriptive cryptic support was insufficient.** This is not independent biological replication. The [prospective decision and authorization](PILOT_DECISION.md) fixed two libraries before inspecting their outcomes.

## Evidence

[Actions run 45812661932](https://github.com/luisceb1/ela-research/actions/runs/45812661932), commit `8afb8b4627e86868ef58db7f1690676db7ce0566`, completed successfully. All four jobs passed: pilot-control, verify-control, pilot-kd and verify-cleanup. Both ZIP archives passed integrity checks and match the GitHub-published SHA-256 digests. Their original bytes are retained privately; [evidence receipt](pilot_closure.json) records aggregate results and member digests, not raw reads or credentials.

| Field | Control DRR631712 | KD DRR631715 |
|---|---:|---:|
| Canonical | 79 | 56 |
| Cryptic left | 0 | 2 |
| Cryptic right | 0 | 0 |
| SAM records | 105,763,652 | 94,041,900 |
| Alignment groups | 49,746,599 | 44,355,379 |
| Eligible groups | 46,611,372 | 41,689,808 |
| Marked duplicate records | 0 | 0 |
| Rejected groups | 3,135,227 | 2,665,571 |

Both canonical controls are positive. Neither cryptic edge reaches the prespecified descriptive 20-group diagnostic in either library. The four input receipts match the locked ENA MD5s and byte lengths in the [manifest](input_manifest.json); observed SHA-256 values are retained. Both result records reconcile with their QC accounting and execution-commit identity. The rebuilt aligner digest differs from the historical build and between these hosts; fastp matches the historical digest. The audit verifies the archived execution receipts, not a separate rehash of raw reads or the deleted host's index.

## Runtime, cost and cleanup

- Workflow: 11:40:14–14:15:11 UTC (2 h 34 min 57 s).
- Internal runtime: control 4,930.187 s; KD 4,161.208 s.
- Confirmed combined gross rate: EUR 0.269467/h (including IPv4). Estimated EUR 0.70 prorated over workflow elapsed time, or EUR 1.08 assuming two billable hours per server. Not an invoice.
- Independent cleanup confirmations at 13:04:13.586 and 14:15:08.840 UTC. Logs state no matching pilot resources remain; not a whole-project resource inventory.
- [Control artifact](https://github.com/luisceb1/ela-research/actions/runs/45812661932/artifacts/15118864732), [KD artifact](https://github.com/luisceb1/ela-research/actions/runs/45812661932/artifacts/15127440808), both expire 3 December 2026; original ZIPs retained before expiry.

## Interpretation and decision

Low observed support does not establish biological absence, a treatment effect, a causal mechanism, or therapeutic efficacy. The two libraries are not a verified biological pair. Sample/culture independence is still unresolved, and the author supplement schema was not recovered. Close the two-library pilot as a completed technical task with insufficient coverage for the intended comparison. Do not automatically process the remaining seven, lower the diagnostic threshold, or retry the workflow. The previously authorized budget does not grant new execution scope.

Next input: concrete documented independent units and usable source evidence. Preserve the existing observations and their limits for an integrated scientific review. No new execution, contact or expenditure is scheduled by this closure.
