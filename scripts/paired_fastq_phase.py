"""Local integrity phase bound to manifest, transfer ledger and immutable receipts.

No network or production execution. An interrupted phase requires explicit human
reconciliation; it is never restarted or adopted from an orphan result directory.
"""
import hashlib
import json
import re
from pathlib import Path

from paired_fastq_integrity import file_digest, validate_pair
from process_supervisor_v2 import atomic_json

POLICY='paired-fastq-ledger-v1'


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def contract(runner,name):
    if not re.fullmatch('[A-Za-z0-9_-]+',name):raise ValueError('Invalid phase name')
    spec=runner.manifest.get('paired_fastq',{}).get(name)
    if not isinstance(spec,dict) or set(spec)!={'mates','prefix_pairs'}:raise ValueError('Manifest pair contract required')
    if type(spec['prefix_pairs']) is not int or spec['prefix_pairs']<=0:raise ValueError('Fixed positive prefix required')
    mates=spec['mates']
    if not isinstance(mates,list) or len(mates)!=2:raise ValueError('Two ordered mates required')
    bindings=[]
    for mate in mates:
        if not isinstance(mate,dict) or set(mate)!={'transfer','identity','expected'}:raise ValueError('Explicit mate identity and expected hashes required')
        transfer=mate['transfer'];expected=mate['expected']
        if not isinstance(transfer,str) or not re.fullmatch('[A-Za-z0-9_-]+',transfer):raise ValueError('Invalid transfer name')
        if not isinstance(mate['identity'],str) or not mate['identity']:raise ValueError('Missing mate identity')
        if not isinstance(expected,dict) or set(expected)-{'bytes','md5','sha256'} or not {'bytes','md5'}<=set(expected):raise ValueError('Expected size/MD5 required')
        if type(expected['bytes']) is not int or expected['bytes']<=0 or not re.fullmatch('[0-9a-f]{32}',str(expected['md5'])):raise ValueError('Invalid expected transfer metadata')
        if expected.get('sha256') is not None and not re.fullmatch('[0-9a-f]{64}',str(expected['sha256'])):raise ValueError('Invalid expected SHA256')
        phase=runner.state['phases'].get(transfer,{})
        if phase.get('status')!='verified' or phase.get('kind')!='transfer':raise ValueError('Verified transfer required')
        if any(phase.get(k)!=expected[k] for k in ('bytes','md5')) or (expected.get('sha256') is not None and phase.get('sha256')!=expected['sha256']):raise ValueError('Manifest/transfer mismatch')
        # Hash the full compressed input without loading a multi-GB mate into RAM.
        path=runner.root/transfer
        if file_digest(path,runner.guard)!={'bytes':phase['bytes'],'sha256':phase['sha256']}:raise ValueError('Transfer file changed')
        binding={'identity':mate['identity'],'transfer':transfer,'ledger_receipt_sha256':digest(phase)}
        if 'attempts_used' in phase:
            receipt=runner.root/f"{transfer}.attempt-{phase['attempts_used']-1}.json"
            data=json.loads(receipt.read_text())
            if data.get('status')!='verified' or any(data.get(k)!=phase[k] for k in ('md5','sha256')) or data.get('body_bytes')!=phase['bytes']:raise ValueError('Incomplete HTTP transfer receipt')
            binding['http_receipt_sha256']=sha(receipt)
        bindings.append(binding)
    if mates[0]['transfer']==mates[1]['transfer'] or mates[0]['identity']==mates[1]['identity']:raise ValueError('Distinct mate transfers/identities required')
    payload={'policy':POLICY,'spec':spec,'transfers':bindings,'fingerprint':runner.state['fingerprint']}
    return payload,digest(payload)


def verify_phase(runner,name,phase):
    payload,signature=contract(runner,name)
    if signature!=phase['signature'] or payload!=phase['binding']:raise ValueError('Pair binding changed')
    out=runner.root/'paired-fastq'/name
    if sha(out/'receipt.json')!=phase['receipt_sha256']:raise ValueError('Pair receipt changed')
    receipt=json.loads((out/'receipt.json').read_text())
    if receipt.get('status')!='verified' or receipt.get('binding')!=payload:raise ValueError('Incomplete pair receipt')
    if sha(out/'result.json')!=receipt['result_sha256']:raise ValueError('Pair result changed')
    result=json.loads((out/'result.json').read_text())
    if result.get('status')!='verified' or not result.get('source_gzip_eof_crc_validated'):raise ValueError('Incomplete pair result')
    if result['prefix_pairs_written']!=payload['spec']['prefix_pairs']:raise ValueError('Prefix size mismatch')
    for i,expected in enumerate(result['prefixes'],1):
        if file_digest(out/f'prefix-R{i}.fastq.gz',runner.guard)!=expected:raise ValueError('Prefix changed')
    runner.guard()


def run_phase(runner,name):
    payload,signature=contract(runner,name)
    if not runner.begin(name,'paired_fastq',signature):
        phase=runner.state['phases'][name];verify_phase(runner,name,phase);return phase
    phase=runner.state['phases'][name];phase['binding']=payload;runner.save()
    out=runner.root/'paired-fastq'/name
    try:
        spec=payload['spec']
        result=validate_pair(*(runner.root/m['transfer'] for m in spec['mates']),out,spec['prefix_pairs'],checkpoint=runner.guard)
        # Rehash after the full scan and compare both the ledger binding and the
        # validator's pre-scan hashes. Concurrent writers are unsupported.
        if contract(runner,name)!=(payload,signature):raise ValueError('Transfer binding changed during validation')
        expected=[{'bytes':runner.state['phases'][m['transfer']]['bytes'],'sha256':runner.state['phases'][m['transfer']]['sha256']} for m in spec['mates']]
        if result['source_compressed']!=expected:raise ValueError('Source changed during validation')
        atomic_json(out/'receipt.json',{'status':'verified','binding':payload,'result_sha256':sha(out/'result.json'),'raw_execution_ready':False})
        phase.update(status='verified',receipt_sha256=sha(out/'receipt.json'))
        runner.guard();runner.save();return phase
    except BaseException as exc:
        phase.update(status='failed',error_type=type(exc).__name__);runner.save();raise
