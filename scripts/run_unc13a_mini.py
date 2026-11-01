"""Run fixed miniature alignment gate once. Any mismatch stops acceptance."""
import hashlib
import itertools
import json
import sys
from pathlib import Path
from mini_limits import ROOT,run
import pe_fragment_contract as pe

def check(path,expectations):
    text=pe.count_fragments(pe.text_records(path,15),'synthetic')
    hts=pe.count_fragments(pe.hts_records(path,15),'synthetic')
    details=[]
    for key,records in itertools.groupby(pe.text_records(path,15),key=lambda r:(r['rg'],r['qname'])):
        group=list(records);counts,qc=pe.count_fragments(iter(group),'synthetic')
        actual=[list(e[1:]) for e,n in counts.items() if n]
        expected=expectations[key[1]]
        want=[] if expected is None else [expected]
        details.append({'name':key[1],'expected':want,'actual':actual,'pass':sorted(want)==sorted(actual),'qc':qc})
    return {'text_equals_htslib':text==hts,'details':details,'pass':text==hts and len(details)==len(expectations) and all(r['pass'] for r in details)}

def main():
    work=ROOT/'scratch';src=next(work.glob('hisat2-*'));plan=json.loads((ROOT/'fixture_plan.json').read_text())
    results={};out={'passed':False,'references':results,'raw_reads_used':False,'scope':'miniature only; not global mappability or library orientation'}
    try:
        for name in ['wild','multicopy','wrongstrand','wrongmotif']:
            prefix=work/(name+'.idx')
            run('build_'+name,[str(src/'hisat2-build-s'),'-p','2',str(work/(name+'.fa')),str(prefix)])
            fq=('r1.fq','r2.fq') if name=='wild' else ('n1.fq','n2.fq')
            sam=work/(name+'.sam');ordered=work/(name+'.ordered.sam')
            argv=[str(src/'hisat2-align-s'),'-x',str(prefix),'-1',str(work/fq[0]),'-2',str(work/fq[1]),'-S',str(sam),'--no-mixed','--no-discordant','--fr','-p','2','--seed','0']
            run('align_'+name,argv)
            run('collate_'+name,[sys.executable,str(Path(__file__).with_name('collate_pe_sam.py')),str(sam),str(ordered),str(work/(name+'.sort'))])
            if name=='wild':expected={k:v['expected_event'] for k,v in plan['cases'].items()}
            elif name=='wrongstrand':
                c=plan['cases']['canonical_a75']['expected_event'];expected={'negative':c[:-1]+['+']}
            else:expected={'negative':None}
            result=check(ordered,expected);result['sam_sha256']=hashlib.sha256(ordered.read_bytes()).hexdigest();results[name]=result
            if not result['pass']:raise ValueError('Preregistered mismatch: '+name)
        out['passed']=True
    except Exception as e:
        out['error']=f'{type(e).__name__}: {e}'
    (ROOT/'result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
