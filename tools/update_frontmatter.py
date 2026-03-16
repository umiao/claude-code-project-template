"""Batch add/update front matter fields across Hexo blog posts.

Usage examples:
    # Dry-run: show what would change
    python tools/update_frontmatter.py --set "series: DDIA" --filter "title~=DDIA" --dry-run

    # Add a field to all posts (skip if already present)
    python tools/update_frontmatter.py --add "comments: true"

    # Update a field on all posts (overwrite existing)
    python tools/update_frontmatter.py --set "toc: true"

    # Filter by category, tag, or title pattern
    python tools/update_frontmatter.py --set "series: SQL" --filter "categories~=SQL"
    python tools/update_frontmatter.py --set "series: DS" --filter "tags~=Data Science"
    python tools/update_frontmatter.py --set "featured: true" --filter "title~=Note 1"

    # Remove a field from all posts
    python tools/update_frontmatter.py --remove "series" --filter "title~=DDIA"

    # Multiple operations at once
    python tools/update_frontmatter.py --set "toc: true" --add "comments: true" --remove "old_field"
"""

from __future__ import annotations

import argparse
import os
import re
import sys

POSTS_DIR = "source/_posts"


def parse_front_matter(content: str) -> tuple[str | None, str | None]:
    """Split content into front matter and body.

    Returns (front_matter, body) or (None, None) if no front matter found.
    """
    m = re.match(r"^---\n(.*?)\n---\n(.*)", content, re.DOTALL)
    if not m:
        return None, None
    return m.group(1), m.group(2)


def get_fm_value(front_matter: str, key: str) -> str | None:
    """Get a scalar value from front matter by key."""
    m = re.search(rf"^{re.escape(key)}:\s*(.*)$", front_matter, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return None


def get_fm_list_values(front_matter: str, key: str) -> list[str]:
    """Get list values from a YAML list field (e.g., categories, tags)."""
    # Match the key line and subsequent list items (with or without leading spaces)
    pattern = rf"^{re.escape(key)}:\s*\n((?:[ \t]*-\s+.*\n?)*)"
    m = re.search(pattern, front_matter, re.MULTILINE)
    if not m:
        # Try inline value
        scalar = get_fm_value(front_matter, key)
        return [scalar] if scalar else []
    items = re.findall(r"^[ \t]*-\s+(.+)$", m.group(1), re.MULTILINE)
    return [item.strip() for item in items]


def matches_filter(front_matter: str, filter_expr: str) -> bool:
    """Check if front matter matches a filter expression.

    Supported formats:
        key~=pattern   -- regex search on value (case-insensitive)
        key=value      -- exact match
        key!=value     -- not equal
    """
    # Regex match
    m = re.match(r"^(\w+)~=(.+)$", filter_expr)
    if m:
        key, pattern = m.group(1), m.group(2)
        # Check scalar value
        scalar = get_fm_value(front_matter, key)
        if scalar and re.search(pattern, scalar, re.IGNORECASE):
            return True
        # Check list values
        for val in get_fm_list_values(front_matter, key):
            if re.search(pattern, val, re.IGNORECASE):
                return True
        return False

    # Not-equal match
    m = re.match(r"^(\w+)!=(.+)$", filter_expr)
    if m:
        key, value = m.group(1), m.group(2)
        actual = get_fm_value(front_matter, key)
        return actual != value

    # Exact match
    m = re.match(r"^(\w+)=(.+)$", filter_expr)
    if m:
        key, value = m.group(1), m.group(2)
        actual = get_fm_value(front_matter, key)
        if actual == value:
            return True
        return value in get_fm_list_values(front_matter, key)

    print(f"  [WARN] Invalid filter syntax: {filter_expr}", file=sys.stderr)
    return False


def parse_key_value(expr: str) -> tuple[str, str]:
    """Parse 'key: value' or 'key:value' into (key, value)."""
    m = re.match(r"^(\w+):\s*(.+)$", expr)
    if not m:
        print(f"  [FAIL] Invalid key-value: {expr}", file=sys.stderr)
        sys.exit(1)
    return m.group(1), m.group(2)


def set_fm_field(front_matter: str, key: str, value: str) -> str:
    """Set a front matter field, overwriting if it exists."""
    pattern = rf"^{re.escape(key)}:.*$"
    if re.search(pattern, front_matter, re.MULTILINE):
        return re.sub(pattern, f"{key}: {value}", front_matter, flags=re.MULTILINE)
    return front_matter + f"\n{key}: {value}"


def add_fm_field(front_matter: str, key: str, value: str) -> str:
    """Add a front matter field only if it doesn't already exist."""
    if re.search(rf"^{re.escape(key)}:", front_matter, re.MULTILINE):
        return front_matter  # Already exists, skip
    return front_matter + f"\n{key}: {value}"


def remove_fm_field(front_matter: str, key: str) -> str:
    """Remove a front matter field (scalar or list)."""
    # Remove list field (key + indented items)
    pattern = rf"^{re.escape(key)}:\s*\n(?:\s+-\s+.*\n?)*"
    result = re.sub(pattern, "", front_matter, flags=re.MULTILINE)
    if result != front_matter:
        return result.rstrip("\n")
    # Remove scalar field
    pattern = rf"^{re.escape(key)}:.*\n?"
    result = re.sub(pattern, "", front_matter, flags=re.MULTILINE)
    return result.rstrip("\n")


def process_file(
    fpath: str,
    fname: str,
    *,
    set_ops: list[tuple[str, str]],
    add_ops: list[tuple[str, str]],
    remove_ops: list[str],
    filters: list[str],
    dry_run: bool,
) -> bool:
    """Process a single file. Returns True if modified."""
    with open(fpath, encoding="utf-8") as f:
        content = f.read()

    fm, body = parse_front_matter(content)
    if fm is None or body is None:
        return False

    # Check filters
    for filt in filters:
        if not matches_filter(fm, filt):
            return False

    new_fm = fm

    for key, value in set_ops:
        new_fm = set_fm_field(new_fm, key, value)

    for key, value in add_ops:
        new_fm = add_fm_field(new_fm, key, value)

    for key in remove_ops:
        new_fm = remove_fm_field(new_fm, key)

    if new_fm == fm:
        return False

    if dry_run:
        print(f"  [DRY-RUN] {fname}")
        # Show what changed
        old_lines = set(fm.split("\n"))
        new_lines = set(new_fm.split("\n"))
        for line in new_lines - old_lines:
            print(f"    + {line}")
        for line in old_lines - new_lines:
            print(f"    - {line}")
        return True

    new_content = f"---\n{new_fm}\n---\n{body}"
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"  [DONE] {fname}")
    return True


def main() -> None:
    """Run batch front matter updates."""
    parser = argparse.ArgumentParser(
        description="Batch update front matter fields in Hexo posts.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--set",
        action="append",
        default=[],
        metavar="KEY:VALUE",
        help="Set field (overwrite if exists). E.g., --set 'toc: true'",
    )
    parser.add_argument(
        "--add",
        action="append",
        default=[],
        metavar="KEY:VALUE",
        help="Add field (skip if exists). E.g., --add 'comments: true'",
    )
    parser.add_argument(
        "--remove",
        action="append",
        default=[],
        metavar="KEY",
        help="Remove field. E.g., --remove old_field",
    )
    parser.add_argument(
        "--filter",
        action="append",
        default=[],
        metavar="EXPR",
        help="Filter posts. Formats: key~=regex, key=value, key!=value",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would change without modifying files",
    )
    parser.add_argument(
        "--posts-dir",
        default=POSTS_DIR,
        help=f"Posts directory (default: {POSTS_DIR})",
    )

    args = parser.parse_args()

    if not args.set and not args.add and not args.remove:
        parser.error("At least one of --set, --add, or --remove is required")

    set_ops = [parse_key_value(s) for s in args.set]
    add_ops = [parse_key_value(a) for a in args.add]
    remove_ops = args.remove

    if not os.path.isdir(args.posts_dir):
        print(f"[FAIL] Posts directory not found: {args.posts_dir}", file=sys.stderr)
        sys.exit(1)

    modified = 0
    total = 0
    for fname in sorted(os.listdir(args.posts_dir)):
        if not fname.endswith(".md"):
            continue
        total += 1
        fpath = os.path.join(args.posts_dir, fname)
        if process_file(
            fpath,
            fname,
            set_ops=set_ops,
            add_ops=add_ops,
            remove_ops=remove_ops,
            filters=args.filter,
            dry_run=args.dry_run,
        ):
            modified += 1

    action = "Would modify" if args.dry_run else "Modified"
    print(f"\n{action} {modified}/{total} files.")


if __name__ == "__main__":
    main()
