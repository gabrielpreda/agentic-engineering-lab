---
name: incremental-implementation
description: Implement an approved feature plan in small, reviewable test-and-code steps. Keep each change tied to acceptance criteria, verify it with evidence, update task status, and prepare a concise handoff when work moves to another session.
---

# Incremental implementation

Use this workflow after requirements and a feature specification have been reviewed. Follow the project's test commands and existing conventions.

## 1. Establish the current state

- Read the requirements, feature specification, task list, relevant source files, and relevant tests.
- Confirm the task's status, acceptance criteria, prerequisites, and verification plan.
- Check the current branch and working tree before editing. Preserve unrelated user changes.
- If the requirements/spec are drafts or contain a blocking question, pause implementation for that behavior and ask the owner or trainer.
- Select one task. Do not silently expand it to adjacent features.

## 2. Work one reviewable step at a time

- State the task ID and the criterion it addresses.
- Inspect the narrowest relevant implementation and tests before proposing changes.
- Add or update a focused test for the expected behavior before or alongside the implementation, following the task plan and repository conventions.
- Run the focused test, read the actual failure or result, then make the smallest implementation change that addresses it.
- Run relevant regression tests after each meaningful code change. Do not claim checks passed unless they were run and their output inspected.
- Keep test changes independent enough to show the expected behavior; do not weaken a test to make an implementation pass.

## 3. Review against the plan

- Inspect the full diff after each task step.
- Check that the change addresses the named acceptance criterion and preserves compatibility and explicit non-goals.
- Check for unrelated files, generated artifacts, dependency changes, accidental scope expansion, and unverified behavior.
- If implementation reveals a requirement conflict or new scope, stop and update the requirements/spec/task list through the project approval process before continuing.

## 4. Record truthful task state

- Mark a task complete only after its planned evidence is obtained and the diff is reviewed.
- Record exact test commands and concise results in the task list or handoff note. Distinguish passed, failed, skipped, and not run.
- Record decisions, files changed, remaining questions, and the next task. Do not copy a long transcript when a short state summary is sufficient.
- If a task is partly complete, say what remains and keep its status partial/in progress.

## 5. Manage session focus

- Keep the current Copilot session focused on the selected task and its immediate verification.
- Start a new session when moving to a substantially different task, after a long interruption, or when the current conversation no longer provides a reliable summary.
- Before switching, update the handoff note from verified repository state. Include criterion IDs, task ID/status, changed files, tests/results, decisions, blockers, and the next step.
- In the new session, reread the requirements/spec/task list, handoff note, current diff, and test state. Treat repository evidence as authoritative over an old chat summary.

Do not commit, publish, deploy, or make external changes unless the user/project workflow explicitly calls for that action.
