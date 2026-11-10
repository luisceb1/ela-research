"""Wire-contract tests for the real Responses API adapter, without network or spend."""
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from agent_lab.provider import OpenAIProvider, ProviderError
from agent_lab.sources import Paper
from agent_lab.workflow import SCHEMAS, run_lab


RESPONSES = {
    "literature": {"findings": [{"pmid": "12345", "finding": "Signal detected",
                                "limitation": "Single small study"}]},
    "hypothesis": {"hypotheses": [{
        "statement": "There could be an effect", "prediction": "Signal changes",
        "falsifier": "No difference", "proposed_test": "Measure controlled response",
        "required_data": "Independent biological replicates", "pmids": ["12345"],
    }]},
    "skeptic": {"assessment": "Unvalidated", "objections": [{
        "hypothesis_number": 1, "problem": "Replicate structure unclear",
        "severity": "high", "pmids": ["12345"],
    }]},
    "director": {"recommendation": "Review evidence", "next_action": "Read article",
                 "scope": "literature_review", "limitations": ["No new inference"],
                 "pmids": ["12345"]},
}


class FakeHttp:
    def __init__(self):
        self.requests = []
        self.responses = iter(RESPONSES.items())

    def __call__(self, request, timeout):
        self.requests.append(request)
        role, item = next(self.responses)
        actual = json.loads(request.data.decode("utf-8"))
        assert actual["text"]["format"]["name"] == role
        envelope = {
            "status": "completed",
            "output": [{"type": "message", "content": [
                {"type": "output_text", "text": json.dumps(item)}]}],
            "usage": {"input_tokens": 750, "output_tokens": 250, "total_tokens": 1000},
        }
        return io.BytesIO(json.dumps(envelope).encode("utf-8"))


class TestRealAdapterContract(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for filename in ("AGENTS.md", "research/STATE.md",
                         "research/BACKLOG.md", "research/PROTOCOL.md"):
            path = self.root / filename
            path.parent.mkdir(exist_ok=True, parents=True)
            path.write_text("No new experiments without approved evidence.", encoding="utf-8")
        self.paper = Paper("12345", "Test paper", "A result in one model",
                           "2022", "A test journal", "10.9999/test")

    def test_four_real_wire_calls_not_stubbed_role_methods(self):
        fake = FakeHttp()
        provider = OpenAIProvider(model="gpt-6.1-terra", api_key="testing-key-not-valid")
        with patch("agent_lab.provider.urlopen", side_effect=fake):
            report = run_lab("A bounded mechanistic question", [self.paper], provider, self.root)
        self.assertEqual(report["status"], "DRAFT_REQUIRES_HUMAN_REVIEW")
        self.assertEqual(len(fake.requests), 4)
        self.assertEqual(len(provider.usage), 4)
        self.assertEqual(sum(u["total_tokens"] for u in provider.usage), 4000)
        for req in fake.requests:
            payload = json.loads(req.data)
            self.assertEqual(req.full_url, "https://api.openai.com/v1/responses")
            self.assertEqual(payload["model"], "gpt-6.1-terra")
            self.assertFalse(payload["store"])
            self.assertEqual(payload["reasoning"], {"effort": "low"})
            self.assertEqual(payload["max_output_tokens"], 3500)
            self.assertEqual(payload["text"]["format"]["type"], "json_schema")
            self.assertTrue(payload["text"]["format"]["strict"])
            self.assertEqual(req.headers["Authorization"], "Bearer testing-key-not-valid")
            self.assertLessEqual(payload["max_output_tokens"], 3500)
        self.assertNotIn("testing-key-not-valid", json.dumps(report))

    def test_unauthorized_http_response_fails_without_key_leak(self):
        provider = OpenAIProvider(api_key="secret-that-must-never-appear")
        error = HTTPError("https://api.openai.com/v1/responses", 401, "Unauthorized", {}, None)
        with patch("agent_lab.provider.urlopen", side_effect=error):
            with self.assertRaisesRegex(ProviderError, "HTTP 401") as ctx:
                provider.run("literature", "JSON only", {"papers": []},
                             SCHEMAS["literature"])
        self.assertNotIn("secret-that-must-never-appear", str(ctx.exception))

    def test_incomplete_output_is_not_accepted(self):
        provider = OpenAIProvider(api_key="fake-key")
        envelope = {"status": "incomplete",
                    "incomplete_details": {"reason": "max_output_tokens"},
                    "output": []}
        with patch("agent_lab.provider.urlopen",
                   return_value=io.BytesIO(json.dumps(envelope).encode("utf-8"))):
            with self.assertRaisesRegex(ProviderError, "Incomplete"):
                provider.run("literature", "JSON only", {}, SCHEMAS["literature"])

    def test_refusal_is_not_accepted(self):
        provider = OpenAIProvider(api_key="fake-key")
        envelope = {"status": "completed",
                    "output": [{"type": "message", "content": [
                        {"type": "refusal", "refusal": "Cannot comply"}]}]}
        with patch("agent_lab.provider.urlopen",
                   return_value=io.BytesIO(json.dumps(envelope).encode("utf-8"))):
            with self.assertRaisesRegex(ProviderError, "refused"):
                provider.run("literature", "JSON only", {}, SCHEMAS["literature"])


if __name__ == "__main__":
    unittest.main()
