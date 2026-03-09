# Task Backlog

> **Convention**: Pick tasks from top of Active (highest priority first).
> Move to In Progress when starting. Move to Completed when done.

## In Progress
<!-- Only ONE task here at a time. Focus. -->

## Active Tasks

### P0 -- Must Have (core functionality)

#### T-P0-3: Rendering Compatibility Audit
- **Priority**: P0
- **Complexity**: M (1 session)
- **Depends on**: T-P0-2
- **Acceptance Criteria**:
  - [ ] Evaluate markdown renderer: test if `hexo-renderer-marked` works with NexT TOC/mermaid, or switch to `hexo-renderer-markdown-it`
  - [ ] If switching renderer: `npm install hexo-renderer-markdown-it && npm uninstall hexo-renderer-marked`, then verify all 47 posts build without error
  - [ ] Post list diff: `find public -name "*.html" -path "*/20*" | sort` matches baseline (same post count)
  - [ ] Spot-check 5 posts via `hexo s`, for EACH verify:
    - Images load (no 404) -- check posts with `{% asset_img %}` tags
    - TOC generates in sidebar
    - Code blocks have syntax highlighting
    - Math formulas render correctly (check DS/DDIA posts)
    - Page layout is normal (no overflow, no broken sidebar)
  - [ ] Specific posts to check:
    - `Designing-Data-Intensive-Applications-Note-17` (longest DDIA, images + possible math)
    - `Designing-Data-Intensive-Applications-Note-10` (images)
    - `SQL-Study-Note-1` (code blocks)
    - `DS-Study-Note-9` (formulas)
    - Any post with mermaid diagrams
  - [ ] Fix any rendering issues found
- **Files**: `package.json` (if renderer changed), `_config.next.yml` (highlight adjustments)

---

#### T-P0-4: First Deployment -- Theme Only
- **Priority**: P0
- **Complexity**: S (< 30 min)
- **Depends on**: T-P0-3
- **Acceptance Criteria**:
  - [ ] `hexo clean && hexo g && hexo d` succeeds
  - [ ] Live site (umiao.github.io) loads with NexT theme
  - [ ] Spot-check 2 posts on live site: images load, TOC works, no broken layout
  - [ ] CDN resources (fonts, JS) load correctly (check browser console for errors)
- **Files**: None (deploy only)

---

#### T-P0-5: Move Sensitive Posts to Drafts
- **Priority**: P0
- **Complexity**: M (1 session)
- **Depends on**: T-P0-4
- **Acceptance Criteria**:
  - [ ] `source/_drafts/` directory created
  - [ ] Add fixed `permalink` to front matter of each sensitive post BEFORE moving:
    - `Behavioral-Interview-Questions-Crack.md` -> `permalink: behavioral-interview-questions-crack/`
    - `Need-To-Knows-For-Software-Security-Engineer.md` -> `permalink: need-to-knows-for-software-security-engineer/`
    - `System-Design-Interview-Alex-Xu-Notes-1.md` -> `permalink: system-design-interview-alex-xu-notes-1/`
    - `System-Design-Interview-Alex-Xu-Notes-2.md` -> `permalink: system-design-interview-alex-xu-notes-2/`
  - [ ] Note: front matter `permalink` overrides global `:year/:month/:day/:title/` pattern
  - [ ] Move FIRST post + its asset folder to `_drafts/`, run `hexo s --draft`, verify images load from drafts. Only proceed if OK. (Historical bugs with _drafts + post_asset_folder)
  - [ ] Move remaining 3 posts + their asset folders to `_drafts/`
  - [ ] `Object-Oriented-Design.md` stays in `_posts/` (confirmed public)
  - [ ] `hexo s` (without --draft) -- verify 4 sensitive posts are NOT visible
  - [ ] `hexo s --draft` -- verify 4 sensitive posts ARE visible with images
  - [ ] Post count: 43 public posts (47 - 4 drafts)
- **Files**: `source/_drafts/` (new), 4 posts moved, 4 asset folders moved

---

#### T-P0-6: Deployment Safety Script + Guide
- **Priority**: P0
- **Complexity**: M (1 session)
- **Depends on**: T-P0-5
- **Acceptance Criteria**:
  - [ ] `tools/safe-deploy.sh` created with:
    - `hexo clean` first (clears any stale `--draft` builds in public/)
    - `hexo g` to generate
    - After generate: diff `public/` article list vs `source/_posts/` file list -- abort if mismatch (draft leakage check)
    - Print list of posts that WILL be deployed
    - Print list of drafts that will NOT be deployed
    - Interactive confirmation prompt before `hexo d`
    - `hexo d` only after confirmation
  - [ ] `docs/deployment-guide.md` created with:
    - How to preview locally: `hexo s --draft` (includes drafts)
    - How to preview deploy-only: `hexo s` (excludes drafts)
    - How to create new draft: `hexo new draft <title>`
    - How to publish a draft: add `permalink` first, then `hexo publish <filename>`
    - How to un-publish: move file + asset folder back to `_drafts/`
    - Permalink priority explanation (front matter overrides global pattern)
    - Pre-deployment checklist
    - If new posts added to a series: update series index page
  - [ ] Test safe-deploy.sh: run it, verify it lists correct posts, cancel at confirmation
  - [ ] Deploy via safe-deploy.sh: confirm 4 drafts don't appear on live site
- **Files**: `tools/safe-deploy.sh` (new), `docs/deployment-guide.md` (new)

---

### P1 -- Should Have (important features)

#### T-P1-1: Series Master Index Page
- **Priority**: P1
- **Complexity**: S (< 30 min)
- **Depends on**: T-P0-6
- **Acceptance Criteria**:
  - [ ] `source/series/index.md` created with links to DDIA, SQL, DS series
  - [ ] Menu added to `_config.next.yml`: `Series: /series/ || fa fa-book`
  - [ ] Page accessible via nav bar, links work
- **Files**: `source/series/index.md` (new), `_config.next.yml`

---

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
