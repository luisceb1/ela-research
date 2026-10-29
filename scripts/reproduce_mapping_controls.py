"""Hash-pinned technical reconciliation of gene selection; no sample-level export."""
import argparse
import csv
import gc
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import re

try:
    from scripts import map_isoseq_gtf as mapper
except ModuleNotFoundError:
    import map_isoseq_gtf as mapper

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_rows(path):
    with path.open() as f:
        return list(csv.DictReader(f, delimiter="\t"))


def verify_reference(cache):
    reference = json.loads(mapper.REFERENCE_PATH.read_text())
    path = cache / "gencode.v47.annotation.gtf.gz"
    if digest(path) != reference["source_sha256"]:
        raise ValueError("GENCODE reference hash mismatch")
    found = {}
    with gzip.open(path, "rt") as f:
        for line in f:
            if "\tgene\t" not in line:
                continue
            row = line.rstrip("\n").split("\t")
            attr = mapper.attrs(row[8])
            symbol = attr.get("gene_name")
            if symbol not in reference["panel"]:
                continue
            record = {"gene_id": attr["gene_id"].split(".")[0], "chrom": row[0], "strand": row[6]}
            if record != reference["panel"][symbol]:
                raise ValueError("Reference symbol/ID/locus disagreement")
            if symbol in found:
                raise ValueError("Ambiguous reference gene")
            found[symbol] = record
    if set(found) != set(reference["panel"]):
        raise ValueError("Missing reference gene")
    return {"source_sha256": reference["source_sha256"], "panel_verified": found}


def baseline(path, name):
    if path is None:
        return None
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cache", type=Path, required=True)
    p.add_argument("--baseline-current", type=Path)
    p.add_argument("--baseline-historical", type=Path)
    p.add_argument("--prior-transcripts", type=Path)
    args = p.parse_args()
    out = ROOT / "reports/mapping-positive-controls"
    out.mkdir(parents=True, exist_ok=True)
    source_manifest = json.loads((ROOT / "research/references/geo_isoseq_sources_20261029.json").read_text())
    sources = []
    # Verify all four public inputs before analyzing either dataset.
    for name, source in source_manifest.items():
        if digest(args.cache / name) != source["source_sha256"]:
            raise ValueError("GEO input hash mismatch: " + name)
        sources.append({"file": name, "sha256": source["source_sha256"], "bytes": (args.cache / name).stat().st_size, "url": source["url"]})
    baselines = {"main_before_hardening": baseline(args.baseline_current, "baseline_main"),
                 "historical_name_only": baseline(args.baseline_historical, "baseline_old")}
    result = {"scope": "technical selection reproduction, not independent biology", "sources": sources,
              "reference": verify_reference(args.cache), "datasets": {},
              "baseline_comparison_method": "same validated GTF index; unchanged baseline map_counts functions",
              "baseline_source_sha256": {name: digest(path) for name, path in [("main_before_hardening", args.baseline_current), ("historical_name_only", args.baseline_historical)] if path is not None}}
    prior = {}
    if args.prior_transcripts:
        for row in read_rows(args.prior_transcripts):
            prior[(row["gse"], row["txname"])] = (row["symbol"], int(row["n_exons"]), float(row["sum_unique_counts"]))
        result["prior_transcripts_sha256"] = digest(args.prior_transcripts)
    for gse, label in [("GSE310723", "i3N"), ("GSE315972", "NYGC")]:
        index = mapper.index_gtf(args.cache / f"{gse}_{label}_isoseq_extended_annotations.gtf.gz")
        counts = args.cache / f"{gse}_{label}_isoseq_uniqueCounts_transcript.txt.gz"
        output = out / f"{gse}_targets.tsv"
        summary = mapper.map_counts(counts, index, output, set(mapper.GENE_IDS))
        mapper.check_summary(summary, set(mapper.GENE_IDS))
        rows = read_rows(output)
        entry = {"hardened": summary, "output_sha256": digest(output), "baseline_summaries": {}}
        for name, module in baselines.items():
            if module is None:
                continue
            target = out / f"{gse}_{name}.tsv"
            entry["baseline_summaries"][name] = module.map_counts(counts, index, target, set(mapper.GENE_IDS))
            if name == "main_before_hardening":
                entry["main_output_identical_bytes"] = target.read_bytes() == output.read_bytes()
                if not entry["main_output_identical_bytes"]:
                    raise ValueError("Hardening changed real target output; review discrepancy")
        if args.prior_transcripts:
            actual = {(gse, r["TXNAME"]): (r["gene_name"], int(r["n_exons"]), float(r["counts_sum"])) for r in rows}
            expected = {k: v for k, v in prior.items() if k[0] == gse}
            entry["matches_prior_isoform_ids_symbols_exon_counts_and_sums"] = actual == expected
            if actual != expected:
                raise ValueError("Prior branch differs from current target output")
        result["datasets"][gse] = entry
        del index
        gc.collect()
    result["python"] = platform.python_version()
    result["individual_rows_exported"] = False
    (out / "reproduction.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({gse: entry["hardened"] for gse, entry in result["datasets"].items()}))


if __name__ == "__main__":
    main()
