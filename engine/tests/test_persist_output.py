"""Tests for engine.persistence.persist_output — v4.2.0 spec § 5.1 D1.

The load-bearing invariant under test: ``path.write_bytes(content)`` is the
FIRST side effect, ALWAYS. No validation outcome can prevent the write. This
is Principle V (build-fractal/CONSTITUTION.md L76-78) operationalized in code.

Three failure-class proofs:
1. Conformant content writes + no sidecar + no event.
2. Non-conformant content writes + sidecar + event emitted.
3. Unparseable bytes (not JSON) write + sidecar + event emitted.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest

from engine.persistence import persist_output
from engine.schema_validator import SchemaValidator


SCHEMA_DIR = Path(__file__).resolve().parents[1] / "schema" / "v1"
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures" / "v4_2_0"


@dataclass
class _CapturingEventStream:
    """Test double for EventStream that records every warn() call."""

    events: list[dict[str, Any]] = field(default_factory=list)

    def warn(self, *, event: str, **fields: Any) -> None:
        self.events.append({"event": event, **fields})


@pytest.fixture(scope="module")
def validator() -> SchemaValidator:
    return SchemaValidator(SCHEMA_DIR)


def _read_conformant_envelope(output_type: str) -> bytes:
    return (FIXTURES_DIR / f"{output_type}.conformant.json").read_bytes()


def test_conformant_write_emits_no_warning_and_no_sidecar(
    validator: SchemaValidator, tmp_path: Path
) -> None:
    """Conformant output: file on disk, no sidecar, no event."""
    content = _read_conformant_envelope("review")
    target = tmp_path / "round-1" / "agent-a" / "review.json"
    stream = _CapturingEventStream()

    persist_output(target, content, validator, stream)

    assert target.read_bytes() == content
    assert not (target.parent / "review.json.validation-warnings.json").exists()
    assert stream.events == []


def test_non_conformant_write_persists_then_warns(
    validator: SchemaValidator, tmp_path: Path
) -> None:
    """Non-conformant output: file STILL on disk + sidecar + event emitted.

    Removes a required body field, so the validator returns is_conformant=False.
    The file content is preserved exactly as supplied — Principle V's whole point.
    """
    base = json.loads(_read_conformant_envelope("review"))
    del base["body"]["recommendation"]  # REQUIRED_FIELD_MISSING
    content = json.dumps(base).encode("utf-8")

    target = tmp_path / "review.json"
    stream = _CapturingEventStream()

    persist_output(target, content, validator, stream)

    # 1. File on disk, bytes intact.
    assert target.read_bytes() == content
    # 2. Sidecar exists with the right warning.
    sidecar = target.with_suffix(target.suffix + ".validation-warnings.json")
    assert sidecar.exists()
    payload = json.loads(sidecar.read_text())
    assert payload["is_conformant"] is False
    codes = {w["error_code"] for w in payload["warnings"]}
    assert "REQUIRED_FIELD_MISSING" in codes
    # 3. Event stream got exactly one warn() call.
    assert len(stream.events) == 1
    assert stream.events[0]["event"] == "schema_validation_failed"
    assert stream.events[0]["path"] == str(target)


def test_unparseable_bytes_still_write_to_disk(
    validator: SchemaValidator, tmp_path: Path
) -> None:
    """Garbage bytes: file on disk, sidecar + event still emitted.

    The validator surfaces a TYPE_MISMATCH at /; persist_output does not
    second-guess that and writes the bytes regardless. Recovery is downstream.
    """
    content = b"\x00\x01garbage bytes not even close to valid JSON"
    target = tmp_path / "phase-1" / "review.json"
    stream = _CapturingEventStream()

    persist_output(target, content, validator, stream)

    assert target.read_bytes() == content
    sidecar = target.with_suffix(target.suffix + ".validation-warnings.json")
    assert sidecar.exists()
    assert len(stream.events) == 1


def test_creates_parent_directories(
    validator: SchemaValidator, tmp_path: Path
) -> None:
    """persist_output mkdir-p's the parent. Phase writers expect this."""
    content = _read_conformant_envelope("synthesis")
    target = tmp_path / "deep" / "nested" / "round-2" / "summary" / "final.json"
    stream = _CapturingEventStream()

    persist_output(target, content, validator, stream)

    assert target.exists()


def test_write_happens_before_validation_returns(
    validator: SchemaValidator, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Even if validate() were to raise unexpectedly, the file is already written.

    Monkey-patches validate() to raise. The bytes MUST still be on disk after
    the exception propagates — proves the write is structurally first.
    """
    content = _read_conformant_envelope("disputes")
    target = tmp_path / "disputes.json"
    stream = _CapturingEventStream()

    def _explode(*_args: Any, **_kwargs: Any) -> Any:
        raise RuntimeError("simulated validator crash AFTER the write should have happened")

    monkeypatch.setattr(validator, "validate", _explode)

    with pytest.raises(RuntimeError, match="simulated validator crash"):
        persist_output(target, content, validator, stream)

    # The proof: bytes are on disk even though validate() exploded.
    assert target.read_bytes() == content
    # And no sidecar was written (validation never produced a result).
    assert not (target.parent / "disputes.json.validation-warnings.json").exists()
