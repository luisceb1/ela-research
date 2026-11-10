"""Offline benchmark controls. Models and network calls are mocked."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from agent_lab.benchmark import (
    BenchmarkError, check_pubmed_sources, load_benchmark, score_predictions,
)
from agent_lab.sources import Paper


class TestUNC13ABenchmark(unittest.TestCase):
    def setUp(self):
        self.benchmark = load_benchmark()

    def test_fixed_scope_and_distribution(self):
        self.assertEqual(len(self.benchmark["cases"]), 20)
        self.assertEqual(len(self.benchmark["sources"]), 8)
        self.assertEqual(len({s["pmid"] for s in self.benchmark["sources"]}), 8)
        labels = [case["expected"] for case in self.benchmark["cases"]]
        self.assertEqual(labels.count("supported"), 13)
        self.assertEqual(labels.count("insufficient"), 6)
        self.assertEqual(labels.count("contradicted"), 1)

    def _modified_fixture(self, callback):
        result = copy.deepcopy(self.benchmark)
        callback(result)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.json"
            path.write_text(json.dumps(result), encoding="utf-8")
            with self.assertRaises(BenchmarkError):
                load_benchmark(path)

    def test_reject_unverified_pmid(self):
        self._modified_fixture(lambda data: data["cases"][0].update({"pmid": "99999999"}))

    def test_reject_duplicate_case(self):
        self._modified_fixture(lambda data: data["cases"][0].update({"id": data["cases"][1]["id"]}))

    def test_reject_source_scope_change(self):
        self._modified_fixture(lambda data: data["cases"][0].update({"scope": "peer reviewed clinical study"}))

    def _predictions(self):
        return {"predictions": [
            {"id": case["id"], "decision": case["expected"], "reason": "Checked original abstract"}
            for case in self.benchmark["cases"]
        ]}

    def test_perfect_labels_do_not_imply_validated_science(self):
        score = score_predictions(self.benchmark, self._predictions())
        self.assertEqual(score["accuracy"], 1.0)
        self.assertTrue(score["no_overclaims"])
        self.assertIn("NOT_SCIENTIFIC_VALIDATION", score["status"])

    def test_unsafe_overclaims_are_reported_explicitly(self):
        predictions = self._predictions()
        overclaimed = next(
            row for row in predictions["predictions"]
            if row["id"] == "UNC13A-003"
        )
        overclaimed["decision"] = "supported"
        score = score_predictions(self.benchmark, predictions)
        self.assertFalse(score["no_overclaims"])
        self.assertEqual(score["unsafe_overclaims"], ["UNC13A-003"])
        self.assertLess(score["accuracy"], 1)

    def test_reject_unexplained_and_duplicate_predictions(self):
        predictions = self._predictions()
        predictions["predictions"][0]["reason"] = ""
        with self.assertRaises(BenchmarkError):
            score_predictions(self.benchmark, predictions)
        predictions = self._predictions()
        predictions["predictions"][0]["id"] = predictions["predictions"][1]["id"]
        with self.assertRaises(BenchmarkError):
            score_predictions(self.benchmark, predictions)

    def test_live_identity_check_mock(self):
        papers = [Paper(
            pmid=s["pmid"], title=s["short"], abstract="An actual abstract for test purposes.",
            year=str(s["year"]), journal="Mock journal", doi=s["doi"]
        ) for s in self.benchmark["sources"]]
        with patch("agent_lab.benchmark.fetch_pubmed", return_value=papers) as fetch:
            report = check_pubmed_sources(self.benchmark)
        self.assertEqual(report["status"], "LIVE_PUBMED_SOURCE_CHECK_PASS")
        self.assertEqual(fetch.call_count, 1)
        self.assertIn("35197626[PMID]", fetch.call_args.args[0])
        self.assertEqual(fetch.call_args.kwargs["limit"], 8)
        self.assertEqual(report["model_calls"], 0)

    def test_missing_live_source_fails_closed(self):
        with patch("agent_lab.benchmark.fetch_pubmed", return_value=[]):
            report = check_pubmed_sources(self.benchmark)
        self.assertEqual(report["status"], "LIVE_PUBMED_SOURCE_CHECK_FAIL")
        self.assertEqual(report["retrieved_sources"], 0)


if __name__ == "__main__":
    unittest.main()
