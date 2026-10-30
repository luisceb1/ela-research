"""NYGC UNC13A aggregate phenotype/tissue audit; no donor-level output.

Run: py scripts/nygc_unc13a_metadata_audit.py
Reads the local NYGC ZIP one parquet at a time, fetches version-pinned
author metadata into data/external. No statistical or clinical validation.
"""
import csv
import hashlib
import io
import math
import statistics
import urllib.request
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
import pyarrow.parquet as pq
import pyarrow.compute as pc

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data/external/zenodo_15977268"
SOURCE_SHA = "80fa3d70418a4665a85d414e33c7c470a9312086"
URL = ("https://raw.githubusercontent.com/frattalab/cryptic_biology/"
       + SOURCE_SHA + "/data/metadta_nygc.csv")
META = DATA / "metadta_nygc.csv"
TARGETS = {
    (17641556,17642845): "canonical_candidate",
    (17641556,17642414): "novel_donor",
    (17642541,17642845): "novel_acceptor",
    (17642591,17642845): "long_unconfirmed",
}
FIELDS = ["chrom","sample","start","end","strand","junction_count","cluster_count"]
MIN_GROUP_N = 5

def metadata():
    DATA.mkdir(parents=True,exist_ok=True)
    if not META.exists():
        with urllib.request.urlopen(URL, timeout=60) as response:
            META.write_bytes(response.read())
    b=META.read_bytes()
    print("METADATA SHA256:", hashlib.sha256(b).hexdigest())
    entries=list(csv.DictReader(io.StringIO(b.decode("utf-8-sig"))))
    required={"sample","tdp_proteinopathy","rna_tissue_source_simplified","external_subject_id"}
    if not entries or not required.issubset(entries[0]):
        raise ValueError("Unexpected metadata schema")
    lookup={}
    for r in entries:
        sid=r["sample"].strip()
        if not sid or sid in lookup:
            raise ValueError("Missing or duplicate metadata sample ID")
        lookup[sid]=r
    return lookup

def main():
    lookup=metadata()
    counts=defaultdict(dict)
    records=0
    with zipfile.ZipFile(DATA/"nygc_parquets.zip") as z:
        filenames=[n for n in z.namelist() if n.startswith("parquets/")
                   and n.endswith(".parquet") and "/._" not in n]
        for index,name in enumerate(filenames,1):
            with z.open(name) as handle:
                pf=pq.ParquetFile(io.BytesIO(handle.read()))
            for rg in range(pf.num_row_groups):
                t=pf.read_row_group(rg,columns=FIELDS)
                mask=pc.and_(pc.equal(t["chrom"],"chr19"),
                    pc.and_(pc.equal(t["strand"],"-"),
                    pc.and_(pc.and_(pc.greater_equal(t["start"],17641000),
                                    pc.less_equal(t["start"],17643500)),
                            pc.and_(pc.greater_equal(t["end"],17641000),
                                    pc.less_equal(t["end"],17643500))))
                )
                for r in t.filter(mask).to_pylist():
                    event=TARGETS.get((r["start"],r["end"]))
                    if event is None:
                        continue
                    sid=r["sample"]
                    if sid not in lookup or event in counts[sid]:
                        raise ValueError("Unmatched or duplicate NYGC record")
                    j,d=r["junction_count"],r["cluster_count"]
                    if j is None or d is None or j<0 or d<0 or j>d:
                        raise ValueError("Bad counts")
                    counts[sid][event]=(j,d)
                    records+=1
            if index%500==0:
                print("SCANNED",index,"/",len(filenames),flush=True)
    if not counts or any(set(x)!=set(TARGETS.values()) for x in counts.values()):
        raise ValueError("Incomplete target events per sample")
    print("MATCHED SAMPLES",len(counts),"RECORDS",records)
    unique_donors={r["external_subject_id"] for s,r in lookup.items()
                   if s in counts and r["external_subject_id"].strip()}
    print("NONEMPTY UNIQUE EXTERNAL SUBJECT IDS",len(unique_donors))
    grouped=defaultdict(list)
    for sid,events in counts.items():
        r=lookup[sid]
        pathology=r["tdp_proteinopathy"].strip() or "Unknown"
        tissue=r["rna_tissue_source_simplified"].strip() or "Unknown"
        grouped[(tissue,pathology)].append((sid,events,r))
    print("TISSUE | PATHOLOGY | N SAMPLES | N DISTINCT NONEMPTY DONORS | CANONICAL POS | DONOR CE POS | ACCEPTOR CE POS | MEDIAN LOCAL DEPTH | RIN N")
    for (tissue,path),items in sorted(grouped.items()):
        if len(items)<MIN_GROUP_N:
            print(tissue,"|",path,"|",len(items),"| small group (event counts suppressed)")
            continue
        donors={r["external_subject_id"].strip() for _,_,r in items
                if r["external_subject_id"].strip()}
        def pos(event):
            return sum(e[event][0]>0 for _,e,_ in items)
        ds=[e["canonical_candidate"][1] for _,e,_ in items]
        rin_ok=0
        for _,_,r in items:
            try:
                rin_ok+=int(math.isfinite(float(r["rin"])))
            except (ValueError,TypeError):
                pass
        print(tissue,"|",path,"|",len(items),"|",len(donors),"|",
              pos("canonical_candidate"),"|",pos("novel_donor"),"|",
              pos("novel_acceptor"),"|",statistics.median(ds),"|",rin_ok)
    print("No independent donor-level inference: multiple tissues/samples per subject possible.")
    print("No causal, ALS-specific or diagnostic validation; check cross-study donor overlap.")

if __name__=="__main__":
    main()
