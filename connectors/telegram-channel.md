# Telegram Channel (akrakoro)

**Провайдер:** akrakoro
**Страница:** https://rapidapi.com/akrakoro/api/telegram-channel
**Subscribe (Pricing):** https://rapidapi.com/akrakoro/api/telegram-channel/pricing
**Base URL:** `https://telegram-channel.p.rapidapi.com`
**Host-заголовок:** `telegram-channel.p.rapidapi.com`

> ⚠️ **Перед первым запросом — оформи подписку** на странице Pricing. Без подписки любой вызов вернёт `403`. Free-план — **Basic**, оформляется в один клик, **требует привязанную карту**. Подробности в [docs/getting-started.md](../docs/getting-started.md).

Лёгкий API для чтения **публичных** Telegram-каналов: метаданные канала (название, описание, число подписчиков, превью) и последние сообщения с медиа-вложениями. **Только публичные каналы**, без авторизации в Telegram-аккаунт. **2 эндпоинта**, оба GET.

> ✅ **Источник схемы.** Карточка собрана из RapidAPI Playground (params + Example Responses обоих эндпоинтов). Тарифы и формат 401 ошибки — verified живым вызовом. JSON-примеры ниже — реальные имена полей.
>
> Данные могут устареть. Перед прод-кодом сверяйся с playground.

## Авторизация

Стандартная пара заголовков RapidAPI (см. [SKILL.md](../SKILL.md)):

```
X-RapidAPI-Key: <ключ>
X-RapidAPI-Host: telegram-channel.p.rapidapi.com
```

**Формат ошибки 401** (verified):

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{"message": "Invalid API key. Go to https://docs.rapidapi.com/docs/keys for more info."}
```

## Общие заголовки

| Заголовок | Обяз. | Назначение |
|---|---|---|
| `X-RapidAPI-Key` | ✅ | твой ключ |
| `X-RapidAPI-Host` | ✅ | `telegram-channel.p.rapidapi.com` |

Этот коннектор не имеет специфичных заголовков (`X-TOKEN`, `X-CACHEBYPASS` и т.п.) — только два стандартных.

## Эндпоинты

### `GET /channel/info` — метаданные публичного канала

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `channel` | string | ✅ | публичное имя канала (без `@`, без `t.me/`) |

**Пример ответа** (verified — 7 keys):

```json
{
  "verified": true,
  "chat_type": "channel",
  "title": "Telegram News",
  "description": "The official Telegram on Telegram. Much recursion. Very Telegram. Wow.",
  "image": "https://cdn1.telegram-cdn.org/.../photo.jpg",
  "subscribers": "6115045",
  "subscribers_online": "0"
}
```

Заметки:
- `chat_type` — здесь `"channel"` (приватные/гигачаты/боты этим API не отдаются).
- `verified` — официальная галочка Telegram.
- `subscribers_online` бывает `"0"` для каналов (это поле обычно показывает онлайн в группах). Не полагайся на него для каналов.
- `image` — подписанная CDN-ссылка, может протухнуть. При выводе в UI лучше скачать и закэшировать у себя.

### `GET /channel/message` — последние сообщения канала

| Параметр | Тип | Обяз. | Описание | По умолчанию |
|---|---|---|---|---|
| `channel` | string | ✅ | публичное имя канала | — |
| `limit` | number | – | количество сообщений (максимум **50**) | `5` |
| `max_id` | number | – | потолок message ID — все сообщения с ID **строго больше** этого исключаются. Используется для пагинации (см. ниже) | `999999999` |

**Пример ответа** (verified — массив сообщений, 16 keys per item):

```json
[
  {
    "id": 12345,
    "author": "...",
    "date": "2025-04-28 10:30:00",
    "user_read_status": "...",
    "text": "Plain text content",
    "html": "<p>HTML rendered content with <b>formatting</b></p>",
    "views": "5.2K",
    "forwarded": null,
    "button": null,
    "link": {
      "description": "...",
      "name": "...",
      "title": "...",
      "url": "https://..."
    },
    "photo": "https://cdn4.telegram-cdn.org/.../photo.jpg",
    "video": {
      "caption": "...",
      "url": "https://cdn4.telegram-cdn.org/.../video.mp4"
    },
    "audio": null,
    "sticker": null,
    "attachment": null,
    "media_poll": null
  }
]
```

**Ключи в каждом сообщении** (16 штук):

| Поле | Тип | Что |
|---|---|---|
| `id` | number | message ID — монотонно растёт по времени |
| `author` | string \| null | имя автора (для каналов часто `null`) |
| `date` | string | timestamp поста |
| `user_read_status` | string \| null | статус прочтения |
| `text` | string \| null | текст сообщения plain |
| `html` | string \| null | HTML-версия (с разметкой Telegram) |
| `views` | string \| null | счётчик просмотров (формата `"5.2K"`/`"1.3M"` — строка, не число!) |
| `forwarded` | object \| null | данные о пересылке (если форвард) |
| `button` | object \| null | inline-кнопки поста |
| `link` | object \| null | развёрнутый превью ссылки `{description, name, title, url}` |
| `photo` | string \| null | URL фото (если медиа — фото) |
| `video` | object \| null | `{caption, url}` |
| `audio` | object \| null | аудио-вложение |
| `sticker` | object \| null | стикер |
| `attachment` | object \| null | произвольный файл |
| `media_poll` | object \| null | опрос |

#### Пагинация

API не возвращает `continuation`/`token` — пагинация делается через `max_id`. Telegram использует **возрастающие** ID, поэтому:

```
batch1 = GET /channel/message?channel=durov&limit=50         # самые свежие
min_id = min(msg["id"] for msg in batch1)
batch2 = GET /channel/message?channel=durov&limit=50&max_id={min_id - 1}   # старее
min_id = min(msg["id"] for msg in batch2)
batch3 = ...
```

Если `len(batch) < limit` — достигнут самый старый пост в канале.

> ⚠️ **`limit` максимум 50.** Если запросить больше — провайдер всё равно отдаст 50 (или ошибку). Чтобы выгрузить весь канал — итерируй с `limit=50`.

#### Парсинг media-полей

В каждом сообщении только одно из медиа-полей будет заполнено (или ни одного). Универсальный парсер:

```python
def extract_media(msg):
    if msg.get("photo"):
        return ("photo", msg["photo"])
    if msg.get("video"):
        return ("video", msg["video"]["url"])
    if msg.get("audio"):
        return ("audio", msg["audio"])
    if msg.get("sticker"):
        return ("sticker", msg["sticker"])
    if msg.get("attachment"):
        return ("file", msg["attachment"])
    if msg.get("media_poll"):
        return ("poll", msg["media_poll"])
    return (None, None)
```

#### Парсинг счётчика `views`

Поле `views` — это **строка** в человекочитаемом формате (`"5.2K"`, `"1.3M"`, `"42"`). Конвертация в int:

```python
def parse_views(v):
    if not v:
        return 0
    v = v.strip().upper().replace(",", ".")
    if v.endswith("K"):
        return int(float(v[:-1]) * 1_000)
    if v.endswith("M"):
        return int(float(v[:-1]) * 1_000_000)
    return int(v)
```

---

## Минимальные рабочие примеры

### Получить инфу о канале

```python
import os, requests

API_KEY = os.environ["RAPIDAPI_KEY"]
HOST = "telegram-channel.p.rapidapi.com"
headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": HOST}

r = requests.get(f"https://{HOST}/channel/info",
                 headers=headers, params={"channel": "telegram"}, timeout=15)
r.raise_for_status()
data = r.json()
print(f"{data['title']} — {data['subscribers']} subscribers, verified={data['verified']}")
```

### Свежие 50 сообщений с фильтром по медиа

```python
r = requests.get(f"https://{HOST}/channel/message",
                 headers=headers, params={"channel": "telegram", "limit": 50})
messages = r.json()

for m in messages:
    media_type, media_url = extract_media(m)
    print(f"#{m['id']} [{m['date']}] views={m['views']} media={media_type}")
    print(f"  {(m.get('text') or '')[:120]}")
```

### Полная выгрузка канала с пагинацией

```python
def crawl_channel(channel, max_messages=10000):
    HOST = "telegram-channel.p.rapidapi.com"
    headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": HOST}
    max_id = 999999999
    all_msgs = []
    while len(all_msgs) < max_messages:
        r = requests.get(f"https://{HOST}/channel/message",
                         headers=headers,
                         params={"channel": channel, "limit": 50, "max_id": max_id},
                         timeout=15)
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        all_msgs.extend(batch)
        new_max = min(m["id"] for m in batch) - 1
        if new_max == max_id:
            break  # safety: ничего нового
        max_id = new_max
        if len(batch) < 50:
            break  # последняя страница
    return all_msgs
```

### Polling новых сообщений (только новее last_seen_id)

```python
def get_new_messages(channel, last_seen_id):
    """Вернёт сообщения с id > last_seen_id."""
    r = requests.get(f"https://{HOST}/channel/message",
                     headers=headers, params={"channel": channel, "limit": 50})
    fresh = [m for m in r.json() if m["id"] > last_seen_id]
    return fresh
```

> ⚠️ Polling-стратегия: бери `limit=50` каждый раз и фильтруй по `id`. Пока канал постит < 50 сообщений между опросами — все новые увидишь. На очень активных каналах (>50 постов между опросами) часть может потеряться — увеличивай частоту опроса или бери `limit` побольше с пагинацией.

---

## Типичные проблемы

### `HTTP 401 {"message": "Invalid API key. ..."}` (verified)

Невалидный или отсутствующий `X-RapidAPI-Key`.

### Пустой массив `[]` или 404

- Канал **приватный** или закрыт от публичного просмотра — этот API его не достанет.
- Опечатка в `channel` (без `@` и без `t.me/`).
- Канал заблокирован в стране провайдера.

### Канал — на самом деле бот/группа/чат

`/channel/info` отдаёт `chat_type: "channel"` для каналов. Для других сущностей API может вернуть ошибку или странные данные. **Всегда проверяй `chat_type` перед использованием.**

### `views` это строка, а не число

Поле `views` форматировано как `"5.2K"`/`"1.3M"`. Парси через хелпер выше, не приводи `int(views)` напрямую.

### Битые/устаревшие медиа-URL

`photo`/`video.url`/`image` — это подписанные ссылки на Telegram CDN. Они **протухают**, иногда быстро. Если показываешь медиа в долгоживущем UI — скачай к себе и хости с своего CDN.

### `limit > 50`

Провайдер игнорирует значения больше 50. Для больших выгрузок — итерация через `max_id` (см. пример "Полная выгрузка канала").

### Rate limit 429

На Basic и Ultra — **1 req/sec**. На Mega — 10 req/sec. Если делаешь больше — 429. Решения:
- Throttle (`time.sleep(1.1)` между запросами).
- Перейти на Mega ($25/мес) для нагрузок > 1 req/sec.
- Использовать кэш для одинаковых запросов.

### `200 OK` с пустым ответом

Если API не находит канал, иногда отдаёт `200 OK` + `[]` или `{}` вместо 404. **Проверяй структуру тела перед использованием.**

```python
data = r.json()
if not data or (isinstance(data, list) and not data):
    raise RuntimeError(f"empty response for channel={channel}")
```

---

## Тарифы и расчёт расходов

> 📌 Этот раздел — для AI-ассистента. Когда пользователь спрашивает "сколько это будет стоить?" — используй данные ниже, чтобы посчитать точно.

### Тарифные планы (verified из Pricing tab, 2026-04-28)

| План | Запросов/мес | Rate Limit | Цена/мес | Overage |
|------|--------------|------------|----------|---------|
| **Basic** | 100 | **1 req/sec** | **$0** | **$0.002** за каждый extra-запрос (soft limit!) |
| **Ultra** ⭐ | 500 000 | **1 req/sec** | **$15** | **$0.002** за extra |
| **Mega** | 500 000 | **10 req/sec** | **$25** | **$0.001** за extra |

**Bandwidth (на всех планах):** 10 240 MB/мес включено + **$0.001 за каждый дополнительный 1 MB**.

> ⚠️ **Особенность этого коннектора:** на ВСЕХ планах включая Basic — **soft limit** (overage), а не hard limit. Это значит **если ты не следишь за квотой, тебя автоматически списывают за каждый запрос сверх лимита** ($0.002 на Basic/Ultra, $0.001 на Mega). Можно случайно нажечь $$$. Включай мониторинг квоты в RapidAPI dashboard.

> 🤔 **Mega vs Ultra:** одинаковый месячный лимит (500k), но Mega даёт rate-limit 10 req/sec и дешёвле overage (вдвое). Mega окупается если: (а) нужно делать больше 1 req/sec, или (б) ожидаешь большой overage (>10k extra-запросов в месяц).

### Стоимость одного запроса в квоте

| Что делает запрос | Стоимость | Пример |
|---|---|---|
| **База** (любой GET) | **1 unit** | `GET /channel/info` или `GET /channel/message` |

У этого коннектора **нет** платных модификаторов (`extend`, `local`, `forUsername`, `cm`, `X-CACHEBYPASS` — ничего такого). Каждый запрос всегда стоит ровно 1 unit квоты. Это упрощает расчёт.

### Формула расчёта месячной стоимости

```
month_quota_usage = запросов_в_месяц            # каждый = 1 unit
month_bandwidth_mb = средний_размер_ответа_MB × запросов_в_месяц

# Подбор плана:
if month_quota_usage <= 100 and rate <= 1 req/sec:  plan = Basic ($0) + overage
elif month_quota_usage <= 500_000 and rate <= 1:    plan = Ultra ($15) + overage
elif month_quota_usage <= 500_000 and rate <= 10:   plan = Mega ($25) + overage
else:  plan = Mega + overage за каждый extra ($0.001)

# Overage (если переваливает за лимит плана):
extras = max(0, month_quota_usage - plan_quota)
overage_cost = extras × overage_per_extra($)

# Bandwidth:
extra_mb = max(0, month_bandwidth_mb - 10240)
bandwidth_cost = extra_mb × $0.001

total_monthly = plan_price + overage_cost + bandwidth_cost
```

### Реальные сценарии (сколько это будет стоить)

#### 1. Учебный проект — посмотреть инфу 3 каналов раз в неделю

```
3 канала × 4 раза/мес × 2 эндпоинта = 24 запроса/мес
Bandwidth: ~5 KB на сообщение × 50 × 12 ≈ 3 MB → в лимите
ПЛАН: Basic ($0) — без overage
ИТОГО: $0/мес
```

#### 2. Дашборд из 10 каналов, проверка раз в час

```
10 каналов × 24 ч × 30 дней × 2 эндпоинта = 14 400 req/мес
Rate: 1 req/час (далеко от 1 req/sec)
ПЛАН: Basic ($0), но превышение 14 400 - 100 = 14 300 extras × $0.002 = $28.60
   ИЛИ: Ultra ($15) — 14 400 < 500 000, **в плане**
ИТОГО: $15/мес — Ultra сильно дешевле!
```

⚠️ Важно: на 14k запросов Ultra вдвое дешевле, чем Basic + overage. **Soft-limit Basic коварен.**

#### 3. Мониторинг новых постов 50 каналов, опрос каждые 5 минут

```
50 каналов × (60/5 = 12 раз/час) × 24 × 30 = 432 000 req/мес на /channel/message
Rate: 50 каналов × 12 / 60 мин = 10 req/мин ≈ 1 req за 6 сек → укладываемся в 1 req/sec
ПЛАН: Ultra ($15) — 432 000 < 500 000
Bandwidth: ~10 KB × 432k = 4.3 GB → overage 4.3 - 10.24 = ничего, в лимите (10.24 GB включено)
ИТОГО: $15/мес
```

#### 4. Скрейпинг истории 100 каналов (по 5000 постов в среднем)

```
ЗАПРОСЫ:
  100 каналов × 5000/50 = 10 000 запросов /channel/message
  + 100 запросов /channel/info
  ИТОГО: 10 100 запросов
ПЛАН: Ultra ($15) — помещается
Rate: при 1 req/sec выгрузка займёт 10 100 / 3600 = 2.8 часа

BANDWIDTH:
  500 000 сообщений × ~10 KB = 5 GB → в лимите
ИТОГО: $15/мес (одного месяца хватит на проект)
```

#### 5. Real-time мониторинг 200 каналов с минимальной задержкой

```
Хочется опрашивать каждые 30 секунд:
200 каналов × (60×60/30 = 120 раз/час) × 24 × 30 = 17 280 000 req/мес — слишком много

С rate 10 req/sec (Mega) и батчем по 200 каналов: 200/10 = 20 сек на круг.
Один полный обход = 200 запросов / 10 sec = 20 сек.
1.5 круга в минуту × 60 × 24 × 30 = 65 000 кругов × 200 = 13 000 000 req/мес
Лимит Mega: 500 000. Overage: 12.5M × $0.001 = $12 500/мес 😱

РЕАЛЬНЫЙ ВАРИАНТ: опрос каждые 5 минут (см. сценарий 3) — $15/мес.

Если нужен real-time — этот API не подходит, бери официальный Telegram MTProto.
```

⚠️ Этот сценарий показывает: **на overage можно нажечь сильно больше, чем месячный план**. Mega даёт 10 req/sec, но это не значит что разумно использовать.

#### 6. Bandwidth-heavy: скачивание медиа из канала

```
Этот API не даёт прямого скачивания — только URL медиа. Bandwidth API считает только:
  - размер JSON-ответа (~10 KB на сообщение)
  - сами медиа-файлы качаются с CDN Telegram, не через API → bandwidth НЕ списывается
ИТОГО: bandwidth-overage в этом коннекторе редкость, кроме случаев экстремальной нагрузки.
```

### Чеклист "как сэкономить квоту"

1. **Кэшируй `/channel/info`** на сутки (или больше) — данные канала меняются медленно. Один запрос вместо тысяч.
2. **На polling используй `limit=50` с фильтрацией по `id`**, а не повторные опросы с маленьким limit.
3. **Не переусердствуй с частотой опроса** — 5-10 минут обычно хватает; меньше — значит overage.
4. **Используй Ultra ($15), а не Basic + overage**, если ожидаешь >7 500 запросов/мес. Считай порог: $15 / $0.002 = 7500.
5. **Mega только если** реально нужно >1 req/sec или ожидаешь >10k extras (тогда $0.001 vs $0.002 имеет значение).
6. **Throttle на клиенте** для предотвращения 429 на Basic/Ultra: `time.sleep(1.05)` между запросами.
7. **Не дёргай API из браузера** — медиа-URL и так публичные, скачивание медиа не считается в bandwidth этого коннектора.

---

## Что хорошо подходит для учебных проектов

- Парсинг публичных news-каналов для агрегатора новостей.
- Sentiment-анализ постов через `text` или `html` поля + LLM.
- Сравнение каналов: график `subscribers` за время через регулярный опрос `/channel/info`.
- Извлечение всех ссылок из канала (поле `link.url` в сообщениях) — для тематического дайджеста.
- Анализ медиа-микса канала: какой % постов с фото / видео / только текст.
- Подсчёт engagement через `views` (нормализованный к подписчикам).

## Что не делать

- **Не пытаться достать приватные каналы** — этот API только для публичных.
- **Не использовать для real-time** (минимальный разумный polling — раз в 5 минут).
- **Не приводить `views` к int напрямую** — это строка `"5.2K"`. Используй парсер выше.
- **Не публиковать медиа-URL** долгосрочно — Telegram CDN их инвалидирует.
- **Не игнорировать soft-limit на Basic** — overage считается автоматически и может неприятно удивить в счёте. Включай алерты в RapidAPI dashboard.
- **Не вызывать API из браузера** — ключ утечёт.

## Альтернативы для прод-кода

Если эти 2 эндпоинта мало (нужны: отправка сообщений, приватные каналы, реакции, реалтайм):

- **Telegram Bot API** (https://core.telegram.org/bots/api) — бесплатно, но только если канал добавил бота как админа.
- **Telegram MTProto** (через библиотеки `telethon`, `pyrogram`) — полный доступ, но требует реальный аккаунт и сложнее в эксплуатации.
- Этот RapidAPI-коннектор — компромисс: ничего не настраиваешь, но только публичные каналы и только чтение.
