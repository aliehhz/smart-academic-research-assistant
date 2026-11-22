"""Command-line entry point for the document Q&A assistant."""
from __future__ import annotations

import argparse
import os
import sys
from print_format import format_farsi
from router import route_query
from summarizer import summarize_document

from pycallgraph2 import PyCallGraph, Config
from pycallgraph2.output import GraphvizOutput

# مشخص کردن مسیر خروجی عکس
output = GraphvizOutput(output_file='call_graph.png')
config = Config(include=["*.main.*", "*.router.*", "*.summarizer.*", "*.rag_chain.*", "*.llm_service.*", "*.pdf_reasder.*", "*.config.*", "*.vectore_store.*"])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ask questions about the processed document.")
    parser.add_argument("query", nargs="*", help="Question or explicit request to summarize the document")
    parser.add_argument(
        "--distance-threshold",
        type=float,
        default=float(os.environ.get("DISTANCE_THRESHOLD", "1.8")),
        help="Maximum retrieval distance considered relevant (default: DISTANCE_THRESHOLD or 0.5)",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=int(os.environ.get("TOP_K", "3")),
        help="Number of chunks to retrieve (default: TOP_K or 3)",
    )
    return parser


def answer_query(query: str, *, distance_threshold: float = 0.5, top_k: int = 3) -> str:
    """Route a user query to document summarization or retrieval-augmented answering."""
    return route_query(
        query,
        summarize=summarize_document,
        distance_threshold=distance_threshold,
        top_k=top_k,
    )


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.distance_threshold < 0:
        print("--distance-threshold must be non-negative.", file=sys.stderr)
        return 2
    if args.top_k < 1:
        print("--top-k must be at least 1.", file=sys.stderr)
        return 2

    query = " ".join(args.query).strip()
    if not query:
        try:
            query = input("پرسش خود را وارد کنید: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0

    print(answer_query(query, distance_threshold=args.distance_threshold, top_k=args.top_k))
    return 0

if __name__ == "__main__":
    #with PyCallGraph(output=output):
    #    raise SystemExit(main())
    raise SystemExit(main())
