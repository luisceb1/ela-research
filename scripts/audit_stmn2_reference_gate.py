#!/usr/bin/env python3
"""Replay pinned public-reference windows; no patient data, alignments or effects."""
import argparse
import hashlib
import json
from pathlib import Path

WINDOWS = {
    'donor': (79611206, 79611222, 79611214, 'GT'),
    'cryptic': (79616813, 79616829, 79616819, 'AG'),
    'canonical': (79636793, 79636809, 79636799, 'AG'),
}


def slice_genomic(dna, window_start, start, end):
    if not window_start <= start < end <= window_start + len(dna):
        raise ValueError('Requested motif outside window')
    return dna[start-window_start:end-window_start].upper()


def audit(bundle):
    assembly = bundle['assembly_projection']
    if assembly['default_coord_system_version'] != 'GRCh38' or not assembly['assembly_name'].startswith('GRCh38'):
        raise ValueError('Unexpected Ensembl assembly')
    if bundle['chromosome8'] != {'name': '8', 'length': 145138636, 'coord_system': 'chromosome'}:
        raise ValueError('Unexpected chromosome8 identity')
    rows = []
    for event, (start, end, motif_start, expected) in WINDOWS.items():
        u = bundle['records']['ucsc_'+event]
        e = bundle['records']['ensembl_'+event]
        for r in (u, e):
            if r['status'] != 200 or hashlib.sha256(r['body'].encode()).hexdigest() != r['sha256']:
                raise ValueError('HTTP status or raw payload hash mismatch')
        ud = json.loads(u['body'])
        if (ud['genome'], ud['chrom'], ud['start'], ud['end']) != ('hg38', 'chr8', start, end):
            raise ValueError('UCSC response coordinate mismatch')
        expected_u = f'https://api.genome.ucsc.edu/getData/sequence?genome=hg38;chrom=chr8;start={start};end={end}'
        expected_e = f'https://rest.ensembl.org/sequence/region/human/8:{start+1}..{end}:1?content-type=text/plain'
        if u['url'] != expected_u or e['url'] != expected_e:
            raise ValueError('Provider request identity mismatch')
        dna, ensembl = ud['dna'], e['body']
        if len(dna) != end-start or len(ensembl) != end-start or set(dna.upper()) - set('ACGT'):
            raise ValueError('Missing/ambiguous bases or wrong window width')
        if dna.upper() != ensembl.upper():
            raise ValueError('Reference providers disagree')
        motif = slice_genomic(dna, start, motif_start, motif_start+2)
        if motif != expected:
            raise ValueError('Prefixed splice motif prediction failed')
        rows.append({'site': event, 'chrom': 'chr8', 'assembly': 'GRCh38/hg38', 'strand': '+',
                     'window_start_0based': start, 'window_end_exclusive': end,
                     'dna': dna, 'normalized_sha256': hashlib.sha256(dna.upper().encode()).hexdigest(),
                     'motif_start_0based': motif_start, 'motif': motif,
                     'offset_controls': {str(delta): slice_genomic(dna, start, motif_start+delta, motif_start+delta+2)
                                         for delta in (-1, 0, 1)},
                     'same_sequence_two_providers': True})
    return {'sequence_windows_pass': True, 'sites': rows, 'indexed_reference_verified': False,
            'full_fasta_verified': False, 'pilot_ready': False, 'raw_reads_processed': 0,
            'evidence': 'technical reference QC; providers share assembly, not independent biological replication'}


def main():
    p = argparse.ArgumentParser(__doc__)
    p.add_argument('--input', required=True)
    p.add_argument('--expected-sha256', required=True)
    p.add_argument('--out', required=True)
    a = p.parse_args()
    raw = Path(a.input).read_bytes()
    if hashlib.sha256(raw).hexdigest() != a.expected_sha256:
        raise ValueError('Reference bundle hash mismatch')
    result = audit(json.loads(raw))
    Path(a.out).write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__': main()
