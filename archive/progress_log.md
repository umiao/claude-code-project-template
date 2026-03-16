# Progress Log Archive

> Older session entries moved from PROGRESS.md. Chronological order (oldest first).

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

## 2026-03-09 -- [T-P0-4] First Deployment -- Theme Only
- **What I did**: Verified build is ready for deployment. `hexo clean && hexo g` produces 352 files, 90 post HTML files, NexT v8.27.0 Gemini scheme confirmed in output, MathJax enabled, zero errors. hexo-deployer-git v3.0.0 installed, deploy config points to umiao.github.io master branch. All 11 tests pass. Cannot execute `hexo d` autonomously -- deploying to a live public site requires user confirmation.
- **Deliverables**: None (build verification only). TASKS.md updated with blocked status.
- **Sanity check result**: Build verified: 352 files, 90 posts, NexT theme confirmed, MathJax enabled. 11/11 pytest pass.
- **Status**: [BLOCKED] Deployment to live public site (umiao.github.io) requires user action.
- **Request**: No change

## 2026-03-09 -- [T-P0-5] Move Sensitive Posts to Drafts
- **What I did**: Added fixed `permalink` to front matter of 4 sensitive posts. Created `source/_drafts/`. Moved first post + asset folder to test -- verified draft renders with images in `--draft` build and is excluded from regular build. Then moved remaining 3 posts + asset folders.
- **Deliverables**: `source/_drafts/` (new dir), 4 .md files moved, 4 asset folders moved.
- **Sanity check result**: Regular build: 323 files, 4 drafts absent from public/. Draft build: 352 files, all 4 drafts present with images. 11/11 pytest pass.
- **Status**: [DONE]
- **Request**: Move T-P0-5 to Completed

## 2026-03-09 -- [T-P0-6] Deployment Safety Script + Guide
- **What I did**: Created `tools/safe-deploy.sh` with hexo clean, hexo generate, draft-leakage detection, post/draft listing, interactive confirmation, and hexo deploy steps. Created `docs/deployment-guide.md`.
- **Deliverables**: `tools/safe-deploy.sh` (new), `docs/deployment-guide.md` (new)
- **Sanity check result**: Dry-run test: 59 posts listed as deployable, 4 drafts excluded, no leakage detected. 11/11 pytest pass.
- **Status**: [DONE]
- **Request**: Move T-P0-6 to Completed

## 2026-03-09 -- [T-P1-1] Series Master Index Page
- **What I did**: Created `source/series/index.md` with links to DDIA, SQL, and Data Science series pages. Added `series: /series/ || fa fa-book` menu item to `_config.next.yml` nav bar.
- **Deliverables**: `source/series/index.md` (new), `_config.next.yml` (modified)
- **Sanity check result**: `hexo generate` produces 324 files. Series page at `public/series/index.html` with correct links.
- **Status**: [DONE]
- **Request**: Move T-P1-1 to Completed

## 2026-03-09 -- [T-P1-2] DDIA Series Index Page
- **What I did**: Created `source/series/ddia/index.md` with series description, Mermaid mindmap, and ordered list of all 19 posts using `{% post_link %}` tags grouped by book part.
- **Deliverables**: `source/series/ddia/index.md` (new)
- **Sanity check result**: `hexo generate` succeeds. All 19 post links resolve. Mermaid block present in HTML.
- **Status**: [DONE]
- **Request**: Move T-P1-2 to Completed

## 2026-03-09 -- [T-P1-3] SQL Series Index Page
- **What I did**: Created `source/series/sql/index.md` with description, Mermaid mindmap, and ordered list of all 16 SQL posts.
- **Deliverables**: `source/series/sql/index.md` (new)
- **Sanity check result**: `hexo generate` succeeds. All 16 post links resolve.
- **Status**: [DONE]
- **Request**: Move T-P1-3 to Completed

## 2026-03-09 -- [T-P1-4] Data Science Series Index Page
- **What I did**: Created `source/series/ds/index.md` with description, Mermaid mindmap, and ordered list of all 9 DS posts.
- **Deliverables**: `source/series/ds/index.md` (new)
- **Sanity check result**: `hexo generate` succeeds (327 files). All 9 post links resolve.
- **Status**: [DONE]
- **Request**: Move T-P1-4 to Completed

## 2026-03-09 -- [T-P1-5] Deploy Series Pages
- **What I did**: Ran `tools/safe-deploy.sh` to deploy all series pages to production. 327 files pushed to umiao.github.io.
- **Deliverables**: None (deploy only).
- **Sanity check result**: Dry-run clean. Deploy succeeded. All 4 series HTML files present.
- **Status**: [DONE]
- **Request**: Move T-P1-5 to Completed

## 2026-03-09 -- [T-P2-1] Post Front Matter Cleanup
- **What I did**: Added `description:` field to all 59 posts for SEO. Normalized 5 inconsistent tags.
- **Deliverables**: All 59 `source/_posts/*.md` files updated, `tools/add_descriptions.py`
- **Sanity check result**: `hexo generate` produces 327 files. Tag audit shows all tags consistently capitalized.
- **Status**: [DONE]
- **Request**: Move T-P2-1 to Completed

## 2026-03-09 -- [T-P2-2] SEO Basics (Sitemap + RSS)
- **What I did**: Installed `hexo-generator-sitemap` and `hexo-generator-feed`. Added sitemap and RSS feed configuration to `_config.yml`.
- **Deliverables**: `_config.yml` (sitemap + feed config), `package.json` (2 new dependencies)
- **Sanity check result**: `hexo generate` produces 329 files. Both sitemap.xml and atom.xml present with correct URLs.
- **Status**: [DONE]
- **Request**: Move T-P2-2 to Completed

## 2026-03-09 -- [T-P2-3] About Page Restructure
- **What I did**: Rewrote `source/about/index.md` with current bio, work experience, skills, publications, contact.
- **Deliverables**: `source/about/index.md`
- **Sanity check result**: `hexo generate` produces 329 files, about page renders correctly.
- **Status**: [DONE]
- **Request**: Move T-P2-3 to Completed

## 2026-03-10 -- [T-P0-8] Separate Life Category Posts to Sidebar Widget
- **What I did**: Implemented Life category filtering for yilia theme. Modified archive.ejs to filter out Life posts from homepage. Created life.ejs sidebar widget.
- **Deliverables**: `themes/yilia/layout/common/archive.ejs`, `themes/yilia/layout/widget/life.ejs`, `themes/yilia/_config.yml`
- **Sanity check result**: Homepage excludes Cake post. Sidebar shows Life widget. Archives/categories still show Life posts.
- **Status**: [DONE]
- **Request**: Move T-P0-8 to Completed

## 2026-03-11 -- [T-P0-9] Activate Life Sidebar Widget + Add Excerpt Break to Cake Post
- **What I did**: Changed theme from next to yilia (activating Life sidebar widget from T-P0-8). Added `<!-- more -->` tag to Cake-Inspiration-Gallery.md.
- **Deliverables**: `_config.yml`, `source/_posts/Cake-Inspiration-Gallery.md`
- **Sanity check result**: `hexo generate` succeeds with 413 files. Cake post filtered from homepage, Life sidebar widget present.
- **Status**: [DONE]
- **Request**: Move T-P0-9 to Completed

## 2026-03-11 -- [T-P0-11] Review Last 3 Commits + Apply Fixes
- **What I did**: Created tags/categories index pages, fixed about page image sizing, created commit-msg hook for English-only messages.
- **Deliverables**: `source/tags/index.md`, `source/categories/index.md`, `source/about/index.md`, `themes/yilia/_config.yml`, `tools/commit-msg-hook`
- **Sanity check result**: `hexo generate` produces 413 files. Tags/categories pages render. commit-msg hook rejects CJK.
- **Status**: [DONE]
- **Request**: Move T-P0-11 to Completed

## 2026-03-11 -- [T-P0-7, T-P0-9] Restore NexT Theme with Life Category Support
- **What I did**: Switched theme from yilia back to NexT. Created filter-life-homepage.js and sidebar.njk Life widget for NexT.
- **Deliverables**: `_config.yml`, `scripts/filter-life-homepage.js`, `source/_data/sidebar.njk`, `_config.next.yml`
- **Sanity check result**: `hexo generate` produces 394 files. Cake post filtered from homepage, visible in sidebar.
- **Status**: [DONE]
- **Request**: Move T-P0-7 to Completed

## 2026-03-11 -- Knowledge System Task Planning
- **What I did**: Wrote 18 new tasks to TASKS.md across knowledge system phases.
- **Deliverables**: `TASKS.md`
- **Sanity check result**: All 18 tasks present with acceptance criteria, complexity, depends-on fields.
- **Status**: [DONE]
- **Request**: No change

## 2026-03-11 -- Fix TASKS.md Naming Convention (P = Priority, not Phase)
- **What I did**: Reassigned all 18 active task IDs from phase-based to priority-based. Updated CLAUDE.md with explicit P0-P3 definitions.
- **Deliverables**: `CLAUDE.md`, `TASKS.md`, `LESSONS.md`
- **Sanity check result**: No ID collisions. All Depends-on references valid. Hooks exit cleanly.
- **Status**: [DONE]
- **Request**: No change
