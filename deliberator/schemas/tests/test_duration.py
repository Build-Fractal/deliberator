"""Tests for :mod:`deliberator.schemas.duration` (spec 047 phases 1–4).

Covers:

* :class:`Duration` dataclass: ISO 8601 / timedelta / seconds, hashing,
  immutability.
* Tier 1 — ISO 8601 strict parsing.
* Tier 2 — Numeric + unit (singular, plural, fractional).
* Tier 3 — Colloquial vocabulary.
* Tier 4 — Fiscal / abstract markers.
* Tier 5 — Category inference via prefix keywords.
* Edge cases: empty, whitespace, unicode, mixed units, negative.
* Success criteria SC-001..SC-008 from the spec.
"""

from __future__ import annotations

import logging
import time
from datetime import timedelta
from typing import get_args

import pytest

from deliberator.schemas.duration import (
    Duration,
    TemporalCategory,
    TemporalMatch,
    parse_temporal,
)


# ---------------------------------------------------------------------------
# TestDurationDataclass
# ---------------------------------------------------------------------------


class TestDurationDataclass:
    """Duration dataclass: serialization, hashing, immutability."""

    def test_to_iso_8601_months(self) -> None:
        assert Duration(months=3).to_iso_8601() == "P3M"

    def test_to_iso_8601_hours_minutes(self) -> None:
        assert Duration(hours=2, minutes=30).to_iso_8601() == "PT2H30M"

    def test_to_iso_8601_full_year_month_day(self) -> None:
        # SC-005 — the spec's headline serialization example.
        assert Duration(months=3, days=15).to_iso_8601() == "P3M15D"

    def test_to_iso_8601_year_month_day(self) -> None:
        assert Duration(years=1, months=6, days=15).to_iso_8601() == "P1Y6M15D"

    def test_to_iso_8601_zero(self) -> None:
        assert Duration().to_iso_8601() == "PT0S"

    def test_to_iso_8601_milliseconds(self) -> None:
        # 100 ms should serialize as PT0.1S.
        assert Duration(milliseconds=100).to_iso_8601() == "PT0.1S"

    def test_to_iso_8601_seconds_plus_milliseconds(self) -> None:
        assert Duration(seconds=2, milliseconds=500).to_iso_8601() == "PT2.5S"

    def test_to_timedelta_days(self) -> None:
        assert Duration(days=7).to_timedelta() == timedelta(days=7)

    def test_to_timedelta_months_approximated(self) -> None:
        # 1 month = 30 days per documented approximation.
        assert Duration(months=1).to_timedelta() == timedelta(days=30)

    def test_to_timedelta_with_milliseconds(self) -> None:
        td = Duration(seconds=1, milliseconds=500).to_timedelta()
        assert td == timedelta(seconds=1, milliseconds=500)

    def test_as_seconds_minutes(self) -> None:
        assert Duration(minutes=2).as_seconds() == 120.0

    def test_as_seconds_year_approximation(self) -> None:
        # 1 year = 365 days × 86400 s.
        assert Duration(years=1).as_seconds() == 365 * 86400

    def test_hashable(self) -> None:
        a = Duration(months=3)
        b = Duration(months=3)
        s = {a, b}
        assert len(s) == 1  # equal hashable values collapse.

    def test_immutable(self) -> None:
        d = Duration(months=3)
        with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
            d.months = 6  # type: ignore[misc]

    def test_equality(self) -> None:
        assert Duration(months=3) == Duration(months=3)
        assert Duration(months=3) != Duration(months=4)


# ---------------------------------------------------------------------------
# TestParseTemporalTier1ISO8601
# ---------------------------------------------------------------------------


class TestParseTemporalTier1ISO8601:
    """Strict ISO 8601 duration literals."""

    def test_p3m(self) -> None:
        matches = parse_temporal("P3M")
        assert len(matches) == 1
        assert matches[0].duration == Duration(months=3)
        assert matches[0].confidence == 1.0

    def test_pt2h30m(self) -> None:
        matches = parse_temporal("PT2H30M")
        assert len(matches) == 1
        assert matches[0].duration == Duration(hours=2, minutes=30)
        assert matches[0].confidence == 1.0

    def test_p1y6m15d(self) -> None:
        matches = parse_temporal("P1Y6M15D")
        assert len(matches) == 1
        assert matches[0].duration == Duration(years=1, months=6, days=15)

    def test_iso_in_sentence(self) -> None:
        matches = parse_temporal("interval P3M between checks")
        assert any(m.duration == Duration(months=3) for m in matches)


# ---------------------------------------------------------------------------
# TestParseTemporalTier2Numeric
# ---------------------------------------------------------------------------


class TestParseTemporalTier2Numeric:
    """Numeric + unit parsing including fractional values."""

    def test_three_months(self) -> None:
        matches = parse_temporal("3 months")
        assert len(matches) == 1
        assert matches[0].duration == Duration(months=3)
        assert matches[0].confidence == 1.0

    def test_100ms(self) -> None:
        # SC-002 — milliseconds field populated.
        matches = parse_temporal("100ms")
        assert len(matches) == 1
        assert matches[0].duration == Duration(milliseconds=100)

    def test_five_minutes(self) -> None:
        matches = parse_temporal("5 minutes")
        assert matches[0].duration == Duration(minutes=5)

    def test_fractional_years_expand(self) -> None:
        # 1.5 years -> 1 year + 6 months
        matches = parse_temporal("1.5 years")
        assert len(matches) == 1
        assert matches[0].duration == Duration(years=1, months=6)

    def test_singular_unit(self) -> None:
        matches = parse_temporal("1 month")
        assert matches[0].duration == Duration(months=1)

    def test_short_unit_h(self) -> None:
        matches = parse_temporal("2h")
        assert matches[0].duration == Duration(hours=2)

    def test_short_unit_d(self) -> None:
        matches = parse_temporal("90d")
        assert matches[0].duration == Duration(days=90)


# ---------------------------------------------------------------------------
# TestParseTemporalTier3Colloquial
# ---------------------------------------------------------------------------


class TestParseTemporalTier3Colloquial:
    """Colloquial vocabulary."""

    def test_a_week(self) -> None:
        matches = parse_temporal("wait a week before retrying")
        assert any(m.duration == Duration(weeks=1) for m in matches)
        assert any(m.confidence == 0.9 for m in matches)

    def test_fortnight(self) -> None:
        matches = parse_temporal("come back in a fortnight")
        assert any(m.duration == Duration(weeks=2) for m in matches)

    def test_half_a_year(self) -> None:
        matches = parse_temporal("half a year of runway")
        assert any(m.duration == Duration(months=6) for m in matches)

    def test_overnight(self) -> None:
        matches = parse_temporal("overnight batch job")
        assert any(m.duration == Duration(hours=12) for m in matches)


# ---------------------------------------------------------------------------
# TestParseTemporalTier4Fiscal
# ---------------------------------------------------------------------------


class TestParseTemporalTier4Fiscal:
    """Fiscal / abstract markers — duration=None, category='deadline'."""

    def test_q2_2026(self) -> None:
        matches = parse_temporal("Q2 2026")
        # Filter to fiscal-derived match (duration is None).
        fiscal = [m for m in matches if m.duration is None]
        assert len(fiscal) >= 1
        assert fiscal[0].category == "deadline"

    def test_eoy(self) -> None:
        matches = parse_temporal("ship by EOY")
        assert any(m.duration is None and m.category == "deadline" for m in matches)

    def test_h1(self) -> None:
        matches = parse_temporal("plan for H1")
        assert any(m.duration is None and m.category == "deadline" for m in matches)

    def test_fy27(self) -> None:
        matches = parse_temporal("target FY27")
        assert any(m.duration is None and m.category == "deadline" for m in matches)


# ---------------------------------------------------------------------------
# TestParseTemporalTier5CategoryInference
# ---------------------------------------------------------------------------


class TestParseTemporalTier5CategoryInference:
    """Prefix-keyword category inference covering all 6 §2.2 rules."""

    def test_performance_under(self) -> None:
        # "under 100ms" without alert/trigger context -> performance
        matches = parse_temporal("response under 100ms")
        assert any(m.category == "performance" for m in matches)

    def test_latency_bound_within_alert(self) -> None:
        # "within 5 minutes" with trigger context -> latency_bound
        matches = parse_temporal("alert within 5 minutes of trigger")
        assert any(m.category == "latency_bound" for m in matches)

    def test_schedule_every(self) -> None:
        matches = parse_temporal("runs every hour")
        assert any(m.category == "schedule" for m in matches)

    def test_ttl_valid_for(self) -> None:
        matches = parse_temporal("token valid for 90 days")
        assert any(m.category == "ttl" for m in matches)

    def test_deadline_by(self) -> None:
        matches = parse_temporal("ship by 3 months")
        assert any(m.category == "deadline" for m in matches)

    def test_window_over_the_last(self) -> None:
        matches = parse_temporal("over the last 3 months we shipped")
        assert any(m.category == "window" for m in matches)

    def test_no_hint_default_duration(self) -> None:
        # Bare numeric — no surrounding keyword hint.
        matches = parse_temporal("3 months of data")
        assert any(m.category == "duration" for m in matches)


# ---------------------------------------------------------------------------
# TestParseTemporalEdgeCases
# ---------------------------------------------------------------------------


class TestParseTemporalEdgeCases:
    """FR-012..FR-016 edge cases."""

    def test_empty_string(self) -> None:
        assert parse_temporal("") == []

    def test_whitespace_only(self) -> None:
        assert parse_temporal("   \n\t  ") == []

    def test_garbage_no_temporal(self) -> None:
        assert parse_temporal("xyzzy plugh") == []

    def test_unicode_does_not_crash(self) -> None:
        # FR-012 — emoji and non-ascii must not crash.
        matches = parse_temporal("3 months 🚀")
        assert any(m.duration == Duration(months=3) for m in matches)

    def test_mixed_units(self) -> None:
        # FR-014 — "2 weeks 3 days" merges into single Duration.
        matches = parse_temporal("2 weeks 3 days")
        # Expect exactly one merged numeric match.
        numeric = [m for m in matches if m.duration is not None]
        assert len(numeric) == 1
        assert numeric[0].duration == Duration(weeks=2, days=3)

    def test_negative_duration_dropped(self, caplog) -> None:
        # FR-015 — negative durations dropped + warning logged.
        with caplog.at_level(logging.WARNING):
            matches = parse_temporal("minus 3 days")
        assert all(m.duration != Duration(days=3) for m in matches)
        assert any("negative" in rec.message.lower() for rec in caplog.records)

    def test_timezone_token_ignored(self) -> None:
        # FR-016 — "EST" must not crash; "3pm" alone isn't a duration.
        matches = parse_temporal("meeting at 3pm EST")
        # No mass crash; we don't assert anything beyond stability.
        assert isinstance(matches, list)


# ---------------------------------------------------------------------------
# TestParseTemporalSCs — explicit success-criteria coverage
# ---------------------------------------------------------------------------


class TestParseTemporalSCs:
    """Each SC from spec §5."""

    def test_sc_001_ship_in_3_months_by_q2(self) -> None:
        # SC-001 — 2 matches: a numeric duration and a fiscal Q2.
        matches = parse_temporal("ship in 3 months by Q2")
        durations = [m for m in matches if m.duration is not None]
        fiscals = [m for m in matches if m.duration is None]
        assert any(m.duration == Duration(months=3) for m in durations)
        assert any(m.category == "deadline" for m in fiscals)

    def test_sc_002_response_under_100ms(self) -> None:
        matches = parse_temporal("response under 100ms")
        assert any(
            m.category == "performance"
            and m.duration == Duration(milliseconds=100)
            for m in matches
        )

    def test_sc_003_valid_for_90_days(self) -> None:
        matches = parse_temporal("valid for 90 days")
        assert any(
            m.category == "ttl" and m.duration == Duration(days=90)
            for m in matches
        )

    def test_sc_004_runs_every_hour(self) -> None:
        matches = parse_temporal("runs every hour")
        assert any(
            m.category == "schedule" and m.duration == Duration(hours=1)
            for m in matches
        )

    def test_sc_005_iso_serialization(self) -> None:
        assert Duration(months=3, days=15).to_iso_8601() == "P3M15D"

    def test_sc_006_classifier_backward_compat(self) -> None:
        # Backward-compat boolean preserved (full coverage in classifier
        # tests; this is a smoke check).
        from linter.question_classifier import has_constraints

        assert has_constraints("ship by 3 months") is True

    def test_sc_007_garbage_returns_empty(self) -> None:
        assert parse_temporal("") == []
        assert parse_temporal("   ") == []
        assert parse_temporal("???") == []

    def test_sc_008_categories_closed_literal(self) -> None:
        # Indirectly proves FR-006 — Literal members are exactly the seven.
        members = set(get_args(TemporalCategory))
        assert members == {
            "deadline",
            "performance",
            "schedule",
            "ttl",
            "window",
            "latency_bound",
            "duration",
        }


# ---------------------------------------------------------------------------
# TestPerformance
# ---------------------------------------------------------------------------


class TestPerformance:
    """SC-008 — parser must keep up with regex-fast budgets."""

    def test_1000_char_input_under_10ms(self) -> None:
        # Build a realistic 1000-char input mixing temporal references.
        chunk = (
            "Ship in 3 months by Q2 2026; alerts within 5 minutes; "
            "tokens valid for 90 days; runs every hour. "
        )
        text = (chunk * 20)[:1000]
        # Warm up to avoid first-call import cost.
        parse_temporal(text)
        start = time.perf_counter()
        for _ in range(5):
            parse_temporal(text)
        elapsed_ms = ((time.perf_counter() - start) / 5) * 1000.0
        assert elapsed_ms < 10.0, f"avg parse took {elapsed_ms:.2f} ms (>10 ms)"


# ---------------------------------------------------------------------------
# TestOverlapResolution — FR-005
# ---------------------------------------------------------------------------


class TestOverlapResolution:
    """Tier 2 wins over Tier 3 when spans overlap."""

    def test_three_months_beats_a_month(self) -> None:
        matches = parse_temporal("3 months")
        # Tier 2 numeric should win — colloquial "a month" doesn't even
        # fire here, but if both fired we should see only the higher-conf
        # match in the output.
        durations = [m.duration for m in matches if m.duration is not None]
        assert Duration(months=3) in durations
        # No surviving Duration(months=1) from a hypothetical "a month".
        assert Duration(months=1) not in durations


# ---------------------------------------------------------------------------
# TestTemporalMatchType
# ---------------------------------------------------------------------------


class TestTemporalMatchType:
    """TemporalMatch dataclass shape and immutability."""

    def test_fields(self) -> None:
        m = TemporalMatch(
            raw_text="3 months",
            duration=Duration(months=3),
            category="duration",
            confidence=1.0,
            start_pos=0,
            end_pos=8,
        )
        assert m.raw_text == "3 months"
        assert m.duration == Duration(months=3)

    def test_immutable(self) -> None:
        m = TemporalMatch(
            raw_text="3 months",
            duration=Duration(months=3),
            category="duration",
            confidence=1.0,
            start_pos=0,
            end_pos=8,
        )
        with pytest.raises(Exception):
            m.confidence = 0.5  # type: ignore[misc]
