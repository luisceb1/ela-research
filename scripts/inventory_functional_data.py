"""Render a curated availability inventory, never infer missing experimental IDs."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

REQUIRED = ('unit_key', 'biological_batch_key', 'observation_time', 'first_dose_link',
            'paired_baseline', 'post_deficit_start', 'aligned_control', 'functional_outcome')
KNOWN_OTHER_TIMING = {'concurrent', 'preinjury', 'immediate_postinjury', 'pretreated_before_KD'}


def assess(record):
    evidence = record['verified']
    if set(evidence) != set(REQUIRED):
        raise ValueError('Explicit tri-state evidence required for each reconstruction field')
    if any(v is not None and type(v) is not bool for v in evidence.values()):
        raise ValueError('Use true/false/null, not counts or labels as proof')
    if not record.get('locator') or not record.get('version'):
        raise ValueError('Source locator and version required')
    blockers = [k + (':not_verified' if evidence[k] is None else ':missing_in_inspected_projection')
                for k in REQUIRED if evidence[k] is not True]
    if record['timing'] in KNOWN_OTHER_TIMING:
        blockers.append('timing:not_target_post_deficit_contrast')
    if record['data_access'] != 'retrieved':
        blockers.append('data_access:not_retrieved')
    ready = not blockers
    return {'id': record['id'], 'reconstructible_from_inspected_materials': ready,
            'blockers': blockers, 'reported_numeric_entries_are_biological_n': False}


def render(data, out):
    ids = [r['id'] for r in data['records']]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate inventory record')
    results = [assess(r) for r in data['records']]
    out.mkdir(parents=True, exist_ok=True)
    with (out / 'inventory.tsv').open('w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['id', 'version', 'data_access', 'timing', *REQUIRED, 'reconstructible', 'blockers', 'locator'])
        for r, a in zip(data['records'], results):
            w.writerow([r['id'], r['version'], r['data_access'], r['timing'],
                        *['unknown' if r['verified'][k] is None else str(r['verified'][k]).lower() for k in REQUIRED],
                        str(a['reconstructible_from_inspected_materials']).lower(), ';'.join(a['blockers']), r['locator']])
    summary = {'date': data['date'], 'scope': data['scope'], 'records': len(results),
               'reconstructible': sum(r['reconstructible_from_inspected_materials'] for r in results),
               'results': results, 'effects_estimated': False, 'novelty_certified': False,
               'interpretation': 'Inspected projections only; not proof no other data exist'}
    (out / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    return summary


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--register', type=Path, default=Path('research/references/functional_data_inventory_20261029.json'))
    p.add_argument('--out', type=Path, default=Path('reports/functional-data-inventory'))
    a = p.parse_args()
    raw = a.register.read_bytes()
    result = render(json.loads(raw), a.out)
    result['register_sha256'] = hashlib.sha256(raw).hexdigest()
    (a.out / 'summary.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
