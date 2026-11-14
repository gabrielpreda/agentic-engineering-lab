# Task deadlines — feature specification

**Status:** Approved  
**Requirements:** [Task deadlines requirements](../requirements/capstone-deadlines.md)

## Outcome

Clients can assign date-only due dates to tasks and find incomplete work that is upcoming or overdue.

## Behavior

| Spec ID | Observable behavior | Source |
|---|---|---|
| S-1 | Task creation accepts optional `due_date` in `YYYY-MM-DD` form. If omitted, the response contains `"due_date": null`; task responses include the date or null. | AC-1 |
| S-2 | `GET /tasks?due=upcoming` selects incomplete tasks with a due date from the UTC current date through seven days later, inclusive. | AC-2 |
| S-3 | `GET /tasks?due=overdue` selects incomplete tasks with a due date earlier than the UTC current date. | AC-3 |
| S-4 | Without `due`, listing retains the existing completion filter and priority ordering. Existing fields and in-memory storage remain. | AC-4 |
| S-5 | Invalid due-date inputs and unsupported `due` values receive HTTP 422. | AC-5 |

## Constraints and exclusions

- No UI or persistent storage.
- Date-only values; UTC determines today.
- Due filters exclude completed tasks, including when combined with `completed=true`.

## Tasks and verification

| Task ID | Result | Criteria | Verification | Depends on | Status |
|---|---|---|---|---|---|
| T-1 | Add optional due-date creation and response behavior while preserving existing task fields. | AC-1, AC-4, AC-5 | Focused POST tests for a supplied date, omission/null, invalid dates, and existing creation behavior. | — | Done |
| T-2 | Add upcoming and overdue listing filters using UTC date boundaries. | AC-2, AC-3, AC-4, AC-5 | Focused GET tests for inclusive window boundaries, overdue boundary, completed and undated tasks, invalid filter, and coexistence with existing listing behavior. | T-1 | Done |

## Traceability

Each acceptance criterion maps to at least one task and focused automated test. No behavior is deferred.
