# Task Backlog

<!-- Auto-generated from .claude/tasks.db. Do not edit directly. -->
<!-- Use: python .claude/hooks/task_db.py --help -->

## In Progress

## Active Tasks

### P0 -- Must Have (core functionality)

#### T-P0-13: CSS enhancements for index page cards
- **Priority**: P0
- **Complexity**: M
- **Depends on**: T-P0-12
- **Description**: Add styles to source/_data/styles.styl: image max-height+object-fit (no fixed aspect-ratio), excerpt text clamping (max-height+overflow:hidden), box-shadow hover (no translateY), spacing, responsive mobile. AC: card heights roughly consistent, images not distorted, clean mobile view.

### P1 -- Should Have (agentic intelligence)

#### T-P1-14: Add sticky/featured posts with gallery banners
- **Priority**: P1
- **Complexity**: S
- **Depends on**: T-P0-13
- **Description**: Add sticky: 1 + photos: front matter to 1-2 highlight posts. NexT renders full-width gallery banner above title. AC: pinned posts appear at top of home page with banner image.

### P2 -- Nice to Have

#### T-P2-15: Batch front matter update script
- **Priority**: P2
- **Complexity**: S
- **Depends on**: None
- **Description**: Python script tools/update_frontmatter.py for bulk adding/updating front matter fields. Supports dry-run. Off critical path -- useful for future maintenance.

#### T-P2-16: Series badges on home page
- **Priority**: P2
- **Complexity**: M
- **Depends on**: None
- **Description**: Add series name/progress indicator in post meta via source/_data/post-meta.njk injection. Deferred.

### P3 -- Stretch Goals

#### T-P3-17: Split XL posts into smaller units
- **Priority**: P3
- **Complexity**: L
- **Depends on**: None
- **Description**: Split System Design Notes 1&2 (596+713 lines) and Git guide (435 lines) into smaller posts. Deferred -- does not impact home page visuals.

## Blocked

## Completed Tasks

- [x] **2026-03-16** -- T-P0-12: Switch to excerpt mode + fix posts with missing cover images. Set excerpt_description: false in _config.next.yml. Move cover images before <!-- more --> for ~12 posts. Standardize mo
- [x] **2026-03-12** -- T-P3-8: /plan-series Skill: Created `.claude/skills/plan-series/SKILL.md` with 8-step workflow for scaffolding new blog series (series index page with Mermaid mindmap, stub posts with full front matter, concepts.yml registration, series master index update).
- [x] **2026-03-12** -- T-P3-7: Anki Export Tool: Created `tools/export_anki.py` that reads key_concepts and takeaways from all 64 posts, generates 370 Anki flashcards (concept definition + takeaway recall cards) as tab-separated CSV to `data/anki_export.csv`. All file I/O uses encoding="utf-8".
- [x] **2026-03-12** -- T-P3-6: Visual Knowledge Map: Created `source/knowledge-map/index.md` with Mermaid diagram showing 4 domain clusters (DDIA, SQL, DS, Interview) with key concept nodes and cross-domain connections. Added nav menu entry. hexo generate produces 207 files with Mermaid rendering.
- [x] **2026-03-12** -- T-P2-8: Cheat Sheets: Created 3 cheat sheet pages (`source/cheatsheet/ddia.md`, `sql.md`, `ds.md`) condensing all 19 DDIA, 16 SQL, and 9 DS posts into quick-reference format with comparison tables, key formulas, and decision guides. Added index page and nav entry.
- [x] **2026-03-12** -- T-P2-7: Interview Prep Hub: Created `source/interview/index.md` with 7 sections (System Design DDIA, Alex Xu, SQL, DS/ML, Behavioral, OOD, Brainteasers). Added nav menu entry. Page has 13 tables, 87 links, and a 1-week study plan.
- [x] **2026-03-12** -- T-P2-6: Related Posts Plugin: Created `scripts/related-posts.js` Hexo filter plugin that injects "Related Reading" section with top 5 related posts scored by tag overlap + key_concepts overlap (2x weight). 57 of 64 posts show related links.
- [x] **2026-03-12** -- T-P2-5: Series Navigation Plugin: Created `scripts/series-nav.js` Hexo filter plugin that injects prev/next navigation links into series posts using `series` and `series_index` front matter. All 46 series posts get nav links.
- [x] **2026-03-12** -- T-P2-4: Concept Index Generator Plugin: Created `scripts/generate-concept-index.js` Hexo generator that reads key_concepts from all posts, produces alphabetical `/concepts/index.html` with letter navigation and 87 concepts linked to their posts.
- [x] **2026-03-12** -- T-P1-9: Enrich DDIA Series (Pilot): Added key_concepts, takeaways, series: DDIA, series_index to all 19 DDIA posts. Added 10 new DDIA concepts to concepts.yml. Spot-checked 3 posts for accuracy. hexo generate succeeds.
- [x] **2026-03-12** -- T-P1-8: /study-review Skill (Basic): Created `.claude/skills/study-review/SKILL.md` with 7-step workflow integrating review_queue.py (show+mark). Generates 5 question types (definition, application, comparison, connection, recall detail). Supports single post, seque
- [x] **2026-03-12** -- T-P1-7: /refine-post Skill: Created `.claude/skills/refine-post/SKILL.md` with 8-step workflow (locate post, read/analyze, concept lookup against concepts.yml, build updated front matter with merge strategy, fix image alt text, show diff for confirmation, write updated post, flag new concepts). Handles partial front matter without overwriting existing values.
- [x] **2026-03-12** -- T-P1-6: /blog-from-notes Skill: Created `.claude/skills/blog-from-notes/SKILL.md` with 7-step workflow (locate input, analyze content, generate front matter, format body, show draft for confirmation, write post, flag new concepts). Skill references `scaffolds/post.md` template and `data/concepts.yml` for concept tagging. Created `docs/raw-input/` dir
- [x] **2026-03-12** -- T-P1-11: Blog Quality Fixes: Enabled Open Graph + Twitter Cards in `_config.next.yml`, set search preload to true, created `source/404.md` custom error page, fixed placeholder/wrong alt text across ~45 posts (replaced generic "ML_note", "SQL Note of blur!", "apple", "Note" with descriptive alt text). Verified: `hexo generate` succeeds, OG+Twitter meta tags in HTML, 404.html generated.
- [x] **2026-03-12** -- T-P1-10: Enrich SQL + DS + Remaining Posts: Added key_concepts, takeaways, and series metadata to all 41 remaining posts (16 SQL, 9 DS, 16 misc). Added 29 new concepts to concepts.yml (SQL, DS, Interview, General domains). Fixed 4 previously-enriched posts. All 64 p
- [x] **2026-03-11** -- T-P0-9: Activate Life Sidebar Widget + Add Excerpt Break: changed theme from next to yilia in _config.yml (activating Life sidebar widget from T-P0-8), added <!-- more --> tag to Cake-Inspiration-Gallery.md after intro section (line 100). Verified: hexo generate succeeds with 413 files, Cake post filtered from homepage main feed, Life & Hobbies sidebar widg
- [x] **2026-03-11** -- T-P0-10: Establish Major Change Approval Protocol: Added "Major Change Approval Protocol" section to CLAUDE.md defining major changes (theme switches, removing functionality, reversing approved decisions, deployment target changes) with required 4-step approval process (state change + why, list alternatives, show impact, wait for approval). Added lesson entry to LESSONS.md documenting T-P0-9 theme switch incident and correct communication approach. NexT feasi
- [x] **2026-03-10** -- T-P0-8: Separate Life Category Posts to Sidebar: implemented for yilia theme. Modified archive.ejs to filter Life posts from homepage main timeline (using is_home() guard and post.categories.findOne
- [x] **2026-03-09** -- T-P2-3: About Page Restructure: rewrote source/about/index.md with current bio (MLE at eBay), work experience (eBay MLE, eBay intern, NuNova, UCLA research), updated skills, publications, and contact. Removed outdated content. Images preserved.
- [x] **2026-03-09** -- T-P2-2: SEO Basics (Sitemap + RSS): installed hexo-generator-sitemap and hexo-generator-feed, added config to _config.yml, verified sitemap.xml and atom.xml generated with correct URLs.
