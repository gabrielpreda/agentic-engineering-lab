# Task API — Module 1 starter

A deliberately small in-memory FastAPI application for the Agentic Engineering with GitHub Copilot course. This is a learning target, not a production service.

## Requirements

- Python 3.10 or later

## Install and run

```bash
python -m venv .venv
source .venv/bin/activate          # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e .
uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000/docs> to try the API.

## API endpoints

### `GET /healthz`

Returns HTTP `200` with:

```json
{"status":"ok"}
```

### `GET /tasks`

Returns HTTP `200` with a JSON array of task objects. Each task has this shape:

```json
{"id":1,"title":"Buy milk","completed":false,"priority":"low","due_date":null}
```

The `completed` query parameter is optional. Set it to `true` or `false` to return only tasks with that completion status; omit it to return all tasks.

The optional `due` query parameter can be set to `upcoming` or `overdue`:

- `upcoming` returns incomplete tasks due from today through seven days from today, inclusive.
- `overdue` returns incomplete tasks due before today.

The optional `due_before` query parameter accepts a date-only `YYYY-MM-DD` value and returns tasks due on or before that date, inclusive. Tasks without a due date are excluded, and completed tasks are included unless narrowed by another filter. Malformed dates return HTTP `422`.

Due dates use UTC to determine today. The `due` filter can be combined with `completed`; due filters always exclude completed tasks. The `due_before`, `completed`, and `due` filters combine to narrow results. Tasks remain ordered by priority (`high`, `medium`, `low`).

### `POST /tasks`

Creates a task and returns HTTP `201` with the created task, including its assigned `id`:

```json
{"id":1,"title":"Buy milk","completed":false,"priority":"low","due_date":"2026-11-20"}
```

Send a JSON request body with these fields:

| Field | Type | Required | Constraints / default |
|---|---|---|---|
| `title` | string | Yes | Must contain 1–120 characters |
| `completed` | boolean | No | Defaults to `false` |
| `priority` | string | No | `low`, `medium`, or `high`; defaults to `low` |
| `due_date` | string or null | No | Date-only `YYYY-MM-DD`; defaults to `null` |

Tasks are held in memory and reset when the service restarts. There is no database, authentication, or user interface in this starter. Run the tests with `python -m pytest`.
