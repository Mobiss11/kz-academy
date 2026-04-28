# Мониторинг авторов — методология

> 🎯 **Цель:** правильно собирать данные об авторах и их видео, чтобы детектор виральности (см. [viral-detection.md](viral-detection.md)) работал стабильно и не сжигал квоту.

## Что мы мониторим

Две сущности:

1. **Профиль автора** — медленно меняется (followers, biography, avatar).
2. **Лента видео** — быстро меняется (просмотры, лайки, новые посты).

Опрашивать их с разной частотой.

## Расписание опроса

| Тип | Частота | Платформа | Эндпоинт |
|---|---|---|---|
| Профиль автора | **раз в сутки** | Instagram | `/profile2` |
| Профиль автора | раз в сутки | YouTube | `/channel/about` |
| Профиль автора | раз в сутки | TikTok | `/api/user/info` |
| Профиль автора | раз в сутки | Threads | `/api/user/info` |
| Лента видео | **каждый час** | Instagram | `/user-feeds2` |
| Лента видео | каждый час | YouTube | `/channel/videos` |
| Лента видео | каждый час | TikTok | `/api/user/posts` |
| Лента видео | каждый час | Threads | `/api/user/posts` |
| Аватар | **разово при ingest** | все | через профильный эндпоинт |

> 💡 **Не опрашивай профиль каждый час** — это сжигает квоту, а данные меняются раз в сутки максимум. Только лента видео — горячая.

## Что записывать

### При обновлении профиля

```yaml
authors:
  - id: 12345
    platform: instagram
    external_id: "1234567890"   # platform user_id
    username: "zuck"
    full_name: "Mark Zuckerberg"
    avatar_url: "..."
    followers: 14_500_000
    posts_count: 2_345
    is_verified: true
    last_profile_update: 2026-04-28T03:00:00Z
    is_active: true              # для автоматического опроса
    cache_full_response: <JSON>  # полный ответ API для UI
```

> 💡 Кэшируй полный JSON-ответ профиля — UI часто показывает биографию, ссылки, теги. Без этого придётся делать дополнительный запрос.

### При обновлении ленты видео

```yaml
videos:
  - id: 67890                       # internal
    platform_video_id: "Cv1AbcXXXX" # platform-specific (shortcode/videoId)
    author_id: 12345
    platform: instagram
    media_type: 1                   # 1=photo, 2=video, 8=carousel
    caption: "..."
    posted_at: 2026-04-27T15:30:00Z
    first_seen_at: 2026-04-27T16:00:00Z
    last_checked_at: 2026-04-28T10:00:00Z
    duration_seconds: 47
    views_history:
      - {ts: "2026-04-27T16:00", v: 12_000}
      - {ts: "2026-04-27T17:00", v: 35_000}
      - {ts: "2026-04-27T18:00", v: 89_000}
      - ...
    likes_count: 1_234
    comments_count: 56
    is_pinned: false
    is_deleted: false
```

## Ingest нового автора

Когда юзер добавляет нового автора:

```
1. Парсим URL → определяем платформу.
2. Конвертируем (handle/URL → внутренний ID):
   - Instagram: /id?username=X → user_id
   - TikTok:    /api/user/info?uniqueId=X → secUid
   - YouTube:   /resolve?url=X → browseId
   - Threads:   /api/user/info?username=X → pk

3. Вызываем профильный эндпоинт → создаём строку в `authors`.

4. Вызываем ленту видео (count=30-50) → создаём строки в `videos`.

5. Опционально:
   - Скачиваем аватар → S3 (фоновая задача).
   - Запускаем мониторинг = подписываем на регулярный опрос.
```

> 💡 **Первый ingest = до 100 видео** для стартового baseline. Последующие опросы — только новые/изменившиеся.

## Поиск новых авторов автоматически

Ручной ingest по URL — основной путь. Но можно автоматизировать:

### Через Related Profiles (Instagram, TikTok)

- Instagram: [`/related-profiles`](../../connectors/instagram-looter2.md#-user-insights-12) → 30-50 похожих.
- TikTok: косвенно через автора виральных видео из той же ниши.

```
Стартовый автор → /related-profiles → 30 похожих →
для каждого: профиль → следим, набирает ли скорость → если да, добавляем в мониторинг.
```

### Через Hashtag/Search

- Поиск виральных видео по нише через `/search?query=X` или `/hashtag` или `/trending`.
- У автора виральных постов из ниши — его в мониторинг.

### Через Trending/Hype-ленту

- YouTube: `/trending`.
- TikTok: `/api/trending/creator` (платная группа Ads/Trending).
- Authors из топа — кандидаты в мониторинг.

> 💡 Автоматический discovery — мощно, но **взрывает квоту**. Включай только когда у тебя > 1000 авторов и нужен поток новых.

## Сколько авторов реально мониторить

Считается по квоте API. Грубо:

- Каждый автор = 1 запрос профиля/сутки + 24 запроса ленты/сутки = **25 запросов/сутки/автор**.
- 30 дней = **750 запросов/мес/автор**.

| Коннектор | План | Бюджет в месяц | Авторов max |
|---|---|---|---|
| Instagram (looter2) | Pro $9.99 | 15 000 req | **20 авторов** |
| Instagram (looter2) | Ultra $27.90 | 75 000 req | **100 авторов** |
| Instagram (looter2) | Mega $75.90 | 250 000 req | **333 автора** |
| TikTok (api23) | Pro $9.99 | 200 000 req | **266 авторов** |
| TikTok (api23) | Ultra $49.99 | 1 000 000 req | **1 333 автора** |
| YouTube (yt-api) | Pro $51 | 1 770 500 req | **2 360 авторов** |

> 💡 TikTok и YouTube дешевле в пересчёте на автора. Instagram looter2 — самый дорогой по этой методике.

## Оптимизации квоты

### 1. Не опрашивай неактивных авторов

Если автор не постит > 30 дней — снижай частоту лент до раз в сутки или ставь на паузу.

```python
if author.last_post_at < now - 30_days:
    monitoring_frequency = "daily"  # вместо hourly
```

Реальная экономия: 30-50% квоты на активных vs неактивных.

### 2. Не опрашивай ночью

Контент-волны идут в активные часы аудитории. Опрос ночью = меньше шансов поймать новое.

```python
def should_check(author, hour_utc):
    audience_hours = {  # часы пик по часовому поясу аудитории
        "RU": (8, 24),
        "US": (12, 26),  # +4 для перекрытия следующего дня
        "EU": (10, 24),
    }
    start, end = audience_hours[author.audience_country]
    return start <= hour_utc <= end
```

Экономия: ~30% (опрос только в 16 из 24 часов).

### 3. Кэш профилей

Профиль обновляется раз в сутки. Все остальные обращения — из кэша:

```python
@cache(ttl=86400)  # 24 часа
def get_profile(author_id):
    return api_call(...)
```

### 4. `fields` параметр для экономии bandwidth

В Instagram Looter2 везде поддерживается `fields=`:

```
GET /user-feeds2?id=X&count=30&fields=items.id,items.like_count,items.taken_at,items.caption.text
```

Экономия: 70-90% размера ответа = меньше bandwidth-счёт.

### 5. Batch-эндпоинты

YT-API: `/video/info?id=A,B,C` (multi-id) — 1 запрос вместо 3 (квота +1 за extra, но HTTP меньше).
TikTok api23: `/updated_metadata?id=A,B,C` для polling-а счётчиков.

### 6. Кэш на дублирующиеся запросы внутри часа

В `examples/common.py` уже встроен `requests_cache` на 3600 секунд. Не отключай.

## Платформенная специфика

### Instagram

- **secUid не используется** (это TikTok). Использует `user_id` (числовая строка).
- **Карусели**: `media_type=8`, медиа лежит в `carousel_media[]`.
- **Stories**: отдельный эндпоинт, обычно мониторим только posts/reels.

### TikTok

- **3 разных ID**: `uniqueId` (handle), `userId` (число), `secUid` (длинная подпись).
- Видео-эндпоинты принимают **secUid** — конвертируй один раз через `/api/user/info`.
- **`secUid` иногда меняется** при пересохранении кэша TikTok — если запросы стабильно пустые, обновляй secUid.

### YouTube

- **Канал ID** — `UC...` (24 символа). Получай через `/resolve` если на входе handle.
- **Long-form vs Shorts** — разная логика виральности (см. viral-detection.md).
- **Streams и Premieres** — отдельный канал данных через `/channel/liveStreams`.

### Threads

- Самый молодой коннектор, схема может меняться часто.
- **`pk`** — primary key пользователя.
- **end_cursor** — курсор пагинации (не `cursor`/`max_id`).

## Расписание (cron-style)

```cron
# Профили — раз в сутки в 03:00 UTC
0 3 * * * /usr/bin/python -m monitoring.update_profiles

# Ленты — каждый час
0 * * * * /usr/bin/python -m monitoring.update_videos

# Анализ виральности — каждый час, после ленты
15 * * * * /usr/bin/python -m monitoring.analyze_viral

# Очистка — раз в сутки
0 4 * * * /usr/bin/python -m monitoring.cleanup
```

> 💡 **Не запускай всё в `0 * * * *`** — пиковая нагрузка убьёт rate-limit. Разнеси:
> - Лента: на :00.
> - Анализ: на :15.
> - Профили: только в :03.
> - Cleanup: только в :04.

## Дальше

- [viral-detection.md](viral-detection.md) — что делать с собранными данными.
- [cost-modeling.md](cost-modeling.md) — точный бюджет под твоё кол-во авторов.
- Карточки коннекторов с конкретными эндпоинтами и параметрами:
  - [instagram-looter2.md](../../connectors/instagram-looter2.md)
  - [tiktok-api23.md](../../connectors/tiktok-api23.md)
  - [yt-api.md](../../connectors/yt-api.md)
  - [threads-api4.md](../../connectors/threads-api4.md)
