# Подключение к Claude Code

[Claude Code](https://docs.claude.com/en/docs/claude-code/overview) поддерживает скиллы из коробки. Положи репозиторий рядом с проектом и Claude Code подхватит `SKILL.md` автоматически.

## Вариант 1: проектный скилл

В корне твоего проекта создай папку `.claude/skills/` и склонируй туда репо:

```bash
mkdir -p .claude/skills
git clone https://github.com/Mobiss11/kz-academy.git .claude/skills/kz-academy
```

Claude Code будет видеть скилл только в этом проекте.

## Вариант 2: глобальный скилл

Чтобы скилл был доступен во всех проектах, положи его в домашнюю директорию:

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/Mobiss11/kz-academy.git ~/.claude/skills/kz-academy
```

## Проверка

Запусти Claude Code и спроси:

> Помоги мне сделать запрос к yt-api на RapidAPI для поиска видео

Claude должен сам открыть `SKILL.md` и `connectors/yt-api.md`. Если этого не происходит — проверь, что `description` в frontmatter `SKILL.md` достаточно конкретный (он используется для активации скилла).

## Обновление

```bash
cd ~/.claude/skills/kz-academy  # или .claude/skills/kz-academy
git pull
```
