"""Culture-only schema/provenance inventory; never estimates biological effects."""
import argparse
import csv
import hashlib
import json
import platform
import re
from collections import Counter
from pathlib import Path

COUNTS=('UNC13A_annotated','UNC13A_3prime','UNC13A_5prime','UNC13A_5prime_2','UNC13A_5prime_3','STMN2_annotated','STMN2_cryptic')

def source_group(value):
    return value.replace('\\n','\n').splitlines()[0].strip()

def ready(record):
    return all(record.get(x) is True for x in ('file_inspected','junction_fields_verified','coordinate_link_verified','unit_map_verified','independent_units_verified','editorial_identity_verified')) and not record.get('reused',False)

def validate(record):
    if record.get('clinical_data_used',False):raise ValueError('Clinical data not allowed')
    if record.get('ready_for_external_reanalysis',False)!=ready(record):raise ValueError('Unsupported readiness claim')
    if record.get('reused',False) and record.get('independent_units_verified',False):raise ValueError('Reused units cannot become independent')
    return record

def inspect(rows,expected):
    if len(rows)!=42 or len({r['sample'] for r in rows})!=42:raise ValueError('Unexpected/duplicate culture rows')
    allowed={g['source_label']:g for g in expected};out=[]
    for r in rows:
        if source_group(r['source']) not in allowed or r['condition'] not in ('control','TDP-43 KD'):raise ValueError('Unknown culture group/condition')
        for k in COUNTS:
            if not re.fullmatch(r'[0-9]+',r[k]):raise ValueError('Count is not nonnegative integer literal')
    for g in expected:
        selected=[r for r in rows if source_group(r['source'])==g['source_label']]
        c=Counter(r['condition'] for r in selected)
        if c!={'control':g['control'],'TDP-43 KD':g['KD']}:raise ValueError('Unexpected technical row counts')
        reused=g['reused_units']=='same_study_as_issue14'
        rec=dict(source_group=g['source_label'],control_rows=c['control'],KD_rows=c['TDP-43 KD'],accession=g['published_accession'],
                 file_inspected=True,junction_fields_verified=True,coordinate_link_verified=False,unit_map_verified=False,
                 independent_units_verified=False,editorial_identity_verified=g['identity_status']=='culture_group_published',
                 reused=reused,clinical_data_used=False,ready_for_external_reanalysis=False,
                 decision='reused_same_study_not_external' if reused else 'candidate_pending_provenance_and_units')
        out.append(validate(rec))
    return out

def main(source,manifest,out):
    cfg=json.loads(manifest.read_text()); raw=source.read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    if blob!=cfg['culture_csv']['git_blob_sha']:raise ValueError('Public source Git blob mismatch')
    with source.open() as f:
        reader=csv.DictReader(f)
        if len(reader.fieldnames)!=26 or len(set(reader.fieldnames))!=26:raise ValueError('Unexpected schema')
        rows=list(reader)
    result=inspect(rows,cfg['groups']);out.mkdir(parents=True,exist_ok=True)
    with (out/'culture_source_groups.tsv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(result[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(result)
    summary=dict(culture_rows=42,source_groups=5,conditions=['control','TDP-43 KD'],junction_count_fields=list(COUNTS),
        integer_count_cells_checked=42*len(COUNTS),ready_external_groups=sum(r['ready_for_external_reanalysis'] for r in result),
        source_groups_pending=sum(not r['reused'] for r in result),reused_group_count=sum(r['reused'] for r in result),
        biological_replicates_inferred=False,effects_calculated=False,genotype_suffixes_or_individual_aliases_exported=False,
        prediction_status='Not met: direct count file accessible, but coordinate/unit/source independence unresolved',
        coordinate_note='The separate two-line BED encodes exon intervals, not junction endpoints; formal convention unresolved')
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (out/'run.json').write_text(json.dumps(dict(date='2026-10-30',python=platform.python_version(),dependencies='stdlib',
       random_seed=None,parent_commit='91737fa1b92bf3abd87aae120ef49f042bf36c78',repository_commit=cfg['commit'],
       source_git_blob=blob,hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,manifest,Path(__file__)]},
       input_columns=26,projected_count_columns=7,rows_exported='five culture-group aggregates only'),indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for x in ['source','manifest','out']:p.add_argument('--'+x,type=Path,required=True)
    a=p.parse_args();main(a.source,a.manifest,a.out)
