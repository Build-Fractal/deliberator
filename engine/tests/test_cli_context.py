"""Tests for engine.cli.context (spec 042 Phase 2.0).

Exercises every branch of the invocation context detection state machine:
TTY/non-TTY, CI/non-CI, Claude Code session/not, background/not, all
permutations of default provider/renderer/exit code scheme resolution.

Every test passes argv, env, and isatty signals explicitly — no
monkeypatching of ``sys`` or ``os.environ`` — so the detection logic is
exercised as a pure function.
"""

from __future__ import annotations

import pytest

from engine.cli.context import (
    InvocationContext,
    detect_context,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _ctx(
    *,
    argv: list[str] | None = None,
    env: dict[str, str] | None = None,
    stdout_isatty: bool | None = None,
) -> InvocationContext:
    """Shortcut: call detect_context with explicit signals.

    Default argv is ``["conversus"]`` (program name only); default env
    is empty; default isatty is False.  Tests override only what they
    care about.
    """
    return detect_context(
        argv=argv if argv is not None else ["conversus"],
        env=env if env is not None else {},
        stdout_isatty=stdout_isatty if stdout_isatty is not None else False,
    )


# ---------------------------------------------------------------------------
# Raw signal detection
# ---------------------------------------------------------------------------


class TestTTYDetection:
    def test_tty_signal_passes_through(self) -> None:
        assert _ctx(stdout_isatty=True).is_tty is True
        assert _ctx(stdout_isatty=False).is_tty is False


class TestCIDetection:
    @pytest.mark.parametrize(
        "var",
        [
            "CI",
            "GITHUB_ACTIONS",
            "GITLAB_CI",
            "JENKINS_URL",
            "CIRCLECI",
            "BUILDKITE",
            "TF_BUILD",
            "TEAMCITY_VERSION",
            "APPVEYOR",
            "DRONE",
        ],
    )
    def test_any_ci_env_var_flips_is_ci(self, var: str) -> None:
        """Every CI system's env var is recognized."""
        assert _ctx(env={var: "1"}).is_ci is True

    def test_empty_ci_value_does_not_flip(self) -> None:
        """An empty-string env var is treated as absent.

        Some CI systems set CI='' to unset it; we honor that.
        """
        assert _ctx(env={"CI": ""}).is_ci is False

    def test_no_ci_env_vars_means_not_ci(self) -> None:
        assert _ctx(env={"SHELL": "/bin/zsh"}).is_ci is False


class TestClaudeCodeSessionDetection:
    @pytest.mark.parametrize(
        "var",
        ["CLAUDECODE", "CLAUDE_CODE", "CLAUDE_CODE_ACTIVE"],
    )
    def test_any_claude_code_env_var_flips_detection(self, var: str) -> None:
        """Multiple historical variants are all recognized."""
        assert _ctx(env={var: "1"}).is_claude_code_session is True

    def test_no_claude_code_env_vars_means_not_in_session(self) -> None:
        assert _ctx(env={}).is_claude_code_session is False


class TestIsBackground:
    def test_no_tty_no_ci_no_claude_code_is_background(self) -> None:
        """Cron/hook/MCP-server case — nothing is watching directly."""
        ctx = _ctx(stdout_isatty=False, env={})
        assert ctx.is_background is True

    def test_tty_is_not_background(self) -> None:
        assert _ctx(stdout_isatty=True, env={}).is_background is False

    def test_ci_is_not_background(self) -> None:
        """CI is watched (by the log capture), even though there is no human."""
        assert _ctx(stdout_isatty=False, env={"CI": "1"}).is_background is False

    def test_claude_code_session_is_not_background(self) -> None:
        """Claude Code session means the host is rendering for the user."""
        assert _ctx(stdout_isatty=False, env={"CLAUDECODE": "1"}).is_background is False


# ---------------------------------------------------------------------------
# Renderer resolution
# ---------------------------------------------------------------------------


class TestRendererResolution:
    def test_tty_without_ci_selects_tui(self) -> None:
        assert _ctx(stdout_isatty=True, env={}).renderer == "tui"

    def test_ci_selects_json_even_with_tty(self) -> None:
        """CI always wins — even a TTY-attached CI runner gets JSON for log capture."""
        ctx = _ctx(stdout_isatty=True, env={"CI": "1"})
        assert ctx.renderer == "json"

    def test_ci_without_tty_selects_json(self) -> None:
        assert _ctx(stdout_isatty=False, env={"CI": "1"}).renderer == "json"

    def test_non_tty_non_ci_selects_plain(self) -> None:
        """File redirects, cron, hooks, MCP server."""
        assert _ctx(stdout_isatty=False, env={}).renderer == "plain"


# ---------------------------------------------------------------------------
# Exit code scheme resolution
# ---------------------------------------------------------------------------


class TestExitCodeSchemeResolution:
    def test_plain_run_uses_interactive_scheme(self) -> None:
        ctx = _ctx(argv=["conversus", "run", "config.yml"])
        assert ctx.exit_code_scheme == "interactive"

    def test_governance_subcommand_uses_governance_scheme(self) -> None:
        ctx = _ctx(argv=["conversus", "governance", "--gate", "pr"])
        assert ctx.exit_code_scheme == "governance"

    def test_gate_subcommand_uses_governance_scheme(self) -> None:
        """Spec 011 phase consensus gates also use structured exit codes."""
        ctx = _ctx(argv=["conversus", "gate", "review", "spec.md"])
        assert ctx.exit_code_scheme == "governance"

    def test_no_subcommand_uses_interactive_scheme(self) -> None:
        ctx = _ctx(argv=["conversus"])
        assert ctx.exit_code_scheme == "interactive"

    def test_other_subcommands_use_interactive_scheme(self) -> None:
        """``define``, ``interests``, ``mode``, ``arbitrate`` all use interactive codes."""
        for subcmd in ("define", "interests", "mode", "arbitrate", "converge"):
            ctx = _ctx(argv=["conversus", subcmd])
            assert ctx.exit_code_scheme == "interactive", f"subcommand={subcmd}"


# ---------------------------------------------------------------------------
# Default provider resolution (Phase 2.0 — conservative)
# ---------------------------------------------------------------------------


class TestDefaultProviderResolution:
    """Context-aware default provider (Phase 3, post-claude-code-landing).

    The resolution prefers ``claude-code`` when the session signals it
    is reachable (Claude Code session detected). All other contexts
    fall back to ``mock`` — conservative default that won't surprise
    operators with metered LLM calls.
    """

    def test_interactive_tty_default_is_mock(self) -> None:
        """Plain interactive TTY (no Claude Code env vars) → mock."""
        assert _ctx(stdout_isatty=True, env={}).default_provider == "mock"

    def test_ci_default_is_mock(self) -> None:
        """CI environment → mock (no OAuth session by default)."""
        assert _ctx(env={"CI": "1"}).default_provider == "mock"

    def test_claude_code_session_default_is_claude_code(self) -> None:
        """Claude Code session detected → claude-code (Phase 3 default).

        The ``claude -p`` subprocess uses the host OAuth session, so
        defaulting to claude-code in this context picks the
        contextually-correct provider without requiring --provider
        flag or settings.yml override.
        """
        assert _ctx(env={"CLAUDECODE": "1"}).default_provider == "claude-code"

    def test_claude_code_alt_env_var_also_triggers(self) -> None:
        """Historical CLAUDE_CODE / CLAUDE_CODE_ACTIVE env vars also trigger."""
        assert _ctx(env={"CLAUDE_CODE": "1"}).default_provider == "claude-code"
        assert _ctx(env={"CLAUDE_CODE_ACTIVE": "1"}).default_provider == "claude-code"

    def test_background_default_is_mock(self) -> None:
        """Background (no TTY, no CI, no Claude Code) → mock."""
        assert _ctx(stdout_isatty=False, env={}).default_provider == "mock"

    def test_ci_with_claude_code_env_prefers_claude_code(self) -> None:
        """CI + Claude Code env → claude-code (e.g., GitHub Actions runner
        invoked from a Claude Code session). Claude Code signal wins.
        """
        ctx = _ctx(env={"CI": "1", "CLAUDECODE": "1"})
        assert ctx.is_ci is True
        assert ctx.is_claude_code_session is True
        assert ctx.default_provider == "claude-code"


# ---------------------------------------------------------------------------
# Debug env snapshot
# ---------------------------------------------------------------------------


class TestDebugEnvSnapshot:
    def test_consulted_env_vars_are_recorded(self) -> None:
        """The context records only the env vars the detection logic read."""
        ctx = _ctx(env={"CI": "1", "HOME": "/Users/test", "PATH": "/bin"})
        # CI is in the consulted set — should be recorded
        assert ctx.env == {"CI": "1"}

    def test_unrelated_env_vars_are_not_recorded(self) -> None:
        """Env snapshot is narrow — not a full env dump."""
        ctx = _ctx(env={"HOME": "/Users/test", "PATH": "/bin", "SHELL": "/bin/zsh"})
        assert ctx.env == {}

    def test_multiple_consulted_vars_all_recorded(self) -> None:
        ctx = _ctx(env={"CI": "1", "GITHUB_ACTIONS": "true", "CLAUDECODE": "1"})
        assert ctx.env == {
            "CI": "1",
            "GITHUB_ACTIONS": "true",
            "CLAUDECODE": "1",
        }


# ---------------------------------------------------------------------------
# argv snapshot
# ---------------------------------------------------------------------------


class TestArgvSnapshot:
    def test_argv_preserved(self) -> None:
        ctx = _ctx(argv=["conversus", "run", "config.yml", "--verbose"])
        assert ctx.argv == ("conversus", "run", "config.yml", "--verbose")

    def test_argv_is_tuple_not_list(self) -> None:
        """Frozen dataclass semantics — argv must be hashable."""
        ctx = _ctx(argv=["conversus", "run"])
        assert isinstance(ctx.argv, tuple)


# ---------------------------------------------------------------------------
# Integration-style scenarios
# ---------------------------------------------------------------------------


class TestRealisticScenarios:
    """End-to-end scenarios mirroring the three invocation paths."""

    def test_interactive_terminal_user(self) -> None:
        """User types ``conversus run`` in a terminal."""
        ctx = _ctx(
            argv=["conversus", "run", "conversus.yml"],
            env={"SHELL": "/bin/zsh", "HOME": "/Users/alice"},
            stdout_isatty=True,
        )
        assert ctx.is_tty is True
        assert ctx.is_ci is False
        assert ctx.is_claude_code_session is False
        assert ctx.is_background is False
        assert ctx.renderer == "tui"
        assert ctx.exit_code_scheme == "interactive"

    def test_github_actions_governance_gate(self) -> None:
        """CI runs ``conversus governance --gate pr``."""
        ctx = _ctx(
            argv=["conversus", "governance", "--gate", "pr"],
            env={"CI": "true", "GITHUB_ACTIONS": "true"},
            stdout_isatty=False,
        )
        assert ctx.is_tty is False
        assert ctx.is_ci is True
        assert ctx.is_claude_code_session is False
        assert ctx.is_background is False  # CI is watched
        assert ctx.renderer == "json"
        assert ctx.exit_code_scheme == "governance"

    def test_cron_job_mcp_server(self) -> None:
        """Cron job or MCP server invokes conversus with no human present."""
        ctx = _ctx(
            argv=["conversus", "run", "daily-audit.yml"],
            env={},
            stdout_isatty=False,
        )
        assert ctx.is_tty is False
        assert ctx.is_ci is False
        assert ctx.is_claude_code_session is False
        assert ctx.is_background is True
        assert ctx.renderer == "plain"
        assert ctx.exit_code_scheme == "interactive"

    def test_claude_code_interactive_session(self) -> None:
        """User invokes /conversus run inside a Claude Code session."""
        ctx = _ctx(
            argv=["conversus", "run", "conversus.yml"],
            env={"CLAUDECODE": "1"},
            stdout_isatty=False,  # pipes through Claude Code, not a real TTY
        )
        assert ctx.is_claude_code_session is True
        assert ctx.is_background is False
        # Host renders output, so we default to plain (no interference)
        assert ctx.renderer == "plain"
        assert ctx.exit_code_scheme == "interactive"

    def test_gitlab_ci_scheduled_audit(self) -> None:
        """GitLab CI scheduled pipeline running a non-gate conversus audit."""
        ctx = _ctx(
            argv=["conversus", "run", "audit.yml"],
            env={"CI": "true", "GITLAB_CI": "true"},
            stdout_isatty=False,
        )
        assert ctx.is_ci is True
        assert ctx.renderer == "json"
        # Non-governance subcommand means interactive exit scheme even in CI
        assert ctx.exit_code_scheme == "interactive"
