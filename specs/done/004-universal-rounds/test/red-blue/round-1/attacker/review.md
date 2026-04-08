# Attack Surface Analysis: Spec 004 — Universal Rounds, Stagnation Detection, and Arbitration

**Attacker**: Red Team Security & Correctness Reviewer
**Target**: Spec 004 implementation (universal rounds extension)
**Date**: 2026-03-20
**Verdict**: HIGH overall threat — multiple heading mismatches, missing template variables, and silent data loss paths that will cause production failures in non-cooperative multi-round runs.

---

## Executive Summary

Spec 004 extends `rounds > 1`, `stagnation: detect`, and `arbiter` from cooperative-only to all four competition modes. The implementation strategy is template-first: remove two validation gates, add six new templates (three cross-round syntheses, three arbitration templates), and update the Phase 6 heading validation table. The spec claims this is a minimal-risk extension because "cooperative mode behavior is untouched" and "the engine already implements rounds, stagnation, and arbitration generically."

This claim is dangerously incomplete. The engine's round-awareness is NOT generic — it is cooperative-specific in several critical respects that the spec and implementation fail to address. The Phase 1-5 templates for non-cooperative modes do not contain the `{PRIOR_ROUND_SECTION}` variable that makes agents round-aware, meaning Round 2+ agents in red-blue, winner-take-all, and prisoners-dilemma modes will have no instruction to read the prior round's synthesis. The non-cooperative arbitration templates omit the `{REMAINING_DISPUTES}` variable, forcing arbiters to parse entire synthesis documents instead of receiving pre-extracted disputes. And the spec's FR-009 heading table is internally inconsistent with the actual SKILL.md heading table that was deployed, creating a three-way mismatch between spec, SKILL.md, and template content.

The single most dangerous flaw: **non-cooperative round 2+ agents are blind to prior rounds** because no non-cooperative Phase 1 template contains `{PRIOR_ROUND_SECTION}`. A multi-round red-blue run will execute Round 2 agents with no instruction to read Round 1's synthesis, producing a Round 2 that ignores Round 1's risk findings entirely. This defeats the purpose of multi-round deliberation.

---

## Threat Catalog

### Category 1: Template Variable Gaps

**THREAT-01: Missing `{PRIOR_ROUND_SECTION}` in all non-cooperative Phase 1 templates** (Severity: CRITICAL)

- **Attack vector**: Run any non-cooperative mode with `rounds: 2`. Round 2 agents receive `{PRIOR_ROUND_SECTION}` as an empty variable expansion (or literal unreplaced text) because the Phase 1 review templates for red-blue, winner-take-all, and prisoners-dilemma do not include this variable anywhere in their template body.
- **Evidence**:
  - `templates/cooperative/review.md` L21 contains `{PRIOR_ROUND_SECTION}`.
  - `templates/red-blue/review.md` — searched for `PRIOR_ROUND_SECTION`, `PRIOR_ROUND`, `{ROUND}`, `{MAX_ROUNDS}`: zero matches. Same for `templates/winner-take-all/review.md` and `templates/prisoners-dilemma/review.md`.
  - SKILL.md L368-375 defines `{PRIOR_ROUND_SECTION}` as a variable available in ALL Phase 1-5 templates, and specifies that when `{PRIOR_SYNTHESIS_PATH}` is non-empty (Round 2+), it expands to a block instructing agents to read the prior round's synthesis.
  - Spec 004 FR-010 (L182) states: "The existing round-aware template variables... must be populated for all modes, not just cooperative. This is likely already the case in the orchestrator implementation but must be verified." The orchestrator populates the variables, but the templates do not USE them. Population without consumption is inert.
- **Blast radius**: All non-cooperative multi-round runs. Round 2+ agents in red-blue, WTA, and PD modes will not be instructed to read the prior round's synthesis. They will repeat Round 1 analysis independently, producing duplicative rather than iterative output. The entire game-theory justification for multi-round red-blue (Section 3 of the spec: "Red agents read the prior round's synthesis and adapt attacks") is unfulfilled.
- **Likelihood**: Certain — the templates provably do not contain the variable.

**THREAT-02: Missing `{REMAINING_DISPUTES}` in non-cooperative arbitration templates** (Severity: HIGH)

- **Attack vector**: Run any non-cooperative mode with an arbiter. The Phase 6 agent receives no pre-extracted disputes section.
- **Evidence**:
  - `templates/cooperative/arbitration.md` L34-40 contains `## Extracted Remaining Disputes` with `{REMAINING_DISPUTES}` variable.
  - `templates/red-blue/arbitration.md`, `templates/winner-take-all/arbitration.md`, `templates/prisoners-dilemma/arbitration.md` — searched for `REMAINING_DISPUTES`: zero matches across all three files.
  - SKILL.md L569 defines `{REMAINING_DISPUTES}` as a Phase 6 template variable with extraction logic (primary: structural markers, fallback: heading-based, default: empty string).
- **Blast radius**: Non-cooperative arbitration quality. The arbiter must parse the entire synthesis to find disputes instead of having them pre-extracted. This degrades arbitration precision — the arbiter may miss disputes or include non-dispute content in its scope. The cooperative template explicitly handles this with a fallback instruction ("If this section is empty, read the full synthesis"), but the non-cooperative templates lack even this graceful degradation.
- **Likelihood**: Certain — the templates provably do not use the variable.

**THREAT-03: No round-aware variables (`{ROUND}`, `{MAX_ROUNDS}`) in non-cooperative Phase 1-5 templates** (Severity: MEDIUM)

- **Attack vector**: Non-cooperative Phase 1-5 agents receive no context about which round they are executing in. The variables are populated by the orchestrator but unused by the templates.
- **Evidence**: Searched all files in `templates/red-blue/`, `templates/winner-take-all/`, and `templates/prisoners-dilemma/` for `{ROUND}` and `{MAX_ROUNDS}` — only found in the cross-round-synthesis templates (which are post-round-loop, not within rounds). The cooperative review template also does not contain `{ROUND}` directly but receives it via `{PRIOR_ROUND_SECTION}` expansion.
- **Blast radius**: Agent confusion in multi-round runs. Agents have no prompt-level awareness that they are in Round 2 of 3 versus Round 1 of 1. Without this context, agents cannot calibrate their depth of analysis or reference which round they are contributing to in their output.
- **Likelihood**: Certain for any multi-round non-cooperative run.

### Category 2: Heading Mismatches (Stagnation Detection & Phase 6 Validation)

**THREAT-04: Spec FR-009 heading table contradicts deployed SKILL.md heading table** (Severity: HIGH)

- **Attack vector**: Spec FR-009 (L173-178) defines required Phase 6 headings. The SKILL.md implementation (L587-592) uses DIFFERENT headings for at least two modes. Developers referencing the spec will have a different expectation than what the engine validates.
- **Evidence**:
  - Spec FR-009 for red-blue: `Process Note, Risk Framework, Binding Risk Decisions, Residual Risk Summary`
  - SKILL.md L590 for red-blue: `Process Note, Decision Framework, Binding Decisions, Updated Risk Register`
  - Spec FR-009 for winner-take-all: `Process Note, Selection Criteria, Winner Declaration, Runner-Up Assessment`
  - SKILL.md L591 for winner-take-all: `Process Note, Decision Framework, Verdict Review, Binding Decision`
  - Spec FR-009 for prisoners-dilemma: `Process Note, Boundary Framework, Binding Boundary Decisions, Cooperation Assessment`
  - SKILL.md L592 for prisoners-dilemma: `Process Note, Decision Framework, Binding Decisions, Revised Responsibility Map`
  - The SKILL.md headings match the actual template section headings (verified by searching each template). The spec headings match NEITHER the SKILL.md nor the templates.
- **Blast radius**: The spec is the design document that future developers will reference. The three-way divergence (spec says one thing, SKILL.md says another, templates produce a third — though SKILL.md and templates now agree) means the spec is already stale on the day of its creation. Any spec-driven review or audit will flag false discrepancies.
- **Likelihood**: Certain — the text is provably different. The spec was written before the templates were finalized and never reconciled.

**THREAT-05: Winner-take-all stagnation detection uses `## Runner-Up` presence, not dispute count** (Severity: MEDIUM)

- **Attack vector**: The Dispute-Parsing Subsystem (SKILL.md L675) defines WTA fallback stagnation detection as: "Look for `## Runner-Up` heading (presence indicates a contested decision)." This is a boolean test (heading present = disputes exist), not a count-based test. Stagnation detection requires count comparison across rounds (SKILL.md L475: "current round's count is greater than or equal to the prior round's count"). A boolean presence check always returns the same value (the `## Runner-Up` section is always present in WTA synthesis), making stagnation detection for WTA trivially true from Round 1.
- **Evidence**:
  - SKILL.md L675: winner-take-all fallback is `## Runner-Up` presence.
  - WTA synthesis template `templates/winner-take-all/synthesis.md` L88: `## Runner-Up` is a mandatory section — it always appears.
  - WTA cross-round synthesis template `templates/winner-take-all/cross-round-synthesis.md` L84: `## Runner-Up` is also a mandatory section.
  - The structural markers `<!-- CONVERSUS:DISPUTES_BEGIN -->` / `<!-- CONVERSUS:DISPUTES_END -->` wrap `### Remaining Disputes` in the WTA synthesis template (L106-110), which IS count-based. But the fallback heading `## Runner-Up` is always present.
  - Spec FR-002 (L105) says WTA heading is `### Remaining Disputes` with "Any dispute entry" pattern, but SKILL.md L675 says `## Runner-Up`. These disagree.
- **Blast radius**: If structural markers are absent from synthesized output (which happens if the LLM drops them — a known failure mode), the fallback heading detection will find `## Runner-Up` in every WTA synthesis, making the boolean always true. Stagnation detection will see "disputes present" in every round and will NEVER trigger stagnation for WTA. The round loop will always run to max rounds.
- **Likelihood**: Possible — depends on whether the LLM preserves structural markers. The spec itself acknowledges marker-based extraction may fail (SKILL.md L569: "The marker upgrade should be tracked as a continuation item").

**THREAT-06: Winner-take-all stagnation detection is structurally undefined for count-based comparison** (Severity: MEDIUM)

- **Attack vector**: Even when structural markers are present, the WTA `### Remaining Disputes` section (inside markers) does not use a consistent entry pattern like `**Dispute:` (cooperative) or `**[RISK-ID]:` (red-blue). The WTA synthesis template (L107-109) instructs: "If any criteria scores were too close to call, or if evidence was genuinely ambiguous on a decisive criterion, note those contested points here. If the verdict is clear, state: 'No remaining disputes — verdict is decisive.'" This is free-form text, not a countable pattern.
- **Evidence**: Spec FR-002 L105 says entry pattern is "Any dispute entry" with count-based stagnation. But what constitutes a countable "entry" in free-form text? The cooperative mode counts `**Dispute:` entries. Red-blue counts `**[RISK-ID]:` entries. PD counts `### [` sub-headings. WTA has no defined entry pattern, making dispute counting ambiguous.
- **Blast radius**: WTA stagnation detection may produce inconsistent counts across rounds depending on how the LLM formats its disputes, leading to false stagnation or missed stagnation.
- **Likelihood**: Likely — the absence of a defined entry pattern makes counting implementation-dependent.

### Category 3: Arbitration Template Quality

**THREAT-07: Non-cooperative arbitration templates lack dispute-extraction section** (Severity: MEDIUM)

- **Attack vector**: The cooperative arbitration template (L34-40) includes a dedicated `## Extracted Remaining Disputes` section that pre-populates the arbiter with extracted disputes via `{REMAINING_DISPUTES}`. The red-blue, WTA, and PD arbitration templates rely on the arbiter reading the full synthesis to find disputes. This means:
  1. The arbiter may miss disputes embedded in lengthy syntheses.
  2. The arbiter may include non-dispute content in its scope.
  3. The arbiter's output quality is degraded compared to cooperative mode.
- **Evidence**: See THREAT-02 evidence. The cooperative template explicitly handles the empty-extraction case. Non-cooperative templates have no extraction scaffolding at all.
- **Blast radius**: Reduced arbitration precision in all non-cooperative modes. The arbiter is told to "Pay special attention to the synthesis's 'Disputed Risks' section" (red-blue, L32) but receives no pre-extracted content, unlike cooperative mode.
- **Likelihood**: Certain — structural difference between cooperative and non-cooperative templates.

**THREAT-08: Red-blue arbitration "Updated Risk Register" heading mismatch with Phase 6 validation** (Severity: LOW)

- **Attack vector**: The red-blue arbitration template instructs the agent to produce `### Updated Risk Register` (L92). SKILL.md Phase 6 validation (L590) checks for `Updated Risk Register`. These currently match. But the spec FR-009 (L176) says the required heading should be `Residual Risk Summary`. If someone "fixes" the implementation to match the spec, validation will break against the template.
- **Evidence**: Spec L176 vs SKILL.md L590 vs template L92. Three-way state: spec says one thing, implementation says another, both template and SKILL.md agree with each other but not the spec.
- **Blast radius**: Future maintenance confusion. Spec-driven changes will introduce regressions.
- **Likelihood**: Possible — depends on whether anyone uses the spec as the source of truth for future changes.

### Category 4: Edge Cases

**THREAT-09: Red-blue Phase 4 disputes template uses `### Remaining Disputes`, not `### Disputed Risks`** (Severity: LOW)

- **Attack vector**: The red-blue disputes template (`templates/red-blue/disputes.md` L93) instructs blue-team agents to write a `### Remaining Disputes` section in their Phase 4 output. But the Dispute-Parsing Subsystem (SKILL.md L676) looks for `### Disputed Risks` in red-blue mode. These are different headings.
- **Evidence**: `templates/red-blue/disputes.md` L93: `### Remaining Disputes`. SKILL.md L676: "Look for `### Disputed Risks` heading."
- **Blast radius**: LIMITED in practice — the Dispute-Parsing Subsystem reads the Phase 5 SYNTHESIS, not Phase 4 dispute documents. Phase 5's red-blue synthesis template correctly uses `### Disputed Risks` (L114). But the heading mismatch between Phase 4 and Phase 5 creates confusion and could cause issues if Phase 4 outputs are ever parsed directly.
- **Likelihood**: Low — the parsing subsystem reads synthesis, not disputes. But the naming inconsistency is a code smell.

**THREAT-10: Cross-round synthesis templates lack `DISPUTES_BEGIN`/`DISPUTES_END` structural markers** (Severity: HIGH)

- **Attack vector**: The per-round Phase 5 synthesis templates for all modes include `<!-- CONVERSUS:DISPUTES_BEGIN -->` / `<!-- CONVERSUS:DISPUTES_END -->` structural markers around the disputes section. The cross-round synthesis templates (all four modes) do NOT include these markers.
- **Evidence**:
  - Searched `templates/*/cross-round-synthesis.md` for `DISPUTES_BEGIN`: zero matches.
  - Per-round synthesis templates all have markers: cooperative L103/113, red-blue L113/125, WTA L106/110, PD L97/117.
  - SKILL.md L540 states the Phase 6 trigger reads "the definitive synthesis output file (`{output}/summary/final.md`)." For multi-round runs, this is the cross-round synthesis. The cross-round synthesis lacks structural markers, so dispute extraction will fall back to heading-based parsing.
- **Blast radius**: In multi-round runs with an arbiter, Phase 6 trigger evaluation and `{REMAINING_DISPUTES}` extraction will always use the degraded heading-based fallback (or the "neither found" default of `true`). This means:
  1. `{REMAINING_DISPUTES}` extraction is less precise for multi-round runs.
  2. Phase 6 trigger evaluation relies on heading matching, which is fragile.
  3. The stable interface contract (SKILL.md L683) for markers is violated — the cross-round synthesis is a synthesis output but doesn't honor the marker contract.
- **Likelihood**: Certain for any multi-round run with an arbiter — cross-round synthesis templates provably lack markers.

**THREAT-11: `stagnation: detect` with `arbiter` and `trigger: disputes_remain` in red-blue mode creates conflicting termination** (Severity: LOW)

- **Attack vector**: Configure red-blue with `rounds: 3`, `stagnation: detect`, and `arbiter` with `trigger: disputes_remain`. Scenario: Round 1 produces 3 disputed risks. Round 2 also produces 3 disputed risks. Stagnation is detected (count >= prior), round loop terminates at Round 2 with `termination_reason: stagnation`. But 3 disputes remain. Phase 6 trigger fires. The arbiter resolves all 3. The final state is "stagnation detected" but "all disputes resolved" — contradictory narratives. The cross-round synthesis says "stagnation" while the arbitration says "resolved."
- **Evidence**: SKILL.md L474-479 (stagnation detection) and L539-541 (Phase 6 trigger). These are independent mechanisms that don't communicate. Stagnation terminates the round loop but doesn't prevent Phase 6, and Phase 6 doesn't know that stagnation was the reason for termination.
- **Blast radius**: Confusing output narrative. Not a functional failure but a user-experience issue.
- **Likelihood**: Possible — depends on deliberation dynamics.

### Category 5: Backward Compatibility

**THREAT-12: Cooperative mode backward compatibility is preserved — but fragile** (Severity: LOW)

- **Attack vector**: The spec claims "No existing behavior changes" (L212). This is technically true. But the SKILL.md edit that replaced the Phase 6 heading validation table (from a single set of headings to a mode-keyed table) touches cooperative mode's validation path. Any error in the table edit could break cooperative validation.
- **Evidence**: SKILL.md L587-592 shows the mode-keyed table. The cooperative row (`Process Note, Decision Framework, Binding Decisions, Summary of Changes Required`) matches the cooperative arbitration template's actual headings. Verified.
- **Blast radius**: If the table is malformed, cooperative Phase 6 validation emits spurious warnings. But since validation is informational (not blocking per SKILL.md L583), this would only cause false warnings, not failures.
- **Likelihood**: Low — the table has been verified to match.

---

## Cascading Failures

### Cascade 1: "Blind Round 2" — Multi-round non-cooperative runs produce independent parallel analyses instead of iterative deepening

- **Trigger**: THREAT-01 (missing `{PRIOR_ROUND_SECTION}` in non-cooperative review templates).
- **Propagation**: Round 2 agents in red-blue mode write their reviews without reading Round 1's synthesis. Red team attacks the same surface issues. Blue team defends the same positions. Phase 5 Round 2 synthesis sees no evolution because there was none.
- **Terminal state**: Stagnation is detected after Round 2 (THREAT-01 -> THREAT-05 compound: dispute counts stay the same because agents didn't engage with prior rounds). The cross-round synthesis reports "stagnation" but the real cause is that agents were never told about Round 1. The user concludes "multi-round red-blue doesn't work" when the real bug is a missing template variable. Resources wasted on N rounds that produced the same output.

### Cascade 2: "Phantom Stagnation in WTA" — Winner-take-all always runs to max rounds or always stagnates on Round 2

- **Trigger**: THREAT-05 (WTA stagnation uses `## Runner-Up` heading presence) combined with THREAT-06 (no countable entry pattern for WTA disputes).
- **Propagation**: If structural markers are preserved by the LLM: the `### Remaining Disputes` section content is parsed. But without a defined entry pattern, the count is ambiguous. If markers are dropped: fallback to `## Runner-Up`, which is always present. Count = 1 (boolean true). Round 1 count = 1, Round 2 count = 1. Stagnation detected.
- **Terminal state**: WTA stagnation detection is either meaningless (always 1) or underdefined (free-form text counting). Either way, the `stagnation: detect` feature does not work correctly for WTA mode.

### Cascade 3: "Markerless Arbiter" — Multi-round runs with arbitration always use degraded dispute extraction

- **Trigger**: THREAT-10 (cross-round synthesis lacks structural markers) combined with THREAT-02 (non-cooperative arbitration templates lack `{REMAINING_DISPUTES}`).
- **Propagation**: In a multi-round non-cooperative run with an arbiter: (1) cross-round synthesis is produced without `DISPUTES_BEGIN`/`DISPUTES_END` markers; (2) Phase 6 trigger evaluation falls back to heading-based parsing; (3) `{REMAINING_DISPUTES}` extraction finds no markers, falls back to heading, or returns empty string; (4) but the non-cooperative arbitration templates don't even use `{REMAINING_DISPUTES}`, so step 3 is moot — the variable is populated but not consumed.
- **Terminal state**: The arbiter in non-cooperative multi-round runs receives no pre-extracted disputes from any pathway. The arbiter must manually parse a potentially lengthy cross-round synthesis to find disputed items. Arbitration quality degrades proportionally to synthesis length.

---

## Missing Safeguards

### 1. Template completeness validation for round-aware variables

- **What is absent**: No mechanism verifies that templates for modes claiming `rounds > 1` support actually contain the round-aware variables (`{PRIOR_ROUND_SECTION}`, `{ROUND}`, `{MAX_ROUNDS}`). The orchestrator populates them, but consumption is entirely up to templates.
- **Why it is necessary**: The spec explicitly claims round-awareness extends to all modes (FR-010). Without validation, a template can claim to support multi-round execution while being structurally single-round-only. This is the root cause of THREAT-01.
- **Consequence of absence**: Silent functional degradation. Multi-round runs execute without error but produce duplicative rather than iterative output.

### 2. Structural marker contract enforcement for cross-round synthesis templates

- **What is absent**: No validation that cross-round synthesis templates include `<!-- CONVERSUS:DISPUTES_BEGIN -->` / `<!-- CONVERSUS:DISPUTES_END -->` markers. The stable interface contract (SKILL.md L683) is stated but not enforced.
- **Why it is necessary**: Phase 6 trigger evaluation and `{REMAINING_DISPUTES}` extraction depend on these markers for precision. Cross-round synthesis is the "definitive synthesis" that Phase 6 reads. Without markers, every multi-round-with-arbiter run uses degraded extraction.
- **Consequence of absence**: Systematic degradation of arbitration quality in all multi-round runs (THREAT-10).

### 3. Entry pattern definition for winner-take-all dispute counting

- **What is absent**: WTA mode has no defined dispute entry pattern in FR-002 or the Dispute-Parsing Subsystem. Cooperative uses `**Dispute:`, red-blue uses `**[RISK-ID]:`, PD uses `### [` sub-headings. WTA says "Any dispute entry" — which is not a parseable pattern.
- **Why it is necessary**: Stagnation detection requires dispute counting. Counting requires a defined pattern.
- **Consequence of absence**: WTA stagnation detection is undefined behavior (THREAT-06).

### 4. Spec-to-implementation reconciliation check

- **What is absent**: No process ensured the spec's FR-009 heading table was updated after the templates were finalized. The spec was written with placeholder headings (`Risk Framework`, `Binding Risk Decisions`, `Selection Criteria`, `Winner Declaration`, `Boundary Framework`, `Binding Boundary Decisions`, `Cooperation Assessment`) that were never used in the actual templates.
- **Why it is necessary**: The spec is the design document. If it diverges from implementation on the day of creation, it provides negative value — readers who trust the spec will make incorrect assumptions about the system's behavior.
- **Consequence of absence**: Three-way mismatch between spec, SKILL.md, and templates (THREAT-04). Future maintenance guided by the spec will introduce regressions.

### 5. Cross-template `{REMAINING_DISPUTES}` parity

- **What is absent**: No mechanism ensures all arbitration templates use the same variable interface. The cooperative template uses `{REMAINING_DISPUTES}`; the other three do not. This asymmetry is undocumented.
- **Why it is necessary**: The orchestrator computes `{REMAINING_DISPUTES}` for all modes (SKILL.md L569 makes no mode distinction). The computation cost is paid but the result is discarded in 3 of 4 modes.
- **Consequence of absence**: Arbitration quality asymmetry between cooperative and non-cooperative modes (THREAT-02, THREAT-07).

### 6. WTA fallback heading alignment with actual dispute section

- **What is absent**: The Dispute-Parsing Subsystem's fallback heading for WTA (`## Runner-Up`) does not point to the actual disputes section (`### Remaining Disputes`). There is no safeguard ensuring fallback headings point to countable dispute content.
- **Why it is necessary**: The fallback heading is the safety net when structural markers are absent. If it points to a non-dispute section, the safety net catches the wrong thing.
- **Consequence of absence**: WTA Phase 6 trigger always fires (runner-up always exists), and stagnation detection is meaningless for WTA when markers are absent (THREAT-05).
