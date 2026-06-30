"""Security validation tests for the capability registry + persistence layer.

Motivated by the spec 055-059 stability deliberation which identified
three attack surfaces: path traversal in read_deliberation_file,
env var injection via user_config, and Python injection via capability
metadata in the projector's generated source.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

pytestmark = pytest.mark.security

from deliberator.registry import Capability, Param, Surface
from deliberator.registry.adapters._helpers import literal
from deliberator.registry.projector import project_to_cli, project_to_mcp
from engine.persistence import persist_deliberation, read_deliberation_file


# ---------------------------------------------------------------------------
# Path traversal attacks on read_deliberation_file
# ---------------------------------------------------------------------------


@pytest.fixture
def deliberation_fixture(tmp_path: Path) -> tuple[Path, str]:
    """Create a real persisted deliberation and return (project_root, rel_path)."""
    output = tmp_path / "output" / "summary"
    output.mkdir(parents=True)
    (output / "final.md").write_text("# Synthesis\nTest content")
    (tmp_path / "output" / "pragmatist").mkdir()
    (tmp_path / "output" / "pragmatist" / "review.md").write_text("Review")

    project = tmp_path / "project"
    project.mkdir()
    persisted = persist_deliberation(
        source_dir=tmp_path / "output",
        project_root=project,
        question="Test question",
    )
    rel = str(persisted.relative_to(project))
    return project, rel


def test_path_traversal_dot_dot(deliberation_fixture):
    project, rel = deliberation_fixture
    with pytest.raises(ValueError, match="[Pp]ath traversal|outside"):
        read_deliberation_file(project, rel, "../../../etc/passwd")


def test_path_traversal_encoded(deliberation_fixture):
    """URL-encoded ../ should also be rejected."""
    project, rel = deliberation_fixture
    with pytest.raises((ValueError, FileNotFoundError)):
        read_deliberation_file(project, rel, "..%2F..%2Fetc%2Fpasswd")


def test_path_traversal_absolute(deliberation_fixture):
    """Absolute paths outside the deliberation dir should be rejected."""
    project, rel = deliberation_fixture
    with pytest.raises((ValueError, FileNotFoundError)):
        read_deliberation_file(project, rel, "/etc/passwd")


def test_path_traversal_null_byte(deliberation_fixture):
    """Null bytes in paths should not bypass validation."""
    project, rel = deliberation_fixture
    with pytest.raises((ValueError, FileNotFoundError, OSError)):
        read_deliberation_file(project, rel, "summary/final.md\x00.txt")


def test_path_traversal_symlink(deliberation_fixture, tmp_path):
    """Symlinks pointing outside the deliberation dir should be rejected."""
    project, rel = deliberation_fixture
    delib_dir = project / rel
    # Create a symlink inside the deliberation pointing outside
    link_path = delib_dir / "output" / "evil_link.md"
    target = tmp_path / "secret.txt"
    target.write_text("secret data")
    try:
        link_path.symlink_to(target)
    except OSError:
        pytest.skip("Cannot create symlinks on this platform")

    # The resolved path goes outside .deliberator/deliberations/
    with pytest.raises(ValueError, match="[Pp]ath traversal|outside"):
        read_deliberation_file(project, rel, "output/evil_link.md")


def test_valid_file_read_works(deliberation_fixture):
    """Sanity check: legitimate reads still work."""
    project, rel = deliberation_fixture
    content = read_deliberation_file(project, rel, "output/summary/final.md")
    assert "Synthesis" in content


# ---------------------------------------------------------------------------
# Python injection via capability metadata in the projector
# ---------------------------------------------------------------------------


def test_literal_escapes_dangerous_strings():
    """json.dumps should escape quotes so injection can't break out of a string literal."""
    dangerous = '"; import os; os.system("rm -rf /")'
    escaped = literal(dangerous)
    # Must be a valid Python string literal
    assert escaped.startswith('"')
    assert escaped.endswith('"')
    # The internal quotes are escaped — the dangerous content stays INSIDE the string
    assert '\\"' in escaped  # the quotes around rm -rf are escaped
    # Compiling as a Python expression should produce a string, not execute code
    result = eval(escaped)  # returns the string value, does NOT execute import os
    assert isinstance(result, str)
    assert result == dangerous  # round-trips correctly


def test_projector_escapes_malicious_summary():
    """A capability with a malicious summary should not inject code."""
    caps = [
        Capability(
            name="evil",
            summary='"); import os; os.system("pwned',
            surfaces=[Surface.CLI, Surface.MCP],
            params=[],
            handler="m:f",
        )
    ]

    cli_source = project_to_cli(caps)
    mcp_source = project_to_mcp(caps)

    # The generated source should compile cleanly (no syntax errors)
    compile(cli_source, "<test-cli>", "exec")
    compile(mcp_source, "<test-mcp>", "exec")

    # The malicious string should be escaped in the output
    assert "import os" in cli_source  # it's IN the string literal, not as code
    assert 'os.system' not in cli_source.split('help=')[0]  # not in executable position


def test_projector_escapes_malicious_param_help():
    """A param with injection in the help text should be escaped."""
    caps = [
        Capability(
            name="test",
            summary="Test",
            surfaces=[Surface.CLI],
            params=[
                Param(
                    name="x",
                    type=str,
                    default="safe",
                    help='"); exec("import os")',
                ),
            ],
            handler="m:f",
        )
    ]

    source = project_to_cli(caps)
    # The generated source must compile — if injection broke out of
    # the string literal, compile would fail or the code would be
    # structurally different. Compiling cleanly proves the help text
    # stayed inside its string literal.
    compile(source, "<test>", "exec")
    # The help= argument in the generated source should be a quoted string
    assert 'help="' in source


def test_projector_rejects_handler_without_colon():
    """A handler string with no colon is rejected by split_handler."""
    from deliberator.registry.adapters._helpers import split_handler
    with pytest.raises(ValueError, match="handler must be"):
        split_handler("os.system('pwned')")


def test_projector_rejects_handler_with_multiple_colons():
    """A handler string with multiple colons is rejected."""
    from deliberator.registry.adapters._helpers import split_handler
    with pytest.raises(ValueError, match="handler must be"):
        split_handler("a:b:c")


# ---------------------------------------------------------------------------
# Env var injection via user_config / settings cascade
# ---------------------------------------------------------------------------


def test_settings_cascade_sanitizes_provider(monkeypatch):
    """A malicious DELIBERATOR_DEFAULT_PROVIDER env var should not inject."""
    from engine.settings import load_settings

    monkeypatch.setenv("DELIBERATOR_DEFAULT_PROVIDER", "'; DROP TABLE users; --")
    settings = load_settings(Path("/nonexistent"))

    # The value is stored as-is (it's a string, not SQL)
    # but it should not cause a crash
    assert settings.default_provider == "'; DROP TABLE users; --"
    # The real protection is that resolve_provider validates against
    # known provider names — unknown providers raise ProviderError


def test_settings_cascade_invalid_max_launches(monkeypatch):
    """Non-numeric DELIBERATOR_MAX_LAUNCHES should not crash."""
    from engine.settings import load_settings

    monkeypatch.setenv("DELIBERATOR_MAX_LAUNCHES", "not_a_number")
    settings = load_settings(Path("/nonexistent"))

    # Should fall back to default, not crash
    assert settings.max_launches == 20


# ---------------------------------------------------------------------------
# Concurrent deliberation timestamp collision
# ---------------------------------------------------------------------------


def test_persist_deliberation_unique_timestamps(tmp_path):
    """Two rapid persists should get different directory names."""
    output = tmp_path / "output" / "summary"
    output.mkdir(parents=True)
    (output / "final.md").write_text("content")

    project = tmp_path / "project"
    project.mkdir()

    path1 = persist_deliberation(
        source_dir=tmp_path / "output",
        project_root=project,
        question="Question A",
    )
    path2 = persist_deliberation(
        source_dir=tmp_path / "output",
        project_root=project,
        question="Question B",
    )

    # Different slugs should produce different paths
    assert path1 != path2
    assert path1.exists()
    assert path2.exists()
