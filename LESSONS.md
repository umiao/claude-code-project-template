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

### [2026-04-30] [UNIVERSAL] When user reports "I don't see changes" on the frontend, ALWAYS check dev-server proxy port vs actual backend port BEFORE concluding it's React Query / browser cache
- **Source**: MLInterviewPrep LESSONS.md (2026-04-30); promoted via T-P2-665.
- **Context**: Edited Pinterest data via direct DB writes (separate Invariant-3 violation, see other 2026-04-30 lesson). User reported "我在 dashboard 上没看见改动". I verified the data was in the DB by hitting `http://localhost:8000/api/...` directly (returned 200 + correct data) and concluded "browser cache, hard-refresh". User pushed back: "我之前都没有遇到过这个问题 请谨慎认真确认 root cause". After deeper investigation found the real cause: backend was bound to port 8000, but `vite.config.ts:10 target: "http://localhost:8100"` and `scripts/dev.py:22 BACKEND_PORT = 8100` make 8100 the canonical port. Frontend at `:5173` proxies `/api` to `:8100` -> connection refused -> "Failed to load interview timeline" -> dashboard appears empty. Backend on `:8000` was unreachable from the frontend even though I could reach it via curl.
- **What went wrong**: I tested the backend by hitting it directly, not through the same path the browser uses. The browser doesn't curl `:8000` -- it goes through Vite's proxy. A direct curl to the backend confirms the backend works; it does NOT confirm the frontend can reach the backend. Two-port-system bugs (frontend proxy + backend) need testing through the proxy, not around it.
- **Fix / Correct approach**: When user reports frontend doesn't show backend changes, do this BEFORE blaming cache: (1) check `vite.config.ts` (or equivalent) for the proxy `target` port, (2) `curl <proxy_target>/api/...` -- not `curl <backend_actual>/api/...`. If proxy target returns connection-refused but the actual backend is up on a different port, that's the bug -- the user's environment has the backend on a non-canonical port. Fix: identify the canonical launcher (e.g. `scripts/dev.py BACKEND_PORT = 8100`) and have the user restart through it. Detection: any time `curl backend_canonical_port/api` differs from `curl backend_actual_port/api`, suspect the port-mismatch class.
- **Detection heuristic**: dev server framework (Vite / Next / CRA) proxies `/api` to a fixed `target`. If the target port is NOT what the running backend bound to, frontend silently 502s or "Failed to load X". Always verify the proxy target FIRST.
- **Related task**: T-P0-651 (the original Pinterest itinerary update); T-P0-655 (Phase-1 verification, where the autonomous session correctly found this and worked around it via temporary uvicorn on 8100 for the screenshot).
- **Tags**: #frontend #vite-proxy #port-mismatch #dev-server #symptom-vs-cause #universal #propagated

### [2026-04-30] [UNIVERSAL] User says "dashboard" / "app 那边" / "left nav first item" -> they mean a UI widget on the named page, NOT prose in a prep doc
- **Source**: MLInterviewPrep LESSONS.md (2026-04-30); promoted via T-P2-665.
- **Context**: User asked to update Pinterest VO schedule ("更新 Pinterest onsite"). I edited `company_documents.id=83` (Pinterest prep-doc prose) and the `companies.interview_stages` JSON column. Both wrong surface. The Dashboard's `InterviewTimeline` widget (src/frontend/src/components/timeline/InterviewTimeline.tsx) reads `GET /timeline/events` which queries the `interview_events` table -- that was the surface the user actually meant. The prep doc is a study notebook; calendar/event data lives in `interview_events`. The misdirected work shipped to the DB and the user reported "dashboard 上没看见改动" because the widget was reading a different table.
- **What went wrong**: I matched "Pinterest onsite update" to the most prominent Pinterest text I could find (the prep doc, ~12 KB of prose) without first asking "which UI surface renders this?" Pattern-matching from the largest text surface is the failure mode -- it works for prose updates and FAILS for everything else (schedule, status, checklist, focus). Recency priming makes it worse: if the previous turn edited `company_documents`, the next "update" request will keep aiming there even when the user named a different surface.
- **Fix / Correct approach**: For ANY request mentioning a UI surface ("dashboard", "app 那边", "左侧 tab", "first nav item", "left nav", "我们 app"), FIRST identify the frontend page + widget being referenced, then trace `widget -> queryKey -> /api/<endpoint> -> <DB table>` BEFORE editing anything. The mapping table for MLInterviewPrep is in `CLAUDE.md` "Surface Identification" section (canonical source). Routing rules: schedule/itinerary/calendar = `interview_events` (NEVER `company_documents.content`); pipeline status = `companies.status`; daily focus = derived from `framework_nodes` + `reading_progress`; per-company checklist = `companies.prep_notes`; prose study notes ONLY = `company_documents.content`. Two-layer enforcement: (1) `/dashboard` skill at `.claude/skills/dashboard/SKILL.md` walks the 6-step protocol; (2) `.claude/hooks/invariant3_guard.py` (T-P0-660 + T-P0-660b extension) blocks schedule-shaped prose writes (ISO-8601 + interviewer name) to `company_documents.content`.
- **Universal pattern** (apply to any project): when a user names a UI surface, the prior is "find the widget, walk the data chain, edit the source table" -- NOT "find the largest text artifact mentioning the topic". Every project should publish a widget -> table map in CLAUDE.md before the autonomous loop can be trusted with surface-targeted edits.
- **Related task**: T-P0-651 (the misdirected work, superseded), T-P0-654 (the correct fix via interview_events seed -- per supersede chain in T-P0-651), T-P0-660 / T-P0-660b (lint enforcement), T-P0-661 (root-cause investigation memo at `logs/2026-04-30_pinterest_root_cause.md`), T-P1-656 (CLAUDE.md "Surface Identification" + `/dashboard` skill).
- **Tags**: #ux-target-identification #dashboard #widget-vs-prose #interview-events #universal #surface-identification #propagated

### [2026-04-30] [UNIVERSAL] Direct SQL UPDATE on data/*.db violates Invariant 3 -- every DB row must originate from a git-tracked, idempotent Python seed
- **Source**: MLInterviewPrep LESSONS.md (2026-04-30); promoted via T-P2-665.
- **Context**: Twice this session I wrote `scripts/migrations/*.py` that called `sqlite3.connect(...).execute("UPDATE ..." | "INSERT ...")` directly against `data/mle_prep.db`. Specifically `scripts/migrations/add_uber_prob_nextword.py` and `scripts/migrations/update_pinterest_onsite_itinerary.py`. Both were idempotent on their own canonical keys, but they bypassed the seed-based source of truth. The DB is regenerable from `scripts/seed_*.py`; once a migration writes a row that no seed knows about, the next seed run wipes or diverges from it -- timebomb.
- **What went wrong**: `scripts/migrations/` as a directory pattern feels familiar from server-side projects (Django/Rails/Alembic migrations are normal there). In this project there are NO migrations -- there are only idempotent seeds. The mental model "I need a migration to add this row" is the trap; the correct mental model is "which seed owns this row, and how do I extend it idempotently?" Even when the migration is correct in isolation, it creates a divergence between (a) what's in the DB and (b) what the seed scripts would produce. Invariant 3: "every DB content row must have a git-tracked, idempotent Python seed script as its source of truth."
- **Fix / Correct approach**: For ANY DB content change: (1) identify the matching seed in `scripts/seed_*.py` (or create one if no seed owns the row type), (2) edit the seed body to include the new content, (3) re-run the seed -- it should print `[NEW]` for genuinely new rows and `[UNCHANGED]` on subsequent runs. Idempotency requires a canonical key (title / leetcode_id / path / `(company_id, scheduled_at, interviewer_name)` for `interview_events`) and a sentinel-based UPSERT. NEVER write `sqlite3.connect(DATA_DB_PATH).execute("UPDATE"|"INSERT"|"DELETE")` outside `scripts/seed_*.py`. If you find yourself doing it -- STOP, identify the seed that owns this row type, extend that seed instead.
- **Detection / enforcement**: `.claude/hooks/invariant3_guard.py` (T-P0-660 + T-P0-660b) blocks Write/Edit calls to files under `scripts/migrations/*` whose payload contains raw SQL writes against `data/*.db`. Sentinel detection runs on Bash-tool commands too. The hook is the second line of defense; the first is the prior in CLAUDE.md "Invariants" + the `/dashboard` skill protocol.
- **Universal pattern** (apply to any project with regenerable DB content): publish "where does each row type come from?" as a project invariant. If the DB is a projection of seed scripts (vs a long-lived hand-edited store), then `scripts/migrations/` is dead architecture -- replace it with seed extension. The lint hook pattern is portable: detect raw SQL writes against the project's data DB from any path outside the sanctioned seed dir, and block them.
- **Related task**: T-P0-651 (the misdirected migration writes), T-P0-654 (correct fix moving to interview_events seed), T-P0-660 (Phase 2 migration lint hook), T-P0-660b/T-P0-663 (schedule-shaped prose extension), T-P1-657 (Invariant-3 promotion: doc 84 §5 + problem 1097 to seed scripts; deprecation no-op for the two migration files).
- **Tags**: #invariant-3 #seed-not-migration #db-source-of-truth #lint-hook #universal #propagated

## 2026-05-02 — `claude -p ... --bare` reporting "Not logged in" is NOT evidence of auth state [UNIVERSAL] [#claude-cli #autonomous-mode #diagnosis-trap]
- **Lesson**: `claude -p PROMPT --bare` returns `"Not logged in · Please run /login"` *unconditionally* under OAuth-only auth, because per `claude --help`: "**Anthropic auth is strictly ANTHROPIC_API_KEY or apiKeyHelper via --settings (OAuth and keychain are never read)**" in `--bare` mode. The output is a structural artifact of the flag, not a state probe. Two separate hangs of `bash <project>/scripts/autonomous_run.sh ...` on 2026-05-02 (one ~7h overnight, one at 14:05) were misdiagnosed as "expired auth" using this probe; both were actually transient `claude -p` slow-start (cold MCP/plugin/hook init). After 16 probes, `claude auth status` returned `loggedIn: true subscription: max`, and 3 consecutive `claude -p` calls succeeded in 36s.
- **How to apply**:
  - **Use `claude auth status` for auth state**, not `claude -p ... --bare`. The former returns structured JSON with `loggedIn`, `email`, `subscriptionType`.
  - When `claude -p` hangs in a subshell with zero output, the default hypothesis should be **transient slow-start** (MCP server cold init, plugin sync, network blip), not auth. Kill + retry once before chasing structural causes.
  - Heartbeat-style monitor (size delta + task DB completion count) catches the silent-hang state within one tick (~60-90s). Event-stream `tail -f | grep ERROR` monitors do not — there are no log events to stream when the inner `claude -p` is wedged in init.
  - Both root and sub-project `autonomous_run.sh` forms are functionally equivalent — neither is structurally broken. Sub-project local form (`cd <project> && bash scripts/autonomous_run.sh N`) is preferred for clarity (matching cwd, single arg, less drift surface), not because the workspace-orchestrator form is broken.
- **Related infra** (added 2026-05-02 in source workspace, propagate to forks): `INV-AUTORUN-2` (front-load arg validation, reject non-integer max_sessions), `INV-AUTORUN-3` (cwd-sentinel guard, refuse if caller cwd != project root), `## Autonomous Mode Invocation` section in each sub-project CLAUDE.md.
- **Investigation artifact**: `docs/investigations/autorun_hang_2026-05-02.md` in the source workspace — full 16-probe sequence and conclusions.
- **Tags**: #claude-cli #autonomous-mode #diagnosis-trap #universal #propagated