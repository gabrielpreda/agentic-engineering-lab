"""Run Target-project pytest after relevant edits and return bounded agentStop feedback."""

import json
import os
from pathlib import Path
import re
import subprocess
import sys


HOOK_TIMEOUT_SECONDS = 85
MAX_REASON_CHARS = 1200


def emit(payload: dict[str, str]) -> None:
    sys.stdout.write(json.dumps(payload, ensure_ascii=True) + "\n")


def diagnostic(message: str) -> None:
    print(message[:MAX_REASON_CHARS], file=sys.stderr)


def fail(reason: str, retry_already_used: bool) -> None:
    if retry_already_used:
        diagnostic("Tests are still unverified or failing after the Hook continuation: " + reason)
        emit({"decision": "allow"})
    else:
        emit({"decision": "block", "reason": reason[:MAX_REASON_CHARS]})


def changed_python_files(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all", "-z"],
        cwd=root,
        check=True,
        capture_output=True,
        timeout=10,
    )
    # Porcelain -z records end in NUL. For rename/copy records, the first path
    # is followed by a second NUL-delimited path; both are considered below.
    records = result.stdout.decode("utf-8", errors="replace").split("\0")
    paths: list[str] = []
    skip_next = False
    for record in records:
        if not record:
            continue
        if skip_next:
            paths.append(record)
            skip_next = False
            continue
        status = record[:2]
        path = record[3:] if len(record) > 3 else ""
        if path:
            paths.append(path)
        if "R" in status or "C" in status:
            skip_next = True
    return sorted({
        path for path in paths
        if path.endswith(".py") and (path.startswith("app/") or path.startswith("tests/"))
    })


def project_python(root: Path) -> list[str] | None:
    candidates = [root / ".venv" / "bin" / "python", root / ".venv" / "Scripts" / "python.exe"]
    interpreters = [str(path) for path in candidates if path.is_file()] + [sys.executable]
    for python in dict.fromkeys(interpreters):
        try:
            probe = subprocess.run(
                [python, "-m", "pytest", "--version"],
                cwd=root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=5,
            )
        except (OSError, subprocess.TimeoutExpired):
            continue
        if probe.returncode == 0:
            return [python, "-m", "pytest", "-q"]
    return None


def concise_output(output: str) -> str:
    useful = []
    for line in output.splitlines():
        stripped = line.strip()
        if re.search(r"\b(FAILED|ERROR|failed|error|passed|skipped|warnings?)\b", stripped, re.I):
            useful.append(stripped)
    if not useful:
        useful = ["pytest exited unsuccessfully; detailed output is available by running pytest manually."]
    return "\n".join(useful[-8:])[:800]


def main() -> None:
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeError):
        diagnostic("Test feedback Hook received malformed JSON; no test result was produced.")
        emit({})
        return
    if not isinstance(event, dict) or not isinstance(event.get("cwd"), str):
        diagnostic("Test feedback Hook input must be an object with a cwd string; no test result was produced.")
        emit({})
        return
    if not isinstance(event.get("stop_hook_active"), bool):
        diagnostic("Test feedback Hook input is missing boolean stop_hook_active; no test result was produced.")
        emit({})
        return

    root = Path(event["cwd"]).resolve()
    try:
        changes = changed_python_files(root)
    except (OSError, subprocess.SubprocessError) as exc:
        fail(f"Could not inspect Target project changes ({type(exc).__name__}); run pytest manually.", event["stop_hook_active"])
        return
    if not changes:
        emit({})
        return

    command = project_python(root)
    if command is None:
        fail("pytest is unavailable in the Target project's .venv or Hook Python; install requirements-test.txt and run python -m pytest -q.", event["stop_hook_active"])
        return
    try:
        result = subprocess.run(
            command,
            cwd=root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=HOOK_TIMEOUT_SECONDS,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
    except subprocess.TimeoutExpired as exc:
        fail(f"pytest timed out after {HOOK_TIMEOUT_SECONDS}s; run python -m pytest -q manually and inspect the result.", event["stop_hook_active"])
        return
    except OSError as exc:
        fail(f"Could not start pytest ({type(exc).__name__}); run python -m pytest -q manually.", event["stop_hook_active"])
        return

    if result.returncode == 0:
        emit({})
        return
    summary = concise_output((result.stdout or "") + "\n" + (result.stderr or ""))
    fail(
        "Target-project pytest failed (exit " + str(result.returncode) + "). "
        "Diagnose and fix the relevant failure, then verify with pytest. Summary:\n" + summary,
        event["stop_hook_active"],
    )


if __name__ == "__main__":
    main()
