# Task deadlines — requirements worksheet

**Status:** Approved  
**Approval owner:** Requester  
**Approved:** 2026-11-14

## User outcome

Teams can plan work against dates and quickly find tasks that are coming due or already late, while existing clients that omit a due date continue to work.

## Sources reviewed

| Source | What it establishes | Limits or notes |
|---|---|---|
| Request in this conversation (2026-11-14) | Add due dates and make upcoming or late tasks easy to find; keep existing clients working. | Does not alone define date format, time window, or discovery mechanism. |
| Requester clarification in this conversation (2026-11-14) | Use date-only ISO 8601, `GET /tasks?due=upcoming|overdue`, a seven-day upcoming window inclusive of today, exclude completed tasks, return `due_date: null` when unset, and use UTC for date boundaries. Requester approved proceeding with these choices. | Invalid filter behavior follows the explicit assumption below. |
| [Current API implementation](../../app/main.py) and [API tests](../../tests/test_api.py) | Tasks are in memory; creation accepts title, completion, and priority; listing supports completion filtering and priority ordering. | No due-date behavior exists yet. |

## Confirmed facts

- `due_date` is a calendar date represented as `YYYY-MM-DD`; it is optional at task creation.
- A task without a due date has `due_date: null` in task responses.
- `GET /tasks` supports `due=upcoming` and `due=overdue`.
- Upcoming means due from the current UTC date through seven days later, inclusive.
- Overdue means due before the current UTC date.
- Both due filters exclude completed tasks.
- Existing task storage and behavior remain in memory; clients may continue omitting `due_date`.

## Assumptions

- Invalid `due` query values and invalid date strings return HTTP 422, consistent with FastAPI/Pydantic request validation.
- `due` may be combined with the existing `completed` filter; a due filter still excludes completed tasks, so a combined `completed=true` due query returns no tasks.

## Acceptance criteria

- **AC-1:** `POST /tasks` accepts an optional date-only ISO `due_date`. When omitted, the created task has `due_date: null`; successful POST and GET task objects include `due_date`.
- **AC-2:** `GET /tasks?due=upcoming` returns only incomplete tasks whose due dates fall inclusively between today in UTC and seven days from today in UTC.
- **AC-3:** `GET /tasks?due=overdue` returns only incomplete tasks whose due dates are before today in UTC.
- **AC-4:** Omitting `due` preserves the existing listing behavior, including the `completed` filter and priority ordering. Existing clients may omit `due_date`; task storage remains in memory.
- **AC-5:** Invalid date values and unsupported `due` filter values are rejected with HTTP 422.

## Non-goals and constraints

- Do not add a UI, database, or persistent storage.
- Do not change existing completion or priority semantics.
- Do not introduce timestamps or per-user timezone settings; due dates are date-only and evaluated against UTC.

## Open questions

- None for this approved slice.

## Review record

- **Decision:** Approved for implementation.
- **Reviewed by:** Requester in this conversation.
- **Notes:** Approval covers the date format, query filter, upcoming window, completion handling, null representation, and UTC date boundary listed above.
