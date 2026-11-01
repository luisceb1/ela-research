#!/usr/bin/env python3
"""One fixed public control, bounded first1M; stream SAM to two parsers."""
import argparse
from collections import Counter
import gzip
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import threading
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.audit_stmn2_junction_contract import sam_junctions
from scripts.hisat2_synthetic_gate import accepted_pysam
from scripts.fetch_gse122069_pilot import disk_guard

TARGETS={('chr8',79611214,79636802,'+'):'canonical',('chr8',79611214,79616822,'+'):'cryptic'}


def empty_counts():
    return {str(a):{'eligible_intron_observations':0,'canonical':0,'cryptic':0} for a in (8,15)}


def verify_file(path,size,md5,sha256=None):
    if path.stat().st_size!=size:raise ValueError('Input size mismatch')
    h,m=hashlib.sha256(),hashlib.md5()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(8*1024**2),b''):h.update(b);m.update(b)
    if md5 is not None and m.hexdigest()!=md5:raise ValueError('Input MD5 mismatch')
    if sha256 is not None and h.hexdigest()!=sha256:raise ValueError('Input SHA256 mismatch')
    return h.hexdigest()


def fastq_qc(path,limit=1000000):
    lengths,base_counts=Counter(),Counter();n=bases=qsum=scanned=0;qmin,qmax=127,0
    with gzip.open(path,'rb') as f:
        for _ in range(limit):
            lines=[f.readline(20000) for _ in range(4)]
            if not lines[0]:break
            if any(not s.endswith(b'\n') for s in lines) or not lines[0].startswith(b'@') or not lines[2].startswith(b'+'):
                raise ValueError('Invalid/truncated FASTQ record')
            seq,qual=lines[1].rstrip(b'\r\n').upper(),lines[3].rstrip(b'\r\n')
            if not seq or len(seq)!=len(qual) or set(seq)-set(b'ACGTN') or min(qual)<33 or max(qual)>126:
                raise ValueError('FASTQ sequence/quality schema failure')
            n+=1;bases+=len(seq);lengths[len(seq)]+=1;base_counts.update(seq)
            qsum+=sum(qual);qmin=min(qmin,min(qual));qmax=max(qmax,max(qual));scanned+=sum(map(len,lines))
    if n!=limit:raise ValueError('FASTQ shorter than fixed pilot')
    return {'reads':n,'length_histogram':dict(lengths),'bases':bases,'N_bases':base_counts[ord('N')],
            'quality_ascii_min':qmin,'quality_ascii_max':qmax,'mean_quality_if_phred33':qsum/bases-33,
            'uncompressed_bytes_scanned':scanned,'selection':'first records in deposited order, not random',
            'scope':'first1M FASTQ QC only, not complete library or full gzip CRC'}


def count_htslib(out,locus_qc=False):
    import pysam
    counts=empty_counts();records=0;locus=Counter();locus_junctions=Counter()
    with pysam.AlignmentFile('-','r') as file:
        for read in file:
            records+=1
            if locus_qc and not(read.is_unmapped or read.is_secondary or read.is_supplementary or read.is_qcfail) and read.reference_name=='chr8' and read.reference_start<79666158 and read.reference_end>79611116:
                blocks=read.get_blocks()
                if any(a<79666158 and b>79611116 for a,b in blocks):
                    locus['primary_block_overlap']+=1
                    unique=(20<=read.mapping_quality<255 and read.has_tag('NH') and read.get_tag('NH')==1)
                    if unique:
                        locus['unique_mapq_block_overlap']+=1
                        for label,left,right in [('exon1',79611116,79611214),('exon2',79636801,79636897)]:
                            if any(a<right and b>left for a,b in blocks):locus[label+'_unique_overlap']+=1
                        if any(op==3 for op,n in (read.cigartuples or [])):
                            locus['unique_spliced_reads']+=1
                            for (left,right),n in file.find_introns([read]).items():
                                if left<79666158 and right>79611116:
                                    xs=read.get_tag('XS') if read.has_tag('XS') else 'missing'
                                    locus_junctions[(left,right+1,xs)]+=n
            if not accepted_pysam(read):continue
            cigar=read.cigartuples or [];cursor=read.reference_start
            introns=file.find_introns([read]) if any(op==3 for op,n in cigar) else {}
            for i,(op,n) in enumerate(cigar):
                if op==3:
                    anchors=[]
                    for ops in (reversed(cigar[:i]),iter(cigar[i+1:])):
                        anchor=0
                        for op2,n2 in ops:
                            if op2 not in (0,7,8):break
                            anchor+=n2
                        anchors.append(anchor)
                    if introns.get((cursor,cursor+n),0):
                        key=(read.reference_name,cursor,cursor+n+1,read.get_tag('XS'))
                        for a in (8,15):
                            if min(anchors)>=a:
                                counts[str(a)]['eligible_intron_observations']+=1
                                if key in TARGETS:counts[str(a)][TARGETS[key]]+=1
                if op in (0,2,3,7,8):cursor+=n
    result={'counts':counts,'sam_records':records,'pysam':pysam.__version__,
            'htslib':pysam.version.__htslib_version__,'self_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    if locus_qc:result['locus_qc']={'block_overlap_counts':dict(locus),'junctions':[{'left_exon_end_1based':left,'right_exon_start_1based':right,'XS':xs,'count':n} for (left,right,xs),n in sorted(locus_junctions.items())],
                                  'scope':'same first1M; overlap is not proven gene assignment; no retargeting'}
    out.write_text(json.dumps(result,indent=2)+'\n')


def run(a):
    phase_start=time.monotonic()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    row=next(r for r in json.loads(Path(a.manifest).read_text())['rows'] if r['run']=='SRR8144907')
    download=json.loads(Path(a.download_record).read_text());fq=Path(a.fastq)
    if not download['verified'] or download['run']!='SRR8144907':raise ValueError('No verified pilot input')
    digest=verify_file(fq,row['fastq_bytes'],row['md5'],download['sha256'])
    disk_guard(out)
    expected=json.loads(Path(a.index_record).read_text())
    for entry in expected['verified_files']:
        path=Path(a.index_directory).parent/entry['name']
        verify_file(path,entry['bytes'],None,entry['sha256'])
    binary_info=json.loads(Path(a.binary_record).read_text())
    binary=Path(a.source)/'hisat2-align-s'
    if hashlib.sha256(binary.read_bytes()).hexdigest()!=binary_info['hisat2-align-s']['sha256']:
        raise ValueError('Aligner binary hash mismatch')
    affinity=sorted(os.sched_getaffinity(0))[:2];os.sched_setaffinity(0,affinity)
    qc=fastq_qc(fq);(out/'fastq_qc.json').write_text(json.dumps(qc,indent=2)+'\n')
    # /proc task children is unavailable here: bound each process address space
    # instead of claiming an aggregate RSS measurement. Caps sum to5.75GiB.
    old_soft,old_hard=resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,old_hard))
    cmd=['prlimit','--as=5368709120','--',str(binary),'--wrapper','basic-0','-x',a.prefix,'-U','-','-u','1000000','-p','2','-k','5','--seed','0','--no-temp-splicesite','--reorder']
    worker=['prlimit','--as=268435456','--',a.pysam_python,str(Path(__file__)), 'htslib','--out',str(out/'htslib_counts.json')]
    if a.locus_qc:worker.append('--locus-qc')
    start=phase_start;counts=empty_counts();qc_sam=Counter();mapq=Counter();nh=Counter()
    result={'run':row['run'],'gsm':row['gsm'],'command':cmd,'worker_command':worker,'cpu_affinity':affinity,
            'fastq_sha256':digest,'complete':False,'sam_disk_written':False,
            'combined_rss_available':False,'virtual_address_caps_total_bytes':5.75*1024**3,
            'virtual_address_caps':{'aligner':5*1024**3,'parent':512*1024**2,'htslib':256*1024**2},
            'prealignment_seconds':time.monotonic()-phase_start}
    procs=[];stop=threading.Event();fail=[]
    def terminate():
        for proc in procs:
            if proc.poll() is None:
                try:os.killpg(proc.pid,signal.SIGKILL)
                except ProcessLookupError:pass
    def monitor():
        while not stop.wait(0.5):
            try:
                if time.monotonic()-start>1800:raise TimeoutError('Pilot exceeds30min')
                disk_guard(out)
            except Exception as exc:fail.append(type(exc).__name__+': '+str(exc));terminate();return
    try:
        with (out/'hisat2.log').open('w') as log,(out/'htslib.stderr.txt').open('w') as err:
            align=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=log,text=True,bufsize=65536,start_new_session=True);procs.append(align)
            hts=subprocess.Popen(worker,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=err,text=True,bufsize=65536,start_new_session=True);procs.append(hts)
            def feed():
                try:
                    with gzip.open(fq,'rt',encoding='ascii') as inp:
                        for _ in range(1000000):
                            for __ in range(4):
                                line=inp.readline()
                                if not line:raise ValueError('FASTQ truncated while streaming')
                                align.stdin.write(line)
                    align.stdin.close()
                except Exception as exc:
                    fail.append('FASTQ producer: '+type(exc).__name__+': '+str(exc));terminate()
            producer=threading.Thread(target=feed,daemon=True);producer.start()
            thread=threading.Thread(target=monitor,daemon=True);thread.start()
            for line in align.stdout:
                hts.stdin.write(line)
                if line.startswith('@'):continue
                fields=line.split('\t');flag=int(fields[1]);qc_sam['sam_records']+=1
                if not flag&(256|2048):qc_sam['primary_records']+=1
                qc_sam['unmapped_records']+=bool(flag&4);qc_sam['secondary_records']+=bool(flag&256)
                qc_sam['supplementary_records']+=bool(flag&2048);qc_sam['qcfail_records']+=bool(flag&512)
                mapq[int(fields[4])]+=1
                tags={p.split(':',2)[0]:p.split(':',2)[2] for p in fields[11:] if p.count(':')>=2}
                nh[tags.get('NH','missing').strip()]+=1
                for anchor in (8,15):
                    for key in sam_junctions(line,min_anchor=anchor):
                        counts[str(anchor)]['eligible_intron_observations']+=1
                        if key in TARGETS:counts[str(anchor)][TARGETS[key]]+=1
            try:hts.stdin.close()
            except BrokenPipeError:
                if fail:raise RuntimeError('; '.join(fail))
                raise
            align_code=align.wait();hts_code=hts.wait();producer.join();stop.set();thread.join()
        if fail:raise RuntimeError('; '.join(fail))
        if align_code or hts_code:raise RuntimeError(f'Pipeline exits: aligner={align_code},htslib={hts_code}')
        other=json.loads((out/'htslib_counts.json').read_text())
        if other['counts']!=counts or other['sam_records']!=qc_sam['sam_records']:raise ValueError('Independent parser counts disagree')
        if qc_sam['primary_records']!=1000000:raise ValueError('Pilot did not process exactly first1M primary records')
        result.update(complete=True,counts=counts,sam_qc=dict(qc_sam),mapq_histogram=dict(mapq),NH_histogram=dict(nh),
                      independent_parser_concordant=True,coverage_rule={'min_denominator':20,
                      'pilot_denominator_reaches20':counts['15']['canonical']+counts['15']['cryptic']>=20,
                      'scope':'technical subset only; no ratio/effect/PSI or biological absence'})
        if a.locus_qc:result['locus_qc']=other['locus_qc']
    except Exception as exc:result['error']=type(exc).__name__+': '+str(exc);terminate();raise
    finally:
        stop.set();terminate()
        for proc in procs:proc.wait()
        result.update(elapsed_seconds=time.monotonic()-start,maxrss_child_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                      self_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      watchdog_errors=fail)
        (out/'pilot_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(__doc__);p.add_argument('mode',choices=['htslib','run']);p.add_argument('--out',required=True)
    p.add_argument('--locus-qc',action='store_true')
    for name in ['manifest','download-record','fastq','index-record','index-directory','binary-record','source','prefix','pysam-python']:p.add_argument('--'+name)
    a=p.parse_args()
    if a.mode=='htslib':count_htslib(Path(a.out),a.locus_qc)
    else:run(a)
