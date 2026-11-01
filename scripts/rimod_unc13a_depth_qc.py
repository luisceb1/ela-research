"""RiMOD UNC13A: sample-matched depth/RIN confounding checks. Aggregates only.

Run: py scripts/rimod_unc13a_depth_qc.py
No biological validation; no patient-level files or p-values.
"""
import csv
import io
import math
import statistics
import zipfile
from collections import defaultdict, Counter
from pathlib import Path

import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parent.parent
ZIP = ROOT / "data/external/zenodo_15977268/full_rimod_parquets.zip"
META = ROOT / "data/external/zenodo_15977268/metadata_rimod.csv"
JUNC = {
    (17641556, 17642845): "canonical",
    (17641556, 17642414): "cryptic_1",
    (17642541, 17642845): "cryptic_2",
    (17642591, 17642845): "cryptic_long",
}
GROUP = {"control": "comparison", "MAPT": "comparison",
         "C9orf72": "FTLD-TDP-proxy", "GRN": "FTLD-TDP-proxy"}
DEPTH_FILTERS = (0, 20, 50, 100)


def median(values):
    return "NA" if not values else f"{statistics.median(values):.3g}"


def main():
    with META.open(encoding="utf-8-sig", newline="") as f:
        metadata = list(csv.DictReader(f))
    info = {}
    for row in metadata:
        sid = row["sample"]
        if sid in info or row["genotype"] not in GROUP:
            raise ValueError("Duplicate sample or unexpected genotype")
        try:
            rin = float(row["RIN"])
        except (ValueError, TypeError):
            rin = None
        info[sid] = {"group": GROUP[row["genotype"]], "genotype": row["genotype"],
                     "rin": rin, "pmd": row["PMD"], "age": row["Age"]}
    found = defaultdict(dict)
    with zipfile.ZipFile(ZIP) as z:
        names = [n for n in z.namelist()
                 if n.startswith("full_rimod_parquets/chrom=chr19/")
                 and n.endswith(".parquet") and "/._" not in n]
        for name in names:
            with z.open(name) as fh:
                tab = pq.read_table(io.BytesIO(fh.read()), columns=[
                    "sample", "start", "end", "strand",
                    "junction_count", "cluster_count", "cluster"])
            for row in tab.to_pylist():
                s, e = row["start"], row["end"]
                if s is None or e is None or row["strand"] != "-":
                    continue
                if not (17641000 <= s <= 17643500 and 17641000 <= e <= 17643500):
                    continue
                if not (float(s).is_integer() and float(e).is_integer()):
                    raise ValueError("Noninteger junction coordinate")
                key = JUNC.get((int(s), int(e)))
                if key is None:
                    continue
                sid, j, d = row["sample"], row["junction_count"], row["cluster_count"]
                if sid not in info or key in found[sid]:
                    raise ValueError("Duplicate event or unmatched sample")
                if (j is None or d is None or not math.isfinite(j)
                        or not math.isfinite(d) or j < 0 or d < 0 or j > d):
                    raise ValueError("Impossible junction/cluster count")
                found[sid][key] = (float(j), float(d), row["cluster"])
    if set(found) != set(info) or any(set(events) != set(JUNC.values()) for events in found.values()):
        raise ValueError("Incomplete sample/event coverage")

    inconsistent = 0
    zero_depth = 0
    cluster_ids = set()
    for sid, events in found.items():
        denominators = {v[1] for v in events.values()}
        cluster_ids.update(v[2] for v in events.values())
        if len(denominators) != 1:
            inconsistent += 1
        if events["canonical"][1] == 0:
            zero_depth += 1

    print("SOURCE ROWS:", len(info), "MATCHED:", len(found), "PARQUETS:", len(names))
    print("CLUSTER IDS:", sorted(cluster_ids))
    print("SAMPLES WITH INCONSISTENT CLUSTER_COUNT:", inconsistent)
    print("SAMPLES WITH ZERO CLUSTER COUNT:", zero_depth)
    if inconsistent:
        print("STOP: cannot use common denominator pending inspection.")
        return

    for group in ("comparison", "FTLD-TDP-proxy"):
        ids = [s for s in found if info[s]["group"] == group]
        ds = [found[s]["canonical"][1] for s in ids]
        rs = [info[s]["rin"] for s in ids if info[s]["rin"] is not None]
        print("QC GROUP:", group, "N:", len(ids),
              "CLUSTER_DEPTH median:", median(ds), "min:", min(ds), "max:", max(ds),
              "RIN observed:", len(rs), "RIN median:", median(rs))

    print("DEPTH FILTER | GROUP | N retained | CE1 >=1 | CE1 >=3 | CE1 >=5 | CE2 >=1 | CE-long >=1")
    for cutoff in DEPTH_FILTERS:
        for group in ("comparison", "FTLD-TDP-proxy"):
            ids = [s for s in found if info[s]["group"] == group
                   and found[s]["canonical"][1] >= cutoff]
            hits = lambda e, t: sum(found[s][e][0] >= t for s in ids)
            print(cutoff, "|", group, "|", len(ids), "|",
                  hits("cryptic_1",1), "|", hits("cryptic_1",3), "|",
                  hits("cryptic_1",5), "|", hits("cryptic_2",1), "|",
                  hits("cryptic_long",1))
    print("COUNT RATIOS by group: descriptive junction_count / cluster_count")
    for group in ("comparison", "FTLD-TDP-proxy"):
        ids = [s for s in found if info[s]["group"] == group
               and found[s]["canonical"][1] > 0]
        for event in ("canonical", "cryptic_1", "cryptic_2", "cryptic_long"):
            values = [found[s][event][0] / found[s][event][1] for s in ids]
            print(group, event, "n", len(values), "median", median(values),
                  "max", max(values) if values else "NA")
    print("Author uses junction_count / cluster_count as PSI-like measure.")
    print("QC ONLY: verify LeafCutter conventions, exon interpretation, batch, tissue, RIN and depth.")
    print("No independent replication or biomarker validation.")


if __name__ == "__main__":
    main()
