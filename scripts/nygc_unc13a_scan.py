"""NYGC UNC13A targeted ZIP scan, no extraction and no donor-level output.

Run: py scripts/nygc_unc13a_scan.py
Each Parquet is read in memory separately (row-group by row-group).
No metadata / phenotype grouping: this is only a molecular presence audit.
"""
from collections import defaultdict, Counter
from pathlib import Path
import io
import zipfile
import math
import pyarrow.parquet as pq
import pyarrow.compute as pc
import pyarrow as pa

ROOT = Path(__file__).resolve().parent.parent
ZIP = ROOT / "data/external/zenodo_15977268/nygc_parquets.zip"
TARGETS = {
    (17641556, 17642845): "canonical_candidate",
    (17641556, 17642414): "UNC13A_novel_donor",
    (17642541, 17642845): "UNC13A_novel_acceptor",
    (17642591, 17642845): "long_variant_unconfirmed",
}
COLUMNS = ["chrom", "sample", "start", "end", "strand", "junction_count", "cluster_count", "cluster", "psi"]
LOW, HIGH = 17641000, 17643500

def main():
    if not ZIP.exists():
        raise SystemExit(f"Missing local archive: {ZIP}")
    seen = set()
    samples = set()
    counts = defaultdict(float)
    positive = defaultdict(set)
    clusters = defaultdict(set)
    unexpected = Counter()
    matched_files = 0
    total_rows_in_window = 0
    with zipfile.ZipFile(ZIP) as z:
        files = [i for i in z.infolist() if i.filename.startswith("parquets/")
                 and i.filename.endswith(".parquet") and "/._" not in i.filename]
        print("NYGC PARQUETS:", len(files), flush=True)
        for idx, info in enumerate(files, 1):
            with z.open(info) as fd:
                pf = pq.ParquetFile(io.BytesIO(fd.read()))
            file_hit = False
            for rg in range(pf.num_row_groups):
                tab = pf.read_row_group(rg, columns=COLUMNS)
                mask = pc.and_(
                    pc.and_(pc.equal(tab["chrom"], "chr19"), pc.equal(tab["strand"], "-")),
                    pc.and_(
                        pc.and_(pc.greater_equal(tab["start"], LOW), pc.less_equal(tab["start"], HIGH)),
                        pc.and_(pc.greater_equal(tab["end"], LOW), pc.less_equal(tab["end"], HIGH))
                    )
                )
                rows = tab.filter(mask).to_pylist()
                if rows:
                    file_hit = True
                for row in rows:
                    total_rows_in_window += 1
                    coord = (int(row["start"]), int(row["end"]))
                    event = TARGETS.get(coord)
                    if event is None:
                        unexpected[coord] += 1
                        continue
                    sample = row["sample"]
                    j, d = row["junction_count"], row["cluster_count"]
                    if j is None or d is None or j < 0 or d < 0 or j > d:
                        raise ValueError("Invalid count/denominator")
                    identity = (sample, event)
                    if identity in seen:
                        raise ValueError("Duplicate sample-event key; investigate partitions")
                    seen.add(identity)
                    samples.add(sample)
                    counts[event] += j
                    if j > 0:
                        positive[event].add(sample)
                    clusters[event].add((row["cluster"], row["strand"]))
                    psi = row["psi"]
                    if d > 0 and psi is not None and math.isfinite(psi) and abs(psi - j / d) > 1e-6:
                        raise ValueError("Inconsistent supplied PSI")
            if file_hit:
                matched_files += 1
            if idx % 250 == 0:
                print(f"SCANNED: {idx}/{len(files)}", flush=True)
    print("FILES WITH CHR19 WINDOW:", matched_files)
    print("ROWS WITHIN WINDOW:", total_rows_in_window)
    print("SAMPLES WITH AT LEAST ONE TARGET:", len(samples))
    print("EVENT | RECORDS | POSITIVE | TOTAL JUNCTION COUNTS | CLUSTERS")
    for coords, event in TARGETS.items():
        print(event, coords, sum(e == event for _, e in seen),
              len(positive[event]), counts[event], sorted(clusters[event]))
    print("OTHER WINDOW JUNCTIONS:", len(unexpected))
    print("OTHER WINDOW COORDINATES (top 15 by rows):", unexpected.most_common(15))
    print("No sample phenotype interpretation; NYGC provenance, tissue, overlap and coordinate conventions unverified.")

if __name__ == "__main__":
    main()
