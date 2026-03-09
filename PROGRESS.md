# Progress Log

> Append-only session log. Each session adds an entry at the bottom.
> Never edit previous entries.

<!-- Entry format:

## YYYY-MM-DD HH:MM -- [T-XX-N] Brief Title
- **What I did**: 1-3 sentences on concrete actions taken
- **Deliverables**: List of files created/modified
- **Sanity check result**: What I verified and the outcome
- **Status**: [DONE] Done / [PARTIAL] Partial (what remains) / [BLOCKED] Blocked (why)
- **Request**: Cross off TASK-XXX / Move TASK-XXX to In Progress / No change

-->

## 2026-03-01 -- Task Deduplication Defense-in-Depth
- **What I did**: Implemented 3-layer dedup defense: clarified docs (CLAUDE.md, exit-protocol.md), added read-time filtering in session_context.py, created task_dedup_check.py stop hook, and registered it in settings.json. Added 10 tests.
- **Deliverables**: Modified CLAUDE.md, docs/workflow/exit-protocol.md, .claude/hooks/session_context.py, .claude/settings.json. New files: .claude/hooks/task_dedup_check.py, tests/test_task_dedup.py.
- **Sanity check result**: ruff clean, 11/11 pytest pass, hook exits 0 on clean TASKS.md, hook exits 2 and prints diagnostic on duplicate task IDs.
- **Status**: [DONE]
- **Request**: No change

## 2026-03-02 -- Git Pre-Commit Hook for Ruff Version Consistency
- **What I did**: Pinned ruff==0.1.14 in requirements.txt, fixed CI lint job to use requirements.txt, created a POSIX pre-commit hook (version guard + ruff lint + emoji scan), created check_emoji_files.py for targeted file scanning, created setup-hooks.sh installer, and updated docs (QUICKSTART, README, CLAUDE.md, LESSONS).
- **Deliverables**: Modified requirements.txt, .github/workflows/ci.yml, scripts/QUICKSTART.md, README.md, CLAUDE.md, LESSONS.md. New files: scripts/check_emoji_files.py, scripts/git-hooks/pre-commit, scripts/setup-hooks.sh.
- **Sanity check result**: ruff clean, emoji scan clean, 11/11 pytest pass, setup-hooks.sh installs successfully, version extraction tested.
- **Status**: [DONE]
- **Request**: No change

## 2026-03-09 -- [T-P0-1] Backup + Baseline Build
- **What I did**: Created blog-refactor branch. Fixed Hexo/scripts conflict by renaming `scripts/` to `tools/` (Hexo loads all files in `scripts/` as Node plugins). Updated all references across 10+ files. Ran `hexo clean && hexo g` -- zero errors, 90 post HTML files generated. Saved baseline post list to `baseline-posts.txt`. Verified branch switching (main and back) works.
- **Deliverables**: New branch `blog-refactor`. Renamed `scripts/` -> `tools/`. Updated references in CLAUDE.md, README.md, TASKS.md, ci.yml, autonomous.md, claude-code-workflow-guide.md, and all files within tools/. Created `baseline-posts.txt`.
- **Sanity check result**: hexo generate zero errors, 11/11 pytest pass, branch rollback verified.
- **Status**: [DONE]
- **Request**: Move T-P0-1 to Completed

## 2026-03-09 -- [T-P0-2] Install NexT Theme
- **What I did**: Installed hexo-theme-next via npm. Created `_config.next.yml` with Gemini scheme, TOC sidebar, reading progress bar, local search (installed hexo-generator-searchdb), mermaid, MathJax, code copy button, social links (GitHub/Facebook), androidstudio highlight theme. Changed `_config.yml` theme to `next` and set `hljs: true` for NexT compatibility. Kept themes/yilia/ as fallback.
- **Deliverables**: `_config.next.yml` (new), modified `_config.yml` (theme: next, hljs: true), modified `package.json` (added hexo-theme-next, hexo-generator-searchdb).
- **Sanity check result**: `hexo clean && hexo g` zero errors, 352 files generated, 90 post HTML files (matches baseline). 11/11 pytest pass.
- **Status**: [DONE]
- **Request**: Move T-P0-2 to Completed

## 2026-03-09 -- [T-P0-3] Rendering Compatibility Audit
- **What I did**: Audited hexo-renderer-marked compatibility with NexT theme. Verified all 5 required posts: images (asset_img renders correctly), TOC (headers generated for client-side TOC), code blocks (highlight sql classes present), mermaid (NexT built-in support working). Found critical bug: MathJax disabled on all pages because `every_page: false` + no posts had `mathjax: true` in front matter. Fixed by setting `every_page: true` in `_config.next.yml` (32/47 posts use math). No renderer switch needed.
- **Deliverables**: Modified `_config.next.yml` (math.every_page: false -> true).
- **Sanity check result**: `hexo clean && hexo g` zero errors, 352 files, 90 post HTML files (matches baseline). `enableMath: true` confirmed in generated HTML. 11/11 pytest pass.
- **Status**: [DONE]
- **Request**: Move T-P0-3 to Completed
