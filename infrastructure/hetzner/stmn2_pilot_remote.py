"""Replay one fixed, previously measured human STMN2 library on a new host."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import replay_stmn2_minimal as replay

GSM = "GSM8009878"
WORK = Path("/root/ela-replay")
REPORT = WORK / "report"
INPUT = WORK / "input"


def run(args, **kw):
    return subprocess.run(args, check=True, **kw)


def download(url, file, size, sha256, md5=None):
    run(["curl", "--fail", "--location", "--silent", "--show-error",
         "--connect-timeout", "20", "--max-time", "2400", "--max-filesize",
         str(size), "--output", str(file), url])
    actual = replay.digest(file)
    if actual["bytes"] != size or actual["sha256"] != sha256 or (
        md5 is not None and actual["md5"] != md5
    ):
        raise ValueError(f"Input identity mismatch: {file.name}")
    return actual


def main():
    start = time.monotonic()
    REPORT.mkdir()
    INPUT.mkdir()
    if shutil.disk_usage(WORK).free < replay.CAPS["admission_free_bytes"]:
        raise RuntimeError("Insufficient free disk")
    if sys.version_info[:2] != (3, 12):
        raise ValueError("Python 3.12 required")
    import pysam
    if pysam.__version__ != "0.23.3":
        raise ValueError("PySAM version mismatch")
    manifest = replay.reference()
    index_metadata = replay.read(ROOT / "reports/hisat2-index-inspection-20261031/verified_index.json")
    gcc_source = replay.read(ROOT / "reports/unc13a-minigenome-20261102/source.json")
    archive = INPUT / "hisat2-source.tar.gz"
    download(gcc_source["url"], archive, gcc_source["bytes"], gcc_source["sha256"])
    with tarfile.open(archive, "r:gz") as tar:
        tar.extractall(INPUT, filter="data")
    native = INPUT / f"hisat2-{gcc_source['source_commit']}"
    run(["make", "-C", str(native), "-j2", "USE_SRA=0", "hisat2-align-s"],
        stdout=(REPORT / "build.log").open("w"), stderr=subprocess.STDOUT)
    tools = {}
    for key, path, expected_version in (
        ("fastp", Path("/usr/bin/fastp"), "fastp 0.23.4"),
        ("aligner", native / "hisat2-align-s", "hisat2-align-s version 2.2.3"),
    ):
        info = run([str(path), "--version"], capture_output=True, text=True)
        version = info.stdout + info.stderr
        if expected_version not in version:
            raise ValueError(f"Unexpected {key} version")
        sha = replay.sha(path)
        tools[key] = {"path": str(path), "version": version, "sha256": sha,
                      "historical_build_match": sha == manifest["historical_tools"][key]}
    replay.write_new(REPORT / "tools.json", tools)
    print("TOOLS_VERIFIED", flush=True)
    index_archive = INPUT / "index.tar.gz"
    download(index_metadata["pinned_url"], index_archive, index_metadata["size_bytes"],
             index_metadata["archive_sha256"])
    index_dir = INPUT / "index"
    index_dir.mkdir()
    expected_members = {"hg38/" + row["name"]: row for row in manifest["index_files"]}
    seen = set()
    with tarfile.open(index_archive, "r|gz") as tar:
        for member in tar:
            if member.name not in expected_members:
                continue
            row = expected_members[member.name]
            if member.name in seen or not member.isfile() or member.size != row["bytes"]:
                raise ValueError("Index archive member mismatch")
            with tar.extractfile(member) as source, (index_dir / row["name"]).open("xb") as dest:
                shutil.copyfileobj(source, dest)
            if replay.sha(index_dir / row["name"]) != row["sha256"]:
                raise ValueError("Index digest mismatch")
            seen.add(member.name)
    if seen != set(expected_members):
        raise ValueError("Missing index archive shards")
    index_archive.unlink()
    print("INDEX_VERIFIED", flush=True)
    inputs = []
    for row in manifest["inputs"]:
        if row["gsm"] != GSM:
            continue
        path = INPUT / row["filename"]
        download(row["url"], path, row["bytes"], row["sha256"], row["md5"])
        inputs.append(dict(row, path=str(path)))
    if len(inputs) != 2:
        raise ValueError("Expected exactly two mates")
    print("INPUTS_VERIFIED", flush=True)
    plan = {"run_root": str(REPORT), "index_dir": str(index_dir),
            "inputs": inputs, "tools": tools}
    plan["commands"] = {GSM: replay.commands(plan, GSM)}
    plan["code_sha256"] = {path: replay.sha(ROOT / path) for path in replay.CODE}
    plan["repository_commit"] = os.environ["ELA_PILOT_COMMIT"]
    replay.write_new(REPORT / "plan.json", plan)
    print("REPLAY_STARTED", flush=True)
    replay_start = time.monotonic()
    # The original library procedure has exactly the same parameters and counter.
    replay.limits()
    actual = replay.measure(plan, GSM)
    expected = next(r["expected"] for r in manifest["libraries"] if r["gsm"] == GSM)
    observed_match = actual == expected
    replay.write_new(REPORT / "comparison.json", {
        "exact_record_match": observed_match, "gsm": GSM,
        "expected": expected, "observed": actual,
        "replay_seconds": time.monotonic() - replay_start,
        "total_seconds": time.monotonic() - start,
        "python": sys.version, "pysam_version": pysam.__version__,
        "interpretation": "Technical replay of existing human RNA-seq; no independent biological replication.",
    })
    print("RECORDS_MATCH" if observed_match else "RECORDS_DIFFER", flush=True)
    if not observed_match:
        raise RuntimeError("Pre-existing counts/QC differ")


if __name__ == "__main__":
    main()
