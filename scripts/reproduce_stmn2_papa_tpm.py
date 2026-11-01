"""Prospective TPM-based STMN2/PPAU reproduction, per library only."""
import csv
import hashlib
import importlib.util
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
AUDIT = BASE / 'reports/gse296714-design-20261101'
PREVIOUS = BASE / 'reports/stmn2-papa-reproduction-20261101'
OUT = BASE / 'reports/stmn2-papa-tpm-reproduction-20261101'
spec = importlib.util.spec_from_file_location('stmn2_frozen_comparison', BASE / 'scripts/reproduce_stmn2_papa.py')
shared = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shared)


def verify_inputs(paths, expected):
    hashes = {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in paths.items()}
    if hashes != expected:
        raise ValueError('Input hash mismatch')
    return hashes


def tpm_rows(rows):
    rename = {'estimated_count_numerator': 'tpm_numerator',
              'estimated_count_denominator': 'tpm_denominator',
              'counts_based_proportion': 'tpm_based_proportion'}
    return [{rename.get(k, k): v for k, v in row.items()} for row in rows]


def main():
    plan = json.loads((OUT / 'execution_plan.json').read_text())
    receipt = json.loads((OUT / 'retrieval.json').read_text())
    if not receipt.get('saved') or not receipt.get('crc_verified'):
        raise ValueError('TPM receipt is not verified')
    if receipt['member'] != plan['tpm_member']['name']:
        raise ValueError('Unexpected archive member')
    if plan['author_units'] != 'proportion':
        raise ValueError('Author units differ from the prospectively fixed definition')
    paths = {'tpm': OUT / 'sources/tpm.tsv', 'ppau': PREVIOUS / 'sources/ppau.tsv',
             'samples': AUDIT / 'samples.tsv'}
    expected = {'tpm': receipt['member_sha256'], 'ppau': plan['ppau_sha256'],
                'samples': plan['samples_sha256']}
    hashes = verify_inputs(paths, expected)
    with paths['samples'].open() as handle:
        samples = list(csv.DictReader(handle, delimiter='\t'))
    if len(samples) != plan['sample_count']:
        raise ValueError('Missing libraries')
    for key in ('gsm', 'library', 'author_label'):
        if len({row[key] for row in samples}) != len(samples):
            raise ValueError('Duplicate sample mapping')
    columns = [s['author_label'] for s in samples]
    with paths['tpm'].open() as handle:
        abundances, n_tpm = shared.target_matrix(handle, plan['gene_id'], columns)
    with paths['ppau'].open() as handle:
        ppau, n_ppau = shared.target_matrix(handle, plan['gene_id'], columns)
    rows = tpm_rows(shared.compare(abundances, ppau, samples, plan['numerator_group'],
                                   plan['absolute_tolerance'], author_scale=1.0))
    with (OUT / 'per_library_comparison.tsv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter='\t', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    result = {'gene': plan['gene_id'], 'numerator_group': plan['numerator_group'],
              'denominator_groups': sorted(abundances), 'libraries': len(samples),
              'tpm_table_rows': n_tpm, 'ppau_table_rows': n_ppau,
              'absolute_tolerance': plan['absolute_tolerance'], 'author_units': plan['author_units'],
              'passed': sum(r['status'] == 'pass' for r in rows),
              'failed': sum(r['status'] == 'fail' for r in rows),
              'indeterminate': sum(r['status'] == 'indeterminate' for r in rows),
              'max_absolute_difference': max((r['absolute_difference'] for r in rows if r['absolute_difference'] is not None), default=None),
              'accepted': all(r['status'] == 'pass' for r in rows),
              'measurement': 'last-exon-group TPM / sum of gene-group TPM; not junction PSI',
              'prior_counts_hypothesis_remains_rejected': True,
              'group_means_or_p_values_computed': False,
              'biological_independence_or_function_validated': False,
              'inputs_sha256': hashes}
    (OUT / 'result.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
