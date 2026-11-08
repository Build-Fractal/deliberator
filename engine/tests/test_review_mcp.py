"""The MCP review surface: review_mcp runs the protocol and returns review.json as a dict."""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("lattice_graph")

from engine.handlers import review_mcp
from engine.review.service import ReviewInputError, load_targets, parse_reviewers


@pytest.fixture
def project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setenv("DELIBERATOR_ROOT", str(tmp_path))
    return tmp_path


async def test_inline_text_with_mock_provider(project: Path) -> None:
    result = await review_mcp(text="Step 1: drop the users table.", provider="mock")
    assert "error" not in result
    assert result["verdict"] in {"pass", "changes", "block"}
    assert result["exit_code"] in {0, 1, 2}
    run_dir = Path(result["run_dir"])
    assert run_dir.is_relative_to(project / ".deliberator" / "reviews")
    assert (run_dir / "review.json").is_file()
    assert (run_dir / "moves.jsonl").is_file()


async def test_relative_paths_resolve_against_project_root(project: Path) -> None:
    (project / "plan.md").write_text("Step 1: ship it.\n")
    result = await review_mcp(paths=["plan.md"], provider="mock", out_dir=str(project / "out"))
    assert "error" not in result
    assert Path(result["run_dir"]).parent == project / "out"


async def test_rejects_unknown_provider(project: Path) -> None:
    result = await review_mcp(text="x", provider="aider")
    assert "Unknown provider" in result["error"]


async def test_reports_input_errors(project: Path) -> None:
    assert "nothing to review" in (await review_mcp(provider="mock"))["error"]
    assert "not a file" in (await review_mcp(paths=["missing.md"], provider="mock"))["error"]
    bad = await review_mcp(text="x", provider="mock", reviewers=["no-lens"])
    assert "name:lens" in bad["error"]


def test_stdin_only_on_the_command_line() -> None:
    with pytest.raises(ReviewInputError):
        load_targets(["-"])


def test_parse_reviewers() -> None:
    assert parse_reviewers(None) is None
    [r] = parse_reviewers(["sec: injection, secrets "])
    assert (r.name, r.lens) == ("sec", "injection, secrets")
