"""Tests for ``scripts/lint-test-fixes.py`` (Principle XXVIII enforcement).

The lint script is loaded via :mod:`importlib` because its filename contains a
hyphen and so cannot be imported with a normal ``import`` statement. All tests
operate on string fixtures — no subprocess invocations and no real git.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Iterable, List

import pytest


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "lint-test-fixes.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("lint_test_fixes", SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    # Register before exec_module so @dataclasses.dataclass can resolve
    # forward references via sys.modules lookups.
    sys.modules["lint_test_fixes"] = mod
    spec.loader.exec_module(mod)
    return mod


lint = _load_module()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _diff(*, file_path: str, added: Iterable[str], context_before: Iterable[str] = (), context_after: Iterable[str] = (), removed: Iterable[str] = (), new_file: bool = False, deleted_file: bool = False, new_start: int = 1) -> str:
    """Build a minimal but realistic unified-diff string for a single file."""
    pre_path = "/dev/null" if new_file else f"a/{file_path}"
    post_path = "/dev/null" if deleted_file else f"b/{file_path}"
    parts: List[str] = [f"diff --git a/{file_path} b/{file_path}"]
    if new_file:
        parts.append("new file mode 100644")
    if deleted_file:
        parts.append("deleted file mode 100644")
    parts.append(f"--- {pre_path}")
    parts.append(f"+++ {post_path}")
    old_count = len(list(context_before)) + len(list(removed)) + len(list(context_after))
    new_count = len(list(context_before)) + len(list(added)) + len(list(context_after))
    # Recompute since the generator was exhausted by len() above when iterables
    # were not lists. Force materialization upfront:
    cb = list(context_before)
    ca = list(context_after)
    add = list(added)
    rm = list(removed)
    old_count = len(cb) + len(rm) + len(ca)
    new_count = len(cb) + len(add) + len(ca)
    parts.append(f"@@ -1,{max(old_count,1)} +{new_start},{max(new_count,1)} @@")
    for line in cb:
        parts.append(f" {line}")
    for line in rm:
        parts.append(f"-{line}")
    for line in add:
        parts.append(f"+{line}")
    for line in ca:
        parts.append(f" {line}")
    return "\n".join(parts) + "\n"


def _multi_diff(*chunks: str) -> str:
    return "".join(chunks)


# ---------------------------------------------------------------------------
# Clause 1 — skip discipline
# ---------------------------------------------------------------------------


def test_skip_with_citation_and_timeline_passes():
    diff = _diff(
        file_path="pkg/tests/test_foo.py",
        context_before=[
            "def test_thing():",
            "    # Tracked in issue #123, fix scheduled by 2026-06-01",
        ],
        added=[
            "    pytest.skip('flaky on CI, see #123')",
        ],
        context_after=["    assert True"],
    )
    findings = lint.run(diff, pr_body="<!-- test-fix-category: legitimate-test-bug -->\nFixes #123")
    skip_findings = [f for f in findings if f.rule.startswith("skip-")]
    assert skip_findings == [], skip_findings


def test_skip_without_any_citation_is_flagged():
    diff = _diff(
        file_path="pkg/tests/test_foo.py",
        context_before=["def test_thing():"],
        added=["    pytest.skip('not ready')"],
        context_after=["    assert True"],
    )
    findings = lint.run(diff, pr_body="<!-- test-fix-category: legitimate-test-bug --> #123")
    skip_findings = [f for f in findings if f.rule.startswith("skip-")]
    assert len(skip_findings) == 1
    assert skip_findings[0].path == "pkg/tests/test_foo.py"
    assert skip_findings[0].line >= 1
    assert skip_findings[0].rule == "skip-without-citation"


def test_skip_with_citation_but_no_timeline_is_flagged():
    diff = _diff(
        file_path="pkg/tests/test_foo.py",
        context_before=[
            "def test_thing():",
            "    # See issue #456 for details",
        ],
        added=["    pytest.skip('see issue #456')"],
        context_after=["    assert True"],
    )
    findings = lint.run(diff, pr_body="<!-- test-fix-category: legitimate-test-bug --> #456")
    skip_findings = [f for f in findings if f.rule.startswith("skip-")]
    assert len(skip_findings) == 1
    assert skip_findings[0].rule == "skip-without-timeline"


def test_skip_decorator_form_with_valid_context_passes():
    diff = _diff(
        file_path="pkg/tests/test_decorated.py",
        context_before=[
            "# TODO(alice): re-enable before next release; tracking PR 99",
        ],
        added=[
            "@pytest.mark.skip(reason='waiting on PR 99')",
            "def test_decorated():",
        ],
        context_after=["    assert False"],
    )
    findings = lint.run(diff, pr_body="<!-- test-fix-category: legitimate-test-bug --> PR 99")
    skip_findings = [f for f in findings if f.rule.startswith("skip-")]
    assert skip_findings == []


# ---------------------------------------------------------------------------
# Clause 2 — diff-shape consistency
# ---------------------------------------------------------------------------


def test_fixture_drift_with_only_test_files_passes():
    diff = _diff(
        file_path="pkg/tests/test_thing.py",
        added=["def test_new(): assert True"],
    )
    pr_body = "<!-- test-fix-category: fixture-drift -->\nFixture realignment after schema bump."
    findings = lint.run(diff, pr_body)
    cat = [f for f in findings if f.rule.startswith("category-")]
    assert cat == []


def test_fixture_drift_with_production_change_is_flagged():
    diff = _multi_diff(
        _diff(file_path="pkg/tests/test_thing.py", added=["def test_x(): assert True"]),
        _diff(file_path="pkg/core/service.py", added=["def helper(): return 1"]),
    )
    pr_body = "<!-- test-fix-category: fixture-drift -->"
    findings = lint.run(diff, pr_body)
    cat = [f for f in findings if f.rule == "category-mismatch-fixture-drift"]
    assert len(cat) == 1
    assert "pkg/core/service.py" in cat[0].message


def test_production_bug_without_production_change_is_flagged():
    diff = _diff(
        file_path="pkg/tests/test_thing.py",
        added=["def test_y(): assert True"],
    )
    pr_body = "<!-- test-fix-category: production-bug -->\nFixes underlying behaviour."
    findings = lint.run(diff, pr_body)
    cat = [f for f in findings if f.rule == "category-mismatch-production-bug"]
    assert len(cat) == 1


def test_defunct_test_without_deletion_is_flagged():
    diff = _diff(
        file_path="pkg/tests/test_old.py",
        added=["def test_modified(): assert True"],
    )
    pr_body = "<!-- test-fix-category: defunct-test -->"
    findings = lint.run(diff, pr_body)
    cat = [f for f in findings if f.rule == "category-mismatch-defunct-test"]
    assert len(cat) == 1


def test_defunct_test_with_deletion_passes():
    diff = (
        "diff --git a/pkg/tests/test_old.py b/pkg/tests/test_old.py\n"
        "deleted file mode 100644\n"
        "--- a/pkg/tests/test_old.py\n"
        "+++ /dev/null\n"
        "@@ -1,3 +0,0 @@\n"
        "-def test_old():\n"
        "-    assert True\n"
        "-\n"
    )
    pr_body = "<!-- test-fix-category: defunct-test -->\nThis test guarded a removed feature."
    findings = lint.run(diff, pr_body)
    cat = [f for f in findings if f.rule.startswith("category-")]
    assert cat == []


def test_legitimate_test_bug_without_pr_body_citation_is_flagged():
    diff = _diff(
        file_path="pkg/tests/test_thing.py",
        added=["def test_new(): assert True"],
    )
    pr_body = "<!-- test-fix-category: legitimate-test-bug -->\nMinor fix to assertion."
    findings = lint.run(diff, pr_body)
    rules = {f.rule for f in findings}
    assert "legitimate-test-bug-missing-citation" in rules


def test_legitimate_test_bug_with_production_change_is_flagged():
    diff = _multi_diff(
        _diff(file_path="pkg/tests/test_thing.py", added=["def test_x(): assert True"]),
        _diff(file_path="pkg/core/util.py", added=["def fn(): return 1"]),
    )
    pr_body = "<!-- test-fix-category: legitimate-test-bug -->\nFixes #321"
    findings = lint.run(diff, pr_body)
    rules = {f.rule for f in findings}
    assert "category-mismatch-legitimate-test-bug" in rules


def test_multiple_consistent_markers_pass():
    diff = _multi_diff(
        _diff(file_path="pkg/tests/test_a.py", added=["def test_a(): pass"]),
        _diff(file_path="pkg/core/x.py", added=["def x(): return 1"]),
    )
    pr_body = (
        "<!-- test-fix-category: production-bug -->\n"
        "<!-- test-fix-category: fixture-drift -->\n"
    )
    # production-bug holds (production paths exist) but fixture-drift does NOT
    # (production paths exist). Per spec, every individual claim must hold —
    # so this should flag the fixture-drift mismatch.
    findings = lint.run(diff, pr_body)
    rules = {f.rule for f in findings}
    assert "category-mismatch-fixture-drift" in rules
    assert "category-mismatch-production-bug" not in rules


def test_no_marker_with_test_modifications_emits_info():
    diff = _diff(
        file_path="pkg/tests/test_unmarked.py",
        added=["def test_unmarked(): assert True"],
    )
    findings = lint.run(diff, pr_body="No marker here.")
    info = [f for f in findings if f.rule == "missing-category-marker"]
    assert len(info) == 1
    assert info[0].level == "info"


def test_no_marker_without_test_changes_emits_nothing():
    diff = _diff(file_path="pkg/core/x.py", added=["def x(): return 1"])
    findings = lint.run(diff, pr_body="No marker, no tests.")
    assert findings == []


# ---------------------------------------------------------------------------
# CLI / formatting / exit codes
# ---------------------------------------------------------------------------


def test_main_exit_code_zero_when_clean(tmp_path):
    diff_path = tmp_path / "p.diff"
    body_path = tmp_path / "body.md"
    diff_path.write_text(
        _diff(file_path="pkg/core/x.py", added=["def x(): return 1"]),
        encoding="utf-8",
    )
    body_path.write_text("No marker, no tests.", encoding="utf-8")
    rc = lint.main(["--diff", str(diff_path), "--pr-body", str(body_path), "--format", "json"])
    assert rc == 0


def test_main_exit_code_one_when_warnings_present(tmp_path):
    diff_path = tmp_path / "p.diff"
    body_path = tmp_path / "body.md"
    diff_path.write_text(
        _diff(file_path="pkg/tests/test_thing.py", added=["    pytest.skip('nope')"], context_before=["def test():"]),
        encoding="utf-8",
    )
    body_path.write_text("<!-- test-fix-category: legitimate-test-bug --> #1", encoding="utf-8")
    rc = lint.main(["--diff", str(diff_path), "--pr-body", str(body_path), "--format", "json"])
    assert rc == 1


def test_main_exit_code_zero_for_info_only_findings(tmp_path):
    diff_path = tmp_path / "p.diff"
    body_path = tmp_path / "body.md"
    diff_path.write_text(
        _diff(file_path="pkg/tests/test_thing.py", added=["def test_x(): assert True"]),
        encoding="utf-8",
    )
    body_path.write_text("No marker.", encoding="utf-8")
    rc = lint.main(["--diff", str(diff_path), "--pr-body", str(body_path), "--format", "json"])
    # Info-level finding should not flip exit code.
    assert rc == 0


def test_main_exit_code_two_on_missing_diff(tmp_path):
    body_path = tmp_path / "body.md"
    body_path.write_text("body", encoding="utf-8")
    rc = lint.main(["--diff", str(tmp_path / "missing.diff"), "--pr-body", str(body_path)])
    assert rc == 2


def test_github_format_emits_annotation(tmp_path):
    diff = _diff(
        file_path="pkg/tests/test_thing.py",
        context_before=["def test():"],
        added=["    pytest.skip('nope')"],
    )
    findings = lint.run(diff, pr_body="<!-- test-fix-category: legitimate-test-bug --> #1")
    out = lint.format_findings(findings, "github")
    assert "::warning" in out
    assert "file=pkg/tests/test_thing.py" in out


def test_json_format_is_valid_json():
    diff = _diff(file_path="pkg/tests/test_thing.py", added=["def t(): pass"])
    findings = lint.run(diff, pr_body="No marker.")
    out = lint.format_findings(findings, "json")
    parsed = json.loads(out)
    assert isinstance(parsed, list)
    assert parsed and parsed[0]["rule"] == "missing-category-marker"


# ---------------------------------------------------------------------------
# Path classification edge cases
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "path,expected",
    [
        ("pkg/tests/test_a.py", True),
        ("pkg/test_a.py", True),
        ("pkg/a_test.py", True),
        ("pkg/core/service.py", False),
        ("docs/index.md", False),
        ("README.md", False),
        ("", False),
    ],
)
def test_is_test_path(path, expected):
    assert lint.is_test_path(path) is expected


@pytest.mark.parametrize(
    "path,expected",
    [
        ("pkg/core/service.py", True),
        ("pkg/tests/test_a.py", False),
        ("docs/intro.py", False),
        ("specs/071.py", False),
        (".github/workflows/ci.yml", False),
        ("scripts/tests/test_lint.py", False),
        ("scripts/build.py", True),
    ],
)
def test_is_production_path(path, expected):
    assert lint.is_production_path(path) is expected


def test_extract_categories_filters_unknown_values():
    body = (
        "<!-- test-fix-category: production-bug -->\n"
        "<!-- test-fix-category: bogus-value -->\n"
        "<!-- test-fix-category: defunct-test -->"
    )
    cats = lint.extract_categories(body)
    assert cats == ["production-bug", "defunct-test"]
