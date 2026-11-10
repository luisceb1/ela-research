"""Small, bounded PubMed adapter. No full-text download or patient data."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import os
import re
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
MAX_PAPERS = 8
MAX_RESPONSE_BYTES = 3_000_000


@dataclass(frozen=True)
class Paper:
    pmid: str
    title: str
    abstract: str
    year: str
    journal: str
    doi: str

    def to_dict(self) -> dict:
        data = asdict(self)
        data["url"] = f"https://pubmed.ncbi.nlm.nih.gov/{self.pmid}/"
        return data


def _fetch(endpoint: str, params: dict[str, str]) -> bytes:
    if endpoint not in {"esearch.fcgi", "efetch.fcgi"}:
        raise ValueError("Only approved PubMed endpoints are allowed")
    payload = dict(params)
    payload["tool"] = "ELAResearchLab"
    if os.environ.get("NCBI_EMAIL"):
        payload["email"] = os.environ["NCBI_EMAIL"]
    if os.environ.get("NCBI_API_KEY"):
        payload["api_key"] = os.environ["NCBI_API_KEY"]
    url = BASE + endpoint + "?" + urlencode(payload)
    req = Request(url, headers={"User-Agent": "ELAResearchLab/0.1 (academic research)"})
    with urlopen(req, timeout=25) as resp:
        body = resp.read(MAX_RESPONSE_BYTES + 1)
    if len(body) > MAX_RESPONSE_BYTES:
        raise ValueError("PubMed response exceeded the size limit")
    return body


def _clean(element: ET.Element | None) -> str:
    if element is None:
        return ""
    return " ".join("".join(element.itertext()).split())


def fetch_pubmed(query: str, limit: int = 5) -> list[Paper]:
    """Fetch at most 8 public PubMed records, without relying on model-generated citations."""
    if not query or len(query) > 300:
        raise ValueError("query must contain 1-300 characters")
    if not 1 <= limit <= MAX_PAPERS:
        raise ValueError("limit must be between 1 and 8")
    result = json.loads(_fetch("esearch.fcgi", {
        "db": "pubmed", "term": query, "retmode": "json",
        "retmax": str(limit), "sort": "relevance",
    }))
    ids = result.get("esearchresult", {}).get("idlist", [])
    ids = [str(pmid) for pmid in ids if re.fullmatch(r"[0-9]+", str(pmid))]
    ids = list(dict.fromkeys(ids))[:limit]
    if not ids:
        return []

    raw = _fetch("efetch.fcgi", {
        "db": "pubmed", "id": ",".join(ids),
        "retmode": "xml", "rettype": "abstract",
    })
    root = ET.fromstring(raw)
    found = {}
    for record in root.findall(".//PubmedArticle"):
        citation = record.find("MedlineCitation")
        if citation is None:
            continue
        pmid = _clean(citation.find("PMID"))
        if pmid not in ids:
            continue
        article = citation.find("Article")
        if article is None:
            continue
        abstract_el = article.find("Abstract")
        abstract = " ".join(_clean(a) for a in abstract_el.findall("AbstractText")) if abstract_el is not None else ""
        year = _clean(article.find("./Journal/JournalIssue/PubDate/Year"))
        if not year:
            pubdate = _clean(article.find("./Journal/JournalIssue/PubDate/MedlineDate"))
            year_match = re.search(r"\b(19|20)\d{2}\b", pubdate)
            year = year_match.group(0) if year_match else ""
        doi = ""
        for article_id in record.findall("./PubmedData/ArticleIdList/ArticleId"):
            if article_id.attrib.get("IdType") == "doi":
                doi = _clean(article_id)
                break
        found[pmid] = Paper(
            pmid=pmid,
            title=_clean(article.find("ArticleTitle")),
            abstract=abstract[:4000],
            year=year,
            journal=_clean(article.find("./Journal/Title")),
            doi=doi,
        )
    return [found[pmid] for pmid in ids if pmid in found]
