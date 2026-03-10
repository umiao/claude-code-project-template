# Deployment Guide

## Quick Reference

| Action | Command |
|--------|---------|
| Safe deploy (recommended) | `bash tools/safe-deploy.sh` |
| Dry run (no deploy) | `bash tools/safe-deploy.sh --dry-run` |
| Preview with drafts | `hexo s --draft` |
| Preview production view | `hexo s` |

---

## Local Preview

### Preview including drafts

```bash
hexo s --draft
```

Opens at `http://localhost:4000`. Shows all posts AND drafts. Useful for
reviewing draft content before publishing.

### Preview production view (no drafts)

```bash
hexo s
```

Shows only published posts. Use this to verify exactly what the live site
will look like after deployment.

---

## Drafts Workflow

### Create a new draft

```bash
hexo new draft "My Post Title"
```

This creates `source/_drafts/My-Post-Title.md`. The draft will NOT appear
on the live site.

### Publish a draft

Before publishing, add a `permalink` field to the front matter so the URL
stays stable regardless of file location:

```yaml
---
title: My Post Title
permalink: 2026/03/10/My-Post-Title/
---
```

Then publish:

```bash
hexo publish "My-Post-Title"
```

This moves the file (and its asset folder, if any) from `source/_drafts/`
to `source/_posts/`.

### Un-publish a post (move back to drafts)

Manually move the `.md` file and its asset folder:

```bash
mv source/_posts/My-Post-Title.md source/_drafts/
mv source/_posts/My-Post-Title/ source/_drafts/   # asset folder, if exists
```

The `permalink` field in front matter ensures the URL stays the same if
you re-publish later.

---

## Permalink Priority

Hexo resolves post URLs in this order:

1. **Front matter `permalink:`** -- if set, this overrides everything.
2. **`_config.yml` `permalink:` pattern** -- the global default
   (currently `:year/:month/:day/:title/`).

Posts moved between `_posts/` and `_drafts/` keep their URLs as long as
the front matter `permalink` field is set.

---

## Deployment

### Recommended: safe-deploy.sh

```bash
bash tools/safe-deploy.sh
```

The script performs these steps automatically:

1. `hexo clean` -- clears stale builds (including any `--draft` artifacts)
2. `hexo generate` -- production build (no drafts)
3. Draft-leakage check -- scans `public/` for draft slugs; aborts if found
4. Prints list of posts that WILL be deployed
5. Prints list of drafts that will NOT be deployed
6. Interactive confirmation prompt
7. `hexo deploy` -- pushes to GitHub Pages

Use `--dry-run` to run steps 1-5 without deploying.

### Manual deployment (not recommended)

```bash
hexo clean && hexo g && hexo d
```

This skips the draft-leakage check. Only use if you are certain no drafts
were accidentally built.

---

## Pre-Deployment Checklist

- [ ] Run `hexo s` locally and spot-check a few posts
- [ ] Verify images load correctly
- [ ] If math posts changed, verify MathJax renders
- [ ] If new posts added to a series, update the series index page
- [ ] Run `bash tools/safe-deploy.sh --dry-run` to verify no draft leakage
- [ ] Deploy with `bash tools/safe-deploy.sh`
- [ ] After deploy, check https://umiao.github.io/ in the browser
- [ ] Check browser console for CDN/resource errors
