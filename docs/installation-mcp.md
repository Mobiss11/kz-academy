# Подключение через MCP (Model Context Protocol)

MCP — открытый протокол, через который LLM-клиенты подключаются к внешним источникам данных и тулам. Скилл этот можно обернуть в MCP-сервер, и тогда **любой MCP-совместимый клиент** автоматически получит доступ к карточкам коннекторов и тулам поиска.

Поддерживают MCP (на момент апреля 2026):

- **Claude Desktop** (нативно)
- **Cursor** (через настройки MCP)
- **Continue.dev** (VS Code / JetBrains плагин)
- **Cline / Roo Code** (VS Code)
- **OpenAI Agents SDK** (с MCP-адаптером)
- Свои клиенты через [официальные SDK](https://modelcontextprotocol.io/docs)

## Что предоставляет наш MCP-сервер

Файл [scripts/mcp_server.py](../scripts/mcp_server.py) экспортирует:

### Resources (статичные данные)

| URI | Что |
|---|---|
| `rapidapi://skill` | содержимое `SKILL.md` |
| `rapidapi://connector/{name}` | карточка коннектора (`yt-api`, `tiktok-api23`, `telegram-channel`, `threads-api4`, `instagram-looter2`) |

### Tools (вызываемые функции)

| Имя | Что делает |
|---|---|
| `list_connectors` | список всех доступных коннекторов с краткой инфой |
| `get_connector_pricing` | только секция тарифов конкретного коннектора (экономит токены) |
| `search_in_cards` | поиск подстроки во всех карточках (`rate limit`, `cgeo`, `/dl`, ...) |

LLM-клиент сам выбирает что подгружать в зависимости от запроса.

## Установка

### 1. Установи MCP SDK

```bash
pip install "mcp[cli]>=1.0"
```

(Уже добавлять в pyproject.toml не обязательно — это опциональная зависимость для тех, кто использует MCP-вариант.)

### 2. Проверь что сервер запускается

```bash
python -m scripts.mcp_server
```

Должно повиснуть в ожидании stdio (это нормально). Прерви Ctrl+C.

### 3. Подключи к клиенту

#### Claude Desktop

Открой файл конфигурации:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

Добавь блок (или создай файл если его нет):

```json
{
  "mcpServers": {
    "rapidapi-helper": {
      "command": "python",
      "args": ["-m", "scripts.mcp_server"],
      "cwd": "/абсолютный/путь/к/rapidapi-helper"
    }
  }
}
```

Перезапусти Claude Desktop. В чате должен появиться значок 🔌 — кликни и проверь что `rapidapi-helper` подключён.

> 💡 Если используешь виртуальное окружение, укажи путь к Python внутри venv:
> ```json
> "command": "/path/to/venv/bin/python"
> ```

#### Cursor

Открой `Settings` → найди раздел `MCP` (или `Tools and Integrations`):

```json
{
  "mcpServers": {
    "rapidapi-helper": {
      "command": "python",
      "args": ["-m", "scripts.mcp_server"],
      "cwd": "/abs/path/to/rapidapi-helper"
    }
  }
}
```

#### Continue.dev (VS Code)

В `~/.continue/config.json`:

```json
{
  "mcpServers": [
    {
      "name": "rapidapi-helper",
      "command": "python",
      "args": ["-m", "scripts.mcp_server"],
      "cwd": "/abs/path/to/rapidapi-helper"
    }
  ]
}
```

#### OpenAI Agents SDK (Python)

```python
from agents import Agent, MCPServerStdio

mcp_server = MCPServerStdio(
    params={
        "command": "python",
        "args": ["-m", "scripts.mcp_server"],
        "cwd": "/abs/path/to/rapidapi-helper",
    }
)

agent = Agent(
    name="rapidapi-bot",
    instructions="Помогаешь работать с RapidAPI. Используй MCP-сервер.",
    mcp_servers=[mcp_server],
)
```

## Проверка

В клиенте задай:

> Какие у тебя есть коннекторы для RapidAPI?

Клиент должен вызвать тул `list_connectors` и вернуть список из 5 коннекторов с их URI.

Затем:

> Сколько будет стоить мониторить просмотры 100 видео в TikTok каждые 5 минут?

Клиент должен:
1. Вызвать `get_connector_pricing("tiktok-api23")` — получить таблицу тарифов и формулы.
2. Подставить в формулу: 100 × 12 × 24 × 30 = 864 000 req/мес.
3. Вернуть: "План Pro ($9.99/мес) с overage ИЛИ Ultra ($49.99/мес) — Pro+overage дешевле".

## Преимущества MCP-варианта

✅ **Автоматическая загрузка** — клиент сам подтягивает карточку, когда нужно.
✅ **Один сервер — много клиентов**: Claude Desktop, Cursor, Continue, твой бот — все используют одни данные.
✅ **Экономия токенов**: тулы возвращают только нужную часть (например `get_connector_pricing` отдаёт только секцию тарифов, не всю карточку).
✅ **Динамические ответы**: `search_in_cards` ищет в реальном времени, нет необходимости загружать всё.
✅ **Расширяемо**: можно добавить тулы для расчёта стоимости, генерации запросов, проверки квоты и т.д.

## Ограничения

- Нужен Python в фоне (или установить как сервис).
- При обновлении репо (`git pull`) — перезапустить клиент.
- Требует MCP-совместимый клиент. ChatGPT (web/desktop) пока не поддерживает MCP нативно — для них используй [installation-chatgpt.md](installation-chatgpt.md).

## Расширение MCP-сервера

Хочешь добавить свои тулы (например, реальный вызов RapidAPI с автоматической оплатой расходов из карточки)?

Открой `scripts/mcp_server.py`, добавь функцию с декоратором `@mcp.tool()`:

```python
@mcp.tool()
def estimate_monthly_cost(connector: str, requests_per_day: int) -> dict:
    """Калькулятор: посчитать месячные расходы по плану."""
    # ... твоя логика на основе карточки ...
    return {"plan": "Pro", "cost_usd": 9.99, "explanation": "..."}
```

Перезапусти MCP-сервер и клиент — новый тул появится автоматически.

## Дальше

- API-вариант через прямой SDK — см. [installation-via-api.md](installation-via-api.md).
- Generic чат-LLM (без MCP) — см. [installation-generic-llm.md](installation-generic-llm.md).
- Документация MCP — https://modelcontextprotocol.io
