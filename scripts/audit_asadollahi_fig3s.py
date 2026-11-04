"""Read only the permitted experimental block of A25 source data.

No workbook edits, formula evaluation, inferential statistics or clinical files.
The source coordinates identify spreadsheet cells, never neurons or cultures.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation
import hashlib
import io
import json
from pathlib import Path
import platform
import posixpath
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from zoneinfo import ZoneInfo

SOURCE_URL = ('https://static-content.springer.com/esm/'
              'art%3A10.1038%2Fs41588-025-02361-5/MediaObjects/'
              '41588_2025_2361_MOESM10_ESM.xlsx')
SOURCE_SHA256 = '42f9a2266bf8e7dc157350fe588f1d87deb8d0e4c5067bc2c780b9fc7851a49f'
SHEET = 'Figure 3_R202H'
TITLE = 'Figure 3s: Initial EPSC Charge (pC)'
GROUPS = {'I': 'UNC13AWT', 'J': 'UNC13AR202H'}
MAX_BYTES = 2 * 1024 * 1024
MAX_MEMBER_BYTES = 20 * 1024 * 1024
MAX_ROWS = 1000
NS = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
RID = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
CELL_RE = re.compile(r'([A-Z]{1,3})([1-9][0-9]*)\Z')
FORBIDDEN_TEXT = re.compile(r'patient|participant|pedigree|date.of.birth|clinical', re.I)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def xml_member(z: zipfile.ZipFile, name: str, read_hashes: dict) -> ET.Element:
    info = z.getinfo(name)
    if info.file_size > MAX_MEMBER_BYTES:
        raise ValueError('member_size_limit_exceeded')
    raw = z.read(name)  # ZipFile also verifies this member's CRC.
    if b'<!DOCTYPE' in raw or b'<!ENTITY' in raw:
        raise ValueError('xml_entities_not_permitted')
    read_hashes[name] = digest(raw)
    return ET.fromstring(raw)


def relation_path(target: str) -> str:
    if ':' in target or target.startswith('/'):
        raise ValueError('nonlocal_sheet_target')
    resolved = posixpath.normpath(posixpath.join('xl', target))
    if not resolved.startswith('xl/worksheets/') or '..' in resolved.split('/'):
        raise ValueError('sheet_target_outside_worksheets')
    return resolved


def audit_bytes(data: bytes, expected_sha: str = SOURCE_SHA256) -> tuple[dict, list[dict]]:
    if len(data) > MAX_BYTES:
        raise ValueError('download_size_limit_exceeded')
    if digest(data) != expected_sha:
        raise ValueError('source_sha256_mismatch')
    read_hashes: dict[str, str] = {}
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        names = z.namelist()
        if len(names) != len(set(names)):
            raise ValueError('duplicate_zip_member')
        wb = xml_member(z, 'xl/workbook.xml', read_hashes)
        rels = xml_member(z, 'xl/_rels/workbook.xml.rels', read_hashes)
        relmap = {el.get('Id'): el for el in rels}
        sheets = wb.findall('s:sheets/s:sheet', NS)
        selected = [el for el in sheets if el.get('name') == SHEET]
        if len(selected) != 1:
            raise ValueError('selected_sheet_missing_or_ambiguous')
        rel = relmap[selected[0].get(RID)]
        if rel.get('TargetMode') == 'External':
            raise ValueError('external_sheet_not_permitted')
        member = relation_path(rel.get('Target', ''))
        tree = xml_member(z, member, read_hashes)
        cells = {}
        for cell in tree.findall('s:sheetData/s:row/s:c', NS):
            addr = cell.get('r', '')
            match = CELL_RE.fullmatch(addr)
            if not match or int(match[2]) > MAX_ROWS:
                raise ValueError('cell_address_outside_limit')
            if addr in cells:
                raise ValueError('duplicate_cell_address')
            cells[addr] = cell

        # Only resolve string indices used by this experimental sheet. Do not
        # import other sheets or interpret their values, formulas or pictures.
        needed = set()
        for cell in cells.values():
            if cell.get('t') == 's' and cell.find('s:v', NS) is not None:
                needed.add(int(cell.find('s:v', NS).text))
        strings = {}
        if needed:
            sst = xml_member(z, 'xl/sharedStrings.xml', read_hashes)
            for index, el in enumerate(sst):
                if index in needed:
                    strings[index] = ''.join(el.itertext())
            if needed != set(strings):
                raise ValueError('missing_shared_string')

        def text(cell):
            if cell is None:
                return None
            if cell.get('t') == 's':
                v = cell.find('s:v', NS)
                return strings[int(v.text)] if v is not None else None
            if cell.get('t') == 'inlineStr':
                el = cell.find('s:is', NS)
                return ''.join(el.itertext()) if el is not None else None
            return None

        text_fields = []
        for addr, cell in cells.items():
            val = text(cell)
            if val is not None:
                if FORBIDDEN_TEXT.search(val):
                    raise ValueError('scope_review_required_no_text_exported')
                text_fields.append({'source_cell': addr, 'text': val})
        if text(cells.get('I1')) != TITLE:
            raise ValueError('panel_or_unit_header_mismatch')
        for col, group in GROUPS.items():
            if text(cells.get(col + '3')) != group:
                raise ValueError('group_header_mismatch')

        row_numbers = [int(CELL_RE.fullmatch(a)[2]) for a in cells]
        last_row = max(row_numbers, default=3)
        records = []
        qc = {}
        for col, group in GROUPS.items():
            values = []
            populated_rows = []
            blanks = []
            invalid = []
            styles = Counter()
            for row in range(4, last_row + 1):
                addr = col + str(row)
                cell = cells.get(addr)
                v = cell.find('s:v', NS) if cell is not None else None
                if cell is not None and cell.find('s:f', NS) is not None:
                    invalid.append({'source_cell': addr, 'reason': 'formula_not_evaluated'})
                    continue
                if cell is None or (v is None and text(cell) is None):
                    blanks.append(addr)
                    continue
                if cell.get('t', 'n') != 'n':
                    invalid.append({'source_cell': addr, 'reason': 'nonnumeric_cell'})
                    continue
                try:
                    value = Decimal(v.text)
                    if not value.is_finite():
                        raise InvalidOperation
                except (InvalidOperation, TypeError):
                    invalid.append({'source_cell': addr, 'reason': 'invalid_numeric_value'})
                    continue
                populated_rows.append(row)
                styles[cell.get('s', '0')] += 1
                values.append(value)
                records.append({'source_sheet': SHEET, 'source_cell': addr,
                                'published_group': group, 'initial_epsc_charge_pC': v.text,
                                'neuron_id': None, 'culture_id': None})
            repeats = Counter(values)
            qc[group] = {'numeric_count': len(values), 'blank_cells': blanks,
                         'internal_blank_cells': [col + str(r) for r in range(4, max(populated_rows, default=3) + 1)
                                                  if r not in populated_rows],
                         'invalid_cells': invalid, 'zero_count': sum(v == 0 for v in values),
                         'negative_count': sum(v < 0 for v in values),
                         'repeated_numeric_values': sum(n - 1 for n in repeats.values()),
                         'styles': dict(styles)}

        invalid_count = sum(len(v['invalid_cells']) for v in qc.values())
        empty_group = any(v['numeric_count'] == 0 for v in qc.values())
        # The known published layout has measurement columns, no neuron/culture
        # fields. Row positions and identical style IDs are not biological keys.
        known_columns = {'A', 'B', 'E', 'F', 'I', 'J', 'M', 'N', 'Q', 'R'}
        outside = [a for a, c in cells.items()
                   if CELL_RE.fullmatch(a)[1] not in known_columns
                   and (c.find('s:v', NS) is not None or text(c) is not None)]
        metadata_labels = [v for v in text_fields if re.search(r'culture|batch|neuron.?id|cell.?id|exclu|replic|date|experiment', v['text'], re.I)]
        has_unknown_metadata = bool(outside or metadata_labels)
        result = {
            'source_url': SOURCE_URL, 'source_sha256': digest(data), 'source_bytes': len(data),
            'selected_sheet': SHEET, 'selected_member': member,
            'sheet_manifest': [{'name': s.get('name'), 'state': s.get('state', 'visible')} for s in sheets],
            'member_sha256': read_hashes, 'panel': '3s', 'measure': 'Initial EPSC Charge', 'unit': 'pC',
            'metadata_survey_text': text_fields, 'populated_cells_outside_known_measurement_columns': outside,
            'metadata_labels_requiring_review': metadata_labels,
            'defined_names_present': wb.find('s:definedNames', NS) is not None,
            'comment_members_present': any('comments' in n.lower() for n in names),
            'selected_sheet_external_relationship_file_present':
                posixpath.join(posixpath.dirname(member), '_rels', posixpath.basename(member) + '.rels') in names,
            'selected_sheet_table_parts': len(tree.findall('s:tableParts/s:tablePart', NS)),
            'numeric_qc': qc, 'total_numeric_values': len(records),
            'neuron_ids_verified': False, 'culture_map_verified': False, 'exclusions_verified': False,
            'culture_count': None,
            'decision': 'REVIEW_UNEXPECTED_METADATA' if has_unknown_metadata else
                        'NO_GO_NUMERIC_QC' if invalid_count or empty_group else 'PARTIAL_VALUES_AVAILABLE_NO_GO_INFERENCE',
            'reasons': ['culture_map_not_verified', 'neuron_ids_not_verified', 'exclusions_not_verified'],
            'effect_estimated': False, 'p_values_computed': False,
            'other_sheet_values_decoded': False,
        }
        return result, records


def retrieve(path: Path) -> dict:
    with urllib.request.urlopen(SOURCE_URL, timeout=25) as response:
        raw = response.read(MAX_BYTES + 1)
        receipt = {'url': SOURCE_URL, 'status': response.status,
                   'retrieved_at': datetime.now(ZoneInfo('Europe/Madrid')).isoformat(),
                   'declared_length': response.headers.get('Content-Length'),
                   'content_type': response.headers.get('Content-Type')}
    if len(raw) > MAX_BYTES:
        raise ValueError('download_size_limit_exceeded')
    if digest(raw) != SOURCE_SHA256:
        raise ValueError('source_sha256_mismatch')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    return receipt | {'bytes': len(raw), 'sha256': digest(raw)}


def write_projection(path: Path, records: list[dict]) -> None:
    # GitHub text writes preserve LF. Keep byte hashes stable across transports.
    with path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, lineterminator='\n', fieldnames=[
            'source_sheet', 'source_cell', 'published_group',
            'initial_epsc_charge_pC', 'neuron_id', 'culture_id'])
        writer.writeheader()
        writer.writerows(records)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--download', action='store_true')
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    execution = {'started_at': datetime.now(ZoneInfo('Europe/Madrid')).isoformat(),
                 'python': sys.version, 'platform': platform.platform(),
                 'script_sha256': digest(Path(__file__).read_bytes()),
                 'parameters': {'expected_sha256': SOURCE_SHA256, 'sheet': SHEET,
                                'header_cells': ['I1', 'I3', 'J3'], 'data_columns': ['I', 'J'],
                                'data_first_row': 4, 'max_source_bytes': MAX_BYTES,
                                'max_member_bytes': MAX_MEMBER_BYTES, 'max_rows': MAX_ROWS,
                                'download': args.download, 'random_seed': None}}
    try:
        if args.download:
            execution['retrieval'] = retrieve(args.source)
        if args.source.stat().st_size > MAX_BYTES:
            raise ValueError('download_size_limit_exceeded')
        result, records = audit_bytes(args.source.read_bytes())
        (args.output_dir / 'audit.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
        write_projection(args.output_dir / 'fig3s-projection.csv', records)
        execution['result'] = result['decision']
        execution['status'] = 'completed'
    except Exception as exc:
        execution.update(status='error', error_type=type(exc).__name__, error=str(exc))
    execution['finished_at'] = datetime.now(ZoneInfo('Europe/Madrid')).isoformat()
    (args.output_dir / 'execution.json').write_text(json.dumps(execution, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({k: execution[k] for k in ('status', 'result', 'error') if k in execution}))
    return 0 if execution['status'] == 'completed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
