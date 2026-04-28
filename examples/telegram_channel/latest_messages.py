"""Последние сообщения публичного Telegram-канала.

Запуск:
    python -m examples.telegram_channel.latest_messages telegram
    python -m examples.telegram_channel.latest_messages durov --limit 20

Историческая выгрузка через max_id:
    python -m examples.telegram_channel.latest_messages durov --limit 50 --crawl 5
"""

from __future__ import annotations

import argparse
import sys

from examples.common import build_session, get_json

HOST = "telegram-channel.p.rapidapi.com"
URL = f"https://{HOST}/channel/message"


def fetch_page(session, channel: str, *, limit: int = 50, max_id: int = 999_999_999) -> list[dict]:
    return get_json(session, URL, params={"channel": channel, "limit": limit, "max_id": max_id})


def crawl(session, channel: str, *, limit: int = 50, pages: int = 5):
    max_id = 999_999_999
    for _ in range(pages):
        batch = fetch_page(session, channel, limit=limit, max_id=max_id)
        if not batch:
            return
        for msg in batch:
            yield msg
        if len(batch) < limit:
            return  # последняя страница
        max_id = min(m["id"] for m in batch) - 1


def parse_views(v: str | None) -> int:
    if not v:
        return 0
    v = v.strip().upper().replace(",", ".")
    if v.endswith("K"):
        return int(float(v[:-1]) * 1_000)
    if v.endswith("M"):
        return int(float(v[:-1]) * 1_000_000)
    try:
        return int(v)
    except ValueError:
        return 0


def media_type(msg: dict) -> str:
    for kind in ("photo", "video", "audio", "sticker", "attachment", "media_poll"):
        if msg.get(kind):
            return kind
    return "text"


def main() -> int:
    parser = argparse.ArgumentParser(description="Telegram channel latest messages")
    parser.add_argument("channel", help="публичное имя канала без @")
    parser.add_argument("--limit", type=int, default=10, help="сообщений за один запрос (макс 50)")
    parser.add_argument("--crawl", type=int, default=1, help="сколько страниц назад выкачать (1 = только свежие)")
    args = parser.parse_args()

    session = build_session(HOST)

    if args.crawl == 1:
        messages = fetch_page(session, args.channel, limit=args.limit)
    else:
        messages = list(crawl(session, args.channel, limit=min(args.limit, 50), pages=args.crawl))

    if not messages:
        print("Сообщений нет (приватный канал? опечатка в имени?)")
        return 0

    for m in messages:
        text = (m.get("text") or "").replace("\n", " ")[:100]
        print(f"#{m['id']} [{m.get('date', '?')}] views={parse_views(m.get('views')):>10,} media={media_type(m):8} | {text}")

    print(f"\nВсего: {len(messages)} сообщений")
    return 0


if __name__ == "__main__":
    sys.exit(main())
