"""STMN2-only exact splice support; fixed filters, no effects or ratios."""
from collections import Counter

def events(read, targets):
    if read.reference_name!='chr8' or not read.has_tag('XS') or read.get_tag('XS')!='+':return set()
    cigar=read.cigartuples or [];cursor=read.reference_start;hits=set()
    for i,(op,n) in enumerate(cigar):
        if op==3:
            anchors=[]
            for side in (reversed(cigar[:i]),iter(cigar[i+1:])):
                anchor=0
                for o,k in side:
                    if o not in (0,7,8):break
                    anchor+=k
                anchors.append(anchor)
            if min(anchors)>=15:
                for label,interval in targets.items():
                    if (cursor,cursor+n)==tuple(interval):hits.add(label)
        if op in (0,2,3,7,8):cursor+=n
    return hits

def pair_hits(group,targets):
    if len(group)!=2:return None
    if {bool(r.is_read1) for r in group}!={True,False} or any(r.is_read1==r.is_read2 for r in group):return None
    for r in group:
        if (not r.is_paired or not r.is_proper_pair or r.is_unmapped or r.mate_is_unmapped or r.is_secondary or r.is_supplementary or r.is_qcfail or not 20<=r.mapping_quality<255 or not r.has_tag('NH') or r.get_tag('NH')!=1):return None
    a,b=group
    if a.next_reference_id!=b.reference_id or b.next_reference_id!=a.reference_id or a.next_reference_start!=b.reference_start or b.next_reference_start!=a.reference_start:return None
    return events(a,targets)|events(b,targets)

def count_records(records,targets):
    counts={k:0 for k in targets};qc=Counter();group=[];name=None
    def consume():
        qc['alignment_groups']+=1
        hits=pair_hits(group,targets)
        if hits is None:qc['rejected_groups']+=1;return
        qc['eligible_groups']+=1
        qc['marked_duplicate_records']+=sum(r.is_duplicate for r in group)
        for key in hits:counts[key]+=1
    for r in records:
        qc['sam_records']+=1
        if group and r.query_name!=name:consume();group=[]
        name=r.query_name;group.append(r)
        if len(group)>8:raise ValueError('Unexpected query group >8 records; stop')
    if group:consume()
    return {'counts':counts,'qc':dict(qc),'unit':'contiguous paired query group/event/library; anchor 15',
            'positive_control_measured':counts['canonical']>0,
            'support_at_least_20_groups':{k:counts[k]>=20 for k in ('cryptic',)},
            'interpretation':'Below-diagnostic support is insufficient, not a biological zero. No effect or ratio.'}

