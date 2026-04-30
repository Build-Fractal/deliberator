"""Tests for engine.dispatch — single-agent and multi-agent concurrent dispatch."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator

import pytest

from engine.dispatch import (
    DEFAULT_MAX_TOKENS,
    DEFAULT_MODEL,
    FatalProviderResponseError,
    dispatch_agent,
    dispatch_phase,
)
from engine.events import (
    AgentCompleted,
    AgentDispatched,
    CallbackEmitter,
    EngineEvent,
    NullEmitter,
)
from engine.providers import MockProvider


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class FailingProvider:
    """Provider that raises for a specific agent name."""

    def __init__(self, fail_for: str) -> None:
        self.fail_for = fail_for

    async def complete(self, prompt: str, model: str, max_tokens: int) -> str:
        if self.fail_for in prompt:
            raise RuntimeError(f"Simulated failure for {self.fail_for}")
        return f"Success for {model}"

    async def stream(self, prompt: str, model: str, max_tokens: int) -> AsyncIterator[str]:
        yield "not used"


# ---------------------------------------------------------------------------
# dispatch_agent
# ---------------------------------------------------------------------------

class TestDispatchAgent:
    """dispatch_agent calls the provider and emits events."""

    @pytest.mark.asyncio
    async def test_returns_response_text(
        self,
        mock_provider: MockProvider,
        event_collector: tuple[CallbackEmitter, list[EngineEvent]],
    ) -> None:
        emitter, events = event_collector
        text, error = await dispatch_agent(
            prompt="Review this spec.",
            agent_name="agent-a",
            model=DEFAULT_MODEL,
            max_tokens=DEFAULT_MAX_TOKENS,
            provider=mock_provider,
            emitter=emitter,
        )
        assert error is None
        assert "Mock review response" in text

    @pytest.mark.asyncio
    async def test_emits_dispatched_and_completed(
        self,
        mock_provider: MockProvider,
        event_collector: tuple[CallbackEmitter, list[EngineEvent]],
    ) -> None:
        emitter, events = event_collector
        await dispatch_agent(
            prompt="Review this.",
            agent_name="agent-a",
            model=DEFAULT_MODEL,
            max_tokens=DEFAULT_MAX_TOKENS,
            provider=mock_provider,
            emitter=emitter,
        )
        assert len(events) == 2
        assert isinstance(events[0], AgentDispatched)
        assert isinstance(events[1], AgentCompleted)
        assert events[1].success is True
        assert events[1].error is None

    @pytest.mark.asyncio
    async def test_captures_provider_error(
        self,
        event_collector: tuple[CallbackEmitter, list[EngineEvent]],
    ) -> None:
        emitter, events = event_collector
        failing = FailingProvider(fail_for="agent-a")
        text, error = await dispatch_agent(
            prompt="agent-a review",
            agent_name="agent-a",
            model=DEFAULT_MODEL,
            max_tokens=DEFAULT_MAX_TOKENS,
            provider=failing,
            emitter=emitter,
        )
        assert text == ""
        assert error is not None
        assert "Simulated failure" in error
        # AgentCompleted should show failure
        completed = [e for e in events if isinstance(e, AgentCompleted)]
        assert len(completed) == 1
        assert completed[0].success is False

    @pytest.mark.asyncio
    async def test_records_call_on_mock(self, mock_provider: MockProvider) -> None:
        emitter = NullEmitter()
        await dispatch_agent(
            prompt="test prompt",
            agent_name="agent-a",
            model="test-model",
            max_tokens=1024,
            provider=mock_provider,
            emitter=emitter,
        )
        assert len(mock_provider.calls) == 1
        assert mock_provider.calls[0].prompt == "test prompt"
        assert mock_provider.calls[0].model == "test-model"


# ---------------------------------------------------------------------------
# dispatch_phase
# ---------------------------------------------------------------------------

class TestDispatchPhase:
    """dispatch_phase dispatches all agents concurrently."""

    @pytest.mark.asyncio
    async def test_three_agents_all_succeed(
        self,
        mock_provider: MockProvider,
        event_collector: tuple[CallbackEmitter, list[EngineEvent]],
    ) -> None:
        emitter, events = event_collector
        agents = [
            ("agent-a", "Prompt A"),
            ("agent-b", "Prompt B"),
            ("agent-c", "Prompt C"),
        ]
        results = await dispatch_phase(
            agents=agents,
            model=DEFAULT_MODEL,
            max_tokens=DEFAULT_MAX_TOKENS,
            provider=mock_provider,
            emitter=emitter,
        )
        assert len(results) == 3
        for name, text, error in results:
            assert error is None
            assert len(text) > 0

    @pytest.mark.asyncio
    async def test_error_isolation(
        self,
        event_collector: tuple[CallbackEmitter, list[EngineEvent]],
    ) -> None:
        """One failing agent doesn't crash others."""
        emitter, events = event_collector
        failing = FailingProvider(fail_for="agent-b")
        agents = [
            ("agent-a", "Prompt A"),
            ("agent-b", "agent-b review"),
            ("agent-c", "Prompt C"),
        ]
        results = await dispatch_phase(
            agents=agents,
            model=DEFAULT_MODEL,
            max_tokens=DEFAULT_MAX_TOKENS,
            provider=failing,
            emitter=emitter,
        )
        # agent-a and agent-c succeed, agent-b fails
        successes = [(n, t, e) for n, t, e in results if e is None]
        failures = [(n, t, e) for n, t, e in results if e is not None]
        assert len(successes) == 2
        assert len(failures) == 1
        assert failures[0][0] == "agent-b"

    @pytest.mark.asyncio
    async def test_concurrent_execution(
        self,
        event_collector: tuple[CallbackEmitter, list[EngineEvent]],
    ) -> None:
        """Verify agents are dispatched concurrently (not sequentially)."""

        class SlowProvider:
            async def complete(self, prompt: str, model: str, max_tokens: int) -> str:
                await asyncio.sleep(0.05)
                return "done"

            async def stream(self, prompt: str, model: str, max_tokens: int) -> AsyncIterator[str]:
                yield "done"

        emitter, events = event_collector
        agents = [("a", "P"), ("b", "P"), ("c", "P")]

        import time
        start = time.monotonic()
        await dispatch_phase(
            agents=agents,
            model="test",
            max_tokens=100,
            provider=SlowProvider(),
            emitter=emitter,
        )
        elapsed = time.monotonic() - start

        # 3 agents × 50ms each = 150ms sequential; should be ~50ms concurrent
        assert elapsed < 0.15, f"Took {elapsed:.3f}s — agents may not be concurrent"


# ---------------------------------------------------------------------------
# Fail-fast on provider error strings returned as agent content (Bug 3a)
# ---------------------------------------------------------------------------


class TestFailFastOnProviderPassthroughError:
    """When a provider returns an error string as the assistant's response
    text (rather than raising), dispatch must abort the pipeline rather
    than silently writing the error string into the agent artifact and
    producing stub deliberation.
    """

    _ERROR_TEXT = (
        "There's an issue with the selected model "
        "(claude-sonnet-4-20250514). It may not exist or you may not have "
        "access to it. Run --model to pick a different model."
    )

    @pytest.mark.asyncio
    async def test_dispatch_agent_raises_on_passthrough_error(
        self,
        event_collector: tuple[CallbackEmitter, list[EngineEvent]],
    ) -> None:
        emitter, events = event_collector
        provider = MockProvider(response_text=self._ERROR_TEXT)

        with pytest.raises(FatalProviderResponseError) as exc_info:
            await dispatch_agent(
                prompt="Review this spec.",
                agent_name="agent-a",
                model=DEFAULT_MODEL,
                max_tokens=DEFAULT_MAX_TOKENS,
                provider=provider,
                emitter=emitter,
            )

        # Diagnostic must name the matched pattern and include the response
        # body so an operator can see exactly what came back.
        msg = str(exc_info.value)
        assert "there's an issue with the selected model" in msg.lower()
        assert "Run --model" in msg or "--model" in msg

        # AgentCompleted should record the failure — not a successful turn.
        completed = [e for e in events if isinstance(e, AgentCompleted)]
        assert len(completed) == 1
        assert completed[0].success is False

    @pytest.mark.asyncio
    async def test_dispatch_phase_aborts_on_passthrough_error(
        self,
        event_collector: tuple[CallbackEmitter, list[EngineEvent]],
    ) -> None:
        """dispatch_phase must re-raise so the pipeline halts loudly
        instead of returning an all-failed result that synthesizes nothing.
        """
        emitter, events = event_collector
        provider = MockProvider(response_text=self._ERROR_TEXT)
        agents = [
            ("agent-a", "Prompt A"),
            ("agent-b", "Prompt B"),
        ]

        with pytest.raises(FatalProviderResponseError):
            await dispatch_phase(
                agents=agents,
                model=DEFAULT_MODEL,
                max_tokens=DEFAULT_MAX_TOKENS,
                provider=provider,
                emitter=emitter,
            )

    @pytest.mark.asyncio
    async def test_clean_response_does_not_trigger(
        self,
        mock_provider: MockProvider,
        event_collector: tuple[CallbackEmitter, list[EngineEvent]],
    ) -> None:
        """Sanity check: normal responses are not falsely flagged."""
        emitter, _ = event_collector
        text, error = await dispatch_agent(
            prompt="Review this.",
            agent_name="agent-a",
            model=DEFAULT_MODEL,
            max_tokens=DEFAULT_MAX_TOKENS,
            provider=mock_provider,
            emitter=emitter,
        )
        assert error is None

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "preamble_len, expected_to_fire",
        [
            # Pattern fully within the first 1000 chars → detection fires.
            pytest.param(500, True, id="500-chars-pattern-in-head"),
            pytest.param(900, True, id="900-chars-pattern-in-head"),
            # Pattern starts at or past byte 1000 → detection does NOT fire.
            # This documents the deliberate trade-off (1KB head bounds CPU
            # vs. exhaustive scan). If a future provider buries error text
            # past 1KB, the remedy is to update
            # PROVIDER_PASSTHROUGH_ERROR_PATTERNS or raise the head limit
            # explicitly — not to silently extend detection.
            pytest.param(1024, False, id="1024-chars-pattern-past-head"),
            pytest.param(2048, False, id="2048-chars-pattern-past-head"),
            pytest.param(8192, False, id="8192-chars-very-long-preamble"),
        ],
    )
    async def test_provider_passthrough_error_1kb_boundary(
        self,
        preamble_len: int,
        expected_to_fire: bool,
        event_collector: tuple[CallbackEmitter, list[EngineEvent]],
    ) -> None:
        """`_detect_provider_passthrough_error` reads only `content[:1000]`.

        Per the 2026-04-29 session-review deliberation P1 finding (issue
        #58): an adversarial response with the error indicator past byte
        1000 is NOT caught by design. This test documents the boundary
        explicitly so a future maintainer reading it understands the
        head-only check is the way it is.
        """
        emitter, _ = event_collector
        preamble = "x" * preamble_len
        body = preamble + " " + self._ERROR_TEXT
        provider = MockProvider(response_text=body)

        if expected_to_fire:
            with pytest.raises(FatalProviderResponseError):
                await dispatch_agent(
                    prompt="Review this.",
                    agent_name="agent-a",
                    model=DEFAULT_MODEL,
                    max_tokens=DEFAULT_MAX_TOKENS,
                    provider=provider,
                    emitter=emitter,
                )
        else:
            # Detection silent → returns body as content (treats as
            # legitimate agent output). This is the deliberate trade-off
            # the test documents.
            text, error = await dispatch_agent(
                prompt="Review this.",
                agent_name="agent-a",
                model=DEFAULT_MODEL,
                max_tokens=DEFAULT_MAX_TOKENS,
                provider=provider,
                emitter=emitter,
            )
            assert error is None
            assert preamble in text  # body was returned as content


# ---------------------------------------------------------------------------
# dispatch_agent — streaming mode
# ---------------------------------------------------------------------------

class TestDispatchAgentStreaming:
    """dispatch_agent with streaming=True uses provider.stream()."""

    @pytest.mark.asyncio
    async def test_streaming_calls_stream_method(
        self,
        mock_provider: MockProvider,
        event_collector: tuple[CallbackEmitter, list[EngineEvent]],
    ) -> None:
        """When streaming=True with a callback, provider.stream() is used."""
        emitter, events = event_collector
        chunks_received: list[str] = []

        text, error = await dispatch_agent(
            prompt="Review this spec.",
            agent_name="agent-a",
            model=DEFAULT_MODEL,
            max_tokens=DEFAULT_MAX_TOKENS,
            provider=mock_provider,
            emitter=emitter,
            streaming=True,
            stream_callback=lambda c: chunks_received.append(c),
        )

        assert error is None
        assert len(text) > 0
        # MockProvider.stream() splits by whitespace and appends a space
        assert len(chunks_received) > 0
        assert "".join(chunks_received) == text
        # Verify stream method was called (not complete)
        assert mock_provider.calls[-1].method == "stream"

    @pytest.mark.asyncio
    async def test_streaming_emits_response_text(
        self,
        mock_provider: MockProvider,
        event_collector: tuple[CallbackEmitter, list[EngineEvent]],
    ) -> None:
        """AgentCompleted event includes response_text when streaming."""
        emitter, events = event_collector

        await dispatch_agent(
            prompt="Review this.",
            agent_name="agent-a",
            model=DEFAULT_MODEL,
            max_tokens=DEFAULT_MAX_TOKENS,
            provider=mock_provider,
            emitter=emitter,
            streaming=True,
            stream_callback=lambda c: None,
        )

        completed = [e for e in events if isinstance(e, AgentCompleted)]
        assert len(completed) == 1
        assert completed[0].response_text is not None
        assert len(completed[0].response_text) > 0

    @pytest.mark.asyncio
    async def test_non_streaming_also_populates_response_text(
        self,
        mock_provider: MockProvider,
        event_collector: tuple[CallbackEmitter, list[EngineEvent]],
    ) -> None:
        """AgentCompleted event includes response_text even without streaming."""
        emitter, events = event_collector

        await dispatch_agent(
            prompt="Review this.",
            agent_name="agent-a",
            model=DEFAULT_MODEL,
            max_tokens=DEFAULT_MAX_TOKENS,
            provider=mock_provider,
            emitter=emitter,
        )

        completed = [e for e in events if isinstance(e, AgentCompleted)]
        assert len(completed) == 1
        assert completed[0].response_text is not None

    @pytest.mark.asyncio
    async def test_streaming_without_callback_uses_complete(
        self,
        mock_provider: MockProvider,
        event_collector: tuple[CallbackEmitter, list[EngineEvent]],
    ) -> None:
        """streaming=True without stream_callback falls back to complete()."""
        emitter, events = event_collector

        text, error = await dispatch_agent(
            prompt="Review.",
            agent_name="agent-a",
            model=DEFAULT_MODEL,
            max_tokens=DEFAULT_MAX_TOKENS,
            provider=mock_provider,
            emitter=emitter,
            streaming=True,
            stream_callback=None,
        )

        assert error is None
        assert len(text) > 0
        assert mock_provider.calls[-1].method == "complete"
