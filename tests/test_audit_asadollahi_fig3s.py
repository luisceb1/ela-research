"""Software-only fixtures; not biological replicates or experimental evidence."""
import hashlib
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
import zipfile

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'audit_asadollahi_fig3s.py'
spec = importlib.util.spec_from_file_location('audit_asadollahi_fig3s', SCRIPT)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def fixture(*, unit='pC', group='UNC13AR202H', value='2.5', formula=False,
            extra='', styles=False, outside_sheet=False):
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w') as z:
        z.writestr('xl/workbook.xml', '''<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Figure 3_R202H" sheetId="1" r:id="rId1"/><sheet name="Unselected" sheetId="2" r:id="rId2"/></sheets></workbook>''')
        z.writestr('xl/_rels/workbook.xml.rels', '''<Relationships><Relationship Id="rId1" Target="worksheets/sheet1.xml"/><Relationship Id="rId2" Target="worksheets/sheet2.xml"/></Relationships>''')
        f = '<f>1+1.5</f>' if formula else ''
        st = ' s="27"' if styles else ''
        z.writestr('xl/worksheets/sheet1.xml', f'''<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>
<row r="1"><c r="I1" t="inlineStr"><is><t>Figure 3s: Initial EPSC Charge ({unit})</t></is></c></row>
<row r="3"><c r="I3" t="inlineStr"><is><t>UNC13AWT</t></is></c><c r="J3" t="inlineStr"><is><t>{group}</t></is></c></row>
<row r="4"><c r="I4"><v>1.25</v></c><c r="J4"{st}>{f}<v>{value}</v></c></row>
<row r="5"><c r="I5"><v>0</v></c></row>{extra}</sheetData></worksheet>''')
        # A parser that imports all sheets would fail on this intentionally
        # invalid unselected member. Only the authorized sheet is readable.
        z.writestr('xl/worksheets/sheet2.xml', 'not XML' if outside_sheet else '<unused/>')
    return out.getvalue()


def run(data):
    return audit.audit_bytes(data, hashlib.sha256(data).hexdigest())


class SourceAuditTests(unittest.TestCase):
    def test_missing_culture_map_never_enables_inference(self):
        result, rows = run(fixture())
        self.assertEqual(result['decision'], 'PARTIAL_VALUES_AVAILABLE_NO_GO_INFERENCE')
        self.assertFalse(result['culture_map_verified'])
        self.assertFalse(result['effect_estimated'])
        self.assertTrue(all(r['culture_id'] is None and r['neuron_id'] is None for r in rows))

    def test_blank_is_not_imputed_and_zero_is_preserved(self):
        result, rows = run(fixture())
        self.assertEqual(len(rows), 3)
        self.assertEqual(result['numeric_qc']['UNC13AWT']['zero_count'], 1)
        self.assertEqual(result['numeric_qc']['UNC13AR202H']['blank_cells'], ['J5'])

    def test_unit_mismatch_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'panel_or_unit_header_mismatch'):
            run(fixture(unit='pA'))

    def test_group_mismatch_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'group_header_mismatch'):
            run(fixture(group='other'))

    def test_formula_cache_is_not_used_as_observation(self):
        result, rows = run(fixture(formula=True))
        self.assertEqual(result['decision'], 'NO_GO_NUMERIC_QC')
        self.assertEqual(len(rows), 2)
        self.assertEqual(result['numeric_qc']['UNC13AR202H']['invalid_cells'][0]['reason'], 'formula_not_evaluated')

    def test_nonfinite_is_rejected_and_recorded(self):
        result, rows = run(fixture(value='NaN'))
        self.assertEqual(result['decision'], 'NO_GO_NUMERIC_QC')
        self.assertEqual(len(rows), 2)

    def test_empty_group_does_not_claim_available_comparison(self):
        result, _ = run(fixture(value=''))
        self.assertEqual(result['decision'], 'NO_GO_NUMERIC_QC')
        self.assertEqual(result['numeric_qc']['UNC13AR202H']['numeric_count'], 0)

    def test_source_hash_is_checked_before_parsing(self):
        with self.assertRaisesRegex(ValueError, 'source_sha256_mismatch'):
            audit.audit_bytes(fixture())

    def test_unselected_sheet_is_not_parsed(self):
        result, _ = run(fixture(outside_sheet=True))
        self.assertFalse(result['other_sheet_values_decoded'])
        self.assertNotIn('xl/worksheets/sheet2.xml', result['member_sha256'])

    def test_styles_do_not_create_cultures(self):
        result, _ = run(fixture(styles=True))
        self.assertIsNone(result['culture_count'])
        self.assertFalse(result['culture_map_verified'])

    def test_scope_marker_prevents_export(self):
        extra = '<row r="6"><c r="U6" t="inlineStr"><is><t>clinical field</t></is></c></row>'
        with self.assertRaisesRegex(ValueError, 'scope_review_required_no_text_exported'):
            run(fixture(extra=extra))

    def test_duplicate_numeric_values_are_flagged_not_deleted(self):
        extra = '<row r="6"><c r="I6"><v>1.2500</v></c></row>'
        result, rows = run(fixture(extra=extra))
        self.assertEqual(result['numeric_qc']['UNC13AWT']['repeated_numeric_values'], 1)
        self.assertEqual(len(rows), 4)

    def test_extra_numeric_metadata_requires_review(self):
        extra = '<row r="6"><c r="U6"><v>3</v></c></row>'
        result, _ = run(fixture(extra=extra))
        self.assertEqual(result['decision'], 'REVIEW_UNEXPECTED_METADATA')

    def test_projection_byte_hash_survives_text_transport(self):
        _, rows = run(fixture())
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'projection.csv'
            audit.write_projection(path, rows)
            raw = path.read_bytes()
            self.assertNotIn(b'\r', raw)
            self.assertEqual(raw, path.read_text().encode('utf-8'))


if __name__ == '__main__':
    unittest.main()
