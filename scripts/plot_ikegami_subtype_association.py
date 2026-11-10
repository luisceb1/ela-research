#!/usr/bin/env python3
"""Render aggregate coefficients and marginal percentile intervals; no source pairs."""
import argparse
import json
from pathlib import Path


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = json.loads(args.results.read_text())
    entries = [
        ("pooled", "Todos los casos · Spearman (n=35)"),
        ("adjusted", "Ajustado por subtipo · rangos (n=35)"),
        ("ALS Type 1", "Tipo 1 · Spearman (n=12)"),
        ("ALS Type 2a", "Tipo 2a · Spearman (n=12)"),
        ("ALS Type 2b", "Tipo 2b · Spearman (n=11)"),
        ("pooled_without_2b", "Sin Tipo 2b · Spearman (n=24)"),
        ("adjusted_without_2b", "Sin Tipo 2b · ajustado (n=24)"),
    ]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "svg.fonttype": "none"})
    fig, ax = plt.subplots(figsize=(11.8, 5.5))
    for i, (key, label) in enumerate(entries):
        point = result["estimates"][key]
        lo, hi = result["bootstrap"]["estimates"][key]["ci95_percentile"]
        color = "#0f766e" if key == "adjusted" else "#475569"
        ax.plot([lo, hi], [i, i], color=color, linewidth=2)
        ax.scatter([point], [i], color=color, s=40, zorder=3)
        ax.text(1.09, i, f"{point:.3f} [{lo:.3f}, {hi:.3f}]", va="center", fontsize=9)
    ax.set_yticks(range(len(entries)), [label for _, label in entries])
    ax.invert_yaxis(); ax.set_xlim(-1.02, 1.04)
    ax.axvline(0, color="#94a3b8", linewidth=1, linestyle="--")
    ax.set_xticks([-1, -.5, 0, .5, 1])
    ax.set_xlabel("Coeficiente de asociación entre rangos")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0, pad=10)
    ax.grid(axis="x", alpha=.15)
    fig.suptitle("UNC13A–STMN2: asociación global y condicionada por subtipo", x=.04, ha="left", fontsize=14, weight="bold")
    fig.text(.04,.91,"Ikegami/Koike 2026 · mismos 35 casos · análisis exploratorio interno",fontsize=10,color="#475569")
    fig.text(.04,.065,"Barras: intervalos percentiles marginales del 95%; 10.000 remuestreos de pares dentro de subtipo.",fontsize=9)
    fig.text(.04,.025,"Prueba principal: permutación dentro de subtipo, p = 0,07825. Los intervalos no son simultáneos.",fontsize=9)
    fig.subplots_adjust(left=.33, right=.75, top=.85, bottom=.19)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(args.output, dpi=170)
    print(f"Rendered with matplotlib {matplotlib.__version__}: {args.output}")


if __name__ == "__main__":
    main()
