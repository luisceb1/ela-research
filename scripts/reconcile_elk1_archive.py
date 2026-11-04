"""Compare selectively retrieved final-paper-linked ELK1 files with the pinned replay."""
import argparse
import csv
import hashlib
import io
import json
from fractions import Fraction as F
from pathlib import Path
import reproduce_elk1_fish as replay

EXTRA_HASHES = {
    'processed/2023-10-13_fish_counts_processed.tsv': 'fc31a31d5ba6f6617a06c4c9d6ce314d5e1017e862af9158068d9583b8c6d34f',
    'processed/2023-10-13_fish_counts_cleaned_longer.tsv': '059061e571cbf094c54e890d1dde8e9a1b6cb0ec447827a4be79ccb66dac008a',
    'fish_plot.R': '612fb79845fc2c190fd0bc6717ce8ad25311abd89832dcc3322264f00873cc43',
}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--wet-dir', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path)
    args = p.parse_args()
    hashes = {**{'data/'+k:v for k,v in replay.HASHES.items()}, **EXTRA_HASHES}
    data = {}
    for name, sha in hashes.items():
        data[name] = (args.wet_dir/name).read_bytes()
        if hashlib.sha256(data[name]).hexdigest() != sha:
            raise ValueError('Archive member hash mismatch: '+name)
    raw = replay.read_counts(data['data/fish_counts_cleaned.tsv'])
    summaries = replay.aggregate(raw)
    summary_map = {(r['replicate'],r['arm'],r['probe']):r for r in summaries}
    fields = {'sum_nuclei':lambda r:2*r['nuclei'],
              'sum_foci':lambda r:r['nuclear_foci']+r['extranuclear_foci'],
              'mean_cell':lambda r:r['source_pivot_mean'],
              'sum_foci_extranuclear':lambda r:r['extranuclear_foci'],
              'sum_foci_nuclear':lambda r:r['nuclear_foci'],
              'extranuc_nuc_ratio':lambda r:F(r['extranuclear_foci'],r['nuclear_foci']),
              'nuc_extranuc_ratio':lambda r:r['pooled_nuclear_extranuclear']}
    processed = list(csv.DictReader(io.StringIO(data['processed/2023-10-13_fish_counts_processed.tsv'].decode()), delimiter='\t'))
    keys = [(r['replicate'],r['condition'],r['probe']) for r in processed]
    if len(keys)!=12 or len(set(keys))!=12 or set(keys)!=set(summary_map):
        raise ValueError('Processed summary keys differ')
    checks = []
    for r in processed:
        calculated=summary_map[r['replicate'],r['condition'],r['probe']]
        for field,fn in fields.items():
            actual,expected=fn(calculated),F(r[field])
            checks.append(dict(replicate=r['replicate'],arm=r['condition'],probe=r['probe'],
                field=field,calculated=actual,archive=expected,
                difference=actual-expected,matches_1e_12=abs(actual-expected)<F(1,10**12)))
    longer = list(csv.DictReader(io.StringIO(data['processed/2023-10-13_fish_counts_cleaned_longer.tsv'].decode()), delimiter='\t'))
    expected_long = {(r['replicate'],r['arm'],str(int(r['image'][len(r['arm']):])),probe,region):
                     (r['n_nuclei'],r[probe+'_'+region])
                     for r in raw for probe in replay.PROBES for region in ['nuclear','extranuclear']}
    actual_long = {(r['replicate'],r['condition'],r['image'],r['probe'],r['region']):
                   (int(r['n_nuclei']),int(r['n_foci'])) for r in longer}
    if len(longer)!=240 or len(actual_long)!=240 or actual_long!=expected_long:
        raise ValueError('Archived long table differs from source pivot')
    image_rows=[dict(replicate=r['replicate'],arm=r['arm'],image=r['image'],probe=probe,
                     extranuclear_foci=r[probe+'_extranuclear']) for r in raw for probe in replay.PROBES]
    endpoint=[]
    for rep in ['1','2','3']:
        for probe in replay.PROBES:
            ctrl=summary_map[rep,'CTRL',probe]['mean_extranuclear_foci_per_image']
            kd=summary_map[rep,'TDP',probe]['mean_extranuclear_foci_per_image']
            endpoint.append(dict(replicate=rep,probe=probe,images_per_arm=10,
                control_mean_extranuclear_foci=ctrl,KD_mean_extranuclear_foci=kd,
                KD_over_control=kd/ctrl))
    comparisons=replay.compare_deposited({k:data['data/'+k] for k in replay.HASHES},replay.fold_changes(summaries))
    args.output.mkdir(exist_ok=True,parents=True)
    for name,rows in [('processed-table-comparison.csv',checks),('fig3g-image-counts.csv',image_rows),
                      ('fig3g-endpoint.csv',endpoint)]:
        replay.write_table(args.output/name,rows)
    result=dict(archive_member_sha256=hashes,summary_numeric_fields=len(checks),
        summary_fields_matching=sum(x['matches_1e_12'] for x in checks),long_rows_matching=240,
        long_numeric_counts_matching=480,github_data_and_plot_bytes_match=True,
        deposited_ratio_matches=sum(x['matches_1e_8'] for x in comparisons),deposited_ratio_count=9,
        final_paper_linked_input_verified=True,editorial_plot_point_identity_verified=False,
        pvalues_estimated=False,R_executed=False,independent_culture_map_verified=False)
    (args.output/'reconciliation-run.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__': main()
