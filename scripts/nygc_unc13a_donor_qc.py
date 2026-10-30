"""NYGC UNC13A: motor cortex, one library per donor, descriptive QC.

Selection is blinded to cryptic outcome: highest local cluster depth per donor.
No donor-level files or identifiers printed. No inferential or clinical claim.
Run from repository root: py scripts/nygc_unc13a_donor_qc.py
"""
import csv
import io
import math
import statistics
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

import pyarrow.compute as pc
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data/external/zenodo_15977268"
COORDS = {
    (17641556, 17642845): "canonical",
    (17641556, 17642414): "donor",
    (17642541, 17642845): "acceptor",
}
DEPTHS = (0, 50, 100)
RIN_BANDS = (("all", -math.inf, math.inf),
             ("RIN<6.5", -math.inf, 6.5),
             ("RIN6.5-7.5", 6.5, 7.5),
             ("RIN>=7.5", 7.5, math.inf))

def main():
    with (DATA / "metadta_nygc.csv").open(encoding="utf-8-sig", newline="") as fd:
        rows = list(csv.DictReader(fd))
    meta = {}
    critical = ("external_subject_id", "rna_tissue_source_simplified",
                "tdp_proteinopathy", "rin")
    conflicts = 0
    for row in rows:
        sid = row["sample"].strip()
        if not sid:
            raise ValueError("Empty sample ID")
        if sid in meta:
            if any(meta[sid][k].strip() != row[k].strip() for k in critical):
                conflicts += 1
            continue
        meta[sid] = row
    if conflicts:
        raise ValueError(f"Conflicting duplicate sample metadata: {conflicts}")

    eligible = {
        sid: r for sid, r in meta.items()
        if r["rna_tissue_source_simplified"].strip() == "Cortex_Motor"
        and r["tdp_proteinopathy"].strip() in ("ALS-TDP", "Control")
    }
    observed = defaultdict(dict)
    with zipfile.ZipFile(DATA / "nygc_parquets.zip") as z:
        filenames = [n for n in z.namelist() if n.startswith("parquets/")
                     and n.endswith(".parquet") and "/._" not in n]
        for index, filename in enumerate(filenames, 1):
            with z.open(filename) as f:
                parquet = pq.ParquetFile(io.BytesIO(f.read()))
            for rg in range(parquet.num_row_groups):
                table = parquet.read_row_group(rg, columns=[
                    "chrom", "sample", "start", "end", "strand",
                    "junction_count", "cluster_count"
                ])
                mask = pc.and_(
                    pc.equal(table["chrom"], "chr19"),
                    pc.and_(pc.equal(table["strand"], "-"),
                            pc.and_(pc.and_(pc.greater_equal(table["start"], 17641000),
                                           pc.less_equal(table["start"], 17643500)),
                                    pc.and_(pc.greater_equal(table["end"], 17641000),
                                            pc.less_equal(table["end"], 17643500)))))
                for row in table.filter(mask).to_pylist():
                    sid = row["sample"]
                    if sid not in eligible:
                        continue
                    event = COORDS.get((row["start"], row["end"]))
                    if event is None:
                        continue
                    if event in observed[sid]:
                        raise ValueError("Duplicate sample-event pair")
                    j, d = row["junction_count"], row["cluster_count"]
                    if j is None or d is None or j < 0 or d <= 0 or j > d:
                        raise ValueError("Invalid depth or count")
                    observed[sid][event] = (j, d)
            if index % 500 == 0:
                print("SCANNED", index, "/", len(filenames), flush=True)

    if any(set(x) != set(COORDS.values()) for x in observed.values()):
        raise ValueError("Partial event records")

    donors = defaultdict(list)
    missing_donor = Counter()
    for sid, counts in observed.items():
        r = eligible[sid]
        donor = r["external_subject_id"].strip()
        group = r["tdp_proteinopathy"].strip()
        if not donor:
            missing_donor[group] += 1
            continue
        try:
            rin = float(r["rin"])
            if not math.isfinite(rin):
                rin = None
        except (ValueError, TypeError):
            rin = None
        donors[(group, donor)].append((sid, counts, rin))

    # Select one specimen per donor, using local depth only; same donor in
    # two discordant phenotypes is an error, not two independent observations.
    id_groups = defaultdict(set)
    for group, donor in donors:
        id_groups[donor].add(group)
    if any(len(gs) > 1 for gs in id_groups.values()):
        raise ValueError("Donor ID shared across ALS-TDP and Control groups")

    selected = {}
    for key, items in donors.items():
        # Deterministic selection by maximum local depth, then sample id.
        selected[key] = sorted(items, key=lambda x: (-x[1]["canonical"][1], x[0]))[0]
    print("MOTOR CORTEX SAMPLES:", len(observed))
    print("UNIQUE DONORS:", len(selected))
    print("DROPPED SAMPLES MISSING DONOR ID:", dict(missing_donor))
    print("EXTRA LIBRARIES REMOVED BY DEDUPLICATION:",
          sum(len(v) - 1 for v in donors.values()))
    print("GROUP | MIN DEPTH | RIN BAND | DONORS | DONOR JUNC >=1 | ACCEPTOR JUNC >=1 | MEDIAN DEPTH | RIN AVAILABLE")
    for cutoff in DEPTHS:
        for band, low, high in RIN_BANDS:
            for group in ("ALS-TDP", "Control"):
                subset = [item for (g, donor), item in selected.items()
                          if g == group and item[1]["canonical"][1] >= cutoff
                          and (band == "all" or
                               (item[2] is not None and low <= item[2] < high))]
                depths = [x[1]["canonical"][1] for x in subset]
                med = statistics.median(depths) if depths else "NA"
                pos1 = sum(x[1]["donor"][0] >= 1 for x in subset)
                pos2 = sum(x[1]["acceptor"][0] >= 1 for x in subset)
                rin_n = sum(x[2] is not None for x in subset)
                print(group, "|", cutoff, "|", band, "|", len(subset),
                      "|", pos1, "|", pos2, "|", med, "|", rin_n)
    print("Descriptive only. Donor IDs are source metadata proxies.")
    print("Selection by coverage may create bias; confirm provenance and")
    print("missing-metadata patterns before any inference.")

if __name__ == "__main__":
    main()
