"""Multi-round pipeline orchestrator for the conversus engine.

Executes the full deliberation pipeline:
  Phase 1 (review) → iteration loop [Phase 2 (cross-review) → Phase 3 (revision)]
  → Phase 4 (disputes) → Phase 5 (synthesis)

Supports multi-round deliberation with stagnation detection, Phase 6
arbitration (conditional), and cross-round synthesis (after 2+ rounds).

Enforces phase barriers (no phase starts until the previous completes),
tracks active agents across phases for continue-with-N-1 failure semantics,
and emits lifecycle events for every phase.

The pipeline writes all output files via ``OutputManager`` and returns a
``PipelineResult`` summarizing what was produced.
"""

from __future__ import annotations

import asyncio
import time
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel

from engine.cancel import CancellationFlag
from engine.config import AgentConfig, EngineConfig
from engine.dispatch import (
    DEFAULT_MAX_TOKENS,
    DEFAULT_MODEL,
    dispatch_phase,
    dispatch_phase_with_retry,
)
from engine.events import (
    EventEmitter,
    PhaseCompleted,
    PhaseStarted,
)
from engine.output import OutputManager
from engine.dispatch import AnyProvider
from engine._prompt import _assemble_prompt, _read_file_safe
from engine.templates import (
    build_arbitration_context,
    build_cross_review_context,
    build_cross_round_synthesis_context,
    build_disputes_context,
    build_review_context,
    build_revision_context,
    build_synthesis_context,
    fill_template,
    find_templates_dir,
    load_template,
    _extract_remaining_disputes,
)
from linter.arbitration_parser import extract_addressed_disputes
from linter.models import InfluenceLevel
from linter.quality import check_disagreement


# ---------------------------------------------------------------------------
# Result model
# ---------------------------------------------------------------------------


class PipelineResult(BaseModel):
    """Summary of a completed pipeline run."""

    model_config = {"frozen": True}

    output_dir: Path
    written_files: list[Path]
    active_agents: list[str]
    phases_completed: int
    total_dispatches: int
    rounds_completed: int = 1
    termination_reason: str | None = None  # "converged", "stagnation", "max_rounds"
    arbitration_ran: bool = False


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class PipelineError(Exception):
    """Raised when the pipeline cannot continue."""

    pass


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _assemble_phase_prompt(
    filled_template: str,
    target_files: list[Path],
    agent_docs: list[Path],
    prior_output_files: list[Path] | None = None,
    base_dir: Path | None = None,
) -> str:
    """Assemble a prompt that includes both target files and prior-phase outputs.

    Extends the standard ``_assemble_prompt`` by prepending any prior-phase
    output files (reviews, cross-reviews, revisions) before the target files
    and agent docs.
    """
    # For phases 2-5, we inline prior output files so the agent can see them
    prior_sections: list[str] = []
    if prior_output_files:
        for pf in prior_output_files:
            content = _read_file_safe(pf)
            if content is None:
                continue
            if base_dir:
                try:
                    display_path = pf.relative_to(base_dir)
                except ValueError:
                    display_path = pf
            else:
                display_path = pf
            prior_sections.append(
                f"--- FILE: {display_path} ---\n{content}\n--- END FILE ---\n"
            )

    # Build the base prompt using the existing assembler
    base_prompt = _assemble_prompt(
        filled_template=filled_template,
        target_files=target_files,
        agent_docs=agent_docs,
        base_dir=base_dir,
    )

    if prior_sections:
        return "\n".join(prior_sections) + "\n\n" + base_prompt
    return base_prompt


def _emit_phase_started(
    emitter: EventEmitter, phase: str, agent_count: int
) -> None:
    emitter.emit(
        PhaseStarted(
            phase=phase,
            agent_count=agent_count,
            timestamp=datetime.now(timezone.utc),
        )
    )


def _emit_phase_completed(
    emitter: EventEmitter,
    phase: str,
    agent_count: int,
    success_count: int,
    failure_count: int,
    start_time: float,
) -> None:
    duration_ms = int((time.monotonic() - start_time) * 1000)
    emitter.emit(
        PhaseCompleted(
            phase=phase,
            agent_count=agent_count,
            success_count=success_count,
            failure_count=failure_count,
            duration_ms=duration_ms,
            timestamp=datetime.now(timezone.utc),
        )
    )


# ---------------------------------------------------------------------------
# Synthesis metadata injection
# ---------------------------------------------------------------------------


def _build_metadata_block(
    *,
    active_agents: list[str],
    mode: str,
    phases_completed: int,
    iterations: int,
    round_num: int | None = None,
) -> str:
    """Build the ``<!-- CONVERSUS:METADATA ... -->`` block prepended to every
    synthesis ``final.md``.

    This block is the authoritative source of ``agent_count``,
    ``agent_names``, ``mode``, and ``phases_completed`` for downstream
    parsers — the engine knows these values deterministically from its own
    run state, so injecting them eliminates parser reliance on whether the
    LLM synthesizer remembered to recite them in prose.

    The format is stable and machine-readable so parsers can trust it across
    template changes and LLM drift.
    """
    agent_names = ", ".join(active_agents)
    lines = [
        "<!-- CONVERSUS:METADATA",
        f"agents: {len(active_agents)}",
        f"agent_names: {agent_names}",
        f"mode: {mode}",
        f"phases_completed: {phases_completed}",
        f"iterations: {iterations}",
    ]
    if round_num is not None:
        lines.append(f"round: {round_num}")
    lines.append("-->")
    return "\n".join(lines) + "\n\n"


# ---------------------------------------------------------------------------
# Pipeline — single round helper
# ---------------------------------------------------------------------------


class _RoundResult:
    """Internal mutable container for a single round's outputs."""

    __slots__ = (
        "written_files",
        "active_agents",
        "phases_completed",
        "total_dispatches",
        "synthesis_text",
    )

    def __init__(self) -> None:
        self.written_files: list[Path] = []
        self.active_agents: list[str] = []
        self.phases_completed: int = 0
        self.total_dispatches: int = 0
        self.synthesis_text: str = ""


def _build_agent_overrides(
    agents: list[AgentConfig],
    provider_resolver: Any = None,
) -> tuple[dict[str, AnyProvider], dict[str, str], dict[str, int]]:
    """Build per-agent provider, model, and timeout override dicts.

    Returns ``(agent_providers, agent_models, agent_timeouts)`` dicts
    keyed by agent name.

    Args:
        agents: List of agent configs from the engine config.
        provider_resolver: Callable that maps provider name -> ExecutionProvider.
    """
    agent_providers: dict[str, AnyProvider] = {}
    agent_models: dict[str, str] = {}
    agent_timeouts: dict[str, int] = {}

    for agent in agents:
        if agent.provider is not None and provider_resolver is not None:
            agent_providers[agent.name] = provider_resolver(agent.provider)
        if agent.agent_model is not None:
            agent_models[agent.name] = agent.agent_model
        if agent.timeout is not None:
            agent_timeouts[agent.name] = agent.timeout

    return agent_providers, agent_models, agent_timeouts


async def _run_single_round(
    config: EngineConfig,
    provider: AnyProvider,
    emitter: EventEmitter,
    output_mgr: OutputManager,
    templates_dir: Path,
    base_dir: Path,
    *,
    model: str,
    max_tokens: int,
    round_num: int = 1,
    round_base: Path | None = None,
    prior_synthesis_path: str | None = None,
    prior_round_dir: str | None = None,
    prior_arbitration_path: Path | None = None,
    cancel: CancellationFlag | None = None,
    agent_providers: dict[str, AnyProvider] | None = None,
    agent_models: dict[str, str] | None = None,
) -> _RoundResult:
    """Execute phases 1-5 for a single round, returning aggregated results.

    This is the inner loop extracted from the original ``run_pipeline``.
    All output paths are computed relative to *round_base* (or
    ``output_mgr.output_dir`` when *round_base* is ``None``).
    """
    rr = _RoundResult()
    effective_base = round_base if round_base is not None else output_mgr.output_dir

    # Per-agent overrides forwarded to every dispatch_phase call
    _hetero_kw: dict = {}
    if agent_providers:
        _hetero_kw["agent_providers"] = agent_providers
    if agent_models:
        _hetero_kw["agent_models"] = agent_models

    # Round-aware keyword args for context builders
    round_kw: dict = dict(
        round=round_num,
        prior_synthesis_path=prior_synthesis_path,
        prior_round_dir=prior_round_dir,
        prior_arbitration_path=prior_arbitration_path,
    )

    # ── Phase 1: Review ──────────────────────────────────────────────
    if cancel and cancel.is_cancelled:
        raise asyncio.CancelledError("Deliberation cancelled")
    phase1_start = time.monotonic()
    _emit_phase_started(emitter, "review", len(config.agents))

    review_template = load_template(templates_dir, config.mode, "review")

    agent_prompts: list[tuple[str, str]] = []
    for agent in config.agents:
        context = build_review_context(config, agent, effective_base, **round_kw)
        filled = fill_template(review_template, context)
        prompt = _assemble_phase_prompt(
            filled_template=filled,
            target_files=config.target_files,
            agent_docs=agent.docs,
            base_dir=base_dir,
        )
        agent_prompts.append((agent.name, prompt))

    results = await dispatch_phase(
        agents=agent_prompts,
        model=model,
        max_tokens=max_tokens,
        provider=provider,
        emitter=emitter,
        phase="review",
        **_hetero_kw,
    )
    rr.total_dispatches += len(agent_prompts)

    active_agents: list[str] = []
    success_count = 0
    failure_count = 0
    for agent_name, response_text, error in results:
        if error is None:
            path = output_mgr.get_review_path(agent_name, round_base=round_base)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(response_text, encoding="utf-8")
            rr.written_files.append(path)
            active_agents.append(agent_name)
            success_count += 1
        else:
            failure_count += 1

    _emit_phase_completed(
        emitter, "review", len(config.agents), success_count, failure_count, phase1_start
    )
    rr.phases_completed += 1

    if len(active_agents) < 1:
        raise PipelineError(
            "All agents failed in Phase 1 (review). Cannot continue pipeline."
        )

    # ── Iteration loop: Phase 2 (cross-review) → Phase 3 (revision) ─
    for iteration in range(1, config.iterations + 1):
        # ── Phase 2: Cross-review ────────────────────────────────────
        if cancel and cancel.is_cancelled:
            raise asyncio.CancelledError("Deliberation cancelled")
        cross_review_pairs: list[tuple[str, str]] = []
        pair_names: list[str] = []

        cross_review_template = load_template(
            templates_dir, config.mode, "cross-review"
        )

        phase2_count = 0
        for reviewer in active_agents:
            for reviewed in active_agents:
                if reviewer != reviewed:
                    phase2_count += 1

        phase2_start = time.monotonic()
        _emit_phase_started(emitter, "cross-review", phase2_count)

        for reviewer in active_agents:
            reviewer_agent = None
            for a in config.agents:
                if a.name == reviewer:
                    reviewer_agent = a
                    break

            for reviewed in active_agents:
                if reviewer == reviewed:
                    continue

                cr_context = build_cross_review_context(
                    config, reviewer, reviewed, effective_base, iteration,
                    **round_kw,
                )
                filled = fill_template(cross_review_template, cr_context)

                prior_files = [
                    output_mgr.position_path(reviewed, iteration, round_base=round_base),
                    output_mgr.position_path(reviewer, iteration, round_base=round_base),
                ]

                prompt = _assemble_phase_prompt(
                    filled_template=filled,
                    target_files=config.target_files,
                    agent_docs=reviewer_agent.docs if reviewer_agent else [],
                    prior_output_files=prior_files,
                    base_dir=base_dir,
                )
                dispatch_name = f"{reviewer}→{reviewed}"
                cross_review_pairs.append((dispatch_name, prompt))
                pair_names.append(f"{reviewer}:{reviewed}")

        cr_results = await dispatch_phase(
            agents=cross_review_pairs,
            model=model,
            max_tokens=max_tokens,
            provider=provider,
            emitter=emitter,
            phase="cross-review",
            **_hetero_kw,
        )
        rr.total_dispatches += len(cross_review_pairs)

        cr_success = 0
        cr_failure = 0
        for i, (dispatch_name, response_text, error) in enumerate(cr_results):
            reviewer, reviewed = pair_names[i].split(":")
            if error is None:
                path = output_mgr.get_cross_review_path(reviewer, reviewed, round_base=round_base)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(response_text, encoding="utf-8")
                rr.written_files.append(path)
                cr_success += 1
            else:
                cr_failure += 1

        _emit_phase_completed(
            emitter, "cross-review", phase2_count, cr_success, cr_failure, phase2_start
        )
        rr.phases_completed += 1

        # ── Phase 3: Revision ────────────────────────────────────────
        if cancel and cancel.is_cancelled:
            raise asyncio.CancelledError("Deliberation cancelled")
        phase3_start = time.monotonic()
        _emit_phase_started(emitter, "revision", len(active_agents))

        revision_template = load_template(templates_dir, config.mode, "revision")

        revision_prompts: list[tuple[str, str]] = []
        for agent_name in active_agents:
            agent_config = None
            for a in config.agents:
                if a.name == agent_name:
                    agent_config = a
                    break

            other_agents = [n for n in active_agents if n != agent_name]
            rev_context = build_revision_context(
                config, agent_name, effective_base, iteration, other_agents,
                **round_kw,
            )
            filled = fill_template(revision_template, rev_context)

            prior_files = [output_mgr.get_review_path(agent_name, round_base=round_base)]
            for other in other_agents:
                prior_files.append(
                    output_mgr.get_cross_review_path(other, agent_name, round_base=round_base)
                )
                prior_files.append(
                    output_mgr.get_cross_review_path(agent_name, other, round_base=round_base)
                )

            prompt = _assemble_phase_prompt(
                filled_template=filled,
                target_files=config.target_files,
                agent_docs=agent_config.docs if agent_config else [],
                prior_output_files=prior_files,
                base_dir=base_dir,
            )
            revision_prompts.append((agent_name, prompt))

        rev_results = await dispatch_phase(
            agents=revision_prompts,
            model=model,
            max_tokens=max_tokens,
            provider=provider,
            emitter=emitter,
            phase="revision",
            **_hetero_kw,
        )
        rr.total_dispatches += len(revision_prompts)

        rev_success = 0
        rev_failure = 0
        surviving_agents: list[str] = []
        for agent_name, response_text, error in rev_results:
            if error is None:
                path = output_mgr.get_revision_path(agent_name, iteration, round_base=round_base)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(response_text, encoding="utf-8")
                rr.written_files.append(path)
                surviving_agents.append(agent_name)
                rev_success += 1
            else:
                rev_failure += 1

        _emit_phase_completed(
            emitter,
            "revision",
            len(active_agents),
            rev_success,
            rev_failure,
            phase3_start,
        )
        rr.phases_completed += 1

        active_agents = surviving_agents

        if len(active_agents) < 1:
            raise PipelineError(
                f"All agents failed in Phase 3 (revision, iteration {iteration}). "
                "Cannot continue pipeline."
            )

    # ── Phase 4: Disputes ────────────────────────────────────────────
    if cancel and cancel.is_cancelled:
        raise asyncio.CancelledError("Deliberation cancelled")
    phase4_start = time.monotonic()
    _emit_phase_started(emitter, "disputes", len(active_agents))

    disputes_template = load_template(templates_dir, config.mode, "disputes")

    disputes_prompts: list[tuple[str, str]] = []
    for agent_name in active_agents:
        agent_config = None
        for a in config.agents:
            if a.name == agent_name:
                agent_config = a
                break

        disp_context = build_disputes_context(
            config, agent_name, effective_base, config.iterations, active_agents,
            **round_kw,
        )
        filled = fill_template(disputes_template, disp_context)

        prior_files = output_mgr.get_all_final_revision_paths(
            active_agents, config.iterations
        )

        prompt = _assemble_phase_prompt(
            filled_template=filled,
            target_files=config.target_files,
            agent_docs=agent_config.docs if agent_config else [],
            prior_output_files=prior_files,
            base_dir=base_dir,
        )
        disputes_prompts.append((agent_name, prompt))

    disp_results = await dispatch_phase(
        agents=disputes_prompts,
        model=model,
        max_tokens=max_tokens,
        provider=provider,
        emitter=emitter,
        phase="disputes",
        **_hetero_kw,
    )
    rr.total_dispatches += len(disputes_prompts)

    disp_success = 0
    disp_failure = 0
    for agent_name, response_text, error in disp_results:
        if error is None:
            path = output_mgr.get_disputes_path(agent_name, round_base=round_base)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(response_text, encoding="utf-8")
            rr.written_files.append(path)
            disp_success += 1
        else:
            disp_failure += 1

    _emit_phase_completed(
        emitter, "disputes", len(active_agents), disp_success, disp_failure, phase4_start
    )
    rr.phases_completed += 1

    # ── Phase 5: Synthesis ───────────────────────────────────────────
    if cancel and cancel.is_cancelled:
        raise asyncio.CancelledError("Deliberation cancelled")
    phase5_start = time.monotonic()
    _emit_phase_started(emitter, "synthesis", 1)

    synthesis_template = load_template(templates_dir, config.mode, "synthesis")

    synth_context = build_synthesis_context(
        config, effective_base, config.iterations, active_agents=active_agents,
        **round_kw,
    )
    filled = fill_template(synthesis_template, synth_context)

    prior_files_list: list[Path] = []
    prior_files_list.extend(output_mgr.get_all_review_paths(active_agents))
    prior_files_list.extend(output_mgr.get_all_cross_review_paths(active_agents))
    prior_files_list.extend(
        output_mgr.get_all_final_revision_paths(active_agents, config.iterations)
    )
    prior_files_list.extend(output_mgr.get_all_disputes_paths(active_agents))

    prompt = _assemble_phase_prompt(
        filled_template=filled,
        target_files=config.target_files,
        agent_docs=[],
        prior_output_files=prior_files_list,
        base_dir=base_dir,
    )

    # Terminal-phase isolation: use the retry-wrapped dispatcher.
    # Synthesis is a single-agent dispatch whose prompt is the union of
    # all prior phase outputs — it disproportionately encounters
    # rate-limit and prompt-size failures (see engine.dispatch module
    # docstring + project_conversus_arbitration_crash memory).
    synth_results = await dispatch_phase_with_retry(
        agents=[("synthesizer", prompt)],
        model=model,
        max_tokens=max_tokens,
        provider=provider,
        emitter=emitter,
        phase="synthesis",
        **_hetero_kw,
    )
    rr.total_dispatches += 1

    synth_success = 0
    synth_failure = 0
    for _, response_text, error in synth_results:
        if error is None:
            path = output_mgr.get_synthesis_path(round_base=round_base)
            path.parent.mkdir(parents=True, exist_ok=True)
            # Prepend authoritative metadata so the parser doesn't have to
            # reconstruct agent_count / mode / phases_completed from LLM
            # prose. +1 on phases_completed accounts for this synthesis
            # phase, which hasn't been counted yet (see line below).
            metadata = _build_metadata_block(
                active_agents=active_agents,
                mode=config.mode,
                phases_completed=rr.phases_completed + 1,
                iterations=config.iterations,
                round_num=round_num,
            )
            final_text = metadata + response_text
            path.write_text(final_text, encoding="utf-8")
            rr.written_files.append(path)
            rr.synthesis_text = final_text
            synth_success += 1
        else:
            synth_failure += 1

    _emit_phase_completed(
        emitter, "synthesis", 1, synth_success, synth_failure, phase5_start
    )
    rr.phases_completed += 1

    rr.active_agents = active_agents
    return rr


# ---------------------------------------------------------------------------
# Pipeline — main entry point
# ---------------------------------------------------------------------------


async def run_pipeline(
    config: EngineConfig,
    provider: AnyProvider,
    emitter: EventEmitter,
    *,
    model: str = DEFAULT_MODEL,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    config_path: Path | None = None,
    cancel: CancellationFlag | None = None,
) -> PipelineResult:
    """Execute the full deliberation pipeline, potentially over multiple rounds.

    Single-round (``config.rounds == 1``): runs phases 1-5 in flat output,
    optionally followed by Phase 6 arbitration.

    Multi-round (``config.rounds > 1``): wraps phases 1-5 in an outer round
    loop with stagnation detection, then dispatches cross-round synthesis
    and optionally arbitration.

    Args:
        config: Parsed engine configuration.
        provider: The model provider to use for dispatch.
        emitter: Event emitter for lifecycle events.
        model: LLM model identifier.
        max_tokens: Maximum tokens per response.
        config_path: Original config path for template discovery.
        cancel: Optional cancellation flag checked between phases.

    Returns:
        A ``PipelineResult`` summarizing outputs.

    Raises:
        PipelineError: If all agents fail and the pipeline cannot continue.
        asyncio.CancelledError: If *cancel* is set before a phase starts.
    """
    output_mgr = OutputManager(config.output)
    output_mgr.create_phase1_dirs(
        config.agents, has_arbiter=config.arbiter is not None
    )

    # Locate templates directory
    if config_path is not None:
        templates_dir = find_templates_dir(config_path)
    else:
        templates_dir = find_templates_dir(Path.cwd() / "conversus.yml")

    base_dir = config_path.resolve().parent if config_path else Path.cwd()

    # Build per-agent provider/model overrides (heterogeneous deliberation)
    from engine.run import resolve_execution_provider as _resolve_ep
    _agent_providers, _agent_models, _agent_timeouts = _build_agent_overrides(
        config.agents, provider_resolver=_resolve_ep,
    )
    _hetero_kw: dict = {}
    if _agent_providers:
        _hetero_kw["agent_providers"] = _agent_providers
    if _agent_models:
        _hetero_kw["agent_models"] = _agent_models
    if _agent_timeouts:
        _hetero_kw["agent_timeouts"] = _agent_timeouts

    # Load plugins (if configured)
    from conversus.plugins.base import (
        DeliberationState,
        HookPoint,
        execute_hooks,
        load_plugins,
    )
    plugins = load_plugins(config.plugins) if config.plugins else []

    def _make_plugin_state(
        *, round_num: int = 1, synthesis: str | None = None,
        active: list[str] | None = None,
    ) -> DeliberationState:
        return DeliberationState(
            mode=config.mode,
            round=round_num,
            agents=[],
            synthesis=synthesis,
            output_dir=output_mgr.output_dir,
            config={"iterations": config.iterations, "rounds": config.rounds},
        )

    # PRE_EXECUTION hook
    if plugins:
        execute_hooks(
            HookPoint.PRE_EXECUTION, plugins,
            _make_plugin_state(), output_mgr.output_dir,
        )

    # Aggregated state across rounds
    all_written_files: list[Path] = []
    total_dispatches = 0
    total_phases_completed = 0
    final_active_agents: list[str] = []
    round_syntheses: list[str] = []
    rounds_completed = 0
    termination_reason: str | None = None
    prior_dispute_count: int | None = None
    arbitration_ran = False
    # Inter-round arbitration path (spec 006): populated after each
    # round's Phase 6 when config.arbiter.timing == "inter-round".
    # For timing == "final" (default), this stays None for all rounds.
    prior_arbitration_path: Path | None = None
    # FR-P2-6: accumulate per-round inter-round arbitration paths so the
    # cross-round synthesis can render a Resolution Attribution section
    # (spec 006 FR-020 / SC-007). Final-timing arbitrations are written
    # AFTER the round loop and are not part of this list.
    arbitration_paths: list[Path] = []

    # ── Outer round loop ─────────────────────────────────────────────
    for round_num in range(1, config.rounds + 1):
        # Directory management for multi-round
        round_base: Path | None = None
        if round_num == 2:
            output_mgr.retroactive_move_to_round_1()
            output_mgr.create_round_dirs(
                2, config.agents, has_arbiter=config.arbiter is not None
            )
            round_base = output_mgr.get_round_base(2)
            # FR-P2-3: Round 1 wrote its inter-round arbitration to the flat
            # output dir (because Round 1 ran before retroactive_move). After
            # the move, the file lives at round-1/arbitration/resolution.md.
            # Re-target prior_arbitration_path to the post-move location so
            # the next round's context builders see the actual file.
            # Note: OutputManager.get_round_base(1) returns the flat root for
            # legacy reasons; the actual round-1 directory after the move is
            # always {root}/round-1/.
            if (
                prior_arbitration_path is not None
                and not prior_arbitration_path.exists()
            ):
                moved = (
                    output_mgr._root_dir
                    / "round-1"
                    / "arbitration"
                    / "resolution.md"
                )
                if moved.exists():
                    prior_arbitration_path = moved
            # FR-P2-6: keep the cross-round accumulator in sync with the
            # retroactive move so any Round 1 arbitration path appended
            # before the move now points to its post-move location.
            for _i, _p in enumerate(arbitration_paths):
                if not _p.exists():
                    _moved = (
                        output_mgr._root_dir
                        / "round-1"
                        / "arbitration"
                        / "resolution.md"
                    )
                    if _moved.exists():
                        arbitration_paths[_i] = _moved
        elif round_num > 2:
            output_mgr.create_round_dirs(
                round_num, config.agents, has_arbiter=config.arbiter is not None
            )
            round_base = output_mgr.get_round_base(round_num)
        # Round 1: flat output (round_base=None → uses output_mgr.output_dir)

        # Build prior-round context for rounds > 1.
        prior_synthesis_path: str | None = None
        prior_round_dir: str | None = None
        if round_num > 1:
            prior_base = output_mgr.get_round_base(round_num - 1)
            prior_synthesis_path = str(
                output_mgr.get_synthesis_path(round_base=prior_base)
            )
            prior_round_dir = str(prior_base)

        rr = await _run_single_round(
            config,
            provider,
            emitter,
            output_mgr,
            templates_dir,
            base_dir,
            model=model,
            max_tokens=max_tokens,
            round_num=round_num,
            round_base=round_base,
            prior_synthesis_path=prior_synthesis_path,
            prior_round_dir=prior_round_dir,
            prior_arbitration_path=prior_arbitration_path,
            cancel=cancel,
            agent_providers=_agent_providers or None,
            agent_models=_agent_models or None,
        )

        all_written_files.extend(rr.written_files)
        total_dispatches += rr.total_dispatches
        total_phases_completed += rr.phases_completed
        final_active_agents = rr.active_agents
        rounds_completed = round_num

        # Capture synthesis text for this round
        synthesis_text = rr.synthesis_text
        round_syntheses.append(synthesis_text)

        # POST_PHASE_5 hook — after each round's synthesis
        if plugins:
            execute_hooks(
                HookPoint.POST_PHASE_5, plugins,
                _make_plugin_state(round_num=round_num, synthesis=synthesis_text),
                output_mgr.output_dir,
            )

        # ── Inter-round arbitration (spec 006) ─────────────────────
        # When timing == "inter-round", run Phase 6 between rounds
        # (but not after the LAST round — final arb handles that case
        # only for timing == "final").
        if (
            config.arbiter is not None
            and config.arbiter.timing == "inter-round"
            and round_num < config.rounds
        ):
            # Determine whether the trigger condition is met
            _should_run_arb = False
            if config.arbiter.trigger == "always":
                _should_run_arb = True
            elif config.arbiter.trigger == "disputes_remain":
                remaining = _extract_remaining_disputes(
                    synthesis_text, config.mode
                )
                _should_run_arb = bool(remaining.strip())

            if _should_run_arb:
                _arb_start = time.monotonic()
                _emit_phase_started(emitter, "arbitration", 1)

                try:
                    _arb_template = load_template(
                        templates_dir, config.mode, "arbitration"
                    )
                    _arb_round_base = (
                        round_base
                        if round_base is not None
                        else (
                            output_mgr.get_round_base(round_num)
                            if config.rounds > 1
                            else None
                        )
                    )
                    _arb_context = build_arbitration_context(
                        config,
                        config.output,
                        synthesis_text,
                        round_num,
                        round_base=_arb_round_base,
                    )
                    _arb_filled = fill_template(_arb_template, _arb_context)
                    # Arbiter is context-isolated per CONSTITUTION.md Step 4 §
                    # agent-isolation: the filled template already lists
                    # TARGET_FILES + GROUNDING_PATH + ALL_DISPUTES by path,
                    # and inlines REMAINING_DISPUTES. The agent reads
                    # referenced files on-demand via Read tool. Inlining the
                    # full target file set here re-packs the entire
                    # deliberation's input documents into the arbiter prompt,
                    # which (a) violates agent isolation (arbiter sees the
                    # same target files as review agents) and (b) causes
                    # pre-dispatch crashes when prompt assembly exceeds the
                    # claude-code subagent context budget (observed
                    # 2026-05-06 + 2026-05-07: 1ms/2ms crashes on synthesis
                    # sizes 174K-231K chars). Disputes-only-context fix per
                    # the project_conversus_arbitration_crash memory.
                    _arb_prompt = _assemble_phase_prompt(
                        filled_template=_arb_filled,
                        target_files=[],
                        agent_docs=config.arbiter.docs,
                        base_dir=base_dir,
                    )

                    # Terminal-phase isolation: retry-wrapped dispatch
                    # (see synthesis call site for rationale).
                    _arb_results = await dispatch_phase_with_retry(
                        agents=[(config.arbiter.name, _arb_prompt)],
                        model=model,
                        max_tokens=max_tokens,
                        provider=provider,
                        emitter=emitter,
                        phase="arbitration",
                        **_hetero_kw,
                    )
                    total_dispatches += 1

                    _arb_success = 0
                    _arb_failure = 0
                    for _, _arb_text, _arb_error in _arb_results:
                        if _arb_error is None:
                            _arb_path = output_mgr.get_arbitration_path(
                                round_base=_arb_round_base
                            )
                            _arb_path.parent.mkdir(parents=True, exist_ok=True)
                            _arb_path.write_text(_arb_text, encoding="utf-8")
                            all_written_files.append(_arb_path)
                            _arb_success += 1
                            arbitration_ran = True
                            # Feed this round's arbitration to the next round
                            prior_arbitration_path = _arb_path
                            # FR-P2-6: accumulate per-round arbitration paths
                            # for the cross-round synthesis Resolution
                            # Attribution section. Round 1 paths may be
                            # retroactively re-targeted on the round-2
                            # transition above.
                            arbitration_paths.append(_arb_path)
                        else:
                            _arb_failure += 1
                            _arb_path = output_mgr.get_arbitration_path(
                                round_base=_arb_round_base
                            )
                            if _arb_path.exists():
                                _arb_path.unlink()

                    _emit_phase_completed(
                        emitter, "arbitration", 1,
                        _arb_success, _arb_failure, _arb_start,
                    )
                except Exception:
                    # Arbitration failure must not abort the pipeline
                    _arb_path = output_mgr.get_arbitration_path(
                        round_base=round_base
                    )
                    if _arb_path.exists():
                        _arb_path.unlink()
                    _emit_phase_completed(
                        emitter, "arbitration", 1, 0, 1, _arb_start,
                    )

                total_phases_completed += 1

                # POST_ARBITRATION hook
                if plugins and arbitration_ran:
                    execute_hooks(
                        HookPoint.POST_ARBITRATION, plugins,
                        _make_plugin_state(round_num=round_num),
                        output_mgr.output_dir,
                    )

        # ── Stagnation / convergence detection ───────────────────────
        if config.rounds > 1:
            disagree = check_disagreement(
                synthesis_text,
                config.mode,
                influence=(
                    InfluenceLevel(config.arbiter.influence)
                    if config.arbiter else None
                ),
                # FR-P2-4 (issue #68): parse arbiter-addressed disputes
                # from the most recent ``resolution.md``. When inter-round
                # arbitration ran in this round, ``prior_arbitration_path``
                # points at that file and influence-aware adjustment in
                # check_disagreement() suppresses the matching disputes
                # (binding/recommended) or ignores them (advisory/None).
                # When no prior arbitration exists, we fall back to None,
                # preserving the pre-issue-#68 no-op path.
                arbiter_addressed=(
                    extract_addressed_disputes(prior_arbitration_path)
                    if prior_arbitration_path is not None
                    and prior_arbitration_path.exists()
                    else None
                ),
            )
            current_dispute_count = disagree.dispute_count

            if current_dispute_count == 0:
                termination_reason = "converged"
                break

            if (
                prior_dispute_count is not None
                and current_dispute_count >= prior_dispute_count
                and config.stagnation == "detect"
            ):
                termination_reason = "stagnation"
                break

            if round_num == config.rounds:
                termination_reason = "max_rounds"
                break

            prior_dispute_count = current_dispute_count

    # POST_DELIBERATION hook — after all rounds complete
    if plugins:
        execute_hooks(
            HookPoint.POST_DELIBERATION, plugins,
            _make_plugin_state(
                round_num=rounds_completed,
                synthesis=round_syntheses[-1] if round_syntheses else None,
            ),
            output_mgr.output_dir,
        )

    # ── Cross-round synthesis (after 2+ rounds) ──────────────────────
    if rounds_completed >= 2:
        crs_start = time.monotonic()
        _emit_phase_started(emitter, "cross-round-synthesis", 1)

        crs_template = load_template(
            templates_dir, config.mode, "cross-round-synthesis"
        )

        # FR-P2-6: feed accumulated inter-round arbitration outputs into
        # the cross-round synthesis so the Resolution Attribution section
        # can render with non-empty data (spec 006 FR-020 / SC-007).
        # arbitration_paths is the per-round list of resolution.md files;
        # arbitration_rulings is a single pre-formatted block of each
        # path's contents with round headers (matches the str|None shape
        # the context model expects).
        _crs_arb_paths: list[Path] | None = None
        _crs_arb_rulings: str | None = None
        if arbitration_paths:
            _crs_arb_paths = list(arbitration_paths)
            _ruling_blocks: list[str] = []
            for _round_idx, _arb_p in enumerate(arbitration_paths, start=1):
                try:
                    _ruling_text = _arb_p.read_text(encoding="utf-8")
                except OSError:
                    # If the arbitration file is missing/unreadable, skip
                    # it rather than abort the whole synthesis.
                    continue
                _ruling_blocks.append(
                    f"## Round {_round_idx} Arbitration "
                    f"({_arb_p})\n\n{_ruling_text.strip()}"
                )
            if _ruling_blocks:
                _crs_arb_rulings = "\n\n---\n\n".join(_ruling_blocks)

        crs_context = build_cross_round_synthesis_context(
            config,
            config.output,
            round_syntheses,
            rounds_completed,
            termination_reason or "max_rounds",
            arbitration_paths=_crs_arb_paths,
            arbitration_rulings=_crs_arb_rulings,
        )
        filled = fill_template(crs_template, crs_context)
        prompt = _assemble_phase_prompt(
            filled_template=filled,
            target_files=config.target_files,
            agent_docs=[],
            base_dir=base_dir,
        )

        # Terminal-phase isolation: retry-wrapped dispatch (see
        # synthesis call site for rationale).
        crs_results = await dispatch_phase_with_retry(
            agents=[("cross-round-synthesizer", prompt)],
            model=model,
            max_tokens=max_tokens,
            provider=provider,
            emitter=emitter,
            phase="cross-round-synthesis",
            **_hetero_kw,
        )
        total_dispatches += 1

        crs_success = 0
        crs_failure = 0
        for _, response_text, error in crs_results:
            if error is None:
                path = output_mgr.get_cross_round_synthesis_path()
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(response_text, encoding="utf-8")
                all_written_files.append(path)
                crs_success += 1
                # Use cross-round synthesis for arbitration evaluation
                synthesis_text = response_text
            else:
                crs_failure += 1

        _emit_phase_completed(
            emitter, "cross-round-synthesis", 1, crs_success, crs_failure, crs_start
        )
        total_phases_completed += 1
    else:
        # Single round — synthesis_text is already from the only round
        synthesis_text = round_syntheses[0] if round_syntheses else ""

    # ── Phase 6: Arbitration (conditional) ───────────────────────────
    # timing: "final" → always runs after the loop (spec 001 behaviour)
    # timing: "inter-round" → already ran per-round inside the loop;
    #   skip the post-loop arbitration entirely.
    _run_final_arbitration = (
        config.arbiter is not None
        and config.arbiter.timing == "final"
    )
    if _run_final_arbitration:
        should_arbitrate = False
        if config.arbiter.trigger == "always":
            should_arbitrate = True
        elif config.arbiter.trigger == "disputes_remain":
            remaining = _extract_remaining_disputes(synthesis_text, config.mode)
            should_arbitrate = bool(remaining.strip())

        if should_arbitrate:
            arb_start = time.monotonic()
            _emit_phase_started(emitter, "arbitration", 1)

            try:
                arb_template = load_template(
                    templates_dir, config.mode, "arbitration"
                )
                # For multi-round, arbitration resolves the final synthesis
                arb_round_base = (
                    output_mgr.get_round_base(rounds_completed)
                    if rounds_completed >= 2
                    else None
                )
                arb_context = build_arbitration_context(
                    config,
                    config.output,
                    synthesis_text,
                    rounds_completed,
                    round_base=arb_round_base,
                )
                filled = fill_template(arb_template, arb_context)
                # Arbiter context-isolation fix (final-timing dispatch);
                # see inter-round dispatch above for the full rationale.
                prompt = _assemble_phase_prompt(
                    filled_template=filled,
                    target_files=[],
                    agent_docs=config.arbiter.docs,
                    base_dir=base_dir,
                )

                # Terminal-phase isolation: retry-wrapped dispatch (see
                # synthesis call site for rationale).
                arb_results = await dispatch_phase_with_retry(
                    agents=[(config.arbiter.name, prompt)],
                    model=model,
                    max_tokens=max_tokens,
                    provider=provider,
                    emitter=emitter,
                    phase="arbitration",
                    **_hetero_kw,
                )
                total_dispatches += 1

                arb_success = 0
                arb_failure = 0
                for _, response_text, error in arb_results:
                    if error is None:
                        arb_path = output_mgr.get_arbitration_path(
                            round_base=arb_round_base
                        )
                        arb_path.parent.mkdir(parents=True, exist_ok=True)
                        arb_path.write_text(response_text, encoding="utf-8")
                        all_written_files.append(arb_path)
                        arb_success += 1
                        arbitration_ran = True
                    else:
                        arb_failure += 1
                        # Delete partial output on failure
                        arb_path = output_mgr.get_arbitration_path(
                            round_base=arb_round_base
                        )
                        if arb_path.exists():
                            arb_path.unlink()

                _emit_phase_completed(
                    emitter, "arbitration", 1, arb_success, arb_failure, arb_start
                )
            except Exception:
                # Arbitration failure must not abort the pipeline
                arb_path = output_mgr.get_arbitration_path()
                if arb_path.exists():
                    arb_path.unlink()
                _emit_phase_completed(
                    emitter, "arbitration", 1, 0, 1, arb_start
                )

            total_phases_completed += 1

            # POST_ARBITRATION hook
            if plugins and arbitration_ran:
                execute_hooks(
                    HookPoint.POST_ARBITRATION, plugins,
                    _make_plugin_state(round_num=rounds_completed),
                    output_mgr.output_dir,
                )

    return PipelineResult(
        output_dir=output_mgr._root_dir,
        written_files=all_written_files,
        active_agents=final_active_agents,
        phases_completed=total_phases_completed,
        total_dispatches=total_dispatches,
        rounds_completed=rounds_completed,
        termination_reason=termination_reason,
        arbitration_ran=arbitration_ran,
    )
