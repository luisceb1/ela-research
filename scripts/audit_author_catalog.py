#!/usr/bin/env python3
"""Pinned primary-source supplement map and structural QC; no efficacy inference."""
import argparse
import collections
import hashlib
import io
import json
import posixpath
import re
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
REL = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
XLINK = '{http://www.w3.org/1999/xlink}href'
DOI = '10.64898/2026.01.09.698641'
MAX_EXPANDED = 350_000_000
INTRON = re.compile(r'([^:;]+):(\d+)-(\d+)\(([+-])\)')


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def pinned(path, record):
    raw = Path(path).read_bytes()
    if len(raw) != record['bytes'] or sha256(raw) != record['sha256']:
        raise ValueError('Source SHA256/size mismatch: ' + Path(path).name)
    if record.get('md5') and hashlib.md5(raw).hexdigest() != record['md5']:
        raise ValueError('Source MD5 mismatch')
    return raw


def fetch_selected(cache, xml_path):
    """Fetch only five explicitly pinned Office files and primary article XML."""
    manifest = json.loads((ROOT / 'research/references/bolger_author_catalog_v1.json').read_text())
    selected = set(manifest['files'])
    if selected != {'media-1.docx', 'media-6.xlsx', 'media-8.xlsx', 'media-9.xlsx', 'media-16.xlsx'}:
        raise ValueError('Download allowlist changed; review scope')
    records = [(xml_path, manifest['xml'])] + [(cache / n, manifest['files'][n]) for n in sorted(selected)]
    for path, record in records:
        if path.exists():
            pinned(path, record)
            continue
        with urllib.request.urlopen(record['url'], timeout=60) as response:
            raw = response.read(record['bytes'] + 1)
        if len(raw) != record['bytes'] or sha256(raw) != record['sha256']:
            raise ValueError('Download identity mismatch: ' + path.name)
        if record.get('md5') and hashlib.md5(raw).hexdigest() != record['md5']:
            raise ValueError('Download MD5 mismatch')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)


def source_map(raw):
    root = ET.fromstring(raw)
    ids = {e.get('pub-id-type'): e.text for e in root.findall('.//article-id')}
    if ids.get('doi') != DOI or ids.get('pmcid') != 'PMC12803201':
        raise ValueError('Wrong primary article')
    media, by_id = {}, {}
    for s in root.iter('supplementary-material'):
        for link in s.iter('media'):
            href = link.get(XLINK, '')
            if not re.fullmatch(r'media-\d+\.(docx|xlsx)', href):
                raise ValueError('Unexpected supplementary path')
            obj = media.setdefault(href, {'file': href, 'ids': [], 'callouts': []})
            if s.get('id'):
                if s.get('id') in by_id and by_id[s.get('id')] != href:
                    raise ValueError('Conflicting supplementary ID')
                by_id[s.get('id')] = href
                if s.get('id') not in obj['ids']:
                    obj['ids'].append(s.get('id'))
    for p in root.iter('p'):
        for x in p.findall('.//xref[@ref-type="supplementary-material"]'):
            rid = x.get('rid')
            if rid not in by_id:
                raise ValueError('Unresolved supplementary reference')
            media[by_id[rid]]['callouts'].append({
                'paragraph': p.get('id'), 'rid': rid,
                'label': ' '.join(''.join(x.itertext()).split())})
    return root, list(media.values())


def office(raw, kind):
    if not raw.startswith(b'PK'):
        raise ValueError('Not an Office ZIP (possibly HTML)')
    z = zipfile.ZipFile(io.BytesIO(raw))
    names = z.namelist()
    if len(names) != len(set(names)):
        z.close()
        raise ValueError('Duplicate Office members')
    if sum(e.file_size for e in z.infolist()) > MAX_EXPANDED:
        z.close()
        raise ValueError('Office expansion budget exceeded')
    if any(n.startswith('/') or '..' in n.split('/') for n in names):
        z.close()
        raise ValueError('Unsafe Office member path')
    required = 'word/document.xml' if kind == 'docx' else 'xl/workbook.xml'
    if required not in names or any('vbaProject' in n for n in names):
        z.close()
        raise ValueError('Wrong Office type or macro content')
    return z


def legend_ids(raw):
    with office(raw, 'docx') as z:
        root = ET.fromstring(z.read('word/document.xml'))
    result = []
    for p in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
        text = ''.join(p.itertext())
        m = re.match(r'Supplemental table (S\d+[A-Z]?)\.', text)
        if m:
            if m[1] in result:
                raise ValueError('Duplicate table legend')
            result.append(m[1])
    if not result:
        raise ValueError('No table legends')
    return result


def sheets(z):
    wb = ET.fromstring(z.read('xl/workbook.xml'))
    rels = {r.get('Id'): r for r in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
    result = []
    for s in wb.find('m:sheets', NS):
        rel = rels[s.get(REL)]
        if rel.get('TargetMode') == 'External':
            raise ValueError('External worksheet not supported')
        target = rel.get('Target', '')
        path = target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/' + target)
        if not path.startswith('xl/worksheets/') or path not in z.namelist():
            raise ValueError('Unsafe worksheet target')
        result.append((s.get('name'), path))
    return result


def raw_rows(z, path, limit=None):
    with z.open(path) as f:
        context = ET.iterparse(f, events=('start', 'end'))
        _, root = next(context)
        count = 0
        for event, row in context:
            if event == 'end' and row.tag == '{' + NS['m'] + '}row':
                cells = []
                for c in row.findall('m:c', NS):
                    formula = c.find('m:f', NS) is not None
                    cells.append((c.get('r'), 'formula' if formula else c.get('t'),
                                  c.findtext('m:v', default='', namespaces=NS),
                                  ''.join(t.text or '' for t in c.findall('.//m:t', NS))))
                yield int(row.get('r')), cells
                count += 1
                row.clear()
                root.clear()
                if limit is not None and count >= limit:
                    break


def shared_strings(z, wanted=None):
    result = {}
    if 'xl/sharedStrings.xml' not in z.namelist():
        return result
    with z.open('xl/sharedStrings.xml') as f:
        context = ET.iterparse(f, events=('start', 'end'))
        _, root = next(context)
        i = 0
        for event, e in context:
            if event == 'end' and e.tag == '{' + NS['m'] + '}si':
                if wanted is None or i in wanted:
                    result[i] = ''.join(t.text or '' for t in e.findall('.//m:t', NS))
                i += 1
                root.clear()
                if wanted is not None and len(result) == len(wanted):
                    break
    if wanted is not None and set(result) != wanted:
        raise ValueError('Unresolved shared string')
    return result


def decode(cells, strings, allow_formula=False):
    values = {}
    for address, kind, value, inline in cells:
        col = re.fullmatch(r'([A-Z]+)\d+', address)
        if col is None or col[1] in values:
            raise ValueError('Invalid/duplicate cell address')
        if kind == 'formula':
            if not allow_formula:
                raise ValueError('Formula data cell not supported')
            values[col[1]] = '[formula not evaluated]'
        else:
            values[col[1]] = strings[int(value)] if kind == 's' else inline if kind == 'inlineStr' else value
    return values


def headers(raw):
    """Only two header/title rows; never decode subject-level data rows."""
    with office(raw, 'xlsx') as z:
        starts = [(name, list(raw_rows(z, path, limit=2))) for name, path in sheets(z)]
        wanted = {int(v) for _, rows in starts for _, cells in rows for _, t, v, _ in cells if t == 's'}
        strings = shared_strings(z, wanted)
        result = []
        for name, rows in starts:
            if [r for r, _ in rows] != [1, 2]:
                raise ValueError('Expected title row1/header row2')
            title = decode(rows[0][1], strings, allow_formula=True).get('A', '')
            fields = decode(rows[1][1], strings, allow_formula=True)
            duplicates = sorted(k for k, n in collections.Counter(fields.values()).items()
                                if k and n > 1 and k != '[formula not evaluated]')
            title_id = next(iter(re.findall(r'S\d+[A-Z]?', title)), None)
            result.append({'sheet': name, 'title_table_id': title_id,
                           'title_disagrees_with_sheet': title_id != name,
                           'headers_by_column': fields, 'duplicate_headers': duplicates,
                           'formula_header_cells_not_evaluated': [address for _, cells in rows
                                                                  for address, kind, _, _ in cells if kind == 'formula']})
        return result


def integer(value):
    if not re.fullmatch(r'\d+', value):
        raise ValueError('noninteger')
    return int(value)


def bed_junctions(row):
    """Validate BED-like blocks first; return intronic1-based/exon-boundary keys."""
    start, end, n = integer(row.get('B', '')), integer(row.get('C', '')), integer(row.get('J', ''))
    if end <= start or n < 1 or row.get('F') not in ('+', '-') or not row.get('A'):
        raise ValueError('locus_or_span')
    lengths = [integer(x) for x in row.get('K', '').rstrip(',').split(',')]
    offsets = [integer(x) for x in row.get('L', '').rstrip(',').split(',')]
    if len(lengths) != n or len(offsets) != n:
        raise ValueError('block_count_mismatch')
    if offsets[0] != 0 or offsets[-1] + lengths[-1] != end - start:
        raise ValueError('block_span_mismatch')
    if any(x < 1 for x in lengths):
        raise ValueError('nonpositive_block')
    exons = [(start + o, start + o + length) for o, length in zip(offsets, lengths)]
    if any(a[1] > b[0] for a, b in zip(exons, exons[1:])):
        raise ValueError('overlapping_or_unsorted_blocks')
    intronic, boundary = set(), set()
    for a, b in zip(exons, exons[1:]):
        if a[1] == b[0]:
            continue
        intronic.add((row['A'], a[1] + 1, b[0], row['F']))
        boundary.add((row['A'], a[1], b[0] + 1, row['F']))
    return intronic, boundary


def listed_introns(value):
    parts = value.split(';')
    result = []
    for part in parts:
        m = INTRON.fullmatch(part.strip())
        if not m or int(m[2]) >= int(m[3]):
            raise ValueError('invalid_listed_intron')
        result.append((m[1], int(m[2]), int(m[3]), m[4]))
    return result


def structural_qc(raw, allowed_sheets, cryptic_column=False):
    """Only allowlisted culture sheets; no patient/phenotype analysis."""
    result = []
    with office(raw, 'xlsx') as z:
        spec = sheets(z)
        if {x[0] for x in spec} != set(allowed_sheets):
            raise ValueError('Sheet allowlist mismatch')
        strings = shared_strings(z)
        for name, path in spec:
            counts = collections.Counter()
            reasons = collections.Counter()
            examples = []
            for row_number, cells in raw_rows(z, path):
                if row_number <= 2:
                    continue
                row = decode(cells, strings)
                if not any(row.values()):
                    continue
                counts['rows'] += 1
                try:
                    intronic, boundary = bed_junctions(row)
                except ValueError as e:
                    counts['invalid_block_rows'] += 1
                    reasons[str(e)] += 1
                    if len(examples) < 5:
                        examples.append({'sheet_row': row_number, 'reason': str(e)})
                    continue
                counts['valid_block_rows'] += 1
                counts['valid_without_intron_rows' if not intronic else 'valid_spliced_rows'] += 1
                if cryptic_column:
                    try:
                        entries = listed_introns(row.get('N', ''))
                    except ValueError:
                        counts['invalid_intron_label_rows'] += 1
                        continue
                    for key in entries:
                        counts['listed_intron_labels'] += 1
                        if key in boundary:
                            counts['labels_match_exon_boundaries'] += 1
                        elif key in intronic:
                            counts['labels_match_intronic_1based'] += 1
                        else:
                            counts['labels_unexplained_by_blocks'] += 1
            result.append({'sheet': name, 'counts': dict(counts), 'invalid_reasons': dict(reasons),
                           'invalid_row_examples': examples, 'invalid_rows_repaired': False})
    return result


def run(cache, xml_path, output):
    manifest = json.loads((ROOT / 'research/references/bolger_author_catalog_v1.json').read_text())
    xml = pinned(xml_path, manifest['xml'])
    _, media = source_map(xml)
    for x in media:
        x.update(manifest['policy'][x['file']])
    legend = legend_ids(pinned(cache / 'media-1.docx', manifest['files']['media-1.docx']))
    schema = {}
    for name in ('media-6.xlsx', 'media-8.xlsx', 'media-9.xlsx', 'media-16.xlsx'):
        schema[name] = headers(pinned(cache / name, manifest['files'][name]))
    qc = {}
    for name, prefix, cryptic in [('media-8.xlsx', 'S7', False), ('media-9.xlsx', 'S8', True)]:
        qc[name] = structural_qc(pinned(cache / name, manifest['files'][name]),
                                 [prefix + s for s in 'ABCD'], cryptic)
    result = {'supplements': media, 'legend_table_ids': legend, 'schemas': schema,
              'culture_structure_qc': qc, 'author_catalog_matched': False,
              'clinical_table_S12_downloaded': False, 'patient_rows_exported': False,
              'assembly_reported': 'hg38', 'assembly_source_paragraphs': ['P51', 'P52'],
              'comparison_unit_source': 'P54', 'comparison_unit': 'gene plus identical TE copy; category-specific gene collapsing',
              'not_an_exact_junction_intersection': True,
              'scope': 'source/schema/structural QC; no novelty or biological inference'}
    output.mkdir(parents=True, exist_ok=True)
    (output / 'audit.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cache', type=Path, required=True)
    p.add_argument('--xml', type=Path, required=True)
    p.add_argument('--fetch', action='store_true', help='Retrieve only the pinned allowlist; never clinical S12')
    p.add_argument('--out', type=Path, default=ROOT / 'reports/author-catalog-schema')
    a = p.parse_args()
    if a.fetch:
        fetch_selected(a.cache, a.xml)
    run(a.cache, a.xml, a.out)
