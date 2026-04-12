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
    assert ".conversus/deliberations/" in str(result)


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
    config = project_root / "conversus.yml"
    config.write_text("mode: cooperative\nagents: []")

    result = persist_deliberation(
        source_dir=fake_output,
        project_root=project_root,
        question="Test",
        config_path=config,
    )
    assert (result / "conversus.yml").exists()
    assert "cooperative" in (result / "conversus.yml").read_text()


def test_persist_creates_deliberations_dir_lazily(fake_output, project_root):
    """The .conversus/deliberations/ directory is created on first persist."""
    assert not (project_root / ".conversus").exists()
    persist_deliberation(
        source_dir=fake_output,
        project_root=project_root,
        question="Test",
    )
    assert (project_root / ".conversus" / "deliberations").exists()


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
