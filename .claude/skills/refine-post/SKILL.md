# /refine-post -- Enrich Existing Blog Post Front Matter

Read a specified blog post, add or update front matter fields (`key_concepts`, `takeaways`, `series`, `series_index`), fix image alt text, and show a diff for user confirmation before writing.

## Usage

```
/refine-post <filename>                # Post filename in source/_posts/ (with or without .md)
/refine-post <path>                    # Full path to a post file
/refine-post                           # Interactive: list posts missing key_concepts, pick one
```

## Steps

### 1. Locate Post

1. If a filename or path argument is provided, resolve it:
   - Bare filename (e.g., `Designing-Data-Intensive-Applications-Note-5`) -> `source/_posts/<filename>.md`
   - Already ends with `.md` -> use as-is (prepend `source/_posts/` if no directory)
   - Full path -> use directly
2. If no argument, scan `source/_posts/*.md` for posts missing `key_concepts` in front matter. Show a numbered list of the first 20 and ask the user to pick one.
3. If the file does not exist, report the error and stop.

### 2. Read and Analyze Post

1. Read the entire post file.
2. Parse existing front matter (YAML between `---` delimiters).
3. Read the post body (everything after the second `---`).
4. Identify:
   - **Existing front matter fields**: Note which fields already have values (preserve them unless updating).
   - **Topic and domain**: What the post covers (DDIA, SQL, DS, Interview, other).
   - **Series membership**: Check the title and content for series patterns:
     - "Designing Data-Intensive-Applications-Note-N" -> series: DDIA
     - "SQL-" prefix or SQL content -> series: SQL
     - Data science / ML content -> series: Data Science
     - Other patterns as evident from the title
   - **Image tags**: Find `{% asset_img ... %}` tags and check their alt text.

### 3. Look Up Concepts

1. Read `data/concepts.yml` to load the concept registry.
2. Analyze the post content to identify relevant concepts:
   - Match content against concept names AND aliases from the registry.
   - Consider section headers, bold terms, and repeated technical terms.
   - Select 3-8 most relevant concepts for the post.
3. Use the **canonical `name`** from concepts.yml (not aliases).
4. If the post discusses a concept not in concepts.yml, include it and flag it:
   `[NEW: concept-name]` so the user knows it needs to be added.

### 4. Build Updated Front Matter

Merge new fields into existing front matter. Rules:

- **Preserve existing values** for fields the user has already set (title, date, categories, tags, description, permalink).
- **Add missing fields** from the scaffold template (`scaffolds/post.md`):
  - `key_concepts`: List of 3-8 canonical concept names from concepts.yml
  - `takeaways`: List of 3-6 actionable insights (imperative sentences, e.g., "Use X when Y")
  - `description`: If empty/missing, generate a 1-2 sentence summary
  - `series`: If the post belongs to a series (detected in step 2)
  - `series_index`: Integer position within the series
- **Update existing fields** only when they are empty or clearly placeholder values.
- **Never overwrite** non-empty `title`, `date`, `categories`, `tags` unless the user explicitly asks.

#### Series detection and indexing:

To determine `series_index`, count all posts in the same series within `source/_posts/` and assign based on:
- For DDIA: extract the note number from the filename (e.g., "Note-5" -> series_index: 5)
- For SQL: sort by date and assign sequential index
- For other series: sort by date and assign sequential index

### 5. Fix Image Alt Text

1. Scan the post body for `{% asset_img filename.ext alt_text %}` tags.
2. If alt text is missing, generic (e.g., "image", "ML_note", "cover"), or a filename:
   - Generate descriptive alt text based on the surrounding content context.
   - Record the change for the diff display.
3. Do NOT change alt text that is already descriptive and meaningful.

### 6. Show Diff for Confirmation

Present changes to the user in a clear diff format:

```
## Refine Post: <post title>

### Front Matter Changes
  key_concepts: (added)
    - Concept A
    - Concept B
    - [NEW: Concept C]
  takeaways: (added)
    - Takeaway 1
    - Takeaway 2
  series: DDIA (added)
  series_index: 5 (added)
  description: "Updated description" (was: "Old description")

### Image Alt Text Changes
  Line 13: {% asset_img cover.png ML_note %}
        -> {% asset_img cover.png Storage and retrieval chapter cover diagram %}

### No Changes
  title, date, categories, tags: preserved as-is

Apply these changes? (yes/no/edit)
```

- **yes**: Apply all changes and write the file.
- **no**: Abort without writing.
- **edit**: Ask what the user wants to change, apply edits, show updated diff.

### 7. Write Updated Post

1. Reconstruct the post file:
   - Updated front matter (YAML between `---` delimiters)
   - Original body content with any image alt text fixes
2. Write the file back to its original location.
3. Report:

```
[DONE] Post refined: source/_posts/<filename>.md
Changes:
  - key_concepts: <count> concepts (<count new> flagged)
  - takeaways: <count> added
  - series: <series name> (index <N>)  [if applicable]
  - image alt text: <count> fixed  [if applicable]
```

### 8. Flag New Concepts (if any)

If any `key_concepts` were flagged as `[NEW: ...]` in step 3:

```
[WARN] New concepts not yet in data/concepts.yml:
  - <concept 1> (suggested domain: <domain>)
  - <concept 2> (suggested domain: <domain>)

Add these to data/concepts.yml? (yes/no)
```

If yes, append the new concepts to the appropriate domain section in `data/concepts.yml`:

```yaml
- name: <Concept Name>
  aliases:
    - <alias 1>
  domain: <DOMAIN>
```

## Important Rules

- **Merge, don't overwrite**: This skill enriches existing front matter. Never discard existing field values unless they are empty or placeholder.
- **Canonical names only**: Always use the `name` field from concepts.yml, never aliases.
- **No emoji**: Use text tags like [DONE], [WARN], [NEW].
- **No invented content**: Takeaways and descriptions must be derived from the actual post content, not fabricated.
- **All file writes use `encoding="utf-8"`**.
- **One post per invocation**: For batch processing, invoke multiple times or use a task like T-P1-9.
- **When in doubt, ask**: If series membership, concept selection, or any other decision is ambiguous, ask the user rather than guessing.
