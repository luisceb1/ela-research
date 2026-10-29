#!/usr/bin/env python3
"""Dataset-scoped exact isoform mapping and structural comparison; exploratory."""
import csv
import gzip
import json
import platform
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

# Permit both `python scripts/map_isoforms.py` and module import in tests.
try:
    from scripts import geo_audit as a
except ModuleNotFoundError:
    import geo_audit as a

OUT = a.ROOT / 'reports/isoforms'
CONTROLS = {'ACTB': 'ENSG00000075624', 'GAPDH': 'ENSG00000111640'}
GENES = {**a.TARGETS, **CONTROLS}
REF_URL = 'https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_47/gencode.v47.annotation.gtf.gz'


def validated_chain(exons):
    chain = tuple(sorted(exons))
    if not chain or any(s < 1 or e < s for s, e in chain):
        raise ValueError('Missing/invalid exon chain')
    if any(r[0] <= l[1] for l, r in zip(chain, chain[1:])):
        raise ValueError('Overlapping or duplicate exons')
    return chain


def junctions(chain):
    # Boundaries on exonic bases; not intronic start/end, regardless of strand.
    return tuple((l[1], r[0]) for l, r in zip(chain, chain[1:]))


def read_reference(path):
    txs, symbols = {}, defaultdict(set)
    wanted = set(GENES.values())
    with gzip.open(path, 'rt') as f:
        for line in f:
            if line.startswith('#'):
                continue
            row = line.rstrip('\n').split('\t')
            if len(row) != 9:
                raise ValueError('Malformed reference GTF')
            attr = a.attrs(row[8])
            gene = attr.get('gene_id', '').split('.')[0]
            if gene not in wanted:
                continue
            symbols[gene].add(attr.get('gene_name'))
            if row[2] != 'exon':
                continue
            tx = attr['transcript_id']
            rec = txs.setdefault(tx, {'gene': gene, 'chrom': row[0], 'strand': row[6], 'exons': []})
            if (rec['gene'], rec['chrom'], rec['strand']) != (gene, row[0], row[6]):
                raise ValueError('Conflicting reference transcript identity')
            rec['exons'].append((int(row[3]), int(row[4])))
    for symbol, gene in GENES.items():
        if symbols[gene] != {symbol}:
            raise ValueError(f'GENCODE symbol/ID not verified: {symbol}: {symbols[gene]}')
    ref = {}
    for symbol, gene in GENES.items():
        records = [r for r in txs.values() if r['gene'] == gene]
        if not records:
            raise ValueError(f'No reference exons for {symbol}')
        chains, exons, juncs = set(), set(), set()
        for r in records:
            chain = validated_chain(r['exons'])
            prefix = (r['chrom'], r['strand'])
            chains.add(prefix + (chain,))
            exons.update(prefix + e for e in chain)
            juncs.update(prefix + j for j in junctions(chain))
        ref[symbol] = {'gene': gene, 'transcripts': len(records), 'chains': chains,
                       'exons': exons, 'junctions': juncs}
    return ref


def read_local_exons(path, gene_ids=None):
    txs = {}
    wanted = set(GENES.values()) if gene_ids is None else set(gene_ids)
    with gzip.open(path, 'rt') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            row = line.rstrip('\n').split('\t')
            if len(row) != 9:
                raise ValueError('Malformed local GTF')
            if row[2] != 'exon':
                continue
            attr = a.attrs(row[8])
            if attr.get('gene_id', '').split('.')[0] not in wanted:
                continue
            tx = attr['transcript_id']
            rec = txs.setdefault(tx, {'geneid': attr['gene_id'], 'chrom': row[0], 'strand': row[6], 'exons': []})
            if (rec['geneid'], rec['chrom'], rec['strand']) != (attr['gene_id'], row[0], row[6]):
                raise ValueError('Conflicting local transcript identity')
            rec['exons'].append((int(row[3]), int(row[4])))
    for rec in txs.values():
        rec['exons'] = validated_chain(rec['exons'])
    return txs


def classify(rec, reference):
    prefix = (rec['chrom'], rec['strand'])
    chain = rec['exons']
    novel_exons = [e for e in chain if prefix + e not in reference['exons']]
    novel_internal = [e for e in chain[1:-1] if prefix + e not in reference['exons']]
    novel_junctions = [j for j in junctions(chain) if prefix + j not in reference['junctions']]
    return {'full_chain_in_gencode_v47': prefix + (chain,) in reference['chains'],
            'n_unannotated_exons': len(novel_exons), 'n_unannotated_internal_exons': len(novel_internal),
            'n_unannotated_junctions': len(novel_junctions)}


def locus_candidates(path, reference):
    """Flag overlapping other-gene transcripts; never reassign them to a target."""
    loci = {}
    for symbol in a.TARGETS:
        exons = reference[symbol]['exons']
        chroms, strands = {e[0] for e in exons}, {e[1] for e in exons}
        if len(chroms) != 1 or len(strands) != 1:
            raise ValueError(f'Nonunique target locus: {symbol}')
        loci[symbol] = (next(iter(chroms)), next(iter(strands)), min(e[2] for e in exons), max(e[3] for e in exons))
    result = []
    with gzip.open(path, 'rt') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            row = line.rstrip('\n').split('\t')
            if row[2] != 'transcript':
                continue
            for symbol, (chrom, strand, start, end) in loci.items():
                if row[0] != chrom or int(row[3]) > end or int(row[4]) < start:
                    continue
                attr = a.attrs(row[8])
                if attr['gene_id'].split('.')[0] == a.TARGETS[symbol]:
                    continue
                result.append({'symbol_locus': symbol, 'txname': attr['transcript_id'], 'assigned_geneid': attr['gene_id'],
                    'chrom': chrom, 'strand': row[6], 'start_1based': int(row[3]), 'end_1based': int(row[4]),
                    'same_strand_as_target': row[6] == strand, 'assignment': 'not_reassigned_overlap_only'})
    return result


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows, exon_rows, junction_rows, support, negative, overlaps, errors = [], [], [], [], [], [], []
    ref = {}
    try:
        qc = json.loads((a.OUT / 'qc.json').read_text())
        audit_errors = json.loads((a.OUT / 'errors.json').read_text())
        if audit_errors or set(qc) != set(a.SERIES):
            raise ValueError('Complete technical audit required before mapping')
        if any((a.OUT / name).read_text().count('\n') != 1 for name in ['unmapped.tsv', 'gene_mismatches.tsv']):
            raise ValueError('Unresolved mapping discrepancies in audit')
        sources = json.loads((a.OUT / 'sources.json').read_text())
        for gse, label in a.SERIES.items():
            for suffix in ['uniqueCounts_transcript.txt.gz', 'extended_annotations.gtf.gz']:
                name = f'{gse}_{label}_isoseq_{suffix}'
                if a.sha256((a.DATA / name).read_bytes()) != sources[name]['source_sha256']:
                    raise ValueError(f'Input hash changed: {name}')
        ref_manifest_path = OUT / 'reference_source.json'
        manifest = json.loads(ref_manifest_path.read_text()) if ref_manifest_path.exists() else {}
        a.fetch(REF_URL, a.DATA / 'gencode.v47.annotation.gtf.gz', manifest)
        a.dump_json(ref_manifest_path, manifest)
        ref = read_reference(a.DATA / 'gencode.v47.annotation.gtf.gz')
        for gse, label in a.SERIES.items():
            gtf = a.DATA / f'{gse}_{label}_isoseq_extended_annotations.gtf.gz'
            txs = read_local_exons(gtf)
            overlap = locus_candidates(gtf, ref)
            overlap_by_tx = defaultdict(list)
            for r in overlap:
                r['gse'] = gse
                r['sum_unique_counts'] = 0.
                r['samples_gt0'] = 0
                overlap_by_tx[r['txname']].append(r)
            overlaps.extend(overlap)
            by_gene = defaultdict(list)
            path = a.DATA / f'{gse}_{label}_isoseq_uniqueCounts_transcript.txt.gz'
            seen = set()
            for header, tx, geneid, values in a.count_rows(path):
                for r in overlap_by_tx.get(tx, []):
                    if geneid != r['assigned_geneid']:
                        raise ValueError(f'Overlapping gene identity conflict: {tx}')
                    r['sum_unique_counts'] = sum(values)
                    r['samples_gt0'] = sum(v > 0 for v in values)
                symbol = next((s for s, g in GENES.items() if geneid.split('.')[0] == g), None)
                if symbol is None:
                    continue
                if tx in seen:
                    raise ValueError(f'Duplicate target transcript: {tx}')
                seen.add(tx)
                if tx not in txs or txs[tx]['geneid'] != geneid:
                    raise ValueError(f'Target missing or discordant: {gse}:{tx}')
                rec = txs[tx]
                flags = classify(rec, ref[symbol])
                chain = rec['exons']
                row = {'gse': gse, 'symbol': symbol, 'geneid': geneid, 'txname': tx,
                       'origin': 'ENST' if tx.startswith('ENST') else 'non_ENST',
                       'chrom': rec['chrom'], 'strand': rec['strand'], 'n_exons': len(chain),
                       'exon_chain_1based_closed': ','.join(f'{s}-{e}' for s, e in chain),
                       **flags, 'cryptic_event_status': 'unvalidated_no_independent_event_coordinates',
                       'samples_gt0': sum(v > 0 for v in values), 'samples_ge2': sum(v >= 2 for v in values),
                       'sum_unique_counts': sum(values)}
                if symbol in CONTROLS:
                    negative.append(row)
                    continue
                rows.append(row)
                by_gene[symbol].append((tx, values))
                for i, (start, end) in enumerate(chain):
                    exon_rows.append({'gse': gse, 'symbol': symbol, 'txname': tx, 'chrom': rec['chrom'], 'strand': rec['strand'],
                        'genomic_order': i + 1, 'start_1based': start, 'end_1based': end,
                        'position': 'single' if len(chain) == 1 else 'terminal' if i in (0, len(chain)-1) else 'internal',
                        'exact_exon_in_gencode_v47': (rec['chrom'], rec['strand'], start, end) in ref[symbol]['exons']})
                for left, right in junctions(chain):
                    junction_rows.append({'gse': gse, 'symbol': symbol, 'txname': tx, 'chrom': rec['chrom'], 'strand': rec['strand'],
                        'left_exon_end': left, 'right_exon_start': right,
                        'donor_exonic_boundary': left if rec['strand'] == '+' else right,
                        'acceptor_exonic_boundary': right if rec['strand'] == '+' else left,
                        'exact_junction_in_gencode_v47': (rec['chrom'], rec['strand'], left, right) in ref[symbol]['junctions']})
            if any(not any(r['symbol'] == s for r in (rows if s in a.TARGETS else negative) if r['gse'] == gse) for s in GENES):
                raise ValueError(f'Missing target/control gene: {gse}')
            for symbol, records in by_gene.items():
                totals = [sum(v[i] for _, v in records) for i in range(len(header)-2)]
                for tx, values in records:
                    for i, value in enumerate(values):
                        library_total = qc[gse]['uniqueCounts']['assigned_counts'][i]
                        support.append({'gse': gse, 'symbol': symbol, 'txname': tx, 'column': header[i+2],
                            'unique_count': value, 'gene_assigned_unique_sum': totals[i],
                            'share_of_gene_unique_counts': value/totals[i] if totals[i] else '',
                            'unique_per_million_assigned_transcript_counts': value/library_total*1e6 if library_total else ''})
        for name, table in [('transcripts.tsv', rows), ('exons.tsv', exon_rows), ('junctions.tsv', junction_rows),
                            ('support.tsv', support), ('mapping_controls.tsv', negative)]:
            if not table:
                raise ValueError(f'Empty mapping result: {name}')
            a.tsv(OUT / name, table, list(table[0]))
        chains = defaultdict(lambda: defaultdict(list))
        for r in rows:
            key = (r['symbol'], r['chrom'], r['strand'], r['exon_chain_1based_closed'])
            chains[key][r['gse']].append(r['txname'])
        shared = [{'symbol': key[0], 'chrom': key[1], 'strand': key[2], 'exon_chain_1based_closed': key[3],
                   'GSE310723_txnames': ','.join(sorted(v['GSE310723'])),
                   'GSE315972_txnames': ','.join(sorted(v['GSE315972']))}
                  for key, v in sorted(chains.items()) if len(v) == 2]
        a.tsv(OUT / 'shared_full_chains.tsv', shared, ['symbol', 'chrom', 'strand', 'exon_chain_1based_closed', 'GSE310723_txnames', 'GSE315972_txnames'])
        a.tsv(OUT / 'other_gene_locus_overlaps.tsv', overlaps,
            ['gse', 'symbol_locus', 'txname', 'assigned_geneid', 'chrom', 'strand', 'start_1based', 'end_1based',
             'same_strand_as_target', 'assignment', 'sum_unique_counts', 'samples_gt0'])
        summary = {}
        for gse in a.SERIES:
            summary[gse] = {}
            for symbol in a.TARGETS:
                subset = [r for r in rows if r['gse'] == gse and r['symbol'] == symbol]
                summary[gse][symbol] = {'transcripts': len(subset),
                    'ENST': sum(r['origin'] == 'ENST' for r in subset),
                    'non_ENST': sum(r['origin'] != 'ENST' for r in subset),
                    'full_chain_in_gencode_v47': sum(r['full_chain_in_gencode_v47'] for r in subset),
                    'transcripts_with_unannotated_internal_exons': sum(r['n_unannotated_internal_exons'] > 0 for r in subset),
                    'detected_any_sample': sum(r['samples_gt0'] > 0 for r in subset),
                    'at_least_2_unique_in_any_sample': sum(r['samples_ge2'] > 0 for r in subset)}
        a.dump_json(OUT / 'summary.json', {'datasets': summary, 'shared_full_chains': dict(Counter(r['symbol'] for r in shared)),
            'reference': {s: {'gene': r['gene'], 'transcripts': r['transcripts']} for s, r in ref.items()}})
        print(json.dumps(summary, indent=2))
    except Exception as exc:
        errors.append({'type': type(exc).__name__, 'message': str(exc)})
    finally:
        a.dump_json(OUT / 'errors.json', errors)
        a.dump_json(OUT / 'run.json', {'python': platform.python_version(), 'utc': datetime.now(timezone.utc).isoformat(),
            'argv': sys.argv, 'randomness': 'none', 'evidence': 'exploratory', 'status': 'failed' if errors else 'generated'})
    if errors:
        print(errors, file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
