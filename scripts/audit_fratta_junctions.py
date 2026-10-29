"""Audit published junction-index transformations; export aggregate values only."""
import argparse
import collections
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import re
import statistics as st
import zipfile
try:
    from scripts.reproduce_issue14_aggregates import signflip
except ModuleNotFoundError:
    from reproduce_issue14_aggregates import signflip

LABELS = {'STMN2_cryptic', 'STMN2_annotated', 'UNC13A_3prime', 'UNC13A_5prime', 'UNC13A_5prime_2', 'UNC13A_annotated'}
PINS = {'source.bed': ('b9a46c7e4f388d1e871a293b0b6da5c7ae5689ace7fc82d8ead38d3e41a6b447', '89de715d8640382800cef959be064b3af8e76eee'),
        'paper_figures.Rmd': ('3c46c164af6572bef28507b707f39d996d687abb06da00bf5468f89d0d491502', '1534a7312bcee102fae9a60bb450ddd37da5c96c')}


def parse(text):
    rows = []
    for line in text.splitlines():
        p = line.split('\t')
        if len(p) != 7 or p[6] not in LABELS or p[5] not in ('+', '-'):
            raise ValueError('Unexpected BED7 structure/label/strand')
        if int(p[1]) < 0 or int(p[2]) <= int(p[1]) or int(p[4]) < 0:
            raise ValueError('Invalid coordinates/count')
        rows.append(tuple(p))
    if not rows:
        raise ValueError('Empty junction source')
    return rows


def sample_identity(sample):
    m = re.fullmatch(r'((?:FTD|FTD_ALS)_S[1-7])_TDP_43_(positive|negative)\.SJ\.out', sample)
    if m:
        return m[1], 'TP' if m[2] == 'positive' else 'TN'
    if re.fullmatch(r'(?:FTD|FTD_ALS)_S[1-7]_unsorted\.SJ\.out', sample):
        return None, 'unsorted'
    raise ValueError('Unknown technical sample label; do not assign condition by default')


def pivot(rows, naive_sum=False):
    table, geometries = {}, {}
    for p in rows:
        sample_identity(p[3])
        key = p[3], p[6]
        geom = p[0], p[1], p[2], p[5]
        if key in geometries and not naive_sum:
            raise ValueError('Multiple distinct records for sample/class; pivot ambiguous')
        geometries[key] = geom
        row = table.setdefault(p[3], {label: 0 for label in LABELS})
        row[p[6]] += int(p[4])
    return table


def ratio(row, gene, include_second=True):
    cryptic = row['STMN2_cryptic'] if gene == 'STMN2' else row['UNC13A_3prime'] + row['UNC13A_5prime'] + (row['UNC13A_5prime_2'] if include_second else 0)
    canonical = row[gene + '_annotated']
    denominator = cryptic + canonical
    return (cryptic / denominator if denominator else None), denominator


def summarize(table, gene, formula, include_second=True):
    pairs = collections.defaultdict(dict)
    for sample, row in table.items():
        unit, condition = sample_identity(sample)
        if condition == 'unsorted':
            continue
        if condition in pairs[unit]:
            raise ValueError('Duplicated technical condition')
        pairs[unit][condition] = ratio(row, gene, include_second)
    if len(pairs) != 7 or {p.rsplit('_', 1)[1] for p in pairs} != {f'S{i}' for i in range(1, 8)} or any(set(p) != {'TP', 'TN'} for p in pairs.values()):
        raise ValueError('Seven complete pairs required')
    tp = [pairs[p]['TP'][0] for p in sorted(pairs)]
    tn = [pairs[p]['TN'][0] for p in sorted(pairs)]
    if any(x is None for x in tp + tn):
        raise ValueError('Zero denominator is not index zero or an eligible pair')
    delta = [b - a for a, b in zip(tp, tn)]
    result = {'gene': gene, 'formula': formula, 'n_pairs': 7, 'mean_TP': st.mean(tp), 'mean_TN': st.mean(tn),
        'mean_delta_percentage_points': 100 * st.mean(delta), 'median_delta_percentage_points': 100 * st.median(delta),
        'TN_min': min(tn), 'TN_max': max(tn), 'increasing_pairs': sum(x > 0 for x in delta),
        'min_TP_junction_denominator': min(p['TP'][1] for p in pairs.values()),
        'min_TN_junction_denominator': min(p['TN'][1] for p in pairs.values()), 'exploratory_signflip_p': signflip(delta)}
    return result, delta


def write(path, records):
    with path.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(records[0]), delimiter='\t', lineterminator='\n');w.writeheader();w.writerows(records)


def run(cache, upload, out):
    for name, (pin, blob) in PINS.items():
        raw = (cache / name).read_bytes()
        if hashlib.sha256(raw).hexdigest() != pin or hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() != blob:
            raise ValueError('Pinned public source changed')
    rmd = (cache / 'paper_figures.Rmd').read_text().splitlines()
    required = {2686: 'unique()', 2690: 'values_fill = 0', 2694: 'UNC13A_5prime_2', 2766: 'UNC13A_5prime'}
    if any(token not in rmd[line - 1] for line, token in required.items()) or 'UNC13A_5prime_2' in rmd[2765]:
        raise ValueError('Rmd formula localizers differ')
    rows = parse((cache / 'source.bed').read_text());unique = sorted(set(rows));table = pivot(unique)
    if len(table) != 16 or len(rows) != 241 or len(unique) != 69:
        raise ValueError('Published input shape changed')
    main, deltas, alternatives = [], {}, []
    from scipy.stats import wilcoxon
    for gene in ['STMN2', 'UNC13A']:
        r, delta = summarize(table, gene, 'Rmd_2693_2694_three_UNC13A_classes')
        r['exploratory_wilcoxon_exact_p'] = float(wilcoxon(delta, alternative='two-sided', method='exact').pvalue)
        main.append(r);deltas[gene] = delta
    alternative, _ = summarize(table, 'UNC13A', 'Rmd_2766_two_UNC13A_classes', False);alternatives.append(alternative)
    naive = pivot(rows, naive_sum=True)
    for gene in ['STMN2', 'UNC13A']:
        r, _ = summarize(naive, gene, 'counterexample_sum_duplicate_rows');alternatives.append(r)
    packages = list(upload.glob('*reanalisis_02_splicing*.zip'))
    if len(packages) != 1:
        raise ValueError('Expected exactly one received splicing package')
    with zipfile.ZipFile(packages[0]) as z:
        expected_raw = z.read('resultados/resumen_splicing.csv')
    expected = list(csv.DictReader(io.StringIO(expected_raw.decode())))
    mapping = {'n_pares': 'n_pairs', 'psi_TP_media': 'mean_TP', 'psi_TN_media': 'mean_TN',
        'diferencia_media_puntos_porcentuales': 'mean_delta_percentage_points',
        'diferencia_mediana_puntos_porcentuales': 'median_delta_percentage_points',
        'rango_psi_TN_min': 'TN_min', 'rango_psi_TN_max': 'TN_max', 'pares_TN_mayor': 'increasing_pairs',
        'p_exacta_perm_signos_bilateral': 'exploratory_signflip_p', 'p_wilcoxon_exacto_bilateral': 'exploratory_wilcoxon_exact_p',
        'cobertura_minima_uniones_TP': 'min_TP_junction_denominator', 'cobertura_minima_uniones_TN': 'min_TN_junction_denominator'}
    comparisons = []
    for old in expected:
        new = next(r for r in main if r['gene'] == old['gen'])
        for before, after in mapping.items():
            x, y = float(old[before]), new[after]
            comparisons.append({'gene': old['gen'], 'field': before, 'expected': x, 'observed': y,
                                'agrees': math.isclose(x, y, rel_tol=1e-8, abs_tol=1e-8)})
    if any(not r['agrees'] for r in comparisons):
        raise ValueError('Received aggregate summary differs')
    out.mkdir(parents=True, exist_ok=True)
    write(out / 'aggregate_indices.tsv', main);write(out / 'sensitivity.tsv', alternatives);write(out / 'comparison.tsv', comparisons)
    summary = {'raw_rows': len(rows), 'unique_rows': len(unique), 'exact_duplicate_rows_removed': len(rows) - len(unique),
        'technical_samples': len(table), 'paired_samples': 14, 'independent_pairs_not_new_cohort': 7, 'unsorted_excluded': 2,
        'observed_sample_class_cells': len(unique), 'zero_filled_missing_cells_per_author_pivot': len(table) * 6 - len(unique),
        'explicit_zero_count_source_rows': sum(int(r[4]) == 0 for r in unique),
        'unique_rows_per_label': dict(collections.Counter(r[6] for r in unique)),
        'raw_rows_per_label': dict(collections.Counter(r[6] for r in rows)), 'sample_class_pivot_collisions': 0,
        'duplicate_multiplicity_per_label': {label: sorted({n for row, n in collections.Counter(rows).items() if row[6] == label}) for label in sorted(LABELS)},
        'numeric_fields_compared': len(comparisons), 'comparison_mismatches': 0,
        'Rmd_primary_formula_lines': [2685, 2694], 'Rmd_alternative_formula_line': 2766,
        'expected_aggregate_sha256': hashlib.sha256(expected_raw).hexdigest(),
        'package_sha256': hashlib.sha256(packages[0].read_bytes()).hexdigest(),
        'coordinate_convention_converted': False, 'allelic_or_clinical_files_read': False, 'individual_rows_exported': False,
        'interpretation': 'Read-junction indices and formula sensitivity, not molecular isoform fractions, function, titration or new replication'}
    (out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')


if __name__ == '__main__':
    p = argparse.ArgumentParser();p.add_argument('--cache', type=Path, required=True);p.add_argument('--upload', type=Path, required=True)
    p.add_argument('--out', type=Path, default=Path('reports/fratta-junction-audit'))
    args = p.parse_args();run(args.cache, args.upload, args.out)
