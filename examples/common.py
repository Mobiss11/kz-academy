"""Общая обвязка для всех примеров RapidAPI.

Использование:
    from examples.common import build_session

    session = build_session(host="yt-api.p.rapidapi.com")
    r = session.get("https://yt-api.p.rapidapi.com/search", params={"query": "..."})
"""

from __future__ import annotations

import os
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

try:
    from dotenv import load_dotenv

    load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")
except ImportError:  # pragma: no cover
    # python-dotenv не обязателен, но сильно облегчает жизнь
    pass


class RapidAPIKeyMissing(RuntimeError):
    """Ключ RAPIDAPI_KEY не найден ни в окружении, ни в .env."""


def get_api_key() -> str:
    key = os.environ.get("RAPIDAPI_KEY")
    if not key:
        raise RapidAPIKeyMissing(
            "RAPIDAPI_KEY не задан. Скопируй .env.example в .env и пропиши ключ, "
            "либо экспортируй переменную окружения вручную."
        )
    return key


def build_session(
    host: str,
    *,
    timeout: int = 15,
    retries: int = 3,
    cache_seconds: int | None = 3600,
) -> requests.Session:
    """Возвращает requests.Session с правильными хедерами, ретраями и (опционально) кэшем.

    Параметры:
        host: значение для заголовка X-RapidAPI-Host (например 'yt-api.p.rapidapi.com').
        timeout: таймаут на запрос (секунды). Применяется через адаптер.
        retries: число повторных попыток при 429/5xx.
        cache_seconds: TTL кэша; если None — кэш отключён.
    """
    if cache_seconds is not None:
        try:
            import requests_cache

            session: requests.Session = requests_cache.CachedSession(
                cache_name="rapidapi_cache",
                expire_after=cache_seconds,
            )
        except ImportError:
            session = requests.Session()
    else:
        session = requests.Session()

    session.headers.update(
        {
            "X-RapidAPI-Key": get_api_key(),
            "X-RapidAPI-Host": host,
            "Accept": "application/json",
        }
    )

    retry = Retry(
        total=retries,
        backoff_factor=1.0,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET", "POST"]),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    # сохраним таймаут как атрибут — пусть вызывающий код применяет сам
    session.request_timeout = timeout  # type: ignore[attr-defined]
    return session


def get_json(session: requests.Session, url: str, **kwargs) -> dict:
    """Тонкая обёртка: GET + raise_for_status + .json()."""
    timeout = kwargs.pop("timeout", getattr(session, "request_timeout", 15))
    response = session.get(url, timeout=timeout, **kwargs)
    response.raise_for_status()
    return response.json()
