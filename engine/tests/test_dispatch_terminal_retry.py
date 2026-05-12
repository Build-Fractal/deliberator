"""Tests for terminal-phase retry dispatch (synthesis / arbitration).

Verifies the outer-loop retry policy that wraps :func:`dispatch_phase`
for the synthesis, cross-round-synthesis, and arbitration phases. These
phases are single-agent dispatches whose prompts are the union of all
prior phase outputs and which therefore disproportionately encounter
rate-limit and prompt-size failure modes (see ``engine.dispatch``
module docstring for the production failure history).

The retry policy:

- Wraps :func:`dispatch_phase` in an outer loop with exponential backoff.
- Retries when the per-phase result matches a known transient pattern:
  rate-limit error strings, OR all-empty-no-error (silent-drop signature).
- Surfaces the final error unchanged on exhaustion so callers see the
  underlying cause, not a "retries exhausted" wrapper.
- Returns immediately on success or non-retryable failure.
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator

import pytest

from engine.dispatch import (
    DEFAULT_MAX_TOKENS,
    DEFAULT_MODEL,
    DEFAULT_TERMINAL_PHASE_RETRY_ATTEMPTS,
    _is_retryable_phase_failure,
    dispatch_phase_with_retry,
)
from engine.events import CallbackEmitter, EngineEvent
from engine.providers import MockProvider, ProviderError


# ---------------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------------


class FlakyRateLimitProvider:
    """Provider that raises ``RateLimitError``-style ProviderError for the
    first *fail_count* calls, then succeeds.

    Used to verify that the outer-loop retry recovers from the same
    transient 429 pattern observed in the 2026-05-12 production failure.
    """

    def __init__(self, fail_count: int = 1, success_text: str = "ok") -> None:
        self.fail_count = fail_count
        self.success_text = success_text
        self.call_count = 0

    async def complete(self, prompt: str, model: str, max_tokens: int) -> str:
        self.call_count += 1
        if self.call_count <= self.fail_count:
            raise ProviderError(
                "Anthropic rate limit exceeded after 3 attempts: "
                "Error code: 429 - rate_limit_error",
                category="rate_limit",
            )
        return self.success_text

    async def stream(
        self, prompt: str, model: str, max_tokens: int,
    ) -> AsyncIterator[str]:
        # Not used by the retry path.
        yield ""


class AlwaysAuthErrorProvider:
    """Provider that raises a non-retryable auth error every call.

    Used to verify the retry loop does NOT retry permanent failures.
    """

    def __init__(self) -> None:
        self.call_count = 0

    async def complete(self, prompt: str, model: str, max_tokens: int) -> str:
        self.call_count += 1
        raise ProviderError(
            "Anthropic authentication failed: invalid x-api-key",
            category="auth",
        )

    async def stream(
        self, prompt: str, model: str, max_tokens: int,
    ) -> AsyncIterator[str]:
        yield ""


class SilentDropProvider:
    """Provider that returns empty content with no error for the first
    *fail_count* calls, then returns real content.

    Simulates the 2026-05-06 arbitration-crash mode: claude-code
    subprocess silently dropping an oversize prompt — the result is
    "0/1 succeeded" with no error string and empty response_text.
    """

    def __init__(self, fail_count: int = 1, success_text: str = "ok") -> None:
        self.fail_count = fail_count
        self.success_text = success_text
        self.call_count = 0

    async def complete(self, prompt: str, model: str, max_tokens: int) -> str:
        self.call_count += 1
        if self.call_count <= self.fail_count:
            return ""  # silent drop
        return self.success_text

    async def stream(
        self, prompt: str, model: str, max_tokens: int,
    ) -> AsyncIterator[str]:
        yield ""


@pytest.fixture
def fast_backoff(monkeypatch: pytest.MonkeyPatch) -> None:
    """Patch ``asyncio.sleep`` to a no-op so retry tests run in <1s."""
    async def _no_sleep(_seconds: float) -> None:
        return None

    monkeypatch.setattr("engine.dispatch.asyncio.sleep", _no_sleep)


# ---------------------------------------------------------------------------
# _is_retryable_phase_failure — pure-function tests
# ---------------------------------------------------------------------------


class TestIsRetryablePhaseFailure:
    """The retry-classifier identifies transient vs permanent failures."""

    def test_success_is_not_retryable(self) -> None:
        results = [("synth", "real content", None)]
        assert _is_retryable_phase_failure(results) is False

    def test_rate_limit_error_is_retryable(self) -> None:
        results = [
            ("synth", "", "ProviderError: Anthropic rate limit exceeded ..."),
        ]
        assert _is_retryable_phase_failure(results) is True

    def test_429_substring_is_retryable(self) -> None:
        results = [("synth", "", "Error code: 429 - rate_limit_error")]
        assert _is_retryable_phase_failure(results) is True

    def test_ratelimiterror_classname_is_retryable(self) -> None:
        # Matches RateLimitError exception class name appearing in the
        # error string (Anthropic SDK exception type).
        results = [
            ("synth", "", "RateLimitError: 429 from anthropic API"),
        ]
        assert _is_retryable_phase_failure(results) is True

    def test_auth_error_is_not_retryable(self) -> None:
        results = [
            ("synth", "", "ProviderError: Anthropic authentication failed"),
        ]
        assert _is_retryable_phase_failure(results) is False

    def test_silent_drop_is_retryable(self) -> None:
        # Empty response, no error — the 2026-05-06 prompt-overflow signature.
        results = [("synth", "", None)]
        assert _is_retryable_phase_failure(results) is True

    def test_whitespace_only_response_is_silent_drop(self) -> None:
        results = [("synth", "   \n\n  ", None)]
        assert _is_retryable_phase_failure(results) is True

    def test_partial_success_is_not_retryable(self) -> None:
        # If one agent succeeded, the phase is usable; don't retry.
        results = [
            ("synth-a", "real content", None),
            ("synth-b", "", None),
        ]
        assert _is_retryable_phase_failure(results) is False

    def test_empty_results_is_not_retryable(self) -> None:
        assert _is_retryable_phase_failure([]) is False


# ---------------------------------------------------------------------------
# dispatch_phase_with_retry — end-to-end retry behavior
# ---------------------------------------------------------------------------


class TestDispatchPhaseWithRetry:
    """The retry-wrapped dispatcher recovers from transient failures."""

    @pytest.mark.asyncio
    async def test_succeeds_on_first_attempt_when_provider_healthy(
        self,
        mock_provider: MockProvider,
        event_collector: tuple[CallbackEmitter, list[EngineEvent]],
        fast_backoff: None,
    ) -> None:
        emitter, _events = event_collector
        results = await dispatch_phase_with_retry(
            agents=[("synthesizer", "Synthesize.")],
            model=DEFAULT_MODEL,
            max_tokens=DEFAULT_MAX_TOKENS,
            provider=mock_provider,
            emitter=emitter,
            phase="synthesis",
        )
        assert len(results) == 1
        name, text, error = results[0]
        assert name == "synthesizer"
        assert error is None
        assert text  # non-empty
        # Healthy path — no retries; provider called exactly once.
        assert len(mock_provider.calls) == 1

    @pytest.mark.asyncio
    async def test_recovers_from_transient_rate_limit(
        self,
        event_collector: tuple[CallbackEmitter, list[EngineEvent]],
        fast_backoff: None,
    ) -> None:
        """The 2026-05-12 production failure mode: synthesizer hits a 429,
        retry should re-dispatch and succeed."""
        emitter, _events = event_collector
        provider = FlakyRateLimitProvider(fail_count=2, success_text="synth-ok")

        results = await dispatch_phase_with_retry(
            agents=[("synthesizer", "Synthesize.")],
            model=DEFAULT_MODEL,
            max_tokens=DEFAULT_MAX_TOKENS,
            provider=provider,
            emitter=emitter,
            phase="synthesis",
        )

        assert len(results) == 1
        name, text, error = results[0]
        assert error is None
        assert text == "synth-ok"
        # 2 failed + 1 success = 3 calls
        assert provider.call_count == 3

    @pytest.mark.asyncio
    async def test_recovers_from_silent_drop(
        self,
        event_collector: tuple[CallbackEmitter, list[EngineEvent]],
        fast_backoff: None,
    ) -> None:
        """The 2026-05-06 prompt-overflow mode: dispatch returns empty
        content with no error, retry should re-dispatch and succeed."""
        emitter, _events = event_collector
        provider = SilentDropProvider(fail_count=1, success_text="arb-ok")

        results = await dispatch_phase_with_retry(
            agents=[("arbiter", "Arbitrate.")],
            model=DEFAULT_MODEL,
            max_tokens=DEFAULT_MAX_TOKENS,
            provider=provider,
            emitter=emitter,
            phase="arbitration",
        )

        assert len(results) == 1
        _name, text, error = results[0]
        assert error is None
        assert text == "arb-ok"
        assert provider.call_count == 2

    @pytest.mark.asyncio
    async def test_does_not_retry_non_retryable_error(
        self,
        event_collector: tuple[CallbackEmitter, list[EngineEvent]],
        fast_backoff: None,
    ) -> None:
        """Auth errors are permanent — retry would only delay the failure."""
        emitter, _events = event_collector
        provider = AlwaysAuthErrorProvider()

        results = await dispatch_phase_with_retry(
            agents=[("synthesizer", "Synthesize.")],
            model=DEFAULT_MODEL,
            max_tokens=DEFAULT_MAX_TOKENS,
            provider=provider,
            emitter=emitter,
            phase="synthesis",
        )

        assert len(results) == 1
        _name, _text, error = results[0]
        assert error is not None
        assert "auth" in error.lower()
        # Auth errors short-circuit — exactly one provider call.
        assert provider.call_count == 1

    @pytest.mark.asyncio
    async def test_exhausts_attempts_then_surfaces_original_error(
        self,
        event_collector: tuple[CallbackEmitter, list[EngineEvent]],
        fast_backoff: None,
    ) -> None:
        """If all retry attempts fail, the original error must surface
        unchanged (no synthetic 'retries exhausted' wrapper)."""
        emitter, _events = event_collector
        # Make the provider fail more times than the retry budget allows.
        provider = FlakyRateLimitProvider(fail_count=99)

        results = await dispatch_phase_with_retry(
            agents=[("synthesizer", "Synthesize.")],
            model=DEFAULT_MODEL,
            max_tokens=DEFAULT_MAX_TOKENS,
            provider=provider,
            emitter=emitter,
            phase="synthesis",
            max_attempts=3,
        )

        assert len(results) == 1
        _name, _text, error = results[0]
        assert error is not None
        # The original rate-limit text must survive — not wrapped.
        assert "rate limit" in error.lower() or "429" in error
        assert provider.call_count == 3

    @pytest.mark.asyncio
    async def test_max_attempts_one_disables_retry(
        self,
        event_collector: tuple[CallbackEmitter, list[EngineEvent]],
        fast_backoff: None,
    ) -> None:
        """``max_attempts=1`` is equivalent to plain dispatch_phase."""
        emitter, _events = event_collector
        provider = FlakyRateLimitProvider(fail_count=99)

        results = await dispatch_phase_with_retry(
            agents=[("synthesizer", "Synthesize.")],
            model=DEFAULT_MODEL,
            max_tokens=DEFAULT_MAX_TOKENS,
            provider=provider,
            emitter=emitter,
            phase="synthesis",
            max_attempts=1,
        )

        assert provider.call_count == 1
        _name, _text, error = results[0]
        assert error is not None

    @pytest.mark.asyncio
    async def test_max_attempts_zero_raises(
        self,
        mock_provider: MockProvider,
        event_collector: tuple[CallbackEmitter, list[EngineEvent]],
    ) -> None:
        emitter, _events = event_collector
        with pytest.raises(ValueError, match="max_attempts must be >= 1"):
            await dispatch_phase_with_retry(
                agents=[("synthesizer", "x")],
                model=DEFAULT_MODEL,
                max_tokens=DEFAULT_MAX_TOKENS,
                provider=mock_provider,
                emitter=emitter,
                phase="synthesis",
                max_attempts=0,
            )

    @pytest.mark.asyncio
    async def test_default_attempts_constant_is_used(
        self,
        event_collector: tuple[CallbackEmitter, list[EngineEvent]],
        fast_backoff: None,
    ) -> None:
        """Caller omitting ``max_attempts`` uses the module constant."""
        emitter, _events = event_collector
        provider = FlakyRateLimitProvider(fail_count=99)

        await dispatch_phase_with_retry(
            agents=[("synthesizer", "x")],
            model=DEFAULT_MODEL,
            max_tokens=DEFAULT_MAX_TOKENS,
            provider=provider,
            emitter=emitter,
            phase="synthesis",
        )

        assert provider.call_count == DEFAULT_TERMINAL_PHASE_RETRY_ATTEMPTS

    @pytest.mark.asyncio
    async def test_backoff_honored_between_attempts(
        self,
        event_collector: tuple[CallbackEmitter, list[EngineEvent]],
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Exponential backoff sleep is invoked between failed attempts."""
        emitter, _events = event_collector
        provider = FlakyRateLimitProvider(fail_count=2, success_text="ok")

        sleeps: list[float] = []

        async def _record_sleep(seconds: float) -> None:
            sleeps.append(seconds)

        monkeypatch.setattr("engine.dispatch.asyncio.sleep", _record_sleep)

        await dispatch_phase_with_retry(
            agents=[("synthesizer", "x")],
            model=DEFAULT_MODEL,
            max_tokens=DEFAULT_MAX_TOKENS,
            provider=provider,
            emitter=emitter,
            phase="synthesis",
            backoff_base_seconds=1.0,
            backoff_cap_seconds=100.0,
        )

        # 2 failed attempts → 2 sleeps between them (the third attempt
        # succeeds so no sleep after it).
        assert len(sleeps) == 2
        # Exponential: base * 2^0 = 1, base * 2^1 = 2
        assert sleeps[0] == 1.0
        assert sleeps[1] == 2.0

    @pytest.mark.asyncio
    async def test_backoff_cap_respected(
        self,
        event_collector: tuple[CallbackEmitter, list[EngineEvent]],
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        emitter, _events = event_collector
        provider = FlakyRateLimitProvider(fail_count=99)

        sleeps: list[float] = []

        async def _record_sleep(seconds: float) -> None:
            sleeps.append(seconds)

        monkeypatch.setattr("engine.dispatch.asyncio.sleep", _record_sleep)

        await dispatch_phase_with_retry(
            agents=[("synthesizer", "x")],
            model=DEFAULT_MODEL,
            max_tokens=DEFAULT_MAX_TOKENS,
            provider=provider,
            emitter=emitter,
            phase="synthesis",
            max_attempts=5,
            backoff_base_seconds=100.0,
            backoff_cap_seconds=200.0,
        )

        # Without the cap, attempt 1 sleep would be 200, attempt 2 = 400,
        # attempt 3 = 800. The cap should clamp all to 200.
        for s in sleeps:
            assert s <= 200.0


# ---------------------------------------------------------------------------
# Phase integration — verify terminal phases use the retry wrapper
# ---------------------------------------------------------------------------


class TestPhaseIntegration:
    """Phase 5 + 6 + cross-round-synthesis must dispatch via the retry
    wrapper, not the raw dispatch_phase. Source-level check guards
    against regression (someone reverting the call-site wiring)."""

    def test_synthesis_uses_retry_wrapper(self) -> None:
        from pathlib import Path

        phases_src = (
            Path(__file__).resolve().parent.parent / "phases.py"
        ).read_text(encoding="utf-8")
        # Synthesis call site at "synth_results = await ...".
        assert (
            "synth_results = await dispatch_phase_with_retry(" in phases_src
        ), "Synthesis phase must use dispatch_phase_with_retry"

    def test_arbitration_inter_round_uses_retry_wrapper(self) -> None:
        from pathlib import Path

        phases_src = (
            Path(__file__).resolve().parent.parent / "phases.py"
        ).read_text(encoding="utf-8")
        assert (
            "_arb_results = await dispatch_phase_with_retry(" in phases_src
        ), "Inter-round arbitration must use dispatch_phase_with_retry"

    def test_arbitration_final_uses_retry_wrapper(self) -> None:
        from pathlib import Path

        phases_src = (
            Path(__file__).resolve().parent.parent / "phases.py"
        ).read_text(encoding="utf-8")
        assert (
            "arb_results = await dispatch_phase_with_retry(" in phases_src
        ), "Final-timing arbitration must use dispatch_phase_with_retry"

    def test_cross_round_synthesis_uses_retry_wrapper(self) -> None:
        from pathlib import Path

        phases_src = (
            Path(__file__).resolve().parent.parent / "phases.py"
        ).read_text(encoding="utf-8")
        assert (
            "crs_results = await dispatch_phase_with_retry(" in phases_src
        ), "Cross-round synthesis must use dispatch_phase_with_retry"
