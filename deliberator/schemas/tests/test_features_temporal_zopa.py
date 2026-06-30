"""Tests for AgentFeatures + RoundFeatures time-ranged ZOPA fields.

Spec 047 Phase 5 sub-integration #1: negotiation mode AgentFeatures
gain three temporal-constraint fields paired with the existing
price-based ZOPA fields, and RoundFeatures gains the
temporal-aggregate field.

The fields consume Duration parser output (PRs #82 Phase 1-4) by
converting Duration objects to seconds via `Duration.as_seconds()`.
This tests the schema additions; the upstream extraction logic
(AgentFeatures populated from agent positions during feature
extraction) is a separate consumer change.
"""

from __future__ import annotations

import pytest

from deliberator.schemas.duration import Duration, parse_temporal
from deliberator.schemas.features import AgentFeatures, RoundFeatures


# ---------------------------------------------------------------------------
# AgentFeatures temporal-ZOPA fields
# ---------------------------------------------------------------------------


class TestAgentFeaturesTemporalZopa:
    """Three new fields on AgentFeatures for time-ranged ZOPA."""

    def test_default_values_are_zero(self) -> None:
        """All three fields default to 0.0 (FR-003 graceful degrade)."""
        features = AgentFeatures(agent_name="alice")
        assert features.reservation_duration_seconds == 0.0
        assert features.aspiration_duration_seconds == 0.0
        assert features.temporal_zopa_overlap == 0.0

    def test_set_from_duration_as_seconds(self) -> None:
        """Duration objects feed the field via .as_seconds()."""
        reservation = Duration(days=30)
        aspiration = Duration(days=7)
        features = AgentFeatures(
            agent_name="alice",
            reservation_duration_seconds=reservation.as_seconds(),
            aspiration_duration_seconds=aspiration.as_seconds(),
        )
        # 30 days * 86400 seconds/day
        assert features.reservation_duration_seconds == 30 * 86400
        assert features.aspiration_duration_seconds == 7 * 86400

    def test_temporal_zopa_overlap_in_unit_range(self) -> None:
        """temporal_zopa_overlap is a fraction (0.0 to 1.0)."""
        features = AgentFeatures(
            agent_name="alice",
            temporal_zopa_overlap=0.7,
        )
        assert features.temporal_zopa_overlap == 0.7

    def test_pairs_with_price_based_zopa(self) -> None:
        """Temporal and price ZOPA fields coexist on the same agent."""
        features = AgentFeatures(
            agent_name="alice",
            # Price-based ZOPA
            reservation_price=100.0,
            aspiration_price=150.0,
            zopa_coverage=0.8,
            # Time-based ZOPA
            reservation_duration_seconds=Duration(days=30).as_seconds(),
            aspiration_duration_seconds=Duration(days=7).as_seconds(),
            temporal_zopa_overlap=0.5,
        )
        assert features.reservation_price == 100.0
        assert features.reservation_duration_seconds == 30 * 86400
        # Both ZOPA dimensions populated independently
        assert features.zopa_coverage == 0.8
        assert features.temporal_zopa_overlap == 0.5

    def test_frozen_model_immutable(self) -> None:
        """AgentFeatures is frozen — temporal fields participate."""
        features = AgentFeatures(
            agent_name="alice",
            reservation_duration_seconds=100.0,
        )
        with pytest.raises(Exception):
            features.reservation_duration_seconds = 200.0  # type: ignore[misc]


class TestRoundFeaturesTemporalZopa:
    """RoundFeatures gains the temporal aggregate field."""

    def test_default_value_is_zero(self) -> None:
        round_features = RoundFeatures(round_number=1)
        assert round_features.temporal_zopa_size_seconds == 0.0

    def test_pairs_with_price_zopa_size(self) -> None:
        """Temporal and price ZOPA-size fields coexist at round level."""
        round_features = RoundFeatures(
            round_number=2,
            zopa_size=50.0,  # price-based
            temporal_zopa_size_seconds=Duration(days=14).as_seconds(),
        )
        assert round_features.zopa_size == 50.0
        assert round_features.temporal_zopa_size_seconds == 14 * 86400


# ---------------------------------------------------------------------------
# Integration: Duration parser → AgentFeatures
# ---------------------------------------------------------------------------


class TestDurationParserIntegration:
    """End-to-end: extract temporal constraints, populate AgentFeatures."""

    def test_parse_negotiation_position_to_features(self) -> None:
        """Parse a negotiation position string, populate features."""
        # Simulate an agent position carrying a temporal constraint
        agent_position_text = "I want to close this deal within 30 days."
        matches = parse_temporal(agent_position_text)

        # parse_temporal returns at least one TemporalMatch
        assert len(matches) >= 1
        match = matches[0]
        assert match.duration is not None

        # Convert to seconds and populate features
        features = AgentFeatures(
            agent_name="alice",
            reservation_duration_seconds=match.duration.as_seconds(),
        )
        # 30 days * 86400 = 2,592,000 seconds
        assert features.reservation_duration_seconds == 30 * 86400

    def test_parse_two_party_zopa_overlap(self) -> None:
        """Two parties' temporal constraints — compute overlap fraction."""
        alice_text = "I need at least 30 days to close."
        bob_text = "I want to close within 60 days."

        alice_matches = parse_temporal(alice_text)
        bob_matches = parse_temporal(bob_text)

        # Both produce at least one match
        assert alice_matches and alice_matches[0].duration
        assert bob_matches and bob_matches[0].duration

        alice_seconds = alice_matches[0].duration.as_seconds()
        bob_seconds = bob_matches[0].duration.as_seconds()

        # Alice wants ≥30 days (reservation), Bob wants ≤60 days
        # ZOPA exists between 30 and 60 days. Overlap fraction
        # relative to Bob's range (0 to 60) = (60-30)/60 = 0.5
        overlap = max(0.0, (bob_seconds - alice_seconds) / bob_seconds)

        alice_features = AgentFeatures(
            agent_name="alice",
            reservation_duration_seconds=alice_seconds,
            temporal_zopa_overlap=overlap,
        )
        bob_features = AgentFeatures(
            agent_name="bob",
            aspiration_duration_seconds=bob_seconds,
            temporal_zopa_overlap=overlap,
        )

        # Assertion is on the schema's ability to carry the data,
        # not on the specific overlap calculation (which is the
        # caller's concern). The value is in unit range.
        assert 0.0 <= alice_features.temporal_zopa_overlap <= 1.0
        assert alice_features.temporal_zopa_overlap == 0.5
        assert bob_features.temporal_zopa_overlap == 0.5
