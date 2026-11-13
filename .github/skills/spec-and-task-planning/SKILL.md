---
name: spec-and-task-planning
description: Turn reviewed requirements into a concise, implementation-independent feature specification and a small verifiable task list linked to acceptance criteria and planned tests. Use before implementation, or when scope changes require planning artifacts to be revised.
---

# Spec and task planning

Use this workflow to bridge agreed requirements and implementation work. Keep the specification focused on behavior and constraints; keep coding choices open unless the requirements or project establish them.

## 1. Read the approved inputs

- Read the requirements and relevant source material before drafting.
- Identify each acceptance criterion by its stable ID. If the source has no IDs, add concise IDs to the requirements artifact while preserving its content and wording.
- Check the requirements' status, approval owner, assumptions, and open questions.
- Do not silently resolve a material open question. Ask for clarification or state the smallest explicit assumption needed to continue.
- If requirements are still a draft, label the spec draft too and avoid presenting implementation tasks as authorized work.

## 2. Write a concise specification

Describe the user outcome, scope, observable behavior, constraints, and exclusions. Link each behavior to its source criterion. Include error handling or compatibility expectations only when supported by the requirements or confirmed project behavior.

Avoid prescribing class names, internal architecture, file layout, algorithms, or package choices unless a real constraint requires them. Prefer a short, testable statement over an exhaustive design document. A one-page target is a useful limit, not a reason to omit a material behavior or risk.

## 3. Decompose work into small tasks

- Give each task a stable ID and a clear result that can be reviewed independently.
- Link each task to the acceptance criteria it advances.
- Identify the verification evidence for the task: a focused automated test, existing test, manual check, or explicit review. Do not claim a test exists before it has been written.
- Keep tasks small enough to implement and verify in a short step. Combine trivial edits when separating them would add ceremony.
- Include test work where needed; avoid duplicating every test as both a separate task and a task checklist item without reason.
- Identify dependencies only when one task genuinely depends on another.

## 4. Check traceability and coverage

For every acceptance criterion, confirm that at least one task and one verification method cover it, or record why it is deferred. For every task, confirm it supports a criterion, a necessary quality constraint, or an agreed enabling step. Remove unrelated work.

## 5. Handle scope changes explicitly

When a requester changes scope or new evidence changes a requirement:

1. Record the change, source, and date in the requirements artifact if it changes approved behavior or scope.
2. If it is only proposed, do not rewrite approved requirements; record the proposal and its potential impact separately.
3. Identify affected acceptance criteria, tasks, tests, assumptions, and open questions.
4. Update the spec and task list together so their links remain accurate.
5. Mark removed or superseded work clearly instead of silently deleting traceability.
6. Keep artifact status aligned with approval state; ask the owner to review changes that alter approved behavior or scope.

Do not begin implementation merely because the spec and task list are complete. Follow the user's authorization and project workflow.
