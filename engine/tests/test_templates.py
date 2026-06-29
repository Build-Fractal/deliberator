"""Tests for engine.templates — loading, filling, and context building."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from engine.config import AgentConfig, ArbiterConfig, EngineConfig
from engine.templates import (
    DRAFT_MARKER,
    UNFILLED_VAR_RE,
    TemplateError,
    _extract_remaining_disputes,
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
)
from linter.models import (
    ArbitrationContext,
    CrossReviewContext,
    CrossRoundSynthesisContext,
    DisputesContext,
    InfluenceLevel,
    ReviewContext,
    RevisionContext,
    SynthesisContext,
)


# ---------------------------------------------------------------------------
# Template directory discovery
# ---------------------------------------------------------------------------

class TestFindTemplatesDir:
    """find_templates_dir locates the templates/ directory."""

    def test_finds_from_example_config(self, example_config_path: Path) -> None:
        templates_dir = find_templates_dir(example_config_path)
        assert templates_dir.is_dir()
        assert (templates_dir / "cooperative").is_dir()


# ---------------------------------------------------------------------------
# Loading templates
# ---------------------------------------------------------------------------

class TestLoadTemplate:
    """load_template loads review templates for all 4 modes."""

    MODES = ["cooperative", "winner-take-all", "prisoners-dilemma", "red-blue"]

    @pytest.mark.parametrize("mode", MODES)
    def test_review_template_loads(self, mode: str, example_config_path: Path) -> None:
        templates_dir = find_templates_dir(example_config_path)
        content = load_template(templates_dir, mode, "review")
        assert len(content) > 100
        # All review templates should have at least one {VARIABLE} placeholder
        assert UNFILLED_VAR_RE.search(content)

    def test_missing_template_raises(self, example_config_path: Path) -> None:
        templates_dir = find_templates_dir(example_config_path)
        with pytest.raises(TemplateError, match="not found"):
            load_template(templates_dir, "cooperative", "nonexistent-phase")

    def test_draft_template_rejected(self, tmp_path: Path) -> None:
        """A template with the draft marker is rejected."""
        mode_dir = tmp_path / "templates" / "cooperative"
        mode_dir.mkdir(parents=True)
        draft = mode_dir / "review.md"
        draft.write_text(f"{DRAFT_MARKER}\n# Review\n{{OUTPUT_PATH}}")
        with pytest.raises(TemplateError, match="draft"):
            load_template(tmp_path / "templates", "cooperative", "review")


# ---------------------------------------------------------------------------
# Filling templates
# ---------------------------------------------------------------------------

class TestFillTemplate:
    """fill_template substitutes all {VARIABLE} placeholders."""

    @pytest.fixture
    def review_context(self, tmp_path: Path) -> ReviewContext:
        """A ReviewContext with known values for substitution testing."""
        return ReviewContext(
            OUTPUT_PATH=tmp_path / "out" / "agent-a" / "review.md",
            TARGET_FILES=[tmp_path / "spec.md", tmp_path / "plan.md"],
            AGENT_NAME="agent-a",
            AGENT_PROMPT="You are agent A.",
            AGENT_DOCS=[tmp_path / "docs" / "readme.md"],
            MODE="cooperative",
            PRIOR_FILES_SECTION="",
            PRIOR_ROUND_SECTION="",
            ROUND=1,
            MAX_ROUNDS=1,
            PRIOR_SYNTHESIS_PATH=None,
            PRIOR_ROUND_DIR=None,
            PRIOR_ARBITRATION_PATH=None,
            AGENT_ROLE=None,
        )

    def test_no_unfilled_vars_remain(
        self,
        review_context: ReviewContext,
        example_config_path: Path,
    ) -> None:
        """After filling, no {VARIABLE} placeholders should remain."""
        templates_dir = find_templates_dir(example_config_path)
        template = load_template(templates_dir, "cooperative", "review")
        filled = fill_template(template, review_context)
        remaining = UNFILLED_VAR_RE.findall(filled)
        assert remaining == [], f"Unfilled variables remain: {remaining}"

    def test_agent_name_substituted(
        self,
        review_context: ReviewContext,
        example_config_path: Path,
    ) -> None:
        templates_dir = find_templates_dir(example_config_path)
        template = load_template(templates_dir, "cooperative", "review")
        filled = fill_template(template, review_context)
        assert "agent-a" in filled

    def test_pathlist_serialization(self, review_context: ReviewContext) -> None:
        """TARGET_FILES and AGENT_DOCS expand to one bare path per line."""
        template = "Files:\n{TARGET_FILES}\nDocs:\n{AGENT_DOCS}"
        filled = fill_template(template, review_context)
        # Each path on its own line, no bullets
        lines = filled.strip().split("\n")
        path_lines = [l for l in lines if "/" in l and not l.startswith(("Files:", "Docs:"))]
        assert len(path_lines) == 3  # 2 target + 1 doc

    def test_none_fields_become_empty_string(self, review_context: ReviewContext) -> None:
        """Optional None fields like AGENT_ROLE substitute to empty string."""
        template = "Role: '{AGENT_ROLE}'"
        filled = fill_template(template, review_context)
        assert filled == "Role: ''"

    def test_unfilled_variable_raises(self, review_context: ReviewContext) -> None:
        """A template with a variable not in the context raises TemplateError."""
        template = "{AGENT_NAME} and {UNKNOWN_VARIABLE}"
        with pytest.raises(TemplateError, match="Unfilled"):
            fill_template(template, review_context)


# ---------------------------------------------------------------------------
# build_review_context
# ---------------------------------------------------------------------------

class TestBuildReviewContext:
    """build_review_context sets all fields from config + agent."""

    def test_fields_set_correctly(self, tmp_path: Path) -> None:
        config = EngineConfig(
            mode="cooperative",
            target_files=[Path("/spec.md")],
            output=tmp_path / "out",
            agents=[
                AgentConfig(name="agent-a", prompt="You are A.", docs=[Path("/docs")]),
                AgentConfig(name="agent-b", prompt="You are B."),
            ],
            rounds=2,
        )
        agent = config.agents[0]
        ctx = build_review_context(config, agent, config.output)

        assert ctx.AGENT_NAME == "agent-a"
        assert ctx.AGENT_PROMPT == "You are A."
        assert ctx.MODE == "cooperative"
        assert ctx.ROUND == 1
        assert ctx.MAX_ROUNDS == 2
        assert ctx.AGENT_DOCS == [Path("/docs")]
        assert ctx.OUTPUT_PATH == config.output / "agent-a" / "review.md"

    def test_agent_role_none_for_non_red_blue(self, tmp_path: Path) -> None:
        config = EngineConfig(
            mode="cooperative",
            target_files=[Path("/spec.md")],
            output=tmp_path / "out",
            agents=[
                AgentConfig(name="a", prompt="A"),
                AgentConfig(name="b", prompt="B"),
            ],
        )
        ctx = build_review_context(config, config.agents[0], config.output)
        assert ctx.AGENT_ROLE is None

    def test_agent_role_set_for_red_blue(self, tmp_path: Path) -> None:
        config = EngineConfig(
            mode="red-blue",
            target_files=[Path("/spec.md")],
            output=tmp_path / "out",
            agents=[
                AgentConfig(name="attacker", prompt="R", role="red"),
                AgentConfig(name="defender", prompt="B", role="blue"),
            ],
        )
        ctx = build_review_context(config, config.agents[0], config.output)
        assert ctx.AGENT_ROLE == "red"


# ---------------------------------------------------------------------------
# Fill all 4 modes end-to-end (no unfilled vars)
# ---------------------------------------------------------------------------

class TestFillAllModes:
    """Filling review templates for all 4 modes leaves no unfilled vars."""

    MODES = ["cooperative", "winner-take-all", "prisoners-dilemma", "red-blue"]

    @pytest.mark.parametrize("mode", MODES)
    def test_fill_leaves_no_vars(
        self, mode: str, tmp_path: Path, example_config_path: Path
    ) -> None:
        templates_dir = find_templates_dir(example_config_path)
        template = load_template(templates_dir, mode, "review")

        config = EngineConfig(
            mode=mode,
            target_files=[Path("/spec.md")],
            output=tmp_path / "out",
            agents=[
                AgentConfig(name="agent-a", prompt="You are A.", role="red" if mode == "red-blue" else None),
                AgentConfig(name="agent-b", prompt="You are B.", role="blue" if mode == "red-blue" else None),
            ],
        )
        ctx = build_review_context(config, config.agents[0], config.output)
        filled = fill_template(template, ctx)
        remaining = UNFILLED_VAR_RE.findall(filled)
        assert remaining == [], f"Unfilled in {mode}: {remaining}"


# ---------------------------------------------------------------------------
# Shared helpers for Phase 2-5 tests
# ---------------------------------------------------------------------------

def _make_cooperative_config(tmp_path: Path) -> EngineConfig:
    """2-agent cooperative config for context builder tests."""
    return EngineConfig(
        mode="cooperative",
        target_files=[Path("/spec.md")],
        output=tmp_path / "out",
        agents=[
            AgentConfig(name="alpha", prompt="You are Alpha.", docs=[Path("/docs/alpha")]),
            AgentConfig(name="beta", prompt="You are Beta.", docs=[Path("/docs/beta")]),
        ],
        rounds=1,
    )


def _make_red_blue_config(tmp_path: Path) -> EngineConfig:
    """2-agent red-blue config for context builder tests."""
    return EngineConfig(
        mode="red-blue",
        target_files=[Path("/spec.md")],
        output=tmp_path / "out",
        agents=[
            AgentConfig(name="attacker", prompt="Red team.", role="red", docs=[Path("/docs/r")]),
            AgentConfig(name="defender", prompt="Blue team.", role="blue", docs=[Path("/docs/b")]),
        ],
        rounds=1,
    )


# ---------------------------------------------------------------------------
# build_cross_review_context (Phase 2)
# ---------------------------------------------------------------------------

class TestBuildCrossReviewContext:
    """build_cross_review_context sets all fields from config + agents."""

    def test_fields_set_correctly(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_cross_review_context(config, "alpha", "beta", config.output)

        assert isinstance(ctx, CrossReviewContext)
        assert ctx.REVIEWER_NAME == "alpha"
        assert ctx.REVIEWED_NAME == "beta"
        assert ctx.REVIEWER_PROMPT == "You are Alpha."
        assert ctx.AGENT_DOCS == [Path("/docs/alpha")]
        assert ctx.MODE == "cooperative"
        assert ctx.ROUND == 1
        assert ctx.PRIOR_SYNTHESIS_PATH is None
        assert ctx.PRIOR_ROUND_DIR is None
        assert ctx.PRIOR_ARBITRATION_PATH is None

    def test_output_path_in_reviewer_dir(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_cross_review_context(config, "alpha", "beta", config.output)
        expected = config.output / "alpha" / "cross-reviews" / "beta.md"
        assert ctx.OUTPUT_PATH == expected

    def test_iteration_1_reads_reviews(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_cross_review_context(config, "alpha", "beta", config.output, iteration=1)
        assert ctx.REVIEWED_REVIEW_PATH == config.output / "beta" / "review.md"
        assert ctx.REVIEWER_REVIEW_PATH == config.output / "alpha" / "review.md"

    def test_iteration_2_reads_revision_md(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_cross_review_context(config, "alpha", "beta", config.output, iteration=2)
        assert ctx.REVIEWED_REVIEW_PATH == config.output / "beta" / "revision.md"
        assert ctx.REVIEWER_REVIEW_PATH == config.output / "alpha" / "revision.md"

    def test_model_is_frozen(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_cross_review_context(config, "alpha", "beta", config.output)
        with pytest.raises(Exception):
            ctx.REVIEWER_NAME = "changed"  # type: ignore[misc]

    def test_roles_none_for_cooperative(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_cross_review_context(config, "alpha", "beta", config.output)
        assert ctx.REVIEWER_ROLE is None
        assert ctx.REVIEWED_ROLE is None

    def test_roles_set_for_red_blue(self, tmp_path: Path) -> None:
        config = _make_red_blue_config(tmp_path)
        ctx = build_cross_review_context(config, "attacker", "defender", config.output)
        assert ctx.REVIEWER_ROLE == "red"
        assert ctx.REVIEWED_ROLE == "blue"

    def test_fill_template_cooperative(self, tmp_path: Path, example_config_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_cross_review_context(config, "alpha", "beta", config.output)
        templates_dir = find_templates_dir(example_config_path)
        template = load_template(templates_dir, "cooperative", "cross-review")
        filled = fill_template(template, ctx)
        remaining = UNFILLED_VAR_RE.findall(filled)
        assert remaining == [], f"Unfilled variables: {remaining}"

    def test_fill_template_red_blue(self, tmp_path: Path, example_config_path: Path) -> None:
        config = _make_red_blue_config(tmp_path)
        ctx = build_cross_review_context(config, "attacker", "defender", config.output)
        templates_dir = find_templates_dir(example_config_path)
        template = load_template(templates_dir, "red-blue", "cross-review")
        filled = fill_template(template, ctx)
        remaining = UNFILLED_VAR_RE.findall(filled)
        assert remaining == [], f"Unfilled variables: {remaining}"


# ---------------------------------------------------------------------------
# build_revision_context (Phase 3)
# ---------------------------------------------------------------------------

class TestBuildRevisionContext:
    """build_revision_context sets all fields from config + agent."""

    def test_fields_set_correctly(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_revision_context(config, "alpha", config.output, iteration=1, other_agents=["beta"])

        assert isinstance(ctx, RevisionContext)
        assert ctx.AGENT_NAME == "alpha"
        assert ctx.AGENT_PROMPT == "You are Alpha."
        assert ctx.ITERATION == 1
        assert ctx.MODE == "cooperative"
        assert ctx.ROUND == 1

    def test_output_path_iteration_1(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_revision_context(config, "alpha", config.output, iteration=1, other_agents=["beta"])
        assert ctx.OUTPUT_PATH == config.output / "alpha" / "revision.md"

    def test_output_path_iteration_2(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_revision_context(config, "alpha", config.output, iteration=2, other_agents=["beta"])
        assert ctx.OUTPUT_PATH == config.output / "alpha" / "revision_2.md"

    def test_my_review_path(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_revision_context(config, "alpha", config.output, iteration=1, other_agents=["beta"])
        assert ctx.MY_REVIEW_PATH == config.output / "alpha" / "review.md"

    def test_cross_reviews_of_me(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_revision_context(config, "alpha", config.output, iteration=1, other_agents=["beta"])
        expected = [config.output / "beta" / "cross-reviews" / "alpha.md"]
        assert ctx.CROSS_REVIEWS_OF_ME == expected

    def test_my_cross_reviews(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_revision_context(config, "alpha", config.output, iteration=1, other_agents=["beta"])
        expected = [config.output / "alpha" / "cross-reviews" / "beta.md"]
        assert ctx.MY_CROSS_REVIEWS == expected

    def test_model_is_frozen(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_revision_context(config, "alpha", config.output, iteration=1, other_agents=["beta"])
        with pytest.raises(Exception):
            ctx.AGENT_NAME = "changed"  # type: ignore[misc]

    def test_fill_template_cooperative(self, tmp_path: Path, example_config_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_revision_context(config, "alpha", config.output, iteration=1, other_agents=["beta"])
        templates_dir = find_templates_dir(example_config_path)
        template = load_template(templates_dir, "cooperative", "revision")
        filled = fill_template(template, ctx)
        remaining = UNFILLED_VAR_RE.findall(filled)
        assert remaining == [], f"Unfilled variables: {remaining}"


# ---------------------------------------------------------------------------
# build_disputes_context (Phase 4)
# ---------------------------------------------------------------------------

class TestBuildDisputesContext:
    """build_disputes_context sets all fields from config + agent."""

    def test_fields_set_correctly(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_disputes_context(config, "alpha", config.output, iterations=1, all_agents=["alpha", "beta"])

        assert isinstance(ctx, DisputesContext)
        assert ctx.AGENT_NAME == "alpha"
        assert ctx.AGENT_PROMPT == "You are Alpha."
        assert ctx.MODE == "cooperative"
        assert ctx.ROUND == 1

    def test_output_path(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_disputes_context(config, "alpha", config.output, iterations=1, all_agents=["alpha", "beta"])
        assert ctx.OUTPUT_PATH == config.output / "alpha" / "disputes.md"

    def test_my_revision_path_single_iteration(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_disputes_context(config, "alpha", config.output, iterations=1, all_agents=["alpha", "beta"])
        assert ctx.MY_REVISION_PATH == config.output / "alpha" / "revision.md"

    def test_my_revision_path_two_iterations(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_disputes_context(config, "alpha", config.output, iterations=2, all_agents=["alpha", "beta"])
        assert ctx.MY_REVISION_PATH == config.output / "alpha" / "revision_2.md"

    def test_all_revision_paths(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_disputes_context(config, "alpha", config.output, iterations=1, all_agents=["alpha", "beta"])
        assert len(ctx.ALL_REVISION_PATHS) == 2
        assert ctx.ALL_REVISION_PATHS[0] == config.output / "alpha" / "revision.md"
        assert ctx.ALL_REVISION_PATHS[1] == config.output / "beta" / "revision.md"

    def test_model_is_frozen(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_disputes_context(config, "alpha", config.output, iterations=1, all_agents=["alpha", "beta"])
        with pytest.raises(Exception):
            ctx.AGENT_NAME = "changed"  # type: ignore[misc]

    def test_fill_template_cooperative(self, tmp_path: Path, example_config_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_disputes_context(config, "alpha", config.output, iterations=1, all_agents=["alpha", "beta"])
        templates_dir = find_templates_dir(example_config_path)
        template = load_template(templates_dir, "cooperative", "disputes")
        filled = fill_template(template, ctx)
        remaining = UNFILLED_VAR_RE.findall(filled)
        assert remaining == [], f"Unfilled variables: {remaining}"


# ---------------------------------------------------------------------------
# build_synthesis_context (Phase 5)
# ---------------------------------------------------------------------------

class TestBuildSynthesisContext:
    """build_synthesis_context sets all fields for the neutral synthesizer."""

    def test_fields_set_correctly(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_synthesis_context(config, config.output, iterations=1)

        assert isinstance(ctx, SynthesisContext)
        assert ctx.AGENT_NAMES == "alpha, beta"
        assert ctx.MODE == "cooperative"
        assert ctx.ROUND == 1
        assert ctx.TARGET_PATH == Path("/spec.md")

    def test_output_path(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_synthesis_context(config, config.output, iterations=1)
        assert ctx.OUTPUT_PATH == config.output / "summary" / "final.md"

    def test_all_reviews(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_synthesis_context(config, config.output, iterations=1)
        assert len(ctx.ALL_REVIEWS) == 2

    def test_all_cross_reviews(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_synthesis_context(config, config.output, iterations=1)
        # 2 agents → 2 cross-review pairs
        assert len(ctx.ALL_CROSS_REVIEWS) == 2

    def test_all_revisions(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_synthesis_context(config, config.output, iterations=1)
        assert len(ctx.ALL_REVISIONS) == 2
        assert all(p.name == "revision.md" for p in ctx.ALL_REVISIONS)

    def test_all_revisions_with_two_iterations(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_synthesis_context(config, config.output, iterations=2)
        assert all(p.name == "revision_2.md" for p in ctx.ALL_REVISIONS)

    def test_all_disputes(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_synthesis_context(config, config.output, iterations=1)
        assert len(ctx.ALL_DISPUTES) == 2

    def test_model_is_frozen(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_synthesis_context(config, config.output, iterations=1)
        with pytest.raises(Exception):
            ctx.AGENT_NAMES = "changed"  # type: ignore[misc]

    def test_fill_template_cooperative(self, tmp_path: Path, example_config_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_synthesis_context(config, config.output, iterations=1)
        templates_dir = find_templates_dir(example_config_path)
        template = load_template(templates_dir, "cooperative", "synthesis")
        filled = fill_template(template, ctx)
        remaining = UNFILLED_VAR_RE.findall(filled)
        assert remaining == [], f"Unfilled variables: {remaining}"


# ---------------------------------------------------------------------------
# Fill Phase 2-5 templates for all 4 modes (no unfilled vars)
# ---------------------------------------------------------------------------

class TestFillAllModesPhase2:
    """Filling cross-review templates for all 4 modes leaves no unfilled vars."""

    MODES = ["cooperative", "winner-take-all", "prisoners-dilemma", "red-blue"]

    @pytest.mark.parametrize("mode", MODES)
    def test_cross_review_fill(
        self, mode: str, tmp_path: Path, example_config_path: Path
    ) -> None:
        templates_dir = find_templates_dir(example_config_path)
        template = load_template(templates_dir, mode, "cross-review")

        config = EngineConfig(
            mode=mode,
            target_files=[Path("/spec.md")],
            output=tmp_path / "out",
            agents=[
                AgentConfig(name="agent-a", prompt="You are A.", role="red" if mode == "red-blue" else None),
                AgentConfig(name="agent-b", prompt="You are B.", role="blue" if mode == "red-blue" else None),
            ],
        )
        ctx = build_cross_review_context(config, "agent-a", "agent-b", config.output)
        filled = fill_template(template, ctx)
        remaining = UNFILLED_VAR_RE.findall(filled)
        assert remaining == [], f"Unfilled in {mode} cross-review: {remaining}"


# ---------------------------------------------------------------------------
# _extract_remaining_disputes helper
# ---------------------------------------------------------------------------

class TestExtractRemainingDisputes:
    """_extract_remaining_disputes handles markers, heading fallback, and empty text."""

    def test_marker_based_extraction(self) -> None:
        text = (
            "# Synthesis\n\n"
            "Some content.\n\n"
            "<!-- DELIBERATOR:DISPUTES_BEGIN -->\n"
            "**Dispute: API contract mismatch**\n"
            "**Dispute: Auth flow incomplete**\n"
            "<!-- DELIBERATOR:DISPUTES_END -->\n"
            "More content."
        )
        result = _extract_remaining_disputes(text, "cooperative")
        assert "API contract mismatch" in result
        assert "Auth flow incomplete" in result

    def test_marker_without_end(self) -> None:
        text = (
            "# Synthesis\n\n"
            "<!-- DELIBERATOR:DISPUTES_BEGIN -->\n"
            "**Dispute: Orphaned dispute**\n"
        )
        result = _extract_remaining_disputes(text, "cooperative")
        assert "Orphaned dispute" in result

    def test_heading_fallback_cooperative(self) -> None:
        text = (
            "# Synthesis\n\n"
            "## Resolved\nAll good.\n\n"
            "### Remaining Disputes\n\n"
            "**Dispute: One dispute**\n"
            "**Dispute: Two dispute**\n\n"
            "## Conclusion\nDone.\n"
        )
        result = _extract_remaining_disputes(text, "cooperative")
        assert "One dispute" in result
        assert "Two dispute" in result

    def test_heading_fallback_winner_take_all(self) -> None:
        text = (
            "# Synthesis\n\n"
            "## Winner\nAlpha wins.\n\n"
            "## Runner-Up\n\n"
            "Beta was close.\n\n"
            "## Conclusion\nDone.\n"
        )
        result = _extract_remaining_disputes(text, "winner-take-all")
        assert "Beta was close" in result

    def test_heading_fallback_red_blue(self) -> None:
        text = (
            "# Synthesis\n\n"
            "### Disputed Risks\n\n"
            "**[RISK-1]: Buffer overflow**\n\n"
            "### Resolved\nDone.\n"
        )
        result = _extract_remaining_disputes(text, "red-blue")
        assert "Buffer overflow" in result

    def test_heading_fallback_prisoners_dilemma(self) -> None:
        text = (
            "# Synthesis\n\n"
            "## Disputed Boundaries\n\n"
            "### [Auth] vs [DB] overlap\n\n"
            "## Conclusion\nDone.\n"
        )
        result = _extract_remaining_disputes(text, "prisoners-dilemma")
        assert "Auth" in result

    def test_empty_text(self) -> None:
        assert _extract_remaining_disputes("", "cooperative") == ""

    def test_no_markers_no_headings(self) -> None:
        text = "# Simple synthesis\n\nNo disputes here.\n"
        assert _extract_remaining_disputes(text, "cooperative") == ""

    def test_markers_take_precedence_over_headings(self) -> None:
        """When both markers and headings are present, markers win."""
        text = (
            "# Synthesis\n\n"
            "<!-- DELIBERATOR:DISPUTES_BEGIN -->\n"
            "**Dispute: Marker dispute**\n"
            "<!-- DELIBERATOR:DISPUTES_END -->\n\n"
            "### Remaining Disputes\n\n"
            "**Dispute: Heading dispute**\n"
        )
        result = _extract_remaining_disputes(text, "cooperative")
        assert "Marker dispute" in result
        assert "Heading dispute" not in result

    def test_unknown_mode_returns_empty(self) -> None:
        text = "# Synthesis\n\n### Remaining Disputes\nSome dispute.\n"
        # Unknown mode has no heading fallback
        assert _extract_remaining_disputes(text, "unknown-mode") == ""


# ---------------------------------------------------------------------------
# Helper: config with arbiter
# ---------------------------------------------------------------------------

def _make_config_with_arbiter(tmp_path: Path) -> EngineConfig:
    """2-agent cooperative config with an arbiter for context builder tests."""
    # Create a real grounding file for the arbiter
    grounding = tmp_path / "grounding.md"
    grounding.write_text("# Grounding\n\nDecision framework here.\n")

    return EngineConfig(
        mode="cooperative",
        target_files=[Path("/spec.md")],
        output=tmp_path / "out",
        agents=[
            AgentConfig(name="alpha", prompt="You are Alpha.", docs=[Path("/docs/alpha")]),
            AgentConfig(name="beta", prompt="You are Beta.", docs=[Path("/docs/beta")]),
        ],
        rounds=3,
        arbiter=ArbiterConfig(
            name="judge",
            prompt="You are the arbiter.",
            docs=[Path("/docs/arbiter")],
            grounding=grounding,
            trigger="disputes_remain",
        ),
    )


# ---------------------------------------------------------------------------
# build_arbitration_context (Phase 6)
# ---------------------------------------------------------------------------

class TestBuildArbitrationContext:
    """build_arbitration_context produces a valid ArbitrationContext."""

    def test_fields_set_correctly(self, tmp_path: Path) -> None:
        config = _make_config_with_arbiter(tmp_path)
        synthesis_text = (
            "# Synthesis\n\n"
            "<!-- DELIBERATOR:DISPUTES_BEGIN -->\n"
            "**Dispute: Auth flow**\n"
            "<!-- DELIBERATOR:DISPUTES_END -->\n"
        )
        ctx = build_arbitration_context(config, config.output, synthesis_text, round_num=1)

        assert isinstance(ctx, ArbitrationContext)
        assert ctx.ARBITER_NAME == "judge"
        assert ctx.ARBITER_PROMPT == "You are the arbiter."
        assert ctx.MODE == "cooperative"
        assert ctx.TRIGGER == "disputes_remain"
        assert ctx.AGENT_NAMES == "alpha, beta"
        assert "Auth flow" in ctx.REMAINING_DISPUTES

    def test_output_path_is_arbiter_resolution(self, tmp_path: Path) -> None:
        config = _make_config_with_arbiter(tmp_path)
        ctx = build_arbitration_context(config, config.output, "", round_num=1)
        assert ctx.OUTPUT_PATH == config.output / "arbitration" / "resolution.md"

    def test_synthesis_path_set(self, tmp_path: Path) -> None:
        config = _make_config_with_arbiter(tmp_path)
        ctx = build_arbitration_context(config, config.output, "", round_num=1)
        assert ctx.SYNTHESIS_PATH == config.output / "summary" / "final.md"

    def test_all_disputes_paths(self, tmp_path: Path) -> None:
        config = _make_config_with_arbiter(tmp_path)
        ctx = build_arbitration_context(config, config.output, "", round_num=1)
        assert len(ctx.ALL_DISPUTES) == 2

    def test_grounding_path_set(self, tmp_path: Path) -> None:
        config = _make_config_with_arbiter(tmp_path)
        ctx = build_arbitration_context(config, config.output, "", round_num=1)
        assert ctx.GROUNDING_PATH == config.arbiter.grounding

    def test_arbiter_docs_serialized(self, tmp_path: Path) -> None:
        config = _make_config_with_arbiter(tmp_path)
        ctx = build_arbitration_context(config, config.output, "", round_num=1)
        assert "/docs/arbiter" in ctx.ARBITER_DOCS

    # ----- Influence level wiring (spec 061 step 13 §3.1.9, issue #110) -----
    #
    # The arbitration template (templates/cooperative/arbitration.md)
    # contains conditional heading instructions keyed on
    # {INFLUENCE_LEVEL}:
    #   - binding:    "Binding Decisions" / "Summary of Changes Required"
    #   - recommended: "Recommended Resolutions" / "Suggested Changes"
    #   - advisory:   "Advisory Opinions" / "Considerations for Next Round"
    #
    # These three tests pin that build_arbitration_context wires the
    # arbiter.influence value through to ArbitrationContext.INFLUENCE_LEVEL
    # for each variant. The downstream LLM follows the conditional
    # instructions in the rendered prompt (verified by the deepeval
    # quality tier when run with a real provider — see PR #83).

    def test_influence_binding_wired_through(self, tmp_path: Path) -> None:
        """Default arbiter (no explicit influence) → INFLUENCE_LEVEL == binding."""
        config = _make_config_with_arbiter(tmp_path)
        ctx = build_arbitration_context(config, config.output, "", round_num=1)
        from engine.templates import InfluenceLevel
        assert ctx.INFLUENCE_LEVEL == InfluenceLevel.BINDING

    def test_influence_recommended_wired_through(self, tmp_path: Path) -> None:
        """influence='recommended' → INFLUENCE_LEVEL == recommended."""
        from engine.config import ArbiterConfig
        from engine.templates import InfluenceLevel
        config = _make_config_with_arbiter(tmp_path)
        recommended_arbiter = ArbiterConfig(
            name=config.arbiter.name,
            prompt=config.arbiter.prompt,
            docs=config.arbiter.docs,
            grounding=config.arbiter.grounding,
            trigger=config.arbiter.trigger,
            influence="recommended",
        )
        config = EngineConfig(
            mode=config.mode,
            target_files=config.target_files,
            output=config.output,
            agents=config.agents,
            rounds=config.rounds,
            arbiter=recommended_arbiter,
        )
        ctx = build_arbitration_context(config, config.output, "", round_num=1)
        assert ctx.INFLUENCE_LEVEL == InfluenceLevel.RECOMMENDED

    def test_influence_advisory_wired_through_and_renders_advisory_headings(
        self, tmp_path: Path
    ) -> None:
        """influence='advisory' → INFLUENCE_LEVEL wired + template renders advisory headings.

        Closes spec 061 step 13 §3.1.9 advisory-heading gap (issue #110).
        Heading divergence is concrete: the rendered prompt (after
        fill_template substitution) contains the advisory-specific
        heading-instruction text from templates/cooperative/arbitration.md
        with {INFLUENCE_LEVEL} substituted to the literal "advisory".
        """
        from engine.config import ArbiterConfig
        from engine.templates import InfluenceLevel, fill_template
        config = _make_config_with_arbiter(tmp_path)
        advisory_arbiter = ArbiterConfig(
            name=config.arbiter.name,
            prompt=config.arbiter.prompt,
            docs=config.arbiter.docs,
            grounding=config.arbiter.grounding,
            trigger=config.arbiter.trigger,
            influence="advisory",
        )
        config = EngineConfig(
            mode=config.mode,
            target_files=config.target_files,
            output=config.output,
            agents=config.agents,
            rounds=config.rounds,
            arbiter=advisory_arbiter,
        )
        ctx = build_arbitration_context(config, config.output, "", round_num=1)

        # Wiring assertion
        assert ctx.INFLUENCE_LEVEL == InfluenceLevel.ADVISORY

        # Heading divergence assertion: render the arbitration template
        # with this context and confirm the advisory-specific heading
        # instructions are present in the rendered output.
        template_path = (
            Path(__file__).resolve().parents[2]
            / "templates"
            / "cooperative"
            / "arbitration.md"
        )
        template = template_path.read_text(encoding="utf-8")
        rendered = fill_template(template, ctx)

        # The literal "advisory" appears where {INFLUENCE_LEVEL} was substituted
        assert "advisory" in rendered.lower()
        # Advisory-specific heading instructions are present in the prompt
        # (these tell the LLM to use "Advisory Opinions" instead of
        # "Binding Decisions" when {INFLUENCE_LEVEL} == advisory)
        assert "Advisory Opinions" in rendered
        assert "Considerations for Next Round" in rendered

    def test_with_round_base(self, tmp_path: Path) -> None:
        config = _make_config_with_arbiter(tmp_path)
        rb = config.output / "round-2"
        ctx = build_arbitration_context(
            config, config.output, "", round_num=2, round_base=rb
        )
        assert ctx.OUTPUT_PATH == rb / "arbitration" / "resolution.md"
        assert ctx.SYNTHESIS_PATH == rb / "summary" / "final.md"

    def test_model_is_frozen(self, tmp_path: Path) -> None:
        config = _make_config_with_arbiter(tmp_path)
        ctx = build_arbitration_context(config, config.output, "", round_num=1)
        with pytest.raises(Exception):
            ctx.ARBITER_NAME = "changed"  # type: ignore[misc]

    def test_no_arbiter_raises(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)  # no arbiter
        with pytest.raises(TemplateError, match="arbiter"):
            build_arbitration_context(config, config.output, "", round_num=1)

    def test_remaining_disputes_empty_when_no_markers(self, tmp_path: Path) -> None:
        config = _make_config_with_arbiter(tmp_path)
        ctx = build_arbitration_context(config, config.output, "Clean synthesis.", round_num=1)
        assert ctx.REMAINING_DISPUTES == ""


# ---------------------------------------------------------------------------
# FR-P2-5 — INFLUENCE_LEVEL wiring in build_arbitration_context
# ---------------------------------------------------------------------------

def _make_config_with_arbiter_influence(
    tmp_path: Path, influence: str
) -> EngineConfig:
    """2-agent cooperative config with arbiter at a specific influence level."""
    grounding = tmp_path / "grounding.md"
    grounding.write_text("# Grounding\n\nDecision framework here.\n")

    return EngineConfig(
        mode="cooperative",
        target_files=[Path("/spec.md")],
        output=tmp_path / "out",
        agents=[
            AgentConfig(name="alpha", prompt="You are Alpha.", docs=[Path("/docs/alpha")]),
            AgentConfig(name="beta", prompt="You are Beta.", docs=[Path("/docs/beta")]),
        ],
        rounds=2,
        arbiter=ArbiterConfig(
            name="judge",
            prompt="You are the arbiter.",
            docs=[],
            grounding=grounding,
            trigger="always",
            timing="inter-round",
            influence=influence,
        ),
    )


class TestBuildArbitrationContextInfluenceLevel:
    """FR-P2-5: build_arbitration_context populates INFLUENCE_LEVEL from
    config.arbiter.influence so arbitration templates can branch on the
    influence level."""

    def test_build_arbitration_context_populates_influence_level_binding(
        self, tmp_path: Path
    ) -> None:
        config = _make_config_with_arbiter_influence(tmp_path, "binding")
        ctx = build_arbitration_context(config, config.output, "", round_num=1)
        assert ctx.INFLUENCE_LEVEL == InfluenceLevel.BINDING
        assert ctx.INFLUENCE_LEVEL == "binding"

    def test_build_arbitration_context_populates_influence_level_recommended(
        self, tmp_path: Path
    ) -> None:
        config = _make_config_with_arbiter_influence(tmp_path, "recommended")
        ctx = build_arbitration_context(config, config.output, "", round_num=1)
        assert ctx.INFLUENCE_LEVEL == InfluenceLevel.RECOMMENDED
        assert ctx.INFLUENCE_LEVEL == "recommended"

    def test_build_arbitration_context_populates_influence_level_advisory(
        self, tmp_path: Path
    ) -> None:
        config = _make_config_with_arbiter_influence(tmp_path, "advisory")
        ctx = build_arbitration_context(config, config.output, "", round_num=1)
        assert ctx.INFLUENCE_LEVEL == InfluenceLevel.ADVISORY
        assert ctx.INFLUENCE_LEVEL == "advisory"

    def test_build_arbitration_context_default_influence_when_arbiter_omits_field(
        self, tmp_path: Path
    ) -> None:
        """When the arbiter is configured without an explicit influence (defaults
        to 'binding' per ArbiterConfig schema), INFLUENCE_LEVEL is BINDING.

        FR-P2-5 spec: ``arbiter=None`` → INFLUENCE_LEVEL == BINDING — but
        ``build_arbitration_context`` raises TemplateError when arbiter is None
        (covered in test_no_arbiter_raises). The default-binding case is the
        ArbiterConfig default itself.
        """
        config = _make_config_with_arbiter(tmp_path)  # uses ArbiterConfig defaults
        ctx = build_arbitration_context(config, config.output, "", round_num=1)
        # ArbiterConfig.influence defaults to "binding"
        assert ctx.INFLUENCE_LEVEL == InfluenceLevel.BINDING

    def test_build_arbitration_context_influence_level_renders_lowercase_in_template(
        self, tmp_path: Path
    ) -> None:
        """When the context is filled into a template, INFLUENCE_LEVEL must
        render as the lowercase string (templates do `if {INFLUENCE_LEVEL} is binding`)."""
        config = _make_config_with_arbiter_influence(tmp_path, "advisory")
        ctx = build_arbitration_context(config, config.output, "", round_num=1)
        template = "Level: '{INFLUENCE_LEVEL}'"
        filled = fill_template(template, ctx)
        assert filled == "Level: 'advisory'"


# ---------------------------------------------------------------------------
# FR-P2-5 — PRIOR_ARBITRATION_SECTION wiring in build_review_context
# ---------------------------------------------------------------------------


class TestBuildReviewContextPriorArbitrationSection:
    """FR-P2-5: build_review_context populates PRIOR_ARBITRATION_SECTION from
    the prior round's arbitration resolution file when the path is supplied."""

    def test_build_review_context_with_prior_arbitration_path_populates_section(
        self, tmp_path: Path
    ) -> None:
        # Arrange — write a real prior-arbitration resolution file
        prior = tmp_path / "round-1" / "arbitration" / "resolution.md"
        prior.parent.mkdir(parents=True, exist_ok=True)
        resolution_body = (
            "# Round 1 Arbitration Resolution\n\n"
            "Binding ruling: adopt position A on dispute X.\n"
        )
        prior.write_text(resolution_body, encoding="utf-8")

        config = _make_cooperative_config(tmp_path)
        # Act
        ctx = build_review_context(
            config,
            config.agents[0],
            config.output,
            round=2,
            prior_arbitration_path=prior,
        )

        # Assert — the section is populated with a header + file contents
        section = ctx.PRIOR_ARBITRATION_SECTION
        assert section.startswith("## Prior arbitration\n")
        assert "Binding ruling: adopt position A on dispute X." in section
        assert "# Round 1 Arbitration Resolution" in section
        # Path field is preserved as-is
        assert ctx.PRIOR_ARBITRATION_PATH == prior

    def test_build_review_context_without_prior_arbitration_path_default_empty(
        self, tmp_path: Path
    ) -> None:
        """Backward-compatibility guard: omitting prior_arbitration_path leaves
        PRIOR_ARBITRATION_SECTION at its default empty string."""
        config = _make_cooperative_config(tmp_path)
        ctx = build_review_context(config, config.agents[0], config.output)
        assert ctx.PRIOR_ARBITRATION_SECTION == ""
        assert ctx.PRIOR_ARBITRATION_PATH is None

    def test_build_review_context_with_missing_prior_arbitration_file_default_empty(
        self, tmp_path: Path
    ) -> None:
        """When the supplied path does not exist, the section stays empty.

        Defensive behavior: a missing prior file should not crash the engine
        nor inject a "Prior arbitration" header with empty body. FR-P2-5
        contract: section is non-empty *only* when the file exists.
        """
        missing = tmp_path / "does-not-exist" / "resolution.md"
        config = _make_cooperative_config(tmp_path)
        ctx = build_review_context(
            config,
            config.agents[0],
            config.output,
            round=2,
            prior_arbitration_path=missing,
        )
        assert ctx.PRIOR_ARBITRATION_SECTION == ""

    def test_prior_arbitration_section_renders_in_review_template(
        self, tmp_path: Path, example_config_path: Path
    ) -> None:
        """End-to-end: filling a real review template with the populated
        section produces output containing the resolution body and no
        unfilled variables."""
        prior = tmp_path / "round-1" / "arbitration" / "resolution.md"
        prior.parent.mkdir(parents=True, exist_ok=True)
        prior.write_text("Round 1 ruling: adopt position B.\n", encoding="utf-8")

        config = _make_cooperative_config(tmp_path)
        ctx = build_review_context(
            config,
            config.agents[0],
            config.output,
            round=2,
            prior_arbitration_path=prior,
        )

        templates_dir = find_templates_dir(example_config_path)
        template = load_template(templates_dir, "cooperative", "review")
        filled = fill_template(template, ctx)
        # Section content must appear; placeholders must be gone
        assert "Round 1 ruling: adopt position B." in filled
        assert "{PRIOR_ARBITRATION_SECTION}" not in filled


# ---------------------------------------------------------------------------
# build_cross_round_synthesis_context
# ---------------------------------------------------------------------------

class TestBuildCrossRoundSynthesisContext:
    """build_cross_round_synthesis_context produces a valid CrossRoundSynthesisContext."""

    def test_fields_set_correctly(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        config = config.model_copy(update={"rounds": 3})
        ctx = build_cross_round_synthesis_context(
            config,
            config.output,
            round_syntheses=["Round 1 content.", "Round 2 content."],
            rounds_completed=2,
            termination_reason="stagnation",
        )

        assert isinstance(ctx, CrossRoundSynthesisContext)
        assert ctx.AGENT_NAMES == "alpha, beta"
        assert ctx.MODE == "cooperative"
        assert ctx.ROUNDS_COMPLETED == 2
        assert ctx.MAX_ROUNDS == 3
        assert ctx.TERMINATION_REASON == "stagnation"

    def test_output_path_is_root_summary(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_cross_round_synthesis_context(
            config, config.output,
            round_syntheses=["R1"],
            rounds_completed=1,
            termination_reason="converged",
        )
        assert ctx.OUTPUT_PATH == config.output / "summary" / "final.md"

    def test_round_syntheses_formatted(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_cross_round_synthesis_context(
            config, config.output,
            round_syntheses=["Round 1 text.", "Round 2 text."],
            rounds_completed=2,
            termination_reason="max_rounds",
        )
        assert "## Round 1 Synthesis" in ctx.ROUND_SYNTHESES
        assert "Round 1 text." in ctx.ROUND_SYNTHESES
        assert "## Round 2 Synthesis" in ctx.ROUND_SYNTHESES
        assert "Round 2 text." in ctx.ROUND_SYNTHESES
        assert "---" in ctx.ROUND_SYNTHESES  # separator between rounds

    def test_target_path_set(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_cross_round_synthesis_context(
            config, config.output,
            round_syntheses=["R1"],
            rounds_completed=1,
            termination_reason="converged",
        )
        assert ctx.TARGET_PATH == Path("/spec.md")

    def test_arbitration_paths_optional(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_cross_round_synthesis_context(
            config, config.output,
            round_syntheses=["R1"],
            rounds_completed=1,
            termination_reason="converged",
        )
        assert ctx.ARBITRATION_PATHS is None
        assert ctx.ARBITRATION_RULINGS is None

    def test_arbitration_paths_when_provided(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        arb_paths = [config.output / "round-1" / "arbiter" / "resolution.md"]
        ctx = build_cross_round_synthesis_context(
            config, config.output,
            round_syntheses=["R1"],
            rounds_completed=1,
            termination_reason="converged",
            arbitration_paths=arb_paths,
            arbitration_rulings="Arbiter ruled X.",
        )
        assert ctx.ARBITRATION_PATHS == arb_paths
        assert ctx.ARBITRATION_RULINGS == "Arbiter ruled X."

    def test_model_is_frozen(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_cross_round_synthesis_context(
            config, config.output,
            round_syntheses=["R1"],
            rounds_completed=1,
            termination_reason="converged",
        )
        with pytest.raises(Exception):
            ctx.AGENT_NAMES = "changed"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Existing builders accept round-related parameters (backward compat)
# ---------------------------------------------------------------------------

class TestRoundAwareExistingBuilders:
    """Existing context builders accept round/prior_* parameters."""

    def test_review_context_with_round(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_review_context(
            config, config.agents[0], config.output,
            round=2,
            prior_synthesis_path="/out/round-1/summary/final.md",
            prior_round_dir="/out/round-1",
            prior_arbitration_path=Path("/out/round-1/arbitration/resolution.md"),
        )
        assert ctx.ROUND == 2
        assert ctx.PRIOR_SYNTHESIS_PATH == "/out/round-1/summary/final.md"
        assert ctx.PRIOR_ROUND_DIR == "/out/round-1"
        assert ctx.PRIOR_ARBITRATION_PATH == Path("/out/round-1/arbitration/resolution.md")

    def test_cross_review_context_with_round(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_cross_review_context(
            config, "alpha", "beta", config.output,
            round=2,
            prior_synthesis_path="/out/round-1/summary/final.md",
        )
        assert ctx.ROUND == 2
        assert ctx.PRIOR_SYNTHESIS_PATH == "/out/round-1/summary/final.md"

    def test_revision_context_with_round(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_revision_context(
            config, "alpha", config.output,
            iteration=1,
            other_agents=["beta"],
            round=3,
            prior_round_dir="/out/round-2",
        )
        assert ctx.ROUND == 3
        assert ctx.PRIOR_ROUND_DIR == "/out/round-2"

    def test_disputes_context_with_round(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_disputes_context(
            config, "alpha", config.output,
            iterations=1,
            all_agents=["alpha", "beta"],
            round=2,
        )
        assert ctx.ROUND == 2

    def test_synthesis_context_with_round(self, tmp_path: Path) -> None:
        config = _make_cooperative_config(tmp_path)
        ctx = build_synthesis_context(
            config, config.output,
            iterations=1,
            round=2,
            prior_synthesis_path="/out/round-1/summary/final.md",
        )
        assert ctx.ROUND == 2
        assert ctx.PRIOR_SYNTHESIS_PATH == "/out/round-1/summary/final.md"

    def test_defaults_preserve_backward_compat(self, tmp_path: Path) -> None:
        """When called without round kwargs, behavior is identical to before."""
        config = _make_cooperative_config(tmp_path)
        ctx = build_review_context(config, config.agents[0], config.output)
        assert ctx.ROUND == 1
        assert ctx.PRIOR_SYNTHESIS_PATH is None
        assert ctx.PRIOR_ROUND_DIR is None
        assert ctx.PRIOR_ARBITRATION_PATH is None
