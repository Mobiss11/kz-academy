# Threads API (Lundehund) — verified response shapes

> ✅ **Источник:** все 12 эндпоинтов имеют Example Response в RapidAPI Playground (захвачены в основной карточке `connectors/threads-api4.md`). Один edge case прозвонен реально 2026-04-28.
>
> Threads API — это GraphQL поверх REST. Все ответы обёрнуты в `{ data: {...}, errors: [], extensions: {...}, status: "ok" }`.

## Edge case (verified 2026-04-28)

### `GET /api/post/comments?post_id=<bad_id>` → 200 + GraphQL error

```jsonc
{
  "errors": [
    {
      "message": "execution error",
      "path": ["data"],
      "severity": "CRITICAL"
    }
  ],
  "data": null,
  "extensions": {
    "is_final": true,
    "server_metadata": {
      "request_start_time_ms": <ts>,
      "time_at_flush_ms": <ts>
    }
  },
  "status": "ok"
}
```

> ⚠️ **Всегда проверяй `data !== null`** перед обработкой ответа. HTTP `200` + `errors[]` + `data: null` — это бизнес-ошибка (несуществующий/удалённый post_id), а не успех.

## Полные shape'ы

См. [`connectors/threads-api4.md`](../threads-api4.md) — там Example Responses из playground с валидными данными для:

- `/api/user/info`, `/api/user/posts`, `/api/user/followers`, `/api/user/following`
- `/api/post/detail`, `/api/post/comments` (на валидных post_id), `/api/post/quotes`, `/api/post/reposts`
- `/api/search/top`, `/api/search/users`, `/api/search/tag`
- `/api/feed/recommended`
