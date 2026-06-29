"""Tests for engine.config — YAML parsing, validation, and preset resolution."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from engine.config import (
    AGENT_NAME_RE,
    VALID_MODES,
    VALID_PROVIDERS,
    ConfigError,
    EngineConfig,
    parse_config,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_yaml(path: Path, data: dict) -> Path:
    """Write a YAML dict to *path* and return the path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.dump(data, sort_keys=False), encoding="utf-8")
    return path


def _minimal_config(
    tmp_path: Path,
    *,
    mode: str = "cooperative",
    agents: list[dict] | None = None,
    extra: dict | None = None,
) -> Path:
    """Write a minimal valid config with a real target file.

    Creates a stub target file so target resolution succeeds.
    """
    target = tmp_path / "target.md"
    target.write_text("# Target spec\n", encoding="utf-8")

    data: dict = {
        "mode": mode,
        "target": "target.md",
        "output": "out/",
        "agents": agents or [
            {"name": "agent-a", "prompt": "You are agent A."},
            {"name": "agent-b", "prompt": "You are agent B."},
        ],
    }
    if extra:
        data.update(extra)

    return _write_yaml(tmp_path / "deliberator.yml", data)


# ===================================================================
# Parsing the example config
# ===================================================================


class TestParseExampleConfig:
    """Parse deliberator.example.yml and verify the high-level shape."""

    def test_mode(self, sample_engine_config: EngineConfig) -> None:
        assert sample_engine_config.mode == "cooperative"

    def test_agent_count(self, sample_engine_config: EngineConfig) -> None:
        assert len(sample_engine_config.agents) == 3

    def test_agent_names(self, sample_engine_config: EngineConfig) -> None:
        names = [a.name for a in sample_engine_config.agents]
        assert names == ["clarity-reviewer", "technical-reviewer", "adoption-reviewer"]

    def test_target_files(self, sample_engine_config: EngineConfig) -> None:
        assert len(sample_engine_config.target_files) >= 1
        assert all(p.suffix == ".md" for p in sample_engine_config.target_files)

    def test_output_path(self, sample_engine_config: EngineConfig) -> None:
        # The example config sets `output: example-output/`. Assert on the
        # leaf directory name rather than the absolute path — substring
        # checks against the full path are brittle when the repo's local
        # directory name changes (e.g. parent rename or clone location).
        assert sample_engine_config.output.name == "example-output"

    def test_iterations(self, sample_engine_config: EngineConfig) -> None:
        assert sample_engine_config.iterations == 1


# ===================================================================
# Target resolution
# ===================================================================


class TestTargetResolution:
    """Target field resolves single files, lists, and directories."""

    def test_single_file(self, tmp_path: Path) -> None:
        target = tmp_path / "spec.md"
        target.write_text("# Spec\n")
        cfg_path = _write_yaml(tmp_path / "deliberator.yml", {
            "mode": "cooperative",
            "target": "spec.md",
            "output": "out/",
            "agents": [
                {"name": "a", "prompt": "A"},
                {"name": "b", "prompt": "B"},
            ],
        })
        config = parse_config(cfg_path)
        assert len(config.target_files) == 1
        assert config.target_files[0].name == "spec.md"

    def test_file_list(self, tmp_path: Path) -> None:
        for name in ("spec.md", "plan.md"):
            (tmp_path / name).write_text(f"# {name}\n")
        cfg_path = _write_yaml(tmp_path / "deliberator.yml", {
            "mode": "cooperative",
            "target": ["spec.md", "plan.md"],
            "output": "out/",
            "agents": [
                {"name": "a", "prompt": "A"},
                {"name": "b", "prompt": "B"},
            ],
        })
        config = parse_config(cfg_path)
        assert len(config.target_files) == 2

    def test_directory_with_trailing_slash(self, tmp_path: Path) -> None:
        docs = tmp_path / "docs"
        docs.mkdir()
        (docs / "a.md").write_text("# A\n")
        (docs / "b.md").write_text("# B\n")
        cfg_path = _write_yaml(tmp_path / "deliberator.yml", {
            "mode": "cooperative",
            "target": "docs/",
            "output": "out/",
            "agents": [
                {"name": "a", "prompt": "A"},
                {"name": "b", "prompt": "B"},
            ],
        })
        config = parse_config(cfg_path)
        assert len(config.target_files) == 2

    def test_missing_target_file_fails(self, tmp_path: Path) -> None:
        cfg_path = _write_yaml(tmp_path / "deliberator.yml", {
            "mode": "cooperative",
            "target": "nonexistent.md",
            "output": "out/",
            "agents": [
                {"name": "a", "prompt": "A"},
                {"name": "b", "prompt": "B"},
            ],
        })
        with pytest.raises(ConfigError, match="target.*file not found"):
            parse_config(cfg_path)


# ===================================================================
# Agent name validation
# ===================================================================


class TestAgentNameValidation:
    """Agent names must match ^[a-z0-9][a-z0-9-_]*$."""

    @pytest.mark.parametrize("name", ["apm", "spec-kit", "gh-aw", "agent_01"])
    def test_valid_names(self, name: str) -> None:
        assert AGENT_NAME_RE.match(name)

    @pytest.mark.parametrize("name", ["Agent Name", "has spaces", "CamelCase", "_leading"])
    def test_invalid_names_rejected(self, name: str, tmp_path: Path) -> None:
        cfg_path = _minimal_config(
            tmp_path,
            agents=[
                {"name": name, "prompt": "p"},
                {"name": "valid-name", "prompt": "p"},
            ],
        )
        with pytest.raises(ConfigError, match="Invalid agent name"):
            parse_config(cfg_path)


# ===================================================================
# Mode validation
# ===================================================================


class TestModeValidation:
    """All 4 valid modes accepted; invalid modes rejected."""

    @pytest.mark.parametrize("mode", list(VALID_MODES))
    def test_valid_modes_accepted(self, mode: str, tmp_path: Path) -> None:
        agents = [
            {"name": "a", "prompt": "A"},
            {"name": "b", "prompt": "B"},
        ]
        # red-blue needs roles
        if mode == "red-blue":
            agents = [
                {"name": "attacker", "prompt": "red", "role": "red"},
                {"name": "defender", "prompt": "blue", "role": "blue"},
            ]
        cfg_path = _minimal_config(tmp_path, mode=mode, agents=agents)
        config = parse_config(cfg_path)
        assert config.mode == mode

    def test_invalid_mode_rejected(self, tmp_path: Path) -> None:
        cfg_path = _minimal_config(tmp_path, mode="team-deathmatch")
        with pytest.raises(ConfigError, match="mode.*not valid"):
            parse_config(cfg_path)


# ===================================================================
# Red-blue role enforcement
# ===================================================================


class TestRedBlueRoles:
    """red-blue mode requires at least one red and one blue agent."""

    def test_no_red_agent_fails(self, tmp_path: Path) -> None:
        cfg_path = _minimal_config(
            tmp_path,
            mode="red-blue",
            agents=[
                {"name": "a", "prompt": "A", "role": "blue"},
                {"name": "b", "prompt": "B", "role": "blue"},
            ],
        )
        with pytest.raises(ConfigError, match="role: red"):
            parse_config(cfg_path)

    def test_no_blue_agent_fails(self, tmp_path: Path) -> None:
        cfg_path = _minimal_config(
            tmp_path,
            mode="red-blue",
            agents=[
                {"name": "a", "prompt": "A", "role": "red"},
                {"name": "b", "prompt": "B", "role": "red"},
            ],
        )
        with pytest.raises(ConfigError, match="role: blue"):
            parse_config(cfg_path)

    def test_valid_red_blue(self, tmp_path: Path) -> None:
        cfg_path = _minimal_config(
            tmp_path,
            mode="red-blue",
            agents=[
                {"name": "attacker", "prompt": "A", "role": "red"},
                {"name": "defender", "prompt": "B", "role": "blue"},
            ],
        )
        config = parse_config(cfg_path)
        assert config.mode == "red-blue"


# ===================================================================
# Arbiter validation
# ===================================================================


class TestArbiterValidation:
    """Arbiter requires grounding and valid trigger."""

    def _arbiter_config(self, tmp_path: Path, arbiter_data: dict) -> Path:
        grounding = tmp_path / "grounding.md"
        grounding.write_text("# Constitution\n")
        return _minimal_config(tmp_path, extra={"arbiter": arbiter_data})

    def test_missing_grounding_fails(self, tmp_path: Path) -> None:
        cfg_path = self._arbiter_config(tmp_path, {
            "name": "arbiter",
            "prompt": "You decide.",
            "trigger": "always",
            # no grounding
        })
        with pytest.raises(ConfigError, match="grounding"):
            parse_config(cfg_path)

    def test_missing_trigger_fails(self, tmp_path: Path) -> None:
        cfg_path = self._arbiter_config(tmp_path, {
            "name": "arbiter",
            "prompt": "You decide.",
            "grounding": "grounding.md",
            # trigger omitted → None
        })
        with pytest.raises(ConfigError, match="trigger"):
            parse_config(cfg_path)

    def test_invalid_trigger_fails(self, tmp_path: Path) -> None:
        cfg_path = self._arbiter_config(tmp_path, {
            "name": "arbiter",
            "prompt": "You decide.",
            "grounding": "grounding.md",
            "trigger": "sometimes",
        })
        with pytest.raises(ConfigError, match="trigger"):
            parse_config(cfg_path)

    def test_valid_arbiter(self, tmp_path: Path) -> None:
        grounding = tmp_path / "grounding.md"
        grounding.write_text("# Constitution\n")
        cfg_path = _minimal_config(tmp_path, extra={
            "arbiter": {
                "name": "arbiter",
                "prompt": "You decide.",
                "grounding": "grounding.md",
                "trigger": "disputes_remain",
            }
        })
        config = parse_config(cfg_path)
        assert config.arbiter is not None
        assert config.arbiter.trigger == "disputes_remain"


# ===================================================================
# Rounds validation
# ===================================================================


class TestRoundsValidation:
    """rounds must be 1-5; 0 and 6 rejected with appropriate messages."""

    @pytest.mark.parametrize("rounds", [1, 2, 3, 4, 5])
    def test_valid_rounds_accepted(self, rounds: int, tmp_path: Path) -> None:
        cfg_path = _minimal_config(tmp_path, extra={"rounds": rounds})
        config = parse_config(cfg_path)
        assert config.rounds == rounds

    def test_zero_rejected(self, tmp_path: Path) -> None:
        cfg_path = _minimal_config(tmp_path, extra={"rounds": 0})
        with pytest.raises(ConfigError, match="rounds"):
            parse_config(cfg_path)

    def test_six_rejected_with_arbiter_suggestion(self, tmp_path: Path) -> None:
        cfg_path = _minimal_config(tmp_path, extra={"rounds": 6})
        with pytest.raises(ConfigError, match="arbiter"):
            parse_config(cfg_path)


# ===================================================================
# Stagnation validation
# ===================================================================


class TestStagnationValidation:
    """stagnation must be 'detect' or 'ignore'."""

    @pytest.mark.parametrize("value", ["detect", "ignore"])
    def test_valid_values(self, value: str, tmp_path: Path) -> None:
        cfg_path = _minimal_config(tmp_path, extra={"stagnation": value})
        config = parse_config(cfg_path)
        assert config.stagnation == value

    def test_invalid_value_rejected(self, tmp_path: Path) -> None:
        cfg_path = _minimal_config(tmp_path, extra={"stagnation": "panic"})
        with pytest.raises(ConfigError, match="stagnation"):
            parse_config(cfg_path)


# ===================================================================
# Preset resolution
# ===================================================================


class TestPresetResolution:
    """Preset resolution: single, composed, error cases."""

    def test_single_qualified_preset(self, tmp_path: Path) -> None:
        target = tmp_path / "spec.md"
        target.write_text("# Spec\n")
        cfg_path = _write_yaml(tmp_path / "deliberator.yml", {
            "mode": "cooperative",
            "target": "spec.md",
            "output": "out/",
            "agents": [
                {"name": "a", "preset": "domain/security"},
                {"name": "b", "prompt": "You are B."},
            ],
        })
        config = parse_config(cfg_path)
        assert "security" in config.agents[0].prompt.lower()

    def test_single_unqualified_preset(self, tmp_path: Path) -> None:
        target = tmp_path / "spec.md"
        target.write_text("# Spec\n")
        cfg_path = _write_yaml(tmp_path / "deliberator.yml", {
            "mode": "cooperative",
            "target": "spec.md",
            "output": "out/",
            "agents": [
                {"name": "a", "preset": "security"},
                {"name": "b", "prompt": "You are B."},
            ],
        })
        config = parse_config(cfg_path)
        assert len(config.agents[0].prompt) > 10  # resolved successfully

    def test_composed_two_presets(self, tmp_path: Path) -> None:
        target = tmp_path / "spec.md"
        target.write_text("# Spec\n")
        cfg_path = _write_yaml(tmp_path / "deliberator.yml", {
            "mode": "cooperative",
            "target": "spec.md",
            "output": "out/",
            "agents": [
                {"name": "a", "preset": ["domain/security", "philosophy/pragmatist"]},
                {"name": "b", "prompt": "You are B."},
            ],
        })
        config = parse_config(cfg_path)
        # Composed prompt contains both preset names
        assert "security" in config.agents[0].prompt
        assert "pragmatist" in config.agents[0].prompt

    def test_composed_four_presets_rejected(self, tmp_path: Path) -> None:
        target = tmp_path / "spec.md"
        target.write_text("# Spec\n")
        cfg_path = _write_yaml(tmp_path / "deliberator.yml", {
            "mode": "cooperative",
            "target": "spec.md",
            "output": "out/",
            "agents": [
                {
                    "name": "a",
                    "preset": [
                        "domain/security",
                        "domain/performance",
                        "domain/cost",
                        "domain/ux",
                    ],
                },
                {"name": "b", "prompt": "You are B."},
            ],
        })
        with pytest.raises(ConfigError, match="Maximum 3 presets"):
            parse_config(cfg_path)

    def test_nonexistent_preset_error(self, tmp_path: Path) -> None:
        target = tmp_path / "spec.md"
        target.write_text("# Spec\n")
        cfg_path = _write_yaml(tmp_path / "deliberator.yml", {
            "mode": "cooperative",
            "target": "spec.md",
            "output": "out/",
            "agents": [
                {"name": "a", "preset": "standard/does-not-exist"},
                {"name": "b", "prompt": "You are B."},
            ],
        })
        with pytest.raises(ConfigError, match="Preset.*not found"):
            parse_config(cfg_path)


# ===================================================================
# Prior file resolution
# ===================================================================


class TestPriorFiles:
    """Prior files resolve when present and are optional when absent."""

    def test_prior_present(self, tmp_path: Path) -> None:
        target = tmp_path / "spec.md"
        target.write_text("# Spec\n")
        prior = tmp_path / "prior.md"
        prior.write_text("# Prior\n")
        cfg_path = _write_yaml(tmp_path / "deliberator.yml", {
            "mode": "cooperative",
            "target": "spec.md",
            "output": "out/",
            "prior": "prior.md",
            "agents": [
                {"name": "a", "prompt": "A"},
                {"name": "b", "prompt": "B"},
            ],
        })
        config = parse_config(cfg_path)
        assert len(config.prior_files) == 1

    def test_no_prior_is_ok(self, tmp_path: Path) -> None:
        cfg_path = _minimal_config(tmp_path)
        config = parse_config(cfg_path)
        assert config.prior_files == []


# ===================================================================
# Edge cases
# ===================================================================


class TestConfigEdgeCases:
    """Missing config, too few agents, duplicate names."""

    def test_missing_config_file(self, tmp_path: Path) -> None:
        with pytest.raises(ConfigError, match="not found"):
            parse_config(tmp_path / "nonexistent.yml")

    def test_fewer_than_two_agents(self, tmp_path: Path) -> None:
        cfg_path = _minimal_config(
            tmp_path,
            agents=[{"name": "solo", "prompt": "alone"}],
        )
        with pytest.raises(ConfigError, match="at least 2"):
            parse_config(cfg_path)

    def test_duplicate_agent_names(self, tmp_path: Path) -> None:
        cfg_path = _minimal_config(
            tmp_path,
            agents=[
                {"name": "dup", "prompt": "A"},
                {"name": "dup", "prompt": "B"},
            ],
        )
        with pytest.raises(ConfigError, match="Duplicate"):
            parse_config(cfg_path)


# ===================================================================
# Provider field
# ===================================================================


class TestProviderField:
    """provider field defaults to 'anthropic' and validates values."""

    def test_default_is_anthropic(self, tmp_path: Path) -> None:
        """Configs that omit 'provider' default to anthropic (K008 backward compat)."""
        cfg_path = _minimal_config(tmp_path)
        config = parse_config(cfg_path)
        assert config.provider == "anthropic"

    @pytest.mark.parametrize("provider", list(VALID_PROVIDERS))
    def test_valid_providers_accepted(self, provider: str, tmp_path: Path) -> None:
        cfg_path = _minimal_config(tmp_path, extra={"provider": provider})
        config = parse_config(cfg_path)
        assert config.provider == provider

    def test_invalid_provider_rejected(self, tmp_path: Path) -> None:
        cfg_path = _minimal_config(tmp_path, extra={"provider": "nonexistent-provider"})
        with pytest.raises(ConfigError, match="provider.*not valid"):
            parse_config(cfg_path)

    def test_existing_configs_unaffected(self, sample_engine_config: EngineConfig) -> None:
        """The example config has no provider field and still parses fine."""
        assert sample_engine_config.provider == "anthropic"


# ===================================================================
# Per-agent overrides (provider, model, timeout)
# ===================================================================


class TestAgentOverrides:
    """Per-agent provider, model, and timeout fields from deliberator.yml."""

    def test_agent_provider_default_none(self, tmp_path: Path) -> None:
        cfg_path = _minimal_config(tmp_path)
        config = parse_config(cfg_path)
        for agent in config.agents:
            assert agent.provider is None

    def test_agent_provider_set(self, tmp_path: Path) -> None:
        cfg_path = _minimal_config(tmp_path, agents=[
            {"name": "a", "prompt": "A", "provider": "ollama"},
            {"name": "b", "prompt": "B"},
        ])
        config = parse_config(cfg_path)
        assert config.agents[0].provider == "ollama"
        assert config.agents[1].provider is None

    def test_agent_model_default_none(self, tmp_path: Path) -> None:
        cfg_path = _minimal_config(tmp_path)
        config = parse_config(cfg_path)
        for agent in config.agents:
            assert agent.agent_model is None

    def test_agent_model_set(self, tmp_path: Path) -> None:
        cfg_path = _minimal_config(tmp_path, agents=[
            {"name": "a", "prompt": "A", "model": "opus"},
            {"name": "b", "prompt": "B", "model": "haiku"},
        ])
        config = parse_config(cfg_path)
        assert config.agents[0].agent_model == "opus"
        assert config.agents[1].agent_model == "haiku"

    def test_agent_timeout_default_none(self, tmp_path: Path) -> None:
        cfg_path = _minimal_config(tmp_path)
        config = parse_config(cfg_path)
        for agent in config.agents:
            assert agent.timeout is None

    def test_agent_timeout_set(self, tmp_path: Path) -> None:
        cfg_path = _minimal_config(tmp_path, agents=[
            {"name": "a", "prompt": "A", "timeout": 1200},
            {"name": "b", "prompt": "B"},
        ])
        config = parse_config(cfg_path)
        assert config.agents[0].timeout == 1200
        assert config.agents[1].timeout is None

    def test_agent_timeout_string_coerced(self, tmp_path: Path) -> None:
        """YAML may parse '1200' as string; should be coerced to int."""
        cfg_path = _minimal_config(tmp_path, agents=[
            {"name": "a", "prompt": "A", "timeout": "900"},
            {"name": "b", "prompt": "B"},
        ])
        config = parse_config(cfg_path)
        assert config.agents[0].timeout == 900
        assert isinstance(config.agents[0].timeout, int)

    def test_heterogeneous_agents(self, tmp_path: Path) -> None:
        """Full heterogeneous config: different providers, models, timeouts."""
        cfg_path = _minimal_config(tmp_path, agents=[
            {"name": "local", "prompt": "A", "provider": "ollama", "model": "qwen3:0.6b", "timeout": 300},
            {"name": "cloud", "prompt": "B", "provider": "claude-code", "model": "opus", "timeout": 1200},
        ])
        config = parse_config(cfg_path)
        local = config.agents[0]
        cloud = config.agents[1]
        assert local.provider == "ollama"
        assert local.agent_model == "qwen3:0.6b"
        assert local.timeout == 300
        assert cloud.provider == "claude-code"
        assert cloud.agent_model == "opus"
        assert cloud.timeout == 1200


# ===================================================================
# Path resolution rules — uniform behavior across target / output /
# arbiter.grounding. Documented in docs/user-guide/config-reference.md.
# ===================================================================


class TestPathResolution:
    """Pin down the resolution rules for target / output / arbiter.grounding.

    Resolution semantics by field:

    - **target** (input, read): two-pass — try config-dir-relative first,
      fall back to CWD-relative. Convenience for `target: README.md`
      from a config in a subdirectory, run from project root.
    - **arbiter.grounding** (input, read): same two-pass as target.
      Grounding is a read target like target, so users get the same
      "works from any cwd if file exists somewhere" UX.
    - **output** (write target): config-dir-relative only. No fallback
      because the directory does not have to exist yet — we cannot
      probe "where would this end up." Users who want CWD-relative
      output must use an absolute path.

    These tests lock in the contract so the rule cannot drift silently.
    """

    def _grounding_config(
        self, tmp_path: Path, grounding_value: str, grounding_file_at: Path,
    ) -> Path:
        """Write a config in `<tmp_path>/configs/` with an arbiter that
        sets `grounding:` to *grounding_value*. Creates the actual
        grounding file at *grounding_file_at*.
        """
        grounding_file_at.parent.mkdir(parents=True, exist_ok=True)
        grounding_file_at.write_text("# Grounding doc\n", encoding="utf-8")

        target = tmp_path / "spec.md"
        target.write_text("# Target\n", encoding="utf-8")

        config_dir = tmp_path / "configs"
        config_dir.mkdir(exist_ok=True)

        cfg = config_dir / "deliberator.yml"
        cfg.write_text(yaml.dump({
            "mode": "cooperative",
            # Target uses absolute path so the test isolates grounding behavior.
            "target": str(target),
            "output": "out/",
            "agents": [
                {"name": "a", "prompt": "P1"},
                {"name": "b", "prompt": "P2"},
            ],
            "arbiter": {
                "name": "the-subject",
                "prompt": "You decide.",
                "grounding": grounding_value,
                "trigger": "disputes_remain",
            },
        }, sort_keys=False), encoding="utf-8")
        return cfg

    def test_grounding_resolves_config_dir_relative(self, tmp_path: Path) -> None:
        """`grounding: file.md` finds `<config-dir>/file.md` (pass 1)."""
        cfg = self._grounding_config(
            tmp_path,
            grounding_value="constitution.md",
            grounding_file_at=tmp_path / "configs" / "constitution.md",
        )
        config = parse_config(cfg)
        assert config.arbiter is not None
        assert config.arbiter.grounding.name == "constitution.md"
        assert "configs" in str(config.arbiter.grounding)

    def test_grounding_falls_back_to_cwd_relative(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """When the config-dir lookup misses, falls back to CWD.

        Mirrors target's documented two-pass behavior. Without the
        fallback, `grounding: CHANGELOG.md` would fail when invoked
        from the project root with a config in a subdirectory — which
        is the exact failure mode PR #164 hit while building the
        examples/with-arbiter.yml.
        """
        # Grounding file lives at tmp_path, not under tmp_path/configs/.
        cfg = self._grounding_config(
            tmp_path,
            grounding_value="from-cwd.md",
            grounding_file_at=tmp_path / "from-cwd.md",
        )
        # Invoke from tmp_path so cwd-relative lookup finds the file.
        monkeypatch.chdir(tmp_path)
        config = parse_config(cfg)
        assert config.arbiter is not None
        assert config.arbiter.grounding.name == "from-cwd.md"

    def test_grounding_error_message_lists_both_attempts(
        self, tmp_path: Path,
    ) -> None:
        """When neither pass finds the file, the error names both paths."""
        cfg = self._grounding_config(
            tmp_path,
            grounding_value="missing.md",
            # Write a fake grounding file somewhere else so the create-step
            # in _grounding_config does its job but the resolver still misses.
            grounding_file_at=tmp_path / "elsewhere" / "missing.md",
        )
        # Delete the file so both passes fail.
        (tmp_path / "elsewhere" / "missing.md").unlink()
        with pytest.raises(ConfigError) as excinfo:
            parse_config(cfg)
        msg = str(excinfo.value)
        assert "missing.md" in msg
        assert "tried" in msg  # error names both attempted paths

    def test_output_is_config_dir_relative_only(self, tmp_path: Path) -> None:
        """`output: out/` resolves to `<config-dir>/out/`, not `<cwd>/out/`.

        Output is a WRITE target — no fallback semantics apply because
        the directory doesn't have to exist yet. Users who want a
        different anchor must use an absolute path.
        """
        target = tmp_path / "spec.md"
        target.write_text("# Target\n")
        config_dir = tmp_path / "nested" / "configs"
        config_dir.mkdir(parents=True)
        cfg = config_dir / "deliberator.yml"
        cfg.write_text(yaml.dump({
            "mode": "cooperative",
            "target": str(target),
            "output": "deliberation-output/",
            "agents": [
                {"name": "a", "prompt": "P"},
                {"name": "b", "prompt": "P"},
            ],
        }, sort_keys=False), encoding="utf-8")
        config = parse_config(cfg)
        # Output must be anchored at the config file's directory.
        assert config.output.parent == config_dir.resolve()
        assert config.output.name == "deliberation-output"

    def test_output_absolute_path_preserved(self, tmp_path: Path) -> None:
        """An absolute `output:` path is used as-is (escape hatch)."""
        absolute_out = tmp_path / "abs-output"
        cfg_path = _minimal_config(
            tmp_path,
            extra={"output": str(absolute_out)},
        )
        config = parse_config(cfg_path)
        assert config.output == absolute_out.resolve()
