# Probe project-label fix — 12 November 2026

Code correction required by the [Question A plan](../../research/plans/2026-11-12-questionA-measurement-reproducibility.md) before any new measurement. **No recount3 file was downloaded, no coverage was measured and no candidate was inspected.** This is a labelling fix; no recorded count, threshold or gate outcome changes.

## Defect

`scripts/recount3_junction_probe.py` set the output project from the targets file:

```python
"project": spec.get("project", ""),
```

`research/references/unc13a_targets_sealed.json` carries `"project": "SRP166282"` as provenance for the sealed coordinates. Measurement never used that field — targets come from `spec["junctions"]` and `spec["chromosome"]` — but it was copied into every result. Run unchanged against a different project, the output would have claimed `"project": "SRP166282"`, labelling new counts with the accession of the already-rejected Klim dataset.

No published result is known to be wrong because of this: both existing result files name the project they report. But `reports/recount3-unc13a-20261111/results_SRP334561.json` reports `"project": "SRP334561"`, which the current sealed file cannot produce, and how that run was labelled remains **unexplained**. **Resolved 12 November 2026** in [the loose-ends report](../loose-ends-resolved-20261112/REPORT.md): the sealed file has exactly two commits and both carry `SRP166282`, and no second UNC13A targets file was ever committed, so the **committed seal was never broken** and the speculation that it was is withdrawn. The label came from an uncommitted artifact whose identity cannot be determined from the repository; the measurement is unaffected.

## Fix

- `--project-id` is **required** on the CLI and is the only source of the output's project label.
- `run()` raises `ValueError` when it is missing or empty. There is no fallback to the targets file.
- The targets file's own field is still reported, in a separate `targets_provenance_project` key, so provenance stays visible without being able to impersonate a measurement.
- `research/references/unc13a_targets_sealed.json` was **not** edited. Its hash is unchanged: `e35f6e05016b30eab89f8d3aacc2d4ec101840e24e2b6f07159e6c5235d0bc3a`.

Probe hash: `0b5fbaf72d331298e820236d2ecdbf58bc359c6eb9be9ab5685da01440ff4f15` → `8a6d6b78db64316b0b7778d4f531364d0ee10ed7465dbd28e24e4ed7c0d2829f`. The plan's sealed probe hash refers to the pre-fix version and is superseded for the probe only, never for the targets.

## Tests

`tests/test_recount3_junction_probe.py`, 14 tests, all passing. Five are new:

- the sealed file still carries `SRP166282` as provenance — guards the premise, so the regression test cannot become vacuous;
- a run labelled `SRP999999` emits that label and not `SRP166282`, with provenance in its own field;
- a missing or empty project id raises instead of defaulting;
- the CLI exits non-zero without `--project-id` and succeeds with it;
- **the label is the only field the fix can change**: two runs over the same fixture differing only in project id produce identical values for every other key.

That last test is what makes the fix verifiable in CI from now on, independently of any one dataset.

## Deviation from the plan, and what is still outstanding

The plan asked for the SRP166282 inputs to be re-run and confirmed **byte-identical apart from the project label**. Two honest qualifications:

1. **Schema changed by one field.** Output now also carries `targets_provenance_project`. So the result is identical apart from the label *plus that added provenance key*. No measurement field changed, and the new test enforces that permanently. Keeping provenance visible was judged better than literal byte-identity; the deviation is recorded rather than glossed.
2. **The real-data re-run has not been performed.** The five recount3 input files for SRP166282 are not in the repository and re-fetching them is about 24.5 MB of external download, which the plan places under a separate scope decision. The equivalence argument currently rests on the fixture-based test, not on the original bytes. Their recorded SHA256 values are in `reports/recount3-unc13a-20261111/results.json`, so a re-run can be verified against them exactly if authorised.

Nothing else in the Question A plan is started: recount3 availability for the three candidates is still unverified, and no coverage has been measured.
