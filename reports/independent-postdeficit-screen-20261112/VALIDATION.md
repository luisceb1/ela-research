# Documentation verification — 12 November 2026

Executed local checks, not biological validation:

- `git diff --check`: passed.
- Parsed `candidates.tsv`: exactly C1/C2/C3, all 17 fields populated, three pending decisions and zero accepted. Unknown scientific details are labelled unverified rather than silently omitted.
- Parsed `sources.json`: four query groups, eleven exact queries in SEARCH_LOG; prospective plan commit resolves to `bac77055aa0e7eaaab9cced0513ef1cbb19819d5`.
- Nine prior-work rows checked against their exact blob SHAs at base `d09203c8546f3cca7bfeb54911eb322d3451404a`.
- Recomputed SHA256 of the retrieved JCI supplementary PDF; matches manifest `e5e9040526bd6eb948f397d997caea18a2d235666994a3a49590cc73e22a2562`. Header is PDF; `pdfinfo` reports nine pages; `pdfdetach -list` reports zero embedded files. Text extracted across all pages; page 9 rendered with Poppler and visually inspected for temporal same-rat wording.
- Nine local Markdown links checked in new report/plan and new status entries (excluding this then-pending validation file); final existence of this file checked before commit. Historical sections were not certified by this check.
- Confirmed remote main still `d09203c8546f3cca7bfeb54911eb322d3451404a` during review; issue #37 and #44 both closed when inspected. Neither issue changed.

No production code, data executor, input contract, estimator, threshold, historical numerical result or translation was changed. No new tests mirroring prose were added. The full offline scientific-software suite was not rerun locally for this documentation-only change; PR CI is a separate software check and must be read at its actual head. No claim of CI success is made by this file.

The documentary checks validate consistency/transcription and byte provenance where obtained. They do not certify the scientific truth of a paper, experimental independence, correctness of the baseline rule, unseen supplements or numerical eligibility. Search-tool renderings are cited by stable URLs and sections; inaccessible response hashes are explicitly not source-document hashes.

Transport correction: local `git push` failed because the CLI had no HTTPS credentials. The authenticated GitHub connector imports the exact plan and review files into new remote commits. The prospective local plan SHA above is not presented as an already reachable GitHub commit. `local_plan_commit.txt` preserves its raw commit payload; `git hash-object -t commit` reproduces the local SHA. The protocol file is unchanged since that commit.
