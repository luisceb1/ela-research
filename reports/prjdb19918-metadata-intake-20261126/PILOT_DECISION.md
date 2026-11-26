# Provisional remote pilot decision (not executable authorization)

Question: is the fixed UNC13A measurement technically feasible in the Tanaka short-read data, assuming scientific admission remains pending? This is distinct from the original independent-replication question. A finding of adequate or inadequate support would help decide whether a larger computation is worth considering, but cannot resolve culture independence.

## Fixed selection before reading outcomes

The minimum advertised compressed FASTQ pair within each condition is selected to limit resource use. No biological outcome was inspected to select the runs.

| Run | Label | Compressed bytes |
|---|---|---:|
| DRR631712 | SCR2 | 5,482,638,623 |
| DRR631715 | KD1 | 4,867,330,852 |

Total: 10,349,969,475 bytes. This is not a biological pair. Exact input URLs, sizes and MD5s are in [input manifest](input_manifest.json).

## Conditions for execution

- Either the originally requested independent-unit and source admission criteria are met, or the user explicitly approves the revised **technical-only** coverage scope.
- Pin a reviewed reference/event definition, counter implementation, tool/index hashes and QC before execution. Validate with existing offline software checks and a synthetic technical fixture before enabling a workflow.
- Use at most two sequential disposable server leases, maximum three hours per library, with current gross server and IPv4 rate verification, strict input identity checks, bounded execution, evidence retrieval and independent cleanup checks. No automatic retries or additional library. Record actual cost if available, otherwise label estimated cost.
- At the historical server rate of EUR 0.268499/h, six nominal hours cost EUR 1.61 plus IPv4. A proposed two-euro pilot allocation is an estimate, not a provider-enforced hard cap. The wider EUR 10 objective remains available only for authorized phases. Do not run if rate, capacity or cleanup controls cannot be verified.
- A low or missing measurement is a technical/coverage outcome, not biological absence. Do not infer a treatment effect or extend to the seven remaining libraries automatically.

No Hetzner execution has been dispatched. The existing validated disposable lifecycle is retained; the new measurement pipeline has not yet been enabled.

## Operator authorization and execution implementation — 26 November 2026

Luis expressly approved the technical-only alternative after being told the biological-unit gate remains pending. The pilot is limited to the two prespecified libraries, not the remaining seven. The new workflow uses the already-tested disposable lifecycle and exact existing UNC13A counter, validates the sealed manifest, mate MD5/length and observed SHA-256, index and software identity. It requires the combined EUR gross server + IPv4 hourly rate to be no more than EUR 0.32 (six nominal lease hours no more than EUR 1.92; not a hard provider cap). Each library has its own three-hour expiry and 138-minute remote timeout, with separate independent deletion verification. The second runs only if the first and its cleanup succeed. Zero canonical support stops automatic continuation; cryptic support is descriptive only. No retry, biological effect, or automatic extension. The single launch marker is activated only by addition on main; PR checks cannot provision a server. The run and actual cost/evidence will be reported separately.
