# Task Backlog

<!-- Auto-generated from .claude/tasks.db. Do not edit directly. -->
<!-- Use: python .claude/hooks/task_db.py --help -->

## In Progress

## Active Tasks

### P0 -- Must Have (core functionality)

### P1 -- Should Have (agentic intelligence)

### P2 -- Nice to Have

### P3 -- Stretch Goals

#### T-P3-17: Split XL posts into smaller units
- **Priority**: P3
- **Complexity**: L
- **Depends on**: None
- **Description**: Split System Design Notes 1&2 (596+713 lines) and Git guide (435 lines) into smaller posts. Deferred -- does not impact home page visuals.

## Blocked

## Completed Tasks

> 16 completed tasks archived to [archive/completed_tasks.md](archive/completed_tasks.md).

- [x] **2026-03-16** -- T-P2-16: Series badges on home page. Add series name/progress indicator in post meta via source/_data/post-meta.njk injection. Deferred.
- [x] **2026-03-16** -- T-P2-15: Batch front matter update script. Python script tools/update_frontmatter.py for bulk adding/updating front matter fields. Supports dry-run. Off critical p
- [x] **2026-03-16** -- T-P1-14: Add sticky/featured posts with gallery banners. Add sticky: 1 + photos: front matter to 1-2 highlight posts. NexT renders full-width gallery banner above title. AC: pin
- [x] **2026-03-16** -- T-P0-13: CSS enhancements for index page cards. Add styles to source/_data/styles.styl: image max-height+object-fit (no fixed aspect-ratio), excerpt text clamping (max-
- [x] **2026-03-16** -- T-P0-12: Switch to excerpt mode + fix posts with missing cover images. Set excerpt_description: false in _config.next.yml. Move cover images before <!-- more --> for ~12 posts. Standardize mo
- [x] **2026-03-12** -- T-P3-8: /plan-series Skill: Created `.claude/skills/plan-series/SKILL.md` with 8-step workflow for scaffolding new blog series (series index page with Mermaid mindmap, stub posts with full front matter, concepts.yml registration, series master index update).
- [x] **2026-03-12** -- T-P3-7: Anki Export Tool: Created `tools/export_anki.py` that reads key_concepts and takeaways from all 64 posts, generates 370 Anki flashcards (concept definition + takeaway recall cards) as tab-separated CSV to `data/anki_export.csv`. All file I/O uses encoding="utf-8".
- [x] **2026-03-12** -- T-P3-6: Visual Knowledge Map: Created `source/knowledge-map/index.md` with Mermaid diagram showing 4 domain clusters (DDIA, SQL, DS, Interview) with key concept nodes and cross-domain connections. Added nav menu entry. hexo generate produces 207 files with Mermaid rendering.
