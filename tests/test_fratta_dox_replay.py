"""Transformation controls; artificial values are not neuronal evidence."""
import importlib.util
import math
import unittest
from pathlib import Path

P = Path(__file__).resolve().parents[1] / "scripts/reproduce_fratta_dox.py"
SPEC = importlib.util.spec_from_file_location("dox_replay", P)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class DoxReplayTests(unittest.TestCase):
    def fixture(self):
        return [{"Treatment": t, "Gene": gene, "Value": str(value),
                 "Line_Group": labels[0], "Color_Group": labels[1]}
                for t in MOD.TREATMENTS for gene, labels in MOD.SERIES.items()
                for value in (1, 3)]

    def test_key_change_loses_exactly_renamed_series(self):
        summary = MOD.summarize(self.fixture())
        old, new = MOD.replay_join(summary, True), MOD.replay_join(summary, False)
        self.assertEqual([r["Gene"] for r in old if not r["sem_join_matched"]],
                         ["13A-Correct RNA"] * 6)
        self.assertTrue(all(r["sem_join_matched"] for r in new))
        self.assertEqual([r["mean"] for r in old], [r["mean"] for r in new])

    def test_sem_uses_sample_sd(self):
        row = MOD.summarize(self.fixture())[0]
        self.assertEqual(row["mean"], 2)
        self.assertAlmostEqual(row["sd_rows"], math.sqrt(2))
        self.assertAlmostEqual(row["sem_rows"], 1)

    def test_row_order_cannot_define_pairing(self):
        rows = self.fixture()
        self.assertEqual(MOD.summarize(rows), MOD.summarize(list(reversed(rows))))

    def test_identical_observations_not_dropped(self):
        rows = self.fixture()
        rows.append(dict(rows[0]))
        first = next(r for r in MOD.summarize(rows) if r["Treatment"] == "NT"
                     and r["Gene"] == rows[0]["Gene"])
        self.assertEqual(first["n_rows"], 3)
        self.assertAlmostEqual(first["mean"], 5 / 3)

    def test_no_sem_from_single_row(self):
        with self.assertRaises(ValueError):
            MOD.summarize(self.fixture()[:1])


if __name__ == "__main__":
    unittest.main()
