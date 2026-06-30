"""Unit tests for engine.cli.render — render_result function."""

from __future__ import annotations

from io import StringIO

import pytest
from rich.console import Console

from engine.cli.render import render_result
from linter.output_contract import DeliberatorOutput, QualityIndicators


# ── Fixtures ──────────────────────────────────────────────────────────────


def _make_console(*, force_terminal: bool = False) -> tuple[Console, StringIO]:
    """Create a Console that captures output to a StringIO buffer."""
    buf = StringIO()
    console = Console(file=buf, force_terminal=force_terminal, width=120)
    return console, buf


def _sample_output(
    *,
    headline: str = "Adopt microservices with bounded contexts",
    summary: str = "2 agents in cooperative mode completed 5 phases. 3 convergence points, 1 surviving dispute.",
    full_analysis: str = "## Analysis\n\nThis is the **full** analysis with markdown.",
    agent_count: int = 2,
    mode: str = "cooperative",
    phases_completed: int = 5,
    cross_reviews_performed: int = 2,
    disagreements_surfaced: int = 3,
    disagreements_surviving: int = 1,
    debate_transcript: str = "Full transcript here.",
) -> DeliberatorOutput:
    return DeliberatorOutput(
        headline=headline,
        summary=summary,
        full_analysis=full_analysis,
        quality_indicators=QualityIndicators(
            agent_count=agent_count,
            mode=mode,
            phases_completed=phases_completed,
            cross_reviews_performed=cross_reviews_performed,
            genuine_disagreements_surfaced=disagreements_surfaced,
            genuine_disagreements_surviving=disagreements_surviving,
        ),
        debate_transcript=debate_transcript,
    )


# ── Content rendering ────────────────────────────────────────────────────


def test_render_contains_headline() -> None:
    console, buf = _make_console()
    render_result(_sample_output(), console=console)

    output = buf.getvalue()
    assert "Adopt microservices with bounded contexts" in output


def test_render_contains_deliberation_result_title() -> None:
    console, buf = _make_console()
    render_result(_sample_output(), console=console)

    output = buf.getvalue()
    assert "Deliberation Result" in output


def test_render_contains_summary() -> None:
    console, buf = _make_console()
    render_result(_sample_output(), console=console)

    output = buf.getvalue()
    assert "2 agents in cooperative mode" in output


def test_render_contains_quality_indicator_values() -> None:
    console, buf = _make_console()
    render_result(_sample_output(), console=console)

    output = buf.getvalue()
    # Agent count
    assert "2" in output
    # Mode
    assert "cooperative" in output
    # Phases completed
    assert "5" in output
    # Column headers
    assert "Agents" in output
    assert "Mode" in output
    assert "Phases Completed" in output


def test_render_contains_disagreement_counts() -> None:
    console, buf = _make_console()
    render_result(_sample_output(), console=console)

    output = buf.getvalue()
    assert "Disagreements Surfaced" in output
    assert "Disagreements Surviving" in output
    assert "3" in output
    assert "1" in output


def test_render_contains_full_analysis_markdown() -> None:
    console, buf = _make_console()
    render_result(_sample_output(), console=console)

    output = buf.getvalue()
    # Markdown is rendered — Rich strips the ** but shows the text
    assert "Analysis" in output
    assert "full" in output


# ── Empty full_analysis ──────────────────────────────────────────────────


def test_render_with_empty_full_analysis_no_crash() -> None:
    console, buf = _make_console()
    result = _sample_output(full_analysis="")

    # Should not raise
    render_result(result, console=console)

    output = buf.getvalue()
    # Still has headline and summary
    assert "Adopt microservices" in output
    assert "2 agents" in output


def test_render_with_whitespace_only_full_analysis() -> None:
    console, buf = _make_console()
    result = _sample_output(full_analysis="   \n  \n  ")

    render_result(result, console=console)

    output = buf.getvalue()
    assert "Adopt microservices" in output


# ── TTY behavior ──────────────────────────────────────────────────────────


def test_non_tty_output_has_no_ansi_escapes() -> None:
    """Console with force_terminal=False produces clean text."""
    console, buf = _make_console(force_terminal=False)
    render_result(_sample_output(), console=console)

    output = buf.getvalue()
    assert "\x1b[" not in output


def test_tty_output_contains_ansi_escapes() -> None:
    """Console with force_terminal=True produces ANSI-styled text."""
    console, buf = _make_console(force_terminal=True)
    render_result(_sample_output(), console=console)

    output = buf.getvalue()
    assert "\x1b[" in output


# ── Default console ──────────────────────────────────────────────────────


def test_render_with_default_console_no_crash() -> None:
    """Calling render_result without a console uses stdout (no crash)."""
    # This implicitly writes to stdout — just verify it doesn't raise
    result = _sample_output()
    render_result(result)


# ── Cross-reviews column ─────────────────────────────────────────────────


def test_render_contains_cross_reviews_count() -> None:
    console, buf = _make_console()
    render_result(_sample_output(cross_reviews_performed=6), console=console)

    output = buf.getvalue()
    assert "Cross-Reviews Performed" in output
    assert "6" in output
