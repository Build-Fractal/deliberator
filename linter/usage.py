"""
Usage logging and adoption-gate metric reporting for deliberator runs.

Logs structured JSONL entries per Just Ask run to ``~/.deliberator/usage.jsonl``
and computes adoption gate metrics (trust rate, return rate, sharing
indicators) for the summary reporter.

Public API:
    log_usage(synthesis_path, question_path, quality_json, fallback_used, ...) -> UsageEntry
    summarize_usage(path) -> AdoptionMetrics
    format_report(metrics) -> str

Models:
    UsageEntry, AdoptionMetrics

CLI:
    python3 -m linter.usage log  --synthesis-path ... --question-path ... --quality-json '...' --fallback-used false
    python3 -m linter.usage summary [--path ...]
"""

from __future__ import annotations

import hashlib
import json
import os
import secrets
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel

from linter.utils import word_count as _word_count


# ---------------------------------------------------------------------------
# Default paths
# ---------------------------------------------------------------------------

DEFAULT_USAGE_DIR: Path = Path.home() / ".deliberator"
DEFAULT_USAGE_FILE: Path = DEFAULT_USAGE_DIR / "usage.jsonl"


# ---------------------------------------------------------------------------
# Pydantic models — frozen per Constitution Principle IX
# ---------------------------------------------------------------------------


class UsageEntry(BaseModel):
    """A single usage-log entry appended as one JSONL line per run."""

    model_config = {"frozen": True}

    version: int = 1
    timestamp: str
    session_id: str
    question_hash: str
    question_word_count: int
    preset_mode: str
    agent_names: list[str]
    iterations: int
    quality_passed: bool
    disagreement_passed: bool
    attributions_passed: bool
    dispute_count: int
    fallback_used: bool
    phases_completed: int
    agent_count: int


class AdoptionMetrics(BaseModel):
    """Aggregated adoption-gate metrics computed from the JSONL log."""

    model_config = {"frozen": True}

    total_runs: int
    unique_sessions: int
    date_range: str
    trust_rate: float
    return_rate: float
    sharing_status: str
    disagreement_pass_rate: float
    attribution_pass_rate: float
    fallback_rate: float
    run_distribution: dict[str, int]
    corrupt_lines: int = 0


class SynthesisMeta(BaseModel):
    """Metadata extracted from a synthesis file for usage logging."""

    model_config = {"frozen": True}

    preset_mode: str = "cooperative"
    agent_names: list[str] = []
    iterations: int = 1
    phases_completed: int = 5


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _hash_question(text: str) -> str:
    """Return first 16 hex chars of SHA-256 of *text*."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _parse_synthesis_meta(synthesis_path: Path) -> SynthesisMeta:
    """Extract preset_mode, agent_names, iterations, phases_completed from a synthesis file.

    Falls back to sensible defaults when the synthesis file is missing or
    the expected markers are absent.
    """
    preset_mode = "cooperative"
    agent_names: list[str] = []
    iterations = 1
    phases_completed = 5

    try:
        text = synthesis_path.read_text(encoding="utf-8")
    except (FileNotFoundError, OSError):
        return SynthesisMeta()

    # Try to extract agent names from scorecard rows: | XX-R1 | AgentName |
    import re

    agent_pattern = re.compile(
        r"\|\s*[A-Z]{1,3}-[A-Z]?\d+\s*\|\s*([A-Za-z\s\-\']+?)\s*\|"
    )
    agents_found: list[str] = []
    seen: set[str] = set()
    for m in agent_pattern.finditer(text):
        name = m.group(1).strip()
        if name and name.lower() not in seen:
            seen.add(name.lower())
            agents_found.append(name)
    if agents_found:
        agent_names = agents_found

    # Detect mode from text hints
    for mode in ("cooperative", "winner-take-all", "prisoners-dilemma", "red-blue"):
        if mode in text.lower():
            preset_mode = mode
            break

    return SynthesisMeta(
        preset_mode=preset_mode,
        agent_names=agent_names,
        iterations=iterations,
        phases_completed=phases_completed,
    )


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------


def log_usage(
    synthesis_path: str | Path,
    question_path: str | Path,
    quality_json: dict | str,
    fallback_used: bool,
    *,
    session_id: str | None = None,
    usage_file: str | Path | None = None,
) -> UsageEntry:
    """Log one usage entry to the JSONL file and return it.

    Note: JSONL append is not protected by file locking. This is acceptable
    for the M001 single-user prototype. For concurrent access in M002+,
    add fcntl.flock or switch to SQLite.

    Args:
        synthesis_path: Path to the synthesis markdown output.
        question_path: Path to the question file (used for hash/word count).
        quality_json: Quality gate result dict or JSON string with keys
            ``passed``, ``disagreement`` (with ``passed`` and ``dispute_count``),
            ``attributions`` (with ``passed``).
        fallback_used: Whether a fallback mechanism was triggered.
        session_id: Optional 8-char hex session id; generated if absent.
        usage_file: Override for the JSONL target file (default ``~/.deliberator/usage.jsonl``).

    Returns:
        The ``UsageEntry`` that was appended.

    Raises:
        FileNotFoundError: If *question_path* does not exist.
    """
    synthesis_path = Path(synthesis_path)
    question_path = Path(question_path)

    # --- Question metrics (privacy-safe: hash + word count only) -----------
    question_text = question_path.read_text(encoding="utf-8")
    q_hash = _hash_question(question_text)
    q_wc = _word_count(question_text)

    # --- Quality gate fields ------------------------------------------------
    if isinstance(quality_json, str):
        quality_json = json.loads(quality_json)

    quality_passed: bool = bool(quality_json.get("passed", False))

    disagreement = quality_json.get("disagreement", {})
    disagreement_passed: bool = bool(disagreement.get("passed", False))
    dispute_count: int = int(disagreement.get("dispute_count", 0))

    attributions = quality_json.get("attributions", {})
    attributions_passed: bool = bool(attributions.get("passed", False))

    # --- Synthesis metadata --------------------------------------------------
    meta = _parse_synthesis_meta(synthesis_path)

    # --- Entry ---------------------------------------------------------------
    entry = UsageEntry(
        timestamp=datetime.now(timezone.utc).isoformat(),
        session_id=session_id or secrets.token_hex(4),
        question_hash=q_hash,
        question_word_count=q_wc,
        preset_mode=meta.preset_mode,
        agent_names=meta.agent_names,
        iterations=meta.iterations,
        quality_passed=quality_passed,
        disagreement_passed=disagreement_passed,
        attributions_passed=attributions_passed,
        dispute_count=dispute_count,
        fallback_used=fallback_used,
        phases_completed=meta.phases_completed,
        agent_count=len(meta.agent_names),
    )

    # --- Append to JSONL ----------------------------------------------------
    target = Path(usage_file) if usage_file else DEFAULT_USAGE_FILE
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("a", encoding="utf-8") as f:
            f.write(entry.model_dump_json() + "\n")
    except OSError as exc:
        import sys
        print(
            f"Warning: could not persist usage entry: {exc}",
            file=sys.stderr,
        )

    return entry


def summarize_usage(path: str | Path | None = None) -> AdoptionMetrics:
    """Read the JSONL log and compute adoption-gate metrics.

    Args:
        path: Path to the JSONL file (default ``~/.deliberator/usage.jsonl``).

    Returns:
        ``AdoptionMetrics`` with trust rate, return rate, sharing status, etc.
    """
    target = Path(path) if path else DEFAULT_USAGE_FILE

    entries: list[dict] = []
    corrupt_lines = 0
    try:
        with target.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        corrupt_lines += 1
    except FileNotFoundError:
        pass

    total = len(entries)
    if total == 0:
        return AdoptionMetrics(
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
            corrupt_lines=corrupt_lines,
        )

    # --- Dates ---------------------------------------------------------------
    timestamps = sorted(e.get("timestamp", "") for e in entries)
    first_date = timestamps[0][:10] if timestamps else "N/A"
    last_date = timestamps[-1][:10] if timestamps else "N/A"
    date_range = f"{first_date} to {last_date}" if first_date != last_date else first_date

    # --- Trust rate -----------------------------------------------------------
    trust_passed = sum(1 for e in entries if e.get("quality_passed"))
    trust_rate = trust_passed / total

    # --- Return rate ----------------------------------------------------------
    session_counts: Counter[str] = Counter(e.get("session_id", "") for e in entries)
    unique_sessions = len(session_counts)
    returning_sessions = sum(1 for c in session_counts.values() if c > 1)
    return_rate = returning_sessions / unique_sessions if unique_sessions > 0 else 0.0

    # --- Quality breakdown ----------------------------------------------------
    disagreement_passed = sum(1 for e in entries if e.get("disagreement_passed"))
    attribution_passed = sum(1 for e in entries if e.get("attributions_passed"))
    fallback_count = sum(1 for e in entries if e.get("fallback_used"))

    # --- Run distribution -----------------------------------------------------
    one_run = sum(1 for c in session_counts.values() if c == 1)
    two_runs = sum(1 for c in session_counts.values() if c == 2)
    three_plus = sum(1 for c in session_counts.values() if c >= 3)
    run_distribution = {
        "1 run": one_run,
        "2 runs": two_runs,
        "3+ runs": three_plus,
    }

    return AdoptionMetrics(
        total_runs=total,
        unique_sessions=unique_sessions,
        date_range=date_range,
        trust_rate=trust_rate,
        return_rate=return_rate,
        sharing_status="N/A (no sharing mechanism in skill prototype)",
        disagreement_pass_rate=disagreement_passed / total,
        attribution_pass_rate=attribution_passed / total,
        fallback_rate=fallback_count / total,
        run_distribution=run_distribution,
        corrupt_lines=corrupt_lines,
    )


def format_report(metrics: AdoptionMetrics) -> str:
    """Format adoption metrics into the human-readable report.

    The output matches the format defined in S07-RESEARCH.md.
    """
    lines: list[str] = [
        "Deliberator Adoption Gate Report",
        "=" * 30,
        f"Total runs: {metrics.total_runs}",
        f"Unique sessions: {metrics.unique_sessions}",
        f"Date range: {metrics.date_range}",
        "",
    ]

    # Trust rate
    trust_num = round(metrics.trust_rate * metrics.total_runs)
    lines.append(
        f"Trust Rate: {metrics.trust_rate:.1%} "
        f"({trust_num}/{metrics.total_runs} passed quality gates)"
    )

    # Return rate
    returning = round(metrics.return_rate * metrics.unique_sessions)
    lines.append(
        f"Return Rate: {metrics.return_rate:.1%} "
        f"({returning}/{metrics.unique_sessions} sessions had >1 run)"
    )

    # Sharing
    lines.append(f"Sharing: {metrics.sharing_status}")
    lines.append("")

    # Quality breakdown
    lines.append("Quality Breakdown:")
    lines.append(f"  Disagreement gate: {metrics.disagreement_pass_rate:.1%} pass rate")
    lines.append(f"  Attribution gate: {metrics.attribution_pass_rate:.1%} pass rate")
    lines.append(f"  Fallback used: {metrics.fallback_rate:.1%} of runs")
    lines.append("")

    # Run distribution
    lines.append("Run Distribution:")
    for bucket, count in metrics.run_distribution.items():
        lines.append(f"  {bucket}: {count} sessions")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI entry point — invoked via `python3 -m linter.usage <subcommand>`
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        prog="linter.usage",
        description="Deliberator usage logger and adoption-gate reporter.",
    )
    subparsers = parser.add_subparsers(dest="command")

    # --- log subcommand ------------------------------------------------------
    log_parser = subparsers.add_parser("log", help="Log a usage entry to JSONL.")
    log_parser.add_argument(
        "--synthesis-path",
        required=True,
        help="Path to the synthesis output markdown file.",
    )
    log_parser.add_argument(
        "--question-path",
        required=True,
        help="Path to the question file.",
    )
    log_parser.add_argument(
        "--quality-json",
        required=True,
        help="Quality gate result as a JSON string.",
    )
    log_parser.add_argument(
        "--fallback-used",
        required=True,
        choices=["true", "false"],
        help="Whether a fallback mechanism was triggered.",
    )
    log_parser.add_argument(
        "--session-id",
        default=None,
        help="Optional 8-char hex session id.",
    )
    log_parser.add_argument(
        "--usage-file",
        default=None,
        help="Override for the JSONL target file.",
    )

    # --- summary subcommand --------------------------------------------------
    summary_parser = subparsers.add_parser(
        "summary", help="Print adoption-gate metrics report."
    )
    summary_parser.add_argument(
        "--path",
        default=None,
        help="Path to the JSONL file (default: ~/.deliberator/usage.jsonl).",
    )

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    if args.command == "log":
        fallback = args.fallback_used == "true"
        try:
            entry = log_usage(
                synthesis_path=args.synthesis_path,
                question_path=args.question_path,
                quality_json=args.quality_json,
                fallback_used=fallback,
                session_id=args.session_id,
                usage_file=args.usage_file,
            )
        except FileNotFoundError as exc:
            print(json.dumps({"error": str(exc)}), file=sys.stderr)
            sys.exit(2)
        except (json.JSONDecodeError, ValueError) as exc:
            print(json.dumps({"error": f"Invalid quality-json: {exc}"}), file=sys.stderr)
            sys.exit(3)

        print(entry.model_dump_json(indent=2))
        sys.exit(0)

    if args.command == "summary":
        try:
            metrics = summarize_usage(path=args.path)
        except Exception as exc:
            print(json.dumps({"error": str(exc)}), file=sys.stderr)
            sys.exit(1)

        print(format_report(metrics))
        sys.exit(0)
