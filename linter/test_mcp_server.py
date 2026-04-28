"""
Tests for MCP server tool logic — conversus_validate and cost estimation.

Tests exercise the pure functions directly (no running MCP server needed).
Covers:
- Cost estimation formula for various agent/iteration/arbiter configs
- Validate tool with valid YAML config
- Validate tool with malformed YAML
- Validate tool with question classification (present and absent)
- Validate tool with non-dict YAML
- Cost estimate field accuracy
- Preset info extraction
- In-process execution via engine pipeline
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import pytest

# Import from project root mcp_server.py — add project root to path
# so pytest can find it regardless of invocation directory.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mcp_server import (
    CostEstimate,
    DecideResult,
    RunResult,
    ValidateResult,
    _decide,
    _estimate_cost,
    _run_config,
    _validate_config,
)


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

THREE_AGENT_CONFIG_YAML = """\
mode: cooperative
target: specs/001/spec.md
output: specs/001/conversus/
iterations: 1
agents:
  - name: agent-a
    prompt: "Agent A."
    docs: []
  - name: agent-b
    prompt: "Agent B."
    docs: []
  - name: agent-c
    prompt: "Agent C."
    docs: []
"""

ARBITER_CONFIG_YAML = """\
mode: cooperative
target: specs/001/spec.md
output: specs/001/conversus/
iterations: 1
agents:
  - name: agent-a
    prompt: "Agent A."
    docs: []
  - name: agent-b
    prompt: "Agent B."
    docs: []
arbiter:
  name: subject
  prompt: "You are the subject."
  docs: []
  grounding: constitution.md
  trigger: disputes_remain
"""

TWO_ITERATION_CONFIG_YAML = """\
mode: cooperative
target: specs/001/spec.md
output: specs/001/conversus/
iterations: 2
agents:
  - name: agent-a
    prompt: "Agent A."
    docs: []
  - name: agent-b
    prompt: "Agent B."
    docs: []
"""

MALFORMED_YAML = "{ invalid yaml: [unclosed"

NON_DICT_YAML = "- just\n- a\n- list"


# ---------------------------------------------------------------------------
# Cost estimation tests
# ---------------------------------------------------------------------------


class TestEstimateCost:
    """_estimate_cost pure function tests."""

    def test_two_agents_one_iteration(self) -> None:
        """D007: 2 agents, 1 iteration = 2+2+2+2+1 = 9 launches."""
        config = {"agents": [{"name": "a"}, {"name": "b"}], "iterations": 1}
        result = _estimate_cost(config)
        assert result.total_launches == 9
        assert result.agent_count == 2
        assert result.iteration_count == 1
        assert result.launches_per_phase["review"] == 2
        assert result.launches_per_phase["cross_review"] == 2
        assert result.launches_per_phase["revision"] == 2
        assert result.launches_per_phase["disputes"] == 2
        assert result.launches_per_phase["synthesis"] == 1

    def test_three_agents_one_iteration(self) -> None:
        """3 agents, 1 iteration = 3+6+3+3+1 = 16 launches."""
        config = {"agents": [{"name": "a"}, {"name": "b"}, {"name": "c"}], "iterations": 1}
        result = _estimate_cost(config)
        assert result.total_launches == 16
        assert result.launches_per_phase["review"] == 3
        assert result.launches_per_phase["cross_review"] == 6
        assert result.launches_per_phase["revision"] == 3
        assert result.launches_per_phase["disputes"] == 3
        assert result.launches_per_phase["synthesis"] == 1

    def test_arbiter_adds_one_launch(self) -> None:
        """Config with arbiter adds 1 arbitration launch."""
        config = {
            "agents": [{"name": "a"}, {"name": "b"}],
            "iterations": 1,
            "arbiter": {"name": "subject", "prompt": "You decide."},
        }
        result = _estimate_cost(config)
        assert result.total_launches == 10  # 9 + 1 arbitration
        assert result.launches_per_phase["arbitration"] == 1

    def test_no_arbiter_no_arbitration_phase(self) -> None:
        """Without arbiter, arbitration phase is absent from breakdown."""
        config = {"agents": [{"name": "a"}, {"name": "b"}], "iterations": 1}
        result = _estimate_cost(config)
        assert "arbitration" not in result.launches_per_phase

    def test_two_iterations_doubles_revision(self) -> None:
        """2 iterations: revision = agents × iterations = 2 × 2 = 4."""
        config = {"agents": [{"name": "a"}, {"name": "b"}], "iterations": 2}
        result = _estimate_cost(config)
        assert result.launches_per_phase["revision"] == 4
        # Total: 2+2+4+2+1 = 11
        assert result.total_launches == 11
        assert result.iteration_count == 2

    def test_default_iterations(self) -> None:
        """Missing iterations key defaults to 1."""
        config = {"agents": [{"name": "a"}, {"name": "b"}]}
        result = _estimate_cost(config)
        assert result.iteration_count == 1
        assert result.launches_per_phase["revision"] == 2

    def test_zero_agents(self) -> None:
        """Edge case: zero agents still returns a valid CostEstimate."""
        config = {"agents": []}
        result = _estimate_cost(config)
        assert result.total_launches == 1  # synthesis only
        assert result.agent_count == 0

    def test_returns_cost_estimate_model(self) -> None:
        """Return type is a CostEstimate Pydantic model."""
        config = {"agents": [{"name": "a"}], "iterations": 1}
        result = _estimate_cost(config)
        assert isinstance(result, CostEstimate)


# ---------------------------------------------------------------------------
# Validate tool logic tests
# ---------------------------------------------------------------------------


class TestValidateConfig:
    """_validate_config core logic tests."""

    def test_valid_config_returns_valid(self) -> None:
        """A well-formed config with existing templates passes validation."""
        result = _validate_config(VALID_CONFIG_YAML)
        assert isinstance(result, ValidateResult)
        assert result.valid is True
        assert result.errors == []

    def test_valid_config_has_cost_estimate(self) -> None:
        """Valid config produces a cost estimate."""
        result = _validate_config(VALID_CONFIG_YAML)
        assert result.cost_estimate is not None
        assert result.cost_estimate.agent_count == 2
        assert result.cost_estimate.total_launches == 9

    def test_valid_config_has_preset_info(self) -> None:
        """Valid config extracts preset info."""
        result = _validate_config(VALID_CONFIG_YAML)
        assert result.preset_info is not None
        assert any("cooperative" in p for p in result.preset_info)
        assert any("apm" in p for p in result.preset_info)

    def test_malformed_yaml_returns_invalid(self) -> None:
        """Malformed YAML returns valid=False with parse error."""
        result = _validate_config(MALFORMED_YAML)
        assert result.valid is False
        assert len(result.errors) == 1
        assert "YAML parse error" in result.errors[0]
        assert result.cost_estimate is None

    def test_non_dict_yaml_returns_invalid(self) -> None:
        """YAML that parses to a list returns valid=False."""
        result = _validate_config(NON_DICT_YAML)
        assert result.valid is False
        assert any("mapping" in e for e in result.errors)

    def test_question_classification_present(self) -> None:
        """When question is provided, classification field is populated."""
        question = "Should we use React or Vue for the dashboard given our team knows React?"
        result = _validate_config(VALID_CONFIG_YAML, question=question)
        assert result.classification is not None
        assert "sufficient" in result.classification
        assert isinstance(result.classification["sufficient"], bool)

    def test_question_classification_absent(self) -> None:
        """When no question is provided, classification is None."""
        result = _validate_config(VALID_CONFIG_YAML)
        assert result.classification is None

    def test_empty_question_no_classification(self) -> None:
        """Empty string question produces no classification."""
        result = _validate_config(VALID_CONFIG_YAML, question="")
        assert result.classification is None

    def test_whitespace_question_no_classification(self) -> None:
        """Whitespace-only question produces no classification."""
        result = _validate_config(VALID_CONFIG_YAML, question="   ")
        assert result.classification is None

    def test_three_agent_cost_in_validate(self) -> None:
        """Three-agent config returns correct cost through validate path."""
        result = _validate_config(THREE_AGENT_CONFIG_YAML)
        assert result.cost_estimate is not None
        assert result.cost_estimate.total_launches == 16
        assert result.cost_estimate.agent_count == 3

    def test_arbiter_cost_in_validate(self) -> None:
        """Arbiter config returns +1 launch through validate path."""
        result = _validate_config(ARBITER_CONFIG_YAML)
        assert result.cost_estimate is not None
        assert result.cost_estimate.total_launches == 10

    def test_two_iteration_cost_in_validate(self) -> None:
        """Two-iteration config through validate path."""
        result = _validate_config(TWO_ITERATION_CONFIG_YAML)
        assert result.cost_estimate is not None
        assert result.cost_estimate.total_launches == 11
        assert result.cost_estimate.iteration_count == 2


# ---------------------------------------------------------------------------
# Pydantic model tests
# ---------------------------------------------------------------------------


class TestPydanticModels:
    """Verify Pydantic models serialize correctly for MCP transport."""

    def test_cost_estimate_serialization(self) -> None:
        """CostEstimate serializes to JSON with all fields."""
        ce = CostEstimate(
            total_launches=9,
            launches_per_phase={"review": 2, "cross_review": 2, "revision": 2, "disputes": 2, "synthesis": 1},
            agent_count=2,
            iteration_count=1,
        )
        data = ce.model_dump()
        assert data["total_launches"] == 9
        assert len(data["launches_per_phase"]) == 5

    def test_validate_result_serialization(self) -> None:
        """ValidateResult serializes to JSON with optional fields."""
        vr = ValidateResult(valid=True, errors=[])
        data = vr.model_dump()
        assert data["valid"] is True
        assert data["cost_estimate"] is None
        assert data["classification"] is None
        assert data["preset_info"] is None

    def test_validate_result_with_all_fields(self) -> None:
        """ValidateResult with all fields populated serializes correctly."""
        ce = CostEstimate(
            total_launches=9,
            launches_per_phase={"review": 2},
            agent_count=2,
            iteration_count=1,
        )
        vr = ValidateResult(
            valid=False,
            errors=["some error"],
            cost_estimate=ce,
            classification={"sufficient": True, "reason": "ok"},
            preset_info=["mode: cooperative"],
        )
        data = vr.model_dump()
        assert data["valid"] is False
        assert len(data["errors"]) == 1
        assert data["cost_estimate"]["total_launches"] == 9
        assert data["classification"]["sufficient"] is True
        assert len(data["preset_info"]) == 1


# ---------------------------------------------------------------------------
# conversus_run tool logic tests
# ---------------------------------------------------------------------------

# Path to a real reference synthesis for parse-results mode testing
REFERENCE_SYNTHESIS_PATH = str(
    Path(__file__).resolve().parent.parent
    / "conversus"
    / "quality_floor"
    / "reference-outputs"
    / "passing"
    / "monorepo-vs-polyrepo"
    / "summary"
    / "final.md"
)


class TestRunConfig:
    """_run_config core logic tests — both validate-only and parsed-output modes."""

    def test_validate_only_mode_valid_config(self) -> None:
        """No output_path → validate-only mode with instructions."""
        result = _run_config(VALID_CONFIG_YAML)
        assert isinstance(result, RunResult)
        assert result.mode == "validate_only"
        assert result.validated is True
        assert result.errors == []
        assert result.instructions is not None
        assert "/conversus run" in result.instructions
        assert result.output is None

    def test_validate_only_mode_has_cost_estimate(self) -> None:
        """Validate-only mode still returns a cost estimate."""
        result = _run_config(VALID_CONFIG_YAML)
        assert result.cost_estimate is not None
        assert result.cost_estimate.agent_count == 2
        assert result.cost_estimate.total_launches == 9

    def test_empty_output_path_is_validate_only(self) -> None:
        """Empty string output_path behaves as validate-only mode."""
        result = _run_config(VALID_CONFIG_YAML, output_path="")
        assert result.mode == "validate_only"
        assert result.validated is True
        assert result.instructions is not None
        assert result.output is None

    def test_whitespace_output_path_is_validate_only(self) -> None:
        """Whitespace-only output_path behaves as validate-only mode."""
        result = _run_config(VALID_CONFIG_YAML, output_path="   ")
        assert result.mode == "validate_only"
        assert result.validated is True

    def test_parsed_output_mode_with_reference_file(self) -> None:
        """With a real synthesis file → parsed_output mode with structured output."""
        result = _run_config(VALID_CONFIG_YAML, output_path=REFERENCE_SYNTHESIS_PATH)
        assert result.mode == "parsed_output"
        assert result.validated is True
        assert result.errors == []
        assert result.output is not None
        # ConversusOutput fields must be present
        assert "headline" in result.output
        assert "summary" in result.output
        assert "full_analysis" in result.output
        assert "quality_indicators" in result.output
        assert "debate_transcript" in result.output

    def test_parsed_output_has_quality_indicators(self) -> None:
        """Parsed output contains quality indicators with expected fields."""
        result = _run_config(VALID_CONFIG_YAML, output_path=REFERENCE_SYNTHESIS_PATH)
        assert result.output is not None
        qi = result.output["quality_indicators"]
        assert "agent_count" in qi
        assert "mode" in qi
        assert "phases_completed" in qi
        assert qi["agent_count"] == 2
        assert qi["mode"] == "cooperative"

    def test_parsed_output_headline_nonempty(self) -> None:
        """Parsed output extracts a non-empty headline from the synthesis."""
        result = _run_config(VALID_CONFIG_YAML, output_path=REFERENCE_SYNTHESIS_PATH)
        assert result.output is not None
        assert len(result.output["headline"]) > 0

    def test_invalid_yaml_returns_error(self) -> None:
        """Malformed YAML → validated=False with parse error."""
        result = _run_config(MALFORMED_YAML)
        assert result.validated is False
        assert result.mode == "validate_only"
        assert len(result.errors) == 1
        assert "YAML parse error" in result.errors[0]
        assert result.cost_estimate is None

    def test_non_dict_yaml_returns_error(self) -> None:
        """YAML list → validated=False."""
        result = _run_config(NON_DICT_YAML)
        assert result.validated is False
        assert any("mapping" in e for e in result.errors)

    def test_missing_output_file_returns_error(self) -> None:
        """Non-existent output_path → error about missing file."""
        result = _run_config(VALID_CONFIG_YAML, output_path="/nonexistent/path/final.md")
        assert result.mode == "parsed_output"
        # Config itself may be valid, but the output file is missing
        assert any("not found" in e for e in result.errors)
        assert result.output is None

    def test_invalid_yaml_with_output_path(self) -> None:
        """Invalid YAML + output_path → validate-only mode (YAML fails first)."""
        result = _run_config(MALFORMED_YAML, output_path=REFERENCE_SYNTHESIS_PATH)
        assert result.validated is False
        assert "YAML parse error" in result.errors[0]

    def test_validate_only_with_invalid_config_has_instructions(self) -> None:
        """Invalid config in validate-only mode gets fix-first instructions."""
        result = _run_config(MALFORMED_YAML)
        assert result.instructions is not None
        assert "errors" in result.instructions.lower() or "fix" in result.instructions.lower()


# ---------------------------------------------------------------------------
# RunResult Pydantic model tests
# ---------------------------------------------------------------------------


class TestRunResultModel:
    """Verify RunResult Pydantic model serializes correctly for MCP transport."""

    def test_validate_only_serialization(self) -> None:
        """RunResult in validate-only mode serializes with all fields."""
        rr = RunResult(
            mode="validate_only",
            validated=True,
            errors=[],
            cost_estimate=CostEstimate(
                total_launches=9,
                launches_per_phase={"review": 2},
                agent_count=2,
                iteration_count=1,
            ),
            instructions="Config valid.",
        )
        data = rr.model_dump()
        assert data["mode"] == "validate_only"
        assert data["validated"] is True
        assert data["output"] is None
        assert data["instructions"] == "Config valid."
        assert data["cost_estimate"]["total_launches"] == 9

    def test_parsed_output_serialization(self) -> None:
        """RunResult in parsed_output mode serializes with output dict."""
        rr = RunResult(
            mode="parsed_output",
            validated=True,
            errors=[],
            output={"headline": "Test", "summary": "Test summary"},
        )
        data = rr.model_dump()
        assert data["mode"] == "parsed_output"
        assert data["output"]["headline"] == "Test"
        assert data["instructions"] is None

    def test_error_serialization(self) -> None:
        """RunResult with errors serializes correctly."""
        rr = RunResult(
            mode="validate_only",
            validated=False,
            errors=["YAML parse error: bad syntax", "Another error"],
        )
        data = rr.model_dump()
        assert data["validated"] is False
        assert len(data["errors"]) == 2
        assert data["cost_estimate"] is None

    def test_in_process_serialization(self) -> None:
        """RunResult in in_process mode serializes with round info."""
        rr = RunResult(
            mode="in_process",
            validated=True,
            errors=[],
            output={"headline": "Test"},
            rounds_completed=2,
            termination_reason="converged",
        )
        data = rr.model_dump()
        assert data["mode"] == "in_process"
        assert data["rounds_completed"] == 2
        assert data["termination_reason"] == "converged"
        assert data["output"]["headline"] == "Test"

    def test_round_fields_default_none(self) -> None:
        """RunResult round fields default to None for backward compat."""
        rr = RunResult(mode="validate_only", validated=True, errors=[])
        assert rr.rounds_completed is None
        assert rr.termination_reason is None


# ---------------------------------------------------------------------------
# In-process execution tests
# ---------------------------------------------------------------------------


def _make_in_process_config_yaml(base_dir: Path) -> str:
    """Build a valid YAML config string with real file paths in base_dir.

    Creates a target file and output directory so parse_config file
    resolution succeeds. The config uses paths relative to base_dir,
    so _run_in_process must write its temp config file there.
    """
    target = base_dir / "target.md"
    target.write_text("# Test Target\n\nSome spec content.\n", encoding="utf-8")

    output_dir = base_dir / "output"
    output_dir.mkdir(exist_ok=True)

    return """\
mode: cooperative
target: target.md
output: output/
iterations: 1
agents:
  - name: agent-a
    prompt: "You are Agent A."
    docs: []
  - name: agent-b
    prompt: "You are Agent B."
    docs: []
"""


class TestInProcessExecution:
    """Tests for in-process engine execution via _run_config(provider='mock')."""

    def test_run_in_process_mock_provider(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """In-process execution with mock provider returns RunResult(mode='in_process')."""
        monkeypatch.chdir(tmp_path)
        config_yaml = _make_in_process_config_yaml(tmp_path)

        result = _run_config(config_yaml=config_yaml, provider="mock")
        assert isinstance(result, RunResult)
        assert result.mode == "in_process"
        assert result.output is not None

    def test_run_in_process_output_has_fields(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """In-process output dict has expected ConversusOutput fields."""
        monkeypatch.chdir(tmp_path)
        config_yaml = _make_in_process_config_yaml(tmp_path)

        result = _run_config(config_yaml=config_yaml, provider="mock")
        assert result.output is not None
        # ConversusOutput should have at least these fields
        assert len(result.output) > 0
        assert result.rounds_completed is not None
        assert result.rounds_completed >= 1

    def test_run_in_process_invalid_config(self) -> None:
        """Malformed YAML with provider set returns errors."""
        result = _run_config(config_yaml=MALFORMED_YAML, provider="mock")
        # YAML parse fails before we get to in-process mode
        assert result.validated is False
        assert len(result.errors) > 0

    def test_run_in_process_unsupported_provider(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Unknown provider name returns error."""
        monkeypatch.chdir(tmp_path)
        config_yaml = _make_in_process_config_yaml(tmp_path)

        result = _run_config(config_yaml=config_yaml, provider="gemini")
        assert result.mode == "in_process"
        assert any("Unknown provider" in e for e in result.errors)
        assert result.output is None

    def test_validate_only_still_works(self) -> None:
        """Existing validate-only behavior unchanged (no provider, no output_path)."""
        result = _run_config(VALID_CONFIG_YAML)
        assert result.mode == "validate_only"
        assert result.validated is True
        assert result.instructions is not None
        assert "/conversus run" in result.instructions
        assert result.output is None

    def test_parsed_output_still_works(self) -> None:
        """Existing parsed-output behavior unchanged (output_path set)."""
        result = _run_config(VALID_CONFIG_YAML, output_path=REFERENCE_SYNTHESIS_PATH)
        assert result.mode == "parsed_output"
        assert result.validated is True
        assert result.output is not None
        assert "headline" in result.output

    def test_validate_still_works(self) -> None:
        """Existing _validate_config behavior unchanged."""
        result = _validate_config(VALID_CONFIG_YAML)
        assert isinstance(result, ValidateResult)
        assert result.valid is True
        assert result.errors == []
        assert result.cost_estimate is not None


# ---------------------------------------------------------------------------
# conversus_decide tool logic tests
# ---------------------------------------------------------------------------

# A detailed question that reliably passes the question classifier.
SUFFICIENT_QUESTION = (
    "Should we use SQLite or Postgres for our 10-user internal dashboard "
    "that needs to track project hours and generate monthly reports?"
)

# A vague question that gets rejected by the classifier.
INSUFFICIENT_QUESTION = "What should we do?"


class TestDecideConfig:
    """Tests for _decide() pure function and DecideResult model.

    Follows the same monkeypatch.chdir(tmp_path) isolation pattern used by
    TestInProcessExecution.  The _decide() function locates presets from
    mcp_server.py's parent directory, so CWD isolation does not break
    preset resolution — it only ensures temp files are written cleanly.
    """

    # ------------------------------------------------------------------
    # Sufficient question — full pipeline execution
    # ------------------------------------------------------------------

    def test_decide_sufficient_question_mock_provider(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Sufficient question + mock provider → DecideResult with successful output."""
        monkeypatch.chdir(tmp_path)
        result = _decide(SUFFICIENT_QUESTION, provider="mock")

        assert isinstance(result, DecideResult)
        assert result.sufficient is True
        assert result.output is not None
        assert result.rounds_completed is not None
        assert result.rounds_completed >= 1
        assert result.errors == []

    def test_decide_output_has_fields(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Output dict contains expected ConversusOutput fields."""
        monkeypatch.chdir(tmp_path)
        result = _decide(SUFFICIENT_QUESTION, provider="mock")

        assert result.output is not None
        assert "headline" in result.output
        assert "summary" in result.output
        assert "full_analysis" in result.output
        assert "quality_indicators" in result.output
        assert "debate_transcript" in result.output

    def test_decide_has_cost_estimate(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Successful execution includes a cost estimate."""
        monkeypatch.chdir(tmp_path)
        result = _decide(SUFFICIENT_QUESTION, provider="mock")

        assert result.cost_estimate is not None
        assert result.cost_estimate.agent_count == 2
        assert result.cost_estimate.total_launches == 9  # 2 agents, 1 iteration

    def test_decide_has_classification(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Sufficient question still populates the classification field."""
        monkeypatch.chdir(tmp_path)
        result = _decide(SUFFICIENT_QUESTION, provider="mock")

        assert result.classification is not None
        assert result.classification["sufficient"] is True

    # ------------------------------------------------------------------
    # Insufficient / empty / whitespace questions — rejection path
    # ------------------------------------------------------------------

    def test_decide_insufficient_question_rejected(self) -> None:
        """Vague question → sufficient=False with classification and error."""
        result = _decide(INSUFFICIENT_QUESTION, provider="mock")

        assert result.sufficient is False
        assert result.classification is not None
        assert result.classification["sufficient"] is False
        assert result.output is None
        assert len(result.errors) > 0

    def test_decide_empty_question_rejected(self) -> None:
        """Empty string → sufficient=False with errors."""
        result = _decide("", provider="mock")

        assert result.sufficient is False
        assert len(result.errors) > 0
        assert "empty" in result.errors[0].lower()
        assert result.output is None
        assert result.classification is None  # never reaches classifier

    def test_decide_whitespace_question_rejected(self) -> None:
        """Whitespace-only question treated as empty."""
        result = _decide("   \t\n  ", provider="mock")

        assert result.sufficient is False
        assert len(result.errors) > 0
        assert "empty" in result.errors[0].lower()
        assert result.output is None

    # ------------------------------------------------------------------
    # Provider errors
    # ------------------------------------------------------------------

    def test_decide_invalid_provider(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Unknown provider → question passes but execution errors."""
        monkeypatch.chdir(tmp_path)
        result = _decide(SUFFICIENT_QUESTION, provider="gemini")

        # Question should still pass classification
        assert result.sufficient is True
        assert result.classification is not None
        # But provider resolution fails
        assert len(result.errors) > 0
        assert any("provider" in e.lower() or "unknown" in e.lower() for e in result.errors)
        assert result.output is None

    # ------------------------------------------------------------------
    # Cost limit safeguard
    # ------------------------------------------------------------------

    def test_decide_cost_limit_exceeded(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """max_launches=1 refuses execution for 2-agent config (9 launches)."""
        monkeypatch.chdir(tmp_path)
        result = _decide(SUFFICIENT_QUESTION, provider="mock", max_launches=1)

        assert result.sufficient is True
        assert len(result.errors) > 0
        assert any("exceed" in e.lower() or "limit" in e.lower() for e in result.errors)
        assert result.output is None
        # Cost estimate should still be populated
        assert result.cost_estimate is not None
        assert result.cost_estimate.total_launches == 9

    def test_decide_cost_limit_default_allows(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Default max_launches=20 allows 2-agent config (9 launches)."""
        monkeypatch.chdir(tmp_path)
        result = _decide(SUFFICIENT_QUESTION, provider="mock")

        assert result.sufficient is True
        assert result.errors == []
        assert result.output is not None

    # ------------------------------------------------------------------
    # Mode parameter
    # ------------------------------------------------------------------

    def test_decide_mode_parameter(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """mode='red-blue' with default agents → config error about role requirement.

        The _decide() function uses pragmatist + devils-advocate presets, which
        lack the required role:red/role:blue tags for red-blue mode.  This test
        verifies the mode parameter is plumbed through and the config validation
        surfaces the error correctly.
        """
        monkeypatch.chdir(tmp_path)
        result = _decide(SUFFICIENT_QUESTION, provider="mock", mode="red-blue")

        assert result.sufficient is True  # question passes classification
        assert len(result.errors) > 0
        # Config validation should report the red-blue role requirement
        assert any("red" in e.lower() for e in result.errors)
        assert result.output is None

    def test_decide_cooperative_mode_succeeds(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Explicit mode='cooperative' → pipeline succeeds (default mode)."""
        monkeypatch.chdir(tmp_path)
        result = _decide(SUFFICIENT_QUESTION, provider="mock", mode="cooperative")

        assert result.sufficient is True
        assert result.errors == []
        assert result.output is not None

    # ------------------------------------------------------------------
    # DecideResult Pydantic model tests
    # ------------------------------------------------------------------

    def test_decide_result_serialization(self) -> None:
        """DecideResult round-trips through model_dump() / reconstruction."""
        dr = DecideResult(
            sufficient=True,
            classification={"sufficient": True, "reason": "ok"},
            output={"headline": "Test"},
            cost_estimate=CostEstimate(
                total_launches=9,
                launches_per_phase={"review": 2},
                agent_count=2,
                iteration_count=1,
            ),
            errors=[],
            rounds_completed=1,
            termination_reason="completed",
        )
        dumped = dr.model_dump()
        restored = DecideResult(**dumped)
        assert restored.sufficient is True
        assert restored.output == {"headline": "Test"}
        assert restored.rounds_completed == 1
        assert restored.termination_reason == "completed"
        assert restored.cost_estimate is not None
        assert restored.cost_estimate.total_launches == 9

    def test_decide_result_with_all_fields(self) -> None:
        """DecideResult with every field populated serializes correctly."""
        ce = CostEstimate(
            total_launches=10,
            launches_per_phase={"review": 2, "cross_review": 2, "revision": 2, "disputes": 2, "synthesis": 1, "arbitration": 1},
            agent_count=2,
            iteration_count=1,
        )
        dr = DecideResult(
            sufficient=False,
            classification={"sufficient": False, "reason": "vague", "missing_fields": ["context"]},
            output={"headline": "H", "summary": "S", "full_analysis": "F", "quality_indicators": {}, "debate_transcript": "T"},
            cost_estimate=ce,
            errors=["err1", "err2"],
            rounds_completed=3,
            termination_reason="max_rounds",
        )
        data = dr.model_dump()
        assert data["sufficient"] is False
        assert len(data["errors"]) == 2
        assert data["classification"]["missing_fields"] == ["context"]
        assert data["output"]["headline"] == "H"
        assert data["cost_estimate"]["total_launches"] == 10
        assert data["rounds_completed"] == 3
        assert data["termination_reason"] == "max_rounds"

    def test_decide_result_defaults(self) -> None:
        """DecideResult with only required field has correct defaults."""
        dr = DecideResult(sufficient=True)
        assert dr.classification is None
        assert dr.output is None
        assert dr.cost_estimate is None
        assert dr.errors == []
        assert dr.rounds_completed is None
        assert dr.termination_reason is None

    def test_decide_result_error_only(self) -> None:
        """DecideResult for error case serializes correctly."""
        dr = DecideResult(
            sufficient=True,
            errors=["Provider error: Unknown provider 'gemini'"],
        )
        data = dr.model_dump()
        assert data["sufficient"] is True
        assert len(data["errors"]) == 1
        assert data["output"] is None
        assert data["rounds_completed"] is None
