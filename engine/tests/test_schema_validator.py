"""Unit tests for engine.schema_validator.

F2a scope: covers envelope validation against envelope.schema.json and the
ValidationWarning/ValidationResult Pydantic model behavior. Body-schema
validation tests are added in F2b when per-output-type schemas land.

Tests follow the contract specified in v4.2.0 spec § 5.1 + § 4.9.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from engine.schema_validator import (
    SchemaValidator,
    ValidationResult,
    ValidationWarning,
    _stringify,
)


SCHEMA_DIR = Path(__file__).resolve().parents[1] / "schema" / "v1"


# ────────────────────────────────────────────────────────────────────────────
# ValidationWarning — field-alias bridging between § 5.1 (Python) and § 4.9 (JSON)
# ────────────────────────────────────────────────────────────────────────────


def test_validation_warning_python_api_uses_pretty_names():
    """In-Python access uses the § 5.1 field names: message, expected, actual."""
    w = ValidationWarning(
        field_path="/body/disputes/0/severity",
        error_code="ENUM_VIOLATION",
        severity="error",
        message="value not in declared enum",
        expected="one of [blocking, substantive, nit]",
        actual="MAYBE",
    )

    assert w.message == "value not in declared enum"
    assert w.expected == "one of [blocking, substantive, nit]"
    assert w.actual == "MAYBE"


def test_validation_warning_json_uses_wire_contract_names():
    """to_dict() serializes with the § 4.9 wire-contract field names."""
    w = ValidationWarning(
        field_path="/schema_version",
        error_code="PATTERN_VIOLATION",
        severity="error",
        message="schema_version does not match SemVer pattern",
        expected="^[0-9]+\\.[0-9]+\\.[0-9]+(-[A-Za-z0-9.-]+)?$",
        actual="not-a-version",
    )

    payload = w.to_dict()

    assert payload["field_path"] == "/schema_version"
    assert payload["error_code"] == "PATTERN_VIOLATION"
    # § 4.9 wire names:
    assert payload["human_message"] == "schema_version does not match SemVer pattern"
    assert payload["expected_type"] == w.expected
    assert payload["actual_value"] == "not-a-version"
    # The § 5.1 internal names MUST NOT appear in the serialized payload.
    assert "message" not in payload
    assert "expected" not in payload
    assert "actual" not in payload


def test_validation_warning_frozen_immutable():
    """ValidationWarning is frozen per § 5.1 (model_config frozen=True)."""
    w = ValidationWarning(
        field_path="/x", error_code="TYPE_MISMATCH",
        message="m", expected="e", actual="a",
    )
    with pytest.raises(Exception):
        w.field_path = "/y"  # type: ignore[misc]


def test_validation_warning_rejects_extra_fields():
    """extra='forbid' per § 5.1."""
    with pytest.raises(Exception):
        ValidationWarning(
            field_path="/x", error_code="TYPE_MISMATCH",
            message="m", expected="e", actual="a",
            unknown_field="oops",  # type: ignore[call-arg]
        )


# ────────────────────────────────────────────────────────────────────────────
# SchemaValidator — construction
# ────────────────────────────────────────────────────────────────────────────


def test_validator_raises_runtime_error_on_missing_schema_dir(tmp_path):
    """Per § 5.1: infrastructure failures raise RuntimeError at __init__."""
    with pytest.raises(RuntimeError, match="schema_dir does not exist"):
        SchemaValidator(tmp_path / "does-not-exist")


def test_validator_raises_runtime_error_on_missing_envelope_schema(tmp_path):
    """Empty schema_dir (no envelope.schema.json) raises RuntimeError."""
    with pytest.raises(RuntimeError, match="envelope.schema.json missing"):
        SchemaValidator(tmp_path)


def test_validator_constructs_against_real_envelope_schema():
    """The shipped envelope.schema.json is well-formed and the validator constructs."""
    v = SchemaValidator(SCHEMA_DIR)
    assert v is not None


# ────────────────────────────────────────────────────────────────────────────
# SchemaValidator.validate — envelope happy path + failure modes
# ────────────────────────────────────────────────────────────────────────────


def _make_minimal_envelope(**overrides) -> dict:
    """Build a minimal valid envelope with a minimally-valid review body.

    Per F2b: body validation is wired; an empty body would fail the review
    body schema's required fields. Tests targeting envelope-level concerns
    use this minimal valid body to isolate envelope-level errors.
    """
    base = {
        "schema_version": "1.0.0-rc.1",
        "output_type": "review",
        "agent_name": "pragmatist",
        "deliberation_id": "test-deliberation",
        "deliberation_stage": "originating",
        "engine_version": "0.7.3",
        "source_commit": "abcd1234",
        "timestamp": "2026-05-13T12:00:00Z",
        "body": {
            "summary_assessment": "minimal valid body for envelope tests",
            "strengths": [],
            "concerns": [],
            "questions": [],
            "recommendation": "ABSTAIN",
        },
    }
    base.update(overrides)
    return base


def test_validate_well_formed_envelope_is_conformant():
    """A minimal valid envelope passes envelope-only validation."""
    v = SchemaValidator(SCHEMA_DIR)
    envelope = _make_minimal_envelope()
    content = json.dumps(envelope).encode("utf-8")

    result = v.validate(content, schema_version="1.0.0-rc.1")

    assert isinstance(result, ValidationResult)
    assert result.is_conformant is True
    assert result.warnings == []
    assert result.schema_version == "1.0.0-rc.1"
    assert result.output_type == "review"
    assert result.validation_duration_ms >= 0


def test_validate_missing_required_field_emits_warning_non_conformant():
    """Missing a required envelope field produces REQUIRED_FIELD_MISSING."""
    v = SchemaValidator(SCHEMA_DIR)
    envelope = _make_minimal_envelope()
    del envelope["agent_name"]  # required
    content = json.dumps(envelope).encode("utf-8")

    result = v.validate(content, schema_version="1.0.0-rc.1")

    assert result.is_conformant is False
    codes = {w.error_code for w in result.warnings}
    assert "REQUIRED_FIELD_MISSING" in codes


def test_validate_invalid_output_type_emits_enum_violation():
    """An output_type outside the declared enum produces ENUM_VIOLATION."""
    v = SchemaValidator(SCHEMA_DIR)
    envelope = _make_minimal_envelope(output_type="not-a-real-output-type")
    content = json.dumps(envelope).encode("utf-8")

    result = v.validate(content, schema_version="1.0.0-rc.1")

    assert result.is_conformant is False
    codes = {w.error_code for w in result.warnings}
    assert "ENUM_VIOLATION" in codes


def test_validate_invalid_schema_version_pattern_emits_pattern_violation():
    """schema_version not matching SemVer pattern produces PATTERN_VIOLATION."""
    v = SchemaValidator(SCHEMA_DIR)
    envelope = _make_minimal_envelope(schema_version="not-a-version")
    content = json.dumps(envelope).encode("utf-8")

    result = v.validate(content, schema_version="not-a-version")

    assert result.is_conformant is False
    codes = {w.error_code for w in result.warnings}
    assert "PATTERN_VIOLATION" in codes


def test_validate_schema_version_mismatch_with_validator_call_emits_unsupported():
    """envelope.schema_version != caller's schema_version produces SCHEMA_VERSION_UNSUPPORTED."""
    v = SchemaValidator(SCHEMA_DIR)
    envelope = _make_minimal_envelope(schema_version="1.0.0-rc.1")
    content = json.dumps(envelope).encode("utf-8")

    result = v.validate(content, schema_version="2.0.0")

    assert result.is_conformant is False
    codes = {w.error_code for w in result.warnings}
    assert "SCHEMA_VERSION_UNSUPPORTED" in codes


def test_validate_unparseable_json_returns_non_conformant_does_not_raise():
    """Unparseable JSON is a validation failure, not an exception."""
    v = SchemaValidator(SCHEMA_DIR)
    content = b"{ this is not valid json"

    # MUST NOT raise.
    result = v.validate(content, schema_version="1.0.0-rc.1")

    assert result.is_conformant is False
    assert len(result.warnings) >= 1
    assert any("not valid JSON" in w.message for w in result.warnings)


def test_validate_never_raises_on_random_bytes():
    """Per Principle V + § 5.1: validate() is non-raising on conformance failure."""
    v = SchemaValidator(SCHEMA_DIR)
    content = b"\x00\x01\x02 random bytes \xff\xfe"

    # MUST NOT raise.
    result = v.validate(content, schema_version="1.0.0-rc.1")

    assert result.is_conformant is False


# ────────────────────────────────────────────────────────────────────────────
# SchemaValidator.emit_warning — sidecar file
# ────────────────────────────────────────────────────────────────────────────


def test_emit_warning_writes_sidecar(tmp_path):
    """emit_warning writes .validation-warnings.json sibling to output path."""
    v = SchemaValidator(SCHEMA_DIR)
    output_path = tmp_path / "review.json"
    output_path.write_text('{"placeholder": "content"}', encoding="utf-8")

    result = ValidationResult(
        is_conformant=False,
        warnings=[
            ValidationWarning(
                field_path="/body",
                error_code="TYPE_MISMATCH",
                severity="error",
                message="body must be object",
                expected="object",
                actual="null",
            )
        ],
        schema_version="1.0.0-rc.1",
        output_type="review",
        validation_duration_ms=2.5,
    )

    v.emit_warning(result, output_path)

    sidecar = output_path.with_suffix(output_path.suffix + ".validation-warnings.json")
    assert sidecar.is_file()

    payload = json.loads(sidecar.read_text(encoding="utf-8"))
    assert payload["is_conformant"] is False
    assert payload["schema_version"] == "1.0.0-rc.1"
    assert payload["output_type"] == "review"
    assert len(payload["warnings"]) == 1
    # Wire-contract field names per § 4.9.
    assert payload["warnings"][0]["human_message"] == "body must be object"
    assert payload["warnings"][0]["expected_type"] == "object"


def test_emit_warning_idempotent(tmp_path):
    """Calling emit_warning twice for the same path overwrites the sidecar."""
    v = SchemaValidator(SCHEMA_DIR)
    output_path = tmp_path / "review.json"
    output_path.write_text("{}", encoding="utf-8")

    result_v1 = ValidationResult(
        is_conformant=False,
        warnings=[
            ValidationWarning(
                field_path="/a", error_code="TYPE_MISMATCH",
                message="first-call message", expected="x", actual="y",
            )
        ],
        schema_version="1.0.0-rc.1", output_type="review", validation_duration_ms=1.0,
    )
    result_v2 = ValidationResult(
        is_conformant=True,
        warnings=[],
        schema_version="1.0.0-rc.1", output_type="review", validation_duration_ms=1.0,
    )

    v.emit_warning(result_v1, output_path)
    v.emit_warning(result_v2, output_path)

    sidecar = output_path.with_suffix(output_path.suffix + ".validation-warnings.json")
    payload = json.loads(sidecar.read_text(encoding="utf-8"))
    # Second call's result wins.
    assert payload["is_conformant"] is True
    assert payload["warnings"] == []


# ────────────────────────────────────────────────────────────────────────────
# Stringify helper
# ────────────────────────────────────────────────────────────────────────────


def test_stringify_none_returns_empty_string():
    """Per § 5.1: '' when missing."""
    assert _stringify(None) == ""


def test_stringify_string_returns_self():
    assert _stringify("hello") == "hello"


def test_stringify_dict_serializes_json():
    assert _stringify({"a": 1, "b": [2, 3]}) == '{"a": 1, "b": [2, 3]}'
