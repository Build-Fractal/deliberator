#!/usr/bin/env python3
"""v4.0.0 erratum: convert filesystem-relative cross-tier references to GitHub URLs.

Per spec v4 erratum (corrects spec v3 §5 cross-reference patterns table): all
cross-tier references in constitutional documents use canonical GitHub URLs to
the monorepo source-of-truth, not filesystem-relative paths. This makes each
repo's CONSTITUTION.md / CONFORMANCE.md self-contained for standalone reading
(via github.com or pip-installed source) while preserving the single-source-of-
truth model in the monorepo.

The URL prefix is configured below. If the monorepo moves (e.g., build-fractal/
extracts to its own repo at github.com/Build-Fractal/governance), update
URL_PREFIX and re-run this script.

Run from monorepo root:
    cd payer-index-mono && python deliberator/scripts/v4-url-references.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # monorepo root
URL_PREFIX = "https://github.com/Build-Fractal/build-fractal-mono/blob/main"

# Files to convert (relative to monorepo root). Each file's references to
# the monorepo's build-fractal/ + sibling-submodule paths get converted.
FILES = [
    "deliberator/CONSTITUTION.md",
    "deliberator/CONFORMANCE.md",
    "deliberator/CONFORMANCE.md",
    "build-fractal/CONSTITUTION.md",
    "build-fractal/deliberator/CONSTITUTION.md",
    "build-fractal/deliberator/CONSTITUTIONAL_CONVERSATIONS.md",
    "build-fractal/deliberator/GOVERNANCE.md",
    "build-fractal/deliberator/COMPLIANCE.md",
    "build-fractal/deliberator/CLAUDE.md",
    "build-fractal/deliberator/AGENTS.md",
    "build-fractal/deliberator/README.md",
]

# Replacement table. Each tuple: (relative-path-pattern, monorepo-absolute-path).
# The script converts `relative-path-pattern` (with backticks or in markdown links)
# to URL_PREFIX + monorepo-absolute-path.
#
# Order matters: more-specific patterns first to avoid shadowing.
REPLACEMENTS = [
    # From build-fractal/deliberator/* (depth 2)
    ("../../deliberator/CONSTITUTIONAL_CONVERSATIONS.md", "deliberator/CONSTITUTIONAL_CONVERSATIONS.md"),
    ("../../deliberator/CONFORMANCE.md", "deliberator/CONFORMANCE.md"),
    ("../../deliberator/CONSTITUTION.md", "deliberator/CONSTITUTION.md"),
    ("../../deliberator/deliberations", "deliberator/deliberations"),
    ("../../deliberator/specs", "deliberator/specs"),
    ("../../deliberator/scripts", "deliberator/scripts"),
    ("../../deliberator/linter", "deliberator/linter"),
    ("../../deliberator/", "deliberator/"),
    ("../../deliberator/CONFORMANCE.md", "deliberator/CONFORMANCE.md"),
    ("../../deliberator/", "deliberator/"),
    # From build-fractal/* (depth 1)
    ("../deliberator/CONSTITUTIONAL_CONVERSATIONS.md", "deliberator/CONSTITUTIONAL_CONVERSATIONS.md"),
    ("../deliberator/CONFORMANCE.md", "deliberator/CONFORMANCE.md"),
    ("../deliberator/CONSTITUTION.md", "deliberator/CONSTITUTION.md"),
    ("../deliberator/", "deliberator/"),
    ("../deliberator/CONFORMANCE.md", "deliberator/CONFORMANCE.md"),
    ("../deliberator/", "deliberator/"),
    # From deliberator/* and deliberator/*
    ("../build-fractal/CONSTITUTION.md", "build-fractal/CONSTITUTION.md"),
    ("../build-fractal/deliberator/CONSTITUTIONAL_CONVERSATIONS.md", "build-fractal/deliberator/CONSTITUTIONAL_CONVERSATIONS.md"),
    ("../build-fractal/deliberator/COMPLIANCE.md", "build-fractal/deliberator/COMPLIANCE.md"),
    ("../build-fractal/deliberator/GOVERNANCE.md", "build-fractal/deliberator/GOVERNANCE.md"),
    ("../build-fractal/deliberator/CONSTITUTION.md", "build-fractal/deliberator/CONSTITUTION.md"),
    ("../build-fractal/deliberator/", "build-fractal/deliberator/"),
    ("../build-fractal/", "build-fractal/"),
]


def convert_text(text: str) -> tuple[str, list[str]]:
    """Apply all replacements; return (new_text, list of replacements made)."""
    log: list[str] = []
    for relative, abs_path in REPLACEMENTS:
        url = f"{URL_PREFIX}/{abs_path}"
        if relative in text:
            count = text.count(relative)
            text = text.replace(relative, url)
            log.append(f"  {count}× '{relative}' → URL")
    return text, log


def main() -> int:
    total_replacements = 0
    for relpath in FILES:
        path = ROOT / relpath
        if not path.exists():
            print(f"SKIP: {path} (does not exist)", file=sys.stderr)
            continue
        original = path.read_text()
        new_text, log = convert_text(original)
        if new_text == original:
            print(f"NOOP: {relpath} (no relative refs found)")
            continue
        path.write_text(new_text)
        print(f"WROTE: {relpath}")
        for line in log:
            print(line)
        total_replacements += len(log)

    print(f"\nTotal files processed: {len(FILES)}")
    print(f"Total replacement-types applied: {total_replacements}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
