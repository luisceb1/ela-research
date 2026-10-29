#!/usr/bin/env python3
"""Descriptive within-series contrasts only; no p-values or pseudoreplication."""
import csv
import json
import math
import platform
import sys
from collections import defaultdict
from datetime import datetime, timezone
from functools import reduce
from pathlib import Path

try:
    from scripts import geo_audit as a
except ModuleNotFoundError:
    import geo_audit as a

OUT = a.ROOT / 'reports/descriptive'


def ratio(numerator, denominator):
    return numerator / denominator if denominator > 0 else ''


def mean(values):
    return sum(values) / len(values)


def loo_summary(group, controls):
    """Finite leave-one-library-out mean ratios; these are NOT CIs."""
    if min(len(group), len(controls)) < 2:
        raise ValueError('At least two libraries per deposited group required')
    ratios = [ratio(mean(group), mean(controls))]
    ratios += [ratio(mean(group[:i] + group[i+1:]), mean(controls)) for i in range(len(group))]
    ratios += [ratio(mean(group), mean(controls[:i] + controls[i+1:])) for i in range(len(controls))]
    finite = [r for r in ratios if r != '']
    return {'mean_ratio_to_CTL': ratios[0], 'sensitivity_ratio_min': min(finite) if finite else '',
            'sensitivity_ratio_max': max(finite) if finite else '',
            'undefined_ratios': len(ratios) - len(finite),
            'direction_spans_one': bool(finite and min(finite) < 1 < max(finite))}


def load_tsv(path):
    with path.open() as f:
        return list(csv.DictReader(f, delimiter='\t'))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    errors = []
    try:
        mapping_root = a.ROOT / 'reports/isoforms'
        if json.loads((mapping_root / 'run.json').read_text())['status'] != 'generated':
            raise ValueError('Successful isoform mapping required')
        targets = load_tsv(mapping_root / 'transcripts.tsv')
        sample_rows = load_tsv(a.OUT / 'samples.tsv')
        sources = json.loads((a.OUT / 'sources.json').read_text())
        values_rows, culture, brain, scale = [], [], [], []
        for gse, label in a.SERIES.items():
            selection = {r['txname']: r['symbol'] for r in targets if r['gse'] == gse}
            smap = {r['column']: r['group_label'] for r in sample_rows if r['gse'] == gse}
            for measure, suffix in [('uniqueCounts', 'uniqueCounts'), ('counts', 'counts')]:
                name = f'{gse}_{label}_isoseq_{suffix}_transcript.txt.gz'
                path = a.DATA / name
                if a.sha256(path.read_bytes()) != sources[name]['source_sha256']:
                    raise ValueError(f'Input changed: {name}')
                totals, selected, gcd = None, {}, None
                gene_sums = defaultdict(list)
                for header, tx, gene, vals in a.count_rows(path):
                    if totals is None:
                        totals, gcd = [0.] * len(vals), [0] * len(vals)
                    for i, v in enumerate(vals):
                        totals[i] += v
                        if measure == 'uniqueCounts':
                            if not v.is_integer():
                                raise ValueError('Fractional uniqueCounts: GCD interpretation invalid')
                            gcd[i] = math.gcd(gcd[i], int(v))
                    if tx in selection:
                        selected[tx] = vals
                        symbol = selection[tx]
                        if not gene_sums[symbol]:
                            gene_sums[symbol] = [0.] * len(vals)
                        for i, v in enumerate(vals):
                            gene_sums[symbol][i] += v
                columns = header[2:]
                if set(columns) != set(smap) or set(selected) != set(selection):
                    raise ValueError('Unexpected columns/target IDs')
                if measure == 'uniqueCounts':
                    scale += [{'gse': gse, 'column': c, 'nonzero_count_gcd': gcd[i],
                               'interpretation': 'count_scale_only_not_independent_molecules'} for i, c in enumerate(columns)]
                for tx, vals in selected.items():
                    symbol = selection[tx]
                    metrics = {'raw': vals, 'per_million_assigned': [ratio(v*1e6, totals[i]) for i, v in enumerate(vals)],
                               'share_of_gene_assigned': [ratio(v, gene_sums[symbol][i]) for i, v in enumerate(vals)]}
                    for metric, vector in metrics.items():
                        for i, v in enumerate(vector):
                            values_rows.append({'gse': gse, 'symbol': symbol, 'txname': tx, 'measure': measure,
                                                'metric': metric, 'column': columns[i], 'value': v})
                        if gse == 'GSE310723':
                            for aza in ['5Aza', 'noAza']:
                                ci = columns.index(f'i3N_Ctrl_{aza}_hg38_minimap2')
                                ki = columns.index(f'i3N_TDP43KD_{aza}_hg38_minimap2')
                                cv, kv = vector[ci], vector[ki]
                                culture.append({'symbol': symbol, 'txname': tx, 'measure': measure, 'metric': metric, 'arm': aza,
                                    'control_value': cv, 'kd_value': kv, 'kd_to_control_ratio': ratio(kv, cv) if cv != '' and kv != '' else '',
                                    'direction': 'undefined' if cv == '' or kv == '' else 'higher' if kv > cv else 'lower' if kv < cv else 'equal'})
                        else:
                            controls = [v for i, v in enumerate(vector) if smap[columns[i]] == 'CTL']
                            for group in ['ALS', 'ALS-ci', 'ALS-C9']:
                                group_values = [v for i, v in enumerate(vector) if smap[columns[i]] == group]
                                # A missing denominator invalidates the metric; do not drop samples silently.
                                missing = any(v == '' for v in group_values + controls)
                                summary = {'mean_ratio_to_CTL': '', 'sensitivity_ratio_min': '', 'sensitivity_ratio_max': '',
                                           'undefined_ratios': 5, 'direction_spans_one': False} if missing else loo_summary(group_values, controls)
                                brain.append({'symbol': symbol, 'txname': tx, 'measure': measure, 'metric': metric, 'group': group,
                                    'n_group_libraries': len(group_values), 'n_CTL_libraries': len(controls),
                                    'group_mean': '' if missing else mean(group_values), 'group_min': '' if missing else min(group_values),
                                    'group_max': '' if missing else max(group_values), 'CTL_mean': '' if missing else mean(controls), **summary})
        for filename, rows in [('values.tsv', values_rows), ('culture_contrasts.tsv', culture), ('brain_sensitivity.tsv', brain), ('count_scale.tsv', scale)]:
            a.tsv(OUT / filename, rows, list(rows[0]))
        print(f'{len(culture)} culture contrasts; {len(brain)} brain sensitivity rows. No statistical inference.')
    except Exception as exc:
        errors.append({'type': type(exc).__name__, 'message': str(exc)})
    finally:
        a.dump_json(OUT / 'errors.json', errors)
        a.dump_json(OUT / 'run.json', {'utc': datetime.now(timezone.utc).isoformat(), 'python': platform.python_version(),
            'argv': sys.argv, 'randomness': 'none', 'inference': 'none; leave-one-out ranges are not confidence intervals',
            'status': 'failed' if errors else 'generated'})
    if errors:
        print(errors, file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
