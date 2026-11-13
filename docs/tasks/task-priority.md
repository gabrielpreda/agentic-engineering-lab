# Task priority — proposed task list

**Status:** Draft  
**Requirements:** [Task priority requirements](../requirements/task-priority.md)  
**Specification:** [Task priority feature specification](../specs/task-priority.md)  
**Approval owner:** Unassigned

This is a planning draft, not authorization to implement.

## Tasks

| Task ID | Reviewable result and acceptance criteria | Planned verification evidence | Depends on |
|---|---|---|---|
| T-1 | Obtain and record an explicit decision for priority-filter matching and responses to invalid submitted or filtered priorities (AC-1, AC-4). | Review the recorded decision and confirm the requirements approval status; do not assume API behavior before this decision. | — |
| T-2 | Task creation supports the specified priority values and default, returns priority, and preserves existing creation behavior (AC-1, AC-2, AC-5). | Planned focused API tests for each allowed value, omitted priority, and POST response fields; regression checks for existing task fields, completion default, and title validation. Check invalid submitted values according to T-1's decision. | T-1 |
| T-3 | Task listing includes priority, orders high-to-low, applies the decided priority filter, and preserves existing listing behavior (AC-2, AC-3, AC-4, AC-5). | Planned focused API tests for priority in GET responses, ordering (without asserting tie order), decided filter behavior, and combined priority/`completed` filtering; regression check for existing fields and a manual check that data remains in-memory. | T-1, T-2 |

## Pending scope-change impact

**Status:** Proposed; pending approval.  
**Source:** Requester/trainer scope-change instruction (2026-11-13).

The proposed change is to `GET /tasks` ordering: the current implementation returns tasks in insertion order, including when the existing `completed` filter is used. If approved, T-3's ordering verification should explicitly create tasks in an order different from their priorities and check that results are returned high-to-low, without asserting relative order for ties. This is a pending test refinement, not a claim that the test exists.

Potential impact upon approval: the current draft already requires high-to-low ordering in AC-3/S-3. Revise AC-3/S-3 to identify the insertion-order-to-priority-order change and update T-3's result/verification accordingly. Keep AC-1 (priority values/default) and T-1/T-2 unchanged. Do not change AC-2 response shape, AC-4 filter semantics, or AC-5/current `completed` filter behavior. No task IDs are changed or retired while the proposal is pending.

## Criterion-to-task traceability

| Acceptance criterion | Task(s) | Planned evidence |
|---|---|---|
| AC-1 | T-1, T-2 | Decision review for invalid values; focused POST tests for allowed values and default. |
| AC-2 | T-2, T-3 | Focused POST and GET response-shape tests. |
| AC-3 | T-3 | Focused listing-order test; equal-priority relative order is not asserted. |
| AC-4 | T-1, T-3 | Decision review followed by a focused test of the decided filter behavior. |
| AC-5 | T-2, T-3 | Regression checks for task fields, defaults, title validation, and `completed` filtering; manual in-memory behavior check. |

**Coverage:** Every criterion has a task and planned verification evidence. AC-1's invalid-input behavior and AC-4's filter semantics remain blocked on T-1. No unrelated tasks are included. Planned tests are not claimed to exist.

**Owner decision required:** The approval owner is unassigned. Confirm this clarifies existing AC-3/S-3 rather than changing the required ordering outcome, then accept or reject the proposal. Keep the existing task plan as the baseline until that decision.

## Open decision

The requirements do not decide whether a priority filter matches one exact level, multiple levels, or a threshold, nor what response to return for invalid submitted or filtered values. T-1 must resolve these choices before T-2 and T-3 are complete; this plan does not choose an outcome.
