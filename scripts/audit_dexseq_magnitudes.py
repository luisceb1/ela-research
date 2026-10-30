"""Audit published aggregate count fractions; no statistical inference."""
import argparse
import csv
import hashlib
import json
import math
import platform
from collections import defaultdict
from pathlib import Path

GENES = {'STMN2': ('ENSG00000104435', 10), 'UNC13A': ('ENSG00000130477', 62), 'TARDBP': ('ENSG00000120948', 30)}
THRESHOLDS = (0, 0.01, 0.1, 0.5)

def classify(a, b, threshold):
    if not all(math.isfinite(x) for x in (a, b, threshold)) or threshold < 0:
        raise ValueError('Invalid magnitude/threshold')
    if a == 0 or b == 0 or min(abs(a), abs(b)) < threshold:
        return 'below_threshold_or_zero'
    return 'same_direction' if (a > 0) == (b > 0) else 'opposite_direction'

def audit(rows):
    groups = defaultdict(dict)
    for row in rows:
        gene, frag, batch = (row[x] for x in ('gene', 'fragment', 'batch'))
        if gene not in GENES or not frag.startswith(GENES[gene][0] + ':E') or batch not in ('Batch 1', 'Batch 2'):
            raise ValueError('Unknown gene/fragment/batch')
        n = 2 if batch == 'Batch 1' else 4
        if any(int(row[x]) != n for x in ('scramble_libraries', 'KD_libraries')):
            raise ValueError('Unexpected technical library counts')
        key = (gene, frag)
        if batch in groups[key]:
            raise ValueError('Duplicate fragment/batch')
        c, k, d = (float(row[x]) for x in ('mean_control_count_fraction', 'mean_KD_count_fraction', 'change_percentage_points'))
        if not all(math.isfinite(x) for x in (c, k, d)) or not (0 <= c <= 1 and 0 <= k <= 1):
            raise ValueError('Invalid fraction')
        if not math.isclose(d, 100*(k-c), abs_tol=1e-10, rel_tol=1e-10):
            raise ValueError('Delta inconsistent with fractions')
        groups[key][batch] = (c, k, d)
    for gene, (_, expected) in GENES.items():
        gs = [b for (g, f), b in groups.items() if g == gene]
        if len(gs) != expected or any(set(b) != {'Batch 1', 'Batch 2'} for b in gs):
            raise ValueError('Missing fragments/batches')
        for batch in ('Batch 1', 'Batch 2'):
            for i in (0, 1):
                if not math.isclose(math.fsum(b[batch][i] for b in gs), 1, abs_tol=1e-10):
                    raise ValueError('Fractions do not close to one')
    fragments = []
    for (gene, frag), bs in sorted(groups.items()):
        a, b = bs['Batch 1'][2], bs['Batch 2'][2]
        fragments.append(dict(gene=gene, fragment=frag, delta_batch1_pp=a, delta_batch2_pp=b,
                              minimum_absolute_delta_pp=min(abs(a), abs(b)), maximum_absolute_delta_pp=max(abs(a), abs(b)),
                              **{'class_at_' + str(t) + '_pp': classify(a, b, t) for t in THRESHOLDS}))
    summary = {}
    for gene in GENES:
        fs = [f for f in fragments if f['gene'] == gene]
        summary[gene] = {'fragments': len(fs), 'thresholds_pp': {str(t): {label: sum(f['class_at_' + str(t) + '_pp'] == label for f in fs) for label in ('same_direction', 'opposite_direction', 'below_threshold_or_zero')} for t in THRESHOLDS},
                         'total_variation_pp': {b: 0.5 * math.fsum(abs(bs[b][2]) for (g, f), bs in groups.items() if g == gene) for b in ('Batch 1', 'Batch 2')}}
    return fragments, summary

def main(source, out):
    with source.open() as f:
        rows = list(csv.DictReader(f, delimiter='\t'))
    fragments, summary = audit(rows)
    out.mkdir(parents=True, exist_ok=True)
    with (out/'fragment_magnitudes.tsv').open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(fragments[0]), delimiter='\t', lineterminator='\n'); w.writeheader(); w.writerows(fragments)
    (out/'summary.json').write_text(json.dumps(summary, indent=2, allow_nan=False)+'\n')
    files = [source, Path(__file__)]
    (out/'run.json').write_text(json.dumps(dict(python=platform.python_version(), date='2026-10-30', parent_commit='18abfa5477ec78e937590fcc929bd44157a22a39', thresholds_pp=THRESHOLDS, rows=len(rows), fragments=len(fragments), hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}, method='Threshold min(abs(delta1),abs(delta2)); inclusive boundaries; no inference; aggregate input only'), indent=2)+'\n')
    print(json.dumps(summary, indent=2))

if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--source', type=Path, required=True); p.add_argument('--out', type=Path, required=True)
    a = p.parse_args(); main(a.source, a.out)
