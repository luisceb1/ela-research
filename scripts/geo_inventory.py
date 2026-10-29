#!/usr/bin/env python3
"""Inventario solo estructural de tablas uniqueCounts GEO, sin inferencia."""
import csv
import gzip
import io
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports/geo-inventory.md"
SOURCES = {
    "GSE310723": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE310nnn/GSE310723/suppl/GSE310723_i3N_isoseq_uniqueCounts_transcript.txt.gz",
    "GSE315972": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE315nnn/GSE315972/suppl/GSE315972_NYGC_isoseq_uniqueCounts_transcript.txt.gz",
}

def inspect(label, url):
    req = urllib.request.Request(url, headers={"User-Agent": "ELAResearchInventory/0.1"})
    with urllib.request.urlopen(req, timeout=80) as response:
        raw = response.read()
    table = io.StringIO(gzip.decompress(raw).decode("utf-8-sig"))
    header = table.readline().rstrip("\r\n")
    delimiter = "\t" if "\t" in header else ","
    fields = next(csv.reader([header], delimiter=delimiter))
    nrows, widths, example = 0, set(), []
    for row in csv.reader(table, delimiter=delimiter):
        if not row:
            continue
        nrows += 1
        widths.add(len(row))
        if len(example) < 2:
            example.append(row[:4])
    return {
        "dataset": label, "source_url": url, "compressed_bytes": len(raw),
        "n_rows": nrows, "n_columns": len(fields), "columns": fields,
        "observed_row_widths": sorted(widths), "first_rows_first_4_fields": example
    }

def main():
    if REPORT.exists() and "INVENTORY_COMPLETE" in REPORT.read_text(encoding="utf-8"):
        print("Existing completed structural inventory; skip repeated downloads.")
        return
    lines = ["# Inventario técnico GEO", "",
             "Inspección estructural: NO análisis diferencial ni validación biológica.", ""]
    failures = 0
    for label, url in SOURCES.items():
        lines.extend([f"## {label}", "", f"Fuente: {url}", ""])
        try:
            data = inspect(label, url)
            lines.extend(["~~~json", json.dumps(data, indent=2, ensure_ascii=False), "~~~", ""])
        except Exception as exc:
            failures += 1
            lines.extend([f"ERROR NO VALIDADO: {type(exc).__name__}: {str(exc)[:240]}", ""])
    if not failures:
        lines.extend(["", "INVENTORY_COMPLETE — inspección de estructura completada; sin validación científica."])
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"GEO files checked; errors={failures}")
    if failures:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
