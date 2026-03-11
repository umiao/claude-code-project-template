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
