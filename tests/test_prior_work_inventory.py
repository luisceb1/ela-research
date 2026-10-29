import tempfile
import unittest
from pathlib import Path
import zipfile

from scripts.inventory_prior_work import inspect_package, inventory


class PriorWorkInventoryTests(unittest.TestCase):
    def test_shared_bytes_identified_despite_different_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            for archive_name, member in [("one.zip", "a.csv"), ("two.zip", "b.csv")]:
                with zipfile.ZipFile(Path(tmp) / archive_name, "w") as archive:
                    archive.writestr(member, "same synthetic content\n")
            result = inventory(tmp)
            self.assertEqual(len(result["cross_package_identical_members"]), 1)
            self.assertEqual(result["errors"], [])

    def test_traversal_rejected_and_nothing_extracted(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "unsafe.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("../escaped.csv", "synthetic")
            with self.assertRaisesRegex(ValueError, "Unsafe"):
                inspect_package(path)
            self.assertEqual(list(Path(tmp).iterdir()), [path])

    def test_expansion_budget_enforced_before_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "large.zip"
            with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                archive.writestr("data.txt", "x" * 200)
            with self.assertRaisesRegex(ValueError, "exceeds"):
                inspect_package(path, limit=100)

    def test_invalid_pdf_recorded_as_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "fake.pdf").write_text("not a pdf")
            result = inventory(tmp)
            self.assertEqual(result["packages"], [])
            self.assertEqual(len(result["errors"]), 1)
