"""Parser for arbiter ``resolution.md`` files (spec 006 issue #68).

The arbiter writes a ``resolution.md`` file at the end of each arbitration
phase. That file contains one or more *Dispute* sections — markdown headings
of the form::

    ## Dispute: <title>
    ### Dispute: <title>
    #### Dispute: <title>

This module exposes :func:`extract_addressed_disputes`, which walks the file
and returns the per-heading dispute titles in document order. The function is
the canonical bridge between the arbiter's output and the post-arbitration
``check_disagreement`` call site in :mod:`engine.phases`: when the arbiter
addresses a dispute in round N, that title is fed into round N+1's
disagreement check via the ``arbiter_addressed`` kwarg so binding/recommended
influence can suppress it from the round N+1 dispute count.

Behaviour contract:

* Missing file → ``[]`` (no exception).
* Empty file or no dispute headings → ``[]``.
* Best-effort parsing — malformed text never raises.
* Heading levels 2, 3, and 4 are all recognised. The ``Dispute:`` keyword is
  matched case-sensitively (matches the canonical capitalised form the
  arbiter template emits) but tolerates flexible whitespace around the colon
  and the title.
* Duplicate titles are returned with duplicates preserved (the caller decides
  whether to deduplicate).
"""

from __future__ import annotations

import re
from pathlib import Path

# ``^#{2,4}`` — 2-4 leading hash marks (## | ### | ####)
# ``\s*Dispute:`` — optional whitespace, then the literal keyword
# ``\s*(.+?)\s*$`` — capture the title (everything after the colon, trimmed)
#
# ``re.MULTILINE`` makes ``^`` and ``$`` match line boundaries so the pattern
# works on the full file text without splitting first.
_DISPUTE_HEADING_RE = re.compile(
    # ``[^\S\n]`` matches whitespace except newlines so a heading line with
    # a missing/blank title cannot greedily consume the next heading line.
    r"^#{2,4}[^\S\n]*Dispute:[^\S\n]*(.+?)[^\S\n]*$",
    re.MULTILINE,
)


def extract_addressed_disputes(resolution_path: Path) -> list[str]:
    """Extract the list of dispute titles addressed by the arbiter.

    Reads *resolution_path* and returns each ``Dispute: <title>`` heading's
    title in document order. Heading levels ``##``, ``###``, and ``####``
    are recognised.

    Args:
        resolution_path: Path to a ``resolution.md`` file written by the
            arbiter. The path may not exist; in that case the function
            returns an empty list rather than raising.

    Returns:
        List of dispute titles in document order. Duplicate titles are
        preserved. Returns ``[]`` for missing files, empty files, or files
        with no dispute headings.
    """
    try:
        text = resolution_path.read_text(encoding="utf-8")
    except (FileNotFoundError, OSError):
        # Missing file or unreadable file → empty list. We never raise from
        # this entry point so the call site in engine/phases.py can use it
        # unconditionally without try/except plumbing.
        return []

    if not text:
        return []

    titles: list[str] = []
    for match in _DISPUTE_HEADING_RE.finditer(text):
        # Match group 1 is everything after ``Dispute:`` on the heading line,
        # already stripped by the regex (``\s*(.+?)\s*$``). Defensive strip()
        # in case future regex edits relax that.
        title = match.group(1).strip()
        if title:
            titles.append(title)
    return titles


__all__ = ["extract_addressed_disputes"]
