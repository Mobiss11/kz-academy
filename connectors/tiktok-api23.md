# TikTok API (Lundehund)

**Провайдер:** Lundehund
**Страница:** https://rapidapi.com/Lundehund/api/tiktok-api23
**Subscribe (Pricing):** https://rapidapi.com/Lundehund/api/tiktok-api23/pricing
**Base URL:** `https://tiktok-api23.p.rapidapi.com`
**Host-заголовок:** `tiktok-api23.p.rapidapi.com`

> ⚠️ **Перед первым запросом — оформи подписку** на странице Pricing. Без подписки любой вызов вернёт `403`. Free-план — **Basic** (всего 100 req/мес и 10 download/день!), **требует привязанную карту**. Подробности в [docs/getting-started.md](../docs/getting-started.md).

Полнофункциональный API для парсинга **TikTok**: пользователи, видео, лайвы, музыка, эффекты, плейсы, коллекции, тренды (creator/video/hashtag/song/keyword/ads), магазин и скачивание медиа. **56 эндпоинтов** (все GET) в 12 группах + 1 standalone.

> ✅ **Источник схемы.** Карточка собрана из RapidAPI Playground (path + method + params всех 56 эндпоинтов). Тарифы и формат 401 — verified живым вызовом. JSON-структуры приведены для ключевых эндпоинтов; остальные группы имеют единый паттерн ответа.
>
> Размер этого API в 4-5 раз больше typical RapidAPI коннектора. **Перед прод-кодом сверяйся с playground** — провайдер часто меняет имена полей.

## Авторизация

```
X-RapidAPI-Key: <ключ>
X-RapidAPI-Host: tiktok-api23.p.rapidapi.com
```

**Формат ошибки 401** (verified):

```http
HTTP/1.1 401 Unauthorized
{"message": "Invalid API key. Go to https://docs.rapidapi.com/docs/keys for more info."}
```

## Общие правила

### Идентификаторы пользователя

TikTok использует **3 разных ID** для одного юзера, и эндпоинты принимают разные:

- **`uniqueId`** — handle/username без `@` (`charlidamelio`, `mrbeast`). Принимают `/api/user/info`, `/api/user/info-with-region`, `/api/live/check-alive`.
- **`userId`** — числовая строка (стабильный internal ID). Принимают `/api/user/info-by-id`, `/api/user/followers`, `/api/user/followings`, `/api/user/story`.
- **`secUid`** — длинная подписанная строка `MS4wLjABAAAA...`. Принимают `/api/user/posts`, `/api/user/liked-posts`, `/api/user/playlist`, `/api/user/repost`, `/api/user/info-by-id` (как альтернатива userId), `/api/download/user/video`.

**Все три значения** есть в ответе `/api/user/info` (по `uniqueId`). Стандартный flow:

```
uniqueId → /api/user/info → {userId, secUid, ...} → дальнейшие вызовы
```

Закэшируй маппинг — он не меняется.

### Пагинация (3 разных стиля!)

Этот API использует **разные курсоры** в разных группах:

| Эндпоинты | Курсор | Заметка |
|---|---|---|
| `/api/user/posts`, `/liked-posts`, `/playlist`, `/repost`, `/post/comments`, `/post/related`, `/challenge/posts`, `/music/posts`, `/place/posts`, `/effect/posts`, `/collection/posts` | `cursor` (number, default 0) | стандарт; берёшь из ответа `cursor` |
| `/api/user/followers`, `/api/user/followings` | `max_time` (number, default 0) | timestamp последнего показанного, передаёшь обратно |
| `/api/user/story` | `maxCursor` | специальный |
| `/api/download/user/video` | `minCursor` / `maxCursor` | оба, для диапазона |
| `/api/search/general`, `/search/video`, `/search/account`, `/search/live` | `cursor` + `search_id` | search_id связывает страницы одного поиска |
| `/api/post/discover`, `/api/trending/*`, `/api/music/unlimited-sounds` | `page` (number) | пагинация по номеру страницы |
| `/api/post/explore`, `/api/post/trending` | `count` only | без пагинации (берёшь N единиц за один заход) |
| `/api/live/category` | (none) | без пагинации |

В response эти поля называются так же: `cursor`, `max_time`, `maxCursor`, `search_id`. Если не получил — страниц больше нет (или получил `hasMore: false`).

### Внутренний формат ответов

TikTok использует свой нативный формат — реально это парсинг web-API TikTok. Видео-объекты следуют схеме `Aweme` (внутреннее имя у TikTok):

```json
{
  "id": "...",
  "desc": "caption text",
  "createTime": 1700000000,
  "video": {
    "id": "...",
    "duration": 15,
    "playAddr": "...",
    "downloadAddr": "...",
    "cover": "..."
  },
  "author": {
    "uniqueId": "...",
    "id": "<userId>",
    "secUid": "...",
    "nickname": "...",
    "verified": false
  },
  "music": {"id": "...", "title": "...", "authorName": "..."},
  "stats": {
    "diggCount": 0, "shareCount": 0, "commentCount": 0,
    "playCount": 0, "collectCount": 0
  },
  "challenges": [{"id": "...", "title": "..."}]
}
```

> ⚠️ TikTok возвращает счётчики (`diggCount`, `playCount` etc.) как **числа** (не строки `"5.2K"`). Это удобнее, чем у Telegram-channel.

### Особенности

- **`diggCount` = likes** (TikTok внутренне зовёт лайки "digg").
- **`uniqueId` ≠ nickname**: `uniqueId` это URL-handle (стабильный, латиница), `nickname` — отображаемое имя (любой язык, может меняться).
- **`secUid` зависит от `userId`** один-к-одному. Закэшируй маппинг.

---

## Эндпоинты (56)

> 📋 Условные обозначения: ✅ = required, `–` = optional. Смысл групп ниже + полный список путей и параметров.

### Standalone (1)

| Эндпоинт | Path | Параметры | Описание |
|---|---|---|---|
| Get Product Info | `/api/shop/product` | ✅ `productId` | данные товара из TikTok Shop |

### User (10)

| Эндпоинт | Path | Параметры |
|---|---|---|
| Get User Info | `/api/user/info` | ✅ `uniqueId` |
| Get User Info (with region) | `/api/user/info-with-region` | ✅ `uniqueId` |
| Get User Info by ID | `/api/user/info-by-id` | – `userId`, – `secUid` (нужен ровно один) |
| Get User Followers | `/api/user/followers` | – `secUid`/`userId` (один из), – `count` (default 30, max 30), – `max_time` (default 0) |
| Get User Followings | `/api/user/followings` | те же |
| Get User Posts | `/api/user/posts` | ✅ `secUid`, – `count` (default 30, max 30), – `cursor` (default 0) |
| Get User Liked Posts | `/api/user/liked-posts` | ✅ `secUid`, – `count`, – `cursor` |
| Get User Playlist | `/api/user/playlist` | ✅ `secUid`, – `count`, – `cursor` |
| Get User Repost | `/api/user/repost` | ✅ `secUid`, – `count`, – `cursor` |
| Get User Story | `/api/user/story` | ✅ `userId`, – `maxCursor` |

**Пример ответа `/api/user/info`** (структура):

```json
{
  "userInfo": {
    "user": {
      "id": "...",
      "uniqueId": "charlidamelio",
      "secUid": "MS4wLjABAAAA...",
      "nickname": "charli d'amelio",
      "avatarThumb": "https://...",
      "avatarMedium": "https://...",
      "avatarLarger": "https://...",
      "signature": "...",
      "verified": true,
      "privateAccount": false,
      "openFavorite": false,
      "secret": false,
      "ftc": false,
      "relation": 0,
      "isADVirtual": false,
      "createTime": 1539138400
    },
    "stats": {
      "followerCount": 155000000,
      "followingCount": 1234,
      "heartCount": 11500000000,
      "videoCount": 2400,
      "diggCount": 0,
      "heart": 11500000000
    }
  }
}
```

`/api/user/info-with-region` дополнительно отдаёт `region`, `language`, `ttSeller`. `/api/user/info-by-id` принимает userId/secUid и возвращает аналогично.

### Search (5)

| Эндпоинт | Path | Параметры |
|---|---|---|
| Search General (Top) | `/api/search/general` | ✅ `keyword`, – `cursor`, – `search_id` |
| Search Video | `/api/search/video` | те же |
| Search Account | `/api/search/account` | те же |
| Search Live | `/api/search/live` | те же |
| Others Searched For | `/api/search/others-searched-for` | ✅ `keyword` (без пагинации) |

**Пагинация поиска:** в первом запросе передавай только `keyword`. Из ответа возьми `cursor` и `search_id`, передай оба в следующий — search_id связывает страницы одной поисковой сессии.

### Post / Video (7)

| Эндпоинт | Path | Параметры |
|---|---|---|
| Get Post Detail | `/api/post/detail` | ✅ `videoId` |
| Get Comments of Post | `/api/post/comments` | ✅ `videoId`, – `count`, – `cursor` |
| Get Replies Comment of Post | `/api/post/comment/replies` | ✅ `videoId`, ✅ `commentId`, – `count`, – `cursor` |
| Get Related Posts | `/api/post/related` | ✅ `videoId`, – `count`, – `cursor` |
| Get Trending Posts | `/api/post/trending` | – `count` |
| Get Explore Posts | `/api/post/explore` | ✅ `categoryType`, – `count` |
| Discover Posts by Keyword | `/api/post/discover` | ✅ `keyword`, – `page` |

`/api/post/comments` — для **ответов на комментарий** используй `/api/post/comment/replies` с `commentId` родительского комментария.

### Ads & Trending (15) ⭐

> ⚠️ **На странице тарифов отмечено: "Ads and Trending Endpoint — Request Custom".** Это значит для активного использования endpoints этой группы провайдер может попросить переход на custom-план. Уточни в RapidAPI Discussions.

| Эндпоинт | Path | Ключевые параметры |
|---|---|---|
| Get Ads Detail | `/api/trending/ads/detail` | ✅ `ads_id` |
| Get Top Ads | `/api/trending/ads` | – `page`, `period`, `limit`, `country`, `order_by`, `like`, `ad_format`, `objective`, `industry`, `ad_language`, `keyword` |
| Get Trending Creator | `/api/trending/creator` | – `page`, `limit`, `sort_by`, `country`, `audience_count`, `audience_country` |
| Get Trending Video | `/api/trending/video` | – `page`, `limit`, `period`, `order_by`, `country` |
| Get Trending Hashtag | `/api/trending/hashtag` | – `page`, `limit`, `period`, `country`, `sort_by`, `filter_by`, `industry_id` |
| Get Trending Song | `/api/trending/song` | – `page`, `limit`, `period`, `rank_type`, `country`, `new_on_board`, `commercial_music` |
| Get Trending Keyword | `/api/trending/keyword` | – `page`, `limit`, `period`, `country`, `order_by`, `order_type`, `industry`, `objective`, `keyword_type` |
| Get Trending Video By Keyword | `/api/trending/keyword/posts` | ✅ `keyword`, – `country`, `limit`, `period` |
| Get Keyword Sentence | `/api/trending/keyword/sentence` | – `query` |
| Get Commercial Music Playlist Detail | `/api/trending/commercial-music-library/playlist/detail` | ✅ `playlist_id`, – `page`, `limit`, `region` |
| Get Commercial Music Playlist | `/api/trending/commercial-music-library/playlist` | – `limit`, `region` |
| Get Commercial Music Library | `/api/trending/commercial-music-library` | – `page`, `limit`, `region`, `scenarios`, `duration`, `placements`, `themes`, `genres`, `moods`, `music_name`, `singer_name` |
| Get Top Products | `/api/trending/top-products` | – много фильтров |
| Get Top Product Detail | `/api/trending/top-products/detail` | ✅ `product_id` |
| Get Top Product Metrics | `/api/trending/top-products/metrics` | ✅ `product_id` |

Все эти endpoints — это TikTok's **Creative Center** (бизнес-инсайты для маркетологов): тренды по странам, периодам, индустриям. Используй для анализа рынка/конкурентов.

### Download (3) — **отдельная квота!**

| Эндпоинт | Path | Параметры |
|---|---|---|
| Download Video | `/api/download/video` | ✅ `url` |
| Download Music | `/api/download/music` | ✅ `url` |
| Download All User Videos | `/api/download/user/video` | ✅ `secUid`, – `minCursor`, – `maxCursor` |

> ⚠️ **Download endpoints имеют отдельную дневную квоту**, не общую месячную. На Basic — 10/день, на Pro — 500/день, на Ultra — 1000/день, на Mega — 5000/день. См. раздел "Тарифы" ниже.

### Live (4)

| Эндпоинт | Path | Параметры |
|---|---|---|
| Get Live Info | `/api/live/info` | ✅ `roomId` |
| Get Live Stream | `/api/live/stream` | ✅ `related_live_tag`, – `load_more`, – `true` |
| Get Live Category | `/api/live/category` | (без параметров) |
| Check Alive | `/api/live/check-alive` | ✅ `uniqueId` — проверить, идёт ли стрим у юзера |

### Challenge (Hashtag) (2)

| Эндпоинт | Path | Параметры |
|---|---|---|
| Get Challenge Info | `/api/challenge/info` | ✅ `challengeName` (без `#`) |
| Get Challenge Posts | `/api/challenge/posts` | ✅ `challengeId` (из info), – `count`, – `cursor` |

### Music (3)

| Эндпоинт | Path | Параметры |
|---|---|---|
| Get Music Info | `/api/music/info` | ✅ `musicId` |
| Get Music Posts | `/api/music/posts` | ✅ `musicId`, – `count`, – `cursor` |
| Get Unlimited Sounds | `/api/music/unlimited-sounds` | – `page`, `pageSize`, `orderBy` |

### Place (2)

| Эндпоинт | Path | Параметры |
|---|---|---|
| Get Place Info | `/api/place/info` | ✅ `placeId` |
| Get Place Posts | `/api/place/posts` | ✅ `placeId`, – `count`, – `cursor` |

### Effect (2)

| Эндпоинт | Path | Параметры |
|---|---|---|
| Get Effect Info | `/api/effect/info` | ✅ `effectId` |
| Get Effect Posts | `/api/effect/posts` | ✅ `effectId`, – `count`, – `cursor` |

### Collection (2)

| Эндпоинт | Path | Параметры |
|---|---|---|
| Get Collection Info | `/api/collection/info` | ✅ `collectionId` |
| Get Collection Posts | `/api/collection/posts` | ✅ `collectionId`, – `count`, – `cursor` |

> 💡 Все `*/posts` эндпоинты (challenge, music, place, effect, collection) возвращают **массив видео в формате Aweme** (см. секцию "Внутренний формат ответов") с курсорной пагинацией.

---

## Минимальные рабочие примеры

### uniqueId → secUid → последние видео

```python
import os, requests

API_KEY = os.environ["RAPIDAPI_KEY"]
HOST = "tiktok-api23.p.rapidapi.com"
headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": HOST}

# 1. Получить secUid по handle
info = requests.get(f"https://{HOST}/api/user/info",
                    headers=headers, params={"uniqueId": "charlidamelio"}).json()
user = info["userInfo"]["user"]
sec_uid = user["secUid"]
print(f"{user['nickname']} ({info['userInfo']['stats']['followerCount']:,} followers)")

# 2. Видео автора
posts = requests.get(f"https://{HOST}/api/user/posts",
                     headers=headers,
                     params={"secUid": sec_uid, "count": 30, "cursor": 0}).json()
for v in posts.get("data", {}).get("itemList", []):
    print(f"#{v['id']} {v['stats']['playCount']:,} plays — {v['desc'][:80]}")
```

### Пагинация через cursor

```python
def paginate_posts(sec_uid, max_pages=10):
    cursor = 0
    for _ in range(max_pages):
        r = requests.get(f"https://{HOST}/api/user/posts",
                         headers=headers,
                         params={"secUid": sec_uid, "count": 30, "cursor": cursor},
                         timeout=15).json()
        items = r.get("data", {}).get("itemList") or r.get("itemList", [])
        for v in items:
            yield v
        cursor = r.get("data", {}).get("cursor") or r.get("cursor")
        has_more = r.get("data", {}).get("hasMore", False) or r.get("hasMore", False)
        if not has_more or not cursor:
            break
```

### Поиск видео с пагинацией (search_id)

```python
def search_videos(keyword, max_pages=5):
    cursor = "0"
    search_id = None
    for _ in range(max_pages):
        params = {"keyword": keyword, "cursor": cursor}
        if search_id:
            params["search_id"] = search_id
        r = requests.get(f"https://{HOST}/api/search/video",
                         headers=headers, params=params).json()
        for item in r.get("data", []):
            yield item
        cursor = r.get("cursor")
        search_id = r.get("search_id")  # привязка пагинации к одной search-сессии
        if not cursor:
            break
```

### Скачать прямую ссылку на mp4

```python
url = "https://www.tiktok.com/@user/video/123456789"

dl = requests.get(f"https://{HOST}/api/download/video",
                  headers=headers, params={"url": url}, timeout=20).json()
# Структура зависит от версии — обычно есть "video": {"playAddr": "...", "downloadAddr": "..."}
print(dl)
```

⚠️ Это **расходует Download-квоту** (отдельный счётчик от месячного, по дням), не основную.

### Анализ конкурента: топ-50 видео по просмотрам

```python
sec_uid = "MS4wLjABAAAA..."  # из /api/user/info
videos = list(paginate_posts(sec_uid, max_pages=2))  # ~60 видео
top = sorted(videos, key=lambda v: v["stats"]["playCount"], reverse=True)[:50]
for v in top:
    print(f"{v['stats']['playCount']:>15,} | {v['desc'][:80]}")
```

### Проверка идёт ли стрим у юзера

```python
alive = requests.get(f"https://{HOST}/api/live/check-alive",
                     headers=headers, params={"uniqueId": "user"}).json()
if alive.get("data", {}).get("alive"):
    room_id = alive["data"]["roomId"]
    info = requests.get(f"https://{HOST}/api/live/info",
                        headers=headers, params={"roomId": room_id}).json()
    print(info)
```

---

## Типичные проблемы

### `HTTP 401 {"message": "Invalid API key. ..."}` (verified)

Невалидный или отсутствующий `X-RapidAPI-Key`.

### Пустой `itemList` или `data: []`

- Юзер приватный (`privateAccount: true` в user info).
- Юзер забанен.
- Неправильный `secUid` (он привязан к версии user info — иногда выпадают новые).

### "secUid не работает" — рассинхрон

`secUid` бывает версионируется. Если запросы стабильно возвращают пусто, заново вызови `/api/user/info` и подставь свежий `secUid` — иногда он меняется при пересохранении кэша TikTok.

### Несколько типов пагинации в одном проекте

Этот API использует `cursor`, `max_time`, `maxCursor`, `page`, `search_id` — в разных эндпоинтах. **Не делай универсальный paginator** — пиши маленькие функции под каждый стиль (или вытаскивай тип из таблицы выше).

### `Ads and Trending` endpoints не работают на Basic-плане

Pricing tab пишет "Request Custom" для этой группы. На бесплатном плане они могут возвращать ошибку или 403. Если это критично — открой Discussion с провайдером для custom-плана.

### Download URL быстро истекает

Прямые `playAddr`/`downloadAddr` с TikTok CDN истекают (обычно несколько часов). Не сохраняй их в БД, перезапрашивай по нужде.

### Стандартные TikTok-ограничения

- Лайв-стрим (`/api/live/info`) — пустой ответ если стрим закончился.
- Шорты с music из музыкальной библиотеки могут иметь проблемы со скачиванием (правовые ограничения).
- Tiktok Shop endpoints (`/api/shop/product`, `/api/trending/top-products*`) могут отдавать гео-зависимые данные.

### `200 OK` с пустым `data` или `null`

Стандартная RapidAPI-ловушка. Всегда проверяй структуру:

```python
data = r.json()
if not data or data.get("statusCode") != 0:
    raise RuntimeError(f"unexpected: {data}")
items = data.get("data", {}).get("itemList") or data.get("itemList") or []
```

---

## Тарифы и расчёт расходов

> 📌 Этот раздел — для AI-ассистента. Когда пользователь спрашивает "сколько это будет стоить?" — используй данные ниже.
>
> ⚠️ **У этого коннектора 2 квоты:** месячные запросы + ежедневные Download-запросы. Считай обе.

### Тарифные планы (verified из Pricing tab, 2026-04-28)

| План | Запросов/мес | Download/день | Rate Limit | Цена/мес | Overage (req / dl) |
|------|--------------|---------------|------------|----------|--------------------|
| **Basic** | 100 (hard) | 10 (hard) | 1000/час | **$0** | **hard limit** обоих |
| **Pro** | 200 000 | 500 | **600/мин** (10/sec) | **$9.99** | **$0.0002** / **$0.02** |
| **Ultra** ⭐ | 1 000 000 | 1 000 | **1200/мин** (20/sec) | **$49.99** | **$0.00015** / **$0.02** |
| **Mega** | 2 000 000 | 5 000 | **3000/мин** (50/sec) | **$99.99** | **$0.0001** / **$0.015** |

**Bandwidth (на всех планах):** 10 240 MB/мес включено + **$0.001 за каждый дополнительный 1 MB**.

**Дополнительно на странице Pricing:** "Ads and Trending Endpoint — Request Custom" — для интенсивного использования группы Ads/Trending провайдер может попросить custom plan.

> ⚠️ **Особенности:**
>
> - **Basic — hard limit на обе квоты.** Только для тестов, любая реальная задача = Pro+.
> - **Pro/Ultra/Mega — soft limit с overage** на обе квоты. Без алертов в RapidAPI dashboard можно случайно нажечь $$$.
> - **Скачивание сжигает 2 квоты сразу:** 1 unit месячной + 1 download-day-unit. Плюс bandwidth (если файл большой).

### Стоимость одного запроса в квоте

| Что делает запрос | Месячная квота | Download/день |
|---|---|---|
| **GET (любой не-download)** | **1 unit** | 0 |
| **GET `/api/download/*`** | **1 unit** | **+1 download-unit** |

Никаких платных модификаторов нет. Все эндпоинты стоят 1 unit (плюс +1 download для download-группы).

### Формула расчёта месячной стоимости

```
month_quota_usage = запросов_в_месяц            # 1 unit per request
month_dl_usage    = download_запросов_в_месяц   # учитываются и в month_quota и в day_dl
day_dl_usage      = download_запросов_в_день

# Подбор плана: должны вместиться ОБЕ квоты
if month_quota_usage <= 100 and day_dl_usage <= 10:                plan = Basic ($0)
elif month_quota_usage <= 200_000 and day_dl_usage <= 500:         plan = Pro ($9.99)
elif month_quota_usage <= 1_000_000 and day_dl_usage <= 1_000:     plan = Ultra ($49.99)
elif month_quota_usage <= 2_000_000 and day_dl_usage <= 5_000:     plan = Mega ($99.99)
else: plan = Mega + overage

# Overage (если переваливает за лимит плана):
extras_req = max(0, month_quota_usage - plan.req_quota)
extras_dl  = max(0, month_dl_usage * 30 - plan.dl_quota * 30)  # дневной → пересчёт в месяц
overage_req_cost = extras_req × overage_per_req
overage_dl_cost  = extras_dl × overage_per_dl

# Bandwidth:
extra_mb = max(0, MB_in_responses - 10240)
bandwidth_cost = extra_mb × $0.001

total_monthly = plan_price + overage_req_cost + overage_dl_cost + bandwidth_cost
```

### Реальные сценарии (сколько это будет стоить)

#### 1. Учебный — посмотреть инфо 5 авторов разово

```
5 × (/api/user/info + /api/user/posts) = 10 запросов разово
ПЛАН: Basic ($0). 10 < 100 в месяц.
ИТОГО: $0
```

#### 2. Дашборд из 50 авторов с обновлением раз в час

```
50 × 24 × 30 × 1 (только /api/user/info) = 36 000 req/мес
Rate: 50/час = 0.014 req/sec — далеко от любого лимита
ПЛАН: Pro ($9.99) — 36k < 200k
ИТОГО: $9.99/мес
```

#### 3. Мониторинг новых видео 200 авторов каждые 30 минут

```
200 × 48 × 30 = 288 000 req/мес на /user/posts
Rate: 200 за полминуты = 6.7 req/sec → влезает в Pro (10/sec)
ПЛАН: Pro ($9.99) с overage: 88k × $0.0002 = $17.60
   ИЛИ: Ultra ($49.99) — 288k < 1M, без overage
   → Pro+overage = $27.59 vs Ultra = $49.99. Pro дешевле!
ИТОГО: $27.59/мес
```

⚠️ Точка перехода Pro→Ultra: `($49.99 - $9.99) / $0.0002 = 200 000 extras` → выгоднее Pro+overage до 400k req/мес.

#### 4. Скрейпинг истории 1000 авторов (по 100 видео в среднем)

```
1000 × (1 /info + 100/30 ≈ 4 страницы /posts) = 5000 запросов разово
ПЛАН: Pro ($9.99) — 5k < 200k. Можно делать ~40 такого в месяц.
ИТОГО: $9.99 (хватит надолго)
```

#### 5. Скачивание 100 видео в день для контент-агрегатора

```
DL: 100 × 30 = 3 000 download-запросов/мес
Day DL: 100 → нужен план где ≥100/день
Месячная квота: 3 000 (плюс другие вызовы) — Pro вмещает

ПЛАН: Pro ($9.99) — но день-DL лимит 500/день, помещается.
Однако `playAddr` ссылка истекает; чтобы скачать — это ещё bandwidth:
  100 × 30 × 5 MB ≈ 15 GB → overage 5 GB × $0.001 = $5
ИТОГО: $9.99 + $5 = ~$15/мес
```

⚠️ **Скачивание = 2 квоты + bandwidth.** Главный риск — bandwidth-overage когда файлы большие.

#### 6. Real-time мониторинг трендов: трекинг top-100 каждые 5 минут

```
100 × 12 × 24 × 30 = 864 000 req/мес на /api/trending/video
Rate: 100/5min = 0.33 req/sec — норм для всех планов

ПЛАН: Ultra ($49.99) — 864k < 1M, помещается.
   ИЛИ: Pro ($9.99) с overage: 664k × $0.0002 = $132.80
   → Ultra сильно выгоднее: $49.99 vs $142.79

ИТОГО: $49.99/мес — но осторожно: "Ads and Trending" может потребовать custom plan.
```

#### 7. Скачать всю историю популярного автора (5000 видео)

```
DL: 5000 download-запросов разово
Day DL: 5000/день нужно — это лимит **Mega-плана** (5000/день)
Месячная: 5000 + ~50 на навигацию = 5050 req — любой план OK

ПЛАН: Mega ($99.99) — единственный, где 5000/день.
   ИЛИ: Ultra ($49.99) с rate 1000/день → потребуется 5 дней. Дешевле.

BANDWIDTH: 5000 × ~5 MB = 25 GB → overage 15 GB × $0.001 = $15
ИТОГО (вариант Ultra за 5 дней): $49.99 + $15 = $64.99
ИТОГО (вариант Mega за 1 день):  $99.99 + $15 = $114.99
```

⚠️ Если не торопишься — Ultra с распределением по дням сильно дешевле.

### Чеклист "как сэкономить квоту"

1. **Кэшируй `/api/user/info` маппинг (uniqueId → userId/secUid) навсегда** — он не меняется. Один раз вызвал, потом везде по `secUid`.
2. **Кэшируй детерминированные данные** (пост, музыка, плейс, эффект, коллекция, челлендж info) — обычно стабильны на сутки+.
3. **На polling используй `count=30`** (макс) с фильтрацией по `id`/`createTime` на клиенте, чтобы реже опрашивать.
4. **Не используй Mega** если не нужно реально >1000 download/день. Ultra с распределением скачиваний по дням обычно дешевле.
5. **На Basic ничего серьёзного делать нельзя** (100 req/мес и 10 dl/день — кончатся за час).
6. **Запросы Ads/Trending** — если их много, лучше сразу Discussion с провайдером для custom-плана. Не пытайся обмануть лимит.
7. **Throttle на клиенте** под `rate_limit / N`. На Pro: 600/мин = 10/сек, дай sleep ~110ms.
8. **Bandwidth-overage** — главный нечаянный расход при скачивании. Считай заранее: видеоTikTok ≈ 2-10 MB.
9. **Точка перехода Pro→Ultra ≈ 400k req/мес** при overage $0.0002. Считай каждый раз.
10. **Точка перехода Ultra→Mega ≈ 333k extras** (`($99.99-$49.99)/$0.00015`). Mega только если регулярно 1.3M+ req/мес.

---

## Что хорошо подходит для учебных проектов

- Анализ автора: `/user/info` + полный список видео + сортировка по `playCount` — рейтинг лучших.
- Sentiment-анализ комментариев одного популярного видео через `/post/comments`.
- Изучение эффекта (виральности конкретного `effectId`) — все видео с эффектом через `/effect/posts`.
- Тренды по странам и периодам через Ads & Trending группу — данные Creative Center.
- Поиск всех видео под музыкой через `/music/posts`.
- Сравнение `followerCount` и `heartCount` для группы авторов.
- Извлечение хэштегов из `desc` поля видео + анализ через `/challenge/info`.

## Что не делать

- **Не использовать Basic для прода** — 100 req/мес и 10 dl/день кончатся мгновенно.
- **Не игнорировать Ads/Trending custom plan warning** — провайдер может бить по квоте/блокировать.
- **Не качать видео массово** через `/api/download/*` — нарушает ToS TikTok, провайдер забанит.
- **Не публиковать `playAddr`/`downloadAddr`** — они подписаны и быстро протухают.
- **Не вызывать API из браузера** — ключ утечёт.
- **Не путать `userId` (числовая строка) и `secUid` (длинная подпись)** — endpoint'ы принимают разные. См. таблицу выше.
- **Не делать универсальный paginator** — пагинация разная (cursor / max_time / page / maxCursor / search_id). Под каждый стиль свой код.

## Альтернативы

- **Официальный TikTok Research API** (https://developers.tiktok.com/products/research-api) — бесплатно для исследователей, но требует одобрения от TikTok.
- **TikTok Display API** — для приложений с OAuth-авторизацией, ограничен данными авторизованного юзера.
- Этот RapidAPI-коннектор — компромисс: ничего не настраиваешь, работает сразу с публичными данными, но не подходит для очень больших объёмов и требует custom-plan для Ads/Trending.
