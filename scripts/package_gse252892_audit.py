"""Package only bounded metadata from the completed local run; never raw sequencing files."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import zipfile

ROOT=Path(__file__).resolve().parents[1]
PLAN_SHA='61c5f2c73e762ed23d9c940ce7db2b3043713169311e4594d8f87e51d0332369'
MAX_FILE=5*1024**2
MAX_TOTAL=50*1024**2
TOP=['accepted.json','supervision.json','transfer-ledger.json','worker-failure.json','worker.log','progress.json','result.json','index-summary.txt']
LIB=['fastp.json','fastp.log','hisat2.log','hisat2-summary.txt','junction-counts.json']


def read_metadata(path):
    path=Path(path)
    if any(p.is_symlink() for p in [path,*path.parents]):raise ValueError('Symlink in audit source')
    info=path.stat()
    if not stat.S_ISREG(info.st_mode) or info.st_size>MAX_FILE:raise ValueError('Oversized/non-regular audit metadata')
    with path.open('rb') as f:data=f.read(MAX_FILE+1)
    if len(data)>MAX_FILE:raise ValueError('Metadata grew beyond cap')
    return data


def sha(data):return hashlib.sha256(data).hexdigest()


def lineage_plans(node):
    if isinstance(node,dict):
        if 'prior_plan_path' in node:yield Path(node['prior_plan_path']),node['prior_plan_sha256']
        for v in node.values():yield from lineage_plans(v)
    elif isinstance(node,list):
        for v in node:yield from lineage_plans(v)


def verify_archive(path):
    with zipfile.ZipFile(path) as z:
        names=z.namelist()
        if len(names)!=len(set(names)) or len(names)>10000:raise ValueError('Duplicate/oversized member list')
        if sum(i.file_size for i in z.infolist())>MAX_TOTAL+MAX_FILE:raise ValueError('Archive metadata cap exceeded')
        manifest=json.loads(z.read('MANIFEST.json'))
        if set(names)!={'MANIFEST.json',*(r['member'] for r in manifest['files'])}:raise ValueError('Archive inventory mismatch')
        for r in manifest['files']:
            b=z.read(r['member'])
            if len(b)!=r['bytes'] or sha(b)!=r['sha256']:raise ValueError('Archive digest mismatch')
        return manifest


def package(plan_path,output):
    plan_path=Path(plan_path).absolute();output=Path(output).absolute();partial=output.with_name(output.name+'.partial')
    if output.exists() or partial.exists():raise ValueError('New output required; no overwrite')
    raw_plan=read_metadata(plan_path)
    if sha(raw_plan)!=PLAN_SHA:raise ValueError('Expected exact completed run06 proposal')
    plan=json.loads(raw_plan);root=Path(plan['run_root'])
    roots=[Path(p) for p in plan['lineage']['prior_roots']]+[root]
    if len(roots)!=6 or len(set(roots))!=6 or any(not p.is_absolute() for p in roots):raise ValueError('Expected six distinct absolute run roots')
    if any(output==p or p in output.parents for p in roots) or ROOT in output.parents:raise ValueError('Archive must be outside source roots and checkout')
    sup=json.loads(read_metadata(root/'supervision.json'));result=json.loads(read_metadata(root/'result.json'));ledger=json.loads(read_metadata(root/'transfer-ledger.json'))
    if sup.get('status')!='completed' or sup.get('failure') is not None or sup.get('cleanup_error') is not None or sup.get('plan_sha256')!=PLAN_SHA:raise ValueError('Expected clean completed supervision')
    if result!=json.loads((ROOT/'reports/gse252892-local-result-20261114/user-reported-result.json').read_text()):raise ValueError('Actual counts/QC differ from reported output; inspect before archival')
    if ledger.get('active_requests')!=[] or not 0<=ledger['actual_body_bytes']<=ledger['body_upper_bound_bytes']<=14000000000:raise ValueError('Invalid final transfer accounting')
    for lib in result['libraries']:
        if json.loads(read_metadata(root/lib['gsm']/'junction-counts.json'))!=lib:raise ValueError('Per-library result mismatch')
    entries={};total=0
    def add(path,member):
        nonlocal total
        path=Path(path);b=read_metadata(path)
        if member in entries:
            if entries[member][0]!=str(path):raise ValueError('Archive member collision')
            return
        total+=len(b)
        if total>MAX_TOTAL or len(entries)>=9999:raise ValueError('Audit metadata budget exceeded')
        entries[member]=(str(path),b)
    add(plan_path,'plans/'+plan_path.name)
    plans=[(plan_path,PLAN_SHA),*lineage_plans(plan['lineage'])]
    for path,wanted in plans:
        if sha(read_metadata(path))!=wanted:raise ValueError('Source plan SHA changed')
        add(path,'plans/'+path.name);claim=Path(str(path)+'.claimed.json')
        if json.loads(read_metadata(claim))!={'plan_sha256':wanted,'transfer_bytes':14000000000}:raise ValueError('Consumed source claim changed')
        add(claim,'plans/'+claim.name)
    if sha(read_metadata(plan['base_path']))!=plan['base_sha256']:raise ValueError('Base descriptor SHA changed')
    add(Path(plan['base_path']),'plans/'+Path(plan['base_path']).name)
    for i,d in enumerate(roots,1):
        if d.is_symlink() or not d.is_dir():raise ValueError('Invalid source root')
        for required in ['accepted.json','supervision.json','transfer-ledger.json']:read_metadata(d/required)
        prefix=f'runs/{i:02d}/'
        for name in TOP:
            p=d/name
            if p.exists() or p.is_symlink():add(p,prefix+name)
        receipts=d/'transport-receipts'
        if receipts.is_symlink():raise ValueError('Symlink receipt directory')
        if receipts.exists():
            for p in sorted(receipts.glob('*.json')):add(p,prefix+'transport-receipts/'+p.name)
        for gsm in ['GSM8009878','GSM8009881']:
            directory=d/gsm
            if directory.is_symlink():raise ValueError('Symlink library directory')
            for name in LIB:
                p=directory/name
                if p.exists() or p.is_symlink():add(p,prefix+gsm+'/'+name)
            if directory.exists():
                for p in sorted(directory.glob('*.verified.json')):add(p,prefix+gsm+'/'+p.name)
    files=[{'member':m,'source':p,'bytes':len(b),'sha256':sha(b)} for m,(p,b) in sorted(entries.items())]
    manifest={'schema':'gse252892-audit-metadata-v1','source_plan_sha256':PLAN_SHA,'source_roots':[str(p) for p in roots],
        'metadata_only':True,'raw_inputs_included':False,'source_input_hashes_recomputed':False,
        'meaning':'Exact metadata copy with member hashes; not a raw-data replay or proof of FASTQ integrity today.',
        'metadata_bytes':total,'files':files}
    with zipfile.ZipFile(partial,'x',compression=zipfile.ZIP_DEFLATED) as z:
        for m,(_,b) in sorted(entries.items()):z.writestr(m,b)
        z.writestr('MANIFEST.json',json.dumps(manifest,indent=2)+'\n')
    verify_archive(partial)
    # Publish without replacing a concurrently created output; preserve failure evidence.
    with output.open('xb') as dst,partial.open('rb') as src:
        for b in iter(lambda:src.read(1024**2),b''):dst.write(b)
        dst.flush();os.fsync(dst.fileno())
    verify_archive(output);partial.unlink()
    return {'status':'metadata_archive_verified','output':str(output),'zip_bytes':output.stat().st_size,
        'zip_sha256':sha(output.read_bytes()),'metadata_members':len(entries),'metadata_bytes':total,
        'raw_inputs_included':False,'sources_deleted':0,'final_transfer_ledger':ledger}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--plan',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();print(json.dumps(package(a.plan,a.output),indent=2))

if __name__=='__main__':main()
