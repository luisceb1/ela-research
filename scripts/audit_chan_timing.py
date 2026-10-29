"""Audit explicit timing and XLSX metadata; no graph digitization or inference.

Requires Poppler pdftotext for the publisher PDF. Workbook parsing uses stdlib.
Manual interpretation stays in REPORT.md; missing evidence is never false.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import unicodedata
import xml.etree.ElementTree as E
import zipfile

DOI = "10.1038/s42003-026-10832-6"
ROOT = Path(__file__).resolve().parents[1]
NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def normalize(text):
    # Join alphabetic words split by PDF typesetting, retaining TDP-43 etc.
    text = re.sub(r"(?<=[A-Za-z])-\s*\n\s*(?=[a-z])", "", text)
    return " ".join(unicodedata.normalize("NFKC", text).split())


def caption(text, figure):
    marker = f"Fig. {figure} |"
    if text.count(marker) != 1:
        raise ValueError("Missing or ambiguous figure caption")
    return text.split(marker, 1)[1].split("https://doi.org/", 1)[0]


def timing7(text):
    text = normalize(text)
    match = re.search(r"Single dose on DIV (\d+), double doses on DIV (\d+) and DIV (\d+)", text)
    if not match:
        raise ValueError("Explicit first/repeated doses missing")
    return {"single_dose_DIV": [int(match[1])],
            "repeated_doses_DIV": [int(match[2]), int(match[3])],
            "delayed_initiation_arm_verified": None,
            "persistent_functional_deficit_eligibility_verified": None}


def timing8(text):
    text = normalize(text)
    injury = re.search(r"Axotomy was performed on DIV (\d+)", text)
    follow = re.search(r"immunostained (\d+) days after injury", text)
    immediate = "treatment with ASO was performed straight after injury" in text
    if not injury or not follow:
        raise ValueError("Injury or endpoint timing missing")
    return {"axotomy_DIV": int(injury[1]),
            "first_ASO_DIV": int(injury[1]) if immediate else None,
            "postinjury_treatment_order_explicit": True if immediate else None,
            "injury_to_ASO_days_exact": None,
            "timing_category": "immediate_postinjury" if immediate else "unknown",
            "endpoint_days_after_injury": int(follow[1]),
            "endpoint_DIV": int(injury[1]) + int(follow[1]),
            "persistent_functional_deficit_eligibility_verified": None}


def workbook_metadata(path):
    """Emit metadata/counts only, never assume columns are differentiations."""
    selected = {"Figure 7f", "Figure 7g", "Figure 7h", "Figure 7i", "Figure 8b", "Figure 8c"}
    with zipfile.ZipFile(path) as z:
        wb = E.fromstring(z.read("xl/workbook.xml"))
        rels = {r.get("Id"): r.get("Target") for r in E.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
        shared = ["".join(x.itertext()) for x in E.fromstring(z.read("xl/sharedStrings.xml"))] if "xl/sharedStrings.xml" in z.namelist() else []
        result = []
        for sheet in wb.find("s:sheets", NS):
            name = sheet.get("name")
            if name not in selected:
                continue
            rid = sheet.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
            target = rels[rid]
            member = target.lstrip("/") if target.startswith("/") else "xl/" + target
            tree = E.fromstring(z.read(member))
            numeric, labels, formulas, explicit_times = Counter(), [], [], []
            for c in tree.findall(".//s:sheetData/s:row/s:c", NS):
                address = c.get("r")
                val = c.find("s:v", NS)
                form = c.find("s:f", NS)
                if form is not None:
                    formulas.append(address)
                if c.get("t") == "s" and val is not None:
                    labels.append({"cell": address, "text": shared[int(val.text)]})
                elif c.get("t") == "inlineStr":
                    labels.append({"cell": address, "text": "".join(c.find("s:is", NS).itertext())})
                elif c.get("t", "n") == "n" and val is not None and val.text:
                    numeric[re.match(r"[A-Z]+", address)[0]] += 1
                    if name.startswith("Figure 7") and re.fullmatch(r"A\d+", address):
                        explicit_times.append({"cell": address, "DIV": float(val.text)})
            result.append({"sheet": name, "xml_member": member,
                           "dimension": tree.find("s:dimension", NS).get("ref"),
                           "labels": labels, "numeric_cells_by_column_not_replicates": dict(numeric),
                           "explicit_DIV_labels_only_no_interpolation": explicit_times,
                           "formula_cells": formulas,
                           "experiment_or_differentiation_mapping_verified": False})
        if {r["sheet"] for r in result} != selected:
            raise ValueError("Selected source-data sheets missing")
        return {"total_sheets": len(wb.find("s:sheets", NS)), "selected_sheets": result}


def audit(pdf, workbook):
    raw = pdf.read_bytes()
    if not raw.startswith(b"%PDF-"):
        raise ValueError("Not a PDF")
    text = subprocess.check_output(["pdftotext", "-raw", str(pdf), "-"], text=True)
    if DOI not in text:
        raise ValueError("DOI not verified in PDF")
    pages = text.split("\f")
    t7, t8 = caption(text, 7), caption(text, 8)
    locator = lambda marker: [i + 1 for i, p in enumerate(pages) if marker in p]
    return {"doi": DOI, "pdf_sha256": hashlib.sha256(raw).hexdigest(),
            "workbook_sha256": hashlib.sha256(workbook.read_bytes()).hexdigest(),
            "figure7": {**timing7(t7), "pdf_pages": locator("Fig. 7 |"),
                        "normalized_caption_sha256": hashlib.sha256(normalize(t7).encode()).hexdigest(),
                        "scope": "f-i only; n not transferred from other panels",
                        "independent_experiments_reported": 3, "wells_range_reported": [3, 5],
                        "independent_differentiations_verified": None},
            "figure8": {**timing8(t8), "pdf_pages": locator("Fig. 8 |"),
                        "normalized_caption_sha256": hashlib.sha256(normalize(t8).encode()).hexdigest(),
                        "independent_experiments_reported": 2, "chips_range_reported": [3, 5],
                        "independent_differentiations_verified": None},
            "replication_numbers_method": "manual transcription from captions, visually verified; not independently reproduced experiments",
            "workbook": workbook_metadata(workbook),
            "new_effect_sizes_or_pvalues_computed": False,
            "clinical_efficacy_assessed": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path, default=ROOT / "data/cache/chan2026_reference.pdf")
    parser.add_argument("--workbook", type=Path, default=ROOT / "data/cache/chan2026_source_data.xlsx")
    parser.add_argument("--output", type=Path, default=ROOT / "reports/chan-timing/audit.json")
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(audit(args.pdf, args.workbook), ensure_ascii=False, indent=2) + "\n")
