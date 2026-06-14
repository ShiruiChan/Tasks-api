"""Точка входа FastAPI-приложения: маршруты REST API."""

from typing import List

from fastapi import FastAPI, HTTPException, status

from . import __version__
from .models import Task, TaskCreate, TaskUpdate
from .storage import store

app = FastAPI(
    title="Tasks API",
    description="Учебный REST-сервис для управления задачами (тестирование и деплой).",
    version=__version__,
)


@app.get("/", tags=["service"])
def root() -> dict:
    """Корневой эндпоинт со ссылкой на документацию."""
    return {"service": "Tasks API", "version": __version__, "docs": "/docs"}


@app.get("/health", tags=["service"])
def health() -> dict:
    """Проверка работоспособности (для хостинга/мониторинга)."""
    return {"status": "ok"}


@app.get("/tasks", response_model=List[Task], tags=["tasks"])
def list_tasks() -> List[dict]:
    """Получить список всех задач."""
    return store.list()


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate) -> dict:
    """Создать новую задачу."""
    return store.create(payload.title, payload.description)


@app.get("/tasks/{task_id}", response_model=Task, tags=["tasks"])
def get_task(task_id: int) -> dict:
    """Получить задачу по идентификатору."""
    task = store.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task


@app.patch("/tasks/{task_id}", response_model=Task, tags=["tasks"])
def update_task(task_id: int, payload: TaskUpdate) -> dict:
    """Частично обновить задачу (название, описание, статус выполнения)."""
    task = store.update(task_id, payload.model_dump(exclude_unset=True))
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: int) -> None:
    """Удалить задачу."""
    if not store.delete(task_id):
        raise HTTPException(status_code=404, detail="Задача не найдена")
