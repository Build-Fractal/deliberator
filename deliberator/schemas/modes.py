"""Canonical source of truth for valid deliberation modes.

All modules that need VALID_MODES should import from here to ensure
consistency. This was consolidated per spec 036, item M-4.
"""

from __future__ import annotations

VALID_MODES: frozenset[str] = frozenset({
    "cooperative",
    "winner-take-all",
    "prisoners-dilemma",
    "red-blue",
    "negotiation",
    "resource-allocation",
    "fair-division",
    "mechanism-design",
})
