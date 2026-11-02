"""Opt-in local policy: fixed clocks, disk partitions and phase resource caps."""
import math
import os
from pathlib import Path

KINDS={'transfer','archive','paired_fastq','compact','process'}
ALLOCATIONS={'artifacts','prefixes','temporaries','dependencies','receipts'}


def validate(policy,limits):
    if policy is None:return None
    if not isinstance(policy,dict) or set(policy)!={'schema','production_enabled','total_seconds','transfer_seconds','allocations','phases'}:raise ValueError('Execution policy schema')
    if policy['schema']!='pilot-b4-local-v1' or policy['production_enabled'] is not False:raise ValueError('Only local disabled-production policy accepted')
    if any(type(policy[k]) is not int or policy[k]<=0 for k in ('total_seconds','transfer_seconds')):raise ValueError('Clock caps must be positive integers')
    if policy['total_seconds']!=limits['wall_seconds'] or policy['transfer_seconds']>policy['total_seconds']:raise ValueError('Total/transfer clocks inconsistent')
    allocations=policy['allocations']
    if not isinstance(allocations,dict) or set(allocations)!=ALLOCATIONS or any(type(v) is not int or v<0 for v in allocations.values()) or allocations['receipts']<4096:raise ValueError('Disk allocation schema')
    if sum(allocations.values())>limits['disk_bytes']:raise ValueError('Disk partitions exceed total')
    caps=limits.get('process_caps')
    if not isinstance(caps,dict) or set(caps)!={'wall_seconds','rss_bytes','address_space_bytes'} or any(type(v) is not int or v<=0 for v in caps.values()):raise ValueError('Global process caps required')
    phases=policy['phases']
    if not isinstance(phases,dict) or not phases:raise ValueError('Named phase policies required')
    import re
    for name,p in phases.items():
        if not isinstance(name,str) or not re.fullmatch('[A-Za-z0-9_-]+',name) or not isinstance(p,dict):raise ValueError('Invalid policy phase')
        keys={'kind','wall_seconds','rss_bytes','address_space_bytes'}|({'producer_seconds','reduce_seconds'} if p.get('kind')=='compact' else set())
        if set(p)!=keys or p['kind'] not in KINDS or any(type(p[k]) is not int or p[k]<=0 for k in keys-{'kind'}):raise ValueError('Phase cap schema')
        if p['wall_seconds']>policy['total_seconds'] or p['wall_seconds']>caps['wall_seconds'] or p['rss_bytes']>caps['rss_bytes'] or p['address_space_bytes']>caps['address_space_bytes'] or p['address_space_bytes']<p['rss_bytes']:raise ValueError('Phase resources exceed global caps or AS below RSS')
        if p['kind']=='compact' and p['producer_seconds']+p['reduce_seconds']>p['wall_seconds']:raise ValueError('Compact subphase caps exceed phase')
    nontransfer=sum(p['wall_seconds'] for p in phases.values() if p['kind']!='transfer')
    if nontransfer+policy['transfer_seconds']>policy['total_seconds']:raise ValueError('Phase clock envelope exceeds total')
    return policy


def elapsed_transfers(state,now):
    return sum(max(0,p.get('finished_epoch',now)-p['started_epoch']) for p in state['phases'].values() if p['kind']=='transfer' and 'started_epoch' in p)


def guard_clocks(state,policy,now):
    if not math.isfinite(now) or now<state.get('last_epoch',now):raise RuntimeError('Clock moved backwards or invalid')
    spent=elapsed_transfers(state,now)
    if spent>policy['transfer_seconds'] or (spent>=policy['transfer_seconds'] and any(p['kind']=='transfer' and p['status']=='started' for p in state['phases'].values())):raise RuntimeError('Cumulative transfer time cap')
    for p in state['phases'].values():
        if 'started_epoch' in p and p['status']!='failed' and p.get('finished_epoch',now)>=min(p['deadline_epoch'],p.get('subdeadline_epoch',p['deadline_epoch'])):raise RuntimeError('Phase/subphase deadline')


def disk_usage(root,state):
    usage={k:0 for k in ALLOCATIONS};transfers=[n for n,p in state['phases'].items() if p['kind']=='transfer']
    for path in iter_files(root):
        try:
            if not path.is_file():continue
            rel=path.relative_to(root);parts=rel.parts;name=path.name;kind='receipts'
            if parts[0]=='dependencies':kind='dependencies'
            elif len(parts)>3 and parts[0]=='compact' and parts[2]=='work':kind='temporaries'
            elif len(parts)>3 and parts[0]=='archives' and parts[2] in ('files','partial'):kind='artifacts'
            elif parts[0]=='paired-fastq' and name.startswith('prefix-R'):kind='prefixes'
            elif len(parts)==1 and any(name==n or name==n+'.partial' or (name.startswith(n+'.attempt-') and name.endswith('.partial')) for n in transfers):kind='artifacts'
            usage[kind]+=path.stat().st_size
        except FileNotFoundError:pass
    return usage


def iter_files(root):
    def scan_error(error):
        if not isinstance(error,FileNotFoundError):raise error
    # os.walk handles a directory disappearing between listing and descent.
    # Access errors remain fatal; the next watchdog sample sees final paths.
    for directory,_,files in os.walk(root,followlinks=False,onerror=scan_error):
        for name in files:yield Path(directory)/name
