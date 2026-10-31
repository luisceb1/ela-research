#!/usr/bin/env python3
"""Aggregate technical attributes of accepted fixed targets; never identifiers/sequence."""
import re
from scripts.gse122069_pilot import TARGETS

METRICS=('left_anchor','right_anchor','MAPQ','NM','AS','softclip_bases','duplicate_flag')
CIGAR=re.compile(r'(\d+)([MIDNSHP=X])')


def empty_qc():
    return {str(a):{name:{'observations':0,'histograms':{key:{} for key in METRICS}} for name in ('canonical','cryptic')} for a in (8,15)}


def observe(qc,anchor,key,stats):
    name=TARGETS.get(key)
    if name is None:return
    if set(stats)!=set(METRICS):raise ValueError('Incomplete target QC schema')
    target=qc[str(anchor)][name];target['observations']+=1
    for metric,value in stats.items():
        label=str(value);hist=target['histograms'][metric];hist[label]=hist.get(label,0)+1


def sam_integer_tag(fields,name):
    matches=[part.split(':',2) for part in fields[11:] if part.startswith(name+':')]
    if not matches:return 'missing'
    if len(matches)!=1 or len(matches[0])!=3 or matches[0][1]!='i':return 'invalid_type_or_value'
    try:return int(matches[0][2])
    except ValueError:return 'invalid_type_or_value'


def text_stats(line,key):
    f=line.rstrip('\n').split('\t');ops=[(int(n),op) for n,op in CIGAR.findall(f[5])];cursor=int(f[3])-1
    for i,(n,op) in enumerate(ops):
        if op=='N' and (f[2],cursor,cursor+n+1,key[3])==key:
            anchors=[]
            for seq in (reversed(ops[:i]),iter(ops[i+1:])):
                total=0
                for length,code in seq:
                    if code not in ('M','=','X'):break
                    total+=length
                anchors.append(total)
            return {'left_anchor':anchors[0],'right_anchor':anchors[1],'MAPQ':int(f[4]),
                    'NM':sam_integer_tag(f,'NM'),'AS':sam_integer_tag(f,'AS'),
                    'softclip_bases':sum(n for n,op in ops if op=='S'),'duplicate_flag':int(bool(int(f[1])&1024))}
        if op in ('M','D','N','=','X'):cursor+=n
    raise ValueError('Accepted target not located in CIGAR QC projection')


def text_observer(qc):
    def callback(line,anchor,key):
        if key not in TARGETS:return
        stats=text_stats(line,key)
        if min(stats['left_anchor'],stats['right_anchor'])<anchor:raise ValueError('Accepted anchor/QC discrepancy')
        observe(qc,anchor,key,stats)
    return callback


def pysam_integer_tag(read,name):
    if not read.has_tag(name):return 'missing'
    value=read.get_tag(name)
    return value if type(value) is int else 'invalid_type_or_value'


def pysam_observer(qc):
    """Receives only reads accepted by the unchanged HTSlib eligibility policy."""
    def callback(read):
        cigar=read.cigartuples or [];cursor=read.reference_start
        for i,(op,length) in enumerate(cigar):
            if op==3:
                key=(read.reference_name,cursor,cursor+length+1,read.get_tag('XS'))
                if key in TARGETS:
                    left=0;j=i-1
                    while j>=0 and cigar[j][0] in (0,7,8):left+=cigar[j][1];j-=1
                    right=0;j=i+1
                    while j<len(cigar) and cigar[j][0] in (0,7,8):right+=cigar[j][1];j+=1
                    stats={'left_anchor':left,'right_anchor':right,'MAPQ':read.mapping_quality,
                           'NM':pysam_integer_tag(read,'NM'),'AS':pysam_integer_tag(read,'AS'),
                           'softclip_bases':sum(n for code,n in cigar if code==4),'duplicate_flag':int(read.is_duplicate)}
                    for anchor in (8,15):
                        if min(left,right)>=anchor:observe(qc,anchor,key,stats)
            if op in (0,2,3,7,8):cursor+=length
    return callback


def validate_histograms(qc,counts):
    for anchor in ('8','15'):
        for name in ('canonical','cryptic'):
            row=qc[anchor][name]
            if row['observations']!=counts[anchor][name]:raise ValueError('Target QC/count discrepancy')
            if any(sum(hist.values())!=row['observations'] for hist in row['histograms'].values()):
                raise ValueError('Target histogram does not account for every observation')
