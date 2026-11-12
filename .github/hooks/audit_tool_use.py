"""Print a minimal diagnostic before or after a Copilot tool call."""

import json
import sys


def main() -> int:
    phase = sys.argv[1] if len(sys.argv) > 1 else "unknown phase"
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeDecodeError):
        sys.stderr.write("[Module 2 hook] Could not parse event JSON.\n")
        sys.stdout.write("{}\n")
        return 0

    tool_name = event.get("toolName") if isinstance(event, dict) else None
    if not isinstance(tool_name, str):
        sys.stderr.write(f"[Module 2 hook] {phase}: event did not contain a toolName.\n")
    else:
        # Do not log prompts, arguments, results, or environment variables.
        label = "Before tool" if phase == "before" else "After successful tool"
        sys.stderr.write(f"[Module 2 hook] {label}: {tool_name}\n")

    # Empty output makes no permission decision or post-tool change.
    sys.stdout.write("{}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
