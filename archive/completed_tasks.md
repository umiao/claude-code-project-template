# Completed Tasks Archive

> 19 completed tasks archived as of latest archival.

- [x] **2026-03-12** -- T-P0-15: Publish Draft Posts. Moved 4 posts from source/_drafts/ to source/_posts/: Behavioral-Interview-Questions-Crack.md, Need-To-Knows-For-Software-Security-Engineer.md, System-Design-Interview-Alex-Xu-Notes-1.md, System-Design-Interview-Alex-Xu-Notes-2.md. Updated front matter for all 4 posts with key_concepts, takeaways, description. Added series info to System Design posts (series: System Design Interview - Alex Xu, series_index: 1/2). Moved all associated asset folders. source/_drafts/ is now empty. Post count increased from 60 to 64 .md files. hexo generate succeeds with 214 files generated in 1.52s.

- [x] **2026-03-12** -- T-P0-14: Review Queue Tool. Created tools/review_queue.py implementing SM-2 spaced repetition algorithm. Commands: init (scan posts), show (list due posts), mark (record review with rating 0-5), stats (summary). Stores state in data/review_state.json with fields: last_reviewed, interval, easiness, repetitions, next_due, content_hash. Tracks MD5 hash of post body to detect content changes and reset review schedules. All file I/O uses encoding="utf-8". Test suite with 7 tests validates functionality. Tested with 60 blog posts.

- [x] **2026-03-12** -- T-P0-13: Concept Registry. Created data/concepts.yml with 59 concepts covering all 4 domains (DDIA: 18, SQL: 14, DS: 15, Interview: 12). Format: list entries with name, aliases (list), domain fields. Valid YAML parseable by yaml.safe_load. Test suite validates existence, YAML validity, count >= 40, all domains covered, required fields present. All tests pass.

- [x] **2026-03-12** -- T-P0-12: Scaffold + Front Matter Schema. Updated scaffolds/post.md to include knowledge-system fields: categories, tags (preserved), description, key_concepts, takeaways, series, series_index. All fields default to empty. Test: hexo new "Test Post" produces post with full front matter template. hexo generate succeeds (396 files, zero errors). Existing posts unaffected by scaffold change.

- [x] **2026-03-11** -- T-P0-7: Restore NexT theme with Life category support. Switched theme yilia -> next, created scripts/filter-life-homepage.js generator plugin to hide Life posts from homepage, created source/_data/sidebar.njk Life widget for NexT sidebar, added custom_file_path.sidebar to _config.next.yml. Fixed tags/categories 404s, about page image sizing. Build: 394 files, zero errors. Cake post filtered from homepage, visible in sidebar widget and direct URL.

- [x] **2026-03-11** -- T-P0-11: Review Last 3 Commits + Apply Fixes: created source/tags/index.md and source/categories/index.md with proper Hexo front matter, updated yilia menu config to add Tags and Categories links, fixed About page image sizing (removed hard-coded width/height, added max-width CSS), created Python-based commit-msg hook to enforce English-only commit messages (stored in tools/ and installed to .git/hooks/), hexo generate verified (tags/categories/about pages render correctly).

- [x] **2026-03-02** -- T-P2-4: Git pre-commit hook for ruff version consistency. Pinned ruff==0.1.14, fixed CI lint job, created pre-commit hook (version guard + lint + emoji scan), created setup-hooks.sh installer, updated docs.

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
