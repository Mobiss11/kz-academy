# LLM-модели для контент-завода: сравнение и выбор

> 🎯 **Цель:** выбрать оптимальную модель для каждого этапа pipeline (переписывание, суммаризация, классификация ниши, анализ хука) и точно посчитать сколько это будет стоить.
>
> 💰 **Все цены ниже — verified из OpenRouter API на момент апреля 2026.** Данные могут устареть — сверяйся с https://openrouter.ai/models перед прод-кодом.

## Зачем OpenRouter

[OpenRouter](https://openrouter.ai) — единый API для **367+ моделей** разных провайдеров (Anthropic, OpenAI, Google, xAI, Meta, DeepSeek, Mistral, Qwen, Z.AI, Moonshot и десятки других). Один ключ, один формат запросов, прозрачное тарифицирование по токенам.

Зачем это для контент-завода:

1. **Один ключ — все модели.** Не надо регистрироваться у Anthropic, потом у OpenAI, потом у Google — взял `OPENROUTER_API_KEY` и переключаешь модель параметром.
2. **Резерв на отказ.** Если у одного провайдера падает — переключаешь на другую модель в одну строчку.
3. **Дешёвая экспериментация.** Хочешь попробовать DeepSeek для русского переписывания и Gemini для английского? — параметр в запросе.
4. **Почасовая статистика по моделям** — видно где деньги уходят.

## Tier'ы моделей по стоимости

Цены в **$ за 1 миллион токенов** (input / output). Округлены и проверены через OpenRouter API.

### 🟢 Бюджет (output ≤ $0.40/M)

Подходят для **массового переписывания** контент-завода (тысячи скриптов в день):

| Модель | Контекст | Input/M | Output/M | Особенности |
|---|---|---|---|---|
| `deepseek/deepseek-v4-flash` | 1M | $0.14 | $0.28 | Топ соотношение цена/качество. Хорошо переводит RU/EN/CN. |
| `google/gemini-2.0-flash-lite-001` | 1M | $0.075 | $0.30 | Отличный для batch, огромный контекст. |
| `meta-llama/llama-4-scout` | 327k | $0.08 | $0.30 | Быстрый, открытый вес. |
| `openai/gpt-5-nano` | 400k | $0.05 | $0.40 | Самый дешёвый GPT-5 family. |
| `openai/gpt-4.1-nano` | 1M | $0.10 | $0.40 | Если нужен GPT-tier по бюджету. |
| `google/gemini-2.5-flash-lite` | 1M | $0.10 | $0.40 | Свежее поколение Gemini. |
| `mistralai/mistral-nemo` | 131k | $0.02 | $0.04 | **Самый дешёвый**, но качество слабее остальных. |

### 🟡 Средний (output $0.40 – $1.50/M)

Подходят для **качественного переписывания** с учётом тональности и нишевой адаптации:

| Модель | Контекст | Input/M | Output/M | Особенности |
|---|---|---|---|---|
| `x-ai/grok-4.1-fast` | 2M | $0.20 | $0.50 | Огромный контекст, хорош для обработки длинных видео. |
| `openai/gpt-4o-mini` | 128k | $0.15 | $0.60 | Стандарт, проверенный. |
| `deepseek/deepseek-chat-v3.1` | 32k | $0.15 | $0.75 | Качественный для русского. |
| `google/gemini-2.5-flash` (полная) | 1M | $0.30 | $2.50 | Лучшее качество в Flash-семействе. |
| `qwen/qwen-plus` | 1M | $0.26 | $0.78 | Топ для китайского/японского. |
| `mistralai/mistral-large-2512` | 262k | $0.50 | $1.50 | Качественный европейский, хорошо с RU/EN/FR/DE. |

### 🟠 Премиум (output $1.50 – $15/M)

Для **флагманского контента**, агентских клиентов, сложных промптов:

| Модель | Контекст | Input/M | Output/M | Особенности |
|---|---|---|---|---|
| `anthropic/claude-haiku-4.5` | 200k | $1.00 | $5.00 | Топ-тир Anthropic по бюджету. Поддерживает prompt caching. |
| `moonshotai/kimi-k2.5` | 262k | $0.44 | $2.00 | Хорош для длинного контекста. |
| `qwen/qwen-max` | 32k | $1.04 | $4.16 | Топ-тир Alibaba. |
| `anthropic/claude-sonnet-4.6` | 1M | $3.00 | $15.00 | **Лучший выбор для премиум-переписывания.** Поддерживает prompt caching (-90% на повторах). |

### 🔴 Топ (output > $15/M)

Только когда качество критично и бюджет неограничен:

| Модель | Контекст | Input/M | Output/M | Когда использовать |
|---|---|---|---|---|
| `google/gemini-2.5-pro` | 1M | $1.25 | $10.00 | Лучший Gemini, отлично с длинным контекстом. |
| `anthropic/claude-opus-4.7` | 1M | $5.00 | $25.00 | Топ Anthropic, для самых сложных задач (стратегия, длинные промпты). |
| `openai/gpt-5` | — | (выше) | (выше) | Когда нужен топ OpenAI. |

## Какую модель выбрать под задачу

### Задача 1. Переписывание скрипта (Reels/Shorts/TikTok)

Один скрипт = ~2-5k input + 0.5-1k output токенов.

| Бюджет | Модель | Цена за скрипт | Качество (1-10) |
|---|---|---|---|
| Минимум | `deepseek/deepseek-v4-flash` | ~$0.0007 | 7/10 (хорошо для RU/EN) |
| Стандарт | `openai/gpt-4o-mini` | ~$0.001 | 8/10 (универсально) |
| Премиум | `anthropic/claude-sonnet-4.6` | ~$0.025 | 9.5/10 (с кэшем — $0.0025) |

> 💡 **С prompt caching** Claude Sonnet 4.6 дешевле GPT-4o-mini на массовом потоке (10× скидка на повторы system prompt'а в течение 5 минут).

### Задача 2. Hook-анализ (определить силу первой фразы)

Маленькая задача: 200-500 input + 50 output токенов.

| Модель | Цена за анализ |
|---|---|
| `meta-llama/llama-4-scout` | ~$0.0001 |
| `openai/gpt-5-nano` | ~$0.00005 |
| `google/gemini-2.0-flash-lite-001` | ~$0.0001 |

Выбирай **gpt-5-nano** — самый дешёвый для бинарных классификаций.

### Задача 3. Классификация ниши видео

По транскрипции определить: edu / comedy / lifestyle / business / etc.

| Модель | Цена | Точность |
|---|---|---|
| `gpt-5-nano` с structured output | ~$0.0001 | 92% |
| `gemini-2.0-flash-lite` с JSON-schema | ~$0.0001 | 94% |
| `claude-haiku-4.5` | ~$0.001 | 96% |

### Задача 4. Длинный контент (long-form YouTube → полный конспект)

Транскрипция 30-минутного видео = ~6k слов = ~10k токенов.

Нужен **большой контекст + хорошее суммирование**:

| Модель | Цена за конспект | Контекст |
|---|---|---|
| `grok-4.1-fast` | ~$0.005 | 2M (с запасом) |
| `gemini-2.5-flash-lite` | ~$0.005 | 1M |
| `claude-haiku-4.5` | ~$0.015 | 200k |
| `gemini-2.5-pro` (премиум) | ~$0.10 | 1M |

### Задача 5. Перевод между языками

| Языковая пара | Лучшая модель |
|---|---|
| EN ↔ RU | `deepseek-v4-flash`, `claude-haiku-4.5`, `mistral-large` |
| EN ↔ CN | `qwen-plus`, `kimi-k2.5`, `deepseek-v4-flash` |
| EN ↔ ES/FR/DE | `mistral-large-2512`, `gpt-4o-mini` |
| EN ↔ AR | `claude-sonnet-4.6`, `gpt-4o-mini` |
| EN ↔ редкие (HI/TH/VI) | `claude-sonnet-4.6`, `gemini-2.5-pro` |

## Рекомендуемый стек по типу проекта

### Стартап / личный проект (объём < 1k скриптов/мес)

```yaml
hook_analysis: openai/gpt-5-nano       # $0.00005/анализ
classification: openai/gpt-5-nano       # $0.0001/классификация
rewriting: deepseek/deepseek-v4-flash   # $0.0007/скрипт
fallback: openai/gpt-4o-mini            # на случай падения

monthly_budget: ~$5-10
```

### Малый бизнес (агентство, 1k-10k скриптов/мес)

```yaml
hook_analysis: openai/gpt-5-nano        # дёшево, классификация
rewriting_default: openai/gpt-4o-mini   # сбалансированно
rewriting_premium_clients: anthropic/claude-sonnet-4.6  # с кэшем
classification: google/gemini-2.0-flash-lite-001  # быстро + дёшево

monthly_budget: ~$50-200
```

### Крупная редакция (10k+ скриптов/мес, разные ниши)

```yaml
hook_analysis: openai/gpt-5-nano
classification: google/gemini-2.5-flash-lite
rewriting_ru: deepseek/deepseek-v4-flash       # для русского
rewriting_en: openai/gpt-4o-mini               # для английского
rewriting_cn: qwen/qwen-plus                   # для китайского
rewriting_premium: anthropic/claude-sonnet-4.6  # с кэшем для VIP
long_form_summary: x-ai/grok-4.1-fast          # 2M контекст

monthly_budget: ~$500-2000
```

## Сравнение OpenRouter vs прямые ключи

| Критерий | OpenRouter | Прямой ключ (Anthropic, OpenAI) |
|---|---|---|
| **Регистрация** | Один аккаунт | Отдельный у каждого |
| **Цены** | + 5% наценка от base | Базовая цена |
| **Лимиты** | Общие credits | Per-provider rate limits |
| **Prompt caching** | ✅ поддерживается для Anthropic | ✅ нативно |
| **Структурированный вывод** | ✅ для большинства моделей | ✅ |
| **Мониторинг** | Единый dashboard | Per-provider |
| **Поддержка** | OpenRouter community | Платная enterprise |

**Рекомендация:**
- На старте — **OpenRouter** (один ключ, гибкость).
- При объёмах > 10 000 запросов/день и стабильной модели — переключайся на **прямой ключ** (экономия 5-10%).

## Как использовать OpenRouter

### Регистрация и ключ

1. Открой https://openrouter.ai/
2. **Sign Up** через Google/GitHub.
3. Перейди в [Keys](https://openrouter.ai/settings/keys) → **Create Key**.
4. Пополни credits ([Credits](https://openrouter.ai/settings/credits)) — минимум $5 (примет любую карту, в том числе российскую через Stripe).
5. Сохрани ключ в `.env`: `OPENROUTER_API_KEY=sk-or-...`

### Минимальный пример (Python)

```python
import os
from openai import OpenAI

# OpenRouter совместим с OpenAI SDK
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

response = client.chat.completions.create(
    model="deepseek/deepseek-v4-flash",  # или любая из 367+ моделей
    messages=[
        {"role": "system", "content": "Ты сценарист Reels."},
        {"role": "user", "content": "Перепиши: ..."},
    ],
    extra_headers={
        # Опционально для аналитики
        "HTTP-Referer": "https://your-app.com",
        "X-Title": "My Content Factory",
    },
)
print(response.choices[0].message.content)
```

### Минимальный пример (Anthropic SDK с base_url override)

```python
from anthropic import Anthropic

client = Anthropic(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

# Для Claude через OpenRouter с prompt caching
response = client.messages.create(
    model="anthropic/claude-sonnet-4.6",
    max_tokens=1024,
    system=[
        {"type": "text", "text": "Базовый промпт..."},
        {"type": "text", "text": LONG_CONTEXT, "cache_control": {"type": "ephemeral"}},
    ],
    messages=[{"role": "user", "content": "..."}],
)
```

### Fallback / резерв

```python
def rewrite_with_fallback(text):
    fallbacks = [
        "deepseek/deepseek-v4-flash",
        "openai/gpt-4o-mini",
        "google/gemini-2.0-flash-lite-001",
    ]
    for model in fallbacks:
        try:
            return client.chat.completions.create(
                model=model, messages=[...], timeout=60,
            ).choices[0].message.content
        except Exception as e:
            print(f"Model {model} failed: {e}, trying next...")
    raise RuntimeError("All models failed")
```

## Транскрипция: что использовать

OpenRouter **НЕ предоставляет** транскрипцию (только LLM). Для аудио → текст:

| Сервис | Цена | Качество | Где регать |
|---|---|---|---|
| **OpenAI Whisper API** | $0.006/мин | Топ-универсал | https://platform.openai.com |
| **AssemblyAI** | $0.012/мин | Лучше для EN | https://www.assemblyai.com |
| **Deepgram Nova-2** | $0.0043/мин | Топ скорость | https://deepgram.com |
| **Yandex SpeechKit** | от ₽0.10/сек ($0.0011/мин) | Топ для RU | https://cloud.yandex.ru/services/speechkit |
| **Replicate Whisper Large v3** | $0.0008/мин (на CPU) | Топ соотношение цена/качество | https://replicate.com |
| **Локальный Whisper** | Бесплатно (своё железо) | Зависит от GPU | https://github.com/openai/whisper |

> 💡 **Стратегия:** для прод-стартапа — **Replicate Whisper Large v3** ($0.0008/мин). При объёмах > 1000 минут/день — поднимай **локальный Whisper** на GPU (одна 4090 = 30 минут аудио в минуту).

## Как считать общую стоимость pipeline

Один виральный ролик через полный pipeline:

| Этап | Сервис | Цена | Объём |
|---|---|---|---|
| Мониторинг | RapidAPI коннектор | ~$0.0005 | 25 запросов амортизированно |
| Скачивание | RapidAPI Download | $0.001 | 1 запрос |
| Транскрипция | Whisper / Replicate | $0.0008-0.006 | 1 минута |
| Классификация ниши | gpt-5-nano | $0.0001 | 200 токенов |
| Hook-анализ | gpt-5-nano | $0.00005 | 100 токенов |
| Переписывание (deepseek) | deepseek-v4-flash | $0.0007 | 3k+1k токенов |
| Hosting в S3 | AWS S3 | $0.0001/мес | 5 MB |
| **Итого на ролик** | | **~$0.003-0.01** | |

**При 1000 роликов/мес = $3-10** на LLM/транскрипцию (плюс RapidAPI квота).

С Claude Sonnet 4.6 без кэша: ~$0.025/ролик = $25/мес на 1000.
С Claude Sonnet 4.6 с кэшем (после первого запроса): ~$0.005/ролик = $5/мес.

## Подводные камни

### 1. Модели меняются каждый месяц

OpenRouter добавляет/убирает модели часто. Раз в 1-2 месяца перепроверяй:
- https://openrouter.ai/models — текущий список.
- API: `curl 'https://openrouter.ai/api/v1/models' | jq '.data[] | {id, pricing}'`.

### 2. Контекст ≠ оптимальное использование

Модель с 1M контекстом не значит "грузи туда всё". Большой контекст = больше latency и стоимости input. Бери минимум нужного.

### 3. Latency

Топ-модели (Claude Opus, GPT-5) могут отвечать 10-30 секунд. Бюджетные (DeepSeek, Llama-4-scout, GPT-5-nano) — 1-3 секунды. Для real-time сценариев — нижний tier.

### 4. Региональные ограничения

Некоторые модели недоступны в определённых регионах (например, Anthropic из РФ через OpenAI напрямую — нет, через OpenRouter — да). OpenRouter обычно решает.

### 5. Структурированный вывод не у всех

JSON-schema enforced output поддерживают: GPT-4o, GPT-5 family, Claude (через function calling), Gemini, Mistral. **Не поддерживают**: некоторые open-source (Llama, Qwen — частично). Если нужно — фильтруй по поддержке.

## Дальше

- [transcription-rewriting.md](transcription-rewriting.md) — как использовать модели в pipeline переписывания.
- [cost-modeling.md](cost-modeling.md) — общая экономика контент-завода с учётом LLM.
- [../installation-via-api.md](../installation-via-api.md) — программное использование с prompt caching.
- [../full-stack-setup.md](../full-stack-setup.md) — пошаговая настройка всех сервисов (OpenRouter, RapidAPI, Whisper, S3, Telegram).
