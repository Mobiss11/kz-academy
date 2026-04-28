#!/usr/bin/env python3
"""Smoke-test: проверяет что .env настроен и сервисы доступны.

Запускай ПЕРЕД тем как делать что-то серьёзное:
    python scripts/check_env.py

Скрипт по очереди:
- Проверяет наличие переменных в .env
- Делает 1 пробный запрос к каждому сконфигурированному сервису
- Выдаёт чёткий диагноз: что работает, что нет, что не настроено

Не настроенные сервисы не считаются ошибкой — это OK,
ты можешь использовать только часть стека.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except ImportError:
    pass  # без dotenv будем читать из process env


GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
DIM = "\033[2m"
RESET = "\033[0m"


def ok(msg: str) -> None:
    print(f"{GREEN}✓{RESET} {msg}")


def warn(msg: str) -> None:
    print(f"{YELLOW}~{RESET} {msg}")


def err(msg: str) -> None:
    print(f"{RED}✗{RESET} {msg}")


def skip(msg: str) -> None:
    print(f"{DIM}-{RESET} {DIM}{msg}{RESET}")


# ============================================================
# 1. RapidAPI
# ============================================================

def check_rapidapi() -> bool:
    print("\n[1/8] RapidAPI")
    key = os.environ.get("RAPIDAPI_KEY")
    if not key or key == "your-rapidapi-key-here":
        err("RAPIDAPI_KEY не установлен в .env (или оставлен placeholder)")
        print("    → Возьми ключ: https://rapidapi.com/developer/security")
        return False

    import requests

    # Проверяем минимальный коннектор — telegram-channel /channel/info
    try:
        r = requests.get(
            "https://telegram-channel.p.rapidapi.com/channel/info",
            headers={
                "X-RapidAPI-Key": key,
                "X-RapidAPI-Host": "telegram-channel.p.rapidapi.com",
            },
            params={"channel": "telegram"},
            timeout=10,
        )
        if r.status_code == 200:
            ok(f"RapidAPI ключ валиден, telegram-channel отвечает 200")
            return True
        elif r.status_code == 401:
            err("RapidAPI вернул 401 — ключ невалиден")
            return False
        elif r.status_code == 403:
            warn("RapidAPI вернул 403 — ключ ОК, но не подписан на telegram-channel")
            print("    → https://rapidapi.com/akrakoro/api/telegram-channel/pricing")
            print("    → Это OK для других коннекторов — проверь те что нужны.")
            return True
        elif r.status_code == 429:
            warn("RapidAPI вернул 429 — превышен лимит. Подожди или возьми платный план.")
            return True
        else:
            err(f"RapidAPI вернул {r.status_code}: {r.text[:200]}")
            return False
    except Exception as e:
        err(f"Не удалось подключиться к RapidAPI: {e}")
        return False


# ============================================================
# 2. OpenRouter
# ============================================================

def check_openrouter() -> bool:
    print("\n[2/8] OpenRouter (LLM)")
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        skip("OPENROUTER_API_KEY не установлен — этот сервис не используется (это OK)")
        return True

    import requests

    try:
        r = requests.get(
            "https://openrouter.ai/api/v1/auth/key",
            headers={"Authorization": f"Bearer {key}"},
            timeout=10,
        )
        if r.status_code == 200:
            data = r.json().get("data", {})
            limit = data.get("limit") or "?"
            usage = data.get("usage") or 0
            ok(f"OpenRouter ключ валиден. Использовано: ${usage:.4f} из ${limit}")
            return True
        else:
            err(f"OpenRouter вернул {r.status_code}: {r.text[:200]}")
            return False
    except Exception as e:
        err(f"Не удалось подключиться к OpenRouter: {e}")
        return False


# ============================================================
# 3. Транскрипция (any of)
# ============================================================

def check_transcription() -> bool:
    print("\n[3/8] Транскрипция")
    if os.environ.get("OPENAI_API_KEY"):
        # Не делаем реальный вызов — только check ключа
        ok("OPENAI_API_KEY установлен (Whisper API)")
        return True
    if os.environ.get("REPLICATE_API_TOKEN"):
        ok("REPLICATE_API_TOKEN установлен (Replicate Whisper)")
        return True
    if os.environ.get("DEEPGRAM_API_KEY"):
        ok("DEEPGRAM_API_KEY установлен")
        return True
    if os.environ.get("YANDEX_API_KEY"):
        ok("YANDEX_API_KEY установлен (SpeechKit)")
        return True
    skip("Транскрипция не настроена (это OK если pipeline без транскрипции)")
    return True


# ============================================================
# 4. S3 Storage (any of)
# ============================================================

def check_storage() -> bool:
    print("\n[4/8] S3 Storage")
    if os.environ.get("AWS_ACCESS_KEY_ID"):
        ok("AWS_ACCESS_KEY_ID установлен")
        return True
    if os.environ.get("R2_ACCESS_KEY_ID"):
        ok("R2_ACCESS_KEY_ID установлен (Cloudflare R2)")
        return True
    if os.environ.get("YC_ACCESS_KEY"):
        ok("YC_ACCESS_KEY установлен (Yandex Object Storage)")
        return True
    skip("S3 не настроен (это OK если не качаешь медиа)")
    return True


# ============================================================
# 5. Telegram Bot
# ============================================================

def check_telegram() -> bool:
    print("\n[5/8] Telegram Bot")
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        skip("TELEGRAM_BOT_TOKEN не установлен (это OK если нет уведомлений)")
        return True

    import requests

    try:
        r = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=10)
        if r.status_code == 200:
            data = r.json().get("result", {})
            ok(f"Telegram bot @{data.get('username', '?')} работает")
            return True
        else:
            err(f"Telegram вернул {r.status_code}: невалидный токен?")
            return False
    except Exception as e:
        err(f"Не удалось подключиться к Telegram: {e}")
        return False


# ============================================================
# 6. PostgreSQL
# ============================================================

def check_postgres() -> bool:
    print("\n[6/8] PostgreSQL")
    url = os.environ.get("DATABASE_URL")
    if not url:
        skip("DATABASE_URL не установлен (это OK для MVP с SQLite)")
        return True

    try:
        import psycopg2  # type: ignore

        conn = psycopg2.connect(url, connect_timeout=5)
        with conn.cursor() as cur:
            cur.execute("SELECT version()")
            version = cur.fetchone()[0]
        conn.close()
        ok(f"PostgreSQL подключение OK: {version[:50]}")
        return True
    except ImportError:
        warn("psycopg2 не установлен — пропуск проверки. pip install psycopg2-binary")
        return True
    except Exception as e:
        err(f"PostgreSQL не отвечает: {e}")
        return False


# ============================================================
# 7. Redis
# ============================================================

def check_redis() -> bool:
    print("\n[7/8] Redis")
    url = os.environ.get("REDIS_URL")
    if not url:
        skip("REDIS_URL не установлен (это OK на старте)")
        return True

    try:
        import redis  # type: ignore

        r = redis.from_url(url, socket_connect_timeout=5)
        if r.ping():
            ok("Redis отвечает на PING")
            return True
        err("Redis не отвечает")
        return False
    except ImportError:
        warn("redis-py не установлен — пропуск проверки. pip install redis")
        return True
    except Exception as e:
        err(f"Redis не отвечает: {e}")
        return False


# ============================================================
# 8. Python окружение
# ============================================================

def check_python() -> bool:
    print("\n[8/8] Python окружение")
    version = sys.version_info
    if version >= (3, 10):
        ok(f"Python {version.major}.{version.minor}.{version.micro}")
    else:
        err(f"Python {version.major}.{version.minor} — нужен 3.10+")
        return False

    # Проверяем что requests и dotenv установлены
    try:
        import requests  # noqa: F401
        ok("requests установлен")
    except ImportError:
        err("requests не установлен. pip install -e .")
        return False

    try:
        import dotenv  # noqa: F401
        ok("python-dotenv установлен")
    except ImportError:
        warn("python-dotenv не установлен (рекомендуется). pip install python-dotenv")

    return True


# ============================================================
# Main
# ============================================================

def main() -> int:
    print("=" * 60)
    print(" RapidAPI Helper — Environment Check")
    print("=" * 60)

    checks = [
        check_python,
        check_rapidapi,
        check_openrouter,
        check_transcription,
        check_storage,
        check_telegram,
        check_postgres,
        check_redis,
    ]

    results = [c() for c in checks]
    failures = sum(1 for r in results if r is False)

    print("\n" + "=" * 60)
    if failures == 0:
        print(f"{GREEN}✓ Всё настроено корректно. Можно работать.{RESET}")
        return 0
    else:
        print(f"{RED}✗ {failures} проблем. Открой docs/full-stack-setup.md и исправь.{RESET}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
