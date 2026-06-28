from datetime import datetime
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from main import app, todos
from schemas import Todo

client = TestClient(app)

SEED_ID = uuid4()


@pytest.fixture(autouse=True)
def reset_state():
    todos.clear()
    todos.append(Todo(id=SEED_ID, title="Test todo", created_at=datetime.now()))


def test_create_todo():
    response = client.post("/todos", json={"title": "New task"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New task"
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data


def test_list_todos():
    response = client.get("/todos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test todo"


def test_get_todo():
    response = client.get(f"/todos/{SEED_ID}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test todo"


def test_get_todo_not_found():
    response = client.get(f"/todos/{uuid4()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


def test_update_todo():
    response = client.put(
        f"/todos/{SEED_ID}",
        json={"title": "Updated", "completed": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated"
    assert data["completed"] is True


def test_delete_todo():
    response = client.delete(f"/todos/{SEED_ID}")
    assert response.status_code == 204
    response = client.get("/todos")
    assert len(response.json()) == 0
