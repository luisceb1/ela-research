"""Verify the Windows C: drvfs mount before querying its filesystem availability."""
from pathlib import Path
import os
import re


def free_bytes(mountinfo=None,statvfs=None):
    lines=Path('/proc/self/mountinfo').read_text() if mountinfo is None else mountinfo
    matches=[]
    for line in lines.splitlines():
        before,sep,after=line.partition(' - ')
        if not sep:continue
        fields=before.split()
        if len(fields)>4 and fields[4]=='/mnt/c':matches.append(after.split())
    if not matches:return None
    if len(matches)!=1:raise ValueError('Ambiguous /mnt/c mount')
    fields=matches[0]
    if len(fields)<3:raise ValueError('Incomplete /mnt/c mount record')
    kind,source,options=fields[:3]
    source=re.sub(r'\\([0-7]{3})',lambda m:chr(int(m[1],8)),source)
    tokens=set(re.split('[,;]',options))
    if kind!='9p' or source!='C:\\' or 'aname=drvfs' not in tokens or 'path=C:\\' not in tokens:
        raise ValueError('Refuse non-C or unverified drvfs /mnt/c mapping')
    v=(statvfs or os.statvfs)('/mnt/c')
    if v.f_frsize<=0 or not 0<=v.f_bavail<=v.f_blocks:raise ValueError('Invalid C: filesystem availability')
    return v.f_bavail*v.f_frsize
