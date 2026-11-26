"""Recompute the predefined descriptive factorial contrasts from library counts."""
import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean

def fractions(skipping, edge_a, edge_b):
    if skipping <= 0:
        raise ValueError("Missing skipping support")
    return (
        100 * (edge_a + edge_b) / (2 * skipping + edge_a + edge_b),
        100 * edge_a / (skipping + edge_a),
        100 * edge_b / (skipping + edge_b),
    )

def main():
    conditions = ("SCRAMBLE", "UPF1", "TDP43", "TDP43_UPF1")
    values = defaultdict(list)
    with Path(__file__).with_name("counts.csv").open(newline="") as source:
        rows = list(csv.DictReader(source))
    assert len(rows) == len({row["run"] for row in rows}) == 16
    for row in rows:
        counts = [int(row[key]) for key in (
            "unc_skipping", "unc_shared", "unc_short", "unc_long",
            "pfkp_skipping", "pfkp_left", "pfkp_right",
        )]
        assert min(counts) >= 0 and int(row["processed_pairs"]) > 0
        u, s, short, long, p, left, right = counts
        group = row["batch"], row["condition"]
        values[*group, "UNC13A"].append(fractions(u, s, short + long))
        values[*group, "PFKP"].append(fractions(p, left, right))

    print("gene,batch,metric,scramble_percent,upf1_percent,tdp43_percent,double_kd_percent,upf1_delta_pp,double_delta_pp,interaction_pp")
    for gene in ("UNC13A", "PFKP"):
        for batch in ("M85", "M86"):
            groups = [values[batch, condition, gene] for condition in conditions]
            assert all(len(group) == 2 for group in groups)
            for i, metric in enumerate(("symmetric", "edge_a", "edge_b")):
                s, u, t, d = (mean(row[i] for row in group) for group in groups)
                numbers = (s, u, t, d, u - s, d - t, (d - t) - (u - s))
                print(",".join([gene, batch, metric, *(f"{n:.6f}" for n in numbers)]))

if __name__ == "__main__":
    main()
