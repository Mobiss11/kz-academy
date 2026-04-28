# Getting Started — от нуля до первого запроса

Этот гайд проведёт тебя по полному пути: регистрация на RapidAPI → получение API-ключа → подписка на конкретный коннектор → первый рабочий запрос. Если ты впервые слышишь про RapidAPI — начинай отсюда.

> 🕐 Время на прохождение: 15–20 минут
> 💳 **Понадобится банковская карта** (даже для бесплатных Basic-планов RapidAPI просит привязать карту в качестве защиты от абуза. Денег с неё не списывают, пока ты не выходишь за лимит free-плана).

## Шаг 1. Регистрация на RapidAPI

1. Открой [rapidapi.com](https://rapidapi.com/).
2. Нажми **Sign Up** в правом верхнем углу.
3. Зарегистрируйся через **Google**, **GitHub** или **email** — что удобнее.
4. Подтверди email если требуется.

После регистрации ты попадёшь в [RapidAPI Hub](https://rapidapi.com/hub) — это каталог всех API.

## Шаг 2. Получи API-ключ

У тебя автоматически создаётся **default-application** с уникальным API-ключом. Этот ключ нужно вставить в `.env` нашего репо.

1. Открой [Apps Dashboard](https://rapidapi.com/developer/dashboard) — там список твоих приложений.
2. Кликни на `default-application` (или создай новое).
3. Перейди во вкладку **Security** или открой напрямую: [https://rapidapi.com/developer/security](https://rapidapi.com/developer/security).
4. Скопируй значение **Application Key** (это длинная строка вида `abc123def456...`).

> ⚠️ **Это секрет.** Никогда не публикуй ключ в GitHub, не отправляй в чат, не делись скриншотом. Если случайно слил — нажми **Rotate** на той же странице, ключ перевыпустится.

## Шаг 3. Подпишись на конкретный API (КРИТИЧЕСКИЙ ШАГ!)

> 💡 **Ключевой момент, который часто упускают.** Один API-ключ работает со всеми API на RapidAPI, **но для каждого API нужно отдельно оформить подписку**. Без подписки любой запрос вернёт `403 You are not subscribed to this API`.

Каждый коннектор в этом репо имеет свою страницу с тарифами. Прямые ссылки:

| Коннектор | Страница API | Subscribe (Pricing) |
|---|---|---|
| YT-API | https://rapidapi.com/ytjar/api/yt-api | https://rapidapi.com/ytjar/api/yt-api/pricing |
| Telegram Channel | https://rapidapi.com/akrakoro/api/telegram-channel | https://rapidapi.com/akrakoro/api/telegram-channel/pricing |
| Threads API | https://rapidapi.com/Lundehund/api/threads-api4 | https://rapidapi.com/Lundehund/api/threads-api4/pricing |
| TikTok API | https://rapidapi.com/Lundehund/api/tiktok-api23 | https://rapidapi.com/Lundehund/api/tiktok-api23/pricing |
| Instagram Looter | https://rapidapi.com/irrors-apis/api/instagram-looter2 | https://rapidapi.com/irrors-apis/api/instagram-looter2/pricing |

### Как оформить Basic (free) подписку

1. Открой Pricing-страницу нужного API (см. таблицу выше).
2. Найди план **Basic** (или с пометкой `$0.00 /mo`).
3. Нажми **Subscribe / Start Free Plan**.
4. Если RapidAPI попросит карту — привяжи. Деньги не спишутся, пока ты в рамках free-плана.
5. После подписки увидишь зелёную плашку **Subscribed**.

### Как оформить платный план

Если задача больше Basic-лимита (см. секцию "Тарифы" в карточке коннектора):

1. На той же Pricing-странице выбери Pro / Ultra / Mega.
2. **Перепроверь** какие лимиты у плана — они описаны в карточке коннектора.
3. **Внимание на overage**: на некоторых планах превышение списывается автоматически. Карточка коннектора это явно отмечает.
4. После Subscribe у тебя меняется тарифный план — старые лимиты заменяются новыми.

> 💡 **Можно и нужно начинать с Basic** — он бесплатный, помогает протестировать что всё работает. Переходи на платный план только когда упираешься в лимит.

## Шаг 4. Установи репо и пропиши ключ

```bash
# 1. Клонируй репозиторий (или скачай ZIP с GitHub если не пользуешься git)
git clone https://github.com/Mobiss11/kz-academy.git
cd kz-academy

# 2. Скопируй пример .env и пропиши ключ
cp .env.example .env
# Открой .env в редакторе и вставь свой ключ:
#   RAPIDAPI_KEY=abc123def456...

# 3. Установи Python-зависимости (Python 3.10+)
pip install -e .
```

> 💡 Не пользуешься git? На странице репозитория в GitHub нажми зелёную кнопку **Code** → **Download ZIP**, распакуй, открой папку в терминале, дальше шаги те же со 2-го пункта.

## Шаг 5. Smoke-test — проверь что всё настроено

Перед первым реальным запросом запусти автопроверку:

```bash
python scripts/check_env.py
```

Скрипт проверит все 8 потенциальных сервисов (RapidAPI, OpenRouter, Whisper, S3, Telegram, Postgres, Redis, Python окружение) и скажет:
- ✓ что работает
- ~ что не настроено, но это OK
- ✗ что сломано и нужно чинить

На минимуме (только RapidAPI) увидишь 1 ✓ и 7 пропусков — это нормально.

## Шаг 6. Первый реальный запрос

Проверь что всё работает на самом простом и бесплатном эндпоинте — Telegram channel info:

```bash
python -c "
import os, requests
from dotenv import load_dotenv
load_dotenv()

r = requests.get(
    'https://telegram-channel.p.rapidapi.com/channel/info',
    headers={
        'X-RapidAPI-Key': os.environ['RAPIDAPI_KEY'],
        'X-RapidAPI-Host': 'telegram-channel.p.rapidapi.com',
    },
    params={'channel': 'telegram'},
)
print(r.status_code)
print(r.json())
"
```

**Ожидаемый результат:**

```
200
{'verified': True, 'chat_type': 'channel', 'title': 'Telegram News', ...}
```

Если получил **401** — ключ неправильный или не вставлен в `.env`.
Если получил **403** — не подписан на Telegram Channel API. Вернись к шагу 3 и оформи Basic-план.
Если получил **429** — превышен лимит (на Basic у telegram-channel = 100/мес). Подожди или возьми платный план.

## Шаг 6. Подключи скилл к своему ИИ-инструменту

Теперь нейронка сможет генерировать корректный код по карточкам:

- 🟣 [Claude Code](installation-claude-code.md) — самый удобный вариант (полная поддержка скиллов).
- 🟣 [Claude.ai (Projects)](installation-claude-ai.md) — через Project knowledge.
- 🔵 [Cursor](installation-cursor.md) — через `.cursor/rules/`.
- 🟢 [ChatGPT (Custom GPT / Projects)](installation-chatgpt.md) — через knowledge-файлы.

После подключения попроси своего ИИ:

> Напиши Python-функцию, которая возвращает последние 10 видео автора @mrbeast через TikTok API на RapidAPI.

Если всё настроено — нейронка откроет [connectors/tiktok-api23.md](../connectors/tiktok-api23.md), увидит правильный flow (`uniqueId → /api/user/info → secUid → /api/user/posts`) и выдаст рабочий код.

## Шаг 7. Запусти готовые примеры

В `examples/` лежат рабочие Python-скрипты по каждому коннектору. Запуск:

```bash
# YT-API
python -m examples.yt_api.search "claude api tutorial"
python -m examples.yt_api.video_info dQw4w9WgXcQ
python -m examples.yt_api.trending US

# Telegram Channel
python -m examples.telegram_channel.channel_info telegram
python -m examples.telegram_channel.latest_messages telegram --limit 10

# Threads
python -m examples.threads_api4.user_posts reuters

# TikTok
python -m examples.tiktok_api23.user_videos charlidamelio
python -m examples.tiktok_api23.trending US

# Instagram
python -m examples.instagram_looter2.user_profile zuck
python -m examples.instagram_looter2.hashtag_feed travel
```

Все примеры используют общую обвязку `examples/common.py`: подхватывают ключ из `.env`, добавляют ретраи, кэшируют ответы на час чтобы не сжигать квоту в разработке.

## Шаг 8. Что делать дальше

Теперь когда всё работает:

1. **Прочитай карточку коннектора**, который тебе нужен — там список всех эндпоинтов, тарифы и расчёт расходов.
2. **Спроси ИИ** "сколько мне будет стоить если я хочу делать X" — он посчитает по формуле из карточки.
3. **Стартуй с Basic-плана** — пока он покрывает твои нужды, нет смысла платить.
4. **Закладывай кэш** в любой polling-сценарий — это кратно снижает счёт.
5. **Если нужного коннектора нет в `connectors/`** — добавь сам через `python scripts/new_connector.py --name X --host X.p.rapidapi.com` и заполни карточку. Сделать карточку для нового API — отличная учебная задача.

## FAQ

### Можно ли работать без банковской карты?
К сожалению нет. Даже для Basic ($0/мес) RapidAPI требует привязать карту. Это политика площадки. Если карты нет — попроси преподавателя/коллегу.

### Что будет, если кончится free-лимит?
Зависит от плана. На большинстве free-планов **hard limit**: после превышения вернётся `429 Too Many Requests`, новые запросы заблокируются до начала следующего месяца. На некоторых платных планах есть **soft limit с overage** — превышение списывается автоматически по тарифу за extra-запрос. **Всегда читай "Pricing tab" перед прод-кодом.**

### Можно ли использовать один ключ во многих проектах?
Да, но осторожно: квота **общая** на все проекты с этим ключом. Если хочется изолировать — создай отдельное приложение в [Apps Dashboard](https://rapidapi.com/developer/dashboard) → у каждого свой ключ и своя квота.

### Что если коннектор перестал работать?
- Проверь подписку (на Pricing-странице должно быть **Subscribed**).
- Проверь не превышена ли квота — на той же странице видно usage.
- Зайди в **Discussions** на странице API — провайдеры обычно отвечают за день.
- Проверь карточку коннектора в `connectors/` на пометки про известные проблемы.

### Я хочу использовать API из России / страны где RapidAPI заблокирован
RapidAPI работает через CDN и обычно доступен. Если открывается `rapidapi.com` — ключ будет работать из любой страны (запросы идут на `*.p.rapidapi.com`). Если домен заблокирован — нужен VPN на этапе регистрации/оплаты, но для самих API-вызовов VPN обычно не нужен.

### Где взять деньги для платного плана?
Карта Visa/MasterCard. Криптовалюта не принимается. Российские карты в 2025 чаще всего **не принимаются** — нужна зарубежная (Казахстан, Грузия, Турция, ЕС). Альтернатива — виртуальные карты через Wise, Revolut и т.п.
