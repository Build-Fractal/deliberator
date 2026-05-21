"""
End-to-end integration tests for the conversus M001 pipeline.

Exercises every cross-module boundary that S01–S07 built in isolation:
  quality gate → output contract → MCP server → usage logging → question classifier

Uses existing reference outputs as fixtures — no synthetic data.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

pytest.importorskip("mcp")

# ---------------------------------------------------------------------------
# Import linter modules (same pattern as test_quality.py)
# ---------------------------------------------------------------------------

try:
    from .quality import QualityResult, check_quality_floor
except ImportError:
    from quality import QualityResult, check_quality_floor

try:
    from .output_contract import ConversusOutput, parse_synthesis
except ImportError:
    from output_contract import ConversusOutput, parse_synthesis

try:
    from .usage import AdoptionMetrics, UsageEntry, log_usage, summarize_usage
except ImportError:
    from usage import AdoptionMetrics, UsageEntry, log_usage, summarize_usage

try:
    from .question_classifier import ClassificationResult, classify_question
except ImportError:
    from question_classifier import ClassificationResult, classify_question

# Import MCP server functions (project-root module, same pattern as test_mcp_server.py)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mcp_server import RunResult, ValidateResult, _run_config, _validate_config


# ---------------------------------------------------------------------------
# Reference paths
# ---------------------------------------------------------------------------

_PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
_REF_ROOT: Path = _PROJECT_ROOT / "conversus" / "quality_floor" / "reference-outputs"

_PASSING_SYNTHESIS: Path = _REF_ROOT / "passing" / "monorepo-vs-polyrepo" / "summary" / "final.md"
_FAILING_SYNTHESIS: Path = _REF_ROOT / "failing" / "factual-capital" / "summary" / "final.md"
_QUESTION_FILE: Path = _PROJECT_ROOT / "conversus" / "quality_floor" / "questions" / "monorepo-vs-polyrepo.md"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

VALID_CONFIG_YAML = """\
mode: cooperative
target: specs/001-speckit-orchestrator/spec.md
output: specs/001-speckit-orchestrator/conversus/
iterations: 1
agents:
  - name: apm
    prompt: "You are APM."
    docs:
      - apm/docs/
  - name: spec-kit
    prompt: "You are spec-kit."
    docs:
      - spec-kit/README.md
"""

MALFORMED_YAML = "{ invalid yaml: [unclosed"


@pytest.fixture(scope="session")
def passing_text() -> str:
    """Load passing monorepo-vs-polyrepo synthesis text."""
    assert _PASSING_SYNTHESIS.exists(), f"Missing: {_PASSING_SYNTHESIS}"
    return _PASSING_SYNTHESIS.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def failing_text() -> str:
    """Load failing factual-capital synthesis text."""
    assert _FAILING_SYNTHESIS.exists(), f"Missing: {_FAILING_SYNTHESIS}"
    return _FAILING_SYNTHESIS.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Test a) — Full pipeline: quality gate + output contract + usage logging
# ---------------------------------------------------------------------------


class TestPassingSynthesisFullPipeline:
    """Exercises quality gate → output contract → usage logging → metrics
    on the passing monorepo-vs-polyrepo synthesis."""

    def test_quality_floor_passes(self, passing_text: str) -> None:
        result = check_quality_floor(passing_text)
        assert isinstance(result, QualityResult)
        assert result.passed is True

    def test_output_contract_all_5_fields(self, passing_text: str) -> None:
        output = parse_synthesis(passing_text)
        assert isinstance(output, ConversusOutput)
        assert len(output.headline) > 0, "headline must be non-empty"
        assert len(output.summary) > 0, "summary must be non-empty"
        assert len(output.full_analysis) > 0, "full_analysis must be non-empty"
        assert output.quality_indicators is not None, "quality_indicators must be present"
        assert len(output.debate_transcript) > 0, "debate_transcript must be non-empty"

    def test_usage_logging_and_metrics(self, passing_text: str, tmp_path: Path) -> None:
        """Log a usage entry for the passing synthesis and verify metrics."""
        usage_file = tmp_path / "usage.jsonl"

        quality_result = check_quality_floor(passing_text)
        quality_dict = json.loads(quality_result.model_dump_json())

        entry = log_usage(
            synthesis_path=str(_PASSING_SYNTHESIS),
            question_path=str(_QUESTION_FILE),
            quality_json=quality_dict,
            fallback_used=False,
            usage_file=str(usage_file),
        )
        assert isinstance(entry, UsageEntry)

        # Verify the JSONL file has exactly 1 line
        lines = [l for l in usage_file.read_text().strip().splitlines() if l.strip()]
        assert len(lines) == 1, f"Expected 1 JSONL line, got {len(lines)}"

        # Verify metrics from the log
        metrics = summarize_usage(str(usage_file))
        assert isinstance(metrics, AdoptionMetrics)
        assert metrics.total_runs == 1


# ---------------------------------------------------------------------------
# Test b) — Failing synthesis detected but still parseable
# ---------------------------------------------------------------------------


class TestFailingSynthesisDetected:
    """Verifies the quality gate rejects low-quality output while the
    output contract still parses it gracefully."""

    def test_quality_floor_fails(self, failing_text: str) -> None:
        result = check_quality_floor(failing_text)
        assert result.passed is False

    def test_output_contract_still_parseable(self, failing_text: str) -> None:
        """Output contract handles low-quality output gracefully — no crash."""
        output = parse_synthesis(failing_text)
        assert isinstance(output, ConversusOutput)
        # All 5 fields should still be present (even if quality is low)
        assert output.headline is not None
        assert output.summary is not None
        assert output.full_analysis is not None
        assert output.quality_indicators is not None
        assert output.debate_transcript is not None


# ---------------------------------------------------------------------------
# Test c) — MCP validate accepts valid config
# ---------------------------------------------------------------------------


def test_mcp_validate_accepts_valid_config() -> None:
    """_validate_config with a well-formed cooperative YAML returns valid=True."""
    result = _validate_config(VALID_CONFIG_YAML)
    assert isinstance(result, ValidateResult)
    assert result.valid is True
    assert result.cost_estimate is not None
    assert result.cost_estimate.agent_count == 2
    assert result.cost_estimate.total_launches == 9


# ---------------------------------------------------------------------------
# Test d) — MCP validate rejects malformed YAML
# ---------------------------------------------------------------------------


def test_mcp_validate_rejects_invalid_config() -> None:
    """_validate_config with malformed YAML returns valid=False."""
    result = _validate_config(MALFORMED_YAML)
    assert isinstance(result, ValidateResult)
    assert result.valid is False
    assert len(result.errors) > 0
    assert any("YAML parse error" in e for e in result.errors)


# ---------------------------------------------------------------------------
# Test e) — MCP run parses reference synthesis
# ---------------------------------------------------------------------------


def test_mcp_run_parses_reference_synthesis() -> None:
    """_run_config with output_path pointing to passing synthesis returns
    parsed_output mode with all 5 output contract fields."""
    result = _run_config(VALID_CONFIG_YAML, output_path=str(_PASSING_SYNTHESIS))
    assert isinstance(result, RunResult)
    assert result.mode == "parsed_output"
    assert result.output is not None

    # All 5 contract fields must be present
    for field in ("headline", "summary", "full_analysis", "quality_indicators", "debate_transcript"):
        assert field in result.output, f"Missing output contract field: {field}"
        assert result.output[field], f"Output contract field '{field}' is empty"


# ---------------------------------------------------------------------------
# Test f) — Question classifier integration
# ---------------------------------------------------------------------------


class TestQuestionClassifierIntegration:
    """Exercises classify_question for sufficient and insufficient inputs."""

    def test_sufficient_question(self) -> None:
        result = classify_question(
            "Should I use a monorepo or polyrepo for my 15-person team?",
            mode="interactive",
        )
        assert isinstance(result, ClassificationResult)
        assert result.sufficient is True

    def test_insufficient_vague_question(self) -> None:
        result = classify_question("help", mode="interactive")
        assert isinstance(result, ClassificationResult)
        assert result.sufficient is False
        assert result.clarification_question is not None
        assert len(result.clarification_question) > 0


# ---------------------------------------------------------------------------
# Test g) — Full pipeline composition
# ---------------------------------------------------------------------------


def test_full_pipeline_compose(tmp_path: Path) -> None:
    """Combines every module boundary in sequence:
    classify question → validate config → run config → check quality floor
    → parse output contract → log usage → summarize metrics.

    Each step uses the real output, not mocks.
    """
    # Step 1: Classify a sufficient question
    classification = classify_question(
        "Should I use a monorepo or polyrepo for my 15-person team?",
        mode="interactive",
    )
    assert classification.sufficient is True, "Pre-condition: question must be sufficient"

    # Step 2: Validate config
    validation = _validate_config(VALID_CONFIG_YAML)
    assert validation.valid is True, "Pre-condition: config must be valid"

    # Step 3: Run config with synthesis path
    run_result = _run_config(VALID_CONFIG_YAML, output_path=str(_PASSING_SYNTHESIS))
    assert run_result.mode == "parsed_output"
    assert run_result.output is not None

    # Step 4: Check quality floor on the synthesis text
    synthesis_text = _PASSING_SYNTHESIS.read_text(encoding="utf-8")
    quality_result = check_quality_floor(synthesis_text)
    assert quality_result.passed is True

    # Step 5: Parse output contract
    output = parse_synthesis(synthesis_text)
    assert isinstance(output, ConversusOutput)
    assert len(output.headline) > 0

    # Step 6: Log usage to temp file
    usage_file = tmp_path / "usage.jsonl"
    quality_dict = json.loads(quality_result.model_dump_json())
    entry = log_usage(
        synthesis_path=str(_PASSING_SYNTHESIS),
        question_path=str(_QUESTION_FILE),
        quality_json=quality_dict,
        fallback_used=False,
        usage_file=str(usage_file),
    )
    assert isinstance(entry, UsageEntry)

    # Step 7: Summarize metrics
    metrics = summarize_usage(str(usage_file))
    assert isinstance(metrics, AdoptionMetrics)
    assert metrics.total_runs == 1
    assert metrics.trust_rate == 1.0  # single passing run → 100% trust
