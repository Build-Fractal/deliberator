"""Tests for engine.project — .conversus/ directory management.

Covers init_project, read_settings, find_conversus_dir, and all runtime
config generators with real assertions on file content and structure.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from engine.project import (
    AVAILABLE_RUNTIMES,
    CONVERSUS_DIR,
    DEFAULT_SETTINGS,
    GITIGNORE_CONTENT,
    RUNTIME_CONFIGS,
    SETTINGS_FILE,
    _aider_config,
    _claude_config,
    _codex_config,
    _copilot_config,
    _gemini_config,
    _merge_claude_settings,
    _opencode_config,
    find_conversus_dir,
    init_project,
    read_settings,
)


# ===================================================================
# Runtime config generators
# ===================================================================


class TestClaudeConfig:
    """_claude_config returns None content (merge semantics), _merge_claude_settings creates/merges."""

    def test_returns_correct_dir_and_filename(self) -> None:
        dir_name, filename, content = _claude_config()
        assert dir_name == ".claude"
        assert filename == "settings.json"
        assert content is None  # Signals caller to use merge function

    def test_merge_creates_new_file(self, tmp_path: Path) -> None:
        result = _merge_claude_settings(tmp_path)
        assert result is not None
        data = json.loads((tmp_path / ".claude" / "settings.json").read_text())
        assert "permissions" in data
        assert "allow" in data["permissions"]

    def test_merge_includes_file_perms(self, tmp_path: Path) -> None:
        _merge_claude_settings(tmp_path)
        data = json.loads((tmp_path / ".claude" / "settings.json").read_text())
        allow = data["permissions"]["allow"]
        for perm in ("Read", "Write", "Edit", "Glob", "Grep", "Agent"):
            assert perm in allow, f"Missing expected permission: {perm}"

    def test_merge_includes_bash_perms(self, tmp_path: Path) -> None:
        _merge_claude_settings(tmp_path)
        data = json.loads((tmp_path / ".claude" / "settings.json").read_text())
        bash_perms = [p for p in data["permissions"]["allow"] if p.startswith("Bash(")]
        assert len(bash_perms) > 0

    def test_merge_preserves_existing_perms(self, tmp_path: Path) -> None:
        """Merge adds missing perms without removing existing ones."""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        existing = {"permissions": {"allow": ["Bash(docker:*)", "Bash(aws:*)"]}, "hooks": {"foo": "bar"}}
        (claude_dir / "settings.json").write_text(json.dumps(existing))
        _merge_claude_settings(tmp_path)
        data = json.loads((claude_dir / "settings.json").read_text())
        allow = data["permissions"]["allow"]
        assert "Bash(docker:*)" in allow  # Preserved
        assert "Bash(aws:*)" in allow     # Preserved
        assert "Agent" in allow            # Added
        assert "hooks" in data             # Preserved

    def test_merge_noop_when_all_present(self, tmp_path: Path) -> None:
        """Returns None if existing file already has all needed perms."""
        _merge_claude_settings(tmp_path)  # Create initial
        result = _merge_claude_settings(tmp_path)  # Should be noop
        assert result is None

    def test_merge_deny_is_empty(self, tmp_path: Path) -> None:
        _merge_claude_settings(tmp_path)
        data = json.loads((tmp_path / ".claude" / "settings.json").read_text())
        assert data["permissions"]["deny"] == []


class TestOpenCodeConfig:
    """_opencode_config produces valid TOML-shaped content."""

    def test_returns_correct_dir_and_filename(self) -> None:
        dir_name, filename, _ = _opencode_config()
        assert dir_name == ".opencode"
        assert filename == "config.toml"

    def test_content_has_agent_section(self) -> None:
        _, _, content = _opencode_config()
        assert "[agent]" in content

    def test_content_has_model_section(self) -> None:
        _, _, content = _opencode_config()
        assert "[model]" in content

    def test_auto_approve_set(self) -> None:
        _, _, content = _opencode_config()
        assert "auto_approve = true" in content

    def test_max_turns_set(self) -> None:
        _, _, content = _opencode_config()
        assert "max_turns = 50" in content

    def test_mentions_conversus_init(self) -> None:
        _, _, content = _opencode_config()
        assert "conversus init" in content


class TestCopilotConfig:
    """_copilot_config produces valid GitHub Copilot settings."""

    def test_returns_correct_dir_and_filename(self) -> None:
        dir_name, filename, _ = _copilot_config()
        assert dir_name == ".github"
        assert filename == "copilot-settings.json"

    def test_content_is_valid_json(self) -> None:
        _, _, content = _copilot_config()
        data = json.loads(content)
        assert isinstance(data, dict)

    def test_copilot_agent_mode_enabled(self) -> None:
        _, _, content = _copilot_config()
        data = json.loads(content)
        assert data["copilot"]["conversus_agent_mode"] is True

    def test_auto_approve_enabled(self) -> None:
        _, _, content = _copilot_config()
        data = json.loads(content)
        assert data["copilot"]["auto_approve"] is True

    def test_content_ends_with_newline(self) -> None:
        _, _, content = _copilot_config()
        assert content.endswith("\n")


class TestGeminiConfig:
    """_gemini_config produces valid Gemini CLI settings."""

    def test_returns_correct_dir_and_filename(self) -> None:
        dir_name, filename, _ = _gemini_config()
        assert dir_name == ".gemini"
        assert filename == "settings.json"

    def test_content_is_valid_json(self) -> None:
        _, _, content = _gemini_config()
        data = json.loads(content)
        assert isinstance(data, dict)

    def test_sandbox_none(self) -> None:
        _, _, content = _gemini_config()
        data = json.loads(content)
        assert data["sandbox"] == "none"

    def test_auto_approve_enabled(self) -> None:
        _, _, content = _gemini_config()
        data = json.loads(content)
        assert data["auto_approve"] is True

    def test_conversus_agent_flag(self) -> None:
        _, _, content = _gemini_config()
        data = json.loads(content)
        assert data["conversus_agent"] is True


class TestCodexConfig:
    """_codex_config produces valid Codex CLI settings."""

    def test_returns_correct_dir_and_filename(self) -> None:
        dir_name, filename, _ = _codex_config()
        assert dir_name == ".codex"
        assert filename == "settings.json"

    def test_content_is_valid_json(self) -> None:
        _, _, content = _codex_config()
        data = json.loads(content)
        assert isinstance(data, dict)

    def test_full_auto_enabled(self) -> None:
        _, _, content = _codex_config()
        data = json.loads(content)
        assert data["full_auto"] is True

    def test_quiet_enabled(self) -> None:
        _, _, content = _codex_config()
        data = json.loads(content)
        assert data["quiet"] is True

    def test_conversus_agent_flag(self) -> None:
        _, _, content = _codex_config()
        data = json.loads(content)
        assert data["conversus_agent"] is True


class TestAiderConfig:
    """_aider_config produces valid Aider YAML config."""

    def test_returns_empty_dir_name(self) -> None:
        dir_name, _, _ = _aider_config()
        assert dir_name == ""

    def test_returns_correct_filename(self) -> None:
        _, filename, _ = _aider_config()
        assert filename == ".aider.conf.yml"

    def test_auto_commits_disabled(self) -> None:
        _, _, content = _aider_config()
        assert "auto-commits: false" in content

    def test_auto_lint_disabled(self) -> None:
        _, _, content = _aider_config()
        assert "auto-lint: false" in content

    def test_yes_always_enabled(self) -> None:
        _, _, content = _aider_config()
        assert "yes-always: true" in content

    def test_stream_disabled(self) -> None:
        _, _, content = _aider_config()
        assert "stream: false" in content

    def test_mentions_conversus(self) -> None:
        _, _, content = _aider_config()
        assert "conversus" in content


class TestRuntimeConfigsRegistry:
    """RUNTIME_CONFIGS and AVAILABLE_RUNTIMES are consistent."""

    def test_all_runtimes_have_generators(self) -> None:
        for name in AVAILABLE_RUNTIMES:
            assert name in RUNTIME_CONFIGS
            assert callable(RUNTIME_CONFIGS[name])

    def test_available_runtimes_sorted(self) -> None:
        assert AVAILABLE_RUNTIMES == sorted(AVAILABLE_RUNTIMES)

    def test_expected_runtimes_present(self) -> None:
        expected = {"claude-code", "opencode", "copilot", "gemini", "codex", "aider"}
        assert expected == set(RUNTIME_CONFIGS.keys())

    def test_every_generator_returns_three_element_tuple(self) -> None:
        for name, fn in RUNTIME_CONFIGS.items():
            result = fn()
            assert isinstance(result, tuple), f"{name} did not return a tuple"
            assert len(result) == 3, f"{name} returned {len(result)} elements"
            dir_name, filename, content = result
            assert isinstance(dir_name, str), f"{name} dir_name not str"
            assert isinstance(filename, str), f"{name} filename not str"
            # claude-code returns None content (uses merge semantics)
            if name == "claude-code":
                assert content is None, f"claude-code should return None content"
            else:
                assert isinstance(content, str), f"{name} content not str"
                assert len(content) > 0, f"{name} content is empty"
            assert len(filename) > 0, f"{name} filename is empty"


# ===================================================================
# init_project
# ===================================================================


class TestInitProjectCreatesStructure:
    """init_project creates the right directories and files."""

    def test_creates_conversus_dir(self, tmp_path: Path) -> None:
        init_project(tmp_path)
        assert (tmp_path / CONVERSUS_DIR).is_dir()

    def test_creates_output_dir(self, tmp_path: Path) -> None:
        init_project(tmp_path)
        assert (tmp_path / CONVERSUS_DIR / "output").is_dir()

    def test_creates_settings_json(self, tmp_path: Path) -> None:
        init_project(tmp_path)
        settings_path = tmp_path / CONVERSUS_DIR / SETTINGS_FILE
        assert settings_path.is_file()

    def test_settings_json_is_valid(self, tmp_path: Path) -> None:
        init_project(tmp_path)
        settings_path = tmp_path / CONVERSUS_DIR / SETTINGS_FILE
        data = json.loads(settings_path.read_text(encoding="utf-8"))
        assert data["default_provider"] == "claude-code"
        assert data["default_model"] == "sonnet"
        assert data["runtimes"] == ["claude-code"]
        assert data["output_dir"] == "output"

    def test_creates_gitignore(self, tmp_path: Path) -> None:
        init_project(tmp_path)
        gitignore_path = tmp_path / CONVERSUS_DIR / ".gitignore"
        assert gitignore_path.is_file()
        assert gitignore_path.read_text(encoding="utf-8") == GITIGNORE_CONTENT

    def test_creates_claude_config_by_default(self, tmp_path: Path) -> None:
        init_project(tmp_path)
        claude_settings = tmp_path / ".claude" / "settings.json"
        assert claude_settings.is_file()
        data = json.loads(claude_settings.read_text(encoding="utf-8"))
        assert "permissions" in data

    def test_returns_dict_of_created_paths(self, tmp_path: Path) -> None:
        created = init_project(tmp_path)
        assert isinstance(created, dict)
        assert "settings" in created
        assert "gitignore" in created
        assert "runtime:claude-code" in created
        # All values are Path objects that exist
        for key, path in created.items():
            assert isinstance(path, Path), f"{key} value is not a Path"
            assert path.exists(), f"{key} path does not exist: {path}"


class TestInitProjectCustomSettings:
    """init_project respects custom provider, model, and runtime arguments."""

    def test_custom_provider(self, tmp_path: Path) -> None:
        init_project(tmp_path, default_provider="opencode")
        data = json.loads(
            (tmp_path / CONVERSUS_DIR / SETTINGS_FILE).read_text(encoding="utf-8")
        )
        assert data["default_provider"] == "opencode"

    def test_custom_model(self, tmp_path: Path) -> None:
        init_project(tmp_path, default_model="opus")
        data = json.loads(
            (tmp_path / CONVERSUS_DIR / SETTINGS_FILE).read_text(encoding="utf-8")
        )
        assert data["default_model"] == "opus"

    def test_multiple_runtimes(self, tmp_path: Path) -> None:
        runtimes = ["claude-code", "opencode", "gemini"]
        created = init_project(tmp_path, runtimes=runtimes)
        # All three runtime configs should be created
        assert "runtime:claude-code" in created
        assert "runtime:opencode" in created
        assert "runtime:gemini" in created
        # Verify dirs exist
        assert (tmp_path / ".claude" / "settings.json").is_file()
        assert (tmp_path / ".opencode" / "config.toml").is_file()
        assert (tmp_path / ".gemini" / "settings.json").is_file()

    def test_runtimes_recorded_in_settings(self, tmp_path: Path) -> None:
        runtimes = ["claude-code", "copilot"]
        init_project(tmp_path, runtimes=runtimes)
        data = json.loads(
            (tmp_path / CONVERSUS_DIR / SETTINGS_FILE).read_text(encoding="utf-8")
        )
        assert data["runtimes"] == runtimes

    def test_aider_runtime_creates_file_in_root(self, tmp_path: Path) -> None:
        init_project(tmp_path, runtimes=["aider"])
        aider_conf = tmp_path / ".aider.conf.yml"
        assert aider_conf.is_file()
        content = aider_conf.read_text(encoding="utf-8")
        assert "auto-commits: false" in content

    def test_unknown_runtime_silently_skipped(self, tmp_path: Path) -> None:
        created = init_project(tmp_path, runtimes=["nonexistent-runtime"])
        # Should not have a runtime key for the unknown runtime
        assert "runtime:nonexistent-runtime" not in created
        # Should still create the base structure
        assert (tmp_path / CONVERSUS_DIR).is_dir()

    def test_all_runtimes(self, tmp_path: Path) -> None:
        """Every known runtime generates its config file."""
        created = init_project(tmp_path, runtimes=AVAILABLE_RUNTIMES)
        for runtime in AVAILABLE_RUNTIMES:
            assert f"runtime:{runtime}" in created, f"Missing runtime:{runtime}"
            assert created[f"runtime:{runtime}"].is_file()


class TestInitProjectIdempotent:
    """Re-running init_project without --force does not overwrite."""

    def test_settings_not_overwritten(self, tmp_path: Path) -> None:
        init_project(tmp_path, default_model="sonnet")
        # Manually alter the settings file
        settings_path = tmp_path / CONVERSUS_DIR / SETTINGS_FILE
        original_content = settings_path.read_text(encoding="utf-8")
        settings_path.write_text('{"custom": true}\n', encoding="utf-8")

        # Re-run without force
        created = init_project(tmp_path, default_model="opus")
        # settings key should NOT be in created (file was not overwritten)
        assert "settings" not in created
        # Content should be the manually-written version
        assert settings_path.read_text(encoding="utf-8") == '{"custom": true}\n'

    def test_gitignore_not_overwritten(self, tmp_path: Path) -> None:
        init_project(tmp_path)
        gitignore_path = tmp_path / CONVERSUS_DIR / ".gitignore"
        gitignore_path.write_text("custom content\n", encoding="utf-8")

        created = init_project(tmp_path)
        assert "gitignore" not in created
        assert gitignore_path.read_text(encoding="utf-8") == "custom content\n"

    def test_runtime_config_not_overwritten_when_complete(self, tmp_path: Path) -> None:
        """If .claude/settings.json already has all agent perms, merge is a noop."""
        init_project(tmp_path, runtimes=["claude-code"])  # Creates with agent perms

        created = init_project(tmp_path, runtimes=["claude-code"])
        assert "runtime:claude-code" not in created  # Noop — already complete

    def test_output_dir_preserved(self, tmp_path: Path) -> None:
        init_project(tmp_path)
        output_dir = tmp_path / CONVERSUS_DIR / "output"
        marker = output_dir / "existing_file.txt"
        marker.write_text("keep me", encoding="utf-8")

        # Re-run
        init_project(tmp_path)
        assert marker.is_file()
        assert marker.read_text(encoding="utf-8") == "keep me"


class TestInitProjectForce:
    """init_project with force=True overwrites existing files."""

    def test_settings_overwritten_with_force(self, tmp_path: Path) -> None:
        init_project(tmp_path, default_model="sonnet")
        settings_path = tmp_path / CONVERSUS_DIR / SETTINGS_FILE
        settings_path.write_text('{"custom": true}\n', encoding="utf-8")

        created = init_project(tmp_path, default_model="opus", force=True)
        assert "settings" in created
        data = json.loads(settings_path.read_text(encoding="utf-8"))
        assert data["default_model"] == "opus"

    def test_gitignore_overwritten_with_force(self, tmp_path: Path) -> None:
        init_project(tmp_path)
        gitignore_path = tmp_path / CONVERSUS_DIR / ".gitignore"
        gitignore_path.write_text("custom content\n", encoding="utf-8")

        created = init_project(tmp_path, force=True)
        assert "gitignore" in created
        assert gitignore_path.read_text(encoding="utf-8") == GITIGNORE_CONTENT

    def test_runtime_config_overwritten_with_force(self, tmp_path: Path) -> None:
        init_project(tmp_path, runtimes=["gemini"])
        gemini_path = tmp_path / ".gemini" / "settings.json"
        gemini_path.write_text('{"custom": true}\n', encoding="utf-8")

        created = init_project(tmp_path, runtimes=["gemini"], force=True)
        assert "runtime:gemini" in created
        data = json.loads(gemini_path.read_text(encoding="utf-8"))
        assert data["sandbox"] == "none"  # Original gemini config content


# ===================================================================
# read_settings
# ===================================================================


class TestReadSettings:
    """read_settings reads .conversus/settings.json correctly."""

    def test_returns_defaults_when_file_missing(self, tmp_path: Path) -> None:
        result = read_settings(tmp_path)
        assert result == DEFAULT_SETTINGS
        # Verify it's a copy, not the original
        result["extra_key"] = True
        assert "extra_key" not in DEFAULT_SETTINGS

    def test_returns_defaults_when_dir_missing(self, tmp_path: Path) -> None:
        result = read_settings(tmp_path / "nonexistent")
        assert result == DEFAULT_SETTINGS

    def test_reads_valid_settings(self, tmp_path: Path) -> None:
        init_project(tmp_path, default_provider="opencode", default_model="opus")
        result = read_settings(tmp_path)
        assert result["default_provider"] == "opencode"
        assert result["default_model"] == "opus"

    def test_handles_malformed_json(self, tmp_path: Path) -> None:
        settings_dir = tmp_path / CONVERSUS_DIR
        settings_dir.mkdir()
        settings_path = settings_dir / SETTINGS_FILE
        settings_path.write_text("{not valid json!!!", encoding="utf-8")

        result = read_settings(tmp_path)
        assert result == DEFAULT_SETTINGS

    def test_handles_empty_file(self, tmp_path: Path) -> None:
        settings_dir = tmp_path / CONVERSUS_DIR
        settings_dir.mkdir()
        settings_path = settings_dir / SETTINGS_FILE
        settings_path.write_text("", encoding="utf-8")

        result = read_settings(tmp_path)
        assert result == DEFAULT_SETTINGS

    def test_returns_custom_keys_from_file(self, tmp_path: Path) -> None:
        settings_dir = tmp_path / CONVERSUS_DIR
        settings_dir.mkdir()
        settings_path = settings_dir / SETTINGS_FILE
        custom = {"custom_key": "custom_value", "number": 42}
        settings_path.write_text(json.dumps(custom), encoding="utf-8")

        result = read_settings(tmp_path)
        assert result["custom_key"] == "custom_value"
        assert result["number"] == 42


# ===================================================================
# find_conversus_dir
# ===================================================================


class TestFindConversusDir:
    """find_conversus_dir walks up the directory tree correctly."""

    def test_finds_in_current_dir(self, tmp_path: Path) -> None:
        (tmp_path / CONVERSUS_DIR).mkdir()
        result = find_conversus_dir(tmp_path)
        assert result is not None
        assert result == (tmp_path / CONVERSUS_DIR).resolve()

    def test_finds_in_parent_dir(self, tmp_path: Path) -> None:
        (tmp_path / CONVERSUS_DIR).mkdir()
        child = tmp_path / "subdir" / "deep"
        child.mkdir(parents=True)

        result = find_conversus_dir(child)
        assert result is not None
        assert result == (tmp_path / CONVERSUS_DIR).resolve()

    def test_finds_in_grandparent_dir(self, tmp_path: Path) -> None:
        (tmp_path / CONVERSUS_DIR).mkdir()
        deep = tmp_path / "a" / "b" / "c"
        deep.mkdir(parents=True)

        result = find_conversus_dir(deep)
        assert result is not None
        assert result == (tmp_path / CONVERSUS_DIR).resolve()

    def test_returns_none_when_not_found(self, tmp_path: Path) -> None:
        # No .conversus/ anywhere — tmp_path is isolated so walk will hit root
        result = find_conversus_dir(tmp_path)
        assert result is None

    def test_returns_nearest_conversus_dir(self, tmp_path: Path) -> None:
        """When multiple .conversus/ dirs exist, returns the nearest ancestor."""
        # Outer
        (tmp_path / CONVERSUS_DIR).mkdir()
        # Inner
        inner = tmp_path / "project"
        inner.mkdir()
        (inner / CONVERSUS_DIR).mkdir()

        result = find_conversus_dir(inner)
        assert result is not None
        assert result == (inner / CONVERSUS_DIR).resolve()

    def test_ignores_conversus_file(self, tmp_path: Path) -> None:
        """A file named .conversus (not a dir) should not match."""
        (tmp_path / CONVERSUS_DIR).write_text("not a directory", encoding="utf-8")
        result = find_conversus_dir(tmp_path)
        assert result is None

    def test_resolves_symlinks(self, tmp_path: Path) -> None:
        """start path with symlinks still resolves correctly."""
        real_dir = tmp_path / "real"
        real_dir.mkdir()
        (real_dir / CONVERSUS_DIR).mkdir()

        link_dir = tmp_path / "link"
        link_dir.symlink_to(real_dir)

        result = find_conversus_dir(link_dir)
        assert result is not None
        assert result == (real_dir / CONVERSUS_DIR).resolve()
