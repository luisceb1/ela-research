"""Replay pinned ELK1 FISH count aggregation; never establishes rescue or independence."""
import argparse
import csv
import hashlib
import io
import json
import re
import statistics
import sys
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

HASHES = {
    'fish_counts_cleaned.tsv': 'e68958d7400487a5a718a491c1c4b5d99a29a4e6dfb4941f6b5bff5108b65ea7',
    'number_foci_ratio.csv': '7f52429817bbb91dfc41707f9c0cc3cac023db57089330a314a4c3a094ae5f73',
    'nuclear_cyto_ratio.csv': '927507899e023a3f515a209b2f29e62217171ddf4803c88d5750f752ec91dd8f',
}
PROBES = ('proximal', 'distal')
COUNT_FIELDS = ('n_nuclei', 'proximal_nuclear', 'proximal_extranuclear',
                'distal_nuclear', 'distal_extranuclear')


def read_counts(data):
    reader = csv.DictReader(io.StringIO(data.decode('utf-8-sig')), delimiter='\t')
    if reader.fieldnames != ['replicate', 'condition', 'image', *COUNT_FIELDS]:
        raise ValueError('Unexpected count header')
    rows, seen = [], set()
    for raw in reader:
        if None in raw or any(x is None for x in raw.values()):
            raise ValueError('Malformed row')
        match = re.fullmatch(r'(CTRL|TDP)([1-9][0-9]*)', raw['condition'])
        if not match or raw['image'] != raw['condition']:
            raise ValueError('Unresolved image/condition identity')
        key = (raw['replicate'], raw['image'])
        if key in seen or not raw['replicate']:
            raise ValueError('Duplicate or missing image identity')
        seen.add(key)
        row = {**raw, 'arm': match[1]}
        for name in COUNT_FIELDS:
            if not re.fullmatch(r'[0-9]+', raw[name]):
                raise ValueError('Counts must be nonnegative integers')
            row[name] = int(raw[name])
        if row['n_nuclei'] == 0:
            raise ValueError('Zero nuclei denominator')
        rows.append(row)
    if not rows:
        raise ValueError('Empty image table')
    return rows


def divide(a, b):
    return F(a, b) if b else None


def aggregate(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[row['replicate'], row['arm']].append(row)
    output = []
    for (replicate, arm), images in sorted(groups.items()):
        nuclei = sum(r['n_nuclei'] for r in images)
        for probe in PROBES:
            nuc = sum(r[probe + '_nuclear'] for r in images)
            extra = sum(r[probe + '_extranuclear'] for r in images)
            image_ratios = [divide(r[probe + '_nuclear'], r[probe + '_extranuclear'])
                            for r in images]
            output.append(dict(replicate=replicate, arm=arm, probe=probe,
                n_images=len(images), nuclei=nuclei, nuclear_foci=nuc, extranuclear_foci=extra,
                source_pivot_mean=F(nuc + extra, 2 * nuclei),
                pooled_per_nucleus=F(nuc + extra, nuclei),
                equal_image_per_nucleus=statistics.mean(
                    F(r[probe + '_nuclear'] + r[probe + '_extranuclear'], r['n_nuclei'])
                    for r in images),
                pooled_nuclear_extranuclear=divide(nuc, extra),
                equal_image_nuclear_extranuclear=(statistics.mean(image_ratios)
                    if all(v is not None for v in image_ratios) else None),
                mean_extranuclear_foci_per_image=F(extra, len(images))))
    return output


METRICS = ('source_pivot_mean', 'pooled_per_nucleus', 'equal_image_per_nucleus',
           'pooled_nuclear_extranuclear', 'equal_image_nuclear_extranuclear',
           'mean_extranuclear_foci_per_image')


def fold_changes(summary):
    lookup = {(r['replicate'], r['arm'], r['probe']): r for r in summary}
    output = []
    for rep in sorted({r['replicate'] for r in summary}):
        for probe in PROBES:
            if any((rep, c, probe) not in lookup for c in ('CTRL', 'TDP')):
                raise ValueError('Missing within-replicate control arm')
            control, kd = (lookup[rep, c, probe] for c in ('CTRL', 'TDP'))
            row = dict(replicate=rep, probe=probe)
            for metric in METRICS:
                a, b = kd[metric], control[metric]
                row[metric] = a / b if a is not None and b not in (None, 0) else None
            output.append(row)
    return output


def compare_deposited(snapshots, folds):
    lookup = {(r['replicate'], r['probe']): r for r in folds}
    out = []
    for filename, metric in [('number_foci_ratio.csv', 'equal_image_per_nucleus'),
                             ('nuclear_cyto_ratio.csv', 'equal_image_nuclear_extranuclear')]:
        reader = csv.DictReader(io.StringIO(snapshots[filename].decode('utf-8-sig')))
        for row in reader:
            if not re.fullmatch('N[123]', row['replicate']):
                raise ValueError('Unexpected deposited replicate label')
            rep = row['replicate'][1:]
            for color, probe in [('Green', 'proximal'), ('Red', 'distal')]:
                if color not in row:
                    continue
                deposited = F(row[color])
                computed = lookup[rep, probe][metric]
                out.append(dict(file=filename, replicate=rep, probe=probe, metric=metric,
                    deposited=deposited, computed=computed,
                    difference=computed-deposited if computed is not None else None,
                    matches_1e_8=computed is not None and abs(computed-deposited) <= F(1, 10**8)))
    return out


def write_table(path, rows):
    with path.open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows({k:float(v) if isinstance(v, F) else v for k,v in r.items()} for r in rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    snapshots = {}
    for name, sha in HASHES.items():
        snapshots[name] = (args.source_dir/name).read_bytes()
        if hashlib.sha256(snapshots[name]).hexdigest() != sha:
            raise ValueError('Source SHA256 mismatch: '+name)
    rows = read_counts(snapshots['fish_counts_cleaned.tsv'])
    summary = aggregate(rows)
    if len(rows) != 60 or len(summary) != 12 or any(r['n_images'] != 10 for r in summary):
        raise ValueError('Pinned experimental grid differs')
    folds = fold_changes(summary)
    comparisons = compare_deposited(snapshots, folds)
    sensitivity = []
    for probe in PROBES:
        values = {r['replicate']: r['equal_image_per_nucleus'] for r in folds if r['probe']==probe}
        for omitted in (None, *sorted(values)):
            kept = [v for k,v in values.items() if k != omitted]
            sensitivity.append(dict(probe=probe, omitted_replicate=omitted,
                n_source_replicates=len(kept), arithmetic_mean_fold=statistics.mean(kept)))
    args.output.mkdir(parents=True, exist_ok=True)
    for name, data in [('replicate-summary.csv', summary), ('fold-changes.csv', folds),
                       ('deposited-comparison.csv', comparisons), ('sensitivity.csv', sensitivity)]:
        write_table(args.output/name, data)
    receipt = dict(source_sha256=HASHES, python=sys.version, source_images=len(rows),
        source_replicate_labels=sorted({r['replicate'] for r in rows}),
        comparisons=len(comparisons), matches=sum(r['matches_1e_8'] for r in comparisons),
        source_nuclei_doubled_by_pivot=True,
        fold_changes_invariant_to_factor_two=all(r['source_pivot_mean']==r['pooled_per_nucleus'] for r in folds),
        undefined_localization_groups=sum(r['equal_image_nuclear_extranuclear'] is None for r in summary),
        R_executed=False, pvalues_estimated=False, functional_rescue_estimated=False,
        independent_donor_or_differentiation_map_verified=False)
    (args.output/'run.json').write_text(json.dumps(receipt, indent=2, sort_keys=True)+'\n')
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
