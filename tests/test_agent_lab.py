"""Offline controls for the multi-agent research layer. No API calls or biological tests."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from agent_lab.provider import OpenAIProvider, ProviderError
from agent_lab.sources import Paper, fetch_pubmed
from agent_lab.workflow import EvidenceError, run_lab


XML = b"""<?xml version="1.0"?>
<PubmedArticleSet><PubmedArticle>
<MedlineCitation><PMID>123</PMID><Article>
<ArticleTitle>Example title</ArticleTitle>
<Abstract><AbstractText Label="RESULTS">Measured response.</AbstractText></Abstract>
<Journal><Title>Test Journal</Title><JournalIssue>
<PubDate><Year>2022</Year></PubDate></JournalIssue></Journal>
</Article></MedlineCitation>
<PubmedData><ArticleIdList><ArticleId IdType="doi">10.1234/example</ArticleId></ArticleIdList></PubmedData>
</PubmedArticle></PubmedArticleSet>"""


class FakeProvider:
    model = "stub-does-not-call-model"

    def __init__(self, bad_citation=False, too_many=False):
        self.calls = []
        self.bad_citation = bad_citation
        self.too_many = too_many

    def run(self, role, instructions, payload, schema):
        self.calls.append(role)
        if role == "literature":
            return {"findings": [
                {"pmid": "999" if self.bad_citation else "123",
                 "finding": "Abstract reports a measurement",
                 "limitation": "No biological replication details"}
            ]}
        if role == "hypothesis":
            n = 3 if self.too_many else 1
            return {"hypotheses": [
                {"statement": "Test whether a mechanism changes response",
                 "prediction": "Response changes", "falsifier": "No change",
                 "proposed_test": "Predefined comparison",
                 "required_data": "Independent units", "pmids": ["123"]}
                for _ in range(n)
            ]}
        if role == "skeptic":
            return {"assessment": "Not validated", "objections": [
                {"hypothesis_number": 1, "problem": "Independent units missing",
                 "severity": "high", "pmids": ["123"]}
            ]}
        return {"recommendation": "Review sources", "next_action": "Request no new work",
                "scope": "literature_review", "limitations": ["Abstract-only"],
                "pmids": ["123"]}


class TestPubmed(unittest.TestCase):
    def test_only_source_returned_is_parsed(self):
        reply = json.dumps({"esearchresult": {"idlist": ["123", "bad", "123", "345"]}}).encode()
        with patch("agent_lab.sources._fetch", side_effect=[reply, XML]) as fetch:
            items = fetch_pubmed("ALS UNC13A", 3)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].pmid, "123")
        self.assertEqual(items[0].doi, "10.1234/example")
        self.assertIn("Measured response", items[0].abstract)
        self.assertEqual(fetch.call_count, 2)
        self.assertIn("123,345", fetch.call_args[0][1]["id"])

    def test_no_hit_never_fetches_abstracts(self):
        reply = json.dumps({"esearchresult": {"idlist": []}}).encode()
        with patch("agent_lab.sources._fetch", return_value=reply) as fetch:
            self.assertEqual(fetch_pubmed("unknown"), [])
        self.assertEqual(fetch.call_count, 1)

    def test_limit_guard(self):
        for count in (0, 9, -1):
            with self.assertRaises(ValueError):
                fetch_pubmed("ALS", count)
        with self.assertRaises(ValueError):
            fetch_pubmed("a" * 301)

    def test_endpoint_allowlist(self):
        from agent_lab.sources import _fetch
        with self.assertRaises(ValueError):
            _fetch("evil.fcgi", {})


class TestWorkflow(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for filename in ("AGENTS.md", "research/STATE.md",
                         "research/BACKLOG.md", "research/PROTOCOL.md"):
            path = self.root / filename
            path.parent.mkdir(exist_ok=True, parents=True)
            path.write_text("Preserve original gates. No automatic experiments.", encoding="utf-8")
        self.papers = [Paper("123", "Example", "Measured response.", "2022",
                             "Test Journal", "")]

    def test_four_roles_and_draft_label(self):
        provider = FakeProvider()
        report = run_lab("Test question", self.papers, provider, self.root)
        self.assertEqual(provider.calls, ["literature", "hypothesis", "skeptic", "director"])
        self.assertEqual(report["model_calls"], 4)
        self.assertEqual(report["status"], "DRAFT_REQUIRES_HUMAN_REVIEW")
        self.assertIn("research/STATE.md", report["repository_context"])
        self.assertTrue(report["source_metadata_sha256"])

    def test_hallucinated_reference_fails_closed(self):
        provider = FakeProvider(bad_citation=True)
        with self.assertRaises(EvidenceError):
            run_lab("Test", self.papers, provider, self.root)
        self.assertEqual(provider.calls, ["literature"])

    def test_hypothesis_count_fails_closed(self):
        provider = FakeProvider(too_many=True)
        with self.assertRaises(EvidenceError):
            run_lab("Test", self.papers, provider, self.root)
        self.assertEqual(provider.calls, ["literature", "hypothesis"])

    def test_no_sources_fails_closed(self):
        provider = FakeProvider()
        with self.assertRaises(EvidenceError):
            run_lab("Test", [], provider, self.root)
        self.assertEqual(provider.calls, [])

    def test_bad_director_scope_rejected(self):
        class Rogue(FakeProvider):
            def run(self, role, instructions, payload, schema):
                out = super().run(role, instructions, payload, schema)
                if role == "director":
                    out["scope"] = "clinical_treatment"
                return out
        with self.assertRaises(EvidenceError):
            run_lab("Test", self.papers, Rogue(), self.root)

    def test_absent_api_key_not_silently_accepted(self):
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(ProviderError):
                OpenAIProvider()


if __name__ == "__main__":
    unittest.main()
