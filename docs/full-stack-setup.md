# Full-stack setup — пошаговая настройка контент-завода

> 🎯 **Цель:** дать полный чек-лист "что и где зарегистрировать", чтобы запустить контент-завод от нуля до рабочего MVP. С прямыми ссылками на регистрацию каждого сервиса, что копировать в `.env`, сколько денег закладывать.
>
> 🕐 Время на прохождение: **1-2 часа** на регистрацию всего + начальный депозит.
>
> 💳 **Понадобится банковская карта.** Большинство сервисов привязывает её сразу при регистрации. Российские карты в 2026 принимаются не везде — закладывай зарубежную (Казахстан, Грузия, Турция, Wise, Revolut).

## Архитектура — что нам нужно

```
                                  ┌─────────────────┐
                                  │  RapidAPI       │ ← коннекторы соцсетей
                                  └─────────────────┘
                                          │
┌──────────────┐     ┌────────────┐      │
│   Твой Bot   │ ←── │  Backend   │ ←────┘
│  (Telegram)  │     │  (Python)  │
└──────────────┘     └────────────┘
                            │
              ┌─────────────┼──────────────┐
              ▼             ▼              ▼
      ┌────────────┐ ┌────────────┐ ┌────────────┐
      │ OpenRouter │ │  Whisper   │ │     S3     │
      │  (LLM)     │ │ (транскр.) │ │(хранение)  │
      └────────────┘ └────────────┘ └────────────┘
              │
              ▼
        ┌──────────┐
        │PostgreSQL│ ← БД (или SQLite на старте)
        │  + Redis │ ← кэш + очередь (или RabbitMQ)
        └──────────┘
```

**8 сервисов**, которые надо настроить. Полный чек-лист ниже.

---

## Чек-лист настройки

| # | Сервис | Зачем | Стоимость | Сложность |
|---|---|---|---|---|
| 1 | [RapidAPI](#1-rapidapi-коннекторы-соцсетей) | Доступ к коннекторам соцсетей (yt/tiktok/instagram/threads/telegram) | от $0 | ⭐ |
| 2 | [OpenRouter](#2-openrouter-универсальный-llm) | Универсальный LLM (Claude/GPT/Gemini/DeepSeek) для переписывания | от $5 минимум | ⭐ |
| 3 | [Whisper / Replicate / Deepgram](#3-транскрипция-аудио--текст) | Транскрипция видео в текст | от $0.001/мин | ⭐⭐ |
| 4 | [S3-storage](#4-s3-хранение-видеоаватаров) | Хранение скачанных видео и аватаров | от $0.005/GB | ⭐⭐ |
| 5 | [Telegram Bot](#5-telegram-bot-уведомления) | Уведомления о найденных виральных видео | бесплатно | ⭐ |
| 6 | [PostgreSQL](#6-postgresql-основная-бд) | Основная БД | от $0 | ⭐⭐⭐ |
| 7 | [Redis](#7-redis-кэш--очереди) | Кэш + очереди (или RabbitMQ) | от $0 | ⭐⭐ |
| 8 | [Хостинг бэкенда](#8-хостинг-vps--docker) | VPS для запуска backend | от $5/мес | ⭐⭐⭐ |

**Минимальный месячный бюджет (старт):** ~$30-50.

---

## 1. RapidAPI — коннекторы соцсетей

### Регистрация

1. Открой [rapidapi.com/auth/sign-up](https://rapidapi.com/auth/sign-up).
2. **Sign Up** через Google/GitHub/email.
3. Подтверди email.

### Получение ключа

1. Открой [Apps Dashboard](https://rapidapi.com/developer/dashboard).
2. У тебя автоматически создан `default-application`.
3. Открой [Security tab](https://rapidapi.com/developer/security) → скопируй **Application Key**.
4. Положи в `.env`:
   ```
   RAPIDAPI_KEY=abc123def456...
   ```

### Подписка на коннекторы (КРИТИЧНО!)

> ⚠️ **Один ключ работает со всеми API, но для каждого нужна отдельная подписка.** Без подписки — `403 You are not subscribed`.

Для каждого нужного коннектора оформи Basic (free) или платный план:

| Коннектор | Direct subscribe link | Basic free | Когда переходить на платный |
|---|---|---|---|
| YT-API | https://rapidapi.com/ytjar/api/yt-api/pricing | 300 req/мес | > 300 запросов в месяц |
| Telegram Channel | https://rapidapi.com/akrakoro/api/telegram-channel/pricing | 100 req/мес | > 100 |
| Threads API | https://rapidapi.com/Lundehund/api/threads-api4/pricing | 50 req/мес | почти сразу |
| TikTok API | https://rapidapi.com/Lundehund/api/tiktok-api23/pricing | 100 req + 10 dl/день | почти сразу |
| Instagram Looter | https://rapidapi.com/irrors-apis/api/instagram-looter2/pricing | 150 req/мес | > 150 |

### Стоимость

| Объём | Конфигурация | Месяц |
|---|---|---|
| Тест (10 авторов на платформе) | Все Basic | $0 |
| MVP (50 авторов) | TikTok Pro + Instagram Pro | $20 |
| Продакшн (500 авторов) | TikTok Ultra + IG Ultra + YT Pro | $130 |

### Подробности

См. [getting-started.md](getting-started.md) и [methodology/cost-modeling.md](methodology/cost-modeling.md).

---

## 2. OpenRouter — универсальный LLM

### Зачем именно OpenRouter

Один ключ — все 367+ моделей (Claude/GPT/Gemini/DeepSeek/Llama/Mistral/Qwen/Grok). Не надо по отдельности регистрироваться у каждого провайдера.

### Регистрация

1. Открой https://openrouter.ai/.
2. **Sign Up** через Google/GitHub/email.
3. Подтверди email.

### Депозит и ключ

1. Перейди в [Credits](https://openrouter.ai/settings/credits) → **Add Credits**.
2. Минимум **$5** (хватит на ~5000 переписываний на бюджетной модели).
3. Принимает Visa/Mastercard через Stripe (включая некоторые российские карты).
4. Иди в [Keys](https://openrouter.ai/settings/keys) → **Create Key**.
5. Положи в `.env`:
   ```
   OPENROUTER_API_KEY=sk-or-v1-...
   ```

### Выбор модели

См. [methodology/llm-models.md](methodology/llm-models.md). Стартовый стек:

```yaml
hook_analysis: openai/gpt-5-nano
classification: google/gemini-2.0-flash-lite-001
rewriting: deepseek/deepseek-v4-flash
fallback: openai/gpt-4o-mini
```

### Стоимость

| Объём (скриптов/мес) | Бюджетная модель | Премиум модель |
|---|---|---|
| 100 | $0.07 | $2.50 |
| 1 000 | $0.70 | $25 |
| 10 000 | $7 | $250 (с кэшем — $50) |

---

## 3. Транскрипция (аудио → текст)

Выбери **один** сервис из 4 — переключаться можно потом.

### Вариант A: OpenAI Whisper API (универсал)

- **Цена**: $0.006/мин.
- **Регистрация**: https://platform.openai.com → Sign Up → [API keys](https://platform.openai.com/api-keys) → **Create new secret key**.
- **Депозит**: минимум $5.
- **`.env`**:
  ```
  OPENAI_API_KEY=sk-...
  ```

### Вариант B: Replicate Whisper Large v3 (дешевле)

- **Цена**: $0.0008/мин (в 7 раз дешевле OpenAI!).
- **Регистрация**: https://replicate.com → Sign Up.
- **API Token**: [Account → API tokens](https://replicate.com/account/api-tokens) → **Create token**.
- **`.env`**:
  ```
  REPLICATE_API_TOKEN=r8_...
  ```
- Модель: `openai/whisper:8099696689d249cf8b122d833c36ac3f75505c666a395ca40ef26f68e7d3d16e`

### Вариант C: Deepgram (топ скорость)

- **Цена**: $0.0043/мин (Nova-2 model).
- **Регистрация**: https://console.deepgram.com/signup → бесплатно $200 кредитов на старт.
- **API Key**: автоматически создаётся → копируй.
- **`.env`**:
  ```
  DEEPGRAM_API_KEY=...
  ```

### Вариант D: Yandex SpeechKit (топ для RU)

- **Цена**: ~$0.0011/мин (₽0.10/сек).
- **Регистрация**: https://console.cloud.yandex.ru → создать сервисный аккаунт.
- **API Key**: через [IAM → Service Accounts](https://console.cloud.yandex.ru/folders/.../service-accounts).
- **`.env`**:
  ```
  YANDEX_API_KEY=...
  YANDEX_FOLDER_ID=...
  ```

> 💡 **Рекомендация для старта**: **Replicate** ($0.0008/мин). При объёмах > 1000 мин/день — переходи на локальный Whisper на GPU (без подписки).

### Стоимость

| Минут аудио в месяц | Whisper API | Replicate | Локально (GPU $50/мес) |
|---|---|---|---|
| 100 мин | $0.60 | $0.08 | $50 |
| 1 000 мин | $6 | $0.80 | $50 |
| 10 000 мин | $60 | $8 | $50 |

---

## 4. S3 — хранение видео/аватаров

Скачанные видео нужно где-то держать. Выбор сервисов:

### Вариант A: AWS S3 (стандарт индустрии)

- **Цена**: $0.023/GB/мес + $0.0004/1k запросов.
- **Регистрация**: https://aws.amazon.com → Create Account.
- **Bucket**: AWS Console → S3 → Create bucket.
- **API ключи**: IAM → Users → Create user → Access keys.
- **`.env`**:
  ```
  AWS_ACCESS_KEY_ID=AKIA...
  AWS_SECRET_ACCESS_KEY=...
  AWS_REGION=us-east-1
  S3_BUCKET=my-content-factory
  ```

### Вариант B: Cloudflare R2 (нет egress fees!)

- **Цена**: $0.015/GB/мес, **0$ за исходящий трафик** (это огромный плюс если ты раздаёшь видео клиентам).
- **Регистрация**: https://dash.cloudflare.com → R2 → Create bucket.
- **API ключи**: R2 → Manage R2 API Tokens.
- **`.env`**:
  ```
  R2_ACCOUNT_ID=...
  R2_ACCESS_KEY_ID=...
  R2_SECRET_ACCESS_KEY=...
  R2_BUCKET=my-content-factory
  R2_ENDPOINT=https://<account_id>.r2.cloudflarestorage.com
  ```

### Вариант C: Yandex Object Storage (для RU)

- **Цена**: ₽1.85/GB/мес (~$0.020).
- **Регистрация**: https://console.cloud.yandex.ru → Object Storage → Create bucket.
- **`.env`**:
  ```
  YC_ACCESS_KEY=...
  YC_SECRET_KEY=...
  YC_BUCKET=my-content-factory
  YC_ENDPOINT=https://storage.yandexcloud.net
  ```

### Вариант D: MinIO self-hosted (бесплатно, но геморрой)

Поднимаешь на своём VPS — 0$ кроме железа.

> 💡 **Рекомендация**: **Cloudflare R2** — ноль egress fees, S3-совместимое API.

### Стоимость

| GB в месяц (хранения) | AWS S3 | R2 | Yandex |
|---|---|---|---|
| 100 GB | $2.30 | $1.50 | $2.00 |
| 1 TB | $23 | $15 | $20 |
| Egress 1 TB | +$90 (AWS) | $0 | +$90 |

---

## 5. Telegram Bot — уведомления

Когда находим виральное видео / готовый скрипт — уведомление в Telegram юзеру.

### Регистрация

1. Открой [@BotFather](https://t.me/BotFather) в Telegram.
2. Команда `/newbot`.
3. Введи имя бота (любое) и username (должен заканчиваться на `bot`, например `my_content_factory_bot`).
4. BotFather пришлёт **HTTP API token** вида `1234567890:ABCdef...`.

### `.env`

```
TELEGRAM_BOT_TOKEN=1234567890:ABCdef...
```

### Получение `chat_id` юзера

Юзер должен сначала **написать твоему боту** `/start`. Затем бэкенд получает `chat_id` через update webhook или `/getUpdates`.

### Стоимость

**Бесплатно.** Telegram Bot API не имеет тарифов. Лимиты — 30 сообщений/секунду на бота.

### Минимальный пример

```python
import requests

def notify(chat_id: int, text: str, token: str = TELEGRAM_BOT_TOKEN):
    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
    )
```

---

## 6. PostgreSQL — основная БД

### Вариант A: Локально (Docker)

- **Цена**: 0$ (на твоём железе).
- **Запуск**:
  ```bash
  docker run -d --name pg \
    -e POSTGRES_PASSWORD=changeme \
    -p 5432:5432 \
    -v pgdata:/var/lib/postgresql/data \
    postgres:16
  ```
- **`.env`**:
  ```
  DATABASE_URL=postgresql://postgres:changeme@localhost:5432/content_factory
  ```

### Вариант B: Managed Postgres (для продакшна)

- **Supabase** ($0 free tier до 500 MB → платный $25/мес от 8 GB) — https://supabase.com.
- **Neon** ($0 free tier до 0.5 GB compute → $19/мес от 10 GB) — https://neon.tech.
- **Railway** ($5/мес минимум) — https://railway.app.
- **DigitalOcean Managed DB** ($15/мес от 1 GB) — https://digitalocean.com/products/managed-databases.

### Вариант C: SQLite на MVP

- **Цена**: 0$.
- Для < 100 авторов и тестов хватает.
- В Python: `from sqlalchemy import create_engine; engine = create_engine("sqlite:///app.db")`.

### Стоимость

| Объём | Локально | Managed |
|---|---|---|
| MVP (< 1 GB) | 0 | $0-19 |
| Продакшн (10 GB) | 0 (если есть VPS) | $25-50 |
| Большой (100 GB) | 0 | $100+ |

---

## 7. Redis — кэш + очереди

### Зачем

- **Кэш** профилей авторов на 24 часа (минус 95% запросов к API).
- **Очереди** задач (можно вместо RabbitMQ через Celery + Redis).
- **Rate limit** счётчики.

### Вариант A: Локально (Docker)

```bash
docker run -d --name redis -p 6379:6379 redis:7
```

`.env`:
```
REDIS_URL=redis://localhost:6379/0
```

### Вариант B: Upstash Redis (managed, есть free tier)

- **Цена**: $0 free tier (10k requests/day) → $0.20 за 100k запросов.
- **Регистрация**: https://upstash.com → Create Database.
- **`.env`**:
  ```
  REDIS_URL=redis://default:<password>@<host>.upstash.io:<port>
  ```

### Вариант C: Redis Cloud (managed от Redis Labs)

- **Цена**: $0 free до 30 MB → $5/мес от 100 MB.
- https://redis.com/try-free.

### Когда нужен RabbitMQ вместо Redis

При **> 10 000 задач/день** и нужны:
- Приоритеты (1-10).
- TTL задач.
- Dead Letter Queue.

Тогда поднимай RabbitMQ через Docker:
```bash
docker run -d --name rabbitmq \
  -p 5672:5672 -p 15672:15672 \
  rabbitmq:3-management
```

---

## 8. Хостинг — VPS / Docker

Где запускать backend (Python).

### Вариант A: Свой VPS

- **Hetzner Cloud** — от €4/мес (2 vCPU, 4 GB) — https://www.hetzner.com/cloud.
- **DigitalOcean Droplet** — от $6/мес — https://digitalocean.com.
- **Vultr** — от $5/мес — https://vultr.com.
- **Selectel** (RU) — от ₽270/мес — https://selectel.ru.
- **TimeWeb Cloud** (RU) — от ₽180/мес — https://timeweb.cloud.

### Вариант B: PaaS (без VPS-настройки)

- **Railway** ($5/мес) — https://railway.app — деплой через `git push`.
- **Render** (бесплатный tier с засыпанием, $7 за всегда-on) — https://render.com.
- **Fly.io** ($5+ зависит от использования) — https://fly.io.

### Вариант C: Serverless

- **AWS Lambda + API Gateway** — pay-per-use.
- **Cloudflare Workers** — $0 free до 100k requests/день.
- Для контент-завода с фоновыми задачами **не лучший выбор** — нужно постоянное состояние.

### Минимальные требования VPS

- **Для MVP** (10-50 авторов): 1 vCPU, 1 GB RAM, 25 GB SSD (~$5/мес).
- **Для продакшна** (100-500 авторов): 2 vCPU, 4 GB RAM, 80 GB SSD (~$15/мес).
- **Большой проект** (1000+ авторов): 4+ vCPU, 8+ GB RAM, 160+ GB SSD (~$40/мес).

### Деплой через Docker

```yaml
# docker-compose.yml
services:
  app:
    build: .
    env_file: .env
    depends_on: [pg, redis]

  pg:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: changeme
    volumes: [pgdata:/var/lib/postgresql/data]

  redis:
    image: redis:7
    volumes: [redisdata:/data]

volumes:
  pgdata:
  redisdata:
```

---

## Финальный `.env` — собранный воедино

После всей регистрации твой `.env` выглядит так:

```env
# === RapidAPI (коннекторы соцсетей) ===
RAPIDAPI_KEY=abc123...

# === OpenRouter (LLM) ===
OPENROUTER_API_KEY=sk-or-v1-...

# === Транскрипция (выбери один) ===
OPENAI_API_KEY=sk-...                 # если Whisper API
REPLICATE_API_TOKEN=r8_...            # если Replicate
DEEPGRAM_API_KEY=...                  # если Deepgram
YANDEX_API_KEY=...                    # если SpeechKit
YANDEX_FOLDER_ID=...

# === S3 (выбери один) ===
AWS_ACCESS_KEY_ID=AKIA...             # AWS
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
S3_BUCKET=my-content-factory

R2_ACCOUNT_ID=...                     # или Cloudflare R2
R2_ACCESS_KEY_ID=...
R2_SECRET_ACCESS_KEY=...
R2_BUCKET=...
R2_ENDPOINT=https://...r2.cloudflarestorage.com

# === Telegram Bot ===
TELEGRAM_BOT_TOKEN=1234567890:ABCdef...

# === БД и очереди ===
DATABASE_URL=postgresql://user:pass@host:5432/content_factory
REDIS_URL=redis://localhost:6379/0
```

---

## Итоговый месячный бюджет

### Стартап (MVP, 50 авторов)

| Сервис | Цена/мес |
|---|---|
| RapidAPI: Telegram Pro + IG Pro | $20 |
| OpenRouter (1k скриптов на DeepSeek) | $1 |
| Replicate Whisper (200 мин) | $0.16 |
| Cloudflare R2 (10 GB) | $0.15 |
| VPS Hetzner | $5 |
| Telegram Bot | $0 |
| **ИТОГО** | **~$26/мес** |

### Малый бизнес (300 авторов)

| Сервис | Цена/мес |
|---|---|
| RapidAPI: TikTok Pro + IG Ultra + YT Pro | $89 |
| OpenRouter (5k скриптов на gpt-4o-mini) | $3 |
| Replicate Whisper (1500 мин) | $1.20 |
| Cloudflare R2 (50 GB) | $0.75 |
| VPS DigitalOcean | $15 |
| Managed Postgres (Supabase) | $25 |
| **ИТОГО** | **~$134/мес** |

### Крупная редакция (1000+ авторов, премиум)

| Сервис | Цена/мес |
|---|---|
| RapidAPI: TikTok Ultra + IG Mega + YT Ultra + Threads Pro | $349 |
| OpenRouter (20k скриптов: deepseek + claude-haiku premium) | $30 |
| Whisper local (на GPU VPS) | $50 |
| Cloudflare R2 (500 GB) | $7.50 |
| VPS Hetzner CPX31 (4 vCPU, 8 GB) | $20 |
| Managed Postgres + Redis | $50 |
| **ИТОГО** | **~$506/мес** |

---

## FAQ

### С чего начать тестирование?

1. Зарегься на RapidAPI + подпишись на Basic-планы 1-2 коннекторов.
2. Зарегься на OpenRouter, депозит $5.
3. Replicate API token (тестовых $0.01 хватит на десятки минут).
4. Telegram Bot создай.
5. Локально запусти PostgreSQL + Redis в Docker.
6. Деплой не нужен — пиши код в IDE и запускай локально.

**Можно проверить весь pipeline на 5 авторах за $5-10.**

### Какие сервисы можно совместить?

- **OpenRouter заменяет** OpenAI (для LLM, но не для Whisper).
- **Replicate** даёт и LLM, и Whisper, и многое другое — можно использовать как универсальный.
- **Cloudflare R2 + Workers** — можно весь pipeline (storage + serverless backend) делать в одном Cloudflare.

### Что если карты не работают?

Wise / Revolut / Payoneer — виртуальные карты в долларах/евро, принимаются почти везде. Альтернатива — карта банка из РБ/Казахстана/Грузии.

### Как масштабироваться

1. Стартуй с локального хостинга и Basic-планов всех сервисов.
2. После 100 авторов — переход на Pro-планы RapidAPI.
3. После 500 — managed PostgreSQL и больший VPS.
4. После 1000 — собственный Whisper на GPU + Mega-планы.
5. После 10000 — рассмотри прямые ключи (Anthropic/OpenAI) вместо OpenRouter (-5% наценки).

### Куда дальше

- [getting-started.md](getting-started.md) — простой first-call после настройки RapidAPI.
- [methodology/README.md](methodology/README.md) — методологии работы контент-завода.
- [methodology/cost-modeling.md](methodology/cost-modeling.md) — детальные формулы расчёта.
- [methodology/llm-models.md](methodology/llm-models.md) — выбор LLM-модели под задачу.
- [installation-via-api.md](installation-via-api.md) — программная интеграция со скиллом.
