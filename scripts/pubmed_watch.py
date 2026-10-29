#!/usr/bin/env python3
"""Vigilancia de publicaciones PubMed; no implica evaluación científica."""
import datetime as dt
import json
import os
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state/seen_pubmed_ids.json"
REPORTS = ROOT / "reports"
QUERIES = {
    "STMN2_UNC13A": '(TARDBP[All Fields] OR "TDP-43"[All Fields]) AND (STMN2[All Fields] OR UNC13A[All Fields])',
    "cryptic_splicing": '(TARDBP[All Fields] OR "TDP-43"[All Fields]) AND ("cryptic exon"[All Fields] OR "cryptic splicing"[All Fields])',
    "long_reads": '"amyotrophic lateral sclerosis"[All Fields] AND ("long-read"[All Fields] OR "isoform"[All Fields])',
}

def fetch(endpoint, params):
    params = dict(params)
    params["tool"] = "ELAResearchWatcher"
    if os.environ.get("NCBI_CONTACT_EMAIL"):
        params["email"] = os.environ["NCBI_CONTACT_EMAIL"]
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/" + endpoint + "?" + urlencode(params)
    req = Request(url, headers={"User-Agent": "ELAResearchWatcher/0.1"})
    with urlopen(req, timeout=30) as response:
        return json.load(response)

def main():
    previous = set(json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else [])
    categories, ids_seen = {}, set()
    for label, query in QUERIES.items():
        payload = fetch("esearch.fcgi", {
            "db": "pubmed", "term": query, "sort": "pub date",
            "retmax": 25, "retmode": "json"
        })
        ids = payload["esearchresult"]["idlist"]
        categories[label] = ids
        ids_seen.update(ids)
    fresh = sorted(ids_seen - previous, key=int)
    details = {}
    for offset in range(0, len(fresh), 50):
        chunk = fresh[offset:offset+50]
        payload = fetch("esummary.fcgi", {
            "db": "pubmed", "id": ",".join(chunk), "retmode": "json"
        })
        details.update(payload.get("result", {}))
    date = dt.datetime.now(dt.timezone.utc).date().isoformat()
    lines = [f"# PubMed — {date}", "",
             "Solo inventario automático: no significa que los trabajos sean concluyentes.",
             "", f"PMIDs nuevos respecto al registro: {len(fresh)}", ""]
    for category, ids in categories.items():
        lines.extend([f"## {category}", ""])
        selected = [x for x in ids if x in fresh]
        if not selected:
            lines.extend(["No se identificaron PMID nuevos entre los 25 registros consultados.", ""])
        for pmid in selected:
            data = details.get(pmid, {})
            title = str(data.get("title", "Título desconocido")).replace("\n", " ")
            lines.append(f"- [{pmid}](https://pubmed.ncbi.nlm.nih.gov/{pmid}/) — {title} ({data.get('pubdate', 'fecha desconocida')})")
        if selected:
            lines.append("")
    REPORTS.mkdir(parents=True, exist_ok=True)
    path = REPORTS / f"{date}-pubmed.md"
    if fresh or not path.exists():
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(sorted(previous | ids_seen, key=int), indent=2) + "\n", encoding="utf-8")
    print(f"Reviewed {len(ids_seen)} PubMed identifiers; {len(fresh)} new.")

if __name__ == "__main__":
    main()
