#!/usr/bin/env python3
"""Frozen public-culture identity and configuration; planning never opens FASTQ."""
import hashlib
import json
from pathlib import Path
import re

MANIFEST_SHA256='b5ed1bcfaa32132ae3e05af183dcf16d9b1dc60639db1d4827934c944c40ccbd'
DEFAULT_RUN='SRR8144907'
DEFAULT_DEADLINE=1800
MAX_DEADLINE=2700


def load_rows(path):
    data=Path(path).read_bytes()
    if hashlib.sha256(data).hexdigest()!=MANIFEST_SHA256:
        raise ValueError('Frozen culture manifest hash mismatch')
    rows=json.loads(data)['rows']
    if len(rows)!=6 or any(len({r[k] for r in rows})!=6 for k in ('run','gsm','experiment')):
        raise ValueError('Manifest must contain six distinct culture identities')
    return rows


def partition(reads,size):
    if type(reads) is not int or type(size) is not int or reads<=0 or size<=0:
        raise ValueError('Positive integer reads/bin size required')
    whole,remainder=divmod(reads,size)
    if whole+bool(remainder)>10000:raise ValueError('Configuration exceeds10000 technical bins')
    return [size]*whole+([remainder] if remainder else [])


def configure(rows,run=DEFAULT_RUN,max_reads=1000000,complete_library=False,bin_size=1000000,deadline=DEFAULT_DEADLINE):
    selected=[r for r in rows if r['run']==run]
    if len(selected)!=1:raise ValueError('Run must select exactly one fixed manifest row')
    row=selected[0]
    if type(deadline) is not int or not 0<deadline<=MAX_DEADLINE:
        raise ValueError('Explicit phase deadline must be positive and at most2700 seconds')
    if type(max_reads) is not int or not 0<max_reads<=row['reads']:
        raise ValueError('Requested reads outside fixed library')
    if complete_library and max_reads!=row['reads']:
        raise ValueError('Complete-library count must equal frozen manifest')
    bins=partition(max_reads,bin_size)
    return {'run':run,'gsm':row['gsm'],'experiment':row['experiment'],'published_group':row['published_group'],
            'manifest_sha256':MANIFEST_SHA256,'expected_library_reads':row['reads'],'max_reads':max_reads,
            'complete_library':bool(complete_library),'bin_size':bin_size,'bin_reads':bins,
            'phase_deadline_seconds':deadline,'automatic_deadline_increase':False,
            'expected_fastq_bytes':row['fastq_bytes'],'expected_md5':row['md5'],
            'primary_anchor':15,'sensitivity_anchor':8,'minimum_denominator':20,
            'cpu_count':2,'virtual_address_caps':{'aligner':5368709120,'parent':536870912,'htslib':268435456}}


def validate_receipt(config,receipt):
    if not isinstance(receipt,dict):raise ValueError('Download receipt must be an object')
    required={'run':config['run'],'gsm':config['gsm'],'expected_bytes':config['expected_fastq_bytes'],
              'bytes':config['expected_fastq_bytes'],'expected_md5':config['expected_md5'],'md5':config['expected_md5']}
    if receipt.get('verified') is not True or any(receipt.get(k)!=v for k,v in required.items()):
        raise ValueError('Verified download receipt does not bind selected culture identity/bytes/MD5')
    if not isinstance(receipt.get('sha256'),str) or not re.fullmatch('[0-9a-f]{64}',receipt['sha256']):
        raise ValueError('Verified receipt requires SHA256')
    return receipt['sha256']


def aligner_command(binary,prefix,max_reads):
    return ['prlimit','--as=5368709120','--',str(binary),'--wrapper','basic-0','-x',str(prefix),
            '-U','-','-u',str(max_reads),'-p','2','-k','5','--seed','0','--no-temp-splicesite','--reorder']
