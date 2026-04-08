"""Tests for engine.adhoc — shared ad-hoc config builder."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest
import yaml

from engine.adhoc import AgentSpec, build_adhoc_config, _sanitize_agent_name
from engine.config import AGENT_NAME_RE, ConfigError, parse_config


class TestBuildAdhocConfig:
    """build_adhoc_config() creates valid temp dir, question.md, and conversus.yml."""

    def test_returns_three_paths(self) -> None:
        config_path, question_path, tmp_dir = build_adhoc_config("Should we use Postgres?")
        try:
            assert config_path.exists()
            assert question_path.exists()
            assert tmp_dir.is_dir()
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

    def test_question_file_contains_question(self) -> None:
        config_path, question_path, tmp_dir = build_adhoc_config("Should we use Postgres?")
        try:
            content = question_path.read_text(encoding="utf-8")
            assert "Should we use Postgres?" in content
            assert "# Question" in content
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

    def test_config_parses_with_parse_config(self) -> None:
        """Generated YAML should be valid for the engine's config parser."""
        config_path, question_path, tmp_dir = build_adhoc_config("Test question")
        try:
            config = parse_config(config_path)
            assert config.mode == "cooperative"
            assert len(config.agents) == 2
            agent_names = {a.name for a in config.agents}
            assert "pragmatist" in agent_names
            assert "devils-advocate" in agent_names
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

    def test_custom_mode(self) -> None:
        config_path, question_path, tmp_dir = build_adhoc_config(
            "Test question", mode="red-blue"
        )
        try:
            raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
            assert raw["mode"] == "red-blue"
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

    def test_custom_output_dir(self, tmp_path: Path) -> None:
        output_dir = tmp_path / "custom-output"
        config_path, question_path, tmp_dir = build_adhoc_config(
            "Test question", output_dir=output_dir
        )
        try:
            raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
            assert str(output_dir.resolve()) in raw["output"]
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

    def test_default_output_in_tmp_dir(self) -> None:
        config_path, question_path, tmp_dir = build_adhoc_config("Test question")
        try:
            raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
            assert str(tmp_dir) in raw["output"]
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

    def test_empty_question_raises_config_error(self) -> None:
        with pytest.raises(ConfigError, match="[Ee]mpty"):
            build_adhoc_config("")

    def test_whitespace_only_question_raises_config_error(self) -> None:
        with pytest.raises(ConfigError, match="[Ee]mpty"):
            build_adhoc_config("   ")

    def test_config_has_two_agents(self) -> None:
        config_path, question_path, tmp_dir = build_adhoc_config("Test question")
        try:
            raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
            assert len(raw["agents"]) == 2
            names = [a["name"] for a in raw["agents"]]
            assert "pragmatist" in names
            assert "devils-advocate" in names
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

    def test_iterations_is_one(self) -> None:
        config_path, question_path, tmp_dir = build_adhoc_config("Test question")
        try:
            raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
            assert raw["iterations"] == 1
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

    def test_display_names_are_sanitized(self) -> None:
        """Agent display names like 'UX Reviewer' should be sanitized to valid config names."""
        agents = [
            AgentSpec(name="UX Reviewer", preset="philosophy/pragmatist"),
            AgentSpec(name="Devils Advocate", preset="role/devils-advocate"),
        ]
        config_path, question_path, tmp_dir = build_adhoc_config(
            "Test question", agents=agents
        )
        try:
            config = parse_config(config_path)
            for agent in config.agents:
                assert AGENT_NAME_RE.match(agent.name), (
                    f"Sanitized name '{agent.name}' doesn't match AGENT_NAME_RE"
                )
            names = {a.name for a in config.agents}
            assert "ux-reviewer" in names
            assert "devils-advocate" in names
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

    def test_duplicate_sanitized_names_get_suffix(self) -> None:
        """Two agents whose display names sanitize to the same slug get deduplicated."""
        agents = [
            AgentSpec(name="UX Reviewer", preset="philosophy/pragmatist"),
            AgentSpec(name="UX-Reviewer!", preset="role/devils-advocate"),
        ]
        config_path, question_path, tmp_dir = build_adhoc_config(
            "Test question", agents=agents
        )
        try:
            raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
            names = [a["name"] for a in raw["agents"]]
            assert len(names) == len(set(names)), f"Duplicate names: {names}"
            assert "ux-reviewer" in names
            assert "ux-reviewer-2" in names
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)


class TestSanitizeAgentName:
    """_sanitize_agent_name converts display names to valid config identifiers."""

    @pytest.mark.parametrize(
        "display,expected",
        [
            ("UX Reviewer", "ux-reviewer"),
            ("Devils Advocate", "devils-advocate"),
            ("pragmatist", "pragmatist"),
            ("My  Super   Agent", "my-super-agent"),
            ("  leading-trailing  ", "leading-trailing"),
            ("ALL_CAPS_NAME", "all-caps-name"),
            ("agent@#$%special", "agent-special"),
            ("---dashes---", "dashes"),
        ],
    )
    def test_converts_display_to_slug(self, display: str, expected: str) -> None:
        result = _sanitize_agent_name(display)
        assert result == expected
        assert AGENT_NAME_RE.match(result), f"'{result}' doesn't match AGENT_NAME_RE"

    def test_empty_input_returns_fallback(self) -> None:
        assert _sanitize_agent_name("") == "agent"
        assert _sanitize_agent_name("   ") == "agent"
        assert _sanitize_agent_name("!@#$") == "agent"
