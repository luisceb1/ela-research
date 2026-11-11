#!/usr/bin/env python3
"""Inspect the pinned public K26 Fig.4d workbook; never fit an effect or open the gate."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import posixpath
import xml.etree.ElementTree as ET
import zipfile

URL = ('https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-026-11256-2/'
       'MediaObjects/41586_2026_11256_MOESM7_ESM.xlsx')
EXPECTED_SHA256 = '7a01e468d3eaf89a2af9bd0c3fb16434f815e3020033df771d9872799cba3eb7'
NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
RID = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
CONDITIONS = {'B': 'TDP-43 KD', 'C': 'Control', 'D': 'TDP-43 KD +21-6'}


def inspect(path: Path) -> dict:
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError('Workbook differs from the inspected version; review before parsing')
    with zipfile.ZipFile(path) as archive:
        strings = []
        if 'xl/sharedStrings.xml' in archive.namelist():
            root = ET.fromstring(archive.read('xl/sharedStrings.xml'))
            strings = [''.join(node.itertext()) for node in root.findall('m:si', NS)]
        rels = {r.get('Id'): r.get('Target') for r in ET.fromstring(
            archive.read('xl/_rels/workbook.xml.rels'))}
        workbook = ET.fromstring(archive.read('xl/workbook.xml'))
        sheets = workbook.findall('m:sheets/m:sheet', NS)
        matches = [s for s in sheets if s.get('name') == '4d']
        if len(matches) != 1:
            raise ValueError('Expected one exact 4d worksheet')
        target = rels[matches[0].get(RID)]
        target = target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/' + target)
        root = ET.fromstring(archive.read(target))
        cells = {}
        for cell in root.findall('m:sheetData/m:row/m:c', NS):
            if cell.find('m:f', NS) is not None:
                raise ValueError('Unexpected formula in source panel')
            value = cell.find('m:v', NS)
            text = value.text if value is not None else ''
            if cell.get('t') == 's':
                text = strings[int(text)] if text else ''
            elif cell.get('t') == 'inlineStr':
                text = ''.join(cell.find('m:is', NS).itertext())
            if text:
                cells[cell.get('r')] = text
    for column, name in CONDITIONS.items():
        if cells.get(column + '3') != name:
            raise ValueError('Unexpected condition header')
    counts = Counter()
    batches = []
    batch = None
    for row in range(4, 45):
        if f'A{row}' in cells:
            batch = cells[f'A{row}']
            if batch not in ('Batch 1', 'Batch 2', 'Batch 3') or batch in batches:
                raise ValueError('Unexpected or repeated block label')
            batches.append(batch)
        for column, condition in CONDITIONS.items():
            value = cells.get(f'{column}{row}')
            if value is None:
                continue
            if batch is None:
                raise ValueError('Value before an explicit batch label')
            numeric = float(value)
            if not math.isfinite(numeric) or numeric < 0:
                raise ValueError('Nonfinite or negative panel value')
            counts[batch, condition] += 1
    if batches != ['Batch 1', 'Batch 2', 'Batch 3']:
        raise ValueError('Missing or reordered batch labels')
    totals = {condition: sum(counts[b, condition] for b in batches)
              for condition in CONDITIONS.values()}
    if totals != {'TDP-43 KD': 30, 'Control': 34, 'TDP-43 KD +21-6': 25}:
        raise ValueError('Counts differ from the published legend')
    return {
        'source_url': URL, 'source_sha256': digest, 'source_bytes': len(data),
        'sheet_names': [s.get('name') for s in sheets], 'panel': '4d',
        'title': cells.get('A1'), 'condition_headers': CONDITIONS,
        'counts_by_explicit_batch': {b: {c: counts[b, c] for c in CONDITIONS.values()}
                                     for b in batches},
        'total_by_condition': totals, 'total_numeric_observations': sum(totals.values()),
        'all_values_finite_and_nonnegative': True,
        'analysis_gate_opened': False, 'effect_estimated': False,
        'remaining_checks': [
            'Verify amplitude unit and sign/processing against the published axis and methods.',
            'Reconcile explicit Batch labels with the three independent differentiations in the legend.',
            'Review culture/coverslip/cell identity, repeated measurements, QC and exclusions.',
            'Inspect the actual R implementation and reconcile it with the existing prospective plan.'
        ]
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = inspect(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result['total_by_condition']))


if __name__ == '__main__':
    main()
