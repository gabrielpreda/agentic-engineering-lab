# Task deadlines — implementation handoff

**Branch:** `capstone/deadline`  
**Updated:** 2026-11-14  
**Requirements/spec status:** Approved  
**Current task:** T-1 and T-2 — complete

## Implemented criteria

- AC-1: Task creation accepts optional date-only `due_date`; omitted dates serialize as `null`; POST and GET responses include the field.
- AC-2: `due=upcoming` includes incomplete tasks due today through seven days ahead, inclusive, using UTC.
- AC-3: `due=overdue` includes incomplete tasks due before today in UTC.
- AC-4: Existing completion filtering, priority ordering, task fields, and in-memory storage are retained.
- AC-5: Invalid date values and unsupported due filters return HTTP 422.

## Files changed

- `app/main.py`
- `tests/test_api.py`
- `README.md`
- `docs/requirements/capstone-deadlines.md`
- `docs/specs/capstone-deadlines.md`
- `docs/tasks/capstone-deadlines.md`
- `docs/handoffs/capstone-deadlines.md`

## Verification evidence

| Command/check | Result | Notes |
|---|---|---|
| `./.venv/bin/python -m pytest -q tests/test_api.py -k 'due_date or upcoming or overdue or invalid_due_filter'` | Passed: 7 tests | Focused due-date creation, validation, and listing behavior. |
| `./.venv/bin/python -m pytest -q` | Passed: 20 tests | One existing Starlette deprecation warning about `httpx` with `TestClient`. |
| `git diff --check` | Passed | No whitespace errors. |

## Review questions and next step

- No open behavior questions remain for the approved deadline slice.
- The separate task-priority requirements remain Draft, and their open questions and assumptions were not changed.
- The earlier task-priority handoff was checked before editing: priority implementation is already in the committed repository state rather than present as app/test working-tree edits. The initial test run reported 12 passed with one warning, not the handoff's 11 passed.
