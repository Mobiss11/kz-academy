# YT-API (ytjar)

**Провайдер:** ytjar
**Страница:** https://rapidapi.com/ytjar/api/yt-api
**Subscribe (Pricing):** https://rapidapi.com/ytjar/api/yt-api/pricing
**Base URL:** `https://yt-api.p.rapidapi.com`
**Host-заголовок:** `yt-api.p.rapidapi.com`

> ⚠️ **Перед первым запросом — оформи подписку** на нужный план на странице Pricing (см. ссылку выше). Без подписки любой вызов вернёт `403 You are not subscribed to this API`. Free-план называется **Basic**, оформляется в один клик, но **требует привязанную банковскую карту**. Подробности в [docs/getting-started.md](../docs/getting-started.md).

All-in-one API для YouTube. **35 эндпоинтов** (32 GET + 3 POST). Покрывает: видео, шортсы, каналы, поиск, плейлисты, тренды, hype-ленту, главную, комментарии, посты сообщества, хэштеги, разрешение URL, субтитры (с переводом), транскрипты, скриншоты, автодополнение запросов, скачивание/стрим.

> ✅ **Источник схемы.** Эта карточка собрана автоматически из RapidAPI Playground (params + Example Responses всех 35 эндпоинтов). Тарифы и формат 401 ошибки — реальные, проверены живым вызовом. Названия полей в JSON-примерах ниже — настоящие, из ответов провайдера. Длинные значения (continuation tokens, URL и т.д.) заменены на `"..."`.
>
> Данные могут устареть — провайдер меняет схемы без анонсов. Перед прод-кодом сверяйся с playground.

## Авторизация

Стандартная пара заголовков RapidAPI (см. [SKILL.md](../SKILL.md)):

```
X-RapidAPI-Key: <ключ>
X-RapidAPI-Host: yt-api.p.rapidapi.com
```

**Формат ошибки 401** (verified — реальный ответ от RapidAPI с битым ключом):

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{"message": "Invalid API key. Go to https://docs.rapidapi.com/docs/keys for more info."}
```

## Общие заголовки запроса

| Заголовок | Обяз. | Назначение |
|---|---|---|
| `X-RapidAPI-Key` | ✅ | твой ключ |
| `X-RapidAPI-Host` | ✅ | `yt-api.p.rapidapi.com` |
| `Content-Type: application/json` | – | для POST-эндпоинтов |
| `X-TOKEN: <continuation>` | – | альтернатива query-параметру `token`. Решает 414 URI Too Long |
| `X-CACHEBYPASS: 1` | – | принудительно идти за свежими данными. **+1 квота** |

## Общие правила

### Структура ответов

- Все ответы — `application/json`.
- Списочные эндпоинты возвращают `data: [...]` + `continuation` (continuation token). Если поле отсутствует/пустое — страниц больше нет.
- Большинство `/channel/*` эндпоинтов имеют форму `{meta: {<channel about>}, data: [...], continuation}` — `meta` это всегда полная инфа о канале (как `/channel/about`).
- В смешанных лентах элементы имеют `type` (`video`, `shorts`, `channel`, `playlist`, `video_listing`, `shorts_listing`, `post`...). **Всегда фильтруй по `type`**.
- ID видео — 11 символов, ID канала — `UC...` (24 симв.), ID плейлиста — `PL...`/`UU...`/`RD...`/`OL...`.
- Многие ответы возвращают **HTTP 200** с ошибкой в теле (`{"error": "..."}` или `{"status": "fail", ...}`). Всегда проверяй тело перед использованием.

### Квота (verified из playground)

База — 1 единица за запрос. **+1 квота** дополнительно за:
- `forUsername` (handle вместо channelId)
- `extend=1` или `extend=2` в `/video/info`
- `cm=1` в `/dl`
- `local=1` (локализация)
- Заголовок `X-CACHEBYPASS: 1`
- Multi-id режим в `/video/info`/`/updated_metadata`: +1 за каждый дополнительный id
- Не указанный `cgeo` в `/dl`: может стоить +1 и привести к 403

### Универсальные query-параметры

| Параметр | Применимо | Описание |
|---|---|---|
| `geo` | почти везде | ISO-3166 код страны (`US` default, `GB`, `CA`, `IN`, `RU`...) |
| `lang` | почти везде | язык (`en`, `ru`, `hi`, `gb`...) |
| `fields` | везде | селектор полей для экономии трафика (синтаксис как у YouTube Data API) |
| `token` | списки | continuation token из предыдущего ответа |
| `local=1` | где доступно | локализованные результаты, +1 квота |

---

## Поиск, навигация, ленты

### `GET /search` — универсальный поиск

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `query` | string | ✅ | поисковый запрос |
| `token` | string | – | continuation token (или `X-TOKEN`) |
| `type` | enum | – | `video`, `channel`, `playlist`, `movie`, `show`, `shorts` |
| `duration` | enum | – | `under3min`, `3to20min`, `over20min`. Старые `short`/`medium`/`long` тоже работают |
| `features` | string | – | `HD`, `subtitles`, `CCommons`, `3D`, `Live`, `Purchased`, `4K`, `360`, `Location`, `HDR`, `VR180` (через `,`) |
| `upload_date` | enum | – | `hour`, `today`, `week`, `month`, `year` |
| `sort_by` | enum | – | `relevance` (default), `popularity`, `rating`, `date`, `views` |
| `geo` | string | – | страна |
| `lang` | string | – | язык |
| `local` | number | – | `1` для локализации, +1 квота |
| `fields` | string | – | селектор полей |

**Пример ответа** (verified — 5 top-level keys, 12 ключей на видео):

```json
{
  "estimatedResults": "171053689",
  "continuation": "...",
  "data": [
    {
      "type": "video",
      "videoId": "2oRlBmwKzy4",
      "title": "...",
      "channelTitle": "The Kiffness",
      "channelId": "UC...",
      "channelThumbnail": [{"url": "...", "width": 68, "height": 68}],
      "description": "...",
      "viewCount": "10548405",
      "publishedTimeText": "1 year ago",
      "lengthText": "1:48",
      "thumbnail": [
        {"url": "...", "width": 360, "height": 202},
        {"url": "...", "width": 720, "height": 404}
      ],
      "richThumbnail": [{"url": "...", "width": 320, "height": 180}]
    }
  ]
}
```

### `GET /home` — главная лента (с фильтрами по категориям)

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `token` | string | – | continuation |
| `geo` | string | – | страна |
| `lang` | string | – | язык |
| `fields` | string | – | селектор полей |

**Пример ответа** (verified — 4 top-level keys, фильтры — отдельный массив со своими токенами):

```json
{
  "filters": [
    {"filter": "All"},
    {"filter": "Music", "continuation": "..."},
    {"filter": "Gaming", "continuation": "..."},
    {"filter": "Live", "continuation": "..."}
  ],
  "data": [
    {
      "type": "shorts_listing",
      "title": "Shorts",
      "subtitle": null,
      "data": [
        {
          "type": "shorts",
          "videoId": "...",
          "title": "...",
          "viewCountText": "74M views",
          "thumbnail": [{"url": "...", "width": 360, "height": 720}],
          "params": "...",
          "playerParams": "8AEBoAMByAMkuAQF",
          "sequenceParams": "..."
        }
      ]
    }
  ]
}
```

### `GET /trending` — тренды (сгруппированы по темам)

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `geo` | string | ✅ | страна |
| `type` | enum | – | `now` (default), `music`, `games`, `movies` |
| `lang` | string | – | язык |
| `fields` | string | – | селектор полей |

**Пример ответа** (verified — данные сгруппированы как `video_listing` по темам):

```json
{
  "data": [
    {
      "type": "video_listing",
      "title": "Daniela Flores",
      "data": [
        {
          "type": "video",
          "videoId": "FHGzy9jezWk",
          "title": "...",
          "viewCount": "7158969",
          "publishedText": "1 month ago",
          "lengthText": "SHORTS",
          "thumbnail": [{"url": "...", "width": 210, "height": 118}]
        }
      ]
    }
  ],
  "continuation": "..."
}
```

### `GET /hype` — Hype-лента

Параметры: `token`, `geo`, `lang`, `fields` — все опциональные. Возвращает ленту видео, продвигаемых сообществом.

### `GET /hashtag` — посты по хэштегу

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `tag` | string | ✅ | хэштег без `#` |
| `type` | enum | – | `all` (default), `shorts` |
| `params` | string | – | внутренний param (из ответа) |
| `token` | string | – | continuation |
| `geo` | string | – | страна |
| `lang` | string | – | язык |
| `fields` | string | – | селектор полей |

**Пример ответа** (verified — 4 top-level keys):

```json
{
  "meta": {
    "hashtag": "#viral",
    "hashtagInfoText": "110M videos • 10M channels"
  },
  "continuation": "...",
  "data": [
    {
      "videoId": "fc5Sn-4dTJY",
      "title": "...",
      "channelTitle": "DontStopMeowing",
      "channelId": "UC...",
      "description": "",
      "viewCount": "102808",
      "publishedText": "23 hours ago",
      "lengthText": "0:47",
      "thumbnail": [{"url": "...", "width": 168, "height": 94}],
      "richThumbnail": null,
      "channelThumbnail": [{"url": "...", "width": 68, "height": 68}]
    }
  ]
}
```

### `GET /resolve` — handle/URL → ID

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `url` | string | ✅ | YouTube URL: `youtu.be/...`, `youtube.com/@handle`, `youtube.com/channel/<id>`, `youtube.com/watch?v=...` |

**Пример ответа** (verified — 4 keys):

```json
{
  "webPageType": "WEB_PAGE_TYPE_CHANNEL",
  "isVanityUrl": true,
  "browseId": "UCuAXFkgsw1L7xaCfnd5JJOw",
  "params": "..."
}
```

`webPageType` сообщает что это: `WEB_PAGE_TYPE_CHANNEL`, `WEB_PAGE_TYPE_VIDEO`, `WEB_PAGE_TYPE_PLAYLIST`. `browseId` — каноничный ID для дальнейших вызовов.

### `GET /suggest_queries` — автодополнение поиска

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `query` | string | ✅ | префикс |
| `geo` | string | – | страна |
| `lang` | string | – | язык |

---

## Видео

### `GET /video/info` — метаданные (31 top-level keys без extend, больше с `extend=1`)

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `id` | string | ✅ | videoId. Multi-id через `,` (+1 квота за каждый extra) |
| `extend` | enum | – | `1` — likeCount, commentCount, subscriberCountText, relatedVideos, channelBadges, chapters, merchandise, extraMeta, videoAttribution (не работает для multi-id). `2` — likeCount, commentCount, channelHandle. **+1 квота** |
| `geo` | string | – | страна |
| `lang` | string | – | язык |
| `fields` | string | – | селектор полей |

**Пример ответа** (verified — основные top-level поля):

```json
{
  "id": "dQw4w9WgXcQ",
  "title": "...",
  "lengthSeconds": "212",
  "keywords": ["..."],
  "channelTitle": "...",
  "channelId": "UC...",
  "description": "...",
  "thumbnail": [
    {"url": "...", "width": 168, "height": 94},
    {"url": "...", "width": 1920, "height": 1080}
  ],
  "allowRatings": true,
  "viewCount": "1500000000",
  "isPrivate": false,
  "isUnpluggedCorpus": false,
  "isLiveContent": false,
  "isCrawlable": true,
  "isFamilySafe": true,
  "availableCountries": ["AD", "AE", "..."],
  "uploadDate": "...",
  "publishDate": "...",
  "category": "Music"
}
```

С `extend=1` добавляются: `likeCount`, `commentCount`, `subscriberCountText`, `channelHandle`, `chapters`, `merchandise`, `relatedVideos`, `channelBadges`, `extraMeta`, `videoAttribution`.

### `GET /dl` — стрим/скачивание (19 top-level keys)

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `id` | string | ✅ | videoId или shortsId |
| `cgeo` | string | ✅ | ISO-страна потребителя ссылки. **Без неё — 403 и +1 квота** |
| `lang` | string | – | язык аудио |
| `cm` | string | – | `1` — детектить music. Эксперимент. +1 квота |
| `fields` | string | – | селектор полей |

**Пример ответа** (verified):

```json
{
  "status": "OK",
  "id": "arj7oStGLkU",
  "title": "Tim Urban: Inside the mind of a master procrastinator | TED",
  "lengthSeconds": "844",
  "keywords": ["TED Talk", "Tim Urban", "procrastination", "..."],
  "channelTitle": "TED",
  "channelId": "UC...",
  "description": "...",
  "thumbnail": [
    {"url": "...", "width": 120, "height": 90},
    {"url": "...", "width": 640, "height": 480}
  ],
  "allowRatings": true,
  "viewCount": "...",
  "isPrivate": false,
  "isUnpluggedCorpus": false,
  "isLiveContent": false,
  "storyboards": [
    {
      "width": "...", "height": "...", "thumbsCount": "...",
      "columns": "...", "rows": "...", "interval": "...",
      "storyboardCount": 1,
      "url": ["..."]
    }
  ],
  "captions": {
    "captionTracks": [
      {"baseUrl": "...", "name": "...", "vssId": "...", "languageCode": "en"}
    ],
    "translationLanguages": [
      {"languageCode": "es", "languageName": "Spanish"}
    ]
  },
  "formats": [
    {
      "itag": 18,
      "mimeType": "video/mp4; codecs=\"avc1.42001E, mp4a.40.2\"",
      "qualityLabel": "360p",
      "url": "https://rr1---sn-...googlevideo.com/...",
      "contentLength": "...",
      "bitrate": 568000,
      "width": 640,
      "height": 360,
      "fps": 25
    }
  ],
  "adaptiveFormats": [
    {"itag": 137, "mimeType": "video/mp4", "qualityLabel": "1080p", "url": "...", "bitrate": 4000000, "width": 1920, "height": 1080, "fps": 30},
    {"itag": 140, "mimeType": "audio/mp4", "url": "...", "bitrate": 128000, "audioSampleRate": "44100"}
  ],
  "expiresInSeconds": "21540"
}
```

⚠️ Ссылки `url` подписаны и **истекают через `expiresInSeconds`** (~6 ч). Не кэшируй и не публикуй.

### `GET /related` — похожие видео

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `id` | string | ✅ | videoId |
| `token` | string | – | пагинация |
| `geo` | string | – | страна |
| `lang` | string | – | язык |
| `fields` | string | – | селектор полей |

**Пример ответа** (verified):

```json
{
  "continuation": "...",
  "data": [
    {
      "type": "video",
      "videoId": "...",
      "title": "...",
      "lengthText": "3:14",
      "viewCount": "...",
      "publishedTimeText": "...",
      "thumbnail": [{"url": "...", "width": 168, "height": 94}],
      "channelTitle": "...",
      "channelId": "..."
    }
  ]
}
```

### `GET /subtitles` — список субтитров и raw-выгрузка

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `id` | string | ✅ | videoId |
| `format` | enum | – | `json3` (mime: json), `srv1` (xml, default), `srv2`, `srv3`, `ttml`, `vtt`, `srt` |
| `lang` | string | – | код языка. **Если не указан — вернётся список доступных** (а не сами субтитры) |

> Provider не положил Example Response для этого эндпоинта в playground. По смыслу: без `lang` отдаёт `{captionTracks: [{baseUrl, name, languageCode}], translationLanguages: [{languageCode, languageName}]}` (тот же формат, что в `/video/info` или `/dl`). С `lang` — тело субтитра в указанном `format`.

### `GET /subtitle` — конвертация/перевод/скачивание (singular!)

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `url` | string | ✅ | URL субтитра из ответа `/subtitles` или `/video/info` |
| `format` | enum | – | то же |
| `targetLang` | string | – | перевести на язык. Допустимые коды — в `translationLanguages` (`es`, `zh-Hans`, `co`, `hi`...) |

> Тело ответа — сам файл субтитра в `format` (текст или JSON). Provider не запрограммировал Example Response.

### `GET /get_transcript` — транскрипт видео

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `id` | string | ✅ | videoId |
| `params` | string | – | внутренний param для альтернативных версий |
| `lang` | string | – | язык |

**Пример ответа** (verified — 4 ключа top-level, репликами):

```json
{
  "id": "...",
  "transcript": [
    {"startMs": "0", "endMs": "2500", "startTime": "0:00", "text": "Never gonna give you up"},
    {"startMs": "2500", "endMs": "4700", "startTime": "0:02", "text": "Never gonna let you down"}
  ]
}
```

### `GET /updated_metadata` — облегчённое обновление счётчиков

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `id` | string | ✅ | videoId или multi-id через `,` (+1 квота за extra) |

> Provider не положил Example Response. Назначение — polling видеосчётчиков (viewCount, likeCount, commentCount) без полного `/video/info`.

### `GET /video/screenshot` — кадр видео

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `id` | string | ✅ | videoId |
| `timeStamp` | string | ✅ | `HH:MM:SS` |

**Пример ответа** (verified — 3 ключа, ссылки на 3 разрешения):

```json
{
  "link": {
    "720p": "https://...",
    "480p": "https://...",
    "360p": "https://..."
  },
  "status": "OK",
  "msg": "..."
}
```

---

## Shorts

### `GET /shorts/info` — метаданные шортса (19 top-level keys)

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `id` | string | ✅ | shortsId или строка `WHATTOWATCH` для рекомендуемых |
| `params` | string | – | shorts video param |
| `extend` | string | – | `1` — расширенный ответ. +1 квота |
| `geo` | string | – | страна |
| `lang` | string | – | язык |
| `fields` | string | – | селектор полей |

**Пример ответа** (verified):

```json
{
  "videoId": "...",
  "likeStatus": "...",
  "likeCount": 4286,
  "likeCountText": "4.2K",
  "likesAllowed": true,
  "title": "...",
  "titleWithNavDetails": [
    {"text": "..."},
    {"text": "...", "url": "...", "bold": true}
  ],
  "publishedTimeText": "...",
  "channelId": "UC...",
  "channelHandle": "@...",
  "channelNavDetails": {"params": "..."},
  "channelThumbnail": [{"url": "...", "width": 48, "height": 48}],
  "commentCount": "...",
  "soundAttribution": {
    "params": "...",
    "thumbnail": [{"url": "...", "width": 1425, "height": 1425}],
    "...": "..."
  },
  "url": "...",
  "params": "...",
  "channelTitle": "...",
  "viewCount": "...",
  "publishDate": "...",
  "description": "...",
  "descriptionWithNavDetails": [{"text": "..."}, {"text": "...", "url": "..."}]
}
```

В ответе есть `sequenceContinuation` (для `/shorts/sequence`, при `id=WHATTOWATCH`).

### `GET /shorts/sequence` — лента шортсов

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `params` | string | – | `sequenceContinuation` из `/shorts/info` или `continuation` из предыдущего ответа |
| `id` | string | – | shortsId. **Не рекомендуется** |
| `geo` | string | – | страна |
| `lang` | string | – | язык |
| `fields` | string | – | селектор полей |

**Пример ответа** (verified):

```json
{
  "continuation": "...",
  "data": [
    {
      "type": "shorts",
      "videoId": "...",
      "thumbnail": [{"url": "...", "width": 720, "height": 900, "isOriginalAspectRatio": true}],
      "title": "...",
      "publishedTimeText": "...",
      "channelHandle": "@...",
      "channelId": "UC...",
      "channelNavDetails": {"...": "..."}
    }
  ]
}
```

### `GET /shorts/soundAttribution` — все шортсы с конкретным звуком

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `params` | string | – | значение `soundAttribution.params` из `/shorts/info` |
| `id` | string | – | альтернатива: shortsId |
| `token` | string | – | continuation |
| `geo` | string | – | страна |
| `lang` | string | – | язык |
| `fields` | string | – | селектор полей |

Возвращает список шортсов в формате как `/shorts/sequence`.

---

## Каналы

> **Универсальное наблюдение:** все списочные `/channel/*` эндпоинты возвращают форму `{meta: {<полная информация о канале>}, data: [...], continuation, ...}`. То есть `meta` всегда содержит то же, что отдаёт `/channel/about` (15-21 keys), плюс data со специфичным контентом (видео/шортсы/плейлисты/посты/etc.).

Все эндпоинты канала принимают `id` (`UC...`). Альтернативно — `forUsername` (handle/legacy username), но это **+1 квота**.

### `GET /channel/about` — основные данные канала (21 top-level keys)

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `id` | string | – | channelId (нужен `id` или `forUsername`) |
| `forUsername` | string | – | handle (+1 квота) |
| `geo` | string | – | страна |
| `lang` | string | – | язык |
| `fields` | string | – | селектор полей |

**Пример ответа** (verified, top-level keys):

```json
{
  "channelId": "UC...",
  "title": "...",
  "description": "...",
  "channelHandle": "@...",
  "banner": [
    {"url": "...", "width": 1060, "height": 175},
    {"url": "...", "width": 2560, "height": 424}
  ],
  "tvBanner": [{"url": "...", "width": 320, "height": 180}],
  "avatar": [{"url": "...", "width": 88, "height": 88}],
  "subscriberCount": "...",
  "subscriberCountText": "...",
  "videoCount": "...",
  "viewCount": "...",
  "joinedDate": "...",
  "country": "...",
  "links": [{"title": "...", "url": "..."}],
  "tags": ["..."],
  "isVerified": true
}
```

### `GET /channel/home`, `/channel/videos`, `/channel/shorts`, `/channel/liveStreams`, `/channel/playlists`, `/channel/community`, `/channel/channels`, `/channel/search`, `/channel/store`

Все возвращают одну и ту же форму:

```json
{
  "meta": { /* всё, что в /channel/about */ },
  "data": [ /* контент: видео, шортсы, плейлисты, посты, ... в зависимости от эндпоинта */ ],
  "continuation": "..."
}
```

#### Параметры

| Эндпоинт | Параметры | Особенности |
|---|---|---|
| `/channel/home` | `id` или `forUsername`, `token`, `params`, `geo`, `lang`, `fields` | секции главной |
| `/channel/videos` | `id` или `forUsername`, `sort_by` (`newest` default, `popular`, `oldest`), `token`, `geo`, `lang`, `local`, `fields` | |
| `/channel/shorts` | те же | `sort_by`: `newest` (default), `oldest`, `popular` |
| `/channel/liveStreams` | те же + `local` | стримы (текущие, прошедшие, запланированные). **camelCase в URL** |
| `/channel/playlists` | `id` ✅, `forUsername`, `sort_by` (`date_added` default, `last_video_added`), `token`, `geo`, `lang`, `fields` | |
| `/channel/community` | `id` ✅, `token`, `geo`, `lang`, `fields` | посты сообщества |
| `/channel/channels` | `id` или `forUsername`, `token`, `geo`, `lang`, `fields` | Featured Channels |
| `/channel/search` | `id` или `forUsername`, `query` ✅, `token`, `geo`, `lang`, `fields` | поиск внутри канала |
| `/channel/store` | `id` или `forUsername`, `token`, `geo`, `lang`, `fields` | мерч |

### `POST /channel/shorts`, `POST /channel/videos`, `POST /channel/liveStreams`

POST-альтернативы соответствующих GET. Те же поля, но в теле как `multipart/form-data`. Используй когда `token` слишком длинный для query string.

```python
files = {
    "id": (None, "UCuAXFkgsw1L7xaCfnd5JJOw"),
    "sort_by": (None, "newest"),
    "token": (None, "<очень длинный continuation>"),
}
r = requests.post("https://yt-api.p.rapidapi.com/channel/videos", headers=headers, files=files)
```

Поля Body: `id`, `forUsername`, `sort_by`, `token`, `geo`, `lang`, `local`, `fields`. Ответ — той же формы, что у GET-версии.

---

## Комментарии и посты

### `GET /comments` — комментарии к видео или шортсу

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `id` | string | ✅ | videoId **или** shortsId |
| `token` | string | – | continuation **или** `replyToken` для ответов на комментарий |
| `sort_by` | enum | – | `top` (default), `newest` |
| `geo` | string | – | страна |
| `lang` | string | – | язык |
| `fields` | string | – | селектор полей |

**Пример ответа** (verified):

```json
{
  "commentsCount": "1.6K",
  "continuation": "...",
  "data": [
    {
      "commentId": "Ugw...",
      "authorText": "@user123",
      "authorChannelId": "UC...",
      "authorThumbnail": [{"url": "...", "width": 48, "height": 48}],
      "textDisplay": "...",
      "publishedTimeText": "4 years ago",
      "likesCount": "2.1K",
      "replyCount": 20,
      "replyToken": "Eg0KC1Vnd...",
      "isPinned": false
    }
  ]
}
```

> **Ответы на комментарий:** в yt-api нет отдельного `/replies` — вызови тот же `/comments` передавая `replyToken` как `token`.

### `GET /post/info` — данные одного community-поста (11 keys)

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `id` | string | ✅ | postId |
| `channelId` | string | – | channelId автора |
| `geo` | string | – | страна |
| `lang` | string | – | язык |
| `fields` | string | – | селектор полей |

**Пример ответа** (verified):

```json
{
  "type": "post",
  "postId": "Ugk...",
  "authorText": "...",
  "authorChannelId": "UC...",
  "authorThumbnail": [
    {"url": "...", "width": 32, "height": 32},
    {"url": "...", "width": 76, "height": 76}
  ],
  "contentText": "...",
  "publishedTimeText": "...",
  "voteCountText": "...",
  "voteStatus": "...",
  "replyCount": null,
  "attachment": {
    "type": "image",
    "image": [{"url": "...", "width": 288, "height": 288}]
  }
}
```

`attachment.type` бывает: `image`, `video` (с `videoId`), `poll` (с `choices`), `playlist`, и т.д.

### `GET /post/comments` — комментарии к community-посту

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `id` | string | ✅ | postId |
| `channelId` | string | – | channelId автора |
| `sort_by` | enum | – | `top` (default), `newest` |
| `token` | string | – | пагинация |
| `geo` | string | – | страна |
| `lang` | string | – | язык |
| `fields` | string | – | селектор полей |

> Provider не положил Example Response. По смыслу — формат как `/comments`, но для постов сообщества.

---

## Плейлисты

### `GET /playlist` — содержимое плейлиста

| Параметр | Тип | Обяз. | Описание |
|---|---|---|---|
| `id` | string | ✅ | playlistId (`PL...`/`UU...`/`RD...`/`OL...`) |
| `token` | string | – | continuation |
| `geo` | string | – | страна |
| `lang` | string | – | язык |
| `fields` | string | – | селектор полей |

**Пример ответа** (verified — 4 top-level keys):

```json
{
  "meta": {
    "playlistId": "PL...",
    "title": "...",
    "description": "...",
    "thumbnail": "...",
    "videoCount": "200",
    "viewCount": "162531123",
    "lastUpdated": "Updated today",
    "avatar": [
      {"url": "...", "width": 48, "height": 48},
      {"url": "...", "width": 176, "height": 176}
    ],
    "channelTitle": "Redlist - Just Hits",
    "channelId": "UC...",
    "privacy": "PUBLIC"
  },
  "continuation": "...",
  "data": [
    {
      "videoId": "G7KNmW9a75Y",
      "title": "...",
      "index": "1",
      "lengthSeconds": "202",
      "lengthText": "3:22",
      "thumbnail": [
        {"url": "...", "width": 168, "height": 94},
        {"url": "...", "width": 336, "height": 188}
      ],
      "videoOwnerChannelTitle": "Miley Cyrus",
      "videoOwnerChannelId": "UC...",
      "isPlayable": true,
      "videoInfo": "280M views • 1 month ago",
      "viewCountText": "280M views",
      "viewCount": 280000000,
      "publishedTimeText": "1 month ago"
    }
  ]
}
```

---

## Минимальные рабочие примеры

### Универсальный паттерн пагинации

```python
import os
import requests

API_KEY = os.environ["RAPIDAPI_KEY"]
HOST = "yt-api.p.rapidapi.com"
headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": HOST}

def paginate(path, params, max_pages=5):
    token = None
    for _ in range(max_pages):
        if token:
            params = {**params, "token": token}
        r = requests.get(f"https://{HOST}{path}", headers=headers, params=params, timeout=15)
        r.raise_for_status()
        page = r.json()
        if isinstance(page, dict) and (page.get("error") or page.get("status") == "fail"):
            raise RuntimeError(f"yt-api error: {page}")
        for item in page.get("data", []):
            yield item
        token = page.get("continuation") or page.get("token")
        if not token:
            break

for video in paginate("/channel/videos", {"id": "UCuAXFkgsw1L7xaCfnd5JJOw", "sort_by": "newest"}):
    print(video.get("title"), video.get("viewCount"))
```

### Поиск с фильтрами

```python
r = requests.get(
    f"https://{HOST}/search",
    headers=headers,
    params={
        "query": "claude api tutorial",
        "type": "video",
        "duration": "3to20min",
        "upload_date": "month",
        "features": "HD,subtitles",
        "sort_by": "views",
        "lang": "en",
    },
    timeout=15,
)
data = r.json()
for v in data.get("data", []):
    if v.get("type") == "video":
        print(v["title"], "—", v.get("viewCount"), "views")
```

### Handle → channelId → последние видео

```python
resolved = requests.get(
    f"https://{HOST}/resolve",
    headers=headers,
    params={"url": "https://www.youtube.com/@RickAstleyYT"},
    timeout=15,
).json()

assert resolved["webPageType"] == "WEB_PAGE_TYPE_CHANNEL"
channel_id = resolved["browseId"]

videos = requests.get(
    f"https://{HOST}/channel/videos",
    headers=headers,
    params={"id": channel_id, "sort_by": "newest"},
    timeout=15,
).json()

# meta содержит инфу о канале (как /channel/about)
print(videos["meta"]["title"], "—", videos["meta"]["subscriberCountText"])

for v in videos.get("data", [])[:50]:
    print(v.get("title"), v.get("viewCount"))
```

### Видео + транскрипт + LLM-саммари

```python
video_id = "dQw4w9WgXcQ"

info = requests.get(f"https://{HOST}/video/info", headers=headers,
                    params={"id": video_id, "extend": "1"}).json()
transcript = requests.get(f"https://{HOST}/get_transcript", headers=headers,
                          params={"id": video_id}).json()

text = " ".join(seg["text"] for seg in transcript.get("transcript", []))
print(f"Title: {info['title']}")
print(f"Channel: {info['channelTitle']}")
print(f"Views: {info['viewCount']}")
print(f"Likes: {info.get('likeCount')}")  # только при extend=1
print(f"Transcript ({len(text)} chars): {text[:200]}...")
```

### Получение mp4-ссылки

```python
payload = requests.get(
    f"https://{HOST}/dl",
    headers=headers,
    params={"id": "dQw4w9WgXcQ", "cgeo": "US"},
    timeout=20,
).json()

if payload.get("status") != "OK":
    raise RuntimeError(payload)

# Выбираем 360p mp4 со звуком (itag=18 — самый совместимый muxed)
muxed = [f for f in payload.get("formats", []) if f.get("itag") == 18]
if muxed:
    print(muxed[0]["url"])
    print(f"Истечёт через {payload['expiresInSeconds']}s")
```

### Скриншот кадра видео

```python
r = requests.get(
    f"https://{HOST}/video/screenshot",
    headers=headers,
    params={"id": "dQw4w9WgXcQ", "timeStamp": "00:01:30"},
).json()

# Возвращает 3 разрешения
print(r["link"]["720p"])
print(r["link"]["480p"])
print(r["link"]["360p"])
```

### Перевод субтитров на русский

```python
# Сначала получаем доступные субтитры через /video/info
info = requests.get(f"https://{HOST}/video/info", headers=headers,
                    params={"id": video_id}).json()

# Берём английские субтитры
en_url = next(s["baseUrl"] for s in info["captions"]["captionTracks"]
              if s["languageCode"] == "en")

# Переводим на русский в формате SRT
ru = requests.get(f"https://{HOST}/subtitle", headers=headers,
                  params={"url": en_url, "targetLang": "ru", "format": "srt"}).text
print(ru)
```

### Long token через POST

```python
files = {
    "id": (None, "UCuAXFkgsw1L7xaCfnd5JJOw"),
    "sort_by": (None, "newest"),
    "token": (None, very_long_token),
}
r = requests.post(f"https://{HOST}/channel/videos", headers=headers, files=files, timeout=15)
```

Готовые скрипты — см. [examples/yt_api/](../examples/yt_api/).

---

## Типичные проблемы

### `HTTP 401 {"message": "Invalid API key. ..."}` (verified)

Невалидный или отсутствующий `X-RapidAPI-Key`. Проверь .env, dashboard RapidAPI.

### `{"status": "fail", "error": "Sign in to confirm you're not a bot"}`

YouTube блокирует трафик провайдера. Решения:

- Ретрай через 30–60 секунд с экспоненциальным backoff.
- Если воспроизводится стабильно — написать в discussions провайдера.

### `403` на `/dl`

Почти всегда — нет `cgeo` или гео-ограничение видео:

- Передай `cgeo` (страну конечного потребителя ссылки; для серверного использования — страну сервера).
- Попробуй другую страну (`US` обычно самая разрешительная).

### Пустой `data: []`

Гео/языковые ограничения или приватность контента:

- Сменить `geo` (часто `US` даёт максимум).
- Проверить через `/resolve`, что ID существует.
- Для каналов — использовать каноничный `UC...`, не handle напрямую.

### `429 Too Many Requests`

Превышен rate limit или месячная квота:

- Проверить квоту в RapidAPI dashboard.
- На Basic-плане лимит **1000 req/час** (см. Pricing) — при превышении 429.
- Включить локальный кэш (см. `examples/common.py`).
- Избегать `extend=1`, `local=1`, `forUsername`, `X-CACHEBYPASS` где не критично.

### Поля в ответе пропадают/переименовываются

Provider обновляет схему без анонсов. **Никогда не полагайся на наличие конкретного поля** — `.get(key, default)` обязателен. Особенно нестабильны `thumbnail[]`, `runs[]`, `formats[]`, `captions.captionTracks[]`, `attachment`.

### Ссылки из `/dl` не открываются через несколько часов

Они подписаны и истекают (`expiresInSeconds`, обычно `21540` = 6 ч). Перезапрашивай эндпоинт; не сохраняй URL в БД надолго; не публикуй.

### `200 OK`, но JSON содержит `error` или `status: fail`

yt-api часто возвращает HTTP 200 при логических ошибках:

```python
data = r.json()
if isinstance(data, dict) and (data.get("status") == "fail" or "error" in data):
    raise RuntimeError(f"yt-api error: {data}")
```

### Получение ответов на комментарий

Не вызывай несуществующий `/replies` — используй тот же `/comments` с `replyToken` (из `data[].replyToken`) как `token`.

### `414 URI Too Long` на пагинации

Continuation tokens бывают по 2-3 КБ. Решения:

- Передавай через заголовок `X-TOKEN: <token>` вместо query.
- Используй POST-альтернативу (`/channel/videos`, `/channel/shorts`, `/channel/liveStreams`).

### Provider не положил Example Response

Несколько эндпоинтов в playground не имеют примера ответа: `/subtitles`, `/subtitle`, `/updated_metadata`, `/post/comments`. Все четыре прозвонены реальными запросами 2026-04-28 на Basic-плане. Полные shape'ы — в **[_responses/yt-api.md](_responses/yt-api.md)**.

```jsonc
// GET /subtitle?url=<vtt_or_srt_url> → 200
// Возвращает текст субтитра в SRT-формате (Content-Type: text/plain), НЕ JSON
// 1
// 00:00:01,360 --> 00:00:03,040
// [♪♪♪]
//
// 2
// 00:00:18,640 --> 00:00:21,880
// ♪ We're no strangers to love ♪
// ...

// GET /subtitles?id=<videoId> → 200 (JSON-список доступных дорожек)
// { "subtitles": [ { "languageCode": "en", "languageName": "English", "url": "<vtt_url>", "isTranslatable": true }, ... ] }

// GET /updated_metadata?id=dQw4w9WgXcQ → 200
{
  "id": "dQw4w9WgXcQ",
  "viewCountText": "1,766,811,412 views",
  "viewCount": "1766811412",
  "likeCountText": "18M",
  "likeCount": 18983304
}

// GET /post/comments?id=<post_id> → 200 + retry-marker
// При первом вызове возвращает {"error":"Retry","code":"403"} — провайдер ретраит на их стороне.
// Делай retry с экспоненциальной паузой; обычно 2-3 повтора достаточно.
```

---

## Тарифы и расчёт расходов

> 📌 Этот раздел — для AI-ассистента. Когда пользователь спрашивает "сколько это будет стоить?" — используй данные ниже, чтобы посчитать точно.

### Тарифные планы (verified из Pricing tab, 2026-04-28)

| План | Запросов/мес | Rate Limit | Цена/мес | Overage |
|------|--------------|------------|----------|---------|
| **Basic** | 300 | 1000 req/час | **$0** | hard limit → 429 |
| **Pro** | 1 770 500 | без лимита | **$51** | hard limit → 429 |
| **Ultra** | 5 000 000 | без лимита | **$144** | hard limit → 429 |
| **Mega** | 8 400 000 | без лимита | **$240** | **$0.00003** за каждый extra-запрос |

**Bandwidth (на всех планах):** 10 240 MB/мес включено + **$0.001 за каждый дополнительный 1 MB**.

**Features (на всех планах одинаковые):** Fast Streaming, Proxy Support, Live Stream, HLS Support.

### Стоимость одного запроса в квоте

| Что делает запрос | Стоимость | Пример |
|---|---|---|
| **База** (любой GET/POST) | **1 unit** | `GET /search?query=test` |
| `+ extend=1` или `extend=2` | **+1 unit** | `/video/info?id=X&extend=1` = **2 units** |
| `+ forUsername=...` (вместо id) | **+1 unit** | `/channel/about?forUsername=Rick` = **2 units** |
| `+ cm=1` | **+1 unit** | `/dl?id=X&cgeo=US&cm=1` = **2 units** |
| `+ local=1` | **+1 unit** | `/search?query=X&geo=US&local=1` = **2 units** |
| `+ X-CACHEBYPASS: 1` (header) | **+1 unit** | принудительный refetch |
| `+ /dl без cgeo` | **+1 unit** | штраф за отсутствие cgeo |
| **Multi-id** в `/video/info`/`/updated_metadata` | **+1 unit за каждый extra id** | `id=A,B,C` = **3 units** (1 + 2 extra) |

### Формула расчёта месячной стоимости

```
quota_per_request = 1 + sum(модификаторов)
month_quota_usage = quota_per_request × requests_per_month
month_bandwidth_mb = ⌈avg_response_mb × requests_per_month⌉

# Выбор плана:
if month_quota_usage <= 300:        plan = Basic ($0)
elif month_quota_usage <= 1_770_500: plan = Pro ($51)
elif month_quota_usage <= 5_000_000: plan = Ultra ($144)
elif month_quota_usage <= 8_400_000: plan = Mega ($240)
else:                                plan = Mega + overage (extra × $0.00003)

# Bandwidth поверх плана:
extra_mb = max(0, month_bandwidth_mb - 10_240)
bandwidth_cost = extra_mb × $0.001

total_monthly_cost = plan_price + bandwidth_cost
```

**Rate-limit на Basic:** 1000 req/час = ~16.6 req/мин = 1 req каждые 3.6 сек. Если пытаешься сделать больше — 429. Это лимит на ИНТЕНСИВНОСТЬ, отдельно от месячного лимита 300.

### Реальные сценарии (сколько это будет стоить)

#### 1. Учебный проект — поиск 10 видео в день

```
10 запросов/день × 30 = 300 req/месяц
Каждый = 1 unit (просто /search)
Bandwidth: ~50 KB × 300 = 15 MB → в лимите
ПЛАН: Basic ($0)
```

#### 2. Дашборд канала — обновление 1 раз в час

```
24 раза/день × 30 дней = 720 запросов/мес на /channel/videos
+ 1 раз/неделю /channel/about = 4 req/мес
Каждый = 1 unit
ИТОГО: 724 req/мес → не помещается в Basic (300)
ПЛАН: Pro ($51/мес)
```

Совет: добавь кэш на 1 час (`requests_cache.CachedSession(expire_after=3600)`) — тогда уложишься в Basic.

#### 3. Мониторинг счётчиков 100 видео каждые 5 минут

```
100 видео × (60 / 5 = 12 раз/час) × 24 ч × 30 дней = 864 000 запросов/мес
БЕЗ multi-id: 864 000 × 1 = 864 000 units
С multi-id (10 за раз): 86 400 запросов × 10 units (1 base + 9 extra) = 864 000 units
ИТОГО: 864 000 units/мес
ПЛАН: Pro ($51) — помещается с запасом
```

⚠️ Совет: используй `/updated_metadata` (не `/video/info`) — оно лёгкое и подходит для polling.

#### 4. Скачивание видео — 100 видео в день, в среднем 50 MB каждое

```
ЗАПРОСЫ:
  100 × 30 = 3000 запросов /dl/мес
  Каждый = 1 unit (с cgeo, без cm)
  ИТОГО: 3000 units → Pro ($51)

BANDWIDTH:
  100 видео × 50 MB × 30 дней = 150 000 MB/мес
  Лимит включённый: 10 240 MB
  Overage: 150 000 - 10 240 = 139 760 MB × $0.001 = $139.76

ИТОГО МЕСЯЧНО: $51 + $139.76 = $190.76
```

⚠️ **Скачивание сжигает bandwidth, а не квоту.** Главный риск — bandwidth-overage.

#### 5. NLP-анализ комментариев 50 видео × 1000 коммов каждое

```
КОММЕНТАРИИ:
  Один /comments = 20 элементов в data → нужно 50 страниц для 1000 коммов
  50 видео × 50 страниц = 2500 запросов /comments
  + 50 запросов /video/info для метаданных
  ИТОГО: 2550 units/мес → Pro ($51)

BANDWIDTH: ~1 MB на 1000 коммов × 50 = 50 MB → в лимите
ИТОГО: $51/мес
```

#### 6. Скрейпинг: вытащить все видео 1000 каналов за месяц

```
СРЕДНИЙ канал: 200 видео / 50 на странице = 4 страницы
1000 каналов × 4 страницы = 4000 запросов /channel/videos
+ 1000 запросов /channel/about (если нужны меты)
+ 1000 запросов /resolve (если на входе только handle)
Все = 1 unit каждый
ИТОГО: 6000 units/мес → Pro ($51)
```

⚠️ Если на входе handle — каждый `/resolve` = 1 unit (а не +1 от forUsername). `/resolve` дешевле, чем `forUsername` на каждом /channel/* запросе.

### Чеклист "как сэкономить квоту"

1. **Кэшируй детерминированные ответы** на 1 час — `/channel/about`, `/playlist`, `/video/info` без extend.
2. **Не используй `forUsername` в цикле** — один `/resolve` дешевле, потом везде по `id`.
3. **Multi-id режим** в `/video/info`/`/updated_metadata` дешевле полного цикла на N запросов (1+N-1 vs N).
4. **`/updated_metadata` вместо `/video/info`** для polling счётчиков — без `extend=1`.
5. **Не включай `extend=1`** если не нужны likeCount/commentCount/chapters — это +1 unit за запрос.
6. **Не включай `local=1`** в дев-режиме.
7. **Не включай `X-CACHEBYPASS`** в обычной работе.
8. **Передавай `cgeo`** в `/dl` всегда — иначе +1 unit и риск 403.
9. **На Basic-плане** добавь throttle (1 req / 4 сек), чтобы не словить 429 по rate-limit (1000/час).
10. **Скачивание видео** = bandwidth, не квота. Главный расход не в плане, а в overage за MB.

---

## Что хорошо подходит для учебных проектов

- Поиск + метаданные через `/search` + `/video/info` (отработка JSON и фильтров).
- Сбор комментариев + ответов (`replyToken` → `/comments`) для NLP/sentiment-анализа.
- Парсинг канала: `/channel/videos` возвращает meta+data — готовый дашборд.
- Тренды + Hype-лента по странам — источник свежих данных.
- Транскрипт через `/get_transcript` + LLM-саммари (структура `{startMs, endMs, text}` идеальна).
- Перевод субтитров через `/subtitle?targetLang=...`.
- Анализ сообществ канала: `/channel/community` + `/post/info` + `/post/comments`.
- Граф аффилированных каналов через `/channel/channels` (Featured Channels).
- Скриншоты ключевых кадров через `/video/screenshot` (отдаёт 3 разрешения).

## Что не делать

- **Не качать видео массово** через `/dl` — нарушает ToS YouTube, провайдер забанит ключ.
- Не строить продакшн без фолбэка (хотя бы на официальный YouTube Data API).
- Не публиковать ссылки из `/dl` — они подписаны и быстро протухают.
- Не вызывать API из браузера — ключ утечёт. Только через свой бэкенд.
- Не передавать `forUsername` каждый раз вместо `id` — это +1 квота. Закэшируй handle→channelId через `/resolve`.
- Не перепутать `/subtitles` (множественное — список или raw) и `/subtitle` (единственное — конвертация/перевод).
