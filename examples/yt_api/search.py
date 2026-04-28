"""Поиск видео через YT-API.

Запуск:
    python -m examples.yt_api.search "claude api tutorial"
    python -m examples.yt_api.search "обзор макбука" --lang ru --geo RU --limit 10
"""

from __future__ import annotations

import argparse
import json
import sys

from examples.common import build_session, get_json

HOST = "yt-api.p.rapidapi.com"
URL = f"https://{HOST}/search"


def search(query: str, *, lang: str = "en", geo: str = "US", limit: int = 5) -> list[dict]:
    session = build_session(HOST)
    data = get_json(
        session,
        URL,
        params={"query": query, "type": "video", "lang": lang, "geo": geo},
    )
    items = [it for it in data.get("data", []) if it.get("type") == "video"]
    return items[:limit]


def main() -> int:
    parser = argparse.ArgumentParser(description="Поиск видео через YT-API")
    parser.add_argument("query", help="поисковый запрос")
    parser.add_argument("--lang", default="en")
    parser.add_argument("--geo", default="US")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--json", action="store_true", help="вывести raw JSON")
    args = parser.parse_args()

    results = search(args.query, lang=args.lang, geo=args.geo, limit=args.limit)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 0

    if not results:
        print("Ничего не найдено. Попробуй сменить geo или lang.")
        return 0

    for i, item in enumerate(results, 1):
        title = item.get("title", "<без названия>")
        channel = item.get("channelTitle", "?")
        views = item.get("viewCount", "?")
        video_id = item.get("videoId", "?")
        print(f"{i}. {title}")
        print(f"   канал: {channel} · просмотров: {views}")
        print(f"   https://youtube.com/watch?v={video_id}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
