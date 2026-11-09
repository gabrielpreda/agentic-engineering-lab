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

## Starting endpoints

- `GET /healthz` — returns `{"status":"ok"}`.
- `GET /tasks` — returns all in-memory tasks; optional `completed=true` or `completed=false` filters by completion status.
- `POST /tasks` — creates a task from `{"title":"..."}` and optional `completed` value.

Tasks reset when the server restarts. There is no database, authentication, user interface, automated test suite, Copilot customization, or external tool configuration in this starter. Later course modules add capabilities when the exercise requires them.
