#!/usr/bin/env python3
"""Exact-ID public GEO audit. Standard library; no statistical inference."""
import argparse
import csv
import gzip
import hashlib
import io
import json
import math
import platform
import re
import sys
import time
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/cache'
OUT = ROOT / 'reports/geo-audit'
SERIES = {'GSE310723': 'i3N', 'GSE315972': 'NYGC'}
TARGETS = {'STMN2': 'ENSG00000104435', 'UNC13A': 'ENSG00000130477'}


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def soft(text, prefix):
    obj = defaultdict(list)
    for line in text.splitlines():
        if line.startswith(prefix) and ' = ' in line:
            k, v = line.split(' = ', 1)
            obj[k].append(v)
    return dict(obj)


def fetch(url, path, manifest, refresh=False, project=None):
    """Cache only requested bytes or a permitted metadata projection; pin SHA."""
    key = path.name
    old = manifest.get(key)
    if path.exists() and not refresh:
        raw = path.read_bytes()
        expected = (old or {}).get('cache_sha256')
        if not expected or sha256(raw) != expected:
            raise ValueError(f'Unverified cache: {key}; use --refresh')
        return raw
    last = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'ELAResearchAudit/1.0'})
            with urllib.request.urlopen(req, timeout=40) as response:
                raw = response.read()
            if not raw:
                raise ValueError('Empty response')
            break
        except Exception as exc:
            last = exc
            if attempt == 2:
                raise
            time.sleep(attempt + 1)
    record = {'url': url, 'retrieved_utc': datetime.now(timezone.utc).isoformat(),
              'source_sha256': sha256(raw), 'source_bytes': len(raw)}
    cached = project(raw) if project else raw
    if old and old['source_sha256'] != record['source_sha256']:
        raise ValueError(f'Source changed for {key}; review hashes before replacing')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(cached)
    record['cache_sha256'] = sha256(cached)
    record['cache_bytes'] = len(cached)
    record['projection'] = 'technical_metadata_allowlist' if project else 'original'
    manifest[key] = record
    return cached


def technical_projection(raw):
    s = soft(raw.decode('utf-8-sig'), '!Sample_')
    allowed = ('!Sample_title', '!Sample_source_name_ch1', '!Sample_characteristics_ch1',
               '!Sample_data_processing', '!Sample_library_strategy',
               '!Sample_library_source', '!Sample_library_selection')
    # Exclude age, sex, clinical history, contact details and other unrequested fields.
    result = {k: v for k, v in s.items() if k in allowed}
    result['!Sample_characteristics_ch1'] = [v for v in result.get('!Sample_characteristics_ch1', [])
        if v.split(':', 1)[0].lower() in {'cell line', 'cell type', 'treatment', 'tissue', 'genotype', 'diagnosis'}]
    return json.dumps(result, sort_keys=True, ensure_ascii=False, indent=2).encode()


def download(manifest, refresh=False):
    def get(url, path, project=None):
        raw = fetch(url, path, manifest, refresh, project)
        dump_json(OUT / 'sources.json', manifest)
        return raw
    for gse, label in SERIES.items():
        url = f'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={gse}&targ=self&form=text&view=full'
        text = get(url, DATA / f'{gse}.soft').decode()
        s = soft(text, '!Series_')
        if s.get('!Series_geo_accession') != [gse]:
            raise ValueError(f'Unexpected GEO response for {gse}')
        gsms = s['!Series_sample_id']
        for gsm in gsms:
            url = f'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={gsm}&targ=self&form=text&view=full'
            get(url, DATA / f'{gsm}.technical.json', technical_projection)
        for suffix in ('uniqueCounts_transcript.txt.gz', 'counts_transcript.txt.gz', 'extended_annotations.gtf.gz'):
            name = f'{gse}_{label}_isoseq_{suffix}'
            links = [u.replace('ftp://', 'https://') for u in s['!Series_supplementary_file'] if u.endswith('/' + name)]
            if len(links) != 1:
                raise ValueError(f'Supplement missing or ambiguous: {name}')
            get(links[0], DATA / name)
        # Save incrementally so interrupted downloads can be resumed safely.
        dump_json(OUT / 'sources.json', manifest)


def attrs(text):
    values = re.findall(r'(\S+)\s+"([^"]*)"\s*;?', text)
    if not values:
        raise ValueError('Malformed GTF attributes')
    obj = {}
    for k, v in values:
        if k in obj and obj[k] != v and k not in {'tag', 'ont'}:
            raise ValueError(f'Conflicting GTF attribute {k}')
        obj[k] = v
    return obj


def gtf_index(path, include_exons=False):
    index, exons = {}, defaultdict(list)
    features, keys = Counter(), Counter()
    with gzip.open(path, 'rt') as f:
        for n, line in enumerate(f, 1):
            if not line.strip() or line.startswith('#'):
                continue
            row = line.rstrip('\n').split('\t')
            if len(row) != 9:
                raise ValueError(f'GTF row {n}: expected 9 fields')
            chrom, source, feature, start, end, score, strand, frame, attribute = row
            start, end = int(start), int(end)
            if start < 1 or end < start or strand not in ('+', '-', '.'):
                raise ValueError(f'Invalid GTF coordinates at {n}')
            a = attrs(attribute)
            features[feature] += 1
            keys.update(a.keys())
            tx, gene = a.get('transcript_id'), a.get('gene_id')
            if not tx:
                continue
            if not gene:
                raise ValueError(f'Transcript without gene at {n}')
            record = (gene, chrom, strand)
            if tx in index and index[tx] != record:
                raise ValueError(f'Conflicting GTF transcript identity: {tx}')
            index[tx] = record
            if include_exons and feature == 'exon' and gene.split('.')[0] in TARGETS.values():
                exons[tx].append((start, end))
    return index, dict(exons), dict(features), dict(keys)


def count_rows(path):
    with gzip.open(path, 'rt', newline='') as f:
        reader = csv.reader(f, delimiter='\t')
        header = next(reader)
        if header[:2] != ['TXNAME', 'GENEID'] or len(header) < 3 or len(set(header)) != len(header):
            raise ValueError('Unexpected or duplicate count columns')
        for n, row in enumerate(reader, 2):
            if len(row) != len(header):
                raise ValueError(f'Ragged row {n}')
            tx, gene = row[:2]
            if not tx or not gene:
                raise ValueError(f'Empty ID at row {n}')
            counts = [float(v) for v in row[2:]]
            if any(not math.isfinite(x) or x < 0 for x in counts):
                raise ValueError(f'Invalid count at row {n}')
            yield header, tx, gene, counts


def qc_counts(path, index):
    seen, genes, nonmapped, mismatched, targets = set(), set(), [], [], []
    totals = detected = noninteger = None
    for header, tx, gene, values in count_rows(path):
        if tx in seen:
            raise ValueError(f'Duplicate TXNAME: {tx}')
        seen.add(tx)
        genes.add(gene)
        if totals is None:
            totals = [0.] * len(values)
            detected, noninteger = [0] * len(values), [0] * len(values)
        for i, x in enumerate(values):
            totals[i] += x
            detected[i] += x > 0
            noninteger[i] += not x.is_integer()
        if tx not in index:
            nonmapped.append((tx, gene, 'missing_gtf_transcript'))
        elif gene != index[tx][0]:
            mismatched.append((tx, gene, index[tx][0]))
        if gene.split('.')[0] in TARGETS.values():
            targets.append((tx, gene, values))
    if not seen:
        raise ValueError('Empty count table')
    return {'rows': len(seen), 'genes': len(genes), 'columns': header,
            'assigned_counts': totals, 'detected_transcripts': detected,
            'noninteger_counts': noninteger, 'unmapped': nonmapped,
            'gene_mismatches': mismatched, 'gtf_not_in_counts': len(index.keys() - seen)}, targets


def compare_counts(unique, total):
    n, fractional = 0, 0
    it1, it2 = count_rows(unique), count_rows(total)
    import itertools
    for a, b in itertools.zip_longest(it1, it2):
        if a is None or b is None or a[:3] != b[:3]:
            raise ValueError('counts and uniqueCounts row identities/order differ')
        fractional += sum(not v.is_integer() for v in b[3])
        if any(u > c + 1e-8 for u, c in zip(a[3], b[3])):
            raise ValueError(f'uniqueCounts > counts for {a[1]}')
        n += 1
    return {'compared_rows': n, 'unique_le_counts': True, 'counts_fractional_cells': fractional}


def match_samples(gse, columns):
    s = soft((DATA / f'{gse}.soft').read_text(), '!Series_')
    rows = []
    for gsm in s['!Series_sample_id']:
        obj = json.loads((DATA / f'{gsm}.technical.json').read_text())
        title = obj['!Sample_title'][0]
        char = dict(v.split(': ', 1) for v in obj.get('!Sample_characteristics_ch1', []) if ': ' in v)
        if gse == 'GSE310723':
            treatment = char.get('treatment', '').lower()
            if treatment not in {'control', '5-azacytidine', 'tdp-43 crispri', '5-azacytidine & tdp-43 crispri'}:
                raise ValueError(f'Unrecognized treatment: {gsm}')
            kd = 'tdp-43' in treatment
            aza = '5-azacytidine' in treatment
            prefix = f'i3N_{"TDP43KD" if kd else "Ctrl"}_{"5Aza" if aza else "noAza"}_'
            candidates = [c for c in columns if c.startswith(prefix)]
            group = prefix[len('i3N_'):-1]
            model, unit = char.get('cell type', ''), 'one deposited culture library; independent culture replication not established'
            replicate = re.search(r'replicate (\d+)', title, re.I)
            if not replicate or replicate[1] != '1':
                raise ValueError(f'Unexpected replicate label: {gsm}')
        else:
            # Source-provided library identifier anchors the mapping; never fuzzy match.
            ident = re.search(r'CGND-HRA-(\d+)', title)
            if not ident:
                raise ValueError(f'Missing source library identifier: {gsm}')
            candidates = [c for c in columns if f'_{ident[1]}_' in c]
            group = candidates[0].split('_', 1)[0] if len(candidates) == 1 else ''
            # Validate published group against GSM, do not decode "ci" from name alone.
            diagnosis = char.get('diagnosis', '').upper()
            genotype = char.get('genotype', '').lower()
            if group.startswith('ALS') and 'ALS' not in diagnosis:
                raise ValueError(f'Group/diagnosis disagreement: {gsm}')
            if group == 'ALS-C9' and 'c9orf72+' not in genotype:
                raise ValueError(f'C9 group not verified: {gsm}')
            if group == 'ALS-ci' and 'COGNITIVE IMPAIRMENT' not in diagnosis:
                raise ValueError(f'CI group not verified: {gsm}')
            if group == 'ALS' and diagnosis != 'ALS':
                raise ValueError(f'ALS group not verified: {gsm}')
            if group == 'CTL' and diagnosis != 'CONTROL':
                raise ValueError(f'Control group not verified: {gsm}')
            if group != 'ALS-C9' and 'c9orf72-' not in genotype:
                raise ValueError(f'C9-negative group not verified: {gsm}')
            if group not in {'ALS', 'ALS-ci', 'ALS-C9', 'CTL'}:
                raise ValueError(f'Unexpected group: {gsm}')
            model, unit = char.get('tissue', ''), 'one donor library (series reports eight donor samples); group independence not re-established'
        if len(candidates) != 1:
            raise ValueError(f'Ambiguous/unmatched GSM {gsm}: {candidates}')
        rows.append({'gse': gse, 'gsm': gsm, 'column': candidates[0], 'group_label': group,
                     'model_or_tissue': model, 'technique': 'PacBio Iso-Seq / CrypTE-seq',
                     'unit': unit, 'libraries_in_group': 0,
                     'verified_independent_biological_replicates': 'not established' if gse == 'GSE310723' else '2 donors per published stratum; independence/covariates not audited',
                     'group_evidence': 'GSM treatment + title replicate 1' if gse == 'GSE310723' else 'GSM library identifier + published column label; ALS/C9 checked against GSM',
                     'metadata_url': f'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={gsm}'})
    if len({r['column'] for r in rows}) != len(columns) or len(rows) != len(columns):
        raise ValueError(f'Non-bijective GSM/column mapping for {gse}')
    groups = Counter(r['group_label'] for r in rows)
    for r in rows:
        r['libraries_in_group'] = groups[r['group_label']]
    return rows


def dump_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + '\n')


def tsv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--refresh', action='store_true')
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((OUT / 'sources.json').read_text()) if (OUT / 'sources.json').exists() else {}
    errors, summary, sample_rows, depth_rows, unmapped, mismatched = [], {}, [], [], [], []
    try:
        download(manifest, args.refresh)
        for gse, label in SERIES.items():
            prefix = DATA / f'{gse}_{label}_isoseq'
            gtf = Path(str(prefix) + '_extended_annotations.gtf.gz')
            index, _, features, keys = gtf_index(gtf)
            unique, counts = Path(str(prefix) + '_uniqueCounts_transcript.txt.gz'), Path(str(prefix) + '_counts_transcript.txt.gz')
            qc, _ = qc_counts(unique, index)
            sample_rows.extend(match_samples(gse, qc['columns'][2:]))
            for i, col in enumerate(qc['columns'][2:]):
                depth_rows.append({'gse': gse, 'column': col, 'assigned_unique_counts': qc['assigned_counts'][i],
                                   'detected_transcripts': qc['detected_transcripts'][i], 'fractional_unique_cells': qc['noninteger_counts'][i]})
            unmapped.extend({'gse': gse, 'txname': t, 'geneid': g, 'reason': why} for t, g, why in qc.pop('unmapped'))
            mismatched.extend({'gse': gse, 'txname': t, 'count_geneid': g, 'gtf_geneid': a} for t, g, a in qc.pop('gene_mismatches'))
            summary[gse] = {'uniqueCounts': qc, 'gtf_transcripts': len(index), 'gtf_features': features,
                            'gtf_attribute_counts': keys, 'comparison': compare_counts(unique, counts)}
            print(gse, json.dumps(summary[gse]), flush=True)
    except Exception as exc:
        errors.append({'type': type(exc).__name__, 'message': str(exc)})
    finally:
        dump_json(OUT / 'sources.json', manifest)
        dump_json(OUT / 'errors.json', errors)
        dump_json(OUT / 'qc.json', summary)
        dump_json(OUT / 'run.json', {'python': platform.python_version(), 'platform': platform.platform(),
                                  'utc': datetime.now(timezone.utc).isoformat(), 'argv': sys.argv,
                                  'randomness': 'none', 'inference': 'descriptive only',
                                  'status': 'failed' if errors else 'technical audit generated; review metadata caveats'})
        if sample_rows:
            tsv(OUT / 'samples.tsv', sample_rows, list(sample_rows[0]))
        tsv(OUT / 'depth.tsv', depth_rows, ['gse', 'column', 'assigned_unique_counts', 'detected_transcripts', 'fractional_unique_cells'])
        tsv(OUT / 'unmapped.tsv', unmapped, ['gse', 'txname', 'geneid', 'reason'])
        tsv(OUT / 'gene_mismatches.tsv', mismatched, ['gse', 'txname', 'count_geneid', 'gtf_geneid'])
    if errors:
        print(errors, file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
