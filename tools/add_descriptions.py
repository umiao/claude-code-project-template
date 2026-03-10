"""Add description: field to all posts missing it."""

import os
import re

POSTS_DIR = "source/_posts"

# Manual overrides for posts where auto-extract is weak
MANUAL_DESCS: dict[str, str] = {
    "14th-May-Researcher-Paper-Work-Group.md": "Notes from a research paper discussion group covering robust selection, stream processing, and UCB procedures.",
    "DS-Study-Note-9.md": "Study notes on Gradient Boosting Machine Tree models including GBM and XGBoost algorithms.",
    "SQL-Study-Note-1.md": "SQL syntax basics covering SELECT, WHERE, JOIN, and fundamental database query operations.",
    "SQL-Study-Note-2.md": "SQL data manipulation syntax including INSERT, UPDATE, and DELETE operations with table attributes.",
    "SQL-Study-Note-3.md": "SQL built-in functions and aggregate functions including COUNT, MAX, MIN, AVG, and SUM.",
    "SQL-Study-Note-4.md": "SQL Views for storing and reusing query results as virtual tables.",
    "SQL-Study-Note-5.md": "SQL stored procedures and user-defined functions for encapsulating reusable query logic.",
    "SQL-Study-Note-6.md": "SQL triggers and scheduled events for automating database operations.",
    "SQL-Study-Note-7.md": "SQL transactions and ACID principles for ensuring data integrity.",
    "SQL-Study-Note-8.md": "MySQL data types including VARCHAR, TEXT, and best practices for type selection.",
    "SQL-Study-Note-9.md": "Data modeling pipeline, database constraints, and normalization forms for relational databases.",
    "Introduction-to-Git.md": "Thorough analysis and learning notes on Git version control based on official Git documentation.",
}


def extract_description(body: str) -> str:
    """Extract a description from the post body."""
    lines = body.strip().split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("{%") or line.startswith("<!--") or line.startswith("#"):
            continue
        if line.startswith(">"):
            line = line.lstrip("> ")
        # Clean markdown formatting
        line = re.sub(r"\*\*([^*]+)\*\*", r"\1", line)
        line = re.sub(r"\*([^*]+)\*", r"\1", line)
        line = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", line)
        line = re.sub(r"{%.*?%}", "", line)
        line = line.strip()
        if len(line) > 20:
            if len(line) > 160:
                line = line[:157] + "..."
            return line
    return ""


def process_post(fpath: str, fname: str) -> bool:
    """Add description to a post. Returns True if modified."""
    with open(fpath, encoding="utf-8") as f:
        content = f.read()

    m = re.match(r"^---\n(.*?)\n---\n(.*)", content, re.DOTALL)
    if not m:
        print(f"  SKIP (no front matter): {fname}")
        return False

    fm = m.group(1)
    body = m.group(2)

    # Already has description
    if re.search(r"^description:", fm, re.MULTILINE):
        return False

    # Get description
    desc = MANUAL_DESCS.get(fname, "") or extract_description(body)
    if not desc:
        print(f"  WARNING: no description for {fname}")
        return False

    # Escape quotes in description
    desc = desc.replace('"', '\\"')

    # Insert description after the tags block (or at end of front matter)
    new_fm = fm + f'\ndescription: "{desc}"'

    new_content = f"---\n{new_fm}\n---\n{body}"
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True


def main() -> None:
    """Add descriptions to all posts."""
    modified = 0
    for fname in sorted(os.listdir(POSTS_DIR)):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(POSTS_DIR, fname)
        if process_post(fpath, fname):
            modified += 1
            print(f"  [DONE] {fname}")

    print(f"\nModified {modified} files.")


if __name__ == "__main__":
    main()
