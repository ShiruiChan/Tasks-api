# Базовый лёгкий образ Python
FROM python:3.11-slim

# Не писать .pyc и не буферизовать вывод (логи сразу видны)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Сначала зависимости — для кэширования слоёв Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Затем код приложения
COPY app ./app

# Порт, на котором слушает сервис (хостинги пробрасывают $PORT)
EXPOSE 8000

# Запуск через gunicorn с воркерами uvicorn (ASGI)
CMD ["sh", "-c", "gunicorn app.main:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:${PORT:-8000}"]
