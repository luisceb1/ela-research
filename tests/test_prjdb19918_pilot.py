"""Offline admission and cost/accounting contract tests; no cloud calls."""
import copy
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"infrastructure/hetzner"))
import prjdb19918_contract as c


def pricing(server="0.268499", ip="0.001"):
    def row(key,value,rate): return {key:value,"prices":[{"location":"nbg1","price_hourly":{"gross":rate}}]}
    return {"pricing":{"currency":"EUR","server_types":[row("name","ccx33",server)],
                       "primary_ips":[row("type","ipv4",ip)]}}


class Cloud:
    def __init__(self,p): self.p=p
    def request(self,method,path):
        assert method=="GET" and path=="/pricing"
        return self.p


class ContractTests(unittest.TestCase):
    def test_exact_roster(self):
        a=c.select("DRR631712");b=c.select("DRR631715")
        self.assertEqual((a["label"],b["label"]),("SCR2","KD1"))
        self.assertEqual(sum(m["bytes"] for r in (a,b) for m in r["mates"]),10349969475)
        with self.assertRaises(ValueError): c.select("DRR631711")
    def test_tampered_manifest(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/"m.json";p.write_bytes(c.MANIFEST.read_bytes()+b" ")
            with self.assertRaises(ValueError): c.select("DRR631712",p)
    def test_price_cap(self):
        self.assertEqual(c.combined_rate(Cloud(pricing()))["combined_rate_gross"],"0.269499")
        with self.assertRaises(RuntimeError): c.combined_rate(Cloud(pricing(ip="0.1")))
        with self.assertRaises(RuntimeError): c.combined_rate(Cloud(pricing(server="0.30",ip="0")))
        p=pricing();p["pricing"]["currency"]="USD"
        with self.assertRaises(RuntimeError):c.combined_rate(Cloud(p))
        p=pricing();p["pricing"]["primary_ips"]=[]
        with self.assertRaises(RuntimeError):c.combined_rate(Cloud(p))
    def test_technical_result(self):
        row=c.select("DRR631712")
        obj={"run":row["run"],"sample":row["sample"],"complete":True,
             "counts":{"canonical":2,"cryptic_left":0,"cryptic_right":0},
             "qc":{"sam_records":16,"alignment_groups":8,"eligible_groups":7,
                   "marked_duplicate_records":0,"rejected_groups":1}}
        self.assertIs(c.validate_result(obj,row),obj)
        for key,val in (("canonical",0),("cryptic_left",8)):
            x=copy.deepcopy(obj);x["counts"][key]=val
            with self.assertRaises(ValueError): c.validate_result(x,row)
        x=copy.deepcopy(obj);x["qc"]["alignment_groups"]=9
        with self.assertRaises(ValueError):c.validate_result(x,row)


if __name__=="__main__": unittest.main()
