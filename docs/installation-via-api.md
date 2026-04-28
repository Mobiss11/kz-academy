# Подключение через API (Anthropic SDK / OpenAI SDK)

Если ты строишь собственного агента / бота / автоматизацию через прямой вызов LLM API — здесь примеры как программно загрузить SKILL.md и нужные карточки в system prompt.

Сценарии:
- Свой Slack/Telegram-бот с RapidAPI-навыком.
- Автоматизация на n8n / Zapier / Make.
- CI-задача "анализируй счёт и предложи план" — собственный код.

## Anthropic SDK (Claude)

> 💰 **Главная фича Claude API — prompt caching.** Bundle с карточками — это 10-40k токенов, и они одинаковые при каждом запросе. Кэш снижает стоимость в **10 раз** и латенцию в 2-5 раз. Используй обязательно.

### Python

```python
import os
from pathlib import Path
from anthropic import Anthropic

REPO = Path(__file__).resolve().parent.parent  # путь к корню rapidapi-helper

# Соберём контекст: SKILL.md + все нужные карточки
def load_skill_context(connectors: list[str]) -> str:
    parts = [(REPO / "SKILL.md").read_text(encoding="utf-8")]
    for name in connectors:
        parts.append(f"\n# === connectors/{name}.md ===\n\n")
        parts.append((REPO / "connectors" / f"{name}.md").read_text(encoding="utf-8"))
    return "\n\n".join(parts)


client = Anthropic()  # читает ANTHROPIC_API_KEY из окружения

skill_context = load_skill_context(["yt-api", "tiktok-api23"])

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=2048,
    system=[
        {
            "type": "text",
            "text": "Ты помощник по RapidAPI. Используй карточки ниже для генерации кода.",
        },
        {
            "type": "text",
            "text": skill_context,
            "cache_control": {"type": "ephemeral"},  # ключевая строка — кэшируем skill
        },
    ],
    messages=[
        {"role": "user", "content": "Напиши Python-функцию, которая ищет TikTok-видео по ключевому слову."}
    ],
)

print(response.content[0].text)

# При следующих запросах с тем же skill_context — попадание в кэш:
print(f"Cache hit: {response.usage.cache_read_input_tokens} tokens read from cache")
print(f"Cache write: {response.usage.cache_creation_input_tokens} tokens written to cache")
```

### Сколько это стоит

При первом запросе:
- ~30k токенов skill-контекста кэшируются (один раз) → write по тарифу 1.25× базовой цены
- ~30 токенов вопроса → обычная цена

При втором запросе (в течение 5 минут):
- ~30k токенов читаются из кэша → 0.1× базовой цены (в 10 раз дешевле!)
- ~30 токенов нового вопроса → обычная цена

**Итог:** если в день делаешь 100+ запросов с тем же skill — экономия порядка 90% на токенах.

> ⚠️ Cache TTL — 5 минут после последнего использования. Для долгоживущих агентов делай "разогрев" каждые 4 минуты, чтобы не терять кэш.

## OpenAI SDK (GPT-4 / GPT-4o)

OpenAI **не имеет** prompt caching на уровне API (в момент написания). Bundle придётся слать каждый раз. Поэтому здесь критично:

1. Брать только нужные коннекторы.
2. Использовать модели с большим контекстом (gpt-4o, gpt-4-turbo).

### Python

```python
import os
from pathlib import Path
from openai import OpenAI

REPO = Path(__file__).resolve().parent.parent

def load_skill_context(connectors: list[str]) -> str:
    parts = [(REPO / "SKILL.md").read_text(encoding="utf-8")]
    for name in connectors:
        parts.append(f"\n# === connectors/{name}.md ===\n\n")
        parts.append((REPO / "connectors" / f"{name}.md").read_text(encoding="utf-8"))
    return "\n\n".join(parts)


client = OpenAI()  # OPENAI_API_KEY

skill_context = load_skill_context(["yt-api"])

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": (
                "Ты помощник по RapidAPI. Ниже знания по нужным коннекторам. "
                "Используй точные имена параметров и эндпоинтов из карточек, не выдумывай.\n\n"
                + skill_context
            ),
        },
        {"role": "user", "content": "Напиши Python-функцию для поиска видео в YT-API."},
    ],
    temperature=0.3,
)

print(response.choices[0].message.content)
```

> 💡 **Совет**: Если OpenAI запустит prompt caching — добавь поддержку. На момент апреля 2026 у Azure OpenAI и некоторых deployments оно есть.

## Anthropic SDK (TypeScript / JS)

Идентично Python, только синтаксис другой:

```typescript
import Anthropic from "@anthropic-ai/sdk";
import { readFileSync } from "fs";
import { join } from "path";

const REPO = join(__dirname, "..");

function loadSkill(connectors: string[]): string {
  const parts = [readFileSync(join(REPO, "SKILL.md"), "utf-8")];
  for (const name of connectors) {
    parts.push(`\n# === connectors/${name}.md ===\n\n`);
    parts.push(readFileSync(join(REPO, "connectors", `${name}.md`), "utf-8"));
  }
  return parts.join("\n\n");
}

const client = new Anthropic();

const skillContext = loadSkill(["yt-api"]);

const response = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 2048,
  system: [
    { type: "text", text: "Ты помощник по RapidAPI." },
    { type: "text", text: skillContext, cache_control: { type: "ephemeral" } },
  ],
  messages: [{ role: "user", content: "Напиши TS-функцию для поиска через yt-api" }],
});

console.log((response.content[0] as { text: string }).text);
```

## Pattern: бот/автоматизация с автоматическим расчётом расходов

Утилита, которой можно скармливать "хочу X, сколько будет стоить?", и она через ИИ читает карточку, считает по формуле и отвечает:

```python
def estimate_cost(connector: str, scenario: str) -> str:
    skill_context = load_skill_context([connector])

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=[
            {"type": "text", "text": "Ты — финансовый калькулятор для RapidAPI."},
            {"type": "text", "text": skill_context, "cache_control": {"type": "ephemeral"}},
        ],
        messages=[{
            "role": "user",
            "content": (
                f"Сценарий: {scenario}\n\n"
                "Используй формулу из раздела 'Тарифы и расчёт расходов' карточки. "
                "Дай ответ в формате: 'План X, $Y/мес. Обоснование: ...'."
            ),
        }],
    )
    return response.content[0].text


print(estimate_cost(
    connector="tiktok-api23",
    scenario="Хочу мониторить просмотры 200 авторов каждые 30 минут.",
))
# → "План Pro ($9.99/мес) с overage ~$30 при превышении... ИЛИ Ultra ($49.99) без overage..."
```

## Что важно при API-интеграции

1. **Никогда не клади ключи в код.** Anthropic ключ → `ANTHROPIC_API_KEY` в env. RapidAPI ключ → `RAPIDAPI_KEY` в env. Скилл к ключам не имеет отношения — это знания, не секреты.

2. **Skill-контекст можно подгружать ленииво.** Не грузи все 5 коннекторов в каждый запрос — определи нужный по запросу пользователя:

   ```python
   def detect_connector(user_query: str) -> str | None:
       q = user_query.lower()
       if "youtube" in q or "yt-api" in q: return "yt-api"
       if "tiktok" in q: return "tiktok-api23"
       if "instagram" in q: return "instagram-looter2"
       if "telegram" in q: return "telegram-channel"
       if "threads" in q: return "threads-api4"
       return None
   ```

3. **Логируй cache_read_input_tokens** — следи, что кэш реально работает. Если каждый запрос пишет в кэш заново (`cache_creation_input_tokens > 0` каждый раз) — что-то меняется в `system`-блоке между вызовами, и кэш не попадает.

4. **Делай health-check**: раз в час пинг с минимальным запросом, чтобы кэш не протух.

## Дальше

- Готовый MCP-сервер (для Claude Desktop, Cursor, любого MCP-клиента) — см. [installation-mcp.md](installation-mcp.md).
- Generic чат-LLM (Gemini, Llama, локальные модели) — см. [installation-generic-llm.md](installation-generic-llm.md).
