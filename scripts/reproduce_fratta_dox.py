"""Bounded molecular-table replay, not functional rescue or biological inference."""
import argparse
import csv
import hashlib
import io
import json
import math
import random
import statistics
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

TREATMENTS = ("NT", "Dox-1", "Dox-2", "Dox-3", "Dox-4", "Dox-5")
SERIES = {
    "13A-Correct RNA": ("Correct_RNA", "UNC13A"),
    "13A-Protein": ("Protein", "UNC13A"), "13A-RNA": ("RNA", "UNC13A"),
    "13B-Protein": ("Protein", "UNC13B"), "13B-RNA": ("RNA", "UNC13B"),
    "TDP-Protein": ("Protein", "TDP-43"), "TDP-RNA": ("RNA", "TDP-43"),
}
KEYS = ("Treatment", "Gene", "Line_Group", "Color_Group")
HASHES = {
    "csv": "c7de1f2d44f9a5ac243e0ef380f50c455254c1cbefc6a217dc091505918526e5",
    "rmd": "3c46c164af6572bef28507b707f39d996d687abb06da00bf5468f89d0d491502",
}


def read_rows(data):
    reader = csv.DictReader(io.StringIO(data.decode("utf-8"), newline=""))
    if reader.fieldnames != ["Treatment", "Gene", "Value", "Line_Group", "Color_Group"]:
        raise ValueError("Unexpected source header")
    rows = list(reader)
    for row in rows:
        if None in row or any(value is None for value in row.values()):
            raise ValueError("Malformed source row")
        if row["Treatment"] not in TREATMENTS or row["Gene"] not in SERIES:
            raise ValueError("Unknown treatment/series")
        if (row["Line_Group"], row["Color_Group"]) != SERIES[row["Gene"]]:
            raise ValueError("Inconsistent source grouping labels")
        value = float(row["Value"])
        if not math.isfinite(value) or value < 0:
            raise ValueError("Invalid source value")
    if {(r["Treatment"], r["Gene"]) for r in rows} != {
            (t, s) for t in TREATMENTS for s in SERIES}:
        raise ValueError("Incomplete treatment/series grid")
    return rows


def summarize(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[tuple(row[key] for key in KEYS)].append(float(row["Value"]))
    output = []
    for key, values in groups.items():
        if len(values) < 2:
            raise ValueError("Too few rows to reproduce source sample SD")
        sd = statistics.stdev(values)
        output.append(dict(zip(KEYS, key), n_rows=len(values), mean=statistics.mean(values),
                           sd_rows=sd, sem_rows=sd / math.sqrt(len(values))))
    return sorted(output, key=lambda r: (TREATMENTS.index(r["Treatment"]), r["Gene"]))


def replay_join(summary, rename_before_join):
    """Explicit common-column equivalent of the pinned R left_join(tmp)."""
    sem_table = {tuple(r[k] for k in KEYS): r["sem_rows"] for r in summary}
    result = []
    for row in summary:
        if row["Gene"] == "13A-RNA":
            continue  # Exactly the source's plot filter, not removal from audit.
        joined = {k: row[k] for k in KEYS}
        if rename_before_join:
            joined["Line_Group"] = joined["Line_Group"].replace("Correct_RNA", "RNA")
        value = sem_table.get(tuple(joined[k] for k in KEYS))
        joined["Line_Group"] = joined["Line_Group"].replace("Correct_RNA", "RNA")
        joined.update(mean=row["mean"], n_rows=row["n_rows"], sem_rows=value,
                      sem_join_matched=value is not None)
        result.append(joined)
    return result


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def independent_checks(rows, summary):
    groups = defaultdict(list)
    for row in rows:
        groups[tuple(row[key] for key in KEYS)].append(Fraction(row["Value"]))
    for row in summary:
        values = groups[tuple(row[key] for key in KEYS)]
        n = len(values)
        exact_mean = sum(values) / n
        exact_variance = sum((x - exact_mean) ** 2 for x in values) / (n - 1)
        if not (abs(float(exact_mean) - row["mean"]) < 1e-12 and
                abs(math.sqrt(float(exact_variance / n)) - row["sem_rows"]) < 1e-12):
            raise ValueError("Independent rational arithmetic mismatch")
    shuffled = list(rows)
    random.Random(20261104).shuffle(shuffled)
    if summarize(shuffled) != summary:
        raise ValueError("Summary changes under row permutation")
    return {"independent_fraction_checks": len(summary),
            "all_group_means_and_sem_match": True, "row_permutation_preserves_summary": True,
            "rows": len(rows), "groups_with_5_rows": sum(len(v) == 5 for v in groups.values()),
            "groups_with_3_rows": sum(len(v) == 3 for v in groups.values()),
            "all_identical_observations_preserved": True, "biological_pairing_inferred": False,
            "seed_for_order_check": 20261104}


def plot_unc13a(rows, summary, output):
    # Optional plotting dependency; the scientific tables use standard Python only.
    import matplotlib
    matplotlib.use("Agg")
    matplotlib.rcParams["svg.hashsalt"] = "fratta-dox-replay-v1"
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(9.4, 5.6))
    selected = [("13A-RNA", "ARN total", "#69717c"),
                ("13A-Correct RNA", "ARN correcto", "#227eab"),
                ("13A-Protein", "Proteína", "#be593b")]
    x = list(range(len(TREATMENTS)))
    point_count = 0
    for gene, label, color in selected:
        means = [next(r["mean"] for r in summary if r["Gene"] == gene and
                      r["Treatment"] == t) for t in TREATMENTS]
        ax.plot(x, means, color=color, linewidth=2, marker="o", label=label)
        for i, treatment in enumerate(TREATMENTS):
            values = [float(r["Value"]) for r in rows if r["Gene"] == gene and
                      r["Treatment"] == treatment]
            offsets = [(j - (len(values) - 1) / 2) * 0.045 for j in range(len(values))]
            ax.scatter([i + offset for offset in offsets], values, s=22, color=color,
                       alpha=0.65, zorder=3)
            point_count += len(values)
    ax.set_xticks(x, TREATMENTS)
    ax.set_ylim(bottom=0)
    ax.set_ylabel("Valores relativos del archivo (NT ≈ 100)")
    ax.set_xlabel("Condición original; no representa tiempo ni dosis cuantificada")
    ax.set_title("UNC13A: ARN y proteína", loc="left", fontsize=17, fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.18)
    ax.legend(frameon=False, ncol=3, loc="upper right")
    fig.text(0.09, 0.035, "Puntos: mediciones depositadas. Líneas: medias por condición.\n"
             "Sin identificación de réplicas biológicas; sin IC ni prueba de rescate funcional.",
             fontsize=9, color="#4c525a")
    fig.subplots_adjust(left=0.10, right=0.98, top=0.88, bottom=0.23)
    fig.savefig(output / "unc13a-molecular.svg", metadata={"Date": None})
    fig.savefig(output / "unc13a-molecular.png", dpi=160)
    plt.close(fig)
    return {"matplotlib": matplotlib.__version__, "unc13a_points": point_count}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-csv", type=Path, required=True)
    parser.add_argument("--source-rmd", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--plot", action="store_true")
    args = parser.parse_args()
    data, rmd = args.source_csv.read_bytes(), args.source_rmd.read_bytes()
    for key, content in (("csv", data), ("rmd", rmd)):
        if hashlib.sha256(content).hexdigest() != HASHES[key]:
            raise ValueError("Source SHA256 mismatch: " + key)
    rows = read_rows(data)
    summary = summarize(rows)
    checks = independent_checks(rows, summary)
    original, repaired = replay_join(summary, True), replay_join(summary, False)
    args.output.mkdir(parents=True, exist_ok=True)
    write_csv(args.output / "all-groups.csv", summary)
    write_csv(args.output / "source-order-join.csv", original)
    write_csv(args.output / "key-preserving-join.csv", repaired)
    unc13a = []
    for t in TREATMENTS:
        lookup = {r["Gene"]: r for r in summary if r["Treatment"] == t}
        unc13a.append({"condition": t, "total_RNA": lookup["13A-RNA"]["mean"],
                       "correct_RNA": lookup["13A-Correct RNA"]["mean"],
                       "protein": lookup["13A-Protein"]["mean"]})
    write_csv(args.output / "unc13a-means.csv", unc13a)
    (args.output / "independent-checks.json").write_text(
        json.dumps(checks, indent=2, sort_keys=True) + "\n")
    qc = {
        "source_rows": len(rows), "groups": len(summary), "plot_groups": len(original),
        "source_order_missing_sem": [r["Treatment"] + ":" + r["Gene"] for r in original
                                     if not r["sem_join_matched"]],
        "key_preserving_missing_sem": sum(not r["sem_join_matched"] for r in repaired),
        "means_unchanged_by_join_order": all(a["mean"] == b["mean"]
                                            for a, b in zip(original, repaired)),
        "identical_rows_not_deduplicated": sum(n - 1 for n in Counter(
            tuple(r.values()) for r in rows).values() if n > 1),
        "independent_biological_replicates": None, "functional_rescue_estimated": False,
        "R_executed": False, "python": sys.version,
        "source_sha256": HASHES, "interpretation": "row arithmetic and join replay only",
    }
    if args.plot:
        qc.update(plot_unc13a(rows, summary, args.output))
    (args.output / "qc.json").write_text(json.dumps(qc, indent=2, sort_keys=True) + "\n")
    print(json.dumps(qc, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
