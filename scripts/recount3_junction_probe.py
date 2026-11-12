#!/usr/bin/env python3
"""Read recount3 junction counts for fixed target junctions in one project.

Per research/plans/2026-11-11-recount3-unc13a-cycle.md.

recount3 publishes exon-exon junction counts for public RNA-seq projects, so a
locus can be queried without downloading FASTQ or aligning anything. This
script reads the three files recount3 stores per project and reports, for each
sample, the count of each target junction, together with the condition labels
that the deposit itself declares.

It does NOT estimate an effect, compute PSI or test a hypothesis. A count below
the project's coverage threshold is MISSING DATA, never a biological zero, and
the script labels it as such.

Coordinates: recount3 junction rows are 1-based inclusive over the intron
(verified by length == end - start + 1). Targets are given in the project's
sealed convention, intronic 0-based half-open, and converted as
[start0 + 1, end0]. No endpoint is ever shifted to force a match.

Usage:
  python -I scripts/recount3_junction_probe.py \
      --rr RR.gz --mm MM.gz --ids ID.gz --project PROJ.MD.gz --sra SRA.MD.gz \
      --targets targets.json --project-id SRPxxxxxx \
      [--min-coverage 20] [--json OUT]

--project-id is REQUIRED and is the only source of the output's project
label. The targets file's own "project" field is provenance for the sealed
coordinates and is never copied into a result: a sealed file carrying one
project must not silently relabel counts measured from another.

targets.json maps a name to [start0, end0] plus "chromosome", e.g.
  {"chromosome": "chr19",
   "junctions": {"canonical": [17641556, 17642844]}}
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def attribute(blob: str, key: str) -> str:
    """Pull one key out of recount3's 'k;;v|k;;v' sample_attributes string."""
    for part in (blob or "").split("|"):
        if part.startswith(key + ";;"):
            return part.split(";;", 1)[1]
    return ""


def find_target_rows(rr_path: Path, chromosome: str,
                     targets: dict[str, tuple[int, int]]) -> dict[str, dict]:
    """Locate each target junction's 1-based row index in the RR table.

    Matching is exact on chromosome, start and end. A target that is absent is
    reported as absent; the nearest junction on the same chromosome is recorded
    for context only and must never be adopted as a substitute.
    """
    wanted = {name: (start0 + 1, end0) for name, (start0, end0) in targets.items()}
    found: dict[str, dict] = {}
    nearest: dict[str, tuple[int, int, int]] = {}
    with gzip.open(rr_path, "rt") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        for index, row in enumerate(reader, start=1):
            if row["chromosome"] != chromosome:
                continue
            start, end = int(row["start"]), int(row["end"])
            # Convention guard: recount3 stores length inclusive of both ends.
            if int(row["length"]) != end - start + 1:
                raise ValueError(
                    f"row {index}: length {row['length']} does not match "
                    f"end-start+1 for {start}-{end}; coordinate convention "
                    "differs from the one this script assumes")
            for name, (ws, we) in wanted.items():
                if start == ws and end == we:
                    found[name] = {
                        "row": index, "start_1based": start, "end_1based": end,
                        "strand": row["strand"], "annotated": row["annotated"],
                        "left_motif": row["left_motif"],
                        "right_motif": row["right_motif"],
                    }
                else:
                    distance = abs(start - ws) + abs(end - we)
                    if name not in nearest or distance < nearest[name][0]:
                        nearest[name] = (distance, start, end)
    for name in wanted:
        if name not in found:
            dist = nearest.get(name)
            found[name] = {
                "row": None, "absent": True,
                "nearest_junction": None if dist is None else
                {"distance_sum": dist[0], "start_1based": dist[1],
                 "end_1based": dist[2],
                 "note": "context only; never adopted as the target"},
            }
    return found


def assay_shape(rr_path: Path, chromosome: str) -> dict:
    """Flag a quantification that looks targeted rather than transcriptome-wide.

    A real RNA-seq project yields hundreds of thousands of junctions spread
    across every chromosome. A targeted amplicon run yields a handful, nearly
    all at one locus, and SRA metadata may still label it "RNA-Seq" (observed
    for SRP334561, whose paper states the deposit is amplicon sequencing). The
    distinction matters: huge counts in a targeted assay do not demonstrate the
    transcriptome-wide detectability a coverage threshold is meant to ensure.
    """
    total = 0
    on_chrom = 0
    chroms = set()
    with gzip.open(rr_path, "rt") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        for row in reader:
            total += 1
            chroms.add(row["chromosome"])
            if row["chromosome"] == chromosome:
                on_chrom += 1
    share = (on_chrom / total) if total else 0.0
    looks_targeted = bool(total < 5000 and share > 0.5)
    return {
        "total_junctions": total,
        "junctions_on_target_chromosome": on_chrom,
        "share_on_target_chromosome": round(share, 4),
        "distinct_chromosomes": len(chroms),
        "looks_targeted_not_transcriptome_wide": looks_targeted,
        "note": ("Heuristic, not proof. When true, verify the assay against the "
                 "source publication before treating coverage as comparable to "
                 "transcriptome-wide junction counts."),
    }


def read_counts(mm_path: Path, rows: dict[int, str]) -> tuple[dict[str, dict[int, int]], dict]:
    """Stream the MatrixMarket file, keeping only the requested rows."""
    counts: dict[str, dict[int, int]] = {name: {} for name in rows.values()}
    header = {}
    with gzip.open(mm_path, "rt") as fh:
        for line in fh:
            if line.startswith("%"):
                continue
            fields = line.split()
            if len(fields) == 3 and not header:
                header = {"rows": int(fields[0]), "columns": int(fields[1]),
                          "nonzeros": int(fields[2])}
                continue
            if len(fields) != 3:
                continue
            row = int(fields[0])
            name = rows.get(row)
            if name is not None:
                counts[name][int(fields[1])] = int(fields[2])
    return counts, header


def build_samples(ids_path: Path, project_path: Path, sra_path: Path) -> list[dict]:
    with gzip.open(ids_path, "rt") as fh:
        rails = [line.strip() for line in fh
                 if line.strip() and line.strip() != "rail_id"]
    with gzip.open(project_path, "rt") as fh:
        rail_to_run = {r["rail_id"]: r["external_id"]
                       for r in csv.DictReader(fh, delimiter="\t")}
    with gzip.open(sra_path, "rt") as fh:
        meta = {r["external_id"]: r for r in csv.DictReader(fh, delimiter="\t")}
    samples = []
    for column, rail in enumerate(rails, start=1):
        run = rail_to_run.get(rail, "")
        row = meta.get(run, {})
        blob = row.get("sample_attributes", "")
        samples.append({
            "column": column, "rail_id": rail, "run": run,
            "sample_name": row.get("sample_name", ""),
            "sample_title": row.get("sample_title", ""),
            # Declared by the deposit. Never inferred from titles or ordering.
            "genotype": attribute(blob, "genotype"),
            "sirna_type": attribute(blob, "sirna type"),
            "cell_type": attribute(blob, "cell type"),
            "date": attribute(blob, "date"),
        })
    return samples


def run(args) -> dict:
    project_id = getattr(args, "project_id", None)
    if not project_id:
        # No fallback. Inheriting the targets file's project would label counts
        # from one experiment with the accession of another.
        raise ValueError(
            "project_id is required: the output project label must name the "
            "project actually measured, never the sealed targets file's own "
            "provenance field.")

    spec = json.loads(Path(args.targets).read_text(encoding="utf-8"))
    chromosome = spec["chromosome"]
    targets = {k: tuple(v) for k, v in spec["junctions"].items()}

    shape = assay_shape(Path(args.rr), chromosome)
    located = find_target_rows(Path(args.rr), chromosome, targets)
    row_map = {info["row"]: name for name, info in located.items()
               if info.get("row")}
    counts, header = read_counts(Path(args.mm), row_map) if row_map else ({}, {})
    samples = build_samples(Path(args.ids), Path(args.project), Path(args.sra))

    for sample in samples:
        sample["counts"] = {name: counts.get(name, {}).get(sample["column"], 0)
                            for name in targets}
        sample["meets_coverage"] = {
            name: bool(value >= args.min_coverage)
            for name, value in sample["counts"].items()}

    per_junction = {}
    for name in targets:
        values = [s["counts"][name] for s in samples]
        per_junction[name] = {
            "max": max(values) if values else 0,
            "samples_at_or_above_threshold":
                sum(1 for v in values if v >= args.min_coverage),
            "samples_with_any_read": sum(1 for v in values if v > 0),
            "located": located[name],
        }

    # The positive control exists to show the measurement works at this locus.
    # Counting it towards the gate would let a healthy control mask targets
    # with no coverage at all, so the gate is computed without it.
    control = spec.get("positive_control")
    gated = {k: v for k, v in per_junction.items() if k != control}
    verdict = {
        "min_coverage_required": args.min_coverage,
        "positive_control": control,
        "positive_control_meets_coverage": bool(
            control and per_junction[control]["samples_at_or_above_threshold"] > 0),
        "gate_junctions": sorted(gated),
        "gate_met": any(j["samples_at_or_above_threshold"] > 0
                        for j in gated.values()),
        "interpretation_rule": (
            "A count below the threshold is MISSING DATA, not a biological "
            "zero. No effect, PSI or test is computed here."),
        "gate_qualified_by_assay_shape": shape["looks_targeted_not_transcriptome_wide"],
    }
    return {
        "project": project_id,
        "targets_provenance_project": spec.get("project", ""),
        "chromosome": chromosome,
        "coordinate_conversion": "sealed intronic 0-based half-open -> [start0+1, end0] 1-based inclusive",
        "inputs": {Path(p).name: {"sha256": sha256(Path(p)),
                                  "bytes": Path(p).stat().st_size}
                   for p in (args.rr, args.mm, args.ids, args.project, args.sra)},
        "assay_shape": shape,
        "matrix_header": header,
        "n_samples": len(samples),
        "per_junction": per_junction,
        "verdict": verdict,
        "samples": samples,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    for flag in ("rr", "mm", "ids", "project", "sra", "targets"):
        ap.add_argument(f"--{flag}", required=True)
    ap.add_argument("--project-id", required=True,
                    help="Accession of the project actually measured, e.g. "
                         "SRP166282. Never defaulted from the targets file.")
    ap.add_argument("--min-coverage", type=int, default=20)
    ap.add_argument("--json", type=Path)
    args = ap.parse_args(argv)
    out = run(args)
    text = json.dumps(out, ensure_ascii=False, indent=1)
    if args.json:
        args.json.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
