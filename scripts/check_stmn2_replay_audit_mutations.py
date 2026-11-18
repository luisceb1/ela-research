"""Run negative controls against an external supplied STMN2 evidence archive."""
import sys,json,tarfile,tempfile,io,argparse
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import audit_stmn2_replay_bundle as a
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--bundle',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
src=args.bundle
data=a.load_bundle(src)
def changed_json(name,fn):
 d=data.copy();o=json.loads(d[name]);fn(o);d[name]=json.dumps(o).encode();return d
p=a.PREFIX
cases=[('wrong-plan',dict(data,**{a.PLAN:data[a.PLAN]+b' '})),
 ('changed-count',changed_json(p+'result.json',lambda o:o['libraries'][0]['counts'].update(canonical=1946))),
 ('changed-qc',changed_json(p+'result.json',lambda o:o['libraries'][0]['qc'].update(sam_records=139759298))),
 ('per-library-conflict',changed_json(p+'GSM8009878/stmn2-counts.json',lambda o:o['counts'].update(canonical=1946))),
 ('failed-supervisor',changed_json(p+'supervision.json',lambda o:o.update(failure='error'))),
 ('exceeded-rss',changed_json(p+'supervision.json',lambda o:o.update(peak_sampled_group_rss_bytes=7*1024**3))),
 ('insufficient-physical-space',changed_json(p+'supervision.json',lambda o:o.update(minimum_sampled_physical_c_available_bytes=1))),
 ('wrong-claim',changed_json(a.PLAN+'.claimed.json',lambda o:o.update(plan_sha256='0'*64))),
 ('changed-fastp-command',changed_json(p+'GSM8009878/fastp.json',lambda o:o.update(command=o['command']+' --other'))),
 ('changed-fastp-pairs',changed_json(p+'GSM8009878/fastp.json',lambda o:o['summary']['after_filtering'].update(total_reads=1))),
 ('missing-log',{k:v for k,v in data.items() if k!=p+'GSM8009878/fastp.log'}),
 ('unsafe-member',dict(data,**{'../outside':b'unsafe'}))]
results=[]
with tempfile.TemporaryDirectory() as tmp:
 for i,(name,d) in enumerate(cases):
  path=Path(tmp)/f'{i}.tar.gz'
  with tarfile.open(path,'w:gz') as t:
   for n,b in d.items():
    info=tarfile.TarInfo(n);info.size=len(b);t.addfile(info,io.BytesIO(b))
  try:a.audit(path)
  except (ValueError,KeyError) as e:results.append({'case':name,'outcome':'refused','reason':str(e)})
  else:raise AssertionError('Incorrectly accepted '+name)
with args.output.open('x') as output:
 output.write(json.dumps(results,indent=2)+'\n')
print(json.dumps({'negative_cases':len(results),'refused':len(results)}))
