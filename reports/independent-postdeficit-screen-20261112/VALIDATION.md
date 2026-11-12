# Documentation verification — 12 November 2026

Executed local checks, not biological validation:

- `git diff --check`: passed.
- Parsed `candidates.tsv`: exactly C1/C2/C3, all 17 fields populated; originally three pending decisions and zero accepted. Review correction: two pending data gates archived without active follow-up, one discarded at abstract triage, zero accepted. Unknown scientific details are labelled unverified rather than silently omitted.
- Parsed `sources.json`: four query groups, eleven exact queries in SEARCH_LOG; prospective plan commit resolves to `bac77055aa0e7eaaab9cced0513ef1cbb19819d5`.
- Nine prior-work rows checked against their exact blob SHAs at base `d09203c8546f3cca7bfeb54911eb322d3451404a`.
- Recomputed SHA256 of the retrieved JCI supplementary PDF; matches manifest `e5e9040526bd6eb948f397d997caea18a2d235666994a3a49590cc73e22a2562`. Header is PDF; `pdfinfo` reports nine pages; `pdfdetach -list` reports zero embedded files. Text extracted across all pages; page 9 rendered with Poppler and visually inspected for temporal same-rat wording.
- Nine local Markdown links checked in new report/plan and new status entries (excluding this then-pending validation file); final existence of this file checked before commit. Historical sections were not certified by this check.
- Confirmed remote main still `d09203c8546f3cca7bfeb54911eb322d3451404a` during review; issue #37 and #44 both closed when inspected. Neither issue changed.

No production code, data executor, input contract, estimator, threshold, historical numerical result or translation was changed. No new tests mirroring prose were added. The full offline scientific-software suite was not rerun locally for this documentation-only change; PR CI is a separate software check and must be read at its actual head. No claim of CI success is made by this file.

The documentary checks validate consistency/transcription and byte provenance where obtained. They do not certify the scientific truth of a paper, experimental independence, correctness of the baseline rule, unseen supplements or numerical eligibility. Search-tool renderings are cited by stable URLs and sections; inaccessible response hashes are explicitly not source-document hashes.

Transport correction: local `git push` failed because the CLI had no HTTPS credentials. The authenticated GitHub connector imports the exact plan and review files into new remote commits. The prospective local plan SHA above is not presented as an already reachable GitHub commit. `local_plan_commit.txt` preserves its raw commit payload; `git hash-object -t commit` reproduces the local SHA. The protocol file is unchanged since that commit.

Review CI check: all five checks passed on exact pre-correction head `5f0364b961d5840d4de736bc44f690578f70cd70` (python-tests, pe-contract 3.11/3.12, unit-tests 3.11/3.12). This supersedes the earlier conversational in-progress status, not the historical observation. New correction commits need their own checks. Source metadata API response/hash and field propagation are checked separately from software CI; these checks do not turn an abstract into a full-text audit.

Correction checks executed: C1/C2/C3 IDs and 17 populated fields; pending/discarded/pending decisions; exact API-response and abstract hashes; DOI/version/date/licence; zero new candidates; all three current summaries updated; 16 local links; git diff --check. No production code or effect outputs changed.

Residual propagation check: STATE and BACKLOG now both report zero of six specific interventions with bounded documentation wording and a dated pre-curation correction note. Adjacent obsolete prevention/refutation wording in STATE is narrowed to the existing two readings; original pre-curation labels remain explicitly historical. Both isolated-depth sentences in the recount3 source report and its STATE summary are corrected. Matrix bytes and recount3 result JSON bytes are unchanged; only Markdown documentation changed. No full software-suite rerun is needed for this prose-only correction; each new PR head still runs CI separately.
