"""Structured duration parser and temporal constraint classifier (spec 047).

This module replaces the old regex-based ``_CONSTRAINT_PATTERN`` in
``linter.question_classifier`` with a layered, structured parser that returns
:class:`Duration` and :class:`TemporalMatch` values suitable for downstream
consumers (negotiation feature extraction, scenario storage queries,
commentator timing references, governance SLA enforcement).

Design constraints (spec 047 §6):

* Pure functions — no I/O, no timezone lookups, no network.
* Python stdlib only — no ``python-dateutil``, no NLP/transformer models.
* Deterministic and thread-safe by construction.
* Backward-compatible with the existing ``has_constraints()`` boolean API.

Public API:

* :class:`Duration` — frozen dataclass with ISO 8601 / timedelta / seconds
  serialization helpers.
* :class:`TemporalMatch` — a single parsed temporal reference with category
  and confidence.
* :data:`TemporalCategory` — closed ``Literal`` type covering the seven
  semantic categories (FR-006).
* :func:`parse_temporal` — top-level entry point. Returns a possibly-empty
  list of :class:`TemporalMatch`.

The parser applies five tiers in priority order (Tier 1 highest confidence):

1. ISO 8601 strict (``P3M``, ``PT2H30M``).
2. Numeric + unit (``"3 months"``, ``"100ms"``, ``"1.5 years"``).
3. Colloquial (``"a week"``, ``"fortnight"``, ``"half a year"``).
4. Fiscal/abstract (``"Q2 2026"``, ``"H1"``, ``"EOY"``, ``"FY27"``).
5. Category inference from prefix/suffix keywords applied on top of any
   match produced by tiers 1–3.

Overlapping matches are resolved by preferring higher confidence (FR-005);
ties go to the earlier-starting span.
"""

from __future__ import annotations

import logging
import math
import re
from dataclasses import dataclass, field
from datetime import timedelta
from typing import Literal

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Public types
# ---------------------------------------------------------------------------


TemporalCategory = Literal[
    "deadline",
    "performance",
    "schedule",
    "ttl",
    "window",
    "latency_bound",
    "duration",
]


_VALID_CATEGORIES: frozenset[str] = frozenset(
    {
        "deadline",
        "performance",
        "schedule",
        "ttl",
        "window",
        "latency_bound",
        "duration",
    }
)


@dataclass(frozen=True)
class Duration:
    """Structured duration with ISO 8601 / timedelta serialization (spec 047 §2.1).

    All fields are non-negative integers. Negative durations are rejected at
    parse time (FR-015) — direct construction with negative values is
    permitted only because we cannot validate inside a frozen dataclass
    without ``__post_init__`` mutating state, but parser output never
    produces them.
    """

    years: int = 0
    months: int = 0
    weeks: int = 0
    days: int = 0
    hours: int = 0
    minutes: int = 0
    seconds: int = 0
    milliseconds: int = 0  # See SC-002 — performance-category needs ms granularity.

    # ----- Serialization -------------------------------------------------

    def to_iso_8601(self) -> str:
        """Serialize to an ISO 8601 duration literal.

        Examples:
            >>> Duration(months=3).to_iso_8601()
            'P3M'
            >>> Duration(hours=2, minutes=30).to_iso_8601()
            'PT2H30M'
            >>> Duration(months=3, days=15).to_iso_8601()
            'P3M15D'
            >>> Duration().to_iso_8601()
            'PT0S'
        """
        date_parts: list[str] = []
        if self.years:
            date_parts.append(f"{self.years}Y")
        if self.months:
            date_parts.append(f"{self.months}M")
        if self.weeks:
            date_parts.append(f"{self.weeks}W")
        if self.days:
            date_parts.append(f"{self.days}D")

        time_parts: list[str] = []
        if self.hours:
            time_parts.append(f"{self.hours}H")
        if self.minutes:
            time_parts.append(f"{self.minutes}M")
        # Combine seconds + milliseconds into a fractional seconds component
        # for ISO 8601 fidelity (e.g. PT0.1S for 100 ms).
        if self.seconds or self.milliseconds:
            if self.milliseconds:
                total = self.seconds + self.milliseconds / 1000.0
                # Trim trailing zeros for readability (0.1 not 0.100).
                rendered = f"{total:.3f}".rstrip("0").rstrip(".")
                if not rendered:
                    rendered = "0"
                time_parts.append(f"{rendered}S")
            else:
                time_parts.append(f"{self.seconds}S")

        if not date_parts and not time_parts:
            return "PT0S"

        out = "P" + "".join(date_parts)
        if time_parts:
            out += "T" + "".join(time_parts)
        return out

    def to_timedelta(self) -> timedelta:
        """Convert to ``datetime.timedelta`` (months/years approximated).

        Approximations: 1 month = 30 days, 1 year = 365 days. These match
        the convention used by :meth:`as_seconds` and are documented as
        approximate in spec 047 §2.1.
        """
        days = (
            self.years * 365
            + self.months * 30
            + self.weeks * 7
            + self.days
        )
        return timedelta(
            days=days,
            hours=self.hours,
            minutes=self.minutes,
            seconds=self.seconds,
            milliseconds=self.milliseconds,
        )

    def as_seconds(self) -> float:
        """Total duration in seconds (approximate for months/years).

        Uses the same approximation as :meth:`to_timedelta`.
        """
        return self.to_timedelta().total_seconds()


@dataclass(frozen=True)
class TemporalMatch:
    """A single temporal reference parsed from input text (spec 047 §2.1)."""

    raw_text: str
    duration: Duration | None
    category: TemporalCategory
    confidence: float
    start_pos: int
    end_pos: int


# ---------------------------------------------------------------------------
# Tier 1 — ISO 8601 strict
# ---------------------------------------------------------------------------

# Match a complete ISO 8601 duration literal as a standalone token.
# Date part: years/months/weeks/days. Time part: hours/minutes/seconds.
# Requires at least one component after P (or PT).
_ISO_8601_PATTERN = re.compile(
    r"\bP"
    r"(?:(?P<years>\d+)Y)?"
    r"(?:(?P<months>\d+)M)?"
    r"(?:(?P<weeks>\d+)W)?"
    r"(?:(?P<days>\d+)D)?"
    r"(?:T"
    r"(?:(?P<hours>\d+)H)?"
    r"(?:(?P<minutes>\d+)M)?"
    r"(?:(?P<seconds>\d+(?:\.\d+)?)S)?"
    r")?"
    r"\b"
)


def _parse_iso_8601(text: str) -> list[TemporalMatch]:
    matches: list[TemporalMatch] = []
    for m in _ISO_8601_PATTERN.finditer(text):
        # Reject empty "P" (no components matched). Every named group must
        # be checked — if all are None, this is just the bare letter P.
        groups = m.groupdict()
        if not any(v is not None for v in groups.values()):
            continue
        # Reject literal token "P" with no T and no date parts (rare).
        raw = m.group(0)
        if raw == "P" or raw == "PT":
            continue
        seconds_total = 0
        milliseconds_total = 0
        if groups["seconds"] is not None:
            sec_val = float(groups["seconds"])
            seconds_total = int(sec_val)
            milliseconds_total = int(round((sec_val - seconds_total) * 1000))
        duration = Duration(
            years=int(groups["years"] or 0),
            months=int(groups["months"] or 0),
            weeks=int(groups["weeks"] or 0),
            days=int(groups["days"] or 0),
            hours=int(groups["hours"] or 0),
            minutes=int(groups["minutes"] or 0),
            seconds=seconds_total,
            milliseconds=milliseconds_total,
        )
        matches.append(
            TemporalMatch(
                raw_text=raw,
                duration=duration,
                category="duration",
                confidence=1.0,
                start_pos=m.start(),
                end_pos=m.end(),
            )
        )
    return matches


# ---------------------------------------------------------------------------
# Tier 2 — Numeric + unit (singular and plural, with optional fractional)
# ---------------------------------------------------------------------------


# Map every recognised unit token to a canonical Duration field.
_UNIT_FIELDS: dict[str, str] = {
    # Years
    "year": "years",
    "years": "years",
    "yr": "years",
    "yrs": "years",
    "y": "years",
    # Months
    "month": "months",
    "months": "months",
    "mo": "months",
    "mos": "months",
    # Weeks
    "week": "weeks",
    "weeks": "weeks",
    "wk": "weeks",
    "wks": "weeks",
    "w": "weeks",
    # Days
    "day": "days",
    "days": "days",
    "d": "days",
    # Hours
    "hour": "hours",
    "hours": "hours",
    "hr": "hours",
    "hrs": "hours",
    "h": "hours",
    # Minutes
    "minute": "minutes",
    "minutes": "minutes",
    "min": "minutes",
    "mins": "minutes",
    # Seconds
    "second": "seconds",
    "seconds": "seconds",
    "sec": "seconds",
    "secs": "seconds",
    "s": "seconds",
    # Milliseconds
    "millisecond": "milliseconds",
    "milliseconds": "milliseconds",
    "millisec": "milliseconds",
    "ms": "milliseconds",
}


# Sort longer units first to prefer "ms" over "m", "min" over "m", etc.
_UNIT_TOKENS_SORTED: list[str] = sorted(_UNIT_FIELDS.keys(), key=len, reverse=True)
_UNIT_ALTERNATION: str = "|".join(re.escape(tok) for tok in _UNIT_TOKENS_SORTED)

_NUMERIC_UNIT_PATTERN = re.compile(
    rf"(?<![A-Za-z0-9])"
    rf"(?P<num>\d+(?:\.\d+)?)\s*(?P<unit>{_UNIT_ALTERNATION})"
    rf"(?![A-Za-z])",
    re.IGNORECASE,
)


# Conversion factors used to expand fractional values into integer remainders.
# Each tuple lists the smaller fields a fractional value should overflow into,
# along with the multiplier to convert from the source unit.
_FRACTIONAL_OVERFLOW: dict[str, list[tuple[str, float]]] = {
    "years": [("months", 12.0)],
    "months": [("days", 30.0)],
    "weeks": [("days", 7.0)],
    "days": [("hours", 24.0)],
    "hours": [("minutes", 60.0)],
    "minutes": [("seconds", 60.0)],
    "seconds": [("milliseconds", 1000.0)],
    "milliseconds": [],
}


def _expand_numeric(value: float, field_name: str) -> dict[str, int]:
    """Expand a possibly-fractional value into integer Duration fields.

    For example, ``_expand_numeric(1.5, "years")`` yields
    ``{"years": 1, "months": 6}``. Sub-second fractions of milliseconds are
    rounded to the nearest integer ms.
    """
    out: dict[str, int] = {}
    whole = int(value)
    remainder = value - whole
    out[field_name] = whole

    chain = _FRACTIONAL_OVERFLOW.get(field_name, [])
    current = remainder
    for next_field, multiplier in chain:
        if current <= 0:
            break
        next_val = current * multiplier
        next_whole = int(next_val)
        if next_whole > 0:
            out[next_field] = out.get(next_field, 0) + next_whole
        current = next_val - next_whole

    # Anything that survives is rounded into the smallest field of the chain
    # to avoid silently dropping precision.
    if chain and current > 0.5:
        last_field = chain[-1][0]
        out[last_field] = out.get(last_field, 0) + 1
    return out


def _parse_numeric_unit(text: str) -> list[TemporalMatch]:
    matches: list[TemporalMatch] = []
    for m in _NUMERIC_UNIT_PATTERN.finditer(text):
        num_str = m.group("num")
        unit_str = m.group("unit").lower()
        field_name = _UNIT_FIELDS.get(unit_str)
        if field_name is None:
            continue
        try:
            value = float(num_str)
        except ValueError:
            continue
        if value <= 0:
            continue
        fields = _expand_numeric(value, field_name)
        duration = Duration(**fields)  # type: ignore[arg-type]
        matches.append(
            TemporalMatch(
                raw_text=m.group(0),
                duration=duration,
                category="duration",
                confidence=1.0,
                start_pos=m.start(),
                end_pos=m.end(),
            )
        )
    return matches


# ---------------------------------------------------------------------------
# Tier 3 — Colloquial
# ---------------------------------------------------------------------------


# Order matters — multi-word phrases are listed first so they are matched
# before their shorter constituents (e.g. "half a year" before "a year").
_COLLOQUIAL_TERMS: list[tuple[str, Duration]] = [
    # "every hour" / "every day" — bare unit names with no article take the
    # singular Duration. Listed before fragments to win the longest-match
    # race when prefixed by a schedule keyword (every/each/per).
    ("every year", Duration(years=1)),
    ("every quarter", Duration(months=3)),
    ("every month", Duration(months=1)),
    ("every fortnight", Duration(weeks=2)),
    ("every week", Duration(weeks=1)),
    ("every day", Duration(days=1)),
    ("every hour", Duration(hours=1)),
    ("every minute", Duration(minutes=1)),
    ("every second", Duration(seconds=1)),
    ("each year", Duration(years=1)),
    ("each month", Duration(months=1)),
    ("each week", Duration(weeks=1)),
    ("each day", Duration(days=1)),
    ("each hour", Duration(hours=1)),
    ("per year", Duration(years=1)),
    ("per month", Duration(months=1)),
    ("per week", Duration(weeks=1)),
    ("per day", Duration(days=1)),
    ("per hour", Duration(hours=1)),
    ("per minute", Duration(minutes=1)),
    ("per second", Duration(seconds=1)),
    ("half a year", Duration(months=6)),
    ("half a month", Duration(weeks=2)),
    ("half a week", Duration(days=3, hours=12)),
    ("half a day", Duration(hours=12)),
    ("half an hour", Duration(minutes=30)),
    ("half a minute", Duration(seconds=30)),
    ("a couple of years", Duration(years=2)),
    ("a couple of months", Duration(months=2)),
    ("a couple of weeks", Duration(weeks=2)),
    ("a couple of days", Duration(days=2)),
    ("a couple of hours", Duration(hours=2)),
    ("a couple of minutes", Duration(minutes=2)),
    ("next quarter", Duration(months=3)),
    ("this quarter", Duration(months=3)),
    ("a fortnight", Duration(weeks=2)),
    ("fortnight", Duration(weeks=2)),
    ("biweekly", Duration(weeks=2)),
    ("a semester", Duration(months=4)),
    ("semester", Duration(months=4)),
    ("a decade", Duration(years=10)),
    ("decade", Duration(years=10)),
    ("a century", Duration(years=100)),
    ("century", Duration(years=100)),
    ("overnight", Duration(hours=12)),
    ("a year", Duration(years=1)),
    ("a month", Duration(months=1)),
    ("a week", Duration(weeks=1)),
    ("a day", Duration(days=1)),
    ("an hour", Duration(hours=1)),
    ("a minute", Duration(minutes=1)),
    ("a second", Duration(seconds=1)),
]


# Pre-compile a single combined regex so we can preserve match order by
# position. We escape each phrase and join with alternation. Whitespace
# between words must be flexible.
def _build_colloquial_regex() -> re.Pattern[str]:
    parts: list[str] = []
    for phrase, _ in _COLLOQUIAL_TERMS:
        # Replace runs of whitespace with \s+ so multiple spaces still match.
        escaped = r"\s+".join(re.escape(w) for w in phrase.split())
        parts.append(escaped)
    pattern = r"\b(?:" + "|".join(parts) + r")\b"
    return re.compile(pattern, re.IGNORECASE)


_COLLOQUIAL_PATTERN = _build_colloquial_regex()
_COLLOQUIAL_LOOKUP: dict[str, Duration] = {p.lower(): d for p, d in _COLLOQUIAL_TERMS}


def _parse_colloquial(text: str) -> list[TemporalMatch]:
    matches: list[TemporalMatch] = []
    for m in _COLLOQUIAL_PATTERN.finditer(text):
        raw = m.group(0)
        # Normalise internal whitespace for lookup.
        normalized = " ".join(raw.lower().split())
        duration = _COLLOQUIAL_LOOKUP.get(normalized)
        if duration is None:
            # Try every key — handles the case where the regex collapsed
            # whitespace differently than the lookup key.
            for key, val in _COLLOQUIAL_LOOKUP.items():
                if normalized == key:
                    duration = val
                    break
        if duration is None:
            continue
        matches.append(
            TemporalMatch(
                raw_text=raw,
                duration=duration,
                category="duration",
                confidence=0.9,
                start_pos=m.start(),
                end_pos=m.end(),
            )
        )
    return matches


# ---------------------------------------------------------------------------
# Tier 4 — Fiscal / abstract
# ---------------------------------------------------------------------------


_FISCAL_PATTERN = re.compile(
    r"\b(?:"
    r"Q[1-4](?:\s*\d{2,4})?"      # Q1, Q2 2026
    r"|H[12](?:\s*\d{2,4})?"      # H1, H2 2026
    r"|FY\s*\d{2,4}"               # FY27, FY 2027
    r"|EO[DWMQY]"                   # EOD, EOW, EOM, EOQ, EOY
    r"|end\s+of\s+(?:day|week|month|quarter|year)"
    r")\b",
    re.IGNORECASE,
)


def _parse_fiscal(text: str) -> list[TemporalMatch]:
    matches: list[TemporalMatch] = []
    for m in _FISCAL_PATTERN.finditer(text):
        matches.append(
            TemporalMatch(
                raw_text=m.group(0),
                duration=None,
                category="deadline",
                confidence=0.8,
                start_pos=m.start(),
                end_pos=m.end(),
            )
        )
    return matches


# ---------------------------------------------------------------------------
# Tier 5 — Category inference (keyword-based)
# ---------------------------------------------------------------------------


# Each tuple: (compiled keyword pattern, category, applies-to-prefix?, latency-context-marker?).
# Prefix patterns look at the text immediately before the match; suffix
# patterns look at the text immediately after.
_PERFORMANCE_PREFIX = re.compile(
    r"(?:under|less\s+than|max(?:imum)?|at\s+most|no\s+more\s+than|"
    r"sub-?|fewer\s+than|below|faster\s+than|quicker\s+than|"
    r"response\s+(?:in|under|within)|within)\s*$",
    re.IGNORECASE,
)
_LATENCY_CONTEXT = re.compile(
    r"\b(?:within|alert|trigger|notify|fire|escalate|page)\b",
    re.IGNORECASE,
)
_SCHEDULE_PREFIX = re.compile(
    r"(?:every|each|per|once\s+(?:a|every))\s*$",
    re.IGNORECASE,
)
_TTL_PREFIX = re.compile(
    r"(?:valid\s+for|expires?\s+(?:in|after)|TTL(?:\s+of)?|cache(?:d)?\s+for|"
    r"good\s+for|lasts?\s+for|persists?\s+for|retain(?:ed)?\s+for|"
    r"keeps?\s+for|stores?\s+for)\s*$",
    re.IGNORECASE,
)
_DEADLINE_PREFIX = re.compile(
    r"(?:by|before|deadline\s+(?:of|is)?|due\s+(?:by|in)?|"
    r"ship(?:s|ped)?\s+by|deliver(?:s|ed)?\s+by|complete\s+by|"
    r"finish(?:ed)?\s+by|launch(?:es|ed)?\s+by)\s*$",
    re.IGNORECASE,
)
_WINDOW_PREFIX = re.compile(
    r"(?:over\s+the\s+(?:last|past)|in\s+the\s+(?:last|past)|"
    r"during\s+(?:the\s+)?(?:last|past)?|for\s+the\s+(?:last|past)|"
    r"throughout\s+(?:the\s+)?(?:last|past)?)\s*$",
    re.IGNORECASE,
)


_SCHEDULE_INTRINSIC = re.compile(
    r"^(?:every|each|per|once\s+(?:a|every))\b",
    re.IGNORECASE,
)
_LATENCY_INTRINSIC = re.compile(
    r"^within\b",
    re.IGNORECASE,
)


def _classify_category(text: str, match: TemporalMatch) -> tuple[TemporalCategory, float]:
    """Apply Tier 5 inference to upgrade the category of an existing match.

    Returns the inferred ``(category, confidence)`` pair. Confidence is
    lowered to 0.7 only when we move *away* from the structured tier's
    high-confidence ``"duration"`` default — fiscal matches stay at 0.8
    and category-inferred numeric matches drop to 0.7 per spec §2.2 Tier 5.
    """
    # Look at up to 40 chars before the match for prefix keywords.
    prefix = text[max(0, match.start_pos - 40) : match.start_pos]
    raw = match.raw_text

    # Intrinsic checks — when the keyword sits *inside* the match itself
    # (e.g. colloquial "every hour" or "within 5 minutes" forms).
    if _LATENCY_INTRINSIC.search(raw):
        window = text[max(0, match.start_pos - 80) : min(len(text), match.end_pos + 80)]
        if _LATENCY_CONTEXT.search(window) or "within" in raw.lower():
            return ("latency_bound", 0.7)
    if _SCHEDULE_INTRINSIC.search(raw):
        return ("schedule", 0.7)

    # Performance / latency_bound — both share the "under/less than" prefix.
    if _PERFORMANCE_PREFIX.search(prefix):
        # Latency-bound when the surrounding window mentions alert/trigger
        # context. Look at the full sentence-ish window.
        window = text[max(0, match.start_pos - 80) : min(len(text), match.end_pos + 80)]
        if _LATENCY_CONTEXT.search(window):
            return ("latency_bound", 0.7)
        return ("performance", 0.7)

    if _SCHEDULE_PREFIX.search(prefix):
        return ("schedule", 0.7)

    if _TTL_PREFIX.search(prefix):
        return ("ttl", 0.7)

    if _DEADLINE_PREFIX.search(prefix):
        return ("deadline", 0.7)

    if _WINDOW_PREFIX.search(prefix):
        return ("window", 0.7)

    # No hint — keep current category and confidence.
    return (match.category, match.confidence)


# ---------------------------------------------------------------------------
# Negative-duration sentinel
# ---------------------------------------------------------------------------


_NEGATIVE_PREFIX = re.compile(
    r"(?:minus|negative|-)\s*$",
    re.IGNORECASE,
)


def _is_negative(text: str, match: TemporalMatch) -> bool:
    prefix = text[max(0, match.start_pos - 20) : match.start_pos]
    return bool(_NEGATIVE_PREFIX.search(prefix))


# ---------------------------------------------------------------------------
# Overlap resolution (FR-005)
# ---------------------------------------------------------------------------


def _spans_overlap(a: TemporalMatch, b: TemporalMatch) -> bool:
    return a.start_pos < b.end_pos and b.start_pos < a.end_pos


def _resolve_overlaps(matches: list[TemporalMatch]) -> list[TemporalMatch]:
    """Greedy overlap resolution: prefer higher confidence, then earlier start.

    With matches sorted by (-confidence, start_pos) we walk the list and
    accept each match whose span does not collide with any already-accepted
    span. This matches FR-005's requirement that "3 months" (Tier 2, 1.0)
    wins over "a month" (Tier 3, 0.9) when both touch the same characters.
    """
    if not matches:
        return matches
    ranked = sorted(
        matches,
        key=lambda m: (-m.confidence, m.start_pos, -(m.end_pos - m.start_pos)),
    )
    accepted: list[TemporalMatch] = []
    for m in ranked:
        if any(_spans_overlap(m, kept) for kept in accepted):
            continue
        accepted.append(m)
    accepted.sort(key=lambda m: m.start_pos)
    return accepted


# ---------------------------------------------------------------------------
# Mixed-unit merging
# ---------------------------------------------------------------------------


def _merge_adjacent(text: str, matches: list[TemporalMatch]) -> list[TemporalMatch]:
    """Merge adjacent same-tier numeric matches into a single Duration.

    "2 weeks 3 days" appears as two non-overlapping Tier 2 matches whose
    spans are separated only by whitespace. FR-014 requires a single
    ``Duration(weeks=2, days=3)`` result.

    Two matches are considered adjacent when:
      * Both have ``confidence == 1.0`` (Tier 1/2).
      * The gap between them in the source text is whitespace and/or the
        word "and" (case-insensitive) only.
      * Their durations touch disjoint Duration fields (no double-count).
    """
    if len(matches) < 2:
        return matches

    by_pos = sorted(matches, key=lambda m: m.start_pos)
    merged: list[TemporalMatch] = []
    i = 0
    while i < len(by_pos):
        current = by_pos[i]
        # Try to absorb successors.
        while i + 1 < len(by_pos):
            nxt = by_pos[i + 1]
            if current.confidence != 1.0 or nxt.confidence != 1.0:
                break
            if current.duration is None or nxt.duration is None:
                break
            gap = text[current.end_pos : nxt.start_pos]
            if not re.fullmatch(r"\s*(?:,\s*|and\s+)?\s*", gap, re.IGNORECASE):
                break
            combined = _combine_durations(current.duration, nxt.duration)
            if combined is None:
                break
            current = TemporalMatch(
                raw_text=text[current.start_pos : nxt.end_pos],
                duration=combined,
                category=current.category,
                confidence=current.confidence,
                start_pos=current.start_pos,
                end_pos=nxt.end_pos,
            )
            i += 1
        merged.append(current)
        i += 1
    return merged


def _combine_durations(a: Duration, b: Duration) -> Duration | None:
    """Combine two Durations field-wise; return None if any field collides."""
    fields_a = _duration_to_dict(a)
    fields_b = _duration_to_dict(b)
    overlap = {
        k for k in fields_a if fields_a[k] > 0 and fields_b.get(k, 0) > 0
    }
    if overlap:
        return None
    combined = {k: fields_a.get(k, 0) + fields_b.get(k, 0) for k in fields_a | fields_b.keys()}
    return Duration(**combined)


def _duration_to_dict(d: Duration) -> dict[str, int]:
    return {
        "years": d.years,
        "months": d.months,
        "weeks": d.weeks,
        "days": d.days,
        "hours": d.hours,
        "minutes": d.minutes,
        "seconds": d.seconds,
        "milliseconds": d.milliseconds,
    }


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def parse_temporal(text: str) -> list[TemporalMatch]:
    """Parse all temporal references from *text*.

    Returns a possibly-empty list of :class:`TemporalMatch`. Never raises;
    invalid or empty input yields ``[]`` (FR-013, SC-007).

    See :mod:`conversus.schemas.duration` for tier and category semantics.
    """
    if not text or not text.strip():
        return []

    raw_matches: list[TemporalMatch] = []
    raw_matches.extend(_parse_iso_8601(text))
    raw_matches.extend(_parse_numeric_unit(text))
    raw_matches.extend(_parse_colloquial(text))
    fiscal_matches = _parse_fiscal(text)

    # Drop negative-duration matches with a warning (FR-015). We do this
    # before overlap resolution so a negated "minus 3 days" does not block
    # a legitimate later match.
    filtered: list[TemporalMatch] = []
    for m in raw_matches:
        if _is_negative(text, m):
            logger.warning(
                "Negative duration detected and discarded: %r at %d-%d",
                m.raw_text,
                m.start_pos,
                m.end_pos,
            )
            continue
        filtered.append(m)

    # Merge adjacent numeric matches before overlap resolution so the
    # combined span participates in tie-breaking against colloquial spans.
    filtered = _merge_adjacent(text, filtered)

    all_matches = filtered + fiscal_matches
    resolved = _resolve_overlaps(all_matches)

    # Apply Tier 5 category inference to every surviving match. Fiscal
    # matches are already "deadline" — only override if the prefix gives
    # us stronger evidence (e.g. "every Q1" → schedule).
    upgraded: list[TemporalMatch] = []
    for m in resolved:
        new_category, new_confidence = _classify_category(text, m)
        if new_category != m.category:
            m = TemporalMatch(
                raw_text=m.raw_text,
                duration=m.duration,
                category=new_category,
                confidence=new_confidence,
                start_pos=m.start_pos,
                end_pos=m.end_pos,
            )
        upgraded.append(m)

    return upgraded


__all__ = [
    "Duration",
    "TemporalCategory",
    "TemporalMatch",
    "parse_temporal",
]
