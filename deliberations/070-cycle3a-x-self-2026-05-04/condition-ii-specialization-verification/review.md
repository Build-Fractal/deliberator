### Executive Summary

This deliberation evaluates Condition (ii) from the supplemental blind verdict: whether the proposed restored Principle X's sub-bullets specialize Principle V's "every phase MUST report progress" with output-format requirements that V does not cover, or whether they merely compose from existing principles without adding new content.

The candidate proposes four sub-bullets under "Predictable Output Tree": synthesis canonical path, output depth bound, malformed-output emission, and per-file focus. My analysis reveals that three of the four sub-bullets introduce genuinely new structural constraints not covered by existing principles V, VII, or XXIV. However, the critical "malformed-output emission" sub-bullet substantially duplicates Principle V's existing malformed output handling requirements, creating a Criterion 3 distinctness failure.

**Condition (ii) verdict: PARTIAL PASS** — sub-bullets 1, 2, and 4 satisfy distinctness; sub-bullet 3 fails and should remain in operational guidance.

### Alignment

The candidate correctly identifies the analytical framework for specialization verification:

- **V's scope correctly characterized** (`X-path-c-restoration-candidate.md`, L147-148): The candidate accurately describes V as mandating "events emitted at phase boundaries" for progress reporting, establishing the baseline for comparison.

- **VII coordination acknowledged** (`X-path-c-restoration-candidate.md`, L154): The candidate recognizes that sub-bullets extend "V+VII (Reproducibility) with structure-specific concrete invariants," showing awareness of multi-principle composition analysis.

- **XXIV safety-critical carve-out** (`X-path-c-restoration-candidate.md`, L94-95): The malformed-output sub-bullet correctly references "Principle XXIV applies" for safety-critical artifacts, demonstrating proper exception handling.

### Missed Opportunities

The candidate's distinctness analysis contains a critical gap that undermines Condition (ii):

- **Malformed-output duplication unacknowledged**: The candidate claims the malformed-output sub-bullet "mandates a different signal: warnings emitted when artifacts violate structural expectations" (`L149-150`), but fails to recognize that Principle V already requires "Output validation (e.g., Phase 6 heading checks) emits warnings for malformed output" (`CONSTITUTION-v2.5.0-pre-migration.md`, L343-345). Impact: **high** — this oversight leads to a false distinctness claim for the most important sub-bullet.

- **V's "catch malformed results" clause ignored**: The candidate analysis omits V's explicit "Output validation MUST catch malformed results" requirement (`CONSTITUTION-v2.5.0-pre-migration.md`, L339-340), which directly overlaps with proposed X's "emit a warning when documents are malformed, missing, or out-of-spec." Impact: **high** — missing this overlap invalidates the specialization claim.

- **Structural vs. operational distinction missing**: The candidate doesn't distinguish between V's operational requirements (phase-boundary reporting) and structural requirements (output format validation). Three sub-bullets are genuinely structural; one is operational duplication. Impact: **medium** — cleaner categorization would strengthen the distinctness argument for passing sub-bullets.

- **Cross-principle composition analysis incomplete**: While acknowledging V+VII coordination, the candidate doesn't systematically evaluate each sub-bullet against the full principle set (VIII, IX, XXIV, etc.) to establish comprehensive distinctness. Impact: **medium** — incomplete analysis leaves distinctness claims vulnerable.

### Off-Base Assumptions

- **"Different signal" characterization**: The candidate assumes (`L149-150`) that warnings for malformed output constitute a "different signal" from V's progress reporting, when both are operational warning emissions about deliberation state. V already covers malformed output warnings as part of its validation requirements.

### Actionable Recommendations

1. **Acknowledge malformed-output duplication** (Priority: P1)
   - **Current state**: Candidate claims malformed-output sub-bullet provides distinct content from V (`L144-151`).
   - **Proposed change**: Revise Condition (ii) analysis to acknowledge substantial overlap between proposed "emit a warning when documents are malformed, missing, or out-of-spec" and V's existing "Output validation MUST catch malformed results" + "emits warnings for malformed output."
   - **Rationale**: Principle V (`CONSTITUTION-v2.5.0-pre-migration.md`, L339-345) already requires both malformed result detection and warning emission. The proposed sub-bullet restates this requirement without meaningful specialization.
   - **Risk if ignored**: False PASS verdict on distinctness for a sub-bullet that violates Criterion 3, undermining the entire restoration.

2. **Separate structural from operational sub-bullets** (Priority: P1)
   - **Current state**: All four sub-bullets treated as equivalent specializations of V (`L144-155`).
   - **Proposed change**: Categorize sub-bullets 1, 2, and 4 as structural constraints (file existence, directory depth, content organization) that extend VII's deterministic output tree, while acknowledging sub-bullet 3 as operational duplication of V's validation requirements.
   - **Rationale**: Structural constraints (where files exist, how deep, what they contain) are distinct from operational requirements (what warnings to emit). Only structural specialization passes distinctness.
   - **Risk if ignored**: Analytical confusion between genuinely new structural content and operational duplication.

3. **Quantify V's existing malformed-output scope** (Priority: P1)
   - **Current state**: V's malformed output requirements treated as narrow phase-boundary reporting.
   - **Proposed change**: Acknowledge that V's "Output validation MUST catch malformed results" and "emits warnings for malformed output but does NOT block file writes" (`CONSTITUTION-v2.5.0-pre-migration.md`, L343-345) already covers document validation across the deliberation pipeline.
   - **Rationale**: V's scope extends beyond phase boundaries to output validation generally, directly overlapping with proposed X's malformed-output requirements.
   - **Risk if ignored**: Understating V's existing coverage leads to false distinctness claims.

4. **Provide PARTIAL PASS verdict option** (Priority: P2)
   - **Current state**: Analysis assumes all-or-nothing restoration outcome.
   - **Proposed change**: Recommend PARTIAL PASS verdict where sub-bullets 1, 2, and 4 pass distinctness and qualify for constitutional restoration, while sub-bullet 3 remains in operational guidance per the v3.0.0 migration.
   - **Rationale**: The candidate document (`L63-66`) explicitly allows PARTIAL PASS verdicts "if specific sub-bullets pass their condition but the headline does not (or vice versa)."
   - **Risk if ignored**: Binary thinking forces either full restoration (including duplicative content) or complete rejection (losing genuinely distinct structural constraints).

5. **Cross-reference XXIV scope limitation** (Priority: P2)
   - **Current state**: XXIV carve-out mentioned without scope analysis.
   - **Proposed change**: Clarify that XXIV applies only to "synthesis verdict generation" and "provider protocol implementation" (`CONSTITUTION.md`, L1733-1737), not general output validation, confirming that most malformed-output cases fall under V's scope, not XXIV's.
   - **Rationale**: Accurate XXIV scoping prevents over-broad safety-critical exceptions that would artificially narrow V's overlap.
   - **Risk if ignored**: Mischaracterization of safety-critical scope could create loopholes in distinctness analysis.

6. **Document sub-bullet dependency relationships** (Priority: P3)
   - **Current state**: Sub-bullets treated as independent mechanical checks.
   - **Proposed change**: Note that sub-bullet 1 (synthesis canonical path) depends on sub-bullet 2 (output depth bound) for full structural specification — the canonical path constraint only makes sense within a bounded depth structure.
   - **Rationale**: Dependency relationships affect restoration scope if partial pass is required.
   - **Risk if ignored**: Partial restoration might restore dependent sub-bullets incompletely.

### Referenced Documentation

- `<HOME>/code/payer-index-mono/conversus-oss/deliberations/070-cycle3a-x-self-2026-05-04/X-path-c-restoration-candidate.md` — sections cited: L63-66, L144-155
- `<HOME>/code/payer-index-mono/conversus-oss/deliberations/070-supplemental-blind-2026-05-04/CONSTITUTION-v2.5.0-pre-migration.md` — sections cited: L337-347 (Principle V), L484-504 (original Principle X)
- `<HOME>/code/payer-index-mono/conversus-oss/CONSTITUTION.md` — sections cited: L1081-1091 (current Principle V), L1733-1737 (Principle XXIV scope)