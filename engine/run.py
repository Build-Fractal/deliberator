"""Engine entry point and Phase 1 orchestrator.

Wires config parsing, template filling, file inlining, concurrent dispatch,
and output writing into an end-to-end deliberation flow.

For full 5-phase runs (``phase="all"``), delegates to
``engine.phases.run_pipeline``.  For single-phase runs (e.g.
``phase="review"``), the legacy ``run_phase1`` path is preserved for
backward compatibility.
"""

from __future__ import annotations

import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from engine._prompt import (
    INLINE_CONTENT_WARN_LIMIT,
    _assemble_prompt,
    _collect_files_from_path,
    _inline_files,
    _read_file_safe,
)
from engine.config import AgentConfig, EngineConfig, parse_config
from engine.dispatch import DEFAULT_MAX_TOKENS, DEFAULT_MODEL, dispatch_phase
from engine.events import (
    CallbackEmitter,
    EngineEvent,
    EventEmitter,
    NullEmitter,
    PhaseCompleted,
    PhaseStarted,
)
from engine.output import OutputManager
from engine.phases import PipelineResult, run_pipeline
from engine.auth import resolve_provider
from engine.dispatch import AnyProvider, ModelProviderExecutionAdapter
from engine.execution.provider import ExecutionProvider
from engine.execution.providers import PROVIDER_REGISTRY, get_provider
from engine.providers import ModelProvider
from engine.templates import (
    TemplateError,
    build_review_context,
    fill_template,
    find_templates_dir,
    load_template,
)


# ---------------------------------------------------------------------------
# Provider resolution
# ---------------------------------------------------------------------------


def resolve_execution_provider(
    provider_name: str,
    model: str = DEFAULT_MODEL,
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> ExecutionProvider:
    """Resolve a provider name to an :class:`ExecutionProvider`.

    Resolution order:
    1. **Legacy auth providers** (``anthropic``, ``openai``) — these have
       OAuth credential management in :func:`~engine.auth.resolve_provider`.
       Use the legacy path (which handles env vars + OAuth tokens), then
       wrap in :class:`ModelProviderExecutionAdapter`.  This preserves
       ``deliberator login`` / credential store support.
    2. **Execution registry** — for all other names (``claude-code``,
       ``ollama``, ``mock``, etc.), instantiate from
       :data:`~engine.execution.providers.PROVIDER_REGISTRY` directly.
       These providers handle their own auth (env vars, local servers,
       or no auth needed).
    3. **Legacy fallback** — if not in the registry, try
       :func:`resolve_provider` as a last resort (future ModelProviders).

    Args:
        provider_name: Provider identifier (e.g., ``"claude-code"``).
        model: Default model for the adapter (only used in legacy path).
        max_tokens: Default max tokens for the adapter (only used in
            legacy path).

    Returns:
        An :class:`ExecutionProvider` instance, ready for dispatch.
    """
    # Path 1: providers with OAuth support — use legacy resolve_provider
    # which handles env vars, credential store, and OAuth token refresh.
    _LEGACY_AUTH_PROVIDERS = {"anthropic", "openai"}
    if provider_name in _LEGACY_AUTH_PROVIDERS:
        legacy_provider: ModelProvider = resolve_provider(provider_name)
        return ModelProviderExecutionAdapter(
            legacy_provider,
            model=model,
            max_tokens=max_tokens,
            name=provider_name,
        )

    # Path 2: execution registry (all other providers)
    if provider_name in PROVIDER_REGISTRY:
        return get_provider(provider_name)

    # Path 3: legacy fallback for unknown names
    legacy_provider = resolve_provider(provider_name)
    return ModelProviderExecutionAdapter(
        legacy_provider,
        model=model,
        max_tokens=max_tokens,
        name=provider_name,
    )


# ---------------------------------------------------------------------------
# Phase 1 orchestrator
# ---------------------------------------------------------------------------

async def run_phase1(
    config: EngineConfig,
    provider: AnyProvider,
    emitter: EventEmitter,
    *,
    model: str = DEFAULT_MODEL,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    config_path: Path | None = None,
) -> list[Path]:
    """Execute Phase 1 (review) of the deliberation engine.

    Steps:
        1. Create output directories
        2. Emit ``PhaseStarted``
        3. For each agent: build context → fill template → assemble prompt
        4. Dispatch all agents concurrently
        5. Write successful responses to output files
        6. Emit ``PhaseCompleted``

    Args:
        config: Parsed engine configuration.
        provider: The model provider to use for dispatch.
        emitter: Event emitter for lifecycle events.
        model: LLM model identifier (default: claude-sonnet-4-20250514).
        max_tokens: Maximum tokens per response (default: 16384).
        config_path: Original config path for template discovery.

    Returns:
        List of paths to written output files.
    """
    phase_start = time.monotonic()

    # (a) Create output directories
    output_mgr = OutputManager(config.output)
    output_mgr.create_phase1_dirs(config.agents, has_arbiter=config.arbiter is not None)

    # (b) Emit PhaseStarted
    emitter.emit(PhaseStarted(
        phase="review",
        agent_count=len(config.agents),
        timestamp=datetime.now(timezone.utc),
    ))

    # (c) Build prompts for each agent
    # Locate templates directory
    if config_path is not None:
        templates_dir = find_templates_dir(config_path)
    else:
        # Fall back to engine root's parent
        templates_dir = find_templates_dir(Path.cwd() / "deliberator.yml")

    template = load_template(templates_dir, config.mode, "review")

    # Compute base_dir for relative path display in inlined files
    base_dir = config_path.resolve().parent if config_path else Path.cwd()

    agent_prompts: list[tuple[str, str]] = []
    for agent in config.agents:
        # Build review context and fill template
        context = build_review_context(config, agent, config.output)
        filled = fill_template(template, context)

        # Assemble prompt with inlined files
        prompt = _assemble_prompt(
            filled_template=filled,
            target_files=config.target_files,
            agent_docs=agent.docs,
            base_dir=base_dir,
        )
        agent_prompts.append((agent.name, prompt))

    # (d) Dispatch all agents concurrently
    results = await dispatch_phase(
        agents=agent_prompts,
        model=model,
        max_tokens=max_tokens,
        provider=provider,
        emitter=emitter,
        phase="review",
    )

    # (e) Write successful responses to output files
    written_paths: list[Path] = []
    success_count = 0
    failure_count = 0

    for agent_name, response_text, error in results:
        if error is None:
            path = output_mgr.write_agent_output(agent_name, "review", response_text)
            written_paths.append(path)
            success_count += 1
        else:
            failure_count += 1

    # (f) Emit PhaseCompleted
    phase_duration_ms = int((time.monotonic() - phase_start) * 1000)
    emitter.emit(PhaseCompleted(
        phase="review",
        agent_count=len(config.agents),
        success_count=success_count,
        failure_count=failure_count,
        duration_ms=phase_duration_ms,
        timestamp=datetime.now(timezone.utc),
    ))

    return written_paths


# ---------------------------------------------------------------------------
# Convenience entry point
# ---------------------------------------------------------------------------

async def run_engine(
    config_path: Path,
    phase: str = "all",
    provider_name: str = "mock",
    model: str | None = None,
    rounds: int | None = None,
    emitter: EventEmitter | None = None,
) -> list[Path]:
    """Convenience function that parses config, creates provider, and runs the engine.

    This is the primary entry point used by ``__main__.py``.

    When ``phase`` is ``"all"`` (the default) or ``None``, the full 5-phase
    pipeline is executed via :func:`engine.phases.run_pipeline`.  When a
    specific phase name is given (e.g. ``"review"``), only that single phase
    runs.

    Args:
        config_path: Path to the deliberator YAML config file.
        phase: Phase to run.  ``"all"`` (default) runs the full pipeline;
            ``"review"`` runs Phase 1 only.
        provider_name: Provider identifier (``"mock"``, ``"anthropic"``, or ``"openai"``).
        model: LLM model override (uses default if ``None``).
        rounds: Override for the number of deliberation rounds (uses config
            value if ``None``).
        emitter: Optional event emitter for lifecycle events.  When ``None``
            (default), a simple stderr-printing handler is used.  Pass a
            custom emitter (e.g. a Rich-based progress handler) to control
            how events are displayed.

    Returns:
        List of paths to written output files.
    """
    # Parse config
    config = parse_config(config_path)

    # Apply rounds override if specified
    if rounds is not None:
        config = config.model_copy(update={"rounds": rounds})

    # Resolve model early — needed by both provider creation and dispatch
    effective_model = model or DEFAULT_MODEL

    # Create provider via the execution registry (preferred) or fall back
    # to legacy ModelProvider resolution (OAuth, env vars) wrapped in adapter.
    provider: ExecutionProvider = resolve_execution_provider(
        provider_name,
        model=effective_model,
        max_tokens=DEFAULT_MAX_TOKENS,
    )

    # Use caller-supplied emitter, or fall back to simple stderr handler
    if emitter is None:
        def _stderr_handler(event: EngineEvent) -> None:
            if isinstance(event, PhaseStarted):
                print(f"[PHASE_STARTED] {event.phase}: {event.agent_count} agents", file=sys.stderr)
            elif hasattr(event, "agent_name") and hasattr(event, "model"):
                # AgentDispatched
                print(f"[AGENT_DISPATCHED] {event.agent_name} → {event.model}", file=sys.stderr)
            elif hasattr(event, "agent_name") and hasattr(event, "success"):
                # AgentCompleted
                status = "✓" if event.success else f"✗ ({event.error})"
                print(
                    f"[AGENT_COMPLETED] {event.agent_name}: {status} ({event.duration_ms}ms)",
                    file=sys.stderr,
                )
            elif isinstance(event, PhaseCompleted):
                print(
                    f"[PHASE_COMPLETED] {event.phase}: "
                    f"{event.success_count}/{event.agent_count} succeeded, "
                    f"{event.failure_count} failed ({event.duration_ms}ms)",
                    file=sys.stderr,
                )

        emitter = CallbackEmitter(_stderr_handler)

    # Full 5-phase pipeline
    if phase in ("all", None):
        result = await run_pipeline(
            config=config,
            provider=provider,
            emitter=emitter,
            model=effective_model,
            config_path=config_path,
        )
        return list(result.written_files)

    # Single-phase execution (backward compatible Phase 1)
    if phase == "review":
        return await run_phase1(
            config=config,
            provider=provider,
            emitter=emitter,
            model=effective_model,
            config_path=config_path,
        )

    raise ValueError(
        f"Phase '{phase}' is not supported as a standalone phase. "
        "Use 'all' for the full pipeline or 'review' for Phase 1 only."
    )
