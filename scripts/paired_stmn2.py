"""Exploratory paired analysis; technical metadata stays transient, export aggregates."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import platform
import statistics
from audit_stmn2_units import read_table, build_index, join_samples

PREPS = {'Manual KAPA Total', 'Automated KAPA Total'}


def sign_test(differences):
    positive = sum(d > 0 for d in differences)
    negative = sum(d < 0 for d in differences)
    n = positive + negative
    return min(1.0, 2 * sum(math.comb(n, k) for k in range(min(positive, negative) + 1)) / 2**n) if n else None


def select_pairs(left, right, group, threshold):
    # Count multiplicity BEFORE response/coverage filtering.
    buckets = []
    for records in (left, right):
        by_donor = defaultdict(list)
        for row in records:
            by_donor[row['donor']].append(row)
        buckets.append(by_donor)
    a, b = buckets
    exclusions = Counter()
    selected = []
    common = set(a) & set(b)
    for donor in sorted(common):
        if len(a[donor]) != 1 or len(b[donor]) != 1:
            exclusions['multiplicity'] += 1
            continue
        x, y = a[donor][0], b[donor][0]
        if x['group'] != group or y['group'] != group:
            exclusions['not_target_group_in_both'] += 1
            continue
        if x['prep'] not in PREPS or y['prep'] not in PREPS:
            exclusions['unknown_preparation'] += 1
            continue
        if x['prep'] != y['prep']:
            exclusions['preparation_mismatch'] += 1
            continue
        if min(x['c'] + x['k'], y['c'] + y['k']) < threshold:
            exclusions['insufficient_total_denominator'] += 1
            continue
        selected.append((x, y))
    return selected, {'common_declared_donors_before_filters':len(common), 'exclusions_in_order':dict(exclusions)}


def summarize(pairs, inference=False):
    differences = [y['k']/(y['c']+y['k']) - x['k']/(x['c']+x['k']) for x,y in pairs]
    n = len(differences)
    pos, neg = sum(d>0 for d in differences), sum(d<0 for d in differences)
    gate = n >= 10 and pos+neg >= 5
    out = {'n_pairs':n, 'cervical_higher':pos, 'ties':n-pos-neg, 'cervical_lower':neg,
           'median_paired_difference':statistics.median(differences) if n else None,
           'preparation_strata':dict(Counter(x['prep'] for x,y in pairs)),
           'coverage':{}}
    for region, index in [('cortex',0),('cervical',1)]:
        records = [pair[index] for pair in pairs]
        out['coverage'][region] = {'canonical_median':statistics.median(r['c'] for r in records) if n else None,
                                  'total_median':statistics.median(r['c']+r['k'] for r in records) if n else None}
    if inference:
        out['primary_gate_passed'] = gate
        out['two_sided_exact_sign_p'] = sign_test(differences) if gate else None
        out['prediction_median_positive'] = out['median_paired_difference'] > 0 if gate else None
    return out


def linked_records(samples, projects, author, jung, region):
    first, f = join_samples(samples, projects, *author, region, 'Target ALS')
    second, g = join_samples(samples, projects, *jung, region, 'Target ALS PM core')
    result = []
    mismatches = 0
    for sample in samples:
        key = str(sample['rail_id'])
        if key not in first or key not in second:
            continue
        if first[key]['donor'] != second[key]['donor']:
            mismatches += 1
            continue
        result.append({'donor':first[key]['donor'], 'group':sample['group'],
                       'prep':second[key]['extra'][1], 'c':sample['counts']['canonical'], 'k':sample['counts']['cryptic']})
    return result, {'samples':len(samples),'matched_both_agreeing':len(result),'donor_disagreements':mismatches,
                    'author_join_failures':dict(f),'jung_join_failures':dict(g)}


def run(root):
    root = Path(root)
    repo = root/'repo'
    paths = [root/'project_global.source',root/'author_map.source',root/'jung_table.source',
             repo/'reports/stmn2-derivation-20261111/results_corteza.json',repo/'reports/stmn2-derivation-20261111/results_cervical.json']
    projects = read_table(paths[0], '\t')
    author = build_index(read_table(paths[1], ','), ('sample_id_rna','sample'), 'external_subject_id','rna_tissue_source',('project',))
    jung = build_index(read_table(paths[2], '\t'), ('sample_id_alt',), 'subject_id','tissue',('project','libprep'))
    records, joins = [], {}
    for name,path,region in [('cortex',paths[3],'Cortex_Motor_Lateral'),('cervical',paths[4],'Spinal_Cord_Cervical')]:
        rows, summary = linked_records(json.loads(path.read_text())['samples'], projects, author, jung, region)
        records.append(rows);joins[name]=summary
    out = {'evidence':'exploratory paired association in previously inspected cohort; no independent replication',
           'hashes':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
           'python':platform.python_version(),'joins':joins,'analyses':{}}
    for group in ['ALS Spectrum MND','Non-Neurological Control']:
        summaries = {}
        for threshold in [20,50,100]:
            pairs, selection = select_pairs(*records, group, threshold)
            summaries[str(threshold)] = {'selection':selection, 'summary':summarize(pairs, inference=group=='ALS Spectrum MND' and threshold==20)}
        out['analyses'][group] = summaries
    return out


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-root',required=True)
    p.add_argument('--output',required=True)
    args=p.parse_args()
    result=run(args.source_root)
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.output).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(result['analyses'],indent=2))
