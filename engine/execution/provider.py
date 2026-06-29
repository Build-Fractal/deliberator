"""Execution provider protocol for agentic task dispatch.

This module defines the ``ExecutionProvider`` protocol (spec 042) — the
abstraction through which the deliberator engine dispatches agentic tasks to
external runtimes (Claude Code CLI, OpenCode HTTP server, Aider subprocess,
direct LLM APIs, future A2A servers, etc.).

This is distinct from :mod:`engine.providers`' ``ModelProvider``, which is
the raw LLM-completion abstraction (text in → text out).  ``ExecutionProvider``
is the *task-level* abstraction: a task has a prompt, read paths, an output
path, and metadata — and the provider decides *how* to execute it (subprocess,
HTTP, direct API call).

The data-type shape is intentionally A2A-Task-Request-compatible per binding
condition #1 of the spec 042 arbitration ruling.  Providers that do not need
the full structured shape use :meth:`ExecutionTask.from_prompt` for the flat
compatibility path, which constructs an ``ExecutionTask`` with a single text
part.  When deliberator later ships an ``A2AProvider`` wrapping a live A2A
server, no rewrite of the task shape is required — the fields already map
one-to-one to A2A Task Request semantics.

See
`specs/042-execution-providers/spec.md <../../specs/042-execution-providers/spec.md>`_
§0 (Decision Record) and §13 (Binding Conditions) for the full ruling.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta
from typing import Any, Literal, Protocol, runtime_checkable

from engine.providers import ProviderError

# ---------------------------------------------------------------------------
# Structured task shape (A2A-Task-Request-compatible per binding condition #1)
# ---------------------------------------------------------------------------


#: Media types supported inside an ``ExecutionTask`` text part.  Kept as a
#: closed ``Literal`` so downstream consumers (providers, renderers, the
#: MCP server in spec 049) can dispatch exhaustively.
TaskPartMediaType = Literal["text/plain", "text/markdown"]


@dataclass(frozen=True)
class TaskPart:
    """A structured content part inside an :class:`ExecutionTask`.

    Mirrors the A2A Task Request ``message.parts`` shape.  Most deliberator
    tasks carry a single part (the filled phase-template prompt), but the
    structured list exists so providers can attach additional context
    without losing semantic boundaries (e.g., an agent identity block
    separate from the phase template).

    Attributes:
        content: The text content of the part.
        media_type: The MIME type of ``content``.  Defaults to
            ``"text/markdown"`` because deliberator phase templates are
            markdown by construction.
    """

    content: str
    media_type: TaskPartMediaType = "text/markdown"


@dataclass(frozen=True)
class Reference:
    """A structured file reference inside an :class:`ExecutionTask`.

    Mirrors the A2A Task Request ``message.references`` shape.  A reference
    is a pointer to a file the agent should read as input context.  Providers
    that support tool use (e.g., ``claude-code``) pass references to the
    agent as read paths; providers that do not support tool use
    (e.g., direct ``anthropic``) pre-read the contents into the prompt.

    Attributes:
        uri: The reference target.  Currently file-system paths only; future
            providers may accept ``https://``, ``git://``, or custom schemes.
        description: Optional human-readable label for the reference.
    """

    uri: str
    description: str | None = None


# ---------------------------------------------------------------------------
# Cost and duration (binding conditions #5 and #6)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Cost:
    """Per-execution cost telemetry (binding condition #5).

    Every provider that can report cost data must populate this structure
    on :attr:`ExecutionResult.cost`.  Providers that cannot report cost
    leave the result's ``cost`` field as ``None`` rather than zero — the
    distinction between "unknown" and "zero" is load-bearing for downstream
    aggregation in the command center (spec 040) and monetization tier
    tracking (spec 033).

    Attributes:
        input_tokens: Tokens consumed reading the prompt/references.
        output_tokens: Tokens produced in the response.
        usd: Dollar cost.  ``None`` if the provider reports tokens but not
            a dollar amount (the engine may compute it downstream from a
            pricing table).
        currency: ISO 4217 currency code.  Always ``"USD"`` in v1.
    """

    input_tokens: int = 0
    output_tokens: int = 0
    usd: float | None = None
    currency: str = "USD"


#: Alias for the duration field on :class:`ExecutionResult`.
#:
#: Binding condition #6 requires a structured duration type that is
#: compatible with spec 047's ``Duration``.  Until spec 047 ships, we use
#: :class:`datetime.timedelta` from the stdlib — it is convertible with
#: zero precision loss for any duration under ~100 years, which covers
#: every agent execution deliberator will ever see.  When spec 047 lands,
#: this alias is redefined to point at ``deliberator.schemas.duration.Duration``
#: and existing code continues to work via implicit conversion.
Duration = timedelta


# ---------------------------------------------------------------------------
# ExecutionTask and ExecutionResult
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ExecutionTask:
    """A single agent task to execute.

    The canonical shape is A2A-Task-Request-compatible: structured
    :attr:`parts` for content, structured :attr:`references` for input
    files, :attr:`output_path` for the expected write target, and arbitrary
    :attr:`metadata` for phase/agent/mode context.  The :attr:`stream`
    flag is reserved for future streaming support (spec 042 §12 Q4) and
    is ignored by v1 providers.

    Most callers do not construct ``ExecutionTask`` directly — they use
    :meth:`from_prompt`, the flat compatibility constructor that builds
    a single-part task from a prompt string and a list of read paths.
    ``from_prompt`` is the path binding condition #1 reserves for
    subprocess and direct-API providers that do not need the full A2A
    structure.

    Attributes:
        parts: Structured content parts.  At least one part is required.
        references: Structured file references.  May be empty.
        output_path: Absolute path where the provider's output must be
            written.  Providers that capture output in-memory (direct API
            callers) return the content on :attr:`ExecutionResult.content`
            and the engine writes it to this path post-hoc.
        metadata: Execution metadata.  Reserved keys: ``phase``,
            ``agent_name``, ``mode``, ``round``, ``timeout`` (seconds).
            Unknown keys are passed through to provider-specific options.
        stream: Whether the provider should stream output (v2, ignored
            in v1 — flag exists so the protocol shape is stable).
    """

    parts: tuple[TaskPart, ...]
    output_path: str
    references: tuple[Reference, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
    stream: bool = False

    def __post_init__(self) -> None:
        if not self.parts:
            raise ValueError("ExecutionTask requires at least one part")
        if not self.output_path:
            raise ValueError("ExecutionTask requires a non-empty output_path")

    @classmethod
    def from_prompt(
        cls,
        prompt: str,
        output_path: str,
        *,
        read_paths: list[str] | tuple[str, ...] | None = None,
        metadata: dict[str, Any] | None = None,
        stream: bool = False,
    ) -> ExecutionTask:
        """Construct an ``ExecutionTask`` from a flat prompt + read paths.

        This is the compatibility path for providers that do not need the
        full A2A-structured shape — subprocess providers (``claude-code``,
        ``aider``, ``opencode``) and direct-API providers (``anthropic``,
        ``litellm``).  They pass a single prompt string and a list of file
        paths; this constructor wraps them in the canonical structured
        shape without loss.

        Binding condition #1 of the spec 042 ruling mandates that this
        constructor exists from Week 1, so the protocol shape is stable
        regardless of whether the caller speaks the structured form.

        Args:
            prompt: The filled phase-template text.  Becomes a single
                ``TaskPart`` with ``media_type="text/markdown"``.
            output_path: Absolute path where the provider must write.
            read_paths: Optional iterable of file paths the agent should
                read.  Each becomes a :class:`Reference` with no
                description.
            metadata: Optional execution metadata (phase, agent_name,
                mode, round, timeout).
            stream: Reserved for v2 streaming support.

        Returns:
            A new ``ExecutionTask`` with one part and zero or more
            references.
        """
        references = tuple(Reference(uri=p) for p in (read_paths or ()))
        return cls(
            parts=(TaskPart(content=prompt, media_type="text/markdown"),),
            output_path=output_path,
            references=references,
            metadata=dict(metadata or {}),
            stream=stream,
        )

    @property
    def prompt(self) -> str:
        """Return the concatenated text of all parts.

        Convenience for providers that operate on a single prompt string
        regardless of whether the task was constructed with
        :meth:`from_prompt` or with multiple explicit parts.
        """
        return "\n\n".join(p.content for p in self.parts)

    @property
    def read_paths(self) -> tuple[str, ...]:
        """Return the URIs of all references as a tuple.

        Convenience for providers that treat references as a flat list of
        filesystem paths (the common case for subprocess providers).
        """
        return tuple(r.uri for r in self.references)


@dataclass
class ExecutionResult:
    """Result from a single :meth:`ExecutionProvider.execute` call.

    Attributes:
        success: ``True`` if the task executed and produced output without
            provider-layer failure.  ``False`` on any :class:`ProviderError`
            or provider-specific exit condition.
        output_path: The path where the output was (or was intended to be)
            written.  Matches :attr:`ExecutionTask.output_path`.
        content: The output content, if the provider captured it in memory.
            Providers that write directly to ``output_path`` may leave this
            as ``None``; the engine is expected to read the file if
            ``content`` is ``None``.
        error: The :class:`ProviderError` that caused failure, if any.
            ``None`` on success.  The error's category is one of the
            expanded Literal values (binding condition #4) so downstream
            code can reason about failure modes without string parsing.
        cost: Per-execution cost telemetry (binding condition #5).  ``None``
            if the provider cannot report cost data.
        duration: Wall-clock duration of the execution (binding condition
            #6).  ``None`` if the provider did not measure.
        provider: The name of the provider that executed the task (e.g.,
            ``"claude-code"``, ``"anthropic"``, ``"mock"``).
        metadata: Provider-specific metadata (model used, request IDs,
            streaming chunk counts, etc.).  Opaque to the engine.
    """

    success: bool
    output_path: str
    content: str | None = None
    error: ProviderError | None = None
    cost: Cost | None = None
    duration: Duration | None = None
    provider: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# ExecutionProvider protocol
# ---------------------------------------------------------------------------


@runtime_checkable
class ExecutionProvider(Protocol):
    """Protocol for executing a single deliberator agent task.

    An execution provider accepts an :class:`ExecutionTask` and produces
    an :class:`ExecutionResult`.  The provider handles *how* to execute
    (subprocess, HTTP call, direct API, future A2A dispatch).  The engine
    handles *what* to execute (which phase, which template, which agent).

    The spec 042 ruling mandates a 4-provider v1 set: ``mock``,
    ``anthropic`` (direct API), ``claude-code`` (direct CLI subprocess,
    no ``claude-agent-sdk`` dependency), ``opencode`` (HTTP substrate).
    An optional ``litellm`` companion package ships alongside.  All four
    providers implement this protocol; v1 does not require providers to
    inherit from a common base class, but subprocess-based providers
    share a :class:`SubprocessProvider` base (to land in Phase 2) and
    HTTP-based providers share an :class:`HTTPProvider` base.

    Providers are registered via :data:`PROVIDER_REGISTRY` (entry point
    style, post-spec-032 packaging).  The engine resolves providers by
    name at run time from :class:`ExecutionTask.metadata` or from the
    ``deliberator.yml`` ``executor:`` field.
    """

    async def execute(self, task: ExecutionTask) -> ExecutionResult:
        """Execute a single agent task.

        Args:
            task: The structured task to execute.

        Returns:
            An :class:`ExecutionResult` describing success, captured output,
            error (if any), cost, and duration.
        """
        ...

    async def execute_batch(
        self,
        tasks: list[ExecutionTask] | tuple[ExecutionTask, ...],
    ) -> list[ExecutionResult]:
        """Execute multiple tasks concurrently.

        Default implementations use :func:`asyncio.gather`.  Providers with
        native batch dispatch (GitHub Actions matrix jobs, LangGraph
        fan-out, future A2A concurrent Task Requests) may override for
        better throughput.

        Args:
            tasks: The tasks to execute.  Must not be empty.

        Returns:
            Results in the same order as the input tasks.  Failures are
            reported per-task on :attr:`ExecutionResult.success`; the
            batch call does not raise on individual-task failure.
        """
        ...

    @property
    def name(self) -> str:
        """The provider's registry name (e.g., ``"claude-code"``, ``"mock"``)."""
        ...

    @property
    def supports_tool_use(self) -> bool:
        """Whether the provider gives agents autonomous file read/write tools.

        Providers with tool use (Tier 1 agent runtimes: ``claude-code``,
        ``opencode``, future ``aider``, ``copilot``) pass references to the
        agent as allowed read paths and the agent writes output itself.
        Providers without tool use (Tier 3 direct model APIs: ``anthropic``,
        ``litellm``, ``mock``) require the engine to pre-read references
        into the prompt and post-write the output from
        :attr:`ExecutionResult.content`.
        """
        ...

    @property
    def supports_pooling(self) -> bool:
        """Whether the provider can reuse a long-lived process or connection.

        Exposed on the protocol from v1 per the spec 042 ground-truth
        constraint that subprocess cold start (1-3s per invocation) × N
        phases is real.  Providers that can amortize cold start via process
        pools, persistent HTTP sessions, or long-lived server connections
        return ``True``; v1 providers that spawn-per-task return ``False``.

        The engine uses this flag to decide whether to warm pools before
        large phases (Phase 2 cross-reviews may launch 12+ agents).  In v1
        the flag is advisory; a pool implementation lands in v1.1 or v2
        after real-world cold-start measurement.
        """
        ...
