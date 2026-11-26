"""Provision, supervise and clean up the fixed single-library replay."""
import os
from pathlib import Path
import shlex
import subprocess
import sys

import smoke

ROOT = Path(__file__).resolve().parents[2]
# The expiry checker is shared with the smoke test and honors the lease label.
LEASE_SECONDS = 3 * 3600
REMOTE_SECONDS = 140 * 60


def workload(ssh, output):
    output.mkdir(exist_ok=False)
    commit = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
    source = subprocess.check_output(["git", "-C", str(ROOT), "archive", commit])
    subprocess.run(ssh + [
        "mkdir -p /root/ela-replay/code && tar -xf - -C /root/ela-replay/code"
    ], input=source, check=True, timeout=90)
    command = (
        "cloud-init status --wait >/dev/null && "
        "apt-get update -qq && DEBIAN_FRONTEND=noninteractive "
        "apt-get install -y -qq --no-install-recommends build-essential curl fastp python3-venv && "
        "python3 -m venv /root/ela-replay/venv && "
        "/root/ela-replay/venv/bin/pip install --disable-pip-version-check 'pysam==0.23.3' && "
        "ELA_PILOT_COMMIT=" + shlex.quote(commit) + " /root/ela-replay/venv/bin/python "
        "/root/ela-replay/code/infrastructure/hetzner/stmn2_pilot_remote.py"
    )
    status = 1
    try:
        with (output / "execution.log").open("wb") as log:
            result = subprocess.run(
                ssh + ["timeout --kill-after=30s 138m bash -lc " + shlex.quote(command)],
                stdout=log, stderr=subprocess.STDOUT, timeout=REMOTE_SECONDS,
            )
            status = result.returncode
    finally:
        # Retrieve only small result/QC/log files, never reads or intermediate alignments.
        # Individual failures are retained in the controller log and do not prevent cleanup.
        for relative in ("tools.json", "plan.json", "comparison.json", "GSM8009878/stmn2-counts.json",
                         "GSM8009878/fastp.json", "GSM8009878/fastp.log",
                         "GSM8009878/hisat2.log", "GSM8009878/hisat2-summary.txt", "build.log"):
            try:
                result = subprocess.run(ssh + [
                    "f=/root/ela-replay/report/" + relative + "; "
                    "test -f \"$f\" && test $(wc -c < \"$f\") -le 5000000 && cat \"$f\""
                ], capture_output=True, timeout=30)
                if result.returncode == 0:
                    (output / Path(relative).name).write_bytes(result.stdout)
            except subprocess.TimeoutExpired:
                print(f"Result retrieval timed out: {relative}", flush=True)
    if status != 0 or not (output / "comparison.json").is_file():
        raise RuntimeError("Remote replay failed or comparison missing")


def main():
    if len(sys.argv) != 3 or not smoke.NAME.fullmatch(sys.argv[1]):
        raise ValueError("Exact run name and output directory required")
    cloud = smoke.Cloud(os.environ.get("HCLOUD_TOKEN"))
    smoke.run(cloud, sys.argv[1], Path(sys.argv[2]), workload=workload, lease_seconds=LEASE_SECONDS)


if __name__ == "__main__":
    main()
