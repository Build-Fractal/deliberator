"""Slot-marker parser implementing the contract in `SLOT_SYNTAX.md`.

Parses agent prose containing `<<<NAME_BEGIN>>> ... <<<NAME_END>>>` marker pairs
into a dictionary of slot name -> extracted value (string or list[str] depending
on the schema's declared type for the slot).

Per SLOT_SYNTAX.md § 1 (Grammar):
- Slot name: regex `[A-Z][A-Z0-9_]*` (SCREAMING_SNAKE_CASE)
- Markers must be at line-start (optional leading whitespace) and end-of-line
- Inline marker-shaped text is preserved as prose (conservative recognition)

Per SLOT_SYNTAX.md § 3 (Malformed slot pairs):
- Six recovery rules + per-rule warning emission

Per SLOT_SYNTAX.md § 3.8 (Determinism):
- Identical input + schema -> identical output + identical warning order

The parser MUST NOT raise on malformed input (per Tier 2 Principle V). All
malformed conditions produce warnings; recovery is documented in the spec.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Literal

# Slot-marker boundary regex per SLOT_SYNTAX.md § 1.1 + § 2.1 conservative rule:
# - Line-anchored (optional leading whitespace; trailing newline or EOF)
# - SCREAMING_SNAKE_CASE slot name token
# - Exact `_BEGIN>>>` or `_END>>>` suffix
_SLOT_MARKER_RE = re.compile(
    r"^[ \t]*<<<(?P<name>[A-Z][A-Z0-9_]*)_(?P<kind>BEGIN|END)>>>[ \t]*$",
    re.MULTILINE,
)

# Markdown list bullet (per SLOT_SYNTAX.md § 3.7 list-typed slot parsing).
_LIST_BULLET_RE = re.compile(r"^[ \t]*[-*+][ \t]+(?P<item>.*)$")


SlotType = Literal["string", "list"]
"""Declared slot type per the schema's slot_definitions table."""


WarningCode = Literal[
    "slot.unmatched_begin",
    "slot.unmatched_end",
    "slot.nested_same_name",
    "slot.unknown_name",
]
"""Parser-emitted warning codes per SLOT_SYNTAX.md § 3."""


@dataclass(frozen=True)
class ParseWarning:
    """Non-blocking warning emitted by the parser.

    Maps to ValidationWarning at the validator boundary; kept as a separate
    type here so the parser has no Pydantic dependency.
    """

    code: WarningCode
    field_path: str
    expected: str
    actual: str
    line_number: int


@dataclass(frozen=True)
class ParseResult:
    """Result of parsing agent prose into structured slots.

    Per SLOT_SYNTAX.md § 4 (validator integration):
    slots maps slot-name -> extracted value. Type depends on the schema's
    declared slot type:
    - 'string' slots: value is the whitespace-stripped slot body as one str
    - 'list' slots: value is a list[str], one entry per markdown list item

    Slots NOT declared in the schema appear with their raw string body AND
    emit a 'slot.unknown_name' warning per SLOT_SYNTAX.md § 3.6.
    """

    slots: dict[str, str | list[str]] = field(default_factory=dict)
    warnings: list[ParseWarning] = field(default_factory=list)
    preamble: str = ""
    """Text before the first slot marker; preserved verbatim (whitespace-stripped)."""


def parse_slots(
    content: str,
    schema: dict[str, SlotType] | None = None,
) -> ParseResult:
    """Parse `content` (agent prose) into a ParseResult.

    Args:
        content: Raw agent prose (UTF-8 string).
        schema: Map of slot-name -> declared type (`'string'` or `'list'`).
            If None, no schema is enforced; all slots are extracted as raw strings
            and no `slot.unknown_name` warnings are emitted. This matches the
            mode the validator uses when only the envelope (not the body) has
            been validated.

    Returns:
        ParseResult with extracted slots + warnings + preamble.

    The parser is deterministic per SLOT_SYNTAX.md § 3.8: identical input
    + schema produces identical output + warning order. Warning order is
    the order of first occurrence in `content`.
    """
    schema = schema or {}
    warnings: list[ParseWarning] = []

    # Step 1 — scan for all slot markers (per the line-anchored regex).
    # Per SLOT_SYNTAX.md § 2.1 conservative recognition, only line-start
    # `<<<NAME_BEGIN>>>` / `<<<NAME_END>>>` are recognized. Inline marker-shaped
    # text is implicitly preserved as prose (the regex won't match it).
    markers: list[tuple[int, int, str, str]] = [
        (m.start(), m.end(), m.group("name"), m.group("kind"))
        for m in _SLOT_MARKER_RE.finditer(content)
    ]

    if not markers:
        return ParseResult(preamble=content.strip())

    # Step 2 — pair BEGINs with their matching ENDs. The pairing is
    # single-slot-open-at-a-time per SLOT_SYNTAX.md § 3.4: nested
    # different-name slots are NOT supported at line-start; the parser
    # treats a new line-start BEGIN as implicitly closing the prior open.
    slots_raw: dict[str, str] = {}
    open_slot: tuple[str, int] | None = None  # (name, content_start_offset)
    slot_order: list[str] = []

    for start, end, name, kind in markers:
        line_number = content.count("\n", 0, start) + 1

        if kind == "BEGIN":
            # Same-name nesting: SLOT_SYNTAX.md § 3.3 — inner BEGIN is
            # treated as slot content of the outer slot. Do NOT open a
            # new slot; emit a warning instead.
            if open_slot is not None and open_slot[0] == name:
                warnings.append(
                    ParseWarning(
                        code="slot.nested_same_name",
                        field_path=name,
                        expected="no same-name slot nesting",
                        actual=f"inner <<<{name}_BEGIN>>> inside open {name} slot",
                        line_number=line_number,
                    )
                )
                continue

            # Different-name implicit close (SLOT_SYNTAX.md § 3.4): a
            # different-name BEGIN at line-start while a slot is open
            # implicitly closes the prior slot and emits unmatched_begin.
            if open_slot is not None and open_slot[0] != name:
                prior_name, prior_start = open_slot
                prior_body = content[prior_start:start].strip()
                slots_raw[prior_name] = prior_body
                slot_order.append(prior_name)
                warnings.append(
                    ParseWarning(
                        code="slot.unmatched_begin",
                        field_path=prior_name,
                        expected=f"<<<{prior_name}_END>>>",
                        actual="no closing marker found before next slot or EOF",
                        line_number=line_number,
                    )
                )
                open_slot = None

            # Open the new slot.
            open_slot = (name, end + 1 if end < len(content) and content[end] == "\n" else end)
            continue

        # kind == "END"
        if open_slot is None or open_slot[0] != name:
            # Unmatched END (SLOT_SYNTAX.md § 3.2): drop the orphan, warn.
            warnings.append(
                ParseWarning(
                    code="slot.unmatched_end",
                    field_path=name,
                    expected=f"preceding <<<{name}_BEGIN>>>",
                    actual="no matching opening marker found",
                    line_number=line_number,
                )
            )
            continue

        # Matched END: extract slot body.
        body_start = open_slot[1]
        body_end = start
        slot_body = content[body_start:body_end].strip()
        slots_raw[name] = slot_body
        slot_order.append(name)
        open_slot = None

    # Step 3 — handle any still-open slot at EOF (SLOT_SYNTAX.md § 3.1).
    if open_slot is not None:
        prior_name, prior_start = open_slot
        prior_body = content[prior_start:].strip()
        slots_raw[prior_name] = prior_body
        slot_order.append(prior_name)
        warnings.append(
            ParseWarning(
                code="slot.unmatched_begin",
                field_path=prior_name,
                expected=f"<<<{prior_name}_END>>>",
                actual="no closing marker found before next slot or EOF",
                line_number=content.count("\n") + 1,
            )
        )

    # Step 4 — preamble (text before first BEGIN marker).
    first_begin_start = next(
        (start for start, _, _, kind in markers if kind == "BEGIN"),
        len(content),
    )
    preamble = content[:first_begin_start].strip()

    # Step 5 — coerce slot bodies to declared types + emit unknown-name warnings.
    typed_slots: dict[str, str | list[str]] = {}
    for slot_name in slot_order:
        raw_body = slots_raw[slot_name]
        declared = schema.get(slot_name)

        if declared is None and schema:
            # Schema was provided but slot isn't declared (SLOT_SYNTAX.md § 3.6).
            warnings.append(
                ParseWarning(
                    code="slot.unknown_name",
                    field_path=slot_name,
                    expected=f"<one of: {sorted(schema.keys())}>",
                    actual=f"{slot_name} not declared in schema",
                    line_number=0,  # We don't track which line the slot opened anymore.
                )
            )
            # Still extract the raw body so downstream can see what was emitted.
            typed_slots[slot_name] = raw_body
            continue

        if declared == "list":
            typed_slots[slot_name] = _parse_list_body(raw_body)
        else:
            # 'string' (or no schema at all): use raw body verbatim.
            typed_slots[slot_name] = raw_body

    return ParseResult(slots=typed_slots, warnings=warnings, preamble=preamble)


def _parse_list_body(body: str) -> list[str]:
    """Parse a list-typed slot body into a list of strings.

    Per SLOT_SYNTAX.md § 3.7:
    - Split on newlines
    - Recognize markdown list bullets (`-`, `*`, `+`) at line-start
    - Strip the bullet character
    - Drop empty lines
    """
    items: list[str] = []
    for line in body.split("\n"):
        match = _LIST_BULLET_RE.match(line)
        if match:
            item_text = match.group("item").strip()
            if item_text:
                items.append(item_text)
        else:
            # Non-bullet line within a list slot: also include if non-empty.
            # Per SLOT_SYNTAX.md § 3.7 ambiguous: spec says "recognizes markdown
            # list bullets" but doesn't explicitly say non-bullet lines are
            # dropped. We include them as separate items if non-empty, since
            # dropping content silently would surprise the agent.
            stripped = line.strip()
            if stripped:
                items.append(stripped)
    return items
