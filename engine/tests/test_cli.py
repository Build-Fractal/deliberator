"""Integration tests for the conversus CLI (all 5 subcommands).

Uses Click's ``CliRunner`` to exercise ``run``, ``decide``, ``validate``,
``login``, and ``logout`` without subprocess overhead.  Provider and auth
layers are mocked where needed so no real LLM calls or browser opens occur.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest
import yaml
from click.testing import CliRunner

from engine.cli import cli


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_valid_config(tmp_path: Path) -> Path:
    """Write a minimal valid conversus config and return its path.

    Creates the target spec file that the config references so
    ``parse_config`` resolves successfully.
    """
    spec = tmp_path / "spec.md"
    spec.write_text("# Test Spec\n\nContent for testing.\n", encoding="utf-8")

    config_data = {
        "mode": "cooperative",
        "target": "spec.md",
        "output": str(tmp_path / "output"),
        "iterations": 1,
        "agents": [
            {"name": "agent-alpha", "prompt": "Alpha perspective."},
            {"name": "agent-beta", "prompt": "Beta perspective."},
        ],
    }
    config_path = tmp_path / "conversus.yml"
    config_path.write_text(yaml.dump(config_data, sort_keys=False), encoding="utf-8")
    return config_path


def _write_invalid_config(tmp_path: Path) -> Path:
    """Write a config with an invalid mode so ``parse_config`` raises ``ConfigError``."""
    spec = tmp_path / "spec.md"
    spec.write_text("# Bad Spec\n", encoding="utf-8")

    config_data = {
        "mode": "nonexistent-mode",
        "target": "spec.md",
        "output": str(tmp_path / "output"),
        "agents": [
            {"name": "a1", "prompt": "P1"},
        ],
    }
    config_path = tmp_path / "conversus.yml"
    config_path.write_text(yaml.dump(config_data, sort_keys=False), encoding="utf-8")
    return config_path


# ---------------------------------------------------------------------------
# --help
# ---------------------------------------------------------------------------


class TestHelp:
    """Top-level --help lists all 5 subcommands."""

    def test_help_shows_all_commands(self) -> None:
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        for cmd in ("run", "decide", "validate", "login", "logout", "status"):
            assert cmd in result.output, f"Missing subcommand '{cmd}' in --help output"

    def test_help_exit_code_zero(self) -> None:
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0

    def test_group_help_has_examples(self) -> None:
        """Top-level ``conversus --help`` includes usage examples."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "example" in result.output.lower(), (
            f"Missing 'Example' in group --help output:\n{result.output[:500]}"
        )

    def test_all_commands_have_examples(self) -> None:
        """Every command's ``--help`` includes usage examples."""
        runner = CliRunner()
        for cmd in ("run", "decide", "validate", "login", "logout", "status"):
            result = runner.invoke(cli, [cmd, "--help"])
            assert result.exit_code == 0, f"{cmd} --help exited with {result.exit_code}"
            assert "example" in result.output.lower(), (
                f"Missing 'Example' in '{cmd} --help' output:\n{result.output[:500]}"
            )


# ---------------------------------------------------------------------------
# run
# ---------------------------------------------------------------------------


class TestRunCommand:
    """Tests for ``conversus run``."""

    def test_run_valid_config_mock(self, tmp_path: Path) -> None:
        """Run with a valid config and mock provider exits 0."""
        config_path = _write_valid_config(tmp_path)
        runner = CliRunner()
        result = runner.invoke(cli, ["run", str(config_path), "--provider", "mock"])
        assert result.exit_code == 0, f"stdout: {result.output}"

    def test_run_missing_config(self, tmp_path: Path) -> None:
        """Run with a nonexistent config path exits non-zero."""
        runner = CliRunner()
        nonexistent = str(tmp_path / "does_not_exist.yml")
        result = runner.invoke(cli, ["run", nonexistent])
        assert result.exit_code != 0

    def test_run_invalid_config(self, tmp_path: Path) -> None:
        """Run with an invalid mode in config exits 1 with error message."""
        config_path = _write_invalid_config(tmp_path)
        runner = CliRunner()
        result = runner.invoke(cli, ["run", str(config_path), "--provider", "mock"])
        assert result.exit_code != 0
        # Error message should appear in output or stderr
        combined = result.output + (result.stderr_bytes or b"").decode("utf-8", errors="replace")
        assert "error" in combined.lower() or "Error" in combined

    def test_run_help(self) -> None:
        """``conversus run --help`` exits 0 and shows options."""
        runner = CliRunner()
        result = runner.invoke(cli, ["run", "--help"])
        assert result.exit_code == 0
        assert "provider" in result.output.lower()

    def test_run_invalid_provider_rejected(self, tmp_path: Path) -> None:
        """Click rejects an invalid --provider choice."""
        config_path = _write_valid_config(tmp_path)
        runner = CliRunner()
        result = runner.invoke(cli, ["run", str(config_path), "--provider", "gemini"])
        assert result.exit_code != 0

    def test_run_output_contains_file_paths(self, tmp_path: Path) -> None:
        """Successful run prints output file paths to stdout."""
        config_path = _write_valid_config(tmp_path)
        runner = CliRunner()
        result = runner.invoke(cli, ["run", str(config_path), "--provider", "mock"])
        assert result.exit_code == 0
        # Should print paths to the written files
        assert ".md" in result.output


# ---------------------------------------------------------------------------
# validate
# ---------------------------------------------------------------------------


class TestValidateCommand:
    """Tests for ``conversus validate``."""

    def test_validate_valid_config(self, tmp_path: Path) -> None:
        """Validate with valid config exits 0 and prints cost estimate."""
        config_path = _write_valid_config(tmp_path)
        runner = CliRunner()
        result = runner.invoke(cli, ["validate", str(config_path)])
        assert result.exit_code == 0
        assert "launch" in result.output.lower() or "cost" in result.output.lower()

    def test_validate_invalid_config(self, tmp_path: Path) -> None:
        """Validate with invalid config exits non-zero."""
        config_path = _write_invalid_config(tmp_path)
        runner = CliRunner()
        result = runner.invoke(cli, ["validate", str(config_path)])
        assert result.exit_code != 0

    def test_validate_shows_mode(self, tmp_path: Path) -> None:
        """Validate output includes the deliberation mode."""
        config_path = _write_valid_config(tmp_path)
        runner = CliRunner()
        result = runner.invoke(cli, ["validate", str(config_path)])
        assert result.exit_code == 0
        assert "cooperative" in result.output.lower()

    def test_validate_with_question(self, tmp_path: Path) -> None:
        """Validate with --question shows classification info."""
        config_path = _write_valid_config(tmp_path)
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["validate", str(config_path), "--question", "Should we use microservices or a monolith?"],
        )
        assert result.exit_code == 0
        assert "classification" in result.output.lower()

    def test_validate_missing_config(self, tmp_path: Path) -> None:
        """Validate with nonexistent config path exits non-zero."""
        runner = CliRunner()
        nonexistent = str(tmp_path / "nope.yml")
        result = runner.invoke(cli, ["validate", nonexistent])
        assert result.exit_code != 0

    def test_validate_help(self) -> None:
        """``conversus validate --help`` exits 0."""
        runner = CliRunner()
        result = runner.invoke(cli, ["validate", "--help"])
        assert result.exit_code == 0
        assert "question" in result.output.lower()


# ---------------------------------------------------------------------------
# login
# ---------------------------------------------------------------------------


class TestLoginCommand:
    """Tests for ``conversus login``."""

    def test_login_unknown_provider(self) -> None:
        """Login with an unknown provider exits 1."""
        runner = CliRunner()
        result = runner.invoke(cli, ["login", "unknown_provider"])
        assert result.exit_code != 0
        combined = result.output
        assert "error" in combined.lower() or "unknown" in combined.lower()

    @patch("engine.auth.login")
    def test_login_mock_oauth(self, mock_login) -> None:
        """Login with mocked OAuth flow exits 0 and prints success."""
        mock_login.return_value = {"access_token": "fake-token-12345"}
        runner = CliRunner()
        result = runner.invoke(cli, ["login", "anthropic"])
        assert result.exit_code == 0
        assert "success" in result.output.lower()
        mock_login.assert_called_once_with("anthropic")

    @patch("engine.auth.login")
    def test_login_openai_provider(self, mock_login) -> None:
        """Login with openai provider works when mocked."""
        mock_login.return_value = {"access_token": "openai-fake-key"}
        runner = CliRunner()
        result = runner.invoke(cli, ["login", "openai"])
        assert result.exit_code == 0
        assert "success" in result.output.lower()
        mock_login.assert_called_once_with("openai")

    @patch("engine.auth.login")
    def test_login_provider_error_propagates(self, mock_login) -> None:
        """Login that raises ProviderError exits 1 with error message."""
        from engine.providers import ProviderError

        mock_login.side_effect = ProviderError("OAuth flow failed", category="auth")
        runner = CliRunner()
        result = runner.invoke(cli, ["login", "anthropic"])
        assert result.exit_code != 0
        assert "error" in result.output.lower()

    def test_login_help(self) -> None:
        """``conversus login --help`` exits 0."""
        runner = CliRunner()
        result = runner.invoke(cli, ["login", "--help"])
        assert result.exit_code == 0


# ---------------------------------------------------------------------------
# logout
# ---------------------------------------------------------------------------


class TestLogoutCommand:
    """Tests for ``conversus logout``."""

    @patch("engine.auth.logout")
    def test_logout_provider(self, mock_logout) -> None:
        """Logout for a known provider exits 0 and prints confirmation."""
        runner = CliRunner()
        result = runner.invoke(cli, ["logout", "anthropic"])
        assert result.exit_code == 0
        assert "logged out" in result.output.lower()
        mock_logout.assert_called_once_with("anthropic")

    @patch("engine.auth.logout")
    def test_logout_openai(self, mock_logout) -> None:
        """Logout for openai exits 0."""
        runner = CliRunner()
        result = runner.invoke(cli, ["logout", "openai"])
        assert result.exit_code == 0
        assert "logged out" in result.output.lower()

    def test_logout_help(self) -> None:
        """``conversus logout --help`` exits 0."""
        runner = CliRunner()
        result = runner.invoke(cli, ["logout", "--help"])
        assert result.exit_code == 0


# ---------------------------------------------------------------------------
# decide
# ---------------------------------------------------------------------------


class TestDecideCommand:
    """Tests for ``conversus decide``."""

    def test_decide_with_mock_provider(self) -> None:
        """Decide with mock provider completes and prints formatted output."""
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["decide", "Should we use SQLite or Postgres?", "--provider", "mock"],
        )
        assert result.exit_code == 0, f"stderr: {result.output}"
        # Should contain some output text from the formatted results
        assert len(result.output.strip()) > 0

    def test_decide_empty_question(self) -> None:
        """Decide with empty question exits 1."""
        runner = CliRunner()
        result = runner.invoke(cli, ["decide", "", "--provider", "mock"])
        assert result.exit_code != 0
        assert "empty" in result.output.lower() or "error" in result.output.lower()

    def test_decide_whitespace_only_question(self) -> None:
        """Decide with whitespace-only question exits 1."""
        runner = CliRunner()
        result = runner.invoke(cli, ["decide", "   ", "--provider", "mock"])
        assert result.exit_code != 0

    def test_decide_help(self) -> None:
        """``conversus decide --help`` exits 0 and mentions question."""
        runner = CliRunner()
        result = runner.invoke(cli, ["decide", "--help"])
        assert result.exit_code == 0
        assert "question" in result.output.lower()

    def test_decide_insufficient_question_warns(self) -> None:
        """A very short question still runs (mock) but emits a warning."""
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["decide", "help", "--provider", "mock"],
        )
        # Should still exit 0 with mock provider (warning doesn't block)
        assert result.exit_code == 0, f"output: {result.output}"
        # Warning text should appear in the output (stderr is mixed with stdout in CliRunner)
        # The classify_question returns insufficient for very short queries
        # and the decide command echoes "Warning: ..." to stderr, which CliRunner captures in output
        assert "warning" in result.output.lower() or "insufficient" in result.output.lower()

    def test_decide_custom_output_dir(self, tmp_path: Path) -> None:
        """Decide with --output persists files to the specified directory."""
        output_dir = tmp_path / "decide-output"
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "decide",
                "Should we use SQLite or Postgres for the new project?",
                "--provider",
                "mock",
                "--output",
                str(output_dir),
            ],
        )
        assert result.exit_code == 0, f"output: {result.output}"
        # Output files should exist in the specified directory
        assert output_dir.exists()
        assert (output_dir / "summary" / "final.md").exists()

    def test_decide_prints_headline(self) -> None:
        """Decide output includes Deliberation Result panel."""
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["decide", "Should we adopt Kubernetes or stay with Docker Compose?", "--provider", "mock"],
        )
        assert result.exit_code == 0
        assert "deliberation result" in result.output.lower()

    def test_decide_prints_quality_indicators(self) -> None:
        """Decide output includes Quality Indicators section."""
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["decide", "Should we use a message queue or direct API calls?", "--provider", "mock"],
        )
        assert result.exit_code == 0
        assert "quality indicators" in result.output.lower()

    def test_decide_no_ansi_in_piped_output(self) -> None:
        """Piped output from decide contains no ANSI escape codes.

        CliRunner captures stdout to StringIO, which Rich detects as
        non-TTY and auto-strips all ANSI escape sequences.  This proves
        that piped invocations (``conversus decide ... | cat``) produce
        clean, human-readable output with zero ANSI codes.
        """
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["decide", "Should we use microservices?", "--provider", "mock"],
        )
        assert result.exit_code == 0, f"output: {result.output}"

        # Core proof: no ANSI escape codes in stdout
        assert "\x1b[" not in result.output, (
            f"ANSI escape codes found in piped output:\n{result.output[:500]}"
        )

        # Content still present: headline rendered by Rich Panel
        output_lower = result.output.lower()
        assert "deliberation result" in output_lower or "headline" in output_lower, (
            f"Expected headline content in output:\n{result.output[:500]}"
        )

        # Quality indicators still present
        assert "quality indicators" in output_lower, (
            f"Expected quality indicators in output:\n{result.output[:500]}"
        )


# ---------------------------------------------------------------------------
# decide --format json
# ---------------------------------------------------------------------------


class TestDecideJsonFormat:
    """Tests for ``conversus decide --format json``."""

    def test_decide_json_format_outputs_valid_json(self) -> None:
        """``--format json`` emits valid JSON with all ConversusOutput fields."""
        import json

        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["decide", "Should we use SQLite or Postgres?", "--provider", "mock", "--format", "json"],
        )
        assert result.exit_code == 0, f"stdout: {result.stdout}\nstderr: {result.stderr_bytes}"

        data = json.loads(result.stdout)
        for key in ("headline", "summary", "quality_indicators", "full_analysis", "debate_transcript"):
            assert key in data, f"Missing key '{key}' in JSON output"

    def test_decide_json_format_no_ansi(self) -> None:
        """``--format json`` output contains zero ANSI escape sequences."""
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["decide", "Should we adopt Kubernetes?", "--provider", "mock", "--format", "json"],
        )
        assert result.exit_code == 0, f"stdout: {result.stdout}\nstderr: {result.stderr_bytes}"
        assert "\x1b[" not in result.stdout, (
            f"ANSI escape codes found in JSON output:\n{result.stdout[:500]}"
        )

    def test_decide_default_format_uses_rich(self) -> None:
        """Without ``--format``, decide uses Rich rendering (panel title visible)."""
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["decide", "Should we use a message queue?", "--provider", "mock"],
        )
        assert result.exit_code == 0, f"output: {result.output}"
        assert "deliberation result" in result.output.lower(), (
            f"Expected Rich panel title in default output:\n{result.output[:500]}"
        )

    def test_decide_json_quality_indicators_fields(self) -> None:
        """JSON quality_indicators contains all expected sub-fields."""
        import json

        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["decide", "Monolith vs microservices?", "--provider", "mock", "--format", "json"],
        )
        assert result.exit_code == 0, f"stdout: {result.stdout}\nstderr: {result.stderr_bytes}"

        data = json.loads(result.stdout)
        qi = data["quality_indicators"]
        for key in ("agent_count", "mode", "phases_completed", "cross_reviews_performed",
                     "genuine_disagreements_surfaced", "genuine_disagreements_surviving"):
            assert key in qi, f"Missing quality_indicators sub-key '{key}'"


# ---------------------------------------------------------------------------
# status
# ---------------------------------------------------------------------------


class TestStatusCommand:
    """Tests for ``conversus status``."""

    def test_status_no_credentials(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Status with no stored credentials and no env vars shows 'not configured'."""
        auth_path = tmp_path / "auth.json"
        monkeypatch.setattr("engine.auth.DEFAULT_AUTH_PATH", auth_path)
        # Clear env vars so they don't interfere
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        runner = CliRunner()
        result = runner.invoke(cli, ["status"])
        assert result.exit_code == 0
        assert "not configured" in result.output.lower()

    def test_status_with_stored_credentials(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Status with stored OAuth credentials shows 'logged in'."""
        import json
        import time

        auth_path = tmp_path / "auth.json"
        creds = {
            "anthropic": {
                "access_token": "sk-ant-oat-test-token-12345",
                "refresh_token": "rt-test",
                "expires_at": int(time.time()) + 3600,
                "token_type": "bearer",
            }
        }
        auth_path.parent.mkdir(parents=True, exist_ok=True)
        auth_path.write_text(json.dumps(creds), encoding="utf-8")
        monkeypatch.setattr("engine.auth.DEFAULT_AUTH_PATH", auth_path)
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        runner = CliRunner()
        result = runner.invoke(cli, ["status"])
        assert result.exit_code == 0
        assert "logged in" in result.output.lower()

    def test_status_with_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Status with env var set shows 'env var'."""
        auth_path = tmp_path / "auth.json"
        monkeypatch.setattr("engine.auth.DEFAULT_AUTH_PATH", auth_path)
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-api-test-key")
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        runner = CliRunner()
        result = runner.invoke(cli, ["status"])
        assert result.exit_code == 0
        assert "env var" in result.output.lower()

    def test_status_expired_token(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Status with expired token shows 'expired'."""
        import json

        auth_path = tmp_path / "auth.json"
        creds = {
            "anthropic": {
                "access_token": "sk-ant-api-old-token",
                "refresh_token": "rt-test",
                "expires_at": 1000000000,  # 2001-09-09, well in the past
                "token_type": "bearer",
            }
        }
        auth_path.parent.mkdir(parents=True, exist_ok=True)
        auth_path.write_text(json.dumps(creds), encoding="utf-8")
        monkeypatch.setattr("engine.auth.DEFAULT_AUTH_PATH", auth_path)
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        runner = CliRunner()
        result = runner.invoke(cli, ["status"])
        assert result.exit_code == 0
        assert "expired" in result.output.lower()

    def test_status_exit_code_zero(self) -> None:
        """Status always exits 0 regardless of credential state."""
        runner = CliRunner()
        result = runner.invoke(cli, ["status"])
        assert result.exit_code == 0

    def test_status_shows_both_providers(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Status output mentions both anthropic and openai providers."""
        auth_path = tmp_path / "auth.json"
        monkeypatch.setattr("engine.auth.DEFAULT_AUTH_PATH", auth_path)
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        runner = CliRunner()
        result = runner.invoke(cli, ["status"])
        assert result.exit_code == 0
        assert "anthropic" in result.output.lower()
        assert "openai" in result.output.lower()

    def test_status_subscription_token_type(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Status distinguishes subscription tokens (sk-ant-oat prefix)."""
        import json
        import time

        auth_path = tmp_path / "auth.json"
        creds = {
            "anthropic": {
                "access_token": "sk-ant-oat-subscription-token",
                "refresh_token": "rt-test",
                "expires_at": int(time.time()) + 3600,
                "token_type": "bearer",
            }
        }
        auth_path.parent.mkdir(parents=True, exist_ok=True)
        auth_path.write_text(json.dumps(creds), encoding="utf-8")
        monkeypatch.setattr("engine.auth.DEFAULT_AUTH_PATH", auth_path)
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        runner = CliRunner()
        result = runner.invoke(cli, ["status"])
        assert result.exit_code == 0
        assert "subscription" in result.output.lower()
