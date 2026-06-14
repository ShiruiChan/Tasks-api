# Tasks API

Учебный REST API-сервис для управления задачами (to-do list).
Проект по теме **«Тестирование и деплой»**: покрыт unit-тестами (pytest),
упакован в Docker и развёрнут на внешнем хостинге.

Стек: **Python 3.11 · FastAPI · Uvicorn/Gunicorn · pytest · Docker**.

## Демо

- Хостинг: `https://tasks-api-v04c.onrender.com`
- Документация Swagger UI: `https://tasks-api-v04c.onrender.com/docs`

## Возможности

| Метод    | Путь            | Описание                          |
|----------|-----------------|-----------------------------------|
| `GET`    | `/`             | Информация о сервисе              |
| `GET`    | `/health`       | Проверка работоспособности        |
| `GET`    | `/tasks`        | Список всех задач                 |
| `POST`   | `/tasks`        | Создать задачу                    |
| `GET`    | `/tasks/{id}`   | Получить задачу по id             |
| `PATCH`  | `/tasks/{id}`   | Обновить задачу                   |
| `DELETE` | `/tasks/{id}`   | Удалить задачу                    |

## Структура проекта

```
tasks-api/
├── app/
│   ├── __init__.py
│   ├── main.py         # маршруты FastAPI
│   ├── models.py       # Pydantic-модели
│   └── storage.py      # хранилище задач (in-memory)
├── tests/
│   ├── conftest.py     # фикстуры pytest
│   └── test_api.py     # тесты API (13 шт.)
├── examples/
│   ├── requests.sh                     # примеры curl-запросов
│   └── TasksAPI.postman_collection.json# коллекция Postman
├── Dockerfile
├── render.yaml         # конфиг деплоя на Render
├── Procfile            # запуск на Railway/Heroku-совместимых
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
└── README.md
```

## Локальный запуск

### Вариант 1. Через Python (venv)

```bash
# 1. Клонировать репозиторий
git clone https://github.com/<username>/tasks-api.git
cd tasks-api

# 2. Создать виртуальное окружение и установить зависимости
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

# 3. Запустить сервер
uvicorn app.main:app --reload
```

Сервис доступен на http://localhost:8000, документация - http://localhost:8000/docs

### Вариант 2. Через Docker

```bash
# Собрать образ
docker build -t tasks-api .

# Запустить контейнер
docker run -p 8000:8000 tasks-api
```

## Запуск тестов

```bash
pip install -r requirements-dev.txt
pytest
```

Ожидаемый результат: `13 passed`.

## Примеры запросов (curl)

```bash
# Проверка здоровья
curl http://localhost:8000/health
# {"status":"ok"}

# Создать задачу
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Сделать проект", "description": "Тестирование и деплой"}'
# {"id":1,"title":"Сделать проект","description":"Тестирование и деплой","done":false,"created_at":"..."}

# Список задач
curl http://localhost:8000/tasks

# Отметить выполненной
curl -X PATCH http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'

# Удалить
curl -X DELETE http://localhost:8000/tasks/1
```

Готовый скрипт со всеми запросами - `examples/requests.sh`.
Коллекция для Postman - `examples/TasksAPI.postman_collection.json`.

## Деплой

### Render (рекомендуется, есть бесплатный план)

1. Залить код в репозиторий на GitHub.
2. На [render.com](https://render.com) → **New → Web Service** → подключить репозиторий.
3. Render автоматически прочитает `render.yaml` (Blueprint), либо укажите вручную:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn app.main:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT`
   - **Health check path:** `/health`
4. После деплоя сервис доступен по адресу `https://<имя>.onrender.com`.

### Railway

1. [railway.app](https://railway.app) → **New Project → Deploy from GitHub repo**.
2. Railway определит Python-проект и `Procfile` автоматически.

### VPS (screen + gunicorn + nginx)

```bash
# на сервере
git clone https://github.com/<username>/tasks-api.git && cd tasks-api
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# запустить gunicorn в фоне через screen
screen -S tasks
gunicorn app.main:app -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8000
# Ctrl+A, D - отсоединиться от screen (процесс продолжит работать)
```

Конфиг nginx как реверс-прокси:

```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Автор

Афанасьев Афанасий Егорович - ПМИ-ИИ-23, г. Якутск, 2025.
