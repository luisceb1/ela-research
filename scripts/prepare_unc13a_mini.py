"""Generate and preregister miniature inputs before any alignment."""
import hashlib
import json
from pathlib import Path
from mini_limits import ROOT

def rc(s):return s.translate(str.maketrans('ACGT','TGCA'))[::-1]

def main():
    base=Path(__file__).resolve().parents[1]
    seq=json.loads((base/'reports/unc13a-reference-strand-20261102/sources/sequence.json').read_text())
    contract=json.loads((base/'reports/unc13a-reference-strand-20261102/contract.json').read_text())
    dna=seq['dna'].upper();origin=seq['start'];work=ROOT/'scratch'
    events={r['event']:(r['start0']-origin,r['end0']-origin) for r in contract['events']}
    cases={}
    for name,(a,b) in events.items():
        for anchor in (75,15,14):
            name2=f'{name}_a{anchor}';s=dna[a-anchor:a]+dna[b:b+75]
            assert len(s)==anchor+75
            assert dna.count(dna[a-anchor:a])==1 and dna.count(dna[b:b+75])==1
            cases[name2]={'sequence':s,'expected_event':["mini",a,b,'-'] if anchor>=15 else None,'explanation':'anchor below15 excluded' if anchor<15 else 'exact positive'}
    # All mates overlap the same splice: reduction must count one, not two.
    for reference in ['wild','multicopy','wrongstrand','wrongmotif']:
        data=dna
        if reference.startswith('wrong'):
            a,b=events['canonical'];x=list(data)
            x[a:a+2]=list('GT' if reference=='wrongstrand' else 'AA')
            x[b-2:b]=list('AG' if reference=='wrongstrand' else 'TT');data=''.join(x)
        (work/(reference+'.fa')).write_text('>mini\n'+data+'\n'+('>copy\n'+data+'\n' if reference=='multicopy' else ''))
    fq1=[];fq2=[]
    for name,case in cases.items():
        s=case['sequence'];fq1.append(f'@{name}\n{s}\n+\n'+len(s)*'I'+'\n');fq2.append(f'@{name}\n{rc(s)}\n+\n'+len(s)*'I'+'\n')
    (work/'r1.fq').write_text(''.join(fq1));(work/'r2.fq').write_text(''.join(fq2))
    for mate,content in [('n1.fq',cases['canonical_a75']['sequence']),('n2.fq',rc(cases['canonical_a75']['sequence']))]:
        (work/mate).write_text(f'@negative\n{content}\n+\n'+len(content)*'I'+'\n')
    plan={'origin0':origin,'cases':cases,'negative_expected':{'multicopy':'no accepted unique fragments','wrongstrand':'canonical plus-strand event, zero minus-strand target','wrongmotif':'no minus-strand target'},'limits':'source.json caps apply globally','aligner_options':['--no-mixed','--no-discordant','--fr','-p','2','--seed','0'],'forbidden_options':['--rna-strandness','--tmo'],'inputs_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in work.glob('*') if p.suffix in ('.fa','.fq')}}
    (ROOT/'fixture_plan.json').write_text(json.dumps(plan,indent=2)+'\n')
    print('Prepared',len(cases),'positive/anchor fixtures and3negative references')

if __name__=='__main__':main()
