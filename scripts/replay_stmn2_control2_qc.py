#!/usr/bin/env python3
"""Fixed post hoc technical QC replay, preserving original FASTQ names in transit only."""
import argparse
from collections import Counter
import gzip
import json
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts import gse122069_full_control as full
from scripts.stmn2_target_alignment_qc import empty_qc,text_observer,pysam_observer,validate_histograms
SOURCE_READS=54292655
INTERVALS=((1,1000000),(17000001,18000000),(37000001,38000000),(42000001,43000000),(54000001,54292655))
SELECTED_READS=4292655
SHA256='ed2f2f4a30b7f448c246029b0407e20e142493b2d74345e674c4e7b3c3e5527f'
EXPECTED={'15':{'canonical':13,'cryptic':3},'8':{'canonical':15,'cryptic':4}}


def validate_intervals(source_reads,intervals,expected):
    if type(source_reads) is not int or source_reads<=0 or not intervals:raise ValueError('Invalid source/intervals')
    end=total=0
    for lo,hi in intervals:
        if type(lo) is not int or type(hi) is not int or not end<lo<=hi<=source_reads:raise ValueError('Invalid/overlapping intervals')
        total+=hi-lo+1;end=hi
    if total!=expected:raise ValueError('Selected count/interval mismatch')


def select_fastq(path,target,expected,complete_library=False,checkpoint=None,*,source_reads=SOURCE_READS,intervals=INTERVALS):
    if complete_library:raise ValueError('Selected replay cannot be complete library alignment')
    validate_intervals(source_reads,intervals,expected)
    lengths=Counter();n=bases=nbase=qsum=scanned=0;qmin,qmax=127,0;idx=0
    with gzip.open(path,'rb') as inp:
        for ordinal in range(1,source_reads+1):
            lines=[inp.readline(20000) for _ in range(4)]
            if any(not x.endswith(b'\n') for x in lines) or not lines[0].startswith(b'@') or not lines[2].startswith(b'+'):
                raise ValueError('Invalid/truncated source FASTQ record')
            scanned+=sum(map(len,lines))
            while idx<len(intervals) and ordinal>intervals[idx][1]:idx+=1
            if idx==len(intervals) or ordinal<intervals[idx][0]:continue
            seq=lines[1].rstrip(b'\r\n').upper();qual=lines[3].rstrip(b'\r\n')
            if not seq or len(seq)!=len(qual) or set(seq)-set(b'ACGTN') or min(qual)<33 or max(qual)>126:
                raise ValueError('Selected FASTQ sequence/quality schema failure')
            target.write(b''.join(lines).decode('ascii'))
            n+=1;bases+=len(seq);nbase+=seq.count(b'N');lengths[len(seq)]+=1;qsum+=sum(qual)
            qmin=min(qmin,min(qual));qmax=max(qmax,max(qual))
            if checkpoint and n%1000000==0:
                checkpoint({'reads_streamed':n,'source_ordinal_scanned':ordinal,'gzip_eof_crc_validated':False})
        if inp.read(1):raise ValueError('Extra source FASTQ record')
    if n!=expected:raise ValueError('Selected FASTQ count mismatch')
    return {'reads':n,'source_reads_scanned':source_reads,'bases':bases,'N_bases':nbase,'length_histogram':dict(lengths),
            'quality_ascii_min':qmin,'quality_ascii_max':qmax,'mean_quality_if_phred33':qsum/bases-33,
            'uncompressed_bytes_scanned':scanned,'gzip_eof_crc_validated':True,
            'intervals_1based_inclusive':intervals,'selection':'fixed post hoc ordinal intervals; not random; only selected records aligned',
            'sequence_quality_schema_scope':'selected records; source framing and CRC checked throughout; whole source identity pinned by hash'}


def worker(out,expected,bin_size):
    qc=empty_qc()
    full.count_htslib(out,expected,bin_size,on_accepted_read=pysam_observer(qc))
    obj=json.loads(Path(out).read_text());validate_histograms(qc,obj['counts'])
    obj['target_qc_histograms']=qc;obj['complete_query_stream']=obj['complete_library'];obj['complete_library']=False
    obj['input_scope']='received selected stream only; parent verifies real source identity separately'
    full.save(out,obj)


def replay(a):
    qc=empty_qc();callback=text_observer(qc);start=time.monotonic()
    result={'replay_complete':False,'complete_source_library_realigned':False,'scope':'post hoc technical QC, same SRR8144908; no rates, effect, PSI or new replication',
            'source_reads':SOURCE_READS,'selected_reads':SELECTED_READS,'intervals_1based_inclusive':INTERVALS,'expected_target_counts':EXPECTED,
            'coverage_policy':'whole source library already passed >=20; selection-enriched subset is not assessed for coverage',
            'missing_tag_policy':'missing distinct from zero; duplicate flag is not molecular deduplication'}
    out=Path(a.out)
    if out.exists() and any(out.iterdir()):raise ValueError('Refuse non-empty replay output')
    if a.max_reads!=SELECTED_READS or a.complete_library or a.run_accession!='SRR8144908' or a.phase_deadline_seconds!=600:
        raise ValueError('Frozen replay configuration changed')
    receipt=json.loads(Path(a.download_record).read_text())
    if receipt.get('sha256')!=SHA256:raise ValueError('Replay source receipt does not match pinned SHA256')
    def counter(lines,bins,forward=None):return full.count_text(lines,bins,forward,on_accepted_junction=callback)
    try:
        full.run(a,fastq_feeder=select_fastq,text_counter=counter,worker_script=Path(__file__))
        own=json.loads((out/'full-control-results.json').read_text());other=json.loads((out/'htslib-checkpoint.json').read_text())
        validate_histograms(qc,own['counts'])
        if qc!=other['target_qc_histograms']:raise ValueError('Independent QC histograms disagree')
        for anchor,counts in EXPECTED.items():
            for name,value in counts.items():
                if own['counts'][anchor][name]!=value:raise ValueError('Prespecified replay target count mismatch')
        fq=json.loads((out/'fastq_qc.json').read_text())
        if fq['source_reads_scanned']!=SOURCE_READS or fq['reads']!=SELECTED_READS or not fq['gzip_eof_crc_validated']:
            raise ValueError('Selected source completion failed')
        if own['complete_library'] or other['complete_library'] or not other['complete_query_stream']:raise ValueError('Invalid completion scope')
        if time.monotonic()-start>600:raise TimeoutError('Replay exceeds frozen 600s including identity checks')
        result.update(replay_complete=True,independent_counts_and_histograms_concordant=True,target_counts=EXPECTED)
    except Exception as exc:
        result['error']=type(exc).__name__+': '+str(exc)
        raise
    finally:
        if out.exists():
            result.update(elapsed_seconds=time.monotonic()-start,target_qc_histograms=qc)
            full.save(out/'replay-results.json',result)


if __name__=='__main__':
    p=argparse.ArgumentParser(__doc__);p.add_argument('mode',choices=['run','htslib']);p.add_argument('--out',required=True)
    p.add_argument('--max-reads',type=int,default=SELECTED_READS);p.add_argument('--bin-size',type=int,default=1000000)
    p.add_argument('--complete-library',action='store_true');p.add_argument('--run-accession',default='SRR8144908')
    p.add_argument('--phase-deadline-seconds',type=int,default=600)
    for name in ['manifest','download-record','fastq','index-record','index-directory','binary-record','source','prefix','pysam-python']:p.add_argument('--'+name)
    a=p.parse_args()
    if a.mode=='htslib':worker(Path(a.out),a.max_reads,a.bin_size)
    else:replay(a)
