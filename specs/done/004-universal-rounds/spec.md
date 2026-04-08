# Feature Specification: Universal Rounds, Stagnation Detection, and Arbitration

**Feature ID**: `010-universal-rounds`
**Created**: 2026-03-20
**Status**: Draft
**Depends On**: `001-subject-arbitration` (Phase 6 arbitration mechanism), `002-recursive-rounds` (cooperative-only rounds — this spec generalizes it)
**Input**: Extend the `rounds`, `stagnation`, and `arbiter` features — currently restricted to cooperative mode — to all four competition modes (cooperative, red-blue, winner-take-all, prisoners-dilemma).

---

## 1. Feature Summary

Spec 002 introduced recursive rounds for cooperative mode. Spec 001 introduced subject arbitration for cooperative mode. Both features are currently gated by validation rules that reject them for non-cooperative modes:

```
"rounds > 1 is only supported in cooperative mode (current mode: {mode})."
"arbiter is only supported in cooperative mode (current mode: {mode})."
```

This restriction made sense during initial development — cooperative mode was the most natural fit for iterative convergence and neutral arbitration. But in practice, all four modes benefit from multi-round execution and dispute resolution:

- **Red-blue**: Attackers and defenders iterate. Round 1 surfaces initial attacks; Round 2 lets defenders strengthen and attackers pivot. Stagnation = red team found everything they can find. Arbitration = binding risk rulings.
- **Winner-take-all**: Competitors refine their proposals across rounds, incorporating cross-review feedback. Stagnation = no proposal improved. Arbitration = final selection with documented reasoning.
- **Prisoners-dilemma**: Agents reassess cooperation/defection incentives across rounds as they observe other agents' strategies. Stagnation = strategy equilibrium reached. Arbitration = boundary rulings on disputed territory.

This spec removes the mode restrictions and defines the mode-specific behaviors for rounds, stagnation detection, and arbitration in each non-cooperative mode.

**What changes**: Validation rules allow `rounds > 1`, `stagnation`, and `arbiter` for all modes. Mode-specific templates for `cross-round-synthesis.md` and `arbitration.md` are added for red-blue, winner-take-all, and prisoners-dilemma. Stagnation detection uses mode-appropriate dispute headings (already defined in SKILL.md's Dispute-Parsing Subsystem). Phase 6 trigger evaluation uses mode-appropriate headings (already defined in SKILL.md).

**What does not change**: Cooperative mode behavior is untouched. Single-round execution is untouched. The round loop mechanics (Phase 1-5 per round, lazy directory creation, retroactive Round 1 move) are unchanged. The `iterations` field continues to work orthogonally to `rounds` in all modes.

---

## 2. Current State

### What exists (cooperative-only)

| Feature | Cooperative | Red-Blue | Winner-Take-All | Prisoners-Dilemma |
|---------|-------------|----------|-----------------|-------------------|
| `rounds > 1` | Yes (spec 002) | Blocked | Blocked | Blocked |
| `stagnation: detect` | Yes (spec 002) | N/A | N/A | N/A |
| `arbiter` | Yes (spec 001) | Blocked | Blocked | Blocked |
| Phase 6 template | `arbitration.md` | None | None | None |
| Cross-round template | `cross-round-synthesis.md` | None | None | None |
| Dispute-parsing headings | Defined | Defined | Defined | Defined |

### What this spec adds

| Feature | Red-Blue | Winner-Take-All | Prisoners-Dilemma |
|---------|----------|-----------------|-------------------|
| `rounds > 1` | Enabled | Enabled | Enabled |
| `stagnation: detect` | Enabled | Enabled | Enabled |
| `arbiter` | Enabled | Enabled | Enabled |
| Phase 6 template | New | New | New |
| Cross-round template | New | New | New |

---

## 3. Game Theory Analysis per Mode

### Red-Blue Rounds

Multi-round red-blue maps to **iterated attack-defense games**. In security testing, multiple passes are standard — the first pass finds surface issues, subsequent passes find deeper ones as defenders patch surface vulnerabilities.

- **Round N+1 behavior**: Red agents read the prior round's synthesis and adapt attacks. Blue agents strengthen defenses based on what was exposed. This is the natural rhythm of penetration testing.
- **Stagnation**: No new risks identified (red) or no defenses improved (blue). Detected by counting `**[RISK-ID]:` entries under `### Disputed Risks` — if the count doesn't decrease between rounds, the attack surface is exhausted.
- **Convergence incentive**: Red agents that re-attack already-defended positions waste their round. Blue agents that ignore confirmed risks lose credibility. Both sides have incentive to engage with the prior round's record.

### Winner-Take-All Rounds

Multi-round winner-take-all maps to **iterated elimination tournaments**. Each round, proposals are refined based on cross-review feedback. Weak proposals don't survive scrutiny across rounds.

- **Round N+1 behavior**: Competitors read the prior synthesis (which includes a preliminary ranking) and strengthen their proposals where they were weakest. The cross-review process in each round is more informed because agents have seen each other's arguments.
- **Stagnation**: Rankings stabilize — the same proposal wins in consecutive rounds with no movement. Detected by checking `## Runner-Up` presence (if the same runner-up persists, positions are stable).
- **Convergence incentive**: Competitors that don't adapt their proposals based on prior-round feedback will lose. This incentivizes genuine improvement, not just rhetorical restatement.

### Prisoners-Dilemma Rounds

Multi-round prisoners-dilemma maps to the **iterated prisoner's dilemma** — one of the most studied structures in game theory. The iterated version is fundamentally different from the single-shot version because agents can build reputation and retaliate.

- **Round N+1 behavior**: Agents observe who cooperated and who defected in the prior round. Tit-for-tat and related strategies emerge naturally. Agents that defected face retaliation; agents that cooperated build trust.
- **Stagnation**: Boundary disputes stop moving — same disputed boundaries persist across rounds. Detected by counting `### [` sub-headings under `## Disputed Boundaries`.
- **Convergence incentive**: The strongest incentive of any mode. Iterated PD with observable history strongly favors cooperation. Agents that cooperate early build trust for later rounds; agents that defect early face retaliation.

---

## 4. Functional Requirements

### FR-001: Remove Mode Restrictions

Remove the two validation rules that restrict rounds and arbitration to cooperative mode:
- `rounds > 1` validation: allow for all four modes.
- `arbiter` validation: allow for all four modes.

The `stagnation` field requires no validation change — it already defaults to `detect` and is only meaningful when `rounds > 1`, which this FR enables.

### FR-002: Mode-Specific Stagnation Detection

Stagnation detection must use the mode-appropriate dispute heading from the Dispute-Parsing Subsystem (already defined in SKILL.md):

| Mode | Heading | Entry Pattern | Stagnation = |
|------|---------|---------------|--------------|
| cooperative | `### Remaining Disputes` | `**Dispute:` | Count ≥ prior |
| red-blue | `### Disputed Risks` | `**[RISK-ID]:` | Count ≥ prior |
| winner-take-all | `### Remaining Disputes` | Any dispute entry | Count ≥ prior |
| prisoners-dilemma | `## Disputed Boundaries` | `### [` sub-headings | Count ≥ prior |

The structural markers (`DISPUTES_BEGIN`/`DISPUTES_END`) are preferred when present, falling back to heading-based parsing. This is the existing Dispute-Parsing Subsystem interface — no new parsing logic is needed.

### FR-003: Red-Blue Cross-Round Synthesis Template

Create `templates/red-blue/cross-round-synthesis.md` with variables:
- `{ROUND_SYNTHESES}`, `{ROUNDS_COMPLETED}`, `{MAX_ROUNDS}`, `{TERMINATION_REASON}`, `{MODE}`, `{TARGET_FILES}`, `{TARGET_PATH}`, `{AGENT_NAMES}`, `{OUTPUT_PATH}`

The template must instruct the synthesizer to:
- Track risk evolution across rounds (which risks were confirmed, mitigated, or newly discovered).
- Identify attack patterns that shifted between rounds.
- Assess defense effectiveness improvements.
- Produce a final risk register that reflects the cumulative multi-round assessment.

### FR-004: Winner-Take-All Cross-Round Synthesis Template

Create `templates/winner-take-all/cross-round-synthesis.md` with the same variables as FR-003.

The template must instruct the synthesizer to:
- Track proposal evolution across rounds (how each competitor refined their argument).
- Identify which cross-review feedback was incorporated vs. ignored.
- Assess whether the winning proposal improved or merely survived.
- Produce a final ranking with confidence levels informed by multi-round stability.

### FR-005: Prisoners-Dilemma Cross-Round Synthesis Template

Create `templates/prisoners-dilemma/cross-round-synthesis.md` with the same variables as FR-003.

The template must instruct the synthesizer to:
- Track cooperation/defection patterns across rounds per agent.
- Identify whether tit-for-tat dynamics emerged.
- Assess boundary stability — which boundaries settled, which oscillated.
- Produce a final boundary map reflecting the iterated equilibrium.

### FR-006: Red-Blue Arbitration Template

Create `templates/red-blue/arbitration.md` with variables:
- `{ARBITER_NAME}`, `{ARBITER_PROMPT}`, `{ARBITER_DOCS}`, `{GROUNDING_PATH}`, `{SYNTHESIS_PATH}`, `{ALL_DISPUTES}`, `{TARGET_FILES}`, `{TARGET_PATH}`, `{AGENT_NAMES}`, `{MODE}`, `{OUTPUT_PATH}`, `{TRIGGER}`, `{REMAINING_DISPUTES}`

The template must instruct the arbiter to:
- Rule on each disputed risk: accepted (real risk), rejected (not a real risk), or accepted-with-mitigation.
- Cite the grounding document for each ruling.
- Produce binding risk decisions, not mediations.

### FR-007: Winner-Take-All Arbitration Template

Create `templates/winner-take-all/arbitration.md` with the same variables as FR-006.

The template must instruct the arbiter to:
- Select the winning proposal with documented reasoning.
- Explain why the runner-up(s) lost, citing specific weaknesses.
- Optionally: identify elements from losing proposals worth salvaging.

### FR-008: Prisoners-Dilemma Arbitration Template

Create `templates/prisoners-dilemma/arbitration.md` with the same variables as FR-006.

The template must instruct the arbiter to:
- Rule on each disputed boundary: which agent's claimed territory is justified.
- Assess whether defection was strategically justified or harmful.
- Produce binding boundary decisions.

### FR-009: Phase 6 Output Validation per Mode

Extend the Phase 6 output validation (required section headings) for each mode:

| Mode | Required Headings |
|------|-------------------|
| cooperative | Process Note, Decision Framework, Binding Decisions, Summary of Changes Required |
| red-blue | Process Note, Risk Framework, Binding Risk Decisions, Residual Risk Summary |
| winner-take-all | Process Note, Selection Criteria, Winner Declaration, Runner-Up Assessment |
| prisoners-dilemma | Process Note, Boundary Framework, Binding Boundary Decisions, Cooperation Assessment |

### FR-010: Round-Aware Template Variables for All Modes

The existing round-aware template variables (`{ROUND}`, `{MAX_ROUNDS}`, `{PRIOR_SYNTHESIS_PATH}`, `{PRIOR_ROUND_DIR}`, `{PRIOR_ROUND_SECTION}`) must be populated for all modes, not just cooperative. This is likely already the case in the orchestrator implementation but must be verified.

---

## 5. Success Criteria

- **SC-001**: A `conversus.yml` with `mode: red-blue`, `rounds: 2`, `stagnation: detect`, and `arbiter` validates and executes through all phases without error.
- **SC-002**: Stagnation detection correctly identifies when disputed-risk count stops decreasing in red-blue mode.
- **SC-003**: A winner-take-all run with `rounds: 3` produces a cross-round synthesis tracking proposal evolution.
- **SC-004**: A prisoners-dilemma run with `rounds: 2` and `arbiter` produces both a cross-round synthesis and an arbitration resolution.
- **SC-005**: All existing cooperative-mode tests continue to pass unchanged.

---

## 6. Implementation Notes

### Minimal Engine Changes

The conversus engine (SKILL.md orchestrator) already implements rounds, stagnation, and arbitration generically. The mode-specific behavior lives almost entirely in templates. The engine changes are:

1. Remove two validation `if` statements (FR-001).
2. Add mode-specific required headings to Phase 6 validation (FR-009).
3. Verify round-aware variables populate for all modes (FR-010).

### Template-First Approach

The bulk of this spec is template creation (FR-003 through FR-008). Each template requires game-theory-informed prompt engineering specific to the mode's dynamics. The cooperative templates serve as structural references, but the content must reflect each mode's competitive dynamics.

### Backward Compatibility

No existing behavior changes. All new features are opt-in via config fields that were previously rejected by validation. Single-round runs are unaffected. Cooperative mode is untouched.
