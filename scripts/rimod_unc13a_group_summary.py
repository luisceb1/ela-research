"""RiMOD UNC13A: metadata-joined *descriptive* junction counts (no individual export).

Run from repository root with: py scripts/rimod_unc13a_group_summary.py
Requires pyarrow; remote metadata is version-pinned to Fratta Lab.
Outputs only an aggregate report to stdout, no samples or person-level data.
"""
import csv
import hashlib
import io
import math
import statistics
import urllib.request
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parent.parent
ZIP = ROOT / "data/external/zenodo_15977268/full_rimod_parquets.zip"
OUTSIDE_GIT = ROOT / "data/external/zenodo_15977268"
SOURCE_COMMIT = "80fa3d70418a4665a85d414e33c7c470a9312086"
SOURCE_URL = (
    "https://raw.githubusercontent.com/frattalab/cryptic_biology/"
    + SOURCE_COMMIT + "/data/metadata_rimod.csv"
)
METADATA = OUTSIDE_GIT / "metadata_rimod.csv"
EVENTS = {
    (17641556, 17642845): "canonical",
    (17641556, 17642414): "cryptic_1",
    (17642541, 17642845): "cryptic_2",
    (17642591, 17642845): "cryptic_long",
}
GROUPS = ("control", "MAPT", "C9orf72", "GRN")


def load_metadata():
    OUTSIDE_GIT.mkdir(parents=True, exist_ok=True)
    if not METADATA.exists():
        with urllib.request.urlopen(SOURCE_URL, timeout=45) as response:
            METADATA.write_bytes(response.read())
    data = METADATA.read_bytes()
    rows = list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"))))
    if not rows or not {"sample", "genotype", "RNAseq"}.issubset(rows[0]):
        raise ValueError("Unexpected RiMOD metadata schema")
    mapping = {}
    for row in rows:
        sid = row["sample"].strip()
        group = row["genotype"].strip()
        if sid in mapping or group not in GROUPS or row["RNAseq"].lower() != "yes":
            raise ValueError("Duplicated sample, unsupported group or RNAseq=no")
        mapping[sid] = group
    print("Metadata SHA256:", hashlib.sha256(data).hexdigest())
    return mapping


def main():
    mapping = load_metadata()
    by_sample = defaultdict(dict)
    with zipfile.ZipFile(ZIP) as archive:
        names = [
            n for n in archive.namelist()
            if n.startswith("full_rimod_parquets/chrom=chr19/")
            and n.endswith(".parquet")
            and "/._" not in n
        ]
        for name in names:
            with archive.open(name) as fd:
                table = pq.read_table(
                    io.BytesIO(fd.read()),
                    columns=["sample", "start", "end", "strand", "junction_count"],
                )
            for row in table.to_pylist():
                start, end = row["start"], row["end"]
                if start is None or end is None or row["strand"] != "-":
                    continue
                if not (17641000 <= start <= 17643500 and 17641000 <= end <= 17643500):
                    continue
                if not (float(start).is_integer() and float(end).is_integer()):
                    raise ValueError("Non-integral coordinate")
                event = EVENTS.get((int(start), int(end)))
                if event is None:
                    continue
                sid = row["sample"]
                if sid not in mapping:
                    raise ValueError("Junction sample missing from source metadata")
                val = row["junction_count"]
                if val is None or not math.isfinite(val) or val < 0:
                    raise ValueError("Invalid count")
                if event in by_sample[sid]:
                    raise ValueError("Duplicate sample-event record")
                by_sample[sid][event] = float(val)

    if set(by_sample) != set(mapping):
        raise ValueError("Mismatch between sample sets: metadata and junction records")
    if any(set(v) != set(EVENTS.values()) for v in by_sample.values()):
        raise ValueError("Some samples lack an event record")
    print("Parquets read:", len(names))
    print("Matched samples:", len(by_sample))
    print("Group sizes:", dict(Counter(mapping.values())))
    print("Event | Group | N | Positive | Total | Median | Max")
    for event in EVENTS.values():
        for group in GROUPS:
            values = [v[event] for sample, v in by_sample.items() if mapping[sample] == group]
            print(
                f"{event} | {group} | {len(values)} | {sum(v > 0 for v in values)}"
                f" | {sum(values):.0f} | {statistics.median(values):g} | {max(values):g}"
            )
    print("DESCRIPTIVE ONLY: no PSI, inference or biological validation.")
    print("Coordinate conventions and event identity remain provisional.")


if __name__ == "__main__":
    main()
