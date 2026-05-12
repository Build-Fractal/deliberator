# Skeptic-Mathematical Review: Constitutional Inclusion Criteria

## Executive Summary (2-3 paragraphs)

The Governance section's Constitutional Inclusion Criteria attempts to convert a fundamentally aesthetic question ("does this belong in the constitution?") into a mechanical three-gate test. The intent is admirable: keep the constitution from sliding into a wiki of opinions. But the test as written is logically incoherent in two specific ways. First, the three gates are not orthogonal. Mechanical verification capability (criterion 1) is, on a careful reading, a *subset* of falsifiable scope (criterion 2): if you cannot sketch a check, the wording is by definition not falsifiable. The AND structure therefore double-counts the same property and offers no incremental discrimination. Second, the "concrete enough that an engineer can sketch the check in one paragraph" sub-clause is defined by author capability rather than by content properties; a sufficiently fluent author can write a vacuous one-paragraph sketch for *any* principle, including ones that should fail. This converts the gate into a writing-skill filter rather than a content filter.

The grandfathering provision compounds the calibration problem. Principles I-XXVII are exempt from the gate, but several of them — most clearly Principle XVI (Mathematical Transparency) and Principle X (Zen of Python Output) — would arguably fail criterion 1 (no obvious mechanical check for "the user understands what is being optimized" or "if the implementation is hard to explain, it's a bad idea") and criterion 2 ("readability counts" requires interpretation). The constitution implicitly admits this by carving I-XXVII out, but does not state the principle that decides which pre-gate principles *should have been* admitted. Without that, the gate cannot be calibrated against ground truth: we know the gate is intended to admit principles like III, XII, XXII; we do not know if it is intended to admit principles like X or XVI.

The strongest argument for restructuring is that the gate, as written, is more rhetorical than operational. It will not stop a determined amendment author who can write a one-paragraph check sketch and assert "this is distinct from existing principles." It will, however, give reviewers a procedural cudgel to reject amendments they dislike on aesthetic grounds while accepting ones they prefer. That is worse than having no gate at all, because it launders judgment as mechanism. Recommend either tightening the gate substantially (replace "can sketch a check in one paragraph" with "must include the check in the amendment PR, even if not yet wired into CI") or dropping it and trusting the existing amendment process plus principle XI/XII to police duplication and dead infrastructure.

## Alignment (4-6 bullets where the criteria are well-formed)

- **Three-gate structure is conceptually sound.** Verifiability, falsifiability, and distinctness are genuinely the three properties an invariant needs. The categories themselves are well-chosen even if the operationalizations are weak.
- **Operational-guidance escape hatch is correctly placed.** Naming `CONTRIBUTING.md`, the relevant spec, `SKILL.md` instructions, and domain-specific reference documents as the explicit home for "judgment calls" prevents the gate from creating orphaned content. The gate has somewhere to send what it rejects.
- **Prospective-application clause prevents retroactive purges.** Stating that the gate applies only to amendments landing once the gate is in force — and that migrating grandfathered principles is a separate intentional act — avoids destabilizing the existing constitution on the day the gate is adopted. This is the right transition rule.
- **Distinct-from-existing criterion correctly identifies refinement vs. addition.** The instruction "Refining or extending an existing principle goes in that principle's body, not as a new principle" is well-formed and observable: it can be checked by counting whether the proposed amendment cites/overlaps an existing principle.
- **Versioning ladder maps cleanly onto inclusion outcomes.** MAJOR for removals/redefinitions, MINOR for new principles, PATCH for clarifications gives the gate a versioning vocabulary: a passed gate produces a MINOR; a body-of-existing-principle revision produces a PATCH; a rejected amendment produces nothing. The taxonomy is internally consistent.
- **Migration-spec requirement keeps grandfathered cleanup honest.** Forcing the receiving document to be identified explicitly in any future migration spec prevents principles from being silently demoted into ambiguity. This is a real safeguard.

## Missed Opportunities (6-9 bullets where wording/structure could be tightened)

- **Criterion 1 collapses into criterion 2 under standard logic.** "Mechanical verification capability" requires that a future PR violating the principle would fail a check; "falsifiable scope" requires that the wording flags hypothetical violating PRs without interpretation. If the wording cannot flag violations without interpretation, no check is constructible. Therefore criterion 2 entails criterion 1's necessary condition. Treating them as independent gates double-counts. Restructure so criterion 2 is the falsifiability requirement and criterion 1 becomes a *concreteness* requirement (the amendment must produce a check artifact, not merely a sketch).
- **"One paragraph" is an author-capability metric, not a content metric.** A skilled writer can produce a one-paragraph sketch that name-drops "grep" or "linter rule" without any actual verifiable content. The sketch test should require either (a) a *named* CI job, lint rule, or test pattern that already exists in the repo, or (b) a 5-10 line pseudo-code outline. Word count is a poor proxy for verifiability.
- **No counter-example test.** The gate gives criteria for admission but no test for *rejection*. A robust gate needs a reject case: "Principle Z would have been rejected because it fails criterion N, demonstrated by …" Without at least one worked rejection, the gate is unfalsifiable on its own terms — there's no way to know whether it discriminates.
- **Grandfathering boundary is binary when it should be graded.** Principles I-XXVII are blanket-grandfathered, but they vary widely in how well they would pass the gate. Principle XII (Dead Infrastructure) has a clear linter sketch. Principle X (Zen of Python Output) does not. Future arbiters reading the gate will be unable to decide whether to model new principles on XII or on X — both are pre-gate, both are equally-ratified. The grandfathering clause should classify pre-gate principles into "would-pass" and "tolerated" buckets so the gate has a calibration set.
- **No tie-breaker for "addressable by composing existing principles."** Criterion 3 demands distinctness from "composing existing principles," but composition is unbounded — almost any new concern can be argued to be a composition of XI (Single Source of Truth) + XII (Dead Infrastructure) + something. The gate needs a positive test for what counts as a non-compositional concern (e.g., "the principle introduces a vocabulary term not present in any existing principle's body").
- **The gate does not address principle *interaction* drift.** New principles can pass all three gates yet contradict an existing principle (e.g., a new principle requiring runtime tool generation would conflict with VIII Templating Engines Over Inference). Add a fourth implicit gate: "compatibility with existing principles, with conflicts resolved explicitly in the amendment."
- **Severity asymmetry between false-admit and false-reject is not stated.** If the gate is too strict (false-rejects good principles), they go to operational guidance and are still findable. If the gate is too loose (false-admits weak principles), the constitution accumulates noise that becomes hard to remove because of the prospective-only migration rule. The gate should be tuned to err toward strictness, but the criteria as written do not encode that asymmetry.
- **No expiry / re-evaluation cadence.** Principles passed under the gate at time T may, at time T+N, be subsumable by later principles. The gate is one-shot at amendment time but the constitution is long-lived. Add a clause: "Existing principles SHOULD be re-evaluated against the current criteria when a structurally-related principle is added or modified." This connects to grandfathering: pre-gate principles also benefit from periodic re-evaluation, even if migration requires a separate spec.
- **"At amendment time" exception in criterion 1 weakens the gate.** Allowing the check to not exist at amendment time is pragmatic but creates a debt: principle X is admitted, the sketched check is never built, no enforcement materializes. Either require the check to be built within N versions (e.g., "the check MUST exist by the second MINOR after introduction"), or require the amendment PR to include at least a failing test stub.

## Off-Base Assumptions (2-4 points; if none, state explicitly)

- **Assumption: a one-paragraph sketch can be written iff the principle is verifiable.** The gate treats "engineer can sketch the check in one paragraph" as a proxy for the existence of a real check. This is an empirical claim about engineer capability, not a logical guarantee. A sufficiently abstract principle (e.g., "every principle should have a falsifiability story") admits a glib one-paragraph sketch ("CI lint that scans principle bodies for the word 'falsifiable'") that is technically a paragraph and technically a check, but enforces nothing useful. The proxy is not tight.
- **Assumption: the three criteria are independent.** As argued above, criterion 1 is essentially a sufficient-condition consequence of criterion 2, so the AND is a 2-of-3 in disguise. The constitution treats them as if they cut across orthogonal axes; they do not.
- **Assumption: grandfathered principles need no calibration story.** The text reads as if the existing 27 principles are an unproblematic baseline. They are not — they vary in verifiability — and that variation matters because future authors will model amendments on them.

## Actionable Recommendations (7-10 numbered with Priority P1/P2/P3, Current state, Proposed change, Rationale, Risk if ignored)

1. **[P1] Replace "sketch in one paragraph" with "include a concrete check artifact."**
   - *Current state*: criterion 1 says the check path "MUST be concrete enough that an engineer reading the principle can sketch the check in one paragraph."
   - *Proposed change*: "the amendment PR MUST include either (a) a failing test or lint rule demonstrating the check, or (b) a named CI job, file path, or grep pattern that would mechanically detect a violation, with at most a 5-10 line implementation sketch."
   - *Rationale*: replaces an author-capability proxy with a content artifact, reducing gameability.
   - *Risk if ignored*: future amendments pass the gate on the strength of fluent prose rather than verifiable mechanism.

2. **[P1] Collapse criteria 1 and 2 into a single "Mechanical falsifiability" gate.**
   - *Current state*: criteria 1 and 2 are stated as independent, joined by AND.
   - *Proposed change*: merge into "Mechanical Falsifiability: the principle's wording is specific enough that a violating PR can be detected by an automated check, AND the amendment PR includes a concrete description of that check."
   - *Rationale*: criterion 1's "feasibility of a mechanical check" is logically dependent on criterion 2's "falsifiable scope" — if the principle isn't falsifiable, no check exists. Two gates create false confidence; one gate is honest.
   - *Risk if ignored*: future amendment debates will perform-pass criterion 2 but stall on a redundant criterion 1, or vice versa, wasting reviewer cycles.

3. **[P1] Add a worked rejection example to the gate text.**
   - *Current state*: gate provides admission criteria but no rejection demonstration.
   - *Proposed change*: append "Example rejection: a principle stating 'code should be readable' would fail criterion [Mechanical Falsifiability] because no automated check can distinguish readable from unreadable code without subjective interpretation."
   - *Rationale*: a gate without a rejection case is unfalsifiable. The example calibrates reviewers and amendment authors against a shared baseline.
   - *Risk if ignored*: every gate application becomes a fresh interpretive negotiation.

4. **[P2] Classify grandfathered principles into "exemplar" and "tolerated" tiers.**
   - *Current state*: principles I-XXVII are blanket-grandfathered with no quality signal.
   - *Proposed change*: add a footnote or appendix marking each pre-gate principle as either "exemplar" (would pass the gate cleanly; model new amendments on these) or "tolerated" (grandfathered but would not pass the gate today; do not model new amendments on these). Candidates for tolerated: X, XVI, XXI's subjective steps.
   - *Rationale*: future authors need a calibration set. Without one, they will look at the most verbally sophisticated existing principle (likely X or XVI) and conclude that level of abstraction is permissible.
   - *Risk if ignored*: gate drift in the upward direction — each new amendment is just slightly more abstract than the last.

5. **[P2] Add a fourth gate for principle interaction.**
   - *Current state*: criterion 3 covers compositional redundancy but not contradictory interaction.
   - *Proposed change*: add criterion 4: "Compatibility with existing principles. The amendment MUST identify any existing principle whose contract changes as a result of the new principle, and either (a) demonstrate compatibility, or (b) propose explicit edits to the affected principle(s) in the same PR."
   - *Rationale*: composition redundancy and contradiction are different failure modes; only the first is currently caught.
   - *Risk if ignored*: silent drift between e.g., a new optimization principle and VIII (Templating Engines Over Inference).

6. **[P2] Set a deadline for the "check does not have to exist at amendment time" debt.**
   - *Current state*: "The check does NOT have to exist at amendment time."
   - *Proposed change*: "...but it MUST exist by the second MINOR version after introduction, or the principle is automatically reclassified as operational guidance."
   - *Rationale*: prevents accumulation of unverified promissory notes. Connects gate decisions to enforced reality.
   - *Risk if ignored*: principles that promise mechanical verification but never deliver it accumulate, hollowing out the gate's purpose.

7. **[P2] Tighten "distinct from existing principles" with a vocabulary test.**
   - *Current state*: "the principle MUST cover concerns not already addressable by composing existing principles."
   - *Proposed change*: add an operational test: "The amendment MUST identify at least one noun phrase or domain term in its body that does not appear in the body of any existing principle. If no such term exists, the proposed content belongs as an extension to the existing principle whose vocabulary it shares."
   - *Rationale*: composition is too elastic to be a useful test on its own. Vocabulary novelty is a tractable proxy.
   - *Risk if ignored*: criterion 3 becomes a rhetorical exercise where any new principle can be argued to be either a composition or not, depending on framing.

8. **[P3] State the false-admit / false-reject asymmetry explicitly.**
   - *Current state*: gate is silent on which error mode is worse.
   - *Proposed change*: add "When in doubt, the gate errs toward operational guidance. False-rejection is recoverable — operational content remains discoverable and can be re-promoted with a fresh amendment. False-admission is harder to reverse because of the prospective-only migration rule."
   - *Rationale*: makes the calibration philosophy legible to reviewers, reducing inconsistent application.
   - *Risk if ignored*: gate is applied loosely or strictly depending on reviewer mood.

9. **[P3] Add a periodic re-evaluation clause for both pre- and post-gate principles.**
   - *Current state*: gate is one-shot at amendment time; no periodic review.
   - *Proposed change*: "Every MAJOR version bump SHOULD include a constitution audit: each principle is re-evaluated against the current gate criteria, and recommendations for migration to operational guidance are surfaced (though migration itself remains a separate amendment)."
   - *Rationale*: long-lived constitutions accumulate principles whose context has shifted; without periodic audit, the gate ossifies.
   - *Risk if ignored*: constitution becomes append-only, and the operational-guidance escape hatch is one-way in practice.

10. **[P3] Consider replacing the gate with a structured amendment template instead.**
    - *Current state*: the gate is criteria-based prose embedded in Governance.
    - *Proposed change*: convert the gate into an amendment-PR template with required sections: "Mechanical check (artifact or named pattern)", "Falsifying example", "Distinctness statement (vocabulary term, principle interactions)", "Operational-guidance alternative considered". The template *is* the gate.
    - *Rationale*: a template is harder to game than prose criteria because every section produces an artifact. It also makes the gate self-documenting in PR history.
    - *Risk if ignored*: the gate stays rhetorical and review-dependent; structured templates would make it operational.

## Referenced Documentation

- `<HOME>/code/payer-index-mono/conversus-oss/deliberations/069-blind-2026-04-26/CONSTITUTION-v2.4.0-blind.md` — entire document audited; specific focus on Governance section, "Constitutional Inclusion Criteria" subsection (lines 811-844), and grandfathering clause (lines 840-844). Cross-referenced against Principles X, XII, XVI, and XXII as calibration cases.
