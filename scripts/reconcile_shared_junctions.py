"""Reconcile catalog/support/streaming effects without individual-count exports."""
import argparse
import ast
from collections import Counter
import csv
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_shared_junctions import junction_index, stable
from research.prototypes import junction_streaming_legacy as legacy


def reduced_counts(path):
    """Preserve summed zero/nonzero support, discarding column identities."""
    rows, seen = {}, set()
    with gzip.open(path, "rt") as f:
        reader = csv.DictReader(f, delimiter="\t")
        if not {"TXNAME", "GENEID"}.issubset(reader.fieldnames or []):
            raise ValueError("Missing count identity fields")
        columns = [k for k in reader.fieldnames if k not in {"TXNAME", "GENEID"}]
        for row in reader:
            tx = row["TXNAME"]
            if tx in seen:
                raise ValueError("Duplicate transcript")
            seen.add(tx)
            if not tx.startswith("BambuTx"):
                continue
            values = [float(row[c]) for c in columns]
            if any(not math.isfinite(v) or v < 0 or v != int(v) for v in values):
                raise ValueError("Invalid uniqueCounts; no integer truncation allowed")
            rows[tx] = (stable(row["GENEID"]), (sum(values),))
    return rows


def blocks(gtf, rows):
    """Count exon-bearing runs under the legacy contiguous-record assumption."""
    counts, current, has_exons = Counter(), None, False
    with gzip.open(gtf, "rt") as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) != 9 or p[2] not in {"transcript", "exon"}:
                continue
            tx = legacy.attr_value(p[8], "transcript_id")
            if tx != current:
                current, has_exons = tx, False
            if p[2] == "exon" and tx in rows and rows[tx][0].startswith("ENSG") and not has_exons:
                counts[tx] += 1
                has_exons = True
    return counts


def expressed_keys(novel, rows):
    return {key for key, txs in novel.items() if any(sum(rows[tx][1]) > 0 for tx in txs)}


def flatten_legacy(index):
    return {(gene, chrom, start, end, strand) for gene, js in index.items()
            for chrom, start, end, strand in js}


def packaged_keys(path):
    with zipfile.ZipFile(path) as z:
        name = next(n for n in z.namelist() if n.endswith('/uniones_compartidas_todas.csv'))
        rows = list(csv.DictReader(io.StringIO(z.read(name).decode("utf-8-sig"))))
        keys = {(r["gene_id"], r["chrom"], int(r["intron_start"]), int(r["intron_end"]), r["strand"]) for r in rows}
        if len(keys) != len(rows):
            raise ValueError("Duplicate packaged structural keys")
        return keys


def verify_excerpts(inventory):
    source = Path(legacy.__file__).read_text()
    segments = {node.name: ast.get_source_segment(source, node) for node in ast.parse(source).body if isinstance(node, ast.FunctionDef)}
    for record in inventory['reviewed_function_excerpts']:
        if hashlib.sha256(segments[record['function']].encode()).hexdigest() != record['source_segment_sha256']:
            raise ValueError('Legacy source excerpt changed')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cache", type=Path, required=True)
    p.add_argument("--original-zip", type=Path, help="Optional exact ZIP identity recheck; default uses pinned safe structural projection")
    args = p.parse_args()
    out = ROOT / 'reports/junction-filter-reconciliation'
    out.mkdir(parents=True, exist_ok=True)
    inv = json.loads((out / 'source_inventory.json').read_text())
    if args.original_zip and hashlib.sha256(args.original_zip.read_bytes()).hexdigest() != inv['sha256']:
        raise ValueError('Original package hash mismatch')
    verify_excerpts(inv)
    projection = ROOT / inv['safe_projection']['path']
    if hashlib.sha256(projection.read_bytes()).hexdigest() != inv['safe_projection']['sha256']:
        raise ValueError('Structural projection hash mismatch')
    with projection.open() as f:
        projected_rows = list(csv.DictReader(f, delimiter='\t'))
    package = {(r['gene_id'], r['chrom'], int(r['intron_start']), int(r['intron_end']), r['strand']) for r in projected_rows}
    if len(package) != len(projected_rows) or len(package) != inv['safe_projection']['rows']:
        raise ValueError('Structural projection duplicate/row mismatch')
    if args.original_zip and package != packaged_keys(args.original_zip):
        raise ValueError('Projection does not match original ZIP')
    pinned = json.loads((ROOT / 'research/references/geo_isoseq_sources_20261029.json').read_text())
    for name, source in pinned.items():
        if hashlib.sha256((args.cache / name).read_bytes()).hexdigest() != source['source_sha256']:
            raise ValueError('GEO source hash mismatch')
    data, qc = {}, {}
    for gse, label in [('GSE310723','i3N'), ('GSE315972','NYGC')]:
        gtf = args.cache / f'{gse}_{label}_isoseq_extended_annotations.gtf.gz'
        rows = reduced_counts(args.cache / f'{gse}_{label}_isoseq_uniqueCounts_transcript.txt.gz')
        novel, reference = junction_index(gtf, rows)
        old_models, old_stats = legacy.parse_bambu(gtf, rows)
        old_keys = flatten_legacy(legacy.tx_junctions(old_models))
        run_counts = blocks(gtf, rows)
        data[gse] = {'catalog':set(novel), 'positive':expressed_keys(novel,rows),
                     'reference':reference, 'legacy':old_keys}
        qc[gse] = {'Bambu_count_rows':len(rows),
                   'Bambu_positive_sum_rows':sum(sum(v[1])>0 for v in rows.values()),
                   'Bambu_models_with_multiple_exon_runs':sum(n>1 for n in run_counts.values()),
                   'legacy_models_with_junctions':sum(bool(v[1]) for v in old_models.values()),
                   'grouped_models_with_junctions':len({tx for txs in novel.values() for tx in txs}),
                   'legacy_positive_junctions':len(old_keys), 'grouped_catalog_junctions':len(novel),
                   'grouped_positive_junctions':len(data[gse]['positive']),
                   'legacy_parser_counters_per_run_not_unique_transcript':old_stats}
        print(json.dumps({'dataset':gse,'qc':qc[gse]}),flush=True)
    a,b = data.values()
    reference = a['reference'] | b['reference']
    catalog_raw = a['catalog'] & b['catalog']
    catalog = catalog_raw - reference
    positive_raw = a['positive'] & b['positive']
    positive = positive_raw - reference
    old = a['legacy'] & b['legacy']
    legacy_targets = {}
    for gene, chrom, start, end, strand in old:
        legacy_targets.setdefault(gene, set()).add((chrom, start, end, strand))
    legacy_reference = set()
    for gse, label in [('GSE310723','i3N'), ('GSE315972','NYGC')]:
        found = legacy.internal_ref(args.cache / f'{gse}_{label}_isoseq_extended_annotations.gtf.gz', legacy_targets)
        legacy_reference.update((gene, *junction) for gene, junction in found)
    old_after_reference = old - legacy_reference
    if any(k[2] > k[3] for k in package | catalog):
        raise ValueError('Invalid intronic interval in compared output')
    results = {'scope':'structural/QC reconciliation, not clinical or biological inference',
               'source_zip_sha256':inv['sha256'], 'datasets':qc,
               'legacy_source_excerpts_verified':len(inv['reviewed_function_excerpts']),
               'original_zip_verified_this_run':args.original_zip is not None,
               'safe_projection_verified':True,
               'gene_counts':{'grouped_catalog_after_ENST':len({k[0] for k in catalog}),
                              'grouped_positive_after_ENST':len({k[0] for k in positive}),
                              'packaged':len({k[0] for k in package})},
               'stages':{'grouped_shared_before_ENST':len(catalog_raw),
                         'grouped_shared_after_ENST':len(catalog),
                         'positive_shared_before_ENST':len(positive_raw),
                         'positive_shared_after_ENST':len(positive),
                         'legacy_positive_shared_before_ENST':len(old),
                         'legacy_positive_shared_after_ENST':len(old_after_reference),
                         'packaged_shared':len(package)},
               'comparison':{'legacy_keys_equal_packaged_keys':old_after_reference==package,
                             'packaged_in_grouped_catalog_after_ENST':len(package & catalog),
                             'packaged_in_grouped_positive_after_ENST':len(package & positive),
                             'packaged_in_grouped_reference':len(package & reference),
                             'packaged_in_legacy_reference':len(package & legacy_reference),
                             'packaged_not_a_grouped_Bambu_intersection':len(package-catalog_raw),
                             'catalog_only_count':len(catalog-package),
                             'positive_filter_removed_from_1910_catalog':len(catalog-positive)},
               'individual_counts_exported':False,'pvalues_computed':False}
    with (out/'structural_membership.tsv').open('w') as f:
        fields=['gene_id','chrom','intron_start','intron_end','strand','packaged_21','grouped_catalog_after_ENST','grouped_positive_after_ENST','in_grouped_ENST_reference']
        w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(fields)
        for key in sorted(package|catalog):
            w.writerow([*key,key in package,key in catalog,key in positive,key in reference])
    (out/'reconciliation.json').write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
    print(json.dumps(results['stages']),flush=True)
    print(json.dumps(results['comparison']),flush=True)


if __name__=='__main__':
    main()
