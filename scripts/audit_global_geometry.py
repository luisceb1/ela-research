"""All-gene exact reference geometry with two-pass complete-exon recovery."""
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
    from scripts.audit_gene_conflicts import junctions
except ModuleNotFoundError:
    import audit_gene_ambiguity as a
    from audit_gene_conflicts import junctions

ROOT = Path(__file__).resolve().parents[1]
GENE = re.compile(r'gene_id "([^"]+)"')
TX = re.compile(r'transcript_id "([^"]+)"')
NAME = re.compile(r'gene_name "([^"]*)"')


def geometry(row):
    return row['chrom'], int(row['intron_start']), int(row['intron_end']), row['strand']


def global_lookup(open_lines, wanted):
    """open_lines must supply a fresh iterator for each of two complete passes."""
    lefts, rights = collections.defaultdict(set), collections.defaultdict(set)
    for chrom, left, right, strand in wanted:
        if left < 1 or right < left or strand not in ('+', '-'):
            raise ValueError('Invalid wanted intron')
        lefts[chrom, strand].add(left - 1)
        rights[chrom, strand].add(right + 1)
    selected, genes, exons_seen = set(), {}, 0
    with open_lines() as lines:
        for line in lines:
            if line.startswith('#'):
                continue
            p = line.rstrip('\n').split('\t')
            if len(p) != 9:
                raise ValueError('Malformed reference GTF')
            if p[2] == 'gene':
                gid = GENE.search(p[8]);name = NAME.search(p[8])
                if gid is None:
                    raise ValueError('Gene ID missing')
                key = a.m.stable(gid[1]);value = (p[0], p[6], name[1] if name else '')
                if key in genes and genes[key] != value:
                    raise ValueError('Conflicting gene identity')
                genes[key] = value
            if p[2] != 'exon':
                continue
            exons_seen += 1
            if int(p[4]) not in lefts[p[0], p[6]] and int(p[3]) not in rights[p[0], p[6]]:
                continue
            gid, tx = GENE.search(p[8]), TX.search(p[8])
            if not gid or not tx:
                raise ValueError('Missing exon gene/transcript ID')
            selected.add((a.m.stable(gid[1]), tx[1], p[0], p[6]))
    selected_names = {t[1] for t in selected}
    groups = collections.defaultdict(list)
    with open_lines() as lines:
        for line in lines:
            if line.startswith('#'):
                continue
            p = line.rstrip('\n').split('\t')
            if len(p) != 9:
                raise ValueError('Malformed reference GTF')
            if p[2] != 'exon':
                continue
            tx = TX.search(p[8])
            if not tx or tx[1] not in selected_names:
                continue
            gid = GENE.search(p[8])
            if not gid:
                raise ValueError('Missing selected gene ID')
            key = (a.m.stable(gid[1]), tx[1], p[0], p[6])
            if key in selected:
                groups[key].append((int(p[3]), int(p[4])))
    if set(groups) != selected:
        raise ValueError('Selected transcript missing in second pass')
    hits = collections.defaultdict(set)
    for (gid, tx, chrom, strand), exons in groups.items():
        for left, right in junctions(exons):
            g = (chrom, left, right, strand)
            if g in wanted:
                hits[g].add((gid, tx))
    return genes, hits, {'reference_gene_records': len(genes), 'reference_exon_records': exons_seen,
                        'anchor_selected_transcript_groups': len(selected),
                        'all_exons_in_selected_groups': sum(map(len, groups.values()))}


def classify(gid, hits):
    if any(gene == gid for gene, tx in hits):
        return 'same_gene_exact'
    return 'other_gene_only_exact' if hits else 'not_found_in_v47_any_gene'


def coverage_group(global_status, author_status):
    if global_status != 'not_found_in_v47_any_gene':
        return 'reference_geometry_annotated'
    if author_status in ('exact_nonTE_label_match', 'TE_transcript_context_only'):
        return 'author_catalog_representation_only'
    if author_status == 'not_found_in_eligible_culture_subset':
        return 'not_found_in_two_inspected_resources'
    return 'author_or_reference_identity_unresolved'


def run(reference, out):
    parent = ROOT / 'reports/author-junction-match'
    rows = a.pinned_rows(parent / 'matches.tsv', a.PINS['matches.tsv'])
    if len(rows) != 1901 or len({a.tuplekey(r) for r in rows}) != 1901:
        raise ValueError('Candidate universe changed')
    if hashlib.sha256(reference.read_bytes()).hexdigest() != a.m.REFERENCE_SHA256:
        raise ValueError('Reference hash mismatch')
    genes, lookup, qc = global_lookup(lambda: gzip.open(reference, 'rt'), {geometry(r) for r in rows})
    output, evidence = [], []
    for row in rows:
        g = geometry(row);hits = lookup.get(g, set())
        same = sorted({tx for gid, tx in hits if gid == row['gene_id']})
        other = sorted({gid for gid, tx in hits if gid != row['gene_id']})
        state = classify(row['gene_id'], hits)
        if bool(same) != (row['gencode_status'] == 'exact_same_gene_junction'):
            raise ValueError('Same-gene positive control differs from prior audit')
        output.append({**{k: row[k] for k in a.KEY}, 'candidate_symbol': row['reference_symbol'],
            'previous_same_gene_status': row['gencode_status'], 'author_catalog_status': row['match_status'],
            'global_status': state, 'same_gene_transcripts': ';'.join(same) or '.',
            'coverage_group': coverage_group(state, row['match_status']),
            'other_gene_ids': ';'.join(other) or '.', 'reference_genes_with_geometry': len({gid for gid, tx in hits}),
            'reference_transcripts_with_geometry': len(hits)})
        for gid, tx in sorted(hits):
            evidence.append({**{k: row[k] for k in a.KEY}, 'reference_gene_id': gid,
                'reference_symbol': genes[gid][2], 'reference_transcript': tx,
                'relationship': 'same_gene' if gid == row['gene_id'] else 'other_gene'})
    # All 73 canonical alternative-gene witnesses must be reproduced exactly.
    conflicts_path = ROOT / 'reports/author-gene-conflicts/conflicts.tsv'
    if hashlib.sha256(conflicts_path.read_bytes()).hexdigest() != '655e6727f8531d73279b0e7e222dc299928899738ac0ca2815ace6e5252bcf82':
        raise ValueError('Alternative-gene control table changed')
    with conflicts_path.open(newline='') as f:
        conflicts = list(csv.DictReader(f, delimiter='\t'))
    verified = 0
    for r in conflicts:
        if r['reference_junction_category'] != 'author_reference_only':
            continue
        expected = {(r['author_gene_id'], tx) for tx in r['GENCODE_author_transcripts'].split(';')}
        if not expected.issubset(lookup.get(geometry(r), set())):
            raise ValueError('Prior alternative-gene witness lost')
        verified += 1
    if verified != 73:
        raise ValueError('Expected73 alternative-gene positive controls')
    out.mkdir(parents=True, exist_ok=True)
    for name, items, fields in [('annotation.tsv', output, list(output[0])),
            ('reference_witnesses.tsv', evidence, list(evidence[0]))]:
        with (out / name).open('w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n')
            w.writeheader();w.writerows(items)
    cross = collections.Counter((r['author_catalog_status'], r['global_status']) for r in output)
    geometries = {geometry(r) for r in rows}
    summary = {'candidate_keys': len(rows), 'candidate_genes': len({r['gene_id'] for r in rows}),
        'unique_geometries_without_candidate_gene': len(geometries),
        'candidate_statuses': dict(collections.Counter(r['global_status'] for r in output)),
        'joint_coverage_groups_not_novelty_classes': dict(collections.Counter(r['coverage_group'] for r in output)),
        'unique_geometries_annotated_any_gene': len(set(lookup) & geometries),
        'unique_geometries_not_found_any_gene': len(geometries - set(lookup)),
        'candidate_keys_with_both_same_and_other_gene_witnesses': sum(r['same_gene_transcripts'] != '.' and r['other_gene_ids'] != '.' for r in output),
        'author_cross_tab': [{'author_status': x, 'global_status': y, 'candidate_keys': n} for (x, y), n in sorted(cross.items())],
        'same_gene_controls_verified': sum(r['global_status'] == 'same_gene_exact' for r in output),
        'alternative_gene_controls_verified': verified, 'reference_qc': qc,
        'strict_author_matches_unchanged': 354, 'conditional_author_sensitivity_unchanged': 355,
        'novelty_assessed': False, 'clinical_data_used': False,
        'interpretation': 'Exact annotation geometry only; unknown origin/function/crypticity; not found is not novel'}
    (out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--reference', type=Path, required=True)
    p.add_argument('--out', type=Path, default=ROOT / 'reports/global-junction-geometry')
    args = p.parse_args()
    run(args.reference, args.out)
