# Structural Definitions for Conversus Quality Gates

This document defines the two primary quality gates for conversus cooperative deliberation output as parseable structural properties. These definitions are used by the S02 quality checker to programmatically validate that conversus output meets minimum quality standards.

---

## Quality Gate 1: Substantive Disagreement

### Definition

A conversus deliberation output contains **substantive disagreement** when agents recommend *different actions* or reach *opposing conclusions* on at least one dimension of the target question, and this disagreement survives the full deliberation process (through cross-review, revision, and dispute phases) as a formally documented remaining dispute.

**What counts as substantive:**
- Agents recommend different actions (e.g., "hard 3-month deadline" vs. "data-triggered gates with no fixed deadline")
- Agents reach opposing conclusions on a factual matter relevant to the decision (e.g., "migration takes 4-8 weeks" vs. "migration takes 3-4 months")
- Agents assign incompatible interpretive weight to the same evidence (e.g., "children are a wear-and-tear cost" vs. "children are a planning-horizon risk factor")

**What does NOT count as substantive:**
- Stylistic disagreements (different formatting or organization of the same recommendation)
- Formatting preferences (table vs. prose, bulleted vs. numbered)
- Trivially different phrasings of the same recommendation
- Disputes about the deliberation framework itself (e.g., "this question shouldn't need a full pipeline")
- Manufactured disagreement on factual questions where a single correct answer exists

### Primary Marker: Dispute Block

The synthesis template requires disputes to be placed within machine-parseable delimiters:

```
<!-- CONVERSUS:DISPUTES_BEGIN -->
### Remaining Disputes
...
<!-- CONVERSUS:DISPUTES_END -->
```

Within this block, each dispute is headed by:

```
**Dispute: [Label]**
```

or (heading variant):

```
#### Dispute: [Label]
```

**Regex patterns for machine parsing:**

```python
# Detect dispute block boundaries
DISPUTES_BEGIN = r'<!--\s*CONVERSUS:DISPUTES_BEGIN\s*-->'
DISPUTES_END = r'<!--\s*CONVERSUS:DISPUTES_END\s*-->'

# Count individual disputes within the block
DISPUTE_MARKER = r'(?:^|\n)\s*(?:\*\*Dispute:\s*|#{1,4}\s*Dispute:\s*)(.+?)(?:\*\*)?$'

# Verify dispute contains agent positions (at least 2 named agents)
DISPUTE_POSITION = r'\*([A-Za-z\s\-\']+?)(?:\s+position)?:\*\s+'
```

**Detection algorithm:**

1. Find the `DISPUTES_BEGIN` marker. If absent, the output fails the dispute-block gate.
2. Extract text between `DISPUTES_BEGIN` and `DISPUTES_END`.
3. Count matches of `DISPUTE_MARKER` within the extracted block.
4. For each dispute, verify that at least 2 distinct agent names appear with attributed positions.
5. Exclude the special case where the disputes section explicitly states "None" or "no remaining disputes" — this is valid output for factual questions but fails the substantive disagreement gate for deliberative questions.

### Secondary Marker: Recommendation Scorecard Status

The Recommendation Scorecard table may contain a `Final Status` column with the value `Disputed`:

```python
# Detect disputed recommendations in scorecard
DISPUTED_STATUS = r'\|\s*\*\*Disputed\*\*\s*\|'
```

A `Disputed` status in the scorecard should correspond to a named dispute in the disputes block. Mismatches indicate synthesis quality issues.

### Examples from Real Output

**Example 1 — Monorepo synthesis, "Deferral Timeline Shape" dispute:**

```markdown
**Dispute: Deferral Timeline Shape**

**Positions:**
- *Pragmatist:* Hard 3-month outer bound with a 6-8 week early checkpoint. Calendar date forces revisit even if data is ambiguous. Prevents organizational inertia from converting "defer" into "never decide."
- *Devil's Advocate:* 6-8 week validation window with explicit instrumentation. Data-triggered gates, no arbitrary deadline. If signal is clear at week 8, a month-6 deadline wastes decision bandwidth.
```

This is a **substantive** dispute: agents recommend different decision mechanisms (fixed deadline vs. data-triggered gates) for the same decision point.

**Example 2 — Lease synthesis, "Spec Directional Neutrality" dispute:**

```markdown
#### Dispute: Spec Directional Neutrality

**Pragmatist position:** The asker's profile overwhelmingly favors buying on every historical TCO comparison. Stating this in the spec is honest prior information, not bias. The cost model will confirm what the profile suggests.

**Devil's Advocate position:** A spec that requires a neutral cost model while telegraphing "buying is the expected answer" invites confirmation bias in the answering agent.
```

This is a **substantive** dispute: agents hold opposing positions on whether providing directional guidance constitutes legitimate prior information or methodological bias.

**Example 3 — Factual-capital synthesis, no disputes (negative control):**

```markdown
### Remaining Disputes

**None.**

There are no remaining disputes. Both agents declared this independently in Phase 4, and the synthesizer concurs.
```

This correctly produces **zero** substantive disagreements. The quality gate for substantive disagreement should **fail** for this output, confirming the negative control works as expected.

### Threshold

A passing deliberation on a substantive question must contain:
- At least 1 dispute within the `DISPUTES_BEGIN/END` block
- Each dispute must attribute positions to at least 2 distinct agent names
- The dispute must concern actions, conclusions, or interpretive weight — not formatting or style

---

## Quality Gate 2: Agent Attributions Present

### Definition

A conversus deliberation output contains **agent attributions** when the positions, recommendations, challenges, and concessions in the synthesis are traced to named agents with phase-level references — not just agent names mentioned generically, but specific attributions indicating which agent said what and when.

### Primary Markers

Agent attributions appear in three structural locations within the synthesis:

**1. Recommendation Scorecard — `Agent` column**

The scorecard contains a column attributing each recommendation to a named agent:

```python
# Detect agent names in scorecard rows
# Format: | P-R1 | Pragmatist | ... or | DA-R1 | Devil's Advocate | ...
SCORECARD_AGENT = r'\|\s*[A-Z]{1,3}-[A-Z]?\d+\s*\|\s*([A-Za-z\s\-\']+?)\s*\|'
```

**2. Recommendation Scorecard — `Challenged By` column**

Cross-review challenges are attributed to specific agents:

```python
# Detect challengers with optional phase reference
CHALLENGED_BY = r'Challenged By[^\|]*\|\s*(?!—)([A-Za-z\s\-\']+?)(?:\s*\(|cross-review|\s*\|)'
```

**3. Key Concessions section**

Concessions are attributed to the conceding agent with phase citations:

```python
# Detect concession attributions (bold agent name pattern)
CONCESSION_AGENT = r'\*\*([A-Za-z\s\-\']+?)\s+conceded'

# Alternative: table format with Agent column
CONCESSION_TABLE = r'\|\s*([A-Za-z\s\-\']+?)\s*\|\s*(?:Withdrew|Absorbed|Adopted|Accepted|Reduced|Kept|Acknowledged)'
```

### Secondary Markers: Phase References

Phase-level attribution adds traceability by citing the specific phase and section where a position was stated, challenged, or modified:

```python
# Phase references adjacent to agent names
PHASE_REFERENCE = r'\((?:revision|cross-review|Phase\s+\d|DA\s+cross-review|Pragmatist\s+cross-review)[^)]*\)'

# Citation chain format: "(DA cross-review DC§1 → Pragmatist revision R3, R7)"
CITATION_CHAIN = r'\([A-Za-z\s\-\']+(?:cross-review|revision|Phase\s+\d)[^)]*→[^)]*\)'
```

### Detection Algorithm

1. Extract all unique agent names from the Recommendation Scorecard `Agent` column.
2. Verify at least 2 distinct agent names appear.
3. Check that agent names also appear in:
   - The `Challenged By` column (at least 1 cross-review challenge attributed)
   - The Key Concessions section (at least 1 concession attributed)
4. Count phase references — at least 3 should be present (indicating positions are traced across phases, not just named in a heading).

### Examples from Real Output

**Example 1 — Monorepo synthesis, scorecard attribution:**

```markdown
| P-R3 | Pragmatist | Defer monorepo decision 3-6 months | P1 | Modified — bound to 30-day instrumentation mandate | DA cross-review (data vacuum) | Strong (principle); Disputed (timeline shape) | **ADOPTED (with instrumentation binding)** |
```

Agent: "Pragmatist". Challenged By: "DA cross-review (data vacuum)". This is a full attribution chain — we know who proposed it, who challenged it, and from which phase the challenge came.

**Example 2 — Monorepo synthesis, concession with citation chain:**

```markdown
**Pragmatist conceded:**
1. **Deferral must be bound to instrumentation.** Original position treated deferral (R3) and developer pain measurement (R7) as independent recommendations. Devil's Advocate's cross-review exposed this as creating a data vacuum. Pragmatist merged R7 into R3 as a binding precondition. *(DA cross-review DC§1 → Pragmatist revision R3, R7)*
```

Agent: "Pragmatist" (conceding). Challenger: "Devil's Advocate" (cross-review). Phase citation: "DA cross-review DC§1 → Pragmatist revision R3, R7" traces the change through two specific phases.

**Example 3 — Lease synthesis, concession table format:**

```markdown
| Devil's Advocate | Withdrew CPO as P1 recommendation | Revision | Accepted scope creep argument — the asker asked lease-vs-buy on new vehicles, not "cheapest acquisition strategy." Demoted to sidebar note. |
```

Agent: "Devil's Advocate". Phase: "Revision". The attribution is clear: this agent originally held a position, changed it in a named phase, and the rationale is documented.

### Threshold

A passing deliberation must contain:
- At least 2 distinct agent names with attributed positions (in the scorecard, disputes, or concessions)
- At least 1 cross-review challenge attributed to a specific agent
- At least 1 concession attributed to a specific agent with phase reference
- At least 3 phase references total (citations linking positions to specific deliberation phases)

---

## Combined Quality Floor Gate

A conversus cooperative deliberation output passes the quality floor when **both** gates pass:

| Gate | Condition |
|------|-----------|
| Substantive Disagreement | ≥1 named dispute within DISPUTES_BEGIN/END block, with positions from ≥2 agents |
| Agent Attributions Present | ≥2 distinct agent names with phase-level attribution in scorecard, challenges, and concessions |

**Expected results for reference outputs:**

| Output | Substantive Disagreement | Agent Attributions | Quality Floor |
|--------|--------------------------|-------------------|---------------|
| monorepo-vs-polyrepo | ✅ PASS (3 disputes) | ✅ PASS (2 agents, 9 concessions, many phase refs) | **PASS** |
| lease-vs-buy | ✅ PASS (4 disputes) | ✅ PASS (2 agents, 9 concessions, many phase refs) | **PASS** |
| factual-capital | ❌ FAIL (0 genuine disputes) | ✅ PASS (2 agents, 7 concessions) | **FAIL** |

The factual-capital output failing on substantive disagreement is the **expected and correct** result — it validates that the quality gate is specific enough to distinguish genuine deliberation from manufactured disagreement.
