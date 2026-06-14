"""Общие фикстуры pytest."""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage import store


@pytest.fixture
def client():
    """Тестовый клиент с чистым хранилищем перед каждым тестом."""
    store.clear()
    with TestClient(app) as test_client:
        yield test_client
