"""Reproduce received MEA unit tests and adversarial synthetic input checks.

No full simulation CLI, plot/report writers, empirical data or power estimates.
Run separately from the repository's stdlib-only test suite.
"""
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import platform
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.mea_audit_fixtures import cases
from scripts.mea_input_qc import validate_synthetic_rows


def main():
    out = ROOT / "reports/mea-software-audit"
    out.mkdir(parents=True, exist_ok=True)
    prototype = ROOT / "research/prototypes/mea_synthetic"
    manifest = json.loads((prototype / "source_manifest.json").read_text())
    for entry in manifest:
        if hashlib.sha256((ROOT / entry["local_path"]).read_bytes()).hexdigest() != entry["sha256"]:
            raise ValueError("Received source was modified; update audit provenance explicitly")
    test_runs = []
    for label, directory, start, pattern in [
        ("base", ROOT, str(prototype / "base/tests"), "test_design.py"),
        ("sensitivity", prototype / "sensitivity", ".", "test_sensibilidad.py"),
    ]:
        command = [sys.executable, "-m", "unittest", "discover", "-s", start, "-p", pattern, "-v"]
        run = subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=60)
        log = run.stdout + run.stderr
        (out / f"original_{label}_tests.txt").write_text(log)
        match = re.search(r"Ran (\d+) tests?", log)
        test_runs.append({"suite": label, "returncode": run.returncode,
                          "tests_run": int(match[1]) if match else None,
                          "passed": run.returncode == 0 and match is not None and "\nOK\n" in log})
    if not all(r["passed"] for r in test_runs):
        (out / "original_test_status.json").write_text(json.dumps(test_runs, indent=2) + "\n")
        raise RuntimeError("Received tests failed; see captured logs")
    sys.path.insert(0, str(prototype / "base/src"))
    import pandas as pd
    from analizar_csv_estandarizado import validate
    from mea_pipeline import add_baseline_adjustment, well_level_endpoints, summary_by_scenario
    findings = []
    for name, rows in cases().items():
        record = {"fixture": name, "data_type": "explicitly_artificial_minimal_counterexample"}
        frame = pd.DataFrame(rows)
        try:
            validate(frame)
            record["original_validation"] = "accepted"
        except Exception as exc:
            record["original_validation"] = type(exc).__name__ + ": " + str(exc)
        try:
            endpoints = well_level_endpoints(add_baseline_adjustment(frame))
            summary = summary_by_scenario(endpoints, seed=42, B=20)
            record["original_downstream"] = summary.classification.iloc[0]
        except Exception as exc:
            record["original_downstream"] = type(exc).__name__ + ": " + str(exc)
        try:
            validate_synthetic_rows(rows, provenance="synthetic")
            record["strict_preflight"] = "accepted_structurally_only"
        except ValueError as exc:
            record["strict_preflight"] = "rejected: " + str(exc)
        findings.append(record)
    assert all(r["original_validation"] == "accepted" for r in findings)
    assert all(r["strict_preflight"].startswith("rejected:") for r in findings if r["fixture"] != "valid")
    # Adversarial boundary for the second prototype, not a Monte Carlo study.
    sys.path.insert(0, str(prototype / "sensitivity"))
    from analisis_sensibilidad import Config, simulate_once
    extreme = simulate_once(Config(technical_missing=1.0, mortality_hazard=0.0), "none", 13)
    finite_means = sum(math.isfinite(extreme[k]) for k in ("mean_treat_3", "mean_treat_4", "mean_effect_3", "mean_effect_4"))
    assert finite_means == 0
    sensitivity_check = {"fixture": "all_followups_technically_missing_no_deaths",
                         "seed": 13, "technical_missing_probability": 1.0, "mortality_hazard": 0.0,
                         "reported_n_analyzable_blocks": extreme["n_analyzable_blocks"],
                         "finite_mean_contrasts": finite_means,
                         "evidence_recovery": extreme["evidence_recovery"],
                         "finding": "reported block count is formed records, not complete analyzable contrasts"}
    result = {"scope": "software audit only; no biological or experimental validation",
              "source_hashes_verified": len(manifest), "original_unit_tests": test_runs,
              "adversarial_fixtures": findings, "full_montecarlo_rerun": False,
              "sensitivity_denominator_counterexample": sensitivity_check,
              "plots_generated": False, "real_data_import_enabled": False}
    (out / "audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    environment = {"python": platform.python_version(),
                   "dependencies": {n: importlib.metadata.version(n) for n in ("numpy", "pandas", "scipy", "matplotlib")},
                   "fixture_bootstrap_seed": 42, "fixture_bootstrap_draws": 20,
                   "original_test_seeds": "preserved in hash-pinned test sources",
                   "scope": "bootstrap only exercises code branches on artificial fixture, not an inferential estimate"}
    (out / "environment.json").write_text(json.dumps(environment, indent=2) + "\n")
    print(json.dumps({"received_tests": test_runs, "invalid_fixtures_rejected": len(findings)-1,
                      "biological_validation": False}))


if __name__ == "__main__":
    main()
