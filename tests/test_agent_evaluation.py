"""Gold-blind scoring integration checks; no paid or network calls."""
import unittest

from agent_lab.benchmark import BenchmarkError, load_benchmark
from agent_lab.evaluation import evaluate_benchmark
from agent_lab.sources import Paper


class FakeEvaluationProvider:
    model = "mock-no-api"

    def __init__(self, benchmark):
        self.benchmark = benchmark
        self.calls = []

    def run(self, role, instructions, payload, schema):
        self.calls.append((role, instructions, payload, schema))
        return {"predictions": [
            {"id": c["id"], "decision": c["expected"],
             "reason": "Source abstract should support this interpretation"}
            for c in self.benchmark["cases"]
        ]}


class TestEvaluation(unittest.TestCase):
    def setUp(self):
        self.benchmark = load_benchmark()
        self.papers = [
            Paper(s["pmid"], s["short"], "Abstract text for mocked test",
                  str(s["year"]), "Test Journal", s["doi"])
            for s in self.benchmark["sources"]
        ]

    def test_gold_labels_are_not_sent_to_model(self):
        provider = FakeEvaluationProvider(self.benchmark)
        outcome = evaluate_benchmark(self.benchmark, self.papers, provider)
        self.assertEqual(outcome["model_calls"], 1)
        self.assertEqual(len(provider.calls), 1)
        self.assertEqual(outcome["score"]["accuracy"], 1)
        role, _, payload, schema = provider.calls[0]
        self.assertEqual(role, "benchmark")
        self.assertEqual(len(payload["cases"]), 20)
        self.assertEqual(len(payload["papers"]), 8)
        self.assertNotIn("expected", str(payload))
        self.assertEqual(set(payload["cases"][0]), {"id", "pmid", "claim"})
        self.assertEqual(schema["additionalProperties"], False)
        self.assertIn("NOT_SCIENTIFIC_VALIDATION", outcome["score"]["status"])

    def test_missing_or_empty_source_stops_before_model(self):
        provider = FakeEvaluationProvider(self.benchmark)
        with self.assertRaises(BenchmarkError):
            evaluate_benchmark(self.benchmark, self.papers[:-1], provider)
        self.assertEqual(provider.calls, [])
        blank = self.papers[0]
        changed = [Paper(blank.pmid, blank.title, "", blank.year,
                         blank.journal, blank.doi)] + self.papers[1:]
        with self.assertRaises(BenchmarkError):
            evaluate_benchmark(self.benchmark, changed, provider)
        self.assertEqual(provider.calls, [])

    def test_invalid_predictions_fail_closed(self):
        class BadProvider(FakeEvaluationProvider):
            def run(self, role, instructions, payload, schema):
                result = super().run(role, instructions, payload, schema)
                result["predictions"].pop()
                return result
        with self.assertRaises(BenchmarkError):
            evaluate_benchmark(self.benchmark, self.papers, BadProvider(self.benchmark))


if __name__ == "__main__":
    unittest.main()
