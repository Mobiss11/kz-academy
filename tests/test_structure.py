"""Проверки структуры репозитория и формата карточек коннекторов.

Запускается локально и в CI:
    pytest tests/
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
CONNECTORS_DIR = REPO_ROOT / "connectors"
SKILL_PATH = REPO_ROOT / "SKILL.md"


def get_connector_files() -> list[Path]:
    """Все карточки коннекторов кроме шаблона."""
    return sorted(p for p in CONNECTORS_DIR.glob("*.md") if not p.name.startswith("_"))


def test_skill_md_exists():
    assert SKILL_PATH.exists(), "SKILL.md должен лежать в корне репозитория"


def test_skill_md_has_frontmatter():
    content = SKILL_PATH.read_text(encoding="utf-8")
    assert content.startswith("---\n"), "SKILL.md должен начинаться с frontmatter (---)"
    assert "\nname:" in content[:500], "В frontmatter должно быть поле name"
    assert "\ndescription:" in content[:500], "В frontmatter должно быть поле description"


def test_connectors_dir_exists():
    assert CONNECTORS_DIR.is_dir(), "Должна быть папка connectors/"


def test_template_exists():
    assert (CONNECTORS_DIR / "_template.md").exists(), "Должен быть connectors/_template.md"


def test_at_least_one_connector():
    cards = get_connector_files()
    assert cards, "Должна быть хотя бы одна карточка коннектора в connectors/"


@pytest.mark.parametrize("path", get_connector_files(), ids=lambda p: p.name)
def test_connector_card_has_required_sections(path: Path):
    """Каждая карточка должна содержать ключевые разделы.

    Каждый элемент `required` — список альтернативных формулировок;
    карточка считается валидной, если присутствует хотя бы одна из них.
    """
    text = path.read_text(encoding="utf-8")
    required: list[list[str]] = [
        ["Base URL"],
        ["Host-заголовок"],
        ["Авторизация"],
        ["Минимальный рабочий пример", "Минимальные рабочие примеры"],
    ]
    missing = [variants[0] for variants in required if not any(v in text for v in variants)]
    assert not missing, f"{path.name}: не хватает разделов {missing}"


@pytest.mark.parametrize("path", get_connector_files(), ids=lambda p: p.name)
def test_connector_card_starts_with_h1(path: Path):
    first_line = path.read_text(encoding="utf-8").splitlines()[0]
    assert first_line.startswith("# "), f"{path.name}: первая строка должна быть заголовком H1"


@pytest.mark.parametrize("path", get_connector_files(), ids=lambda p: p.name)
def test_connector_filename_is_kebab_case(path: Path):
    stem = path.stem
    assert re.fullmatch(r"[a-z0-9][a-z0-9-]*[a-z0-9]", stem), (
        f"{path.name}: имя файла должно быть в kebab-case (a-z, 0-9, дефисы)"
    )
