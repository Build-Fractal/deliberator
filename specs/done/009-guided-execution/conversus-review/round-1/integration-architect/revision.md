# Integration Architect Revision: 009-Guided-Execution

**Reviewer**: integration-architect
**Spec**: `009-guided-execution`
**Phase**: 3 (Post-Cross-Review Revision)
**Date**: 2026-03-22

---

## Recommendation Dispositions

### P0: Replace `/conversus arbitrate` dead reference with actionable workaround

**Original recommendation**: Replace `/conversus arbitrate` suggestions in the post-execution report with actionable workaround guidance until the `arbitrate` subcommand is implemented.

**Cross-review input**: FT agrees on substance, rates it P1, suggests gating the suggestion or adding "(coming soon)." DA agrees the dead reference is a real problem, notes the root cause is in the spec itself (FR-009 says "suggest `/conversus arbitrate`" without acknowledging the command does not exist), and calls out a tension between my ALIGNED-with-caveat verdict on FR-009 and my P0 severity rating.

**Disposition**: **KEEP at P0, sharpen the verdict and the fix.**

DA is right that my original review contains an internal tension: I marked FR-009 as "ALIGNED (with caveat)" while simultaneously calling the issue P0 flow-breaking. These are incompatible positions. I revise FR-009 to **ALIGNED (literal) / MISALIGNED (intent)**. The implementation literally does what FR-009 says -- it suggests `/conversus arbitrate`. But the intent of FR-009, read in context with SC-001 (non-expert usability), is to give the user a working path forward. A suggestion that produces an "Unknown subcommand" error is not a working path.

The fix combines my original recommendation with FT's framing: replace the `/conversus arbitrate` suggestion with the manual workaround ("configure an `arbiter:` section in `conversus.yml` and re-run `/conversus converge`") and add a note that a dedicated `/conversus arbitrate` subcommand is planned. This gives users an actionable path today and sets expectations for the future. The fix applies to SKILL.md lines 1469, 1488, and the spec's FR-009 text should be updated to say "suggest how to resolve disputes" rather than naming a specific subcommand that may not exist yet.

---

### P1: Add `--output <dir>` flag to converge handler

**Original recommendation**: Add `--output <dir>` flag for consistency with `define`, `interests`, and `mode` handlers.

**Cross-review input**: FT agrees at P1 priority. DA lists it as a real gap (Safe Agreement #6 in DA's cross-review of my review). Neither reviewer contests it.

**Disposition**: **KEEP at P1, uncontested.**

All three upstream handlers (`define`, `interests`, `mode`) accept `--output <dir>`. The converge handler reads from the working directory only (line 1336). A user who ran the guided workflow with `--output my-delib/` cannot use `converge` without `cd my-delib/` or file relocation. This breaks the guided flow for a legitimate usage pattern the upstream handlers explicitly support.

---

### P2: Add plain-language failure handling for delegated `run` errors

**Original recommendation**: Add a brief failure-handling clause for when the delegated `/conversus run` fails.

**Cross-review input**: FT raises a related pre-flight concern (validation error preview in pre-execution summary) and notes the complementary relationship -- pre-flight warnings vs. post-flight error translation. DA frames the same gap more aggressively as a missing failure recovery position (Missed Opportunity #2), arguing the spec should at minimum state that partial recovery is not supported.

**Disposition**: **KEEP at P2, expand scope to include DA's acknowledgment requirement.**

My original recommendation was too narrow -- "present the error in plain language" addresses the symptom but not the cost. DA is correct that a non-expert who burns 34 successful agent calls and loses them to a Phase 5 failure needs to know the recovery position, even if that position is "full re-run required." The revised recommendation: add a failure-handling clause that (1) translates the engine error to plain language, (2) states explicitly that failures require a full re-run, and (3) notes that resume capability is deferred to future work. This costs one paragraph in the spec and sets correct expectations for the target persona.

---

### P2: Extend staleness check to include `problem.md`

**Original recommendation**: Compare `problem.md` modification time against `conversus.yml` in addition to `interests.md`.

**Cross-review input**: DA challenges the entire mtime-based mechanism as unreliable (git operations, autosaves, content-irrelevant timestamp changes) and argues that extending the check to `problem.md` would increase false positives. DA proposes content hashing instead. FT did not raise staleness concerns but agrees in cross-review that the extension is well-motivated.

**Disposition**: **WITHDRAW. Reframe as a spec 008 concern.**

DA's challenge forced me to think harder about where the fix belongs. In my own cross-review of DA, I concluded that staleness is a spec 008 problem, not a spec 009 problem. The mode handler (spec 008) generates `conversus.yml` and knows which source files contributed to it. Spec 008 should embed provenance metadata (content hashes of `problem.md` and `interests.md`) into `conversus.yml` at generation time. The converge handler then reads those hashes and compares. This design is correct because: (1) the config generator knows the inputs, (2) the config consumer just verifies, (3) no new schema is added by the converge handler itself. Extending the mtime check within converge is a band-aid that belongs in the wrong spec.

FT's point that content hashing would burden hand-crafted configs is valid -- a hand-crafted `conversus.yml` without hash fields would always trigger the warning. The spec 008 design should make the hash fields optional: if present, verify; if absent, skip the staleness check. This preserves the hand-crafted-config constraint (spec 009, Section 4).

---

### P3: Clarify that "Estimated agent launches" is an upper bound

**Original recommendation**: Note in the post-execution report that the estimate is a maximum, not a prediction.

**Cross-review input**: DA argues the number is meaningless to non-experts regardless of whether it is labeled as an upper bound or an estimate, and proposes adding time/cost context. FT agrees the number is opaque. Both cross-reviews of my review note I underweighted the UX impact.

**Disposition**: **SUPERSEDED by new recommendation (see below).**

DA and FT are both right that I focused on mathematical accuracy ("upper bound is still an estimate") while missing the interpretability gap. The target persona (SC-001) has no mental model for what "16 agent launches" means. Clarifying it is an upper bound does not help a user who does not know what an agent launch costs. The fix is not better labeling -- it is better framing. See New Recommendation #1 below.

---

### Not in original: Fix "Problem" label to "Mode" (raised by FT, confirmed in cross-review)

**Cross-review input**: FT's P1 recommendation to rename the `Problem:` label at SKILL.md line 1377 to `Mode:`. DA escalates this further, arguing the summary should include both the problem statement from `problem.md` and the mode.

**Disposition**: **ACCEPT as P1. Fix the label; defer problem-statement inclusion.**

I missed this in my original review. FT is correct: the pre-execution summary labels its first field `Problem:` but fills it with the mode and its plain-language explanation. The post-execution report correctly uses `Mode:` at line 1439. This is an internal inconsistency within the handler. The fix is a one-line change: rename `Problem:` to `Mode:` at line 1377.

DA's escalation -- that the summary should also include the actual problem statement from `problem.md` -- is compelling but expands scope. FR-001 lists "mode (plain-language explanation)" as a required summary element. It does not list the problem definition. Adding it would be a spec amendment, not a bug fix. I agree it would improve informed consent, but it belongs in a follow-up, not in this fix.

---

### Not in original: Formula discrepancy in Important Notes (raised by DA, confirmed in cross-review)

**Cross-review input**: DA identified that the Step 4 formula and the Important Notes simplified formula disagree for N=3, iterations=1 (16 vs. 13). In my cross-review of DA, I traced the root cause: the Important Notes section (line 1517) has an internal arithmetic error. The left side `N + N*(N-1) + N + N + 1` expands to `N^2 + 2N + 1`, but the right side claims `N^2 + N + 1`, dropping a term. Phase 4 (Disputes, N agents) is the missing component. FT independently confirmed this analysis in their cross-review of DA, noting the Important Notes simplified formula "drops Phase 4 entirely."

**Disposition**: **ACCEPT as P1. Fix the Important Notes arithmetic.**

This is a concrete bug I should have caught in my original review. I cited the formula at line 155 of my review and verified SC-004 without cross-checking against Important Notes. The Step 4 formula used by the converge handler (line 1404) is correct. The Important Notes simplified formulas need correction:

- Line 1517: `N^2 + N + 1` should be `N^2 + 2N + 1`
- Line 1518: `N^2 + N + 2` should be `N^2 + 2N + 2`
- Line 1519: "13 total agent launches" should be "16 total agent launches"
- Line 1520: "14 total agent launches" should be "17 total agent launches"
- Line 1524: "3 * 13 + 1 = 40" should be "3 * 16 + 1 = 49"
- Line 1525: "3 * 25 + 1 = 76" should be "3 * 25 + 1 = 76" (verify: for iterations=2, per_round = 3 + 2*(6+3) + 3 + 1 = 25; this line is correct)

---

### Not in original: Speckit integration is spec drift (raised by DA, unaddressed in original)

**Cross-review input**: DA flags the `/speckit.specify --input {output}/summary/final.md` next step at SKILL.md lines 1504-1507 as spec drift. FT did not raise it. DA's cross-review of my review notes I "either missed it or implicitly accepted it under the same 'superset' reasoning."

**Disposition**: **ACCEPT as P2. Add spec acknowledgment, do not remove.**

DA caught something I missed. The speckit integration is not authorized by any FR in spec 009. My original review applied "superset, not a violation" reasoning to FR-003's "Cancel entirely" option but did not examine the speckit integration at all -- an inconsistency in my review scope.

However, I disagree with DA's recommendation to remove it from the SKILL.md. FR-008 requires "suggested next steps based on outcome" without enumerating a closed set of permitted suggestions. A cross-tool suggestion under this umbrella is a reasonable implementation choice. The fix is to add a brief note to the spec acknowledging that next steps may include cross-tool suggestions when contextually relevant, making the speckit integration spec-authorized rather than spec-drifted. This is cheaper and more useful than removing a genuinely helpful UX affordance.

---

### Not in original: Dispute-parsing file target ambiguity (raised by FT)

**Cross-review input**: FT's P2 recommendation to specify `{output}/summary/final.md` as the explicit file target for dispute parsing at line 1464, rather than "Check the run engine's output." DA's cross-review of FT escalates severity, noting an LLM agent could parse the wrong file in multi-round runs.

**Disposition**: **ACCEPT as P2.**

FT is right that line 1464 should name the specific file. The Dispute-Parsing Subsystem (line 751) takes a file path as input. The post-execution report at line 1442 already references `{output}/summary/final.md`. Line 1464 should do the same for consistency and to eliminate ambiguity for the executing agent. DA's severity escalation is warranted -- in multi-round runs, multiple synthesis files exist in the output tree, and "the run engine's output" is genuinely ambiguous.

---

### Not in original: Prior context disclosure in pre-execution summary (raised by FT)

**Cross-review input**: FT's P2 recommendation to add `Prior context: {paths}` to the pre-execution summary when `PRIOR_FILES` is non-empty. DA's cross-review of FT supports the concern (Tensions #1: the summary omits inputs that influence all agents).

**Disposition**: **ACCEPT as P3.**

FT makes a valid informed-consent argument: prior files silently influence every agent's deliberation, and their omission from the summary means the user consents to something they cannot fully see. I did not raise this in my original review because I implicitly assumed prior files are an advanced feature unlikely in the guided flow. But the spec's Section 4 constraint explicitly permits hand-crafted configs, which may include `prior:` sections. The fix is low-cost -- one conditional line in the summary template.

I rate this P3 rather than FT's P2 because the information gap is real but the impact is narrow: prior files are an advanced configuration dimension, and users who set them are more likely to be aware of their influence than the non-expert persona SC-001 targets.

---

## New Recommendations

### NEW-1 (P2): Add a "What to Expect" narrative to the pre-execution summary

The cross-review process revealed a consensus gap: all three reviewers agree that the agent launch count is opaque to non-experts, but none of us proposed a fix that works within the spec's constraints. DA's recommendation for time/cost estimates requires engine instrumentation that does not exist. My original P3 for clarifying "upper bound" does not address interpretability. FT's suggestion to frame it as out-of-scope defers a problem the spec should own.

DA's alternative suggestion -- explain what happens during execution in plain language -- is the right approach. After the launch estimate line in the pre-execution summary, add a one-sentence explanation:

```
Estimated agent launches: {count}
  (Each agent reads the target documents and writes a review. Agents then cross-review
   each other's work, revise, and a synthesis is produced.)
```

This gives the launch count a frame of reference without requiring engine instrumentation. It serves SC-001 (non-expert usability) and SC-004 (plain-language summary). It adds no execution logic and no new configuration.

---

### NEW-2 (P2): Make delegation semantics explicit in the Execution section

DA raises a legitimate concern that "Delegate to `/conversus run`" is ambiguous in a SKILL.md context. In my cross-review of DA, I conceded this is worth a one-line clarification. The current instruction at line 1426 relies on the executing agent to interpret "delegate" correctly. For clarity, revise to:

```
Proceed to Run: Execution Step 1 through Step 5 using the config already parsed
in the pre-execution summary. Do not re-invoke `/conversus run` as a separate
skill invocation -- continue within the current conversation.
```

This eliminates the ambiguity DA identified without changing the handler's behavior. It makes explicit what was previously implicit: delegation means "follow the Run handler sections in this document," not "start a new invocation."

---

## Position Summary

The cross-review process surfaced three categories of findings.

**Things I missed that I should have caught.** The formula discrepancy in Important Notes is a concrete arithmetic error that I cited the formula's source without verifying. The "Problem" label mislabeling is a one-line inconsistency I overlooked. The speckit integration at lines 1504-1507 is unspec'd behavior I did not examine. All three are now accepted into my recommendation set.

**Things I got right that cross-reviews confirmed.** The `/conversus arbitrate` dead reference is the highest-priority issue across all three reviews. The `--output` flag gap is uncontested. The zero-new-engine-logic constraint verification is independently confirmed by all reviewers. The prerequisite routing permutation analysis holds up.

**Things where cross-review changed my position.** I withdrew my staleness-check extension (P2) after DA's challenge and my own cross-review analysis revealed the fix belongs in spec 008, not spec 009. I superseded my "upper bound" clarification (P3) with a "What to Expect" narrative (NEW-1) after recognizing that the interpretability gap is the real problem, not the labeling. I accepted DA's delegation-semantics concern (NEW-2) as a legitimate fragility in LLM-executed instruction sets.

**Consolidated priority list:**

| Priority | Recommendation | Source |
|----------|---------------|--------|
| **P0** | Fix `/conversus arbitrate` dead reference with workaround + planned note | Original (sharpened) |
| **P1** | Add `--output <dir>` flag to converge | Original |
| **P1** | Fix "Problem" label to "Mode" at line 1377 | FT (accepted) |
| **P1** | Fix Important Notes formula arithmetic (lines 1517-1524) | DA (accepted) |
| **P2** | Add plain-language failure handling with recovery-position statement | Original (expanded) |
| **P2** | Add "What to Expect" narrative to pre-execution summary | NEW-1 |
| **P2** | Make delegation semantics explicit in Execution section | NEW-2 |
| **P2** | Add spec acknowledgment for cross-tool next steps (speckit) | DA (accepted, reframed) |
| **P2** | Specify dispute-parsing file target as `{output}/summary/final.md` | FT (accepted) |
| **P3** | Add prior context disclosure to pre-execution summary | FT (accepted, deprioritized) |
| **WITHDRAWN** | Extend staleness check to `problem.md` (belongs in spec 008) | Original (withdrawn) |
| **SUPERSEDED** | Clarify "upper bound" labeling (replaced by NEW-1) | Original (superseded) |
