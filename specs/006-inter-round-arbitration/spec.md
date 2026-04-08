# Feature Specification: Inter-Round Arbitration with Influence Control

**Feature ID**: `006-inter-round-arbitration`
**Created**: 2026-03-20
**Revised**: 2026-03-21
**Status**: **Half-shipped — reopened 2026-04-04**. Phase 1 (schema/template plumbing, config fields, dispute-parsing hooks) complete. Phase 2 (execution model — round-loop dispatch, influence-aware dispute counting, context carry-through via `prior_arbitration_path`) NOT complete. See `IMPLEMENTATION-GAP.md` for the 7-point finish-up checklist. Moved out of `done/` on 2026-04-04 after the spec 045 test coverage deliberation discovered the execution branch at `engine/phases.py:661` is unreachable.
**Depends On**: `001-subject-arbitration` (done), `004-universal-rounds` (done), `005-generalized-templates` (done — schema variables pre-provisioned)
**Input**: Add an inter-round arbiter that reviews each round's synthesis and feeds decisions into the next round, with configurable influence level controlling whether rulings are binding, recommended, or advisory.

---

## 1. Feature Summary

Spec 001 introduced subject arbitration as a terminal Phase 6 — the arbiter rules once, after all deliberation is complete. Spec 004 introduced multi-round execution where disputes propagate across 5-phase cycles. The current design keeps the arbiter out of the loop until recursion is exhausted: rounds run, stagnation may be detected, and only then does the arbiter rule on whatever remains.

This creates two structural problems:

1. **Wasted rounds on intractable disputes.** A 3-round deliberation where Round 1 surfaces 5 disputes and Round 2 resolves 2 — the remaining 3 are genuine design trade-offs agents will never self-resolve. Round 3 is wasted. The better intervention is after Round 2: let the arbiter address the 3 intractable disputes, feed those into Round 3, and let agents focus on higher-order concerns with the deadlocks cleared.

2. **Binary authority model.** The current arbiter produces "Binding Decisions" — agents in subsequent rounds must treat them as settled. This is a dictator mechanism: efficient but reduces agent incentive to self-resolve. Some deliberations benefit from softer intervention — an arbiter who suggests rather than commands, nudging convergence without closing off exploration.

This spec introduces two new arbiter capabilities:

- **Inter-round timing** (`arbiter.timing: inter-round`): Phase 6 runs between rounds, not just after the final round. The arbiter reviews each round's synthesis, addresses disputes it can ground in its decision framework, and those positions are injected into the next round's context.

- **Influence control** (`arbiter.influence: advisory | recommended | binding`): Controls how much authority the arbiter's positions carry. `binding` = current behavior (agents must comply). `recommended` = agents should adopt unless they have grounded counter-evidence. `advisory` = agents consider the arbiter's perspective but may freely disagree.

The two capabilities are orthogonal. `timing` controls WHEN the arbiter acts. `influence` controls HOW MUCH WEIGHT the arbiter's positions carry. All four combinations are valid.

**What changes**: Two new optional fields on the `arbiter` config: `timing` (default `final`) and `influence` (default `binding`). When `timing: inter-round`, Phase 6 executes after each round's synthesis. When `influence` is `advisory` or `recommended`, arbiter output uses different template language and dispute counting adjusts accordingly.

**What does not change**: Single-round behavior is identical. Default values (`timing: final`, `influence: binding`) produce identical behavior to spec 001. The arbiter's grounding document, trigger mechanism, and template structure are unchanged. The Phase 6 template is reused with additional context variables and influence-aware language.

---

## 2. User Stories

### US-1: Inter-Round Arbiter with Binding Influence

As a developer running a multi-round deliberation with intractable disputes, I want the arbiter to intervene between rounds with binding authority so that deadlocks are cleared early and subsequent rounds focus on remaining open questions.

**Acceptance Criteria**:

1. **Given** `rounds: 3`, `arbiter.timing: inter-round`, `arbiter.influence: binding`, `arbiter.trigger: disputes_remain`, **When** Round 1 synthesis has 5 disputes and the arbiter can ground rulings for 3, **Then** Phase 6 runs after Round 1, produces binding rulings for 3 disputes, Round 2 agents receive the arbitration as mandatory context, and those 3 disputes are excluded from the Round 2 dispute count.

2. **Given** `arbiter.timing: inter-round`, `arbiter.influence: binding`, **When** the arbiter resolves ALL disputes after Round 1, **Then** Round 2 does not execute. Early termination via arbiter convergence.

3. **Given** `arbiter.timing: final` (or omitted), `arbiter.influence: binding` (or omitted), **Then** behavior is identical to spec 001 + spec 004.

### US-2: Advisory Arbiter as Mediator

As a developer running a deliberation where I want the arbiter to guide without dictating, I want an advisory influence mode so that agents receive the arbiter's perspective but retain full autonomy to disagree.

**Acceptance Criteria**:

1. **Given** `arbiter.influence: advisory`, **When** Phase 6 produces output, **Then** the output header reads "Advisory Opinion" (not "Binding Decisions"). The template instructs: "The arbiter has offered perspective on these disputes. Consider their reasoning but you are not bound by it."

2. **Given** `arbiter.influence: advisory`, **When** Round 2 agents receive the prior arbitration, **Then** the template says "consider these positions" not "you MUST treat these as settled." Agents may freely propose alternatives.

3. **Given** `arbiter.influence: advisory`, **When** computing the dispute count for stagnation/termination, **Then** disputes the arbiter opined on remain in the count. Advisory opinions do not reduce dispute counts.

### US-3: Recommended Influence as Middle Ground

As a developer who wants arbiter intervention stronger than advisory but without the rigidity of binding, I want a recommended influence mode where agents should adopt the arbiter's positions unless they have evidence to the contrary.

**Acceptance Criteria**:

1. **Given** `arbiter.influence: recommended`, **When** Phase 6 produces output, **Then** the output header reads "Recommended Resolutions." The template instructs: "The arbiter has recommended resolutions for these disputes. You should adopt these unless you have grounded counter-evidence. If you disagree, you must cite specific documentation or prior-round evidence."

2. **Given** `arbiter.influence: recommended`, **When** computing dispute counts, **Then** disputes the arbiter recommended on are counted as "provisionally resolved" — they reduce the dispute count for stagnation purposes but can be re-opened if an agent provides grounded counter-evidence in the next round.

3. **Given** `arbiter.influence: recommended` and an agent re-opens a recommended resolution with evidence, **When** Phase 5 synthesis runs, **Then** the synthesizer notes the re-opening and evaluates whether the counter-evidence is sufficient to override the recommendation.

### US-4: Multi-Round Arbitration Output Structure

As a developer reviewing conversus output, I want to see per-round arbiter positions organized clearly with influence level labeled, so I can trace which disputes were addressed when, by what mechanism, and with what authority.

**Acceptance Criteria**:

1. **Given** `rounds: 3` with inter-round arbitration, **When** arbitration fires after Rounds 1 and 2, **Then** the output structure includes:
   ```
   {output}/
   ├── round-1/
   │   ├── {agent}/...
   │   ├── summary/final.md
   │   └── arbitration/resolution.md   ← Round 1 arbiter positions
   ├── round-2/
   │   ├── {agent}/...
   │   ├── summary/final.md
   │   └── arbitration/resolution.md   ← Round 2 arbiter positions
   ├── round-3/
   │   └── ...
   ├── summary/final.md               ← cross-round synthesis
   └── arbitration/resolution.md       ← final arbitration (if disputes remain)
   ```

2. **Given** the cross-round synthesis, **Then** it tracks dispute resolution attribution: "Resolved by agents in Round N" vs. "Addressed by arbiter after Round N (binding/recommended/advisory)" vs. "Unresolved."

### US-5: Influence Level with Final Timing

As a developer using `timing: final` (single arbitration after all rounds), I want the influence level to still apply so that I can have a final advisory opinion rather than a binding ruling.

**Acceptance Criteria**:

1. **Given** `arbiter.timing: final`, `arbiter.influence: advisory`, **When** Phase 6 runs after the final round, **Then** the output is an advisory opinion, not binding rulings. Template language reflects the advisory role.

2. **Given** `arbiter.timing: final`, `arbiter.influence: recommended`, **Then** the output is a set of recommended resolutions with the appropriate template language.

---

## 3. Functional Requirements

### Schema Extension

- **FR-001**: The `arbiter` config block MUST support an optional `timing` field accepting values `final` (default) or `inter-round`.
- **FR-002**: The `arbiter` config block MUST support an optional `influence` field accepting values `binding` (default), `recommended`, or `advisory`.
- **FR-003**: Validation MUST reject `timing: inter-round` when `rounds: 1` (or `rounds` omitted) with error: "arbiter.timing: inter-round requires rounds > 1. With a single round, use timing: final (or omit timing)."
- **FR-004**: When `timing` is omitted, it MUST default to `final`. When `influence` is omitted, it MUST default to `binding`. Existing configs without these fields are unchanged.

### Execution Model

- **FR-005**: When `arbiter.timing: inter-round`, after each round's Phase 5 synthesis AND before the round termination check, Phase 6 MUST execute (subject to the `trigger` condition). The per-round sequence becomes: Phase 1-5 → Phase 6 (conditional) → termination check.
- **FR-006**: When `arbiter.timing: inter-round`, Phase 6 output for Round N MUST be written to `{output}/round-N/arbitration/resolution.md` (inside the round directory, not at the top level).
- **FR-007**: A final top-level `{output}/arbitration/resolution.md` is produced only if disputes remain after the final round's Phase 6 (or if `trigger: always`). This is a cumulative resolution referencing all per-round arbitration.
- **FR-008**: When `arbiter.timing: final`, behavior MUST be identical to spec 001 + spec 004. No per-round arbitration directories.

### Influence-Aware Dispute Counting

- **FR-009**: The termination check MUST account for the arbiter's influence level when computing post-arbitration dispute counts:

  | Influence | Effect on dispute count | Re-litigation |
  |-----------|------------------------|---------------|
  | `binding` | Disputes addressed by arbiter are removed from count | Not permitted |
  | `recommended` | Disputes addressed are removed from count (provisionally) | Permitted with grounded counter-evidence |
  | `advisory` | Disputes addressed remain in count | Freely permitted |

- **FR-010**: When `influence: binding` and the arbiter addresses all remaining disputes, the round terminates as "converged."
- **FR-011**: When `influence: advisory`, arbitration never causes early termination — only agent convergence can.
- **FR-012**: When `influence: recommended` and an agent re-opens a provisionally resolved dispute in the next round, the re-opened dispute returns to the active count.

### Cross-Round Context Injection

- **FR-013**: In Round R > 1, when inter-round arbitration fired in Round R-1, Phase 1 agents MUST receive `{PRIOR_ARBITRATION_PATH}` as a mandatory read (in addition to `{PRIOR_SYNTHESIS_PATH}`).
- **FR-014**: The `{PRIOR_ARBITRATION_SECTION}` conditional block MUST use influence-aware language:

  | Influence | Template language |
  |-----------|-------------------|
  | `binding` | "The arbiter has issued binding rulings on the following disputes. You MUST treat these as settled. Do not propose alternatives to, argue against, or re-litigate arbiter rulings." |
  | `recommended` | "The arbiter has recommended resolutions for the following disputes. You should adopt these unless you have grounded counter-evidence from your documentation or the target specification. If you disagree, you must cite specific evidence." |
  | `advisory` | "The arbiter has offered perspective on the following disputes. Consider their reasoning as you form your positions. You are not bound by these opinions and may freely propose alternatives." |

- **FR-015**: The Phase 5 synthesis template for Round R > 1 MUST handle arbiter-addressed disputes based on influence level:
  - `binding`: Exclude from "Remaining Disputes", list under "Arbiter-Resolved Disputes (Prior Rounds)"
  - `recommended`: List under "Provisionally Resolved Disputes" with note that agents may re-open with evidence
  - `advisory`: Keep in "Remaining Disputes" but note the arbiter's position as additional context

### Template Variables

- **FR-016**: All Phase 1-5 templates MUST support `{PRIOR_ARBITRATION_PATH}` (empty string when no prior-round arbitration exists). *Already provisioned in schema by spec 005.*
- **FR-017**: The cross-round synthesis template MUST support `{ARBITRATION_PATHS}` (newline-separated list of per-round arbitration paths). *Already provisioned in schema by spec 005.*
- **FR-018**: All Phase 1 (review) templates MUST support a new `{PRIOR_ARBITRATION_SECTION}` conditional block variable. When prior-round arbitration exists, this expands to the influence-aware context block (FR-014). When no prior arbitration exists, this is empty string. Note: only Phase 1 templates receive this variable — Phases 2-5 operate within a single round's artifacts and do not need prior-round arbitration context.
- **FR-019**: All Phase 6 templates MUST support a new `{INFLUENCE_LEVEL}` variable (string: "binding", "recommended", or "advisory"). The template uses this to adjust its output headings and language.
- **FR-020**: The cross-round synthesis MUST include a "Resolution Attribution" section tracking which disputes were resolved by agent convergence vs. arbiter (with influence level noted), and in which round.

### Stagnation Interaction

- **FR-021**: When `arbiter.timing: inter-round` and `stagnation: detect`, stagnation detection MUST use post-arbitration dispute counts adjusted by influence level (per FR-009). Stagnation requires: total active disputes did not decrease between rounds.
- **FR-022**: When the arbiter addresses zero disputes in a round (all are outside the grounding document's scope), that round's arbitration still counts as "attempted." Stagnation is evaluated on active dispute count, not arbitration productivity.

### Arbitration Template Adaptation

- **FR-023**: When `influence` is `advisory` or `recommended`, the Phase 6 arbitration template output headings MUST change:

  | Influence | Heading replacements |
  |-----------|---------------------|
  | `binding` | No change (current: "Binding Decisions", "Summary of Changes Required") |
  | `recommended` | "Binding Decisions" → "Recommended Resolutions", "Summary of Changes Required" → "Suggested Changes" |
  | `advisory` | "Binding Decisions" → "Advisory Opinions", "Summary of Changes Required" → "Considerations for Next Round" |

  Note: The Phase 6 output validation (heading checks) MUST use the influence-adjusted headings, not the default binding headings.

---

## 4. Success Criteria

- **SC-001**: A `rounds: 3`, `timing: inter-round`, `influence: binding` run produces per-round arbitration with binding rulings. Round 2+ agents reference and comply with prior rulings. Dispute counts decrease.
- **SC-002**: A `rounds: 3`, `timing: inter-round`, `influence: advisory` run produces per-round advisory opinions. Round 2+ agents acknowledge but may disagree. Dispute counts are unaffected by arbiter opinions.
- **SC-003**: A `rounds: 3`, `timing: inter-round`, `influence: recommended` run produces recommended resolutions. An agent re-opens a recommendation with evidence in Round 2 — the dispute returns to active count.
- **SC-004**: `timing: final`, `influence: binding` (or both omitted) produces output identical to spec 001 + spec 004.
- **SC-005**: `timing: final`, `influence: advisory` produces an advisory opinion after the final round with advisory template language.
- **SC-006**: `timing: inter-round` with `rounds: 1` is rejected with a clear error.
- **SC-007**: Cross-round synthesis correctly attributes dispute resolution with influence level: "Resolved by agents (Round 2)", "Resolved by arbiter binding ruling (Round 1)", "Recommended by arbiter (Round 1, adopted by agents in Round 2)", "Advisory opinion (Round 1, agent disagreed in Round 2)."
- **SC-008**: Stagnation detection with `influence: binding` correctly excludes arbiter-resolved disputes. Stagnation with `influence: advisory` ignores arbiter opinions.

---

## 5. Implementation Notes

### Game Theory Justification

In mechanism design, the distinction between a **dictator** (binding), **mediator** (recommended), and **observer** (advisory) maps to different equilibrium and incentive properties:

- **Binding (dictator)**: Maximizes efficiency — deadlocks are cleared immediately. But reduces agent incentive to self-resolve on topics they expect the arbiter to handle. Agents may strategically defer difficult trade-offs to the arbiter rather than negotiating in good faith. Best for: time-constrained deliberations, clear authority hierarchies.

- **Recommended (mediator)**: Balances efficiency and autonomy. Agents feel pressure to adopt but retain the ability to override with evidence. Creates a "comply or explain" dynamic that encourages genuine engagement. Best for: collaborative design decisions, spec reviews, architecture discussions.

- **Advisory (observer)**: Maximizes agent autonomy. The arbiter's value is informational — providing a perspective agents may not have considered. Does not short-circuit the deliberation process. Best for: exploratory deliberations, brainstorming, early-stage design where premature convergence is worse than extended discussion.

The influence level interacts with timing:
- `timing: final` + `influence: advisory` = "get an expert opinion after the debate"
- `timing: inter-round` + `influence: advisory` = "have an expert observe and comment each round"
- `timing: inter-round` + `influence: binding` = "have an authority clear deadlocks progressively"

### Pre-Provisioned Schema (Spec 005)

Spec 005 (Generalized Templates) pre-provisioned the following in anticipation of this spec:
- `PRIOR_ARBITRATION_PATH` variable in `schema/variables.yml` with `config_conditions: arbiter.timing = inter-round`
- `ARBITRATION_PATHS` and `ARBITRATION_RULINGS` variables in schema and context models
- `ConfigCondition` Pydantic model supporting the `arbiter.timing` condition

This spec adds `PRIOR_ARBITRATION_SECTION` (conditional block) and `INFLUENCE_LEVEL` (string) as new variables. These must be added to `schema/variables.yml` and the appropriate context models.

### Template Reuse

The existing Phase 6 arbitration template is reused with these modifications:
- `{INFLUENCE_LEVEL}` variable controls output heading text
- Arbiter prompt preamble adjusts tone based on influence level
- For `advisory`/`recommended`, the arbiter is instructed to frame positions as opinions/recommendations rather than rulings

No new template files are needed. The existing `templates/{mode}/arbitration.md` handles all influence levels via the `{INFLUENCE_LEVEL}` variable.

### Interaction with Universal Rounds (Spec 004)

Inter-round arbitration works with all four modes since spec 004 removed mode restrictions on rounds and arbitration. The mode-specific arbitration templates handle influence-adjusted headings via FR-023.

### Backward Compatibility

- Omitting `timing` → `final` (current behavior)
- Omitting `influence` → `binding` (current behavior)
- Both omitted → identical to spec 001 + spec 004

No existing configs break. No existing templates require modification for backward compatibility. New template variables (`{PRIOR_ARBITRATION_SECTION}`, `{INFLUENCE_LEVEL}`) are empty string / absent when the features are not configured.

---

## 6. Delivery Phases

### Phase 1: Schema + Validation (S-effort)
- Add `timing` and `influence` fields to SKILL.md config parsing
- Add validation rules (FR-001 through FR-004)
- Add `PRIOR_ARBITRATION_SECTION` and `INFLUENCE_LEVEL` to `schema/variables.yml` and `models.py`
- Update linter to validate new variables

### Phase 2: Execution Model (M-effort)
- Modify SKILL.md round loop to insert Phase 6 between rounds when `timing: inter-round`
- Implement influence-aware dispute counting (FR-009 through FR-012)
- Implement per-round arbitration output paths (FR-006, FR-007)
- Implement `{PRIOR_ARBITRATION_PATH}` injection in Round R > 1 (FR-013)

### Phase 3: Template Modifications (M-effort)
- Add `{PRIOR_ARBITRATION_SECTION}` to all review templates with influence-aware language (FR-014)
- Update synthesis templates for influence-aware dispute categorization (FR-015)
- Update arbitration templates with `{INFLUENCE_LEVEL}` heading adaptation (FR-023)
- Update cross-round synthesis template with Resolution Attribution section (FR-020)

### Phase 4: Validation (S-effort)
- Test all 4 timing×influence combinations: final/binding, final/advisory, inter-round/binding, inter-round/advisory
- Test recommended influence with agent re-opening
- Test stagnation interaction per influence level
- Verify backward compatibility
