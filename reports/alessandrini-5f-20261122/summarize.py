"""Recompute descriptive batch contrasts from the reported library counts."""
import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean


def fractions(skipping, edge_a, edge_b):
    return (
        100 * (edge_a + edge_b) / (2 * skipping + edge_a + edge_b),
        100 * edge_a / (skipping + edge_a),
        100 * edge_b / (skipping + edge_b),
    )


values = defaultdict(list)
with Path(__file__).with_name("counts.csv").open(newline="") as counts:
    rows = list(csv.DictReader(counts))
    assert len(rows) == len({row["run"] for row in rows}) == 8
    for row in rows:
        u, s, short, long, p, left, right = [
            int(row[key]) for key in (
                "unc_skipping", "unc_shared", "unc_short", "unc_long",
                "pfkp_skipping", "pfkp_left", "pfkp_right",
            )
        ]
        group = row["batch"], row["condition"]
        values[*group, "UNC13A"].append(fractions(u, s, short + long))
        values[*group, "PFKP"].append(fractions(p, left, right))

print("gene,batch,metric,tdp43_percent,double_kd_percent,delta_pp")
for gene in ("UNC13A", "PFKP"):
    for batch in ("M85", "M86"):
        tdp = values[batch, "TDP43", gene]
        double = values[batch, "TDP43_UPF1", gene]
        assert len(tdp) == len(double) == 2
        for metric, a, b in zip(
            ("symmetric", "edge_a", "edge_b"), zip(*tdp), zip(*double), strict=True
        ):
            baseline, combined = mean(a), mean(b)
            print(f"{gene},{batch},{metric},{baseline:.6f},{combined:.6f},{combined-baseline:.6f}")
