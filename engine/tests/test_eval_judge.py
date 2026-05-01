"""Unit tests for :mod:`engine.eval_judge` (issue #87).

The :class:`engine.eval_judge.ClaudeCodeJudge` shim closes the
OAuth-user gap from spec 061 step 7: it lets the deepeval suite run
without an Anthropic API key by routing the judge through the host
``claude`` CLI subprocess. These tests exercise the construction and
contract surface without invoking the subprocess — that costs money
and requires the binary on PATH, so the live test is parked behind
``@pytest.mark.live``.
"""

from __future__ import annotations

import pytest

from engine.eval_judge import ClaudeCodeJudge


class TestClaudeCodeJudgeConstruction:
    """Construction-time invariants for :class:`ClaudeCodeJudge`."""

    def test_claude_code_judge_construction(self) -> None:
        """Explicit-model construction wires up the underlying provider lazily."""
        judge = ClaudeCodeJudge(model="sonnet")
        assert judge._model_name == "sonnet"
        # Provider is lazy — not built until we ask for it.
        assert judge._provider is None
        provider = judge.load_model()
        assert provider is not None
        # Subsequent calls return the cached instance.
        assert judge.load_model() is provider

    def test_claude_code_judge_default_model(self) -> None:
        """Default model is ``"sonnet"`` (the OAuth-friendly alias)."""
        judge = ClaudeCodeJudge()
        assert judge._model_name == "sonnet"
        assert judge.get_model_name() == "sonnet (claude-code)"

    def test_claude_code_judge_get_model_name_format(self) -> None:
        """``get_model_name`` always carries the ``(claude-code)`` suffix.

        The suffix is the telemetry marker downstream consumers use to
        separate OAuth-judge runs from API-judge runs; locking the
        format here prevents silent regressions.
        """
        judge = ClaudeCodeJudge(model="claude-3-5-haiku-20241022")
        assert judge.get_model_name() == "claude-3-5-haiku-20241022 (claude-code)"

    def test_claude_code_judge_load_model_returns_provider(self) -> None:
        """``load_model`` returns the underlying ClaudeCodeProvider instance."""
        from engine.execution.providers.claude_code import ClaudeCodeProvider

        judge = ClaudeCodeJudge(model="sonnet")
        provider = judge.load_model()
        assert isinstance(provider, ClaudeCodeProvider)


@pytest.mark.live
class TestClaudeCodeJudgeLive:
    """Live tests that actually invoke ``claude -p`` — opt-in only.

    These require the ``claude`` binary on PATH and a working host
    OAuth session. They are excluded from default CI via the ``live``
    marker; run manually with ``-m live`` when validating end-to-end.
    """

    def test_generate_returns_string(self) -> None:
        """``generate`` returns a non-empty string from the live subprocess."""
        judge = ClaudeCodeJudge(model="sonnet")
        result = judge.generate(
            "Reply with exactly the word OK and nothing else."
        )
        assert isinstance(result, str)
        assert result  # non-empty
