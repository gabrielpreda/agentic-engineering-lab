# Task priority — requirements worksheet

**Status:** Draft  
**Approval owner:** Unassigned  
**Last reviewed:** Not yet reviewed

## Request

> We need a way for the team to prioritize work. Add priority to tasks so users can see what is urgent. Keep it simple.

## User outcome

Users can distinguish urgent tasks from lower-priority tasks through the Task API.

## Sources reviewed

| Source | What it establishes | Limits or notes |
|---|---|---|
| [Trainer-prepared GitHub Issue #5](https://github.com/gabrielpreda/agentic-engineering-lab/issues/5) | The request is to add task priority so users can see urgency, keeping the feature simple. | The original issue did not define priority values or API behavior; requester answers below resolve several points. |
| Requester answers in this conversation (2026-11-13) | Priority values are `low < medium < high`; priority may be omitted on creation and defaults to `low`; task responses include priority; `GET /tasks` filters and orders by priority, highest first; no UI; equal-priority order is not guaranteed. | Filtering match semantics and invalid-value behavior remain unspecified. |
| [Current API implementation](../../app/main.py) | Tasks are held in memory; current task fields are `id`, `title`, and `completed`; `GET /tasks` supports an optional `completed` filter; `POST /tasks` returns HTTP 201. | Priority is not currently implemented. |
| [API tests](../../tests/test_api.py), [title validation test](../../tests/test_title_validation.py), and [test fixture](../../tests/conftest.py) | Tests cover health, empty listing, task creation/default completion, title rejection, and listing a created task; the fixture resets in-memory tasks and IDs. | No priority behavior or combined priority/completed filtering is tested. |
| [README](../../README.md) | Documents the current endpoint contract and in-memory task storage. | It does not document priority. |
| Related repository issues [#2](https://github.com/gabrielpreda/agentic-engineering-lab/issues/2) and [#4](https://github.com/gabrielpreda/agentic-engineering-lab/issues/4) | #2 concerns API documentation; #4 concerns whitespace-only title validation. | Neither describes duplicate task-priority work. |

## Confirmed facts

- The request is to add priority to tasks so users can identify urgency, while keeping the feature simple. Source: Issue #5.
- The priority levels are `low`, `medium`, and `high`, ordered from lowest to highest. Source: requester answer.
- Priority is optional when creating a task; if omitted, it is `low`. Source: requester answer.
- Task responses must include the priority value. Source: requester answer.
- `GET /tasks` must support filtering by priority and order results with highest priority first. Source: requester answers.
- No UI is in scope for now. Source: requester answer.
- Tasks with equal priority have no guaranteed relative order. Source: requester answer.
- The current API is in-memory and already supports filtering by `completed`. Source: [app/main.py](../../app/main.py).

## Assumptions and inferences

| Statement | Evidence | Confirmation needed? |
|---|---|---|
| Priority filtering uses a single `priority` query parameter and exact-matches the requested level. | Requester asked for priority filtering but did not specify filter shape or match semantics. | Yes |

## Acceptance criteria

AC-1. `POST /tasks` accepts `low`, `medium`, or `high` as a task priority. If priority is omitted, the created task has priority `low`. Source: requester answer; priority is not currently supported in [app/main.py](../../app/main.py).  

AC-2. Successful task responses from `POST /tasks` and `GET /tasks` include the task's priority value. Source: requester answer.

AC-3. `GET /tasks` returns tasks ordered from highest to lowest priority (`high`, `medium`, `low`). The relative order of tasks with equal priority is unspecified. Source: requester answers.

AC-4. Provisionally, `GET /tasks` accepts a priority filter and returns matching tasks. The exact filter matching and invalid-value behavior remain open; see Open questions. Source: requester answer.

AC-5. Existing task behavior remains in place: tasks remain in memory, and the existing `completed` filter and task fields continue to work. Sources: [app/main.py](../../app/main.py), [tests/test_api.py](../../tests/test_api.py), and project constraints.

## Non-goals and constraints

- Do not add a UI. Source: requester answer.
- Keep task data in memory; do not add persistence or a database. Source: current project constraint and [README](../../README.md).
- Preserve existing endpoint behavior outside the priority addition, including the `completed` filter and current title validation. Sources: [app/main.py](../../app/main.py) and tests.

## Open questions

- Should priority filtering match one exact level, include multiple levels, or use a threshold such as “this level and higher”?
- What should the API return when a priority filter or submitted priority is not one of `low`, `medium`, or `high`?

## Review record

- **Decision:** Draft; not approved.
- **Reviewed by:** Unassigned.
- **Notes:** Requester clarification is recorded above. Update this record only after the responsible person reviews the requirements.
