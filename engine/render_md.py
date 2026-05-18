"""JSON → Markdown renderer for deliberation outputs (v4.2.0 spec § 5.2).

Pure function: same envelope dict in → identical Markdown string out, every
time. The Markdown companion file under ``deliberations/**`` is regenerable
from the canonical JSON; the renderer is the only sanctioned writer of those
``.md`` files.

Design:

* **Deterministic.** No timestamps in the output text (the envelope's
  ``timestamp`` field is rendered verbatim from JSON, not regenerated).
  Dict iteration uses the input dict's natural order; JSON parses preserve
  insertion order in Python 3.7+, so envelopes round-trip stably.
* **Type-driven.** Dicts become heading sections (H2/H3/H4 by nesting
  depth). Lists become Markdown lists. Scalars become inline values, with
  ``ENUM_SHAPED_STRINGS`` rendered in backticks per § 5.2's "enum values
  in backticks" requirement.
* **Schema-aware where it matters.** Envelope-level fields (output_type,
  agent_name, deliberation_id, …) get a deterministic header layout
  ("# {output_type} by {agent_name}"). Body fields render generically.
* **No external deps.** Pure stdlib — no jinja, no markdown libraries.
  The output is plain CommonMark.

Invariants (test_render_md.py asserts each):

1. ``render(env) == render(env)`` — deterministic.
2. ``render(env)`` raises only on malformed input (non-dict envelope, etc.).
3. Closed-enum field values appear inside backticks.
4. Headings start at H1 (the agent-identity line); body fields start at H2.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

# Fields rendered as enum values when their value is a closed-set string.
# Captured here rather than read from the schemas at render time because
# render_md.py runs in contexts (test harness, CI) where schema loading
# would be overkill. If a new enum field is added to a body schema, mirror
# the field name here. The schema-validate gate catches enum-value drift;
# this list controls only *presentation*.
_ENUM_FIELDS: frozenset[str] = frozenset(
    {
        # review
        "recommendation",
        "severity",
        # cross-review
        "stance",
        # revision
        "updated_recommendation",
        # synthesis
        # (severity covered above)
        # arbitration
        "combined_disposition",
        "verdict",
        "disposition",
        # envelope
        "deliberation_stage",
    }
)

# Pattern for "looks like an identifier we should backtick on sight" —
# ALL_CAPS_WITH_UNDERSCORES_AND_HYPHENS plus dotted variants. Matches things
# like APPROVE-WITH-FIXES, PROCEED-TO-RATIFICATION, but NOT free prose.
_ENUM_VALUE_RE = re.compile(r"^[A-Z][A-Z0-9_-]+(?:[.][A-Z0-9_-]+)*$")


# ────────────────────────────────────────────────────────────────────────────
# Public API
# ────────────────────────────────────────────────────────────────────────────


def json_to_md(envelope: dict[str, Any]) -> str:
    """Render a deliberation envelope as Markdown. Pure + deterministic.

    Args:
        envelope: A parsed JSON envelope (e.g., from ``json.loads(...)``).
            Must be a dict; ``output_type`` and ``agent_name`` are read for
            the H1 line. Other fields are rendered generically.

    Returns:
        A Markdown string. Trailing newline included.

    Raises:
        TypeError: if ``envelope`` is not a dict.
    """
    if not isinstance(envelope, dict):
        raise TypeError(
            f"json_to_md expects a dict envelope; got {type(envelope).__name__}"
        )

    lines: list[str] = []

    # H1: "{output_type} by {agent_name}" — or fall back gracefully.
    output_type = envelope.get("output_type", "<unknown>")
    agent_name = envelope.get("agent_name", "<unknown>")
    lines.append(f"# {output_type} by {agent_name}")
    lines.append("")

    # Envelope metadata block (everything except `body`).
    lines.append("## Envelope")
    lines.append("")
    for key, value in envelope.items():
        if key == "body":
            continue
        lines.append(f"- **{key}:** {_render_inline(value, key)}")
    lines.append("")

    # Body — recursive type-driven render.
    body = envelope.get("body")
    if isinstance(body, dict):
        lines.append("## Body")
        lines.append("")
        _render_dict(body, depth=3, out=lines)
    elif body is not None:
        # Unusual but not strictly malformed; render whatever's there.
        lines.append("## Body")
        lines.append("")
        lines.append(_render_inline(body, "body"))
        lines.append("")

    # Ensure exactly one trailing newline.
    text = "\n".join(lines).rstrip("\n") + "\n"
    return text


def json_to_md_from_path(json_path: Path) -> str:
    """Convenience wrapper: read JSON from disk, render to MD."""
    envelope = json.loads(json_path.read_text(encoding="utf-8"))
    return json_to_md(envelope)


# ────────────────────────────────────────────────────────────────────────────
# Internal rendering
# ────────────────────────────────────────────────────────────────────────────


def _render_dict(d: dict[str, Any], depth: int, out: list[str]) -> None:
    """Render a dict as a sequence of heading sections.

    Scalars are rendered as `- **key:** value` bullet items, grouped before
    the first nested-section header so the bullet block reads as a
    "properties" prelude. Lists and nested dicts become their own heading
    sub-sections at ``depth``.
    """
    heading = "#" * depth

    # First pass: emit scalar/inline properties as a bulleted list.
    scalar_lines: list[str] = []
    section_keys: list[str] = []
    for key, value in d.items():
        if isinstance(value, (dict, list)):
            section_keys.append(key)
        else:
            scalar_lines.append(f"- **{key}:** {_render_inline(value, key)}")

    if scalar_lines:
        out.extend(scalar_lines)
        out.append("")

    # Second pass: nested dicts/lists as their own heading sections.
    for key in section_keys:
        value = d[key]
        out.append(f"{heading} {key}")
        out.append("")
        if isinstance(value, dict):
            _render_dict(value, depth + 1, out)
        elif isinstance(value, list):
            _render_list(value, depth + 1, out)


def _render_list(lst: list[Any], depth: int, out: list[str]) -> None:
    """Render a list: scalars as bullets; complex items as sub-sections."""
    if not lst:
        out.append("_(empty)_")
        out.append("")
        return

    # If all items are scalars, render as a flat bullet list.
    if all(not isinstance(item, (dict, list)) for item in lst):
        for item in lst:
            out.append(f"- {_render_inline(item, None)}")
        out.append("")
        return

    # Mixed/complex: render each item as a sub-section.
    heading = "#" * depth
    for index, item in enumerate(lst):
        item_label = _list_item_label(item, index)
        out.append(f"{heading} {item_label}")
        out.append("")
        if isinstance(item, dict):
            _render_dict(item, depth + 1, out)
        elif isinstance(item, list):
            _render_list(item, depth + 1, out)
        else:
            out.append(_render_inline(item, None))
            out.append("")


def _list_item_label(item: Any, index: int) -> str:
    """Produce a stable, human-friendly header for a list item.

    Prefers an ``id`` field if present (e.g., ``S1``, ``D2``); falls back
    to the 1-based index.
    """
    if isinstance(item, dict):
        identifier = item.get("id")
        if isinstance(identifier, (str, int)) and str(identifier).strip():
            return f"`{identifier}`"
    return f"#{index + 1}"


def _render_inline(value: Any, field_name: str | None) -> str:
    """Render a scalar value for inline use (bullet items, properties).

    Enum-shaped strings are backticked. Lists of strings collapse to a
    comma-separated list. None → "_(none)_". Booleans + numbers → plain.
    """
    if value is None:
        return "_(none)_"
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        if _looks_like_enum(value, field_name):
            return f"`{value}`"
        return value
    if isinstance(value, list):
        # Inline lists of scalars get joined; lists of dicts shouldn't reach
        # here because _render_dict routes them through _render_list as
        # nested sections.
        if all(not isinstance(item, (dict, list)) for item in value):
            return ", ".join(_render_inline(item, field_name) for item in value)
        # Defensive fallback for an edge case (e.g., a scalar field whose
        # value happens to be a nested list).
        return json.dumps(value, sort_keys=True)
    # Dict or other — fall back to JSON dump for stability.
    return json.dumps(value, sort_keys=True)


def _looks_like_enum(value: str, field_name: str | None) -> bool:
    """Decide whether to backtick a string value.

    Two signals:
    1. Field name is in ``_ENUM_FIELDS`` — the schema declares it as a
       closed-enum field.
    2. The value itself matches ``_ENUM_VALUE_RE`` — looks like an
       identifier (ALL_CAPS-with-hyphens).
    """
    if field_name in _ENUM_FIELDS:
        return True
    return bool(_ENUM_VALUE_RE.match(value))
