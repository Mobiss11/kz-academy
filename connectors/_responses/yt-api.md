# YT-API (ytjar) — verified response shapes

> ✅ **Источник:** все 35 эндпоинтов покрыты. **31 эндпоинт** имеет Example Response в RapidAPI Playground (захвачен в основной карточке `connectors/yt-api.md`). **4 эндпоинта** были без playground-примера и прозвонены реально 2026-04-28 — их формы ниже.
>
> Длинные подписанные CDN-URL замаскированы как `<url>`. Долгие токены → `<x>`.

---

## Реально-verified эндпоинты (4)

### `GET /subtitle?url=<vtt_or_srt_url>` → 200

Возвращает **plain text в формате SRT** (НЕ JSON). Content-Type: text/plain.

```
1
00:00:01,360 --> 00:00:03,040
[♪♪♪]

2
00:00:18,640 --> 00:00:21,880
♪ We're no strangers to love ♪

3
00:00:22,640 --> 00:00:26,960
♪ You know the rules
and so do I ♪
```

Опционально:
- `targetLang` — переводит на указанный язык (en, ru, es, …) сохраняя SRT-формат.
- `format` — переключение srt/vtt/text.

### `GET /subtitles?id=<videoId>` → 200

JSON со списком доступных субтитров. Каждый элемент — кандидат на скачивание через `/subtitle`.

```jsonc
{
  "subtitles": [
    {
      "languageCode": "en",
      "languageName": "English",
      "url": "<vtt_url>",      // → передавай в /subtitle?url=...
      "isTranslatable": true   // можно ли через targetLang перевести
    }
    /* +N more languages */
  ]
}
```

### `GET /updated_metadata?id=<videoId>` → 200

Облегчённый эндпоинт для polling счётчиков. **Намного дешевле** чем `/video/info`.

```jsonc
{
  "id": "dQw4w9WgXcQ",
  "viewCountText": "1,766,811,412 views",
  "viewCount": "1766811412",       // ← integer-как-строка, парси через int()
  "likeCountText": "18M",
  "likeCount": 18983304            // ← integer
}
```

> ⚠️ Multi-id режим (`id=A,B,C`) расширяет ответ в массив. Проверяй обе формы — иногда возвращается `[{...}, {...}]` вместо одного объекта.

### `GET /post/comments?id=<post_id>` → 200 + retry-marker

Provider использует ретрай на своей стороне. На первом вызове часто возвращает:

```jsonc
{ "error": "Retry", "code": "403" }
```

Это НЕ ошибка, а сигнал «попробуй ещё раз». Делай retry с экспоненциальной паузой (2-3 повтора обычно достаточно). При успехе:

```jsonc
{
  "comments": [
    {
      "commentId": "<id>",
      "authorChannelId": "<channel_id>",
      "authorText": "...",
      "authorThumbnail": [ { "url": "<url>", "width": 32, "height": 32 } ],
      "textDisplay": "...",
      "textOriginal": "...",
      "publishedTimeText": "1 day ago",
      "likeCount": 12,
      "replyCount": 3,
      "isHearted": false,
      "isPinned": false
    }
  ],
  "continuation": "<cursor>"
}
```

---

## Playground-verified эндпоинты (31)

Полные JSON-примеры этих эндпоинтов лежат в основной карточке [`connectors/yt-api.md`](../yt-api.md), захваченные из RapidAPI Playground (Example Response provider'а). Группы:

- **Channel** (`/channel/about`, `/channel/home`, `/channel/videos`, `/channel/shorts`, `/channel/playlists`, `/channel/community`, `/channel/liveStreams`, `/channel/details`)
- **Video** (`/video/info`, `/related`, `/comments`, `/replies`)
- **Playlist** (`/playlist/info`, `/playlist/videos`)
- **Search** (`/search`)
- **Trending** (`/trending`, `/trending/regions`)
- **Post / Community** (`/post/info`)
- **Hashtag** (`/hashtag`)
- **Music** (`/music/charts`, `/music/genre`, `/music/mood`)
- ...

Если нужно проверить конкретное поле без открытия большой карточки — запусти запрос на Basic-плане (500 req/мес, $0).
