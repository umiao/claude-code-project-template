# /blog-from-notes -- Create Blog Post from Raw Notes

Transform raw notes or outlines into a fully formatted Hexo blog post with enriched front matter.

## Usage

```
/blog-from-notes                        # Interactive: list files in docs/raw-input/, pick one
/blog-from-notes <filename>             # Process a specific file from docs/raw-input/
/blog-from-notes <path>                 # Process a file from an arbitrary path
```

## Steps

### 1. Locate Input

1. If a filename or path argument is provided, use that file directly.
2. Otherwise, list all `.md` and `.txt` files in `docs/raw-input/`.
3. If the directory is empty, tell the user:
   ```
   No input files found in docs/raw-input/.
   Place your raw notes there (Markdown or plain text) and run /blog-from-notes again.
   ```
4. If multiple files exist, show a numbered list and ask the user to pick one.

### 2. Analyze Input Content

1. Read the selected input file completely.
2. Identify:
   - **Topic**: What the notes are about (e.g., "DDIA Chapter 5", "SQL Window Functions")
   - **Domain**: Which domain it belongs to (DDIA, SQL, DS, Interview, or other)
   - **Existing structure**: Headers, sections, code blocks, images
   - **Series potential**: Does this belong to an existing series? Check existing posts in `source/_posts/` for series patterns (DDIA, SQL, DS, System Design Interview, etc.)

### 3. Generate Front Matter

Build front matter using the scaffold template from `scaffolds/post.md`:

```yaml
---
title: <Descriptive title derived from content>
permalink: <kebab-case-slug>/
date: <current date in YYYY-MM-DD HH:mm:ss format>
categories:
- [<Top-level>, <Sub-level>]
tags:
- <tag1>
- <tag2>
description: <1-2 sentence summary of what the reader will learn>
key_concepts:
- <concept 1>
- <concept 2>
takeaways:
- <actionable insight 1>
- <actionable insight 2>
series: <series name if applicable, omit if standalone>
series_index: <number if part of a series, omit if standalone>
---
```

#### Front matter field guidelines:

- **title**: Clear, descriptive. Match the style of existing posts (e.g., "Designing Data Intensive Applications Note 5" for DDIA series).
- **permalink**: Kebab-case version of the title, ending with `/`.
- **date**: Use current date/time.
- **categories**: Use nested array format `[Top-level, Sub-level]`. Look at existing posts for category conventions:
  - `[Study Notes, Data Systems]` for DDIA
  - `[Study Notes, Database]` for SQL
  - `[Study Notes, Data Science]` for DS
  - `[Job Search, Software Engineering]` for Interview
  - Create sensible categories for new topics
- **tags**: 3-8 specific tags. Prefer reusing existing tags from the blog.
- **description**: 1-2 sentences summarizing the post's value to the reader.
- **key_concepts**: Look up `data/concepts.yml` for matching concepts.
  - Use the canonical `name` field from concepts.yml (not aliases).
  - If the notes discuss a concept not yet in concepts.yml, include it anyway and flag it: `[NEW: concept-name]` so the user knows it needs to be added to the registry.
  - Aim for 3-8 key concepts per post.
- **takeaways**: 3-6 actionable insights the reader should remember. Write as imperative sentences (e.g., "Use X when Y" not "X is used when Y").
- **series** / **series_index**: Set these if the post belongs to a series. Determine the next index by counting existing posts in the series within `source/_posts/`.

### 4. Format Post Body

1. Convert raw notes into clean Hexo-compatible Markdown:
   - Add a brief intro paragraph before `<!-- more -->` (the excerpt break).
   - Organize content under clear `#` / `##` / `###` headers.
   - Wrap code snippets in fenced code blocks with language tags.
   - For images: use `{% asset_img filename.ext alt text %}` syntax if images will be in the post asset folder. Otherwise use standard Markdown image syntax.
   - Preserve any tables, lists, and formatting from the original notes.
2. Do NOT invent content -- only restructure and format what the user provided. If sections are thin, leave them thin rather than padding with generic text.
3. Add `<!-- more -->` after the introductory section (first 2-4 sentences or first paragraph) to control the homepage excerpt.

### 5. Show Draft for Confirmation

Present the complete post to the user in a structured preview:

```
## Draft Post Preview

### Front Matter
<show the YAML front matter block>

### Content Preview (first 30 lines)
<show the first ~30 lines of body content>

### Summary
- File: source/_posts/<Proposed-Filename>.md
- Series: <series name> (index <N>) | Standalone
- Key concepts: <count> (<count new> not in concepts.yml)
- Word count: ~<N> words

Proceed with writing this post? (yes/no/edit)
```

- **yes**: Write the file and report success.
- **no**: Abort without writing.
- **edit**: Ask what changes the user wants, apply them, show updated preview.

### 6. Write Post File

1. Determine the filename: `source/_posts/<Title-In-Kebab-Case>.md`
   - Match existing naming conventions (e.g., `Designing-Data-Intensive-Applications-Note-5.md`)
2. If the post uses `{% asset_img %}` tags, create the asset directory:
   `source/_posts/<Title-In-Kebab-Case>/`
3. Write the complete post file (front matter + body).
4. Report to the user:

```
[DONE] Post created: source/_posts/<filename>.md
- Run `hexo generate` to verify
- Run `hexo server` to preview locally
```

### 7. Flag New Concepts (if any)

If any `key_concepts` were tagged as `[NEW: ...]` in step 3:

```
[WARN] New concepts not yet in data/concepts.yml:
  - <concept 1> (suggested domain: <domain>)
  - <concept 2> (suggested domain: <domain>)

Add these to data/concepts.yml? (yes/no)
```

If yes, append the new concepts to the appropriate domain section in `data/concepts.yml` using the standard format:

```yaml
- name: <Concept Name>
  aliases:
    - <alias 1>
  domain: <DOMAIN>
```

## Notes

- This skill creates ONE post per invocation. For bulk processing, run it multiple times.
- The skill does not delete or modify the input file in `docs/raw-input/`.
- No emoji in output -- use text tags like [DONE], [WARN], [NEW].
- All file writes use `encoding="utf-8"`.
- When in doubt about categorization or series membership, ask the user rather than guessing.
