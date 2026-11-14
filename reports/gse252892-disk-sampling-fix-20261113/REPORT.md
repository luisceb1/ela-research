# Disk sampler atomic-rename race — 13 November 2026

Current status: final host receipts have now been supplied; see [post-sampler evidence and continuation](../gse252892-after-sampler-20261113/REPORT.md). The missing-receipt status below describes the earlier diagnosis.

## Evidence and cause

The [user traceback](user-failure.json) is in the supervisor, not the range downloader: `root_bytes` observed `transport-receipts/000232.json.tmp` as a file and then attempted a second stat after the worker atomically renamed it. The vanished temporary pathname caused an unhandled FileNotFoundError. This is a software race introduced by the runner, not an observed memory/disk/transfer limit or evidence of a new network failure. The last heartbeat (9,592 s; lineage upper bound 3,948,860,671 bytes) precedes failure and must not be treated as the final charge.

The exception enters the existing cleanup/final supervision path. Final supervision, ledger, outstanding reservations, block inventory and verified-file receipts are still needed from the host before any continuation. No final cleanup status or recoverable-byte total is inferred from the traceback. No new live transfer is performed or proposed by this fix; the consumed v3 proposal remains consumed. No biological result is demonstrated.

## Correction

The disk sampler now obtains one non-following `lstat` metadata snapshot per listed name and uses that same snapshot for type and size. If a leaf name disappears between listing and metadata acquisition, that sample skips the vanished name. Missing roots, root/leaf symlinks, traversal and permission errors still fail. This removes the redundant existence/type/size reads that raced with atomic receipt/block promotion.

This remains a sampled guard, not a transactional disk snapshot or a kernel quota. Concurrent changes can affect sampled totals; no exact instantaneous disk-use guarantee is added. Original 100 GiB across prior/current roots and actual C: reserve remain. Transport settings, fixed body-byte cap, charge retention, scientific operations, estimator/count rules and existing closures are unchanged. No cloud service or merge is authorized by the fix.

## Validation and next step

[Focused tests](focused-tests.json): 92 passed, no failures/errors/skips. Six new regressions cover atomic promotion after metadata acquisition, disappearance before acquisition, propagated permission/traversal errors, missing roots and symlink roots; existing leaf-symlink and scientific-source-equality controls also pass. Python compilation and diff checks pass. This verifies fixtures, not a resumed host run.

Next: obtain the final v3 supervision/ledger and current verified-file/attempt inventory without changing that root. Retain all three attempts. A future continuation needs a new prospective proposal with the final conservative charge, complete original FASTQs if verified, and validated remaining blocks; do not relaunch consumed v3 or claim this patch enables resume by itself.
