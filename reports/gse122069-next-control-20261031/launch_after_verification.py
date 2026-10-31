#!/usr/bin/env python3
"""One-shot launcher of fixed SRR8144908 after already-started download.

No download, retry, budget increase, alternate run or clinical fields here.
Commands and original entrypoints are recorded in this repository.
"""
from pathlib import Path
import json
import os
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent

def read(path):return json.loads(path.read_text())
def write(path,value):
    tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(value,indent=2)+'\n');os.replace(tmp,path)

if __name__=='__main__':
    os.chdir(ROOT)
    start=time.monotonic()
    try:
        while True:
            try:
                if (OUT/'download-launcher.json').exists():
                    launched=read(OUT/'download-launcher.json')
                    if launched['exit_code']!=0:raise RuntimeError('Selected control download failed; alignment not started')
                    receipt=read(OUT/'download.json')
                    if receipt.get('verified') is not True or receipt.get('run')!='SRR8144908':
                        raise ValueError('No verified selected-control receipt')
                    if (OUT/'index-restore-verification.json').exists():
                        index=read(OUT/'index-restore-verification.json')
                        if not index['all_9_member_hashes_match_previous_record']:raise ValueError('Index restore not verified')
                        break
            except json.JSONDecodeError:
                pass  # writer may be finishing; never infer readiness from a partial JSON
            if time.monotonic()-start>2000:raise TimeoutError('No verified readiness within fixed download supervision window')
            time.sleep(2)
        command=read(ROOT/'reports/gse122069-parameterization-20261031/next-control/commands.json')['alignment_argv_after_verified_download']
        command[0]=sys.executable
        assert not (OUT/'execution').exists()
        os.sched_setaffinity(0,sorted(os.sched_getaffinity(0))[:2])
        write(OUT/'alignment-command.json',{'argv':command,'run':'SRR8144908','phase_deadline_seconds':2700,
              'verified_download_sha256':receipt['sha256'],'index_restore_verified':True,'other_runs_excluded':True})
        with (OUT/'execution-progress.txt').open('w') as log,(OUT/'execution-stderr.txt').open('w') as err:
            phase=time.monotonic();process=subprocess.Popen(command,stdout=log,stderr=err)
            write(OUT/'active-process.json',{'engine_pid':process.pid,'scope':'control2 technical phase only'})
            code=process.wait()
        write(OUT/'launcher.json',{'exit_code':code,'elapsed_seconds':time.monotonic()-phase,'readiness_wait_seconds':phase-start})
        print('second-control phase exit',code,flush=True)
        sys.exit(code)
    except Exception as exc:
        write(OUT/'readiness-or-launch-error.json',{'complete_library':False,'run':'SRR8144908','error':type(exc).__name__+': '+str(exc),'alignment_started':(OUT/'alignment-command.json').exists()})
        raise
