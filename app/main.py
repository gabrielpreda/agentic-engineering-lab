"""A small in-memory task API used in the Copilot course."""

from datetime import date, datetime, timedelta, timezone
from itertools import count
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="Course Task API", version="0.1.0")


class TaskCreate(BaseModel):
    """Fields accepted when creating a task."""

    title: str = Field(min_length=1, max_length=120)
    completed: bool = False
    priority: Literal["low", "medium", "high"] = "low"
    due_date: date | None = None

    @field_validator("due_date", mode="before")
    @classmethod
    def due_date_must_use_iso_format(cls, value: object) -> date | None:
        if value is None:
            return None
        if isinstance(value, date) and not isinstance(value, datetime):
            return value
        if not isinstance(value, str):
            raise ValueError("due_date must use YYYY-MM-DD format")
        parsed_date = date.fromisoformat(value)
        if parsed_date.isoformat() != value:
            raise ValueError("due_date must use YYYY-MM-DD format")
        return parsed_date

    @field_validator("title")
    @classmethod
    def title_must_contain_non_whitespace(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("title must contain at least one non-whitespace character")
        return value


class Task(TaskCreate):
    """Task returned by the API."""

    id: int


_tasks: list[Task] = []
_task_ids = count(1)
_PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}


def _utc_today() -> date:
    return datetime.now(timezone.utc).date()


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    """Report that the service is running."""

    return {"status": "ok"}


@app.get("/tasks", response_model=list[Task])
async def list_tasks(
    completed: bool | None = None,
    due: Literal["upcoming", "overdue"] | None = None,
) -> list[Task]:
    """Return all tasks or filter by completion status."""

    if completed is None:
        tasks = _tasks
    else:
        tasks = [task for task in _tasks if task.completed is completed]
    if due is not None:
        today = _utc_today()
        if due == "upcoming":
            last_upcoming_day = today + timedelta(days=7)
            tasks = [
                task
                for task in tasks
                if not task.completed
                and task.due_date is not None
                and today <= task.due_date <= last_upcoming_day
            ]
        else:
            tasks = [
                task
                for task in tasks
                if not task.completed
                and task.due_date is not None
                and task.due_date < today
            ]
    return sorted(tasks, key=lambda task: _PRIORITY_RANK[task.priority])


@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(request: TaskCreate) -> Task:
    """Create a task and store it in memory."""

    task = Task(id=next(_task_ids), **request.model_dump())
    _tasks.append(task)
    return task
