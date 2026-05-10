"""Tests for scripts/strip-constitution-for-blind.py.

Per spec 067 §4.2, the strip script enables blind verification by
removing the candidate amendment's SIR, version footer, and citation
markers from CONSTITUTION.md so blind reviewers cannot identify the
candidate amendment by metadata alone.

Test file location is binding per the strip-script-061-substeps
deliberation (2026-05-01) — Rec 7 declares
``engine/tests/test_strip_constitution.py`` as the canonical location.
Moving the file requires a CI discovery update before the move lands.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Direct unit tests on the helper function
# ---------------------------------------------------------------------------
#
# We import the helper directly rather than executing the script so the
# tests can run in <100ms and don't depend on subprocess overhead.

_SCRIPT_PATH = Path(__file__).resolve().parents[2] / "scripts" / "strip-constitution-for-blind.py"


def _import_strip_module():
    """Load the strip script as a module for direct function access."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("strip_script", _SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def strip_module():
    return _import_strip_module()


# ---------------------------------------------------------------------------
# verify_zero_leakage — HTML comment exclusion contract
# ---------------------------------------------------------------------------
#
# Pre-fix behaviour (the bug): if --date appeared in any prior SIR
# comment block, the leakage check tripped even when the rendered body
# was leakage-free. Operators running blind verification against a
# constitution with multi-SIR history could not use --date as documented.
#
# Post-fix behaviour: HTML comment blocks are excluded from the date
# scan because dates legitimately appear in prior-SIR audit trails
# (which are NOT visible to blind reviewers examining the rendered
# constitution). Version needles are NOT excluded because version
# strings in the rendered footer are visible to readers.


class TestDateExcludesHtmlComments:
    """The --date scan ignores dates inside <!-- ... --> comment blocks."""

    def test_date_in_comment_only_returns_no_leakage(self, strip_module):
        """Date inside HTML comment doesn't trigger leakage."""
        stripped = """
# Conversus Constitution

<!--
Sync Impact Report (prior — preserved for audit trail)
Version change: 3.0.0 → 3.1.0 amended on 2026-05-01.
-->

Some body text without dates.
"""
        leaks = strip_module.verify_zero_leakage(stripped, "v3.2.0", "2026-05-01")
        assert leaks == []

    def test_date_in_body_returns_leakage(self, strip_module):
        """Date in rendered (non-comment) body text IS a real leakage."""
        stripped = """
# Conversus Constitution

This amendment was made on 2026-05-01.
"""
        leaks = strip_module.verify_zero_leakage(stripped, "v3.2.0", "2026-05-01")
        assert len(leaks) == 1
        assert "2026-05-01" in leaks[0]
        assert "1x remaining" in leaks[0]

    def test_date_in_both_comment_and_body_only_counts_body(
        self, strip_module
    ):
        """Mixed case: only body occurrence counts toward leakage."""
        stripped = """
<!--
Prior SIR: amended 2026-05-01.
-->

Body says: ratified on 2026-05-01.
"""
        leaks = strip_module.verify_zero_leakage(stripped, "v3.2.0", "2026-05-01")
        assert len(leaks) == 1
        # Only the body occurrence counts
        assert "1x remaining" in leaks[0]

    def test_multiple_dates_in_comments_no_leakage(self, strip_module):
        """5 prior SIRs all dated 2026-05-01 → still 0 leakage in body."""
        stripped = """<!-- SIR 1: 2026-05-01 -->
<!-- SIR 2: 2026-05-01 -->
<!-- SIR 3: 2026-05-01 -->
<!-- SIR 4: 2026-05-01 -->
<!-- SIR 5: 2026-05-01 -->

# Constitution body

Pure body text.
"""
        leaks = strip_module.verify_zero_leakage(stripped, "v3.2.0", "2026-05-01")
        assert leaks == []


class TestVersionNeedleNotCommentExcluded:
    """Version strings DO trigger leakage even when only in comments.

    The asymmetry is intentional: a version string in a comment is
    audit-trail metadata that can leak the candidate's identity to a
    reviewer who reads source. A date is generally less identifying
    (many amendments share dates) and SIR audit trails legitimately
    accumulate dates over time.
    """

    def test_version_in_comment_returns_leakage(self, strip_module):
        stripped = """<!--
Prior SIR for v3.2.0
-->
"""
        leaks = strip_module.verify_zero_leakage(stripped, "v3.2.0", None)
        # v3.2.0 OR 3.2.0 (both checked) — at least one match
        assert len(leaks) >= 1

    def test_version_with_v_prefix_strips_correctly(self, strip_module):
        """Both 'v3.2.0' and '3.2.0' needles are checked."""
        stripped = "Version 3.2.0 was ratified."  # no v prefix
        leaks = strip_module.verify_zero_leakage(stripped, "v3.2.0", None)
        # 3.2.0 matches even without v prefix
        assert any("3.2.0" in leak for leak in leaks)


class TestNoDateProvided:
    """When --date is None, only version needles are checked."""

    def test_no_date_no_check(self, strip_module):
        """--date=None must not trigger any date-needle scanning."""
        stripped = "Some body text with 2026-05-01 mentioned."
        leaks = strip_module.verify_zero_leakage(stripped, "v3.2.0", None)
        # No date check, no version match → 0 leakages
        assert leaks == []


# ---------------------------------------------------------------------------
# End-to-end: strip current CONSTITUTION.md for a hypothetical future v3.2.0
# ---------------------------------------------------------------------------
#
# This test exercises the full script subprocess. It demonstrates that
# in a realistic blind-verification workflow (candidate version + date
# distinct from any pre-existing amendment), the strip script
# produces clean output.


class TestEndToEndRealisticFlow:
    """Full subprocess invocation against the real CONSTITUTION.md."""

    @pytest.fixture
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    def test_realistic_candidate_strips_clean(
        self, repo_root: Path, tmp_path: Path
    ):
        """Operator workflow: add candidate SIR + footer, then strip.

        Simulates: the operator has added a v5.0.0 SIR + bumped the
        version footer to v5.0.0 dated 2027-12-15 (a date NOT yet
        appearing in any prior SIR; v5.0.0 is a hypothetical future
        version not yet referenced in the body). Running the strip
        script against this enriched document should produce clean
        output.

        Before the HTML comment exclusion fix (see deliberation
        verdict 2026-05-01), the script would have tripped on the
        2026-05-01 dates inside the prior v3.1.x SIR comment blocks.
        After the fix, only body-text occurrences of 2027-12-15 (the
        candidate date) would count — and the candidate's SIR + footer
        ARE stripped, so no occurrences should remain.

        Note on candidate version selection: this test must use a
        version NOT yet referenced anywhere in the constitution body.
        v3.2.0 was used initially but became stale after PR #116
        added v3.2.0 references to the body (Constitutional Amendment
        Pathways subsection cites prior versions including v3.0.0,
        v3.1.0, v3.1.1, v3.1.2, v3.1.3, v3.2.0). v5.0.0 is currently
        clean; future test maintainers should bump to whatever the
        next-clean-future version is.
        """
        constitution = repo_root / "CONSTITUTION.md"
        original = constitution.read_text(encoding="utf-8")

        # Add a hypothetical v5.0.0 candidate SIR + bump footer.
        # Use 2027-12-15 — distinct from any existing date in body.
        candidate_sir = """<!--
Sync Impact Report
Version change: 3.2.2 → 4.0.0 (MAJOR — hypothetical test amendment).
Governance log entry: 2027-12-15 in CONSTITUTIONAL_CONVERSATIONS.md.
Prior amendment (v3.2.1 → v3.2.2): see prior SIR comment block below.
-->

"""
        # The current footer line — find dynamically so the test
        # doesn't break on each version bump.
        current_footer_match = re.search(
            r"\*\*Version\*\*: \d+\.\d+\.\d+ \| \*\*Ratified\*\*: [^|]+\| \*\*Last Amended\*\*: [^\n]+",
            original,
        )
        assert current_footer_match, "Could not locate version footer in CONSTITUTION.md"
        current_footer = current_footer_match.group()

        enriched = candidate_sir + original.replace(
            current_footer,
            "**Version**: 5.0.0 | **Ratified**: 2026-03-20 | **Last Amended**: 2027-12-15",
        )

        # Write to tmp + run script
        candidate_path = tmp_path / "CONSTITUTION-v5.0.0-candidate.md"
        candidate_path.write_text(enriched, encoding="utf-8")
        output_path = tmp_path / "CONSTITUTION-v5.0.0-blind.md"

        result = subprocess.run(
            [
                sys.executable,
                str(_SCRIPT_PATH),
                "--input", str(candidate_path),
                "--output", str(output_path),
                "--version", "v5.0.0",
                "--date", "2027-12-15",
            ],
            capture_output=True,
            text=True,
        )

        # Should exit 0 (no leakage)
        assert result.returncode == 0, (
            f"Strip script exited {result.returncode}.\n"
            f"stderr: {result.stderr}\nstdout: {result.stdout}"
        )

        # Verify the candidate version + date are absent in the
        # rendered (non-comment) body of the stripped output
        stripped = output_path.read_text(encoding="utf-8")
        body_only = re.sub(r"<!--.*?-->", "", stripped, flags=re.DOTALL)
        assert "v5.0.0" not in body_only
        assert "2027-12-15" not in body_only
