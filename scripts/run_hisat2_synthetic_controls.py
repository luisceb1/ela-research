#!/usr/bin/env python3
"""Run the prospectively fixed commands on synthetic reads only."""
import argparse
import json
from pathlib import Path
import resource
import subprocess
import time


def run(source, genome, out):
    out.mkdir(parents=True, exist_ok=True)
    mini=out/'mini_index'
    commands=[('mini_build',[str(source/'hisat2-build'),str(out/'mini_reference.fa'),str(mini)]),
              ('genome',[str(source/'hisat2'),'-x',genome,'-U',str(out/'synthetic_reads.fastq'),'-S',str(out/'genome.sam'),'-p','2','-k','5','--seed','0','--no-temp-splicesite','--reorder']),
              ('mini',[str(source/'hisat2'),'-x',str(mini),'-U',str(out/'mini_reads.fastq'),'-S',str(out/'mini.sam'),'-p','2','-k','5','--seed','0','--no-temp-splicesite','--reorder'])]
    records=[]
    try:
        for name,args in commands:
            cmd=['prlimit','--as=6442450944','--','timeout','600',*args]
            start=time.monotonic()
            with (out/(name+'.log')).open('w') as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
            records.append({'name':name,'command':cmd,'exit_code':r.returncode,'elapsed_seconds':time.monotonic()-start,
                            'maxrss_children_so_far_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss})
            if r.returncode:raise RuntimeError(f'{name} exited {r.returncode}')
    finally:
        (out/'alignment_commands.json').write_text(json.dumps({'records':records,'real_fastq_reads':0,
              'memory_scope':'maximum child RSS observed across all commands so far, not separate per-command measurement'},indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser(__doc__);p.add_argument('--source',required=True);p.add_argument('--genome',required=True);p.add_argument('--out',required=True);a=p.parse_args()
    run(Path(a.source),a.genome,Path(a.out))
