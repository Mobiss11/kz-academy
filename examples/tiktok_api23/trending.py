"""Топовые трендовые видео на TikTok.

Запуск:
    python -m examples.tiktok_api23.trending US
    python -m examples.tiktok_api23.trending RU --limit 20

⚠️ Это endpoint из группы 'Ads (Trending)' — на странице тарифов помечен как
'Ads and Trending Endpoint — Request Custom'. На Basic-плане может не работать.
Если получаешь 403 — нужен платный план или Discussion с провайдером.
"""

from __future__ import annotations

import argparse
import sys

from examples.common import build_session, get_json

HOST = "tiktok-api23.p.rapidapi.com"


def main() -> int:
    parser = argparse.ArgumentParser(description="TikTok trending videos by country")
    parser.add_argument("country", help="ISO-код страны (US, RU, IN, GB, ...)")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    session = build_session(HOST)
    data = get_json(
        session,
        f"https://{HOST}/api/trending/video",
        params={"country": args.country, "limit": min(args.limit, 30)},
    )

    items = data.get("data") or data.get("videos") or []
    if not items:
        print("Пусто. Возможно нужна Custom подписка для группы Trending.")
        print(f"Raw response keys: {list(data.keys())}")
        return 0

    print(f"Топ-{len(items)} трендовых видео в {args.country}:\n")
    for v in items[:args.limit]:
        title = v.get("title") or v.get("desc") or "<без названия>"
        play = v.get("play_count") or v.get("playCount") or v.get("views") or "?"
        author = v.get("author") or v.get("username") or "?"
        print(f"  {play:>10} views | @{author} | {title[:80]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
