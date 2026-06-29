"""
Shared utility functions for deliberator linter modules.

Public API:
    word_count(text) -> int
"""

from __future__ import annotations


def word_count(text: str) -> int:
    """Return the number of whitespace-delimited words in *text*."""
    return len(text.split())
