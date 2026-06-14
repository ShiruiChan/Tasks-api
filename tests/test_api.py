"""Unit/интеграционные тесты REST API (pytest + FastAPI TestClient)."""


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_root(client):
    resp = client.get("/")
    assert resp.status_code == 200
    body = resp.json()
    assert body["service"] == "Tasks API"
    assert "version" in body


def test_list_empty(client):
    resp = client.get("/tasks")
    assert resp.status_code == 200
    assert resp.json() == []


def test_create_task(client):
    resp = client.post(
        "/tasks", json={"title": "Купить хлеб", "description": "в магазине"}
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["id"] == 1
    assert body["title"] == "Купить хлеб"
    assert body["description"] == "в магазине"
    assert body["done"] is False
    assert "created_at" in body


def test_create_task_minimal(client):
    resp = client.post("/tasks", json={"title": "Без описания"})
    assert resp.status_code == 201
    assert resp.json()["description"] == ""


def test_create_task_validation_error(client):
    # Пустой title недопустим
    resp = client.post("/tasks", json={"title": ""})
    assert resp.status_code == 422


def test_get_task(client):
    created = client.post("/tasks", json={"title": "Задача"}).json()
    resp = client.get(f"/tasks/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == created["id"]


def test_get_task_not_found(client):
    resp = client.get("/tasks/999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Задача не найдена"


def test_update_task(client):
    created = client.post("/tasks", json={"title": "Старое"}).json()
    resp = client.patch(
        f"/tasks/{created['id']}", json={"title": "Новое", "done": True}
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["title"] == "Новое"
    assert body["done"] is True


def test_update_task_not_found(client):
    resp = client.patch("/tasks/999", json={"done": True})
    assert resp.status_code == 404


def test_delete_task(client):
    created = client.post("/tasks", json={"title": "Удалить меня"}).json()
    resp = client.delete(f"/tasks/{created['id']}")
    assert resp.status_code == 204
    # Повторное получение - 404
    assert client.get(f"/tasks/{created['id']}").status_code == 404


def test_delete_task_not_found(client):
    resp = client.delete("/tasks/999")
    assert resp.status_code == 404


def test_full_flow(client):
    """Сквозной сценарий: создать несколько, обновить, удалить, проверить список."""
    client.post("/tasks", json={"title": "A"})
    client.post("/tasks", json={"title": "B"})
    assert len(client.get("/tasks").json()) == 2

    client.patch("/tasks/1", json={"done": True})
    client.delete("/tasks/2")

    tasks = client.get("/tasks").json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == 1
    assert tasks[0]["done"] is True
