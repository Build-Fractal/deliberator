"""Tests for engine.render_md — v4.2.0 § 5.2 JSON → Markdown renderer.

Invariants under test:

1. **Deterministic.** `render(env) == render(env)` — same input, same output,
   every time. The CI gate's renderer-round-trip check relies on this.
2. **Doesn't crash on conformant fixtures.** All 6 output types in
   `tests/fixtures/v4_2_0/*.conformant.json` render without error.
3. **Closed-enum field values appear in backticks.** Per § 5.2.
4. **Heading hierarchy.** H1 = agent/output-type line, H2 = top-level
   sections (Envelope, Body), H3+ = body sub-sections.
5. **Type errors are explicit.** Non-dict envelope → TypeError.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from engine.render_md import json_to_md, json_to_md_from_path

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures" / "v4_2_0"
OUTPUT_TYPES = [
    "review",
    "cross-review",
    "revision",
    "disputes",
    "synthesis",
    "arbitration",
]


def _load(output_type: str) -> dict:
    return json.loads((FIXTURES_DIR / f"{output_type}.conformant.json").read_text())


# ────────────────────────────────────────────────────────────────────────────
# Determinism — the load-bearing property
# ────────────────────────────────────────────────────────────────────────────


@pytest.mark.parametrize("output_type", OUTPUT_TYPES)
def test_rendering_is_deterministic(output_type):
    """Two renders of the same fixture produce byte-identical output."""
    envelope = _load(output_type)
    first = json_to_md(envelope)
    second = json_to_md(envelope)
    assert first == second, f"{output_type} render not deterministic"


@pytest.mark.parametrize("output_type", OUTPUT_TYPES)
def test_render_from_path_matches_render_from_dict(output_type):
    """`json_to_md_from_path` == `json_to_md(json.loads(path.read_text()))`."""
    path = FIXTURES_DIR / f"{output_type}.conformant.json"
    from_path = json_to_md_from_path(path)
    from_dict = json_to_md(json.loads(path.read_text()))
    assert from_path == from_dict


# ────────────────────────────────────────────────────────────────────────────
# Doesn't-crash sweep
# ────────────────────────────────────────────────────────────────────────────


@pytest.mark.parametrize("output_type", OUTPUT_TYPES)
def test_renders_conformant_fixture_without_error(output_type):
    """Every conformant fixture renders to non-empty Markdown."""
    md = json_to_md(_load(output_type))
    assert md.strip(), f"{output_type} rendered to empty string"
    assert md.endswith("\n"), "Output should end with exactly one newline"


# ────────────────────────────────────────────────────────────────────────────
# Heading hierarchy
# ────────────────────────────────────────────────────────────────────────────


@pytest.mark.parametrize("output_type", OUTPUT_TYPES)
def test_h1_contains_output_type_and_agent(output_type):
    """The first non-empty line is `# {output_type} by {agent_name}`."""
    envelope = _load(output_type)
    md = json_to_md(envelope)
    first_line = md.split("\n", 1)[0]
    assert first_line.startswith("# ")
    assert envelope["output_type"] in first_line
    assert envelope["agent_name"] in first_line


@pytest.mark.parametrize("output_type", OUTPUT_TYPES)
def test_envelope_and_body_appear_as_h2_sections(output_type):
    """The structural sections (Envelope, Body) start at H2."""
    md = json_to_md(_load(output_type))
    lines = md.split("\n")
    assert "## Envelope" in lines, f"{output_type} missing '## Envelope'"
    # Body section may be absent if the fixture has no body, but all our
    # conformant fixtures have one.
    assert "## Body" in lines, f"{output_type} missing '## Body'"


# ────────────────────────────────────────────────────────────────────────────
# Enum-value backticking
# ────────────────────────────────────────────────────────────────────────────


def test_review_recommendation_appears_in_backticks():
    """`recommendation` is a closed enum (APPROVE-AS-DRAFTED, etc.) — backtick it."""
    envelope = _load("review")
    md = json_to_md(envelope)
    recommendation = envelope["body"]["recommendation"]
    assert f"`{recommendation}`" in md


def test_arbitration_combined_disposition_in_backticks():
    """`combined_disposition` is a closed enum — backtick it."""
    envelope = _load("arbitration")
    md = json_to_md(envelope)
    disposition = envelope["body"]["combined_disposition"]
    assert f"`{disposition}`" in md


def test_disputes_severity_in_backticks():
    """`severity` field in disputes is a closed enum (blocking|substantive)."""
    envelope = _load("disputes")
    md = json_to_md(envelope)
    # Every dispute's severity field should appear backticked
    for dispute in envelope["body"]["disputes"]:
        sev = dispute["severity"]
        assert f"`{sev}`" in md, f"severity {sev!r} not backticked in rendered output"


def test_free_prose_is_not_backticked():
    """Sentences and free-text fields should NOT be backticked.

    Backticking should fire only for closed-enum values (ALL_CAPS-style),
    not for free-form prose like the `summary_assessment` field.
    """
    envelope = _load("review")
    md = json_to_md(envelope)
    summary = envelope["body"]["summary_assessment"]
    # The prose should appear in the rendered output without surrounding
    # backticks. Check by looking for "`<full sentence>`" — should not match.
    assert f"`{summary}`" not in md


# ────────────────────────────────────────────────────────────────────────────
# Error handling
# ────────────────────────────────────────────────────────────────────────────


def test_non_dict_envelope_raises_type_error():
    """Passing a non-dict envelope raises TypeError with a clear message."""
    with pytest.raises(TypeError, match="json_to_md expects a dict"):
        json_to_md("not a dict")  # type: ignore[arg-type]

    with pytest.raises(TypeError, match="json_to_md expects a dict"):
        json_to_md([1, 2, 3])  # type: ignore[arg-type]


def test_empty_envelope_renders_with_unknown_placeholders():
    """An empty dict renders to valid markdown with `<unknown>` placeholders."""
    md = json_to_md({})
    assert md.startswith("# <unknown> by <unknown>")
    assert "## Envelope" in md
    # No `## Body` section since there's no body key.
    assert "## Body" not in md


def test_envelope_without_body_renders_envelope_only():
    """A dict with envelope fields but no body renders only the envelope section."""
    envelope = {"output_type": "review", "agent_name": "test-agent", "schema_version": "1.0.0-rc.1"}
    md = json_to_md(envelope)
    assert "# review by test-agent" in md
    assert "## Envelope" in md
    assert "## Body" not in md
    assert "schema_version" in md


# ────────────────────────────────────────────────────────────────────────────
# Edge case: list with no `id` field falls back to index
# ────────────────────────────────────────────────────────────────────────────


def test_list_items_without_id_get_index_labels():
    """List items rendered as sub-sections use `#N` headers when no id is present."""
    envelope = {
        "output_type": "review",
        "agent_name": "tester",
        "body": {
            "concerns": [
                {"severity": "blocking", "text": "no id here"},
                {"severity": "nit", "text": "also no id"},
            ]
        },
    }
    md = json_to_md(envelope)
    # When items have no `id`, they render as `### #1`, `### #2`, etc.
    assert "#1" in md
    assert "#2" in md
