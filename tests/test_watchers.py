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

class TestQueryScope(unittest.TestCase):
    """La consulta de lecturas largas debe acotar campos, no buscar en referencias."""

    def test_long_reads_query_is_field_restricted(self):
        query = pubmed_watch.QUERIES["long_reads"]
        self.assertIn("TITLE_ABS:", query)
        # Ningún término suelto sin campo: cada comilla de término va precedida de TITLE_ABS.
        self.assertNotRegex(query, r'(?<!TITLE_ABS:)"amyotrophic lateral sclerosis"')
        # 'isoform' genérico fue la causa del ruido; solo se admite acotado.
        self.assertNotIn("OR isoform)", query)

    def test_every_query_keeps_a_disease_or_gene_anchor(self):
        anchors = ("TDP-43", "TARDBP", "amyotrophic lateral sclerosis",
                   "frontotemporal dementia", "STMN2", "UNC13A")
        for name, query in pubmed_watch.QUERIES.items():
            with self.subTest(query=name):
                self.assertTrue(any(a in query for a in anchors))

class TestTrackedPreprints(unittest.TestCase):
    """El seguimiento de versiones revisadas por pares no valida nada por si solo."""

    def test_every_tracked_preprint_is_in_the_timing_matrix(self):
        self.assertEqual(len(pubmed_watch.TRACKED_PREPRINTS), 6)
        for label, title in pubmed_watch.TRACKED_PREPRINTS.items():
            with self.subTest(label=label):
                self.assertNotIn('"', title)
                self.assertGreater(len(title), 20)

    def test_reports_hits_per_label(self):
        record = {"source": "MED", "id": "999", "title": "T",
                  "journalTitle": "J", "firstPublicationDate": "2026-01-01"}
        with patch.object(pubmed_watch, "search_pubmed", return_value=[record]):
            found = pubmed_watch.check_published_versions()
        self.assertEqual(len(found), len(pubmed_watch.TRACKED_PREPRINTS))
        first = next(iter(found.values()))
        self.assertEqual(first[0]["pmid"], "999")

    def test_no_hits_yields_empty_mapping(self):
        with patch.object(pubmed_watch, "search_pubmed", return_value=[]):
            self.assertEqual(pubmed_watch.check_published_versions(), {})
