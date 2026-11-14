# Task deadlines — implementation tasks

**Status:** Approved  
**Requirements:** [Task deadlines requirements](../requirements/capstone-deadlines.md)  
**Specification:** [Task deadlines feature specification](../specs/capstone-deadlines.md)

| Task ID | Reviewable result | Acceptance criteria | Planned verification | Depends on | Status |
|---|---|---|---|---|---|
| T-1 | Accept optional date-only due dates, include the date or null in task responses, and retain existing creation behavior. | AC-1, AC-4, AC-5 | Focused POST tests for valid, omitted, and invalid due dates; run existing creation and title-validation tests. | — | Done |
| T-2 | Filter listing for upcoming or overdue incomplete tasks using the approved UTC boundaries. | AC-2, AC-3, AC-4, AC-5 | Focused GET tests for both date boundaries, completed and undated tasks, invalid filter values, existing `completed` filtering, and priority order. | T-1 | Done |

## Traceability

| Criterion | Task(s) | Verification |
|---|---|---|
| AC-1 | T-1 | POST date/default/response tests |
| AC-2 | T-2 | Upcoming window boundary tests |
| AC-3 | T-2 | Overdue boundary tests |
| AC-4 | T-1, T-2 | Existing behavior regression tests |
| AC-5 | T-1, T-2 | Invalid input tests |

## Scope and dependencies

- No UI, database, or persistence changes.
- T-2 depends on T-1 because the listing filter operates on the new task due-date field.
