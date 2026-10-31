#!/usr/bin/env python3
"""Prospective SE junction contract audit; no raw-read CLI or biological inference."""
import argparse
import csv
import hashlib
import io
import json
import platform
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CIGAR = re.compile(r"([1-9][0-9]*)([MIDNSHP=X])")


def boundaries(left, right):
    """1-based exonic flanks -> intron inclusive and BED half-open."""
    if type(left) is not int or type(right) is not int or left < 1 or right <= left + 1:
        raise ValueError("Invalid exon boundaries")
    return {"left_exon_end_1based": left, "right_exon_start_1based": right,
            "intron_start_1based": left + 1, "intron_end_1based": right - 1,
            "intron_bed_start_0based": left, "intron_bed_end_exclusive": right - 1,
            "skipped_reference_bases": right - left - 1}


def parse_cigar(cigar):
    ops = [(int(n), op) for n, op in CIGAR.findall(cigar)]
    if not ops or ''.join(f'{n}{op}' for n, op in ops) != cigar:
        raise ValueError("Malformed CIGAR")
    # H/S may only flank the aligned core; P unsupported, never silently ignored.
    core = [i for i, (_, op) in enumerate(ops) if op not in 'HS']
    if not core or any(op in 'HSP' for _, op in ops[min(core):max(core)+1]):
        raise ValueError("Unsupported CIGAR clipping/padding")
    prefix = ''.join(op for _, op in ops[:min(core)])
    suffix = ''.join(op for _, op in ops[max(core)+1:])
    if prefix not in ('', 'H', 'S', 'HS') or suffix not in ('', 'H', 'S', 'SH'):
        raise ValueError("Invalid clipping order")
    return ops


def sam_junctions(line, min_mapq=20, min_anchor=8):
    """Return (chrom,left_exonic,right_exonic,XS). Missing NH/XS excludes read.

    Alignment flag 0x10 is NOT transcript strand. No paired-end support, no
    duplicate removal. Adjacent aligned M/= /X bases define conservative anchors;
    an insertion/deletion/clip breaks an anchor. Sequence '*' allowed by SAM.
    This is an offline contract prototype pending independent-tool comparison.
    """
    if line.startswith('@'):
        return []
    f = line.rstrip('\n').split('\t')
    if len(f) < 11:
        raise ValueError("SAM requires 11 fields")
    flag, pos, mapq = int(f[1]), int(f[3]), int(f[4])
    if not 0 <= flag <= 65535 or not 0 <= mapq <= 255:
        raise ValueError("Invalid SAM numeric field")
    if flag & 1:
        raise ValueError("Paired-end records outside SE contract")
    if flag & (4 | 256 | 512 | 2048):
        return []
    if pos < 1 or f[2] == '*':
        raise ValueError("Invalid mapped position/reference")
    ops = parse_cigar(f[5])
    qlen = sum(n for n, op in ops if op in 'MIS=X')
    if f[9] != '*' and len(f[9]) != qlen:
        raise ValueError("CIGAR/SEQ length mismatch")
    if f[10] != '*' and (f[9] == '*' or len(f[10]) != len(f[9])):
        raise ValueError("SEQ/QUAL length mismatch")
    tags = {}
    for field in f[11:]:
        parts = field.split(':', 2)
        if len(parts) != 3 or parts[0] in tags:
            raise ValueError("Malformed/duplicate SAM tag")
        tags[parts[0]] = (parts[1], parts[2])
    if 'NH' in tags and (tags['NH'][0] != 'i' or not tags['NH'][1].isdigit() or int(tags['NH'][1]) < 1):
        raise ValueError("Invalid NH tag")
    if 'XS' in tags and tags['XS'] not in [('A', '+'), ('A', '-')]:
        raise ValueError("Invalid XS tag")
    if mapq == 255 or mapq < min_mapq or tags.get('NH') != ('i', '1') or 'XS' not in tags:
        return []
    out = []
    cursor = pos
    for i, (n, op) in enumerate(ops):
        if op == 'N':
            anchors = []
            for step in (-1, 1):
                k, anchor = i + step, 0
                while 0 <= k < len(ops) and ops[k][1] in 'M=X':
                    anchor += ops[k][0]
                    k += step
                anchors.append(anchor)
            if min(anchors) >= min_anchor:
                out.append((f[2], cursor - 1, cursor + n, tags['XS'][1]))
        if op in 'MDN=X':
            cursor += n
    return out


def checked_inputs(manifest):
    result = {}
    for path, expected in manifest['inputs'].items():
        raw = (BASE / path).read_bytes()
        if hashlib.sha256(raw).hexdigest() != expected:
            raise ValueError(f"Input hash mismatch: {path}")
        result[path] = raw
    return result


def build_contract(manifest):
    inputs = checked_inputs(manifest)
    paper = json.loads(inputs['reports/event-reference/paper_evidence.json'])
    rows = list(csv.DictReader(io.StringIO(inputs['reports/isoforms/junctions.tsv'].decode()), delimiter='\t'))
    left, right = paper['left_exonic_boundary'], paper['right_exonic_boundary']
    if paper['assembly'] != 'GRCh38' or paper['symbol'] != 'STMN2' or paper['chrom'] != 'chr8':
        raise ValueError("Event identity mismatch")
    selected = [r for r in rows if r['symbol'] == 'STMN2' and r['chrom'] == paper['chrom']
                and r['strand'] == '+' and int(r['left_exon_end']) == left]
    if not any(int(r['right_exon_start']) == right for r in selected):
        raise ValueError("Cryptic candidate not present in projection")
    canonical = [r for r in selected if r['exact_junction_in_gencode_v47'] == 'True']
    acceptors = {int(r['right_exon_start']) for r in canonical}
    if len(acceptors) != 1:
        raise ValueError("Canonical comparator absent or ambiguous")
    acceptor = acceptors.pop()
    if not left < right < acceptor:
        raise ValueError("Cryptic/canonical geometry mismatch")
    exons = list(csv.DictReader(io.StringIO(inputs['reports/isoforms/exons.tsv'].decode()), delimiter='\t'))
    txs = sorted({r['txname'] for r in canonical})
    for tx in txs:
        ex = [e for e in exons if e['txname'] == tx and e['symbol'] == 'STMN2'
              and e['exact_exon_in_gencode_v47'] == 'True' and e['chrom'] == 'chr8' and e['strand'] == '+']
        if not any(int(e['end_1based']) == left for e in ex) or not any(int(e['start_1based']) == acceptor for e in ex):
            raise ValueError("Canonical exon witness absent")
    events = {name: boundaries(left, end) for name, end in [('cryptic', right), ('canonical', acceptor)]}
    for event in events.values():
        start = left - 7
        n = event['skipped_reference_bases']
        sam = f'synthetic\t0\tchr8\t{start}\t60\t8M{n}N8M\t*\t0\t0\t*\t*\tNH:i:1\tXS:A:+'
        if sam_junctions(sam) != [('chr8', left, event['right_exon_start_1based'], '+')]:
            raise ValueError("Synthetic coordinate control failed")
    return {"assembly": "GRCh38", "chrom": "chr8", "strand": "+", "events": events,
            "canonical_transcript_witnesses": txs,
            "evidence_level": "reused molecular projection plus synthetic software QC",
            "denominator_proposed": "canonical + cryptic counts sharing donor; conditional read ratio, not molecular PSI",
            "unmeasured_other_donor_branches": True,
            "raw_reads_processed": 0, "fasta_verified": False, "index_verified": False,
            "pilot_ready": False, "alignment_tool_comparison_done": False,
            "limits": ["Not independent GTF reconstruction", "No full transcript/polyA inference",
                       "Paper caption strand not explicit; strand inherited from audited projection",
                       "No biological effect, replication or functional validation"]}


def main():
    p = argparse.ArgumentParser(__doc__)
    p.add_argument('--manifest', required=True)
    p.add_argument('--out', required=True)
    args = p.parse_args()
    manifest = json.loads(Path(args.manifest).read_text())
    result = build_contract(manifest)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'contract.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    run = {'python': platform.python_version(), 'parameters': vars(args), 'inputs': manifest['inputs'],
           'contract_sha256': hashlib.sha256((out / 'contract.json').read_bytes()).hexdigest(),
           'randomness': 'none', 'reads_processed': 0}
    (out / 'run.json').write_text(json.dumps(run, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
