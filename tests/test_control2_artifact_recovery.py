import hashlib
import csv
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

class Control2FullArtifactRecoveryTests(unittest.TestCase):
    def test_full_result_matches_original_pre_loss_sha256(self):
        path = OUT / "execution/full-control-results.json"
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
                         "cb26604160e43cdc04d2eab0a2525fc02f296059d70f5e0d9d731a32d9f6b4a7")
        result = json.loads(path.read_text())
        self.assertTrue(result["complete_library"])
        self.assertEqual(result["run"], "SRR8144908")
        self.assertEqual(result["watchdog_errors"], [])

    def test_all55_bins_agree_across_original_extractors_and_tsv(self):
        result = json.loads((OUT / "execution/full-control-results.json").read_text())
        text = json.loads((OUT / "execution/text-checkpoint.json").read_text())
        hts = json.loads((OUT / "execution/htslib-checkpoint.json").read_text())
        self.assertEqual(text["completed_bins"], hts["completed_bins"])
        self.assertEqual(text["completed_bins"], result["completed_bins"])
        prefix = json.loads((OUT / "in-progress-checkpoint.json").read_text())
        self.assertEqual(prefix["completed_bins"], result["completed_bins"][:30])
        self.assertEqual(prefix["source_sha256"], result["fastq_sha256"])
        self.assertEqual(text["counts"], hts["counts"])
        self.assertEqual(text["counts"], result["counts"])
        with (OUT / "bin-qc.tsv").open(newline="") as stream:
            rows = list(csv.DictReader(stream, delimiter="\t"))
        self.assertEqual(len(rows), 55)
        self.assertEqual([int(row["reads"]) for row in rows], [1000000] * 54 + [292655])
        self.assertEqual(sum(int(row["primary_records"]) for row in rows), 54292655)
        self.assertEqual(sum(int(row["sam_records"]) for row in rows), result["sam_records"])
        for index, (row, original) in enumerate(zip(rows, result["completed_bins"])):
            for key in ("first_read", "last_read", "reads", "primary_records", "sam_records"):
                self.assertEqual(int(row[key]), original[key])
            for anchor in ("8", "15"):
                for target in ("canonical", "cryptic"):
                    self.assertEqual(int(row[target + "_anchor" + anchor]), original["counts"][anchor][target])
                self.assertEqual(int(row["total_introns_anchor" + anchor]), original["counts"][anchor]["eligible_intron_observations"])
            for exon in ("exon1_unique_overlap", "exon2_unique_overlap"):
                self.assertEqual(int(row[exon]), hts["locus_bins"][index].get(exon, 0))
        for anchor in ("8", "15"):
            self.assertEqual(sum(int(row["total_introns_anchor" + anchor]) for row in rows), result["counts"][anchor]["eligible_intron_observations"])
            for target in ("canonical", "cryptic"):
                self.assertEqual(sum(int(row[target + "_anchor" + anchor]) for row in rows), result["counts"][anchor][target])

if __name__ == "__main__":
    unittest.main()
