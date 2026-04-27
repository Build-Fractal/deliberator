# Cross-Review: skeptic-mathematical's Review

**Cross-reviewer**: skeptic-cross-principle
**Subject**: skeptic-mathematical's review of CONSTITUTION-v2.4.0-blind.md (Constitutional Inclusion Criteria)

## Executive Summary

skeptic-mathematical attacks the gate from a logic/calibration angle: criteria 1 and 2 are non-orthogonal (criterion 1 is a sufficient consequence of criterion 2), the "one-paragraph sketch" is a writing-skill filter, and grandfathering provides no calibration set. My review attacked from a cross-principle/corpus angle: the gate's third criterion is a redundant double-anchor with Principle XI, and at least four grandfathered principles (VI, X, XVI, XX, XXI) would be rejected if proposed today. The two reviews are largely complementary and converge on three core diagnoses: (a) the gate has redundancy somewhere — I locate it at criterion 3 vs XI, the mathematical reviewer locates it at criterion 1 vs criterion 2; (b) the "one-paragraph sketch" bar is unsound; (c) grandfathering is under-specified. But the reviews disagree, sometimes sharply, on *which* criterion is redundant and *what* should replace it.

## Dangerous Contradictions

### 1. We disagree on which criterion is redundant — and our remedies are mutually exclusive

The mathematical review (Recommendation 2, P1) calls to **collapse criteria 1 and 2** into a single "Mechanical Falsifiability" gate, on the logical claim that criterion 1 entails criterion 2's necessary condition. My review (Recommendation 1) calls to **delete or merge criterion 3 into Principle XI**, on the cross-principle claim that criterion 3 restates XI. If both recommendations are accepted, only criterion 1's content survives — which is also my Recommendation 10 (fold the gate into Principle XII). If only one is accepted, the gate looks structurally different depending on whose redundancy diagnosis wins. This is a dangerous contradiction because *both diagnoses are plausibly correct*: criterion 1 may be a logical subset of criterion 2 *and* criterion 3 may be a corpus-level subset of XI. Constitution authors will have to pick. If they pick the mathematical reviewer's collapse (1+2 → falsifiability) without my fix to criterion 3, they end up with a two-criterion gate that still double-anchors XI. If they pick mine without the mathematical reviewer's fix, they end up with a three-criterion gate where 1 and 2 still double-count.

### 2. The mathematical reviewer's "vocabulary novelty" test (Rec 7) directly contradicts grandfathered Principle XI's recursive application

Recommendation 7 proposes "the amendment MUST identify at least one noun phrase or domain term in its body that does not appear in the body of any existing principle." This is mechanical and tractable. But applied retroactively to the existing corpus (which Principle XI requires per my reading), it would flag legitimate principles that legitimately share vocabulary with parents — e.g., XII (Dead Infrastructure) and XI (Single Source of Truth) both use "schema," "variable," "template." A vocabulary-novelty test would either reject genuinely distinct principles whose distinctness lies in the *predicate*, not the *vocabulary*, or it would force authors to coin neologisms — converting the gate into a thesaurus puzzle. The mathematical review treats this as a P2; I would call it a P1 hazard if adopted.

### 3. Conflicting positions on whether to require check artifacts at amendment time

The mathematical review (Rec 1, P1) requires "the amendment PR MUST include either (a) a failing test or lint rule demonstrating the check, or (b) a named CI job, file path, or grep pattern." My review (Rec 2) accepts that "the check need not be implemented at amendment time" and instead requires a structured `Verification:` block naming the check type and artifact. The mathematical review's bar is *substantially higher* — it converts the gate from "concrete description" to "working artifact." If adopted, several existing principles' grandfathered status would be unstable: XII says "the linter SHOULD eventually check for dead variables" — explicitly deferring the artifact. XIII similarly defers ("test suite SHOULD verify"). Adopting the mathematical reviewer's standard for amendments creates an even sharper two-tier system than I flagged: future amendments need shipping artifacts; grandfathered principles got away with "SHOULD eventually." This is a contradiction the constitution cannot ignore — pick the bar, apply it consistently.

## Tensions

### 1. "Worked rejection example" vs cross-principle interaction concern

The mathematical reviewer's Recommendation 3 (P1) proposes a worked rejection example: "code should be readable" fails criterion 2. This is a sound calibration device. But my Missed Opportunity §6 worries about *interaction drift* between principles — the case where a new principle passes all criteria yet contradicts an existing one (e.g., a runtime-tool-generation principle vs VIII Templating Engines Over Inference). The mathematical reviewer's rejection example does not exercise this failure mode. A constitution that has a worked rejection but no worked interaction-conflict example will catch low-quality amendments and miss medium-quality-but-incompatible amendments. The two reviews complement here, but the mathematical reviewer's framing privileges intra-principle quality over inter-principle compatibility.

### 2. "Tolerated" vs "exemplar" tier (Math Rec 4) vs "audit by v3.0.0" (my Rec 4)

The mathematical reviewer proposes a static binary classification of grandfathered principles. My review proposes a time-boxed audit forcing each pre-gate principle to gain verification, migrate, or earn a documented permanent exception. These are not contradictory but they push different incentives. The static tier ossifies the inconsistency permanently (every author can see "X and XVI are tolerated, don't model new amendments on them") whereas the audit creates a deadline forcing resolution. If both are adopted, the audit subsumes the tier (post-audit, every principle is exemplar-grade or out of the constitution). If only the tier is adopted, the inconsistency is permanent. If only the audit is adopted, authors lack interim guidance on which principles to model amendments on. The reviews are stronger combined than separately.

### 3. Severity asymmetry framing (Math Rec 8) vs my migration-versioning framing (my Rec 7)

The mathematical reviewer's Recommendation 8 (P3) states the false-admit / false-reject asymmetry: false-rejection is recoverable (operational guidance is discoverable), false-admission is sticky (prospective-only migration). This framing is sound *as long as* migration of admitted-but-bad principles is feasible. My Recommendation 7 specifies the versioning rule for migrations (MAJOR for removal). If migration is MAJOR, false-admission is even more sticky than the mathematical reviewer assumes — MAJOR bumps are rare, so a falsely-admitted principle effectively persists across a major release cycle. The mathematical reviewer's "err toward strictness" guidance is therefore *more* important than the review states, given the real cost of correction.

### 4. "One paragraph" critique convergence with implementation concern

Both reviews independently identify the "one paragraph" bar as broken. The mathematical reviewer's diagnosis (Off-Base Assumption §1, Rec 1) is that fluent prose can game the bar. My diagnosis (Missed Opportunity §5) is that the bar is itself unverifiable — who decides what's "concrete enough"? These are the same conclusion via different paths. The tension is in the remedy: the mathematical reviewer wants either a working artifact or a 5-10 line pseudo-code outline; I want a structural `Verification:` block with named check type and artifact. The artifact-based remedy is stricter; the structural remedy is more author-friendly. The constitution should not adopt both — they would compose into "structural block AND working artifact," which over-burdens amendment authors and may discourage legitimate principles. Pick one.

### 5. Periodic re-evaluation (Math Rec 9) vs my Extension-block treatment (my Rec 8)

The mathematical reviewer proposes MAJOR-bump audits to re-evaluate all principles. My Rec 8 says Extension blocks within existing principles are themselves amendments and must satisfy the gate. These mechanisms overlap but are not redundant: the audit catches *latent* drift (principle was admitted under v2.4 criteria, v3.0 criteria are tighter), while Extension-block gating catches *active* expansion (someone bolts a new requirement onto a grandfathered principle). The tension is that Extension-block gating *retroactively pulls grandfathered principles into the gate*, which the mathematical reviewer's "prospective-only" reading would oppose. Both reviews are correct that the prospective-only design is unstable (Math Off-Base Assumption §2; my Off-Base Assumption §2), but we differ on the fix.

## Safe Agreements

### 1. The gate's "concrete enough that an engineer can sketch the check in one paragraph" sub-clause is broken

Both reviews independently flag this exact phrase as the weakest single point in the gate. The mathematical reviewer calls it author-capability rather than content-property; I call it a recursive judgment-gate that cannot pass its own falsifiable-scope test. Different framings, identical conclusion: this clause should not survive in its current form. Whatever the rewrite is — artifact-based, structural-block-based, or pseudo-code-based — *something* concrete should replace prose word-counting. This is the strongest convergence point and should be treated as P1 by any synthesizer.

### 2. Grandfathering is under-specified and creates a two-tier constitution

The mathematical reviewer's Missed Opportunity §3 ("grandfathering boundary is binary when it should be graded") and my Missed Opportunity §3 ("VI and X are the most flagrant grandfather beneficiaries") converge on the same diagnosis: blanket grandfathering of I-XXVII without quality discrimination is unstable. Whether the fix is the mathematical reviewer's tier classification, my time-boxed audit, or both, *some* mechanism must address the calibration-set problem. Future amendment authors will model on whatever is in the constitution; if the constitution contains both X (irreducibly subjective) and XXII (mechanically verifiable) as equal-status principles, the gate cannot be calibrated.

### 3. The gate lacks an enforcement path

The mathematical reviewer's Recommendation 10 (template-based gate) and my Recommendation 6 (specify the gate's enforcement path) converge: prose criteria embedded in Governance with no explicit enforcement mechanism are rhetorical, not operational. Both reviews diagnose this as a P2/P3 issue but the agreement is unconditional. The constitution must specify *who runs the gate, when, and what artifact records the result* — whether that is a `/speckit.constitution` checklist, a CI lint on `CONSTITUTION.md` diffs, or a structured PR template. No matter the mechanism, "the gate runs by reviewer goodwill" is not adequate.

### 4. The amendment-process needs an explicit interaction/compatibility check

The mathematical reviewer's Recommendation 5 (P2, fourth gate for interaction) and my Missed Opportunity related observations (cross-principle drift, e.g., XV-XXVII coordination, XVII content-classification overlap with operational guidance) both surface the same gap: passing all the gate criteria does not guarantee compatibility with the existing corpus. The constitution already demonstrates this concern in practice — Principle XXVII explicitly coordinates with XV ("Coordination with Principle XV"), Principle XXV explicitly coordinates with XXII ("Interaction with Principle XXII"). These coordinations were authored ad-hoc; the gate should make them required.
