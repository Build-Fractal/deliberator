"""F2c parametrized tests over the 18 non-conformant fixtures.

Each fixture is the conformant baseline with one targeted defect injected.
The test parameter table declares which error code each defect MUST produce.
Failure modes covered (per spec § 5.3 + Principle XXVIII sub-clause 2):
  - missing-required → REQUIRED_FIELD_MISSING
  - wrong-type → TYPE_MISMATCH
  - enum-violation → ENUM_VIOLATION

Fixture generation lives in `generate_non_conformant.py`; these tests assert
that the validator produces the expected outcome for each generated fixture.
The two are versioned together — if a body schema's enum or required-set
changes, regenerate fixtures and update this expectations table.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from engine.schema_validator import SchemaValidator

SCHEMA_DIR = Path(__file__).resolve().parents[1] / "schema" / "v1"
NON_CONFORMANT_DIR = Path(__file__).resolve().parent / "fixtures" / "v4_2_0" / "non-conformant"


# (output_type, mode, expected_error_code)
EXPECTATIONS: list[tuple[str, str, str]] = [
    # review
    ("review", "missing-required", "REQUIRED_FIELD_MISSING"),
    ("review", "wrong-type", "TYPE_MISMATCH"),
    ("review", "enum-violation", "ENUM_VIOLATION"),
    # cross-review
    ("cross-review", "missing-required", "REQUIRED_FIELD_MISSING"),
    ("cross-review", "wrong-type", "TYPE_MISMATCH"),
    ("cross-review", "enum-violation", "ENUM_VIOLATION"),
    # revision
    ("revision", "missing-required", "REQUIRED_FIELD_MISSING"),
    ("revision", "wrong-type", "TYPE_MISMATCH"),
    ("revision", "enum-violation", "ENUM_VIOLATION"),
    # disputes
    ("disputes", "missing-required", "REQUIRED_FIELD_MISSING"),
    ("disputes", "wrong-type", "TYPE_MISMATCH"),
    ("disputes", "enum-violation", "ENUM_VIOLATION"),
    # synthesis
    ("synthesis", "missing-required", "REQUIRED_FIELD_MISSING"),
    ("synthesis", "wrong-type", "TYPE_MISMATCH"),
    ("synthesis", "enum-violation", "ENUM_VIOLATION"),
    # arbitration
    ("arbitration", "missing-required", "REQUIRED_FIELD_MISSING"),
    ("arbitration", "wrong-type", "TYPE_MISMATCH"),
    ("arbitration", "enum-violation", "ENUM_VIOLATION"),
]


@pytest.fixture(scope="module")
def validator() -> SchemaValidator:
    return SchemaValidator(SCHEMA_DIR)


def test_eighteen_fixtures_exist_on_disk() -> None:
    """Sanity: every (type, mode) pair has a fixture file."""
    for output_type, mode, _ in EXPECTATIONS:
        path = NON_CONFORMANT_DIR / f"{output_type}.{mode}.json"
        assert path.is_file(), f"missing fixture: {path}"


@pytest.mark.parametrize("output_type,mode,expected_code", EXPECTATIONS)
def test_fixture_fails_with_expected_error_code(
    validator: SchemaValidator, output_type: str, mode: str, expected_code: str
) -> None:
    """Each non-conformant fixture MUST fail validation with the expected error code.

    Failure here means either:
    1. The fixture is no longer producing the expected defect (regenerate it).
    2. The body schema changed in a way that masks the defect (intentional schema
       change requires updating expectations + regenerating fixtures).
    3. The validator's error-code mapping regressed (the most serious signal).
    """
    path = NON_CONFORMANT_DIR / f"{output_type}.{mode}.json"
    content = path.read_bytes()
    envelope = json.loads(content)
    schema_version = envelope.get("schema_version", "1.0.0-rc.1")

    result = validator.validate(content, schema_version)

    assert result.is_conformant is False, (
        f"{output_type}.{mode}.json validated as conformant — defect not effective"
    )
    codes = {w.error_code for w in result.warnings}
    assert expected_code in codes, (
        f"{output_type}.{mode}.json: expected {expected_code} in warnings, got "
        f"{sorted(codes)}. Field paths: {[w.field_path for w in result.warnings]}"
    )
