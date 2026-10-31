#!/usr/bin/env python3
"""Generate declared synthetic controls and compare independent SAM parsers."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import random
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_stmn2_junction_contract import sam_junctions
from scripts.compare_hisat2_reference import overlap_piece


def reverse_complement(s):
    return s.translate(str.maketrans('ACGTN', 'TGCAN'))[::-1]


def prepare(binary, prefix, out):
    out.mkdir(parents=True, exist_ok=True)
    intervals={'donor':(79611154,79611214),'cryptic':(79616821,79616881),'canonical':(79636801,79636861)}
    flanks={k:'' for k in intervals}
    cmd=['prlimit','--as=6442450944','--','timeout','900',binary,'-a','65536',prefix]
    with (out/'flank-inspect.stderr.txt').open('w') as err:
        with subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=err,text=True) as p:
            chrom,offset=None,0
            try:
                for line in p.stdout:
                    if line.startswith('>'):chrom=line[1:].strip().split()[0];offset=0
                    else:
                        dna=line.strip().upper()
                        if chrom=='chr8':
                            for k,(a,b) in intervals.items(): flanks[k]+=overlap_piece(dna,offset,a,b)
                        offset+=len(dna)
                if p.wait()!=0:raise RuntimeError('Reference flank reconstruction failed')
            except BaseException:p.kill();p.wait();raise
    if any(len(s)!=60 or set(s)-set('ACGT') for s in flanks.values()):raise ValueError('Invalid reference flanks')
    rows=[]
    for event,right in [('cryptic',79616822),('canonical',79636802)]:
        for length,left,category in [(50,25,'required'),(100,50,'required'),(50,7,'sensitivity'),(50,8,'sensitivity'),(50,15,'sensitivity'),(50,20,'sensitivity')]:
            s=flanks['donor'][-left:]+flanks[event][:length-left]
            for orientation in ['forward','reverse']:
                rows.append({'name':f'{event}_{length}_{left}_{orientation}','category':category,'event':event,'left_anchor':left,'right_anchor':length-left,'sequence':s if orientation=='forward' else reverse_complement(s),'expected_junction':['chr8',79611214,right,'+']})
    rows += [{'name':'continuous_exon_50','category':'negative','sequence':flanks['donor'][-50:],'expected_junction':None},
             {'name':'ambiguous_N50','category':'negative','sequence':'N'*50,'expected_junction':None}]
    (out/'controls.json').write_text(json.dumps({'synthetic':True,'flank_source':'indexed reference, not biological reads','intervals_0based':intervals,'flanks':flanks,'reads':rows},indent=2)+'\n')
    write_fastq(out/'synthetic_reads.fastq',rows)
    rng=random.Random(20261031)
    def locus():
        exon1=''.join(rng.choice('ACGT') for _ in range(200));intron='GT'+''.join(rng.choice('ACGT') for _ in range(96))+'AG';exon2=''.join(rng.choice('ACGT') for _ in range(200))
        return exon1+intron+exon2,exon1[-25:]+exon2[:25]
    dup,dup_read=locus();unique,unique_read=locus()
    (out/'mini_reference.fa').write_text('>copy1\n'+dup+'\n>copy2\n'+dup+'\n>unique\n'+unique+'\n')
    mini=[{'name':'mini_multisplice','category':'multi','sequence':dup_read},{'name':'mini_unique_splice','category':'unique','sequence':unique_read}]
    write_fastq(out/'mini_reads.fastq',mini)
    (out/'preparation.json').write_text(json.dumps({'command':cmd,'mini_seed':20261031,'full_genome_controls':len(rows),'mini_controls':len(mini),'real_fastq_reads':0},indent=2)+'\n')


def write_fastq(path, rows):
    path.write_text(''.join('@'+r['name']+'\n'+r['sequence']+'\n+\n'+'I'*len(r['sequence'])+'\n' for r in rows))


def accepted_pysam(read):
    if read.is_paired:raise ValueError('SE contract only')
    return (not(read.is_unmapped or read.is_secondary or read.is_supplementary or read.is_qcfail)
            and 20<=read.mapping_quality<255 and read.has_tag('NH') and read.get_tag('NH')==1
            and read.has_tag('XS') and read.get_tag('XS') in ('+','-'))


def htslib_events(sam, min_anchor=8):
    import pysam
    events=[]
    with pysam.AlignmentFile(str(sam),'r') as file:
        for r in file:
            if not accepted_pysam(r):continue
            # HTSlib parses SAM/CIGAR; find_introns supplies interval geometry.
            introns=file.find_introns([r])
            cursor=r.reference_start
            cigar=r.cigartuples or []
            for i,(op,n) in enumerate(cigar):
                if op==3:
                    left=right=0
                    for op2,n2 in reversed(cigar[:i]):
                        if op2 not in (0,7,8):break
                        left+=n2
                    for op2,n2 in cigar[i+1:]:
                        if op2 not in (0,7,8):break
                        right+=n2
                    if left>=min_anchor and right>=min_anchor and introns[(cursor,cursor+n)]>0:
                        events.append((r.query_name,r.reference_name,cursor,cursor+n+1,r.get_tag('XS')))
                if op in (0,2,3,7,8):cursor+=n
    return events


def compare(out):
    import pysam
    controls=json.loads((out/'controls.json').read_text())
    result={'synthetic':True,'real_reads_processed':0,'pysam_version':pysam.__version__,
            'htslib_samtools_version':pysam.__samtools_version__,'gate_pass':False}
    comparisons={}
    for name in ['genome','mini']:
        own=[]
        with (out/(name+'.sam')).open() as f:
            for line in f:
                if line.startswith('@'):continue
                own.extend((line.split('\t',1)[0],*j) for j in sam_junctions(line))
        other=htslib_events(out/(name+'.sam'))
        comparisons[name]={'own_events':own,'htslib_events':other,'concordant':Counter(own)==Counter(other)}
    genome=comparisons['genome']['own_events'];outcomes=[]
    for r in controls['reads']:
        observed=[list(e[1:]) for e in genome if e[0]==r['name']]
        expected=r['expected_junction']
        passed=(observed==[expected]) if r['category']=='required' else (not observed if r['category']=='negative' else None)
        outcomes.append({'name':r['name'],'category':r['category'],'expected':expected,'observed':observed,'required_pass':passed})
    with pysam.AlignmentFile(str(out/'mini.sam'),'r') as f:
        multi=[{'name':r.query_name,'reference':r.reference_name,'cigar':r.cigarstring,'flag':r.flag,'mapq':r.mapping_quality,'NH':r.get_tag('NH') if r.has_tag('NH') else None,'XS':r.get_tag('XS') if r.has_tag('XS') else None} for r in f]
    with pysam.AlignmentFile(str(out/'genome.sam'),'r') as f:
        genome_records=[{'name':r.query_name,'reference':r.reference_name,'cigar':r.cigarstring,'flag':r.flag,'mapq':r.mapping_quality,'NH':r.get_tag('NH') if r.has_tag('NH') else None,'XS':r.get_tag('XS') if r.has_tag('XS') else None} for r in f]
    m=[r for r in multi if r['name']=='mini_multisplice' and r['reference'] in ('copy1','copy2') and r['cigar'] and 'N' in r['cigar']]
    multi_pass=bool(m) and {r['reference'] for r in m}=={'copy1','copy2'} and all(r['NH'] is not None and r['NH']>=2 for r in m) and not any(e[0]=='mini_multisplice' for e in comparisons['mini']['own_events'])
    unique_pass=comparisons['mini']['own_events']==[('mini_unique_splice','unique',200,301,'+')]
    result.update(comparisons=comparisons,outcomes=outcomes,mini_records=multi,genome_records=genome_records,multimapping_control_pass=multi_pass,
                  mini_unique_control_pass=unique_pass,gate_pass=all(r['required_pass'] for r in outcomes if r['category']!='sensitivity') and multi_pass and unique_pass and all(v['concordant'] for v in comparisons.values()),
                  unbiased_ratio_validated=False,pilot_requires_anchor_policy=True,
                  scope='Technical synthetic controls only; short-anchor recovery must be reviewed separately; no biological efficacy or empirical read-quality sensitivity')
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'gate_pass':result['gate_pass'],'outcomes':outcomes,'multi_pass':multi_pass,'unique_pass':unique_pass,'parser_concordance':all(v['concordant'] for v in comparisons.values())},indent=2))
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(__doc__);p.add_argument('mode',choices=['prepare','compare']);p.add_argument('--out',required=True);p.add_argument('--binary');p.add_argument('--prefix');a=p.parse_args()
    if a.mode=='prepare':prepare(a.binary,a.prefix,Path(a.out))
    elif not compare(Path(a.out))['gate_pass']:raise SystemExit(1)
