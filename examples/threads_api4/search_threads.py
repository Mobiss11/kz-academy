"""Поиск в Threads (свежие посты по ключевому слову).

Запуск:
    python -m examples.threads_api4.search_threads "claude api"
    python -m examples.threads_api4.search_threads "tesla" --top  # топ-результаты вместо свежих
"""

from __future__ import annotations

import argparse
import sys

from examples.common import build_session, get_json

HOST = "threads-api4.p.rapidapi.com"


def main() -> int:
    parser = argparse.ArgumentParser(description="Search Threads posts")
    parser.add_argument("query", help="поисковый запрос")
    parser.add_argument("--top", action="store_true", help="top вместо recent")
    parser.add_argument("--limit", type=int, default=15)
    args = parser.parse_args()

    session = build_session(HOST)
    path = "/api/search/top" if args.top else "/api/search/recent"
    data = get_json(session, f"https://{HOST}{path}", params={"query": args.query})

    edges = data.get("data", {}).get("searchResults", {}).get("edges", [])
    if not edges:
        print("Ничего не найдено")
        return 0

    for edge in edges[:args.limit]:
        items = edge["node"]["thread"]["thread_items"]
        for item in items:
            post = item["post"]
            user = post.get("user", {})
            caption = (post.get("caption") or {}).get("text", "")
            print(f"@{user.get('username', '?'):<25} | {caption[:100]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
