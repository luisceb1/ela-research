"""Read-only analysis of one authorized public human RNA-seq library; no effect estimate."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import time

import prjdb19918_contract as contract
ROOT = contract.ROOT
sys.path.insert(0, str(ROOT / "scripts"))
import replay_stmn2_minimal as replay
import run_gse252892_local as original
from stmn2_pilot_remote import download as pinned_download

WORK = Path("/root/ela-replay")
REPORT = WORK / "report"
INPUT = WORK / "input"


def run(args, **kw):
    return subprocess.run(args, check=True, **kw)


def prepare_reference():
    ref = replay.reference()
    idx = replay.read(ROOT / "reports/hisat2-index-inspection-20261031/verified_index.json")
    gcc = replay.read(ROOT / "reports/unc13a-minigenome-20261102/source.json")
    archive = INPUT / "hisat2-source.tar.gz"
    pinned_download(gcc["url"], archive, gcc["bytes"], gcc["sha256"])
    with tarfile.open(archive, "r:gz") as tar:
        tar.extractall(INPUT, filter="data")
    native = INPUT / f"hisat2-{gcc['source_commit']}"
    with (REPORT / "build.log").open("wb") as log:
        run(["make", "-C", str(native), "-j2", "USE_SRA=0", "hisat2-align-s"], stdout=log, stderr=subprocess.STDOUT)
    tools = {}
    for key, path, expected in (("fastp", Path("/usr/bin/fastp"), "fastp 0.23.4"),
                                ("aligner", native / "hisat2-align-s", "hisat2-align-s version 2.2.3")):
        ver = run([str(path), "--version"], capture_output=True, text=True)
        version = ver.stdout + ver.stderr
        if expected not in version:
            raise ValueError("Unexpected tool version")
        sha = replay.sha(path)
        tools[key] = {"path": str(path), "version": version, "sha256": sha,
                      "historical_build_match": sha == ref["historical_tools"][key]}
    replay.write_new(REPORT / "tools.json", tools)
    arc = INPUT / "index.tar.gz"
    pinned_download(idx["pinned_url"], arc, idx["size_bytes"], idx["archive_sha256"])
    index = INPUT / "index"
    index.mkdir()
    expected = {"hg38/" + r["name"]: r for r in ref["index_files"]}
    seen = set()
    with tarfile.open(arc, "r|gz") as tar:
        for member in tar:
            if member.name not in expected:
                continue
            r = expected[member.name]
            if member.name in seen or not member.isfile() or member.size != r["bytes"]:
                raise ValueError("Index archive member mismatch")
            dest = index / r["name"]
            with tar.extractfile(member) as src, dest.open("xb") as out:
                shutil.copyfileobj(src, out)
            if replay.sha(dest) != r["sha256"]:
                raise ValueError("Index digest mismatch")
            seen.add(member.name)
    if seen != set(expected):
        raise ValueError("Index shards missing")
    arc.unlink()
    return tools, index


def fetch_inputs(row):
    inputs=[]
    for mate in row["mates"]:
        file=INPUT / f"{row['run']}_{mate['mate']}.fastq.gz"
        run(["curl", "--fail", "--location", "--silent", "--show-error", "--connect-timeout", "20",
             "--max-time", "2400", "--max-filesize", str(mate["bytes"]), "--output", str(file), mate["url"]])
        actual=replay.digest(file)
        if actual["bytes"] != mate["bytes"] or actual["md5"] != mate["md5"]:
            raise ValueError("Input identity mismatch")
        inputs.append({**mate, **actual, "path": str(file), "gsm": row["run"]})
    replay.write_new(REPORT/"input-receipts.json", inputs)
    return inputs


def measure(plan, row, targets):
    import pysam
    run_id=row["run"]
    d=REPORT/run_id
    d.mkdir()
    cmd=plan["commands"][run_id]
    with (d/"fastp.log").open("xb") as log:
        run(cmd["fastp"], stdout=log, stderr=subprocess.STDOUT)
    if not all(Path(p).is_file() and Path(p).stat().st_size for p in cmd["plain_files"]):
        raise ValueError("Missing preprocessing outputs")
    replay.free_check(WORK)
    with (d/"hisat2.log").open("xb") as log:
        process=subprocess.Popen(cmd["align"], stdout=subprocess.PIPE, stderr=log)
        try:
            with pysam.AlignmentFile(process.stdout, "r") as sam:
                if sam.get_reference_length("chr19") != 58617616:
                    raise ValueError("chr19 header mismatch")
                result=original.count_records(sam, targets)
            if process.wait()!=0:
                raise ValueError("Alignment failed")
        finally:
            process.stdout.close()
            if process.poll() is None:
                process.terminate()
                try: process.wait(timeout=2)
                except subprocess.TimeoutExpired: process.kill(); process.wait()
    for key in ("sam_records","alignment_groups","eligible_groups","marked_duplicate_records","rejected_groups"):
        result["qc"].setdefault(key,0)
    result.update(run=run_id,sample=row["sample"],condition=row["condition"],gene="UNC13A",
                  complete=True,scope="technical coverability only; not biological replication")
    replay.write_new(REPORT/"result.json",result)
    for p in cmd["plain_files"]:Path(p).unlink()
    return contract.validate_result(result,row)


def main():
    if len(sys.argv)!=2:
        raise ValueError("Exact run required")
    row=contract.select(sys.argv[1])
    start=time.monotonic()
    REPORT.mkdir(); INPUT.mkdir()
    replay.free_check(WORK, admission=True)
    if sys.version_info[:2]!=(3,12):
        raise ValueError("Python version mismatch")
    import pysam
    if pysam.__version__!="0.23.3":
        raise ValueError("PySAM version mismatch")
    target_file=ROOT/"research/references/unc13a_targets_sealed.json"
    target=replay.read(target_file)
    if target["assembly"]!="GRCh38/hg38" or target["chromosome"]!="chr19" or target["strand"]!="-":
        raise ValueError("Unexpected reference contract")
    targets=target["junctions"]
    tools,index=prepare_reference()
    inputs=fetch_inputs(row)
    plan={"run_root":str(REPORT),"index_dir":str(index),"inputs":inputs,"tools":tools,
          "run":row["run"],"sample":row["sample"],"commit":os.environ["ELA_PILOT_COMMIT"],
          "manifest_sha256":contract.MANIFEST_SHA,"reference_sha256":replay.sha(target_file),
          "counter_sha256":replay.sha(ROOT/"scripts/run_gse252892_local.py")}
    plan["commands"]={row["run"]:replay.commands(plan,row["run"])}
    replay.write_new(REPORT/"plan.json",plan)
    replay.limits()
    result=measure(plan,row,targets)
    replay.write_new(REPORT/"timing.json",{"total_seconds":time.monotonic()-start})
    print("TECHNICAL_RESULT_VALID",flush=True)


if __name__=="__main__":
    main()
