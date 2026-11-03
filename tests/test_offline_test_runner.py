"""Exercise runner exit policy with artificial test modules, not research data."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/run_offline_tests.py"


class OfflineRunnerTests(unittest.TestCase):
    def invoke(self, body, *extra):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "test_fixture.py").write_text("import unittest\n" + body, encoding="utf-8")
            report, summary = root / "results.json", root / "summary.md"
            env = dict(os.environ)
            env.pop("GITHUB_STEP_SUMMARY", None)
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--start-dir", str(root), "--report", str(report),
                 "--summary", str(summary), *extra],
                text=True, capture_output=True, timeout=15, env=env,
            )
            self.assertTrue(report.is_file(), result.stderr)
            return result.returncode, json.loads(report.read_text(encoding="utf-8")), summary.read_text(encoding="utf-8")

    def test_allowed_skip_is_reported_without_claiming_execution(self):
        code, data, summary = self.invoke(
            "class Controls(unittest.TestCase):\n"
            "    def test_pass(self): self.assertTrue(True)\n"
            "    @unittest.skip('optional | dependency')\n"
            "    def test_skip(self): pass\n"
        )
        self.assertEqual(code, 0)
        self.assertEqual(data["status"], "passed_with_skips")
        self.assertEqual((data["discovered"], data["executed"], len(data["skipped"])), (2, 1, 1))
        self.assertEqual(data["passed"], 1)
        self.assertEqual(data["skipped"][0]["reason"], "optional | dependency")
        self.assertIn("optional \\| dependency", summary)

    def test_strict_suite_rejects_skipped_controls(self):
        code, data, _ = self.invoke(
            "class Controls(unittest.TestCase):\n"
            "    @unittest.skip('dependency missing')\n"
            "    def test_skip(self): pass\n", "--fail-on-skip"
        )
        self.assertNotEqual(code, 0)
        self.assertEqual(data["status"], "unexpected_skips")

    def test_assertion_failure_is_not_masked_by_reporting(self):
        code, data, _ = self.invoke(
            "class Controls(unittest.TestCase):\n"
            "    def test_failure(self): self.fail('artificial failure')\n"
        )
        self.assertNotEqual(code, 0)
        self.assertEqual(data["status"], "failed")
        self.assertEqual(len(data["failures"]), 1)

    def test_exception_is_not_masked_by_reporting(self):
        code, data, _ = self.invoke(
            "class Controls(unittest.TestCase):\n"
            "    def test_error(self): raise RuntimeError('artificial error')\n"
        )
        self.assertNotEqual(code, 0)
        self.assertEqual(len(data["errors"]), 1)

    def test_empty_discovery_fails(self):
        code, data, _ = self.invoke("# no test cases\n")
        self.assertNotEqual(code, 0)
        self.assertEqual(data["status"], "empty_selection")

    def test_one_missing_pattern_fails_even_when_another_passes(self):
        code, data, _ = self.invoke(
            "class Controls(unittest.TestCase):\n"
            "    def test_pass(self): pass\n", "test_fixture.py", "test_missing.py"
        )
        self.assertNotEqual(code, 0)
        self.assertEqual(data["missing_patterns"], ["test_missing.py"])


if __name__ == "__main__":
    unittest.main()
