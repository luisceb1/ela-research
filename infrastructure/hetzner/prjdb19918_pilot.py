"""Supervise one fixed technical pilot lease; reuse the independently verified lifecycle."""
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys

import smoke
import prjdb19918_contract as contract

ROOT = contract.ROOT


def workload(ssh, output, row):
    commit = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
    source = subprocess.check_output(["git", "-C", str(ROOT), "archive", commit])
    subprocess.run(ssh + ["mkdir -p /root/ela-replay/code && tar -xf - -C /root/ela-replay/code"],
                   input=source, check=True, timeout=90)
    command = (
        "cloud-init status --wait >/dev/null && "
        "apt-get update -qq && DEBIAN_FRONTEND=noninteractive "
        "apt-get install -y -qq --no-install-recommends build-essential curl fastp python3-venv && "
        "python3 -m venv /root/ela-replay/venv && "
        "/root/ela-replay/venv/bin/pip install --disable-pip-version-check 'pysam==0.23.3' && "
        "ELA_PILOT_COMMIT=" + shlex.quote(commit) + " /root/ela-replay/venv/bin/python "
        "/root/ela-replay/code/infrastructure/hetzner/prjdb19918_pilot_remote.py "
        + shlex.quote(row["run"])
    )
    status = 1
    log_path=output/"execution.log"
    try:
        with log_path.open("wb") as log:
            result=subprocess.run(ssh + ["timeout --kill-after=30s 138m bash -lc " + shlex.quote(command)],
                                  stdout=log,stderr=subprocess.STDOUT,timeout=contract.REMOTE_SECONDS)
            status=result.returncode
    finally:
        run_id=row["run"]
        for relative in ("tools.json","plan.json","input-receipts.json","result.json","timing.json","build.log",
                         f"{run_id}/fastp.json",f"{run_id}/fastp.log",f"{run_id}/hisat2.log",f"{run_id}/hisat2-summary.txt"):
            try:
                result=subprocess.run(ssh + ["f=/root/ela-replay/report/" + relative +
                    "; test -f \"$f\" && test $(wc -c < \"$f\") -le 5000000 && cat \"$f\""],
                    capture_output=True,timeout=15)
                if result.returncode==0:
                    (output/Path(relative).name).write_bytes(result.stdout)
            except (subprocess.TimeoutExpired, OSError):
                print("Result retrieval failed: "+relative,flush=True)
        if log_path.exists() and log_path.stat().st_size>5_000_000:
            with log_path.open("rb") as f:
                f.seek(-1_000_000,2);tail=f.read()
            log_path.write_bytes(b"[truncated execution log tail]\n"+tail)
    if status!=0 or not (output/"result.json").is_file():
        raise RuntimeError("Remote pilot failed or result missing")
    required=("result.json","timing.json","tools.json","plan.json","input-receipts.json",
              "fastp.json","hisat2-summary.txt")
    if not all((output/name).is_file() for name in required):
        raise RuntimeError("Technical evidence incomplete")
    contract.validate_result(json.loads((output/"result.json").read_text()),row)
    plan=json.loads((output/"plan.json").read_text())
    receipts=json.loads((output/"input-receipts.json").read_text())
    if plan["commit"]!=commit or plan["manifest_sha256"]!=contract.MANIFEST_SHA:
        raise RuntimeError("Provenance mismatch")
    if len(receipts)!=2 or any(r["md5"]!=m["md5"] or r["bytes"]!=m["bytes"] for r,m in zip(receipts,row["mates"])):
        raise RuntimeError("Input evidence mismatch")


def main():
    if len(sys.argv)!=4 or not smoke.NAME.fullmatch(sys.argv[1]):
        raise ValueError("Exact run name, library, and output directory required")
    row=contract.select(sys.argv[2])
    output=Path(sys.argv[3]);output.mkdir(exist_ok=False)
    cloud=smoke.Cloud(os.environ.get("HCLOUD_TOKEN"))
    rate=contract.combined_rate(cloud)
    (output/"price.json").write_text(json.dumps(rate,indent=2)+"\n")
    print("Verified combined hourly price: EUR "+rate["combined_rate_gross"],flush=True)
    smoke.run(cloud,sys.argv[1],output,workload=lambda ssh,out:workload(ssh,out,row),
              lease_seconds=contract.LEASE_SECONDS)


if __name__=="__main__":
    main()
