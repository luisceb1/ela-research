"""Supervise the preregistered miniature experiment; no automatic retries."""
import json
import os
import signal
import subprocess
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/'reports/unc13a-minigenome-20261102'

def run(name,argv,cwd=None):
    source=json.loads((ROOT/'source.json').read_text());deadline=source['global_deadline_epoch']
    if time.time()>=deadline:raise RuntimeError('Global 15-minute deadline expired')
    def restrict():
        os.sched_setaffinity(0,sorted(os.sched_getaffinity(0))[:2])
    start=time.time();peak=0;violation=None
    with (ROOT/(name+'.log')).open('w') as log:
        proc=subprocess.Popen(argv,cwd=cwd,stdout=log,stderr=subprocess.STDOUT,start_new_session=True,preexec_fn=restrict)
        while proc.poll() is None:
            rss=0
            for p in Path('/proc').glob('[0-9]*'):
                try:
                    if os.getpgid(int(p.name))==proc.pid:rss+=int((p/'statm').read_text().split()[1])*os.sysconf('SC_PAGE_SIZE')
                except (OSError,ValueError,ProcessLookupError):pass
            peak=max(peak,rss)
            disk=sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file())
            if time.time()>=deadline:violation='global_wall_time'
            elif rss>2*1024**3:violation='process_tree_rss'
            elif disk>1024**3:violation='experiment_disk'
            if violation:
                os.killpg(proc.pid,signal.SIGKILL);break
            time.sleep(.2)
        code=proc.wait()
    record={'name':name,'argv':list(map(str,argv)),'cwd':str(cwd),'seconds':time.time()-start,'exit':code,'max_tree_rss_bytes_sampled':peak,'violation':violation}
    path=ROOT/'commands.json';records=json.loads(path.read_text()) if path.exists() else [];records.append(record);path.write_text(json.dumps(records,indent=2)+'\n')
    if code or violation:raise RuntimeError(f'{name} failed: {record}')
    return record
