"""Exact junction attribution audit. Model support never chooses the true gene."""
import argparse
import collections
import csv
import gzip
import hashlib
import json
from pathlib import Path
import re
try:
    from scripts import audit_gene_ambiguity as a
except ModuleNotFoundError:
    import audit_gene_ambiguity as a

ROOT = Path(__file__).resolve().parents[1]


def junctions(exons):
    exons = sorted(set(exons))
    if any(s < 1 or e < s for s, e in exons):
        raise ValueError('Invalid exon')
    if any(left[1] >= right[0] for left, right in zip(exons, exons[1:])):
        raise ValueError('Overlapping exons in one transcript')
    return {(left[1] + 1, right[0] - 1) for left, right in zip(exons, exons[1:]) if left[1] + 1 <= right[0] - 1}


def models(lines, genes):
    groups = collections.defaultdict(list)
    for line in lines:
        if line.startswith('#'):
            continue
        p = line.rstrip('\n').split('\t')
        if len(p) != 9 or p[2] != 'exon':
            continue
        g = re.search(r'gene_id "([^"]+)"', p[8])
        if not g or a.m.stable(g[1]) not in genes:
            continue
        t = re.search(r'transcript_id "([^"]+)"', p[8])
        if not t or p[6] not in ('+', '-'):
            raise ValueError('Missing transcript or strand in target gene')
        groups[(a.m.stable(g[1]), t[1], p[0], p[6])].append((int(p[3]), int(p[4])))
    index = collections.defaultdict(set)
    for (gid, tx, chrom, strand), exons in groups.items():
        for left, right in junctions(exons):
            index[(gid, chrom, str(left), str(right), strand)].add(tx)
    return index, len(groups)


def canonical_category(candidate, author):
    if candidate and author:
        return 'both_reference_genes'
    if candidate:
        return 'candidate_reference_only'
    if author:
        return 'author_reference_only'
    return 'neither_reference_gene'


def witness(index, row, gid):
    return sorted(index.get((gid, row['chrom'], row['intron_start'], row['intron_end'], row['strand']), set()))


def primary_rows(cache, evidence, out):
    manifest = json.loads((ROOT / 'research/references/bolger_author_catalog_v1.json').read_text())
    expected = collections.defaultdict(list)
    for e in evidence:
        expected[(e['sheet'], int(e['sheet_row']))].append(e)
    checked = []
    for filename, cat in [('media-8.xlsx', 'S7'), ('media-9.xlsx', 'S8')]:
        raw = a.m.a.pinned(cache / filename, manifest['files'][filename])
        with a.m.a.office(raw, 'xlsx') as z:
            strings = a.m.a.shared_strings(z)
            for sheet, path in a.m.a.sheets(z):
                wanted = {n for s, n in expected if s == sheet}
                if not wanted:
                    continue
                for number, cells in a.m.a.raw_rows(z, path):
                    if number in wanted:
                        row = a.m.a.decode(cells, strings)
                        keys, _ = a.m.eligible_keys(row, cat)
                        for e in expected[sheet, number]:
                            key = (e['chrom'], int(e['intron_start']), int(e['intron_end']), e['strand'])
                            if key not in keys or row.get('M', '') != e['author_symbols'] or row.get('D', '') != e['author_transcript']:
                                raise ValueError('Original author row differs from projection')
                        checked.append({'sheet': sheet, 'row': number, 'evidence_references': len(expected[sheet, number])})
                    if number >= max(wanted):
                        break
    if len(checked) != len(expected):
        raise ValueError('Not all original author rows recovered')
    (out / 'primary_rows.json').write_text(json.dumps({'rows': checked,
        'rows_verified': len(checked), 'evidence_references_verified': sum(x['evidence_references'] for x in checked),
        'checks': 'Pinned original XLSX blocks, eligible label geometry, gene and transcript fields'}, indent=2) + '\n')


def run(cache, out, author_cache=None):
    parent = ROOT / 'reports/author-junction-match'
    candidates = a.pinned_rows(parent / 'matches.tsv', a.PINS['matches.tsv'])
    evidence = a.pinned_rows(parent / 'evidence.tsv', a.PINS['evidence.tsv'])
    target = {a.tuplekey(r): r for r in candidates if r['match_status'] == 'coordinate_match_different_gene'}
    if len(target) != 74:
        raise ValueError('Expected74 conflict keys')
    selected = [e for e in evidence if a.tuplekey(e) in target]
    by_id, by_symbol = a.m.reference_index(cache / 'gencode.v47.annotation.gtf.gz')
    pairs = {}
    for e in selected:
        state, gid = a.m.resolve(e['author_symbols'], by_symbol)
        if state != 'unique_reference_gene' or gid == e['gene_id']:
            raise ValueError('Expected unique different author gene')
        ref = by_id[gid]
        if (ref['chrom'], ref['strand']) != (e['chrom'], e['strand']):
            raise ValueError('Author locus discordance')
        pairs[a.tuplekey(e), gid] = (target[a.tuplekey(e)], gid)
    genes = {r['gene_id'] for r in target.values()} | {gid for _, gid in pairs}
    geo = json.loads((ROOT / 'research/references/geo_isoseq_sources_20261029.json').read_text())
    sources = [('GENCODE', 'gencode.v47.annotation.gtf.gz', a.m.REFERENCE_SHA256)]
    sources += [(name.split('_')[0], name, spec['cache_sha256']) for name, spec in geo.items() if name.endswith('.gtf.gz')]
    indices, source_qc = {}, []
    for label, name, pin in sources:
        path = cache / name
        if hashlib.sha256(path.read_bytes()).hexdigest() != pin:
            raise ValueError('GTF hash mismatch')
        with gzip.open(path, 'rt') as f:
            index, n = models(f, genes)
        indices[label] = index
        source_qc.append({'source': label, 'file': name, 'sha256': pin, 'target_transcript_groups': n})
    out.mkdir(parents=True, exist_ok=True)
    results = []
    for (key, gid), (row, _) in sorted(pairs.items()):
        r = {k: row[k] for k in a.KEY}
        r.update(candidate_symbol=row['reference_symbol'], author_gene_id=gid, author_symbol=by_id[gid]['symbol'])
        c, b = by_id[row['gene_id']], by_id[gid]
        r['reference_gene_spans_overlap_diagnostic_only'] = max(c['start'], b['start']) <= min(c['end'], b['end'])
        for label, index in indices.items():
            r[label + '_candidate_transcripts'] = ';'.join(witness(index, row, row['gene_id'])) or '.'
            r[label + '_author_transcripts'] = ';'.join(witness(index, row, gid)) or '.'
        r['reference_junction_category'] = canonical_category(
            r['GENCODE_candidate_transcripts'] != '.', r['GENCODE_author_transcripts'] != '.')
        r['gene_assignment_resolved'] = False
        results.append(r)
    with (out / 'conflicts.tsv').open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(results[0]), delimiter='\t', lineterminator='\n')
        w.writeheader();w.writerows(results)
    summary = {'candidate_keys': len(target), 'candidate_genes': len({r['gene_id'] for r in target.values()}),
        'candidate_author_pairs': len(results), 'author_evidence_rows_not_replicates': len(selected),
        'reference_pair_categories': dict(collections.Counter(r['reference_junction_category'] for r in results)),
        'geo_model_pair_states': {label: dict(collections.Counter(
            ('both_genes' if r[label + '_candidate_transcripts'] != '.' and r[label + '_author_transcripts'] != '.' else
             'candidate_only' if r[label + '_candidate_transcripts'] != '.' else
             'author_only' if r[label + '_author_transcripts'] != '.' else 'neither_gene') for r in results))
             for label in indices if label != 'GENCODE'},
        'spans_overlap_pairs_diagnostic_only': sum(r['reference_gene_spans_overlap_diagnostic_only'] for r in results),
        'source_qc': source_qc, 'assignments_resolved': 0, 'original_strict_matches_unchanged': 354,
        'interpretation': 'Exact annotation/model witnesses are alternative explanations, not proof of true gene, read support, function or novelty'}
    (out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    if author_cache:
        primary_rows(author_cache, selected, out)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--cache', type=Path, required=True)
    p.add_argument('--author-cache', type=Path)
    p.add_argument('--out', type=Path, default=ROOT / 'reports/author-gene-conflicts')
    args = p.parse_args()
    run(args.cache, args.out, args.author_cache)
