"""
Test suite for the deliberator usage logger and adoption-gate reporter (linter/usage.py).

Exercises the UsageEntry and AdoptionMetrics models, log_usage(), summarize_usage(),
format_report(), and the CLI entry points (log + summary).
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

try:
    from .usage import (
        AdoptionMetrics,
        SynthesisMeta,
        UsageEntry,
        format_report,
        log_usage,
        summarize_usage,
    )
except ImportError:
    from usage import (
        AdoptionMetrics,
        SynthesisMeta,
        UsageEntry,
        format_report,
        log_usage,
        summarize_usage,
    )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def question_file(tmp_path: Path) -> Path:
    """Create a sample question file and return its path."""
    p = tmp_path / "question.md"
    p.write_text("Should we use monorepo or polyrepo for this project?", encoding="utf-8")
    return p


@pytest.fixture()
def synthesis_file(tmp_path: Path) -> Path:
    """Create a minimal synthesis file and return its path."""
    p = tmp_path / "final.md"
    p.write_text("# Synthesis\nSome cooperative deliberation output.\n", encoding="utf-8")
    return p


@pytest.fixture()
def quality_dict() -> dict:
    """A quality gate result dict with both sub-gates passing."""
    return {
        "passed": True,
        "disagreement": {"passed": True, "dispute_count": 2},
        "attributions": {"passed": True},
    }


@pytest.fixture()
def quality_dict_fail() -> dict:
    """A quality gate result dict with both sub-gates failing."""
    return {
        "passed": False,
        "disagreement": {"passed": False, "dispute_count": 0},
        "attributions": {"passed": False},
    }


@pytest.fixture()
def usage_file(tmp_path: Path) -> Path:
    """Return a fresh, non-existent JSONL path inside tmp_path."""
    return tmp_path / "data" / "usage.jsonl"


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


class TestUsageEntryModel:
    """Tests for the UsageEntry frozen Pydantic model."""

    def test_frozen(self) -> None:
        entry = UsageEntry(
            timestamp="2026-03-22T00:00:00+00:00",
            session_id="abcd1234",
            question_hash="0123456789abcdef",
            question_word_count=9,
            preset_mode="cooperative",
            agent_names=["Pragmatist", "Devil's Advocate"],
            iterations=1,
            quality_passed=True,
            disagreement_passed=True,
            attributions_passed=True,
            dispute_count=2,
            fallback_used=False,
            phases_completed=5,
            agent_count=2,
        )
        with pytest.raises(Exception):
            entry.version = 99  # type: ignore[misc]

    def test_default_version(self) -> None:
        entry = UsageEntry(
            timestamp="2026-03-22T00:00:00+00:00",
            session_id="abcd1234",
            question_hash="0123456789abcdef",
            question_word_count=9,
            preset_mode="cooperative",
            agent_names=[],
            iterations=1,
            quality_passed=False,
            disagreement_passed=False,
            attributions_passed=False,
            dispute_count=0,
            fallback_used=False,
            phases_completed=5,
            agent_count=0,
        )
        assert entry.version == 1

    def test_all_15_fields(self) -> None:
        """Verify the model has exactly 15 fields."""
        assert len(UsageEntry.model_fields) == 15

    def test_required_fields_without_version(self) -> None:
        """Omitting a required field raises ValidationError."""
        with pytest.raises(Exception):
            UsageEntry(  # type: ignore[call-arg]
                timestamp="2026-03-22T00:00:00+00:00",
                # session_id missing
                question_hash="0123456789abcdef",
                question_word_count=9,
                preset_mode="cooperative",
                agent_names=[],
                iterations=1,
                quality_passed=False,
                disagreement_passed=False,
                attributions_passed=False,
                dispute_count=0,
                fallback_used=False,
                phases_completed=5,
                agent_count=0,
            )


class TestAdoptionMetricsModel:
    """Tests for the AdoptionMetrics frozen Pydantic model."""

    def test_frozen(self) -> None:
        m = AdoptionMetrics(
            total_runs=0,
            unique_sessions=0,
            date_range="N/A",
            trust_rate=0.0,
            return_rate=0.0,
            sharing_status="N/A",
            disagreement_pass_rate=0.0,
            attribution_pass_rate=0.0,
            fallback_rate=0.0,
            run_distribution={},
        )
        with pytest.raises(Exception):
            m.total_runs = 99  # type: ignore[misc]


class TestSynthesisMetaModel:
    """Tests for the SynthesisMeta frozen Pydantic model (M1)."""

    def test_frozen(self) -> None:
        meta = SynthesisMeta(
            preset_mode="cooperative",
            agent_names=["Pragmatist"],
            iterations=1,
            phases_completed=5,
        )
        with pytest.raises(Exception):
            meta.preset_mode = "red-blue"  # type: ignore[misc]

    def test_has_expected_fields(self) -> None:
        """Verify the model has exactly 4 fields."""
        assert set(SynthesisMeta.model_fields.keys()) == {
            "preset_mode",
            "agent_names",
            "iterations",
            "phases_completed",
        }

    def test_defaults(self) -> None:
        meta = SynthesisMeta()
        assert meta.preset_mode == "cooperative"
        assert meta.agent_names == []
        assert meta.iterations == 1
        assert meta.phases_completed == 5

    def test_custom_values(self) -> None:
        meta = SynthesisMeta(
            preset_mode="red-blue",
            agent_names=["Red", "Blue"],
            iterations=3,
            phases_completed=4,
        )
        assert meta.preset_mode == "red-blue"
        assert meta.agent_names == ["Red", "Blue"]
        assert meta.iterations == 3
        assert meta.phases_completed == 4


# ---------------------------------------------------------------------------
# log_usage() tests
# ---------------------------------------------------------------------------


class TestLogUsage:
    """Tests for the log_usage() function."""

    def test_creates_directory_and_file(
        self,
        question_file: Path,
        synthesis_file: Path,
        quality_dict: dict,
        usage_file: Path,
    ) -> None:
        assert not usage_file.parent.exists()
        log_usage(
            synthesis_path=synthesis_file,
            question_path=question_file,
            quality_json=quality_dict,
            fallback_used=False,
            usage_file=usage_file,
        )
        assert usage_file.exists()

    def test_appends_valid_jsonl(
        self,
        question_file: Path,
        synthesis_file: Path,
        quality_dict: dict,
        usage_file: Path,
    ) -> None:
        # Log twice
        log_usage(
            synthesis_path=synthesis_file,
            question_path=question_file,
            quality_json=quality_dict,
            fallback_used=False,
            usage_file=usage_file,
        )
        log_usage(
            synthesis_path=synthesis_file,
            question_path=question_file,
            quality_json=quality_dict,
            fallback_used=True,
            usage_file=usage_file,
        )
        lines = [l for l in usage_file.read_text().strip().split("\n") if l]
        assert len(lines) == 2
        for line in lines:
            data = json.loads(line)
            assert "version" in data
            assert "timestamp" in data

    def test_question_hash_is_sha256_truncated(
        self,
        question_file: Path,
        synthesis_file: Path,
        quality_dict: dict,
        usage_file: Path,
    ) -> None:
        entry = log_usage(
            synthesis_path=synthesis_file,
            question_path=question_file,
            quality_json=quality_dict,
            fallback_used=False,
            usage_file=usage_file,
        )
        question_text = question_file.read_text(encoding="utf-8")
        expected = hashlib.sha256(question_text.encode("utf-8")).hexdigest()[:16]
        assert entry.question_hash == expected
        assert len(entry.question_hash) == 16

    def test_word_count(
        self,
        question_file: Path,
        synthesis_file: Path,
        quality_dict: dict,
        usage_file: Path,
    ) -> None:
        entry = log_usage(
            synthesis_path=synthesis_file,
            question_path=question_file,
            quality_json=quality_dict,
            fallback_used=False,
            usage_file=usage_file,
        )
        expected_wc = len(question_file.read_text().split())
        assert entry.question_word_count == expected_wc

    def test_quality_field_mapping(
        self,
        question_file: Path,
        synthesis_file: Path,
        quality_dict: dict,
        usage_file: Path,
    ) -> None:
        entry = log_usage(
            synthesis_path=synthesis_file,
            question_path=question_file,
            quality_json=quality_dict,
            fallback_used=False,
            usage_file=usage_file,
        )
        assert entry.quality_passed is True
        assert entry.disagreement_passed is True
        assert entry.attributions_passed is True
        assert entry.dispute_count == 2

    def test_quality_json_as_string(
        self,
        question_file: Path,
        synthesis_file: Path,
        quality_dict: dict,
        usage_file: Path,
    ) -> None:
        entry = log_usage(
            synthesis_path=synthesis_file,
            question_path=question_file,
            quality_json=json.dumps(quality_dict),
            fallback_used=False,
            usage_file=usage_file,
        )
        assert entry.quality_passed is True

    def test_session_id_generated(
        self,
        question_file: Path,
        synthesis_file: Path,
        quality_dict: dict,
        usage_file: Path,
    ) -> None:
        entry = log_usage(
            synthesis_path=synthesis_file,
            question_path=question_file,
            quality_json=quality_dict,
            fallback_used=False,
            usage_file=usage_file,
        )
        assert len(entry.session_id) == 8

    def test_session_id_explicit(
        self,
        question_file: Path,
        synthesis_file: Path,
        quality_dict: dict,
        usage_file: Path,
    ) -> None:
        entry = log_usage(
            synthesis_path=synthesis_file,
            question_path=question_file,
            quality_json=quality_dict,
            fallback_used=False,
            session_id="deadbeef",
            usage_file=usage_file,
        )
        assert entry.session_id == "deadbeef"

    def test_fallback_used_field(
        self,
        question_file: Path,
        synthesis_file: Path,
        quality_dict: dict,
        usage_file: Path,
    ) -> None:
        entry = log_usage(
            synthesis_path=synthesis_file,
            question_path=question_file,
            quality_json=quality_dict,
            fallback_used=True,
            usage_file=usage_file,
        )
        assert entry.fallback_used is True

    def test_returns_usage_entry(
        self,
        question_file: Path,
        synthesis_file: Path,
        quality_dict: dict,
        usage_file: Path,
    ) -> None:
        entry = log_usage(
            synthesis_path=synthesis_file,
            question_path=question_file,
            quality_json=quality_dict,
            fallback_used=False,
            usage_file=usage_file,
        )
        assert isinstance(entry, UsageEntry)

    def test_oserror_on_write_returns_entry(
        self,
        question_file: Path,
        synthesis_file: Path,
        quality_dict: dict,
        tmp_path: Path,
    ) -> None:
        """I4: OSError during write returns the entry without raising."""
        # Create a read-only directory so the write fails
        readonly_dir = tmp_path / "readonly"
        readonly_dir.mkdir()
        readonly_dir.chmod(0o444)
        usage_file = readonly_dir / "subdir" / "usage.jsonl"
        try:
            entry = log_usage(
                synthesis_path=synthesis_file,
                question_path=question_file,
                quality_json=quality_dict,
                fallback_used=False,
                usage_file=usage_file,
            )
            assert isinstance(entry, UsageEntry)
            assert entry.quality_passed is True
        finally:
            # Restore permissions so pytest can clean up
            readonly_dir.chmod(0o755)


class TestLogUsagePrivacy:
    """Ensure raw question text never appears in the JSONL output."""

    def test_no_raw_question_in_jsonl(
        self,
        question_file: Path,
        synthesis_file: Path,
        quality_dict: dict,
        usage_file: Path,
    ) -> None:
        raw_question = question_file.read_text(encoding="utf-8")
        log_usage(
            synthesis_path=synthesis_file,
            question_path=question_file,
            quality_json=quality_dict,
            fallback_used=False,
            usage_file=usage_file,
        )
        logged = usage_file.read_text(encoding="utf-8")
        assert raw_question not in logged

    def test_no_raw_question_in_entry_json(
        self,
        question_file: Path,
        synthesis_file: Path,
        quality_dict: dict,
        usage_file: Path,
    ) -> None:
        raw_question = question_file.read_text(encoding="utf-8")
        entry = log_usage(
            synthesis_path=synthesis_file,
            question_path=question_file,
            quality_json=quality_dict,
            fallback_used=False,
            usage_file=usage_file,
        )
        entry_json = entry.model_dump_json()
        assert raw_question not in entry_json


# ---------------------------------------------------------------------------
# summarize_usage() tests
# ---------------------------------------------------------------------------


def _write_entries(path: Path, entries: list[dict]) -> None:
    """Helper: write a list of dicts as JSONL."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e) + "\n")


def _make_entry(
    *,
    session_id: str = "aabb0011",
    quality_passed: bool = True,
    disagreement_passed: bool = True,
    attributions_passed: bool = True,
    fallback_used: bool = False,
    timestamp: str = "2026-03-22T12:00:00+00:00",
) -> dict:
    """Helper: create a valid usage entry dict."""
    return {
        "version": 1,
        "timestamp": timestamp,
        "session_id": session_id,
        "question_hash": "0123456789abcdef",
        "question_word_count": 9,
        "preset_mode": "cooperative",
        "agent_names": ["Pragmatist", "Devil's Advocate"],
        "iterations": 1,
        "quality_passed": quality_passed,
        "disagreement_passed": disagreement_passed,
        "attributions_passed": attributions_passed,
        "dispute_count": 2,
        "fallback_used": fallback_used,
        "phases_completed": 5,
        "agent_count": 2,
    }


class TestSummarizeUsage:
    """Tests for the summarize_usage() function."""

    def test_corrupt_jsonl_lines_skipped(self, usage_file: Path) -> None:
        """C3: corrupt JSONL lines are skipped, not crashed on."""
        usage_file.parent.mkdir(parents=True, exist_ok=True)
        with usage_file.open("w", encoding="utf-8") as f:
            f.write(json.dumps(_make_entry(session_id="s1")) + "\n")
            f.write("THIS IS NOT VALID JSON\n")
            f.write(json.dumps(_make_entry(session_id="s2")) + "\n")
        metrics = summarize_usage(usage_file)
        assert metrics.total_runs == 2
        assert metrics.corrupt_lines == 1

    def test_empty_file(self, usage_file: Path) -> None:
        # File does not exist
        metrics = summarize_usage(usage_file)
        assert metrics.total_runs == 0
        assert metrics.unique_sessions == 0
        assert metrics.trust_rate == 0.0
        assert metrics.return_rate == 0.0

    def test_single_run(self, usage_file: Path) -> None:
        _write_entries(usage_file, [_make_entry()])
        metrics = summarize_usage(usage_file)
        assert metrics.total_runs == 1
        assert metrics.unique_sessions == 1
        assert metrics.trust_rate == 1.0
        assert metrics.return_rate == 0.0  # 1 session, 1 run → no return

    def test_trust_rate_mixed(self, usage_file: Path) -> None:
        entries = [
            _make_entry(quality_passed=True, session_id="s1"),
            _make_entry(quality_passed=True, session_id="s2"),
            _make_entry(quality_passed=False, session_id="s3"),
            _make_entry(quality_passed=False, session_id="s4"),
        ]
        _write_entries(usage_file, entries)
        metrics = summarize_usage(usage_file)
        assert metrics.trust_rate == pytest.approx(0.5)

    def test_return_rate_with_multi_run_sessions(self, usage_file: Path) -> None:
        entries = [
            _make_entry(session_id="s1"),
            _make_entry(session_id="s1"),  # s1 returns
            _make_entry(session_id="s2"),
            _make_entry(session_id="s3"),
        ]
        _write_entries(usage_file, entries)
        metrics = summarize_usage(usage_file)
        assert metrics.unique_sessions == 3
        # s1 has >1 run → 1 returning session out of 3
        assert metrics.return_rate == pytest.approx(1 / 3)

    def test_sharing_status_always_na(self, usage_file: Path) -> None:
        _write_entries(usage_file, [_make_entry()])
        metrics = summarize_usage(usage_file)
        assert "N/A" in metrics.sharing_status

    def test_disagreement_pass_rate(self, usage_file: Path) -> None:
        entries = [
            _make_entry(disagreement_passed=True),
            _make_entry(disagreement_passed=False),
        ]
        _write_entries(usage_file, entries)
        metrics = summarize_usage(usage_file)
        assert metrics.disagreement_pass_rate == pytest.approx(0.5)

    def test_attribution_pass_rate(self, usage_file: Path) -> None:
        entries = [
            _make_entry(attributions_passed=True),
            _make_entry(attributions_passed=True),
            _make_entry(attributions_passed=False),
        ]
        _write_entries(usage_file, entries)
        metrics = summarize_usage(usage_file)
        assert metrics.attribution_pass_rate == pytest.approx(2 / 3)

    def test_fallback_rate(self, usage_file: Path) -> None:
        entries = [
            _make_entry(fallback_used=True),
            _make_entry(fallback_used=False),
            _make_entry(fallback_used=False),
            _make_entry(fallback_used=False),
        ]
        _write_entries(usage_file, entries)
        metrics = summarize_usage(usage_file)
        assert metrics.fallback_rate == pytest.approx(0.25)

    def test_run_distribution(self, usage_file: Path) -> None:
        entries = [
            _make_entry(session_id="a1"),  # 1 run
            _make_entry(session_id="b2"),
            _make_entry(session_id="b2"),  # 2 runs
            _make_entry(session_id="c3"),
            _make_entry(session_id="c3"),
            _make_entry(session_id="c3"),  # 3 runs
        ]
        _write_entries(usage_file, entries)
        metrics = summarize_usage(usage_file)
        assert metrics.run_distribution["1 run"] == 1
        assert metrics.run_distribution["2 runs"] == 1
        assert metrics.run_distribution["3+ runs"] == 1

    def test_date_range(self, usage_file: Path) -> None:
        entries = [
            _make_entry(timestamp="2026-03-01T00:00:00+00:00"),
            _make_entry(timestamp="2026-04-15T00:00:00+00:00"),
        ]
        _write_entries(usage_file, entries)
        metrics = summarize_usage(usage_file)
        assert metrics.date_range == "2026-03-01 to 2026-04-15"

    def test_date_range_same_day(self, usage_file: Path) -> None:
        entries = [
            _make_entry(timestamp="2026-03-22T10:00:00+00:00"),
            _make_entry(timestamp="2026-03-22T14:00:00+00:00"),
        ]
        _write_entries(usage_file, entries)
        metrics = summarize_usage(usage_file)
        assert metrics.date_range == "2026-03-22"


# ---------------------------------------------------------------------------
# format_report() tests
# ---------------------------------------------------------------------------


class TestFormatReport:
    """Tests for the format_report() function."""

    def test_contains_header(self) -> None:
        metrics = AdoptionMetrics(
            total_runs=10,
            unique_sessions=5,
            date_range="2026-03-01 to 2026-03-10",
            trust_rate=0.8,
            return_rate=0.4,
            sharing_status="N/A (no sharing mechanism in skill prototype)",
            disagreement_pass_rate=0.9,
            attribution_pass_rate=0.85,
            fallback_rate=0.1,
            run_distribution={"1 run": 3, "2 runs": 1, "3+ runs": 1},
        )
        report = format_report(metrics)
        assert "Deliberator Adoption Gate Report" in report

    def test_contains_trust_rate(self) -> None:
        metrics = AdoptionMetrics(
            total_runs=10,
            unique_sessions=5,
            date_range="2026-03-01 to 2026-03-10",
            trust_rate=0.8,
            return_rate=0.4,
            sharing_status="N/A",
            disagreement_pass_rate=0.9,
            attribution_pass_rate=0.85,
            fallback_rate=0.1,
            run_distribution={},
        )
        report = format_report(metrics)
        assert "Trust Rate:" in report
        assert "80.0%" in report

    def test_contains_return_rate(self) -> None:
        metrics = AdoptionMetrics(
            total_runs=10,
            unique_sessions=5,
            date_range="2026-03-01 to 2026-03-10",
            trust_rate=0.8,
            return_rate=0.4,
            sharing_status="N/A",
            disagreement_pass_rate=0.9,
            attribution_pass_rate=0.85,
            fallback_rate=0.1,
            run_distribution={},
        )
        report = format_report(metrics)
        assert "Return Rate:" in report
        assert "40.0%" in report

    def test_contains_sharing(self) -> None:
        metrics = AdoptionMetrics(
            total_runs=0,
            unique_sessions=0,
            date_range="N/A",
            trust_rate=0.0,
            return_rate=0.0,
            sharing_status="N/A (no sharing mechanism in skill prototype)",
            disagreement_pass_rate=0.0,
            attribution_pass_rate=0.0,
            fallback_rate=0.0,
            run_distribution={},
        )
        report = format_report(metrics)
        assert "Sharing:" in report
        assert "N/A" in report

    def test_contains_quality_breakdown(self) -> None:
        metrics = AdoptionMetrics(
            total_runs=10,
            unique_sessions=5,
            date_range="2026-03-01 to 2026-03-10",
            trust_rate=0.8,
            return_rate=0.4,
            sharing_status="N/A",
            disagreement_pass_rate=0.9,
            attribution_pass_rate=0.85,
            fallback_rate=0.1,
            run_distribution={},
        )
        report = format_report(metrics)
        assert "Quality Breakdown:" in report
        assert "Disagreement gate:" in report
        assert "Attribution gate:" in report
        assert "Fallback used:" in report

    def test_contains_run_distribution(self) -> None:
        metrics = AdoptionMetrics(
            total_runs=6,
            unique_sessions=3,
            date_range="2026-03-22",
            trust_rate=1.0,
            return_rate=0.667,
            sharing_status="N/A",
            disagreement_pass_rate=1.0,
            attribution_pass_rate=1.0,
            fallback_rate=0.0,
            run_distribution={"1 run": 1, "2 runs": 1, "3+ runs": 1},
        )
        report = format_report(metrics)
        assert "Run Distribution:" in report
        assert "1 run:" in report
        assert "2 runs:" in report
        assert "3+ runs:" in report


# ---------------------------------------------------------------------------
# CLI tests
# ---------------------------------------------------------------------------


class TestCLILog:
    """Tests for the `log` CLI subcommand via subprocess."""

    def test_log_creates_jsonl(
        self,
        question_file: Path,
        synthesis_file: Path,
        quality_dict: dict,
        tmp_path: Path,
    ) -> None:
        usage_file = tmp_path / "cli_test" / "usage.jsonl"
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "linter.usage",
                "log",
                "--synthesis-path",
                str(synthesis_file),
                "--question-path",
                str(question_file),
                "--quality-json",
                json.dumps(quality_dict),
                "--fallback-used",
                "false",
                "--usage-file",
                str(usage_file),
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
        # Stdout should be valid JSON
        data = json.loads(result.stdout)
        assert data["version"] == 1
        # JSONL file should exist
        assert usage_file.exists()
        lines = [l for l in usage_file.read_text().strip().split("\n") if l]
        assert len(lines) == 1

    def test_log_with_session_id(
        self,
        question_file: Path,
        synthesis_file: Path,
        quality_dict: dict,
        tmp_path: Path,
    ) -> None:
        usage_file = tmp_path / "cli_sid" / "usage.jsonl"
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "linter.usage",
                "log",
                "--synthesis-path",
                str(synthesis_file),
                "--question-path",
                str(question_file),
                "--quality-json",
                json.dumps(quality_dict),
                "--fallback-used",
                "true",
                "--session-id",
                "cafebabe",
                "--usage-file",
                str(usage_file),
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert data["session_id"] == "cafebabe"
        assert data["fallback_used"] is True


class TestCLISummary:
    """Tests for the `summary` CLI subcommand via subprocess."""

    def test_summary_prints_report(self, tmp_path: Path) -> None:
        usage_file = tmp_path / "summary_test" / "usage.jsonl"
        _write_entries(usage_file, [_make_entry(), _make_entry(quality_passed=False)])
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "linter.usage",
                "summary",
                "--path",
                str(usage_file),
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "Deliberator Adoption Gate Report" in result.stdout
        assert "Trust Rate:" in result.stdout

    def test_summary_empty_file(self, tmp_path: Path) -> None:
        # Non-existent file — should produce zero-run report
        missing = tmp_path / "no_such" / "usage.jsonl"
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "linter.usage",
                "summary",
                "--path",
                str(missing),
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "Total runs: 0" in result.stdout


class TestCLIHelp:
    """Tests that --help works for the module and subcommands."""

    def test_module_help(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "linter.usage", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "log" in result.stdout
        assert "summary" in result.stdout

    def test_log_help(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "linter.usage", "log", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "--synthesis-path" in result.stdout
        assert "--question-path" in result.stdout
        assert "--quality-json" in result.stdout
        assert "--fallback-used" in result.stdout

    def test_summary_help(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "linter.usage", "summary", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "--path" in result.stdout
