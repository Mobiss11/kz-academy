# RapidAPI Helper

Учебный набор инструкций, который помогает ИИ-помощникам (Claude, ChatGPT, Cursor и др.) **правильно** работать с любым коннектором из [RapidAPI Hub](https://rapidapi.com/).

Идея простая: у каждого коннектора в RapidAPI свои эндпоинты, параметры, лимиты и грабли. Если просто бросить нейронке "напиши мне запрос к API X" — она часто галлюцинирует имена параметров и хедеры. Этот репозиторий даёт ИИ структурированный контекст: общие правила RapidAPI + карточки конкретных коннекторов.

## Быстрый старт

> 🚀 **Если ты впервые слышишь про RapidAPI** — открой [docs/getting-started.md](docs/getting-started.md). Там полный путь от регистрации на RapidAPI до первого работающего запроса (≈15 минут). **Без подписки на конкретный API любой запрос вернёт 403** — это самая частая ошибка новичков.

Краткий путь:

1. **Регистрация на RapidAPI** → [rapidapi.com/auth/sign-up](https://rapidapi.com/auth/sign-up)
2. **Получить API-ключ** → [rapidapi.com/developer/security](https://rapidapi.com/developer/security)
3. **Подписаться на нужный коннектор** (см. таблицу ниже, ссылка на Pricing)
4. **Клонировать этот репо**, прописать ключ в `.env`
5. **Подключить к ИИ** ([Claude Code](docs/installation-claude-code.md), [Cursor](docs/installation-cursor.md), [ChatGPT](docs/installation-chatgpt.md), [Claude.ai](docs/installation-claude-ai.md))

## Что внутри

```
rapidapi-helper/
├── SKILL.md                  # главный файл-роутер: общие правила + формула расчёта расходов
├── connectors/               # карточки конкретных коннекторов (5 готовых + шаблон)
│   ├── _template.md          # шаблон для новой карточки
│   ├── yt-api.md             # YT-API (ytjar) — 35 эндпоинтов
│   ├── telegram-channel.md   # Telegram Channel (akrakoro) — 2 эндпоинта
│   ├── threads-api4.md       # Threads (Lundehund) — 12 эндпоинтов
│   ├── tiktok-api23.md       # TikTok (Lundehund) — 56 эндпоинтов
│   └── instagram-looter2.md  # Instagram (irrors-apis) — 30 эндпоинтов
├── examples/                 # рабочий Python-код для каждого коннектора
│   ├── common.py             # общая обвязка (ключ, ретраи, кэш)
│   ├── yt_api/               # search.py, video_info.py, trending.py
│   ├── telegram_channel/     # channel_info.py, latest_messages.py
│   ├── threads_api4/         # user_posts.py, search_threads.py
│   ├── tiktok_api23/         # user_videos.py, trending.py
│   └── instagram_looter2/    # user_profile.py, hashtag_feed.py
├── scripts/
│   ├── new_connector.py      # CLI: создать новую карточку из шаблона
│   ├── bundle.py             # склеить SKILL.md + карточки в один markdown для generic LLM
│   └── mcp_server.py         # MCP-сервер для Claude Desktop / Cursor / Continue
├── docs/
│   ├── getting-started.md           # 🚀 онбординг от нуля до первого запроса
│   ├── full-stack-setup.md          # 🛠️  регистрация ВСЕХ сервисов (RapidAPI/OpenRouter/Whisper/S3/...)
│   ├── installation-claude-code.md  # подключение к Claude Code (нативный скилл)
│   ├── installation-cursor.md       # подключение к Cursor (.cursor/rules/)
│   ├── installation-claude-ai.md    # подключение к Claude.ai Projects
│   ├── installation-chatgpt.md      # подключение к ChatGPT (Project / Custom GPT)
│   ├── installation-mcp.md          # подключение через MCP (любой MCP-клиент)
│   ├── installation-via-api.md      # программное подключение через SDK
│   ├── installation-generic-llm.md  # для Gemini/Llama/локальных моделей
│   └── methodology/                 # playbook'и контент-завода
│       ├── README.md                #   индекс методологий
│       ├── pipeline-overview.md     #   полный flow: автор → виральное → скрипт
│       ├── viral-detection.md       #   алгоритм детекции виральности (ССН, baseline)
│       ├── author-monitoring.md     #   мониторинг блогеров — расписание и оптимизации
│       ├── transcription-rewriting.md #   Whisper + LLM-переписывание с промптами
│       ├── llm-models.md            #   сравнение 367+ LLM через OpenRouter (verified prices)
│       └── cost-modeling.md         #   экономика: стоимость 1 миллионника + full pipeline
├── tests/                    # проверка структуры репо (pytest)
└── .github/workflows/        # CI: линтер markdown, валидация структуры
```

## Готовые коннекторы

| Коннектор | Эндпоинтов | Free-план (Basic) | Subscribe |
|---|---|---|---|
| [YT-API](connectors/yt-api.md) | 35 | 300 req/мес | [pricing](https://rapidapi.com/ytjar/api/yt-api/pricing) |
| [Telegram Channel](connectors/telegram-channel.md) | 2 | 100 req/мес | [pricing](https://rapidapi.com/akrakoro/api/telegram-channel/pricing) |
| [Threads API](connectors/threads-api4.md) | 12 | 50 req/мес | [pricing](https://rapidapi.com/Lundehund/api/threads-api4/pricing) |
| [TikTok API](connectors/tiktok-api23.md) | 56 | 100 req + 10 download/день | [pricing](https://rapidapi.com/Lundehund/api/tiktok-api23/pricing) |
| [Instagram Looter](connectors/instagram-looter2.md) | 30 | 150 req/мес | [pricing](https://rapidapi.com/irrors-apis/api/instagram-looter2/pricing) |

Все 5 коннекторов имеют **верифицированные** тарифы (выгружены прямо со страниц Pricing), реальные параметры эндпоинтов и формулы расчёта расходов.

## Методологии контент-завода

Не просто справочник API — но и playbook'и, как из коннекторов собрать рабочий конвейер.

| Playbook | О чём |
|---|---|
| [📋 pipeline-overview](docs/methodology/pipeline-overview.md) | Полный flow от "взяли блогера" до "получили переписанный скрипт". 7 этапов, очереди, приоритеты. |
| [🔥 viral-detection](docs/methodology/viral-detection.md) | Как **отличать виральное от популярного**. Метрика ССН, baseline по автору, тройной фильтр, готовые числовые пороги. |
| [👥 author-monitoring](docs/methodology/author-monitoring.md) | Расписание опроса авторов и видео, оптимизации квоты, авто-discovery новых блогеров. |
| [✍️ transcription-rewriting](docs/methodology/transcription-rewriting.md) | Whisper/AssemblyAI → LLM-переписывание. Готовые промпты под edu/comedy/lifestyle/business. Действия (rewrite/add_depth/change_cta). |
| [🤖 llm-models](docs/methodology/llm-models.md) | Сравнение **367+ моделей** через OpenRouter (Claude / GPT / Gemini / DeepSeek / Llama / Qwen ...). Tier'ы по бюджету. Какую модель под какую задачу. Verified цены. |
| [💰 cost-modeling](docs/methodology/cost-modeling.md) | Сколько стоит **1 миллионник** просмотров. 3 стека (бюджет / стандарт / премиум) с конкретными цифрами. Полная стоимость pipeline (RapidAPI + LLM + Whisper + Storage). |

## Full-stack setup

> 🛠️ **[docs/full-stack-setup.md](docs/full-stack-setup.md)** — пошаговая регистрация **всех сервисов**, нужных для запуска контент-завода:
>
> 1. RapidAPI (коннекторы соцсетей)
> 2. OpenRouter (LLM)
> 3. Whisper / Replicate / Deepgram / Yandex (транскрипция)
> 4. AWS S3 / Cloudflare R2 / Yandex Object Storage (хранение видео)
> 5. Telegram Bot (уведомления)
> 6. PostgreSQL (БД)
> 7. Redis / RabbitMQ (кэш + очереди)
> 8. VPS (Hetzner / DigitalOcean / Railway)
>
> С прямыми ссылками на регистрацию, полным `.env` примером, и финальными бюджетами для **Стартапа ($26/мес), SMB ($134/мес), Крупной редакции ($506/мес)**.

Методологии адаптированы из реальных продакшн-систем виральной аналитики Reels/Shorts/TikTok, обрабатывающих сотни авторов в день. Все числовые пороги — стартовые дефолты, проверенные практикой.

## Что умеет AI с этим скиллом

После установки нейронка получает структурированные знания и сможет:

1. **Писать корректные HTTP-запросы** к любому коннектору из карточки — с правильными заголовками (`X-RapidAPI-Key`, `X-RapidAPI-Host`), параметрами, форматом тела.
2. **Парсить ответы**, опираясь на реальные имена полей и структуру JSON из карточки (а не галлюцинировать).
3. **Отлаживать ошибки** (401/403/429, `200 OK` с `error` в теле, `414 URI Too Long`, истёкшие подписанные URL) — типичные сценарии и решения для каждого описаны в карточках.
4. **Считать расходы и подбирать тариф** под задачу пользователя (см. ниже).
5. **Предлагать оптимизации** — кэш, multi-id, дешёвые альтернативные эндпоинты, отказ от платных модификаторов.

## Расчёт расходов и тарифные планы

> 💰 Каждая карточка коннектора (`connectors/<имя>.md`) содержит отдельный раздел **«Тарифы и расчёт расходов»**. Когда пользователь спрашивает «сколько это будет стоить?» — AI берёт цифры оттуда, а не из памяти.

Что лежит в этом разделе у каждого коннектора:

- **Таблица тарифных планов** (Basic / Pro / Ultra / Mega) — реальные цифры с RapidAPI: requests/мес, rate-limit (req/час или req/сек), цена/мес, поведение при превышении (hard limit vs overage с ценой за extra-запрос).
- **Bandwidth** — сколько MB включено в план и цена за overage за каждый MB.
- **Стоимость одного запроса в квоте** — таблица модификаторов (`+1 за extend=1`, `+1 за forUsername`, `+1 за multi-id` и т.п.).
- **Формула расчёта месячной стоимости** — как из количества запросов и параметров получить $/мес.
- **Реальные сценарии** — 5-7 разобранных примеров с цифрами (учебный проект, дашборд канала, мониторинг, скрейпинг, скачивание файлов и т.д.).
- **Чеклист «как сэкономить квоту»** — конкретные приёмы (кэш, multi-id, дешёвые эндпоинты для polling).

### Универсальная формула (общая для всех коннекторов RapidAPI)

```
quota_per_request = 1 + sum(модификаторов с пометкой "+1 квота")
month_quota_usage  = quota_per_request × запросов_в_месяц
month_bandwidth_mb = средний_размер_ответа × запросов_в_месяц

# Тариф подбирается так, чтобы month_quota_usage помещался в req/мес плана
# Bandwidth-overage считается отдельно: (фактические_MB - включённые_MB) × $/MB

total_monthly = price(plan) + bandwidth_overage($)
```

### Пример

Пользователь хочет мониторить просмотры 100 видео каждые 5 минут:

- 100 видео × (60/5 = 12 раз/час) × 24 ч × 30 дней = **864 000 запросов/мес**
- Если использовать `/video/info` — 864 000 units → **Pro ($51) хватит** (лимит 1 770 500)
- Но через multi-id (10 за раз) — 86 400 HTTP-вызовов = в 10 раз ниже риск rate-limit
- Или с кэшем 5 минут — запросов вдвое меньше → можно остаться на **Basic ($0)**

### Что AI всегда сообщает пользователю

- Конкретную сумму в долларах: `$X (план) + $Y (bandwidth) = $Z в месяц`
- Какой план рекомендован и почему
- Список оптимизаций для удешевления
- Предупреждение про **rate-limit** (количество запросов в час — отдельно от месячного)
- Предупреждение про **hard limit vs overage** — на большинстве планов после превышения 429, без автодоплат

Полная универсальная инструкция в [SKILL.md](SKILL.md), раздел «Расчёт расходов».

## Установка

> 📖 Подробная инструкция от регистрации до первого запроса — в [docs/getting-started.md](docs/getting-started.md).

### Клонирование

```bash
git clone https://github.com/<your-org>/rapidapi-helper.git
cd rapidapi-helper
cp .env.example .env  # вписать свой RAPIDAPI_KEY (берётся в developer/security)
```

> ⚠️ Замени `<your-org>` на реальный аккаунт/организацию, где опубликован репо. Если он у тебя локально (преподаватель раздал по zip/курсу) — пропусти этот шаг и просто работай в полученной папке.

> 💡 Не пользуешься git? На странице репо в GitHub нажми **Code** → **Download ZIP**, распакуй и работай с папкой как обычно.

### Зависимости (для запуска примеров)

Через `pip` (Python 3.10+):

```bash
pip install -e .
```

Или через Docker (см. ниже).

## Подключение к ИИ-инструменту

Подходит для **любого** LLM-инструмента, но степень "автоматизации" разная. Выбирай свой вариант:

| Инструмент | Что подключаешь | Автоактивация |
|---|---|---|
| [Claude Code](docs/installation-claude-code.md) | папка в `~/.claude/skills/` | ✅ настоящий скилл (по `description`) |
| [Cursor](docs/installation-cursor.md) | `.cursor/rules/*.mdc` | ✅ через Cursor rules |
| [Claude Desktop / Cursor / Continue (через MCP)](docs/installation-mcp.md) | MCP-сервер с тулами | ✅ авто-вызов тулов |
| [Claude.ai Projects](docs/installation-claude-ai.md) | Project knowledge files | ⚠️ только через custom instructions |
| [ChatGPT (Custom GPT / Projects)](docs/installation-chatgpt.md) | knowledge files | ⚠️ только через custom instructions |
| [Anthropic / OpenAI SDK](docs/installation-via-api.md) | system prompt в коде (с prompt caching) | программно |
| [Любой generic LLM](docs/installation-generic-llm.md) (Gemini, Llama, DeepSeek, ...) | вставить bundle в чат | ❌ ручная вставка |

## Запуск примеров

В `examples/` лежит рабочий Python-код для каждого коннектора. Работает с любым коннектором, на который ты оформил подписку.

```bash
# YT-API
python -m examples.yt_api.search "claude api tutorial"
python -m examples.yt_api.video_info dQw4w9WgXcQ
python -m examples.yt_api.trending US

# Telegram Channel
python -m examples.telegram_channel.channel_info telegram
python -m examples.telegram_channel.latest_messages durov --limit 20

# Threads
python -m examples.threads_api4.user_posts reuters
python -m examples.threads_api4.search_threads "claude api"

# TikTok
python -m examples.tiktok_api23.user_videos charlidamelio
python -m examples.tiktok_api23.trending US

# Instagram
python -m examples.instagram_looter2.user_profile zuck
python -m examples.instagram_looter2.hashtag_feed travel
```

Все примеры используют общую обвязку `examples/common.py` — она подхватывает `RAPIDAPI_KEY` из `.env`, добавляет ретраи на 429/5xx и кэширует ответы на час, чтобы не сжигать квоту в разработке.

Через Docker:

```bash
docker compose build
docker compose run --rm app python -m examples.yt_api.search "claude api tutorial"
```

Не забудь прописать `RAPIDAPI_KEY` в `.env` и подписаться на нужный коннектор на RapidAPI.

## Добавление нового коннектора

```bash
python scripts/new_connector.py --name "weather-api" --host "weather-api123.p.rapidapi.com"
```

Скрипт создаст `connectors/weather-api.md` из шаблона. Дальше — заполни поля по документации с RapidAPI и (по желанию) добавь рабочие примеры в `examples/<имя>/`.

## Для преподавателей

Идея в том, чтобы ученики **сами** добавляли карточки коннекторов. Это двойная польза:

1. Учатся читать документацию API (пока перекладывают её в карточку).
2. Прокачивают общий инструмент, которым пользуются все.

Можно превратить в учебное задание: "выбери любой коннектор RapidAPI, напиши для него карточку и хотя бы один работающий пример". Pull request через Git — заодно тренировка работы с GitHub.

## Лицензия

MIT — см. [LICENSE](LICENSE).
