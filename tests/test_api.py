from datetime import date, timedelta

import pytest

import app.main as task_api


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
        "due_date": None,
    }


def test_create_task_accepts_due_date(client):
    response = client.post(
        "/tasks",
        json={"title": "Write API docs", "due_date": "2026-11-20"},
    )
    listed = client.get("/tasks")

    assert response.status_code == 201
    assert response.json()["due_date"] == "2026-11-20"
    assert listed.json()[0]["due_date"] == "2026-11-20"


@pytest.mark.parametrize(
    "due_date",
    [
        "not-a-date",
        "2026-02-30",
        "2026-11-20T12:00:00",
        "2026-11-20T00:00:00",
        0,
    ],
)
def test_create_task_rejects_invalid_due_date(client, due_date):
    response = client.post(
        "/tasks",
        json={"title": "Write API docs", "due_date": due_date},
    )

    assert response.status_code == 422


def test_list_tasks_filters_upcoming_dates_inclusive_of_seven_day_window(
    client, monkeypatch
):
    today = date(2026, 11, 14)
    monkeypatch.setattr(task_api, "_utc_today", lambda: today, raising=False)
    for title, due_date, completed in [
        ("Due today", today, False),
        ("Due in seven days", today + timedelta(days=7), False),
        ("Due in eight days", today + timedelta(days=8), False),
        ("Overdue", today - timedelta(days=1), False),
        ("No due date", None, False),
        ("Completed due today", today, True),
    ]:
        client.post(
            "/tasks",
            json={
                "title": title,
                "due_date": due_date.isoformat() if due_date else None,
                "completed": completed,
            },
        )

    response = client.get("/tasks?due=upcoming")

    assert response.status_code == 200
    assert {task["title"] for task in response.json()} == {
        "Due today",
        "Due in seven days",
    }


def test_list_tasks_filters_overdue_incomplete_tasks(client, monkeypatch):
    today = date(2026, 11, 14)
    monkeypatch.setattr(task_api, "_utc_today", lambda: today, raising=False)
    for title, due_date, completed in [
        ("Due yesterday", today - timedelta(days=1), False),
        ("Due today", today, False),
        ("Completed overdue", today - timedelta(days=1), True),
        ("No due date", None, False),
    ]:
        client.post(
            "/tasks",
            json={
                "title": title,
                "due_date": due_date.isoformat() if due_date else None,
                "completed": completed,
            },
        )

    response = client.get("/tasks?due=overdue")

    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["Due yesterday"]


def test_list_tasks_rejects_invalid_due_filter(client):
    response = client.get("/tasks?due=next")

    assert response.status_code == 422


def test_due_filters_preserve_completed_filter(client, monkeypatch):
    today = date(2026, 11, 14)
    monkeypatch.setattr(task_api, "_utc_today", lambda: today, raising=False)
    for title, completed in [("Incomplete", False), ("Completed", True)]:
        client.post(
            "/tasks",
            json={
                "title": title,
                "completed": completed,
                "due_date": today.isoformat(),
            },
        )

    completed_tasks = client.get("/tasks?completed=true")
    upcoming_tasks = client.get("/tasks?completed=false&due=upcoming")
    completed_upcoming_tasks = client.get("/tasks?completed=true&due=upcoming")

    assert [task["title"] for task in completed_tasks.json()] == ["Completed"]
    assert [task["title"] for task in upcoming_tasks.json()] == ["Incomplete"]
    assert completed_upcoming_tasks.json() == []


def test_list_tasks_filters_due_before_inclusively_and_keeps_priority_order(client):
    created = {}
    for title, due_date, completed, priority in [
        ("Low before cutoff", "2026-11-19", False, "low"),
        ("High on cutoff", "2026-11-20", True, "high"),
        ("Medium after cutoff", "2026-11-21", False, "medium"),
        ("No due date", None, False, "high"),
    ]:
        payload = {"title": title, "completed": completed, "priority": priority}
        if due_date is not None:
            payload["due_date"] = due_date
        response = client.post("/tasks", json=payload)
        assert response.status_code == 201
        created[title] = response.json()

    response = client.get("/tasks", params={"due_before": "2026-11-20"})

    assert response.status_code == 200
    assert response.json() == [
        created["High on cutoff"],
        created["Low before cutoff"],
    ]


def test_list_tasks_due_before_returns_empty_when_no_tasks_match(client):
    client.post(
        "/tasks",
        json={"title": "Due later", "due_date": "2026-11-21"},
    )
    client.post("/tasks", json={"title": "No due date"})

    response = client.get("/tasks", params={"due_before": "2026-11-20"})

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.parametrize(
    ("completed", "expected_title"),
    [(True, "Completed before cutoff"), (False, "Incomplete before cutoff")],
)
def test_due_before_combines_with_completed_filter(client, completed, expected_title):
    for title, task_completed, due_date in [
        ("Completed before cutoff", True, "2026-11-20"),
        ("Incomplete before cutoff", False, "2026-11-19"),
        ("Completed after cutoff", True, "2026-11-21"),
        ("Incomplete after cutoff", False, "2026-11-21"),
        ("Undated incomplete", False, None),
    ]:
        payload = {"title": title, "completed": task_completed}
        if due_date is not None:
            payload["due_date"] = due_date
        client.post("/tasks", json=payload)

    response = client.get(
        "/tasks",
        params={
            "completed": str(completed).lower(),
            "due_before": "2026-11-20",
        },
    )

    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == [expected_title]


@pytest.mark.parametrize(
    ("due", "due_before", "expected_titles"),
    [
        (
            "upcoming",
            "2026-11-15",
            {"Due today", "Next day"},
        ),
        (
            "overdue",
            "2026-11-11",
            {"Old overdue", "Cutoff overdue"},
        ),
    ],
)
def test_due_before_combines_with_existing_due_filter(
    client, monkeypatch, due, due_before, expected_titles
):
    today = date(2026, 11, 14)
    monkeypatch.setattr(task_api, "_utc_today", lambda: today, raising=False)
    for title, task_due_date, completed in [
        ("Old overdue", today - timedelta(days=5), False),
        ("Cutoff overdue", today - timedelta(days=3), False),
        ("Recent overdue", today - timedelta(days=1), False),
        ("Due today", today, False),
        ("Next day", today + timedelta(days=1), False),
        ("Upcoming after cutoff", today + timedelta(days=4), False),
        ("Beyond upcoming", today + timedelta(days=8), False),
        ("Completed overdue", today - timedelta(days=5), True),
        ("Completed upcoming", today + timedelta(days=1), True),
    ]:
        client.post(
            "/tasks",
            json={
                "title": title,
                "completed": completed,
                "due_date": task_due_date.isoformat(),
            },
        )

    response = client.get(
        "/tasks",
        params={"due": due, "due_before": due_before},
    )

    assert response.status_code == 200
    assert {task["title"] for task in response.json()} == expected_titles


@pytest.mark.parametrize(
    "due_before",
    ["not-a-date", "2026-02-30", "2026-11-20T12:00:00"],
)
def test_list_tasks_rejects_invalid_due_before_filter(client, due_before):
    response = client.get("/tasks", params={"due_before": due_before})

    assert response.status_code == 422


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
