"""Shared entry points for the CLI and MCP review surfaces.

Both surfaces turn the same inputs (targets, provider name, reviewer specs) into one call to
`run_review`; this module holds that translation so they cannot drift.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from engine.review.run import DEFAULT_ARBITER, Reviewer, run_review


class ReviewInputError(ValueError):
    """Bad review input: no targets, an unreadable file, a malformed reviewer spec."""


def parse_reviewers(specs: list[str] | tuple[str, ...] | None) -> list[Reviewer] | None:
    """`"name:lens"` strings as reviewers; None (the defaults) when there are none."""
    if not specs:
        return None
    reviewers = []
    for spec in specs:
        name, sep, lens = spec.partition(":")
        if not sep or not name.strip() or not lens.strip():
            raise ReviewInputError(f'reviewer must be "name:lens", got {spec!r}')
        reviewers.append(Reviewer(name.strip(), lens.strip()))
    return reviewers


def load_targets(paths: list[str] | tuple[str, ...], text: str = "", text_name: str = "output",
                 *, stdin: Any = None) -> list[tuple[str, str]]:
    """(name, text) for each file, `-` for stdin, plus inline `text` when given."""
    loaded: list[tuple[str, str]] = []
    for p in paths:
        if p == "-":
            if stdin is None:
                raise ReviewInputError('"-" (stdin) is only available on the command line')
            loaded.append(("stdin", stdin.read()))
            continue
        path = Path(p)
        if not path.is_file():
            raise ReviewInputError(f"not a file: {p}")
        loaded.append((path.name, path.read_text(encoding="utf-8", errors="replace")))
    if text:
        loaded.append((text_name, text))
    if not any(t.strip() for _, t in loaded):
        raise ReviewInputError("nothing to review")
    return loaded


def build_provider(provider: str, model: str | None = None, effort: str | None = "low") -> Any:
    """An execution provider for review calls.

    claude-code gets lean calls: no tools, MCP servers, skills or settings (~690 tokens of
    overhead per call instead of ~39,000). Review replies are plain JSON; no tools are needed.
    """
    if provider == "claude-code":
        from engine.execution.providers import get_provider

        return get_provider("claude-code", lean=True, effort=effort)
    from engine.run import DEFAULT_MAX_TOKENS, DEFAULT_MODEL, resolve_execution_provider

    return resolve_execution_provider(
        provider, model=model or DEFAULT_MODEL, max_tokens=DEFAULT_MAX_TOKENS
    )


async def review_targets(
    targets: list[tuple[str, str]],
    *,
    provider: str,
    out_dir: Path,
    model: str | None = None,
    reviewers: list[Reviewer] | None = None,
    arbiter: bool = True,
    effort: str | None = "low",
    run_id: str | None = None,
):
    """Build the provider and run one review. Returns a `ReviewResult`."""
    execution = build_provider(provider, model, effort)
    return await run_review(
        targets,
        provider=execution,
        out_dir=out_dir,
        model=model,
        reviewers=reviewers,
        arbiter=DEFAULT_ARBITER if arbiter else None,
        run_id=run_id,
    )
