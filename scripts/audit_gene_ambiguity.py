"""Conservative gene-identity sensitivity, separate from original exact matches."""
import argparse
import collections
import csv
import gzip
import hashlib
import json
from pathlib import Path
import re

try:
    from scripts import match_author_junctions as m
except ModuleNotFoundError:
    import match_author_junctions as m

ROOT = Path(__file__).resolve().parents[1]
PINS = {'matches.tsv': 'd6a5730a03cf0241147d3bc6c4456cb1691443d0f5a62c436f103fe97c4c46f6',
        'evidence.tsv': 'b04796b59aa7c039cd0ab8c5380484e2f0e3416d43e26100d8dfca37a54b3e65'}
KEY = ['gene_id', 'chrom', 'intron_start', 'intron_end', 'strand']


def tuplekey(row):
    return tuple(row[k] for k in KEY)


def candidate_id(row, by_id):
    gid = m.stable(row['gene_id'])
    ref = by_id.get(gid)
    if ref is None:
        return 'reference_gene_missing'
    if (ref['chrom'], ref['strand']) != (row['chrom'], row['strand']):
        return 'reference_locus_discordant'
    return 'candidate_id_locus_confirmed'


def author_resolution(value, chrom, strand, candidate, by_id, by_symbol):
    tokens = sorted(set(t.strip() for t in value.split(',')))
    all_ids, unknown, provenance = set(), [], []
    for token in tokens:
        if re.fullmatch(r'ENSG\d+(?:\.\d+)?(?:_PAR_Y)?', token):
            stable = m.stable(token)
            ids = {stable} if stable in by_id else set()
            source = 'explicit_stable_id'
        else:
            ids = set(by_symbol.get(token, set())) if token not in ('', '.', 'NA', 'None') else set()
            source = 'exact_reference_symbol'
        if not ids:
            unknown.append(token)
        all_ids.update(ids)
        provenance.append({'token': token, 'method': source, 'ids': sorted(ids)})
    compatible = {gid for gid in all_ids if (by_id[gid]['chrom'], by_id[gid]['strand']) == (chrom, strand)}
    # Unknown tokens cannot be discarded simply because a known token matches.
    if unknown:
        state = 'unresolved_token'
    elif not compatible:
        state = 'no_id_at_chrom_strand'
    elif len(compatible) > 1:
        state = 'multiple_ids_at_chrom_strand'
    elif compatible == {candidate}:
        state = 'conditional_same_gene'
    else:
        state = 'conditional_other_gene'
    return {'state': state, 'tokens_json': json.dumps(provenance, ensure_ascii=False, separators=(',', ':')),
            'all_ids': ';'.join(sorted(all_ids)) or '.',
            'compatible_ids': ';'.join(sorted(compatible)) or '.',
            'excluded_locus_ids': ';'.join(sorted(all_ids - compatible)) or '.',
            'unresolved_tokens_json': json.dumps(unknown, ensure_ascii=False)}


def pinned_rows(path, expected):
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise ValueError('Pinned table changed: ' + str(path))
    with path.open(newline='') as f:
        return list(csv.DictReader(f, delimiter='\t'))


def write(path, rows, fields):
    with path.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n')
        w.writeheader();w.writerows(rows)


def primary_checks(author_cache, geo_cache, out):
    manifest = json.loads((ROOT / 'research/references/bolger_author_catalog_v1.json').read_text())
    raw = m.a.pinned(author_cache / 'media-9.xlsx', manifest['files']['media-9.xlsx'])
    wanted = {'S8A': {16245, 16246}, 'S8D': {13754}}
    rows = []
    with m.a.office(raw, 'xlsx') as z:
        strings = m.a.shared_strings(z)
        for name, path in m.a.sheets(z):
            if name not in wanted:
                continue
            for n, cells in m.a.raw_rows(z, path):
                if n in wanted[name]:
                    r = m.a.decode(cells, strings)
                    keys, excluded = m.eligible_keys(r, 'S8')
                    if ('chrY', 317052, 317278, '-') not in keys or r['M'] != 'GTPBP6':
                        raise ValueError('Conditional primary row check failed')
                    rows.append({'sheet': name, 'row': n,
                                 'fields': {c: r.get(c, '') for c in ['A', 'B', 'C', 'D', 'F', 'J', 'K', 'L', 'M', 'N', 'O']},
                                 'target_intronic_key_recovered': True, 'excluded_labels': excluded})
                if n >= max(wanted[name]):
                    break
    if len(rows) != 3:
        raise ValueError('Expected all three conditional source rows')
    (out / 'conditional_primary_rows.json').write_text(json.dumps({
        'source_sha256': m.a.sha256(raw), 'rows': rows,
        'interpretation': 'Direct eligible-block/label check; not raw-read chromosomal assignment'}, indent=2) + '\n')
    pins = {'GSE310723_i3N_isoseq_extended_annotations.gtf.gz': '4a72d89df3f76c55694a53cca4462b53e5b1fc6cb4c3d931b26dd8402ac6e288',
            'GSE315972_NYGC_isoseq_extended_annotations.gtf.gz': '53bbd59fd8e3bbf558a9c5a60e6af0e3c658455d6b7db8e2b86c2420051e0976'}
    provenance = []
    for name, pin in pins.items():
        path = geo_cache / name
        if hashlib.sha256(path.read_bytes()).hexdigest() != pin:
            raise ValueError('GEO source changed')
        count, examples = 0, []
        with gzip.open(path, 'rt') as f:
            for line in f:
                attrs = line.rstrip().split('\t')
                if len(attrs) == 9 and re.search(r'gene_id "ENSG00000276256(?:\.\d+)?";', attrs[8]):
                    count += 1
                    if len(examples) < 3:
                        examples.append(line.rstrip())
        if not count:
            raise ValueError('Missing gene provenance not recovered in original GTF')
        provenance.append({'file': name, 'sha256': pin, 'matching_lines_not_replicates': count,
                           'examples': examples, 'meaning': 'Published source annotation, not inferred replacement ID'})
    (out / 'missing_gene_provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')


def run(reference, out):
    parent = ROOT / 'reports/author-junction-match'
    candidates = pinned_rows(parent / 'matches.tsv', PINS['matches.tsv'])
    evidence = pinned_rows(parent / 'evidence.tsv', PINS['evidence.tsv'])
    if len(candidates) != 1901 or len({tuplekey(r) for r in candidates}) != 1901:
        raise ValueError('Candidate universe changed')
    by_id, by_symbol = m.reference_index(reference)
    index = {tuplekey(r): r for r in candidates}
    by_candidate = collections.defaultdict(list)
    all_diagnostics = []
    for e in evidence:
        k = tuplekey(e)
        if k not in index:
            raise ValueError('Evidence outside candidate universe')
        result = author_resolution(e['author_symbols'], e['chrom'], e['strand'], e['gene_id'], by_id, by_symbol)
        diag = {**e, **result}
        by_candidate[k].append(diag)
        all_diagnostics.append(diag)
    reference_rows, targeted_rows, all_rows = [], [], []
    for row in candidates:
        k = tuplekey(row)
        es = by_candidate[k]
        identity = candidate_id(row, by_id)
        conditional = [e for e in es if e['state'] == 'conditional_same_gene'] if identity == 'candidate_id_locus_confirmed' else []
        result = {k: row[k] for k in KEY}
        result.update(previous_status=row['match_status'], candidate_id_state=identity,
                      conditional_same_rows=len(conditional),
                      conditional_s8_rows=sum(e['category'] == 'S8' for e in conditional),
                      conditional_s7_rows=sum(e['category'] == 'S7' for e in conditional),
                      evidence_rows=len(es),
                      row_states_json=json.dumps(dict(collections.Counter(e['state'] for e in es)), sort_keys=True))
        all_rows.append(result)
        if row['reference_identity'] != 'reference_identity_resolved':
            ref = by_id.get(row['gene_id'])
            reference_rows.append({**result, 'source_symbol': row['reference_symbol'],
                                   'reference_symbol': ref['symbol'] if ref else '.',
                                   'global_symbol_ids': ';'.join(sorted(by_symbol.get(row['reference_symbol'], set()))) or '.'})
        if row['match_status'] == 'coordinate_match_gene_unresolved':
            targeted_rows.append(result)
    if len(reference_rows) != 36 or len(targeted_rows) != 278:
        raise ValueError('Target partitions changed')
    baseline_strict = {'exact_nonTE_label_match', 'TE_transcript_context_only'}
    strict = [r for r in all_rows if r['previous_status'] in baseline_strict]
    if len(strict) != 354 or any(not r['conditional_same_rows'] for r in strict):
        raise ValueError('Baseline positive controls lost')
    additional = [r for r in all_rows if r['conditional_same_rows'] and r['previous_status'] not in baseline_strict]
    fields = KEY + ['previous_status', 'candidate_id_state', 'conditional_same_rows', 'conditional_s8_rows',
                    'conditional_s7_rows', 'evidence_rows', 'row_states_json']
    out.mkdir(parents=True, exist_ok=True)
    write(out / 'candidate_identity.tsv', reference_rows, fields + ['source_symbol', 'reference_symbol', 'global_symbol_ids'])
    write(out / 'author_ambiguous_candidates.tsv', targeted_rows, fields)
    write(out / 'all_candidates.tsv', all_rows, fields)
    write(out / 'evidence_diagnostics.tsv', all_diagnostics,
          list(evidence[0]) + ['state', 'tokens_json', 'all_ids', 'compatible_ids', 'excluded_locus_ids', 'unresolved_tokens_json'])
    summary = {'candidates': len(candidates), 'evidence_rows_not_replicates': len(evidence),
               'reference_36_states': dict(collections.Counter(r['candidate_id_state'] for r in reference_rows)),
               'author_278_conditional_same': sum(bool(r['conditional_same_rows']) for r in targeted_rows),
               'author_278_evidence_states': dict(collections.Counter(e['state'] for r in targeted_rows for e in by_candidate[tuplekey(r)])),
               'baseline_strict_unchanged': len(strict), 'additional_conditional_candidates': additional,
               'all_evidence_states': dict(collections.Counter(r['state'] for r in all_diagnostics)),
               'conditional_total_not_new_strict_matches': sum(bool(r['conditional_same_rows']) for r in all_rows),
               'gene_spans_or_nearest_neighbor_used': False, 'clinical_data_used': False,
               'interpretation': 'Annotation-dependent sensitivity; no new transcript, function, replication or novelty claim'}
    (out / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--reference', type=Path, required=True)
    p.add_argument('--out', type=Path, default=ROOT / 'reports/author-gene-ambiguity')
    p.add_argument('--author-cache', type=Path)
    p.add_argument('--geo-cache', type=Path)
    args = p.parse_args()
    if bool(args.author_cache) != bool(args.geo_cache):
        p.error('Provide both primary-source cache paths, or neither')
    run(args.reference, args.out)
    if args.author_cache:
        primary_checks(args.author_cache, args.geo_cache, args.out)
