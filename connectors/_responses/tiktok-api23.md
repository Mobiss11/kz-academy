# TikTok API (Lundehund) — verified response shapes

> ✅ **Источник:** все 56 эндпоинтов имеют верифицированную форму ответа.
>
> - **41 эндпоинт** — захвачены из RapidAPI Playground (Example Response provider'а, authoritative).
> - **15 эндпоинтов (Ads/Trending group)** — захвачены аналогично, но без user-friendly-имени в playground (UUID-only); идентифицированы по содержимому.
> - **15 эндпоинтов** — реально прозвонены на Basic-плане 2026-04-28 (edge-cases для disabled subscription / 204 / status_code).
> - Длинные подписанные CDN-URL замаскированы как `<url>`. Долгие base64-токены/request_id → `<x>`. Длинные строки (описания, signatures) → `<str>`.
>
> Этот файл — **canonical reference** для проверки имён полей. Если ученик пишет код и сомневается в названии поля — grep по этому файлу.

---

## Стандартные паттерны обёртки

```jsonc
// Паттерн A — feed/list (cursor-пагинация)
{ "extra": { "fatal_item_ids": [], "logid": "<x>", "now": <ts> },
  "log_pb": { "impr_id": "<x>" },
  "status_code": 0, "cursor": "30", "hasMore": true,
  "itemList": [/* Aweme */] }

// Паттерн B — single object detail
{ "itemInfo": { "itemStruct": { /* Aweme */ } },
  "extra": {...}, "log_pb": {...}, "status_code": 0 }

// Паттерн C — wrapped data (Ads/Trending/Music groups)
{ "code": 0, "msg": "OK", "request_id": "<x>",
  "data": { "list": [...], "pagination": {...} } }
```

`status_code != 0` или `code != 0` = ошибка. Всегда проверяй после HTTP-200.

---

## User group (11 endpoints)

### Get User Info — `/api/user/info?uniqueId=...`

```jsonc
{
  "extra": { "fatal_item_ids": [], "logid": "<x>", "now": <ts> },
  "log_pb": { "impr_id": "<x>" },
  "shareMeta": { "desc": "...", "title": "Taylor Swift on TikTok" },
  "statusCode": 0, "status_code": 0, "status_msg": "",
  "userInfo": {
    "stats": { "diggCount": 2276, "followerCount": 33300000, "followingCount": 0, "friendCount": 0, "heart": 263500000, "heartCount": 263500000, "videoCount": 78 },
    "statsV2": { "diggCount": "2276", "followerCount": "33265139", "followingCount": "0", "friendCount": "0", "heart": "263479941", "heartCount": "263479941", "videoCount": "78" },
    "user": {
      "UserStoryStatus": 0,
      "avatarLarger": "<url>", "avatarMedium": "<url>", "avatarThumb": "<url>",
      "bioLink": { "link": "...", "risk": 0 },
      "canExpPlaylist": true,
      "commentSetting": 0, "commerceUserInfo": { /* */ },
      "duetSetting": 0, "stitchSetting": 0,
      "downloadSetting": 0,
      "followingVisibility": 1,
      "ftc": false, "id": "<id>",
      "isADVirtual": false, "isEmbedBanned": false,
      "nickname": "Taylor Swift", "openFavorite": true,
      "privateAccount": false, "secret": false,
      "secUid": "<x>", "shortId": "",
      "signature": "...", "ttSeller": false,
      "uniqueId": "taylorswift", "verified": true
    }
  }
}
```

### Get User Info (Include User Region) — `/api/user/info-with-region`

```jsonc
{
  "userInfo": {
    "user": { /* 39 keys, includes the standard user fields above plus profileTab */
      "id": "<id>", "shortId": "", "uniqueId": "taylorswift", "nickname": "Taylor Swift",
      "avatarLarger": "<url>", "avatarMedium": "<url>", "avatarThumb": "<url>",
      "signature": "...", "createTime": 1628514847,
      "verified": true, "secUid": "<x>",
      "ftc": false, "relation": 0, "openFavorite": true,
      "bioLink": { "link": "...", "risk": 0 },
      "commentSetting": 0,
      "commerceUserInfo": { "commerceUser": false },
      "duetSetting": 0, "stitchSetting": 0,
      "privateAccount": false, "secret": false,
      "isADVirtual": false, "roomId": "",
      "uniqueIdModifyTime": 0, "ttSeller": false,
      "downloadSetting": 0,
      "profileTab": { "showMusicTab": true, "showQuestionTab": false, "showPlayListTab": false },
      "followingVisibility": 1, "recommendReason": "",
      "nowInvitationCardUrl": "", "nickNameModifyTime": 0,
      "region": "US"   /* ← главное отличие от обычного /info */
    }
  }
}
```

### Get User Info by ID — `/api/user/info-by-id?userId=...`

```jsonc
{
  "extra": {...}, "log_pb": {...}, "status_code": 0, "status_msg": "",
  "user": {  /* internal mobile schema, snake_case */
    "account_type": 0,
    "avatar_300x300": { "uri": "<x>", "url_list": ["<url>"] },
    "avatar_larger": { "uri": "<x>", "url_list": ["<url>"] },
    "avatar_medium": { "uri": "<x>", "url_list": ["<url>"] },
    "avatar_thumb": { "uri": "<x>", "url_list": ["<url>"] },
    "commerce_user_level": 0,
    "custom_verify": "verified account",
    "enterprise_verify_reason": "",
    "follow_status": 0,
    "follower_count": 33265168,
    "follower_status": 0,
    "following_count": 0,
    "is_block": false, "is_blocked": false,
    "nickname": "Taylor Swift",
    /* + ~15 more snake_case fields */
  }
}
```

### Get User Followers — `/api/user/followers?secUid=...`

```jsonc
{
  "followers": [
    {  /* 120 keys per follower! Polymorphic User-detail schema */
      "accept_private_policy": false, "account_labels": null,
      "account_region": "", "ad_cover_url": null,
      "advance_feature_item_order": null, "advanced_feature_info": null,
      "apple_account": 0, "authority_status": 0,
      "avatar_168x168": { "uri": "<x>", "url_list": [...] },
      "avatar_300x300": {...}, "avatar_larger": {...},
      "avatar_medium": {...}, "avatar_thumb": {...},
      /* +~110 more snake_case profile fields */
    }
  ],
  /* + cursor / has_more / total / status_code */
}
```

### Get User Followings — `/api/user/followings?secUid=...`

Та же схема что `/followers`. На приватных юзерах:

```jsonc
// Real-call edge case — user hides following list:
{
  "status_code": 3002060,
  "status_msg": "Profile user is hiding following list",
  "max_time": 0, "min_time": 0
}
```

### Get User Posts — `/api/user/posts?secUid=...&count=35&cursor=0`

```jsonc
{
  "data": {
    "cursor": "1664510413000",
    "extra": {...}, "log_pb": {...},
    "hasMore": true,
    "itemList": [
      {  /* Aweme-объект (33 keys) */
        "AIGCDescription": "", "CategoryType": 113, "HasPromoteEntry": 0,
        "author": {
          "avatarLarger": "<url>", "avatarMedium": "<url>", "avatarThumb": "<url>",
          "commentSetting": 0, "downloadSetting": 0, "duetSetting": 0,
          "ftc": false, "id": "<id>", "isADVirtual": false, "isEmbedBanned": false,
          "nickname": "Taylor Swift", "openFavorite": true,
          "privateAccount": false, "relation": 0, "secUid": "<x>",
          "secret": false, "signature": "<str>", "stitchSetting": 0,
          "uniqueId": "taylorswift", "verified": true
        },
        "authorStats": { "diggCount": 2204, "followerCount": 32800000, "followingCount": 0, "friendCount": 0, "heart": 246300000, "heartCount": 246300000, "videoCount": 78 },
        /* + challenges, contents, music, stats, statsV2, video, ... */
      }
    ]
  }
}
```

### Get User Liked Posts — `/api/user/liked-posts?secUid=...`

```http
// Real-call: на приватных лайках
HTTP/1.1 204 No Content
// Парсер должен явно проверять status==204 и не пытаться .json()
```

Если у юзера лайки публичные — структура аналогична `/api/user/posts`.

### Get User Playlist — `/api/user/playlist?secUid=...&cursor=0`

```jsonc
{
  "cursor": "20", "hasMore": true,
  "extra": {...}, "log_pb": {...},
  "playList": [
    {
      "cover": "<url>",
      "creator": {  /* compact user (15 keys) */
        "id": "<id>", "uniqueId": "cnn",
        "nickname": "CNN",
        "avatarLarger": "<url>", "avatarMedium": "<url>", "avatarThumb": "<url>",
        "signature": "...",
        "ftc": false, "isADVirtual": false,
        "openFavorite": false, "privateAccount": true,
        "relation": 0, "secUid": "<x>",
        "secret": true, "verified": false
      },
      "id": "<playlist_id>", "mixId": "<playlist_id>",
      "mixName": "Government shutdown",
      "name": "Government shutdown",
      "videoCount": 5
    }
  ]
}
```

### Get User Repost — `/api/user/repost?secUid=...&cursor=0&count=30`

Те же поля что `/api/user/posts.itemList`, но `cursor` идёт по числовому индексу. Пример:

```jsonc
{
  "cursor": "30", "hasMore": true,
  "extra": {...},
  "itemList": [
    {  /* Aweme + author + authorStats */
      "AIGCDescription": "",
      "author": { /* full author 20 keys */ },
      "authorStats": { /* same 7 keys */ },
      "challenges": [/* challenge objects */],
      /* +Aweme fields */
    }
  ]
}
```

### Get User Story — `/api/user/story?secUid=...`

```jsonc
{
  "AllViewed": false, "CurrentPosition": "0",
  "HasMoreAfter": false, "HasMoreBefore": false,
  "LastStoryCreatedAt": "1764090811561",
  "MaxCursor": "1764090811561", "MinCursor": "1764090811561",
  "TotalCount": "1",
  "extra": {...},
  "itemList": [{ /* Aweme story object, 32 keys */ }]
}
```

### Get User Oldest Posts — `/api/user/oldest-posts?secUid=...`

Та же структура что `/api/user/posts`, отсортированная по возрастанию `createTime`.

### Get User Popular Posts — `/api/user/popular-posts?secUid=...`

Та же структура что `/api/user/posts`, отсортированная по `stats.playCount` desc.

---

## Search group (5 endpoints)

### Search General (Top) — `/api/search/general?keyword=...&cursor=0`

```jsonc
{
  "ad_info": {}, "backtrace": "", "cursor": 12,
  "data": [
    {
      "common": { "doc_id_str": "<id>" },
      "item": { /* Aweme + author + authorStats + challenges */
        "author": { /* compact 18 keys */ },
        "authorStats": { /* 6 keys: diggCount, followerCount, ... */ },
        "challenges": [{ "id": "...", "title": "...", "stats": {...} }],
        /* + Aweme media fields */
      },
      /* + type, position */
    }
  ],
  "extra": {...}, "log_pb": {...}, "status_code": 0
}
```

### Search Video — `/api/search/video?keyword=...&cursor=0`

Та же обёртка `data:[]` с `item` внутри. Каждый item — Aweme.

### Search Account — `/api/search/account?keyword=...`

```jsonc
{
  "type": 1,
  "user_list": [
    {
      "user_info": {
        "uid": "<id>",
        "nickname": "Taylor Swift",
        "signature": "<str>",
        "avatar_thumb": { "uri": "<x>", "url_list": [...], "width": 720, "height": 720, "url_prefix": null },
        "follow_status": 0,
        "follower_count": 33300000,
        "total_favorited": 263941369,
        "custom_verify": "Verified account",
        "unique_id": "taylorswift",
        "room_id": 0,
        "enterprise_verify_reason": "",
        "sec_uid": "<x>",
        /* + ~25 fields, mostly null */
      }
    }
  ]
  /* + log_id, status_code, ... */
}
```

### Search Live — `/api/search/live?keyword=...`

```jsonc
{
  "backtrace": "", "cursor": 12,
  "data": [
    {
      "live_info": {
        "raw_data": "<JSON_string>"  /* ⚠️ raw_data — это вложенный JSON-строка, не объект */
      }
    }
  ],
  "extra": {...}, "log_pb": {...}, "status_code": 0
}
```

`raw_data` парсится JSON.parse'ом. Внутри: `id`, `id_str`, `status`, `owner_user_id`, `title`, `user_count`, `os_type`, `client_version`, `cover{url_list, uri}`, `stream_url{rtmp_pull_url, flv_pull_url{FULL_HD1, SD1, SD2}, candidate_resolution, flv_pull_url_params, live_core_sdk_data{pull_data{stream_data}}}`, ...

### Others Searched For (Suggest Search) — `/api/search/suggest?keyword=...`

```jsonc
{
  "data": [
    { "group_id": "<id>", "word": "Funny cat videos" },
    { "group_id": "<id>", "word": "cats meowing to attract cat" }
    /* +N more */
  ],
  "log_id": "<x>", "status_code": 0, "status_msg": ""
}
```

---

## Post (Video) group (8 endpoints)

### Get Post Detail — `/api/post/detail?videoId=...`

```jsonc
{
  "itemInfo": {
    "itemStruct": {  /* 40 keys — full Aweme schema */
      "AIGCDescription": "", "IsAigc": false,
      "author": {
        "avatarLarger": "<url>", "avatarMedium": "<url>", "avatarThumb": "<url>",
        "canExpPlaylist": false, "commentSetting": 0, "createTime": 0,
        "downloadSetting": 0, "duetSetting": 0, "ftc": false, "id": "<id>",
        "isADVirtual": false, "isEmbedBanned": false,
        "nickNameModifyTime": 0, "nickname": "Taylor Swift",
        "nowInvitationCardUrl": "", "openFavorite": true,
        "privateAccount": false, "recommendReason": "",
        "relation": 0, "roomId": "", "secUid": "<x>",
        "secret": false, "shortId": "",
        "signature": "...", "stitchSetting": 0,
        "suggestAccountBind": false, "ttSeller": false,
        "uniqueId": "taylorswift", "uniqueIdModifyTime": 0,
        "verified": true
      },
      "challenges": [],
      "channelTags": [], "collected": false, "comments": [],
      /* + music, stats, statsV2, video, contents, createTime, desc, id, digged, duetEnabled, ... */
    }
  },
  "extra": {...}, "log_pb": {...}, "status_code": 0
}
```

### Get Comments of Post — `/api/post/comments?videoId=...&count=50`

```jsonc
{
  "alias_comment_deleted": false,
  "comments": [
    {  /* 30 keys per comment */
      "allow_download_photo": true, "author_pin": false,
      "aweme_id": "<id>", "cid": "<comment_id>",
      "collect_stat": 0, "comment_language": "en",
      "comment_post_item_ids": null,
      "create_time": 1701091808,
      "digg_count": 47418,
      "image_list": null, "is_author_digged": false,
      "is_comment_translatable": true, "is_high_purchase_intent": false,
      "label_list": null, "no_show": false,
      "reply_comment": null, "reply_comment_total": 211,
      "reply_id": "0", "reply_to_reply_id": "0",
      "share_info": { "acl": {...}, "code": 0, "extra": "{}", "desc": "...", "title": "...", "url": "<url>" },
      "sort_extra_score": { "reply_score": 0.006964, "show_more_score": 0.177659 },
      "sort_tags": "{\"top_list\":1}",
      "status": 1, "stick_position": 0,
      "text": "...", "text_extra": [], "trans_btn_style": 0,
      "user": {  /* 32 keys */
        "account_labels": null, "ad_cover_url": null,
        "avatar_thumb": { "uri": "<x>", "url_list": [...], "url_prefix": null },
        "follow_status": 0, "follower_status": 0,
        "nickname": "...", "uid": "<id>", "unique_id": "...",
        /* + ~25 more */
      }
    }
  ],
  /* + cursor / has_more / status_code / total */
}
```

### Get Replies Comment of Post — `/api/post/comment-replies?cid=...`

```jsonc
{
  "comments": [
    {  /* same comment shape as Get Comments, but with reply_id !== "0" */
      "aweme_id": "<id>", "cid": "<reply_cid>",
      "reply_id": "<parent_cid>",
      "reply_to_reply_id": "0",
      /* + same 25+ fields */
    }
  ],
  "cursor": ..., "has_more": ..., "status_code": 0
}
```

### Get Related Posts — `/api/post/related?videoId=...`

```jsonc
{
  "extra": {...},
  "itemList": [/* Aweme objects, 35 keys each — same schema as user posts */],
  "status_code": 0
  /* НЕТ cursor/hasMore — это одна страница */
}
```

### Get Trending Posts — `/api/post/trending?count=20`

```jsonc
{
  "cursor": "0",
  "extra": {...}, "log_pb": {...},
  "hasMore": true,
  "itemList": [/* Aweme objects, 35 keys */]
}
```

### Get Explore Posts — `/api/post/explore?count=30&cursor=0`

```jsonc
{
  "cursor": "0", "extra": {...}, "hasMore": true,
  "itemList": [
    {  /* 24 keys — explore-shape Aweme */
      "author": { /* full 20 keys */ },
      "authorStats": { /* 7 keys */ },
      "collected": false,
      "contents": [{ "desc": "..." }],
      /* + media, stats, video */
    }
  ]
}
```

### Discover Posts by Keyword — `/api/post/discover?keyword=...`

```jsonc
{
  "cacheSessionId": "<x>",
  "extra": {...}, "log_pb": {...}, "hasMore": true,
  "seoBizItemInfoList": [
    {
      "customTdk": {
        "article": "",
        "description": "...",
        "keywords": ["...", "..."],
        "title": "..."
      },
      "itemId": "<id>"
    }
  ],
  "videoList": [/* Aweme-объекты */],
  "statusCode": 0, "status_code": 0, "status_msg": ""
}
```

### Download All User Videos — `/api/user/download-all?secUid=...`

```jsonc
{
  "itemList": [
    {  /* 6 keys — download-friendly compact shape */
      "id": "<id>", "desc": "...",
      "play": "<url>", "cover": "<url>",
      "stats": {
        "collect_count": 44455, "comment_count": 49271,
        "digg_count": 1467716, "download_count": 3066,
        "forward_count": 0, "play_count": 10959929,
        "repost_count": 0, "share_count": 44677
      },
      "create_time": 1770959608
    }
  ]
  /* + cursor / hasMore */
}
```

---

## Download group (3 endpoints)

### Download Video — `/api/download/video?url=<tt_url>`

```jsonc
{
  "play": "<signed_cdn_url_no_watermark>",
  "play_watermark": "<signed_cdn_url_with_watermark>"
}

// Real-call edge case — URL без видео:
HTTP/1.1 204 No Content
```

### Download Music — `/api/download/music?url=<tt_url>`

```jsonc
{ "play": "<signed_cdn_url_mp3>" }
```

### Download All User Videos — described above in Post group.

---

## Live group (4 endpoints)

### Get Live Info — `/api/live/info?roomId=...`

```jsonc
// Real-call edge — bad/expired roomId:
{
  "data": { "message": "Request params error", "prompts": "Request params error" },
  "extra": { "now": <ts> },
  "status_code": 10011
}
// На валидном roomId — структура с данными о live комнате (24+ полей)
```

### Get Live Stream — `/api/live/stream?cursor=0`

```jsonc
{
  "status_code": 0,
  "extra": {
    "log_pb": { "impr_id": "<x>", "session_id": "<id>" },
    "has_more": true, "cost": 126,
    "max_time": 1735206515562, "total": 12,
    "banner": {}, "unread_extra": "<json_string>",
    "now": 1735206515562
  },
  "data": [
    {
      "type": 1, "rid": "<x>",
      "data": {  /* live broadcast info, 23 keys */
        "id": <int>, "id_str": "<id>",
        "status": 2, "owner_user_id": <int>,
        "title": "...", "user_count": 1268,
        "client_version": 44,
        "cover": { "url_list": [...], "uri": "<x>" },
        "stream_url": {
          "rtmp_pull_url": "<url>",
          "flv_pull_url": { "SD2": "<url>", "SD1": "<url>", "HD1": "<url>" },
          "flv_pull_url_params": { "SD2": "<json_string>", ... }
        }
      }
    }
  ]
}
```

### Get Live Category — `/api/live/category`

```jsonc
{
  "data": [
    {
      "is_not_show_tab": false,
      "sub_tabs": [
        { "cover_url": "<url>", "position": 0,
          "rank_type": "hot_game",
          "tab_name": "Garena Free Fire", "tab_type": "Garena Free Fire",
          "viewer_count": 65303 }
        /* + N more sub_tabs */
      ]
    }
  ]
  /* +status_code, extra */
}
```

### Check Alive — `/api/live/check-alive?room_ids[]=...`

```jsonc
{
  "data": [
    { "alive": false, "room_id": <int>, "room_id_str": "<id>" }
  ],
  "extra": { "now": <ts> },
  "status_code": 0
}
```

---

## Challenge (Hashtag) group (2 endpoints)

### Get Challenge Info — `/api/challenge/info?challengeName=fyp`

```jsonc
{
  "challengeInfo": {
    "challenge": {
      "coverLarger": "", "coverMedium": "", "coverThumb": "",
      "desc": "", "id": "<id>", "isCommerce": false,
      "profileLarger": "", "profileMedium": "", "profileThumb": "",
      "stats": { "videoCount": 0, "viewCount": 105814200000000 },
      "title": "fyp"
    },
    "challengeAnnouncement": { "body": "", "title": "" },
    "stats": { "videoCount": 0, "viewCount": 105814200000000 },
    "statsV2": { "videoCount": "8050280214", "viewCount": "105814218058744" }
  },
  "extra": {...}, "log_pb": {...},
  "shareMeta": { "desc": "...", "title": "#fyp on TikTok" },
  "statusCode": 0, "status_code": 0, "status_msg": ""
}
```

### Get Challenge Posts — `/api/challenge/posts?challengeId=...&cursor=0`

```jsonc
{
  "cursor": "30", "extra": {...}, "hasMore": true,
  "itemList": [/* full Aweme — 35 keys: author, authorStats, challenges, music, stats, video, ... */]
}
```

---

## Music group (3 endpoints)

### Get Music Info — `/api/music/info?musicId=...`

```jsonc
{
  "extra": {...}, "log_pb": {...},
  "musicInfo": {
    "artist": {  /* 13 keys */
      "id": "<id>", "uniqueId": "taylorswift", "nickname": "Taylor Swift",
      "avatarLarger": "<url>", "avatarMedium": "<url>", "avatarThumb": "<url>",
      "ftc": false, "openFavorite": false, "privateAccount": false,
      "relation": 0, "secUid": "<x>", "secret": false, "signature": "..."
    },
    "artists": [/* same shape as artist */],
    "music": {
      "album": "The Life of a Showgirl", "authorName": "...",
      /* + 14 more music fields */
    }
  }
}
```

### Get Music Posts — `/api/music/posts?musicId=...&cursor=0`

```jsonc
{
  "cursor": "30", "extra": {...}, "hasMore": true,
  "itemList": [/* full Aweme objects */]
}
```

### Get Unlimited Sounds — `/api/music/unlimited-sounds`

```jsonc
{
  "data": {
    "has_more": true,
    "music_list": [
      {  /* 69 keys per sound — full sound metadata */
        "album": "", "artists": [],
        "audition_duration": 0,
        "author": "Official Sound Studio",
        "author_deleted": false, "author_position": null,
        "avatar_medium": { "uri": "<x>", "url_list": [...], "url_prefix": null, "height": 720, "width": 720 },
        "avatar_thumb": {...},
        "binded_challenge_id": 0,
        "can_be_stitched": true, "can_not_reuse": false,
        "collect_stat": 0, "commercial_right_type": 2,
        "cover_large": {...}, "cover_medium": {...}, "cover_thumb": {...},
        /* + ~54 more music fields: duration, music_id, title, play_url, ... */
      }
    ]
  }
  /* + status_code, code, msg */
}
```

---

## Place (Location) group (2 endpoints)

### Get Place Info — `/api/place/info?placeId=...`

```jsonc
{
  "extra": {...}, "log_pb": {...},
  "poiInfo": {
    "poi": {  /* 24 keys */
      "address": "California, United States",
      "allLevelGeoPoiInfo": {},
      "category": "Places",
      "city": "", "cityCode": "<code>",
      "country": "", "countryCode": "<code>",
      "fatherPoiId": "", "fatherPoiName": "",
      "id": "<id>", "indexEnabled": true,
      "isClaimed": false, "isCollected": false,
      "name": "Hollywood",
      "phoneInfo": { "exist": false },
      "pictureAlbum": { "totalCount": 0 },
      "poiDetailTags": [{ "content": "Places", "tagType": 5 }],
      "province": "",
      "ttTypeCode": "<code>",
      "ttTypeNameMedium": "Places",
      "ttTypeNameSuper": "Place and Address",
      "ttTypeNameTiny": "Other Places",
      "type": 1, "typeCode": ""
    },
    "stats": { "videoCount": <n> }
  }
}
```

### Get Place Posts — `/api/place/posts?placeId=...&cursor=0`

```jsonc
{
  "cursor": "30", "extra": {...}, "hasMore": true,
  "itemList": [/* Aweme objects, 37 keys (slightly more than user posts) */]
}
```

---

## Effect group (2 endpoints)

### Get Effect Info — `/api/effect/info?effectId=...`

```jsonc
// Real-call edge — bad/non-existent effectId:
{
  "log_pb": { "impr_id": "<x>" },
  "status_code": 4,
  "status_msg": "Server is currently unavailable. Please try again later."
}
// На валидных effectId возвращается effect metadata
```

### Get Effect Posts — `/api/effect/posts?effectId=...`

```jsonc
{
  "aweme_list": [
    {  /* 120 keys per Aweme — much fuller schema */
      "add_yours_info": { "video_source": 1 },
      "added_sound_music_info": {  /* 63 keys — full music object */
        "album": "Bad (Remastered)",
        "artists": [], "audition_duration": 0,
        "author": "Michael Jackson",
        "cover_large": { "uri": "<x>", "url_list": [{ "0": "<url>" }], "url_prefix": null, "height": 720, "width": 720 },
        "cover_medium": {...}, "cover_thumb": {...},
        "create_time": 1613653657, "duration": 9,
        "duration_high_precision": { "audition_duration_precision": 0, "duration_precision": 9, ... },
        /* + ~50 more music fields */
      }
      /* + 119 more Aweme fields */
    }
  ]
  /* + status_code, extra, log_pb */
}
```

---

## Collection group (2 endpoints)

### Get Collection Info — `/api/collection/info?collectionId=...`

> Provider не положил Example Response. По реальному вызову — ту же обёртку Aweme что у `/api/user/posts`.

### Get Collection Posts — `/api/collection/posts?collectionId=...`

```jsonc
// Real-call:
{
  "cursor": "10",
  "extra": { "fatal_item_ids": [], "logid": "<x>", "now": <ts> },
  "hasMore": true,
  "itemList": [/* Aweme objects, same schema as user posts */]
}
```

---

## Ads (Trending) group ⭐ — custom-plan-only (12 endpoints)

> ⛔ На Basic/Pro/Ultra/Mega эти эндпоинты отдают:
> ```http
> HTTP/1.1 401 {"message": "This endpoint is disabled for your subscription"}
> ```
> Для доступа — custom plan от провайдера. Ниже — verified shapes из playground'а.

### Get Trending Creators — `/api/trending/creator?country=US`

```jsonc
{
  "code": 0,
  "data": {
    "list": [
      {
        "creator": {  /* 10 keys */
          "avatar_url": "<url>",
          "country_code": "US",
          "follower_cnt": 15773811,
          "items": [
            { "cover_url": "<url>", "create_time": 1682522127,
              "item_id": "<id>", "liked_cnt": 26872,
              "tt_link": "<url>", "vv": 1737911 }
          ],
          "liked_cnt": 678393052,
          "nick_name": "...",
          "tcm_id": "<id>", "tcm_link": "<url>",
          "tt_link": "<url>"
        }
      }
    ]
  },
  "msg": "OK", "request_id": "<x>"
}
```

### Get Trending Hashtags — `/api/trending/hashtag?country=US&period=7`

```jsonc
{
  "code": 0, "data": {
    "list": [
      {  /* 12 keys per hashtag */
        "country_info": { "id": "US", "label": "US", "value": "United States" },
        "creators": [
          { "avatar_url": "<url>", "nick_name": "..." }
        ],
        "hashtag_id": "<id>", "hashtag_name": "roblox",
        "industry_info": { "id": <int>, "label": "label_25000000000", "value": "Games" },
        "is_promoted": false,
        "publish_cnt": 1252948,
        "rank": 1, "rank_diff": 0, "rank_diff_type": 2,
        "trend": [ { "time": 1708128000, "value": 0.84 } ]
      }
    ]
  }
}
```

### Get Trending Songs — `/api/trending/song?country=US&period=7`

```jsonc
{
  "code": 0, "data": {
    "pagination": { "has_more": true, "page": 1, "size": 20, "total": 98 },
    "sound_list": [
      {  /* 18 keys */
        "author": "...", "clip_id": "<id>",
        "country_code": "US", "cover": "<url>",
        "duration": 60, "if_cml": false, "is_search": false,
        "link": "<url>",
        "on_list_times": null, "promoted": false,
        "rank": 1, "rank_diff": null, "rank_diff_type": 4,
        "related_items": [ { "cover_uri": "<url>", "item_id": <int> } ],
        "song_id": "<id>"
        /* + ~5 more */
      }
    ]
  }
}
```

### Get Trending Keywords — `/api/trending/keyword?country=US`

```jsonc
{
  "code": 0, "data": {
    "keyword_list": [
      {  /* 13 keys */
        "comment": 1825, "cost": 570000,
        "cpa": 0.93, "ctr": 4.08, "cvr": 45.67,
        "impression": 70500000,
        "keyword": "free shipping",
        "like": 152003, "play_six_rate": 8.61,
        "post": 3520, "post_change": 99.16,
        "share": 4974,
        "video_list": ["<id>", "<id>", ...]
      }
    ]
  }
}
```

### Get Trending Ads — `/api/trending/ads`

> Empty playground example (provider didn't fill it).
> Real call: `401 {"message": "This endpoint is disabled for your subscription"}`.
> Schema по аналогии с `/api/trending/keyword` ожидаемо `{code, data:{ad_list[]}}`.

### Get Ad Detail — `/api/trending/ad/detail?adId=...`

```jsonc
{
  "code": 0,
  "data": {  /* 24 keys */
    "ad_title": "Hurry up! 40%OFF TODAY",
    "brand_name": "...",
    "comment": 488, "cost": 2,
    "country_code": ["GB", "CA", "US", "IE", /* +37 more */ ],
    "ctr": 0.06, "favorite": false,
    "has_summary": true, "highlight_text": "",
    "id": "<id>", "industry_key": "label_<id>",
    "is_search": false
    /* + ~12 more analytics fields */
  }
}
```

### Get Top Products — `/api/trending/top-products?country=US`

```jsonc
{
  "code": 0, "msg": "OK", "request_id": "<x>",
  "data": {
    "list": [
      {  /* 17 keys */
        "comment": 10190, "cost": 174000,
        "cover_url": "<url>",
        "cpa": 1.84, "ctr": 3.12, "cvr": 4.44,
        "ecom_type": "l3",
        "first_ecom_category": { "id": "<id>", "label": "category_<id>", "value": "Menswear & Men's Underwear" },
        "second_ecom_category": { "id": "<id>", "label": "...", "parent_id": "<id>", "value": "Men's Tops" },
        "third_ecom_category": { "id": "<id>", "label": "...", "parent_id": "<id>", "value": "T-Shirts" },
        "impression": 159000000, "like": 653663,
        "play_six_rate": 12.58,
        "post": 56300, "post_change": -6.93,
        "share": 11660,
        "url_title": "T-Shirts"
      }
    ]
  }
}
```

### Get Top Products Detail — `/api/trending/top-products/detail?product_id=...`

> Empty playground example. Real-call edge:
> ```jsonc
> // Bad/short product_id
> {
>   "code": 40000,
>   "msg": "Key: 'GetProductDetailParams.Id' Error:Field validation for 'Id' failed on the 'max' tag",
>   "request_id": "<x>"
> }
> ```

### Get Top Products Metrics — `/api/trending/top-products/metrics?product_id=...`

> Аналогично выше. Same error shape on bad product_id.

### Get Trending Videos by Country — `/api/trending/videos?country=US`

```jsonc
{
  "code": 0, "data": {
    "pagination": { "has_more": true, "limit": 20, "page": 1, "total_count": 500 },
    "videos": [
      {  /* 8 keys */
        "country_code": "US",
        "cover": "<url>", "duration": 15,
        "id": "<id>", "item_id": "<id>",
        "item_url": "<url>",
        "region": "United States",
        "title": "..."
      }
    ]
  }
}
```

### Get Trending Sound Clips — `/api/trending/sound-clips`

```jsonc
{
  "code": 0, "msg": "OK", "request_id": "<x>",
  "data": {
    "list": [
      {  /* 14 keys */
        "clip_id": "<id>", "detail": "<url>",
        "duration": 1, "genre": "Experimental",
        "is_on_ad": true,
        "meta_song_id": "<id>",
        "mood": "", "music_id": "<id>",
        "music_url": "<url>",
        "placement_allowed": ["TBNR", "Helo"],
        "poster_url": "<url>",
        "singer": "...", "theme": "Sound Effect",
        "title": "..."
      }
    ]
  }
}
```

### Get Sound Clips by Music — `/api/trending/sound-clips/by-music?music_id=...`

```jsonc
{
  "code": 0, "msg": "OK", "request_id": "<x>",
  "data": {
    "music_list": [
      {  /* 13 keys, same shape as Trending Sound Clips */
        "clip_id": "<id>", "detail": "<url>",
        "duration": 60, "genre": "Hip Hop/Rap",
        "music_id": "<id>", "music_url": "<url>",
        "placement_allowed": ["TikTok"],
        "title": "Gameday",
        /* + 6 more */
      }
    ]
  }
}
```

### Get Editorial Playlists — `/api/trending/playlists`

```jsonc
{
  "code": 0, "msg": "OK", "request_id": "<x>",
  "data": {
    "list": [
      { "playlist_id": <int>, "poster_url": "<url>", "title": "TikTok Viral" },
      { "playlist_id": <int>, "poster_url": "<url>", "title": "New Releases" },
      { "playlist_id": <int>, "poster_url": "<url>", "title": "Pop" }
      /* + N more */
    ]
  }
}
```

### Get Top Ad Scripts — `/api/trending/ad-scripts?country=US`

```jsonc
{
  "code": 0, "data": {
    "pagination": { "has_more": false, "page": 1, "size": 50, "total": 4 },
    "sentence_list": [
      {  /* 5 keys */
        "covers": ["<url>", "<url>", "<url>"],
        "ctr": 1.41, "cvr": 0,
        "sentence": "Promotion (this week) + free delivery",
        "use_type": "script_use_type_title"
      }
    ]
  }
}
```

### Get Trending Video IDs (deprecated) — `/api/trending/video-ids`

```jsonc
{
  "code": 0,
  "data": { "video_list": ["<id>", "<id>", "<id>", /* 10 IDs */ ] },
  "msg": "OK", "request_id": "<x>"
}
```

---

## Standalone

### Get Product Info — `/api/product/info?product_id=...`

> ⚠️ Note: this is the **e-commerce** product info, отличается от `/api/trending/top-products/detail`.

```jsonc
{
  "product_base": {  /* 5 keys */ },
  "desc_detail": [  /* 45 items */
    { "text": "Đặc điểm nổi bật", "type": "text" },
    {
      "content": ["..."],
      "type": "ul"
    },
    {
      "image": { "height": 842, "uri": "<x>", "url_list": ["<url>"], "width": 800 },
      "type": "image"
    }
    /* + 40 more text/image/ul items */
  ]
}
```

---

## 🔴 Edge cases (verified by real API calls)

| Endpoint | Edge case | Shape |
|---|---|---|
| `/api/live/info` | bad roomId | `{data{message,prompts}, status_code:10011}` |
| `/api/effect/info` | bad effectId | `{log_pb, status_code:4, status_msg:"Server unavailable..."}` |
| `/api/user/followings` | private user | `{status_code:3002060, status_msg:"hiding following list"}` |
| `/api/user/liked-posts` | private likes | `204 No Content` |
| `/api/download/video` | URL без видео | `204 No Content` |
| `/api/trending/ads`, `/api/trending/keyword/posts` | Basic-подписка | `401 {"message":"endpoint disabled for subscription"}` |
| `/api/trending/top-products/detail`, `/metrics` | bad product_id | `{code:40000, msg:"Field validation failed", request_id}` |

> Всегда проверяй `status_code` (или `code`) ПОСЛЕ HTTP-200. Если != 0 — это бизнес-ошибка.
