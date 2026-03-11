# Project Context

<!-- CUSTOMIZE: Replace this section with your project's overview -->

## Project Overview
<!-- Describe what your project does in 2-3 sentences -->

## Tech Stack
<!-- List your core technologies -->
- Python 3.11+
- pytest (testing)
- ruff (linting)

## Key Constraints
<!-- CUSTOMIZE: Add your project-specific constraints -->
- All API keys and cookies from .env, never hardcoded
- Every function must have type hints and docstring

## File Structure
<!-- CUSTOMIZE: Describe your project's directory layout -->
- `src/` - Source code
- `tests/` - Test files
- `config/` - Configuration files
- `data/` - Runtime data (not in git)
- `tools/git-hooks/` - Git hook sources (installed via `tools/setup-hooks.sh`)

## Invariants (must always hold, violation = bug)
<!-- CUSTOMIZE: List your project's invariants. These are checked by /review -->
1. .env file never tracked by git
2. No hardcoded secrets in code
3. <!-- Add your domain-specific invariants here -->

## Git Conventions
- **Language**: All commit messages must be in English. No CJK characters.
- **Enforcement**: 3-layer defense -- PreToolUse hook (`commit_msg_guard.py`), git `commit-msg` hook, CI pipeline.

## Code Style
- Use ruff for linting
- Type checking: mypy
- Test: pytest
- **Regression tests**: When fixing a bug, always add a regression test
- **No emoji**: Never use emoji characters in code, docs, configs, or hook output.
  Use ASCII text tags (e.g., [DONE], [FAIL], [WARN]) instead.
- **Explicit UTF-8**: All file I/O and subprocess calls must specify `encoding="utf-8"`.
  Never rely on locale defaults (cp1252 on Windows).

## Prohibited Actions
- Never hardcode API keys, cookies, or personal info
- Never use emoji characters anywhere in the project
- Never use subprocess.run(text=True) without encoding="utf-8"
- Never read/write files without explicit encoding="utf-8"
<!-- CUSTOMIZE: Add your project-specific prohibitions -->

### Major Change Approval Protocol

**Definition of Major Changes** (require explicit user approval before execution):
- **Theme switches**: Changing the active Hexo theme in `_config.yml`
- **Removing functionality**: Deleting features, widgets, or pages that users interact with
- **Reversing approved decisions**: Undoing changes from completed tasks (e.g., reverting T-P0-1 through T-P0-4 NexT migration)
- **Deployment target changes**: Modifying publish repository, deployment scripts, or public URLs
- **Breaking changes to content structure**: Bulk renaming/moving posts, changing permalink format

**Required Process** (4 steps, all mandatory):
1. **State the proposed change and why**: Clearly describe what will change and the motivation
2. **List alternatives**: Present at least 2-3 alternative approaches (including "do nothing")
3. **Show impact**: Explain what will break, what users will see differently, rollback difficulty
4. **Wait for explicit approval**: Do NOT proceed until user responds with clear confirmation

**What is NOT a major change** (can proceed without approval workflow):
- Bug fixes within the current theme (e.g., fixing broken links, correcting config typos)
- Adding requested content (new posts, pages, features explicitly asked for in current task)
- Non-visible config tweaks (performance tuning, SEO meta tags, analytics)
- Routine maintenance (dependency updates, linting fixes, test improvements)

**Example Application**:
```
User: "switch back to NexT theme"

Correct response:
"I propose switching the active theme from yilia to NexT to complete the migration
approved in T-P0-1 through T-P0-4.

Alternatives:
1. Keep yilia (current state)
2. Switch to NexT (completes migration)
3. Evaluate a different theme

Impact:
- Homepage appearance will change (NexT layout vs yilia layout)
- Life sidebar widget will need migration (yilia-specific customization)
- Tags/Categories/About pages use NexT native rendering
- Rollback: change theme in _config.yml and run hexo generate

May I proceed with option 2 (switch to NexT)?"

[Wait for user approval before executing]
```

## Behavior Rules
- **Fix violations immediately**: When a check you run (lint, emoji scan, tests) discovers
  violations in project files, fix them immediately.

### Task Planning Mode
When the user says "plan tasks" / "edit TASKS.md only" / contains keyword "TASKS.md":
- **ONLY** read code and edit TASKS.md (add/reorder/restructure tasks, set dependencies)
- Do **NOT** execute any task, write code, create files, or run tests
- Do **NOT** use TaskCreate/TaskUpdate/TaskList tools (session-only, not persistent)
- Write clear task specs with acceptance criteria, complexity, and dependencies
- End by summarizing what changed in TASKS.md

## Hook Development Rules
- **Never use bare `json.load(sys.stdin)`** -- always use `hook_utils.safe_read_stdin()`
- **Hooks must never crash** -- infrastructure errors must exit 0, never a raw traceback
- **Use `hook_utils.run_hook()`** as the entry point for all hooks
- **New hooks**: copy `.claude/hooks/_template.py` and fill in the logic

## Human Input Protocol
- Tasks requiring human-provided files are tagged `[NEEDS-INPUT: description]` in TASKS.md
- `docs/human_input/` contains the master checklist and per-task spec files
- Use `/collect-input` to check status, guide input, validate, and unblock tasks

---

## Session Workflow

The **SessionStart hook** provides authoritative startup context including task status,
recent progress, and lessons. Trust its output at session start.

### During Work
- Work on **one task at a time**. Move it to "In Progress" in TASKS.md when you begin.
- Refer to the task's **Acceptance Criteria** as your definition of done.
- If you discover new work, add it to TASKS.md. Don't silently absorb scope.
- For **L-complexity tasks**, maintain `.claude/checkpoint.json` with sub-task progress:
  ```json
  {"task": "T-XX-N", "subtasks": [{"name": "...", "done": false}],
   "last_working_file": "src/...", "last_working_line": 42}
  ```

### Autonomous Mode
When triggered via `tools/autonomous_run.sh`, read `docs/workflow/autonomous.md` for
the full ruleset.

---

## Exit Protocol

Before stopping, complete these steps (the **Stop hook** enforces them):

1. **Verify**: Run code, check outputs exist, run tests if applicable
2. **PROGRESS.md**: Append a session entry (format below)
3. **TASKS.md**: Update task status (done = remove spec from active section AND add to Completed)
4. **LESSONS.md**: Only if bug >10 min, surprising behavior, or effective pattern

```
## YYYY-MM-DD HH:MM -- [TASK-XXX] Brief Title
- **What I did**: 1-3 sentences
- **Deliverables**: Files created/modified
- **Sanity check result**: What was verified
- **Status**: [DONE] / [PARTIAL] (what remains) / [BLOCKED] (why)
- **Request**: Move TASK-XXX to Completed / No change
```

Full protocol details: `docs/workflow/exit-protocol.md`

---

## File Conventions

| File | Purpose | Update frequency |
|------|---------|-----------------|
| `TASKS.md` | Task backlog and status tracking | Every session |
| `PROGRESS.md` | Chronological session log | Every session (append-only) |
| `LESSONS.md` | Critical knowledge and mistakes | Only when a lesson is learned |

TASKS.md is the **single source of truth** for what needs to be done.
