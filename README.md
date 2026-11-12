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
{"id":1,"title":"Buy milk","completed":false}
```

The `completed` query parameter is optional. Set it to `true` or `false` to return only tasks with that completion status; omit it to return all tasks.

### `POST /tasks`

Creates a task and returns HTTP `201` with the created task, including its assigned `id`:

```json
{"id":1,"title":"Buy milk","completed":false}
```

Send a JSON request body with these fields:

| Field | Type | Required | Constraints / default |
|---|---|---|---|
| `title` | string | Yes | Must contain 1–120 characters |
| `completed` | boolean | No | Defaults to `false` |

Tasks are held in memory and reset when the service restarts. There is no database, authentication, user interface, automated test suite, Copilot customization, or external tool configuration in this starter. Later course modules add capabilities when the exercise requires them.
