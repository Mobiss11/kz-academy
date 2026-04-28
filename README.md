# kz-academy

> 🎓 **Учебная база знаний КонтентЗавода** — всё что нужно ученику, чтобы построить свой контент-завод с нуля: от регистрации сервисов до рабочего конвейера виральной аналитики и переписывания скриптов.

---

## 🚀 Установка скилла к себе (60 секунд)

Скилл подключается **к твоему ИИ-ассистенту** (Claude Code, Cursor, ChatGPT и т.д.) и даёт ему структурированные знания про коннекторы соцсетей и контент-завод. Без скилла нейронка галлюцинирует имена эндпоинтов и параметров. Со скиллом — даёт точный код.

### Шаг 1. Клонируй репо

```bash
git clone https://github.com/Mobiss11/kz-academy.git
cd kz-academy
```

> 💡 Не пользуешься git? → **Code → Download ZIP** на странице репо, распакуй и работай с папкой.

### Шаг 2. Подключи к своему ИИ — выбери свой инструмент

| Твой инструмент | Что делать | Подробно |
|---|---|---|
| **🟣 Claude Code** (CLI) | `cp -R . ~/.claude/skills/kz-academy/` — Claude сам подхватит скилл по `description` | [installation-claude-code.md](docs/installation-claude-code.md) |
| **🔵 Cursor** | Создать `.cursor/rules/kz-academy.mdc` со ссылкой на этот клон | [installation-cursor.md](docs/installation-cursor.md) |
| **🟢 Claude Desktop / Continue / Cline** (через MCP) | Запустить `python -m scripts.mcp_server` и добавить в config клиента | [installation-mcp.md](docs/installation-mcp.md) |
| **🟡 Claude.ai (web)** | Загрузить `SKILL.md` + нужные карточки в Project knowledge | [installation-claude-ai.md](docs/installation-claude-ai.md) |
| **🟡 ChatGPT (Plus/Team)** | Загрузить файлы в Project / Custom GPT knowledge | [installation-chatgpt.md](docs/installation-chatgpt.md) |
| **⚙️ Свой бот через Anthropic/OpenAI SDK** | Подгружать `SKILL.md` + карточки в system prompt программно (с prompt caching!) | [installation-via-api.md](docs/installation-via-api.md) |
| **⚪ Любой generic LLM** (Gemini, Llama, DeepSeek...) | `python scripts/bundle.py > bundle.md` — вставить в system prompt чата | [installation-generic-llm.md](docs/installation-generic-llm.md) |

### Шаг 3. Проверь что AI видит скилл

Спроси у нейронки:

> Какие коннекторы есть в kz-academy? Какие у TikTok-API эндпоинты для скачивания видео?

Правильный ответ упомянет конкретные эндпоинты вроде `/api/download/video`, `/api/download/music`, `/api/download/user/video` — это значит ИИ прочитал [connectors/tiktok-api23.md](connectors/tiktok-api23.md). Если нейронка отвечает общими словами — что-то с подключением, перечитай инструкцию для своего инструмента.

### Шаг 4. (Опционально) Установи Python-зависимости для запуска готовых примеров

```bash
cp .env.example .env  # вписать ключи (минимум RAPIDAPI_KEY)
pip install -e .
python scripts/check_env.py  # smoke-test всех настроенных сервисов
```

---

## 📖 Что внутри скилла

После подключения нейронка получает структурированные знания про:

- 🔌 **5 готовых RapidAPI-коннекторов** соцсетей (YouTube, TikTok, Instagram, Threads, Telegram) — все эндпоинты, параметры, тарифы.
- 🏭 **Методологии контент-завода** — мониторинг блогеров, виральная детекция, транскрипция, переписывание скриптов.
- 💰 **Реальная экономика** — тарифы verified из API, формулы расчёта, точки перехода между планами.
- 🤖 **Сравнение 367+ LLM** через OpenRouter (Claude / GPT / Gemini / DeepSeek / ...) с актуальными ценами.
- 🛠️ **Где зарегистрировать всё** — RapidAPI, OpenRouter, Whisper, S3, Telegram Bot, БД, VPS — с прямыми ссылками.

Концепция: **AI + структурированный контекст = надёжный код без галлюцинаций.**

---

## Зачем это

Ты строишь контент-завод (платформу аналитики виральных Reels/Shorts/TikTok с переписыванием скриптов под свою нишу) и хочешь:

- ✅ Не галлюцинировать имена эндпоинтов и параметров API.
- ✅ Точно знать **сколько денег уйдёт** до того как написал первую строку кода.
- ✅ Подобрать модели и сервисы под бюджет: **Стартап ($26/мес) — SMB ($134) — Крупная редакция ($506)**.
- ✅ Не изобретать алгоритм виральной детекции (он тут уже описан с числовыми порогами).
- ✅ Получать готовые промпты для переписывания и понимать **как** настраивать их под свою аудиторию.

---

## Готовые коннекторы

| Коннектор | Эндпоинтов | Free-план (Basic) | Subscribe |
|---|---|---|---|
| [YT-API](connectors/yt-api.md) | 35 | 300 req/мес | [pricing](https://rapidapi.com/ytjar/api/yt-api/pricing) |
| [Telegram Channel](connectors/telegram-channel.md) | 2 | 100 req/мес | [pricing](https://rapidapi.com/akrakoro/api/telegram-channel/pricing) |
| [Threads API](connectors/threads-api4.md) | 12 | 50 req/мес | [pricing](https://rapidapi.com/Lundehund/api/threads-api4/pricing) |
| [TikTok API](connectors/tiktok-api23.md) | 56 | 100 req + 10 download/день | [pricing](https://rapidapi.com/Lundehund/api/tiktok-api23/pricing) |
| [Instagram Looter](connectors/instagram-looter2.md) | 30 | 150 req/мес | [pricing](https://rapidapi.com/irrors-apis/api/instagram-looter2/pricing) |

Все 5 коннекторов имеют **верифицированные тарифы** (выгружены прямо со страниц Pricing), реальные параметры эндпоинтов и формулы расчёта расходов.

---

## Методологии контент-завода

Не просто справочник API — playbook'и, как из коннекторов собрать рабочий конвейер.

| Playbook | О чём |
|---|---|
| [📋 pipeline-overview](docs/methodology/pipeline-overview.md) | Полный flow от "взяли блогера" до "получили переписанный скрипт". 7 этапов, очереди, приоритеты. |
| [🔥 viral-detection](docs/methodology/viral-detection.md) | Как **отличать виральное от популярного**. Метрика ССН, baseline по автору, тройной фильтр, готовые числовые пороги. |
| [👥 author-monitoring](docs/methodology/author-monitoring.md) | Расписание опроса авторов и видео, оптимизации квоты, авто-discovery новых блогеров. |
| [✍️ transcription-rewriting](docs/methodology/transcription-rewriting.md) | Whisper/AssemblyAI → LLM-переписывание. Готовые промпты под edu/comedy/lifestyle/business. Действия (rewrite/add_depth/change_cta). |
| [🤖 llm-models](docs/methodology/llm-models.md) | Сравнение **367+ моделей** через OpenRouter (Claude / GPT / Gemini / DeepSeek / Llama / Qwen ...). Tier'ы по бюджету. Какую модель под какую задачу. Verified цены. |
| [💰 cost-modeling](docs/methodology/cost-modeling.md) | Сколько стоит **1 миллионник** просмотров. 3 стека (бюджет/стандарт/премиум) с конкретными цифрами. Полная стоимость pipeline (RapidAPI + LLM + Whisper + Storage). |

Методологии адаптированы из реальной продакшн-системы виральной аналитики Reels/Shorts/TikTok, обрабатывающей сотни авторов в день. Все числовые пороги — стартовые дефолты, проверенные практикой.

---

## Full-stack setup — где зарегать всё

> 🛠️ **[docs/full-stack-setup.md](docs/full-stack-setup.md)** — пошаговая регистрация **всех 8 сервисов**:
>
> 1. **RapidAPI** — коннекторы соцсетей
> 2. **OpenRouter** — универсальный LLM (Claude/GPT/Gemini/DeepSeek через один ключ)
> 3. **Whisper / Replicate / Deepgram / Yandex** — транскрипция
> 4. **AWS S3 / Cloudflare R2 / Yandex Object Storage** — хранение видео
> 5. **Telegram Bot** — уведомления
> 6. **PostgreSQL** — БД
> 7. **Redis / RabbitMQ** — кэш и очереди
> 8. **VPS** (Hetzner / DigitalOcean / Railway)
>
> С прямыми ссылками на регистрацию, полным `.env` примером, и финальными бюджетами для **Стартапа ($26/мес), SMB ($134/мес), Крупной редакции ($506/мес)**.

Если ты впервые с RapidAPI и хочешь только сделать первый запрос — открой [docs/getting-started.md](docs/getting-started.md) (быстрее, минимум для теста).

---

## Что умеет AI с этим скиллом

После подключения нейронка получает структурированные знания и сможет:

1. **Писать корректные HTTP-запросы** к любому коннектору с правильными заголовками и параметрами.
2. **Парсить ответы**, опираясь на реальные имена полей и структуру JSON (а не галлюцинировать).
3. **Отлаживать ошибки** (401/403/429, 200 OK с error в теле, 414 URI Too Long, истёкшие подписанные URL) — типичные сценарии описаны в каждой карточке.
4. **Считать расходы и подбирать тариф** — формулы расчёта в [cost-modeling](docs/methodology/cost-modeling.md).
5. **Предлагать оптимизации** — кэш, multi-id batch, дешёвые альтернативные эндпоинты.
6. **Выбирать LLM-модель** под задачу (бюджет / стандарт / премиум) — сравнение в [llm-models](docs/methodology/llm-models.md).
7. **Строить pipeline контент-завода** — алгоритм виральной детекции, мониторинг, переписывание (методологии в `docs/methodology/`).

---

## Запуск примеров

В `examples/` — рабочий Python-код по каждому коннектору. Работает на любом коннекторе, на который ты оформил подписку.

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

Все примеры используют общую обвязку [examples/common.py](examples/common.py) — она подхватывает `RAPIDAPI_KEY` из `.env`, добавляет ретраи на 429/5xx и кэширует ответы на час, чтобы не сжигать квоту в разработке.

Через Docker:

```bash
docker compose build
docker compose run --rm app python -m examples.yt_api.search "claude api tutorial"
```

---

## Расчёт расходов на пальцах

Универсальная формула (общая для всех коннекторов RapidAPI):

```
quota_per_request  = 1 + sum(модификаторов с пометкой "+1 квота")
month_quota_usage  = quota_per_request × запросов_в_месяц
month_bandwidth_mb = средний_размер_ответа × запросов_в_месяц

total_monthly = price(plan) + bandwidth_overage($)
```

**Пример.** Хочется мониторить просмотры 100 видео каждые 5 минут:

- 100 × (60/5) × 24 × 30 = **864 000 запросов/мес**
- На YT-API через `/video/info` → **Pro $51** (лимит 1 770 500)
- Через multi-id (10 за раз) — те же 864k units, но в **10× меньше HTTP-вызовов**
- Или с кэшем 5 минут — запросов вдвое меньше → можно остаться на Basic ($0)

AI всегда сообщает: **сумма + рекомендованный план + список оптимизаций + предупреждение про rate-limit**.

---

## Добавление нового коннектора

```bash
python scripts/new_connector.py --name "weather-api" --host "weather-api123.p.rapidapi.com"
```

Скрипт создаст `connectors/weather-api.md` из шаблона. Дальше заполни поля по документации с RapidAPI и (по желанию) добавь рабочие примеры в `examples/<имя>/`.

---

## Для преподавателей

Идея — ученики **сами** добавляют карточки коннекторов. Двойная польза:

1. Учатся читать документацию API (пока перекладывают её в карточку).
2. Прокачивают общий инструмент, которым пользуются все.

**Учебное задание:** "выбери любой коннектор RapidAPI, напиши для него карточку и хотя бы один работающий пример." Pull request через Git — заодно тренировка GitHub.

---

## Полная структура репозитория

```
kz-academy/
├── SKILL.md                            # главный файл-роутер: общие правила + расчёт расходов
├── README.md                           # этот файл
├── connectors/
│   ├── _template.md                    # шаблон для новой карточки
│   ├── yt-api.md                       # YT-API (ytjar) — 35 эндпоинтов
│   ├── telegram-channel.md             # Telegram Channel (akrakoro) — 2 эндпоинта
│   ├── threads-api4.md                 # Threads (Lundehund) — 12 эндпоинтов
│   ├── tiktok-api23.md                 # TikTok (Lundehund) — 56 эндпоинтов
│   └── instagram-looter2.md            # Instagram (irrors-apis) — 30 эндпоинтов
├── examples/                           # рабочий Python-код по каждому коннектору
│   ├── common.py                       # общая обвязка (ключ, ретраи, кэш)
│   ├── yt_api/                         # search, video_info, trending
│   ├── telegram_channel/               # channel_info, latest_messages
│   ├── threads_api4/                   # user_posts, search_threads
│   ├── tiktok_api23/                   # user_videos, trending
│   └── instagram_looter2/              # user_profile, hashtag_feed
├── scripts/
│   ├── new_connector.py                # CLI: создать новую карточку из шаблона
│   ├── bundle.py                       # склеить SKILL.md + карточки для generic LLM
│   ├── mcp_server.py                   # MCP-сервер для Claude Desktop / Cursor / Continue
│   └── check_env.py                    # smoke-test всех настроенных сервисов
├── docs/
│   ├── getting-started.md              # 🚀 онбординг от нуля до первого запроса
│   ├── full-stack-setup.md             # 🛠️ регистрация ВСЕХ сервисов
│   ├── installation-claude-code.md     # подключение к Claude Code (нативный скилл)
│   ├── installation-cursor.md          # подключение к Cursor (.cursor/rules/)
│   ├── installation-claude-ai.md       # подключение к Claude.ai Projects
│   ├── installation-chatgpt.md         # подключение к ChatGPT (Project / Custom GPT)
│   ├── installation-mcp.md             # подключение через MCP (любой MCP-клиент)
│   ├── installation-via-api.md         # программное подключение через SDK
│   └── installation-generic-llm.md     # для Gemini / Llama / локальных моделей
│   └── methodology/
│       ├── README.md                   # индекс методологий
│       ├── pipeline-overview.md        # полный flow контент-завода
│       ├── viral-detection.md          # алгоритм детекции виральности (ССН, baseline)
│       ├── author-monitoring.md        # мониторинг блогеров — расписание и оптимизации
│       ├── transcription-rewriting.md  # Whisper + LLM-переписывание с промптами
│       ├── llm-models.md               # сравнение 367+ LLM через OpenRouter
│       └── cost-modeling.md            # экономика: 1 миллионник + full pipeline
├── tests/                              # pytest проверка структуры
├── .github/workflows/                  # CI: линтер markdown + тесты структуры
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── .env.example                        # шаблон с 8 сервисами (закомментировано что не нужно)
```

---

## Лицензия

MIT — см. [LICENSE](LICENSE).
