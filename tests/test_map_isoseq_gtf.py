import tempfile
import unittest
from pathlib import Path
from scripts.map_isoseq_gtf import index_gtf, map_counts

class TestIsoSeqMapping(unittest.TestCase):
    def test_match_and_conflict(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d/"a.gtf").write_text('chr1\tsrc\ttranscript\t1\t100\t.\t+\t.\tgene_id "ENSG1.1"; transcript_id "BambuTx1"; gene_name "STMN2";\nchr1\tsrc\texon\t1\t50\t.\t+\t.\tgene_id "ENSG1.1"; transcript_id "BambuTx1"; gene_name "STMN2";\n')
            (d/"a.tsv").write_text("TXNAME\tGENEID\ts1\ts2\nBambuTx1\tENSG1.2\t2\t3\nBambuTx2\tENSG2\t1\t0\n")
            idx=index_gtf(d/"a.gtf")
            x=map_counts(d/"a.tsv",idx,d/"out.tsv",{"STMN2"})
            self.assertEqual(x["target_transcripts"],1)
            self.assertEqual(x["gtf_matched"],1)
            self.assertEqual(x["gene_id_conflicts"],0)
            self.assertIn("BambuTx1", (d/"out.tsv").read_text())
    def test_conflict(self):
        with tempfile.TemporaryDirectory() as d:
            d=Path(d)
            (d/"a.gtf").write_text('chr1\tsrc\ttranscript\t1\t100\t.\t+\t.\tgene_id "ENSG9"; transcript_id "BambuTx1"; gene_name "UNC13A";\n')
            (d/"a.tsv").write_text("TXNAME\tGENEID\ts1\nBambuTx1\tENSG1\t2\n")
            x=map_counts(d/"a.tsv",index_gtf(d/"a.gtf"),d/"out.tsv",{"UNC13A"})
            self.assertEqual(x["gene_id_conflicts"],1)
if __name__=="__main__":
    unittest.main()

    def test_ensembl_id_without_gene_name(self):
        with tempfile.TemporaryDirectory() as d:
            d=Path(d)
            (d/"a.gtf").write_text('chr8\\tsrc\\ttranscript\\t1\\t100\\t.\\t+\\t.\\tgene_id "ENSG00000104435.5"; transcript_id "BambuTx1";\\n')
            (d/"a.tsv").write_text("TXNAME\\tGENEID\\ts1\\nBambuTx1\\tENSG00000104435.5\\t3\\n")
            x=map_counts(d/"a.tsv",index_gtf(d/"a.gtf"),d/"out.tsv",{"STMN2"})
            self.assertEqual(x["by_target"]["STMN2"], 1)
            self.assertIn("STMN2", (d/"out.tsv").read_text())
