"""
Tests for linter/utils.py shared utility functions.
"""

from __future__ import annotations

import pytest

try:
    from .utils import word_count
except ImportError:
    from utils import word_count


class TestWordCount:
    """Tests for the word_count() function."""

    def test_simple_sentence(self) -> None:
        assert word_count("hello world") == 2

    def test_empty_string(self) -> None:
        assert word_count("") == 0

    def test_whitespace_only(self) -> None:
        assert word_count("   ") == 0

    def test_single_word(self) -> None:
        assert word_count("hello") == 1

    def test_multiple_spaces(self) -> None:
        assert word_count("hello   world   foo") == 3

    def test_tabs_and_newlines(self) -> None:
        assert word_count("hello\tworld\nfoo") == 3

    def test_realistic_question(self) -> None:
        text = "Should we use monorepo or polyrepo for this project?"
        assert word_count(text) == 9

    def test_long_text(self) -> None:
        text = " ".join(["word"] * 100)
        assert word_count(text) == 100
