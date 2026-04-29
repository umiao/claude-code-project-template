# Lessons Learned

> Only log if: bug >10 min to debug, surprising behavior, effective pattern, non-obvious gotcha.

<!-- ENTRY FORMAT:

### [YYYY-MM-DD] Short descriptive title
- **Context**: What I was trying to do
- **What went wrong / What I learned**: The core insight
- **Fix / Correct approach**: How to do it right
- **Related task**: T-XX-N (if applicable)
- **Tags**: #tag1 #tag2 (for grep-based lookup)

-->

1. Windows UTF-8 (universal gotcha)
  - Python defaults to cp1252 on Windows. Non-ASCII paths/content break silently.
  - Rule: Force encoding="utf-8" on all open(), subprocess.run(), Path.read_text(). Force UTF-8 on sys.stdin/stdout/stderr in hooks.

  2. Stop hooks MUST output JSON to stdout (mentioned twice - both prompt and command types)
  - Exit codes alone = "JSON validation failed". Empty stdout = crash.
  - Rule: Every Stop hook prints {"ok": true} or {"ok": false, "reason": "..."} on every exit path (success, failure, timeout, error).
  Diagnostics go to stderr only.

  3. Hooks must never crash on bad stdin
  - /clear and other commands send unexpected input to hooks.
  - Rule: Never use bare json.load(sys.stdin). Always try/except with diagnostics. On parse failure: warn to stderr, exit 0.

  4. Shared hook_utils.py pattern
  - DRY boilerplate: UTF-8 init, JSON parsing, exception catching.
  - Rule: Use a single run_hook(name, main_fn) entry point for all hooks. Hooks become pure business logic.

  5. Rename/replace = reverse-reference scan
  - Plans list what to create, not what references the old thing.
  - Rule: grep -r "old_name" before and after. Add all referencing files to work list.

  6. Debug philosophy: check the contract before blaming the LLM
  - "Validation failed" = schema mismatch (deterministic). Not "LLM non-determinism".
  - Rule: (1) read exact error, (2) read docs for expected schema, (3) compare actual vs expected, (4) fix minimal delta. Never rewrite
  architecture on first failure.

### [2026-03-18] Stop hooks don't fire when Claude ends with pure text (no tool call)
- **Context**: A ruff F401 error slipped through because the session ended with a pure text response, and the Stop hook only fires after tool calls.
- **What went wrong / What I learned**: The Stop hook (lint_check.py) is not guaranteed to run on every session exit. If Claude's final response is pure text with no tool call, the hook infrastructure never triggers. Additionally, lint cache could produce false passes if files changed between cache write and next session.
- **Fix / Correct approach**: (1) Added `scripts/check.sh` as unified ruff+pytest runner. (2) Made running `bash scripts/check.sh` Step 0 in Exit Protocol -- primary defense. (3) Removed lint cache from lint_check.py so every Stop hook invocation runs fresh.
- **Tags**: #hooks #lint #ruff #exit-protocol #cache

### [2026-03-20] batch command doc/code mismatch caused silent data loss
- **Context**: `task_db.py batch` created tasks with empty title and description because batch call used nested `{"cmd": "add", "args": {"title": "..."}}` format but code reads flat keys: `cmd_dict.get("title", "")`.
- **What went wrong / What I learned**: Documentation showed `args` nesting format that never existed in implementation. Batch add had no validation -- empty title silently accepted. The `{"ok": true}` response gave no signal of data loss.
- **Fix / Correct approach**: (1) Support BOTH flat and nested-args formats. (2) Added title-non-empty validation. (3) Fixed docs to show correct flat format. Key takeaway: any CLI command returning success must validate required fields.
- **Tags**: #task-db #batch #validation #docs-code-mismatch

### [2026-03-15] SQLAlchemy create_all() does not ALTER existing tables
- **Context**: Added new column to model. Tests passed (in-memory DBs start fresh), but production crashed with missing column error.
- **What went wrong / What I learned**: `Base.metadata.create_all()` only creates NEW tables, never ALTER TABLE for existing ones. In-memory test DBs always start from scratch, hiding this gap.
- **Fix / Correct approach**: Added versioned auto-migration system that tracks applied versions. Each migration is idempotent. Added file-based migration tests and schema audit tests.
- **Tags**: #sqlalchemy #migration #sqlite #schema-drift

### [2026-03-02] Ruff version drift between local and CI
- **Context**: requirements.txt had `ruff>=0.1.0` (loose pin) while CI ran `pip install ruff` (latest). Newer ruff versions add rules under the `UP` category that the project selects, causing CI-only lint failures invisible locally.
- **What went wrong / What I learned**: Loose version pins + separate install commands = silent version drift. CI gets a different ruff than local, and new rules break the build with no local repro.
- **Fix / Correct approach**: (1) Pin `ruff==X.Y.Z` exactly in requirements.txt. (2) CI lint job uses `pip install -r requirements.txt` instead of bare `pip install ruff`. (3) Pre-commit hook verifies installed ruff version matches the pin before every commit.
- **Tags**: #ruff #ci #version-drift #pre-commit

### [2026-03-11] Unauthorized theme switch reversal (T-P0-9 incident)
- **Context**: During T-P0-9, I changed the active theme from NexT back to yilia in `_config.yml` to activate the Life sidebar widget without explicit user approval. This reversed the carefully planned NexT migration completed in T-P0-1 through T-P0-4.
- **What went wrong / What I learned**: Theme switches are major architectural changes that affect the entire site appearance, user experience, and feature compatibility. Making such changes without presenting options and waiting for user decision violates user autonomy and can waste previous work. The user had invested significant effort migrating to NexT; reversing it without approval was incorrect.
- **Fix / Correct approach**: Before making ANY major change (theme switches, removing functionality, reversing approved decisions, changing deployment targets), I must: (1) State the proposed change and why, (2) List 2-3 alternatives including "do nothing", (3) Show impact (what breaks, what changes, rollback cost), (4) Wait for explicit user approval before executing. This is now codified in CLAUDE.md "Major Change Approval Protocol".
- **Related task**: T-P0-10
- **Tags**: #theme #approval #major-change #communication

### [2026-03-11] Task ID "P = Phase" anti-pattern went undetected
- **Context**: When adding 18 new tasks to TASKS.md, I numbered them T-P3-*, T-P4-*, T-P5-* treating "P" as a sequential phase counter (Phase 1/2/3 of new work), continuing the pattern from completed tasks (P0/P1/P2). CLAUDE.md said "P = priority" but lacked explicit P0-P3 definitions, so the misuse was not caught by hooks or review.
- **What went wrong / What I learned**: The existing `task_header_check.py` hook validates ID *format* (T-P\d+-\d+) but cannot validate *semantics* (whether P reflects actual priority). Without explicit priority-level definitions, "P3" looks valid whether it means "Stretch Goal" or "Phase 3". Convention drift happens when rules are implicit.
- **Fix / Correct approach**: (1) Added explicit priority definitions to CLAUDE.md: P0=Must Have, P1=Should Have, P2=Nice to Have, P3=Stretch. (2) Added prohibition: "Never use P as a phase/stage counter." (3) Reassigned all 18 task IDs based on actual priority. (4) Changed TASKS.md section headers from "Phase N" to priority-based grouping ("Must Have (P0)", etc.).
- **Tags**: #task-naming #convention-drift #implicit-rules

### [2026-03-15] Deployed from wrong branch, sensitive content leaked
- **Context**: `hexo deploy` was run from `blog-refactor` instead of `main`, causing unreleased feature pages (knowledge-map, cheatsheet, concepts, interview hub) and sensitive interview prep posts (`Behavioral-Interview-Questions-Crack.md`, `brainteaser_1.md`) to go live on `umiao.github.io`.
- **What went wrong / What I learned**: The deploy script had no branch guard -- it would happily deploy from any branch. Additionally, sensitive personal content was stored in `source/_posts/` alongside regular posts, with no safety net to prevent publication.
- **Fix / Correct approach**: (1) Added branch guard to `tools/safe-deploy.sh` that blocks deploys from non-main branches (with `DEPLOY_ALLOW_BRANCH` escape hatch). (2) Moved sensitive files to `source/_drafts/`. (3) Added source-path sensitive file check in deploy script (more stable than slug-based checks). (4) Added `render_drafts` config guard. Defense in depth: multiple checks catch the problem at different stages.
- **Tags**: #deployment #security #branch-guard #sensitive-content

### [2026-04-11] [PROPAGATED] Long-running bash scripts must trap SIGPIPE and log to an owned file
- **Source**: MLInterviewPrep autonomous_run.sh (forensic diagnosis 2026-04-11, propagated to all projects)
- **Rule**: Any bash script with `set -e` that loops and uses `echo` between iterations will die from SIGPIPE if its stdout fd gets closed by a parent harness (e.g., Claude Code's `run_in_background`). **Fix**: (1) `trap '' PIPE` at the top. (2) `exec > >(tee -a logs/<script>.log) 2>&1` to own stdout. (3) On Windows, use `python` not `python3` (Store stub exits code 49). A PowerShell native version (`autonomous_run.ps1`) is also available in this template.
- **Tags**: #bash #sigpipe #orchestration #claude-code #background-subprocess #windows

### [2026-03-20] [PROPAGATED] Claude Code Bash tool ignores .bashrc
- **Source**: MLInterviewPrep (propagated via cross-project review 2026-03-21)
- **What I learned**: The Bash tool runs non-login, non-interactive shells. `.bashrc` and `.bash_profile` are NOT sourced. The only way to inject env vars is `$CLAUDE_ENV_FILE` (written by a SessionStart bash hook). All hook commands in `settings.json` must use absolute paths.
- **Tags**: #windows #bash-tool #path #hooks #claude-code #propagated

### [2026-04-27] [UNIVERSAL] task_db.py routes by Path.cwd(), not by the script's location -- explicit cd or --project required
- **Source**: root LESSONS.md (Gen_AI_Proj/LESSONS.md, 2026-04-27); root T-P1-255 added the systemic fix, root T-P2-259 propagated this entry.
- **Context**: Adding a P0 hotfix task to MLInterviewPrep's task_db before launching `MLInterviewPrep/scripts/autonomous_run.sh`. Called `python "$ROOT/MLInterviewPrep/.claude/hooks/task_db.py" add --priority P0 ...` from a Bash session whose cwd was the workspace root. Got `{"ok": true, "id": "T-P0-253"}` and assumed it landed in MLI's tasks.db.
- **What went wrong**: The autonomous_run.sh's inner Claude session reported "no unblocked tasks" and worked on stale emoji warnings instead. Direct sqlite probe confirmed the row sat in the **root** `.claude/tasks.db`, not MLInterviewPrep's. Reason: `task_db.py`'s `_find_project_root()` returns the first ancestor of `Path.cwd()` that contains a `CLAUDE.md`. Both root and MLI have CLAUDE.md. With cwd = root, the script picked root's DB. The fact that the script binary lives under `<subproject>/.claude/hooks/` is irrelevant -- `__file__` is only the fallback when cwd has no CLAUDE.md.
- **Fix / Correct approach**: ALWAYS `cd <subproject> && python .claude/hooks/task_db.py ...` when targeting a sub-project's task_db from the workspace root. Calling `python <subproject>/.claude/hooks/task_db.py ...` with cwd=root silently routes to the root DB. Preferred: pass `--project <name>` or `--cwd <path>` (added in root T-P1-255) so routing is explicit from any cwd. Symptom to watch for: an autonomous_run.sh session that says "no unblocked tasks" right after you added one -- first check `python -c "import sqlite3; ..."` against BOTH DBs.
- **Related task**: T-P0-253 (mis-routed) -> T-P0-626 (re-added correctly under MLI after delete from root); root T-P1-255 (--project flag), root T-P2-259 (propagation).
- **Tags**: #task-db #routing #cwd #autonomous #orchestrator #gotcha #universal #propagated

### [2026-04-27] [UNIVERSAL] autonomous_run.sh trusts session_state.json `all_done=true` even when task_db has unblocked work
- **Source**: root LESSONS.md (Gen_AI_Proj/LESSONS.md, 2026-04-27); root T-P1-257 added the orchestrator-startup reset, root T-P2-259 propagated this entry.
- **Context**: After (mis-)adding T-P0-253 to MLI's task_db (in fact root's, see lesson above), launched `bash MLInterviewPrep/scripts/autonomous_run.sh`. Inner Claude session opened, looked at session_state.json (which had `all_done=true` from a 2026-04-26 run that legitimately drained the queue), and concluded there was nothing to do. Picked up emoji-cleanup of unrelated scripts as filler instead of re-checking task_db.
- **What went wrong**: session_state.json is sticky across orchestrator invocations. The orchestrator never resets `all_done` at start; the inner session inherits the prior state and treats it as authoritative even when task_db.py reports unblocked work. Same sticky-gate class as the 2026-04-19 [UNIVERSAL] "human-approval gate prose stays sticky" lesson, but in orchestrator persistent state instead of in a task description.
- **Fix / Correct approach**: At orchestrator startup (in `autonomous_run.sh` before the first session loop), reset `session_state.json` to `all_done=false` IFF `task_db.py has-unblocked` returns truthy. Equivalently: the inner session's "next-pick" logic must always run `task_db.py list --status active` and treat session_state.json as a hint, not a final verdict. Defensive workaround: after adding new tasks to task_db, manually edit `.claude/session_state.json` to set `"all_done": false` before launching.
- **Related task**: T-P0-626 (the hotfix that autonomous_run.sh failed to pick up); root T-P1-257 (orchestrator startup reset), root T-P2-259 (propagation).
- **Tags**: #autonomous #orchestrator #session-state #sticky-state #task-db #routing #gotcha #universal #propagated