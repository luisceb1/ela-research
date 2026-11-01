"""Execute the preregistered counts-ratio/PPAU check; no group inference."""
import csv
import hashlib
import json
import math
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
AUDIT = BASE / 'reports/gse296714-design-20261101'
OUT = BASE / 'reports/stmn2-papa-reproduction-20261101'


def target_matrix(handle, gene, sample_columns):
    reader = csv.DictReader(handle, delimiter='\t')
    header = reader.fieldnames or []
    if len(header) != len(set(header)) or header[:2] != ['le_id', 'gene_id']:
        raise ValueError('Missing identifiers or duplicate columns')
    if any(c not in header for c in sample_columns):
        raise ValueError('Missing library column')
    if len(sample_columns) != len(set(sample_columns)):
        raise ValueError('Duplicate requested library')
    seen, targets = set(), {}
    row_count = 0
    for row in reader:
        row_count += 1
        if None in row or any(row[c] is None for c in header):
            raise ValueError('Malformed matrix row')
        if row['le_id'] in seen:
            raise ValueError('Duplicate last-exon group')
        seen.add(row['le_id'])
        if row['gene_id'] != gene:
            continue
        values = {c: float(row[c]) for c in sample_columns}
        if any(not math.isfinite(v) or v < 0 for v in values.values()):
            raise ValueError('Invalid target value')
        targets[row['le_id']] = values
    if not targets:
        raise ValueError('Target gene absent')
    return targets, row_count


def compare(counts, ppau, samples, numerator, tolerance, author_scale):
    if set(counts) != set(ppau) or numerator not in counts:
        raise ValueError('Target groups differ or numerator absent')
    if author_scale not in (1.0, 100.0):
        raise ValueError('Unit scale must be documented as proportion or percent')
    rows = []
    for sample in samples:
        column = sample['author_label']
        values = [counts[group][column] for group in counts]
        published_values = [ppau[group][column] / author_scale for group in ppau]
        if any(v < 0 or not math.isfinite(v) for v in values):
            raise ValueError('Invalid counts')
        if any(not math.isfinite(v) or not 0 <= v <= 1 for v in published_values):
            raise ValueError('Published PPAU outside documented units')
        denominator = math.fsum(values)
        if denominator > 0 and abs(math.fsum(published_values) - 1) > tolerance:
            raise ValueError('Published target group proportions do not sum to one')
        fraction = counts[numerator][column] / denominator if denominator else None
        author_fraction = ppau[numerator][column] / author_scale
        difference = abs(fraction - author_fraction) if fraction is not None else None
        rows.append({'gsm': sample['gsm'], 'library': sample['library'],
                     'author_label': column, 'condition': sample['group'],
                     'numerator_group': numerator, 'denominator_groups': ';'.join(sorted(counts)),
                     'estimated_count_numerator': counts[numerator][column],
                     'estimated_count_denominator': denominator,
                     'counts_based_proportion': fraction,
                     'author_ppau_proportion': author_fraction,
                     'absolute_difference': difference, 'tolerance': tolerance,
                     'status': 'indeterminate' if difference is None else 'pass' if difference <= tolerance else 'fail'})
    return rows


def main():
    plan = json.loads((OUT / 'execution_plan.json').read_text())
    receipt = json.loads((OUT / 'retrieval.json').read_text())
    definition = json.loads((OUT / 'measurement_definition.json').read_text())
    if definition['unit'] != 'proportion':
        raise ValueError('This execution expects author-code-defined proportion units')
    paths = {'counts': AUDIT / 'sources/papa_counts.tsv', 'ppau': OUT / 'sources/ppau.tsv',
             'samples': AUDIT / 'samples.tsv'}
    expected = {'counts': plan['counts_sha256'], 'ppau': receipt['member_sha256'],
                'samples': json.loads((AUDIT / 'repeat_verification.json').read_text())['sha256']['samples.tsv']}
    hashes = {name: hashlib.sha256(p.read_bytes()).hexdigest() for name, p in paths.items()}
    if hashes != expected or not receipt.get('saved') or not receipt.get('crc_verified'):
        raise ValueError('Input hashes or receipt verification failed')
    with paths['samples'].open() as handle:
        samples = list(csv.DictReader(handle, delimiter='\t'))
    if len(samples) != 12:
        raise ValueError('Expected all twelve libraries')
    for key in ('gsm', 'library', 'author_label'):
        if len({r[key] for r in samples}) != len(samples):
            raise ValueError('Non-unique sample mapping')
    columns = [s['author_label'] for s in samples]
    with paths['counts'].open() as handle:
        counts, count_rows = target_matrix(handle, plan['gene_id'], columns)
    with paths['ppau'].open() as handle:
        ppau, ppau_rows = target_matrix(handle, plan['gene_id'], columns)
    tolerance = plan['absolute_tolerance_proportion_units']
    rows = compare(counts, ppau, samples, plan['numerator_group'], tolerance, author_scale=1.0)
    with (OUT / 'per_library_comparison.tsv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter='\t', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    result = {'gene': plan['gene_id'], 'numerator_group': plan['numerator_group'],
              'target_groups': sorted(counts), 'libraries': len(rows),
              'count_table_rows': count_rows, 'ppau_table_rows': ppau_rows,
              'absolute_tolerance': tolerance, 'author_units': 'proportion',
              'passed': sum(r['status'] == 'pass' for r in rows),
              'failed': sum(r['status'] == 'fail' for r in rows),
              'indeterminate': sum(r['status'] == 'indeterminate' for r in rows),
              'max_absolute_difference': max(r['absolute_difference'] for r in rows if r['absolute_difference'] is not None),
              'accepted': all(r['status'] == 'pass' for r in rows),
              'gate': 'accepted' if all(r['status'] == 'pass' for r in rows) else 'stopped_by_preregistered_rule',
              'denominator_or_tolerance_changed': False,
              'group_means_or_p_values_computed': False,
              'inputs_sha256': hashes}
    (OUT / 'result.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
