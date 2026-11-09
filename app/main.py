"""A small in-memory task API used in the Copilot course."""

from itertools import count

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Course Task API", version="0.1.0")


class TaskCreate(BaseModel):
    """Fields accepted when creating a task."""

    title: str = Field(min_length=1, max_length=120)
    completed: bool = False


class Task(TaskCreate):
    """Task returned by the API."""

    id: int


_tasks: list[Task] = []
_task_ids = count(1)


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    """Report that the service is running."""

    return {"status": "ok"}


@app.get("/tasks", response_model=list[Task])
async def list_tasks() -> list[Task]:
    """Return all tasks currently held in memory."""

    return list(_tasks)


@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(request: TaskCreate) -> Task:
    """Create a task and store it in memory."""

    task = Task(id=next(_task_ids), **request.model_dump())
    _tasks.append(task)
    return task
