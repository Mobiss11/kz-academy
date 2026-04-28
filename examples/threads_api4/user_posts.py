"""Последние посты пользователя Threads.

Запуск:
    python -m examples.threads_api4.user_posts reuters
    python -m examples.threads_api4.user_posts zuck --limit 30
"""

from __future__ import annotations

import argparse
import sys

from examples.common import build_session, get_json

HOST = "threads-api4.p.rapidapi.com"


def get_user_id(session, username: str) -> str:
    info = get_json(session, f"https://{HOST}/api/user/info", params={"username": username})
    return info["data"]["user"]["pk"]


def fetch_posts(session, user_id: str, end_cursor: str | None = None) -> dict:
    params = {"user_id": user_id}
    if end_cursor:
        params["end_cursor"] = end_cursor
    return get_json(session, f"https://{HOST}/api/user/posts", params=params)


def main() -> int:
    parser = argparse.ArgumentParser(description="Latest Threads posts of a user")
    parser.add_argument("username", help="Threads username без @")
    parser.add_argument("--limit", type=int, default=10, help="макс. постов")
    args = parser.parse_args()

    session = build_session(HOST)

    print(f"Получаем user_id для @{args.username}...")
    user_id = get_user_id(session, args.username)
    print(f"  user_id = {user_id}")

    response = fetch_posts(session, user_id)

    edges = response.get("data", {}).get("mediaData", {}).get("edges", [])
    print(f"\nПостов получено: {len(edges)}\n")

    shown = 0
    for edge in edges:
        if shown >= args.limit:
            break
        for item in edge["node"]["thread_items"]:
            post = item["post"]
            caption = (post.get("caption") or {}).get("text", "")
            print(f"#{post.get('pk', '?')}: {caption[:120]}")
            shown += 1
            if shown >= args.limit:
                break
    return 0


if __name__ == "__main__":
    sys.exit(main())
