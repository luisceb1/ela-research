"""Inspect NYGC ZIP layout without extracting multi-gigabyte archive.

No inference or data export. Requires stdlib only.
"""
import collections
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parent.parent
path = root / "data/external/zenodo_15977268/nygc_parquets.zip"
with zipfile.ZipFile(path) as archive:
    allinfo = archive.infolist()
    real = [x for x in allinfo if x.filename.endswith(".parquet")
            and not x.filename.startswith("__MACOSX/")
            and "/._" not in x.filename]
    target = [x for x in real if "/chrom=chr19/" in x.filename]
    chrom_counts = collections.Counter()
    for x in real:
        for part in x.filename.split("/"):
            if part.startswith("chrom="):
                chrom_counts[part] += 1
                break
    print("ZIP:", path.name)
    print("ALL ZIP ENTRIES:", len(allinfo))
    print("REAL PARQUETS:", len(real))
    print("CHR19 PARQUETS:", len(target))
    print("CHR19 UNCOMPRESSED BYTES:", sum(x.file_size for x in target))
    print("CHROM PARTITIONS:", dict(sorted(chrom_counts.items())))
    print("FIRST 10 CHR19 FILES:")
    for x in target[:10]:
        print(x.filename, "bytes:", x.file_size)
    print("FIRST 10 REAL FILES:")
    for x in real[:10]:
        print(x.filename, "bytes:", x.file_size)
    if not target:
        print("IMPORTANT: chr19 naming differs; inspect sample file list before filtering.")
