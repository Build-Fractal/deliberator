"""Mock execution provider for tests and the default Phase 2 dispatch path.

The ``mock`` provider is the reference implementation of
:class:`~engine.execution.ExecutionProvider`: the simplest possible
provider that still exercises every part of the protocol contract.  It
returns canned responses, records every call for later assertion, and
does not touch the filesystem, the network, or subprocesses.

Per the spec 042 arbitration ruling, ``mock`` is one of the four v1
providers and ships with core deliberator (not an optional package).  It
serves two jobs:

1. **Default provider during Phase 2 bring-up.**  Until ``anthropic``
   lands in Phase 2.3 and ``claude-code`` lands in Phase 3, every
   non-explicit-config caller resolves to ``mock`` via
   :func:`~engine.cli.context.detect_context`.  This forces users to
   opt into real providers via ``deliberator.yml`` rather than silently
   picking a real LLM.

2. **Test substrate for the entire engine test suite.**  The
   ``mock`` provider replaces the need for integration tests to touch
   real LLM APIs.  Test fixtures construct a ``MockExecutionProvider``
   with a canned response map and assert on the recorded call log.

The provider exposes ``supports_tool_use=False`` because it does not
give agents autonomous filesystem access — the engine is responsible
for inlining read-path contents into prompts before delegating to
``mock`` (the same pattern used by ``anthropic``, ``openai``, and any
future direct-API provider).

It also exposes ``supports_pooling=False`` because there is nothing to
pool: every call is a pure in-memory lookup.  Binding condition #5
(structured cost telemetry) is honored by reporting zero tokens and
``usd=None`` — the mock cannot spend money, but it also does not
pretend its cost is zero (which would be a real number different from
"unknown").
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field
from datetime import timedelta
from typing import TYPE_CHECKING, Any

from engine.execution.provider import (
    Cost,
    Duration,
    ExecutionResult,
    ExecutionTask,
    TaskPart,
)

if TYPE_CHECKING:
    from collections.abc import Callable


# ---------------------------------------------------------------------------
# CallRecord — what tests assert on
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CallRecord:
    """A single recorded :meth:`MockExecutionProvider.execute` invocation.

    Tests can assert on any field to verify dispatch behavior.  The record
    is frozen so tests can safely share references across assertions.

    Attributes:
        prompt: The concatenated prompt text from
            :attr:`ExecutionTask.prompt` at call time.
        output_path: The target output path the provider was asked to
            write to.
        read_paths: The tuple of reference URIs the provider was asked
            to consult.
        metadata: A snapshot of the task metadata at call time.
        stream: Whether the task had streaming requested.
        part_count: How many structured parts the task contained.
            Useful for tests that want to verify ``from_prompt()`` vs
            canonical-shape construction.
    """

    prompt: str
    output_path: str
    read_paths: tuple[str, ...]
    metadata: dict[str, Any]
    stream: bool
    part_count: int


# ---------------------------------------------------------------------------
# MockExecutionProvider
# ---------------------------------------------------------------------------


class MockExecutionProvider:
    """A deterministic in-memory :class:`ExecutionProvider` for tests and bring-up.

    The provider accepts a response template or a callable that maps a
    task to response content, records every call, and returns
    :class:`ExecutionResult` objects with realistic shapes (non-None
    duration, zero-cost reporting, correct provider name).

    Response resolution is tried in this order:

    1. **Explicit response map** keyed by ``metadata["agent_name"]`` —
       lets tests assign distinct canned responses per agent without
       coupling to prompt text.
    2. **Callable fallback** — if a ``response_fn`` was passed, it is
       called with the task and its return value is used.
    3. **Response template** — a format string with ``{prompt}``,
       ``{agent_name}``, ``{phase}``, ``{output_path}`` placeholders.

    Tests wanting simple "provider conformance" assertions use only the
    template.  Tests wanting per-agent distinct responses use the map.
    Tests wanting prompt-dependent logic use ``response_fn``.

    Args:
        response_template: Default response string.  Supports
            ``{prompt}``, ``{agent_name}``, ``{phase}``, ``{output_path}``
            and ``{model}`` placeholders.
        response_map: Optional map from ``metadata["agent_name"]`` to
            per-agent response strings.  Bypasses the template when hit.
        response_fn: Optional callable taking an :class:`ExecutionTask`
            and returning a response string.  Called when the map misses
            and before the template is used.
        simulated_latency: How long to pretend each call took, in
            seconds.  Appears on :attr:`ExecutionResult.duration`.
            Defaults to zero (tests run fast; duration is non-None so
            downstream code that reads it does not crash).
        fail_for_agents: Optional set of ``agent_name`` values that
            should result in an error result (``success=False``) with
            a :class:`~engine.providers.ProviderError` carrying
            ``category="unknown"``.  Used by tests that exercise the
            failure path.
    """

    name: str = "mock"
    supports_tool_use: bool = False
    supports_pooling: bool = False

    def __init__(
        self,
        response_template: str = "[mock:{agent_name}] {prompt}",
        *,
        response_map: dict[str, str] | None = None,
        response_fn: Callable[[ExecutionTask], str] | None = None,
        simulated_latency: float = 0.0,
        fail_for_agents: set[str] | None = None,
    ) -> None:
        self.response_template = response_template
        self.response_map: dict[str, str] = dict(response_map or {})
        self.response_fn = response_fn
        self.simulated_latency = simulated_latency
        self.fail_for_agents: set[str] = set(fail_for_agents or ())
        self.calls: list[CallRecord] = []

    # ------------------------------------------------------------------
    # ExecutionProvider protocol
    # ------------------------------------------------------------------

    async def execute(self, task: ExecutionTask) -> ExecutionResult:
        """Execute a single task and return a canned response.

        Records the call, honors the failure set, applies the response
        resolution order, and builds an :class:`ExecutionResult` with
        realistic cost, duration, and provider fields.
        """
        # Record the call first — tests want to see the call even if
        # it ends up failing via fail_for_agents.
        self.calls.append(
            CallRecord(
                prompt=task.prompt,
                output_path=task.output_path,
                read_paths=task.read_paths,
                metadata=dict(task.metadata),
                stream=task.stream,
                part_count=len(task.parts),
            ),
        )

        start = time.monotonic()
        if self.simulated_latency > 0:
            await asyncio.sleep(self.simulated_latency)

        agent_name = str(task.metadata.get("agent_name", ""))

        # Failure path — return a structured error result.
        if agent_name in self.fail_for_agents:
            from engine.providers import ProviderError

            return ExecutionResult(
                success=False,
                output_path=task.output_path,
                content=None,
                error=ProviderError(
                    f"mock provider configured to fail for agent {agent_name!r}",
                    category="unknown",
                ),
                cost=Cost(input_tokens=0, output_tokens=0, usd=None),
                duration=timedelta(seconds=time.monotonic() - start),
                provider=self.name,
                metadata={"mock_failure": True, "agent_name": agent_name},
            )

        # Success path — resolve response content.
        content = self._resolve_response(task, agent_name)

        return ExecutionResult(
            success=True,
            output_path=task.output_path,
            content=content,
            error=None,
            # Cost is reported as zero tokens with usd=None per binding
            # condition #5: unknown cost is None, not zero.  The mock
            # knows its token count (zero) but cannot report a dollar
            # amount meaningfully.
            cost=Cost(input_tokens=0, output_tokens=0, usd=None),
            duration=timedelta(seconds=time.monotonic() - start),
            provider=self.name,
            metadata={"agent_name": agent_name, "part_count": len(task.parts)},
        )

    async def execute_batch(
        self,
        tasks: list[ExecutionTask] | tuple[ExecutionTask, ...],
    ) -> list[ExecutionResult]:
        """Execute multiple tasks concurrently via ``asyncio.gather``.

        The default batch implementation from the spec 042 protocol.
        The mock provider has no native batch dispatch, so every task
        is scheduled independently.
        """
        return list(await asyncio.gather(*(self.execute(t) for t in tasks)))

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _resolve_response(self, task: ExecutionTask, agent_name: str) -> str:
        """Apply the 4-tier response resolution order."""
        # Tier 1: response map
        if agent_name and agent_name in self.response_map:
            return self.response_map[agent_name]

        # Tier 2: callable
        if self.response_fn is not None:
            return self.response_fn(task)

        # Tier 3: synthesis-phase structured template.
        # When the phase is "synthesis", return markdown that
        # parse_synthesis can parse — headline, agent metadata,
        # convergence/disputes sections.  Without this, the entire
        # smoke tier exercises the error-recovery fallback in
        # StructuredDeliberation.from_events (spec 061, dispute 1).
        phase = task.metadata.get("phase", "")
        if phase == "synthesis":
            mode = task.metadata.get("mode", "cooperative")
            return self._synthesis_template(agent_name, mode)

        # Tier 4: generic template
        return self.response_template.format(
            prompt=task.prompt,
            agent_name=agent_name,
            phase=phase,
            output_path=task.output_path,
            model=task.metadata.get("model") or "",
        )

    @staticmethod
    def _synthesis_template(agent_name: str, mode: str) -> str:
        """Return synthesis markdown parseable by output_contract.parse_synthesis.

        The template contains the minimum headings and metadata that the
        parser needs to extract: headline, agent count, mode, phases,
        convergence, and disputes sections.  Content is clearly mock
        data but structurally valid.
        """
        return (
            f"# Synthesis: Mock Deliberation Result\n\n"
            f"**Agents:** pragmatist, devils-advocate\n"
            f"**Deliberation mode:** {mode}\n"
            f"**Phases completed:** 4\n\n"
            f"## Process Summary\n\n"
            f"| Agents | 2 (pragmatist, devils-advocate) |\n"
            f"| Mode | {mode} |\n"
            f"| Phases | 5 |\n\n"
            f"### Convergence Achieved\n\n"
            f"1. **Both agents agree on the core trade-off.** "
            f"The fundamental tension is well-understood.\n"
            f"2. **Implementation approach is uncontested.** "
            f"No disputes on the technical path forward.\n\n"
            f"### Remaining Disputes\n\n"
            f"**None.** All perspectives converged during deliberation.\n\n"
            f"## Verdict\n\n"
            f"[mock:{agent_name}] This is a mock synthesis. "
            f"In a real deliberation, this section contains the "
            f"synthesizer's verdict grounded in the full adversarial record.\n"
        )

    # ------------------------------------------------------------------
    # Test helpers
    # ------------------------------------------------------------------

    def reset(self) -> None:
        """Clear the recorded call log.

        Useful in test teardown between parametrized cases so a single
        provider instance can be reused without stale call history.
        """
        self.calls.clear()

    def last_call(self) -> CallRecord:
        """Return the most recent recorded call.

        Raises:
            IndexError: If no calls have been made.  Tests should use
                this as an implicit assertion that at least one call
                occurred.
        """
        return self.calls[-1]


# ---------------------------------------------------------------------------
# Registration — called at module import time
# ---------------------------------------------------------------------------

# Register under the canonical name "mock".  The registry import happens
# at package init time, so simply importing this module is enough to make
# :func:`engine.execution.providers.get_provider` resolve ``"mock"``.
from engine.execution.providers import register_provider  # noqa: E402

register_provider("mock", MockExecutionProvider)
# "demo" alias for non-technical users — same synthetic responses,
# friendlier name for Desktop Extension users who don't know what "mock" means.
register_provider("demo", MockExecutionProvider)
