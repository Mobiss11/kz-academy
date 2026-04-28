# Telegram Channel (akrakoro) — verified response shapes

> ✅ **Источник:** оба эндпоинта прозвонены реальными API-вызовами на Basic-плане. Минимальный, простой коннектор.

## `GET /channel/info?channel=<username>` → 200

```jsonc
{
  "verified": true,
  "chat_type": "channel",       // или "supergroup"
  "title": "Telegram News",
  "description": "...",
  "members_count": 8500000,
  "photo": "<url>",             // подписанный CDN-URL аватарки
  "username": "telegram",
  "id": -1001006503122           // числовой Telegram chat_id (отрицательный для каналов)
}
```

## `GET /channel/messages?channel=<username>&limit=10` → 200

```jsonc
{
  "messages": [
    {
      "id": 12345,                       // message_id внутри канала
      "date": 1700000000,                // unix timestamp
      "text": "...",                     // text body или caption
      "views": 1234567,                  // просмотры на момент запроса
      "forwards": 1234,                  // репосты
      "replies_count": 56,
      "reactions": [
        { "emoji": "🔥", "count": 1234 },
        { "emoji": "❤️", "count": 567 }
      ],
      "media_type": "photo",             // null | "photo" | "video" | "document"
      "media_url": "<url>",              // если есть медиа — подписанная CDN-ссылка
      "url": "https://t.me/telegram/12345"
    }
  ],
  "has_more": true,
  "offset": 12340                        // передавай в `offset_id` для следующей страницы
}
```

## Edge cases

| Сценарий | Ответ |
|---|---|
| Несуществующий канал | `404 {"error": "channel not found"}` |
| Приватный канал | `403 {"error": "channel is private"}` |
| Превышение Basic-лимита (100/мес) | `429 Too Many Requests` |

## Пагинация

`/channel/messages` использует обратную пагинацию (от новых к старым):

```python
offset = None
while True:
    params = {"channel": "telegram", "limit": 50}
    if offset:
        params["offset_id"] = offset
    r = requests.get(url, headers=headers, params=params).json()
    for m in r["messages"]:
        process(m)
    if not r["has_more"]:
        break
    offset = r["offset"]
```
