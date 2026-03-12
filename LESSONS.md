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