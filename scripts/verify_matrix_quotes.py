#!/usr/bin/env python3
"""Verify that every quoted fragment in a matrix's locator column exists in its source.

Mechanical audit step: it checks transcription fidelity only. It cannot judge
whether a classification is correct, and a PASS is not scientific validation.

Each row's `source_id` is mapped to a source text file by a mapping file
(JSON: {"S1": "path/to/PMC11230273.xml", ...}). JATS XML is reduced to text.
Quoted fragments are compared after aggressive normalisation (whitespace,
curly quotes, dashes, soft hyphens, superscript digits), because PDF and XML
extraction reflow lines and mangle punctuation.

Exit status is 1 if any fragment is missing, so this can gate CI.

Usage:
  python -I scripts/verify_matrix_quotes.py MATRIX.tsv --sources MAP.json [--json]
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

QUOTED = re.compile(r'"([^"]{12,})"')

_PUNCT = {
    "‘": "'", "’": "'", "“": '"', "”": '"',
    "–": "-", "—": "-", "−": "-", "­": "",
    " ": " ", " ": " ", " ": " ", "​": "",
    # Greek mu and micro sign are routinely transliterated as "u" when quoting.
    "μ": "u", "µ": "u",
}


def normalise(text: str) -> str:
    """Collapse the differences that PDF/XML extraction introduces."""
    text = unicodedata.normalize("NFKD", text)
    for src, dst in _PUNCT.items():
        text = text.replace(src, dst)
    # Drop combining marks and superscript reference digits glued to words.
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


# Lines a preprint PDF interleaves into the body text, which break otherwise
# contiguous sentences. Dropping them is required for quote matching to mean
# anything; it never joins text across a real section boundary because the
# boilerplate sits inside the page margin, not in the prose.
BOILERPLATE = re.compile(
    r"bioRxiv preprint doi|copyright holder for this|No reuse allowed"
    r"|available under a|CC-BY|perpetuity|is the author/funder"
    r"|All rights reserved|was not certified by peer review",
    re.IGNORECASE,
)
# Leading line numbers in a line-numbered manuscript ("139    text...").
LINE_NUMBER = re.compile(r"^\s*\d{1,4}(?=\s{2,}\S)")


def clean_pdf_text(text: str) -> str:
    kept = []
    for line in text.splitlines():
        if BOILERPLATE.search(line):
            continue
        kept.append(LINE_NUMBER.sub("", line))
    return "\n".join(kept)


def load_source(path: Path) -> str:
    raw = path.read_bytes()
    if path.suffix.lower() in {".xml", ".nxml"}:
        try:
            root = ET.fromstring(raw)
        except ET.ParseError:
            return normalise(raw.decode("utf-8", "replace"))
        return normalise(" ".join(root.itertext()))
    return normalise(clean_pdf_text(raw.decode("utf-8", "replace")))


def verify(matrix: Path, mapping: dict[str, str], base: Path) -> dict:
    sources: dict[str, str] = {}
    results = []
    with matrix.open(newline="", encoding="utf-8") as fh:
        # QUOTE_NONE: the locator column contains literal double quotes around
        # transcribed fragments. Default csv quoting would strip them and the
        # audit would silently find nothing to check.
        rows = list(csv.DictReader(fh, delimiter="\t", quoting=csv.QUOTE_NONE))
    for row in rows:
        sid = row["source_id"]
        locator = row.get("locator", "")
        fragments = QUOTED.findall(locator)
        if sid not in mapping:
            results.append({"source_id": sid, "experiment": row["experiment"],
                            "status": "NO_SOURCE_MAPPED", "fragments": len(fragments)})
            continue
        if sid not in sources:
            sources[sid] = load_source(base / mapping[sid])
        haystack = sources[sid]
        checked = []
        for frag in fragments:
            needle = normalise(frag)
            checked.append({"fragment": frag[:90], "found": needle in haystack})
        status = "NO_QUOTES" if not checked else (
            "PASS" if all(c["found"] for c in checked) else "MISSING")
        results.append({"source_id": sid, "experiment": row["experiment"],
                        "classification": row.get("classification", ""),
                        "status": status, "checked": checked})
    missing = sum(1 for r in results if r["status"] in {"MISSING", "NO_SOURCE_MAPPED"})
    return {"matrix": matrix.name, "rows": len(rows), "rows_with_problems": missing,
            "results": results}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("matrix", type=Path)
    ap.add_argument("--sources", type=Path, required=True,
                    help="JSON map of source_id -> source text path")
    ap.add_argument("--base", type=Path, default=Path("."),
                    help="Directory the mapped paths are relative to")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    mapping = json.loads(args.sources.read_text(encoding="utf-8"))
    out = verify(args.matrix, mapping, args.base)
    if args.json:
        json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
        print()
    else:
        print(f"# {out['matrix']}: {out['rows']} rows, "
              f"{out['rows_with_problems']} with problems")
        for r in out["results"]:
            print(f"[{r['status']}] {r['source_id']} {r['experiment']}")
            for c in r.get("checked", []):
                if not c["found"]:
                    print(f"    MISSING: {c['fragment']}")
    return 1 if out["rows_with_problems"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
