"""Pruebas offline, no validación científica."""
import gzip
import unittest
from unittest.mock import patch

from scripts import geo_inventory, pubmed_watch

class Response:
    def __init__(self, data):
        self.data = data
    def __enter__(self):
        return self
    def __exit__(self, *args):
        return False
    def read(self):
        return self.data

class TestGeo(unittest.TestCase):
    def test_structure(self):
        payload = gzip.compress(b"transcript\tcontrol\ttreatment\nT1\t3\t4\nT2\t0\t8\n")
        with patch.object(geo_inventory.urllib.request, "urlopen", return_value=Response(payload)):
            data = geo_inventory.inspect("TEST", "https://example.invalid/mock.gz")
        self.assertEqual(data["n_rows"], 2)
        self.assertEqual(data["n_columns"], 3)
        self.assertEqual(data["observed_row_widths"], [3])

class TestPubmed(unittest.TestCase):
    def test_queries(self):
        self.assertIn("STMN2_UNC13A", pubmed_watch.QUERIES)
        self.assertIn("cryptic_splicing", pubmed_watch.QUERIES)
        self.assertTrue(all("[All Fields]" in query for query in pubmed_watch.QUERIES.values()))
