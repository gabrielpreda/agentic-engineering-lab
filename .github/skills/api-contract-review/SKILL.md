---
name: api-contract-review
description: Inspect and explain an API's externally visible contract from its implementation and project documentation. Use when asked to review or document endpoints, inputs, outputs, validation, status codes, or contract discrepancies.
---

# Review an API contract

Use this procedure for the API or endpoints named in the request. Adapt it to the repository's language, framework, and organization; do not assume particular filenames or frameworks.

1. If the request does not identify the API or endpoints and the repository contains several, ask which ones to review. Otherwise, identify the likely route handlers, controllers, or router definitions from the repository structure.
2. Trace each requested endpoint to its input and output schemas, validation rules, status codes, and relevant middleware or error handling. Follow references across files when necessary.
3. Look for related API documentation and, if present, tests or schema definitions. Use them as evidence and identify conflicts; do not assume that documentation or tests match the implementation.
4. Report each endpoint's method and path, accepted inputs, successful response, explicitly defined validation and error behavior, and any relevant authentication or authorization requirements that are visible in the code.
5. Distinguish implemented behavior from intended behavior in a supplied requirement. If they differ, describe the gap instead of silently choosing one.
6. Do not infer behavior that is not supported by the repository. Mark missing or ambiguous details as unknown and ask a focused question when a decision depends on them.
7. Give evidence for each important claim using file paths and relevant symbols or code areas. Do not claim that the API was run, tested, or verified unless you actually performed that check.
8. Keep the review read-only. Do not edit files, add dependencies, or run commands unless the user asks for those actions.

## Suggested report structure

- Endpoint: method and path.
- Inputs: fields, types, defaults, and constraints that are explicit in the implementation.
- Outputs: status code and response shape.
- Other behavior: explicit errors, authentication, or authorization details relevant to the request.
- Evidence: repository files and symbols supporting the summary.
- Gaps: missing, ambiguous, or conflicting information.

Adapt the report to the user's request. Omit sections that do not apply instead of inventing details.

The Skill supplies a reusable review procedure. The repository and any supplied requirements provide the specific facts; a human checks the report against its evidence.
