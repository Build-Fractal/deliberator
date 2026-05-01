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

Authentication:

    The deliberation defaults to ``claude-code`` (host-session OAuth via
    ``claude -p`` subprocess). The judge defaults to deepeval's
    ``AnthropicModel`` (requires ``ANTHROPIC_API_KEY``) but can be
    switched to ``ClaudeCodeJudge`` (also OAuth, no API key) by setting
    ``CONVERSUS_EVAL_JUDGE_PROVIDER=claude-code``. With both flipped to
    ``claude-code``, the entire eval suite runs under host OAuth with
    no API key.

    Auth matrix:

    +---------------------------+-----------------------------+----------------------+--------------------------------+
    | CONVERSUS_EVAL_PROVIDER   | CONVERSUS_EVAL_JUDGE_PROVID | ANTHROPIC_API_KEY    | Behavior                       |
    +===========================+=============================+======================+================================+
    | claude-code (default)     | anthropic (default)         | unset                | judge skips -> quality skip    |
    +---------------------------+-----------------------------+----------------------+--------------------------------+
    | claude-code               | anthropic                   | set                  | full eval execute              |
    +---------------------------+-----------------------------+----------------------+--------------------------------+
    | claude-code               | claude-code                 | unset                | full eval via OAuth (no key)   |
    +---------------------------+-----------------------------+----------------------+--------------------------------+
    | anthropic                 | anthropic                   | set                  | full eval execute              |
    +---------------------------+-----------------------------+----------------------+--------------------------------+
    | anthropic                 | claude-code                 | set                  | mixed: OAuth judge, API delib  |
    +---------------------------+-----------------------------+----------------------+--------------------------------+

Provider override:

    Set ``CONVERSUS_EVAL_PROVIDER`` to override the deliberation
    provider. Default: ``claude-code``. Other values flow through
    ``engine.run.resolve_execution_provider`` (e.g. ``anthropic``,
    ``mock`` for smoke runs that won't produce judge-able output).

Judge provider override:

    Set ``CONVERSUS_EVAL_JUDGE_PROVIDER`` to override the judge
    transport. Default: ``anthropic`` (deepeval's ``AnthropicModel``;
    requires ``ANTHROPIC_API_KEY``). Set to ``claude-code`` to use
    :class:`engine.eval_judge.ClaudeCodeJudge` instead (OAuth via
    ``claude -p``; no API key required).

Judge model override:

    Set ``CONVERSUS_EVAL_JUDGE_MODEL`` to override the model used as
    the GEval judge. Default: ``claude-sonnet-4-20250514`` (the
    Anthropic-API literal). When the judge provider is
    ``claude-code``, the default Anthropic literal is normalized back
    to the ``"sonnet"`` alias because OAuth sessions cannot reach
    arbitrary dated model IDs.

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
from deepeval.models.llms.anthropic_model import AnthropicModel
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

from engine.config import AgentConfig, EngineConfig
from engine.events import NullEmitter
from engine.phases import run_pipeline


# ---------------------------------------------------------------------------
# Judge factory (Anthropic-backed; matches SC-004 same-family discipline)
# ---------------------------------------------------------------------------

_DEFAULT_JUDGE_PROVIDER = "anthropic"  # override via CONVERSUS_EVAL_JUDGE_PROVIDER
_DEFAULT_JUDGE_MODEL = "claude-sonnet-4-20250514"  # override via CONVERSUS_EVAL_JUDGE_MODEL


def _build_judge():
    """Build a deepeval judge based on ``CONVERSUS_EVAL_JUDGE_PROVIDER``.

    - ``"anthropic"`` (default): uses deepeval's ``AnthropicModel``;
      requires ``ANTHROPIC_API_KEY``. Preserves PR #85's same-family
      discipline (Claude judges Claude).
    - ``"claude-code"``: uses :class:`engine.eval_judge.ClaudeCodeJudge`,
      which shells out to the host ``claude`` CLI via OAuth — no
      Anthropic API key required. Closes the OAuth-user gap from
      issue #87.

    Override the judge model via ``CONVERSUS_EVAL_JUDGE_MODEL``. When
    the provider is ``claude-code`` and the model env var is at its
    default Anthropic literal (``claude-sonnet-4-20250514``), it is
    normalized to the ``"sonnet"`` alias because OAuth sessions cannot
    reach arbitrary dated model IDs (see ``ClaudeCodeProvider``'s
    engine-default leak guard).
    """
    judge_provider = os.environ.get(
        "CONVERSUS_EVAL_JUDGE_PROVIDER", _DEFAULT_JUDGE_PROVIDER
    )
    model_name = os.environ.get("CONVERSUS_EVAL_JUDGE_MODEL", _DEFAULT_JUDGE_MODEL)

    if judge_provider == "claude-code":
        from engine.eval_judge import ClaudeCodeJudge

        # If the user did not override the judge model, the env var is
        # still pointing at the Anthropic-API literal that the OAuth
        # subprocess can't address — normalize it back to the alias.
        cc_model = "sonnet" if model_name == _DEFAULT_JUDGE_MODEL else model_name
        return ClaudeCodeJudge(model=cc_model)

    if judge_provider == "anthropic":
        if not os.environ.get("ANTHROPIC_API_KEY"):
            pytest.skip(
                "ANTHROPIC_API_KEY not set; required for Anthropic-backed deepeval judge. "
                "Set CONVERSUS_EVAL_JUDGE_PROVIDER=claude-code to use OAuth instead."
            )
        return AnthropicModel(model=model_name)

    pytest.skip(
        f"Unknown CONVERSUS_EVAL_JUDGE_PROVIDER: {judge_provider!r}. "
        "Expected 'anthropic' or 'claude-code'."
    )


# ---------------------------------------------------------------------------
# Metrics (spec 061 §3.2.1)
# ---------------------------------------------------------------------------
#
# Metrics are built lazily via ``_build_metric`` so module import stays
# cheap (no eager judge construction at collection time).  The judge is
# attached explicitly via ``model=_build_judge()`` so we never fall
# through to deepeval's OpenAI default.

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
    """Construct a :class:`GEval` metric with the Anthropic judge attached.

    Skips the test if ``ANTHROPIC_API_KEY`` is unset (via
    ``_build_judge``).  This bypasses deepeval's default OpenAI judge
    entirely so the test suite never depends on a non-Anthropic
    provider key.
    """
    judge = _build_judge()
    return GEval(model=judge, **kwargs)


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
        ``claude-code`` — host-session OAuth via ``claude -p``
        subprocess, so OAuth-only users can run the deliberation
        without an Anthropic API key). The judge still requires
        ``ANTHROPIC_API_KEY`` (handled by ``_build_judge``); when the
        key is absent, individual quality tests skip via
        ``_build_metric``, but the fixture itself runs to capture the
        deliberation artifacts.

        Skip behavior:
        - For ``anthropic`` provider override: skip the whole fixture
          if ``ANTHROPIC_API_KEY`` is unset (the deliberation itself
          can't run without it).
        - For ``claude-code`` (default) or other providers: fixture
          always attempts to run; provider resolution surfaces its
          own auth errors via the try/except below.
        """
        from engine.run import resolve_execution_provider

        provider_name = os.environ.get("CONVERSUS_EVAL_PROVIDER", "claude-code")
        if provider_name == "anthropic" and not os.environ.get("ANTHROPIC_API_KEY"):
            pytest.skip(
                "ANTHROPIC_API_KEY not set; set it or use "
                "CONVERSUS_EVAL_PROVIDER=claude-code (default — OAuth via "
                "claude -p subprocess)."
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


# ---------------------------------------------------------------------------
# Judge-configuration tests (no @eval marker — run in default CI)
# ---------------------------------------------------------------------------


class TestJudgeConfiguration:
    """Verify the deepeval judge is Anthropic-backed (not OpenAI default).

    These tests run in default CI (no ``eval`` marker) so a regression
    that flipped the judge back to OpenAI — or broke the env-var
    plumbing — would surface immediately, even when the expensive
    ``@eval`` suite is skipped.
    """

    def test_judge_factory_returns_anthropic_model(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """``_build_judge()`` returns an :class:`AnthropicModel` instance."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-real")
        monkeypatch.delenv("CONVERSUS_EVAL_JUDGE_MODEL", raising=False)
        monkeypatch.delenv("CONVERSUS_EVAL_JUDGE_PROVIDER", raising=False)
        judge = _build_judge()
        assert isinstance(judge, AnthropicModel)
        # Default model is claude-sonnet-4-20250514 (or env override).
        assert judge.get_model_name().startswith("claude")

    def test_judge_factory_skips_without_api_key(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """``_build_judge()`` skips when ``ANTHROPIC_API_KEY`` is unset."""
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        monkeypatch.delenv("CONVERSUS_EVAL_JUDGE_PROVIDER", raising=False)
        with pytest.raises(pytest.skip.Exception):
            _build_judge()

    def test_judge_factory_respects_model_override(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """``CONVERSUS_EVAL_JUDGE_MODEL`` overrides the judge model."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-real")
        monkeypatch.delenv("CONVERSUS_EVAL_JUDGE_PROVIDER", raising=False)
        monkeypatch.setenv(
            "CONVERSUS_EVAL_JUDGE_MODEL", "claude-3-5-haiku-20241022"
        )
        judge = _build_judge()
        # ``AnthropicModel.get_model_name()`` returns "<model> (Anthropic)";
        # the underlying ``name`` attribute holds the bare model id.
        assert judge.name == "claude-3-5-haiku-20241022"

    def test_judge_factory_claude_code_provider(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """``CONVERSUS_EVAL_JUDGE_PROVIDER=claude-code`` returns ``ClaudeCodeJudge``.

        Closes the OAuth-user gap from issue #87: the judge is built
        without consulting ``ANTHROPIC_API_KEY`` and the suffix on
        ``get_model_name()`` lets test telemetry distinguish OAuth runs
        from API-key runs.
        """
        from engine.eval_judge import ClaudeCodeJudge

        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        monkeypatch.setenv("CONVERSUS_EVAL_JUDGE_PROVIDER", "claude-code")
        monkeypatch.delenv("CONVERSUS_EVAL_JUDGE_MODEL", raising=False)
        judge = _build_judge()
        assert isinstance(judge, ClaudeCodeJudge)
        assert judge.get_model_name().endswith("(claude-code)")

    def test_judge_factory_invalid_provider_skips(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """An unknown ``CONVERSUS_EVAL_JUDGE_PROVIDER`` skips cleanly."""
        monkeypatch.setenv("CONVERSUS_EVAL_JUDGE_PROVIDER", "bogus")
        with pytest.raises(pytest.skip.Exception):
            _build_judge()

    def test_claude_code_judge_get_model_name_includes_suffix(self) -> None:
        """Direct test of :meth:`ClaudeCodeJudge.get_model_name` format.

        The ``(claude-code)`` suffix is the marker downstream telemetry
        uses to tell OAuth-judge runs apart from API-judge runs; lock
        the format so future refactors don't silently drop it.
        """
        from engine.eval_judge import ClaudeCodeJudge

        judge = ClaudeCodeJudge(model="opus")
        assert judge.get_model_name() == "opus (claude-code)"
