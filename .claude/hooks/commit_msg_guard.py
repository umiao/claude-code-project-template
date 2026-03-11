"""PreToolUse hook: block git commits containing CJK characters in messages."""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hook_utils import run_hook  # noqa: E402

# Matches any CJK Unified Ideographs (common Chinese/Japanese/Korean characters)
CJK_PATTERN = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]")

# Patterns that extract a commit message from a git commit command
COMMIT_MSG_FLAGS = re.compile(
    r"""git\s+commit\s+.*?(?:-m\s+(?:"([^"]*?)"|'([^']*?)'|(\S+)))""",
    re.DOTALL,
)


def main(hook_input: dict) -> None:
    """Block git commit commands whose message contains CJK characters."""
    tool_name = hook_input.get("tool_name", "")
    if tool_name != "Bash":
        sys.exit(0)

    tool_input = hook_input.get("tool_input", {})
    command = tool_input.get("command", "")

    # Only check commands that look like git commit
    if "git commit" not in command and "git commit" not in command.replace("  ", " "):
        sys.exit(0)

    # Extract commit message from -m flag
    match = COMMIT_MSG_FLAGS.search(command)
    if not match:
        # No -m flag found (could be --amend, interactive, etc.) -- allow
        sys.exit(0)

    # Get whichever capture group matched
    msg = match.group(1) or match.group(2) or match.group(3) or ""

    if CJK_PATTERN.search(msg):
        print(
            json.dumps({
                "decision": "block",
                "reason": (
                    "Commit message contains CJK characters. "
                    "All commit messages must be in English. "
                    f"Message: {msg[:80]}"
                ),
            })
        )
        sys.exit(0)

    # No CJK found -- allow
    sys.exit(0)


if __name__ == "__main__":
    run_hook("commit_msg_guard", main)
