"""Информация о публичном Telegram-канале.

Запуск:
    python -m examples.telegram_channel.channel_info telegram
    python -m examples.telegram_channel.channel_info durov --json
"""

from __future__ import annotations

import argparse
import json
import sys

from examples.common import build_session, get_json

HOST = "telegram-channel.p.rapidapi.com"
URL = f"https://{HOST}/channel/info"


def channel_info(channel: str) -> dict:
    session = build_session(HOST)
    return get_json(session, URL, params={"channel": channel})


def main() -> int:
    parser = argparse.ArgumentParser(description="Telegram channel info")
    parser.add_argument("channel", help="публичное имя канала без @ (например telegram)")
    parser.add_argument("--json", action="store_true", help="вывести raw JSON")
    args = parser.parse_args()

    data = channel_info(args.channel)

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0

    print(f"Канал: {data.get('title', '?')}")
    print(f"  тип: {data.get('chat_type', '?')}")
    print(f"  верифицирован: {data.get('verified', False)}")
    print(f"  подписчиков: {data.get('subscribers', '?')}")
    desc = data.get("description") or ""
    if desc:
        print(f"  описание: {desc[:200]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
