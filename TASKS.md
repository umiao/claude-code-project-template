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

#### T-P0-14: Review Queue Tool
- Complexity: M | Depends on: none
- Create `tools/review_queue.py` implementing the SM-2 spaced repetition algorithm
- Commands: `show` (list due posts), `mark <slug> <rating>` (record review, rating 0-5), `init` (scan posts, build initial queue), `stats` (summary of review status)
- Store review state in `data/review_state.json` (per-post: last_reviewed, interval, easiness, repetitions, next_due)
- Track `content_hash` (MD5 of post body) per post to detect content changes and reset intervals
- All file I/O must use `encoding="utf-8"`
- **Acceptance Criteria**:
  1. `tools/review_queue.py` exists, runs without errors (`python tools/review_queue.py --help`)
  2. `init` command scans `source/_posts/` and populates `data/review_state.json`
  3. `show` command lists posts due for review (initially all posts)
  4. `mark` command updates interval/next_due using SM-2 formula
  5. `stats` command prints summary (total posts, due today, average interval)
  6. Content hash change detection works (modify a post, run show, see it flagged)

#### T-P0-15: Publish Draft Posts
- Complexity: S | Depends on: T-P0-12
- Move 4 posts from `source/_drafts/` to `source/_posts/` with updated front matter
- Add `key_concepts`, `takeaways`, proper categories/tags using scaffold template
- **Acceptance Criteria**:
  1. `source/_drafts/` is empty (all 4 posts moved)
  2. Each moved post has complete front matter (key_concepts, takeaways, categories, tags)
  3. `hexo generate` succeeds, post count increases by 4
  4. No draft leakage issues (posts are now intentionally public)

### Should Have (P1)

#### T-P1-6: /blog-from-notes Skill
- Complexity: L | Depends on: T-P0-12, T-P0-13
- Create `.claude/skills/blog-from-notes/SKILL.md`
- Skill reads raw material from `docs/raw-input/`, generates a formatted Hexo post using the scaffold template from T-P0-12, looks up `data/concepts.yml` for concept tagging, and shows draft for user confirmation before writing
- Include instructions for: reading input files, mapping content to front matter fields, selecting appropriate categories/tags, generating `key_concepts` from concepts.yml matches
- **Acceptance Criteria**:
  1. `.claude/skills/blog-from-notes/SKILL.md` exists with complete skill instructions
  2. Skill references scaffold template fields and concepts.yml lookup
  3. Skill includes confirmation step before writing the post file
  4. Manual test: place a sample `.md` in `docs/raw-input/`, invoke `/blog-from-notes`, verify output post has correct front matter

#### T-P1-7: /refine-post Skill
- Complexity: M | Depends on: T-P0-12, T-P0-13
- Create `.claude/skills/refine-post/SKILL.md`
- Skill reads a specified post, adds/updates `key_concepts` (validated against `data/concepts.yml`), `takeaways`, `series`/`series_index`, fixes image alt text, and shows a diff for user confirmation before writing
- Must handle posts that already have partial front matter (merge, don't overwrite)
- **Acceptance Criteria**:
  1. `.claude/skills/refine-post/SKILL.md` exists with complete skill instructions
  2. Skill validates concepts against concepts.yml (warns on unrecognized concepts)
  3. Skill shows diff before applying changes
  4. Manual test: run on one DDIA post, verify front matter is enriched correctly

#### T-P1-8: /study-review Skill (Basic)
- Complexity: M | Depends on: T-P0-14
- Create `.claude/skills/study-review/SKILL.md`
- Skill runs `tools/review_queue.py show` to find due posts, reads each due post, generates quiz questions (key concept recall, application questions), presents to user, user self-rates (0-5), skill calls `mark` to update queue
- Basic version: generates questions from full post content (enhanced later with key_concepts front matter)
- **Acceptance Criteria**:
  1. `.claude/skills/study-review/SKILL.md` exists with complete skill instructions
  2. Skill integrates with review_queue.py (show + mark commands)
  3. Skill generates at least 3 question types (definition, application, comparison)
  4. Manual test: init queue, invoke `/study-review`, complete one review cycle

> **P1 Checkpoint**: User can (1) create new posts from notes via `/blog-from-notes`, (2) run daily review sessions via `/study-review`.

#### T-P1-9: Enrich DDIA Series (Pilot)
- Complexity: M | Depends on: T-P1-7
- Use `/refine-post` to add `key_concepts`, `takeaways`, `series: DDIA`, `series_index` to all 19 DDIA posts
- This is the pilot batch: validate concept index output and front matter quality before proceeding to other series
- **Acceptance Criteria**:
  1. All 19 DDIA posts have `key_concepts` (non-empty list), `takeaways`, `series: DDIA`, `series_index` (1-19)
  2. All key_concepts values exist in `data/concepts.yml` (or concepts.yml updated to include new ones)
  3. `hexo generate` succeeds with no errors
  4. Spot-check 3 posts: concepts and takeaways are accurate and meaningful

#### T-P1-10: Enrich SQL + DS + Remaining Posts
- Complexity: L | Depends on: T-P1-9
- Use `/refine-post` on 16 SQL posts, 9 DS posts, and ~11 remaining posts
- Apply same quality bar as DDIA pilot
- **Acceptance Criteria**:
  1. All 47 published posts have `key_concepts` (non-empty) and `takeaways`
  2. SQL posts have `series: SQL`, DS posts have `series: Data Science`, with correct `series_index`
  3. All key_concepts values exist in `data/concepts.yml`
  4. `hexo generate` succeeds with no errors

#### T-P1-11: Blog Quality Fixes
- Complexity: S | Depends on: none
- Enable Open Graph + Twitter Cards in `_config.next.yml`
- Fix search config (`preload: true`)
- Create custom `source/404.md`
- Fix wrong `asset_img` alt text across posts
- **Acceptance Criteria**:
  1. Open Graph and Twitter Card meta tags present in generated HTML
  2. Local search works with preload enabled
  3. `public/404.html` exists after `hexo generate`
  4. No empty or placeholder alt text in post images

### Nice to Have (P2)

#### T-P2-4: Concept Index Generator Plugin
- Complexity: M | Depends on: T-P1-9
- Create `scripts/generate-concept-index.js` as a Hexo generator plugin
- Reads `key_concepts` from all post front matter, produces alphabetical index page at `/concepts/`
- Create `source/concepts/index.md` scaffold page
- Format: each concept links to all posts that reference it
- **Acceptance Criteria**:
  1. `scripts/generate-concept-index.js` exists and is loaded by Hexo
  2. `hexo generate` produces `public/concepts/index.html`
  3. Concept index page lists concepts alphabetically with links to relevant posts
  4. At least the 19 DDIA posts' concepts appear correctly

#### T-P2-5: Series Navigation Plugin
- Complexity: S | Depends on: T-P1-9
- Create `scripts/series-nav.js` as a Hexo filter plugin
- Uses `series` + `series_index` front matter to inject prev/next navigation links into post content
- Follow pattern from `scripts/filter-life-homepage.js` for Hexo filter registration
- **Acceptance Criteria**:
  1. `scripts/series-nav.js` exists and is loaded by Hexo
  2. DDIA posts show prev/next links (e.g., post 5 links to posts 4 and 6)
  3. First post has no "prev", last post has no "next"
  4. `hexo generate` succeeds with no errors

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
<!-- Move finished tasks here with [x] and completion date -->
<!-- Historical note: Completed tasks below used P as Phase (P0-P5).
     Active tasks follow canonical convention: T-P{priority}-{number}, where P = Priority. -->

- [x] **2026-03-12** -- T-P0-13: Concept Registry. Created data/concepts.yml with 59 concepts covering all 4 domains (DDIA: 18, SQL: 14, DS: 15, Interview: 12). Format: list entries with name, aliases (list), domain fields. Valid YAML parseable by yaml.safe_load. Test suite validates existence, YAML validity, count >= 40, all domains covered, required fields present. All tests pass.
- [x] **2026-03-12** -- T-P0-12: Scaffold + Front Matter Schema. Updated scaffolds/post.md to include knowledge-system fields: categories, tags (preserved), description, key_concepts, takeaways, series, series_index. All fields default to empty. Test: hexo new "Test Post" produces post with full front matter template. hexo generate succeeds (396 files, zero errors). Existing posts unaffected by scaffold change.
- [x] **2026-03-11** -- T-P0-7: Restore NexT theme with Life category support. Switched theme yilia -> next, created scripts/filter-life-homepage.js generator plugin to hide Life posts from homepage, created source/_data/sidebar.njk Life widget for NexT sidebar, added custom_file_path.sidebar to _config.next.yml. Fixed tags/categories 404s, about page image sizing. Build: 394 files, zero errors. Cake post filtered from homepage, visible in sidebar widget and direct URL.
- [x] **2026-03-11** -- T-P0-11: Review Last 3 Commits + Apply Fixes: created source/tags/index.md and source/categories/index.md with proper Hexo front matter, updated yilia menu config to add Tags and Categories links, fixed About page image sizing (removed hard-coded width/height, added max-width CSS), created Python-based commit-msg hook to enforce English-only commit messages (stored in tools/ and installed to .git/hooks/), hexo generate verified (tags/categories/about pages render correctly).
- [x] **2026-03-02** -- Git pre-commit hook for ruff version consistency: pinned ruff==0.1.14, fixed CI lint job, created pre-commit hook (version guard + lint + emoji scan), created setup-hooks.sh installer, updated docs.
- [x] **2026-03-09** -- T-P0-1: Backup + Baseline Build: created blog-refactor branch, fixed Hexo scripts/ conflict by renaming to tools/, baseline build succeeds (90 post HTML files, zero errors), rollback verified.
- [x] **2026-03-09** -- T-P0-2: Install NexT Theme: installed hexo-theme-next, created _config.next.yml (Gemini, TOC, reading progress, local search, mermaid, MathJax, code copy, social links, androidstudio highlight), switched theme to next, 90 post HTML files generated.
- [x] **2026-03-09** -- T-P0-3: Rendering Compatibility Audit: hexo-renderer-marked works with NexT (no switch needed). Fixed MathJax not loading (every_page: false -> true, since 32/47 posts use math). Verified images, TOC, code highlighting, mermaid across 5 posts. 90 post HTML files match baseline.
- [x] **2026-03-09** -- T-P0-4: First Deployment -- Theme Only: deployed NexT theme to umiao.github.io. User confirmed deployment.
- [x] **2026-03-09** -- T-P0-5: Move Sensitive Posts to Drafts: added fixed permalinks, moved 4 posts + asset folders to source/_drafts/, verified excluded from regular build (323 files) and included in --draft build (352 files) with images.
- [x] **2026-03-09** -- T-P0-6: Deployment Safety Script + Guide: created tools/safe-deploy.sh (clean, generate, draft-leakage check, post/draft listing, confirmation prompt, deploy) and docs/deployment-guide.md (preview, drafts workflow, permalink priority, pre-deploy checklist). Dry-run verified: 59 posts listed, 4 drafts excluded, no leakage.
- [x] **2026-03-09** -- T-P1-1: Series Master Index Page: created source/series/index.md with links to DDIA, SQL, DS series. Added Series menu item to _config.next.yml nav bar.
- [x] **2026-03-09** -- T-P1-2: DDIA Series Index Page: created source/series/ddia/index.md with 2-paragraph description, Mermaid mindmap (Part I/II/III topic groupings), and ordered list of all 19 posts with post_link tags.
- [x] **2026-03-09** -- T-P1-3: SQL Series Index Page: created source/series/sql/index.md with series description, Mermaid mindmap (5 topic groups), and ordered list of all 16 SQL posts with post_link tags.
- [x] **2026-03-09** -- T-P1-4: Data Science Series Index Page: created source/series/ds/index.md with series description, Mermaid mindmap (5 topic groups), and ordered list of all 9 DS posts with post_link tags.
- [x] **2026-03-09** -- T-P1-5: Deploy Series Pages: deployed all series pages to production via safe-deploy.sh. 327 files, no draft leakage, 59 posts deployed.
- [x] **2026-03-09** -- T-P2-1: Post Front Matter Cleanup: added description field to all 59 posts, normalized 5 inconsistent tags (DataScience -> Data Science, capitalized investment/options/futures/trading). All posts already had more breaks.
- [x] **2026-03-09** -- T-P2-2: SEO Basics (Sitemap + RSS): installed hexo-generator-sitemap and hexo-generator-feed, added config to _config.yml, verified sitemap.xml and atom.xml generated with correct URLs.
- [x] **2026-03-09** -- T-P2-3: About Page Restructure: rewrote source/about/index.md with current bio (MLE at eBay), work experience (eBay MLE, eBay intern, NuNova, UCLA research), updated skills, publications, and contact. Removed outdated content. Images preserved.
- [x] **2026-03-10** -- T-P0-8: Separate Life Category Posts to Sidebar: implemented for yilia theme. Modified archive.ejs to filter Life posts from homepage main timeline (using is_home() guard and post.categories.findOne()), created life.ejs widget for sidebar, added to widgets config. Tested: Cake post in sidebar only, not in main timeline. /archives/ and /categories/Life/ still show Life posts. Note: Feature implemented for yilia theme; site currently uses NexT theme.
- [x] **2026-03-11** -- T-P0-9: Activate Life Sidebar Widget + Add Excerpt Break: changed theme from next to yilia in _config.yml (activating Life sidebar widget from T-P0-8), added <!-- more --> tag to Cake-Inspiration-Gallery.md after intro section (line 100). Verified: hexo generate succeeds with 413 files, Cake post filtered from homepage main feed, Life & Hobbies sidebar widget displays with Cake post, full cake gallery content hidden from homepage excerpt.
- [x] **2026-03-11** -- T-P0-10: Establish Major Change Approval Protocol: Added "Major Change Approval Protocol" section to CLAUDE.md defining major changes (theme switches, removing functionality, reversing approved decisions, deployment target changes) with required 4-step approval process (state change + why, list alternatives, show impact, wait for approval). Added lesson entry to LESSONS.md documenting T-P0-9 theme switch incident and correct communication approach. NexT feasibility research completed: (1) Life sidebar widget - FEASIBLE via custom_file_path.sidebar in _config.next.yml, (2) Homepage Life post filtering - FEASIBLE with Hexo filter plugin in scripts/, (3) Tags/Categories pages - NATIVE support in NexT, (4) About page image aspect ratios - FEASIBLE via markdown/CSS. Conclusion: All yilia-specific features can be replicated in NexT with no blockers.
