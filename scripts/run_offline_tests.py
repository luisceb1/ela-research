"""Run unittest controls and report skipped coverage explicitly."""
import argparse
from collections import Counter
import json
import os
from pathlib import Path
import sys
import unittest


class CoverageResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.passed = 0

    def addSuccess(self, test):
        self.passed += 1
        super().addSuccess(test)


def run(start_dir, patterns, report, summary=None, fail_on_skip=False):
    # Direct script invocation otherwise exposes scripts/ but not its parent,
    # unlike python -m unittest. Historical tests use both import styles.
    root = str(Path(__file__).resolve().parents[1])
    if root not in sys.path:
        sys.path.insert(0, root)
    suite = unittest.TestSuite()
    counts = {}
    for pattern in patterns:
        tests = unittest.TestLoader().discover(str(start_dir), pattern=pattern)
        counts[pattern] = tests.countTestCases()
        suite.addTests(tests)
    result = unittest.TextTestRunner(verbosity=2, resultclass=CoverageResult).run(suite)
    missing = [pattern for pattern, count in counts.items() if count == 0]
    skipped = [{"test": test.id(), "reason": reason} for test, reason in result.skipped]
    failed = [test.id() for test, _ in result.failures]
    errors = [test.id() for test, _ in result.errors]
    if missing:
        status = "empty_selection"
    elif not result.wasSuccessful():
        status = "failed"
    elif skipped and fail_on_skip:
        status = "unexpected_skips"
    else:
        status = "passed_with_skips" if skipped else "passed"
    data = {
        "status": status,
        "python": sys.version.split()[0],
        "patterns": counts,
        "discovered": sum(counts.values()),
        "run": result.testsRun,
        "executed": result.testsRun - len(skipped),
        "passed": result.passed,
        "failures": failed,
        "errors": errors,
        "skipped": skipped,
        "expected_failures": [test.id() for test, _ in result.expectedFailures],
        "unexpected_successes": [test.id() for test in result.unexpectedSuccesses],
        "missing_patterns": missing,
        "fail_on_skip": fail_on_skip,
    }
    report = Path(report)
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if summary:
        # Reasons can contain arbitrary fixture text; escape Markdown table syntax.
        def safe(value):
            return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ")

        reasons = Counter(item["reason"] for item in skipped)
        lines = ["## Offline test coverage", "", f"Status: **{status}**", "",
                 f"Discovered: {data['discovered']}; executed: {data['executed']}; "
                 f"passed: {result.passed}; skipped: {len(skipped)}; "
                 f"failures: {len(failed)}; errors: {len(errors)}; "
                 f"expected failures: {len(result.expectedFailures)}; "
                 f"unexpected successes: {len(result.unexpectedSuccesses)}.", "",
                 "Skipped controls are not verified by this job. Full IDs and reasons are in the JSON artifact.", ""]
        if reasons:
            lines += ["| Skip reason | Count |", "|---|---:|"]
            lines += [f"| {safe(reason)} | {count} |" for reason, count in sorted(reasons.items())]
        if missing:
            lines += ["", "Empty requested patterns: " + ", ".join(safe(p) for p in missing)]
        with Path(summary).open("a", encoding="utf-8") as handle:
            handle.write("\n".join(lines) + "\n")
    print(json.dumps({key: data[key] for key in ("status", "discovered", "executed")}, sort_keys=True))
    return 0 if status in {"passed", "passed_with_skips"} else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("patterns", nargs="*", default=["test_*.py"])
    parser.add_argument("--start-dir", type=Path, default=Path("tests"))
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--summary", type=Path, default=os.environ.get("GITHUB_STEP_SUMMARY"))
    parser.add_argument("--fail-on-skip", action="store_true")
    args = parser.parse_args()
    if len(args.patterns) != len(set(args.patterns)):
        parser.error("Repeated test patterns would run the same selection more than once")
    return run(args.start_dir, args.patterns, args.report, args.summary, args.fail_on_skip)


if __name__ == "__main__":
    raise SystemExit(main())
