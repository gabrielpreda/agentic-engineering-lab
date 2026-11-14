---
name: delivery-lifecycle
description: Move an approved Jira story from source review through implementation, tests, commit, push, pull request, merge, deployment, and verified status updates with separate approval gates.
---

# Jira-backed delivery lifecycle

Use this workflow for a feature or fix tracked in Jira. Keep story generation separate from implementation. State the current delivery stage and blockers; report external actions only after verifying them in the connected system.

## Story intake and readiness

1. Read the live Jira story, status, acceptance criteria, dependencies, priority, and related work. Read linked Miro/Figma evidence where relevant, approved requirements/spec, and repository instructions.
2. Confirm scope when sources conflict or a consequential decision is unresolved. Do not implement from an old chat summary.
3. Inspect repository architecture, tests, branches, and delivery configuration. Present a short plan tied to acceptance criteria.

## Separate approval gates

Reading sources and preparing recommendations are read-only. Obtain explicit approval for each external write: Jira story create/update/transition, commit, push, PR creation/update, review submission, merge, and deployment. Present the exact action and scope before requesting approval. Approval to implement or commit does not authorize a push, PR, merge, or deployment. If scope changes materially, obtain fresh approval.

## One story at a time

1. Check working tree and refs; preserve unrelated work. Create a story-specific branch from the repository's agreed integration base. Never force-push or discard unknown changes.
2. Update Jira to an in-progress status only after approval and only using a valid project transition.
3. Protect existing behavior with focused tests, add tests for acceptance criteria, and implement the smallest complete change for this story only.
4. Run project-required checks. Report exact commands and observed outcomes; do not infer test/CI success.
5. Review the full diff for criteria coverage, unrelated changes, validation, authorization, security, dependencies, and secrets.
6. Show the staged diff and proposed Jira-keyed commit message; obtain approval before committing. Then obtain separate approval before pushing. Verify the remote branch and commit after push.
7. Open/update a PR only after showing its target, title, body, linked Jira story, verification evidence, and risks and receiving approval. Follow human review and repository CI requirements. Never represent unreceived approval as granted.
8. For a dependent story, use the merged integration base unless the team explicitly approves another branch strategy. Do not stack work on an unreviewed branch without recording that decision.
9. Mark Jira done only after required PR merge and checks succeed, and with approval for that status write.

## Deployment and closeout

Deployment is a separate stage. Confirm target project/environment/region/resource, source revision, access policy, configuration/secrets, verification and rollback plan; obtain approval for that exact scope before cloud writes. Verify rollout and health checks, record the deployed revision, then reconcile Jira and delivery evidence. If tools/permissions are unavailable, state the gap without claiming deployment.
