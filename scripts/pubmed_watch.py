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
    # Restringido a TITLE_ABS el 10/11/2026: la consulta anterior
    # ('"amyotrophic lateral sclerosis" AND ("long-read" OR isoform)') buscaba en
    # todos los campos, incluidas las listas de referencias, y devolvía 11.040
    # resultados con artículos ajenos (APOE, prion, Huntington). La versión
    # restringida devuelve 42. No es un filtro de calidad: solo acota el campo.
    "long_reads": (
        '(TITLE_ABS:"amyotrophic lateral sclerosis" OR TITLE_ABS:"frontotemporal dementia"'
        ' OR TITLE_ABS:"TDP-43" OR TITLE_ABS:TARDBP)'
        ' AND (TITLE_ABS:"long-read" OR TITLE_ABS:"long read" OR TITLE_ABS:"Iso-Seq"'
        ' OR TITLE_ABS:nanopore OR TITLE_ABS:"PacBio" OR TITLE_ABS:"isoform-level"'
        ' OR TITLE_ABS:"full-length transcript")'
    ),
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

# Preprints whose peer-reviewed version we want to be told about. The timing
# matrix in reports/unc13a-intervention-timing-20261110 rests on preprints, and
# a peer-reviewed version is the free route to the independent review that the
# matrix still lacks. Titles are matched in TITLE, restricted to SRC:MED, so a
# hit means PubMed now indexes a non-preprint record.
TRACKED_PREPRINTS = {
    "Keuss UNC13A splice correction": "Loss of TDP-43 induces synaptic dysfunction",
    "Mallika multi-target rescue": "Restoring multiple TDP-43 cryptic targets",
    "Cao Unc13a memory": "Prevention of Unc13a cryptic splicing",
    "Guo cryptic splicing excitability": "Cryptic splicing in synaptic and membrane excitability genes",
    "Mehta U7 STMN2/UNC13A": "U7 small nuclear RNA splice-switching therapeutics",
    "Gomberg dual-targeting snRNA": "Dual-targeting snRNA gene therapy",
}


def check_published_versions():
    """Report tracked preprints that now have a PubMed-indexed version.

    A hit is a lead, not proof: title matching can collide, and the record must
    be read before any claim is attached to it. Failure to find one proves
    nothing about publication status.
    """
    found = {}
    for label, title in TRACKED_PREPRINTS.items():
        escaped = title.replace('"', "")
        records = search_pubmed(f'TITLE:"{escaped}"')
        if records:
            found[label] = [
                {"pmid": str(r["id"]),
                 "title": clean_title(r.get("title", "")),
                 "journal": clean_title(r.get("journalTitle", "")),
                 "date": r.get("firstPublicationDate", r.get("pubYear", "sin fecha"))}
                for r in records
            ]
    return found


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
    published = check_published_versions()
    lines += ["## Versiones revisadas por pares de preprints seguidos", ""]
    if not published:
        lines += ["Ninguno de los preprints seguidos tiene todavía un registro"
                  " indexado en PubMed. La ausencia no prueba que no esten"
                  " publicados.", ""]
    else:
        lines += ["Posible version revisada por pares. Verificar el registro"
                  " antes de atribuirle cualquier afirmacion:", ""]
        for label, hits in published.items():
            for h in hits:
                lines.append(
                    f"- {label}: PMID [{h['pmid']}]"
                    f"(https://pubmed.ncbi.nlm.nih.gov/{h['pmid']}/)"
                    f" — {h['title']} ({h['journal']}, {h['date']})")
        lines.append("")

    REPORTS.mkdir(parents=True, exist_ok=True)
    report = REPORTS / f"{date}-pubmed.md"
    if new_ids or published or not report.exists():
        report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(sorted(previous | seen, key=int), indent=2) + "\n", encoding="utf-8")
    print(f"Europe PMC SRC:MED: checked {len(seen)} PMID, new {len(new_ids)}, "
          f"tracked preprints with a PubMed record: {len(published)}.")

if __name__ == "__main__":
    main()
