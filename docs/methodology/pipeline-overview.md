# Pipeline overview — полный flow контент-завода

Как собрать конвейер: блогер → виральное видео → транскрипция → переписанный скрипт под твою аудиторию.

## Высокоуровневая схема

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   1. INGEST           2. TRACK              3. DETECT               │
│   Добавили автора →   Опрос видео N×/час →  Алгоритм виральности →  │
│                                                                     │
│   4. ENRICH           5. TRANSCRIBE         6. REWRITE              │
│   Скачали + S3 →      Whisper/AssemblyAI →  LLM с промптом →        │
│                                                                     │
│   7. DELIVER                                                        │
│   Уведомление в Telegram + готовый скрипт в UI                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

7 этапов. Каждый — отдельная задача в очереди (RabbitMQ или SQS), запускается асинхронно.

## Этап 1. Ingest — добавили автора

**Что происходит:**
- Юзер вставляет URL Instagram/YouTube/TikTok автора.
- Система парсит платформу из URL ([platform detector](../../SKILL.md#общие-правила) или regex).
- По `username` (платформа Instagram) или `handle` (TikTok/Threads) или URL канала (YouTube) получает универсальный ID автора.

**Какой эндпоинт коннектора используется:**
- Instagram: [`/id`](../../connectors/instagram-looter2.md#-identity-utilities-4) → получаем `user_id`.
- TikTok: [`/api/user/info`](../../connectors/tiktok-api23.md) с `uniqueId` → получаем `secUid`.
- YouTube: [`/resolve`](../../connectors/yt-api.md) с URL/handle → получаем `browseId`.
- Threads: [`/api/user/info`](../../connectors/threads-api4.md) с `username` → получаем `pk`.

**Что сохраняется в БД:**
- `platform`, `external_id`, `username/handle`, `last_known_followers`, `last_known_avatar_url`.
- Кэш профиля целиком в `JSON`-поле — для быстрого UI.

**Аватарка** скачивается отдельной фоновой задачей (низкий приоритет) и кладётся в S3.

> 💡 Ingest **не блокируется** на скачивании аватара. UI показывает автора сразу, аватар подтягивается через ~30 сек.

## Этап 2. Track — мониторинг видео

Самая нагруженная часть pipeline.

**Расписание:**
- Активные авторы → опрос **каждый час**.
- Профили (метрики канала) → опрос **раз в сутки**.
- Новый автор → первый опрос **сразу**, потом по расписанию.

**Что собирается за один опрос:**
- Последние 30-50 видео (max что отдаёт API за один запрос).
- Для каждого видео: `id`, `taken_at`/`upload_date`, `view_count`, `like_count`, `comment_count`.

**Какие эндпоинты:**
- TikTok: [`/api/user/posts`](../../connectors/tiktok-api23.md) с `secUid`, `count=30`.
- Instagram: [`/user-feeds2`](../../connectors/instagram-looter2.md) с `id`, `count=30`.
- YouTube: [`/channel/videos`](../../connectors/yt-api.md) с `id`, `sort_by=newest`.
- Threads: [`/api/user/posts`](../../connectors/threads-api4.md) с `user_id`.

**Что записывается в БД:**

```
videos
  id (платформенный)
  author_id (FK)
  platform
  views_history: [{ts: 2026-04-28T10:00, views: 12000}, {ts: 11:00, views: 18500}, ...]
  first_seen_at
  last_checked_at
```

**Каждый час** добавляется новая точка в `views_history` — это ключевое для следующего этапа (детекция виральности по динамике).

> 💡 Используй кэш на 50-55 минут: одинаковый запрос внутри одного часа возвращает то же. Экономит 90%+ квоты.

## Этап 3. Detect — алгоритм виральности

Это самая важная часть — в [viral-detection.md](viral-detection.md) детально. Здесь — кратко.

**Не виральное:**
- Просто ≥ 100k просмотров.

**Виральное:**
- (а) Скорость набора просмотров за окно (`ССН` — средняя скорость набора) выше порогов **И**
- (б) Видео пересекло baseline автора (`avg_views` за 30 дней).

Без обоих условий — false positive (либо мега-блогер с миллионами по умолчанию, либо случайный всплеск).

**Расписание:**
- Анализ **каждый час** (после очередного track).

**Что записывается:**
- `trend_signals` — таблица флагов: какое видео когда пересекло порог, какой тип сигнала (`ССН`, `ССН1`, `ССН2`).
- `viral_content` — таблица "горячих" видео для дальнейшей обработки.

## Этап 4. Enrich — скачивание + S3

Найденное виральное видео нужно скачать и сохранить, чтобы:
- Транскрибировать (нужен файл).
- Сохранить копию (CDN-ссылки на оригинал быстро протухают).
- Отдавать клиентам в UI (own-CDN ссылки).

**Какие эндпоинты:**
- TikTok: [`/api/download/video`](../../connectors/tiktok-api23.md) с URL → возвращает прямой mp4.
- YouTube: [`/dl`](../../connectors/yt-api.md) с `id` + `cgeo` → массив форматов (берёшь муxed `itag=18` для совместимости).
- Instagram: [`/post-dl`](../../connectors/instagram-looter2.md) с URL → массив URL'ов для медиа.

**Куда сохраняется:**
- AWS S3 / Yandex Object Storage / любой совместимый storage.
- Путь: `users/{user_id}/videos/{platform}/{video_id}.mp4`.
- Aватарка: `avatars/{platform}/{author_id}.jpg`.

**Особенности:**
- Таймаут на скачивание: 60 секунд (большие видео — TikTok long-form > 60 сек могут не успеть, увеличь до 120).
- Параллельность: не больше 5 скачиваний одновременно (rate limit на CDN).
- Retry 3 раза с экспоненциальным backoff.

> ⚠️ **Bandwidth-overage** — главный нечаянный расход. Видео TikTok/Reels ~2-10 MB, Shorts ~5-15 MB, обычное YouTube ~50-300 MB. См. секции "Bandwidth" в карточках коннекторов.

## Этап 5. Transcribe — речь в текст

Детально в [transcription-rewriting.md](transcription-rewriting.md). Кратко:

- **Primary**: OpenAI Whisper API (`whisper-1`).
- **Fallback**: AssemblyAI.
- Auto-detect языка.
- Таймаут: 5 минут на видео.
- Цена: ~$0.006 за минуту видео (Whisper).

**Триггеры запуска:**
- Authomatic — после попадания в `viral_content` с приоритетом `urgent`/`high`.
- Manual — кнопка "Транскрибировать" в UI.

## Этап 6. Rewrite — переписывание скрипта

Детально в [transcription-rewriting.md](transcription-rewriting.md).

- **LLM**: OpenAI GPT-4 (через Assistants API) или Claude (через Anthropic API).
- 3 действия: `rewrite`, `add_depth`, `change_cta`.
- Промпты с локализацией (русский / другая аудитория).
- Каждый запрос — новый thread/conversation для изоляции контекста.

## Этап 7. Deliver — доставка

- Ссылка на видео + транскрипция + переписанный скрипт сохраняются в `viral_content`.
- Уведомление в Telegram (через Telegram Bot API) сотруднику/клиенту.
- В UI — отдельная вкладка "Готовые скрипты".

## Архитектура очередей (типы задач)

В реальной системе 10 типов очередей. Минимально достаточно 5:

| # | Очередь | Триггер | Параллелизм | Приоритет |
|---|---|---|---|---|
| 1 | `author_update` | Manual / Daily | 5 consumer'ов | 5 (normal), 8 (VIP) |
| 2 | `video_tracking` | Hourly | 10 consumer'ов | 6-9 |
| 3 | `viral_analysis` | Hourly после tracking | 1 (singleton) | 9 |
| 4 | `transcription` | После виральности | 2 consumer'а | 3-10 (по приоритету) |
| 5 | `script_rewriting` | Manual | 3 consumer'а | 5-7 |
| 6 | `video_download` | После виральности | 2 consumer'а | 5 |
| 7 | `avatar_download` | После ingest | 2 consumer'а | 3 (low) |

Plus периодические:
- `daily_profile_update` (02:00 UTC)
- `daily_author_update` (03:00 UTC)
- `daily_monitoring_update` (04:00 UTC)
- `daily_cleanup` (05:00 UTC) — чистит старые виральные сигналы (>48 часов)

## Приоритизация (1-10 шкала)

| Приоритет | Кто получает |
|---|---|
| **10** Urgent | VIP-пользователи (особый список user_id), горячие виральные видео |
| **8-9** High | Виральные видео обычных юзеров, ручные переключения |
| **5-7** Normal | Обычные обновления авторов и видео |
| **3-4** Low | Аватары, бэкграунд-задачи |
| **1-2** Very Low | Cleanup, статистика |

> 💡 Без приоритизации в часы пик (когда твоё VIP-задача стоит за 1000 обычных) ждёшь часами. С приоритетами — VIP проходит вперёд за минуты.

## Retry & Dead Letter Queue (DLQ)

- Каждая задача может ретриться **3 раза** перед попаданием в DLQ.
- Между ретраями — **2 секунды** (или экспоненциально: 2с, 8с, 30с).
- Задача **протухает** через 2 часа (TTL): если не успели обработать — в DLQ.
- DLQ-задачи разбираются вручную / отдельным консьюмером (логи, алерты).

## Технологический стек (минимально)

Что нужно для production:

- **Очередь**: RabbitMQ (mature, приоритеты, TTL) или Redis Streams (попроще).
- **БД**: PostgreSQL (JSON-поля для views_history, индексы для виральных запросов).
- **Storage**: S3-совместимый (AWS / Yandex / Cloudflare R2 / MinIO).
- **Cache**: Redis для кэша профилей и rate-limit-tracking.
- **LLM**: OpenAI или Anthropic API (см. transcription-rewriting.md).
- **Transcription**: OpenAI Whisper или AssemblyAI.
- **Backend**: Python (FastAPI / aiohttp) или Go.
- **Scheduler**: APScheduler / Celery Beat / cron.

Минимальный MVP можно сделать на:
- SQLite + Python multiprocessing/asyncio (без RabbitMQ).
- Локальная FS вместо S3.
- Без транскрипции/LLM — просто детекция и UI.

## Следующие шаги

- [viral-detection.md](viral-detection.md) — формулы и пороги детекции.
- [author-monitoring.md](author-monitoring.md) — конкретика по сбору и расписанию.
- [transcription-rewriting.md](transcription-rewriting.md) — промпты для LLM.
- [cost-modeling.md](cost-modeling.md) — сколько это всё стоит.
