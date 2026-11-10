#!/usr/bin/env python3
"""Locate timing sentences in a JATS full-text XML (Europe PMC fullTextXML).

Documentary helper for reports/unc13a-intervention-timing-20261110. It does not
classify anything: it lists sentences that mention an intervention or a
TDP-43 perturbation together with a time marker, with section titles and
SHA256 of the input, so that a reader can transcribe the chronology with a
verifiable locator. Classification remains a human/agent reading step.

Usage: python -I scripts/extract_intervention_timing.py ARTICLE.xml [--json]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

INTERVENTION = re.compile(
    r"\b(ASOs?|antisense|oligonucleotides?|U7|snRNA|AAV[-\w.]*|PHP\.eB|"
    r"shRNA|siRNA|doxycycline|dox\b|tamoxifen|CRISPR|knock-?(?:in|down)|"
    r"treat(?:ed|ment)|transduc\w*|inject\w*|deliver\w*|dCas\w*|repressor)\b",
    re.IGNORECASE,
)
TIME = re.compile(
    r"\b(day|days|DIV|d\d+|D\d+|week|weeks|wk|month|months|postnatal|P\d+|"
    r"hours?|h\b|baseline|onset|prior to|before|after|following|age)\b",
    re.IGNORECASE,
)
SENTENCE = re.compile(r"(?<=[.;])\s+(?=[A-Z(])")


def text_of(elem: ET.Element) -> str:
    return " ".join("".join(elem.itertext()).split())


def iter_paragraphs(root: ET.Element):
    """Yield (section path, paragraph text) for body paragraphs and figure captions."""

    def walk(elem: ET.Element, path: tuple[str, ...]):
        for child in elem:
            tag = child.tag.split("}")[-1]
            if tag == "sec":
                title = child.find("title")
                yield from walk(child, path + ((text_of(title) if title is not None else "?"),))
            elif tag == "p":
                yield " > ".join(path) or "(root)", text_of(child)
            elif tag in {"fig", "table-wrap"}:
                cap = child.find("caption")
                label = child.find("label")
                if cap is not None:
                    name = text_of(label) if label is not None else tag
                    yield " > ".join(path + (name,)), text_of(cap)
            else:
                yield from walk(child, path)

    body = root.find(".//body")
    if body is not None:
        yield from walk(body, ())
    back = root.find(".//back")
    if back is not None:
        yield from walk(back, ("back",))


def find_timing_sentences(xml_bytes: bytes) -> list[dict]:
    root = ET.fromstring(xml_bytes)
    hits = []
    for section, para in iter_paragraphs(root):
        for sent in SENTENCE.split(para):
            if INTERVENTION.search(sent) and TIME.search(sent):
                hits.append({"section": section, "sentence": sent.strip()})
    return hits


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("xml", type=Path)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    data = args.xml.read_bytes()
    hits = find_timing_sentences(data)
    out = {"file": args.xml.name, "sha256": hashlib.sha256(data).hexdigest(),
           "bytes": len(data), "n_hits": len(hits), "hits": hits}
    if args.json:
        json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
        print()
    else:
        print(f"# {out['file']} sha256={out['sha256']} bytes={out['bytes']} hits={out['n_hits']}")
        for h in hits:
            print(f"[{h['section']}] {h['sentence']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
