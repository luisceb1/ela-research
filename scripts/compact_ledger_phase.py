"""Compact computation bound to synthetic source, policy, dependencies and ledger."""
import hashlib
import importlib
import json
from pathlib import Path
import re

from paired_fastq_integrity import file_digest
from paired_fastq_phase import digest,sha
from process_supervisor_v2 import atomic_json


def decoder_identity():
    import pysam
    files={'pysam':Path(pysam.__file__)}
    for key in ('pysam.libcalignedsegment','pysam.libchtslib'):files[key]=Path(importlib.import_module(key).__file__)
    for name in ('compact_pe_pipeline.py','pe_fragment_contract.py','compact_ledger_phase.py','pilot_execution_policy.py','pilot_dry_runner.py','external_local_stage.py','process_supervisor_v2.py'):files[name]=Path(__file__).with_name(name)
    return {'pysam_version':pysam.__version__,'samtools_version':pysam.__samtools_version__,'sha256':{k:sha(v) for k,v in files.items()}}


def contract(runner,name):
    if not runner.policy:raise ValueError('Compact ledger requires explicit execution policy')
    caps=runner.phase_policy(name,'compact')
    spec=runner.manifest.get('compact',{}).get(name)
    keys={'source_scope','transfer','library','targets','limits','decoder','minimum_fragment_union'}
    if not isinstance(spec,dict) or set(spec)!=keys or spec['source_scope']!='existing-synthetic-sam-only':raise ValueError('Synthetic compact contract required')
    if type(spec['minimum_fragment_union']) is not int or spec['minimum_fragment_union']<=0:raise ValueError('Fixed positive union coverage required')
    from compact_pe_pipeline import validate
    validate(spec['library'],spec['targets'],spec['limits'])
    if spec['limits']['max_temp_bytes']>runner.policy['allocations']['temporaries']:raise ValueError('Compact temp cap exceeds partition')
    if 2*spec['limits']['max_result_bytes']>runner.policy['allocations']['receipts']:raise ValueError('Receipt staging exceeds partition')
    if spec['decoder']!=decoder_identity():raise ValueError('Decoder version or binary/script hash changed')
    source=spec['transfer']
    if not isinstance(source,str) or not re.fullmatch('[A-Za-z0-9_-]+',source):raise ValueError('Named synthetic transfer required')
    p=runner.state['phases'].get(source,{})
    if p.get('kind')!='transfer' or p.get('status')!='verified':raise ValueError('Verified source required')
    if file_digest(runner.root/source,runner.guard)!={'bytes':p['bytes'],'sha256':p['sha256']}:raise ValueError('Compact source changed')
    binding={'policy':'compact-ledger-v1','spec':spec,'phase_caps':caps,'fingerprint':runner.state['fingerprint'],'source_receipt_sha256':digest(p)}
    if 'attempts_used' in p:
        receipt=runner.root/f"{source}.attempt-{p['attempts_used']-1}.json";rec=json.loads(receipt.read_text())
        if rec.get('status')!='verified' or rec.get('body_bytes')!=p['bytes'] or any(rec.get(k)!=p[k] for k in ('md5','sha256')):raise ValueError('Incomplete compact source HTTP receipt')
        binding['http_receipt_sha256']=sha(receipt)
    return binding,digest(binding)


def coverage(result,spec):
    primary=result['routes']['text15'];union=primary['target_fragment_union']
    return {'definition':'accepted RG/QNAME groups with at least one target; marked duplicates retained, not unique molecules','anchor':15,'fragment_union':union,'event_support_sum':primary['target_event_support_sum'],'minimum':spec['minimum_fragment_union'],'adequate':union>=spec['minimum_fragment_union']}


def verify_compact(runner,name,phase):
    binding,signature=contract(runner,name)
    if binding!=phase['binding'] or signature!=phase['signature']:raise ValueError('Compact binding changed')
    out=runner.root/'compact'/name
    if sha(out/'receipt.json')!=phase['receipt_sha256']:raise ValueError('Compact receipt changed')
    receipt=json.loads((out/'receipt.json').read_text())
    if receipt.get('status')!='verified' or receipt['binding']!=binding or sha(out/'result.json')!=receipt['result_sha256']:raise ValueError('Compact result/receipt changed')
    result=json.loads((out/'result.json').read_text())
    source=runner.state['phases'][binding['spec']['transfer']]
    if result.get('status')!='verified' or result.get('producer_exit_code')!=0 or result.get('source_sha256')!=source['sha256']:raise ValueError('Incomplete compact result')
    if receipt['coverage']!=coverage(result,binding['spec']) or phase['coverage']!=receipt['coverage']:raise ValueError('Coverage receipt changed')
    runner.guard()


def run_compact(runner,name):
    binding,signature=contract(runner,name)
    if not runner.begin(name,'compact',signature):
        phase=runner.state['phases'][name];verify_compact(runner,name,phase);return phase
    phase=runner.state['phases'][name];phase['binding']=binding;runner.save();out=runner.root/'compact'/name
    try:
        from compact_pe_pipeline import run
        spec=binding['spec']
        with (runner.root/spec['transfer']).open('rb') as stream:
            result=run(stream,out,spec['library'],spec['targets'],spec['limits'],lambda:runner.compact_reduction(name),checkpoint=runner.guard)
        if contract(runner,name)!=(binding,signature) or result['source_sha256']!=runner.state['phases'][spec['transfer']]['sha256']:raise ValueError('Source/binding changed during compact computation')
        metric=coverage(result,spec)
        atomic_json(out/'receipt.json',{'status':'verified','binding':binding,'result_sha256':sha(out/'result.json'),'coverage':metric,'raw_execution_ready':False})
        phase.update(status='verified',receipt_sha256=sha(out/'receipt.json'),coverage=metric);runner.guard();runner.save();return phase
    except BaseException as exc:
        phase.update(status='failed',error_type=type(exc).__name__);runner.save();raise
