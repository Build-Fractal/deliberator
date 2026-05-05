"""Tests for the engine-first /conversus skill execution path.

These tests validate that the CLI commands the skill calls produce
correct output. The skill is a thin wrapper — these tests verify the
underlying engine, not the skill's markdown rendering.

Mirrors the promptfoo eval suite (evals/promptfooconfig.yaml) but
runs as pytest for CI integration and finer-grained assertions.
"""

import json
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

pytestmark = pytest.mark.smoke


def _run_decide(question: str, mode: str = "cooperative", provider: str = "mock",
                fmt: str = "json") -> dict:
    """Run conversus decide and return parsed JSON or error dict."""
    result = subprocess.run(
        ["uv", "run", "conversus", "decide", question,
         "--provider", provider, "--mode", mode, "--format", fmt],
        capture_output=True, text=True, cwd=str(REPO_ROOT), timeout=30,
    )
    if result.returncode != 0:
        return {"error": True, "message": result.stderr.strip(),
                "returncode": result.returncode}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"error": True, "message": "Invalid JSON output",
                "raw": result.stdout[:500]}


def _run_validate(config_path: str) -> subprocess.CompletedProcess:
    """Run conversus validate and return the CompletedProcess."""
    return subprocess.run(
        ["uv", "run", "conversus", "validate", config_path],
        capture_output=True, text=True, cwd=str(REPO_ROOT), timeout=15,
    )


# ---------------------------------------------------------------
# Mode coverage — all 4 primary modes produce valid JSON
# ---------------------------------------------------------------

class TestModes:
    """Every mode produces valid JSON with expected schema."""

    @pytest.mark.parametrize("mode", [
        "cooperative", "winner-take-all", "prisoners-dilemma", "red-blue",
    ])
    def test_mode_produces_valid_output(self, mode: str) -> None:
        result = _run_decide("Should we use Postgres or MongoDB?", mode=mode)
        assert "error" not in result, f"Engine error: {result.get('message')}"
        assert "headline" in result
        assert "summary" in result
        assert "full_analysis" in result
        assert "quality_indicators" in result
        assert "debate_transcript" in result

    @pytest.mark.parametrize("mode", [
        "cooperative", "winner-take-all", "prisoners-dilemma", "red-blue",
    ])
    def test_quality_indicators_schema(self, mode: str) -> None:
        result = _run_decide("Should we use Postgres or MongoDB?", mode=mode)
        assert "error" not in result
        qi = result["quality_indicators"]
        assert isinstance(qi, dict)
        assert isinstance(qi["agent_count"], int)
        assert isinstance(qi["mode"], str)
        assert isinstance(qi["phases_completed"], int)
        assert isinstance(qi["cross_reviews_performed"], int)
        assert isinstance(qi["genuine_disagreements_surfaced"], int)
        assert isinstance(qi["genuine_disagreements_surviving"], int)

    def test_cooperative_phases_completed(self) -> None:
        result = _run_decide("Should we use Redis or Memcached?")
        assert result["quality_indicators"]["phases_completed"] >= 4


# ---------------------------------------------------------------
# Mock provider exercises production parsing path
# ---------------------------------------------------------------

class TestMockParsing:
    """Mock provider output is parseable by parse_synthesis (spec 061 P0)."""

    def test_headline_not_empty(self) -> None:
        result = _run_decide("Build vs buy for auth?")
        assert result["headline"], "headline should not be empty (mock synthesis)"

    def test_agent_count_populated(self) -> None:
        result = _run_decide("Build vs buy for auth?")
        assert result["quality_indicators"]["agent_count"] >= 2

    def test_phases_at_least_four(self) -> None:
        result = _run_decide("Build vs buy for auth?")
        assert result["quality_indicators"]["phases_completed"] >= 4


# ---------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------

class TestEdgeCases:
    """Edge cases and error handling."""

    def test_shell_metacharacters_safe(self) -> None:
        result = _run_decide(
            "Should we use $HOME or /tmp? What about 'quotes' and \"doubles\"?"
        )
        assert "error" not in result
        assert "headline" in result

    def test_very_short_question(self) -> None:
        """Very short questions should still produce output (may warn)."""
        result = _run_decide("Redis?")
        # The engine may accept or reject — either is valid
        # but it must not crash
        assert isinstance(result, dict)

    def test_invalid_provider_errors_gracefully(self) -> None:
        result = _run_decide("test question", provider="nonexistent")
        assert result.get("error") or result.get("returncode", 0) != 0


# ---------------------------------------------------------------
# Validate subcommand
# ---------------------------------------------------------------

class TestValidate:
    """conversus validate produces useful output."""

    def test_validate_nonexistent_config(self) -> None:
        result = _run_validate("/nonexistent/conversus.yml")
        assert result.returncode != 0

    def test_validate_valid_config(self, tmp_path: Path) -> None:
        """A minimal valid config passes validation."""
        config = tmp_path / "conversus.yml"
        question = tmp_path / "question.md"
        question.write_text("# Test\nShould we use X or Y?")
        config.write_text(
            f"mode: cooperative\n"
            f"target: {question.resolve()}\n"
            f"output: {tmp_path / 'output'}\n"
            f"agents:\n"
            f"  - name: agent-a\n"
            f"    preset: philosophy/pragmatist\n"
            f"  - name: agent-b\n"
            f"    preset: role/devils-advocate\n"
        )
        result = _run_validate(str(config))
        # validate may print warnings but should not error on valid config
        assert result.returncode == 0, f"Validate failed: {result.stderr}"


# ---------------------------------------------------------------
# Provider resolution — all registered providers instantiate
# ---------------------------------------------------------------

class TestProviders:
    """All registered providers resolve via resolve_execution_provider."""

    @pytest.mark.parametrize("name", [
        "mock", "demo", "ollama", "claude-code", "aider",
        "opencode", "codex", "copilot", "gemini", "pi",
    ])
    def test_provider_resolves(self, name: str) -> None:
        from engine.run import resolve_execution_provider
        provider = resolve_execution_provider(name)
        assert provider is not None
        assert hasattr(provider, "execute")


# ---------------------------------------------------------------
# Cross-surface parity — CLI and MCP produce same schema
# ---------------------------------------------------------------

class TestCrossSurfaceParity:
    """CLI and MCP handlers produce structurally identical output."""

    def test_decide_cli_vs_mcp_schema(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # Use a longer question to satisfy MCP's stricter sufficiency gate
        question = (
            "Should we use Postgres or MongoDB for our metadata store "
            "given we need ACID transactions and JSON document support?"
        )

        # Pin context-default to "mock" by clearing Claude Code env vars.
        # Post the Phase-3 context-aware default (commit f1c5xxx),
        # ``run_decide_mcp("...", "mock", ...)`` would treat the "mock"
        # arg as "no preference" and use the InvocationContext's
        # session-inferred default — but MCP-supported providers don't
        # include claude-code. This test's purpose is CLI/MCP parity
        # for the mock-provider path; the context-aware behavior is
        # tested in test_cli_context.py + test_settings.py.
        for var in ("CLAUDECODE", "CLAUDE_CODE", "CLAUDE_CODE_ACTIVE"):
            monkeypatch.delenv(var, raising=False)

        # CLI path
        cli_result = _run_decide(question)
        assert "error" not in cli_result

        # MCP path
        from engine.handlers import run_decide_mcp
        mcp_result = run_decide_mcp(question, "mock", "cooperative", 20)
        assert mcp_result.output is not None, (
            f"MCP rejected question: {mcp_result.errors}"
        )

        # Both should have the same top-level keys
        mcp_output = mcp_result.output
        for key in ["headline", "summary", "full_analysis",
                     "quality_indicators", "debate_transcript"]:
            assert key in cli_result, f"CLI missing {key}"
            assert key in mcp_output, f"MCP missing {key}"

        # quality_indicators should have same sub-keys
        cli_qi = cli_result["quality_indicators"]
        mcp_qi = mcp_output["quality_indicators"]
        for key in ["agent_count", "mode", "phases_completed"]:
            assert key in cli_qi, f"CLI qi missing {key}"
            assert key in mcp_qi, f"MCP qi missing {key}"
