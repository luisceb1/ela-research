"""Summarize bounded public Git provenance search, not biological absence."""
import argparse,hashlib,json,platform
from pathlib import Path

TARGETS=('STMN2_annotated','STMN2_cryptic','UNC13A_annotated','UNC13A_3prime','UNC13A_5prime','UNC13A_5prime_2','UNC13A_5prime_3')

def audit(cfg):
    histories=cfg['history_metadata'];trees=cfg['sampled_trees'];scripts=cfg['inspected_script_projections']
    if len(histories)!=2 or len(trees)!=8 or len(scripts)!=5:raise ValueError('Unexpected declared search coverage')
    for h in histories:
        if h['last_page_count']>=100 or len({x['sha'] for x in h['commits']})!=len(h['commits']):raise ValueError('Incomplete or duplicated commit pagination')
    if any(t['truncated'] for t in trees):raise ValueError('Truncated historical tree cannot support bounded search')
    paths=[f['path'] for t in trees for f in t['files']]
    target='stmn2_and_unc13a.bed'
    found=[p for p in paths if Path(p).name==target]
    if found:raise ValueError('Definition found: inspect new candidate before declaring block')
    if cfg['explicit_definitions_recovered']:raise ValueError('New definition requires coordinate audit')
    refs=[dict(commit=s['commit'],blob=s['blob'],path=s['path'],**e) for s in scripts for e in s['excerpts'] if 'bed_file' in e['text'] and target in e['text']]
    if len(refs)!=2:raise ValueError('Expected two exact historical references')
    return dict(commits_with_metadata=sum(len(h['commits']) for h in histories),historical_trees_inspected=len(trees),script_versions_inspected=len(scripts),
                definition_basename=target,definition_file_found_in_sampled_trees=False,definition_references=refs,
                target_fields=list(TARGETS),fully_linked_coordinate_fields=1,exact_labels_with_strand_conflict=2,aliases_unresolved=4,
                library_run_links_previously_verified=6,new_biological_data_analyzed=False,biological_absence_inferred=False,
                source_linkage_status='blocked_pending_new_explicit_definition',all_history_or_worldwide_absence_claim=False,
                next_step='Do not repeat this search without a new source; keep SH-SY5Y seven-event reanalysis blocked and preserve completed run map')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--manifest',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    result=audit(json.loads(a.manifest.read_text()));a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    (a.out/'run.json').write_text(json.dumps(dict(date='2026-10-30',python=platform.python_version(),dependencies='stdlib',
       parent_commit='2965c6f20e2f7b6e22fb26dedced4b2658e505f9',method='Metadata and source-path evidence only; no genotype/clinical data or external code executed',
       hashes={str(x):hashlib.sha256(x.read_bytes()).hexdigest() for x in [a.manifest,Path(__file__)]}),indent=2)+'\n')
    print(json.dumps(result,indent=2))
