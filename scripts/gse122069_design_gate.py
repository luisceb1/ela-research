#!/usr/bin/env python3
"""Bounded public-culture design audit; accession/alias is never an independent unit."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
ALLOWED={'source name','cell line','cell type','treatment','biological replicate','biological replicate id',
         'biological experiment id','culture id','batch','batch id','culture batch','transfection batch',
         'pair id','paired sample','replicate','passage','library id','library name','lane','flowcell'}
DESIGN=ALLOWED-{'source name','cell line','cell type','treatment'}
FIELDS=('gsm','run','experiment','sample','biosample','published_group','sample_alias','library_name',
        'explicit_unit','explicit_batch','explicit_pair','status')


def write(path,value):
    Path(path).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')


def normalize(key):
    return re.sub(r'[_\s-]+',' ',key.strip().lower())


def attributes(root,tag):
    result={}
    for node in root.findall('.//'+tag):
        key=normalize(node.findtext('TAG') or '')
        if key not in ALLOWED:continue
        value=(node.findtext('VALUE') or '').strip()
        if key in result and result[key]!=value:raise ValueError('Conflicting technical attribute')
        result[key]=value
    return result


def project_xml(data,kind,accession):
    root=ET.fromstring(data)
    node=root.find('.//'+kind) if root.tag!=kind else root
    if node is None:raise ValueError('Missing record kind')
    identifiers={x.text for x in node.findall('./IDENTIFIERS/*') if x.tag in ('PRIMARY_ID','SECONDARY_ID')}
    if node.get('accession')!=accession and accession not in identifiers:raise ValueError('Unexpected public accession')
    if kind=='EXPERIMENT':
        ref=node.find('.//SAMPLE_DESCRIPTOR')
        if ref is None:raise ValueError('Missing sample accession')
        return {'accession':accession,'sample':ref.get('accession'),
                'title':node.findtext('TITLE'),'library_name':node.findtext('.//LIBRARY_NAME'),
                'layout':'SINGLE' if node.find('.//LIBRARY_LAYOUT/SINGLE') is not None else 'OTHER',
                'instrument':node.findtext('.//INSTRUMENT_MODEL'),
                'technical_attributes':attributes(node,'EXPERIMENT_ATTRIBUTE')}
    if kind!='SAMPLE':raise ValueError('Unexpected record kind')
    return {'accession':accession,'primary_accession':node.get('accession'),'sample_alias':node.get('alias'),
            'technical_attributes':attributes(node,'SAMPLE_ATTRIBUTE')}


def retrieve(accession,kind):
    url='https://www.ebi.ac.uk/ena/browser/api/xml/'+accession
    record={'url':url,'accession':accession,'kind':kind,'date_utc':datetime.now(timezone.utc).isoformat()}
    try:
        with urllib.request.urlopen(url,timeout=30) as f:
            b=f.read(2000001)
            if len(b)>2000000:raise ValueError('Metadata byte cap exceeded')
            record.update(http_status=f.status,bytes=len(b),sha256_original=hashlib.sha256(b).hexdigest())
        record['projection']=project_xml(b,kind,accession)
    except Exception as exc:record['error']=type(exc).__name__+': '+str(exc)
    return record


def validate_manifest(rows):
    if len(rows)!=6 or {r['gsm'] for r in rows}!={f'GSM{x}' for x in range(3454242,3454248)}:
        raise ValueError('Expected exactly six fixed culture accessions')
    for key in ('gsm','run','experiment'):
        if len({r[key] for r in rows})!=6:raise ValueError('Duplicate manifest accession')
    if [r['published_group'] for r in rows]!=['siControl 1','siControl 2','siControl 3','siTDP-43 1','siTDP-43 2','siTDP-43 3']:
        raise ValueError('Published group/order mismatch')


def audit(rows,sources,curated):
    validate_manifest(rows)
    by_accession={}
    for source in sources:
        if source['accession'] in by_accession:raise ValueError('Duplicate metadata source')
        by_accession[source['accession']]=source
    result=[];errors=[];candidate_fields=[]
    for row in rows:
        e=by_accession.get(row['experiment'],{})
        p=e.get('projection',{});s=by_accession.get(p.get('sample'),{});sp=s.get('projection',{})
        if e.get('error') or s.get('error') or not p or not sp:errors.append(row['gsm'])
        attrs=sp.get('technical_attributes',{})
        if sp and sp.get('sample_alias')!=row['gsm']:raise ValueError('Sample alias/GSM mismatch')
        if sp and attrs.get('source name')!='SH-SY5Y cell line':raise ValueError('Non-target culture metadata')
        if sp and attrs.get('treatment')!=row['published_group'].rsplit(' ',1)[0]:raise ValueError('Treatment/group mismatch')
        if p and p.get('layout')!='SINGLE':raise ValueError('Unexpected library layout')
        if p and not (p.get('title') or '').startswith(row['gsm']+': '+row['published_group']+';'):
            raise ValueError('Experiment/group does not match fixed manifest')
        for level,values in [('experiment',p.get('technical_attributes',{})),('sample',attrs)]:
            for key,value in values.items():
                if key in DESIGN:candidate_fields.append({'gsm':row['gsm'],'level':level,'field':key,'value':value})
        # Only a reviewed explicit source map may supply these; nulls stay null.
        claim=curated.get('library_map',{}).get(row['gsm'],{})
        for key in ('unit','batch','pair'):
            if claim.get(key) and claim.get(key+'_evidence_source') not in curated.get('evidence_sources',{}):
                raise ValueError('Design assignment without explicit source evidence')
        result.append({**{k:row[k] for k in ('gsm','run','experiment','published_group')},
                       'sample':p.get('sample'),'biosample':sp.get('primary_accession'),'sample_alias':sp.get('sample_alias'),
                       'library_name':p.get('library_name'),'explicit_unit':claim.get('unit'),
                       'explicit_batch':claim.get('batch'),'explicit_pair':claim.get('pair'),
                       'status':'metadata_error' if row['gsm'] in errors else 'technical_link_only'})
    explicit_all=all(r['explicit_unit'] is not None for r in result)
    return {'library_map':result,'metadata_errors':errors,'candidate_design_fields':candidate_fields,
            'explicit_all_library_units_documented':explicit_all,
            'full_design_gate_pass':explicit_all and all(curated.get(k+'_structure_documented') is True and curated.get(k+'_structure_evidence_source') in curated.get('evidence_sources',{}) for k in ('batch','pairing')) and not errors,
            'independent_units_inferred_from_accessions_or_suffixes':False,
            'author_claim_three_biological_replicates_per_condition':curated.get('author_declared_n_per_condition')==3,
            'author_claim_is_prior_evidence_not_new_replication':True,
            'no_statistical_inference_or_new_fastq':True}


def main():
    parser=argparse.ArgumentParser(__doc__);parser.add_argument('mode',choices=['collect','audit']);parser.add_argument('--out',required=True);parser.add_argument('--retry-errors',action='store_true');a=parser.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    manifest=ROOT/'reports/gse122069-resource-plan/input_manifest.json';rows=json.loads(manifest.read_text())['rows'];validate_manifest(rows)
    if a.mode=='collect':
        if a.retry_errors:
            sources=json.loads((out/'source-projections.json').read_text())
            if (out/'source-projections-attempt1.json').exists():raise ValueError('One documented repair only')
            write(out/'source-projections-attempt1.json',sources)
            write(out/'retrieval-run-attempt1.json',json.loads((out/'retrieval-run.json').read_text()))
            failed=[s for s in sources if 'error' in s]
            with ThreadPoolExecutor(max_workers=3) as pool:fixed=list(pool.map(lambda s:retrieve(s['accession'],s['kind']),failed))
            repairs={s['accession']:s for s in fixed}
            sources=[repairs.get(s['accession'],s) for s in sources]
        else:
            with ThreadPoolExecutor(max_workers=3) as pool:sources=list(pool.map(lambda r:retrieve(r['experiment'],'EXPERIMENT'),rows))
            samples=[s['projection']['sample'] for s in sources if 'projection' in s]
            if len(set(samples))!=len(samples):raise ValueError('Repeated sample accession; manual review required')
            with ThreadPoolExecutor(max_workers=3) as pool:sources+=list(pool.map(lambda x:retrieve(x,'SAMPLE'),samples))
        write(out/'source-projections.json',sources)
        write(out/'retrieval-run.json',{'python':platform.python_version(),'timestamp_utc':datetime.now(timezone.utc).isoformat(),'manifest_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),'max_workers':3,'timeout_seconds':30,'byte_cap':2000000,'errors':[s for s in sources if 'error' in s],'scope':'technical allowlist, six public culture libraries only; original bodies not retained'})
        print('retrieved records',len(sources),'errors',sum('error' in s for s in sources))
    else:
        result=audit(rows,json.loads((out/'source-projections.json').read_text()),json.loads((out/'reviewed-design-evidence.json').read_text()))
        write(out/'results.json',result)
        with (out/'library-design.tsv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=FIELDS,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(result['library_map'])
        print(json.dumps({k:v for k,v in result.items() if k!='library_map'},indent=2))

if __name__=='__main__':main()
