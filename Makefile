.PHONY: help install test lint new docker-build docker-test docker-run

help:
	@echo "Команды:"
	@echo "  make install       — установить зависимости (pip install -e .[dev])"
	@echo "  make test          — запустить pytest"
	@echo "  make lint          — линтер markdown"
	@echo "  make new NAME=x HOST=x.p.rapidapi.com  — создать карточку коннектора"
	@echo "  make docker-build  — собрать Docker-образ"
	@echo "  make docker-test   — pytest в Docker"
	@echo "  make docker-run    — запустить пример в Docker"

install:
	pip install -e ".[dev]"

test:
	pytest

lint:
	pymarkdown --config .pymarkdown.json scan SKILL.md README.md connectors/ docs/

new:
	@if [ -z "$(NAME)" ] || [ -z "$(HOST)" ]; then \
		echo "Использование: make new NAME=weather-api HOST=weather-api123.p.rapidapi.com"; \
		exit 1; \
	fi
	python scripts/new_connector.py --name $(NAME) --host $(HOST)

docker-build:
	docker compose build

docker-test:
	docker compose run --rm app pytest

docker-run:
	docker compose run --rm app
