"""Rich-based result rendering for deliberation output.

Renders a :class:`linter.output_contract.DeliberatorOutput` to the
terminal using Rich panels, tables, and markdown. TTY detection is
automatic — piped output contains zero ANSI escape sequences.

Usage::

    from engine.cli.render import render_result
    from linter.output_contract import parse_synthesis

    result = parse_synthesis(synthesis_text, mode="cooperative")
    render_result(result)
"""

from __future__ import annotations

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

from linter.output_contract import DeliberatorOutput


def render_result(
    result: DeliberatorOutput,
    console: Console | None = None,
) -> None:
    """Render a deliberation result with Rich formatting.

    Parameters:
        result: The parsed deliberation output to render.
        console: Rich Console to render to. Defaults to
                 ``Console()`` (stdout, auto TTY detection).
    """
    if console is None:
        console = Console()

    # Headline in a styled panel
    console.print(
        Panel(result.headline, title="Deliberation Result", style="bold")
    )

    # Summary paragraph
    console.print(f"\n{result.summary}\n")

    # Quality indicators table
    qi = result.quality_indicators
    table = Table(title="Quality Indicators", show_header=True)
    table.add_column("Metric", style="bold")
    table.add_column("Value")

    table.add_row("Agents", str(qi.agent_count))
    table.add_row("Mode", qi.mode)
    table.add_row("Phases Completed", str(qi.phases_completed))
    table.add_row("Cross-Reviews Performed", str(qi.cross_reviews_performed))
    table.add_row("Disagreements Surfaced", str(qi.genuine_disagreements_surfaced))
    table.add_row("Disagreements Surviving", str(qi.genuine_disagreements_surviving))

    console.print(table)

    # Full analysis as rendered markdown (skip if empty)
    if result.full_analysis and result.full_analysis.strip():
        console.print()
        console.print(Markdown(result.full_analysis))
