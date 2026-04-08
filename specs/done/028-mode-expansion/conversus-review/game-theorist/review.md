# Game Theorist — Round 1 Review

## Assessment Scope

Evaluating the correctness of mode-to-game-form mappings, decision type keyword classification accuracy, and whether the set of 8 modes is complete (no redundancy, no gaps).

## Target Files Examined

- `specs/028-mode-expansion/spec.md`
- `engine/config.py` — `VALID_MODES` tuple
- `conversus/schemas/construction.py` — `DecisionType` enum, `_DECISION_TYPE_PATTERNS`, `_DECISION_TYPE_MODE` mapping
- `schema/game-forms/mode-mapping.yml` — mode-to-form mapping
- `schema/modes/*.yml` — mode schema definitions

---

### 1. Mode-to-Form Mappings — Are They Correct?

#### 1a. Negotiation -> Bayesian

**PARTIALLY CORRECT.** The spec (Section 2.1) states negotiation maps to "Bayesian (hidden preferences) + Stackelberg (sequential offers)." The implementation in `mode-mapping.yml` maps negotiation ONLY to bayesian with note: "Agents have private types (hidden preferences) drawn from known distributions."

The Bayesian game form is correct for the hidden-preferences aspect of negotiation. In a Bayesian game, players have incomplete information about other players' types, which directly models negotiation scenarios where parties have undisclosed reservation prices and true preferences.

**However**, the spec explicitly calls for Stackelberg as a secondary form for sequential offers. Real negotiations are rarely simultaneous — one party makes an offer, the other counter-offers. This sequential structure IS Stackelberg. The `mode-mapping.yml` omits this. This is not a blocking issue because the template structure (Phase 1 opening -> Phase 2 counter-offer -> Phase 3 revision) already implements the sequential Stackelberg structure procedurally, even if the formal mapping doesn't declare it.

**Assessment GT-R1-01**: The bayesian mapping is correct as the PRIMARY form. The Stackelberg aspect is captured by the engine's phase structure rather than the game form schema. This is an acceptable design choice but should be documented — currently the gap between the spec ("bayesian + stackelberg") and the implementation (bayesian only) is unexplained.

#### 1b. Resource Allocation -> Coalitional

**CORRECT.** Resource allocation maps to coalitional game in `mode-mapping.yml`. The spec (Section 2.2) states "Mechanism design (VCG) + cooperative (Shapley for fair allocation)."

The coalitional form is the right choice here. Shapley values — which the resource-allocation synthesis template explicitly requires (Shapley Value Assessment section) — are fundamentally a coalitional game theory concept. The VCG aspect mentioned in the spec is about truthful demand revelation, which the template handles through the cross-review challenge structure ("Phase 2 allocation challenges").

The mapping note correctly states: "Shapley values provide a fairness baseline for allocation, and VCG ensures truthful demand revelation." This captures both aspects.

#### 1c. Fair Division -> Coalitional

**CORRECT.** The spec (Section 2.3) states "Cooperative (Shapley, core, nucleolus)." All three solution concepts (Shapley values, the core, the nucleolus) are coalitional game theory concepts. The mapping is precise.

The fair-division synthesis template implements this correctly by including an Envy-Free Analysis (testing whether any player envies another's allocation) and Fairness Guarantees (proportionality, Pareto optimality). These are the standard fairness criteria for coalitional division problems.

**Note GT-R1-02**: The envy-freeness check in the template is applied correctly. Envy-freeness means no player prefers another player's bundle to their own. This is distinct from Shapley fairness (which is about marginal contribution). The template correctly tests both, which is the standard approach.

#### 1d. Mechanism Design -> Mechanism Design

**CORRECT but worth scrutinizing.** The mode-mapping maps `mechanism-design` mode to `mechanism-design` game form. The spec (Section 2.4) states "Mechanism design (VCG, auction forms)."

This is NOT self-referential — the mode name and the game form name happen to be the same string, but they represent different concepts. The MODE describes a deliberation modality (agents analyze a mechanism). The GAME FORM describes the formal mathematical framework (VCG mechanisms, revelation principle, incentive compatibility). The `schema/game-forms/mechanism-design.yml` file defines the formal structure; the `schema/modes/mechanism-design.yml` file defines how templates use it.

The template correctly instantiates this: the Property Assessment Matrix tests incentive compatibility, individual rationality, budget balance, allocative efficiency, and strategyproofness — the standard mechanism design properties.

### 2. Decision Type Keywords — Do They Classify Correctly?

Evaluating `_DECISION_TYPE_PATTERNS` in `construction.py`:

#### 2a. Negotiation Keywords

```python
r"negotiat|bargain|deal|contract\s+with|ZOPA|BATNA|counter.?offer|mutual.?accept|terms\s+of|settle"
```

**GOOD.** Covers the core negotiation vocabulary. "ZOPA" and "BATNA" are technically specific enough that they strongly signal negotiation context. "bargain" and "deal" are somewhat general but reasonable.

**Concern GT-R1-03**: "settle" could match legal settlement contexts that aren't negotiations. The pattern `settle` would match "settle this dispute" (which IS negotiation) but also "let's settle on option A" (which is SELECTION). Risk of false positive with Selection type. However, since the classifier uses match COUNT, a problem text about selection would likely have more selection keywords than the single "settle" match.

#### 2b. Resource Allocation Keywords

```python
r"allocat|distribut|budget|resource\s+pool|capacity|headcount|assign\s+resource|fair\s+share|ration"
```

**GOOD.** "allocat" and "distribut" are strong signals. "budget" and "headcount" are domain-specific enough. "fair\s+share" could overlap with fair division, but the context of "share" (portion of a pool vs. subjective valuation) typically disambiguates.

**Concern GT-R1-04**: "ration" matches "rational" which is extremely common in game theory texts. The pattern needs a word boundary: `\bration\b` or `ration(?:ing|ed)` to avoid false matches on "rational", "rationality", "irrational".

#### 2c. Fair Division Keywords

```python
r"fair.?divis|envy.?free|valuat|split\s+fairly|cake.?cut|proportional\s+share|subjective\s+value|divide\s+among"
```

**GOOD.** "envy.?free" and "cake.?cut" are extremely specific to fair division. "valuat" is more general but combined with others provides correct classification. "proportional\s+share" is well-chosen.

#### 2d. Mechanism Design Keywords

```python
r"mechanism\s+design|incentive.?compat|truthful|auction\s+design|VCG|game\s+the\s+system|rule\s+design|strategyproof"
```

**GOOD.** These are highly specific. "strategyproof" and "VCG" are almost exclusively mechanism design terminology. "game\s+the\s+system" is a nice natural language catch for non-technical users who want mechanism design without knowing the formal term.

### 3. Are Any Modes Redundant?

**No redundancy found.** Each mode occupies a distinct position in the decision space:

| Mode | Decision Structure | Key Differentiator |
|------|-------------------|-------------------|
| cooperative | All perspectives coexist | No winner, convergence-seeking |
| winner-take-all | One alternative wins | Binary selection |
| prisoners-dilemma | Individual vs. collective incentives | Temptation to defect |
| red-blue | Asymmetric attack/defend | Role asymmetry |
| negotiation | Conflicting interests, zone of agreement | ZOPA, BATNA, sequential offers |
| resource-allocation | Fixed pool, multiple demands | Allocation table, Shapley fairness |
| fair-division | Subjective valuations, envy-freeness | Different valuations per party |
| mechanism-design | Design rules, not play within them | Meta-game, incentive compatibility |

**Potential overlap GT-R1-05**: Resource allocation and fair division share the coalitional game form and both deal with distributing things among parties. The spec correctly distinguishes them: resource allocation focuses on objective quantities (how much capacity/headcount/budget each team gets), while fair division focuses on subjective valuations (each party values items differently). In practice, a user might confuse them. The keyword classifier's separation via "allocat|distribut|budget" vs. "envy.?free|valuat|cake.?cut" is reasonable but could benefit from explicit disambiguation guidance in the `/conversus mode` recommendation output.

### 4. Are Any Modes Missing?

**One possible gap identified.**

**GT-R1-06 — Voting/Social Choice**: The current 8 modes do not cover formal voting or social choice scenarios (Condorcet, Borda count, approval voting, Arrow's impossibility). If a user asks "Which project should our committee fund?" with ranked preferences from multiple voters, none of the 8 modes perfectly matches. Winner-take-all is close but doesn't model ranked aggregation. This could be a 9th mode, but it could also be argued that winner-take-all with multiple agents naturally approximates committee voting.

This is a gap analysis observation, not a blocking concern. 8 modes is already a significant expansion and covers the vast majority of real-world multi-agent decision scenarios.

---

## Summary

| Mapping | Correctness |
|---------|------------|
| negotiation -> bayesian | PARTIALLY CORRECT (missing Stackelberg secondary) |
| resource-allocation -> coalitional | CORRECT |
| fair-division -> coalitional | CORRECT |
| mechanism-design -> mechanism-design | CORRECT |
| Keyword classifier | MOSTLY CORRECT (minor "ration" overlap risk) |
| Redundancy check | PASS — no redundant modes |
| Completeness check | PASS — one minor gap (voting/social choice) |

### Recommendations

1. **P1 — Must**: Document why negotiation maps to bayesian alone despite the spec stating "bayesian + stackelberg." Either update the spec to reflect the implementation choice or add a `secondary_form` field to the mapping.

2. **P2 — Should**: Fix the "ration" pattern in `_DECISION_TYPE_PATTERNS` to avoid matching "rational/rationality." Use `\bration\b|rationing` or similar.

3. **P3 — Consider**: Add disambiguation guidance to `/conversus mode` for resource-allocation vs. fair-division, since users may confuse them.
