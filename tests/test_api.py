import pytest


def test_healthz_reports_service_is_running(client):
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_tasks_starts_empty(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_create_task_defaults_to_incomplete(client):
    response = client.post("/tasks", json={"title": "Write API docs"})

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "Write API docs",
        "completed": False,
        "priority": "low",
    }


@pytest.mark.parametrize("priority", ["low", "medium", "high"])
def test_create_task_accepts_priority(client, priority):
    response = client.post(
        "/tasks",
        json={"title": "Write API docs", "priority": priority},
    )

    assert response.status_code == 201
    assert response.json()["priority"] == priority


def test_create_task_rejects_invalid_priority(client):
    response = client.post(
        "/tasks",
        json={"title": "Write API docs", "priority": "urgent"},
    )

    assert response.status_code == 422


@pytest.mark.parametrize("title", ["", " \t\n"])
def test_create_task_rejects_empty_or_whitespace_only_title(client, title):
    response = client.post("/tasks", json={"title": title})

    assert response.status_code == 422


def test_created_task_appears_in_list(client):
    created = client.post(
        "/tasks",
        json={"title": "Review test feedback", "completed": True},
    )

    listed = client.get("/tasks")

    assert created.status_code == 201
    assert listed.status_code == 200
    assert listed.json() == [created.json()]


def test_list_tasks_orders_by_priority_highest_first(client):
    for title, priority in [
        ("Low priority task", "low"),
        ("Medium priority task", "medium"),
        ("High priority task", "high"),
    ]:
        client.post("/tasks", json={"title": title, "priority": priority})

    response = client.get("/tasks")

    assert response.status_code == 200
    assert [task["priority"] for task in response.json()] == [
        "high",
        "medium",
        "low",
    ]
