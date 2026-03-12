#!/usr/bin/env python3
"""
Review Queue Tool with SM-2 Spaced Repetition Algorithm

Tracks blog posts for spaced review using the SM-2 algorithm.
Stores review state in data/review_state.json.

Commands:
  init                    Scan posts and initialize review queue
  show                    List posts due for review
  mark <slug> <rating>    Record review with rating 0-5
  stats                   Show review statistics
"""

import argparse
import hashlib
import json
import re
from datetime import datetime, timedelta
from pathlib import Path


class ReviewQueue:
    """Manages spaced repetition review queue for blog posts."""

    def __init__(self, posts_dir: str, state_file: str):
        self.posts_dir = Path(posts_dir)
        self.state_file = Path(state_file)
        self.state: dict[str, dict] = {}

    def load_state(self) -> None:
        """Load review state from JSON file."""
        if self.state_file.exists():
            with open(self.state_file, encoding="utf-8") as f:
                self.state = json.load(f)
        else:
            self.state = {}

    def save_state(self) -> None:
        """Save review state to JSON file."""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)

    def _extract_post_body(self, content: str) -> str:
        """Extract post body (content after front matter)."""
        # Match YAML front matter (--- ... ---)
        match = re.match(r'^---\s*\n.*?\n---\s*\n', content, re.DOTALL)
        if match:
            return content[match.end():]
        return content

    def _compute_content_hash(self, post_path: Path) -> str:
        """Compute MD5 hash of post body content."""
        with open(post_path, encoding="utf-8") as f:
            content = f.read()
        body = self._extract_post_body(content)
        return hashlib.md5(body.encode("utf-8")).hexdigest()

    def _get_post_slug(self, post_path: Path) -> str:
        """Extract slug from post filename (remove .md extension)."""
        return post_path.stem

    def _scan_posts(self) -> list[Path]:
        """Scan source/_posts/ for all .md files."""
        if not self.posts_dir.exists():
            return []
        return sorted(self.posts_dir.glob("*.md"))

    def _sm2_update(
        self,
        quality: int,
        repetitions: int,
        interval: int,
        easiness: float
    ) -> tuple[int, int, float]:
        """
        SM-2 algorithm for spaced repetition.

        Args:
            quality: Quality of recall (0-5)
            repetitions: Number of successful reviews
            interval: Current interval in days
            easiness: Easiness factor (EF)

        Returns:
            (new_repetitions, new_interval, new_easiness)
        """
        # Update easiness factor
        new_easiness = easiness + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        new_easiness = max(1.3, new_easiness)  # Minimum EF is 1.3

        if quality < 3:
            # Failed recall: reset
            new_repetitions = 0
            new_interval = 1
        else:
            # Successful recall
            new_repetitions = repetitions + 1
            if new_repetitions == 1:
                new_interval = 1
            elif new_repetitions == 2:
                new_interval = 6
            else:
                new_interval = int(interval * new_easiness)

        return new_repetitions, new_interval, new_easiness

    def init(self) -> None:
        """Initialize review queue by scanning all posts."""
        self.load_state()
        posts = self._scan_posts()

        if not posts:
            print(f"No posts found in {self.posts_dir}")
            return

        today = datetime.now().strftime("%Y-%m-%d")
        new_posts = 0
        updated_posts = 0

        for post_path in posts:
            slug = self._get_post_slug(post_path)
            content_hash = self._compute_content_hash(post_path)

            if slug not in self.state:
                # New post: initialize with default values
                self.state[slug] = {
                    "last_reviewed": None,
                    "interval": 0,
                    "easiness": 2.5,
                    "repetitions": 0,
                    "next_due": today,
                    "content_hash": content_hash
                }
                new_posts += 1
            else:
                # Existing post: update hash if needed
                if self.state[slug]["content_hash"] != content_hash:
                    # Content changed: reset review schedule
                    self.state[slug].update({
                        "interval": 0,
                        "repetitions": 0,
                        "next_due": today,
                        "content_hash": content_hash
                    })
                    updated_posts += 1
                else:
                    # Hash unchanged: keep existing state
                    pass

        self.save_state()
        print("Initialized review queue:")
        print(f"  New posts: {new_posts}")
        print(f"  Updated posts: {updated_posts}")
        print(f"  Total posts: {len(self.state)}")

    def show(self) -> None:
        """Show posts due for review."""
        self.load_state()
        today = datetime.now().strftime("%Y-%m-%d")

        due_posts = []
        for slug, data in self.state.items():
            next_due = data.get("next_due")
            if next_due and next_due <= today:
                content_hash_current = self._compute_content_hash(
                    self.posts_dir / f"{slug}.md"
                )
                content_changed = content_hash_current != data["content_hash"]

                due_posts.append({
                    "slug": slug,
                    "next_due": next_due,
                    "interval": data["interval"],
                    "repetitions": data["repetitions"],
                    "content_changed": content_changed
                })

        if not due_posts:
            print("No posts due for review today.")
            return

        # Sort by due date (oldest first)
        due_posts.sort(key=lambda x: x["next_due"])

        print(f"Posts due for review ({len(due_posts)}):\n")
        for post in due_posts:
            flag = " [CONTENT CHANGED]" if post["content_changed"] else ""
            print(f"  {post['slug']}")
            print(f"    Due: {post['next_due']} | "
                  f"Interval: {post['interval']}d | "
                  f"Reps: {post['repetitions']}{flag}")
            print()

    def mark(self, slug: str, quality: int) -> None:
        """Mark a post as reviewed with quality rating."""
        self.load_state()

        if slug not in self.state:
            print(f"Error: Post '{slug}' not found in review queue.")
            print("Run 'init' command first.")
            return

        if not 0 <= quality <= 5:
            print(f"Error: Quality must be 0-5, got {quality}")
            return

        post_path = self.posts_dir / f"{slug}.md"
        if not post_path.exists():
            print(f"Error: Post file not found: {post_path}")
            return

        # Update content hash
        new_hash = self._compute_content_hash(post_path)
        old_hash = self.state[slug]["content_hash"]

        if new_hash != old_hash:
            print("Note: Content has changed since last review. Resetting schedule.")
            # Reset to initial state before applying rating
            self.state[slug].update({
                "interval": 0,
                "repetitions": 0,
                "easiness": 2.5,
                "content_hash": new_hash
            })

        # Apply SM-2 algorithm
        data = self.state[slug]
        new_reps, new_interval, new_easiness = self._sm2_update(
            quality=quality,
            repetitions=data["repetitions"],
            interval=data["interval"],
            easiness=data["easiness"]
        )

        # Calculate next due date
        today = datetime.now()
        next_due = (today + timedelta(days=new_interval)).strftime("%Y-%m-%d")

        # Update state
        self.state[slug].update({
            "last_reviewed": today.strftime("%Y-%m-%d"),
            "interval": new_interval,
            "easiness": round(new_easiness, 2),
            "repetitions": new_reps,
            "next_due": next_due,
            "content_hash": new_hash
        })

        self.save_state()

        print(f"Reviewed: {slug}")
        print(f"  Quality: {quality}/5")
        print(f"  New interval: {new_interval} days")
        print(f"  Next due: {next_due}")
        print(f"  Repetitions: {new_reps}")
        print(f"  Easiness: {new_easiness:.2f}")

    def stats(self) -> None:
        """Show review statistics."""
        self.load_state()

        if not self.state:
            print("No posts in review queue. Run 'init' command first.")
            return

        today = datetime.now().strftime("%Y-%m-%d")

        total = len(self.state)
        due_today = sum(1 for data in self.state.values()
                       if data.get("next_due", "") <= today)
        reviewed = sum(1 for data in self.state.values()
                      if data.get("last_reviewed") is not None)
        never_reviewed = total - reviewed

        # Calculate average interval
        intervals = [data["interval"] for data in self.state.values()
                    if data["interval"] > 0]
        avg_interval = sum(intervals) / len(intervals) if intervals else 0

        print("Review Queue Statistics:")
        print(f"  Total posts: {total}")
        print(f"  Due today: {due_today}")
        print(f"  Reviewed at least once: {reviewed}")
        print(f"  Never reviewed: {never_reviewed}")
        print(f"  Average interval: {avg_interval:.1f} days")

        # Distribution by interval
        if intervals:
            print("\nInterval distribution:")
            for days in [1, 6, 14, 30, 90]:
                count = sum(1 for i in intervals if i >= days)
                print(f"    >= {days} days: {count}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Review Queue Tool with SM-2 Spaced Repetition",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # init command
    subparsers.add_parser("init", help="Scan posts and initialize review queue")

    # show command
    subparsers.add_parser("show", help="List posts due for review")

    # mark command
    mark_parser = subparsers.add_parser("mark", help="Record review with rating")
    mark_parser.add_argument("slug", help="Post slug (filename without .md)")
    mark_parser.add_argument("quality", type=int, choices=range(6),
                            help="Quality rating (0-5)")

    # stats command
    subparsers.add_parser("stats", help="Show review statistics")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Default paths (relative to script location)
    script_dir = Path(__file__).parent.parent
    posts_dir = script_dir / "source" / "_posts"
    state_file = script_dir / "data" / "review_state.json"

    queue = ReviewQueue(str(posts_dir), str(state_file))

    if args.command == "init":
        queue.init()
    elif args.command == "show":
        queue.show()
    elif args.command == "mark":
        queue.mark(args.slug, args.quality)
    elif args.command == "stats":
        queue.stats()


if __name__ == "__main__":
    main()
