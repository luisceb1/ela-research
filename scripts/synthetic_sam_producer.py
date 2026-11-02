"""Fixed synthetic SAM replay, validates prefix names only; never an aligner."""
import argparse
import gzip
from pathlib import Path
import sys
import time
from paired_fastq_integrity import record


def emit(sam,r1,r2,behavior):
    names=set()
    with gzip.open(r1,'rb') as a,gzip.open(r2,'rb') as b:
        while True:
            x,y=record(a,1),record(b,2)
            if x is None and y is None:break
            if x is None or y is None or x[0]!=y[0] or x[0] in names:raise ValueError('Synthetic prefix identity mismatch')
            names.add(x[0])
            if len(names)>64:raise ValueError('Synthetic replay limited to64pairs')
    observed=set();total=0
    # Precheck bounded fixture membership before emitting any SAM payload.
    with Path(sam).open('rb') as f:
        while True:
            line=f.readline(65537)
            if not line:break
            total+=len(line)
            if total>1024**2 or len(line)>65536 or not line.endswith(b'\n'):raise ValueError('Synthetic SAM cap/framing')
            if not line.startswith(b'@'):observed.add(line.split(b'\t',1)[0])
    if observed!=names:raise ValueError('Synthetic replay names differ from verified prefix')
    with Path(sam).open('rb') as f:
        for chunk in iter(lambda:f.read(65536),b''):sys.stdout.buffer.write(chunk)
    sys.stdout.buffer.flush()
    if behavior=='stall':time.sleep(30)
    return 7 if behavior=='exit7' else 0


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--sam',type=Path,required=True);p.add_argument('--r1',type=Path,required=True);p.add_argument('--r2',type=Path,required=True);p.add_argument('--behavior',choices=('ok','exit7','stall'),required=True);a=p.parse_args()
    raise SystemExit(emit(a.sam,a.r1,a.r2,a.behavior))
