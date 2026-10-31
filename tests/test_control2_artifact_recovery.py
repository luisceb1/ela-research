import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports/gse122069-next-control-20261031"

class Control2ArtifactRecoveryTests(unittest.TestCase):
    """Recovery integrity against hashes recorded before execution-host loss."""
    def test_summary_matches_original_pre_loss_sha256(self):
        path = OUT / "summary.json"
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
                         "71eeabbc01277786fd7a849958c4fdc2eadb127ed6e7bba7d984b7c46052cf87")
        summary = json.loads(path.read_text())
        self.assertTrue(summary["complete_library"])
        self.assertEqual(summary["concordant_completed_reads"], 54292655)
        self.assertEqual(summary["concordant_completed_bins"], 55)
        self.assertEqual(summary["counts"]["15"]["cryptic"], 3)
        self.assertIsNone(summary["first1M_matches_historical_pilot"])

    def test_fastq_qc_matches_original_pre_loss_sha256(self):
        path = OUT / "execution/fastq_qc.json"
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
                         "8b4c0704ab24ac103b7abea19cd79b761c49ef9931b042bf963af0504e6a7641")
        qc = json.loads(path.read_text())
        self.assertTrue(qc["gzip_eof_crc_validated"])
        self.assertEqual(sum(qc["length_histogram"].values()), 54292655)
        self.assertEqual(sum(int(k) * v for k,v in qc["length_histogram"].items()),
                         qc["bases"])

if __name__ == "__main__":
    unittest.main()
