#!/usr/bin/env python3
"""Сборка одного markdown-файла из SKILL.md + выбранных карточек коннекторов.

Используется когда нужно просто вставить весь контекст в чат-LLM без поддержки
скиллов (Gemini, Llama, DeepSeek, любой generic chat).

Запуск:
    # все коннекторы
    python scripts/bundle.py > bundle.md

    # только yt-api
    python scripts/bundle.py --connector yt-api > yt-bundle.md

    # несколько
    python scripts/bundle.py --connector yt-api --connector tiktok-api23 > bundle.md

    # узнать что есть
    python scripts/bundle.py --list
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = REPO_ROOT / "SKILL.md"
CONNECTORS_DIR = REPO_ROOT / "connectors"


def list_available() -> list[str]:
    return sorted(p.stem for p in CONNECTORS_DIR.glob("*.md") if not p.name.startswith("_"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Bundle SKILL.md + connector cards into one markdown")
    parser.add_argument(
        "--connector", "-c", action="append", default=[],
        help="имя коннектора (без .md). Можно указать несколько раз. Без флага — все.",
    )
    parser.add_argument("--list", action="store_true", help="показать доступные коннекторы и выйти")
    parser.add_argument("--no-skill", action="store_true", help="не включать SKILL.md (только карточки)")
    args = parser.parse_args()

    available = list_available()

    if args.list:
        print("Доступные коннекторы:")
        for name in available:
            print(f"  - {name}")
        return 0

    selected = args.connector or available
    unknown = [s for s in selected if s not in available]
    if unknown:
        print(f"Неизвестные коннекторы: {unknown}", file=sys.stderr)
        print(f"Доступные: {available}", file=sys.stderr)
        return 1

    out: list[str] = []
    out.append("# RapidAPI Helper — bundled context\n")
    out.append(
        "Этот файл — собранный контекст для ИИ-чата без поддержки скиллов.\n"
        "Вставь его целиком в начало диалога (или в system prompt), и нейронка\n"
        "получит знания по выбранным RapidAPI-коннекторам.\n\n"
        "---\n"
    )

    if not args.no_skill and SKILL_PATH.exists():
        out.append(f"\n# === {SKILL_PATH.name} ===\n\n")
        out.append(SKILL_PATH.read_text(encoding="utf-8"))
        out.append("\n\n---\n")

    for name in selected:
        path = CONNECTORS_DIR / f"{name}.md"
        out.append(f"\n# === connectors/{path.name} ===\n\n")
        out.append(path.read_text(encoding="utf-8"))
        out.append("\n\n---\n")

    sys.stdout.write("".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
