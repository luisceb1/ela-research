"""Exploratory UNC13A stratified RIN sensitivity, RiMOD.

Run from repo root: py scripts/rimod_unc13a_rin_strata.py
Requires pyarrow and author metadata already downloaded by group_summary script.
Prints aggregate cells only; descriptive, not an adjusted causal model.
"""
import csv
import io
import math
import statistics
import zipfile
from collections import defaultdict
from pathlib import Path
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data/external/zenodo_15977268"
TARGETS = {(17641556, 17642845): "canonical",
           (17641556, 17642414): "cryptic_1",
           (17642541, 17642845): "cryptic_2",
           (17642591, 17642845): "cryptic_long"}
GROUP = {"control": "comparison", "MAPT": "comparison",
         "GRN": "FTLD-TDP-proxy", "C9orf72": "FTLD-TDP-proxy"}
# Declared exploratory splits, chosen without examining per-sample outcomes.
RIN_BANDS = [("RIN < 6.5", 0, 6.5), ("6.5 <= RIN < 7.5", 6.5, 7.5),
             ("RIN >= 7.5", 7.5, math.inf)]
DEPTH_MINIMA = [0, 50, 100]


def main():
    with (DATA / "metadata_rimod.csv").open(encoding="utf-8-sig", newline="") as fd:
        rows = list(csv.DictReader(fd))
    metadata = {}
    for r in rows:
        sid, genotype = r["sample"].strip(), r["genotype"].strip()
        if sid in metadata or genotype not in GROUP:
            raise ValueError("Invalid metadata sample or genotype")
        rin = float(r["RIN"])
        if not math.isfinite(rin):
            raise ValueError("Invalid RIN")
        metadata[sid] = (GROUP[genotype], rin)
    found = defaultdict(dict)
    with zipfile.ZipFile(DATA / "full_rimod_parquets.zip") as archive:
        names = [n for n in archive.namelist() if n.startswith(
            "full_rimod_parquets/chrom=chr19/") and n.endswith(".parquet")
            and "/._" not in n]
        for name in names:
            with archive.open(name) as fd:
                t = pq.read_table(io.BytesIO(fd.read()), columns=[
                    "sample", "start", "end", "strand", "junction_count",
                    "cluster_count", "cluster"])
            for r in t.to_pylist():
                s, e = r["start"], r["end"]
                if s is None or e is None or r["strand"] != "-":
                    continue
                if not (17641000 <= s <= 17643500 and 17641000 <= e <= 17643500):
                    continue
                if not (float(s).is_integer() and float(e).is_integer()):
                    raise ValueError("Nonintegral coordinate")
                event = TARGETS.get((int(s), int(e)))
                if event is None:
                    continue
                sid, count, depth = r["sample"], r["junction_count"], r["cluster_count"]
                if sid not in metadata or event in found[sid]:
                    raise ValueError("Missing metadata or duplicate junction")
                if (count is None or depth is None or not math.isfinite(count)
                        or not math.isfinite(depth) or count < 0 or depth <= 0
                        or count > depth):
                    raise ValueError("Invalid junction/cluster counts")
                found[sid][event] = (float(count), float(depth), r["cluster"])
    if set(found) != set(metadata) or any(set(v) != set(TARGETS.values()) for v in found.values()):
        raise ValueError("Incomplete sample-event mapping")
    if any(len({v[1] for v in e.values()}) != 1 for e in found.values()):
        raise ValueError("Inconsistent denominator")
    if {v[2] for e in found.values() for v in e.values()} != {"clu_46643_-"}:
        raise ValueError("Unexpected clusters")

    print("RIN STRATIFICATION / EXPLORATORY; n=", len(found))
    print("GROUP | RIN BAND | MIN CLUSTER DEPTH | N | CE1>=1 | CE1>=3 | CE1>=5 | median CE1 ratio | median depth | median RIN")
    for depth_min in DEPTH_MINIMA:
        for label, lower, upper in RIN_BANDS:
            for group in ("comparison", "FTLD-TDP-proxy"):
                ids = [sid for sid in found if metadata[sid][0] == group
                       and lower <= metadata[sid][1] < upper
                       and found[sid]["canonical"][1] >= depth_min]
                n = len(ids)
                positives = [sum(found[sid]["cryptic_1"][0] >= k for sid in ids)
                             for k in (1, 3, 5)]
                ratios = [found[sid]["cryptic_1"][0] / found[sid]["cryptic_1"][1]
                          for sid in ids]
                depths = [found[sid]["canonical"][1] for sid in ids]
                rins = [metadata[sid][1] for sid in ids]
                val = lambda arr: f"{statistics.median(arr):.4g}" if arr else "NA"
                print(f"{group} | {label} | {depth_min} | {n} | "
                      f"{positives[0]} | {positives[1]} | {positives[2]} | "
                      f"{val(ratios)} | {val(depths)} | {val(rins)}")
    print("LIMITATIONS: descriptive strata can be sparse; RIN band selection exploratory.")
    print("No donor-level output; no formal confounding adjustment, PSI validation, causal inference or independent replication.")


if __name__ == "__main__":
    main()
