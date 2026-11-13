"""Add a small requirements-status reminder when an agent session starts."""

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
WORKSHEET = PROJECT_ROOT / "docs" / "requirements" / "task-priority.md"


def main() -> None:
    try:
        content = WORKSHEET.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        print("{}")
        return

    status = next(
        (line.split(":**", 1)[1].strip() for line in content.splitlines()
         if line.strip().lower().startswith("**status:**")),
        "unspecified",
    )
    context = (
        f"Requirements worksheet exists at "
        f"{WORKSHEET.relative_to(PROJECT_ROOT).as_posix()} (status: {status}). "
        "Read it before planning or editing related behavior. Preserve its open questions "
        "and assumptions; do not treat a draft as approved."
    )
    print(json.dumps({"additionalContext": context}))


if __name__ == "__main__":
    main()
