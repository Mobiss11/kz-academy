# Verified response shapes — справочник по полям ответов

Этот каталог — **canonical reference** для проверки имён полей в ответах всех 5 коннекторов. Если ученик пишет код и сомневается «как называется поле X в ответе Y» — grep по этому каталогу.

## Источники верификации

| Коннектор | Эндпоинтов | Verified by |
|---|---|---|
| [instagram-looter2.md](instagram-looter2.md) | 30 | **Real API calls** на Basic-плане 2026-04-28 (provider не положил ни одного Example Response в playground) |
| [tiktok-api23.md](tiktok-api23.md) | 56 | 41 playground + 15 real-call edge cases (subscription disabled, 204, status_code errors) |
| [yt-api.md](yt-api.md) | 35 | 31 playground + 4 real-call (subtitles, updated_metadata, post/comments) |
| [threads-api4.md](threads-api4.md) | 12 | 11 playground + 1 real-call edge (GraphQL execution error) |
| [telegram-channel.md](telegram-channel.md) | 2 | Real API calls (минимальный коннектор) |
| **Итого** | **135** | Все 135 эндпоинтов имеют верифицированную форму ответа |

## Что значит «verified»

Каждое поле в JSON-блоках этих файлов либо:

- **наблюдалось живым API-вызовом** на боевом ключе с подпиской Basic, ИЛИ
- **взято из RapidAPI Playground** «Example Response» — это authoritative-данные провайдера (его ответ при тестировании в их же UI).

Длинные подписанные CDN-URL замаскированы как `<url>`, base64-токены/request_id → `<x>`, длинные пользовательские строки (signatures, descriptions) → `<str>` чтобы не загромождать reference.

## Как пользоваться

### Просто проверить поле

```bash
# В каком эндпоинте есть поле "follower_count"?
grep -l "follower_count" connectors/_responses/*.md

# Какие top-level ключи возвращает /api/user/info?
grep -A 30 "/api/user/info" connectors/_responses/tiktok-api23.md | head -40
```

### Из ИИ-агента

Подгружай эти файлы вместе со SKILL.md и нужной карточкой коннектора. Если сомневаешься в имени поля — открой соответствующий `_responses/<api>.md` и сверь.

## Edge cases — отдельная ценность

В каждом файле есть секция «Edge cases» с пойманными нестандартными ответами:

- TikTok: 401 disabled subscription / 204 No Content / status_code != 0 (10011, 4, 3002060, 40000)
- Instagram: behaviour /music на пустых данных, привязка media_id-форматов
- Threads: GraphQL execution-error при невалидных post_id
- Telegram: 404 / 403 / 429

Эти кейсы критически важны для production-кода — без них парсер падает на первом же edge-case.
