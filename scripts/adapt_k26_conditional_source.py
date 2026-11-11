#!/usr/bin/env python3
"""Exact-source adapter for the authorized nA, source-batch-only K26 replay."""
from __future__ import annotations
import argparse
from collections import Counter
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import posixpath
import re
import xml.etree.ElementTree as ET
import zipfile

SOURCE_SHA256 = '7a01e468d3eaf89a2af9bd0c3fb16434f815e3020033df771d9872799cba3eb7'
COUNTS = {'Control': 34, 'KD': 30, 'KD_ASO': 25}
HEADERS = {'B3': 'TDP-43 KD', 'C3': 'Control', 'D3': 'TDP-43 KD +21-6'}
CONDITIONS = {'B': 'KD', 'C': 'Control', 'D': 'KD_ASO'}
BATCHES = ['Batch 1', 'Batch 2', 'Batch 3']
FIELDS = ['source_cell', 'source_batch', 'condition', 'value_nA', 'source_numeric_text']
NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


def check_contract(contract):
    if (contract.get('schema_version') != 'FR-K26-4d-conditional-v2' or
        contract.get('enabled_for_conditional_replay') is not True or
        contract.get('strict_v1_gate_passed') is not False or
        contract.get('unit') != 'nA_magnitude' or contract.get('source_sha256') != SOURCE_SHA256 or
        contract.get('expected_counts') != COUNTS or contract.get('source_batch_labels') != BATCHES):
        raise ValueError('Conditional contract mismatch; no unit conversion or strict-gate substitution allowed')


def pinned_cells(blob):
    if hashlib.sha256(blob).hexdigest() != SOURCE_SHA256:
        raise ValueError('Changed source SHA256; review instead of adapting silently')
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            strings = [''.join(s.itertext()) for s in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si', NS)]
        rels = {x.get('Id'): x.get('Target') for x in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        sheets = ET.fromstring(z.read('xl/workbook.xml')).findall('m:sheets/m:sheet', NS)
        selected = [s for s in sheets if s.get('name') == '4d']
        if len(selected) != 1:
            raise ValueError('Exactly one 4d sheet required')
        rid = selected[0].get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
        target = rels[rid]
        target = target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/' + target)
        root = ET.fromstring(z.read(target)); cells = {}
        for node in root.findall('m:sheetData/m:row/m:c', NS):
            if node.find('m:f', NS) is not None:
                raise ValueError('Unexpected formula in panel')
            address = node.get('r')
            if address in cells:
                raise ValueError('Duplicate source-cell coordinate')
            value = node.find('m:v', NS); value = value.text if value is not None else ''
            if node.get('t') == 's':
                value = strings[int(value)] if value else ''
            elif node.get('t') == 'inlineStr':
                value = ''.join(node.find('m:is', NS).itertext())
            if value:
                cells[address] = value
        return cells


def observations(cells, expected_counts=None):
    """Source coordinates are observation keys, never invented biological IDs."""
    expected_counts = COUNTS if expected_counts is None else expected_counts
    if any(cells.get(address) != text for address, text in HEADERS.items()):
        raise ValueError('Panel condition/header mismatch')
    if not cells.get('A1', '').startswith('Figure 4d, Measurement of evoked EPSCs in spinal motor neuron'):
        raise ValueError('Panel title mismatch')
    rows = []; batch = None; seen_batches = []
    for row in range(4, 45):
        if cells.get(f'A{row}'):
            batch = cells[f'A{row}']
            if batch not in BATCHES or batch in seen_batches:
                raise ValueError('Unexpected or repeated batch label')
            seen_batches.append(batch)
        for col, condition in CONDITIONS.items():
            raw = cells.get(f'{col}{row}')
            if raw is None or raw == '':
                continue
            if batch is None:
                raise ValueError('Numeric entry without declared batch')
            value = float(raw)
            if not math.isfinite(value) or value < 0:
                raise ValueError('Nonfinite/negative source magnitude; do not take abs')
            rows.append({'source_cell': f'4d!{col}{row}', 'source_batch': batch,
                         'condition': condition, 'value_nA': repr(value), 'source_numeric_text': raw})
    if seen_batches != BATCHES:
        raise ValueError('Missing or reordered source blocks')
    if Counter(r['condition'] for r in rows) != Counter(expected_counts):
        raise ValueError('Unexpected included counts')
    for batch in BATCHES:
        if {r['condition'] for r in rows if r['source_batch'] == batch} != set(COUNTS):
            raise ValueError('Incomplete condition block')
    unexpected = [k for k in cells if re.fullmatch(r'[BCD]\d+', k) and int(k[1:]) > 44]
    if unexpected:
        raise ValueError('Unexpected extra data rows')
    return rows


def run(source, contract_path, output_dir, plan_commit):
    if not re.fullmatch(r'[0-9a-f]{40}', plan_commit):
        raise ValueError('A committed plan SHA is required')
    contract_blob = Path(contract_path).read_bytes(); contract = json.loads(contract_blob)
    check_contract(contract)
    blob = Path(source).read_bytes(); rows = observations(pinned_cells(blob))
    output_dir = Path(output_dir); output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / 'observations.csv'
    if output.resolve() == Path(source).resolve():
        raise ValueError('Source must not be overwritten')
    with output.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator='\n')
        writer.writeheader(); writer.writerows(rows)
    receipt = {'plan_commit': plan_commit, 'source_sha256': SOURCE_SHA256,
               'contract_sha256': hashlib.sha256(contract_blob).hexdigest(),
               'csv_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
               'n_observations': len(rows), 'unit': 'nA_magnitude', 'scale_factor_applied': 1,
               'batch_labels': BATCHES, 'strict_v1_gate_passed': False,
               'observation_key_meaning': 'Original worksheet cell coordinate; not a verified biological cell ID'}
    (output_dir / 'adapter_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--contract', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--plan-commit', required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.contract, args.output_dir, args.plan_commit), sort_keys=True))

if __name__ == '__main__':
    main()
