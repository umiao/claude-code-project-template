# Task Backlog

> **Convention**: Pick tasks from top of Active (highest priority first).
> Move to In Progress when starting. Move to Completed when done.

## In Progress
<!-- Only ONE task here at a time. Focus. -->

## Active Tasks

### P1 -- Should Have (important features)

#### T-P1-2: DDIA Series Index Page
- **Priority**: P1
- **Complexity**: M (1 session)
- **Depends on**: T-P1-1
- **Acceptance Criteria**:
  - [ ] `source/series/ddia/index.md` created with:
    - Series description (1-2 paragraphs about DDIA book)
    - Mermaid mindmap at TOPIC level only (Part I/II/III groupings, NOT 19 leaf nodes)
    - Ordered markdown list of all 19 posts with `{% post_link %}` links
  - [ ] Mermaid mindmap renders correctly via `hexo s`
  - [ ] All 19 post links work
- **Files**: `source/series/ddia/index.md` (new)

---

#### T-P1-3: SQL Series Index Page
- **Priority**: P1
- **Complexity**: S (< 30 min)
- **Depends on**: T-P1-1
- **Acceptance Criteria**:
  - [ ] `source/series/sql/index.md` created with:
    - Series description
    - Mermaid mindmap of SQL topic areas
    - Ordered list of all 16 SQL posts with links
  - [ ] All links work, mindmap renders
- **Files**: `source/series/sql/index.md` (new)

---

#### T-P1-4: Data Science Series Index Page
- **Priority**: P1
- **Complexity**: S (< 30 min)
- **Depends on**: T-P1-1
- **Acceptance Criteria**:
  - [ ] `source/series/ds/index.md` created with:
    - Series description
    - Mermaid mindmap of DS topic areas
    - Ordered list of all 9 DS posts with links
  - [ ] All links work, mindmap renders
- **Files**: `source/series/ds/index.md` (new)

---

#### T-P1-5: Deploy Series Pages
- **Priority**: P1
- **Complexity**: S (< 30 min)
- **Depends on**: T-P1-2, T-P1-3, T-P1-4
- **Acceptance Criteria**:
  - [ ] Run `tools/safe-deploy.sh`
  - [ ] Verify series pages accessible on live site
  - [ ] All post links from series pages work on live site
- **Files**: None (deploy only)

---

### P2 -- Nice to Have (polish, optimization)

#### T-P2-1: Post Front Matter Cleanup
- **Priority**: P2
- **Complexity**: M (1 session)
- **Depends on**: T-P0-6
- **Acceptance Criteria**:
  - [ ] All posts have `description:` field in front matter (for SEO)
  - [ ] Category/tag naming is consistent across all posts (audit and normalize)
  - [ ] All posts have `<!-- more -->` break for proper excerpt on index page
- **Files**: All `source/_posts/*.md`

---

#### T-P2-2: SEO Basics (Sitemap + RSS)
- **Priority**: P2
- **Complexity**: S (< 30 min)
- **Depends on**: T-P0-4
- **Acceptance Criteria**:
  - [ ] `npm install hexo-generator-sitemap hexo-generator-feed`
  - [ ] Sitemap config added to `_config.yml`
  - [ ] RSS feed config added to `_config.yml`
  - [ ] `hexo g` produces `public/sitemap.xml` and `public/atom.xml`
  - [ ] Both files contain correct URLs
- **Files**: `_config.yml`, `package.json`

---

#### T-P2-3: About Page Restructure
- **Priority**: P2
- **Complexity**: S (< 30 min)
- **Depends on**: T-P0-4
- **Acceptance Criteria**:
  - [ ] `source/about/index.md` restructured into sections: Bio / Work / Skills / Projects
  - [ ] [NEEDS-INPUT: user to provide current role, title, key info]
  - [ ] Old outdated content removed ("year-one MS student", "incoming intern at ebay")
  - [ ] Images still load correctly
- **Files**: `source/about/index.md`

---

## Dependency Graph

```
T-P0-1 (Backup)
  |
T-P0-2 (Install NexT)
  |
T-P0-3 (Rendering Audit)
  |
T-P0-4 (First Deploy) ----+----+
  |                        |    |
T-P0-5 (Move Drafts)    T-P2-2 T-P2-3
  |                      (SEO)  (About)
T-P0-6 (Safety Script)
  |
T-P1-1 (Series Master)
  |
  +--------+--------+
  |        |        |
T-P1-2  T-P1-3  T-P1-4
(DDIA)  (SQL)   (DS)
  |        |        |
  +--------+--------+
           |
        T-P1-5 (Deploy Series)

T-P2-1 (Front Matter) -- depends on T-P0-6, independent of series
```

---

## Blocked
<!-- Tasks that can't proceed and why -->
- T-P2-3 (About Page): [NEEDS-INPUT: user to provide current role/bio details]

## Completed Tasks
<!-- Move finished tasks here with [x] and completion date -->

- [x] **2026-03-02** -- Git pre-commit hook for ruff version consistency: pinned ruff==0.1.14, fixed CI lint job, created pre-commit hook (version guard + lint + emoji scan), created setup-hooks.sh installer, updated docs.
- [x] **2026-03-09** -- T-P0-1: Backup + Baseline Build: created blog-refactor branch, fixed Hexo scripts/ conflict by renaming to tools/, baseline build succeeds (90 post HTML files, zero errors), rollback verified.
- [x] **2026-03-09** -- T-P0-2: Install NexT Theme: installed hexo-theme-next, created _config.next.yml (Gemini, TOC, reading progress, local search, mermaid, MathJax, code copy, social links, androidstudio highlight), switched theme to next, 90 post HTML files generated.
- [x] **2026-03-09** -- T-P0-3: Rendering Compatibility Audit: hexo-renderer-marked works with NexT (no switch needed). Fixed MathJax not loading (every_page: false -> true, since 32/47 posts use math). Verified images, TOC, code highlighting, mermaid across 5 posts. 90 post HTML files match baseline.
- [x] **2026-03-09** -- T-P0-4: First Deployment -- Theme Only: deployed NexT theme to umiao.github.io. User confirmed deployment.
- [x] **2026-03-09** -- T-P0-5: Move Sensitive Posts to Drafts: added fixed permalinks, moved 4 posts + asset folders to source/_drafts/, verified excluded from regular build (323 files) and included in --draft build (352 files) with images.
- [x] **2026-03-09** -- T-P0-6: Deployment Safety Script + Guide: created tools/safe-deploy.sh (clean, generate, draft-leakage check, post/draft listing, confirmation prompt, deploy) and docs/deployment-guide.md (preview, drafts workflow, permalink priority, pre-deploy checklist). Dry-run verified: 59 posts listed, 4 drafts excluded, no leakage.
- [x] **2026-03-09** -- T-P1-1: Series Master Index Page: created source/series/index.md with links to DDIA, SQL, DS series. Added Series menu item to _config.next.yml nav bar.
