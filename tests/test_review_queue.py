"""Tests for review_queue.py tool."""

import json
from pathlib import Path

import pytest


@pytest.fixture
def temp_blog_structure(tmp_path):
    """Create a temporary blog directory structure for testing."""
    posts_dir = tmp_path / "source" / "_posts"
    posts_dir.mkdir(parents=True)
    data_dir = tmp_path / "data"
    data_dir.mkdir(parents=True)

    # Create sample posts
    post1_content = """---
title: Test Post 1
date: 2022-01-01
categories:
  - Test
tags:
  - Testing
---

This is the content of test post 1.
Some more content here.
"""
    post2_content = """---
title: Test Post 2
date: 2022-01-02
---

Different content for post 2.
"""
    (posts_dir / "test-post-1.md").write_text(post1_content, encoding="utf-8")
    (posts_dir / "test-post-2.md").write_text(post2_content, encoding="utf-8")

    return tmp_path, posts_dir, data_dir


def test_review_queue_exists():
    """Test that review_queue.py exists."""
    script_path = Path(__file__).parent.parent / "tools" / "review_queue.py"
    assert script_path.exists(), "review_queue.py not found"


def test_review_queue_imports():
    """Test that review_queue.py can be imported without errors."""
    import sys
    script_dir = Path(__file__).parent.parent / "tools"
    sys.path.insert(0, str(script_dir))

    try:
        import review_queue
        assert hasattr(review_queue, "ReviewQueue")
        assert hasattr(review_queue, "main")
    finally:
        sys.path.pop(0)


def test_review_queue_init(temp_blog_structure):
    """Test init command scans posts and creates state file."""
    import sys
    script_dir = Path(__file__).parent.parent / "tools"
    sys.path.insert(0, str(script_dir))

    try:
        from review_queue import ReviewQueue

        tmp_path, posts_dir, data_dir = temp_blog_structure
        state_file = data_dir / "review_state.json"

        queue = ReviewQueue(str(posts_dir), str(state_file))
        queue.init()

        # Verify state file was created
        assert state_file.exists()

        # Verify state file contains both posts
        with open(state_file, encoding="utf-8") as f:
            state = json.load(f)

        assert len(state) == 2
        assert "test-post-1" in state
        assert "test-post-2" in state

        # Verify required fields
        for _slug, data in state.items():
            assert "last_reviewed" in data
            assert "interval" in data
            assert "easiness" in data
            assert "repetitions" in data
            assert "next_due" in data
            assert "content_hash" in data

            # Initial values
            assert data["last_reviewed"] is None
            assert data["interval"] == 0
            assert data["easiness"] == 2.5
            assert data["repetitions"] == 0
            assert data["content_hash"] != ""
    finally:
        sys.path.pop(0)


def test_review_queue_content_hash(temp_blog_structure):
    """Test content hash detection."""
    import sys
    script_dir = Path(__file__).parent.parent / "tools"
    sys.path.insert(0, str(script_dir))

    try:
        from review_queue import ReviewQueue

        tmp_path, posts_dir, data_dir = temp_blog_structure
        state_file = data_dir / "review_state.json"

        queue = ReviewQueue(str(posts_dir), str(state_file))
        queue.init()

        # Get initial hash
        with open(state_file, encoding="utf-8") as f:
            initial_state = json.load(f)
        initial_hash = initial_state["test-post-1"]["content_hash"]

        # Modify post content
        post_file = posts_dir / "test-post-1.md"
        original_content = post_file.read_text(encoding="utf-8")
        modified_content = original_content + "\nNew content added."
        post_file.write_text(modified_content, encoding="utf-8")

        # Re-init and verify hash changed
        queue.init()
        with open(state_file, encoding="utf-8") as f:
            new_state = json.load(f)
        new_hash = new_state["test-post-1"]["content_hash"]

        assert new_hash != initial_hash
        # Schedule should be reset
        assert new_state["test-post-1"]["interval"] == 0
        assert new_state["test-post-1"]["repetitions"] == 0
    finally:
        sys.path.pop(0)


def test_review_queue_sm2_algorithm(temp_blog_structure):
    """Test SM-2 algorithm updates intervals correctly."""
    import sys
    script_dir = Path(__file__).parent.parent / "tools"
    sys.path.insert(0, str(script_dir))

    try:
        from review_queue import ReviewQueue

        tmp_path, posts_dir, data_dir = temp_blog_structure
        state_file = data_dir / "review_state.json"

        queue = ReviewQueue(str(posts_dir), str(state_file))
        queue.init()

        # First review (quality 4)
        queue.mark("test-post-1", 4)
        queue.load_state()
        assert queue.state["test-post-1"]["interval"] == 1
        assert queue.state["test-post-1"]["repetitions"] == 1

        # Second review (quality 4)
        queue.mark("test-post-1", 4)
        queue.load_state()
        assert queue.state["test-post-1"]["interval"] == 6
        assert queue.state["test-post-1"]["repetitions"] == 2

        # Third review (quality 5)
        queue.mark("test-post-1", 5)
        queue.load_state()
        # Should be 6 * easiness (which should be > 2.5)
        assert queue.state["test-post-1"]["interval"] > 6
        assert queue.state["test-post-1"]["repetitions"] == 3

        # Test failed review (quality < 3)
        queue.mark("test-post-1", 2)
        queue.load_state()
        assert queue.state["test-post-1"]["interval"] == 1
        assert queue.state["test-post-1"]["repetitions"] == 0  # Reset
    finally:
        sys.path.pop(0)


def test_review_queue_encoding():
    """Test that all file I/O uses utf-8 encoding."""
    script_path = Path(__file__).parent.parent / "tools" / "review_queue.py"
    content = script_path.read_text(encoding="utf-8")

    # Check that all file operations specify encoding="utf-8"
    assert 'encoding="utf-8"' in content
    # Count occurrences - should be in multiple file operations
    # (load_state, save_state, _compute_content_hash)
    count = content.count('encoding="utf-8"')
    assert count >= 3, f"Expected at least 3 utf-8 encoding declarations, found {count}"


def test_state_file_structure():
    """Test that the actual review_state.json has correct structure."""
    state_file = Path(__file__).parent.parent / "data" / "review_state.json"

    # Only test if file exists (init may not have been run yet)
    if not state_file.exists():
        pytest.skip("review_state.json not yet created")

    with open(state_file, encoding="utf-8") as f:
        state = json.load(f)

    # Verify structure for at least one post
    if len(state) > 0:
        first_post = next(iter(state.values()))
        required_fields = ["last_reviewed", "interval", "easiness",
                          "repetitions", "next_due", "content_hash"]
        for field in required_fields:
            assert field in first_post, f"Missing required field: {field}"
