"""Stop hook: detect task ID overlap between active and completed sections in TASKS.md."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hook_utils import check_stop_cache, run_hook, write_stop_cache  # noqa: E402


def _extract_section_task_ids(content: str, section_name: str) -> set[str]:
    """Extract task IDs (T-xxx) from a named section of TASKS.md.

    Args:
        content: Full TASKS.md text.
        section_name: Section header (e.g. "Active Tasks", "Completed Tasks").

    Returns:
        Set of task ID strings found in that section.
    """
    section_match = re.search(
        rf"## {re.escape(section_name)}\s*\n(.*?)(?=\n## |\Z)", content, re.DOTALL
    )
    if not section_match:
        return set()
    return set(re.findall(r"(T-\S+)(?=:)", section_match.group(1)))


def main(hook_input: dict) -> None:
    """Check TASKS.md for task IDs appearing in both active and completed sections.

    Args:
        hook_input: Parsed JSON dict from stdin.
    """
    if check_stop_cache("task_dedup"):
        print(
            "[TASK DEDUP] No files changed since last pass -- skipping (cached PASS)",
            file=sys.stderr,
        )
        sys.exit(0)

    # Find project root
    project_root = Path(__file__).resolve().parent.parent.parent
    tasks_file = project_root / "TASKS.md"

    if not tasks_file.exists():
        sys.exit(0)

    try:
        content = tasks_file.read_text(encoding="utf-8")
    except OSError:
        sys.exit(0)

    # Collect task IDs from active sections
    active_ids: set[str] = set()
    for section in ["In Progress", "Active Tasks", "Blocked"]:
        active_ids |= _extract_section_task_ids(content, section)

    completed_ids = _extract_section_task_ids(content, "Completed Tasks")

    overlap = active_ids & completed_ids
    if overlap:
        sorted_overlap = sorted(overlap)
        print(
            f"[TASK DEDUP] Task ID(s) found in BOTH active and completed sections: "
            f"{', '.join(sorted_overlap)}\n"
            f"  Each task must appear in exactly one section.\n"
            f"  Remove the duplicate from either active or completed before stopping.",
            file=sys.stderr,
        )
        sys.exit(2)

    write_stop_cache("task_dedup")
    sys.exit(0)


if __name__ == "__main__":
    run_hook("task_dedup_check", main)
