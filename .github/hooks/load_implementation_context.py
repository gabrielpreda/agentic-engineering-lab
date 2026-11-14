"""Remind a new agent session to verify the latest implementation handoff."""

import json
from pathlib import Path


HANDOFF = Path("docs/handoffs/task-priority.md")


def field_value(lines: list[str], label: str, default: str) -> str:
    prefix = f"**{label}:**".lower()
    for line in lines:
        stripped = line.strip()
        if stripped.lower().startswith(prefix):
            return stripped[len(prefix) :].strip()
    return default


def main() -> None:
    try:
        lines = HANDOFF.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError):
        print("{}")
        return

    task = field_value(lines, "Current task", "unspecified")
    status = field_value(lines, "Task status", "unspecified")
    context = (
        f"Implementation handoff: {HANDOFF.as_posix()} (current task: {task}; "
        f"task status: {status}). Read the handoff and current requirements/spec/task "
        "artifacts, then verify its claims against the repository and test state before editing."
    )
    print(json.dumps({"additionalContext": context}))


if __name__ == "__main__":
    main()

