# Prepare a bounded local execution proposal

Use the exact reviewed commit communicated for this PR. Keep the old pilot checkout/environment. Update only the new detached `/home/luisceb/proyectos/ela-local-20261112` worktree after confirming it is clean. Substitute REVIEWED_COMMIT; run one line at a time and stop on errors.

```powershell
wsl -d Ubuntu-24.04 -- git -C /home/luisceb/proyectos/ela-local-20261112 status --short
wsl -d Ubuntu-24.04 -- git -C /home/luisceb/proyectos/ela-local-20261112 fetch origin REVIEWED_COMMIT
wsl -d Ubuntu-24.04 -- git -C /home/luisceb/proyectos/ela-local-20261112 checkout --detach REVIEWED_COMMIT
wsl -d Ubuntu-24.04 -- /home/luisceb/proyectos/ela-research-piloto/.venv/bin/python /home/luisceb/proyectos/ela-local-20261112/scripts/run_gse252892_local.py prepare --base-descriptor /home/luisceb/ela-gse252892-prepared-20261112.json --fastp /usr/bin/fastp --run-root /home/luisceb/ela-gse252892-run-01 --output /home/luisceb/ela-gse252892-execution-20261112.json
```

Success is `execution_proposal_not_started` with a descriptor SHA256, advertised input bytes 12,826,593,031, transfer cap 14,000,000,000, wall 43,200 seconds, CPU/RAM/disk caps and raw bytes downloaded 0. It checks real C: free bytes through PowerShell interop, not the virtual ext4 capacity. Index rehashing takes local I/O time. No FASTQ is acquired in this phase. The existing disabled descriptor remains untouched.

The execute action requires exact accepted proposal SHA256 and `--accept-transfer-bytes 14000000000`; it consumes the proposal once and creates a new run root. Do not invoke it until the concrete proposal and raw budget are explicitly approved. No resume, overwrite or wider library selection is available. Stop errors are retained in supervision/worker/transfer receipts. During approved execution a progress summary is printed approximately every 30 seconds; Ctrl+C requests process-group cleanup. Closing WSL/Windows can bypass cleanup receipts and is not a safe resume mechanism.

This runbook intentionally gives preparation commands only. The [report](../../reports/gse252892-bounded-runner-20261112/REPORT.md) records software tests, units, pipeline differences and unvalidated live behaviour.
