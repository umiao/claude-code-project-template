#!/usr/bin/env python3
"""
Anki Export Tool

Reads key_concepts and takeaways from all blog post front matter,
generates an Anki-compatible CSV file for flashcard import.

Card types generated:
  1. Concept cards: Front = "What is <concept>?" / Back = takeaways from that post
  2. Takeaway cards: Front = takeaway as question / Back = post title + context

Output: data/anki_export.csv
Usage: python tools/export_anki.py [--posts-dir source/_posts] [--output data/anki_export.csv]
"""

import argparse
import csv
import re
import sys
from pathlib import Path


def parse_front_matter(filepath: Path) -> dict[str, object]:
    """Parse YAML front matter from a markdown file.

    Returns dict with title, key_concepts, takeaways, tags, series fields.
    """
    text = filepath.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}

    fm_text = match.group(1)
    result: dict[str, object] = {}

    # Extract title
    title_match = re.search(r"^title:\s*(.+)$", fm_text, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip().strip("\"'")
        result["title"] = title

    # Extract series
    series_match = re.search(r"^series:\s*(.+)$", fm_text, re.MULTILINE)
    if series_match:
        val = series_match.group(1).strip()
        if val and val != "null":
            result["series"] = val

    # Extract key_concepts (YAML list)
    result["key_concepts"] = _extract_yaml_list(fm_text, "key_concepts")

    # Extract takeaways (YAML list)
    result["takeaways"] = _extract_yaml_list(fm_text, "takeaways")

    # Extract tags (YAML list)
    result["tags"] = _extract_yaml_list(fm_text, "tags")

    return result


def _extract_yaml_list(text: str, field: str) -> list[str]:
    """Extract a YAML list field from front matter text."""
    pattern = rf"^{field}:\s*\n((?:\s+-\s+.+\n?)*)"
    match = re.search(pattern, text, re.MULTILINE)
    if not match:
        return []
    items = re.findall(r"^\s+-\s+(.+)$", match.group(1), re.MULTILINE)
    return [item.strip().strip("\"'") for item in items if item.strip()]


def generate_cards(posts_dir: Path) -> list[dict[str, str]]:
    """Generate Anki flashcards from all posts with key_concepts."""
    cards: list[dict[str, str]] = []
    post_files = sorted(posts_dir.glob("*.md"))
    posts_with_concepts = 0

    for filepath in post_files:
        fm = parse_front_matter(filepath)
        if not fm.get("key_concepts"):
            continue

        posts_with_concepts += 1
        title = fm.get("title", filepath.stem)
        series = fm.get("series", "")
        concepts = fm["key_concepts"]
        takeaways = fm.get("takeaways", [])
        tags_list = fm.get("tags", [])
        tag_str = ", ".join(tags_list) if tags_list else ""
        series_tag = series if series else ""

        # Card type 1: Concept definition cards
        # Front: "What is <concept>?" Back: related takeaways from the post
        for concept in concepts:
            relevant_takeaways = _find_relevant_takeaways(concept, takeaways)
            if not relevant_takeaways:
                # Use all takeaways if none specifically match
                relevant_takeaways = takeaways[:3] if takeaways else []

            if relevant_takeaways:
                back = "<br>".join(
                    f"- {t}" for t in relevant_takeaways
                )
                back += f"<br><br><i>Source: {title}</i>"
                cards.append({
                    "front": f"What is {concept}?",
                    "back": back,
                    "tags": _build_tags(series_tag, tag_str, "concept"),
                })

        # Card type 2: Takeaway recall cards
        # Front: takeaway phrased as question, Back: full takeaway + source
        for takeaway in takeaways:
            question = _takeaway_to_question(takeaway)
            back = (
                f"{takeaway}"
                f"<br><br><i>Source: {title}</i>"
            )
            cards.append({
                "front": question,
                "back": back,
                "tags": _build_tags(series_tag, tag_str, "takeaway"),
            })

    print(f"Processed {len(post_files)} posts, "
          f"{posts_with_concepts} with key_concepts, "
          f"{len(cards)} cards generated.")
    return cards


def _find_relevant_takeaways(
    concept: str, takeaways: list[str]
) -> list[str]:
    """Find takeaways that mention the given concept."""
    concept_lower = concept.lower()
    words = concept_lower.split()
    relevant = []
    for t in takeaways:
        t_lower = t.lower()
        if concept_lower in t_lower or any(w in t_lower for w in words if len(w) > 3):
            relevant.append(t)
    return relevant[:3]


def _takeaway_to_question(takeaway: str) -> str:
    """Convert a takeaway statement into a recall question."""
    # Simple heuristic: wrap as "True or false?" or "Explain:"
    if len(takeaway) < 80:
        return f"Explain: {takeaway}"
    return f"What do you know about: {takeaway[:80]}...?"


def _build_tags(series: str, tags: str, card_type: str) -> str:
    """Build Anki tag string from components."""
    parts = [card_type]
    if series:
        parts.append(series.replace(" ", "_"))
    if tags:
        for t in tags.split(", "):
            cleaned = t.strip().replace(" ", "_")
            if cleaned:
                parts.append(cleaned)
    return " ".join(parts)


def write_csv(cards: list[dict[str, str]], output_path: Path) -> None:
    """Write cards to Anki-compatible CSV.

    Anki CSV format: front, back, tags (tab-separated, no header by default).
    Using semicolon separator for compatibility since content may contain tabs.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t", quoting=csv.QUOTE_ALL)
        for card in cards:
            writer.writerow([card["front"], card["back"], card["tags"]])
    print(f"Written {len(cards)} cards to {output_path}")


def main() -> None:
    """Entry point for Anki export tool."""
    parser = argparse.ArgumentParser(
        description="Export blog post concepts and takeaways to Anki CSV"
    )
    parser.add_argument(
        "--posts-dir",
        default="source/_posts",
        help="Path to blog posts directory (default: source/_posts)",
    )
    parser.add_argument(
        "--output",
        default="data/anki_export.csv",
        help="Output CSV file path (default: data/anki_export.csv)",
    )
    args = parser.parse_args()

    posts_dir = Path(args.posts_dir)
    if not posts_dir.is_dir():
        print(f"Error: Posts directory not found: {posts_dir}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output)
    cards = generate_cards(posts_dir)

    if not cards:
        print("No cards generated. Check that posts have key_concepts front matter.",
              file=sys.stderr)
        sys.exit(1)

    write_csv(cards, output_path)


if __name__ == "__main__":
    main()
