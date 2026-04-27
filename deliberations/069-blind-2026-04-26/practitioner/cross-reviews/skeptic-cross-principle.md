# Cross-Review of skeptic-cross-principle

Reviewing skeptic-cross-principle's review against my own (practitioner) review of the Constitutional Inclusion Criteria gate. Both reviews converge on the gate's three-criterion structure and the enforcement vacuum, but diverge sharply on remedies. Skeptic-cross-principle pushes toward structural simplification (collapse the gate into XI + XII); I pushed toward procedural mechanization (PR template + CI lint). The differences are not cosmetic — they pick different theories of what makes a constitutional gate work.

---

### Dangerous Contradictions

1. **Reduce-the-gate vs. mechanize-the-gate is a fork in the road.** Skeptic-cross-principle's Recommendation 10 ("remove the gate entirely and rely on Principle XI + amendment-process discipline") and the headline framing ("more useful as a single-criterion check") collapse the gate into existing principles. My Recommendations 1-2 keep all three criteria but mechanize them via PR template + CI lint. If both go in, the result is incoherent: a gate that has been argued out of existence in the prose but still has a CI lint enforcing its three subsections. The maintainer must pick: structural collapse OR procedural enforcement, not both. This is the most consequential disagreement and downstream readers should treat it as a binary fork.

2. **Skeptic's "merge criterion 3 into XI" silently changes XI's verification posture.** Skeptic-cross-principle Recommendation 1 proposes adding to XI's body: "This principle applies to the constitution itself: a new principle that restates an existing principle in different words is a duplication." Read against XI's *Origin* note (XI was learned from MODE_PRESENCE / INFLUENCE_LEVEL / FR-018 — concrete data duplications detectable by parity tests), this extension turns XI from a *data-duplication* principle into a *prose-duplication* principle, which is exactly the unverifiable kind of rule the gate is meant to exclude. My review did not contemplate this drift. The skeptic's recommendation is more disruptive to XI than it acknowledges and could fail XI's *own* verification posture once amended.

3. **Skeptic time-boxes the grandfather clause; I left it open.** Skeptic-cross-principle Recommendation 4 ("by v3.0.0, an audit MUST evaluate Principles I-XXVII against the gate") imposes a hard deadline. My Recommendation 6 only adds a footnote saying grandfathered prose-principles "should not be cited as precedent." These are not equivalent — the time-box forces a MAJOR-version migration burden onto the project; the footnote leaves the corpus stable but acknowledges the precedent risk. If both recommendations are adopted, the project commits to a v3.0.0 audit *and* a footnote disclaiming grandfathered principles — a contradictory posture (the principles are both retained-as-valid and pre-flagged-for-removal). Pick one stance.

4. **Skeptic's "demote criterion 2 to one sentence" undercuts my "drop criterion 1" alternative.** My Recommendation 3 offered "remove Criterion 1 entirely and rely on Criteria 2 and 3" as an aggressive simplification. Skeptic-cross-principle does the opposite: demotes Criterion 2 to a one-sentence MUST/SHOULD reminder (their Recommendation 3) and keeps Criterion 1 as the load-bearing element. We agree the gate is over-trifurcated but disagree which criterion is the keeper. This is a real contradiction: Criterion 1 is what skeptic considers "genuinely new and load-bearing" while I consider its "concrete enough to sketch in one paragraph" subclause the most unfalsifiable part of the gate. A maintainer reading both reviews will get opposite advice on which criterion to keep.

---

### Tensions

1. **Antipattern catalog routing — productive but partial overlap.** Skeptic-cross-principle Missed Opportunity 6 + Recommendation 9 surface the antipattern catalog as a destination for migrated grandfathered principles. I did not raise this. The recommendation is sound and complementary to my "specify the receiving file and owner" point (my Recommendation 7), but the two recommendations interact: if the antipattern catalog becomes the migration destination, *its* maintainer becomes the owner who must sign off. Neither review carries this through to its conclusion.

2. **Versioning rules for migrations — different framings, both incomplete.** Skeptic-cross-principle Missed Opportunity 8 + Recommendation 7 propose a three-way versioning rule (MAJOR for migration-out, PATCH for adding verification, MINOR for Extension blocks). My Recommendation 9 raised the body-vs-new-principle trade-off but did not propose specific versioning rules. The skeptic's framing is sharper, but it leaves "what version bump for adopting the gate itself" unaddressed. The current constitution shows version "(under review)" — both reviews assume this resolves to MINOR (new principle) but neither says so explicitly.

3. **Extension blocks — skeptic engaged, I sidestepped.** Skeptic-cross-principle Missed Opportunity 9 + Recommendation 8 ("Extension blocks within existing principles ARE amendments and MUST satisfy the gate's verification requirement") is a substantive scope expansion. My review noted the body-bloat incentive (Missed Opportunity 9, Recommendation 9) but did not push the gate's reach into Extension blocks. The skeptic's position is more rigorous; mine is more permissive. Tension, not contradiction — but reasonable maintainers could disagree.

4. **Two-tier-stability assumption — skeptic challenged it, I accepted it.** Skeptic-cross-principle Off-Base Assumption 2 argues the prospective-only design is unstable because future extensions to grandfathered principles get partially gated, producing mixed-tier principles. My review treated the prospective-only carve-out as "correctly drafted." The skeptic's analysis is the stronger one — once Extension blocks (per their Recommendation 8) are gated, every grandfathered principle eventually accumulates a gated extension and the two-tier system ceases to be stable. I should have caught this.

5. **Recursion-of-criterion-1 — same finding, different remedies.** Both reviews flag that "concrete enough to sketch in one paragraph" is itself unfalsifiable (skeptic Missed Opportunity 5; my Missed Opportunity 3). Skeptic recommends a `Verification:` block with structured fields (check type, artifact, failure signal). I recommended naming the artifact location. The skeptic's structured-block proposal is more rigorous and is the better remedy. My version is a subset.

---

### Safe Agreements

1. **The gate has no enforcer.** Both reviews independently identify this as the largest gap. Skeptic-cross-principle Off-Base Assumption 4 + Recommendation 6; my Missed Opportunity 2 + Off-Base Assumption 1 + Recommendation 1/5. The skeptic frames it as "no enforcement path"; I frame it as "self-assessment is a rubber stamp." Same finding, two angles. Any maintainer reading the two reviews will treat this as the priority-1 fix.

2. **Grandfathered prose-principles (VI, X, XVI) would fail Criterion 1 if proposed today.** Both reviews call out the same principles. Skeptic-cross-principle Missed Opportunities 2 + 3; my Missed Opportunity 1 + Recommendation 6. Different remedies (skeptic's time-boxed audit; my footnote disclaiming precedent), but the underlying finding is identical and well-supported. This finding is robust against either set of remedies being adopted.

3. **The constitution-vs-operational-guidance boundary is the gate's most useful contribution.** Skeptic Alignment 5 ("the gate names the right alternative venues"); my Alignment 2 ("pushing 'judgment calls and rules of thumb' into CONTRIBUTING.md, specs, SKILL.md, or domain reference documents is exactly the right home"). Identical positive finding. Whatever the maintainer does with the criteria themselves, the venue-naming should be preserved.

4. **Criterion 3 (distinct-from-existing) needs a worked example.** Skeptic Missed Opportunity 1 + Recommendation 1 (merge into XI); my Missed Opportunity 8 + Recommendation 4 (add a worked example). The reviews agree the criterion is under-served by current text, though we propose different fixes. If the gate survives skeptic's collapse-into-XI proposal, my "add a worked example" is the minimum viable remedy and both reviews support it.

