"""Deepeval quality tests for the deliberation pipeline (spec 061 step 7).

These tests use the deepeval library's ``GEval`` metric class to evaluate
the *qualitative* output of a real (non-mock) deliberation run.  They are
expensive — every test in this module triggers paid LLM evaluations on top
of the deliberation that produced the artifacts — so they are marked
``@pytest.mark.eval`` and excluded from default CI runs.

Run manually:

    uv run deepeval test run engine/tests/test_evals.py
    # or
    uv run --extra mcp --extra test pytest engine/tests/test_evals.py -m eval

Provider selection:

    The ``cooperative_pipeline_output`` fixture runs the deliberation once
    per test class against a small target spec.  By default it uses the
    ``anthropic`` provider, which requires ``ANTHROPIC_API_KEY``.  Set the
    ``CONVERSUS_EVAL_PROVIDER`` env var to override (e.g. to
    ``claude-code`` for host-session delegation).

Spec mapping (061 §3.2.1):

    Review independence            threshold = 0.7
    Cross-review adversarial       threshold = 0.7
    Revision responsiveness        threshold = 0.6
    Dispute specificity            threshold = 0.7
    Synthesis grounding            threshold = 0.8

The thresholds above are spec defaults.  After step 8 (baseline snapshots)
runs the suite once and captures real scores, the thresholds will be
recalibrated to ``baseline - 0.1`` per spec 061 step 7's calibration plan.

    # TODO(spec-061-step8): calibrate thresholds from baseline-snapshot run.
"""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

import pytest

from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

from engine.config import AgentConfig, EngineConfig
from engine.events import NullEmitter
from engine.phases import run_pipeline


# ---------------------------------------------------------------------------
# Metrics (spec 061 §3.2.1)
# ---------------------------------------------------------------------------
#
# ``GEval`` instantiation eagerly constructs its default judge model
# (OpenAI) and raises if no API key is available.  That breaks test
# *collection* in environments without ``OPENAI_API_KEY`` even though
# these tests are gated behind ``-m eval``.  Build metrics lazily so the
# module imports cleanly everywhere; the cost of instantiation is paid
# only when an eval test actually runs.

_REVIEW_INDEPENDENCE_KW = dict(
    name="Review Independence",
    criteria=(
        "Each agent's review is substantively different from others. "
        "Score 1 if the reviews disagree on at least one substantive "
        "claim. Score 0 if reviews are paraphrases of each other. "
        "Score 0.5 if reviews differ in style but agree on all claims."
    ),
    # TODO(spec-061-step8): calibrate threshold from baseline-snapshot run.
    threshold=0.7,
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
)

_CROSS_REVIEW_ADVERSARIAL_KW = dict(
    name="Cross-Review Adversarial Quality",
    criteria=(
        "Cross-reviews identify specific disagreements with the "
        "reviewed agent's claims, not generic praise. Score 1 if at "
        "least one specific challenge is made; 0 if the cross-review "
        "is generic agreement; 0.5 if challenges are vague."
    ),
    # TODO(spec-061-step8): calibrate threshold from baseline-snapshot run.
    threshold=0.7,
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
)

_REVISION_RESPONSIVENESS_KW = dict(
    name="Revision Responsiveness",
    criteria=(
        "Revisions explicitly address the cross-review challenges. "
        "Score 1 if the revision quotes or paraphrases each cross-review "
        "challenge before responding. 0 if the revision ignores the "
        "challenges. 0.5 if responsiveness is partial."
    ),
    # TODO(spec-061-step8): calibrate threshold from baseline-snapshot run.
    threshold=0.6,
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
        LLMTestCaseParams.CONTEXT,
    ],
)

_DISPUTE_SPECIFICITY_KW = dict(
    name="Dispute Specificity",
    criteria=(
        "Disputes name concrete disagreements with evidence (a specific "
        "claim, a citation, a counterexample). Score 1 if every dispute "
        "names a specific claim and evidence. 0 if disputes are generic. "
        "0.5 if some are specific and others vague."
    ),
    # TODO(spec-061-step8): calibrate threshold from baseline-snapshot run.
    threshold=0.7,
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
)

_SYNTHESIS_GROUNDING_KW = dict(
    name="Synthesis Grounding",
    criteria=(
        "The synthesis must (1) reference specific claims from "
        "individual agent reviews, (2) acknowledge where agents "
        "disagreed, (3) provide a clear verdict, and (4) not "
        "introduce claims absent from the pipeline record. Score 0 "
        "if the verdict is missing. 0.5 if the verdict exists but "
        "doesn't reference the debate. 1 if fully grounded."
    ),
    # TODO(spec-061-step8): calibrate threshold from baseline-snapshot run.
    threshold=0.8,
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
        LLMTestCaseParams.CONTEXT,
    ],
)


def _build_metric(kwargs: dict) -> GEval:
    """Instantiate a :class:`GEval` metric, skipping the test if the
    default judge can't authenticate."""
    try:
        return GEval(**kwargs)
    except Exception as exc:  # noqa: BLE001 — broad: deepeval raises various
        pytest.skip(
            f"deepeval judge unavailable for metric {kwargs.get('name')!r}: "
            f"{exc}"
        )


# ---------------------------------------------------------------------------
# Fixture: run a real deliberation once per test class
# ---------------------------------------------------------------------------

# A small, self-contained target paragraph so the deliberation has
# something concrete to talk about without dragging in the full README
# (which would inflate token cost).
_TARGET_TEXT = """\
# Conversus quickstart claim

Conversus is a multi-agent deliberation engine.  It supports four game
theory modes (cooperative, winner-take-all, prisoners-dilemma, red-blue)
and runs every deliberation through five phases: review, cross-review,
revision, disputes, and synthesis.  A single ``conversus run`` invocation
should produce a synthesised verdict in under sixty seconds for a
two-agent cooperative deliberation against a small target.
"""

_QUESTION = (
    "Evaluate whether the quickstart claim is accurate, complete, and "
    "free of misleading statements."
)


def _make_eval_config(work_dir: Path, *, agents: list[str]) -> EngineConfig:
    """Build a minimal two-agent cooperative ``EngineConfig``."""
    target = work_dir / "target.md"
    target.write_text(_TARGET_TEXT, encoding="utf-8")

    output_dir = work_dir / "output"
    output_dir.mkdir(exist_ok=True)

    agent_configs = [
        AgentConfig(
            name=name,
            prompt=(
                f"You are reviewer {name}.  Read the target and respond "
                f"to the question with concrete claims; do not hedge."
            ),
            docs=[],
        )
        for name in agents
    ]

    return EngineConfig(
        mode="cooperative",
        target_files=[target],
        output=output_dir,
        agents=agent_configs,
        iterations=1,
        rounds=1,
        stagnation="detect",
        prior_files=[],
        arbiter=None,
        validate_templates=True,
    )


@pytest.mark.eval
class TestDeliberationQuality:
    """Quality tests for deliberation outputs.

    Marked ``@eval`` so they're excluded from the default CI suite — these
    spawn real provider calls and have non-trivial cost.

    Run manually:
        uv run deepeval test run engine/tests/test_evals.py
        # or
        uv run --extra mcp --extra test pytest engine/tests/test_evals.py -m eval
    """

    @pytest.fixture(scope="class")
    def cooperative_pipeline_output(
        self, tmp_path_factory: pytest.TempPathFactory
    ) -> Path:
        """Run a cooperative deliberation once; share artifacts across tests.

        Uses the provider named in ``CONVERSUS_EVAL_PROVIDER`` (default:
        ``anthropic``).  Skips if the provider is unauthenticated.
        """
        from engine.run import resolve_execution_provider

        provider_name = os.environ.get("CONVERSUS_EVAL_PROVIDER", "anthropic")
        if provider_name == "anthropic" and not os.environ.get("ANTHROPIC_API_KEY"):
            pytest.skip(
                "ANTHROPIC_API_KEY not set; set it or override "
                "CONVERSUS_EVAL_PROVIDER."
            )

        work_dir = tmp_path_factory.mktemp("eval_pipeline")
        config = _make_eval_config(work_dir, agents=["alice", "bob"])

        try:
            provider = resolve_execution_provider(provider_name)
        except Exception as exc:  # auth failure or missing creds
            pytest.skip(f"Provider {provider_name!r} unavailable: {exc}")

        config_path = work_dir / "conversus.yml"
        config_path.write_text("# placeholder for template discovery\n", encoding="utf-8")

        result = asyncio.run(
            run_pipeline(
                config,
                provider,
                NullEmitter(),
                config_path=config_path,
            )
        )
        return result.output_dir

    # ------------------------------------------------------------------
    # Helpers (instance methods so subclasses could override; static-ish)
    # ------------------------------------------------------------------

    @staticmethod
    def _read_review_files(output_dir: Path) -> dict[str, str]:
        """Return ``{agent_name: review_text}`` for every Phase 1 review."""
        return {
            p.parent.name: p.read_text(encoding="utf-8")
            for p in sorted(output_dir.glob("*/review.md"))
        }

    @staticmethod
    def _read_cross_reviews(output_dir: Path) -> dict[tuple[str, str], str]:
        """Return ``{(reviewer, reviewed): cross_review_text}``."""
        out: dict[tuple[str, str], str] = {}
        for p in sorted(output_dir.glob("*/cross-reviews/*.md")):
            reviewer = p.parent.parent.name
            reviewed = p.stem
            out[(reviewer, reviewed)] = p.read_text(encoding="utf-8")
        return out

    @staticmethod
    def _read_revisions(output_dir: Path) -> dict[str, str]:
        """Return ``{agent_name: revision_text}`` for the final revision."""
        return {
            p.parent.name: p.read_text(encoding="utf-8")
            for p in sorted(output_dir.glob("*/revision.md"))
        }

    @staticmethod
    def _read_disputes(output_dir: Path) -> dict[str, str]:
        """Return ``{agent_name: disputes_text}``."""
        return {
            p.parent.name: p.read_text(encoding="utf-8")
            for p in sorted(output_dir.glob("*/disputes.md"))
        }

    @staticmethod
    def _read_synthesis(output_dir: Path) -> str:
        """Return the synthesis text from ``summary/final.md``."""
        synth = output_dir / "summary" / "final.md"
        return synth.read_text(encoding="utf-8") if synth.exists() else ""

    # ------------------------------------------------------------------
    # Tests
    # ------------------------------------------------------------------

    def test_review_independence(self, cooperative_pipeline_output: Path) -> None:
        """Each review is substantively different from the others."""
        metric = _build_metric(_REVIEW_INDEPENDENCE_KW)
        reviews = self._read_review_files(cooperative_pipeline_output)
        assert len(reviews) >= 2, "need at least 2 reviews to compare independence"

        agents = sorted(reviews.keys())
        # Compare each ordered pair (reviewer A vs the others) so we
        # exercise pairwise independence rather than treating the set
        # as a single blob.
        for agent in agents:
            others = "\n\n---\n\n".join(
                f"### {name}\n{reviews[name]}" for name in agents if name != agent
            )
            test_case = LLMTestCase(
                input=(
                    f"Question: {_QUESTION}\n"
                    f"Compare review by '{agent}' against the other agents' reviews. "
                    f"Other reviews:\n{others}"
                ),
                actual_output=reviews[agent],
            )
            metric.measure(test_case)
            assert metric.score is not None
            assert metric.score >= metric.threshold, (
                f"{agent}: review independence {metric.score:.2f} "
                f"< {metric.threshold} — {metric.reason}"
            )

    def test_cross_review_adversarial_quality(
        self, cooperative_pipeline_output: Path
    ) -> None:
        """Cross-reviews identify specific disagreements, not generic praise."""
        metric = _build_metric(_CROSS_REVIEW_ADVERSARIAL_KW)
        reviews = self._read_review_files(cooperative_pipeline_output)
        cross_reviews = self._read_cross_reviews(cooperative_pipeline_output)
        assert cross_reviews, "expected at least one cross-review"

        for (reviewer, reviewed), cross_text in cross_reviews.items():
            target_review = reviews.get(reviewed, "")
            test_case = LLMTestCase(
                input=(
                    f"Question: {_QUESTION}\n"
                    f"Original review by '{reviewed}' that '{reviewer}' is challenging:\n"
                    f"{target_review}"
                ),
                actual_output=cross_text,
            )
            metric.measure(test_case)
            assert metric.score is not None
            assert metric.score >= metric.threshold, (
                f"{reviewer}->{reviewed}: cross-review adversarial quality "
                f"{metric.score:.2f} < {metric.threshold} — {metric.reason}"
            )

    def test_revision_responsiveness(
        self, cooperative_pipeline_output: Path
    ) -> None:
        """Revisions explicitly address the cross-review challenges."""
        metric = _build_metric(_REVISION_RESPONSIVENESS_KW)
        revisions = self._read_revisions(cooperative_pipeline_output)
        cross_reviews = self._read_cross_reviews(cooperative_pipeline_output)
        assert revisions, "expected at least one revision"

        for agent, revision_text in revisions.items():
            # Challenges are cross-reviews where this agent was the
            # reviewed party (others reviewing them).
            challenges = [
                text
                for (reviewer, reviewed), text in cross_reviews.items()
                if reviewed == agent
            ]
            if not challenges:
                continue  # nothing to be responsive to
            test_case = LLMTestCase(
                input=(
                    f"Question: {_QUESTION}\n"
                    f"Cross-review challenges issued to '{agent}':\n"
                    + "\n\n---\n\n".join(challenges)
                ),
                actual_output=revision_text,
                context=challenges,
            )
            metric.measure(test_case)
            assert metric.score is not None
            assert metric.score >= metric.threshold, (
                f"{agent}: revision responsiveness "
                f"{metric.score:.2f} < {metric.threshold} — {metric.reason}"
            )

    def test_dispute_specificity(
        self, cooperative_pipeline_output: Path
    ) -> None:
        """Disputes name concrete disagreements with evidence."""
        metric = _build_metric(_DISPUTE_SPECIFICITY_KW)
        disputes = self._read_disputes(cooperative_pipeline_output)
        assert disputes, "expected at least one disputes file"

        for agent, dispute_text in disputes.items():
            test_case = LLMTestCase(
                input=(
                    f"Question: {_QUESTION}\n"
                    f"Disputes raised by '{agent}' after revision."
                ),
                actual_output=dispute_text,
            )
            metric.measure(test_case)
            assert metric.score is not None
            assert metric.score >= metric.threshold, (
                f"{agent}: dispute specificity "
                f"{metric.score:.2f} < {metric.threshold} — {metric.reason}"
            )

    def test_synthesis_grounding(
        self, cooperative_pipeline_output: Path
    ) -> None:
        """Synthesis references specific claims from the pipeline record."""
        metric = _build_metric(_SYNTHESIS_GROUNDING_KW)
        synthesis = self._read_synthesis(cooperative_pipeline_output)
        assert synthesis, "expected synthesis file at summary/final.md"

        reviews = self._read_review_files(cooperative_pipeline_output)
        revisions = self._read_revisions(cooperative_pipeline_output)
        disputes = self._read_disputes(cooperative_pipeline_output)

        # Provide every upstream artifact as context so the judge can
        # check that the synthesis doesn't introduce unsupported claims.
        context = (
            [f"Review by {a}:\n{t}" for a, t in reviews.items()]
            + [f"Revision by {a}:\n{t}" for a, t in revisions.items()]
            + [f"Disputes by {a}:\n{t}" for a, t in disputes.items()]
        )

        test_case = LLMTestCase(
            input=f"Question: {_QUESTION}\nPipeline produced reviews, revisions, and disputes.",
            actual_output=synthesis,
            context=context,
        )
        metric.measure(test_case)
        assert metric.score is not None
        assert metric.score >= metric.threshold, (
            f"synthesis grounding {metric.score:.2f} "
            f"< {metric.threshold} — {metric.reason}"
        )
