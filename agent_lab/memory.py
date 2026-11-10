"""SQLite research memory: immutable, queryable drafts; no clinical or private data."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import re
import sqlite3


SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS reports (
    report_id TEXT PRIMARY KEY,
    created_at_utc TEXT NOT NULL,
    question TEXT NOT NULL,
    status TEXT NOT NULL,
    source_sha256 TEXT NOT NULL,
    report_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS papers (
    pmid TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    year TEXT NOT NULL,
    journal TEXT NOT NULL,
    doi TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS report_papers (
    report_id TEXT NOT NULL REFERENCES reports(report_id),
    pmid TEXT NOT NULL REFERENCES papers(pmid),
    PRIMARY KEY (report_id, pmid)
);
CREATE TABLE IF NOT EXISTS hypotheses (
    report_id TEXT NOT NULL REFERENCES reports(report_id),
    ordinal INTEGER NOT NULL,
    statement TEXT NOT NULL,
    prediction TEXT NOT NULL,
    falsifier TEXT NOT NULL,
    proposed_test TEXT NOT NULL,
    required_data TEXT NOT NULL,
    pmids_json TEXT NOT NULL,
    PRIMARY KEY (report_id, ordinal)
);
"""


def save_report(db_path: Path, report: dict) -> str:
    """Persist only fully completed draft reports; content-addressed and idempotent."""
    if report.get("status") != "DRAFT_REQUIRES_HUMAN_REVIEW":
        raise ValueError("Only human-review drafts can be stored")
    papers = report.get("papers", [])
    hypotheses = report.get("agents", {}).get("hypothesis", {}).get("hypotheses", [])
    allowed = {paper.get("pmid") for paper in papers}
    if not papers or not all(isinstance(pmid, str) and re.fullmatch(r"[0-9]+", pmid)
                             for pmid in allowed):
        raise ValueError("Missing or malformed PMIDs")
    for hypothesis in hypotheses:
        refs = hypothesis.get("pmids")
        if not isinstance(refs, list) or not refs or any(pmid not in allowed for pmid in refs):
            raise ValueError("Unverified hypothesis citation")
    serialized = json.dumps(report, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    report_id = sha256(serialized.encode("utf-8")).hexdigest()
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as db:
        db.executescript(SCHEMA)
        db.execute(
            "INSERT OR IGNORE INTO reports VALUES (?, ?, ?, ?, ?, ?)",
            (report_id, report["generated_at_utc"], report["question"],
             report["status"], report["source_metadata_sha256"], serialized),
        )
        for paper in papers:
            db.execute(
                "INSERT OR IGNORE INTO papers VALUES (?, ?, ?, ?, ?)",
                (paper["pmid"], paper["title"], paper["year"], paper["journal"], paper["doi"]),
            )
            db.execute(
                "INSERT OR IGNORE INTO report_papers VALUES (?, ?)",
                (report_id, paper["pmid"]),
            )
        for index, hypothesis in enumerate(hypotheses, start=1):
            db.execute(
                "INSERT OR IGNORE INTO hypotheses VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (report_id, index, hypothesis["statement"], hypothesis["prediction"],
                 hypothesis["falsifier"], hypothesis["proposed_test"],
                 hypothesis["required_data"], json.dumps(hypothesis["pmids"])),
            )
    return report_id


def list_hypotheses(db_path: Path, limit: int = 20) -> list[dict]:
    """Read-only list of candidate hypotheses; they remain unverified drafts."""
    if not 1 <= limit <= 100:
        raise ValueError("limit must be within 1..100")
    with sqlite3.connect(db_path) as db:
        db.row_factory = sqlite3.Row
        rows = db.execute(
            "SELECT h.report_id, h.ordinal, r.created_at_utc, r.question, "
            "h.statement, h.prediction, h.falsifier, h.pmids_json "
            "FROM hypotheses h JOIN reports r ON r.report_id=h.report_id "
            "ORDER BY r.created_at_utc DESC LIMIT ?", (limit,),
        ).fetchall()
    return [
        {**dict(row), "pmids": json.loads(row["pmids_json"])}
        for row in rows
    ]
