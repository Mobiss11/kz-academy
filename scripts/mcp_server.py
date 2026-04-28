#!/usr/bin/env python3
"""MCP-сервер: предоставляет SKILL.md и карточки коннекторов как ресурсы.

Любой MCP-клиент (Claude Desktop, Cursor, Continue.dev, кастомный код)
сможет автоматически подгружать карточки коннекторов и использовать их
как тулинг.

Установка:
    pip install "mcp[cli]>=1.0"

Запуск (stdio — для Claude Desktop, Cursor):
    python -m scripts.mcp_server

Подключение в Claude Desktop:
    Settings → Developer → Edit Config → добавь блок (см. docs/installation-mcp.md)
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print(
        "Не установлен пакет 'mcp'. Установи:\n"
        "    pip install 'mcp[cli]>=1.0'",
        file=sys.stderr,
    )
    sys.exit(1)


REPO = Path(__file__).resolve().parent.parent
SKILL_PATH = REPO / "SKILL.md"
CONNECTORS = REPO / "connectors"


mcp = FastMCP("kz-academy")


# === Resources: статические markdown-файлы ===

@mcp.resource("rapidapi://skill")
def skill_md() -> str:
    """Главный файл скилла: общие правила RapidAPI + расчёт расходов."""
    return SKILL_PATH.read_text(encoding="utf-8")


@mcp.resource("rapidapi://connector/{name}")
def connector_card(name: str) -> str:
    """Карточка конкретного коннектора (yt-api, tiktok-api23, ...).

    Содержит: эндпоинты, параметры, JSON-ответы, тарифы, формулы расходов.
    """
    path = CONNECTORS / f"{name}.md"
    if not path.exists():
        available = [p.stem for p in CONNECTORS.glob("*.md") if not p.name.startswith("_")]
        raise ValueError(f"Connector '{name}' not found. Available: {available}")
    return path.read_text(encoding="utf-8")


# === Tools: запросы и действия ===

@mcp.tool()
def list_connectors() -> list[dict]:
    """Список всех доступных коннекторов с краткой инфой.

    Возвращает массив объектов с полями: name, file, first_line.
    """
    out = []
    for p in sorted(CONNECTORS.glob("*.md")):
        if p.name.startswith("_"):
            continue
        first_line = p.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
        out.append({
            "name": p.stem,
            "file": f"connectors/{p.name}",
            "title": first_line,
            "uri": f"rapidapi://connector/{p.stem}",
        })
    return out


@mcp.tool()
def get_connector_pricing(name: str) -> str:
    """Только секция 'Тарифы и расчёт расходов' конкретного коннектора.

    Использовать когда юзер спрашивает 'сколько будет стоить' — экономит токены
    относительно полной карточки.
    """
    path = CONNECTORS / f"{name}.md"
    if not path.exists():
        raise ValueError(f"Connector '{name}' not found")
    text = path.read_text(encoding="utf-8")

    # Вытаскиваем секцию начиная с заголовка про тарифы
    markers = ["## Тарифы и расчёт расходов", "## Тарифы (verified", "## Тарифы\n"]
    for marker in markers:
        if marker in text:
            return text[text.index(marker):]
    return "(секция Тарифы не найдена в карточке)"


@mcp.tool()
def search_in_cards(query: str) -> list[dict]:
    """Поиск подстроки во всех карточках коннекторов.

    Полезно когда не знаешь, в какой карточке искать. Например 'rate limit',
    'extend=1', 'cgeo', '/dl', 'continuation'.

    Возвращает массив {connector, line_number, line, context}.
    """
    out = []
    q = query.lower()
    for p in sorted(CONNECTORS.glob("*.md")):
        if p.name.startswith("_"):
            continue
        lines = p.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(lines, 1):
            if q in line.lower():
                ctx_start = max(0, i - 2)
                ctx_end = min(len(lines), i + 2)
                out.append({
                    "connector": p.stem,
                    "line_number": i,
                    "line": line,
                    "context": "\n".join(lines[ctx_start:ctx_end]),
                })
                if len(out) > 30:  # сильно много матчей — обрезаем
                    return out
    return out


def main():
    mcp.run()


if __name__ == "__main__":
    main()
