"""Non-blocking JSON Schema validator for conversus deliberation outputs.

Implements the F2 class signatures specified in v4.2.0 spec § 5.1.

Conforms to Tier 2 Principle V (non-blocking writes): `validate()` NEVER raises
on conformance failure; callers (engine.persistence.persist_output) ALWAYS
proceed to write regardless of `is_conformant`. Mechanical enforcement bite
lives at the PR-required CI gate (§ 5.4), not at write-time.

Field-name bridging: the Pydantic ValidationWarning model uses the cleaner
in-Python names per § 5.1 (`message`, `expected`, `actual`); JSON serialization
uses the wire-contract names per § 4.9 (`human_message`, `expected_type`,
`actual_value`). Bridge via Pydantic v2 field aliases.

F2a scope (this file at first landing): Pydantic models + SchemaValidator class
skeleton (envelope-only validation). Body-schema validation (review,
cross-review, revision, disputes, synthesis, arbitration) lands in F2b when
those schemas are added under engine/schema/v1/.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

_ERROR_CODES = Literal[
    "REQUIRED_FIELD_MISSING",
    "TYPE_MISMATCH",
    "ENUM_VIOLATION",
    "PATTERN_VIOLATION",
    "ADDITIONAL_PROPERTY_FORBIDDEN",
    "SCHEMA_VERSION_UNSUPPORTED",
    "ENVELOPE_BODY_TYPE_MISMATCH",
    "ARRAY_MIN_ITEMS_VIOLATION",
]


class ValidationWarning(BaseModel):
    """Single conformance defect raised by the validator.

    Per v4.2.0 spec § 5.1 (F2 Pydantic class signature). JSON serialization
    via `to_dict()` matches the wire contract in § 4.9 (validator-error.schema.json):
    `message` -> 'human_message', `expected` -> 'expected_type', `actual` -> 'actual_value'.
    """

    model_config = ConfigDict(frozen=True, extra="forbid", populate_by_name=True)

    field_path: str = Field(
        ...,
        description="JSON pointer to the offending field, e.g., '/body/disputes/0/severity'.",
    )
    error_code: _ERROR_CODES
    severity: Literal["error", "warning"] = "warning"
    message: str = Field(
        ...,
        min_length=1,
        alias="human_message",
        description="Human-friendly explanation of the failure.",
    )
    expected: str = Field(
        ...,
        alias="expected_type",
        description="Schema-declared expected shape (type/pattern/enum).",
    )
    actual: str = Field(
        ...,
        alias="actual_value",
        description="Stringified actual value at field_path; '' when missing.",
    )
    suggested_fix: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize for sidecar JSON + event stream.

        Uses alias names so the on-disk JSON matches the § 4.9 wire contract:
        `human_message`, `expected_type`, `actual_value`.
        """
        return self.model_dump(mode="json", by_alias=True)


class ValidationResult(BaseModel):
    """Aggregate result of a single `SchemaValidator.validate()` call.

    Per v4.2.0 spec § 5.1 (F2). `is_conformant` is True iff `warnings` contains
    no entry with severity='error'.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    is_conformant: bool
    warnings: list[ValidationWarning] = Field(default_factory=list)
    schema_version: str = Field(
        ..., description="schema_version field read from envelope."
    )
    output_type: str = Field(..., description="output_type field read from envelope.")
    validation_duration_ms: float = Field(..., ge=0.0)


class SchemaValidator:
    """Non-blocking JSON Schema validator for conversus deliberation outputs.

    Per v4.2.0 spec § 5.1 (F2):
    - `validate()` NEVER raises on conformance failure.
    - Returns a structured ValidationResult.
    - Callers (engine.persistence.persist_output) ALWAYS proceed to write.
    - Mechanical enforcement bite lives at the PR-required CI gate (§ 5.4).

    F2a skeleton: implements envelope validation against
    `engine/schema/v1/envelope.schema.json`. Body validation against per-type
    schemas (review, cross-review, etc.) is added in F2b when those schemas
    land. Until then, the body is validated as `{"type": "object"}` only —
    structural-not-shape validation.

    Compilation is cached in memory for the process lifetime (performance
    discipline per v4.2.0 § 5.1 + § 5.1.1 budget validation framework).
    """

    def __init__(self, schema_dir: Path) -> None:
        """Initialize validator with compiled schemas from `schema_dir`.

        Args:
            schema_dir: Path to the directory containing envelope.schema.json
                + (eventually) the six body schemas. Typically
                `engine/schema/v1/` within conversus-oss.

        Raises:
            RuntimeError: if `schema_dir` is missing or required schemas are
                malformed. Per § 5.1, this is the ONLY raise path. The engine
                catches this once at startup and falls back to write-only mode.
        """
        if not schema_dir.is_dir():
            raise RuntimeError(
                f"SchemaValidator: schema_dir does not exist: {schema_dir}"
            )

        envelope_path = schema_dir / "envelope.schema.json"
        if not envelope_path.is_file():
            raise RuntimeError(
                f"SchemaValidator: envelope.schema.json missing at {envelope_path}"
            )

        self._schema_dir = schema_dir

        # Lazy import jsonschema so the module is importable for tests that
        # only touch the Pydantic models without requiring the heavy validator
        # dependency. The import failure is converted to a RuntimeError per
        # the § 5.1 "infrastructure failure" contract.
        try:
            from jsonschema import Draft202012Validator
            from jsonschema.exceptions import SchemaError
        except ImportError as exc:
            raise RuntimeError(
                "SchemaValidator: jsonschema library not installed; "
                "add to pyproject.toml dependencies."
            ) from exc

        try:
            envelope_schema = json.loads(envelope_path.read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(envelope_schema)
        except (json.JSONDecodeError, SchemaError) as exc:
            raise RuntimeError(
                f"SchemaValidator: envelope.schema.json is malformed: {exc}"
            ) from exc

        # F2a: envelope-only validator. We strip the `allOf` body-ref branches
        # because the per-type body schemas don't exist yet (F2b adds them).
        # Once F2b lands, we drop this stripping and validate full envelope+body.
        envelope_no_body_refs = dict(envelope_schema)
        envelope_no_body_refs.pop("allOf", None)
        self._envelope_validator = Draft202012Validator(envelope_no_body_refs)

    def validate(self, content: bytes, schema_version: str) -> ValidationResult:
        """Validate `content` (raw bytes of a single deliberation output JSON file).

        Per v4.2.0 spec § 5.1 F2: MUST NOT raise on conformance failure. MUST
        raise only on infrastructure failure (which is handled in __init__).

        Args:
            content: Raw bytes of the output JSON file (typically from
                Path.read_bytes()).
            schema_version: Expected schema version (e.g., '1.0.0-rc.1'). Used
                for SCHEMA_VERSION_UNSUPPORTED detection.

        Returns:
            ValidationResult with is_conformant=False on any error-severity
            warning; warnings-only outputs return is_conformant=True with a
            non-empty warnings list.
        """
        start_ns = time.perf_counter_ns()
        warnings: list[ValidationWarning] = []
        output_type = "<unknown>"
        envelope_schema_version = "<unknown>"

        # Parse the JSON. Parse failure is itself a validation failure (not
        # an infrastructure failure) — file is on disk, just not valid JSON.
        # Catches both JSONDecodeError (malformed JSON) and UnicodeDecodeError
        # (bytes that aren't valid utf-8 / utf-16). Per Principle V: never
        # raise on file-content malformation.
        try:
            envelope = json.loads(content)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            message = (
                f"file is not valid JSON: {exc.msg} at line {exc.lineno} col {exc.colno}"
                if isinstance(exc, json.JSONDecodeError)
                else f"file is not valid utf-8/utf-16: {exc}"
            )
            warnings.append(
                ValidationWarning(
                    field_path="/",
                    error_code="TYPE_MISMATCH",
                    severity="error",
                    message=message,
                    expected="application/json",
                    actual="<unparseable>",
                )
            )
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000.0
            return ValidationResult(
                is_conformant=False,
                warnings=warnings,
                schema_version=schema_version,
                output_type=output_type,
                validation_duration_ms=duration_ms,
            )

        # Extract envelope identity fields for the result (best-effort; the
        # envelope-validator below catches missing/wrong-type cases).
        if isinstance(envelope, dict):
            envelope_schema_version = str(envelope.get("schema_version", "<unknown>"))
            output_type = str(envelope.get("output_type", "<unknown>"))

            if envelope_schema_version != "<unknown>" and envelope_schema_version != schema_version:
                warnings.append(
                    ValidationWarning(
                        field_path="/schema_version",
                        error_code="SCHEMA_VERSION_UNSUPPORTED",
                        severity="error",
                        message=(
                            f"envelope declares schema_version={envelope_schema_version!r} but "
                            f"validator was invoked for {schema_version!r}"
                        ),
                        expected=schema_version,
                        actual=envelope_schema_version,
                    )
                )

        # Run envelope JSON Schema validation.
        for jsonschema_error in self._envelope_validator.iter_errors(envelope):
            warnings.append(_convert_jsonschema_error(jsonschema_error))

        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000.0
        is_conformant = not any(w.severity == "error" for w in warnings)

        return ValidationResult(
            is_conformant=is_conformant,
            warnings=warnings,
            schema_version=envelope_schema_version,
            output_type=output_type,
            validation_duration_ms=duration_ms,
        )

    def emit_warning(
        self, result: ValidationResult, output_path: Path
    ) -> None:
        """Emit non-conformance to two channels.

        1. Sibling `.validation-warnings.json` sidecar at
           `output_path.with_suffix(output_path.suffix + '.validation-warnings.json')`.
        2. (Future) deliberation event stream — F2c wires this when the engine's
           event stream gains a `schema_validation_failed` event type. For F2a,
           only the sidecar is written; F2c upgrades the engine integration.

        Idempotent: calling twice for the same output path overwrites the sidecar.
        """
        sidecar = output_path.with_suffix(output_path.suffix + ".validation-warnings.json")
        payload = {
            "is_conformant": result.is_conformant,
            "schema_version": result.schema_version,
            "output_type": result.output_type,
            "validation_duration_ms": result.validation_duration_ms,
            "warnings": [w.to_dict() for w in result.warnings],
        }
        sidecar.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _convert_jsonschema_error(err: Any) -> ValidationWarning:
    """Map a jsonschema.ValidationError into a ValidationWarning.

    Maps jsonschema's `validator` attribute (e.g., 'required', 'type', 'enum',
    'pattern', 'additionalProperties', 'minItems') to the v4.2.0 error_code
    enum per spec § 4.9.
    """
    validator_to_code: dict[str, str] = {
        "required": "REQUIRED_FIELD_MISSING",
        "type": "TYPE_MISMATCH",
        "enum": "ENUM_VIOLATION",
        "pattern": "PATTERN_VIOLATION",
        "additionalProperties": "ADDITIONAL_PROPERTY_FORBIDDEN",
        "minItems": "ARRAY_MIN_ITEMS_VIOLATION",
    }
    error_code = validator_to_code.get(err.validator, "TYPE_MISMATCH")

    # Build JSON pointer from absolute_path (jsonschema uses deque of path parts).
    path_parts = list(err.absolute_path)
    field_path = "/" + "/".join(str(p) for p in path_parts) if path_parts else "/"

    return ValidationWarning(
        field_path=field_path,
        error_code=error_code,  # type: ignore[arg-type]
        severity="error",
        message=err.message,
        expected=str(err.validator_value) if err.validator_value is not None else err.validator,
        actual=_stringify(err.instance),
    )


def _stringify(value: Any) -> str:
    """Stringify a JSON value for the `actual` field of ValidationWarning.

    Per § 5.1: '' when missing; otherwise stringified value.
    """
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return json.dumps(value, sort_keys=True)
