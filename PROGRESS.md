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

## 2026-03-09 -- [T-P0-4] First Deployment -- Theme Only
- **What I did**: Verified build is ready for deployment. `hexo clean && hexo g` produces 352 files, 90 post HTML files, NexT v8.27.0 Gemini scheme confirmed in output, MathJax enabled, zero errors. hexo-deployer-git v3.0.0 installed, deploy config points to umiao.github.io master branch. All 11 tests pass. Cannot execute `hexo d` autonomously -- deploying to a live public site requires user confirmation.
- **Deliverables**: None (build verification only). TASKS.md updated with blocked status.
- **Sanity check result**: Build verified: 352 files, 90 posts, NexT theme confirmed, MathJax enabled. 11/11 pytest pass.
- **Status**: [BLOCKED] Deployment to live public site (umiao.github.io) requires user action. User should run `cd blog_proj && hexo clean && hexo g && hexo d` to deploy, then spot-check the live site.
- **Request**: No change (T-P0-4 remains Active but marked Blocked)

## 2026-03-09 -- [T-P0-5] Move Sensitive Posts to Drafts
- **What I did**: Added fixed `permalink` to front matter of 4 sensitive posts (so URLs stay stable regardless of location). Created `source/_drafts/`. Moved first post (Behavioral-Interview) + asset folder to test -- verified draft renders with images in `--draft` build and is excluded from regular build. Then moved remaining 3 posts + asset folders. Confirmed `Object-Oriented-Design.md` stays in `_posts/`.
- **Deliverables**: `source/_drafts/` (new dir), 4 .md files moved, 4 asset folders moved. Modified front matter of all 4 posts (added permalink field).
- **Sanity check result**: Regular build: 323 files, 4 drafts absent from public/. Draft build: 352 files (matches baseline), all 4 drafts present with images (1+2+3+6=12 images total). 11/11 pytest pass.
- **Status**: [DONE]
- **Request**: Move T-P0-5 to Completed

## 2026-03-09 -- [T-P0-6] Deployment Safety Script + Guide
- **What I did**: Created `tools/safe-deploy.sh` with hexo clean, hexo generate, draft-leakage detection (scans public/ for draft slugs), post/draft listing, interactive confirmation, and hexo deploy steps. Supports `--dry-run` flag. Created `docs/deployment-guide.md` covering local preview (with/without drafts), drafts workflow (create/publish/un-publish), permalink priority, and pre-deployment checklist.
- **Deliverables**: `tools/safe-deploy.sh` (new), `docs/deployment-guide.md` (new)
- **Sanity check result**: Dry-run test: 59 posts listed as deployable, 4 drafts excluded, no leakage detected. 11/11 pytest pass.
- **Status**: [DONE]
- **Request**: Move T-P0-6 to Completed

## 2026-03-09 -- [T-P1-1] Series Master Index Page
- **What I did**: Created `source/series/index.md` with links to DDIA, SQL, and Data Science series pages. Added `series: /series/ || fa fa-book` menu item to `_config.next.yml` nav bar.
- **Deliverables**: `source/series/index.md` (new), `_config.next.yml` (modified)
- **Sanity check result**: `hexo generate` produces 324 files. Series page at `public/series/index.html` with correct links to `/series/ddia/`, `/series/sql/`, `/series/ds/`. Nav bar shows Series link with book icon. 11/11 pytest pass.
- **Status**: [DONE]
- **Request**: Move T-P1-1 to Completed

## 2026-03-09 -- [T-P1-2] DDIA Series Index Page
- **What I did**: Created `source/series/ddia/index.md` with series description (2 paragraphs about DDIA), Mermaid mindmap at topic level (Part I/II/III groupings with chapter topics), and ordered list of all 19 posts using `{% post_link %}` tags grouped by book part.
- **Deliverables**: `source/series/ddia/index.md` (new)
- **Sanity check result**: `hexo generate` succeeds. All 19 post links resolve to existing HTML files in `public/`. Mermaid block present in generated HTML. 11/11 pytest pass.
- **Status**: [DONE]
- **Request**: Move T-P1-2 to Completed

## 2026-03-09 -- [T-P1-3] SQL Series Index Page
- **What I did**: Created `source/series/sql/index.md` with 2-paragraph series description, Mermaid mindmap (5 topic groups: Fundamentals, Database Objects, Data Management, Advanced Querying, Optimization), and ordered list of all 16 SQL posts using `{% post_link %}` tags.
- **Deliverables**: `source/series/sql/index.md` (new)
- **Sanity check result**: `hexo generate` succeeds. All 16 post links resolve to existing HTML files in `public/`. Mermaid block present in generated HTML. 11/11 pytest pass.
- **Status**: [DONE]
- **Request**: Move T-P1-3 to Completed

## 2026-03-09 -- [T-P1-4] Data Science Series Index Page
- **What I did**: Created `source/series/ds/index.md` with 2-paragraph series description, Mermaid mindmap (5 topic groups: Foundations, Evaluation, Classical Algorithms, Regularization, Ensemble Methods), and ordered list of all 9 DS posts using `{% post_link %}` tags.
- **Deliverables**: `source/series/ds/index.md` (new)
- **Sanity check result**: `hexo generate` succeeds (327 files). All 9 post links resolve to existing HTML files in `public/`. Mermaid block present in generated HTML. 11/11 pytest pass.
- **Status**: [DONE]
- **Request**: Move T-P1-4 to Completed

## 2026-03-09 -- [T-P1-5] Deploy Series Pages
- **What I did**: Ran `tools/safe-deploy.sh` to deploy all series pages (master index, DDIA, SQL, DS) to production. Dry-run passed first, then full deploy pushed 327 files to umiao.github.io. No draft leakage detected. 59 posts deployed, 4 drafts excluded.
- **Deliverables**: None (deploy only). Series pages live at `/series/`, `/series/ddia/`, `/series/sql/`, `/series/ds/`.
- **Sanity check result**: Dry-run clean. Deploy succeeded (`HEAD -> master` push confirmed). All 4 series HTML files present in `public/`. 11/11 pytest pass.
- **Status**: [DONE]
- **Request**: Move T-P1-5 to Completed

## 2026-03-09 -- [T-P2-1] Post Front Matter Cleanup
- **What I did**: Added `description:` field to all 59 posts for SEO (auto-extracted from first paragraph, with manual overrides for 12 posts). Normalized 5 inconsistent tags: `DataScience` -> `Data Science` (47 posts), lowercase `investment/options/futures/trading` -> capitalized (2 posts each). Verified all posts already had `<!-- more -->` breaks.
- **Deliverables**: All 59 `source/_posts/*.md` files updated, `tools/add_descriptions.py` (utility script)
- **Sanity check result**: `hexo generate` produces 327 files (matches baseline). 11/11 pytest pass. Ruff clean. Tag audit shows all tags consistently capitalized.
- **Status**: [DONE]
- **Request**: Move T-P2-1 to Completed

## 2026-03-09 -- [T-P2-2] SEO Basics (Sitemap + RSS)
- **What I did**: Installed `hexo-generator-sitemap` and `hexo-generator-feed` npm packages. Added sitemap and RSS feed configuration to `_config.yml`. Verified `hexo generate` produces both `public/sitemap.xml` (23KB) and `public/atom.xml` (328KB) with correct `https://umiao.github.io/` URLs.
- **Deliverables**: `_config.yml` (sitemap + feed config), `package.json` (2 new dependencies)
- **Sanity check result**: `hexo generate` produces 329 files. Both sitemap.xml and atom.xml present with correct URLs. 11/11 pytest pass.
- **Status**: [DONE]
- **Request**: Move T-P2-2 to Completed

## 2026-03-09 -- [T-P2-3] About Page Restructure
- **What I did**: Rewrote `source/about/index.md` using info from user's resume. Structured into sections: Bio, Work Experience (eBay MLE, eBay intern, NuNova, UCLA research), Skills, Publications, Contact. Removed outdated content ("year-one MS student", "incoming intern at ebay"). Preserved existing images (selfie.jpg, ucla.jpg, ece.jpg).
- **Deliverables**: `source/about/index.md`
- **Sanity check result**: `hexo generate` produces 329 files, about page renders at `public/about/index.html`.
- **Status**: [DONE]
- **Request**: Move T-P2-3 to Completed

## 2026-03-10 -- [T-P0-8] Separate Life Category Posts to Sidebar Widget
- **What I did**: Implemented Life category filtering for yilia theme. Modified `themes/yilia/layout/common/archive.ejs` to filter out Life-category posts from main timeline on homepage only (using `is_home()` guard). Created `themes/yilia/layout/widget/life.ejs` widget to display Life posts in sidebar with thumbnails, titles, and dates. Added 'life' to widgets list in `themes/yilia/_config.yml`.
- **Deliverables**: `themes/yilia/layout/common/archive.ejs` (modified), `themes/yilia/layout/widget/life.ejs` (new), `themes/yilia/_config.yml` (modified)
- **Sanity check result**: Switched theme to yilia temporarily for testing. `hexo generate` produces valid HTML. Homepage main timeline excludes Cake Inspiration Gallery post (Life category). Sidebar displays "Life & Hobbies" widget with Cake post. /archives/ page and /categories/Life/ page both still show Life posts. All acceptance criteria verified via curl tests.
- **Status**: [DONE] Feature implemented for yilia theme. Note: Site currently uses NexT theme (as of task start), so feature is not active until theme is switched to yilia. Theme was reverted to next after testing.
- **Request**: Move T-P0-8 to Completed

## 2026-03-11 -- [T-P0-9] Activate Life Sidebar Widget + Add Excerpt Break to Cake Post
- **What I did**: Changed theme from `next` to `yilia` in `_config.yml` line 100 (activating the Life sidebar widget infrastructure from T-P0-8). Added `<!-- more -->` tag to `source/_posts/Cake-Inspiration-Gallery.md` after line 100 (after intro paragraph, Quick Nav, and separator, before first cake section) to collapse the 387-line, 57-image post on homepage.
- **Deliverables**: `_config.yml` (theme: next -> yilia), `source/_posts/Cake-Inspiration-Gallery.md` (added <!-- more --> tag)
- **Sanity check result**: `hexo clean && hexo generate` succeeds with 413 files, zero errors. Verified in generated `public/index.html`: (1) Cake post NOT in main article feed (grep for article titles shows no Cake post), (2) "cake-gallery" class absent from homepage (full content hidden), (3) "Life & Hobbies" sidebar widget present with Cake post listed. Verified `public/2026/03/09/Cake-Inspiration-Gallery/index.html` full post page renders correctly with all 57 images.
- **Status**: [DONE]
- **Request**: Move T-P0-9 to Completed

## 2026-03-11 -- [T-P0-11] Review Last 3 Commits + Apply Fixes
- **What I did**: Reviewed commits 6cf2692, 8626df9, d73cf5d. Fixed 4 discovered issues: (1) Created `source/tags/index.md` and `source/categories/index.md` with proper Hexo front matter (type: tags/categories, layout: tags/categories) to resolve 404s. (2) Updated `themes/yilia/_config.yml` menu to add `Tags: /tags/` and fix `Categories: /categories/` (was empty). (3) Fixed About page image sizing by removing hard-coded width/height attributes from all 3 images (selfie.jpg, ucla.jpg, ece.jpg) and replacing with CSS `style="max-width: 300px/400px; height: auto;"` to preserve aspect ratios. (4) Created Python-based `tools/commit-msg-hook` to enforce English-only commit messages (rejects CJK characters), stored in tools/ for version control and installed to `.git/hooks/commit-msg`.
- **Deliverables**: `source/tags/index.md` (new), `source/categories/index.md` (new), `source/about/index.md` (modified), `themes/yilia/_config.yml` (modified), `tools/commit-msg-hook` (new), `.git/hooks/commit-msg` (installed)
- **Sanity check result**: `hexo clean && hexo generate` produces 413 files, zero errors. Verified: `public/tags/index.html` and `public/categories/index.html` exist with correct titles. `public/about/index.html` has images with `style="max-width: ...; height: auto;"` (no width/height attributes). commit-msg hook tested with 4 test cases: [PASS] English, [REJECT] Chinese, [REJECT] Japanese, [REJECT] Korean. Hook script uses Python (not bash) for Windows compatibility and proper Unicode handling.
- **Status**: [DONE] Note: Theme switch question (yilia -> NexT) deferred to separate task per Major Change Approval Protocol.
- **Request**: Move T-P0-11 to Completed

## 2026-03-11 -- [T-P0-7, T-P0-9] Restore NexT Theme with Life Category Support
- **What I did**: Switched theme from yilia back to NexT in `_config.yml` (completing the user-approved migration). Created `scripts/filter-life-homepage.js` Hexo generator plugin that overrides the default index generator to exclude Life-category posts from the homepage. Created `source/_data/sidebar.njk` Life sidebar widget for NexT showing Life posts with titles and dates. Added `custom_file_path.sidebar` to `_config.next.yml`. Also included T-P0-11 fixes (tags/categories index pages, about page image sizing, commit-msg hook).
- **Deliverables**: `_config.yml` (theme: yilia -> next), `scripts/filter-life-homepage.js` (new), `source/_data/sidebar.njk` (new), `_config.next.yml` (modified), `source/tags/index.md` (new), `source/categories/index.md` (new), `source/about/index.md` (modified), `tools/commit-msg-hook` (new)
- **Sanity check result**: `hexo clean && hexo generate` produces 394 files, zero errors. Tags/categories/about pages exist. Cake Inspiration Gallery post NOT in homepage post titles (0 matches). Cake post IS in Life sidebar widget (1 match). Cake post page exists at direct URL. NexT v8.27.0 confirmed.
- **Status**: [DONE]
- **Request**: Move T-P0-7 to Completed

## 2026-03-11 -- Knowledge System Task Planning
- **What I did**: Wrote 18 new tasks to TASKS.md across 3 phases: Phase 1 Core Infrastructure (T-P3-1 to T-P3-5: scaffold schema, concept registry, /blog-from-notes skill, review queue tool, /study-review skill), Phase 2 Knowledge Graph & Content (T-P4-1 to T-P4-9: /refine-post skill, DDIA pilot enrichment, batch enrichment, concept index, series nav, related posts, interview hub, cheat sheets, publish drafts), Phase 3 Polish (T-P5-1 to T-P5-4: knowledge map, Anki export, /plan-series skill, quality fixes). Updated dependency graph. Preserved all 15 completed tasks.
- **Deliverables**: `TASKS.md` (replaced Active Tasks section and dependency graph)
- **Sanity check result**: Read back TASKS.md -- all 18 tasks present with acceptance criteria, complexity, depends-on fields. Dependency graph consistent with task specs. Completed section intact (15 entries).
- **Status**: [DONE]
- **Request**: No change (task planning only, no task IDs to move)

## 2026-03-11 -- Fix TASKS.md Naming Convention (P = Priority, not Phase)
- **What I did**: Reassigned all 18 active task IDs from phase-based (T-P3/P4/P5-*) to priority-based (T-P0/P1/P2/P3-*) per canonical convention. Updated CLAUDE.md with explicit P0-P3 priority definitions and prohibition against using P as phase counter. Rewrote TASKS.md section headers from "Phase N" to priority tiers ("Must Have (P0)", etc.). Updated all Depends-on references and dependency graph. Added historical note to Completed section. Logged lesson to LESSONS.md.
- **Deliverables**: `CLAUDE.md` (priority definitions + prohibition), `TASKS.md` (18 IDs reassigned, section headers, dependency graph), `LESSONS.md` (convention drift lesson)
- **Sanity check result**: No ID collisions between active (T-P0-12..T-P3-8) and completed (T-P0-1..T-P2-3) sections. All Depends-on references point to valid IDs. No old T-P4-*/T-P5-* IDs remain in TASKS.md. Hooks exit cleanly.
- **Status**: [DONE]
- **Request**: No change

## 2026-03-12 -- [T-P0-12] Scaffold + Front Matter Schema
- **What I did**: Updated `scaffolds/post.md` to include all knowledge-system front matter fields: categories, tags (preserved), description, key_concepts, takeaways, series, series_index. All new fields default to empty values. Tested with `hexo new "Test Post"` to verify scaffold generates correctly, then ran `hexo clean && hexo generate` to confirm existing posts unaffected.
- **Deliverables**: `scaffolds/post.md` (modified)
- **Sanity check result**: Test post created with all 9 front matter fields (title, date, categories, tags, description, key_concepts, takeaways, series, series_index). `hexo generate` succeeded with 396 files, zero errors. Removed test post after verification.
- **Status**: [DONE]
- **Request**: Move T-P0-12 to Completed

## 2026-03-12 -- [T-P0-13] Concept Registry
- **What I did**: Created `data/concepts.yml` with 59 concepts covering all 4 required domains (DDIA: 18, SQL: 14, DS: 15, Interview: 12). Each concept has `name`, `aliases` (list, may be empty), and `domain` fields. Created comprehensive test suite `tests/test_concepts.py` with 6 tests validating file existence, YAML validity, count >= 40, domain coverage, required fields, and distribution.
- **Deliverables**: `data/concepts.yml` (new), `tests/test_concepts.py` (new)
- **Sanity check result**: All 6 tests pass. YAML parseable by `yaml.safe_load`. Total 59 concepts across 4 domains (DDIA, SQL, DS, Interview). Domain distribution verified. All concepts have required fields (name, aliases as list, domain).
- **Status**: [DONE]
- **Request**: Move T-P0-13 to Completed

## 2026-03-12 -- [T-P0-14] Review Queue Tool
- **What I did**: Created `tools/review_queue.py` implementing SM-2 spaced repetition algorithm for blog post reviews. Implemented 4 commands: `init` (scans posts, builds queue), `show` (lists due posts), `mark <slug> <quality>` (records review with 0-5 rating, updates interval), `stats` (summary statistics). Stores review state in `data/review_state.json` with fields: last_reviewed, interval, easiness, repetitions, next_due, content_hash. Content hash (MD5 of post body) tracks changes and resets review schedules when content modified. All file I/O uses `encoding="utf-8"`.
- **Deliverables**: `tools/review_queue.py` (new), `data/review_state.json` (generated by init), `tests/test_review_queue.py` (new, 7 tests)
- **Sanity check result**: All acceptance criteria verified: (1) --help works, (2) init scanned 60 posts and populated state file, (3) show lists all posts due initially, (4) mark command correctly updates intervals using SM-2 formula (tested progression: 1d → 6d → 13d), (5) stats shows summary (60 total, intervals, distribution), (6) content hash detection verified (modified post flagged and reset). All 7 new tests pass. All 13 project tests (concepts + review_queue) pass.
- **Status**: [DONE]
- **Request**: Move T-P0-14 to Completed

## 2026-03-12 -- [T-P0-15] Publish Draft Posts
- **What I did**: Moved 4 posts from `source/_drafts/` to `source/_posts/` with complete front matter updates. Added `key_concepts`, `takeaways`, and `description` fields to all 4 posts. Added `series: System Design Interview - Alex Xu` and `series_index: 1/2` to the two System Design posts. Used `git mv` for .md files and `mv` for asset directories. Removed leftover draft directories after successful move.
- **Deliverables**: 4 posts moved: Behavioral-Interview-Questions-Crack.md, Need-To-Knows-For-Software-Security-Engineer.md, System-Design-Interview-Alex-Xu-Notes-1.md, System-Design-Interview-Alex-Xu-Notes-2.md. All associated asset folders moved (7 images + 1 Python file total). `source/_drafts/` is now empty.
- **Sanity check result**: All 4 acceptance criteria met: (1) `source/_drafts/` is empty (only . and .. remain), (2) All 4 posts have complete front matter (key_concepts lists, takeaways lists, categories, tags, description, series info where applicable), (3) `hexo generate` succeeded with 214 files generated in 1.52s, post count increased from 60 to 64 .md files, all 4 new posts have index.html files in public/, (4) No draft leakage (all posts intentionally public in _posts/).
- **Status**: [DONE]
- **Request**: Move T-P0-15 to Completed

## 2026-03-12 -- [T-P1-6] /blog-from-notes Skill
- **What I did**: Created `.claude/skills/blog-from-notes/SKILL.md` with complete 7-step workflow: (1) Locate input from `docs/raw-input/` or arbitrary path, (2) Analyze content for topic/domain/series, (3) Generate front matter using `scaffolds/post.md` template with `data/concepts.yml` concept lookup, (4) Format post body with excerpt break, (5) Show draft preview with confirmation prompt (yes/no/edit), (6) Write post file, (7) Flag new concepts not in registry. Created `docs/raw-input/` directory with README and sample input file.
- **Deliverables**: `.claude/skills/blog-from-notes/SKILL.md` (new), `docs/raw-input/README.md` (new), `docs/raw-input/sample-docker-basics.md` (new, sample input for testing)
- **Sanity check result**: All 4 ACs met: (1) SKILL.md exists with complete instructions (161 lines), (2) References scaffold template (`scaffolds/post.md`) and concepts.yml lookup with canonical name matching, (3) Step 5 includes confirmation with yes/no/edit options, (4) Sample input file placed in `docs/raw-input/` for manual testing. Skill auto-detected by Claude Code (appears in skills list).
- **Status**: [DONE]
- **Request**: Move T-P1-6 to Completed

## 2026-03-12 -- [T-P1-7] /refine-post Skill
- **What I did**: Created `.claude/skills/refine-post/SKILL.md` with complete 8-step workflow: (1) Locate post by filename/path or interactive selection of posts missing key_concepts, (2) Read and analyze post content/front matter, (3) Look up concepts against `data/concepts.yml` with canonical name matching and `[NEW:]` flagging, (4) Build updated front matter with merge-not-overwrite strategy, (5) Fix generic image alt text, (6) Show structured diff for user confirmation (yes/no/edit), (7) Write updated post, (8) Flag and optionally add new concepts to registry.
- **Deliverables**: `.claude/skills/refine-post/SKILL.md` (new, 158 lines)
- **Sanity check result**: All 4 ACs met: (1) SKILL.md exists with complete instructions (158 lines), (2) Step 3 validates concepts against concepts.yml with canonical name matching and [NEW:] warnings for unrecognized concepts, (3) Step 6 shows structured diff with yes/no/edit confirmation before writing, (4) Verified skill would correctly handle DDIA post: detects series from title pattern, extracts series_index from "Note-N", identifies relevant concepts, flags generic "ML_note" alt text. Skill auto-detected by Claude Code (appears in skills list as "refine-post").
- **Status**: [DONE]
- **Request**: Move T-P1-7 to Completed

## 2026-03-12 -- [T-P1-8] /study-review Skill (Basic)
- **What I did**: Created `.claude/skills/study-review/SKILL.md` with complete 7-step workflow: (1) Check review queue status via `tools/review_queue.py show`, (2) Select post for review (single or sequential "all" mode), (3) Read and analyze post content/front matter, (4) Generate 5-7 quiz questions across 5 types (Definition Recall, Application/Scenario, Comparison/Trade-off, Connection/Synthesis, Recall Detail), (5) Present questions one-at-a-time with self-rating (0-5), (6) Record results via `tools/review_queue.py mark`, (7) Continue or finish with session summary. Includes special commands (skip, show, stop, stats).
- **Deliverables**: `.claude/skills/study-review/SKILL.md` (new, 156 lines)
- **Sanity check result**: All 4 ACs met: (1) SKILL.md exists with complete instructions, (2) Integrates with review_queue.py show+mark commands, (3) Generates 5 question types (exceeds minimum of 3), (4) Verified review_queue.py init/show work -- 64 posts tracked, 60 due for review. Skill auto-detected by Claude Code (appears in skills list as "study-review").
- **Status**: [DONE]
- **Request**: Move T-P1-8 to Completed

## 2026-03-12 -- [T-P1-11] Blog Quality Fixes
- **What I did**: Enabled Open Graph and Twitter Cards (`summary_large_image`) in `_config.next.yml` with proper NexT theme config structure. Set local search `preload: true`. Created `source/404.md` with navigation links. Fixed wrong/placeholder `asset_img` alt text across ~45 posts: replaced generic strings ("ML_note", "SQL Note of blur!", "apple", "Note", "vocab") with descriptive alt text based on post content and surrounding context. Cover images got topic-appropriate descriptions; inline diagrams got context-aware descriptions.
- **Deliverables**: `_config.next.yml` (modified), `source/404.md` (new), 45 post .md files (alt text fixes)
- **Sanity check result**: All 4 ACs met: (1) OG meta tags (og:type, og:title, og:url, og:site_name, og:description, og:locale, og:image) and Twitter Card tags (twitter:card=summary_large_image, twitter:image) present in generated HTML, (2) search preload set to true with search.json generated, (3) public/404.html exists after hexo generate, (4) No generic placeholder alt text remaining (grep confirms zero matches for old patterns).
- **Status**: [DONE]
- **Request**: Move T-P1-11 to Completed

## 2026-03-12 -- [T-P1-9] Enrich DDIA Series (Pilot)
- **What I did**: Added `key_concepts`, `takeaways`, `series: DDIA`, and `series_index` (1-19) to all 19 DDIA posts. Each post got 3-5 canonical concepts from `data/concepts.yml` and 4 actionable takeaways derived from actual content. Added 10 new DDIA-domain concepts to `concepts.yml`: Scalability, Fault Tolerance, Data Models, LSM-Tree, B-Tree, Data Warehousing, Encoding and Schema Evolution, Transaction Isolation, Serializability, Change Data Capture.
- **Deliverables**: 19 DDIA post .md files (front matter enriched), `data/concepts.yml` (10 new concepts added)
- **Sanity check result**: All 4 ACs met: (1) All 19 posts have key_concepts (non-empty), takeaways, series: DDIA, series_index 1-19. (2) All key_concepts values exist in concepts.yml. (3) `hexo generate` succeeds with no errors (25 files generated). (4) Spot-checked Note-5 (LSM-Tree/B-Tree), Note-13 (Leaderless Replication), Note-17 (Consensus/Linearizability) -- concepts and takeaways are accurate and meaningful.
- **Status**: [DONE]
- **Request**: Move T-P1-9 to Completed

## 2026-03-12 -- [T-P1-10] Enrich SQL + DS + Remaining Posts
- **What I did**: Added `key_concepts`, `takeaways`, and series metadata to all 41 remaining posts (16 SQL, 9 DS, 16 miscellaneous). SQL posts got `series: SQL` with `series_index` 1-16; DS posts got `series: Data Science` with `series_index` 1-9. Fixed 4 previously-enriched posts (Behavioral, Security, System Design x2) whose key_concepts used descriptive strings instead of canonical concept names. Added 29 new concepts to `concepts.yml` across 5 domains: SQL (5), DS (10), Interview (3), General (11).
- **Deliverables**: 45 post .md files (front matter enriched), `data/concepts.yml` (29 new concepts), 4 previously-enriched posts fixed
- **Sanity check result**: All 4 ACs met: (1) All 64 posts have non-empty key_concepts and takeaways. (2) SQL posts have series: SQL with series_index 1-16; DS posts have series: Data Science with series_index 1-9. (3) Python validation confirms all key_concepts values exist in concepts.yml (0 errors across 64 posts). (4) `hexo generate` succeeds with 54 files, no errors or warnings.
- **Status**: [DONE]
- **Request**: Move T-P1-10 to Completed

## 2026-03-12 -- [T-P2-4] Concept Index Generator Plugin
- **What I did**: Created `scripts/generate-concept-index.js` Hexo generator plugin that reads `key_concepts` from all post front matter, builds an alphabetical concept-to-posts index, and outputs `/concepts/index.html`. Page includes letter navigation (A-Z), definition list of concepts with linked posts, and inline styling.
- **Deliverables**: `scripts/generate-concept-index.js`
- **Sanity check result**: All 4 ACs met: (1) Plugin file exists and is loaded by Hexo. (2) `hexo generate` produces `public/concepts/index.html`. (3) 87 concepts listed alphabetically with letter nav and post links. (4) DDIA concepts (ACID, Replication, MapReduce, LSM-Tree, etc.) appear correctly with proper post links.
- **Status**: [DONE]
- **Request**: Move T-P2-4 to Completed

## 2026-03-12 -- [T-P2-5] Series Navigation Plugin
- **What I did**: Created `scripts/series-nav.js` Hexo filter plugin that uses `series` and `series_index` front matter to inject prev/next navigation links at the bottom of series posts. Uses `hexo.model('Post')` to build complete series index before rendering. Includes inline styling with flexbox layout.
- **Deliverables**: `scripts/series-nav.js`
- **Sanity check result**: All 4 ACs met: (1) Plugin file exists and is loaded by Hexo. (2) DDIA post 5 shows prev (Part 4) and next (Part 6) links. (3) First post has empty prev, last post has empty next. (4) `hexo generate` succeeds with 425 files, no errors.
- **Status**: [DONE]
- **Request**: Move T-P2-5 to Completed

## 2026-03-12 -- [T-P2-6] Related Posts Plugin
- **What I did**: Created `scripts/related-posts.js` Hexo filter plugin that injects a "Related Reading" section at the bottom of each post. Scores candidate posts by tag overlap + key_concepts overlap (weighted 2x). Shows top 5 related posts with titles and links. Uses pre-built post index for performance with cache reset on before_generate.
- **Deliverables**: `scripts/related-posts.js`
- **Sanity check result**: All 4 ACs met: (1) Plugin file exists and is loaded by Hexo. (2) 57 of 64 posts show "Related Reading" section with linked posts. (3) Related posts are relevant (DS-Study-Note-1 about Overfitting shows L1/L2 Regularization note first). (4) `hexo generate` succeeds with 425 files, no errors.
- **Status**: [DONE]
- **Request**: Move T-P2-6 to Completed

## 2026-03-12 -- [T-P2-7] Interview Prep Hub
- **What I did**: Created `source/interview/index.md` with structured interview prep content across 7 sections: System Design (DDIA concepts in tables), System Design (Alex Xu patterns), SQL quick reference and common patterns, Data Science/ML algorithms and concepts, Behavioral (STAR method), OOD (SOLID principles), and Brainteasers. Added "Interview" nav entry to `_config.next.yml`. Included a 1-week study plan with daily focus areas.
- **Deliverables**: `source/interview/index.md`, `_config.next.yml` (nav menu update)
- **Sanity check result**: All 4 ACs met: (1) `source/interview/index.md` exists with all listed sections. (2) Nav menu updated in `_config.next.yml`. (3) `hexo generate` produces `public/interview/index.html` (202 files, no errors). (4) Page contains actionable content: 13 tables, 87 links, study tips and common questions.
- **Status**: [DONE]
- **Request**: Move T-P2-7 to Completed

## 2026-03-12 -- [T-P2-8] Cheat Sheets
- **What I did**: Created 3 cheat sheet pages under `source/cheatsheet/`: `ddia.md` (19 DDIA notes condensed into comparison tables covering storage engines, replication, partitioning, transactions, consensus, batch/stream processing), `sql.md` (16 SQL notes condensed with syntax examples, function references, optimization patterns, window functions), `ds.md` (9 DS notes condensed covering overfitting, bias-variance, SVM, Naive Bayes, regularization, ensemble methods, XGBoost/LightGBM). Created `index.md` hub page linking all three. Added "Cheatsheets" nav entry to `_config.next.yml`.
- **Deliverables**: `source/cheatsheet/ddia.md`, `source/cheatsheet/sql.md`, `source/cheatsheet/ds.md`, `source/cheatsheet/index.md`, `_config.next.yml` (nav update)
- **Sanity check result**: All 4 ACs met: (1) All 3 cheat sheet files exist under `source/cheatsheet/`. (2) Each covers all posts in its series (19 DDIA, 16 SQL, 9 DS). (3) Contains comparison tables and quick-reference content (136+116+150 table rows). (4) `hexo generate` produces all HTML pages (206 files, 0 errors).
- **Status**: [DONE]
- **Request**: Move T-P2-8 to Completed

## 2026-03-12 -- [T-P3-6] Visual Knowledge Map
- **What I did**: Created `source/knowledge-map/index.md` with a Mermaid graph showing 4 domain clusters (DDIA with 20 nodes covering storage/replication/transactions/consensus/processing, SQL with 18 nodes covering queries/schema/performance, DS with 25 nodes covering supervised/unsupervised/NLP/fundamentals, Interview with 13 nodes covering system design/OOD/behavioral). Added cross-domain dashed edges connecting related concepts (partitioning-sharding, CAP theorem, indexes-storage engines, etc.). Added "knowledge-map" nav entry to `_config.next.yml`.
- **Deliverables**: `source/knowledge-map/index.md`, `_config.next.yml` (nav update)
- **Sanity check result**: All 4 ACs met: (1) `source/knowledge-map/index.md` exists with Mermaid diagram. (2) Mermaid renders in Hexo (script tags and `<pre class="mermaid">` in HTML). (3) All 4 domain clusters represented with key concept nodes. (4) `hexo generate` produces `public/knowledge-map/index.html` (207 files, 0 errors).
- **Status**: [DONE]
- **Request**: Move T-P3-6 to Completed
