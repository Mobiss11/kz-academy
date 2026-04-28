FROM python:3.12-slim

WORKDIR /app

# Сначала зависимости, чтобы кэш слоёв работал
COPY pyproject.toml README.md ./
RUN pip install --no-cache-dir -e ".[dev]"

# Потом исходники
COPY . .

# Дефолтная команда — показать список доступных примеров
CMD ["python", "-c", "import os; [print(' -', f) for f in sorted(os.listdir('examples/yt_api')) if f.endswith('.py') and not f.startswith('_')]"]
