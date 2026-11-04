"""Inspect only the experimental Supplementary Data3 design evidence for Fig3s."""
import argparse
import io
import json
from pathlib import Path
import re
import sys
import urllib.request
import zipfile

from audit_asadollahi_fig3s import NS, RID, digest, relation_path, xml_member

SOURCE_URL = ('https://static-content.springer.com/esm/art%3A10.1038%2Fs41588-025-02361-5/'
              'MediaObjects/41588_2025_2361_MOESM8_ESM.xlsx')
SOURCE_SHA256 = '7ba494959360e824eb333eeadb2e0fd1bb431a32859da92cabdd5a958cf1c2e7'
MAX_BYTES = 256 * 1024
COUNT_RE = re.compile(r'\s*\(n\s*=\s*(\d+)\)\s*\Z')
DESIGN_RE = re.compile(r'\bcultures?\b|\bbatch\b|\breplicates?\b|\bindependent\b|'
                       r'\b(?:neuron|cell)[ _-]?id\b|\bexclu', re.I)


def inspect_table(data, expected_sha=SOURCE_SHA256, include_published_means=False):
    if len(data) > MAX_BYTES or digest(data) != expected_sha:
        raise ValueError('source_size_or_sha256_mismatch')
    hashes = {}
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        if len(z.namelist()) != len(set(z.namelist())):
            raise ValueError('duplicate_zip_member')
        wb = xml_member(z, 'xl/workbook.xml', hashes)
        rels = {x.get('Id'): x for x in xml_member(z, 'xl/_rels/workbook.xml.rels', hashes)}
        sheets = wb.findall('s:sheets/s:sheet', NS)
        if len(sheets) != 1 or sheets[0].get('name') != 'Table 3':
            raise ValueError('unexpected_sheet_manifest')
        rel = rels[sheets[0].get(RID)]
        if rel.get('TargetMode') == 'External':
            raise ValueError('external_sheet_not_permitted')
        path = relation_path(rel.get('Target', ''))
        tree = xml_member(z, path, hashes)
        strings = [''.join(x.itertext()) for x in xml_member(z, 'xl/sharedStrings.xml', hashes)]
        cells = {}
        for c in tree.findall('s:sheetData/s:row/s:c', NS):
            addr = c.get('r')
            if addr in cells:
                raise ValueError('duplicate_cell_address')
            v = c.find('s:v', NS)
            if c.find('s:f', NS) is not None:
                raise ValueError('formula_not_evaluated')
            if v is not None:
                cells[addr] = strings[int(v.text)] if c.get('t') == 's' else v.text
            else:
                s = c.find('s:is', NS)
                if s is not None:
                    cells[addr] = ''.join(s.itertext())
        if 'Electrophysiological characterization' not in cells.get('A1', ''):
            raise ValueError('experimental_table_title_mismatch')
        expected = {'C18': 'UNC13AWT', 'E18': 'UNC13AR202H',
                    'B35': 'Charge (pC)', 'I35': '3s'}
        if any(cells.get(addr) != value for addr, value in expected.items()):
            raise ValueError('panel_unit_or_group_mismatch')
        counts = {}
        for addr, group in [('C36', 'UNC13AWT'), ('E36', 'UNC13AR202H')]:
            match = COUNT_RE.fullmatch(cells.get(addr, ''))
            if match is None:
                raise ValueError('observation_count_not_explicit')
            counts[group] = int(match[1])
        candidates = [{'source_cell': addr, 'text': value} for addr, value in cells.items()
                      if DESIGN_RE.search(value)]
        selected_fields = ['A1', *expected, 'C36', 'E36']
        if include_published_means:
            if not all(cells.get(a) for a in ('C35', 'E35')):
                raise ValueError('published_summary_missing')
            selected_fields += ['C35', 'E35']
        return {'source_url': SOURCE_URL, 'source_sha256': digest(data), 'source_bytes': len(data),
                'sheet': 'Table 3', 'selected_member': path, 'member_sha256': hashes,
                'selected_fields': {addr: cells.get(addr) for addr in selected_fields},
                'published_observation_counts': counts,
                'design_label_candidates': candidates,
                'defined_names_present': wb.find('s:definedNames', NS) is not None,
                'comment_members_present': any('comments' in n.lower() for n in z.namelist()),
                'culture_map_verified': False, 'culture_assignments': None,
                'exclusions_verified': False,
                'decision': 'MANUAL_REVIEW_DESIGN_LABELS' if candidates else 'NO_MAP_IN_INSPECTED_SUPPLEMENT',
                'effect_estimated': False, 'p_values_computed': False, 'p_values_exported': False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--download', action='store_true')
    a = p.parse_args()
    if a.download:
        with urllib.request.urlopen(SOURCE_URL, timeout=25) as r:
            data = r.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES or digest(data) != SOURCE_SHA256:
            raise ValueError('source_size_or_sha256_mismatch')
        a.source.parent.mkdir(parents=True, exist_ok=True)
        a.source.write_bytes(data)
    result = inspect_table(a.source.read_bytes())
    result['execution'] = {'python': sys.version, 'script_sha256': digest(Path(__file__).read_bytes()),
                           'parameters': {'max_bytes': MAX_BYTES, 'timeout_seconds': 25,
                                          'expected_source_sha256': SOURCE_SHA256}}
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'decision': result['decision'], 'counts': result['published_observation_counts']}))


if __name__ == '__main__':
    main()
