# Practitioner Cross-Review of Skeptic-Mathematical

Reviewing skeptic-mathematical's audit of the Constitutional Inclusion Criteria gate, from the lens of an amendment author who must apply the gate operationally.

---

### Dangerous Contradictions

1. **Collapsing Criterion 1 into Criterion 2 removes the only artifact-producing requirement and makes the gate harder to enforce, not easier.**
   Skeptic-mathematical's P1 recommendation #2 ("Collapse criteria 1 and 2 into a single 'Mechanical falsifiability' gate") is logically clean — they are correct that falsifiability entails check-feasibility — but it is operationally backwards. My review identifies the gate's largest gap as the absence of an artifact: there is no PR template field, no required check-pointer, no enforcer. Criterion 1, even in its weak "sketch in one paragraph" form, is the only criterion that asks for something *concrete* (a check sketch). Criterion 2 is a property of *wording*, which any author can self-certify. Collapsing them yields one criterion that is satisfied by prose alone. The right move is the opposite: keep Criterion 1, *strengthen* it by demanding a named artifact (file path, lint name, test pattern) — which is skeptic-mathematical's own P1 recommendation #1, in tension with their #2. They cannot have both. I would keep #1 and reject the collapse.

2. **The "tolerated vs. exemplar" tiering of grandfathered principles is a process bomb.**
   Skeptic-mathematical's P2 recommendation #4 proposes annotating each pre-gate principle as "exemplar" or "tolerated." This sounds calibrating but is dangerous: it unilaterally declares Principles X, XVI, and parts of IX to be second-class on the day the gate ships, without the migration spec the gate's prospective-only clause requires. That conflicts directly with the carve-out's purpose ("migration is a separate, intentional act"). Future amendment authors looking at a "tolerated" annotation on Principle X have been handed a procedural cudgel to argue X is invalid as precedent — exactly the bad-faith reading the carve-out forecloses. My review surfaced the same precedent problem and recommended a softer footnote ("X, XVI, prose subsections of IX should not be cited as precedent for new prose-principles"), which preserves the grandfathering while warning future authors. Skeptic-mathematical's tiering goes too far and effectively pre-litigates migration without the spec.

3. **The "automatic reclassification" deadline (P2 #6) creates a worse outcome than the debt it tries to eliminate.**
   Skeptic-mathematical proposes that if a sketched check does not exist by the second MINOR after introduction, the principle is "automatically reclassified as operational guidance." This automation is incompatible with the constitution's own amendment process: migration to operational guidance requires a migration spec naming the receiving document, per the existing prospective-only clause. Auto-reclassification bypasses that. Worse, it punishes principles whose checks are genuinely hard to build (e.g., XII's dead-infrastructure linter — non-trivial to implement well) by demoting them rather than escalating them as tracked debt. My P3 recommendation #8 (sunset for "linter SHOULD eventually" hedges via tracking spec citation) addresses the same debt without inventing an auto-demotion mechanism that no human has reviewed. Auto-anything in governance is a contradiction with the rest of the amendment process.

---

### Tensions

1. **Vocabulary-novelty test (P2 #7) vs. operational simplicity.**
   Skeptic-mathematical proposes that Criterion 3 require "at least one noun phrase or domain term in [the principle's] body that does not appear in the body of any existing principle." Mathematically tidy, but operationally hostile: amendment authors must now grep all 27 existing principle bodies for vocabulary collisions. My review flagged that Criterion 3 needs a worked example, not a new mechanical sub-test. A worked example ("Principle XXVIII proposing lowercase template variables is rejected because it composes IX + XI") is far cheaper to apply and gives reviewers a calibration anchor. Vocabulary-novelty is a clever heuristic that will be wrong often (synonyms, paraphrase, legitimate vocabulary reuse) and will mostly serve as a rejection lever, not an admission test. I prefer the example-based approach.

2. **Counter-example test (P1 #3) is correct in principle, narrower in execution.**
   Skeptic-mathematical's recommendation that the gate include a worked rejection ("'code should be readable' fails because no automated check…") is sound — and aligns with my recommendation #4 (worked example for Criterion 3). The tension is in scope: skeptic-mathematical wants a rejection example for the merged falsifiability criterion. I want an example for distinctness (Criterion 3). Both are needed, and they are independent. The constitution should carry two worked examples — one rejection per criterion that benefits from it (Criteria 2 and 3). Skeptic-mathematical's framing under-counts the worked-example need.

3. **Periodic re-evaluation (P3 #9) vs. constitutional stability.**
   The proposal that "every MAJOR version bump SHOULD include a constitution audit" is well-intentioned but in practical tension with how constitutional documents earn their authority. Constitutions are valuable precisely because they are *not* re-litigated every cycle. Adding a triennial-style audit invites continual debate over which principles "still pass the gate," which is destabilizing. My review lands closer to "the gate is one-shot at amendment time, and migration is its own intentional act" — which is what the existing carve-out already says. The audit cadence is a soft-sounding addition that hardens into a process drag. I'd narrow it: re-evaluation triggers only when a structurally-related principle is added, not on every MAJOR.

4. **Severity asymmetry (P3 #8) is the right idea, but stated as a tie-breaker rather than a calibration philosophy.**
   Skeptic-mathematical correctly identifies that false-admit and false-reject have different costs and recommends explicit asymmetry language. My review did not state this directly but my recommendation set leans the same way (procedural enforcement, named-artifact requirement) — both biases push toward strictness. The tension is rhetorical: skeptic-mathematical adds a clause; I add machinery. Machinery is more durable than a stated bias because reviewers ignore stated biases under pressure. Both should ship; the machinery does the work.

5. **Compatibility-with-existing-principles fourth gate (P2 #5) vs. risk of gate proliferation.**
   The proposal for a fourth criterion (compatibility with existing principles, with conflicts addressed in-PR) catches a real failure mode I did not surface: silent contradiction. The tension is that adding a fourth criterion compounds the friction problem I flagged in my Missed Opportunities #6 (asymmetric slowdown of legitimate amendments). A four-criterion gate with self-assessment and no enforcer is worse than a three-criterion gate with the same flaws. Skeptic-mathematical's fourth gate is content-correct but should land *only* once enforcement (PR template, maintainer review) is in place. Sequence matters.

---

### Safe Agreements

1. **The "sketch in one paragraph" subclause is broken and must be replaced with a named-artifact requirement.**
   Both reviews independently identify this as the gate's weakest single sentence. Skeptic-mathematical's P1 #1 (named CI job, file path, or grep pattern, plus 5-10 line sketch) and my recommendation #2 (named artifact location) converge on the same fix. Strong agreement.

2. **The gate has no specified enforcer and this is the largest single defect.**
   Both reviews surface this — skeptic-mathematical implicitly via the rubber-stamp critique and recommendations 1 and 10 (PR template), I directly in my Missed Opportunities #2 and #5 and recommendations #1 and #5. Mechanizing enforcement via PR template plus required maintainer review is the highest-leverage change and both reviews back it.

3. **Grandfathered principles create a precedent problem distinct from the legal carve-out problem.**
   Both reviews note that the prospective-only clause solves the validity question but does not solve the "future authors will model new amendments on Principle X" problem. We disagree on the remedy (skeptic-mathematical's tiering is too aggressive; my footnote is softer), but the problem statement is shared.

4. **Worked examples in the gate text are non-optional.**
   Skeptic-mathematical's P1 #3 (rejection example) and my recommendation #4 (Criterion 3 worked example) agree the gate as written is interpretively underspecified. A gate without worked examples becomes a fresh negotiation every time.
