"""UNC13A evidence benchmark: deterministic controls and optional LIVE PubMed source check.

No LLM calls, no downloaded alignments, no patient data, no article scraping.
Labels assess what is justified by the PubMed ABSTRACT, not global truth.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys
from time import sleep

from .sources import MAX_PAPERS, fetch_pubmed
from .provider import ProviderError


BENCHMARK = Path(__file__).parent / "benchmarks" / "unc13a_v01.json"
CORPUS = Path(__file__).parent / "benchmarks" / "tdp43_primary_corpus_v01.json"
LABELS = {"supported", "contradicted", "insufficient"}


class BenchmarkError(ValueError):
    pass


def load_benchmark(path: Path = BENCHMARK) -> dict:
    benchmark = json.loads(path.read_text(encoding="utf-8"))
    sources = benchmark["sources"]
    cases = benchmark["cases"]
    ids = [case["id"] for case in cases]
    pmids = [source["pmid"] for source in sources]
    if benchmark.get("version") != "v0.1":
        raise BenchmarkError("Unexpected benchmark version")
    if len(ids) != 20 or len(set(ids)) != 20:
        raise BenchmarkError("Benchmark must contain exactly 20 unique cases")
    if not 1 <= len(pmids) <= MAX_PAPERS or len(pmids) != len(set(pmids)):
        raise BenchmarkError("Source identifiers must be unique and within PubMed limit")
    if any(not re.fullmatch(r"\d+", pmid) for pmid in pmids):
        raise BenchmarkError("PMIDs must be numeric")
    for case in cases:
        if case.get("pmid") not in pmids:
            raise BenchmarkError(f"Unverified source in case {case.get('id')}")
        if case.get("expected") not in LABELS:
            raise BenchmarkError(f"Unexpected label in {case.get('id')}")
        if case.get("scope") != "PubMed abstract":
            raise BenchmarkError("Cannot silently change evidence scope")
        if not case.get("claim") or not case.get("focus"):
            raise BenchmarkError("Empty claim or scientific focus")
    return benchmark


def score_predictions(benchmark: dict, predictions: dict) -> dict:
    """Score externally generated decisions; does NOT validate scientific truth."""
    gold = {case["id"]: case["expected"] for case in benchmark["cases"]}
    rows = predictions.get("predictions")
    if not isinstance(rows, list) or len(rows) != len(gold):
        raise BenchmarkError("Supply exactly one prediction per benchmark case")
    received = {}
    for row in rows:
        if not isinstance(row, dict) or row.get("id") not in gold:
            raise BenchmarkError("Unknown benchmark case")
        case_id = row["id"]
        if case_id in received:
            raise BenchmarkError(f"Duplicate predicted case {case_id}")
        if row.get("decision") not in LABELS:
            raise BenchmarkError(f"Invalid decision for {case_id}")
        if not isinstance(row.get("reason"), str) or not row["reason"].strip():
            raise BenchmarkError(f"Missing audit explanation for {case_id}")
        received[case_id] = row["decision"]
    confusion = Counter((gold[key], received[key]) for key in gold)
    false_support = [
        key for key in gold
        if received[key] == "supported" and gold[key] != "supported"
    ]
    return {
        "status": "LABEL_AGREEMENT_ONLY_NOT_SCIENTIFIC_VALIDATION",
        "total": len(gold),
        "correct": sum(gold[key] == received[key] for key in gold),
        "accuracy": sum(gold[key] == received[key] for key in gold) / len(gold),
        "confusion": [
            {"expected": a, "predicted": b, "count": n}
            for (a, b), n in sorted(confusion.items())
        ],
        "unsafe_overclaims": false_support,
        "no_overclaims": len(false_support) == 0,
        "warnings": [
            "Gold labels have not yet passed a second independent curator review",
            "PMID citation correctness is not evidence of claim correctness",
            "No biological inference, replication or patient benefit is assessed here",
        ],
    }


def check_pubmed_sources(benchmark: dict) -> dict:
    """Query the LIVE NCBI E-utilities endpoint for all fixed PMIDs.

    This method is never called by offline tests. It does not run model calls.
    """
    expected = {source["pmid"]: source for source in benchmark["sources"]}
    query = " OR ".join(f"{pmid}[PMID]" for pmid in expected)
    papers = fetch_pubmed(query, limit=len(expected))
    found = {paper.pmid: paper for paper in papers}
    rows = []
    for pmid, source in expected.items():
        item = found.get(pmid)
        doi_expected = source.get("doi", "").lower()
        doi_live = item.doi.lower() if item else ""
        rows.append({
            "pmid": pmid,
            "source": source["short"],
            "found": item is not None,
            "has_abstract": bool(item and item.abstract),
            "doi_matches_if_specified": bool(item and (not doi_expected or doi_live == doi_expected)),
            "live_title": item.title if item else "",
            "live_doi": item.doi if item else "",
            "live_year": item.year if item else "",
        })
    passed = all(
        row["found"] and row["has_abstract"] and row["doi_matches_if_specified"]
        for row in rows
    )
    return {
        "status": "LIVE_PUBMED_SOURCE_CHECK_PASS" if passed else "LIVE_PUBMED_SOURCE_CHECK_FAIL",
        "query": query,
        "expected_sources": len(expected),
        "retrieved_sources": len(found),
        "items": rows,
        "model_calls": 0,
        "warnings": [
            "Live PubMed response verifies identity, DOI and abstract presence only",
            "The scientific benchmark labels and complete article interpretations remain unvalidated",
        ],
    }



def load_corpus(path: Path = CORPUS) -> dict:
    """Validate a 20-publication review corpus; never equate versions of one work."""
    corpus = json.loads(path.read_text(encoding="utf-8"))
    sources = corpus["sources"]
    pmids = [source["pmid"] for source in sources]
    if corpus.get("version") != "v0.1" or len(sources) != 20 or len(set(pmids)) != 20:
        raise BenchmarkError("Expected 20 distinct PubMed identifiers for corpus v0.1")
    if len({source["independent_study_id"] for source in sources}) != 20:
        raise BenchmarkError("Corpus contains multiple versions of the same study")
    if any(not re.fullmatch(r"\d+", pmid) for pmid in pmids):
        raise BenchmarkError("Invalid PMID in corpus")
    if any(source["kind"] not in {"preprint", "journal"} for source in sources):
        raise BenchmarkError("Unexpected publication status")
    return corpus


def check_full_corpus(corpus: dict) -> dict:
    """Retrieve source metadata in three capped NCBI requests of 8, 8 and 4 papers."""
    sources = corpus["sources"]
    rows = []
    for offset in range(0, len(sources), MAX_PAPERS):
        if offset:
            sleep(0.8)  # NCBI default policy: at most 3 E-utils requests/second.
        group = sources[offset:offset + MAX_PAPERS]
        query = " OR ".join(f'{source["pmid"]}[PMID]' for source in group)
        live = {paper.pmid: paper for paper in fetch_pubmed(query, limit=len(group))}
        for source in group:
            paper = live.get(source["pmid"])
            expected_doi = source.get("doi", "").lower()
            rows.append({
                "pmid": source["pmid"],
                "short": source["short"],
                "priority": source["priority"],
                "found": paper is not None,
                "has_abstract": bool(paper and paper.abstract),
                "doi_matches_if_specified": bool(
                    paper and (not expected_doi or paper.doi.lower() == expected_doi)
                ),
                "title": paper.title if paper else "",
                "doi": paper.doi if paper else "",
            })
    passed = all(row["found"] and row["has_abstract"] and row["doi_matches_if_specified"]
                 for row in rows)
    return {
        "status": "LIVE_20_PUBMED_SOURCE_CHECK_PASS" if passed else "LIVE_20_PUBMED_SOURCE_CHECK_FAIL",
        "expected_sources": 20,
        "verified_sources": sum(
            row["found"] and row["has_abstract"] and row["doi_matches_if_specified"]
            for row in rows
        ),
        "batches": 3,
        "model_calls": 0,
        "items": rows,
        "warnings": [
            "Presence and identity only; scientific interpretation and independent replication are NOT validated",
            "Preprints are not peer reviewed, even when indexed by PubMed",
        ],
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--validate", action="store_true", help="Offline schema and reference validation")
    mode.add_argument("--score", type=Path, metavar="PREDICTIONS.json",
                      help="Offline comparison with 20 author-curated label controls")
    mode.add_argument("--validate-corpus", action="store_true", help="Offline check of 20-paper register")
    mode.add_argument("--check-corpus", action="store_true", help="LIVE three-batch retrieval of 20 PubMed records")
    mode.add_argument("--evaluate-model", action="store_true",
                      help="One PAID Responses API model call to evaluate 20 gold-blind claims")
    mode.add_argument("--source-check", action="store_true",
                      help="LIVE PubMed source retrieval, no model API or spending")
    parser.add_argument("--output", type=Path, help="Write a local JSON report")
    parser.add_argument("--model", default=None,
                        help="Model for --evaluate-model (default gpt-6.1-terra)")
    args = parser.parse_args(argv)
    try:
        benchmark = load_benchmark()
        if args.validate:
            report = {
                "status": "OFFLINE_BENCHMARK_SCHEMA_VALID",
                "cases": len(benchmark["cases"]),
                "sources": len(benchmark["sources"]),
                "distribution": dict(sorted(Counter(
                    case["expected"] for case in benchmark["cases"]
                ).items())),
                "model_calls": 0,
            }
        elif args.score:
            report = score_predictions(benchmark, json.loads(
                args.score.read_text(encoding="utf-8")))
        elif args.validate_corpus:
            corpus = load_corpus()
            report = {"status": "OFFLINE_20_PAPER_CORPUS_SCHEMA_VALID",
                      "records": len(corpus["sources"]), "model_calls": 0}
        elif args.check_corpus:
            report = check_full_corpus(load_corpus())
        elif args.evaluate_model:
            # Explicitly selected: ONE paid model call after source identity checks.
            from .evaluation import evaluate_benchmark
            from .provider import OpenAIProvider
            ids = [source["pmid"] for source in benchmark["sources"]]
            query = " OR ".join(f"{pmid}[PMID]" for pmid in ids)
            papers = fetch_pubmed(query, limit=len(ids))
            report = evaluate_benchmark(benchmark, papers, OpenAIProvider(model=args.model))
        else:
            report = check_pubmed_sources(benchmark)
        rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
        print(rendered)
        return 1 if report["status"] in {
            "LIVE_PUBMED_SOURCE_CHECK_FAIL", "LIVE_20_PUBMED_SOURCE_CHECK_FAIL"
        } else 0
    except (BenchmarkError, ProviderError, ValueError, KeyError, OSError, TimeoutError) as exc:
        print(f"Benchmark stopped: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
