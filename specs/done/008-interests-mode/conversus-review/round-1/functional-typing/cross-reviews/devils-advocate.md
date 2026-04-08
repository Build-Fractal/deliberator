# Cross-Review of Devil's Advocate — by Functional-Typing

**Cross-reviewer**: functional-typing
**Reviewing**: devils-advocate's review of spec 008
**Date**: 2026-03-22

---

## Dangerous Contradictions

### 1. Confidence labels: "fabricated" vs. structurally valid defaults

Devil's advocate claims the decision matrix confidence is "fabricated" (review lines 29-37) and calls the universal "High" labels "misleading." The specific challenge is that `scoping -> prisoners-dilemma` at High is "the weakest link" because "many scoping problems have no deception incentive at all."

This contradicts what the spec and SKILL.md actually specify. The confidence label does not claim empirical validation — it indicates the strength of the default mapping within the closed taxonomy. The taxonomy itself (SKILL.md lines 834-850) is explicitly stated as "intentionally closed" (SKILL.md line 850), meaning every problem that enters the guided workflow has already been classified into one of these four types. Within that closed set, the mappings ARE high-confidence by construction: each type was designed to pair with its mode. Devil's advocate's example — "Which team owns the data pipeline?" being a coordination problem — is actually a classification issue at the `define` step (is this scoping or integration?), not a mapping issue at the `mode` step.

More dangerously, devil's advocate then argues (review line 37): "If the mapping is truly high-confidence, why does the spec need heuristic mode detection at all?" This confuses two different code paths. The decision matrix (spec lines 44-51) fires when the problem type IS set. Heuristic detection (spec lines 63-68) fires when the problem type is "unset or ambiguous" (SKILL.md line 1145). These are disjoint conditions, not fallbacks for the same condition. The existence of a fallback for missing data does not impugn the confidence of the primary mapping — it handles a different input state entirely.

My own review (review lines 92-104) identified the actual structural problem: the spec's `ambiguous` row (spec line 52) defaults to `cooperative` at Low confidence, but SKILL.md replaces this with heuristic detection that could recommend ANY mode. That is a real divergence with real consequences. Devil's advocate's framing obscures this concrete gap by attacking the High labels on the non-ambiguous rows, which are not the problem.

### 2. "interests.md is a coupling artifact with unclear value" contradicts the spec's separation-of-concerns design

Devil's advocate argues (review lines 49-57) that `interests.md` duplicates information in `conversus.yml` and proposes making it optional or collapsing `interests` and `mode` into a single command.

This contradicts the spec's explicit architectural decision. Spec line 17 states: "interests determine mode, and mode generates the config." The two-step design is intentional: interests are a human-legible intermediate representation that the user reviews and modifies (spec line 39: add/remove/modify existing interests) BEFORE mode selection locks in the game-theoretic structure. Collapsing them eliminates the user's ability to iterate on agent perspectives independently of mode.

Devil's advocate says "the mode is determined primarily by the problem type from problem.md, not by the interest structure" (review line 55). This is only partially true. The decision matrix keys on problem type for the DEFAULT, but the heuristic detection (spec lines 63-68) explicitly uses interest structure as a signal: "interests named after products/tools/approaches" (WTA), "interests named after teams/roles/systems" (cooperative). The interest structure IS an input to mode selection, which is exactly why it needs to exist before mode runs.

Furthermore, devil's advocate's own recommendation #5 (review line 97) suggests a `--from-problem` shortcut that "generates interests inline." This shortcut would still need to present interests for confirmation (spec line 104: "Must NOT generate agents without user confirmation"), display them in the same structured format, and allow modification — which means it would recreate the interests.md workflow inside the mode command, not eliminate it. The coupling devil's advocate objects to would simply move from inter-file to intra-command, without reducing complexity.

My own review confirmed that the `interests.md` schema is faithfully implemented (review lines 17-26, 58-66, 70-77) and that the Preset field addition (review lines 176-185) is a reasonable extension that the spec should adopt. The file earns its keep as an editable, versionable intermediate artifact.

---

## Tensions

### 1. Heuristic formalization: how much is enough?

Devil's advocate demands formalization of the heuristic detection scoring (review lines 39-47): "define a concrete scoring mechanism (keyword presence counts, minimum signal count for 'clear lead,' explicit tie-breaking rules)." The alternative offered is to "demote the heuristics from 'detection' to 'suggestion.'"

My own review did not flag heuristic underspecification as an issue. On reflection, there is a genuine tension here, but devil's advocate overstates the problem. The heuristics run in the main conversation (SKILL.md line 1097: "the mode command executes entirely in the main conversation. No subagents are launched"), meaning an LLM interprets them. Formalizing keyword counts and thresholds into a rigid scoring function would be fighting the medium — the spec is an LLM-executed instruction set, not compiled code. The Dispute-Parsing Subsystem (SKILL.md lines 743-770) that devil's advocate holds up as a positive contrast operates on structured text output with known markers, which is a fundamentally different parsing problem than classifying free-text problem descriptions.

That said, devil's advocate is right that the spec should explicitly state that the heuristic recommendation is always subject to user confirmation. SKILL.md line 1210 already requires this ("Do not write `conversus.yml` until the user confirms"), but the heuristic section itself (SKILL.md lines 1147-1156) does not reference this gate. Adding a sentence there — "The heuristic recommendation is always presented to the user for confirmation before proceeding" — would close the gap without the false precision of keyword scoring functions.

### 2. Agent-launch cost transparency: real concern, different scope

Devil's advocate identifies a missed opportunity: no agent-launch cost estimate is shown before confirming interests (review lines 69-73). The formula from SKILL.md lines 1304-1306 (N^2 + N + 1 per round) is already documented, but neither the interests confirmation nor the mode confirmation surfaces it.

My own review did not flag this, focused as it was on structural compliance. Devil's advocate is right that this is a gap — but the scope they propose is too broad. The interests command cannot estimate total cost because it does not know the mode, iteration count, or round count yet. Those are set by the mode command. The mode command's confirmation step (SKILL.md lines 1193-1210) shows agent count but not launch count. The correct fix is narrower than devil's advocate suggests: add the launch estimate to the MODE confirmation (not interests), since only at mode time are all the variables known.

### 3. Problem type / interest structure cross-validation

Devil's advocate argues (review lines 76-79) that the mode command should cross-check the interest structure against the stated problem type and warn when they contradict. My own review identified a related but distinct gap: no explicit handling when the Type field contains a `[CLARIFY: ...]` tag (review lines 195-199).

These concerns are complementary. Devil's advocate addresses the case where the type is set but the interests contradict it. My review addresses the case where the type is marked as uncertain. Both are real gaps, and fixing both would produce a more robust mode command. The tension is in prioritization: devil's advocate's cross-validation requires semantic analysis of interest names (are they "products" or "teams"?), which inherits the same LLM-interpretation ambiguity that makes heuristic formalization difficult. My proposed fix (extract the best-guess type from the CLARIFY tag) is more mechanical and therefore more reliably implementable.

### 4. Feedback loop from /conversus run

Devil's advocate identifies a missing feedback loop (review lines 63-67): the guided workflow flows one direction (`define -> interests -> mode -> run`) with no mechanism to feed run results back into interest or mode refinement.

My own review did not address this because it falls outside the scope of spec 008 — the spec explicitly states "What does not change: /conversus run behavior" (spec line 23). Devil's advocate is aware of this boundary but argues the guided workflow should at least SUGGEST refinement after a run. This is a reasonable product enhancement, but it belongs in a future spec (possibly an 009-refine or 011-iterate spec), not as a requirement on 008. The `prior:` mechanism (SKILL.md lines 75-80) that devil's advocate cites is a run-engine feature, not a guided-workflow feature, and grafting it onto 008 would expand the spec's scope beyond its stated boundary.

---

## Safe Agreements

### 1. Schema compatibility is correctly maintained

Devil's advocate (review lines 13-15) confirms that FR-011 is satisfied: generated YAML uses the same schema as hand-crafted configs, with no schema extensions. My own review reached the same conclusion (review lines 138-144), noting a "verbatim match" between spec and SKILL.md on this requirement. Both reviews cite the same evidence: spec line 57, SKILL.md line 1231, and the generated YAML structure at SKILL.md lines 1233-1250.

### 2. Subcommand dispatch integration is sound

Devil's advocate (review lines 16-17) and my review (review lines 187-193) both confirm that the spec correctly depends on 007's dispatch infrastructure and that SKILL.md correctly routes the `interests` and `mode` subcommands. Devil's advocate cites SKILL.md lines 19-37; my review cites SKILL.md lines 932-939 for prerequisite routing.

### 3. User confirmation gates are consistently implemented

Devil's advocate (review lines 22-23) cites spec lines 38, 55, 103 as requiring user confirmation, mapped to SKILL.md line 1020. My review confirms this for interests (review lines 70-77) and mode (review lines 118-124). Both reviews agree that the implementation does not allow silent writes of either `interests.md` or `conversus.yml`.

### 4. Agent name validation is consistent

Devil's advocate (review line 21) cites spec line 964 and SKILL.md line 198 for the `[a-z0-9][a-z0-9-_]*` pattern. My review does not explicitly call this out but references the same validation in the post-write validation section (SKILL.md line 1061). No disagreement.

### 5. Preset integration is correctly scoped as optional

Devil's advocate (review lines 18-19) and my review (review lines 80-87) both confirm that FR-006 treats preset matching as optional ("MAY reference presets"), with the soft dependency on spec 004 being appropriate. My review additionally notes that SKILL.md adds merge semantics for documentation paths (line 990), which both reviews consider a reasonable extension.

### 6. `problem.md` draft status behavior is undefined

Devil's advocate's recommendation #6 (review line 99) flags that spec 008 never defines how `interests` should treat `problem.md` with `status: draft` or unresolved `[CLARIFY:]` tags. My review independently identified the same gap (review lines 195-199) from the SKILL.md side: the Interest Generation table (lines 957-962) has no row for handling a `[CLARIFY: ...]`-tagged Type field. Both reviews agree this is a real gap that needs resolution. Devil's advocate approaches it from the spec side (should `interests` warn or block?); my review approaches it from the implementation side (what calibration style to use?). Both need answers.

---

## Referenced Documentation

| Document | Lines Referenced | Topic |
|---|---|---|
| Devil's advocate review | 13-23 | Alignment section |
| Devil's advocate review | 29-37 | Decision matrix confidence challenge |
| Devil's advocate review | 39-47 | Heuristic detection challenge |
| Devil's advocate review | 49-57 | interests.md value challenge |
| Devil's advocate review | 63-73 | Missed opportunities (feedback loop, cost estimate) |
| Devil's advocate review | 76-83 | Missed opportunities (cross-validation, deduplication) |
| Devil's advocate review | 89-99 | Actionable recommendations |
| Functional-typing review | 17-26, 58-66, 70-77 | FR compliance (interests schema, presets, existing file check) |
| Functional-typing review | 92-104 | Ambiguous row divergence finding |
| Functional-typing review | 138-144 | FR-011 schema compliance |
| Functional-typing review | 176-185 | Preset field schema divergence |
| Functional-typing review | 195-199 | CLARIFY-tagged Type handling gap |
| Spec 008 | Lines 17-18 | Two-command architecture rationale |
| Spec 008 | Lines 44-52 | Decision matrix with ambiguous row |
| Spec 008 | Lines 63-68 | Heuristic mode detection signals |
| Spec 008 | Line 104 | Constraint: no agents without confirmation |
| SKILL.md | Lines 834-850 | Problem type taxonomy (intentionally closed) |
| SKILL.md | Lines 1097 | Mode runs in main conversation |
| SKILL.md | Lines 1138-1145 | Decision matrix and ambiguous fallback |
| SKILL.md | Lines 1147-1156 | Heuristic mode detection |
| SKILL.md | Lines 1193-1210 | Mode confirmation gate |
| SKILL.md | Lines 1304-1306 | Agent launch count formula |
