"""Свежие посты по хэштегу Instagram.

Запуск:
    python -m examples.instagram_looter2.hashtag_feed travel
    python -m examples.instagram_looter2.hashtag_feed coding --limit 20
"""

from __future__ import annotations

import argparse
import sys

from examples.common import build_session, get_json

HOST = "instagram-looter2.p.rapidapi.com"


def main() -> int:
    parser = argparse.ArgumentParser(description="Instagram hashtag feed")
    parser.add_argument("hashtag", help="хэштег без #")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    session = build_session(HOST)
    data = get_json(
        session,
        f"https://{HOST}/tag-feeds",
        params={
            "query": args.hashtag,
            # fields-селектор экономит bandwidth — берём только то что нужно для вывода
            "fields": "items.id,items.shortcode,items.caption.text,items.like_count,items.media_type,items.user.username",
        },
    )

    items = data.get("items") or data.get("data") or []
    if not items:
        print(f"По хэштегу #{args.hashtag} ничего не найдено")
        return 0

    print(f"Свежие посты по #{args.hashtag} ({min(len(items), args.limit)} из {len(items)}):\n")
    for m in items[:args.limit]:
        user = m.get("user", {}).get("username", "?")
        likes = m.get("like_count", 0)
        media_type = {1: "photo", 2: "video", 8: "carousel"}.get(m.get("media_type"), "?")
        cap = ((m.get("caption") or {}).get("text") or "").replace("\n", " ")[:80]
        shortcode = m.get("shortcode", "?")
        print(f"  @{user:<20} [{media_type:8}] likes={likes:>8,} | {cap}")
        print(f"    https://instagram.com/p/{shortcode}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
