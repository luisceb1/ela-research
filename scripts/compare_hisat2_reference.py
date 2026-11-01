#!/usr/bin/env python3
"""Inspect indexed reference in a stream; retain hashes/lengths, not full FASTA."""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import subprocess
import time


def overlap_piece(sequence, offset, start, end):
    left, right = max(offset, start), min(offset+len(sequence), end)
    return sequence[left-offset:right-offset] if left < right else ''


def inspect(binary, prefix, expected, out):
    cmd = ['prlimit', '--as=6442450944', '--', 'timeout', '900', binary, '-a', '65536', prefix]
    start = time.monotonic()
    targets = expected['sites']
    windows = {r['site']: '' for r in targets}
    contigs, names = [], set()
    name, length, digest = None, 0, None
    result = {'command': cmd, 'index_reference_gate_pass': False, 'raw_reads_processed': 0}
    stderr = out.with_suffix('.stderr.txt')
    try:
        with stderr.open('w') as err:
            with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=err, text=True) as proc:
                try:
                    for line in proc.stdout:
                        if line.startswith('>'):
                            if name is not None: contigs.append({'name': name, 'length': length, 'sequence_sha256': digest.hexdigest()})
                            name = line[1:].strip().split()[0]
                            if name in names: raise ValueError('Duplicate indexed reference name')
                            names.add(name); length = 0; digest = hashlib.sha256()
                        else:
                            dna = line.strip().upper()
                            if name is None or set(dna) - set('ACGTN'): raise ValueError('Invalid indexed FASTA output')
                            if name == 'chr8':
                                for r in targets:
                                    windows[r['site']] += overlap_piece(dna, length, r['window_start_0based'], r['window_end_exclusive'])
                            digest.update(dna.encode()); length += len(dna)
                    if name is not None: contigs.append({'name': name, 'length': length, 'sequence_sha256': digest.hexdigest()})
                    code = proc.wait()
                    if code != 0: raise RuntimeError(f'inspect exit {code}')
                except BaseException:
                    proc.kill(); proc.wait(); raise
        chr8 = [r for r in contigs if r['name'] == 'chr8']
        if len(chr8) != 1 or chr8[0]['length'] != 145138636:
            raise ValueError('Indexed chr8 name/length mismatch')
        for r in targets:
            if windows[r['site']] != r['dna'].upper(): raise ValueError('Indexed STMN2 window mismatch')
        result.update(index_reference_gate_pass=True, contigs=contigs, chr8=chr8[0], windows=windows,
                      total_reference_bases=sum(r['length'] for r in contigs),
                      external_reference_scope='Three STMN2 windows plus chr8 length; genome-wide hashes recorded but not independently matched',
                      pilot_ready=False, runtime_alignment_semantics_validated=False)
    except Exception as exc:
        result['error'] = type(exc).__name__+': '+str(exc)
        raise
    finally:
        usage=resource.getrusage(resource.RUSAGE_CHILDREN)
        result.update(elapsed_seconds=time.monotonic()-start, maxrss_child_kib=usage.ru_maxrss,
                      child_user_seconds=usage.ru_utime, child_system_seconds=usage.ru_stime)
        out.write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__ == '__main__':
    p=argparse.ArgumentParser(__doc__)
    p.add_argument('--binary',required=True);p.add_argument('--prefix',required=True)
    p.add_argument('--expected',required=True);p.add_argument('--out',required=True)
    a=p.parse_args()
    r=inspect(a.binary,a.prefix,json.loads(Path(a.expected).read_text()),Path(a.out))
    print(json.dumps({k:v for k,v in r.items() if k!='contigs'},indent=2))
