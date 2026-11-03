"""Linux PID-namespace-aware group watchdog and per-command atomic receipts.

Commands MUST NOT detach or change process groups. RSS cap is sampled, not a
kernel-enforced aggregate-memory ceiling. Short commands may be unmeasured.
"""
import json
import os
from pathlib import Path
import re
import resource
import signal
import subprocess
import tempfile
import time

def atomic_json(path,data):
    path=Path(path);fd,tmp=tempfile.mkstemp(prefix='receipt-',dir=path.parent)
    try:
        with os.fdopen(fd,'w') as f:json.dump(data,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
        os.replace(tmp,path)
        directory=os.open(path.parent,os.O_DIRECTORY)
        try:os.fsync(directory)
        finally:os.close(directory)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)

def proc_info(pid):
    fields=Path(f'/proc/{pid}/stat').read_text().rsplit(')',1)[1].split()
    return {'group':int(fields[2]),'state':fields[0],
            'rss':int(fields[21])*os.sysconf('SC_PAGE_SIZE')}

def group_rss(group):
    found=[]
    for p in Path('/proc').glob('[0-9]*'):
        try:
            info=proc_info(p.name)
            if info['group']==group and info['state']!='Z':found.append((int(p.name),info['rss']))
        except (OSError,ValueError,IndexError):pass
    return sum(rss for _,rss in found),[pid for pid,_ in found]

def supervise(name,argv,folder,timeout=5,rss_limit=128*1024**2,address_space=128*1024**2,checkpoint=None,group_checkpoint=None):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    if not re.fullmatch('[A-Za-z0-9_-]+',name):raise ValueError('Invalid command name')
    receipt=folder/(name+'.json');lock=folder/(name+'.lock')
    fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY);os.close(fd)
    if receipt.exists():raise ValueError('Receipt already exists')
    start=time.monotonic();record={'name':name,'argv':argv,'status':'started','memory_mode':'sampled group RSS; per-process RLIMIT_AS','detaching_supported':False}
    atomic_json(receipt,record)
    read_fd,write_fd=os.pipe()
    def setup():
        host_pid=int(os.readlink('/proc/self'))
        group=proc_info(host_pid)['group']
        os.write(write_fd,json.dumps({'namespace_pid':os.getpid(),'procfs_pid':host_pid,'procfs_group':group}).encode());os.close(write_fd)
        os.sched_setaffinity(0,sorted(os.sched_getaffinity(0))[:2])
        resource.setrlimit(resource.RLIMIT_AS,(address_space,address_space))
    proc=None
    try:
        with (folder/(name+'.log')).open('w') as log:
            proc=subprocess.Popen(argv,stdout=log,stderr=subprocess.STDOUT,start_new_session=True,preexec_fn=setup,pass_fds=(write_fd,))
            os.close(write_fd);write_fd=None
            identity=json.loads(os.read(read_fd,4096));record.update(identity)
            atomic_json(receipt,record)
            peak=0;samples=0;max_members=0;violation=None
            while True:
                if checkpoint is not None:checkpoint()
                code=proc.poll();rss,members=group_rss(identity['procfs_group'])
                if members:samples+=1;peak=max(peak,rss);max_members=max(max_members,len(members))
                if group_checkpoint is not None:group_checkpoint(rss,members,identity)
                if time.monotonic()-start>timeout:violation='timeout'
                elif rss>rss_limit:violation='memory'
                elif code is not None and members:violation='lingering_descendants'
                if violation:
                    try:os.killpg(proc.pid,signal.SIGKILL)
                    except ProcessLookupError:pass
                    break
                if code is not None:break
                time.sleep(.01)
            record.update(exit_code=proc.wait(),violation=violation,peak_group_rss_bytes_sampled=peak if samples and peak>0 else None,samples=samples,max_group_members=max_members,rss_observed=bool(samples and peak>0))
            # Await reaping/zombie transition; no live members should remain.
            for _ in range(100):
                _,remaining=group_rss(identity['procfs_group'])
                if not remaining:break
                time.sleep(.01)
            record['live_group_members_after_cleanup']=remaining
    except BaseException as exc:
        if proc is not None:
            try:os.killpg(proc.pid,signal.SIGKILL)
            except ProcessLookupError:pass
            record['exit_code']=proc.wait()
            if 'procfs_group' in record:
                for _ in range(100):
                    _,remaining=group_rss(record['procfs_group'])
                    if not remaining:break
                    time.sleep(.01)
                record['live_group_members_after_cleanup']=remaining
        record['supervisor_error']=f'{type(exc).__name__}: {exc}'
        raise
    finally:
        os.close(read_fd)
        if write_fd is not None:os.close(write_fd)
        record.update(status='finished',elapsed_seconds=time.monotonic()-start)
        atomic_json(receipt,record)
    return record
