# Task priority — feature specification

**Status:** Draft  
**Requirements source:** [Task priority requirements](../requirements/task-priority.md)  
**Approval owner:** Unassigned

This is a planning draft, not approval to implement.

## Outcome

Users can distinguish urgent tasks from lower-priority tasks through the Task API.

## Current API behavior

- `POST /tasks` requires a title of 1-120 characters, rejects whitespace-only titles with HTTP 422, accepts optional `completed` (default `false`), and returns HTTP 201 with `id`, `title`, and `completed`.
- `GET /tasks` returns HTTP 200 with an array of `id`, `title`, and `completed` fields and optionally filters by the `completed` boolean; tasks currently have no priority or priority ordering.
- Tasks are held in memory. The implementation and tests confirm these behaviors; see [app/main.py](../../app/main.py), [API tests](../../tests/test_api.py), [title validation test](../../tests/test_title_validation.py), and [test fixture](../../tests/conftest.py). The README describes the endpoint contract, but its statement that no automated test suite exists conflicts with the tests present in the repository; see [README](../../README.md).

## Scope and behavior

| Spec ID | Behavior or constraint | Source criterion |
|---|---|---|
| S-1 | Task creation accepts `low`, `medium`, or `high`; omitted priority defaults to `low`. | AC-1 |
| S-2 | Successful task creation and listing responses include each task's priority. | AC-2 |
| S-3 | Listing orders tasks `high`, `medium`, then `low`; relative order among equal-priority tasks is unspecified. | AC-3 |
| S-4 | Listing supports a priority filter, but its matching and invalid-value behavior is unresolved. | AC-4 |
| S-5 | Preserve existing task behavior, including in-memory storage, task fields, title validation, and the `completed` filter. | AC-5 |

## Constraints and exclusions

- Do not add a UI or persistent storage/database.
- Preserve existing endpoint behavior outside the priority addition.

## Assumptions and open questions

- The requirements provisionally assume a single exact-level `priority` query filter; this is not confirmed (AC-4).
- Should priority filtering match one exact level, include multiple levels, or use a threshold such as “this level and higher”?
- What should the API return when a priority filter or submitted priority is not one of `low`, `medium`, or `high`?

## Proposed work and verification intent

The following is a planning breakdown only; the requirements remain Draft and implementation is not authorized by this specification.

| Task ID | Result and criteria | Planned verification |
|---|---|---|
| T-1 | Resolve filter matching and invalid-value behavior before fixing the filter contract (AC-4; also informs invalid submitted priority under AC-1). | Record the decision in the requirements and confirm its approval status. |
| T-2 | Define priority creation/default and response behavior (AC-1, AC-2). | Planned API checks for each allowed value, omitted priority, and priority in successful POST/GET response bodies; check invalid input only after its behavior is decided. |
| T-3 | Define listing order and filter behavior while preserving existing task behavior (AC-3, AC-4, AC-5). Depends on T-1. | Planned API checks for high-to-low ordering, the approved filter semantics, coexistence with `completed`, unchanged task fields/title validation, and in-memory behavior. Do not assert relative order among equal priorities. |

## Pending scope-change impact

**Status:** Proposed; pending approval.  
**Source:** Requester/trainer scope-change instruction (2026-11-13).

The proposal affects the order returned by `GET /tasks`: the current implementation returns tasks in insertion order when `completed` is omitted and preserves insertion order among matching tasks when it is supplied. If approved, the endpoint would return tasks in priority order (`high`, `medium`, `low`); relative order among equal-priority tasks would remain unspecified. This is an ordering-only change: response fields and the existing `completed` filter behavior remain outside its scope. The separately requested priority filter and its unresolved matching semantics are also unchanged by this proposal.

The current draft already requires high-to-low ordering in AC-3/S-3. If approved, revise AC-3 and S-3 to identify the insertion-order-to-priority-order change, and refine T-3's planned verification with an ordering test that creates tasks in a different order from their priorities and checks the returned order. AC-1 (priority values/default) retains its ID and wording; AC-2 (response shape), AC-4 (filter behavior), and AC-5 (existing behavior) remain unchanged. T-1 and T-2 are unaffected; T-3 is the affected task. This test refinement is pending, not part of the current baseline.

**Owner decision required:** The approval owner is unassigned. Confirm whether this proposal is a clarification of existing AC-3/S-3 (rather than a change to the required ordering outcome), then accept or reject it. Do not revise the requirements or treat this proposal as approved before that decision.

## Scope changes

| Date | Change and source | Affected criteria/tasks/evidence | Review status |
|---|---|---|---|
| 2026-11-13 | Added stable IDs AC-1–AC-5 to the requirements worksheet without changing criterion wording. | All source-criterion references above. | Draft; not approved |
| 2026-11-13 | Requester/trainer proposed making the effect on `GET /tasks` ordering explicit. | AC-3/S-3 and T-3's planned ordering verification; AC-1, AC-2, AC-4, and AC-5 unchanged. | Proposed; awaiting owner approval |
