#!/usr/bin/env python3
"""Technical metadata only; dates/rep numbers never become biological unit IDs."""
import argparse
import csv
import gzip
import hashlib
import json
import zipfile
from collections import Counter
from pathlib import Path

CONDITIONS = {'siScr': 'scramble', 'siTDP43': 'TDP43', 'siRED': 'fluorescent', 'NoTx': 'none'}


def parse_soft(text):
    records = []
    for block in text.split('^SAMPLE = ')[1:]:
        lines = block.splitlines()
        gsm = lines[0].strip()
        def one(prefix):
            values = [line[len(prefix):].strip() for line in lines if line.startswith(prefix)]
            if len(values) != 1 or not values[0]:
                raise ValueError(f'{gsm}: missing/ambiguous {prefix}')
            return values[0]
        alias = one('!Sample_description = ')
        prefix = alias.rsplit('_', 1)[0]
        condition = one('!Sample_characteristics_ch1 = sirna type: ')
        if prefix not in CONDITIONS or CONDITIONS[prefix] != condition:
            raise ValueError(f'{gsm}: alias/condition mismatch')
        cell = one('!Sample_characteristics_ch1 = cell type: ')
        if cell != 'differentiated HUES3 into hMNs':
            raise ValueError('Only the whitelisted HUES3 culture model is allowed')
        records.append(dict(gsm=gsm, alias=alias, condition=condition, cell_model=cell,
                            deposited_date=one('!Sample_characteristics_ch1 = date: '),
                            experiment_id='unknown', differentiation_id='unknown',
                            well_id='unknown', sirna_reagent_id='unknown'))
    if not records:
        raise ValueError('No sample records')
    for key in ('gsm', 'alias'):
        if len({r[key] for r in records}) != len(records):
            raise ValueError(f'duplicate {key}')
    return records


def link_columns(records, header):
    columns = [h for h in header if h.startswith('countData.')]
    if not columns or len(set(columns)) != len(columns):
        raise ValueError('Missing/duplicate countData columns')
    lookup = {r['alias']: r for r in records}
    result = []
    for col in columns:
        alias = col.removeprefix('countData.')
        if alias not in lookup:
            raise ValueError(f'Unmatched column {col}')
        row = lookup[alias]
        if row['condition'] not in ('scramble', 'TDP43'):
            raise ValueError('Unexpected contrast condition')
        result.append(dict(column=col, **row))
    return result


def apply_published_batches(records, manifest):
    mapping = manifest['alias_to_published_batch']
    if set(mapping) != {r['alias'] for r in records}:
        raise ValueError('Published batch map must cover exactly all GEO aliases')
    if set(mapping.values()) != {'Batch 1', 'Batch 2'}:
        raise ValueError('Unexpected published batch labels')
    return [dict(r, published_batch=mapping[r['alias']],
                 experiment_id='published grouping: '+mapping[r['alias']],
                 differentiation_id='published grouping: '+mapping[r['alias']]) for r in records]


def audit(records, linked):
    cells = Counter((r['deposited_date'], r['condition']) for r in linked)
    dates = sorted({r['deposited_date'] for r in linked})
    crossed = all(cells[d, c] > 0 for d in dates for c in ('scramble', 'TDP43'))
    return dict(series_libraries=len(records), contrast_columns=len(linked),
                all_condition_counts=dict(Counter(r['condition'] for r in records)),
                contrast_date_condition=[dict(deposited_date=d, condition=c, libraries=cells[d,c])
                    for d in dates for c in ('scramble', 'TDP43')],
                condition_crossed_with_deposited_date=crossed,
                date_is_verified_experiment_id=False,
                published_batch_links=sum('published_batch' in r for r in linked),
                independent_MN_differentiation_experiments_reported=2,
                experiment_count_source='Klim2019 Fig1b legend; manual source audit, not computed from library count',
                published_batch_counts=dict(Counter(r.get('published_batch','unknown') for r in linked)),
                inferential_refit_allowed=False,
                reason='Published batch grouping recovered when manifest supplied, but well/reagent identity and original model formula unresolved. No automatic inferential refit; 12 libraries do not imply 12 independent differentiations.')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--soft', type=Path, required=True)
    p.add_argument('--dexseq', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--published-batches', type=Path)
    p.add_argument('--primary-cache', type=Path)
    a = p.parse_args()
    records = parse_soft(gzip.decompress(a.soft.read_bytes()).decode())
    if a.published_batches:
        manifest = json.loads(a.published_batches.read_text())
        if not a.primary_cache:
            raise ValueError('--primary-cache required to verify inspected figure member')
        with zipfile.ZipFile(a.primary_cache/'NIHMS1512656-supplement-1.docx') as z:
            member = z.read(manifest['member'])
        if hashlib.sha256(member).hexdigest() != manifest['member_sha256']:
            raise ValueError('Figure member hash mismatch')
        records = apply_published_batches(records, manifest)
    with gzip.open(a.dexseq, 'rt') as f:
        header = next(csv.reader(f))
    linked = link_columns(records, header)
    a.out.mkdir(parents=True, exist_ok=True)
    for name, rows in [('culture_libraries.tsv', records), ('dexseq_column_map.tsv', linked)]:
        with (a.out/name).open('w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter='\t'); w.writeheader(); w.writerows(rows)
    summary = audit(records, linked)
    (a.out/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    sources = []
    for path, url in [(a.soft, 'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE121nnn/GSE121569/soft/GSE121569_family.soft.gz'),
                      (a.dexseq, 'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE121nnn/GSE121569/suppl/GSE121569_dexseq-all.csv.gz')]:
        raw = path.read_bytes()
        sources.append(dict(url=url, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(), accessed='2026-10-29', attribution='GEO GSE121569 / Klim et al. 2019', license='No separate license independently verified; raw files not redistributed'))
    if a.primary_cache:
        for name in ['PMC7153761.1.xml', 'NIHMS1512656-supplement-1.docx', 'nihms-1512656-f0001.jpg']:
            raw = (a.primary_cache/name).read_bytes()
            sources.append(dict(url='https://pmc-oa-opendata.s3.amazonaws.com/PMC7153761.1/'+name,
                                bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(), accessed='2026-10-29',
                                attribution='Klim et al. Nat Neurosci 2019;22:167–179; PMC7153761 author manuscript',
                                license='Full source not redistributed; rights remain with original source'))
    (a.out/'sources.json').write_text(json.dumps(sources, indent=2)+'\n')
    print(json.dumps(summary, indent=2))

if __name__ == '__main__':
    main()
