# Task priority — implementation handoff

**Updated:** 2026-11-14  
**Requirements:** Draft; approval owner unassigned  
**Specification:** Draft; not implementation authorization  
**Current task:** T-2 — AC-1, AC-2, AC-5  

## Status

- **T-1:** Blocked on decisions and requirements approval. Priority-filter matching and invalid filtered/submitted value behavior remain open.
- **T-2:** Implementation and focused tests are present in the working tree, but the task is not complete; its T-1 dependency and approval gate are unresolved.
- **T-3:** Pending; depends on T-1 and T-2.
- Proposed clarification of listing order remains pending owner review.

## Decisions and observed behavior

- The requirements draft specifies `low`, `medium`, `high`, defaults omitted priority to `low`, includes priority in responses, and orders listing high-to-low.
- Current `app/main.py` uses a `Literal` priority field with default `low`; Pydantic currently rejects an invalid submitted value with HTTP 422. That observed behavior is not a recorded or approved requirements decision.
- Priority filtering and its invalid-value behavior are not implemented or decided.

## Files and verification

- Existing working-tree implementation changes: `app/main.py` and `tests/test_api.py` (T-2 priority support and focused creation tests).
- This update changes only `docs/handoffs/task-priority.md`. The existing `docs/handoff/task-priority.md` was left untouched.
- `./.venv/bin/python -m pytest -q` — **11 passed, 1 warning** (Starlette deprecation warning concerning `httpx` with `TestClient`).
- `git diff --check` — **passed**.

## Blockers and next task

The requirements and specification are still drafts, with no assigned approval owner. Resolve and record T-1's filter matching and invalid-value decisions, and obtain the required review/approval before treating T-2 as complete or proceeding with T-3. Then continue T-2 verification and move to T-3 as authorized.
