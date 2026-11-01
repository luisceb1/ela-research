"""Inspect NYGC Parquet schema and candidate chr19 UNC13A rows from ZIP.

Read a small number of files first; no extraction of the 5GB ZIP.
Run: py scripts/nygc_schema_probe.py
"""
import io
import zipfile
from pathlib import Path
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parent.parent
PATH = ROOT / "data/external/zenodo_15977268/nygc_parquets.zip"

with zipfile.ZipFile(PATH) as z:
    infos = [i for i in z.infolist()
             if i.filename.startswith("parquets/")
             and i.filename.endswith(".parquet") and "/._" not in i.filename]
    print("PARQUETS:", len(infos))
    for info in infos[:3]:
        with z.open(info) as fd:
            content = fd.read()
        parquet = pq.ParquetFile(io.BytesIO(content))
        print("\nFILE:", info.filename, "BYTES:", len(content))
        print("SCHEMA:\n", parquet.schema_arrow)
        print("ROWS:", parquet.metadata.num_rows)
        table = parquet.read_row_group(0)
        print("FIRST TWO RECORDS:", table.slice(0, 2).to_pylist())
    print("\nNOTE: Schema inspection only. Chromosome, coordinate, sample and")
    print("reference-assembly conventions must be verified before filtering.")
