---
name: test-feedback
description: Add or update tests for a requested behavior, diagnose relevant test failures, and use test feedback to guide a focused change. Use when implementing a feature, fixing a regression, or investigating a failing test.
---

# Work from tests and feedback

Use this workflow when a task involves adding or changing behavior, writing or updating tests, or diagnosing a test failure. Adapt to the repository's language, framework, and test conventions; do not assume specific filenames or commands.

1. **Understand the expected behavior.** Identify the request, acceptance criteria, affected behavior, and constraints. Ask a focused question if an ambiguity changes what should be tested or implemented.
2. **Inspect the project test setup.** Find the relevant tests, test framework, documented commands, and code paths. Do not invent a test command when the repository documents one.
3. **Make the test express the expectation.** Add or update a focused test for the requested behavior or regression before changing application code when practical. Preserve existing assertions. Do not weaken or delete a test just to make it pass.
4. **Run the smallest relevant check that the user has authorized.** Read the full failure, including the test name, assertion, expected value, actual value, and traceback. Distinguish an application defect from a test setup, dependency, or environment problem.
5. **Explain before editing when diagnosis is requested.** Connect the failure to the relevant code with file and symbol evidence. State uncertainties instead of guessing.
6. **Make the smallest change that satisfies the expectation.** Keep unrelated refactoring, formatting, dependency changes, and behavior changes out of scope. Do not change the test expectation to fit an implementation unless the requirement itself is wrong and the user agrees.
7. **Rerun checks.** Run the focused test first, then the relevant broader suite if authorized and available. Report the exact commands and results; do not claim checks passed if they were not run.
8. **Review the diff and remaining gaps.** Confirm the intended test remains present, check for unrelated changes, and state relevant cases or risks the tests do not cover.

Do not install dependencies, access external services, deploy, or perform destructive operations unless the user explicitly authorizes that action. The Skill is a procedure, not proof that a change is correct; verify the evidence and review the diff.
