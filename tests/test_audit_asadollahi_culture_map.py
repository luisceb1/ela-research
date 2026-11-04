"""Software fixtures, never biological data or additional experiments."""
import hashlib
import io
from pathlib import Path
import sys
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import audit_asadollahi_culture_map as audit


def fixture(*, unit='pC', panel='3s', count='(n =38)', extra=''):
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w') as z:
        z.writestr('xl/workbook.xml', '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Table 3" sheetId="2" r:id="rId1"/></sheets></workbook>')
        # A styles relationship first prevents erroneous positional selection.
        z.writestr('xl/_rels/workbook.xml.rels', '<Relationships><Relationship Id="rId3" Target="styles.xml"/><Relationship Id="rId1" Target="worksheets/sheet1.xml"/></Relationships>')
        z.writestr('xl/sharedStrings.xml', '<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"/>')
        values = {'A1': 'Electrophysiological characterization', 'C18': 'UNC13AWT',
                  'E18': 'UNC13AR202H', 'B35': f'Charge ({unit})', 'I35': panel,
                  'C36': count, 'E36': '(n =35)'}
        cells = ''.join(f'<row><c r="{addr}" t="inlineStr"><is><t>{v}</t></is></c></row>' for addr, v in values.items())
        z.writestr('xl/worksheets/sheet1.xml', '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>'+cells+extra+'</sheetData></worksheet>')
    return out.getvalue()


def inspect(data):
    return audit.inspect_table(data, hashlib.sha256(data).hexdigest())


class CultureMapTests(unittest.TestCase):
    def test_n_counts_are_not_culture_assignments(self):
        r = inspect(fixture())
        self.assertEqual(r['published_observation_counts'], {'UNC13AWT': 38, 'UNC13AR202H': 35})
        self.assertFalse(r['culture_map_verified'])
        self.assertIsNone(r['culture_assignments'])
        self.assertEqual(r['decision'], 'NO_MAP_IN_INSPECTED_SUPPLEMENT')

    def test_wrong_measure_or_panel_cannot_match_by_n_alone(self):
        for kw in ({'unit': 'nA'}, {'panel': '3u'}):
            with self.subTest(kw=kw), self.assertRaisesRegex(ValueError, 'panel_unit_or_group_mismatch'):
                inspect(fixture(**kw))

    def test_implicit_count_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'observation_count_not_explicit'):
            inspect(fixture(count='38'))

    def test_culture_label_requests_review_without_inventing_map(self):
        extra = '<row><c r="A190" t="inlineStr"><is><t>3 cultures</t></is></c></row>'
        r = inspect(fixture(extra=extra))
        self.assertEqual(r['decision'], 'MANUAL_REVIEW_DESIGN_LABELS')
        self.assertFalse(r['culture_map_verified'])

    def test_changed_source_is_rejected_before_parsing(self):
        with self.assertRaisesRegex(ValueError, 'source_size_or_sha256_mismatch'):
            audit.inspect_table(fixture())


if __name__ == '__main__':
    unittest.main()
