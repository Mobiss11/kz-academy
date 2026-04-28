"""Получение трендов YouTube по стране.

Запуск:
    python -m examples.yt_api.trending
    python -m examples.yt_api.trending --geo RU --type music --limit 10
"""

from __future__ import annotations

import argparse
import sys

from examples.common import build_session, get_json

HOST = "yt-api.p.rapidapi.com"
URL = f"https://{HOST}/trending"

VALID_TYPES = ("now", "music", "gaming", "movies")


def get_trending(geo: str = "US", trend_type: str = "now", limit: int = 5) -> list[dict]:
    session = build_session(HOST)
    data = get_json(session, URL, params={"geo": geo, "type": trend_type})
    return [it for it in data.get("data", []) if it.get("type") == "video"][:limit]


def main() -> int:
    parser = argparse.ArgumentParser(description="Тренды YouTube")
    parser.add_argument("--geo", default="US", help="код страны (US, RU, DE, ...)")
    parser.add_argument("--type", dest="trend_type", default="now", choices=VALID_TYPES)
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()

    items = get_trending(args.geo, args.trend_type, args.limit)
    if not items:
        print("Тренды не получены — попробуй сменить geo.")
        return 0

    print(f"Тренды ({args.trend_type}) для {args.geo}:\n")
    for i, item in enumerate(items, 1):
        title = item.get("title", "<без названия>")
        channel = item.get("channelTitle", "?")
        views = item.get("viewCount", "?")
        print(f"{i}. {title}")
        print(f"   {channel} · {views} просмотров\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
