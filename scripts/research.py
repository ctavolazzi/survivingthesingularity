#!/usr/bin/env python3
"""
research.py — web research tool for STS content

Usage:
  python research.py "AI milestones 2025"
  python research.py "humanoid robots factory deployment" --n 10
  python research.py "AGI timeline predictions" --format timeline
  python research.py --interactive

Requires:
  pip install duckduckgo-search httpx rich
"""

import argparse
import json
import sys
from datetime import datetime


def search(query: str, n: int = 8) -> list[dict]:
    try:
        try:
            from ddgs import DDGS
        except ImportError:
            from duckduckgo_search import DDGS
    except ImportError:
        print("Run: pip install duckduckgo-search")
        sys.exit(1)

    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=n))
    return results


def search_news(query: str, n: int = 8) -> list[dict]:
    try:
        try:
            from ddgs import DDGS
        except ImportError:
            from duckduckgo_search import DDGS
    except ImportError:
        print("Run: pip install duckduckgo-search")
        sys.exit(1)

    with DDGS() as ddgs:
        results = list(ddgs.news(query, max_results=n))
    return results


def print_results(results: list[dict], fmt: str = "plain"):
    try:
        from rich.console import Console
        from rich.panel import Panel
        from rich.text import Text
        console = Console()
        use_rich = True
    except ImportError:
        use_rich = False

    if fmt == "json":
        print(json.dumps(results, indent=2))
        return

    if fmt == "timeline":
        print_timeline_format(results, use_rich)
        return

    for i, r in enumerate(results, 1):
        title = r.get("title", "")
        body = r.get("body", r.get("snippet", ""))
        url = r.get("href", r.get("url", ""))
        date = r.get("date", "")

        if use_rich:
            date_str = f" [{date}]" if date else ""
            panel_title = f"[bold amber]{i}. {title}[/bold amber]{date_str}"
            content = f"{body}\n\n[dim]{url}[/dim]"
            console.print(Panel(content, title=panel_title, border_style="dim"))
        else:
            print(f"\n{'='*60}")
            print(f"{i}. {title}")
            if date:
                print(f"   {date}")
            print(f"   {body}")
            print(f"   {url}")


def print_timeline_format(results: list[dict], use_rich: bool):
    """Format results as JS timeline entries ready to paste into the site."""
    print("\n// Suggested timeline entries — verify before adding:\n")
    for r in results:
        title = r.get("title", "")
        body = r.get("body", r.get("snippet", ""))[:120]
        url = r.get("href", r.get("url", ""))
        date = r.get("date", "")
        year = date[:4] if date and len(date) >= 4 else "20??"

        entry = (
            f"{{ year: '{year}', "
            f"event: '{title[:80].replace(chr(39), chr(34))}', "
            f"impact: '{body.replace(chr(39), chr(34))}', "
            f"source: '{url}' }},"
        )
        print(entry)
        print()


def interactive_mode():
    print("STS Research Tool — type a query, 'news <query>' for news, or 'quit' to exit.\n")
    while True:
        try:
            raw = input(">>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not raw or raw.lower() in ("quit", "exit", "q"):
            break

        is_news = raw.lower().startswith("news ")
        query = raw[5:].strip() if is_news else raw

        print(f"\nSearching {'news' if is_news else 'web'} for: {query}\n")
        results = search_news(query) if is_news else search(query)
        print_results(results)
        print()


def main():
    parser = argparse.ArgumentParser(description="Web research tool for STS content")
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument("--n", type=int, default=8, help="Number of results (default 8)")
    parser.add_argument("--news", action="store_true", help="Search news instead of web")
    parser.add_argument("--format", choices=["plain", "json", "timeline"], default="plain",
                        help="Output format (plain, json, or timeline for copy-paste JS)")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
        return

    if not args.query:
        parser.print_help()
        sys.exit(1)

    print(f"\nSearching: {args.query}\n")
    results = search_news(args.query, args.n) if args.news else search(args.query, args.n)
    print_results(results, args.format)


if __name__ == "__main__":
    main()
