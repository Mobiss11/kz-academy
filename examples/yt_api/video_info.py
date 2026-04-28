"""Получение детальной информации о видео.

Запуск:
    python -m examples.yt_api.video_info dQw4w9WgXcQ
    python -m examples.yt_api.video_info "https://youtu.be/dQw4w9WgXcQ"
"""

from __future__ import annotations

import argparse
import re
import sys

from examples.common import build_session, get_json

HOST = "yt-api.p.rapidapi.com"
URL = f"https://{HOST}/video/info"

YOUTUBE_ID_RE = re.compile(r"(?:v=|youtu\.be/|shorts/)([\w-]{11})")


def extract_video_id(value: str) -> str:
    """Принимает либо чистый ID, либо URL — возвращает ID."""
    if len(value) == 11 and re.fullmatch(r"[\w-]{11}", value):
        return value
    match = YOUTUBE_ID_RE.search(value)
    if not match:
        raise ValueError(f"Не удалось извлечь YouTube ID из: {value}")
    return match.group(1)


def get_video_info(video_id: str) -> dict:
    session = build_session(HOST)
    return get_json(session, URL, params={"id": video_id})


def main() -> int:
    parser = argparse.ArgumentParser(description="Информация о видео из YouTube")
    parser.add_argument("video", help="ID или URL видео")
    args = parser.parse_args()

    try:
        video_id = extract_video_id(args.video)
    except ValueError as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        return 1

    info = get_video_info(video_id)

    print(f"Название:      {info.get('title', '?')}")
    print(f"Канал:         {info.get('channelTitle', '?')}")
    print(f"Длительность:  {info.get('lengthSeconds', '?')} сек")
    print(f"Просмотров:    {info.get('viewCount', '?')}")
    print(f"Лайков:        {info.get('likeCount', '?')}")
    print(f"Опубликовано:  {info.get('publishDate', '?')}")
    description = info.get("description", "")
    if description:
        preview = description[:200].replace("\n", " ")
        print(f"\nОписание (первые 200 символов):\n{preview}{'…' if len(description) > 200 else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
