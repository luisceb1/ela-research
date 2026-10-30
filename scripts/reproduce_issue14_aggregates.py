"""Reproduce aggregate published-data summaries; never export case/sample rows."""
import argparse
import csv
import gzip
import hashlib
import itertools
import json
import math
from pathlib import Path
import statistics as st

GENES = {'STMN2': 'ENSG00000104435', 'UNC13A': 'ENSG00000130477', 'TARDBP': 'ENSG00000120948'}
CE_DECLARED = {'STMN2': ('chr8', 80529057, 80529284), 'UNC13A': ('chr19', 17753223, 17753350)}
PINS = {'GSE126542_NeuronalNuclei_RNAseq_counts.txt.gz': 'c7a9ddae801f160e5ee6f02d4a6f127bde351a1ca85adaaba07228d4c24da0f8',
        'GSE121569_dexseq-all.csv.gz': 'daaf355a7cbd48b617d30201ba289d8f0c4efc9fbc2a23ca2f991c84e1d814f4'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def signflip(values):
    if not values or any(not math.isfinite(v) for v in values):
        raise ValueError('Finite nonempty paired differences required')
    observed = abs(st.mean(values))
    return sum(abs(st.mean(v * s for v, s in zip(values, signs))) >= observed - 1e-12
               for signs in itertools.product((-1, 1), repeat=len(values))) / 2 ** len(values)


def validate_columns(header):
    expected = {f'S{i}_{condition}' for i in range(1, 8) for condition in ['TP', 'TN']}
    if len(header) != 14 or set(header) != expected:
        raise ValueError('Expected exactly seven technical TP/TN pairs')


def read_counts(path):
    with gzip.open(path, 'rt', newline='') as f:
        reader = csv.reader(f, delimiter='\t');header = next(reader);validate_columns(header)
        named, total, na, nrows = {}, [0] * 14, 0, 0
        for row in reader:
            if len(row) != 15:
                raise ValueError('GEO count row width changed')
            values = [int(x) for x in row[1:]]
            if any(x < 0 for x in values):
                raise ValueError('Negative counts')
            total = [a + b for a, b in zip(total, values)];nrows += 1
            if row[0] == 'NA':
                na += 1
            elif row[0] in named:
                raise ValueError('Duplicate named gene')
            else:
                named[row[0]] = values
    if not set(GENES).issubset(named) or min(total) <= 0:
        raise ValueError('Missing targets or empty library')
    return header, named, total, {'rows': nrows, 'literal_NA_rows': na, 'named_unique_genes': len(named), 'libraries': 14, 'pairs': 7}


def size_factors(named):
    positive = [v for v in named.values() if min(v) > 0]
    if not positive:
        raise ValueError('No all-positive genes')
    ratios = [[] for _ in positive[0]]
    for values in positive:
        gm = math.exp(st.mean(math.log(x) for x in values))
        for col, value in zip(ratios, values):
            col.append(value / gm)
    factors = [st.median(x) for x in ratios]
    gm = math.exp(st.mean(math.log(x) for x in factors))
    return [x / gm for x in factors], len(positive)


def paired_differences(values, header):
    lookup = dict(zip(header, values))
    return [lookup[f'S{i}_TN'] - lookup[f'S{i}_TP'] for i in range(1, 8)]


def expression(path):
    from scipy.stats import t
    header, named, total, qc = read_counts(path)
    factors, n = size_factors(named)
    if n < 1000:
        raise ValueError('Insufficient all-positive genes for this reproduction')
    qc['positive_genes_for_size_factors'] = n
    named_total = [sum(v[i] for v in named.values()) for i in range(14)]
    output = []
    for gene in GENES:
        raw = named[gene]
        if min(raw) <= 0:
            raise ValueError('Target zeros need a separately justified log policy')
        cpm = paired_differences([math.log2(v / lib * 1e6 + .5) for v, lib in zip(raw, total)], header)
        mr = paired_differences([math.log2(v / sf) for v, sf in zip(raw, factors)], header)
        alternate = paired_differences([math.log2(v / lib * 1e6 + .5) for v, lib in zip(raw, named_total)], header)
        se = st.stdev(cpm) / math.sqrt(7);crit = float(t.ppf(.975, 6))
        r = {'gene': gene, 'pairs': 7, 'mean_delta_log2_CPM': st.mean(cpm),
             'CPM_geometric_ratio': 2 ** st.mean(cpm), 'CPM_change_percent': 100 * (2 ** st.mean(cpm) - 1),
             'CPM_CI_t_low': st.mean(cpm) - crit * se, 'CPM_CI_t_high': st.mean(cpm) + crit * se,
             'CPM_increasing_pairs': sum(x > 0 for x in cpm), 'CPM_decreasing_pairs': sum(x < 0 for x in cpm),
             'CPM_exploratory_signflip_p': signflip(cpm), 'mean_delta_log2_median_ratio': st.mean(mr),
             'median_ratio_change_percent': 100 * (2 ** st.mean(mr) - 1),
             'median_ratio_geometric_ratio': 2 ** st.mean(mr),
             'median_ratio_increasing_pairs': sum(x > 0 for x in mr),
             'median_ratio_decreasing_pairs': sum(x < 0 for x in mr),
             'median_ratio_exploratory_signflip_p': signflip(mr),
             'CPM_named_only_change_percent': 100 * (2 ** st.mean(alternate) - 1),
             'CPM_named_only_direction_agrees': (st.mean(cpm) > 0) == (st.mean(alternate) > 0)}
        output.append(r)
    return output, qc


def number(value):
    return None if value in ('', 'NA', 'NaN', 'nan') else float(value)


def overlaps(chrom, start, end, interval):
    return chrom == interval[0] and start <= interval[2] and end >= interval[1]


def dexseq(path):
    by_id = {v: k for k, v in GENES.items()};targets = [];nrows = missing = 0
    with gzip.open(path, 'rt', newline='') as f:
        reader = csv.DictReader(f);columns = reader.fieldnames
        for row in reader:
            nrows += 1;missing += row['symbol'] in ('', 'NA', 'NaN', 'nan')
            if row['groupID'] in by_id or row['symbol'] in GENES:
                if row['groupID'] not in by_id:
                    raise ValueError('Target symbol/ID discordance')
                targets.append(row)
    if len({r['fragment'] for r in targets}) != len(targets):
        raise ValueError('Duplicate target fragment')
    output, coverage = [], []
    for gid, gene in by_id.items():
        rs = [r for r in targets if r['groupID'] == gid]
        ps = [number(r['padj']) for r in rs];ps = [p for p in ps if p is not None]
        if any(not 0 <= p <= 1 for p in ps):
            raise ValueError('Invalid provided adjusted pvalue')
        output.append({'gene': gene, 'fragments': len(rs), 'provided_padj_evaluable': len(ps),
                       'provided_padj_missing': len(rs) - len(ps), 'provided_padj_below_0_05': sum(p < .05 for p in ps),
                       'provided_padj_below_0_10': sum(p < .1 for p in ps), 'min_provided_padj': min(ps) if ps else None})
        if gene in CE_DECLARED:
            interval = CE_DECLARED[gene]
            hit = [r for r in rs if overlaps(r['genomicData.seqnames'], int(r['genomicData.start']), int(r['genomicData.end']), interval)]
            distances = [(max(interval[1] - int(r['genomicData.end']), int(r['genomicData.start']) - interval[2], 0), r['fragment'])
                         for r in rs if r['genomicData.seqnames'] == interval[0]]
            distance, closest = min(distances)
            coverage.append({'gene': gene, 'declared_interval': interval, 'assembly': 'GRCh37/hg19',
                             'interval_independently_validated': False, 'overlapping_fragments': len(hit),
                             'nearest_fragment': closest, 'nearest_distance_bp': distance})
    return output, {'rows': nrows, 'columns': len(columns), 'missing_symbols': missing,
                    'target_fragments': len(targets), 'count_column_names_technical_only': [c for c in columns if c.startswith('countData.')],
                    'declared_CE_coverage': coverage, 'DEXSeq_model_refitted': False}


def write(path, records):
    with path.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(records[0]), delimiter='\t', lineterminator='\n');w.writeheader();w.writerows(records)


def run(cache, out):
    for name, pin in PINS.items():
        if sha(cache / name) != pin:
            raise ValueError('Public input hash mismatch: ' + name)
    out.mkdir(parents=True, exist_ok=True)
    expr, eq = expression(cache / 'GSE126542_NeuronalNuclei_RNAseq_counts.txt.gz')
    dex, dq = dexseq(cache / 'GSE121569_dexseq-all.csv.gz')
    write(out / 'expression_aggregate.tsv', expr);write(out / 'dexseq_aggregate.tsv', dex)
    (out / 'qc.json').write_text(json.dumps({'expression': eq, 'dexseq': dq,
        'per_case_or_sample_rows_exported': False, 'clinical_variables_used': False,
        'interpretation': 'Numerical aggregate reproduction, not independent replication or therapeutic inference'}, indent=2) + '\n')


if __name__ == '__main__':
    p = argparse.ArgumentParser();p.add_argument('--cache', type=Path, required=True)
    p.add_argument('--out', type=Path, default=Path('reports/issue14-reproduction'))
    args = p.parse_args();run(args.cache, args.out)
