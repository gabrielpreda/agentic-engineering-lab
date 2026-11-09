# Copilot instructions for the Course Task API

- This repository is a small Python 3.10+ FastAPI teaching application. Start it with `uvicorn app.main:app --reload` and inspect the API at `/docs`.
- API routes and Pydantic request/response models are currently defined in `app/main.py`.
- Task data is held in the in-memory `_tasks` list and resets when the process restarts. Do not add a database or change persistence unless the request explicitly asks for it.
- Keep a requested change focused. Preserve the existing endpoint behavior unless the task says otherwise.
- Use FastAPI and Pydantic patterns already present in the file. Explain any assumptions and identify files changed.
- Do not claim that behavior is verified unless you have run or manually exercised the relevant endpoint.
