# Two loose ends resolved — 12 November 2026

Both items left open by [PR #66](../probe-project-label-fix-20261112/REPORT.md) are now closed. No new biological measurement; this is verification and provenance work.

## 1. The SRP166282 re-run, now done with the real bytes

PR #66 deferred this: the fix's equivalence rested on a synthetic fixture, because the five recount3 input files were not in the repository and re-fetching them fell under a separate scope decision.

**Re-fetched, and the bytes are identical to those recorded in November.** All five files reproduce both the SHA256 and the byte size stored in `reports/recount3-unc13a-20261111/results.json`:

| File | Bytes | SHA256 reproduced |
|---|---|---|
| sra.junctions.SRP166282.ALL.RR.gz | 9,646,299 | yes |
| sra.junctions.SRP166282.ALL.MM.gz | 14,862,092 | yes |
| sra.junctions.SRP166282.ALL.ID.gz | 95 | yes |
| sra.recount_project.SRP166282.MD.gz | 271 | yes |
| sra.sra.SRP166282.MD.gz | 3,108 | yes |

That is worth recording for its own sake: the deposit served byte-identical files a day later, so the earlier result rests on inputs that can still be reproduced exactly.

Re-running the fixed probe over them:

```
python3 -I scripts/recount3_junction_probe.py \
  --rr  sra.junctions.SRP166282.ALL.RR.gz \
  --mm  sra.junctions.SRP166282.ALL.MM.gz \
  --ids sra.junctions.SRP166282.ALL.ID.gz \
  --project sra.recount_project.SRP166282.MD.gz \
  --sra sra.sra.SRP166282.MD.gz \
  --targets research/references/unc13a_targets_sealed.json \
  --project-id SRP166282 --min-coverage 20
```

**Every field shared with the committed result is identical**: `per_junction`, `verdict`, `samples`, `matrix_header`, `assay_shape`, `inputs`, `n_samples`, and `project` itself. The only difference is the single added key `targets_provenance_project`, which is the documented schema change from PR #66.

So the deviation PR #66 recorded — equivalence argued from a fixture rather than the original bytes — is now closed against the real data, and the recorded schema addition is confirmed to be the only change.

## 2. The SRP334561 label: resolved as far as the repository allows

`reports/recount3-unc13a-20261111/results_SRP334561.json` reports `"project": "SRP334561"`. The pre-fix probe copied that field from the targets file, and the sealed targets file carries `SRP166282`, so the file appeared to be impossible to produce.

Evidence from the repository:

- `research/references/unc13a_targets_sealed.json` has exactly **two commits**, `afa84bb` and `83cf23a`. **Both carry `"project": "SRP166282"`.** The sealed file has never held `SRP334561` in committed history.
- **No second UNC13A targets file has ever been committed**, on any branch. The only other sealed targets file in the repository is `stmn2_targets_sealed.json`.
- The plan addendum that fixed SRP334561 as a candidate (`b593cb0`) records the candidate and its prespecified interpretation, but **not the probe command or the targets path used**.

**Conclusion.** The label came from an artifact that was never committed — most plausibly an ad-hoc targets file written outside the repository, since the probe accepts any path — or from a manual edit of the output. **Which of the two cannot be determined from the repository**, and no further evidence exists to settle it. That uncertainty is recorded rather than resolved by assumption.

What can be stated positively:

- **The committed seal was never broken.** No commit of the sealed file shows anything but `SRP166282`, so the earlier worry that "its seal was broken at that moment" is **not supported** by the history and is withdrawn.
- **The measurement is unaffected.** The probe never read `project` for measurement; targets come from `junctions` and `chromosome`. The input hashes recorded in `results_SRP334561.json` are SRP334561's own files, so the counts belong to the project the file names.
- **It cannot recur.** Since PR #66 the label comes from a required `--project-id` argument with no fallback, and a regression test asserts a new project id cannot emit `SRP166282`.

The residual item is a documentation gap in a November cycle, not a data-integrity problem: that run's exact invocation was not recorded. Plans written since PR #66 record the command and the targets hash, so the gap does not extend forward.

## Boundaries

Verification and provenance only. No effect, coverage, PSI, p-value or model; no biological claim is made, strengthened or withdrawn. The SRP166282 coverage rejection and the SRP334561 ineligibility both stand exactly as recorded. Transfer: 24.5 MB, re-fetching files already hashed in the repository.
