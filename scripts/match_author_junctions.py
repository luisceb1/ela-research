#!/usr/bin/env python3
"""Exact culture catalog overlap, with gene identity and explicit missingness."""
import argparse
import collections
import csv
import gzip
import json
import re
from pathlib import Path

try:
    from scripts import audit_author_catalog as a
except ModuleNotFoundError:
    import audit_author_catalog as a

ROOT = Path(__file__).resolve().parents[1]
INPUT_SHA256 = 'd8e28f96f5a3257766d79321a554f54b87233d3095962a33871bcbea357fad23'
REFERENCE_SHA256 = 'df11938c66d2b39f8ebbdb5f1720919321f9cf9d58f02b019753f6a24ca3db24'
STMN2 = ('ENSG00000104435', 'chr8', 79611215, 79616821, '+')
CANONICAL_STMN2 = ('chr8', 79636898, 79641377, '+')
CONTROL_SOURCE_SHA256 = 'e26d9d9d172d233151be7455f303e4a7977cd6a6a36d6182ed95925e495fff58'


def verify_control_source():
    path = ROOT / 'reports/isoforms/junctions.tsv'
    if a.sha256(path.read_bytes()) != CONTROL_SOURCE_SHA256:
        raise ValueError('Control source SHA256 changed')
    with path.open(newline='') as f:
        rows = list(csv.DictReader(f, delimiter='\t'))
    geometry = {(r['chrom'], int(r['left_exon_end']) + 1, int(r['right_exon_start']) - 1, r['strand'])
                for r in rows if r['gse'] == 'GSE310723' and r['symbol'] == 'STMN2'}
    if STMN2[1:] not in geometry or CANONICAL_STMN2 not in geometry:
        raise ValueError('Known control geometries not present in GTF projection')


def stable(value):
    return re.sub(r'\.\d+(?=_PAR_Y$|$)', '', value)


def reference_index(path):
    if a.sha256(path.read_bytes()) != REFERENCE_SHA256:
        raise ValueError('Reference SHA256 changed')
    by_id, by_symbol = {}, collections.defaultdict(set)
    with gzip.open(path, 'rt') as f:
        for line in f:
            if line.startswith('#'):
                continue
            p = line.rstrip('\n').split('\t')
            if p[2] != 'gene':
                continue
            attrs = dict(re.findall(r'(\w+) "([^"]*)"', p[8]))
            gid = stable(attrs['gene_id'])
            rec = {'symbol': attrs.get('gene_name', ''), 'chrom': p[0], 'strand': p[6],
                   'start': int(p[3]), 'end': int(p[4])}
            if gid in by_id and by_id[gid] != rec:
                raise ValueError('Conflicting reference gene identity')
            by_id[gid] = rec
            by_symbol[rec['symbol']].add(gid)
    return by_id, by_symbol


def resolve(value, by_symbol):
    tokens = set(x.strip() for x in value.split(',') if x.strip())
    if not tokens or tokens <= {'None', '.', 'NA'}:
        return 'missing_author_gene', None
    if len(tokens) != 1:
        return 'multiple_author_symbols', None
    ids = by_symbol.get(next(iter(tokens)), set())
    if not ids:
        return 'symbol_not_in_reference', None
    if len(ids) != 1:
        return 'ambiguous_reference_symbol', None
    return 'unique_reference_gene', next(iter(ids))


def key(row):
    return row['gene_id'], row['chrom'], int(row['intron_start']), int(row['intron_end']), row['strand']


def candidate_identity(row, by_id, by_symbol):
    k = key(row)
    if k[2] < 1 or k[3] < k[2] or k[4] not in ('+', '-'):
        raise ValueError('Invalid candidate coordinates')
    ref = by_id.get(k[0])
    if not ref:
        return 'reference_gene_missing'
    state, gid = resolve(row['reference_symbol'], by_symbol)
    if state != 'unique_reference_gene' or gid != k[0]:
        return 'reference_symbol_not_unique_for_id'
    if (ref['chrom'], ref['strand']) != (k[1], k[4]):
        return 'reference_locus_discordant'
    return 'reference_identity_resolved'


def eligible_keys(row, category):
    """BED blocks define truth; S8 label must equal an exonic-boundary pair."""
    intronic, boundary = a.bed_junctions(row)
    if category == 'S7':
        return intronic, 0
    labels = a.listed_introns(row.get('N', ''))
    valid, excluded = set(), 0
    for chrom, left, right, strand in labels:
        if (chrom, left, right, strand) not in boundary:
            excluded += 1
            continue
        converted = (chrom, left + 1, right - 1, strand)
        if converted not in intronic:
            raise ValueError('Coordinate conversion failed internal consistency')
        valid.add(converted)
    return valid, excluded


def evidence_identity(row, candidate, by_id, by_symbol):
    state, gid = resolve(row.get('M', ''), by_symbol)
    if state != 'unique_reference_gene':
        return state
    rec = by_id[gid]
    if (rec['chrom'], rec['strand']) != (row.get('A'), row.get('F')):
        return 'author_gene_locus_discordant'
    return 'exact_same_gene' if gid == candidate[0] else 'different_unique_gene'


def classify(identity, evidence):
    if identity != 'reference_identity_resolved':
        return 'reference_identity_unresolved'
    strict = [e for e in evidence if e['gene_resolution'] == 'exact_same_gene']
    if any(e['category'] == 'S8' for e in strict):
        return 'exact_nonTE_label_match'
    if strict:
        return 'TE_transcript_context_only'
    if any(e['gene_resolution'] != 'different_unique_gene' for e in evidence):
        return 'coordinate_match_gene_unresolved'
    if evidence:
        return 'coordinate_match_different_gene'
    return 'not_found_in_eligible_culture_subset'


def control_eligibility(diagnostics):
    partial, canonical = [], []
    for d in diagnostics:
        fields = d['fields_by_column']
        if fields.get('M') != 'STMN2' or (fields.get('A'), fields.get('F')) != ('chr8', '+'):
            continue
        if d['block_valid'] and any(tuple(k) == CANONICAL_STMN2 for k in d['intronic_keys']):
            canonical.append({'sheet': d['sheet'], 'sheet_row': d['sheet_row']})
        if not d['block_valid']:
            try:
                offsets = [a.integer(x) for x in fields['L'].rstrip(',').split(',')]
                n = a.integer(fields['J'])
                anchor = a.integer(fields['B']) + offsets[-1] + 1
            except (ValueError, KeyError, IndexError):
                continue
            if n == 2 and len(offsets) == 2 and offsets[0] == 0 and anchor == STMN2[3] + 1:
                partial.append({'sheet': d['sheet'], 'sheet_row': d['sheet_row'],
                                'partial_right_exonic_anchor': anchor, 'not_a_full_junction_match': True})
    return {'canonical_geometry_control': {'intronic_key': CANONICAL_STMN2, 'evidence': canonical,
                                           'recovered': bool(canonical), 'not_a_cryptic_event': True},
            'cryptic_control_source_eligibility': 'not_evaluable_due_to_invalid_blocks' if partial else 'no_partial_anchor_identified',
            'invalid_block_partial_anchor_rows': partial}


def match_tables(cache, candidates, by_id, by_symbol, manifest):
    index = collections.defaultdict(list)
    for c in candidates:
        k = key(c)
        index[k[1:]].append(k)
    if STMN2 not in {key(c) for c in candidates}:
        index[STMN2[1:]].append(STMN2)
    evidence = collections.defaultdict(list)
    qc = []
    control_diagnostics = []
    for filename, category in [('media-8.xlsx', 'S7'), ('media-9.xlsx', 'S8')]:
        raw = a.pinned(cache / filename, manifest['files'][filename])
        with a.office(raw, 'xlsx') as z:
            spec = a.sheets(z)
            if {s for s, _ in spec} != {category + x for x in 'ABCD'}:
                raise ValueError('Culture-only sheet allowlist changed')
            strings = a.shared_strings(z)
            for sheet, path in spec:
                counts = collections.Counter()
                reasons = collections.Counter()
                for number, cells in a.raw_rows(z, path):
                    if number <= 2:
                        continue
                    row = a.decode(cells, strings)
                    if not any(row.values()):
                        continue
                    counts['rows'] += 1
                    if row.get('A') == 'chr8' and row.get('F') == '+':
                        try:
                            covers_control = int(row.get('B', '0')) <= STMN2[2] and int(row.get('C', '0')) >= STMN2[3]
                        except ValueError:
                            covers_control = False
                        if covers_control and sum(x['sheet'] == sheet for x in control_diagnostics) < 20:
                            diag = {'sheet': sheet, 'sheet_row': number,
                                    'fields_by_column': {k: row.get(k, '') for k in ['A', 'B', 'C', 'D', 'F', 'J', 'K', 'L', 'M', 'N', 'O']}}
                            try:
                                ik, ek = a.bed_junctions(row)
                                diag['block_valid'] = True
                                diag['intronic_keys'] = sorted(ik)
                                diag['exonic_boundary_keys'] = sorted(ek)
                            except ValueError as exc:
                                diag['block_valid'] = False
                                diag['block_error'] = str(exc)
                            control_diagnostics.append(diag)
                    try:
                        # Separate invalid block/label rows instead of accepting label-only claims.
                        a.bed_junctions(row)
                    except ValueError as exc:
                        counts['invalid_block_rows'] += 1
                        reasons[str(exc)] += 1
                        continue
                    counts['valid_block_rows'] += 1
                    try:
                        keys, excluded = eligible_keys(row, category)
                    except ValueError as exc:
                        counts['invalid_label_rows'] += 1
                        reasons[str(exc)] += 1
                        continue
                    counts['unexplained_labels_excluded'] += excluded
                    counts['eligible_rows_with_junction'] += bool(keys)
                    matched_row = False
                    for geometry in sorted(keys):
                        for candidate in index.get(geometry, []):
                            state = evidence_identity(row, candidate, by_id, by_symbol)
                            evidence[candidate].append({
                                'category': category, 'sheet': sheet, 'sheet_row': number,
                                'author_transcript': row.get('D', ''), 'author_symbols': row.get('M', ''),
                                'author_class': row.get('O', ''), 'gene_resolution': state})
                            matched_row = True
                    counts['rows_with_candidate_or_control_geometry'] += matched_row
                qc.append({'file': filename, 'sheet': sheet, 'counts': dict(counts), 'excluded_reasons': dict(reasons)})
    return evidence, qc, control_diagnostics


def write_tsv(path, rows, fields):
    with path.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


def run(cache, reference, output):
    verify_control_source()
    source = ROOT / 'reports/gencode-junction-annotation/annotation.tsv'
    if a.sha256(source.read_bytes()) != INPUT_SHA256:
        raise ValueError('Candidate table SHA256 changed')
    with source.open(newline='') as f:
        candidates = list(csv.DictReader(f, delimiter='\t'))
    if len(candidates) != 1901 or len({key(c) for c in candidates}) != 1901:
        raise ValueError('Expected 1901 unique candidate keys')
    by_id, by_symbol = reference_index(reference)
    identities = {key(c): candidate_identity(c, by_id, by_symbol) for c in candidates}
    if STMN2[0] not in by_id or by_symbol.get('STMN2') != {STMN2[0]}:
        raise ValueError('Reference STMN2 positive control identity failed')
    manifest = json.loads((ROOT / 'research/references/bolger_author_catalog_v1.json').read_text())
    evidence, qc, control_diagnostics = match_tables(cache, candidates, by_id, by_symbol, manifest)
    # Verify that all source rows and block exclusions equal the independent schema audit.
    baseline = json.loads((ROOT / 'reports/author-catalog-schema/audit.json').read_text())
    expected = {(f, x['sheet']): x['counts'] for f, entries in baseline['culture_structure_qc'].items() for x in entries}
    for r in qc:
        for name in ['rows', 'valid_block_rows', 'invalid_block_rows']:
            if r['counts'].get(name, 0) != expected[r['file'], r['sheet']].get(name, 0):
                raise ValueError('Independent block QC counts differ')
    table, rows = [], []
    for c in candidates:
        k = key(c)
        es = evidence.get(k, [])
        strict = [e for e in es if e['gene_resolution'] == 'exact_same_gene'] if identities[k] == 'reference_identity_resolved' else []
        result = {n: c[n] for n in ['gene_id', 'chrom', 'intron_start', 'intron_end', 'strand', 'reference_symbol']}
        result.update({'reference_identity': identities[k], 'gencode_status': c['status'],
                       'match_status': classify(identities[k], es),
                       's8_sheets': ';'.join(sorted({e['sheet'] for e in strict if e['category'] == 'S8'})) or '.',
                       's7_context_sheets': ';'.join(sorted({e['sheet'] for e in strict if e['category'] == 'S7'})) or '.',
                       'strict_evidence_rows': len(strict), 'other_geometry_evidence_rows': len(es) - len(strict)})
        table.append(result)
        for e in es:
            rows.append(dict(zip(['gene_id', 'chrom', 'intron_start', 'intron_end', 'strand'], k), **e))
    control_evidence = evidence.get(STMN2, [])
    control_status = classify('reference_identity_resolved', control_evidence)
    control_checks = control_eligibility(control_diagnostics)
    if not control_checks['canonical_geometry_control']['recovered']:
        raise ValueError('Real canonical STMN2 geometry positive control not recovered')
    summary = {'input_junctions': len(table), 'input_genes': len({x['gene_id'] for x in table}),
               'reference_genes': len(by_id), 'ambiguous_reference_symbols': sum(len(x) > 1 for x in by_symbol.values()),
               'candidate_identity_statuses': dict(collections.Counter(identities.values())),
               'statuses': dict(collections.Counter(x['match_status'] for x in table)),
               's8_exact_unique_junctions': sum(x['s8_sheets'] != '.' and x['reference_identity'] == 'reference_identity_resolved' for x in table),
               's7_context_unique_junctions': sum(x['s7_context_sheets'] != '.' and x['reference_identity'] == 'reference_identity_resolved' for x in table),
               'both_s7_and_s8': sum(x['s7_context_sheets'] != '.' and x['s8_sheets'] != '.' and x['reference_identity'] == 'reference_identity_resolved' for x in table),
               'control_STMN2': {'key': STMN2, 'status': control_status, 'evidence': control_evidence,
                                 'included_in_1901': STMN2 in identities, 'diagnostic_rows': control_diagnostics,
                                 **control_checks},
               'source_qc': qc, 'author_full_catalog_compared': False,
               'culture_eligible_structural_subset_compared': True, 'brain_author_tables_compared': False,
               'independent_biological_validation': False, 'absence_or_novelty_inferred': False,
               'candidate_sha256': INPUT_SHA256, 'reference_sha256': REFERENCE_SHA256,
               'control_source_sha256': CONTROL_SOURCE_SHA256,
               'identity_method': 'exact unique GENCODEv47 symbol-to-ENSG plus chromosome/strand; no aliases or proximity',
               'comparison_scope': 'S8 declared cryptic labels versus S7 TE-transcript context; valid blocks only; no expression inference'}
    output.mkdir(parents=True, exist_ok=True)
    write_tsv(output / 'matches.tsv', table, list(table[0]))
    evidence_fields = ['gene_id', 'chrom', 'intron_start', 'intron_end', 'strand', 'category', 'sheet',
                       'sheet_row', 'author_transcript', 'author_symbols', 'author_class', 'gene_resolution']
    write_tsv(output / 'evidence.tsv', rows, evidence_fields)
    (output / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    return summary


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cache', required=True, type=Path)
    p.add_argument('--reference', required=True, type=Path)
    p.add_argument('--out', type=Path, default=ROOT / 'reports/author-junction-match')
    args = p.parse_args()
    result = run(args.cache, args.reference, args.out)
    print(json.dumps({'statuses': result['statuses'], 'control': result['control_STMN2']['status']}))
