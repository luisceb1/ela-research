# PR #53 integration review — 12 November 2026

## Scope and decision

Luis authorized preparing #53 for review/merge and parking #51. Integrate the historical #53 head `fedfa4fd8122b40f45fbd2d0d88c28d3b7e92e6f` with current main `e2fbdc09283239c373fa806727b88c3abac9f476`, preserving both histories. No new scientific search, original-data transfer, biological fit, threshold change or contact is performed. PR #51 is closed unmerged as not currently planned; its branch is retained. No agent/API workflow from #51 enters this integration.

## Conflict resolution and scientific record

The sole conflicted file is the earlier Ikegami replay report. Keep main's existing caveats about non-significance, confounding, internal reproducibility and Spearman variance; retain the bounded corrections and reference to the later subtype-conditioned result. The two versions express compatible limits. All later main results, the #75 interpretation corrections, AD request status and cycle closures remain in place.

The subtype-conditioned result remains unchanged: pooled rho 0.57367; adjusted rank rho 0.31669; stratified two-sided permutation p=0.07825; marginal bootstrap 95% interval [-0.02342, 0.62758] on the same 35 cases. The fixed prediction was not met. This does not establish absence of association, a difference between subtype correlations, mechanism or independent replication. No favourable replacement analysis is selected.

The independent paired-marker screen remains closed with zero of its three sources admitted. The recorded authorized Quadros request was sent on 11 November; no reply or delivery of data is verified here. Communication logs are preserved rather than reissued. The early Keuss check is labelled historical and superseded by the later final-source recovery/conditional replay (#60–#62); it does not reopen #44, resolve strict v1, or authorize another follow-up. Current STATE/BACKLOG and the English findings page carry these distinctions. Dated original reports remain available; added status notices are in English. None of the seven source-pinned translations is modified by this integration.

## Validation

- [Focused software controls](focused-tests.json): 22/22 pass, no skips. These use fixtures and check software, not new biological evidence. The full suite is delegated to CI for the exact integrated head; an older green run is not evidence about this head.
- [Artifact preservation](artifact-preservation.json): numerical/figure artifacts, selected source receipts/decisions, communication log, original scripts/test and prospective plans match the original #53 bytes. The original `artifact-hashes.json` also verifies. No scientific executor is changed.
- Local Markdown targets and `git diff --check` are checked during integration.
- Original workbook and original source retrieval hashes are recorded, not freshly verified by downloading them. This integration is not another reproduction of the patient-data statistics.

## Stop and next input

Leave #53 ready for human review after its current-head CI checks. No automatic merge is authorized by this preparation. Preserve #37/#44/STMN2 closures. A new task requires concrete usable source material or author clarification with a separately fixed question and controls. AD support's acknowledgement confirms receipt/review of the workspace request only; active workspace and dataset access remain unconfirmed.
