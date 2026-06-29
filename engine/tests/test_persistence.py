"""Tests for the deliberation persistence module (spec 056).

Covers: persist_deliberation, cleanup, list, read, slug/timestamp
generation, and path traversal security.
"""

from __future__ import annotations

import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from engine.persistence import (
    _make_slug,
    _make_timestamp,
    cleanup_old_deliberations,
    list_deliberations,
    persist_deliberation,
    read_deliberation_file,
)


# ---------------------------------------------------------------------------
# Slug generation
# ---------------------------------------------------------------------------


def test_make_slug_basic():
    assert _make_slug("Should we use Postgres?") == "should-we-use-postgres"


def test_make_slug_special_chars():
    assert _make_slug("LLC vs S-Corp: what's best?") == "llc-vs-s-corp-what-s-best"


def test_make_slug_truncation():
    long = "a" * 100
    assert len(_make_slug(long, max_len=40)) == 40


def test_make_slug_empty():
    assert _make_slug("") == ""


def test_make_slug_only_special_chars():
    assert _make_slug("!@#$%^&*()") == ""


# ---------------------------------------------------------------------------
# Timestamp
# ---------------------------------------------------------------------------


def test_make_timestamp_format():
    ts = _make_timestamp()
    # Should be YYYYMMDDTHHMMSS
    assert len(ts) == 15
    assert ts[8] == "T"
    # Should parse back
    datetime.strptime(ts, "%Y%m%dT%H%M%S")


# ---------------------------------------------------------------------------
# Persist deliberation
# ---------------------------------------------------------------------------


@pytest.fixture
def fake_output(tmp_path: Path) -> Path:
    """Create a fake deliberation output tree."""
    output = tmp_path / "output"
    (output / "pragmatist").mkdir(parents=True)
    (output / "devils-advocate" / "cross-reviews").mkdir(parents=True)
    (output / "summary").mkdir(parents=True)
    (output / "pragmatist" / "review.md").write_text("Pragmatist review")
    (output / "devils-advocate" / "review.md").write_text("DA review")
    (output / "devils-advocate" / "cross-reviews" / "pragmatist.md").write_text("Cross-review")
    (output / "summary" / "final.md").write_text("# Synthesis\nThe verdict is...")
    return output


@pytest.fixture
def project_root(tmp_path: Path) -> Path:
    """A temp project root for persistence tests."""
    root = tmp_path / "project"
    root.mkdir()
    return root


def test_persist_creates_deliberation_directory(fake_output, project_root):
    result = persist_deliberation(
        source_dir=fake_output,
        project_root=project_root,
        question="Should we use Postgres?",
    )
    assert result.exists()
    assert result.is_dir()
    assert ".deliberator/deliberations/" in str(result)


def test_persist_copies_output_tree(fake_output, project_root):
    result = persist_deliberation(
        source_dir=fake_output,
        project_root=project_root,
        question="Test question",
    )
    # Check key files were copied
    assert (result / "output" / "summary" / "final.md").exists()
    assert (result / "output" / "pragmatist" / "review.md").exists()
    assert (result / "output" / "devils-advocate" / "cross-reviews" / "pragmatist.md").exists()


def test_persist_creates_question_md(fake_output, project_root):
    result = persist_deliberation(
        source_dir=fake_output,
        project_root=project_root,
        question="Should we use Postgres?",
    )
    question_file = result / "question.md"
    assert question_file.exists()
    assert "Postgres" in question_file.read_text()


def test_persist_copies_config_when_provided(fake_output, project_root):
    config = project_root / "deliberator.yml"
    config.write_text("mode: cooperative\nagents: []")

    result = persist_deliberation(
        source_dir=fake_output,
        project_root=project_root,
        question="Test",
        config_path=config,
    )
    assert (result / "deliberator.yml").exists()
    assert "cooperative" in (result / "deliberator.yml").read_text()


def test_persist_creates_deliberations_dir_lazily(fake_output, project_root):
    """The .deliberator/deliberations/ directory is created on first persist."""
    assert not (project_root / ".deliberator").exists()
    persist_deliberation(
        source_dir=fake_output,
        project_root=project_root,
        question="Test",
    )
    assert (project_root / ".deliberator" / "deliberations").exists()


# ---------------------------------------------------------------------------
# Cleanup
# ---------------------------------------------------------------------------


def test_cleanup_removes_old_deliberations(fake_output, project_root):
    # Create a deliberation
    result = persist_deliberation(
        source_dir=fake_output,
        project_root=project_root,
        question="Old deliberation",
    )

    # Rename to simulate an old timestamp (91 days ago)
    old_ts = (datetime.now(timezone.utc) - timedelta(days=91)).strftime("%Y%m%dT%H%M%S")
    old_name = f"{old_ts}-old-deliberation"
    old_path = result.parent / old_name
    result.rename(old_path)

    deleted = cleanup_old_deliberations(project_root, retention_days=90)
    assert deleted == 1
    assert not old_path.exists()


def test_cleanup_preserves_recent_deliberations(fake_output, project_root):
    result = persist_deliberation(
        source_dir=fake_output,
        project_root=project_root,
        question="Recent deliberation",
    )
    deleted = cleanup_old_deliberations(project_root, retention_days=90)
    assert deleted == 0
    assert result.exists()


# ---------------------------------------------------------------------------
# List deliberations
# ---------------------------------------------------------------------------


def test_list_returns_empty_when_no_deliberations(project_root):
    result = list_deliberations(project_root)
    assert result == []


def test_list_returns_deliberation_metadata(fake_output, project_root):
    persist_deliberation(
        source_dir=fake_output,
        project_root=project_root,
        question="Timber vs conventional framing",
    )

    result = list_deliberations(project_root)
    assert len(result) == 1
    d = result[0]
    assert "timber" in d.get("question", "").lower() or "timber" in d.get("path", "").lower()
    assert d.get("has_synthesis") is True


def test_list_sorted_newest_first(fake_output, project_root):
    persist_deliberation(
        source_dir=fake_output,
        project_root=project_root,
        question="First question",
    )
    time.sleep(1.1)  # ensure different timestamp
    persist_deliberation(
        source_dir=fake_output,
        project_root=project_root,
        question="Second question",
    )

    result = list_deliberations(project_root)
    assert len(result) == 2
    # Newest first
    assert result[0]["path"] > result[1]["path"]  # lexicographic on timestamp prefix


# ---------------------------------------------------------------------------
# Read deliberation file
# ---------------------------------------------------------------------------


def test_read_returns_file_content(fake_output, project_root):
    persisted = persist_deliberation(
        source_dir=fake_output,
        project_root=project_root,
        question="Test",
    )
    rel_delib = str(persisted.relative_to(project_root))

    content = read_deliberation_file(project_root, rel_delib, "output/summary/final.md")
    assert "Synthesis" in content
    assert "verdict" in content


def test_read_rejects_path_traversal(fake_output, project_root):
    persisted = persist_deliberation(
        source_dir=fake_output,
        project_root=project_root,
        question="Test",
    )
    rel_delib = str(persisted.relative_to(project_root))

    with pytest.raises(ValueError, match="[Pp]ath traversal|outside"):
        read_deliberation_file(project_root, rel_delib, "../../../etc/passwd")


def test_read_raises_for_missing_file(fake_output, project_root):
    persisted = persist_deliberation(
        source_dir=fake_output,
        project_root=project_root,
        question="Test",
    )
    rel_delib = str(persisted.relative_to(project_root))

    with pytest.raises(FileNotFoundError):
        read_deliberation_file(project_root, rel_delib, "nonexistent.md")


# ---------------------------------------------------------------------------
# End-to-end round-trip (spec 061 step 14)
# ---------------------------------------------------------------------------
#
# Existing tests cover persist+read and persist+list pairwise. The
# round-trip test below exercises the full user workflow in one chain:
#
#   1. Run deliberation → persist_deliberation
#   2. `deliberator list` → list_deliberations finds the persisted run
#   3. `deliberator show <id>` → read_deliberation_file resolves the id
#      from list and returns the synthesis content
#
# This is the integration boundary spec 061 step 14 calls out under
# "persist→list→show". A bug where, for example, the slug returned by
# persist_deliberation didn't match the id list_deliberations exposes
# would not regress the pairwise tests but would break the actual CLI
# workflow. The chain test pins the slug-as-public-id contract.


@pytest.mark.integration
class TestPersistListShowRoundTrip:
    """Full persist→list→show user-workflow chain."""

    def test_single_deliberation_round_trip(
        self, fake_output, project_root
    ):
        """Persist one run, list finds it, show returns its synthesis."""
        question = "Should we use Postgres for the new pipeline?"

        # Step 1: persist
        persisted = persist_deliberation(
            source_dir=fake_output,
            project_root=project_root,
            question=question,
        )

        # Step 2: list — must surface the just-persisted run
        listing = list_deliberations(project_root)
        assert len(listing) == 1, "list should report exactly one deliberation"

        entry = listing[0]
        assert entry["question"] == question, (
            "list must round-trip the question text verbatim"
        )
        assert entry["path"] == persisted, (
            "list's path must match the path persist returned"
        )
        assert entry["has_synthesis"] is True, (
            "list must reflect that summary/final.md exists"
        )

        # Step 3: show — read the synthesis using the id (path) from list
        rel_delib = str(entry["path"].relative_to(project_root))
        synthesis = read_deliberation_file(
            project_root, rel_delib, "output/summary/final.md"
        )
        assert "Synthesis" in synthesis
        assert "verdict" in synthesis

    def test_multiple_deliberations_round_trip_each(
        self, tmp_path: Path, project_root
    ):
        """N persists, list finds all, show reads each by its own id.

        Pins that the (slug, timestamp) pair is unique enough to give
        each persisted run a distinct, addressable id even when slugs
        collide on the question prefix.
        """
        questions = [
            "Should we use Postgres for the pipeline?",
            "Should we use Postgres for the index?",
            "Should we use SQLite for the demo?",
        ]
        persisted_paths = []

        for i, q in enumerate(questions):
            # Build a fresh fake output per iteration with distinct
            # synthesis content so we can verify show returns the
            # right one.
            output = tmp_path / f"output-{i}"
            (output / "alice").mkdir(parents=True)
            (output / "summary").mkdir(parents=True)
            (output / "alice" / "review.md").write_text(f"Review {i}")
            (output / "summary" / "final.md").write_text(
                f"# Synthesis {i}\nVerdict for question {i}."
            )

            persisted = persist_deliberation(
                source_dir=output,
                project_root=project_root,
                question=q,
            )
            persisted_paths.append(persisted)
            # Stagger timestamps so list ordering is deterministic.
            time.sleep(1.1)

        # Step 2: list returns all 3, newest first
        listing = list_deliberations(project_root)
        assert len(listing) == 3

        # Each list entry's path must match a persist return value
        listed_paths = {entry["path"] for entry in listing}
        assert listed_paths == set(persisted_paths)

        # Step 3: show each by its id, verify each returns its own
        # distinct synthesis content (no cross-contamination)
        for entry in listing:
            rel_delib = str(entry["path"].relative_to(project_root))
            synthesis = read_deliberation_file(
                project_root, rel_delib, "output/summary/final.md"
            )
            # Identify which persist call this came from by question
            expected_index = questions.index(entry["question"])
            assert f"Synthesis {expected_index}" in synthesis
            assert f"question {expected_index}" in synthesis

    def test_list_after_cleanup_excludes_pruned(
        self, fake_output, project_root
    ):
        """Round-trip survives cleanup: pruned runs disappear from list."""
        # Persist a recent run
        recent = persist_deliberation(
            source_dir=fake_output,
            project_root=project_root,
            question="Recent run",
        )

        # Persist an old run (manually backdate the directory mtime
        # via cleanup's age threshold; here we use a stale timestamp
        # in the dir name).
        old = persist_deliberation(
            source_dir=fake_output,
            project_root=project_root,
            question="Old run",
        )

        # Backdate the old run by manipulating the directory name's
        # timestamp prefix so cleanup_old_deliberations treats it as
        # past the retention window.
        old_renamed = old.parent / old.name.replace(
            old.name.split("-")[0], "20200101T000000"
        )
        old.rename(old_renamed)

        # Both should appear before cleanup
        before = list_deliberations(project_root)
        assert len(before) == 2

        cleanup_old_deliberations(project_root, retention_days=30)

        # After cleanup: only recent survives
        after = list_deliberations(project_root)
        assert len(after) == 1
        assert after[0]["path"] == recent
        assert after[0]["question"] == "Recent run"

        # Read still works on the surviving run
        rel = str(after[0]["path"].relative_to(project_root))
        synthesis = read_deliberation_file(
            project_root, rel, "output/summary/final.md"
        )
        assert "Synthesis" in synthesis
