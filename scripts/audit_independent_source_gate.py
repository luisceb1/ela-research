"""Audit three published culture sources without computing biological effects.

stdlib for metadata; --parquet additionally requires pyarrow==21.0.0.
Original inputs stay outside git. Only public accessions, published culture
conditions, technical fields and aggregate integrity QC are exported.
"""
import argparse
import collections
import csv
import gzip
import hashlib
import json
from pathlib import Path
import platform
import re
import struct
import tarfile


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def checked_sources(cache, manifest):
    for source in manifest['sources']:
        path = cache / source['cache_file']
        if digest(path) != source['sha256']:
            raise ValueError('source hash mismatch: ' + source['id'])


def soft_samples(text):
    out = []
    seen = set()
    for block in text.split('^SAMPLE = ')[1:]:
        lines = block.splitlines()
        gsm = lines[0].strip()
        if gsm in seen or not re.fullmatch(r'GSM\d+', gsm):
            raise ValueError('duplicate or invalid GSM')
        seen.add(gsm)
        fields = collections.defaultdict(list)
        for line in lines[1:]:
            if ' = ' in line:
                k, v = line.split(' = ', 1)
                if k in {'!Sample_title', '!Sample_source_name_ch1',
                         '!Sample_data_processing', '!Sample_relation'}:
                    fields[k].append(v)
        out.append({'gsm': gsm, 'fields': dict(fields)})
    return out


def collapse_sdrf(rows):
    """Paired FASTQ rows are not biological replicates; retain contradictions."""
    by_assay = {}
    for row in rows:
        assay = row['Assay Name']
        record = {
            'assay': assay,
            'run': row['Comment[ENA_RUN]'],
            'experiment': row['Comment[ENA_EXPERIMENT]'],
            'sample_accession': row['Comment[ENA_SAMPLE]'],
            'derived_file': row['Derived Array Data File'],
            'cell_line': row['Characteristics[cell line]'],
            'compartment': row['Factor Value[organism part]'],
            'stimulus': row['Factor Value[stimulus]'],
        }
        if assay in by_assay and by_assay[assay] != record:
            raise ValueError('inconsistent SDRF rows for assay')
        by_assay[assay] = record
    if len({r['run'] for r in by_assay.values()}) != len(by_assay):
        raise ValueError('run assigned to multiple assays')
    return sorted(by_assay.values(), key=lambda x: x['assay'])


def sdrf_conflicts(records):
    conflicts = []
    files = collections.defaultdict(list)
    for r in records:
        files[r['derived_file']].append(r['run'])
        m = re.search(r'_(cytosol|nucleus)_', r['derived_file'])
        if not m or m[1] != r['compartment']:
            conflicts.append({'run': r['run'], 'derived_file': r['derived_file'],
                              'source_compartment': r['compartment'],
                              'file_compartment': m[1] if m else None})
    collisions = {k: sorted(v) for k, v in files.items() if len(v) > 1}
    return conflicts, collisions


def link_processed_keys(keys, records):
    """Exact normalized deposited filenames only; never repair a compartment."""
    by_file = collections.defaultdict(list)
    for r in records:
        key = r['derived_file'].removesuffix('.quant.sf').lower()
        by_file[key].append(r['run'])
    return [{'processed_key': key, 'runs': sorted(by_file.get(key, [])),
             'status': ('unmatched' if not by_file.get(key) else
                        'unique' if len(by_file[key]) == 1 else 'ambiguous')}
            for key in sorted(keys)]


def ready(candidate):
    required = ('public_attributable', 'direct_junction_counts',
                'event_identity_linked', 'independent_units_documented',
                'perturbation_control_documented', 'new_experimental_source')
    checks = candidate['criteria']
    missing = [k for k in required if checks.get(k) is not True]
    # A numeric library count does not supply the missing independence evidence.
    if candidate.get('minimum_independent_units_per_condition', 0) < 3:
        missing.append('minimum_independent_units_per_condition')
    return not missing, missing


def parquet_qc(path):
    import pyarrow as pa
    import pyarrow.compute as pc
    import pyarrow.parquet as pq
    t = pq.read_table(path)
    count = t['uniquely_mapping']
    if not pa.types.is_integer(count.type) or count.null_count:
        raise ValueError('junction counts must be non-null integers')
    if pc.any(pc.less(count, 0)).as_py():
        raise ValueError('negative junction count')
    cols = ['tdp_kd', 'nmdi', 'compartment', 'sample', 'sample_2']
    libs = t.select(cols).group_by(cols).aggregate([]).to_pylist()
    for r in libs:
        if '_'.join(str(r[x]) for x in cols[:-1]) != r['sample_2']:
            raise ValueError('sample key contradicts technical group')
    grouped = t.select(['junction', 'sample_2', 'uniquely_mapping']).group_by(
        ['junction', 'sample_2']).aggregate([('uniquely_mapping', 'count')])
    duplicated_keys = pc.sum(pc.greater(grouped['uniquely_mapping_count'], 1)).as_py()
    if duplicated_keys:
        raise ValueError('duplicate sample/junction keys; never sum implicitly')
    return {
        'rows': t.num_rows, 'columns': t.column_names, 'libraries': len(libs),
        'groups': sorted(libs, key=lambda r: r['sample_2']),
        'negative_counts': 0, 'null_counts': 0,
        'explicit_zero_rows': pc.sum(pc.equal(count, 0)).as_py(),
        'duplicate_sample_junction_keys': duplicated_keys,
        'strand_column_present': 'strand' in t.column_names,
        'missing_combinations_filled': False,
        'pyarrow_version': pa.__version__,
        'scope': 'Integrity only; no target effects, PSI or inferential statistics',
    }


def run(cache, manifest, parquet=False):
    checked_sources(cache, manifest)
    pointer = (cache/'cryptic_biology_star_pointer.txt').read_text()
    oid = re.search(r'^oid sha256:([a-f0-9]{64})$', pointer, re.M)
    size = re.search(r'^size (\d+)$', pointer, re.M)
    payload = cache/'fractionation_parquet.source'
    if not oid or not size or int(size[1]) != payload.stat().st_size or oid[1] != digest(payload):
        raise ValueError('LFS pointer does not match actual Parquet payload')
    ma = soft_samples(gzip.decompress((cache/'ma_family.source').read_bytes()).decode())
    mel = soft_samples(gzip.decompress((cache/'melamed_family.source').read_bytes()).decode())
    selected = []
    for r in mel:
        title = r['fields']['!Sample_title'][0]
        if re.fullmatch(r'si(?:Control|TDP-43) [123]', title):
            relations = ' '.join(r['fields'].get('!Sample_relation', []))
            srx = re.search(r'SRX\d+', relations)
            if not srx:
                raise ValueError('selected culture lacks SRA experiment')
            selected.append({'gsm': r['gsm'], 'published_group': title,
                             'experiment': srx[0]})
    ena = list(csv.DictReader((cache/'melamed_ena.source').read_text().splitlines(), delimiter='\t'))
    selection = {r['experiment']: r for r in selected}
    runs = []
    for r in ena:
        if r['experiment_accession'] in selection:
            runs.append({**selection[r['experiment_accession']], 'run': r['run_accession'],
                         'fastq_bytes': sum(int(v) for v in r['fastq_bytes'].split(';')),
                         'read_count': int(r['read_count']), 'base_count': int(r['base_count'])})
    if len(runs) != 6 or len({r['run'] for r in runs}) != 6:
        raise ValueError('six unique selected Melamed runs required')
    with tarfile.open(cache/'ma_tar.source') as tar:
        members = tar.getmembers()
        if len(members) != 12 or not all(m.isfile() and m.name.endswith('.bw') for m in members):
            raise ValueError('unexpected Ma processed archive members')
        for m in members:
            # Read header in memory; never extract an external tar to disk.
            h = tar.extractfile(m).read(64)
            if len(h) != 64 or struct.unpack('<I', h[:4])[0] != 0x888FFC26:
                raise ValueError('invalid BigWig header')
    raw = list(csv.DictReader((cache/'fractionation_sdrf_resolved.source').read_text().splitlines(), delimiter='\t'))
    records = collapse_sdrf(raw)
    conflicts, collisions = sdrf_conflicts(records)
    projection = {
        'ma': {'gsm': [r['gsm'] for r in ma], 'libraries': len(ma),
               'processed_files': 12, 'format': 'BigWig coverage; not direct junction counts',
               'independence': 'iMN1/2/3 and rep1/2 are labels; unit hierarchy not certified'},
        'melamed_selected_runs': sorted(runs, key=lambda r: r['gsm']),
        'melamed_fastq_bytes_total': sum(r['fastq_bytes'] for r in runs),
        'melamed_processed_format': 'RSEM gene TPM, per GEO deposit; not junction counts',
        'fractionation': {
            'sdrf_rows': len(raw), 'libraries': len(records),
            'unique_derived_filenames': len({r['derived_file'] for r in records}),
            'metadata': records, 'compartment_conflicts': conflicts,
            'derived_file_collisions': collisions,
            'explicit_unit_or_batch_headers': [h for h in raw[0] if re.search(r'replicate|batch', h, re.I)],
            'independent_culture_units_certified': False,
            'lfs_payload_sha256_verified': oid[1],
        },
        'decisions': [],
    }
    candidates = manifest['candidates']
    if len(candidates) > 3 or len({c['accession'] for c in candidates}) != len(candidates):
        raise ValueError('candidate cap or unique accession violated')
    for c in candidates:
        ok, missing = ready(c)
        projection['decisions'].append({'accession': c['accession'],
                                        'decision': 'accepted' if ok else 'not_ready_this_cycle',
                                        'unmet_or_unknown': missing})
    if parquet:
        qc = parquet_qc(cache/'fractionation_parquet.source')
        projection['fractionation']['parquet_qc'] = qc
        projection['fractionation']['filename_links'] = link_processed_keys(
            [r['sample_2'] for r in qc['groups']], records)
    return projection


def main():
    a = argparse.ArgumentParser(description=__doc__)
    a.add_argument('--cache', type=Path, required=True)
    a.add_argument('--manifest', type=Path, required=True)
    a.add_argument('--out', type=Path, required=True)
    a.add_argument('--parquet', action='store_true')
    args = a.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    try:
        m = json.loads(args.manifest.read_text())
        result = run(args.cache, m, args.parquet)
        (args.out/'results.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
        (args.out/'errors.json').write_text('[]\n')
        (args.out/'run.json').write_text(json.dumps({
            'python': platform.python_version(), 'platform': platform.platform(),
            'manifest_sha256': digest(args.manifest), 'script_sha256': digest(__file__),
            'parameters': vars(args) | {'cache': str(args.cache), 'manifest': str(args.manifest),
                                        'out': str(args.out)},
            'randomness': 'none', 'raw_alignment_executed': False,
            'effect_analysis_executed': False,
        }, indent=2)+'\n')
        print(json.dumps({'candidates': len(result['decisions']),
                          'accepted': sum(r['decision']=='accepted' for r in result['decisions']),
                          'results_sha256': digest(args.out/'results.json')}))
    except Exception as e:
        (args.out/'errors.json').write_text(json.dumps([{'error': type(e).__name__, 'message': str(e)}], indent=2)+'\n')
        raise


if __name__ == '__main__':
    main()
