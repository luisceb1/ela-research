"""Offline design/count audit. No differential-expression or splicing inference."""
import csv
import gzip
import hashlib
import io
import json
import math
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'reports/gse296714-design-20261101'
TARGETS = {'ENSG00000104435': 'STMN2', 'ENSG00000130477': 'UNC13A', 'ENSG00000120948': 'TARDBP'}


def samples_from_soft(text):
    samples = []
    for section in re.split(r'(?m)^\^SAMPLE = ', text)[1:]:
        gsm = section.splitlines()[0].strip()
        fields = {}
        for line in section.splitlines()[1:]:
            if line.startswith('^'):
                break
            if line.startswith('!Sample_') and ' = ' in line:
                key, value = line.split(' = ', 1)
                fields.setdefault(key, []).append(value)
        def one(key):
            values = fields.get('!Sample_' + key, [])
            if len(values) != 1:
                raise ValueError(f'{gsm}: expected single {key}')
            return values[0]
        title = one('title')
        group = re.search(r' - (Control|Knockdown) [1-6]$', title)
        names = [v.removeprefix('Library name: ') for v in fields.get('!Sample_description', []) if v.startswith('Library name: ')]
        if not group or len(names) != 1:
            raise ValueError(f'{gsm}: ambiguous group/name')
        relations = '\n'.join(fields.get('!Sample_relation', []))
        srx = re.findall(r'SRX\d+', relations)
        samn = re.findall(r'SAMN\d+', relations)
        if len(srx) != 1 or len(samn) != 1:
            raise ValueError('Ambiguous technical identifiers')
        samples.append({'gsm': gsm, 'library': names[0],
                        'group': 'control' if group[1] == 'Control' else 'TDP43_KD',
                        'srx': srx[0], 'biosample': samn[0],
                        'cell_line': one('source_name_ch1'), 'harvest_day': 30,
                        'biological_unit_id': 'not_documented',
                        'differentiation_batch': 'not_documented', 'pair_id': 'not_documented'})
    if len(samples) != 12 or Counter(x['group'] for x in samples) != {'control': 6, 'TDP43_KD': 6}:
        raise ValueError('Unexpected sample set')
    for key in ('gsm', 'library', 'srx', 'biosample'):
        if len({x[key] for x in samples}) != len(samples):
            raise ValueError(f'Duplicate {key}')
    return samples


def audit_matrix(handle, libraries):
    reader = csv.reader(handle)
    header = next(reader)
    if header[0] != 'gene_id' or len(header[1:]) != len(set(header[1:])):
        raise ValueError('Duplicate columns or missing gene_id')
    if set(header[1:]) != set(libraries):
        raise ValueError('Matrix/sample linkage mismatch')
    totals = [0.0] * len(libraries)
    seen = set()
    stable_ids = set()
    targets = []
    fractional = 0
    for row in reader:
        if len(row) != len(header) or row[0] in seen:
            raise ValueError('Malformed row or duplicate gene')
        seen.add(row[0])
        stable = row[0].split('.')[0]
        if stable in stable_ids:
            raise ValueError('Duplicate stable gene ID')
        stable_ids.add(stable)
        values = [float(v) for v in row[1:]]
        if any(not math.isfinite(v) or v < 0 for v in values):
            raise ValueError('Nonfinite or negative abundance')
        fractional += sum(not v.is_integer() for v in values)
        totals = [a + b for a, b in zip(totals, values)]
        if stable in TARGETS:
            targets.extend({'gene': TARGETS[stable], 'gene_id': row[0], 'library': lib,
                            'estimated_gene_count': value}
                           for lib, value in zip(header[1:], values))
    if set(x['gene'] for x in targets) != set(TARGETS.values()):
        raise ValueError('Missing target')
    return {'rows': len(seen), 'sample_columns': len(header) - 1,
            'fractional_values': fractional,
            'measurement': 'Salmon/tximport estimated gene counts; not junctions or molecule counts',
            'totals': dict(zip(header[1:], totals))}, targets


def link_ena(samples, rows):
    linked = []
    for sample in samples:
        matches = [r for r in rows if r['experiment_accession'] == sample['srx']]
        if len(matches) != 1:
            raise ValueError('Non-unique SRX to run linkage')
        run = matches[0]
        if run['sample_accession'] != sample['biosample'] or run['sample_alias'] != sample['library']:
            raise ValueError('GEO/ENA identity mismatch')
        sizes = [int(x) for x in run['fastq_bytes'].split(';')]
        md5 = run['fastq_md5'].split(';')
        if run['library_layout'] != 'PAIRED' or len(sizes) != 2 or len(md5) != 2:
            raise ValueError('Expected paired-end mates')
        linked.append({**sample, 'run': run['run_accession'], 'layout': run['library_layout'],
                       'read_count_ena': int(run['read_count']), 'fastq_bytes_ena': sum(sizes),
                       'fastq_md5_r1': md5[0], 'fastq_md5_r2': md5[1]})
    if len({x['run'] for x in linked}) != len(linked):
        raise ValueError('Duplicated run')
    return linked


def write_tsv(path, rows):
    with path.open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter='\t', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def audit_papa(handle, column_map):
    reader = csv.DictReader(handle, delimiter='\t')
    header = reader.fieldnames
    if len(header) != len(set(header)) or header[:2] != ['le_id', 'gene_id'] or set(header[2:]) != set(column_map):
        raise ValueError('PAPA columns do not match author metadata')
    if len(set(column_map.values())) != len(column_map):
        raise ValueError('PAPA mapping is not one-to-one')
    seen, projected = set(), []
    for row in reader:
        if row['le_id'] in seen or None in row or any(row[x] is None for x in header):
            raise ValueError('Malformed or duplicate PAPA event')
        seen.add(row['le_id'])
        values = {c: float(row[c]) for c in header[2:]}
        if any(not math.isfinite(v) or v < 0 for v in values.values()):
            raise ValueError('Invalid PAPA abundance')
        stable = row['gene_id'].split('.')[0]
        if stable in TARGETS and TARGETS[stable] in ('STMN2', 'UNC13A'):
            projected.extend({'gene': TARGETS[stable], 'le_id': row['le_id'],
                              'author_label': c, 'library': column_map[c],
                              'estimated_pas_group_count': v} for c, v in values.items())
    return {'rows': len(seen), 'columns': len(column_map),
            'target_groups': sorted({r['le_id'] for r in projected}),
            'measurement': 'PAPA/Salmon estimated last-exon-group abundance; not direct junction support'}, projected


def target_annotations(text):
    rows = []
    for line in text.splitlines():
        if line.startswith('#') or not line.strip():
            continue
        fields = line.split('\t')
        if len(fields) != 9:
            raise ValueError('Malformed GTF')
        attrs = dict(re.findall(r'(\w+) "([^"]*)"', fields[8]))
        if attrs.get('gene_id', '').split('.')[0] in TARGETS and attrs.get('gene_name') in ('STMN2', 'UNC13A'):
            rows.append({'gene': attrs['gene_name'], 'le_id': attrs['le_id'],
                         'chromosome': fields[0], 'start_1based': int(fields[3]),
                         'end_1based_inclusive': int(fields[4]), 'strand': fields[6],
                         'transcript_id': attrs['transcript_id'],
                         'event_type': attrs.get('event_type', ''),
                         'simple_event_type': attrs.get('simple_event_type', '')})
    return rows


def main():
    sources = ROOT / 'sources'
    expected = {}
    for receipt in sorted(ROOT.glob('retrievals*.json')):
        for row in json.loads(receipt.read_text()):
            if row.get('saved') and row.get('name') and row.get('sha256'):
                expected.setdefault(row['name'], set()).add(row['sha256'])
            if row.get('saved') and row.get('member_sha256'):
                name = ('papa_counts.tsv' if row['member'].endswith('summarised_pas_quantification.counts.tsv')
                        else 'cryptic_annotation.gtf' if row['member'].endswith('.gtf')
                        else 'humphrey_sample_table.csv')
                expected.setdefault(name, set()).add(row['member_sha256'])
    required = ['family.soft', 'ena.tsv', 'gene_counts_geo.csv.gz', 'humphrey_sample_table.csv', 'papa_counts.tsv', 'cryptic_annotation.gtf']
    hashes = {}
    for name in required:
        digest = hashlib.sha256((sources / name).read_bytes()).hexdigest()
        if expected.get(name) != {digest}:
            raise ValueError(f'Missing, changed, or conflicting source hash: {name}')
        hashes[name] = digest
    samples = samples_from_soft((sources / 'family.soft').read_text())
    ena_rows = list(csv.DictReader(io.StringIO((sources / 'ena.tsv').read_text()), delimiter='\t'))
    linked = link_ena(samples, ena_rows)
    with gzip.open(sources / 'gene_counts_geo.csv.gz', 'rt') as handle:
        counts, targets = audit_matrix(handle, [x['library'] for x in samples])
    author = list(csv.DictReader(io.StringIO((sources / 'humphrey_sample_table.csv').read_text())))
    for sample in samples:
        matches = [r for r in author if Path(r['path']).name == sample['library'] + '.bam']
        if len(matches) != 1 or matches[0]['condition'] != ('CTRL' if sample['group'] == 'control' else 'TDP'):
            raise ValueError('Author metadata mismatch')
        sample['author_label'] = matches[0]['sample_name']
    if len(author) != 12:
        raise ValueError('Unexpected author sample set')
    with (sources / 'papa_counts.tsv').open() as handle:
        papa, papa_targets = audit_papa(handle, {s['author_label']: s['library'] for s in samples})
    annotations = target_annotations((sources / 'cryptic_annotation.gtf').read_text())
    current_ids = {s[k] for s in linked for k in ('gsm', 'srx', 'biosample', 'run')}
    overlaps = []
    for p in sorted((ROOT / 'baseline').glob('*')):
        data = p.read_bytes()
        previous_ids = set(re.findall(r'(?:GSM|SRX|SAMN|SRR|ERR)\d+', data.decode()))
        overlaps.append({'baseline': p.name, 'sha256': hashlib.sha256(data).hexdigest(),
                         'explicit_ids': len(previous_ids), 'shared_ids': sorted(current_ids & previous_ids)})
    result = {'samples': len(samples), 'groups': dict(Counter(s['group'] for s in samples)),
              'ena_project_rows': len(ena_rows), 'ena_selected_runs': len(linked),
              'ena_fastq_bytes_selected': sum(x['fastq_bytes_ena'] for x in linked),
              'ena_read_count_selected': sum(x['read_count_ena'] for x in linked),
              'author_metadata_linked': len(samples), 'matrix': counts,
              'papa': papa, 'target_annotation_rows': len(annotations),
              'overlap_check': overlaps, 'independence_certified': False,
              'inference': 'not_executed', 'junction_coverage': 'not_measured',
              'gate': 'descriptive_gene_and_PAS_group_counts; reconstruct biological units before inference; no direct junction measurement'}
    write_tsv(ROOT / 'samples.tsv', [{**x, 'author_label': samples[i]['author_label']} for i, x in enumerate(linked)])
    write_tsv(ROOT / 'target_gene_counts.tsv', targets)
    write_tsv(ROOT / 'target_pas_group_counts.tsv', papa_targets)
    write_tsv(ROOT / 'target_annotations.tsv', annotations)
    (ROOT / 'results.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    (ROOT / 'input_hashes.json').write_text(json.dumps(hashes, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
