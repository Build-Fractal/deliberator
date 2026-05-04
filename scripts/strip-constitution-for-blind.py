#!/usr/bin/env python3
"""Strip a constitution amendment's anchoring markers for blind verification.

Reference implementation of spec 067 §4.2's stripping recipe. Reads
``CONSTITUTION.md`` (or any path provided), removes the anchoring artifacts
that bias agents toward ratifying recent additions, and writes the
stripped output to a target file.

Stripping recipe (spec 067 §4.2):
    1. Remove the Sync Impact Report HTML comment at the top.
    2. Remove version markers from new principles (`(vX.Y.Z)` mentions
       inside principle bodies, `**Extension (vX.Y.Z):**` -> `**Extension:**`).
    3. Strip Origin attributions referencing the originating deliberation
       or specific PRs *for the new/extended principles only*. Pre-amendment
       Origin lines (e.g., spec 005, spec 011a) are preserved.
    4. Anonymize the version footer to "(under review)".
    5. Verify zero leakage of the candidate version string.

Usage::

    python scripts/strip-constitution-for-blind.py \\
        --input CONSTITUTION.md \\
        --output deliberations/<slug>/CONSTITUTION-blind.md \\
        --version v2.3.0 \\
        --date 2026-04-25

The ``--version`` and ``--date`` are the leakage-check anchors -- the
script greps for these strings in the stripped output and exits non-zero
if any remain. This is the "verify zero leakage" requirement from
spec 067 §4.2.5.

Exit codes:
    0 -- stripped successfully, zero leakage detected
    1 -- leakage detected (candidate version or date string remained)
    2 -- input file not found / output dir does not exist

This script is intentionally minimal -- it does NOT auto-regenerate the
constitution, does NOT run the deliberation, does NOT format the output.
It does ONE thing: produce the stripped file from the source. Future
amendments can compose this script with their own deliberation pipeline.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def strip_constitution(source: str, version: str) -> str:
    """Apply the spec 067 §4.2 stripping recipe to ``source``."""
    out = source

    # Step 1 -- remove the leading Sync Impact Report HTML comment.
    out = re.sub(
        r"^<!--\nSync Impact Report.*?-->\n\n", "", out, count=1, flags=re.DOTALL
    )
    # If a "Sync Impact Report (prior ...)" still references the candidate
    # version, strip that one too.
    out = re.sub(
        rf"<!--\nSync Impact Report \(prior[^\n]*\nVersion change:[^\n]*"
        rf"{re.escape(version[1:])} . [^\n]*\n.*?-->\n\n",
        "",
        out,
        flags=re.DOTALL,
    )

    # Step 2 -- remove version markers from extension headers and prose.
    out = re.sub(
        rf"\*\*Extension \({re.escape(version)}\):\*\*",
        "**Extension:**",
        out,
    )
    out = re.sub(rf"\s*\({re.escape(version)}\)", "", out)
    out = re.sub(rf"\s*\({re.escape(version[1:])}\)", "", out)

    # Step 3 -- strip Origin attributions referencing the candidate version.
    origin_patterns = [
        r"\*Origin: PR #[\d, #]+\.[^*]*\*\n+",
        r"\*Origin: PR #[\d, #]+ introduced[^*]*\*\n+",
        r"\*Origin: PR #\d+ \([^)]*\)[^*]*\*\n+",
    ]
    for pat in origin_patterns:
        out = re.sub(pat, "", out, flags=re.DOTALL)

    # Step 3b -- strip Amendment record subsections (introduced v3.0.x
    # cycle 2B). These would otherwise survive Origin stripping because
    # they sit AFTER the Origin note and are formatted as their own
    # italicized blocks. Leaving them in place tips a blind reviewer
    # that the post-amendment governance infrastructure exists.
    out = re.sub(
        r"\*Amendment record \([^)]*\):[^*]*\*\n+",
        "",
        out,
        flags=re.DOTALL,
    )

    out = re.sub(
        r"The \d{4}-\d{2}-\d{2} deliberation arbiter explicitly extended this scope to\s+",
        "This principle's scope extends to ",
        out,
    )
    out = re.sub(
        r"The \d{4}-\d{2}-\d{2} deliberation arbiter ruled[^.]*\.",
        "",
        out,
    )

    # Step 4 -- anonymize the version footer.
    out = re.sub(
        rf"\*\*Version\*\*: {re.escape(version[1:])}\s*\|\s*\*\*Ratified\*\*:[^|]+\|\s*\*\*Last Amended\*\*:[^\n]+",
        "**Version**: (under review) | **Ratified**: 2026-03-20",
        out,
    )

    return out


def verify_zero_leakage(stripped: str, version: str, date: str | None) -> list[str]:
    """Return list of leakage strings still present in ``stripped``.

    HTML comment blocks (the SIR audit-trail format) are excluded from
    the date-needle scan because dates legitimately appear in prior-SIR
    blocks (e.g. "Last Amended: 2026-05-01") that survive Step 1's
    candidate-version SIR strip but are NOT visible to a blind reviewer
    examining the rendered constitution. Without this exclusion, the
    --date check trips on every prior SIR's amendment date and exits 1
    even when the rendered (non-comment) body is leakage-free.

    Version needles are NOT excluded from comments because a version
    string in the rendered footer (e.g. "**Version**: 3.1.3") is
    visible to readers and is a real leakage source.
    """
    leaks: list[str] = []
    version_needles = [version, version[1:]]
    for needle in version_needles:
        if needle in stripped:
            count = stripped.count(needle)
            leaks.append(f"{needle!r} ({count}x remaining)")
    if date:
        body_only = re.sub(r"<!--.*?-->", "", stripped, flags=re.DOTALL)
        if date in body_only:
            count = body_only.count(date)
            leaks.append(f"{date!r} ({count}x remaining)")
    return leaks


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Strip constitution amendment markers for blind verification (spec 067 §4.2).",
    )
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--version",
        required=True,
        help="Candidate version string with v prefix (e.g. 'v2.3.0').",
    )
    parser.add_argument(
        "--date",
        default=None,
        help="Optional originating deliberation date for leakage check.",
    )
    args = parser.parse_args()

    if not args.input.is_file():
        print(f"Error: input file not found: {args.input}", file=sys.stderr)
        return 2
    if not args.output.parent.is_dir():
        print(
            f"Error: output directory does not exist: {args.output.parent}",
            file=sys.stderr,
        )
        return 2

    source = args.input.read_text(encoding="utf-8")
    stripped = strip_constitution(source, args.version)

    leaks = verify_zero_leakage(stripped, args.version, args.date)
    if leaks:
        print(
            f"Error: leakage detected in stripped output: {', '.join(leaks)}.\n"
            f"  Spec 067 §4.2.5 requires 0 matches. The stripping recipe "
            f"may have a regex gap for this constitution's specific format.",
            file=sys.stderr,
        )
        return 1

    args.output.write_text(stripped, encoding="utf-8")
    print(
        f"Stripped {args.input} -> {args.output} "
        f"({len(stripped)} chars, {stripped.count(chr(10))} lines)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
