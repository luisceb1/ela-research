"""UNC13A reference-only geometry gate; no biological read processing."""
import json
import hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/'reports/unc13a-reference-strand-20261102'
CANDIDATES={'canonical':(17641556,17642845),'cryptic_genomic_left':(17641556,17642414),'cryptic_genomic_right':(17642541,17642845)}

def interval(a,b,model):
    return {'halfopen0':(a,b),'inclusive1':(a-1,b),'exonic1':(a,b-1),'closed0':(a,b+1)}[model]

def motifs(dna,origin,start,end):
    if not origin<=start<end<=origin+len(dna):raise ValueError('Reference window insufficient')
    return dna[start-origin:start-origin+2].upper(),dna[end-origin-2:end-origin].upper()

def evaluate(seq,annotation):
    if seq['genome']!='hg38' or seq['chrom']!='chr19':raise ValueError('Wrong reference')
    if len(seq['dna'])!=seq['end']-seq['start']:raise ValueError('Sequence length mismatch')
    if annotation.get('genome')!='hg38' or annotation.get('chrom')!='chr19' or annotation.get('track')!='wgEncodeGencodeCompV47':raise ValueError('Wrong annotation')
    rows=annotation['wgEncodeGencodeCompV47'];models=[]
    reference=[]
    for row in rows:
        if row['name2']!='UNC13A' or row['strand']!='-' or row['chrom']!='chr19':continue
        starts=[int(x) for x in row['exonStarts'].strip(',').split(',')]
        ends=[int(x) for x in row['exonEnds'].strip(',').split(',')]
        reference.extend((ends[i],starts[i+1],row['name']) for i in range(len(starts)-1))
    for name,(a,b) in CANDIDATES.items():
        for model in ['halfopen0','inclusive1','exonic1','closed0']:
            lo,hi=interval(a,b,model);left,right=motifs(seq['dna'],seq['start'],lo,hi)
            models.append({'event':name,'model':model,'start0':lo,'end0':hi,'left_plus':left,'right_plus':right,'minus_gt_ag':(left,right)==('CT','AC'),'canonical_transcripts':[t for l,r,t in reference if name=='canonical' and (l,r)==(lo,hi)]})
    accepted=[r for r in models if r['minus_gt_ag'] and (r['event']!='canonical' or r['canonical_transcripts'])]
    if len(accepted)!=3 or len({r['model'] for r in accepted})!=1:raise ValueError('Ambiguous or unsupported geometry')
    return models,accepted

def main():
    sources=ROOT/'sources';receipt=json.loads((ROOT/'retrievals.json').read_text())
    for row in receipt:
        if not row.get('saved') or hashlib.sha256((sources/row['name']).read_bytes()).hexdigest()!=row['sha256']:raise ValueError('Unverified source')
    seq=json.loads((sources/'sequence.json').read_text());ann=json.loads((sources/'annotation.json').read_text())
    models,accepted=evaluate(seq,ann)
    contract={'assembly':'hg38','chromosome':'chr19','transcript_strand':'-','interval_convention':'intronic 0-based half-open, same as PE parser N span','events':accepted,'cryptic_exon_interval0':[17642413,17642541],'cryptic_exon_length':128,'primary_library_strandness':'unstranded: omit --rna-strandness','RF_expected_from_kit_but_not_certified_for_actual_libraries':True,'require_XS_reference_motif_concordance':True,'aligner_end_to_end_verified':False,'raw_execution_ready':False,'two_independent_sequence_providers':False}
    (ROOT/'models.json').write_text(json.dumps(models,indent=2)+'\n')
    (ROOT/'contract.json').write_text(json.dumps(contract,indent=2)+'\n')
    print(json.dumps(contract,indent=2))

if __name__=='__main__':main()
