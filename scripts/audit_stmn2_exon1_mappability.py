#!/usr/bin/env python3
"""Reference-only exhaustive 50/51nt tiling; no new biological reads."""
import argparse
from collections import Counter
import csv
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.audit_stmn2_junction_contract import sam_junctions
from scripts.compare_hisat2_reference import overlap_piece

REGIONS={'exon1':(79611116,79611214),'exon2':(79636801,79636897),'exon3':(79641377,79641550),'cryptic_acceptor':(79616821,79616881)}
COMMON_EXON1=(79611151,79611214)


def audit_definition(exons):
    with exons.open() as stream:rows=list(csv.DictReader(stream,delimiter='\t'))
    wanted=('ENST00000220876.12','ENST00000518111.5')
    selected=[]
    for tx in wanted:
        for order in (1,2,3):
            hits={(int(r['start_1based'])-1,int(r['end_1based'])) for r in rows if r['symbol']=='STMN2' and r['txname']==tx and r['genomic_order']==str(order) and r['chrom']=='chr8' and r['strand']=='+' and r['exact_exon_in_gencode_v47']=='True'}
            expected=(COMMON_EXON1 if tx==wanted[1] and order==1 else REGIONS['exon'+str(order)])
            if hits!={expected}:raise ValueError('Canonical exon definition mismatch')
            selected.append({'transcript':tx,'exon_order':order,'start_0based':expected[0],'end_exclusive':expected[1]})
    return {'reused_projection':str(exons),'sha256':hashlib.sha256(exons.read_bytes()).hexdigest(),'selected_exons':selected,'not_independent_GTF_reconstruction':True}


def rc(s):return s.translate(str.maketrans('ACGT','TGCA'))[::-1]


def tile(region,sequence,start,length):
    if length<1 or length>len(sequence):raise ValueError('Invalid tile length')
    for offset in range(len(sequence)-length+1):
        for reverse in (False,True):
            s=sequence[offset:offset+length]
            yield {'name':f'{region}_L{length}_S{offset:03d}_{"R" if reverse else "F"}',
                   'type':'tile','region':region,'length':length,'expected_pos_1based':start+offset+1,
                   'reverse':reverse,'sequence':rc(s) if reverse else s,
                   'inside_shared63':region=='exon1' and start+offset>=COMMON_EXON1[0] and start+offset+length<=COMMON_EXON1[1]}


def prepare(inspect_binary,prefix,out,cache):
    seqs={k:'' for k in REGIONS};cmd=['prlimit','--as=5368709120','--',inspect_binary,'-a','65536',prefix]
    with (out/'inspect.stderr.txt').open('w') as err:
        with subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=err,text=True) as p:
            chrom=None;offset=0
            for line in p.stdout:
                if line.startswith('>'):chrom=line[1:].strip().split()[0];offset=0
                else:
                    s=line.strip().upper()
                    if chrom=='chr8':
                        for k,(start,end) in REGIONS.items():seqs[k]+=overlap_piece(s,offset,start,end)
                    offset+=len(s)
            if p.wait()!=0:raise RuntimeError('Indexed reference extraction failed')
    for k,s in seqs.items():
        if len(s)!=REGIONS[k][1]-REGIONS[k][0] or set(s)-set('ACGT'):raise ValueError('Invalid reference interval')
    reads=[]
    for region in ('exon1','exon2','exon3'):
        for length in (50,51):reads.extend(tile(region,seqs[region],REGIONS[region][0],length))
    for event,right,acceptor in [('canonical',79636802,'exon2'),('cryptic',79616822,'cryptic_acceptor')]:
        for length in (50,51):
            s=seqs['exon1'][-25:]+seqs[acceptor][:length-25]
            for reverse in (False,True):
                reads.append({'name':f'junction_{event}_{length}_{"R" if reverse else "F"}','type':'junction','region':event,'length':length,'reverse':reverse,
                              'sequence':rc(s) if reverse else s,'expected_junction':['chr8',79611214,right,'+']})
    reads.append({'name':'negative_N50','type':'negative','region':'negative','length':50,'sequence':'N'*50})
    manifest={'synthetic_only':True,'index_prefix':prefix,'regions_0based':REGIONS,'shared_exon1_interval_0based':COMMON_EXON1,'sequences':seqs,'reads':reads,
              'sequence_sha256':{k:hashlib.sha256(s.encode()).hexdigest() for k,s in seqs.items()},'prepare_command':cmd}
    (out/'controls.json').write_text(json.dumps(manifest,indent=2)+'\n')
    fq=cache/'tiles.fastq';fq.write_text(''.join('@'+r['name']+'\n'+r['sequence']+'\n+\n'+'I'*r['length']+'\n' for r in reads))
    return manifest,fq


def align(binary,prefix,fq,sam,out):
    os.sched_setaffinity(0,sorted(os.sched_getaffinity(0))[:2])
    cmd=['prlimit','--as=5368709120','--','timeout','600',binary,'--wrapper','basic-0','-x',prefix,'-U',str(fq),'-S',str(sam),'-p','2','-k','5','--seed','0','--no-temp-splicesite','--reorder']
    start=time.monotonic()
    with (out/'alignment.log').open('w') as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
    record={'command':cmd,'exit_code':r.returncode,'elapsed_seconds':time.monotonic()-start,'maxrss_children_so_far_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
            'memory_scope':'maximum child across inspector/aligner, not separate combined RSS'}
    (out/'run.json').write_text(json.dumps(record,indent=2)+'\n')
    if r.returncode:raise RuntimeError('Alignment failed')


def evaluate_tile(expected,primary):
    if primary['flag']&4:return 'unmapped'
    if primary['NH']!=1:return 'reported_multimapping_or_missing_NH'
    if not 20<=primary['MAPQ']<255:return 'mapq_excluded'
    if (primary['chrom'],primary['pos'])!=('chr8',expected['expected_pos_1based']):return 'other_location'
    if bool(primary['flag']&16)!=expected['reverse']:return 'other_orientation'
    if primary['cigar']!=str(expected['length'])+'M' or primary['NM']!=0:return 'partial_or_mismatch'
    return 'exact_unique_source'


def analyze(manifest,sam,out):
    expected={r['name']:r for r in manifest['reads']};groups={k:[] for k in expected}
    with sam.open() as f:
        for line in f:
            if line.startswith('@'):continue
            fields=line.rstrip('\n').split('\t');tags={p.split(':',2)[0]:p.split(':',2)[2] for p in fields[11:] if p.count(':')>=2}
            row={'name':fields[0],'chrom':fields[2],'pos':int(fields[3]),'flag':int(fields[1]),'MAPQ':int(fields[4]),'cigar':fields[5],
                 'NH':int(tags['NH']) if 'NH' in tags else None,'NM':int(tags['NM']) if 'NM' in tags else None,
                 'accepted_junctions':[list(j) for j in sam_junctions(line,min_anchor=15)]}
            if row['name'] not in groups:raise ValueError('Unexpected synthetic query')
            groups[row['name']].append(row)
    observations=[];summary={};positive=True;negative=True
    for name,r in expected.items():
        primary=[x for x in groups[name] if not x['flag']&(256|2048)]
        if len(primary)!=1:raise ValueError('Synthetic query lacks one primary record')
        p=primary[0]
        if r['type']=='tile':
            reason=evaluate_tile(r,p);key=f'{r["region"]}_{r["length"]}'
            summary.setdefault(key,Counter())['total']+=1;summary[key][reason]+=1
            if r['inside_shared63']:
                key=f'shared63_{r["length"]}';summary.setdefault(key,Counter())['total']+=1;summary[key][reason]+=1
        elif r['type']=='junction':
            passed=p['accepted_junctions']==[r['expected_junction']];positive &= passed;reason='positive_pass' if passed else 'positive_fail'
        else:
            passed=bool(p['flag']&4);negative &= passed;reason='negative_pass' if passed else 'negative_fail'
        observations.append({**p,'type':r['type'],'region':r['region'],'length':r['length'],'expected_pos_1based':r.get('expected_pos_1based'),
                             'inside_shared63':r.get('inside_shared63',False),'classification':reason,'reported_records':len(groups[name])})
    result={'synthetic_queries':len(expected),'tile_summary':{k:dict(v) for k,v in summary.items()},'positive_controls_pass':positive,'negative_control_pass':negative,
            'first_exon_some_exact_for_each_length':all(summary[f'exon1_{length}']['exact_unique_source']>0 for length in (50,51)),
            'perfect_reference_only':True,'real_FASTQ_reads_processed':0,'biological_replication':False,'not_exhaustive_uniqueness':True}
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    fields=['name','type','region','length','expected_pos_1based','inside_shared63','chrom','pos','flag','MAPQ','cigar','NH','NM','classification','reported_records']
    with (out/'observations.tsv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n',extrasaction='ignore');w.writeheader();w.writerows(observations)
    (out/'output_checks.json').write_text(json.dumps({'SAM_sha256':hashlib.sha256(sam.read_bytes()).hexdigest(),
             'all_expected_queries_present':True,'no_real_query_ids':True},indent=2)+'\n')
    if not positive or not negative:raise ValueError('Control failure; mappability result not accepted')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(__doc__);p.add_argument('--inspect',required=True);p.add_argument('--aligner',required=True);p.add_argument('--prefix',required=True);p.add_argument('--out',required=True);p.add_argument('--cache',required=True);a=p.parse_args()
    out=Path(a.out);cache=Path(a.cache);out.mkdir(parents=True,exist_ok=True);cache.mkdir(parents=True,exist_ok=True)
    (out/'definition.json').write_text(json.dumps(audit_definition(Path('reports/isoforms/exons.tsv')),indent=2)+'\n')
    m,fq=prepare(a.inspect,a.prefix,out,cache);sam=cache/'tiles.sam';align(a.aligner,a.prefix,fq,sam,out);analyze(m,sam,out)
