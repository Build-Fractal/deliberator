"""Unit tests for engine.schema.slot_parser.

Tests each clause of SLOT_SYNTAX.md § 3 (parser semantics for malformed slot
pairs). Each malformed condition gets a dedicated test that asserts both the
recovery behavior AND the emitted warning code.

Grammar happy paths (§ 1) are covered by the well-formed-input tests.
Determinism (§ 3.8) is covered implicitly: the same fixture run twice would
produce identical output.
"""

from __future__ import annotations

import pytest

from engine.schema.slot_parser import (
    ParseResult,
    ParseWarning,
    SlotType,
    parse_slots,
)


# ────────────────────────────────────────────────────────────────────────────
# § 1 — Grammar happy paths
# ────────────────────────────────────────────────────────────────────────────


def test_single_string_slot_extracted_verbatim():
    """A single well-formed string-typed slot extracts to its body content."""
    content = "<<<VERDICT_BEGIN>>>\nAPPROVE-WITH-FIXES\n<<<VERDICT_END>>>\n"
    schema: dict[str, SlotType] = {"VERDICT": "string"}

    result = parse_slots(content, schema)

    assert result.slots == {"VERDICT": "APPROVE-WITH-FIXES"}
    assert result.warnings == []


def test_three_slots_in_order_per_spec_worked_example():
    """The § 1.3 worked example: STRENGTHS + CONCERNS + VERDICT, no warnings."""
    content = """The proposal scopes well to a 4-week implementation window.

<<<STRENGTHS_BEGIN>>>
- Clear interface boundary at the persistence layer.
- Three worked-example fixtures per output type satisfy XXVIII C6.
- Tier 3 placement matches the evidence base.
<<<STRENGTHS_END>>>

<<<CONCERNS_BEGIN>>>
- The 100ms validator budget is unmeasured against real synthesis outputs.
- Markdown deprecation cliff overlaps with conversus-oss v1.0.0-rc cycle.
<<<CONCERNS_END>>>

<<<VERDICT_BEGIN>>>
APPROVE-WITH-FIXES
<<<VERDICT_END>>>
"""
    schema: dict[str, SlotType] = {
        "STRENGTHS": "list",
        "CONCERNS": "list",
        "VERDICT": "string",
    }

    result = parse_slots(content, schema)

    assert result.warnings == []
    assert result.slots["STRENGTHS"] == [
        "Clear interface boundary at the persistence layer.",
        "Three worked-example fixtures per output type satisfy XXVIII C6.",
        "Tier 3 placement matches the evidence base.",
    ]
    assert result.slots["CONCERNS"] == [
        "The 100ms validator budget is unmeasured against real synthesis outputs.",
        "Markdown deprecation cliff overlaps with conversus-oss v1.0.0-rc cycle.",
    ]
    assert result.slots["VERDICT"] == "APPROVE-WITH-FIXES"
    assert result.preamble.startswith("The proposal scopes well")


def test_preamble_preserved_when_text_precedes_first_slot():
    """Text before the first BEGIN marker becomes the preamble."""
    content = "Some preamble prose.\n\n<<<VERDICT_BEGIN>>>\nAPPROVE\n<<<VERDICT_END>>>\n"

    result = parse_slots(content)

    assert result.preamble == "Some preamble prose."
    assert result.slots == {"VERDICT": "APPROVE"}


def test_no_slot_markers_returns_preamble_only():
    """Content with no markers returns the whole content as preamble."""
    content = "Plain agent prose with no slot markers at all.\nJust text."

    result = parse_slots(content)

    assert result.slots == {}
    assert result.warnings == []
    assert result.preamble == content.strip()


# ────────────────────────────────────────────────────────────────────────────
# § 2 — Escape rules / conservative recognition
# ────────────────────────────────────────────────────────────────────────────


def test_inline_marker_shaped_text_preserved_as_prose():
    """Marker-shaped tokens inline (not at line-start) pass through as prose."""
    content = """<<<STRENGTHS_BEGIN>>>
- The marker `<<<EXAMPLE_BEGIN>>>` appears inline here.
- Reference docs mention <<<NOT_A_SLOT>>> patterns too.
<<<STRENGTHS_END>>>
"""
    schema: dict[str, SlotType] = {"STRENGTHS": "list"}

    result = parse_slots(content, schema)

    assert result.warnings == []
    assert len(result.slots["STRENGTHS"]) == 2
    assert "<<<EXAMPLE_BEGIN>>>" in result.slots["STRENGTHS"][0]
    assert "<<<NOT_A_SLOT>>>" in result.slots["STRENGTHS"][1]


def test_marker_with_trailing_text_on_same_line_not_recognized():
    """A line that starts with `<<<NAME_BEGIN>>>` but has trailing text is prose, not a boundary."""
    content = """<<<STRENGTHS_BEGIN>>>
- Item 1
<<<STRENGTHS_END>>> with trailing words here
"""
    schema: dict[str, SlotType] = {"STRENGTHS": "list"}

    result = parse_slots(content, schema)

    # The trailing-text END line is NOT recognized as a boundary; the slot is
    # therefore unmatched at EOF (§ 3.1).
    assert any(w.code == "slot.unmatched_begin" for w in result.warnings)


# ────────────────────────────────────────────────────────────────────────────
# § 3.1 — Unmatched BEGIN (no closing END)
# ────────────────────────────────────────────────────────────────────────────


def test_unmatched_begin_recovers_to_next_slot_with_warning():
    """An open slot followed by a different-name BEGIN: recover to next, warn."""
    content = """<<<STRENGTHS_BEGIN>>>
- Item 1
- Item 2

<<<CONCERNS_BEGIN>>>
- Concern A
<<<CONCERNS_END>>>
"""
    schema: dict[str, SlotType] = {"STRENGTHS": "list", "CONCERNS": "list"}

    result = parse_slots(content, schema)

    unmatched = [w for w in result.warnings if w.code == "slot.unmatched_begin"]
    assert len(unmatched) == 1
    assert unmatched[0].field_path == "STRENGTHS"
    # Both slots still extracted; CONCERNS is well-formed.
    assert "Concern A" in result.slots["CONCERNS"]
    assert "Item 1" in str(result.slots["STRENGTHS"])


def test_unmatched_begin_at_eof_recovers_to_eof_with_warning():
    """An open slot with no closing END before EOF: recover to EOF, warn."""
    content = "<<<STRENGTHS_BEGIN>>>\n- Item 1\n- Item 2\n"
    schema: dict[str, SlotType] = {"STRENGTHS": "list"}

    result = parse_slots(content, schema)

    unmatched = [w for w in result.warnings if w.code == "slot.unmatched_begin"]
    assert len(unmatched) == 1
    assert unmatched[0].field_path == "STRENGTHS"
    assert result.slots["STRENGTHS"] == ["Item 1", "Item 2"]


# ────────────────────────────────────────────────────────────────────────────
# § 3.2 — Unmatched END (no preceding BEGIN)
# ────────────────────────────────────────────────────────────────────────────


def test_unmatched_end_dropped_with_warning():
    """An orphan END marker is dropped; warning emitted."""
    content = """<<<STRENGTHS_BEGIN>>>
- Item 1
<<<STRENGTHS_END>>>
<<<CONCERNS_END>>>
"""
    schema: dict[str, SlotType] = {"STRENGTHS": "list"}

    result = parse_slots(content, schema)

    orphans = [w for w in result.warnings if w.code == "slot.unmatched_end"]
    assert len(orphans) == 1
    assert orphans[0].field_path == "CONCERNS"
    # STRENGTHS still extracted normally.
    assert result.slots["STRENGTHS"] == ["Item 1"]


# ────────────────────────────────────────────────────────────────────────────
# § 3.3 — Nested same-name slots
# ────────────────────────────────────────────────────────────────────────────


def test_nested_same_name_inner_begin_treated_as_content_with_warning():
    """An inner BEGIN of the same name inside an open slot: warn + recover."""
    content = """<<<STRENGTHS_BEGIN>>>
- Outer item
<<<STRENGTHS_BEGIN>>>
- Inner item
<<<STRENGTHS_END>>>
<<<STRENGTHS_END>>>
"""
    schema: dict[str, SlotType] = {"STRENGTHS": "list"}

    result = parse_slots(content, schema)

    same_name = [w for w in result.warnings if w.code == "slot.nested_same_name"]
    assert len(same_name) == 1
    assert same_name[0].field_path == "STRENGTHS"
    # Per § 3.3: the inner BEGIN becomes content; the first END closes the
    # (only) open slot; the second END is orphaned.
    orphans = [w for w in result.warnings if w.code == "slot.unmatched_end"]
    assert len(orphans) == 1


# ────────────────────────────────────────────────────────────────────────────
# § 3.4 — Nested different-name slots
# ────────────────────────────────────────────────────────────────────────────


def test_inline_different_name_marker_passes_through_as_content():
    """An inline different-name marker (not line-start) is preserved as prose."""
    content = """<<<STRENGTHS_BEGIN>>>
- Item with embedded reference: see <<<CONCERNS_BEGIN>>> for related.
- Item 2
<<<STRENGTHS_END>>>
"""
    schema: dict[str, SlotType] = {"STRENGTHS": "list"}

    result = parse_slots(content, schema)

    # No warnings — well-formed input.
    assert result.warnings == []
    assert len(result.slots["STRENGTHS"]) == 2
    assert "<<<CONCERNS_BEGIN>>>" in result.slots["STRENGTHS"][0]


def test_line_start_different_name_begin_implicitly_closes_prior():
    """A different-name BEGIN at line-start implicitly closes the prior slot."""
    content = """<<<STRENGTHS_BEGIN>>>
- Item 1
<<<CONCERNS_BEGIN>>>
- Concern A
<<<CONCERNS_END>>>
"""
    schema: dict[str, SlotType] = {"STRENGTHS": "list", "CONCERNS": "list"}

    result = parse_slots(content, schema)

    # Per § 3.4: implicit close emits slot.unmatched_begin for STRENGTHS.
    unmatched = [w for w in result.warnings if w.code == "slot.unmatched_begin"]
    assert len(unmatched) == 1
    assert unmatched[0].field_path == "STRENGTHS"
    # Both slots present.
    assert result.slots["STRENGTHS"] == ["Item 1"]
    assert result.slots["CONCERNS"] == ["Concern A"]


# ────────────────────────────────────────────────────────────────────────────
# § 3.5 — Empty slot content
# ────────────────────────────────────────────────────────────────────────────


def test_empty_slot_content_yields_empty_string_no_warning():
    """An empty slot body is parsed as empty string; no parser warning."""
    content = "<<<VERDICT_BEGIN>>>\n<<<VERDICT_END>>>\n"
    schema: dict[str, SlotType] = {"VERDICT": "string"}

    result = parse_slots(content, schema)

    assert result.slots == {"VERDICT": ""}
    assert result.warnings == []


# ────────────────────────────────────────────────────────────────────────────
# § 3.6 — Unknown slot name (not in schema)
# ────────────────────────────────────────────────────────────────────────────


def test_unknown_slot_name_extracted_with_warning():
    """A slot whose name isn't in the schema: structurally parsed, warning."""
    content = """<<<KNOWN_BEGIN>>>
declared content
<<<KNOWN_END>>>
<<<UNKNOWN_BEGIN>>>
extra content
<<<UNKNOWN_END>>>
"""
    schema: dict[str, SlotType] = {"KNOWN": "string"}

    result = parse_slots(content, schema)

    unknown = [w for w in result.warnings if w.code == "slot.unknown_name"]
    assert len(unknown) == 1
    assert unknown[0].field_path == "UNKNOWN"
    # Body still extracted so downstream can debug.
    assert result.slots["UNKNOWN"] == "extra content"
    assert result.slots["KNOWN"] == "declared content"


def test_no_schema_provided_means_no_unknown_warnings():
    """When schema=None, all slots are accepted; no unknown-name warnings."""
    content = "<<<ANY_NAME_BEGIN>>>\nbody\n<<<ANY_NAME_END>>>\n"

    result = parse_slots(content)  # schema=None

    assert result.warnings == []
    assert result.slots == {"ANY_NAME": "body"}


# ────────────────────────────────────────────────────────────────────────────
# § 3.7 — Whitespace handling
# ────────────────────────────────────────────────────────────────────────────


def test_list_typed_slot_parses_markdown_bullets():
    """List-typed slots split body on newlines and recognize markdown bullets."""
    content = """<<<ITEMS_BEGIN>>>
- alpha
* beta
+ gamma
<<<ITEMS_END>>>
"""
    schema: dict[str, SlotType] = {"ITEMS": "list"}

    result = parse_slots(content, schema)

    assert result.slots["ITEMS"] == ["alpha", "beta", "gamma"]


def test_list_slot_drops_empty_lines():
    """Empty lines between list items are dropped."""
    content = """<<<ITEMS_BEGIN>>>
- alpha

- beta


- gamma
<<<ITEMS_END>>>
"""
    schema: dict[str, SlotType] = {"ITEMS": "list"}

    result = parse_slots(content, schema)

    assert result.slots["ITEMS"] == ["alpha", "beta", "gamma"]


def test_string_slot_strips_leading_trailing_whitespace():
    """String-typed slots strip outer whitespace; interior preserved."""
    content = "<<<MSG_BEGIN>>>\n\n  hello world  \n\n<<<MSG_END>>>\n"
    schema: dict[str, SlotType] = {"MSG": "string"}

    result = parse_slots(content, schema)

    assert result.slots["MSG"] == "hello world"


# ────────────────────────────────────────────────────────────────────────────
# § 3.8 — Determinism
# ────────────────────────────────────────────────────────────────────────────


def test_determinism_same_input_produces_same_output():
    """Identical input + schema produces identical output + warning order."""
    content = """<<<STRENGTHS_BEGIN>>>
- Item 1
<<<CONCERNS_BEGIN>>>
- Concern A
<<<CONCERNS_END>>>
<<<UNKNOWN_END>>>
"""
    schema: dict[str, SlotType] = {"STRENGTHS": "list", "CONCERNS": "list"}

    first = parse_slots(content, schema)
    second = parse_slots(content, schema)

    assert first.slots == second.slots
    assert [w.code for w in first.warnings] == [w.code for w in second.warnings]
    assert [w.field_path for w in first.warnings] == [w.field_path for w in second.warnings]


# ────────────────────────────────────────────────────────────────────────────
# Parser robustness — non-raising on malformed input (Principle V compliance)
# ────────────────────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "pathological_input",
    [
        "",  # empty input
        "<<<>>>\n",  # malformed marker, no name
        "<<<a_BEGIN>>>\n",  # lowercase name (not recognized by regex)
        "<<<__BEGIN>>>\n",  # name starts with underscore (not recognized)
        "<<<123_BEGIN>>>\n",  # name starts with digit (not recognized)
        "<<<X_BEGIN>>>" * 100,  # 100 unmatched BEGINs all on one line (not line-start after first)
    ],
)
def test_parser_never_raises_on_pathological_input(pathological_input):
    """Per Principle V: parser must not raise. Worst case is warnings."""
    # Must not raise.
    result = parse_slots(pathological_input)
    # Result is a ParseResult instance regardless.
    assert isinstance(result, ParseResult)
