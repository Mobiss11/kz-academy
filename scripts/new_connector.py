#!/usr/bin/env python3
"""CLI: создаёт новую карточку коннектора в connectors/ из шаблона.

Запуск:
    python scripts/new_connector.py --name weather-api --host weather-api123.p.rapidapi.com
    python scripts/new_connector.py --name weather-api --host weather-api123.p.rapidapi.com --provider acmecorp
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = REPO_ROOT / "connectors" / "_template.md"
CONNECTORS_DIR = REPO_ROOT / "connectors"

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")


def slugify(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"[^a-z0-9-]+", "-", name)
    name = re.sub(r"-+", "-", name).strip("-")
    return name


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Создать карточку нового коннектора RapidAPI из шаблона"
    )
    parser.add_argument(
        "--name",
        required=True,
        help="имя коннектора в kebab-case (например 'weather-api')",
    )
    parser.add_argument(
        "--host",
        required=True,
        help="полный host из RapidAPI (например 'weather-api123.p.rapidapi.com')",
    )
    parser.add_argument(
        "--provider",
        default="<provider>",
        help="ник провайдера на RapidAPI (опционально)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="перезаписать карточку, если она уже есть",
    )
    args = parser.parse_args()

    name = slugify(args.name)
    if not NAME_RE.match(name):
        print(
            f"Ошибка: имя '{args.name}' не подходит. "
            "Используй латиницу, цифры и дефисы (например 'weather-api').",
            file=sys.stderr,
        )
        return 1

    target = CONNECTORS_DIR / f"{name}.md"
    if target.exists() and not args.force:
        print(f"Файл уже существует: {target.relative_to(REPO_ROOT)}", file=sys.stderr)
        print("Добавь --force чтобы перезаписать.", file=sys.stderr)
        return 1

    if not TEMPLATE_PATH.exists():
        print(f"Шаблон не найден: {TEMPLATE_PATH}", file=sys.stderr)
        return 1

    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    # хост приводим к виду без https:// и без / в конце
    host = args.host.replace("https://", "").replace("http://", "").rstrip("/")
    host_root = host.split(".p.rapidapi.com")[0]

    content = (
        template
        .replace("{ИМЯ КОННЕКТОРА}", name)
        .replace("{название провайдера}", args.provider)
        .replace("{provider}", args.provider)
        .replace("{name}", name)
        .replace("{host}", host_root)
    )

    target.write_text(content, encoding="utf-8")
    rel = target.relative_to(REPO_ROOT)
    print(f"✔ Создана карточка: {rel}")
    print(f"  Дальше: открой {rel}, заполни эндпоинты и добавь рабочий пример в examples/{name.replace('-', '_')}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
