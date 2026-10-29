#!/usr/bin/env python3
"""Inventario automático de registros PubMed mediante Europe PMC (SRC:MED)."""
import datetime as dt
import html
import json
import re
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state/seen_pubmed_ids.json"
REPORTS = ROOT / "reports"
BASE = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
QUERIES = {
    "STMN2_UNC13A": '(TARDBP OR "TDP-43") AND (STMN2 OR UNC13A)',
    "cryptic_splicing": '(TARDBP OR "TDP-43") AND ("cryptic exon" OR "cryptic splicing")',
    "long_reads": '"amyotrophic lateral sclerosis" AND ("long-read" OR isoform)',
}

def request_json(url):
    """Retry transient network failures; do not retry invalid responses."""
    req = Request(url, headers={"User-Agent": "ELAResearchWatcher/0.2 (bibliographic metadata)"})
    for retry in range(4):
        try:
            with urlopen(req, timeout=35) as response:
                return json.load(response)
        except HTTPError as exc:
            if exc.code not in (429, 500, 502, 503, 504) or retry == 3:
                raise
        except (URLError, TimeoutError):
            if retry == 3:
                raise
        time.sleep((1, 3, 9)[retry])
    raise RuntimeError("Unreachable retry state")

def search_pubmed(query):
    params = {
        "query": f"({query}) AND SRC:MED",
        "format": "json",
        "resultType": "lite",
        "pageSize": 25,
        "sort": "P_PDATE_D desc",
    }
    url = BASE + "?" + urlencode(params)
    data = request_json(url)
    if not isinstance(data, dict) or not isinstance(data.get("resultList"), dict):
        raise ValueError("Invalid Europe PMC response: resultList missing")
    records = data["resultList"].get("result")
    if not isinstance(records, list):
        raise ValueError("Invalid Europe PMC response: result missing")
    return [r for r in records if r.get("source") == "MED" and str(r.get("id", "")).isdigit()]

def clean_title(title):
    """Escape untrusted bibliographic text before Markdown reporting."""
    plain = html.unescape(re.sub(r"<[^>]*>", "", str(title)))
    return re.sub(r"\s+", " ", plain).replace("[", r"\[").replace("]", r"\]").strip()[:500]

def main():
    previous = set(json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else [])
    categories, details, seen = {}, {}, set()
    for name, query in QUERIES.items():
        records = search_pubmed(query)
        categories[name] = [str(item["id"]) for item in records]
        for item in records:
            pmid = str(item["id"])
            details[pmid] = item
            seen.add(pmid)
    new_ids = seen - previous
    date = dt.datetime.now(dt.timezone.utc).date().isoformat()
    lines = [
        f"# Publicaciones PubMed — {date}", "",
        "Fuente: Europe PMC REST API, filtrada por SRC:MED (registros PubMed).",
        "Metadatos automatizados no equivalen a lectura crítica o validación científica.",
        "", f"Identificadores nuevos desde la última comprobación: {len(new_ids)}", ""
    ]
    for name, ids in categories.items():
        lines += [f"## {name}", ""]
        selected = [x for x in ids if x in new_ids]
        if not selected:
            lines += ["Sin PMID nuevos en los últimos 25 resultados recuperados.", ""]
        for pmid in selected:
            item = details[pmid]
            title = clean_title(item.get("title", "Título no recuperado"))
            date_text = item.get("firstPublicationDate", item.get("pubYear", "sin fecha"))
            lines.append(f"- PMID [{pmid}](https://pubmed.ncbi.nlm.nih.gov/{pmid}/) — {title} ({date_text})")
        lines.append("")
    REPORTS.mkdir(parents=True, exist_ok=True)
    report = REPORTS / f"{date}-pubmed.md"
    if new_ids or not report.exists():
        report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(sorted(previous | seen, key=int), indent=2) + "\n", encoding="utf-8")
    print(f"Europe PMC SRC:MED: checked {len(seen)} PMID, new {len(new_ids)}.")

if __name__ == "__main__":
    main()
