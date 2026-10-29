"""Explicitly artificial adversarial fixtures; no empirical data."""

def synthetic_fixture():
    rows = []
    for arm in ("sham", "late_ASO", "damage_control"):
        for t in (0, 1, 2, 4, 5, 8, 9):
            y = .7 if arm == "sham" or t < 4 else .4 if t <= 5 else .6 if arm == "late_ASO" else .3
            rows.append(dict(scenario="synthetic_fixture", differentiation_id="synthetic_D",
                             well_id="synthetic_" + arm, arm=arm, time_index=t, synchrony=y,
                             viability=.9, qc_ok=1, status="observed", t0_index=None if arm == "sham" else 5))
    return rows


def cases():
    result = {"valid": synthetic_fixture()}
    for name in ("fractional_t0", "no_valid_baseline", "missing_sham_time", "revival", "invalid_viability", "missing_control_arm"):
        rows = synthetic_fixture()
        if name == "missing_sham_time":
            rows = [r for r in rows if not (r["arm"] == "sham" and r["time_index"] == 8)]
        elif name == "missing_control_arm":
            rows = [r for r in rows if r["arm"] != "damage_control"]
        else:
            for r in rows:
                if name == "fractional_t0" and r["arm"] != "sham": r["t0_index"] = 5.9
                if name == "no_valid_baseline" and r["arm"] != "sham" and r["time_index"] in (0, 1, 2):
                    r.update(synchrony=None, qc_ok=0, status="technical_missing")
                if name == "revival" and r["arm"] == "late_ASO" and r["time_index"] == 8:
                    r.update(synchrony=None, viability=0, qc_ok=0, status="dead")
                if name == "invalid_viability" and r["arm"] == "late_ASO": r["viability"] = 1.5
        result[name] = rows
    return result
