"""Start the Task API and verify its public HTTP contract in CI."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from urllib.error import URLError
from urllib.request import Request, urlopen


BASE_URL = "http://127.0.0.1:8000"


def request_json(path: str, *, method: str = "GET", payload: dict | None = None) -> tuple[int, object]:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = Request(
        f"{BASE_URL}{path}",
        data=data,
        method=method,
        headers={"Content-Type": "application/json"},
    )
    with urlopen(request, timeout=3) as response:
        return response.status, json.load(response)


def wait_until_ready(process: subprocess.Popen[bytes]) -> None:
    deadline = time.monotonic() + 20
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"Uvicorn exited early with status {process.returncode}")
        try:
            status, body = request_json("/healthz")
        except (URLError, TimeoutError, ConnectionError):
            time.sleep(0.5)
            continue
        if status == 200 and body == {"status": "ok"}:
            return
        time.sleep(0.5)
    raise TimeoutError("Task API did not become ready within 20 seconds")


def main() -> int:
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        wait_until_ready(process)

        status, created = request_json(
            "/tasks",
            method="POST",
            payload={"title": "CI smoke task"},
        )
        if status != 201 or not isinstance(created, dict) or created.get("title") != "CI smoke task":
            raise AssertionError(f"Unexpected task creation response: status={status}, body={created!r}")

        status, tasks = request_json("/tasks")
        if status != 200 or not isinstance(tasks, list):
            raise AssertionError(f"Unexpected task list response: status={status}, body={tasks!r}")
        if not any(task.get("id") == created.get("id") for task in tasks if isinstance(task, dict)):
            raise AssertionError("Created task was not present in the subsequent task list")

        print("Live API smoke check passed: health, create task, and list task")
        return 0
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)


if __name__ == "__main__":
    raise SystemExit(main())
