"""Pydantic-модели запросов и ответов."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """Данные для создания задачи."""

    title: str = Field(..., min_length=1, max_length=200, description="Название задачи")
    description: str = Field("", max_length=2000, description="Описание задачи")


class TaskUpdate(BaseModel):
    """Данные для частичного обновления задачи."""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    done: Optional[bool] = None


class Task(BaseModel):
    """Модель задачи в ответах API."""

    id: int
    title: str
    description: str
    done: bool
    created_at: datetime
