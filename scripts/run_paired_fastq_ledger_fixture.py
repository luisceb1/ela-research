"""Reproducible synthetic-only transfer -> integrity -> cached resume receipt."""
import argparse
import copy
import gzip
import hashlib
import json
from pathlib import Path
from pilot_dry_runner import DryRunner
from process_supervisor_v2 import atomic_json


def run(root):
    root=Path(root)
    data=[gzip.compress(b''.join(f'@fixture{i}/{m}\nACGT\n+\nIIII\n'.encode() for i in range(3)),mtime=0) for m in (1,2)]
    expected=[{'bytes':len(b),'md5':hashlib.md5(b).hexdigest(),'sha256':hashlib.sha256(b).hexdigest()} for b in data]
    manifest={'paired_fastq':{'pair':{'mates':[{'identity':f'fixture/R{i+1}','transfer':f'mate{i+1}','expected':e} for i,e in enumerate(expected)],'prefix_pairs':2}}}
    limits={'wall_seconds':100,'transfer_bytes':10000,'disk_bytes':2*1024**2,'reserve_bytes':0}
    a=DryRunner(root,manifest,limits,clock=lambda:100)
    try:
        for i,b in enumerate(data):a.transfer(f'mate{i+1}',[b],expected[i])
        a.paired_fastq('pair');before=copy.deepcopy(a.state)
    finally:a.close()
    b=DryRunner(root,manifest,limits,clock=lambda:101)
    try:
        b.paired_fastq('pair')
        if b.state!=before:raise AssertionError('Resume changed ledger')
        summary={'same_ledger_on_resume':True,'transfer_bytes_consumed':b.state['transfer_bytes_consumed'],'deadline_epoch':b.state['deadline_epoch'],'pairs_scanned':3,'prefix_pairs':2,'clock':'injected synthetic epoch 100 -> 101; not a timing benchmark','raw_execution_ready':False}
    finally:b.close()
    atomic_json(root/'manifest.json',manifest);atomic_json(root/'summary.json',summary)
    return summary


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--synthetic-root',type=Path,required=True)
    print(json.dumps(run(p.parse_args().synthetic_root),indent=2))
