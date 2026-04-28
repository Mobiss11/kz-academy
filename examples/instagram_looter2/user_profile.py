"""Профиль пользователя Instagram + последние посты.

Запуск:
    python -m examples.instagram_looter2.user_profile zuck
    python -m examples.instagram_looter2.user_profile cristiano --limit 30
"""

from __future__ import annotations

import argparse
import sys

from examples.common import build_session, get_json

HOST = "instagram-looter2.p.rapidapi.com"


def main() -> int:
    parser = argparse.ArgumentParser(description="Instagram profile + recent posts")
    parser.add_argument("username", help="Instagram username без @")
    parser.add_argument("--limit", type=int, default=10, help="макс. постов")
    args = parser.parse_args()

    session = build_session(HOST)

    # 1. Профиль (V2 — расширенный, с fields для экономии bandwidth)
    profile = get_json(
        session,
        f"https://{HOST}/profile2",
        params={
            "username": args.username,
            "fields": "id,username,full_name,follower_count,following_count,media_count,is_verified,biography",
        },
    )
    user_id = profile.get("id") or profile.get("user_id") or profile.get("pk")

    print(f"@{profile.get('username', args.username)}")
    print(f"  full name: {profile.get('full_name', '?')}")
    print(f"  verified: {profile.get('is_verified', False)}")
    print(f"  followers: {profile.get('follower_count', 0):,}")
    print(f"  following: {profile.get('following_count', 0):,}")
    print(f"  posts: {profile.get('media_count', 0):,}")
    bio = profile.get("biography") or ""
    if bio:
        print(f"  bio: {bio[:150]}")

    if not user_id:
        print("\nuser_id не получен — посты загрузить не получится")
        return 1

    # 2. Посты (V2 endpoint)
    print(f"\nПоследние {args.limit} постов:")
    feed = get_json(
        session,
        f"https://{HOST}/user-feeds2",
        params={"id": user_id, "count": min(args.limit, 30)},
    )
    items = feed.get("items") or feed.get("data") or []

    for m in items[:args.limit]:
        likes = m.get("like_count", 0)
        comments = m.get("comment_count", 0)
        cap = ((m.get("caption") or {}).get("text") or "").replace("\n", " ")[:90]
        media_type = {1: "photo", 2: "video", 8: "carousel"}.get(m.get("media_type"), "?")
        print(f"  [{media_type:8}] likes={likes:>10,} comments={comments:>6,} | {cap}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
