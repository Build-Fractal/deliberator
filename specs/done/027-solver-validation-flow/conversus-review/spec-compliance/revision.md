# Phase 3 Revision: spec-compliance

**Spec**: 027-solver-validation-flow
**Agent**: spec-compliance
**Round**: 1

---

## Position Changes After Cross-Review

### REVISED: FR-002 -- CHANGED from MET to PARTIALLY MET

The optimization-engineer's argument is persuasive: `generate_validation_config(problem_type="scheduling")` raises ValueError for a problem type listed in the spec's section 3 table. While FR-002's text does not enumerate required types, the immediately adjacent table establishes five expected types. Implementing 3 of 5 is partial satisfaction.

The devex-advocate reinforces this from a domain perspective: scheduling and negotiation problems have fundamentally different validation concerns that generic agents cannot substitute for.

**Revised status**: PARTIALLY MET (3/5 expected problem types implemented).

### REVISED: FR-010 -- CHANGED from PARTIALLY MET to NOT MET

The optimization-engineer's argument is decisive: FR-010 says "MUST be consumable by the solver for re-optimization." `list[str]` with natural-language constraint descriptions is not consumable by any solver. The existence of a data field that could theoretically hold solver-compatible content does not constitute partial consumability.

I originally rated this PARTIALLY MET based on "data structure exists." After cross-review, I agree this is too generous. The requirement is binary: either the solver can consume it or it cannot. It cannot.

**Revised status**: NOT MET.

### REVISED: FR-011 -- CHANGED from PARTIALLY MET to NOT MET

The devex-advocate's argument is correct: `iterations: 1` in the config is a deliberation engine parameter, not iteration tracking. There is no counter, no history, no mechanism to track which validation pass produced a given verdict. The accidental overlap with the config field does not constitute partial implementation of iteration tracking.

**Revised status**: NOT MET.

### MAINTAINED: SC-002 -- PARTIALLY MET (defending against devex-advocate's NOT MET push)

The devex-advocate argues SC-002 should be NOT MET because the system does not "actually produce this finding." I maintain PARTIALLY MET for the following reason:

SC-002 says: "Sensitivity analysis correctly identifies that a portfolio solution becomes infeasible if interest rates increase by 2%." The word "identifies" in the context of a framework spec means the framework enables identification. The sensitivity analysis template directs agents to look for exactly this type of finding. The SensitivityFinding model can represent it. The risk-minimizer agent is prompted to "assess the portfolio's exposure to downside risk."

A NOT MET classification would mean the spec criterion cannot be satisfied at all. But the framework is designed to produce this finding -- it just has not been tested in an end-to-end run. PARTIALLY MET correctly captures "designed for but not demonstrated."

### MAINTAINED: SC-005 -- MET

No cross-reviewer contested this. The timing analysis is correct and the scope is "3-agent deliberation."

### NEW ASSESSMENT: Section 6 Constraints (from devex-advocate suggestion)

The devex-advocate noted I did not assess section 6 constraints. Adding:

1. "Validation deliberation uses the same engine as regular deliberation" -- **MET by design**. The config dict produces a standard conversus.yml that the existing engine would process.
2. "Solution critique agents are auto-generated from templates, not hardcoded" -- **MET**. The `_AGENT_TEMPLATES` dict is a template system; agents are constructed dynamically from templates.
3. "Validation flow MUST NOT modify the original solution" -- **MET by design**. The flow generates a config and a verdict model. Neither modifies input files.

### NEW: FR-009 enforcement gap escalated

The devex-advocate's and optimization-engineer's cross-reviews both highlight that revise/reject verdicts with empty constraint_additions are problematic. This reinforces my original observation. I upgrade the FR-009 gap from a footnote to a formal finding:

**FR-009 should be PARTIALLY MET** (maintained) with explicit remediation: add a model_validator enforcing `verdict in ("revise", "reject") implies len(constraint_additions) > 0`.

### NEW: Spec-level gap in FR-010

The optimization-engineer reveals that FR-010 is not just an implementation gap but a spec gap: the requirement says "consumable by the solver" but does not define a constraint interchange format. The spec should specify:
- What format constraint additions should take (AMPL syntax, abstract constraint template, structured expression)
- Whether the solver integration is direct (generate AMPL) or mediated (human reviews and translates)

Without this clarification, any implementation of FR-010 is guessing at the spec's intent.

---

## Revised Compliance Summary

| Requirement | Original | Revised | Change Reason |
|-------------|----------|---------|---------------|
| FR-001 | NOT MET | NOT MET | -- |
| FR-002 | MET | PARTIALLY MET | 3/5 problem types; scheduling ValueError |
| FR-003 | MET | MET | -- |
| FR-004 | MET | MET | -- |
| FR-005 | MET | MET | -- |
| FR-006 | NOT MET | NOT MET | -- |
| FR-007 | NOT MET | NOT MET | -- |
| FR-008 | PARTIALLY MET | PARTIALLY MET | -- |
| FR-009 | PARTIALLY MET | PARTIALLY MET | Enforcement gap escalated |
| FR-010 | PARTIALLY MET | NOT MET | Free-form strings not solver-consumable |
| FR-011 | PARTIALLY MET | NOT MET | Config field is not iteration tracking |
| FR-012 | NOT MET | NOT MET | -- |
| SC-001 | MET | MET | -- |
| SC-002 | PARTIALLY MET | PARTIALLY MET | Maintained against NOT MET push |
| SC-003 | NOT MET | NOT MET | -- |
| SC-004 | NOT MET | NOT MET | -- |
| SC-005 | MET | MET | -- |
| C-001 | -- | MET | New: same engine |
| C-002 | -- | MET | New: template-based agents |
| C-003 | -- | MET | New: no solution modification |

**Revised totals**: 4/12 FRs MET, 3/12 PARTIALLY MET, 5/12 NOT MET. 2/5 SCs MET, 1/5 PARTIALLY MET, 2/5 NOT MET. 3/3 Constraints MET.
