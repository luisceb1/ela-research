"""Offline exact comparison of the closed UNC13A inventory with NCBI RefSeq.

No sequence data, network, endpoint shifts, coverage promotion or inference.
genePred exon arrays are genomic ascending on both strands: intron [end_i,start_i+1).
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

REGION = ['chr19', 17600000, 17690000]


def reference_edges(annotation):
    if (annotation.get('genome'), annotation.get('chrom'), annotation.get('track')) != ('hg38', 'chr19', 'ncbiRefSeq'):
        raise ValueError('Expected hg38 chr19 ncbiRefSeq')
    records = annotation.get('ncbiRefSeq', [])
    if annotation.get('itemsReturned') != len(records) or annotation.get('maxItemsLimit'):
        raise ValueError('Incomplete reference response')
    edges, names = {}, set()
    for row in records:
        if row['name2'] != 'UNC13A':
            continue
        if row['chrom'] != 'chr19' or row['strand'] != '-':
            raise ValueError('Unexpected UNC13A identity')
        starts = [int(x) for x in row['exonStarts'].strip(',').split(',')]
        ends = [int(x) for x in row['exonEnds'].strip(',').split(',')]
        if (len(starts) != len(ends) or len(starts) != row['exonCount'] or not starts
                or any(s < 0 or s >= e for s, e in zip(starts, ends))
                or any(e >= s for e, s in zip(ends, starts[1:]))
                or starts[0] != row['txStart'] or ends[-1] != row['txEnd']):
            raise ValueError('Invalid exon geometry')
        if row['name'] in names:
            raise ValueError('Duplicate transcript')
        names.add(row['name'])
        for start, end in zip(ends, starts[1:]):
            edges.setdefault(('chr19', start, end, '-'), set()).add(row['name'])
    if not names:
        raise ValueError('No UNC13A annotation')
    return edges, sorted(names)


def compare(inventory, annotation):
    if (inventory.get('status') != 'sealed_exploratory_locus_audit'
            or inventory.get('console_inventory_is_summary')
            or inventory.get('gate_promoted') is not False
            or inventory.get('original_control_gate') != 'coverage_insufficient'
            or inventory.get('same_prefix_target_and_qc_replay_identical') is not True):
        raise ValueError('Expected closed full reported inventory with insufficient coverage')
    audit = inventory['regional_audit']
    if audit['window'] != REGION:
        raise ValueError('Unexpected inventory window')
    edges, names = reference_edges(annotation)
    rows, summary = [], {}
    for route in ('text15', 'text8'):
        seen, matched = set(), 0
        for item in audit['routes'][route]['junctions']:
            event, support = item['event'], item['fragments']
            if (not isinstance(event, list) or len(event) != 4 or event[0] != 'chr19'
                    or event[3] not in ('-', '+') or type(event[1]) is not int
                    or type(event[2]) is not int or not 0 <= event[1] < event[2]
                    or event[1] >= REGION[2] or event[2] <= REGION[1]
                    or type(support) is not int or support <= 0):
                raise ValueError('Invalid observed junction')
            key = tuple(event)
            if key in seen:
                raise ValueError('Duplicate observed junction')
            seen.add(key)
            hits = sorted(edges.get(key, []))
            matched += bool(hits)
            rows.append(dict(route=route, chrom=event[0], start0=event[1], end0=event[2],
                             strand=event[3], fragments=support, exact_refseq=bool(hits),
                             curated_NM=';'.join(x for x in hits if x.startswith('NM_')),
                             predicted_XM=';'.join(x for x in hits if x.startswith('XM_'))))
        summary[route] = dict(observed=len(seen), exact_matches=matched, no_exact_match=len(seen)-matched)
    return dict(coordinate_convention='intronic 0-based half-open; no shifts',
                annotation_track='ncbiRefSeq', reference_transcripts=names,
                reference_distinct_junctions=len(edges), data_time=annotation.get('dataTime'),
                routes=summary, rows=sorted(rows, key=lambda r: (r['route'], r['start0'], r['end0'], r['strand'])),
                inventory_is_operator_report=True, independent_WSL_verification=False,
                coverage_gate='coverage_insufficient', gate_promoted=False,
                biological_validation=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inventory', type=Path, required=True)
    parser.add_argument('--annotation', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = compare(json.loads(args.inventory.read_bytes()), json.loads(args.annotation.read_bytes()))
    result['input_sha256'] = {label: hashlib.sha256(path.read_bytes()).hexdigest()
                              for label, path in [('inventory', args.inventory), ('annotation', args.annotation)]}
    args.out.mkdir(parents=True, exist_ok=False)
    (args.out / 'comparison.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    with (args.out / 'junctions.tsv').open('w', newline='', encoding='utf-8') as out:
        fields = ['route', 'chrom', 'start0', 'end0', 'strand', 'fragments', 'exact_refseq', 'curated_NM', 'predicted_XM']
        writer = csv.DictWriter(out, fieldnames=fields, delimiter='\t', lineterminator='\n')
        writer.writeheader()
        writer.writerows(result['rows'])
    print(json.dumps({key: value for key, value in result.items() if key != 'rows'}, indent=2))


if __name__ == '__main__':
    main()
