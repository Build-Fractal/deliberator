"""Tests for dev-setup.sh logic.

Validates binary detection and summary output formatting by running the
script in --check-only mode with controlled PATH.  No actual installs
are performed.
"""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DEV_SETUP_SH = PROJECT_ROOT / "scripts" / "dev-setup.sh"

# All tool binaries the script checks for.
ALL_TOOLS = [
    "python",
    "conversus",
    "claude",
    "aider",
    "opencode",
    "ollama",
    "codex",
    "gemini",
    "gh",
    "llama-server",
    "vllm",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _run_dev_setup(
    *extra_args: str,
    env_override: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run dev-setup.sh --check-only and return the result.

    Always passes ``--check-only`` so nothing is installed.
    """
    cmd = ["bash", str(DEV_SETUP_SH), "--check-only", *extra_args]
    env = {**os.environ, **(env_override or {})}
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=30,
        env=env,
    )


def _strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences for easier assertion."""
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


# ---------------------------------------------------------------------------
# Tests — script basics
# ---------------------------------------------------------------------------


class TestScriptBasics:
    """Verify the script exists, is executable, and runs without errors."""

    def test_script_exists(self) -> None:
        assert DEV_SETUP_SH.exists(), f"dev-setup.sh not found at {DEV_SETUP_SH}"

    def test_script_is_executable(self) -> None:
        assert os.access(DEV_SETUP_SH, os.X_OK), "dev-setup.sh is not executable"

    def test_help_flag(self) -> None:
        result = subprocess.run(
            ["bash", str(DEV_SETUP_SH), "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0
        assert "--check-only" in result.stdout
        assert "--skip" in result.stdout

    def test_check_only_does_not_fail(self) -> None:
        """--check-only should exit 0 regardless of what's installed."""
        result = _run_dev_setup()
        # The script uses set -uo pipefail but no set -e, so it should
        # always exit 0 even when tools are missing.
        assert result.returncode == 0, (
            f"dev-setup.sh --check-only failed:\n{result.stderr}"
        )


# ---------------------------------------------------------------------------
# Tests — binary detection
# ---------------------------------------------------------------------------


class TestBinaryDetection:
    """Verify the script correctly detects installed/missing tools."""

    def test_python_detected_when_present(self) -> None:
        """Python is on the dev machine, so it should show as installed."""
        result = _run_dev_setup()
        output = _strip_ansi(result.stdout)
        # The summary table should show python as installed.
        assert re.search(r"python\s+installed", output, re.IGNORECASE), (
            f"Expected python to be detected as installed.\nOutput:\n{output}"
        )

    def test_missing_tool_shown_as_missing(self) -> None:
        """When PATH is restricted, most tools should show as missing."""
        # Create a minimal PATH with only essential system tools + python.
        # This avoids installing anything but still lets the script run.
        minimal_path = "/usr/bin:/bin"
        result = _run_dev_setup(env_override={"PATH": minimal_path})
        output = _strip_ansi(result.stdout)
        # claude is unlikely to be in /usr/bin, so it should be missing.
        assert re.search(r"claude\s+missing", output, re.IGNORECASE), (
            f"Expected claude to show as missing with minimal PATH.\nOutput:\n{output}"
        )

    def test_skip_flag_marks_skipped(self) -> None:
        """--skip should cause the tool to show as skipped, not missing."""
        result = _run_dev_setup("--skip", "ollama,vllm")
        output = _strip_ansi(result.stdout)
        assert re.search(r"ollama\s+skipped", output, re.IGNORECASE), (
            f"Expected ollama to be skipped.\nOutput:\n{output}"
        )

    def test_skip_multiple_tools(self) -> None:
        """Multiple tools in --skip should all be skipped."""
        result = _run_dev_setup("--skip", "claude,aider,codex")
        output = _strip_ansi(result.stdout)
        for tool in ["claude", "aider", "codex"]:
            assert re.search(rf"{tool}\s+skipped", output, re.IGNORECASE), (
                f"Expected {tool} to be skipped.\nOutput:\n{output}"
            )

    def test_vllm_shows_info_status(self) -> None:
        """vLLM should show as 'info' (GPU-only, never auto-installed)."""
        result = _run_dev_setup()
        output = _strip_ansi(result.stdout)
        # vLLM should show info or installed, never attempted install.
        assert re.search(r"vllm\s+(info|installed)", output, re.IGNORECASE), (
            f"Expected vllm to show info or installed status.\nOutput:\n{output}"
        )


# ---------------------------------------------------------------------------
# Tests — summary output formatting
# ---------------------------------------------------------------------------


class TestSummaryOutput:
    """Verify the summary table is well-formed."""

    def test_summary_header_present(self) -> None:
        result = _run_dev_setup()
        output = _strip_ansi(result.stdout)
        assert "Tool" in output
        assert "Status" in output
        assert "Details" in output

    def test_summary_line_present(self) -> None:
        """The separator line of dashes should be present."""
        result = _run_dev_setup()
        output = _strip_ansi(result.stdout)
        assert "----" in output

    def test_summary_count(self) -> None:
        """The 'Summary: X/Y installed' line should be present."""
        result = _run_dev_setup()
        output = _strip_ansi(result.stdout)
        assert re.search(r"Summary:\s+\d+/\d+\s+installed", output), (
            f"Expected summary count line.\nOutput:\n{output}"
        )

    def test_all_tools_in_summary(self) -> None:
        """Every tracked tool should appear in the summary table."""
        result = _run_dev_setup()
        output = _strip_ansi(result.stdout)
        for tool in ALL_TOOLS:
            assert tool in output, (
                f"Expected '{tool}' in summary output.\nOutput:\n{output}"
            )

    def test_title_present(self) -> None:
        result = _run_dev_setup()
        output = _strip_ansi(result.stdout)
        assert "conversus dev-setup" in output

    def test_check_only_indicator(self) -> None:
        result = _run_dev_setup()
        output = _strip_ansi(result.stdout)
        assert "check-only" in output.lower()

    def test_skip_reflected_in_summary_count(self) -> None:
        """When tools are skipped, the summary should mention 'skipped'."""
        result = _run_dev_setup("--skip", "ollama,codex")
        output = _strip_ansi(result.stdout)
        assert "skipped" in output.lower(), (
            f"Expected 'skipped' in summary.\nOutput:\n{output}"
        )


# ---------------------------------------------------------------------------
# Tests — idempotency (conceptual)
# ---------------------------------------------------------------------------


class TestIdempotency:
    """Running check-only twice should produce the same output."""

    def test_consistent_output(self) -> None:
        result1 = _run_dev_setup()
        result2 = _run_dev_setup()
        out1 = _strip_ansi(result1.stdout)
        out2 = _strip_ansi(result2.stdout)
        assert out1 == out2, "Two consecutive --check-only runs produced different output"
