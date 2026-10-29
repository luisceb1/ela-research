"""Pruebas offline (no constituyen validación científica)."""
import gzip
import unittest
from unittest.mock import patch

from scripts import geo_inventory, pubmed_watch

class FakeResponse:
    def __init__(self, raw):
        self.raw = raw
    def __enter__(self):
        return self
    def __exit__(self, *args):
        return False
    def read(self):
        return self.raw

class TestGeo(unittest.TestCase):
    def test_structure(self):
        raw = gzip.compress(b"transcript\tcontrol\ttreatment\nT1\t3\t4\nT2\t0\t8\n")
        with patch.object(geo_inventory.urllib.request, "urlopen", return_value=FakeResponse(raw)):
            obj = geo_inventory.inspect("FIXTURE", "https://example.invalid/file.gz")
        self.assertEqual(obj["n_rows"], 2)
        self.assertEqual(obj["n_columns"], 3)
        self.assertEqual(obj["observed_row_widths"], [3])

class TestPubmed(unittest.TestCase):
    def test_filters_non_pubmed_records(self):
        response = {"resultList":{"result":[
            {"source":"MED", "id":"1234", "title":"STMN2"},
            {"source":"PPR", "id":"PPR123", "title":"Unreviewed preprint"},
        ]}}
        with patch.object(pubmed_watch, "request_json", return_value=response) as call:
            records = pubmed_watch.search_pubmed("STMN2")
        self.assertEqual([r["id"] for r in records], ["1234"])
        self.assertIn("SRC%3AMED", call.call_args.args[0])

    def test_bad_response_rejected(self):
        with patch.object(pubmed_watch, "request_json", return_value={"resultList": {}}):
            with self.assertRaises(ValueError):
                pubmed_watch.search_pubmed("STMN2")

    def test_untrusted_title_sanitized(self):
        self.assertEqual(pubmed_watch.clean_title("<i>Gene</i> [important]"), "Gene \\[important\\]")
