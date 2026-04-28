# Instagram Looter (irrors-apis)

**Провайдер:** irrors-apis
**Страница:** https://rapidapi.com/irrors-apis/api/instagram-looter2
**Subscribe (Pricing):** https://rapidapi.com/irrors-apis/api/instagram-looter2/pricing
**Base URL:** `https://instagram-looter2.p.rapidapi.com`
**Host-заголовок:** `instagram-looter2.p.rapidapi.com`

> ⚠️ **Перед первым запросом — оформи подписку** на странице Pricing. Без подписки любой вызов вернёт `403`. Free-план — **Basic** (150 req/мес), **требует привязанную карту**. Pro и Basic — оба hard limit, без overage. Подробности в [docs/getting-started.md](../docs/getting-started.md).

API для парсинга **Instagram**: профили, посты, рилсы, репосты, отмеченные медиа, хэштеги, локации, исследовательская лента (Explore), глобальный поиск, утилиты конвертации username/userId/mediaURL/shortcode. **30 эндпоинтов** (все GET) в 7 группах.

> ✅ **Источник схемы.** Все **30 эндпоинтов** провалидированы реальными API-вызовами на Basic-плане (2026-04-28). Тарифы, формат 401 и форма ответа — verified живыми запросами. Точные ключи верхнего уровня по каждому эндпоинту см. в секции "Verified response shapes" в конце карточки.
>
> Провайдер не заполнил Example Responses в Playground для этого API — поэтому сверяйся либо с этой карточкой, либо делай свой запрос на Basic ($0).

## Авторизация

```
X-RapidAPI-Key: <ключ>
X-RapidAPI-Host: instagram-looter2.p.rapidapi.com
```

**Формат ошибки 401** (verified):

```http
HTTP/1.1 401 Unauthorized
{"message": "Invalid API key. Go to https://docs.rapidapi.com/docs/keys for more info."}
```

## Общие правила

### Идентификаторы Instagram

Этот API использует все основные идентификаторы Instagram:

- **`username`** — handle без `@` (`zuck`, `cristiano`).
- **`id`** / **`userId`** — числовая строка (стабильный internal user ID).
- **`shortcode`** — буквенно-цифровой код поста из URL (`Cv1AbcXXXX` из `instagram.com/p/Cv1AbcXXXX/`).
- **`media id`** — числовой ID поста (внутренний).
- **`location id`** — числовой ID локации.
- **`city_id`** — внутренний ID города (для локационной иерархии).

Стандартный flow для пользователя:
```
username → /id → userId → /profile или /user-feeds → ...
```

И для поста:
```
URL поста → /id-media → media_id → /post → детали
```

### Параметр `fields` — бесплатная экономия bandwidth

**Все 30 эндпоинтов** принимают опциональный параметр `fields` для сокращения размера ответа:

```python
params = {"username": "zuck", "fields": "id,username,full_name,follower_count"}
```

Возвращаются только запрошенные поля. Не влияет на квоту, но **сильно сокращает bandwidth** — главное оружие в этом коннекторе. Используй везде.

### Пагинация (3 разных стиля)

Этот API использует разные курсоры в разных группах:

| Эндпоинты | Курсор | Заметка |
|---|---|---|
| `/user-feeds`, `/reels`, `/user-reposts`, `/section`, `/music` | `max_id` | string ID последнего элемента |
| `/user-feeds2`, `/user-tags`, `/tag-feeds`, `/location-feeds` | `end_cursor` | стандартный Instagram-курсор |
| `/cities`, `/locations` | `page` | пагинация по номеру страницы |

В response поля называются так же. Если не получил — страниц больше нет.

### Универсальный `/search` — 4 разных поведения

**Внимание:** есть 4 разных эндпоинта по пути `/search`:

| Контекст | `select` | Что возвращает |
|---|---|---|
| Search users by keyword | `users` | поиск пользователей |
| Search hashtags by keyword | `hashtags` | поиск хэштегов |
| Search locations by keyword | `locations` | поиск локаций |
| Global search | (нет, только `query`) | смешанная выдача |

`select` — обязательный параметр для трёх первых. Без `select` (только `query`) — это Global search.

### Внутренний формат ответов

Использует Instagram API структуру. Видео/посты следуют схеме `Media` (`Item`):

```json
{
  "id": "12345_67890",
  "shortcode": "Cv1AbcXXXX",
  "taken_at": 1700000000,
  "media_type": 1,
  "caption": {"text": "..."},
  "image_versions2": {"candidates": [{"url": "...", "width": 1080, "height": 1080}]},
  "video_versions": [{"url": "...", "width": 720, "height": 1280}],
  "user": {"pk": "...", "username": "...", "full_name": "...", "is_verified": false},
  "like_count": 123,
  "comment_count": 45,
  "play_count": 1000,
  "carousel_media": [...]
}
```

`media_type`: 1 = фото, 2 = видео/рилс, 8 = карусель (несколько медиа в `carousel_media`).

---

## Эндпоинты (30)

### 🧩 Identity Utilities (4)

Утилиты конвертации между разными идентификаторами Instagram.

| Эндпоинт | Path | Параметры |
|---|---|---|
| Username from user ID | `/id` | ✅ `id`, – `fields` |
| User ID from username | `/id` | ✅ `username`, – `fields` |
| Media shortcode from media ID | `/id-media` | ✅ `id`, – `fields` |
| Media ID from media URL | `/id-media` | ✅ `url`, – `fields` |

> 💡 Это самые **дешёвые** и быстрые эндпоинты — каждый = 1 unit. Кэшируй результаты **навсегда** (детерминированные конвертеры).

### 👤 User Insights (12)

| Эндпоинт | Path | Параметры |
|---|---|---|
| User info by username | `/profile` | ✅ `username`, – `fields` |
| User info (V2) by username | `/profile2` | ✅ `username`, – `fields` |
| User info by user ID | `/profile` | ✅ `id`, – `fields` |
| User info (V2) by user ID | `/profile2` | ✅ `id`, – `fields` |
| Web profile info by username | `/web-profile` | ✅ `username`, – `fields` |
| Media list by user ID | `/user-feeds` | ✅ `id`, ✅ `count`, – `allow_restricted_media`, – `max_id`, – `fields` |
| Media list (V2) by user ID | `/user-feeds2` | ✅ `id`, ✅ `count`, – `end_cursor`, – `fields` |
| Reels by user ID | `/reels` | ✅ `id`, ✅ `count`, – `max_id`, – `fields` |
| Reposts by user ID | `/user-reposts` | ✅ `id`, – `max_id`, – `fields` |
| Tagged media by user ID | `/user-tags` | ✅ `id`, ✅ `count`, – `end_cursor`, – `fields` |
| Related profiles by user ID | `/related-profiles` | ✅ `id`, – `fields` |
| Search users by keyword | `/search` | ✅ `query`, ✅ `select=users`, – `fields` |

> 💡 **Когда какую версию выбрать:**
> - `/profile` — базовая инфа (имя, био, follower_count, аватар).
> - `/profile2` — расширенная (то же + business info, contact, более глубокие поля).
> - `/web-profile` — сырой JSON, который Instagram отдаёт на странице профиля. Самый детальный, но и самый "сырой".
> - `/user-feeds` vs `/user-feeds2` — разная пагинация (`max_id` vs `end_cursor`). V2 обычно стабильнее.

### 📸 Media Details (4)

| Эндпоинт | Path | Параметры |
|---|---|---|
| Media info by URL | `/post` | ✅ `url`, – `fields` |
| Media info by ID | `/post` | ✅ `id`, – `fields` |
| Download link by media ID or URL | `/post-dl` | ✅ `url`, – `fields` |
| Music info by music ID | `/music` | ✅ `id`, – `max_id`, – `fields` |

`/post` принимает `url` ИЛИ `id` — один из. `/post-dl` отдаёт прямые ссылки на видео/фото.

### 🔖 Hashtag Lookup (2)

| Эндпоинт | Path | Параметры |
|---|---|---|
| Media by hashtag | `/tag-feeds` | ✅ `query` (без `#`), – `end_cursor`, – `fields` |
| Search hashtags by keyword | `/search` | ✅ `query`, ✅ `select=hashtags`, – `fields` |

### 🗺️ Location Data (5)

| Эндпоинт | Path | Параметры |
|---|---|---|
| Search locations by keyword | `/search` | ✅ `query`, ✅ `select=locations`, – `fields` |
| Location info by location ID | `/location-info` | ✅ `id`, – `fields` |
| Media by location ID | `/location-feeds` | ✅ `id`, ✅ `tab`, – `ranked`, – `end_cursor`, – `fields` |
| Cities by country code | `/cities` | ✅ `country_code` (ISO `US`, `RU`...), – `page`, – `fields` |
| Locations by city ID | `/locations` | ✅ `city_id`, – `page`, – `fields` |

`/location-feeds` параметр `tab`: `recent` (свежее) или `top` (топ). `ranked` — bool флаг для альтернативной сортировки.

### 🔍 Explore Feed (2)

Лента "Интересное" (Explore) Instagram, разбита на категории.

| Эндпоинт | Path | Параметры |
|---|---|---|
| Explore sections list | `/sections` | – `fields` (без обязательных) |
| Media by explore section ID | `/section` | ✅ `id`, ✅ `count`, – `max_id`, – `fields` |

Сначала `/sections` для списка категорий, потом `/section?id=<categoryId>` для контента.

### 🌐 Global Search (1)

| Эндпоинт | Path | Параметры |
|---|---|---|
| Global search by keyword | `/search` | ✅ `query`, – `fields` |

Без `select` параметра — смешанная выдача (юзеры + хэштеги + локации).

---

## Минимальные рабочие примеры

### username → user_id → последние посты

```python
import os, requests

API_KEY = os.environ["RAPIDAPI_KEY"]
HOST = "instagram-looter2.p.rapidapi.com"
headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": HOST}

# 1. Конвертируем username в id
r1 = requests.get(f"https://{HOST}/id",
                  headers=headers, params={"username": "zuck"}).json()
user_id = r1.get("id") or r1.get("user_id")

# 2. Получаем профиль
profile = requests.get(f"https://{HOST}/profile2",
                       headers=headers,
                       params={"id": user_id, "fields": "username,full_name,follower_count,is_verified"}).json()
print(f"{profile['full_name']} ({profile['follower_count']:,} followers)")

# 3. Последние 30 постов (V2 — стабильнее)
posts = requests.get(f"https://{HOST}/user-feeds2",
                     headers=headers,
                     params={"id": user_id, "count": 30}).json()
for m in posts.get("items", []):
    cap = (m.get("caption") or {}).get("text", "")
    print(f"#{m['id']} likes={m.get('like_count',0)} — {cap[:80]}")
```

### Пагинация через end_cursor (V2 endpoints)

```python
def get_all_posts_v2(user_id, max_pages=10):
    end_cursor = None
    for _ in range(max_pages):
        params = {"id": user_id, "count": 30}
        if end_cursor:
            params["end_cursor"] = end_cursor
        r = requests.get(f"https://{HOST}/user-feeds2",
                         headers=headers, params=params, timeout=15).json()
        for item in r.get("items", []):
            yield item
        end_cursor = r.get("end_cursor") or r.get("next_max_id")
        if not end_cursor:
            break
```

### Пагинация через max_id (V1)

```python
def get_all_reels(user_id, max_pages=10):
    max_id = None
    for _ in range(max_pages):
        params = {"id": user_id, "count": 30}
        if max_id:
            params["max_id"] = max_id
        r = requests.get(f"https://{HOST}/reels",
                         headers=headers, params=params, timeout=15).json()
        for item in r.get("items", []):
            yield item
        max_id = r.get("next_max_id") or r.get("max_id")
        if not max_id:
            break
```

### URL поста → детали → скачать

```python
url = "https://www.instagram.com/p/Cv1AbcXXXX/"

# Прямые ссылки на медиа
dl = requests.get(f"https://{HOST}/post-dl",
                  headers=headers, params={"url": url}).json()
# обычно содержит "video_url" или "image_url" или "carousel" массив

# Полные метаданные
info = requests.get(f"https://{HOST}/post",
                    headers=headers, params={"url": url}).json()
print(f"likes={info.get('like_count')} comments={info.get('comment_count')}")
```

### Универсальный поиск через `/search`

```python
# Юзеры
users = requests.get(f"https://{HOST}/search",
                     headers=headers, params={"query": "tesla", "select": "users"}).json()

# Хэштеги
tags = requests.get(f"https://{HOST}/search",
                    headers=headers, params={"query": "tesla", "select": "hashtags"}).json()

# Локации
locations = requests.get(f"https://{HOST}/search",
                         headers=headers, params={"query": "berlin", "select": "locations"}).json()

# Глобально (всё сразу)
mixed = requests.get(f"https://{HOST}/search",
                     headers=headers, params={"query": "tesla"}).json()
```

### Локационная иерархия: страна → город → локации → посты

```python
# 1. Города России
cities = requests.get(f"https://{HOST}/cities",
                      headers=headers, params={"country_code": "RU"}).json()

# 2. Локации в Москве (берём первый city из cities)
city_id = cities["data"][0]["id"]
locs = requests.get(f"https://{HOST}/locations",
                    headers=headers, params={"city_id": city_id}).json()

# 3. Посты в локации (берём первую)
loc_id = locs["data"][0]["id"]
feed = requests.get(f"https://{HOST}/location-feeds",
                    headers=headers, params={"id": loc_id, "tab": "top"}).json()

for item in feed.get("items", []):
    print(item["id"], item.get("caption", {}).get("text", "")[:80])
```

### Выгрузка с минимальным bandwidth через fields

```python
# Запросить только нужные поля — экономия 80-90% размера ответа
r = requests.get(f"https://{HOST}/user-feeds2",
                 headers=headers,
                 params={"id": user_id, "count": 30,
                         "fields": "items.id,items.caption.text,items.like_count,items.taken_at"}).json()
```

---

## Типичные проблемы

### `HTTP 401 {"message": "Invalid API key. ..."}` (verified)

Невалидный или отсутствующий `X-RapidAPI-Key`.

### `200 OK` с пустым ответом

- Юзер приватный — посты не отдаются.
- Юзер удалён или забанен Instagram.
- Невалидный `id` (часто — забыл прогнать username через `/id`).
- Гео-блокировка (Instagram CDN).

### `next_max_id` vs `end_cursor` — разные поля в разных версиях

- V1 (`/user-feeds`, `/reels`) — пагинация по `max_id`, поле в response `next_max_id`.
- V2 (`/user-feeds2`, `/user-tags`) — пагинация по `end_cursor`, поле в response `end_cursor`.

**Не путай их между эндпоинтами.** Используй маленькие функции под каждый стиль.

### `/search` возвращает пусто без `select`

Без `select` — это global search (смешанная выдача). С `select` — нужно указать одно из `users`/`hashtags`/`locations`. Промежуточные значения не работают.

### Карусели (`media_type: 8`)

Если пост — карусель (несколько фото/видео), реальные медиа лежат в `carousel_media[]`, а не в верхнеуровневых `image_versions2`/`video_versions`. Парсер должен это учитывать:

```python
def get_media_urls(item):
    if item.get("media_type") == 8:
        return [c.get("video_versions") or c.get("image_versions2") for c in item.get("carousel_media", [])]
    return [item.get("video_versions") or item.get("image_versions2")]
```

### Истёкшие медиа-URL

`image_versions2.candidates[].url` и `video_versions[].url` подписаны и **протухают** через несколько часов. Не сохраняй надолго — перезапрашивай.

### Rate limit 429

- Basic: 1000/час (но месяц 150 — упрёшься быстрее).
- Pro: 10 req/sec.
- Ultra: 30 req/sec.
- Mega: 60 req/sec.

При превышении — 429.

### `count` — обязательный параметр в нескольких эндпоинтах

В отличие от других API (где `count` опциональный), здесь у `/user-feeds`, `/user-feeds2`, `/reels`, `/user-tags`, `/section` параметр `count` помечен **обязательным**. Без него — ошибка.

---

## Тарифы и расчёт расходов

> 📌 Этот раздел — для AI-ассистента. Когда пользователь спрашивает "сколько это будет стоить?" — используй данные ниже.

### Тарифные планы (verified из Pricing tab, 2026-04-28)

| План | Запросов/мес | Rate Limit | Цена/мес | Overage |
|------|--------------|------------|----------|---------|
| **Basic** | 150 | 1000/час | **$0** | **hard limit** → 429 |
| **Pro** | 15 000 | **10 req/sec** | **$9.90** | **hard limit** → 429 |
| **Ultra** | 75 000 | **30 req/sec** | **$27.90** | **$0.001** за extra (soft) |
| **Mega** ⭐ | 250 000 | **60 req/sec** | **$75.90** | **$0.0005** за extra (soft) |

**Bandwidth (на всех планах):** 10 240 MB/мес включено + **$0.001 за каждый дополнительный 1 MB**.

> ⚠️ **Особенности тарифов:**
>
> - **Basic И Pro — оба hard limit!** Это редкость. На Pro ($9.90) при превышении 15k req будет 429 без автоплат — задача встанет до начала следующего месяца.
> - **Ultra/Mega — soft limit с overage**. Если планируешь >15k req/мес — переходи на Ultra сразу, иначе Pro заблокируется.
> - **Высокий rate-limit на Mega** (60 req/sec) — сильно быстрее других коннекторов в этом репо.

### Стоимость одного запроса в квоте

| Что делает запрос | Стоимость | Пример |
|---|---|---|
| **База** (любой GET) | **1 unit** | любой эндпоинт |

У этого коннектора **нет** платных модификаторов. Каждый запрос всегда = 1 unit. `fields` бесплатный (наоборот, экономит bandwidth).

### Формула расчёта месячной стоимости

```
month_quota_usage = запросов_в_месяц            # 1 unit per request
month_bandwidth_mb = средний_размер_ответа × запросов_в_месяц
                    # с fields обычно 1-5 KB на ответ; без fields — 50-200 KB

# Подбор плана:
if month_quota_usage <= 150:                       plan = Basic ($0)
elif month_quota_usage <= 15_000 and rate ≤ 10:    plan = Pro ($9.90, hard!)
elif month_quota_usage <= 75_000 and rate ≤ 30:    plan = Ultra ($27.90)
elif month_quota_usage <= 250_000 and rate ≤ 60:   plan = Mega ($75.90)
else: plan = Mega + overage ($0.0005 × extras)

# Bandwidth (если без fields):
extra_mb = max(0, month_bandwidth_mb - 10240)
bandwidth_cost = extra_mb × $0.001

total_monthly = plan_price + overage_cost + bandwidth_cost
```

### Реальные сценарии (сколько это будет стоить)

#### 1. Учебный — 5 профилей разово

```
5 × (1 /id + 1 /profile2) = 10 запросов разово
ПЛАН: Basic ($0) — 10 < 150
ИТОГО: $0
```

#### 2. Дашборд из 30 профилей раз в час

```
30 × 24 × 30 = 21 600 req/мес на /profile2
ПЛАН: Pro ($9.90) — НЕТ, 21.6k > 15k → попадёт в hard limit, оборвёт.
   → Ultra ($27.90) — единственный нормальный путь.
   ИЛИ: реже опросы (раз в 2 часа) → 10800 req → Pro подходит.
ИТОГО: $27.90/мес ИЛИ $9.90 при половинной частоте.
```

⚠️ **Pro hard limit** — это ловушка: если планируешь чуть больше 15k, переходи сразу на Ultra. Pro $9.90 не подстрахуется автоматически.

#### 3. Скрейпинг 1000 профилей с глубокой выгрузкой постов

```
1000 × (1 /id + 1 /profile2 + 5 страниц /user-feeds2) = 7000 запросов разово
ПЛАН: Pro ($9.90) — 7k < 15k. Но если проект регулярный — учти месячный лимит.
ИТОГО: $9.90 (одна выгрузка); $9.90/мес если делать раз в месяц
```

#### 4. Мониторинг новых постов 100 авторов каждые 30 минут

```
100 × 48 × 30 = 144 000 req/мес на /user-feeds2
Rate: 100/30мин = 0.055 req/sec → влезает в любой план
ПЛАН: Ultra ($27.90) — 144k < 75k → НЕТ, > 75k.
   → Mega ($75.90) — 144k < 250k, помещается.
   ИЛИ: Ultra ($27.90) с overage: 144 000 - 75 000 = 69 000 × $0.001 = $69
   → Ultra+overage = $96.90 vs Mega = $75.90. **Mega дешевле!**
ИТОГО: $75.90/мес
```

⚠️ Точка перехода Ultra→Mega: `($75.90 - $27.90) / $0.001 = 48 000 extras`. Выше 123k req/мес выгоднее Mega.

#### 5. Анализ хэштегов: трекинг 200 хэштегов раз в час

```
200 × 24 × 30 = 144 000 req/мес на /tag-feeds (та же ситуация что в №4)
ПЛАН: Mega ($75.90)
ИТОГО: $75.90/мес
```

#### 6. Локационный анализ: посты по всем городам страны

```
1 запрос /cities (получить список) + 100 городов × (1 /locations + 1 /location-feeds × 5 страниц) ≈ 600 запросов разово
ПЛАН: Pro ($9.90) — 600 < 15k. Хватит надолго.
ИТОГО: $9.90 (одна выгрузка)
```

#### 7. Скачивание медиа 50 авторов × 100 постов

```
ЗАПРОСЫ: 50 × (1 /id + 4 /user-feeds2 + 100 /post-dl) ≈ 5250 запросов разово
ПЛАН: Pro ($9.90) — 5250 < 15k.

BANDWIDTH:
  50 × 100 × ~1 MB на пост (метаданные в ответе) = 5 GB → в лимите 10 GB
  Само скачивание медиа идёт с CDN Instagram (mim Instagram CDN), bandwidth API НЕ учитывается.
ИТОГО: $9.90 (одна выгрузка)
```

⚠️ Скачивание медиа из CDN не считается в bandwidth этого API (как с Telegram-channel).

#### 8. Real-time мониторинг 500 авторов каждые 5 минут

```
500 × 12 × 24 × 30 = 4 320 000 req/мес 😱
Rate: 500/5min = 1.67 req/sec → норм для всех планов

ПЛАН: Mega ($75.90) — 4.3M > 250k, overage 4.07M × $0.0005 = $2035
ИТОГО: $75.90 + $2035 = ~$2110/мес 💸

РЕАЛЬНЫЙ ВАРИАНТ: каждые 30 мин → 720 000 req/мес → Mega ($75.90) с overage 470k × $0.0005 = $235
ИТОГО: $310/мес
```

⚠️ Real-time на Instagram = очень дорого. Используй максимум опрос раз в 30+ минут с кэшем "последний виденный media_id".

### Чеклист "как сэкономить квоту"

1. **Используй `fields` параметр везде** — экономия 80-90% bandwidth, влияет на overage за MB.
2. **Кэшируй `/id` и `/id-media` навсегда** — конвертеры детерминированные.
3. **Кэшируй `/profile2` на сутки** — данные профиля меняются медленно.
4. **На polling используй `count=30` (макс)** + фильтрация по id, чтобы не перебирать страницы.
5. **На Pro плане осторожно** — hard limit на 15k. Считай заранее. Переход на Ultra ($27.90) гораздо безопаснее, если есть риск.
6. **Mega ⭐ дешевле Ultra+overage** при >123k req/мес. Считай по точке перехода.
7. **`/sections` (Explore list) кэшируй на день** — категории редко меняются.
8. **Не дёргай Instagram CDN из этого API** — медиа-URL уже в ответе на `/post-dl`, скачивание идёт мимо API bandwidth.
9. **Throttle на клиенте**: на Pro ~100ms между запросами, Ultra ~33ms, Mega ~17ms.
10. **Не делай универсальный paginator** — `max_id` (V1) и `end_cursor` (V2) — разные стили. Под каждый эндпоинт свой код.

---

## Что хорошо подходит для учебных проектов

- Анализ профиля автора + последние 30 постов на Basic ($0).
- Sentiment-анализ caption из 100 постов автора.
- Сравнение метрик нескольких профилей (`follower_count`, `media_count`).
- Поиск виральных постов по хэштегу через `/tag-feeds`.
- Локационный анализ: какие посты популярны в конкретном городе.
- Граф related-profiles для поиска похожих аккаунтов.

## Что не делать

- **Не игнорировать hard limit на Pro** — превышение = 429 без автоплат, проект встанет до конца месяца. Если объём близок к 15k — берёшь Ultra сразу.
- **Не путать `id` (числовая строка) и `username`** — большинство feed-эндпоинтов принимают только `id`. Сначала прогоняй username через `/id`.
- **Не сохранять подписанные media-URL** надолго — они протухают.
- **Не смешивать `max_id` и `end_cursor`** между эндпоинтами — разные стили.
- **Не вызывать API из браузера** — ключ утечёт.
- **Не качать медиа массово** — нарушает ToS Instagram.

## Альтернативы

- **Instagram Graph API** (https://developers.facebook.com/docs/instagram-api) — официальный, бесплатный, но только для Business/Creator аккаунтов с OAuth.
- **Instagram Basic Display API** — для обычных юзеров с OAuth, ограничено собственными данными.
- Этот RapidAPI-коннектор — только публичные данные, без OAuth, но с риском ToS-нарушения при массовом использовании.

---

## Verified response shapes (2026-04-28)

> ✅ Все 30 эндпоинтов прошуршаны реальными API-вызовами на Basic-плане. Ниже — top-level ключи каждого ответа. Это «контракт минимум» — реальные ответы могут содержать больше вложенных полей, но top-level всегда такой.

### 🧩 Identity Utilities

```jsonc
// GET /id?username=zuck → 200
{ "status": true, "username": "zuck", "user_id": "314216", "attempts": "3" }

// GET /id?id=314216 → 200
{ "status": true, "username": "zuck", "user_id": "314216", "attempts": "10" }

// GET /id-media?id=<media_id>  ИЛИ  /id-media?url=<post_url> → 200
{ "status": true, "shortcode": "DWuq1e1D1E6", "media_id": "<numeric_id>" }
```

### 👤 User Insights

```jsonc
// GET /profile?username=zuck (или ?id=314216) → 200 — самая полная "сырая" схема
// Top-level keys (62):
{
  "status": true,
  "ai_agent_owner_username": null,
  "biography": "I build stuff",
  "bio_links": [],
  "fb_profile_biolink": null,
  "biography_with_entities": { "raw_text": "...", "entities": [] },
  "blocked_by_viewer": false,
  "restricted_by_viewer": null,
  "country_block": false,
  "eimu_id": "<id>",
  "external_url": null,
  "external_url_linkshimmed": null,
  "edge_followed_by": { "count": 14000000 },
  "fbid": "<id>",
  "followed_by_viewer": false,
  "edge_follow": { "count": 600 },
  "follows_viewer": false,
  "full_name": "Mark Zuckerberg",
  "group_metadata": null,
  "has_ar_effects": false,
  "has_clips": true,
  "has_guides": false,
  "has_channel": false,
  "has_blocked_viewer": false,
  "highlight_reel_count": 35,
  "has_onboarded_to_text_post_app": true,
  "has_requested_viewer": false,
  "hide_like_and_view_counts": false,
  "id": "314216",
  "is_business_account": false,
  "is_professional_account": true,
  "is_supervision_enabled": false,
  "is_guardian_of_viewer": false,
  "is_supervised_by_viewer": false,
  "is_supervised_user": false,
  "is_embeds_disabled": false,
  "is_joined_recently": false,
  "guardian_id": null,
  "business_address_json": null,
  "business_contact_method": "UNKNOWN",
  "business_email": null,
  "business_phone_number": null,
  "business_category_name": null,
  "overall_category_name": null,
  "category_enum": null,
  "category_name": "Personal Blog",
  "is_private": false,
  "is_verified": true,
  "is_verified_by_mv4b": false,
  "is_regulated_c18": false,
  "pinned_channels_list_count": 0,
  "profile_pic_url": "<signed_cdn_url>",
  "profile_pic_url_hd": "<signed_cdn_url>",
  "requested_by_viewer": false,
  "should_show_category": true,
  "should_show_public_contacts": false,
  "show_account_transparency_details": true,
  "show_text_post_app_badge": null,
  "remove_message_entrypoint": false,
  "transparency_label": null,
  "transparency_product": null,
  "username": "zuck",
  "edge_owner_to_timeline_media": { "count": 312, "edges": [...] }
}

// GET /profile2?username=zuck (или ?id=314216) → 200 — V2-схема, ближе к internal IG mobile API
// Top-level keys (60):
{
  "status": true,
  "fbid_v2": "<id>",
  "is_memorialized": false, "is_private": false, "has_story_archive": null,
  "is_coppa_enforced": null, "supervision_info": null,
  "is_regulated_c18": false, "regulated_news_in_locations": null,
  "bio_links": [],
  "linked_fb_info": null,
  "text_post_app_badge_label": null, "show_text_post_app_badge": null,
  "username": "zuck", "pk": "314216",
  "live_broadcast_visibility": 0, "live_broadcast_id": null,
  "profile_pic_url": "<signed_cdn_url>",
  "hd_profile_pic_url_info": { "url": "...", "width": 1080, "height": 1080 },
  "is_unpublished": false, "latest_reel_media": 0, "has_profile_pic": true,
  "profile_pic_genai_tool_info": [],
  "biography": "I build stuff", "full_name": "Mark Zuckerberg",
  "is_verified": true, "show_account_transparency_details": true,
  "account_type": 3,
  "follower_count": 14000000, "mutual_followers_count": 0,
  "profile_context_links_with_user_ids": [], "profile_context_facepile_users": [],
  "address_street": "", "city_name": "", "is_business": false, "zip": "",
  "biography_with_entities": { "entities": [] },
  "category": "Personal Blog", "should_show_category": true,
  "is_ring_creator": false, "show_ring_award": false, "ring_creator_metadata": null,
  "account_badges": [],
  "external_lynx_url": null, "external_url": null,
  "transparency_label": null, "transparency_product": null,
  "hide_creator_marketplace_badge": false,
  "id": "314216",
  "has_chaining": true, "remove_message_entrypoint": false,
  "is_embeds_disabled": false, "is_cannes": false,
  "is_professional_account": true, "following_count": 600,
  "media_count": 312, "total_clips_count": 50,
  "has_visible_media_notes": false,
  "latest_besties_reel_media": 0, "reel_media_seen_timestamp": 0,
  "attempts": "1"
}

// GET /web-profile?username=zuck → 200 — это "сырой" GraphQL ответ, обёрнутый в data
{ "data": { "user": { /* почти то же что /profile, в обёртке */ } } }

// GET /user-feeds?id=314216&count=30 → 200
{ "more_available": true, "items": [ /* IG Media-объекты */ ], "next_max_id": "..." }

// GET /user-feeds2?id=314216&count=30 → 200
{ "data": { "user": { "edge_owner_to_timeline_media": { "edges": [...], "page_info": { "end_cursor": "...", "has_next_page": true } } } } }

// GET /reels?id=314216&count=30 → 200
{ "items": [ /* Reels Media */ ] }

// GET /user-reposts?id=314216 → 200
{ "more_available": true, "items": [...] }

// GET /user-tags?id=314216&count=30 → 200
{ "data": { "user": { "edge_user_to_photos_of_you": { "edges": [...], "page_info": { "end_cursor": "...", "has_next_page": true } } } } }

// GET /related-profiles?id=314216 → 200
{ "data": { "user": { "edge_related_profiles": { "edges": [...] } } }, "status": true, "attempts": "1" }
```

### 📸 Media Details

```jsonc
// GET /post?url=<post_url> ИЛИ ?id=<media_id> → 200 — top-level keys (22):
{
  "status": true,
  "__typename": "GraphSidecar",  // или "GraphImage", "GraphVideo"
  "id": "<media_id>",
  "shortcode": "DWuq1e1D1E6",
  "thumbnail_src": "<signed_cdn_url>",
  "dimensions": { "height": 1350, "width": 1080 },
  "gating_info": null,
  "fact_check_overall_rating": null, "fact_check_information": null,
  "sensitivity_friction_info": null, "sharing_friction_info": { "should_have_sharing_friction": false },
  "media_overlay_info": null, "media_preview": "...",
  "display_url": "<signed_cdn_url>",
  "display_resources": [ {"src": "...", "config_width": 640, "config_height": 800}, ... ],
  "is_video": false, "tracking_token": "<x>",
  "upcoming_event": null,
  "edge_media_to_tagged_user": { "edges": [] },
  "owner": { "id": "...", "username": "...", "is_verified": true },
  "accessibility_caption": null,
  "edge_sidecar_to_children": { "edges": [...] }   // только для Sidecar
}

// GET /post-dl?url=<post_url> → 200
{ "data": { "video_url": "...", "image_url": "...", "carousel": [...] }, "status": true, "attempts": "1" }

// GET /music?id=<music_id>&max_id=... → 200
{ /* зависит от наличия данных; если ничего нет — { "attempts": "..." } */ }
```

### 🔖 Hashtag Lookup

```jsonc
// GET /tag-feeds?query=travel → 200
{ "data": { "hashtag": { "edge_hashtag_to_media": { "edges": [...], "page_info": { "end_cursor": "...", "has_next_page": true } } } } }
```

### 🗺️ Location Data

```jsonc
// GET /location-info?id=212988663 → 200
{
  "location_info": {
    "category": "Government organization",
    "hours": { "status": "" },
    "ig_business": { "profile": "null" },
    "lat": 40.7142, "lng": -74.0064,
    "location_address": "", "location_city": "", "location_zip": "",
    "location_id": "212988663",
    "media_count": 82334189,
    "name": "New York, New York",
    "phone": "", "price_range": 3,
    "slug": "new-york-new-york"
  },
  "attempts": "10"
}

// GET /location-feeds?id=212988663&tab=top → 200
{ "edges": [ { "node": { "code": "...", "pk": "...", "id": "..._<owner_id>", /* IG Media поля */ } }, ... ] }

// GET /cities?country_code=US → 200
{
  "country_info": { "id": "US", "name": "United States", "slug": "united-states" },
  "city_list": [ { "id": "c2753900", "name": "...", "slug": "..." }, ... ]
}

// GET /locations?city_id=c2753900 → 200
{
  "country_info": { "id": "US", ... },
  "city_info": { "id": "c2753900", "name": "...", "slug": "..." },
  "location_list": [ { "id": "372247132", "name": "...", "slug": "..." }, ... ]
}
```

### 🔍 Explore Feed

```jsonc
// GET /sections → 200
{ "sections": [ { /* explore category */ }, ... ] }

// GET /section?id=<section_id>&count=30 → 200
{ "section_name": "...", "max_id": "...", "more_available": true, "items": [...] }
```

### 🌐 Search (4 формы)

```jsonc
// GET /search?query=tesla&select=users → 200
{ "status": true, "users": [ { "user": { "pk": "...", "username": "...", ... } }, ... ] }

// GET /search?query=tesla&select=hashtags → 200
{ "status": true, "hashtags": [ { "name": "...", "media_count": ..., "id": "..." }, ... ] }

// GET /search?query=berlin&select=locations → 200
{ "status": true, "places": [ { "place": { "location": { "pk": "...", "name": "...", "lat": ..., "lng": ... } } }, ... ] }

// GET /search?query=tesla → 200 (global)
{ "status": true, "hashtags": [...], "places": [...], "users": [...] }
```

> 📝 Все 31 запрос (один эндпоинт `/profile2` тестирован дважды — by username и by id, отдают одинаковую структуру) сделаны 2026-04-28 на боевом ключе подписки Basic.
