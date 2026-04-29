#!/usr/bin/env python3
"""Principle XXVIII enforcement lint — Test-Fix Boundary Preservation (v2.5.0).

Reads a unified-diff file and a PR-body markdown file and verifies two clauses:

Clause 1 — Skip discipline
    Newly added pytest skip directives (``pytest.skip(...)``, ``@pytest.skip``,
    ``@pytest.mark.skip``) inside test files must be accompanied by both a
    citation (issue/PR/TODO) and a remediation timeline cue within ±5 lines of
    the same diff hunk.

Clause 2 — Diff-shape consistency
    The PR body declares one or more category markers via the HTML comment
    ``<!-- test-fix-category: VALUE -->`` where VALUE is one of
    ``fixture-drift``, ``production-bug``, ``legitimate-test-bug``, or
    ``defunct-test``. The actual diff shape (test paths modified, production
    paths modified, test files deleted) must be consistent with each declared
    category. If multiple markers are present, every individual claim must hold.

Output formats: ``github`` (default — emits ``::warning`` annotations),
``text`` (human-readable), ``json`` (list of finding dicts).

Exit codes: ``0`` no findings, ``1`` findings present, ``2`` usage error.

Per spec 071 §6 (v2). The script is stdlib-only and runs as ADVISORY in CI
(``continue-on-error: true``) until the false-positive rate stabilizes.
"""

from __future__ import annotations

import argparse
import dataclasses
import fnmatch
import json
import re
import sys
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_CATEGORIES = frozenset(
    {"fixture-drift", "production-bug", "legitimate-test-bug", "defunct-test"}
)

CATEGORY_MARKER_RE = re.compile(
    r"<!--\s*test-fix-category:\s*([a-z\-]+)\s*-->", re.IGNORECASE
)

SKIP_PATTERNS = (
    re.compile(r"\bpytest\.skip\s*\("),
    re.compile(r"@pytest\.skip\b"),
    re.compile(r"@pytest\.mark\.skip\b"),
)

CITATION_RE = re.compile(r"(issue|PR|#\d+|TODO\([^)]+\))", re.IGNORECASE)

# Timeline cues — any of these in the adjacent context satisfies the timeline
# requirement.
TIMELINE_RES: Tuple[re.Pattern[str], ...] = (
    re.compile(r"by\s+\d{4}-\d{2}-\d{2}", re.IGNORECASE),
    re.compile(r"before\s+next\s+release", re.IGNORECASE),
    re.compile(r"next\s+release", re.IGNORECASE),
    re.compile(r"before\s+merge", re.IGNORECASE),
    re.compile(r"by\s+[A-Z][a-z]+\s+\d", re.IGNORECASE),
)

# PR-body issue / PR citation regex — case-insensitive.
PR_BODY_CITATION_RE = re.compile(r"#\d+|issue\s+\d+|PR\s+\d+", re.IGNORECASE)

# Test path globs.
TEST_GLOBS = ("**/test_*.py", "**/*_test.py", "**/tests/**/*.py")

# Production-path exclusions: paths under these prefixes don't count as
# production code for the purpose of clause 2.
PRODUCTION_EXCLUDE_PREFIXES = (
    "docs/",
    "specs/",
    "deliberations/",
    ".github/",
    "scripts/tests/",
)

CONTEXT_WINDOW = 5  # lines on each side of a skip directive

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class Finding:
    """A single lint finding.

    Attributes:
        path: Repository-relative file path the finding applies to. May be the
            empty string for repo-wide findings.
        line: 1-indexed line number in ``path`` (post-image), or ``0`` when not
            applicable.
        level: ``warning`` or ``info``.
        rule: Short rule identifier (e.g. ``skip-without-citation``).
        message: Human-readable explanation.
    """

    path: str
    line: int
    level: str
    rule: str
    message: str

    def to_dict(self) -> dict:
        return dataclasses.asdict(self)


@dataclasses.dataclass
class Hunk:
    """A single diff hunk.

    ``lines`` preserves the raw diff lines (with leading ``+``, ``-``, or `` ``).
    ``new_start`` is the 1-indexed starting line in the post-image.
    """

    file_path: str
    new_start: int
    lines: List[str]

    def added_lines(self) -> List[Tuple[int, str]]:
        """Return ``(post_image_lineno, content)`` for each ``+`` line."""
        out: List[Tuple[int, str]] = []
        lineno = self.new_start
        for raw in self.lines:
            if raw.startswith("+++"):
                continue
            if raw.startswith("+"):
                out.append((lineno, raw[1:]))
                lineno += 1
            elif raw.startswith("-"):
                continue
            else:
                # Context line; advance lineno.
                lineno += 1
        return out

    def context_lines(self) -> List[str]:
        """Return all hunk content (added + context) without the diff prefix."""
        out: List[str] = []
        for raw in self.lines:
            if raw.startswith("+++") or raw.startswith("---"):
                continue
            if raw.startswith("+") or raw.startswith("-") or raw.startswith(" "):
                out.append(raw[1:])
            else:
                out.append(raw)
        return out


@dataclasses.dataclass
class FileDiff:
    """Aggregate diff information for a single file."""

    path: str
    hunks: List[Hunk] = dataclasses.field(default_factory=list)
    is_deletion: bool = False
    added_count: int = 0
    removed_count: int = 0


# ---------------------------------------------------------------------------
# Diff parsing
# ---------------------------------------------------------------------------

_HUNK_HEADER_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")


def parse_diff(diff_text: str) -> List[FileDiff]:
    """Parse a unified diff into a list of :class:`FileDiff` objects.

    The parser handles standard ``git diff`` output. It tolerates ``new file``
    and ``deleted file`` markers and binary-file stanzas (which are ignored
    from a lint standpoint).
    """

    files: List[FileDiff] = []
    current: Optional[FileDiff] = None
    current_hunk: Optional[Hunk] = None
    pending_deletion = False

    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            # Flush previous file/hunk.
            if current_hunk is not None and current is not None:
                current.hunks.append(current_hunk)
                current_hunk = None
            if current is not None:
                files.append(current)
            current = None
            pending_deletion = False
            continue

        if raw.startswith("deleted file mode"):
            pending_deletion = True
            continue

        if raw.startswith("--- ") or raw.startswith("+++ "):
            # Use the +++ line to derive the post-image path; if the file is
            # being deleted, fall back to the --- path.
            if raw.startswith("+++ "):
                path = _strip_diff_path(raw[4:])
                if path == "/dev/null":
                    # Deletion — wait for the --- path.
                    if current is None:
                        current = FileDiff(path="", is_deletion=True)
                    else:
                        current.is_deletion = True
                else:
                    if current is None:
                        current = FileDiff(path=path)
                    else:
                        current.path = path
            elif raw.startswith("--- "):
                path = _strip_diff_path(raw[4:])
                if path != "/dev/null" and (current is None or not current.path):
                    if current is None:
                        current = FileDiff(path=path)
                    else:
                        current.path = path
                if pending_deletion and current is not None:
                    current.is_deletion = True
                    if path != "/dev/null":
                        current.path = path
            continue

        if raw.startswith("@@"):
            if current is None:
                # Defensive: a hunk without a file header — ignore.
                continue
            if current_hunk is not None:
                current.hunks.append(current_hunk)
            match = _HUNK_HEADER_RE.match(raw)
            new_start = int(match.group(1)) if match else 1
            current_hunk = Hunk(
                file_path=current.path, new_start=new_start, lines=[]
            )
            continue

        if current_hunk is not None:
            current_hunk.lines.append(raw)
            if raw.startswith("+") and not raw.startswith("+++"):
                if current is not None:
                    current.added_count += 1
            elif raw.startswith("-") and not raw.startswith("---"):
                if current is not None:
                    current.removed_count += 1

    if current_hunk is not None and current is not None:
        current.hunks.append(current_hunk)
    if current is not None:
        files.append(current)

    # Refresh hunk paths now that file paths are settled.
    for f in files:
        for h in f.hunks:
            h.file_path = f.path

    return files


def _strip_diff_path(s: str) -> str:
    """Strip git's ``a/`` or ``b/`` prefix and trailing whitespace from a diff path."""
    s = s.strip()
    # Remove timestamp suffix if present (separated by tab).
    if "\t" in s:
        s = s.split("\t", 1)[0]
    if s.startswith("a/") or s.startswith("b/"):
        s = s[2:]
    return s


# ---------------------------------------------------------------------------
# Path classification
# ---------------------------------------------------------------------------


def is_test_path(path: str) -> bool:
    """Return ``True`` if ``path`` looks like a test file."""
    if not path or not path.endswith(".py"):
        return False
    return any(fnmatch.fnmatch(path, glob) for glob in TEST_GLOBS)


def is_production_path(path: str) -> bool:
    """Return ``True`` if ``path`` should be treated as production code."""
    if not path or not path.endswith(".py"):
        return False
    if is_test_path(path):
        return False
    for prefix in PRODUCTION_EXCLUDE_PREFIXES:
        if path.startswith(prefix):
            return False
    return True


# ---------------------------------------------------------------------------
# Clause 1 — Skip discipline
# ---------------------------------------------------------------------------


def find_skip_violations(files: Sequence[FileDiff]) -> List[Finding]:
    findings: List[Finding] = []
    for f in files:
        if not is_test_path(f.path):
            continue
        for hunk in f.hunks:
            added = hunk.added_lines()
            context = hunk.context_lines()
            for lineno, content in added:
                if not _line_has_skip(content):
                    continue
                # Build the ±CONTEXT_WINDOW window around this added line. We
                # use indices within the hunk's context list — find the
                # context-line index of this added line.
                idx = _index_in_context(hunk, lineno)
                if idx is None:
                    window = context
                else:
                    lo = max(0, idx - CONTEXT_WINDOW)
                    hi = min(len(context), idx + CONTEXT_WINDOW + 1)
                    window = context[lo:hi]
                window_text = "\n".join(window)
                has_citation = bool(CITATION_RE.search(window_text))
                has_timeline = any(rx.search(window_text) for rx in TIMELINE_RES)
                if has_citation and has_timeline:
                    continue
                if not has_citation and not has_timeline:
                    msg = (
                        "Newly added pytest skip lacks both an issue/PR/TODO "
                        "citation and a remediation timeline cue (Principle "
                        "XXVIII clause 1)."
                    )
                    rule = "skip-without-citation"
                elif not has_citation:
                    msg = (
                        "Newly added pytest skip lacks an issue/PR/TODO "
                        "citation in adjacent context (Principle XXVIII "
                        "clause 1)."
                    )
                    rule = "skip-without-citation"
                else:
                    msg = (
                        "Newly added pytest skip cites an issue/PR but lacks a "
                        "remediation timeline cue (Principle XXVIII clause 1)."
                    )
                    rule = "skip-without-timeline"
                findings.append(
                    Finding(
                        path=f.path,
                        line=lineno,
                        level="warning",
                        rule=rule,
                        message=msg,
                    )
                )
    return findings


def _line_has_skip(content: str) -> bool:
    return any(p.search(content) for p in SKIP_PATTERNS)


def _index_in_context(hunk: Hunk, target_lineno: int) -> Optional[int]:
    """Return the index of the post-image line ``target_lineno`` in the
    hunk's flat context list, or ``None`` if not found.
    """
    idx = 0
    lineno = hunk.new_start
    for raw in hunk.lines:
        if raw.startswith("+++") or raw.startswith("---"):
            continue
        if raw.startswith("-"):
            continue
        # ``+`` and `` `` lines occupy one slot in context_lines().
        if lineno == target_lineno and raw.startswith("+"):
            return idx
        idx += 1
        lineno += 1
    return None


# ---------------------------------------------------------------------------
# Clause 2 — Diff-shape consistency
# ---------------------------------------------------------------------------


def extract_categories(pr_body: str) -> List[str]:
    """Return the list of declared categories from the PR body.

    Unknown values are silently dropped. Order is preserved; duplicates are
    kept (callers can ``set()`` them if desired).
    """

    out: List[str] = []
    for m in CATEGORY_MARKER_RE.finditer(pr_body):
        value = m.group(1).strip().lower()
        if value in VALID_CATEGORIES:
            out.append(value)
    return out


def compute_diff_shape(
    files: Sequence[FileDiff],
) -> Tuple[List[str], List[str], List[str]]:
    """Return ``(test_paths_modified, production_paths_modified, test_deletions)``."""
    test_paths: List[str] = []
    prod_paths: List[str] = []
    deletions: List[str] = []
    for f in files:
        if is_test_path(f.path):
            test_paths.append(f.path)
            if f.is_deletion:
                deletions.append(f.path)
        elif is_production_path(f.path):
            prod_paths.append(f.path)
    return test_paths, prod_paths, deletions


def find_category_violations(
    files: Sequence[FileDiff], pr_body: str
) -> List[Finding]:
    findings: List[Finding] = []
    categories = extract_categories(pr_body)
    test_paths, prod_paths, deletions = compute_diff_shape(files)

    if not categories:
        if test_paths:
            findings.append(
                Finding(
                    path="",
                    line=0,
                    level="info",
                    rule="missing-category-marker",
                    message=(
                        "PR modifies test files but no "
                        "<!-- test-fix-category: VALUE --> marker is present in "
                        "the PR body (Principle XXVIII clause 2). Add one of: "
                        "fixture-drift, production-bug, legitimate-test-bug, "
                        "defunct-test."
                    ),
                )
            )
        return findings

    for category in categories:
        if category == "fixture-drift" and prod_paths:
            findings.append(
                Finding(
                    path="",
                    line=0,
                    level="warning",
                    rule="category-mismatch-fixture-drift",
                    message=(
                        "Category 'fixture-drift' claims test-only changes but "
                        f"{len(prod_paths)} production path(s) were modified: "
                        f"{', '.join(sorted(prod_paths))} (Principle XXVIII "
                        "clause 2)."
                    ),
                )
            )
        elif category == "production-bug" and not prod_paths:
            findings.append(
                Finding(
                    path="",
                    line=0,
                    level="warning",
                    rule="category-mismatch-production-bug",
                    message=(
                        "Category 'production-bug' claims a production fix but "
                        "zero production paths were modified (Principle XXVIII "
                        "clause 2)."
                    ),
                )
            )
        elif category == "defunct-test" and not deletions:
            findings.append(
                Finding(
                    path="",
                    line=0,
                    level="warning",
                    rule="category-mismatch-defunct-test",
                    message=(
                        "Category 'defunct-test' claims a deleted test but no "
                        "test files were entirely removed (Principle XXVIII "
                        "clause 2)."
                    ),
                )
            )
        elif category == "legitimate-test-bug":
            if prod_paths:
                findings.append(
                    Finding(
                        path="",
                        line=0,
                        level="warning",
                        rule="category-mismatch-legitimate-test-bug",
                        message=(
                            "Category 'legitimate-test-bug' claims a test-only "
                            f"fix but {len(prod_paths)} production path(s) "
                            f"were modified: {', '.join(sorted(prod_paths))} "
                            "(Principle XXVIII clause 2)."
                        ),
                    )
                )
            if not PR_BODY_CITATION_RE.search(pr_body):
                findings.append(
                    Finding(
                        path="",
                        line=0,
                        level="warning",
                        rule="legitimate-test-bug-missing-citation",
                        message=(
                            "Category 'legitimate-test-bug' requires an "
                            "issue/PR citation (e.g. '#123', 'issue 42', 'PR "
                            "99') in the PR body to justify a test-only "
                            "change (Principle XXVIII clause 2)."
                        ),
                    )
                )
    return findings


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


def format_findings(findings: Sequence[Finding], fmt: str) -> str:
    if fmt == "json":
        return json.dumps([f.to_dict() for f in findings], indent=2)
    if fmt == "github":
        return "\n".join(_github_annotation(f) for f in findings)
    if fmt == "text":
        if not findings:
            return "No findings."
        lines: List[str] = []
        for f in findings:
            loc = f.path or "<repo>"
            if f.line:
                loc = f"{loc}:{f.line}"
            lines.append(f"[{f.level}] {f.rule} {loc} — {f.message}")
        return "\n".join(lines)
    raise ValueError(f"unknown format: {fmt}")


def _github_annotation(f: Finding) -> str:
    annotation = "warning" if f.level != "info" else "notice"
    parts: List[str] = []
    if f.path:
        parts.append(f"file={f.path}")
    if f.line:
        parts.append(f"line={f.line}")
    parts.append(f"title=Principle XXVIII ({f.rule})")
    head = ",".join(parts)
    # Replace newlines so the message stays on one annotation line.
    body = f.message.replace("\n", " ")
    return f"::{annotation} {head}::{body}"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def run(diff_text: str, pr_body: str) -> List[Finding]:
    files = parse_diff(diff_text)
    findings: List[Finding] = []
    findings.extend(find_skip_violations(files))
    findings.extend(find_category_violations(files, pr_body))
    return findings


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="lint-test-fixes",
        description=(
            "Principle XXVIII (Test-Fix Boundary Preservation) lint. Verifies "
            "skip discipline and diff-shape consistency for PRs that touch "
            "test files."
        ),
    )
    parser.add_argument(
        "--diff",
        required=True,
        type=Path,
        help="Path to a unified-diff file (typically `git diff base...HEAD`).",
    )
    parser.add_argument(
        "--pr-body",
        required=True,
        type=Path,
        help="Path to a markdown file containing the PR body.",
    )
    parser.add_argument(
        "--format",
        choices=("github", "text", "json"),
        default="github",
        help="Output format (default: github).",
    )
    try:
        args = parser.parse_args(list(argv) if argv is not None else None)
    except SystemExit as exc:
        # argparse exits with 2 on usage error already; propagate.
        return int(exc.code) if exc.code is not None else 2

    if not args.diff.is_file():
        print(f"error: --diff path does not exist: {args.diff}", file=sys.stderr)
        return 2
    if not args.pr_body.is_file():
        print(
            f"error: --pr-body path does not exist: {args.pr_body}",
            file=sys.stderr,
        )
        return 2

    diff_text = _read_text(args.diff)
    pr_body = _read_text(args.pr_body)
    findings = run(diff_text, pr_body)
    output = format_findings(findings, args.format)
    if output:
        print(output)
    # Info-only findings do not flip the exit code; warnings do.
    has_warning = any(f.level == "warning" for f in findings)
    return 1 if has_warning else 0


if __name__ == "__main__":
    sys.exit(main())
