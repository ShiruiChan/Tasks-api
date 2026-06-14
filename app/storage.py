"""Хранилище задач в оперативной памяти.

Для учебного проекта используется простое in-memory хранилище.
В реальном проекте здесь была бы база данных (PostgreSQL и т.п.).
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional


class TaskStore:
    """Потокобезопасное по уровню процесса хранилище задач."""

    def __init__(self) -> None:
        self._tasks: Dict[int, dict] = {}
        self._next_id: int = 1

    def clear(self) -> None:
        """Очистить хранилище (используется в тестах)."""
        self._tasks.clear()
        self._next_id = 1

    def list(self) -> List[dict]:
        return list(self._tasks.values())

    def get(self, task_id: int) -> Optional[dict]:
        return self._tasks.get(task_id)

    def create(self, title: str, description: str) -> dict:
        task = {
            "id": self._next_id,
            "title": title,
            "description": description,
            "done": False,
            "created_at": datetime.now(timezone.utc),
        }
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def update(self, task_id: int, fields: dict) -> Optional[dict]:
        task = self._tasks.get(task_id)
        if task is None:
            return None
        for key, value in fields.items():
            if value is not None:
                task[key] = value
        return task

    def delete(self, task_id: int) -> bool:
        return self._tasks.pop(task_id, None) is not None


# Единый экземпляр хранилища на всё приложение.
store = TaskStore()
