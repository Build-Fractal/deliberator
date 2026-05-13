"""F2b tests — body-schema validation for all six output types.

Exercises the conformant fixtures + per-output-type failure modes that
prove body validation is wired correctly. Failure-mode fixtures
(missing-required, wrong-type, baseline) come in F2c via the
schema-validate CI workflow.

Each fixture lives at engine/tests/fixtures/v4_2_0/{output_type}.conformant.json.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from engine.schema_validator import SchemaValidator, ValidationWarning


SCHEMA_DIR = Path(__file__).resolve().parents[1] / "schema" / "v1"
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures" / "v4_2_0"


_OUTPUT_TYPES = [
    "review",
    "cross-review",
    "revision",
    "disputes",
    "synthesis",
    "arbitration",
]


@pytest.fixture(scope="module")
def validator() -> SchemaValidator:
    """One validator per test module; schemas compiled once."""
    return SchemaValidator(SCHEMA_DIR)


def _load_fixture(output_type: str) -> dict:
    """Load the conformant fixture for `output_type`."""
    path = FIXTURES_DIR / f"{output_type}.conformant.json"
    return json.loads(path.read_text(encoding="utf-8"))


# ────────────────────────────────────────────────────────────────────────────
# All conformant fixtures pass envelope + body validation
# ────────────────────────────────────────────────────────────────────────────


@pytest.mark.parametrize("output_type", _OUTPUT_TYPES)
def test_conformant_fixture_passes_full_validation(validator, output_type):
    """Each output_type's conformant fixture validates clean (envelope + body)."""
    envelope = _load_fixture(output_type)
    content = json.dumps(envelope).encode("utf-8")

    result = validator.validate(content, schema_version="1.0.0-rc.1")

    assert result.is_conformant, (
        f"{output_type}.conformant.json failed validation. Warnings: "
        + ", ".join(f"{w.field_path}: {w.error_code}" for w in result.warnings)
    )
    assert result.warnings == []
    assert result.output_type == output_type


# ────────────────────────────────────────────────────────────────────────────
# Per-body required-field violations are caught with /body/... field paths
# ────────────────────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "output_type,required_field",
    [
        ("review", "summary_assessment"),
        ("review", "recommendation"),
        ("cross-review", "reviewing_agent"),
        ("cross-review", "disagreement_points"),
        ("revision", "iteration"),
        ("revision", "updated_recommendation"),
        ("disputes", "disputes"),
        ("synthesis", "recommendation_to_arbiter"),
        ("synthesis", "disputes"),
        ("arbitration", "process_note"),
        ("arbitration", "combined_disposition"),
        ("arbitration", "per_question_rulings"),
    ],
)
def test_missing_body_required_field_emits_warning(
    validator, output_type, required_field
):
    """Removing a body's required field produces REQUIRED_FIELD_MISSING with /body/... path."""
    envelope = _load_fixture(output_type)
    body = copy.deepcopy(envelope["body"])
    del body[required_field]
    envelope["body"] = body
    content = json.dumps(envelope).encode("utf-8")

    result = validator.validate(content, schema_version="1.0.0-rc.1")

    assert result.is_conformant is False
    matching = [
        w for w in result.warnings
        if w.error_code == "REQUIRED_FIELD_MISSING" and w.field_path.startswith("/body")
    ]
    assert len(matching) >= 1, (
        f"Expected REQUIRED_FIELD_MISSING under /body for missing {required_field!r}. "
        f"Got: {[(w.field_path, w.error_code) for w in result.warnings]}"
    )


# ────────────────────────────────────────────────────────────────────────────
# Per-body enum violations emit ENUM_VIOLATION with the offending path
# ────────────────────────────────────────────────────────────────────────────


def test_review_invalid_recommendation_enum_emits_violation(validator):
    """A review body with recommendation='MAYBE' fails (not in declared enum)."""
    envelope = _load_fixture("review")
    envelope["body"]["recommendation"] = "MAYBE"
    content = json.dumps(envelope).encode("utf-8")

    result = validator.validate(content, schema_version="1.0.0-rc.1")

    assert result.is_conformant is False
    enum_violations = [w for w in result.warnings if w.error_code == "ENUM_VIOLATION"]
    assert len(enum_violations) >= 1
    assert any("/body/recommendation" in w.field_path for w in enum_violations)


def test_disputes_severity_outside_enum_emits_violation(validator):
    """A dispute with severity='nit' (not in disputes-schema enum) fails."""
    envelope = _load_fixture("disputes")
    # disputes.schema.json restricts severity to ["blocking", "substantive"]
    # (no "nit"; that's the review schema's enum).
    envelope["body"]["disputes"][0]["severity"] = "nit"
    content = json.dumps(envelope).encode("utf-8")

    result = validator.validate(content, schema_version="1.0.0-rc.1")

    assert result.is_conformant is False
    enum_violations = [w for w in result.warnings if w.error_code == "ENUM_VIOLATION"]
    assert len(enum_violations) >= 1
    assert any("/body/disputes/0/severity" in w.field_path for w in enum_violations)


def test_arbitration_combined_disposition_outside_enum_emits_violation(validator):
    """An arbitration with combined_disposition='YOLO' fails."""
    envelope = _load_fixture("arbitration")
    envelope["body"]["combined_disposition"] = "YOLO"
    content = json.dumps(envelope).encode("utf-8")

    result = validator.validate(content, schema_version="1.0.0-rc.1")

    assert result.is_conformant is False
    assert any(
        w.error_code == "ENUM_VIOLATION" and "/body/combined_disposition" in w.field_path
        for w in result.warnings
    )


# ────────────────────────────────────────────────────────────────────────────
# Per-body pattern violations emit PATTERN_VIOLATION with the offending path
# ────────────────────────────────────────────────────────────────────────────


def test_review_strength_id_pattern_violation(validator):
    """A strength with id='not-an-S-id' violates the ^S[0-9]+$ pattern."""
    envelope = _load_fixture("review")
    envelope["body"]["strengths"][0]["id"] = "not-an-S-id"
    content = json.dumps(envelope).encode("utf-8")

    result = validator.validate(content, schema_version="1.0.0-rc.1")

    assert result.is_conformant is False
    assert any(
        w.error_code == "PATTERN_VIOLATION" and "/body/strengths/0/id" in w.field_path
        for w in result.warnings
    )


def test_synthesis_dispute_id_pattern_violation(validator):
    """A synthesis dispute with id='X9' violates the ^D[0-9]+$ pattern."""
    envelope = _load_fixture("synthesis")
    envelope["body"]["disputes"][0]["id"] = "X9"
    content = json.dumps(envelope).encode("utf-8")

    result = validator.validate(content, schema_version="1.0.0-rc.1")

    assert result.is_conformant is False
    assert any(
        w.error_code == "PATTERN_VIOLATION" and "/body/disputes/0/id" in w.field_path
        for w in result.warnings
    )


# ────────────────────────────────────────────────────────────────────────────
# Bug C fix verification — synthesis disputes_remain trigger becomes structural
# ────────────────────────────────────────────────────────────────────────────


def test_synthesis_dispute_severity_is_structural_field(validator):
    """The synthesis body.disputes[*].severity field is the source-of-truth
    for Phase 6's `disputes_remain` trigger (fixes Bug C — grep-mismatch).

    This test demonstrates the structural-not-regex property: a synthesis
    with one blocking dispute MUST validate; the engine can mechanically
    check `len([d for d in body.disputes if d.severity == 'blocking']) > 0`
    without any prose drift concerns.
    """
    envelope = _load_fixture("synthesis")
    content = json.dumps(envelope).encode("utf-8")

    result = validator.validate(content, schema_version="1.0.0-rc.1")
    assert result.is_conformant

    # Demonstrate the structural trigger check:
    body = envelope["body"]
    blocking_disputes = [d for d in body["disputes"] if d["severity"] == "blocking"]
    assert len(blocking_disputes) == 1, "Fixture should have one blocking dispute"

    # The trigger condition for Phase 6 firing:
    disputes_remain = len(blocking_disputes) > 0
    assert disputes_remain, "Phase 6 trigger should fire structurally"


# ────────────────────────────────────────────────────────────────────────────
# Multi-error reporting: a body with multiple violations reports all of them
# ────────────────────────────────────────────────────────────────────────────


def test_multiple_body_violations_all_reported(validator):
    """A body with several violations gets one warning per violation, not the first."""
    envelope = _load_fixture("review")
    del envelope["body"]["summary_assessment"]  # REQUIRED_FIELD_MISSING
    envelope["body"]["recommendation"] = "MAYBE"  # ENUM_VIOLATION
    envelope["body"]["strengths"][0]["id"] = "bad-id"  # PATTERN_VIOLATION
    content = json.dumps(envelope).encode("utf-8")

    result = validator.validate(content, schema_version="1.0.0-rc.1")

    assert result.is_conformant is False
    codes = {w.error_code for w in result.warnings}
    assert {"REQUIRED_FIELD_MISSING", "ENUM_VIOLATION", "PATTERN_VIOLATION"} <= codes
