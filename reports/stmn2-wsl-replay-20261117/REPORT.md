# WSL2 replay admission extension — 17 November 2026

## Evidence

Luis's terminal output located all twelve named FASTQs, the hg38 index and fastp
0.23.4 / hisat2-align-s 2.2.3 in `Ubuntu-24.04`, rather than the default `Ubuntu`.
Python 3.12.3 and PySAM 0.23.3 were reported in a dedicated environment. These
are supplied host observations; the actual FASTQ/index hashes remain unverified
by this preparation. No real replay was performed here.

The [prospective extension](../../research/plans/2026-11-17-stmn2-wsl-replay.md)
adds plan-bound WSL2 registry/VHD identity, root-ext4 output admission, 150 GiB
guest/physical-C: admission and a 50 GiB reserve on each during supervision.
WSL admission also requires 7 GiB available guest RAM. Physical C: telemetry uses
the existing verified drvfs helper; inability to read it fails closed. The
supervision record retains its minimum sampled successful observation; a failed
check is recorded as a failure rather than successful execution.

## Interpretation

This permits a bounded attempt on the reported machine after real host admission
and exact raw/index hashing. It changes neither scientific targets/counter nor
preprocessing/alignment options, library order, expected counts or QC totals.
The offline comparison remains `records_match` for all six archived libraries,
with `raw_replay_verified: false`. A v2 plan binds the new host modules and host
identity; old v1 plans cannot silently opt into the new execution environment.

## Validation

Software fixtures test registry/mount/identity refusals, missing/malformed/failed
interop, insufficient host space/RAM, changed host bindings, and supervisor
termination on lost host telemetry. Existing synthetic subprocess measurement
and historical-command equivalence controls still pass. Full offline-suite
results are recorded in `validation.json`.

## Limitations and next step

PowerShell registry/VHD checks have not been executed on a real Windows host in
this preparation. Mocked JSON does not validate Windows behavior. `check-host`
is the next real-host check and performs no alignment, raw download or output
creation. A successful result still requires `prepare` with exact local inputs.

Only C:-backed WSL2 root ext4 is supported. Reparse points/other host drives are
refused. Available RAM is an admission observation, not reserved memory. Host
concurrency and VHD allocation can outrun 0.5 s sampling; this is not a hard
aggregate quota, authenticated attestation or network isolation. No raw file or
old run is deleted. No biological replication, functional rescue, new finding,
#83 execution, outreach or cloud spend is added.
