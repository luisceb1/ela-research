#!/usr/bin/env python3
"""Apply explicit, auditable filters to the broad shared-junction TSV.
Does not treat assigned isoform reads as splice-junction-spanning read evidence.
"""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path

def choose(columns, prefix, token):
    selected=[x for x in columns if x.startswith(prefix) and token in x]
    return selected

def evaluate(path, out):
    with open(path, newline="", encoding="utf-8") as f:
        reader=csv.DictReader(f,delimiter="\t")
        cols=reader.fieldnames or []
        culture_ctrl_no=choose(cols,"culture__","Ctrl_noAza")
        culture_ctrl_aza=choose(cols,"culture__","Ctrl_5Aza")
        culture_kd_no=choose(cols,"culture__","TDP43KD_noAza")
        culture_kd_aza=choose(cols,"culture__","TDP43KD_5Aza")
        brain_ci=choose(cols,"brain__","ALS-ci_")
        brain_ctl=choose(cols,"brain__","CTL_")
        groups=[culture_ctrl_no,culture_ctrl_aza,culture_kd_no,culture_kd_aza,brain_ci,brain_ctl]
        expected=[1,1,1,1,2,2]
        actual=list(map(len,groups))
        if actual!=expected:
            raise ValueError(f"Missing/ambiguous sample columns: expected {expected}, got {actual}; do not guess clinical groups")
        fields=["gene_id","chrom","intron_start","intron_end","strand","culture_tx","brain_tx",
                "culture_strict","brain_strict","dual_strict"]
        rows=[];tot=Counter()
        for x in reader:
            def n(k):return int(float(x[k]))
            cellular=(n(culture_ctrl_no[0])==0 and n(culture_ctrl_aza[0])==0 and
                      n(culture_kd_no[0])>=3 and n(culture_kd_aza[0])>=3)
            # Two observed ALS-ci labels, NOT 3 cases cited in an earlier report.
            brain=all(n(z)>=2 for z in brain_ci) and all(n(z)==0 for z in brain_ctl)
            row={k:x[k] for k in fields[:7]}
            row.update(culture_strict=int(cellular),brain_strict=int(brain),dual_strict=int(cellular and brain))
            rows.append(row)
            tot["all"]+=1
            tot["culture_strict"]+=cellular
            tot["brain_strict"]+=brain
            tot["dual_strict"]+=cellular and brain
    p=Path(out);p.mkdir(parents=True,exist_ok=True)
    with open(p/"filtered_junctions.tsv","w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t");w.writeheader();w.writerows(rows)
    summary=dict(tot)
    summary.update(group_columns=dict(control_no5aza=culture_ctrl_no,control_5aza=culture_ctrl_aza,
                         kd_no5aza=culture_kd_no,kd_5aza=culture_kd_aza,als_ci=brain_ci,ctl=brain_ctl),
        warning="ALS-ci labels are not clinically verified; two labeled ALS-ci, not three. Isoform-assigned counts are not junction-spanning reads.")
    (p/"filter_audit.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2))
    return summary
if __name__=="__main__":
    a=argparse.ArgumentParser();a.add_argument("--junctions",required=True);a.add_argument("--out",required=True)
    x=a.parse_args();evaluate(x.junctions,x.out)
