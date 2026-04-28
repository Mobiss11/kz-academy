# Threads API (Lundehund)

**Провайдер:** Lundehund
**Страница:** https://rapidapi.com/Lundehund/api/threads-api4
**Subscribe (Pricing):** https://rapidapi.com/Lundehund/api/threads-api4/pricing
**Base URL:** `https://threads-api4.p.rapidapi.com`
**Host-заголовок:** `threads-api4.p.rapidapi.com`

> ⚠️ **Перед первым запросом — оформи подписку** на странице Pricing. Без подписки любой вызов вернёт `403`. Free-план — **Basic** (50 req/мес!), оформляется в один клик, **требует привязанную карту**. Подробности в [docs/getting-started.md](../docs/getting-started.md).

API для парсинга **Threads** (Meta) — публичные профили, посты, комментарии, репосты и поиск. **12 эндпоинтов** (все GET), сгруппированы в 3 секции: User (5), Post (4), Search (3).

> ✅ **Источник схемы.** Карточка собрана из RapidAPI Playground (params + Example Responses всех 12 эндпоинтов). Тарифы и формат 401 — verified живым вызовом. Имена полей JSON — реальные, из ответов провайдера.
>
> Threads — продукт Meta, схемы ответов отражают внутреннее GraphQL API Threads (поля типа `edges/node`, `__typename`, `pk` для primary key). Это сырой Instagram-style формат.
>
> Данные могут устареть — провайдер обновляет схемы. Перед прод-кодом сверяйся с playground.

## Авторизация

Стандартная пара заголовков RapidAPI (см. [SKILL.md](../SKILL.md)):

```
X-RapidAPI-Key: <ключ>
X-RapidAPI-Host: threads-api4.p.rapidapi.com
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
| `X-RapidAPI-Host` | ✅ | `threads-api4.p.rapidapi.com` |

Этот коннектор не имеет специфичных заголовков (`X-TOKEN`, `X-CACHEBYPASS` и т.п.) — только два стандартных.

## Общие правила

### Структура ответов

- Все ответы — `{"data": {...}}`. Реальный контент — внутри `data`.
- **Пагинация — через `end_cursor`** (не `token`/`continuation`!). Имя параметра query — `end_cursor`. Имя поля в ответе для следующей страницы — `end_cursor` или внутри `page_info.end_cursor`. Если не получили — страниц больше нет.
- Списки используют **GraphQL-style обёртки**: `{edges: [{node: {...}}]}`. Реальные элементы вложены в `node` (а у постов — ещё глубже, в `thread_items[].post`).
- ID пользователя называется `pk` (primary key, числовая строка) или `id`. ID поста тоже `pk`. **Threads используют тот же ID-формат, что Instagram.**
- **Username** — с `@` без префикса (`reuters`, не `@reuters`).
- Поле `__typename` на узлах указывает GraphQL-тип (`XDTThreadItem`, `XDTUserDict`, и т.п.).

### Пагинация (универсальный паттерн)

```python
def paginate(path, params, max_pages=10):
    end_cursor = None
    for _ in range(max_pages):
        if end_cursor:
            params = {**params, "end_cursor": end_cursor}
        r = requests.get(f"https://{HOST}{path}", headers=headers, params=params, timeout=15)
        r.raise_for_status()
        page = r.json()
        # путь к edges зависит от эндпоинта (см. ниже в каждом)
        yield page
        # ищем end_cursor в любом из стандартных мест
        end_cursor = (
            page.get("data", {}).get("end_cursor")
            or page.get("data", {}).get("page_info", {}).get("end_cursor")
        )
        if not end_cursor:
            break
```

### Threads-специфика

- **Threads нет понятия "private channel"** в традиционном смысле — у пользователя есть флаг `text_post_app_is_private`. У приватного юзера API может вернуть `friendship_status` без постов.
- **Verified-галочка**: `is_verified` (bool).
- **Counts** (`follower_count`, `like_count` и т.п.) — это **числа**, не строки `"5.2K"` (в отличие от telegram-channel API).
- **Время** — `taken_at` (Unix timestamp) или ISO string в зависимости от поля.

---

## User (5 эндпоинтов)

### `GET /api/user/info` — данные пользователя по `username`

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `username` | string | ✅ | username без `@` (`reuters`, `zuck`) |

**Пример ответа** (verified — 14 keys в `data.user`):

```json
{
  "data": {
    "user": {
      "pk": "1234567890",
      "username": "reuters",
      "full_name": "Reuters",
      "biography": "...",
      "text_app_biography": {
        "text_fragments": {
          "fragments": [
            {"fragment_type": "text", "plaintext": "...", "link_fragment": null,
             "mention_fragment": null, "tag_fragment": null, "linkified_web_url": null}
          ]
        }
      },
      "follower_count": 1083901,
      "profile_pic_url": "https://...",
      "hd_profile_pic_versions": [
        {"height": 320, "url": "...", "width": 320},
        {"height": 640, "url": "...", "width": 640}
      ],
      "is_verified": true,
      "text_post_app_is_private": false,
      "friendship_status": {
        "followed_by": false,
        "following": false,
        "outgoing_request": false
      },
      "profile_context_facepile_users": null,
      "text_post_app_has_fediverse_enabled": null
    }
  }
}
```

> ⚠️ **`pk` — это ID пользователя.** Используй его в дальнейших вызовах `/api/user/posts`, `/api/user/reposts`, `/api/user/replies` (которые принимают `user_id`).

### `GET /api/user/info` (by user ID) — данные по `id`

Тот же путь, **другой параметр**:

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `id` | string | ✅ | user pk (например `1234567890`) |

**Пример ответа** (verified — 20 keys в `data.user`, **больше полей** чем при поиске по username):

```json
{
  "data": {
    "user": {
      "pk": "...",
      "username": "...",
      "profile_pic_url": "...",
      "hd_profile_pic_versions": [...],
      "friendship_status": {
        "followed_by": false,
        "following": false,
        "outgoing_request": false,
        "blocking": false,
        "incoming_request": false
      },
      "text_post_app_is_private": false,
      "is_verified": true,
      "follower_count": "...",
      "biography": "...",
      "full_name": "..."
    }
  }
}
```

> Этот вариант возвращает дополнительные поля (`blocking`, `incoming_request` в friendship_status и т.п.). Используй когда нужны полные данные.

### `GET /api/user/posts` — посты пользователя

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `user_id` | string | ✅ | user pk (из `/api/user/info`) |
| `end_cursor` | string | – | пагинация |

**Пример ответа** (verified):

```json
{
  "data": {
    "mediaData": {
      "edges": [
        {
          "node": {
            "thread_header_context": null,
            "thread_items": [
              {
                "post": {
                  "pk": "...",
                  "user": {
                    "pk": "...",
                    "username": "...",
                    "profile_pic_url": "...",
                    "is_verified": true,
                    "friendship_status": {"muting": false, "following": false, "followed_by": false},
                    "text_post_app_info": { /* 15 keys */ },
                    "transparency_label": null,
                    "transparency_product": null,
                    "transparency_product_enabled": false,
                    "eligible_for_text_app_activation_badge": false
                  },
                  "is_post_unavailable": false,
                  "pinned_post_info": {
                    "is_pinned_to_profile": false,
                    "is_pinned_to_parent_post": false
                  }
                  /* ещё ~25 полей: text, taken_at, like_count, ... */
                }
              }
            ]
          }
        }
      ],
      "page_info": { "end_cursor": "...", "has_next_page": true }
    }
  }
}
```

Путь к данным: `data.mediaData.edges[].node.thread_items[].post`

### `GET /api/user/reposts` — репосты пользователя

Параметры идентичны `/api/user/posts`. Структура ответа похожа, но в `node` присутствует `thread_header_context` с метаданными репоста:

```json
{
  "thread_header_context": {
    "context_type": "REPOST",
    "text": "..."
  },
  "thread_items": [{ "post": { /* оригинальный пост */ } }]
}
```

Используй `thread_header_context` чтобы отличить репост от собственного поста.

### `GET /api/user/replies` — ответы пользователя

Параметры идентичны. Главное отличие от `/api/user/posts`: `thread_items` содержит **2 элемента** — `[родительский_пост, ответ_пользователя]`. То есть ты получаешь контекст беседы.

```json
{
  "node": {
    "thread_items": [
      { "post": { /* пост, на который отвечают */ } },
      { "post": { /* собственно ответ */ } }
    ]
  }
}
```

---

## Post (4 эндпоинта)

### `GET /api/post/get-id` — конвертер URL → post_id

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `url` | string | ✅ | полный URL поста (`https://www.threads.net/@user/post/abc...`) |

**Пример ответа** (verified — простая структура):

```json
{
  "data": {
    "url": "https://www.threads.net/@reuters/post/...",
    "route": "...",
    "post_id": "..."
  }
}
```

Используй для нормализации пользовательского ввода: ссылка из браузера → `post_id` для дальнейших вызовов.

### `GET /api/post/detail` — детальный пост + ветка

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `post_id` | string | ✅ | post pk (из `get-id` или из юзер-постов) |

**Пример ответа** (verified — 31 поле в `post`):

```json
{
  "data": {
    "data": {
      "edges": [
        {
          "cursor": "...",
          "node": {
            "__typename": "XDTThreadItem",
            "header": null,
            "id": "...",
            "thread_header_context": null,
            "thread_items": [
              {
                "line_type": "...",
                "post": {
                  "pk": "...",
                  "accessibility_caption": null,
                  "audio": null,
                  "caption": {
                    "has_translation": null,
                    "pk": "...",
                    "text": "..."
                  },
                  "caption_add_on": null
                  /* ещё ~26 полей: like_count, taken_at, image_versions2, video_versions, ... */
                }
              }
            ]
          }
        }
      ]
    }
  }
}
```

> 💡 Двойное вложение `data.data.edges` — это особенность этого эндпоинта (не опечатка). Внешний `data` это RapidAPI-обёртка, внутренний — Threads GraphQL.

### `GET /api/post/related` — похожие посты

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `post_id` | string | ✅ | post pk |

**Пример ответа** (verified):

```json
{
  "data": {
    "relatedPosts": {
      "threads": [
        {
          "id": "...",
          "thread_header_context": null,
          "thread_items": [
            { "post": { /* 34 поля */ } }
          ]
        }
      ]
    }
  }
}
```

### `GET /api/post/comments` — комментарии к посту

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `post_id` | string | ✅ | post pk |
| `end_cursor` | string | – | пагинация |

**Пример ответа**: структура аналогична `/api/post/detail`, но в `edges` лежат комментарии (не оригинальный пост).

> ⚠️ **Edge-case (verified 2026-04-28):** при некорректном или несуществующем `post_id` API возвращает `200 OK` с GraphQL-ошибкой:
> ```json
> {"errors":[{"message":"execution error","path":["data"],"severity":"CRITICAL"}],"data":null,"extensions":{"is_final":true,"server_metadata":{...}},"status":"ok"}
> ```
> Всегда проверяй `data !== null` перед обработкой.

---

## Search (3 эндпоинта)

### `GET /api/search/top` — top-результаты поиска

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `query` | string | ✅ | поисковый запрос |
| `end_cursor` | string | – | пагинация |

**Пример ответа** (verified):

```json
{
  "data": {
    "searchResults": {
      "inform_module": null,
      "edges": [
        {
          "node": {
            "thread": {
              "id": "...",
              "thread_items": [
                {
                  "post": {
                    "id": "...",
                    "pk": "...",
                    "user": {
                      "pk": "...",
                      "username": "...",
                      "profile_pic_url": "...",
                      "friendship_status": null,
                      "id": "..."
                    }
                    /* ещё ~26 полей поста */
                  }
                }
              ]
            }
          }
        }
      ]
      /* + page_info с end_cursor */
    }
  }
}
```

### `GET /api/search/recent` — свежие результаты поиска

Параметры идентичны `/api/search/top`. Структура ответа та же. Различие: `top` — алгоритмическая лента, `recent` — отсортировано по времени (свежее сверху).

### `GET /api/search/profiles` — поиск пользователей

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `query` | string | ✅ | поисковый запрос |

**Пример ответа** (verified):

```json
{
  "data": {
    "xdt_api__v1__users__search_connection": {
      "edges": [
        {
          "node": {
            "username": "...",
            "pk": "...",
            "id": "...",
            "full_name": "...",
            "profile_pic_url": "...",
            "is_verified": true,
            "is_active_on_text_post_app": true,
            "has_onboarded_to_text_post_app": true
          }
        }
      ]
    }
  }
}
```

> ⚠️ **`/api/search/profiles` НЕ поддерживает пагинацию** — нет параметра `end_cursor`. Возвращает фиксированный набор результатов (обычно 10).

---

## Минимальные рабочие примеры

### Username → user_id → последние посты

```python
import os, requests

API_KEY = os.environ["RAPIDAPI_KEY"]
HOST = "threads-api4.p.rapidapi.com"
headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": HOST}

# 1. Получаем user_id по username
info = requests.get(f"https://{HOST}/api/user/info",
                    headers=headers, params={"username": "reuters"}).json()
user = info["data"]["user"]
user_id = user["pk"]
print(f"{user['full_name']} ({user['follower_count']:,} followers)")

# 2. Получаем посты
posts = requests.get(f"https://{HOST}/api/user/posts",
                     headers=headers, params={"user_id": user_id}).json()

for edge in posts["data"]["mediaData"]["edges"]:
    for item in edge["node"]["thread_items"]:
        post = item["post"]
        text = post.get("caption", {}).get("text", "")
        print(f"#{post['pk']}: {text[:120]}")
```

### Пагинация постов

```python
def get_all_posts(user_id, max_pages=10):
    end_cursor = None
    for _ in range(max_pages):
        params = {"user_id": user_id}
        if end_cursor:
            params["end_cursor"] = end_cursor
        r = requests.get(f"https://{HOST}/api/user/posts",
                         headers=headers, params=params, timeout=15).json()
        media = r["data"]["mediaData"]
        for edge in media.get("edges", []):
            for item in edge["node"]["thread_items"]:
                yield item["post"]
        end_cursor = media.get("page_info", {}).get("end_cursor")
        if not end_cursor:
            break
```

### URL поста → детали

```python
url = "https://www.threads.net/@reuters/post/Cv1abcXXXX"

# 1. Конвертируем URL в post_id
ids = requests.get(f"https://{HOST}/api/post/get-id",
                   headers=headers, params={"url": url}).json()
post_id = ids["data"]["post_id"]

# 2. Получаем детали
detail = requests.get(f"https://{HOST}/api/post/detail",
                      headers=headers, params={"post_id": post_id}).json()
post = detail["data"]["data"]["edges"][0]["node"]["thread_items"][0]["post"]
print(post["caption"]["text"])
```

### Поиск свежих упоминаний и фильтр верифицированных

```python
results = requests.get(f"https://{HOST}/api/search/recent",
                       headers=headers, params={"query": "claude api"}).json()

for edge in results["data"]["searchResults"]["edges"]:
    post = edge["node"]["thread"]["thread_items"][0]["post"]
    if post["user"].get("friendship_status") is None:  # verified-only фильтр пропускаю
        username = post["user"]["username"]
        print(f"@{username}: ...")
```

### Анализ репостов автора

```python
reposts = requests.get(f"https://{HOST}/api/user/reposts",
                       headers=headers, params={"user_id": user_id}).json()

for edge in reposts["data"]["mediaData"]["edges"]:
    node = edge["node"]
    if node.get("thread_header_context", {}).get("context_type") == "REPOST":
        post = node["thread_items"][0]["post"]
        print(f"Reposted from @{post['user']['username']}: {post.get('caption', {}).get('text', '')[:100]}")
```

---

## Типичные проблемы

### `HTTP 401 {"message": "Invalid API key. ..."}` (verified)

Невалидный или отсутствующий `X-RapidAPI-Key`.

### Пустые `edges: []`

- Юзер приватный (`text_post_app_is_private: true`).
- Юзер удалён или забанен Meta.
- Запрос с истёкшим/неверным `end_cursor`.

### `null` в `caption` или `user`

Threads-API часто возвращает `null` для отсутствующих полей. **Всегда используй `.get()`** или защитное чтение:

```python
text = post.get("caption", {}).get("text", "") if post.get("caption") else ""
```

### Глубокая вложенность `data.data.edges`

В `/api/post/detail` и некоторых других эндпоинтах `data` встречается дважды. Это не опечатка — внешний `data` это RapidAPI-обёртка, внутренний — Threads GraphQL. Запиши один раз helper:

```python
def thread_items(response, *path):
    cur = response
    for p in path:
        cur = cur[p]
    return cur
```

### `__typename` поле

Threads возвращает GraphQL-теги (`XDTThreadItem`, `XDTUserDict`). Не пугайся — это нормально, просто игнорируй если не строишь типизированный клиент.

### Схема меняется

Meta агрессивно меняет внутреннее API Threads — провайдер за этим следует, имена полей могут поменяться без анонса. **Всегда `.get(key, default)`**, не используй точечный доступ.

### Rate limit 429

Лимиты по плану:
- Basic: 1000 req/час (но месячный лимит 50 — упрёшься быстрее)
- Pro: 3 req/sec
- Ultra: 5 req/sec
- Mega: 10 req/sec

При превышении — 429. Throttle на клиенте (`time.sleep(1.05/rate)`), кэш для одинаковых запросов.

### `200 OK`, но `data: null` или `data: {}`

API может вернуть успешный статус с пустыми данными при некорректном `user_id`/`post_id`. Всегда проверяй наличие ключевых полей перед использованием.

```python
data = r.json().get("data", {})
if not data or "user" not in data:
    raise RuntimeError(f"unexpected response: {r.json()}")
```

---

## Тарифы и расчёт расходов

> 📌 Этот раздел — для AI-ассистента. Когда пользователь спрашивает "сколько это будет стоить?" — используй данные ниже.

### Тарифные планы (verified из Pricing tab, 2026-04-28)

| План | Запросов/мес | Rate Limit | Цена/мес | Overage |
|------|--------------|------------|----------|---------|
| **Basic** | 50 | 1000 req/час | **$0** | **hard limit** → 429 |
| **Pro** | 20 000 | **3 req/sec** | **$19.99** | $0.0035 за extra (soft) |
| **Ultra** ⭐ | 100 000 | **5 req/sec** | **$99.99** | $0.002 за extra (soft) |
| **Mega** | 500 000 | **10 req/sec** | **$299.99** | $0.001 за extra (soft) |

**Bandwidth (на всех планах):** 10 240 MB/мес включено + **$0.001 за каждый дополнительный 1 MB**.

> ⚠️ **Особенности тарифов этого коннектора:**
>
> - **Basic — hard limit (50 req/мес!).** Это очень мало, на тестирование хватит, но любая реальная задача требует Pro+.
> - **Pro/Ultra/Mega — soft limit с overage.** Если не следить за квотой — деньги списываются автоматически. Включай алерты в RapidAPI dashboard.
> - **Threads — дорогой коннектор.** Сравни с telegram-channel (Pro $15) или yt-api (Pro $51) — тут $20 уже на Pro.

### Стоимость одного запроса в квоте

| Что делает запрос | Стоимость | Пример |
|---|---|---|
| **База** (любой GET) | **1 unit** | любой эндпоинт |

У этого коннектора **нет** платных модификаторов (`extend`, `local`, multi-id и т.п.). Каждый запрос всегда = ровно 1 unit. Это упрощает расчёт.

### Формула расчёта месячной стоимости

```
month_quota_usage = запросов_в_месяц            # каждый = 1 unit
month_bandwidth_mb = средний_размер_ответа_MB × запросов_в_месяц

# Подбор плана:
if month_quota_usage <= 50:                     plan = Basic ($0)  # очень тесно
elif month_quota_usage <= 20_000 and rate ≤ 3:  plan = Pro ($19.99)
elif month_quota_usage <= 100_000 and rate ≤ 5: plan = Ultra ($99.99)
elif month_quota_usage <= 500_000 and rate ≤ 10: plan = Mega ($299.99)
else:  plan = Mega + overage ($0.001 × extras)

# Overage (для Pro/Ultra/Mega — soft):
extras = max(0, month_quota_usage - plan_quota)
overage_cost = extras × overage_per_extra($)

# Bandwidth:
extra_mb = max(0, month_bandwidth_mb - 10240)
bandwidth_cost = extra_mb × $0.001

total_monthly = plan_price + overage_cost + bandwidth_cost
```

### Реальные сценарии (сколько это будет стоить)

#### 1. Учебный проект — посмотреть инфо 5 профилей и по 1 странице постов

```
5 × (1 запрос /user/info + 1 запрос /user/posts) = 10 запросов разово
ПЛАН: Basic ($0) — помещается в 50 req/мес
ИТОГО: $0
```

#### 2. Полная выгрузка постов 10 профилей (по 200 постов в среднем)

```
10 × (1 /user/info + 200/25 = 8 страниц по /user/posts) = 90 запросов разово
ПЛАН: Basic ($0) — помещается
ИТОГО: $0 (одна выгрузка)

Но если делать каждый день: 90 × 30 = 2700/мес → не Basic
ПЛАН: Pro ($19.99) — 2700 < 20 000
```

#### 3. Дашборд из 50 профилей с обновлением раз в час

```
50 × 24 × 30 × 1 (только /user/info, без постов) = 36 000 req/мес
Rate: 50/час = 0.014 req/sec — далеко от любого лимита
Bandwidth: ~3 KB × 36k = 108 MB → в лимите
ПЛАН: Ultra ($99.99) — 36k < 100k
   ИЛИ: Pro ($19.99) с overage: 36k - 20k = 16k × $0.0035 = $56
   → Ultra на $20 дешевле
ИТОГО: $99.99/мес — но только если кэшировать на час нет смысла
```

С кэшем: проверка раз в 6 часов → 6000 req/мес → Pro ($19.99).

#### 4. Мониторинг новых постов 20 профилей каждые 30 минут

```
20 × 48 × 30 × 1 (/user/posts) = 28 800 req/мес
Rate: 20 за полминуты = 0.67 req/sec → влезает в Pro (3 req/sec)
ПЛАН: Pro ($19.99) с overage: 28 800 - 20 000 = 8 800 × $0.0035 = $30.80
   ИЛИ: Ultra ($99.99) — 28k < 100k, без overage
   → Pro+overage = $50.80, Ultra = $100. **Pro дешевле!**

ИТОГО: $50.80/мес
```

⚠️ Этот сценарий показывает что иногда **Pro+overage дешевле, чем Ultra**. Точка перехода: `(Ultra - Pro) / overage_per_extra = ($99.99 - $19.99) / $0.0035 = 22 858 extras`. То есть до 42 858 req/мес выгоднее Pro, выше — Ultra.

#### 5. Скрейпинг 1000 профилей с глубокой выгрузкой постов и комментариев

```
1000 × (1 /user/info + 5 страниц /user/posts) = 6 000 req/мес на профили
Допустим, по 50 интересных постов на профиль и комментарии к ним (3 страницы):
  1000 × 50 × 3 = 150 000 req/мес на /post/comments

ИТОГО: ~156 000 req/мес
Rate: при 5 req/sec выгрузка займёт 156k/3600/5 = 8.7 часа

ПЛАН: Ultra ($99.99) с overage: 56k × $0.002 = $112
   ИЛИ: Mega ($299.99) — 156k < 500k, без overage и rate 10/sec
   → Ultra+overage = $212, Mega = $300. Ultra дешевле, но Mega быстрее.

ИТОГО: $212/мес (Ultra) или $300/мес (Mega за +5 req/sec скорости)
```

#### 6. Real-time мониторинг 200 поисковых запросов каждые 5 минут

```
200 × (60/5 = 12) × 24 × 30 = 1 728 000 req/мес — больше Mega
Mega даёт 500k включено, overage = 1.228M × $0.001 = $1228
ИТОГО: $299.99 + $1228 = ~$1528/мес 😱

РЕАЛЬНЫЙ ВАРИАНТ: опрос раз в 30 минут вместо 5 → 288k/мес → Mega ($299.99) без overage.
ЛУЧШЕ: распределить по приоритетам — топ-50 раз в 5 мин, остальные раз в час.
```

⚠️ Real-time на Threads — **дорого**. Если нужен инкремент новых постов — лучше polling раз в 30+ минут с кэшем `pk` последнего виденного.

### Чеклист "как сэкономить квоту"

1. **Кэшируй `/api/user/info`** на сутки или больше — данные профиля меняются медленно.
2. **Кэшируй `/api/post/get-id`** **навсегда** — URL → post_id это детерминированный converter, никогда не меняется.
3. **Не дёргай `/user/info` каждый раз** — сохраняй `pk` (user_id) в БД, обращайся к юзеру по нему. Это разовый запрос на профиль.
4. **При мониторинге новых постов** — сохраняй `pk` последнего виденного поста и фильтруй на клиенте, а не запрашивай всю историю.
5. **Сравни Pro+overage vs Ultra** на нагрузках 20-43k req/мес — Pro+overage может быть дешевле!
6. **Mega только если** реально нужно >5 req/sec или ожидаешь >100k extras (тогда $0.001 имеет значение).
7. **Throttle на клиенте** для предотвращения 429: `time.sleep(1/rate_limit + 0.05)`.
8. **Не используй `/user/posts` для метрик профиля** — `/user/info` уже даёт `follower_count`, `is_verified`. `posts` нужен только для контента.
9. **`/api/search/profiles` нет пагинации** — 1 запрос даёт максимум, не пытайся брать страницы.
10. **На Basic-плане осторожно** — 50 req/мес кончатся за 1 часа реальной отладки. Закладывай Pro сразу.

---

## Что хорошо подходит для учебных проектов

- Анализ постов публичного профиля (10-100 постов) — Basic хватит.
- Поиск трендовых тем через `/api/search/top` — топ-результаты.
- Сравнение `follower_count` нескольких профилей — батч из 5-20 `/user/info`.
- Sentiment-анализ комментариев одного поста через `/api/post/comments`.
- Извлечение упоминаний (mentions) из биографий через `text_app_biography.text_fragments`.
- Обнаружение репостов влиятельных аккаунтов через `/user/reposts`.

## Что не делать

- **Не качать всю историю Threads** для популярного профиля — это десятки тысяч постов, на Basic закончится за минуту, на Pro — за час квоты.
- **Не строить real-time** на этом коннекторе — минимальный разумный polling 30 минут.
- **Не использовать Basic для прода** — 50 req/мес = 1.6 в день, нереально.
- **Не игнорировать soft limit на Pro/Ultra/Mega** — overage считается автоматически и может неприятно удивить в счёте.
- **Не публиковать `profile_pic_url`** долгосрочно — Threads/Instagram CDN их инвалидирует.
- **Не вызывать API из браузера** — ключ утечёт.
- **Не сохранять `__typename` поля** в БД — они зашумляют схему и могут поменяться.

## Альтернативы

Если эти 12 эндпоинтов недостаточно (нужны: постинг, реакции, DM, приватные профили):

- **Официальный Threads API** (https://developers.facebook.com/docs/threads) — бесплатно, но требует Meta App + OAuth.
- Этот RapidAPI-коннектор — компромисс: ничего не настраиваешь, работает сразу, но только публичные данные на чтение.
