import io
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from scripts import audit_author_catalog as a


def archive(entries):
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w') as z:
        for name, content in entries.items():
            z.writestr(name, content)
    return output.getvalue()


def row(strand='+'):
    return {'A': 'chr1', 'B': '100', 'C': '170', 'F': strand,
            'J': '2', 'K': '20,10', 'L': '0,60'}


class AuthorCatalogTests(unittest.TestCase):
    def test_body_reference_not_media_number_and_duplicates(self):
        raw = f'''<article xmlns:xlink="http://www.w3.org/1999/xlink">
          <article-id pub-id-type="doi">{a.DOI}</article-id>
          <article-id pub-id-type="pmcid">PMC12803201</article-id>
          <p id="P"><xref ref-type="supplementary-material" rid="SD8">Table S7</xref></p>
          <supplementary-material id="SD8"><media xlink:href="media-8.xlsx"/></supplementary-material>
          <supplementary-material id="alias"><media xlink:href="media-8.xlsx"/></supplementary-material>
        </article>'''.encode()
        _, result = a.source_map(raw)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['callouts'][0]['label'], 'Table S7')
        self.assertEqual(result[0]['ids'], ['SD8', 'alias'])
        with self.assertRaisesRegex(ValueError, 'Wrong primary'):
            a.source_map(raw.replace(a.DOI.encode(), b'wrong'))
        with self.assertRaisesRegex(ValueError, 'Unresolved'):
            a.source_map(raw.replace(b'rid="SD8"', b'rid="missing"'))

    def test_html_macro_and_expansion_rejected(self):
        with self.assertRaisesRegex(ValueError, 'possibly HTML'):
            a.office(b'<html>captcha</html>', 'xlsx')
        raw = archive({'xl/workbook.xml': '<workbook/>', 'xl/vbaProject.bin': b'code'})
        with self.assertRaisesRegex(ValueError, 'macro'):
            a.office(raw, 'xlsx')
        with patch.object(a, 'MAX_EXPANDED', 1):
            with self.assertRaisesRegex(ValueError, 'budget'):
                a.office(archive({'xl/workbook.xml': 'large'}), 'xlsx')

    def test_source_changes_fail_before_processing(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'source';p.write_bytes(b'original')
            record = {'bytes': 8, 'sha256': a.sha256(b'original')}
            self.assertEqual(a.pinned(p, record), b'original')
            p.write_bytes(b'changed!')
            with self.assertRaisesRegex(ValueError, 'mismatch'):
                a.pinned(p, record)

    def test_intronic_and_exonic_boundaries_on_both_strands(self):
        for strand in ['+', '-']:
            intronic, boundary = a.bed_junctions(row(strand))
            self.assertEqual(intronic, {('chr1', 121, 160, strand)})
            self.assertEqual(boundary, {('chr1', 120, 161, strand)})
            self.assertNotEqual(intronic, boundary)

    def test_concatenated_block_sizes_not_repaired(self):
        r = row();r['K'] = '2010'
        with self.assertRaisesRegex(ValueError, 'block_count_mismatch'):
            a.bed_junctions(r)
        r = row();r['L'] = '0,10'
        with self.assertRaises(ValueError):
            a.bed_junctions(r)

    def test_invalid_loci_and_adjacent_blocks(self):
        for key, value in [('B', '-1'), ('F', '.'), ('J', '0'), ('C', '100')]:
            r = row();r[key] = value
            with self.assertRaises(ValueError):
                a.bed_junctions(r)
        r = row();r.update({'C': '130', 'L': '0,20'})
        self.assertEqual(a.bed_junctions(r), (set(), set()))

    def test_intron_labels_not_silently_normalized(self):
        self.assertEqual(a.listed_introns('chr1:120-161(-)'), [('chr1', 120, 161, '-')])
        for bad in ['chr1:120-161', 'chr1:161-120(+)', 'chr1:120-161(+);garbage']:
            with self.assertRaises(ValueError):
                a.listed_introns(bad)

    def test_formula_metadata_is_marked_and_data_formula_rejected(self):
        cells = [('A2', 'formula', '999', '')]
        self.assertEqual(a.decode(cells, {}, allow_formula=True), {'A': '[formula not evaluated]'})
        with self.assertRaisesRegex(ValueError, 'Formula data'):
            a.decode(cells, {})

    def test_header_only_preserves_duplicate_positions_and_skips_data(self):
        ns = a.NS['m']
        raw = archive({
            'xl/workbook.xml': f'<workbook xmlns="{ns}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="S15" r:id="r1"/></sheets></workbook>',
            'xl/_rels/workbook.xml.rels': '<Relationships><Relationship Id="r1" Target="worksheets/sheet1.xml"/></Relationships>',
            'xl/worksheets/sheet1.xml': f'''<worksheet xmlns="{ns}"><sheetData>
              <row r="1"><c r="A1" t="s"><v>0</v></c></row>
              <row r="2"><c r="A2" t="s"><v>1</v></c><c r="B2" t="s"><v>1</v></c></row>
              <row r="3"><c r="A3"><f>DO_NOT_EXECUTE()</f><v>999</v></c></row>
              </sheetData></worksheet>''',
            'xl/sharedStrings.xml': f'<sst xmlns="{ns}"><si><t>S15 title</t></si><si><t>Transcript 1 Start</t></si><si><t>RESTRICTED FIXTURE</t></si></sst>'})
        result = a.headers(raw)
        self.assertEqual(result[0]['duplicate_headers'], ['Transcript 1 Start'])
        self.assertEqual(set(result[0]['headers_by_column']), {'A', 'B'})
        self.assertNotIn('RESTRICTED', str(result))

    def test_qc_separates_invalid_blocks_and_coordinate_conventions(self):
        ns = a.NS['m']
        good = row();good['N'] = 'chr1:120-161(+);chr1:121-160(+);chr1:122-160(+)'
        bad = row();bad['K'] = '2010'
        data = ''
        for number, values in [(3, good), (4, bad)]:
            data += '<row r="' + str(number) + '">'
            for col, value in values.items():
                data += f'<c r="{col}{number}" t="inlineStr"><is><t>{value}</t></is></c>'
            data += '</row>'
        raw = archive({
            'xl/workbook.xml': f'<workbook xmlns="{ns}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="S8A" r:id="r1"/></sheets></workbook>',
            'xl/_rels/workbook.xml.rels': '<Relationships><Relationship Id="r1" Target="worksheets/sheet1.xml"/></Relationships>',
            'xl/worksheets/sheet1.xml': f'<worksheet xmlns="{ns}"><sheetData>{data}</sheetData></worksheet>'})
        result = a.structural_qc(raw, ['S8A'], cryptic_column=True)[0]
        self.assertEqual(result['counts']['rows'], 2)
        self.assertEqual(result['counts']['invalid_block_rows'], 1)
        self.assertEqual(result['counts']['labels_match_exon_boundaries'], 1)
        self.assertEqual(result['counts']['labels_match_intronic_1based'], 1)
        self.assertEqual(result['counts']['labels_unexplained_by_blocks'], 1)
        with self.assertRaisesRegex(ValueError, 'allowlist'):
            a.structural_qc(raw, ['S15'], cryptic_column=True)


if __name__ == '__main__':
    unittest.main()
