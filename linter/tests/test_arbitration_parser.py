"""Tests for :mod:`linter.arbitration_parser` (spec 006 issue #68).

Covers the canonical contract laid out in the issue:

* typical resolution.md with multiple dispute headings
* empty file → ``[]``
* nonexistent path → ``[]``
* heading level variations (``##``, ``###``, ``####``)
* malformed text (whitespace variations, missing colons)
* duplicate dispute titles preserved in document order
"""

from __future__ import annotations

from pathlib import Path

import pytest

from linter.arbitration_parser import extract_addressed_disputes


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write(tmp_path: Path, name: str, text: str) -> Path:
    """Write *text* to *tmp_path/name* and return the path."""
    p = tmp_path / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# Typical case — three disputes, document order preserved
# ---------------------------------------------------------------------------


class TestTypicalResolution:
    def test_three_disputes_in_document_order(self, tmp_path: Path) -> None:
        path = _write(
            tmp_path,
            "resolution.md",
            "# Arbiter Resolution\n"
            "\n"
            "Some preamble explaining the ruling.\n"
            "\n"
            "## Dispute: Should we use SQL or NoSQL?\n"
            "\n"
            "Ruling: SQL — the consistency requirements demand it.\n"
            "\n"
            "## Dispute: Authentication: JWT vs sessions?\n"
            "\n"
            "Ruling: sessions for this product surface area.\n"
            "\n"
            "## Dispute: Caching layer placement\n"
            "\n"
            "Ruling: in front of the read replicas.\n",
        )

        result = extract_addressed_disputes(path)

        assert result == [
            "Should we use SQL or NoSQL?",
            "Authentication: JWT vs sessions?",
            "Caching layer placement",
        ]


# ---------------------------------------------------------------------------
# Empty / missing files
# ---------------------------------------------------------------------------


class TestEmptyFile:
    def test_empty_file_returns_empty_list(self, tmp_path: Path) -> None:
        path = _write(tmp_path, "resolution.md", "")
        assert extract_addressed_disputes(path) == []

    def test_no_dispute_headings_returns_empty_list(self, tmp_path: Path) -> None:
        path = _write(
            tmp_path,
            "resolution.md",
            "# Arbiter Resolution\n"
            "\n"
            "## Summary\n"
            "\n"
            "All disputes were resolved by agent self-correction; no\n"
            "arbiter ruling was required.\n",
        )
        assert extract_addressed_disputes(path) == []


class TestNonexistentPath:
    def test_nonexistent_path_returns_empty_list(self, tmp_path: Path) -> None:
        path = tmp_path / "does-not-exist.md"
        assert not path.exists()
        assert extract_addressed_disputes(path) == []

    def test_nonexistent_nested_path_returns_empty_list(
        self, tmp_path: Path
    ) -> None:
        # Parent directory also missing; must still not raise.
        path = tmp_path / "missing-dir" / "resolution.md"
        assert extract_addressed_disputes(path) == []


# ---------------------------------------------------------------------------
# Heading-level coverage
# ---------------------------------------------------------------------------


class TestHeadingLevels:
    def test_h2_h3_h4_all_recognised(self, tmp_path: Path) -> None:
        path = _write(
            tmp_path,
            "resolution.md",
            "# Resolution\n"
            "\n"
            "## Dispute: H2-level dispute\n"
            "Body.\n"
            "\n"
            "### Dispute: H3-level dispute\n"
            "Body.\n"
            "\n"
            "#### Dispute: H4-level dispute\n"
            "Body.\n",
        )

        assert extract_addressed_disputes(path) == [
            "H2-level dispute",
            "H3-level dispute",
            "H4-level dispute",
        ]

    def test_h1_is_not_a_dispute_heading(self, tmp_path: Path) -> None:
        # The contract explicitly requires 2-4 leading hashes; ``# Dispute:``
        # at H1 is the document title and must not be picked up.
        path = _write(
            tmp_path,
            "resolution.md",
            "# Dispute: Document title that should not match\n"
            "\n"
            "## Dispute: Real dispute heading\n",
        )
        assert extract_addressed_disputes(path) == [
            "Real dispute heading",
        ]

    def test_h5_is_not_a_dispute_heading(self, tmp_path: Path) -> None:
        # 5 hashes falls outside the [2, 4] range.
        path = _write(
            tmp_path,
            "resolution.md",
            "##### Dispute: Too deep, ignored\n"
            "\n"
            "## Dispute: Recognised\n",
        )
        assert extract_addressed_disputes(path) == ["Recognised"]


# ---------------------------------------------------------------------------
# Malformed input — best-effort parsing, never raises
# ---------------------------------------------------------------------------


class TestMalformedInput:
    def test_whitespace_around_keyword_tolerated(self, tmp_path: Path) -> None:
        # Extra spaces between ``##``, ``Dispute:``, and the title.
        path = _write(
            tmp_path,
            "resolution.md",
            "##   Dispute:    Lots of spaces around the title    \n"
            "\n"
            "###\tDispute:\tTab-separated title\t\n",
        )

        assert extract_addressed_disputes(path) == [
            "Lots of spaces around the title",
            "Tab-separated title",
        ]

    def test_missing_colon_is_ignored(self, tmp_path: Path) -> None:
        # ``## Dispute Without Colon`` is not a dispute heading per the
        # contract (the colon is structurally required).
        path = _write(
            tmp_path,
            "resolution.md",
            "## Dispute Without Colon Should Not Match\n"
            "\n"
            "## Dispute: Real one\n",
        )
        assert extract_addressed_disputes(path) == ["Real one"]

    def test_dispute_keyword_inline_is_not_a_match(self, tmp_path: Path) -> None:
        # The pattern is anchored to the start of the line; inline
        # mentions of ``Dispute:`` in body prose must not match.
        path = _write(
            tmp_path,
            "resolution.md",
            "## Resolution Notes\n"
            "\n"
            "The Dispute: foo paragraph mentions the keyword inline\n"
            "but should NOT be treated as a heading.\n"
            "\n"
            "## Dispute: Genuine heading\n",
        )
        assert extract_addressed_disputes(path) == ["Genuine heading"]

    def test_empty_title_after_colon_is_skipped(self, tmp_path: Path) -> None:
        # ``## Dispute:`` with no title is skipped — the regex's lazy ``+?``
        # requires at least one non-whitespace character to match (with
        # ``\s*`` trims).
        path = _write(
            tmp_path,
            "resolution.md",
            "## Dispute:   \n"
            "\n"
            "## Dispute: Has a title\n",
        )
        assert extract_addressed_disputes(path) == ["Has a title"]


# ---------------------------------------------------------------------------
# Duplicate handling
# ---------------------------------------------------------------------------


class TestDuplicateTitles:
    def test_duplicates_preserved_in_order(self, tmp_path: Path) -> None:
        path = _write(
            tmp_path,
            "resolution.md",
            "## Dispute: Same title\n"
            "First ruling.\n"
            "\n"
            "## Dispute: Different title\n"
            "Some ruling.\n"
            "\n"
            "## Dispute: Same title\n"
            "Second ruling — duplicate heading kept by parser.\n",
        )

        # Caller is responsible for deduplication; the parser preserves
        # raw document order including repeats.
        assert extract_addressed_disputes(path) == [
            "Same title",
            "Different title",
            "Same title",
        ]


# ---------------------------------------------------------------------------
# Defensive: parser is read-only and signature-stable
# ---------------------------------------------------------------------------


class TestReturnTypeAndPurity:
    def test_return_type_is_list_of_strings(self, tmp_path: Path) -> None:
        path = _write(
            tmp_path,
            "resolution.md",
            "## Dispute: A\n## Dispute: B\n",
        )
        result = extract_addressed_disputes(path)
        assert isinstance(result, list)
        assert all(isinstance(t, str) for t in result)

    def test_does_not_modify_file(self, tmp_path: Path) -> None:
        original = "## Dispute: Stable\n"
        path = _write(tmp_path, "resolution.md", original)
        extract_addressed_disputes(path)
        # File contents must be byte-identical after parsing.
        assert path.read_text(encoding="utf-8") == original


# ---------------------------------------------------------------------------
# Smoke parametrize — end-to-end count check
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("body", "expected_count"),
    [
        ("", 0),
        ("# Heading only\n", 0),
        ("## Dispute: Solo\n", 1),
        ("## Dispute: One\n## Dispute: Two\n", 2),
        ("## Dispute: A\n### Dispute: B\n#### Dispute: C\n", 3),
    ],
)
def test_count_matches_expected(
    tmp_path: Path, body: str, expected_count: int
) -> None:
    path = _write(tmp_path, "resolution.md", body)
    assert len(extract_addressed_disputes(path)) == expected_count
