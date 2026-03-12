# Task Backlog

> **Convention**: Pick tasks from top of Active (highest priority first).
> Move to In Progress when starting. Move to Completed when done.
>
> **Task Schema Template** (required fields for every new task):
> ```
> #### T-PX-NN: Title
> - **Priority**: P0 | P1 | P2 | P3
> - **Complexity**: S (< 1 session) | M (1-2 sessions) | L (3+ sessions)
> - **Depends on**: T-XX-NN | None
> - **Description**: What and why (2-4 sentences)
> - **Acceptance Criteria**:
>   1. Specific, verifiable outcome
>   2. At least one full user journey AC
>   3. Manual smoke test AC for UX tasks
> ```
>
> **Size invariant**: Active TASKS.md must stay under 300 lines. Completed tasks
> are archived to `archive/completed_tasks.md` when exceeded.

## In Progress
<!-- Only ONE task here at a time. Focus. -->

## Active Tasks

### Must Have (P0)
<!-- None -->

### Should Have (P1)

> **P1 Checkpoint**: User can (1) create new posts from notes via `/blog-from-notes`, (2) run daily review sessions via `/study-review`.

### Nice to Have (P2)

#### T-P2-6: Related Posts Plugin
- Complexity: M | Depends on: T-P1-9
- Create `scripts/related-posts.js` as a Hexo filter plugin
- Injects "Related Reading" section at the bottom of each post
- Scoring: tag overlap + key_concepts overlap (weighted 2x higher than tags)
- Show top 3-5 related posts with titles and links
- **Acceptance Criteria**:
  1. `scripts/related-posts.js` exists and is loaded by Hexo
  2. Posts show "Related Reading" section with 3-5 linked posts
  3. Related posts are relevant (share concepts/tags with the source post)
  4. `hexo generate` succeeds with no errors

#### T-P2-7: Interview Prep Hub
- Complexity: M | Depends on: none
- Create `source/interview/index.md` with sections: System Design (DDIA + Alex Xu concepts), Behavioral, Brainteasers, OOD, SQL highlights, system design patterns derived from DDIA
- Add "Interview" to NexT nav menu in `_config.next.yml`
- **Acceptance Criteria**:
  1. `source/interview/index.md` exists with all listed sections
  2. Nav menu updated in `_config.next.yml`
  3. `hexo generate` produces `public/interview/index.html`
  4. Page contains actionable study content (not just headers)

#### T-P2-8: Cheat Sheets
- Complexity: L | Depends on: T-P1-9
- Create `source/cheatsheet/ddia.md` (all 19 DDIA notes condensed into single-page reference)
- Create `source/cheatsheet/sql.md` and `source/cheatsheet/ds.md`
- Format: comparison tables, key formulas, one-liner summaries per topic
- **Acceptance Criteria**:
  1. All 3 cheat sheet files exist under `source/cheatsheet/`
  2. Each cheat sheet covers all posts in its series
  3. Contains comparison tables and quick-reference content (not just links)
  4. `hexo generate` produces all 3 HTML pages

> **P2 Checkpoint**: User can (1) search any concept via `/concepts/` page, (2) navigate series with prev/next links, (3) see related posts on every article, (4) use interview hub for prep, (5) quick-review via cheat sheets.

### Stretch Goals (P3)

#### T-P3-6: Visual Knowledge Map
- Complexity: M | Depends on: T-P1-10
- Create `source/knowledge-map/index.md` with clustered Mermaid subgraphs
- Subgraphs for: DDIA, SQL, DS, Interview -- showing concept relationships
- **Acceptance Criteria**:
  1. `source/knowledge-map/index.md` exists with Mermaid diagram
  2. Diagram renders correctly in Hexo (Mermaid already enabled in NexT config)
  3. All 4 domain clusters represented with key concept nodes
  4. `hexo generate` produces `public/knowledge-map/index.html`

#### T-P3-7: Anki Export Tool
- Complexity: M | Depends on: T-P1-10
- Create `tools/export_anki.py` that reads `key_concepts` + `takeaways` from all posts
- Generates Anki-compatible CSV (front: concept/question, back: takeaway/answer)
- All file I/O must use `encoding="utf-8"`
- **Acceptance Criteria**:
  1. `tools/export_anki.py` exists, runs without errors
  2. Produces valid CSV importable by Anki (tested with sample)
  3. Covers all posts with key_concepts front matter
  4. Output file written to `data/anki_export.csv`

#### T-P3-8: /plan-series Skill
- Complexity: M | Depends on: T-P0-12, T-P1-6
- Create `.claude/skills/plan-series/SKILL.md`
- Skill scaffolds a new blog series: creates series index page, generates stub posts with front matter, updates concepts.yml with new domain concepts
- **Acceptance Criteria**:
  1. `.claude/skills/plan-series/SKILL.md` exists with complete skill instructions
  2. Skill creates series index page under `source/series/<name>/index.md`
  3. Skill generates stub posts with scaffold template front matter
  4. Manual test: plan a test series, verify all files created correctly

> **P3 Checkpoint**: User can (1) export flashcards to Anki, (2) visualize knowledge map, (3) scaffold entire new series from a topic.

---

## Dependency Graph

```
Must Have (P0)
T-P0-12 (Scaffold) ----+---> T-P1-6 (blog-from-notes)
T-P0-13 (Concepts) ----+---> T-P1-7 (refine-post)
T-P0-14 (Review Queue) ----> T-P1-8 (study-review)
T-P0-12 -----------------> T-P0-15 (Publish drafts)

Should Have (P1)
T-P0-12 + T-P0-13 ---> T-P1-7 (refine-post skill)
T-P1-7 ---> T-P1-9 (Enrich DDIA pilot)
T-P1-9 ---> T-P1-10 (Enrich remaining)
T-P1-11 (Quality fixes) -- independent

Nice to Have (P2)
T-P1-9 ---> T-P2-4 (Concept index)
T-P1-9 ---> T-P2-5 (Series nav)
T-P1-9 ---> T-P2-6 (Related posts)
T-P1-9 ---> T-P2-8 (Cheat sheets)
T-P2-7 (Interview hub) -- independent

Stretch Goals (P3)
T-P1-10 ---> T-P3-6 (Knowledge map)
T-P1-10 ---> T-P3-7 (Anki export)
T-P0-12 + T-P1-6 ---> T-P3-8 (plan-series)
```

---

## Blocked
<!-- Tasks that can't proceed and why -->
<!-- None -->

## Completed Tasks

> 19 completed tasks archived to [archive/completed_tasks.md](archive/completed_tasks.md).

- [x] **2026-03-09** -- T-P2-2: SEO Basics (Sitemap + RSS): installed hexo-generator-sitemap and hexo-generator-feed, added config to _config.yml, verified sitemap.xml and atom.xml generated with correct URLs.

- [x] **2026-03-09** -- T-P2-3: About Page Restructure: rewrote source/about/index.md with current bio (MLE at eBay), work experience (eBay MLE, eBay intern, NuNova, UCLA research), updated skills, publications, and contact. Removed outdated content. Images preserved.

- [x] **2026-03-10** -- T-P0-8: Separate Life Category Posts to Sidebar: implemented for yilia theme. Modified archive.ejs to filter Life posts from homepage main timeline (using is_home() guard and post.categories.findOne()), created life.ejs widget for sidebar, added to widgets config. Tested: Cake post in sidebar only, not in main timeline. /archives/ and /categories/Life/ still show Life posts. Note: Feature implemented for yilia theme; site currently uses NexT theme.

- [x] **2026-03-11** -- T-P0-9: Activate Life Sidebar Widget + Add Excerpt Break: changed theme from next to yilia in _config.yml (activating Life sidebar widget from T-P0-8), added <!-- more --> tag to Cake-Inspiration-Gallery.md after intro section (line 100). Verified: hexo generate succeeds with 413 files, Cake post filtered from homepage main feed, Life & Hobbies sidebar widget displays with Cake post, full cake gallery content hidden from homepage excerpt.

- [x] **2026-03-11** -- T-P0-10: Establish Major Change Approval Protocol: Added "Major Change Approval Protocol" section to CLAUDE.md defining major changes (theme switches, removing functionality, reversing approved decisions, deployment target changes) with required 4-step approval process (state change + why, list alternatives, show impact, wait for approval). Added lesson entry to LESSONS.md documenting T-P0-9 theme switch incident and correct communication approach. NexT feasibility research completed: (1) Life sidebar widget - FEASIBLE via custom_file_path.sidebar in _config.next.yml, (2) Homepage Life post filtering - FEASIBLE with Hexo filter plugin in scripts/, (3) Tags/Categories pages - NATIVE support in NexT, (4) About page image aspect ratios - FEASIBLE via markdown/CSS. Conclusion: All yilia-specific features can be replicated in NexT with no blockers.

- [x] **2026-03-12** -- T-P1-6: /blog-from-notes Skill: Created `.claude/skills/blog-from-notes/SKILL.md` with 7-step workflow (locate input, analyze content, generate front matter, format body, show draft for confirmation, write post, flag new concepts). Skill references `scaffolds/post.md` template and `data/concepts.yml` for concept tagging. Created `docs/raw-input/` directory with README and sample input file for testing.

- [x] **2026-03-12** -- T-P1-7: /refine-post Skill: Created `.claude/skills/refine-post/SKILL.md` with 8-step workflow (locate post, read/analyze, concept lookup against concepts.yml, build updated front matter with merge strategy, fix image alt text, show diff for confirmation, write updated post, flag new concepts). Handles partial front matter without overwriting existing values.

- [x] **2026-03-12** -- T-P1-8: /study-review Skill (Basic): Created `.claude/skills/study-review/SKILL.md` with 7-step workflow integrating review_queue.py (show+mark). Generates 5 question types (definition, application, comparison, connection, recall detail). Supports single post, sequential "all" mode, and special commands (skip/show/stop/stats).

- [x] **2026-03-12** -- T-P1-11: Blog Quality Fixes: Enabled Open Graph + Twitter Cards in `_config.next.yml`, set search preload to true, created `source/404.md` custom error page, fixed placeholder/wrong alt text across ~45 posts (replaced generic "ML_note", "SQL Note of blur!", "apple", "Note" with descriptive alt text). Verified: `hexo generate` succeeds, OG+Twitter meta tags in HTML, 404.html generated.

- [x] **2026-03-12** -- T-P1-9: Enrich DDIA Series (Pilot): Added key_concepts, takeaways, series: DDIA, series_index to all 19 DDIA posts. Added 10 new DDIA concepts to concepts.yml. Spot-checked 3 posts for accuracy. hexo generate succeeds.

- [x] **2026-03-12** -- T-P1-10: Enrich SQL + DS + Remaining Posts: Added key_concepts, takeaways, and series metadata to all 41 remaining posts (16 SQL, 9 DS, 16 misc). Added 29 new concepts to concepts.yml (SQL, DS, Interview, General domains). Fixed 4 previously-enriched posts. All 64 posts validated. hexo generate succeeds.

- [x] **2026-03-12** -- T-P2-4: Concept Index Generator Plugin: Created `scripts/generate-concept-index.js` Hexo generator that reads key_concepts from all posts, produces alphabetical `/concepts/index.html` with letter navigation and 87 concepts linked to their posts.

- [x] **2026-03-12** -- T-P2-5: Series Navigation Plugin: Created `scripts/series-nav.js` Hexo filter plugin that injects prev/next navigation links into series posts using `series` and `series_index` front matter. All 46 series posts get nav links.
