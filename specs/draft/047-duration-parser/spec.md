# Feature Specification: Structured Duration Parser & Temporal Constraint Classifier

**Feature ID**: `047-duration-parser`
**Created**: 2026-04-04
**Status**: Draft
**Depends On**: `linter/question_classifier.py` (current regex-based temporal detection)
**Docs Update**: New docs/developer-guide/duration-parsing.md; update linter docs with the new classifier API
**Origin**: Bug #4 fix (plural time units) exposed a deeper architectural gap. The regex-based `_CONSTRAINT_PATTERN` detects a limited vocabulary and returns no structured data. Downstream consumers (AMPL negotiation solver, scenario storage, feature extraction) need durations as **structured values**, not just pattern matches.

---

## 1. Problem

`linter/question_classifier.py::_CONSTRAINT_PATTERN` currently uses a regex pattern to detect temporal constraints:

```python
r"\b(?:months?|years?|weeks?|days?)\b"
```

This has three problems:

### Problem 1: Limited vocabulary

The pattern covers 4 time units (`day`, `week`, `month`, `year`). Missing:
- **Sub-day**: `hour`, `minute`, `second`, `millisecond`
- **Large**: `quarter`, `decade`
- **Colloquial**: `fortnight`, `biweekly`, `semester`
- **Fiscal**: `Q1`, `Q2`, `H1`, `FY26`, `EOD`, `EOW`, `EOM`, `EOQ`, `EOY`

Adding each unit to the regex is an exponential scope-creep trap — the pattern grows, edge cases multiply, and the regex becomes unreadable.

### Problem 2: No structured output

Even when the regex matches, the classifier returns **boolean**. Downstream code can't distinguish:
- "3 months" (a constraint of magnitude 3 months)
- "30 years" (a constraint of magnitude 30 years)

The classifier knows both are constraints but can't tell you **how long**.

### Problem 3: Category blur

The classifier currently treats all temporal references as equivalent, but they serve different semantic purposes:

| Phrase | Category | Example use |
|--------|----------|-------------|
| "Ship by Q2 2026" | **Deadline** | Planning constraint — project completion target |
| "Response under 100ms" | **Performance** | SLO/SLA — runtime behavior |
| "Runs every hour" | **Schedule** | Recurrence — cron, scheduled jobs |
| "Valid for 90 days" | **TTL** | Expiration — token lifetime, cache duration |
| "Over the last 3 months" | **Window** | Retrospective range — analytics, reports |
| "Within 5 minutes of trigger" | **Latency bound** | Reactive constraint — alert response |

Treating these as the same "constraint" category loses information. A deadline and a performance target have completely different implications for deliberation (and for AMPL models — e.g., the negotiation mode's ZOPA has a time dimension that is a TTL, not a deadline).

---

## 2. Solution: Replace the regex with a structured duration parser

### 2.1 New module: `conversus/schemas/duration.py`

Pure-function duration parser that takes a string and returns a structured result:

```python
from dataclasses import dataclass
from typing import Literal
from datetime import timedelta
import re

TemporalCategory = Literal[
    "deadline",          # "by Q2", "before Friday"
    "performance",       # "under 100ms", "less than 5 seconds"
    "schedule",          # "every hour", "daily at 9am"
    "ttl",               # "valid for 90 days", "expires in 7d"
    "window",            # "over the last 3 months"
    "latency_bound",     # "within 5 minutes"
    "duration",          # bare duration, no semantic hint
]

@dataclass(frozen=True)
class Duration:
    """Structured duration with ISO 8601 serialization support."""
    years: int = 0
    months: int = 0
    weeks: int = 0
    days: int = 0
    hours: int = 0
    minutes: int = 0
    seconds: int = 0

    def to_iso_8601(self) -> str:
        """Serialize to ISO 8601 duration (e.g., 'P3M', 'PT2H30M')."""
        ...

    def to_timedelta(self) -> timedelta:
        """Convert to timedelta (approximate for months/years)."""
        ...

    def as_seconds(self) -> float:
        """Total seconds (approximate — 1 month = 30 days, 1 year = 365 days)."""
        ...

@dataclass(frozen=True)
class TemporalMatch:
    """Result of parsing a temporal reference from text."""
    raw_text: str                      # Original matched text, e.g., "3 months"
    duration: Duration | None          # Parsed duration, None for deadlines like "Q2"
    category: TemporalCategory
    confidence: float                  # 0.0-1.0 — regex match is 1.0, NLP-inferred is lower
    start_pos: int                     # Character position in source string
    end_pos: int

def parse_temporal(text: str) -> list[TemporalMatch]:
    """Parse all temporal references from a string.

    Returns a list of matches (possibly empty). Handles:
    - Numeric durations: "3 months", "90 days", "5 minutes"
    - Colloquial: "a week", "half a year", "fortnight"
    - Fiscal: "Q2 2026", "H1", "EOY"
    - Category hints: "by Friday" (deadline), "every hour" (schedule), "under 100ms" (performance)
    - ISO 8601: "P3M", "PT2H30M"
    """
    ...
```

### 2.2 Parsing strategies

The parser uses **layered strategies** with explicit confidence scores:

**Tier 1: ISO 8601 strict parsing** (confidence 1.0)
```
P3M        → Duration(months=3), category="duration"
PT2H30M    → Duration(hours=2, minutes=30), category="duration"
```

**Tier 2: Numeric + unit** (confidence 1.0)
```
"3 months"     → Duration(months=3)
"2 weeks"      → Duration(weeks=2)
"90 days"      → Duration(days=90)
"100ms"        → Duration(seconds=0.1)  (or milliseconds field)
"5 minutes"    → Duration(minutes=5)
"1.5 years"    → Duration(years=1, months=6)  (fractional expansion)
```

**Tier 3: Colloquial** (confidence 0.9)
```
"a week"       → Duration(weeks=1)
"half a year"  → Duration(months=6)
"fortnight"    → Duration(weeks=2)
"overnight"    → Duration(hours=12)
"next quarter" → Duration(months=3)  (with category="deadline")
```

**Tier 4: Fiscal/abstract** (confidence 0.8)
```
"Q2 2026"      → duration=None, category="deadline", absolute_date hint
"EOY"          → duration=None, category="deadline"
"EOQ"          → duration=None, category="deadline"
"by FY27"      → duration=None, category="deadline"
```

**Tier 5: Category inference** (confidence 0.7)

Uses surrounding context to classify:
- `"under|less than|max|at most"` + duration → `category="performance"` or `"latency_bound"`
- `"every|each|per"` + duration → `category="schedule"`
- `"valid for|expires in|TTL"` + duration → `category="ttl"`
- `"by|before|deadline|due"` + duration/fiscal → `category="deadline"`
- `"over the last|in the past|during"` + duration → `category="window"`
- No hint → `category="duration"` (bare)

### 2.3 Classifier integration

Update `linter/question_classifier.py::has_constraints()`:

```python
from conversus.schemas.duration import parse_temporal

def has_constraints(text: str) -> bool:
    """True if text contains any planning constraint, including temporal."""
    # Existing non-temporal detection...
    if _NON_TEMPORAL_PATTERN.search(text):
        return True
    # Temporal: use structured parser
    matches = parse_temporal(text)
    return any(
        m.category in ("deadline", "ttl", "window", "latency_bound")
        for m in matches
    )

def extract_temporal_constraints(text: str) -> list[TemporalMatch]:
    """Return structured temporal constraints (for feature extraction)."""
    return parse_temporal(text)
```

The old regex-based `_CONSTRAINT_PATTERN` is deleted. The boolean `has_constraints()` API is preserved for backward compatibility, but a new `extract_temporal_constraints()` returns the structured data.

---

## 3. Why structured duration matters downstream

### 3.1 Feature extraction for negotiation mode

The negotiation mode's ZOPA (Zone of Possible Agreement) has a time dimension in many real deliberations ("we need this in 3 months" vs "we need this in 18 months"). Current `AgentFeatures.zopa_coverage` is a scalar — it can't represent time-ranged ZOPAs.

With structured durations, feature extraction can populate:
```python
class NegotiationAgentFeatures:
    zopa_time_min: Duration  # earliest acceptable delivery
    zopa_time_max: Duration  # latest acceptable delivery
    time_reservation: Duration  # walk-away time constraint
```

The AMPL negotiation solver (spec 043) then optimizes over a time-bounded ZOPA directly.

### 3.2 Scenario storage

Scenarios accumulate over time. Queries like "show me all deliberations where an agent claimed a <1 week deadline" require structured durations — you can't do this with regex matches.

### 3.3 Commentator agents (spec 046)

Play-by-play commentators reference timing ("this deliberation took 45 minutes — the cross-review phase alone ate 28 of those"). Color commentary notes patterns ("FP-guru is faster than SDET by a 2:1 margin, but SDET's revisions are more durable"). Both need structured duration data.

### 3.4 Governance mode (spec 048)

Spec 048 (autonomous governance) includes SLA-style rules in constitutions: "PR reviews must complete within 24 hours." The arbiter enforces these by comparing deliberation timestamps against constitution-declared durations. Regex won't work — the arbiter needs arithmetic.

---

## 4. Functional Requirements

### Parser
- **FR-001**: `parse_temporal(text)` MUST return a list of `TemporalMatch` objects (empty list if no matches).
- **FR-002**: The parser MUST handle all 5 tiers (ISO 8601, numeric+unit, colloquial, fiscal, category inference) with confidence scores.
- **FR-003**: `Duration` MUST be a frozen dataclass (immutable, hashable).
- **FR-004**: `Duration.to_iso_8601()` MUST produce valid ISO 8601 durations.
- **FR-005**: Overlapping matches MUST be resolved by preferring higher confidence (e.g., "3 months" matches Tier 2 before "a month" matches Tier 3).

### Categorization
- **FR-006**: The 7 `TemporalCategory` values MUST be a closed `Literal` type (no runtime strings).
- **FR-007**: Category inference MUST use surrounding context (prefix/suffix keywords) with documented keyword lists.
- **FR-008**: When no category hint is found, the default MUST be `"duration"` (bare).

### Classifier integration
- **FR-009**: `has_constraints(text)` MUST preserve backward compatibility — all existing tests that check the boolean result MUST still pass.
- **FR-010**: A new function `extract_temporal_constraints(text)` MUST expose the structured matches.
- **FR-011**: The old `_CONSTRAINT_PATTERN` regex MUST be removed (no dead code).

### Edge cases
- **FR-012**: Unicode input (e.g., "3 months 🚀") MUST be handled without crashing.
- **FR-013**: Malformed input (empty string, whitespace only, random garbage) MUST return an empty list.
- **FR-014**: Mixed units ("2 weeks 3 days") MUST parse into a single `Duration(weeks=2, days=3)`.
- **FR-015**: Negative durations ("minus 3 days") MUST NOT be silently accepted — return an empty match and log a warning.
- **FR-016**: Timezone references ("at 3pm EST") are OUT OF SCOPE for v1.

---

## 5. Success Criteria

- **SC-001**: `parse_temporal("ship in 3 months by Q2")` returns 2 matches: one `duration=Duration(months=3)` with category `"duration"` or `"deadline"`, and one `duration=None, category="deadline"` for "Q2".
- **SC-002**: `parse_temporal("response under 100ms")` returns 1 match with `category="performance"`, `duration=Duration(milliseconds=100)` (or equivalent).
- **SC-003**: `parse_temporal("valid for 90 days")` returns 1 match with `category="ttl"`, `duration=Duration(days=90)`.
- **SC-004**: `parse_temporal("runs every hour")` returns 1 match with `category="schedule"`, `duration=Duration(hours=1)`.
- **SC-005**: `Duration(months=3, days=15).to_iso_8601() == "P3M15D"`.
- **SC-006**: All existing `has_constraints()` tests pass unchanged (backward compat).
- **SC-007**: Empty, whitespace-only, and garbage input return `[]` without raising.
- **SC-008**: Parse time for a 1000-character string is under 10ms (regex-fast).

---

## 6. Constraints

- **Pure function**: no I/O, no timezone lookups, no network calls. Deterministic.
- **No external dependencies** in v1 — pure Python stdlib. Consider `python-dateutil` in v2 if edge cases justify it.
- **Timezones are out of scope** — durations are context-free (no "3pm EST"). Absolute times become category `"deadline"` with `duration=None`.
- **Backward compatibility** — `has_constraints()` returns the same boolean for all current test inputs.
- **No NLP** in v1 — pure regex + rule-based inference. No transformer models, no embeddings.

---

## 7. Phasing

### Phase 1: Core parser (~2 days)
- `conversus/schemas/duration.py` with `Duration`, `TemporalMatch`, `TemporalCategory`, `parse_temporal()`
- Tiers 1-2 (ISO 8601 + numeric) with full test coverage
- `Duration.to_iso_8601()`, `to_timedelta()`, `as_seconds()`

### Phase 2: Colloquial + fiscal (~1 day)
- Tier 3 (colloquial: "a week", "fortnight", "half a year")
- Tier 4 (fiscal: Q1-Q4, H1-H2, FY, EOY/EOW/EOD)
- Confidence scoring

### Phase 3: Category inference (~1 day)
- Tier 5 (keyword-based category inference)
- Documented keyword lists per category

### Phase 4: Classifier integration (~1 day)
- Replace `_CONSTRAINT_PATTERN` in `linter/question_classifier.py`
- Preserve `has_constraints()` boolean API
- Add `extract_temporal_constraints()` structured API
- Update all affected tests (the 10 cases added in Bug #4 fix plus any new behavioral tests)

### Phase 5: Downstream integration (~2 days, separate follow-up)
- Negotiation mode `AgentFeatures` fields for time-ranged ZOPA
- Scenario storage queries on structured durations
- Commentator agent access to deliberation timing
- Defer governance SLA enforcement to spec 048

---

## 8. Open Questions

1. **Should `Duration` support fractional units?** E.g., `Duration(hours=2.5)` vs `Duration(hours=2, minutes=30)`.
   - **Lean**: Integer-only, with fractional inputs normalized. "1.5 hours" → `Duration(hours=1, minutes=30)`.

2. **Millisecond precision?** `Duration.milliseconds` as a field? Or just use `Duration(seconds=0.1)`?
   - **Lean**: Add `milliseconds` field explicitly. Performance-category matches need ms granularity ("100ms response").

3. **Ambiguity resolution**: "in a month" could be `duration` or `deadline` depending on context. How hard to lean into disambiguation?
   - **Lean**: When ambiguous, return the match with category `"duration"` and confidence ~0.7. Callers that need disambiguation can run a follow-up check.

4. **Should fiscal quarters expand to concrete dates?** "Q2 2026" → `date(2026, 4, 1)` to `date(2026, 6, 30)`?
   - **Lean**: No. Fiscal quarters vary by company (some Q2 starts in April, some in May). Return `duration=None, category="deadline"` and let the caller resolve against their fiscal calendar.

5. **Natural language ranges**: "between 3 and 6 months"?
   - **Lean**: Return 2 matches, one for each bound. Let the caller reconstruct the range. Or add a `DurationRange` type in v2.

6. **Should the parser be async-safe?** Threading considerations?
   - **Lean**: Pure function, no state. Thread-safe by construction.

7. **Internationalization**: Non-English temporal expressions ("3 mois", "一ヶ月")?
   - **Lean**: Out of scope for v1. Structure the code so a locale parameter can be added later.

8. **Should `parse_temporal` integrate with `python-dateutil`?**
   - **Lean**: No in v1 (zero dependencies). Revisit if users report edge cases.

---

## 9. Relationship to Other Specs

- **Spec 039 (new mode payoffs)**: Negotiation mode's `zopa_coverage` is a scalar today. With structured durations, it becomes a time-ranged interval. This spec unblocks that.
- **Spec 043 (AMPL game solvers)**: The negotiation ZOPA solver needs bounded time intervals as constraints. Cannot work with regex matches.
- **Spec 046 (commentator agents)**: Play-by-play narration references timing. "Phase 3 took 15 minutes" requires structured durations.
- **Spec 048 (autonomous governance)**: Governance rules often include SLA-style durations ("reviews within 24 hours"). Arbiter enforcement requires arithmetic over durations.
- **Spec 020 (scenario storage)**: Cross-run queries like "show deliberations with <1 week deadlines" require structured durations in the storage layer.

---

## 10. Non-Goals

- Natural language generation of durations ("3 months" from a `Duration(months=3)`). That's for commentator agents.
- Calendar math (business days, holidays). Use a dedicated library if needed.
- Timezone conversion. Out of scope.
- Fuzzy temporal matching ("around a month or so"). Return the best structured match with reduced confidence.
