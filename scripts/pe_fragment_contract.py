"""Synthetic PE contract. Input sorted lexicographically by (RG,QNAME).

Text and HTSlib decode CIGAR independently; pair selection/reduction is shared.
This module does not download reads or run an aligner.
"""
import itertools
import re
from collections import Counter
from pathlib import Path


def text_records(path, anchor):
    with Path(path).open() as handle:
        yield from text_records_from_lines(handle,anchor)


def text_records_from_lines(handle,anchor):
    for line in handle:
        if line.startswith('@'):
            continue
        f=line.rstrip('\n').split('\t')
        if len(f)<11:raise ValueError('Truncated SAM')
        tags={}
        for field in f[11:]:
            key,kind,value=field.split(':',2)
            if key in tags:raise ValueError('Duplicate SAM tag')
            tags[key]=int(value) if kind=='i' else value
        cigar=re.findall(r'(\d+)([MIDNSHP=X])',f[5]) if f[5]!='*' else []
        if f[5]!='*' and ''.join(n+op for n,op in cigar)!=f[5]:raise ValueError('Invalid CIGAR')
        if any(int(n)<=0 for n,_ in cigar):raise ValueError('Zero CIGAR operation')
        cursor=int(f[3])-1;events=[]
        for i,(length,op) in enumerate(cigar):
            n=int(length)
            if op=='N' and i>0 and i+1<len(cigar):
                left=right=0
                for j in range(i-1,-1,-1):
                    if cigar[j][1] not in 'M=X':break
                    left+=int(cigar[j][0])
                for j in range(i+1,len(cigar)):
                    if cigar[j][1] not in 'M=X':break
                    right+=int(cigar[j][0])
                if min(left,right)>=anchor:
                    events.append((f[2],cursor,cursor+n,tags.get('XS')))
            if op in 'MDN=X':cursor+=n
        yield {'qname':f[0],'flag':int(f[1]),'ref':f[2],'pos':int(f[3])-1,
               'mate_ref':f[2] if f[6]=='=' else f[6],'mate_pos':int(f[7])-1,
               'mapq':int(f[4]),'rg':tags.get('RG','<missing>'),'nh':tags.get('NH'),
               'xs':tags.get('XS'),'events':events}


def hts_records(path, anchor):
    import pysam
    with pysam.AlignmentFile(str(path),'r') as handle:
        yield from hts_decoded(handle,anchor)


def hts_decoded(records,anchor):
    for r in records:
        # Reference increments use HTSlib operation codes, not the text regex.
        cursor=r.reference_start;events=[];ops=r.cigartuples or []
        for i,(code,n) in enumerate(ops):
            if code==3 and 0<i<len(ops)-1:
                l=i-1;left=0
                while l>=0 and ops[l][0] in (0,7,8):left+=ops[l][1];l-=1
                j=i+1;right=0
                while j<len(ops) and ops[j][0] in (0,7,8):right+=ops[j][1];j+=1
                if min(left,right)>=anchor:
                    events.append((r.reference_name,cursor,cursor+n,r.get_tag('XS') if r.has_tag('XS') else None))
            if code in (0,2,3,7,8):cursor+=n
        yield {'qname':r.query_name,'flag':r.flag,'ref':r.reference_name or '*',
               'pos':r.reference_start,'mate_ref':r.next_reference_name or '*',
               'mate_pos':r.next_reference_start,'mapq':r.mapping_quality,
               'rg':r.get_tag('RG') if r.has_tag('RG') else '<missing>',
               'nh':r.get_tag('NH') if r.has_tag('NH') else None,
               'xs':r.get_tag('XS') if r.has_tag('XS') else None,'events':events}


def pair_reason(records):
    if len(records)!=2:return 'primary_mate_count'
    a,b=records
    if sorted((bool(r['flag']&64),bool(r['flag']&128)) for r in records)!=[(False,True),(True,False)]:return 'mate_identity'
    if any(not r['flag']&1 or not r['flag']&2 or r['flag']&(4|8|512) for r in records):return 'pair_flags'
    if a['ref']!=b['ref'] or a['mate_ref']!=b['ref'] or b['mate_ref']!=a['ref'] or a['mate_pos']!=b['pos'] or b['mate_pos']!=a['pos']:return 'mate_coordinates'
    if bool(a['flag']&32)!=bool(b['flag']&16) or bool(b['flag']&32)!=bool(a['flag']&16):return 'mate_reverse_flags'
    if bool(a['flag']&16)==bool(b['flag']&16):return 'orientation'
    forward,reverse=(b,a) if a['flag']&16 else (a,b)
    if forward['pos']>reverse['pos']:return 'orientation'
    if any(r['nh']!=1 or not 20<=r['mapq']<255 for r in records):return 'mapping_quality'
    strands={r['xs'] for r in records if r['events']}
    if any(s not in ('+','-') for s in strands) or len(strands)>1:return 'event_strand'
    return None


def count_fragments(records, library):
    if not library:raise ValueError('Explicit library identifier required')
    counts=Counter();qc=Counter();last=None
    for key,group in itertools.groupby(records,key=lambda r:(r['rg'],r['qname'])):
        if last is not None and key<=last:raise ValueError('Input must be lexicographically grouped by RG,QNAME')
        last=key
        batch=list(itertools.islice(group,17))
        if len(batch)>16:raise ValueError('Fragment group exceeds 16 records')
        primary=[r for r in batch if not r['flag']&(256|2048)]
        qc['nonprimary_excluded']+=len(batch)-len(primary)
        qc['groups']+=1
        reason=pair_reason(primary)
        if reason:
            qc['excluded:'+reason]+=1
            continue
        qc['accepted_pairs']+=1
        if any(r['flag']&1024 for r in primary):qc['accepted_marked_duplicate_pairs']+=1
        for event in set(e for r in primary for e in r['events']):counts[(library,)+event]+=1
    return dict(sorted(counts.items())),dict(sorted(qc.items()))
