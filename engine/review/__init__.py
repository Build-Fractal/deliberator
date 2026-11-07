"""Structured review: Deliberator as a review backend (spec 074).

Reviewers bound to roles produce findings, challenge each other's findings, answer objections,
and an arbiter rules only on what stays contested. Every reply is one terse JSON object; the
record is phase envelopes plus a move log, folded into an argument graph (lattice-graph), and
the verdict is computed from which findings stand, not narrated by a synthesis call.

    from engine.review import run_review, Reviewer
    result = await run_review([("plan.md", text)], provider=provider, out_dir=Path("reviews"))
    result.verdict      # "pass" | "changes" | "block"
    result.exit_code    # 0 | 1 | 2

Needs the graph extra: ``pip install 'deliberator[graph]'``.
"""

from engine.review.protocol import Protocol, load_protocol
from engine.review.report import Finding, ReviewResult
from engine.review.run import DEFAULT_LENSES, Reviewer, run_review

__all__ = [
    "DEFAULT_LENSES",
    "Finding",
    "Protocol",
    "ReviewResult",
    "Reviewer",
    "load_protocol",
    "run_review",
]
