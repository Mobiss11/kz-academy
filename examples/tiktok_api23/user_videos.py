"""Видео автора TikTok.

Запуск:
    python -m examples.tiktok_api23.user_videos charlidamelio
    python -m examples.tiktok_api23.user_videos mrbeast --limit 30
"""

from __future__ import annotations

import argparse
import sys

from examples.common import build_session, get_json

HOST = "tiktok-api23.p.rapidapi.com"


def get_user_info(session, unique_id: str) -> dict:
    return get_json(session, f"https://{HOST}/api/user/info", params={"uniqueId": unique_id})


def get_user_posts(session, sec_uid: str, *, count: int = 30, cursor: int = 0) -> dict:
    return get_json(
        session,
        f"https://{HOST}/api/user/posts",
        params={"secUid": sec_uid, "count": count, "cursor": cursor},
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="TikTok user videos")
    parser.add_argument("username", help="TikTok username без @")
    parser.add_argument("--limit", type=int, default=10, help="макс. видео")
    args = parser.parse_args()

    session = build_session(HOST)

    print(f"Получаем профиль @{args.username}...")
    info = get_user_info(session, args.username)
    user = info.get("userInfo", {}).get("user", {})
    stats = info.get("userInfo", {}).get("stats", {})

    if not user:
        print("Юзер не найден или приватный")
        return 1

    print(f"  {user.get('nickname', '?')} (verified={user.get('verified', False)})")
    print(f"  followers={stats.get('followerCount', 0):,}  hearts={stats.get('heartCount', 0):,}  videos={stats.get('videoCount', 0):,}")

    sec_uid = user.get("secUid")
    if not sec_uid:
        print("secUid не получен — не можем дальше")
        return 1

    print(f"\nЗагружаем видео (limit {args.limit})...")
    posts = get_user_posts(session, sec_uid, count=min(args.limit, 30))
    items = posts.get("data", {}).get("itemList") or posts.get("itemList", [])

    print()
    for v in items[:args.limit]:
        play = v.get("stats", {}).get("playCount", 0)
        likes = v.get("stats", {}).get("diggCount", 0)
        desc = (v.get("desc") or "").replace("\n", " ")[:90]
        print(f"#{v.get('id','?')} plays={play:>15,} likes={likes:>10,} | {desc}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
