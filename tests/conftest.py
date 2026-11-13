from itertools import count

import pytest
from fastapi.testclient import TestClient

import app.main as task_api


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """Give each test an empty in-memory task store and a fresh ID sequence."""

    monkeypatch.setattr(task_api, "_tasks", [])
    monkeypatch.setattr(task_api, "_task_ids", count(1))
    return TestClient(task_api.app)
