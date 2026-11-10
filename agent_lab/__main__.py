"""Command line entrypoint: preview sources for free or opt into exactly four model calls."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys

from .memory import list_hypotheses, save_report
from .provider import OpenAIProvider, ProviderError
from .sources import fetch_pubmed
from .workflow import EvidenceError, run_lab


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", help="PubMed search, not an instruction to execute")
    parser.add_argument("--max-papers", type=int, default=5, choices=range(1, 9), metavar="1-8")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--preview", action="store_true", help="PubMed-only, zero model calls")
    mode.add_argument("--live", action="store_true", help="Four paid OpenAI API calls")
    mode.add_argument("--history", action="store_true", help="Read saved hypotheses, no network or model calls")
    parser.add_argument("--model", default=os.environ.get("ELA_LAB_MODEL", "gpt-6.1-terra"))
    parser.add_argument("--output", type=Path, help="Optional output JSON file (local only)")
    parser.add_argument("--database", type=Path, default=Path("data/ela-agent-lab.sqlite"),
                        help="Local SQLite store for --live and --history (gitignored by default)")
    args = parser.parse_args(argv)
    if not args.history and not args.query:
        parser.error("--query is required for --preview and --live")
    try:
        if args.history:
            print(json.dumps({"status": "UNVERIFIED_HYPOTHESIS_HISTORY",
                              "hypotheses": list_hypotheses(args.database)},
                             ensure_ascii=False, indent=2))
            return 0
        papers = fetch_pubmed(args.query, args.max_papers)
        if args.preview:
            result = {
                "status": "PUBMED_METADATA_PREVIEW_ONLY",
                "query": args.query,
                "model_calls": 0,
                "papers": [paper.to_dict() for paper in papers],
            }
        else:
            provider = OpenAIProvider(model=args.model)
            root = Path(__file__).resolve().parents[1]
            result = run_lab(args.query, papers, provider, root)
            result["memory_report_id"] = save_report(args.database, result)

        rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
            print(f"Wrote local draft: {args.output}")
        else:
            print(rendered)
        return 0
    except (ValueError, EvidenceError, ProviderError, OSError, json.JSONDecodeError) as exc:
        print(f"ELA Research Lab stopped: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
