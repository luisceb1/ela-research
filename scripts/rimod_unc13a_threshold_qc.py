"""Prospective descriptive UNC13A threshold/QC audit for local RiMOD parquets.

Requires pyarrow; metadata downloaded by rimod_unc13a_group_summary.py.
Only prints aggregate statistics; no patient-level export.
"""
import csv
import io
import math
import zipfile
from collections import defaultdict
from pathlib import Path

import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = ROOT / "data/external/zenodo_15977268/full_rimod_parquets.zip"
META = ROOT / "data/external/zenodo_15977268/metadata_rimod.csv"
EVENTS = {
    (17641556, 17642845): "canonical",
    (17641556, 17642414): "cryptic_1",
    (17642541, 17642845): "cryptic_2",
    (17642591, 17642845): "cryptic_long",
}
GROUPS = {
    "control": "comparator",
    "MAPT": "comparator",
    "C9orf72": "FTLD-TDP-proxy",
    "GRN": "FTLD-TDP-proxy",
}
THRESHOLDS = (1, 3, 5)


def main():
    if not META.exists():
        raise SystemExit("Missing metadata: first run scripts/rimod_unc13a_group_summary.py")
    with META.open(encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    lookup = {}
    for row in rows:
        sample, genotype = row["sample"], row["genotype"]
        if sample in lookup or genotype not in GROUPS:
            raise ValueError("Duplicate sample or unknown genotype")
        lookup[sample] = genotype

    counts, clusters = defaultdict(dict), defaultdict(dict)
    with zipfile.ZipFile(ARCHIVE) as archive:
        names = [n for n in archive.namelist()
                 if n.startswith("full_rimod_parquets/chrom=chr19/")
                 and n.endswith(".parquet") and "/._" not in n]
        for name in names:
            with archive.open(name) as fh:
                table = pq.read_table(io.BytesIO(fh.read()), columns=[
                    "sample", "start", "end", "strand", "junction_count",
                    "cluster", "cluster_count"
                ])
            for r in table.to_pylist():
                s, e = r["start"], r["end"]
                if s is None or e is None or r["strand"] != "-":
                    continue
                if not (17641000 <= s <= 17643500 and 17641000 <= e <= 17643500):
                    continue
                if not (float(s).is_integer() and float(e).is_integer()):
                    raise ValueError("Nonintegral coordinate")
                event = EVENTS.get((int(s), int(e)))
                if event is None:
                    continue
                sid = r["sample"]
                if sid not in lookup or event in counts[sid]:
                    raise ValueError("Missing metadata or duplicate sample-event")
                val, denom = r["junction_count"], r["cluster_count"]
                if val is None or not math.isfinite(val) or val < 0:
                    raise ValueError("Invalid junction count")
                if denom is None or not math.isfinite(denom) or denom < 0:
                    raise ValueError("Invalid cluster count")
                counts[sid][event] = float(val)
                clusters[sid][event] = (r["cluster"], float(denom))
    if set(counts) != set(lookup) or any(set(v) != set(EVENTS.values()) for v in counts.values()):
        raise ValueError("Sample or event coverage mismatch")

    print("SAMPLES:", len(counts), "PARQUETS:", len(names))
    for event in EVENTS.values():
        ids = {clusters[sid][event][0] for sid in counts}
        print("CLUSTER_IDS", event, sorted(ids))
    print("Threshold | Event | Group | N positive / N total")
    for threshold in THRESHOLDS:
        for event in EVENTS.values():
            for genotype in ("control", "MAPT", "C9orf72", "GRN"):
                values = [counts[sid][event] for sid in counts if lookup[sid] == genotype]
                print(threshold, event, genotype, sum(v >= threshold for v in values), "/", len(values), sep=" | ")

    print("Co-occurrence of cryptic junctions (per group; >=1 count each):")
    for genotype in ("control", "MAPT", "C9orf72", "GRN"):
        ids = [s for s in counts if lookup[s] == genotype]
        print(genotype,
              "any:", sum(any(counts[s][e] >= 1 for e in ("cryptic_1", "cryptic_2", "cryptic_long")) for s in ids),
              "all3:", sum(all(counts[s][e] >= 1 for e in ("cryptic_1", "cryptic_2", "cryptic_long")) for s in ids),
              "pair12:", sum(counts[s]["cryptic_1"] >= 1 and counts[s]["cryptic_2"] >= 1 for s in ids))
    print("QC only: grouping is genotype-derived, reference and CE transcript identity pending.")
    print("No PSI/p-values/diagnostic accuracy; do not sum junctions as independent molecules.")


if __name__ == "__main__":
    main()
