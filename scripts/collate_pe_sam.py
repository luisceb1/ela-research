"""Disk-backed lexicographic (RG,QNAME) SAM sort. No read filtering."""
import argparse
import os
from pathlib import Path
import subprocess

def collate(source,destination,scratch):
    scratch=Path(scratch);scratch.mkdir(parents=True,exist_ok=True)
    keyed=scratch/'keyed.tsv';ordered=scratch/'ordered.tsv';headers=[]
    with Path(source).open() as incoming,keyed.open('w') as out:
        for line in incoming:
            if line.startswith('@'):headers.append(line);continue
            fields=line.rstrip('\n').split('\t')
            if len(fields)<11:raise ValueError('Truncated SAM')
            rgs=[v[5:] for v in fields[11:] if v.startswith('RG:Z:')]
            if len(rgs)>1:raise ValueError('Duplicate RG')
            rg=rgs[0] if rgs else '<missing>'
            if not all(ord(c)<128 for c in rg+fields[0]):raise ValueError('ASCII collation contract')
            out.write(rg+'\t'+fields[0]+'\t'+line)
    with ordered.open('w') as out:
        subprocess.run(['sort','--stable','-S','1M','-T',str(scratch),'-t','\t','-k1,1','-k2,2',str(keyed)],stdout=out,env={**os.environ,'LC_ALL':'C'},check=True)
    with Path(destination).open('w') as out,ordered.open() as ordered_in:
        out.writelines(headers)
        for line in ordered_in:out.write(line.split('\t',2)[2])
    keyed.unlink();ordered.unlink()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('destination');p.add_argument('scratch');a=p.parse_args();collate(a.source,a.destination,a.scratch)
