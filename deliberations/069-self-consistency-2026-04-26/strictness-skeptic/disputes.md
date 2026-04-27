# Strictness-Skeptic Disputes (Phase 4)

**Role**: strictness-skeptic
**Position**: the v2.4.0 gate as drafted is too strict and structurally mis-calibrated. Phase 3 cross-revisions narrowed the disagreement surface but did not eliminate it. Three load-bearing disputes remain after governance-skeptic and practitioner each amended their proposals; resolving them in my favor is necessary before merge.

---

### Remaining Disputes

#### Dispute 1: AND-coupling on criterion 1 vs. partial-OR substitution (R-1 stands; practitioner's NR-1 deferral is insufficient)

**The disagreement.** I argued in Phase 2 (R-1) and reaffirmed in Phase 3 that the gate's three-criterion AND structure systematically rejects form constraints, taste-level invariants, and meta-principles. The candidate text in §Governance lines 872-905 requires a one-paragraph mechanical-check sketch (criterion 1) AND falsifiable scope (criterion 2) AND distinctness (criterion 3) — all conjunctively. By spec 069 §5's own enumeration, this gate would have rejected Principles VI (Scripts Over Markdown), X (Zen of Python Output), and XVI (Mathematical Transparency). All three are load-bearing in the current corpus, all three were ratified through a converged deliberation, and all three would fail criterion 1 because their normative content is taste/form-shaped rather than lint-shaped. A gate that rejects 3 of 27 grandfathered principles is not a marginal calibration error — it is a category exclusion.

Practitioner's New Recommendation #1 proposes evidence-first deferral: ship the gate as drafted, log criterion-1-only rejections to a derived precedent log, and trigger a calibration review after ≥3 such rejections accumulate. This is an attractive sequencing argument and I have engaged with it directly. It is wrong on two counts.

First, the trigger threshold (≥3 rejections) is set above the historical reject-on-this-criterion rate the corpus itself produces. If the gate had been in force during the v2.3.0 deliberation, the three rejections would have been simultaneous (VI, X, XVI all proposed at once) and the calibration review would not have fired in time to admit them — they would simply have been routed to operational guidance. The threshold mechanism only protects against future rejections, not against the rejections the gate is *currently* committing to. Practitioner's mechanism solves a problem that does not exist (drift) while leaving the actual problem (calibration error at the gate's effective date) untouched.

Second, the deferral framing assumes the precedent log accumulates evidence cheaply. It does not. Each rejection imposes real cost on the rejected amendment author — drafting a principle, running it through the verification deliberation, watching it fail criterion 1, then re-routing the content to operational guidance is a multi-week loop. Three such loops before the calibration trigger fires is a 3-6 month window during which the gate exhibits its mis-calibration on real authors. "Defer until evidence" is acceptable when evidence-gathering is cheap; it is not acceptable here.

Governance-skeptic's modified Recommendation 4 (withdrawn taxonomy, retained substantive self-assessment) partially addresses the category-exclusion concern by removing the fixed check-type list, but does not address the AND-coupling itself. A free-form criterion 1 self-assessment still requires the author to demonstrate mechanical verification capability for principles whose normative content is not mechanical. Removing the taxonomy is necessary but not sufficient.

**My position**: R-1 stands as revised in Phase 3. The gate must require criterion 2 (falsifiable scope) AND criterion 3 (distinctness) AND at least one of criterion 1 (mechanical sketch) OR a peer-review-rubric operationalization with a cited precedent. The closed-list enumeration in revised R-3/R-7 (Principles VI, X, XVI, XVII, XVIII as the relaxed-criterion-1 set) supplies the anti-laundering protection practitioner's DC-2 correctly demanded. I am not asking for theory-first loosening; I am asking for evidence-grounded loosening where the evidence is the existing corpus, which contains three principles the gate would reject.

#### Dispute 2: The candidate's missing v2.4.0 Sync Impact Report and grandfathering disclosure (R-11)

**The disagreement.** This is a narrower, mechanically-resolvable dispute on which all three Phase 3 revisions converged in *spirit* but diverged in *substance*. Governance-skeptic's NR-2 and practitioner's strengthened Recommendation #6 both endorse adding a v2.4.0 Sync Impact Report to the candidate file. My R-11 endorses the same plus an additional requirement: the Sync Impact Report MUST explicitly enumerate the failed-grandfathered-principles list (VI, X, XVI per spec 069 §5).

Governance-skeptic's NR-2 proposes including "the first Inclusion Criteria Self-Assessment as a reflexive demonstration." Practitioner's strengthened #6 accepted my T-3 escalation in cross-review but the revision text frames it as documentation hygiene rather than a calibration anchor. Neither version makes the grandfathering disclosure load-bearing in the way it needs to be.

The disclosure matters because it is the only mechanism by which future amendment authors confront the calibration evidence directly. Burying the v2.3.0 → v2.4.0 transition in deliberation 069's spec text means future authors read the constitution, see the gate, and have no in-document signal that the current corpus was authored under a looser bar. They will then propose principles in the spirit of VI, X, or XVI, get rejected, and have no contextual evidence to cite when challenging the rejection. The Sync Impact Report at the top of the constitution is the only place this evidence belongs because it is the only artifact every amendment author is required to consume (per Principle XII / Versioning).

A self-assessment that does not enumerate the grandfathering set is not a calibration anchor — it is a fig leaf. The reflexive demonstration governance-skeptic proposes is good but insufficient: demonstrating the gate's application to itself does not demonstrate its application to the corpus it is grandfathering.

**My position**: R-11 stands. The v2.4.0 Sync Impact Report MUST contain three components: (a) the version-bump rationale (the new gate), (b) a reflexive self-assessment of the gate against its own criteria (per governance-skeptic's NR-2), AND (c) an explicit enumeration of the grandfathered principles that fail each criterion, with one-sentence justification per principle. Without (c), the Sync Impact Report fails its calibration-anchoring function and the gate ships without the empirical evidence that justifies its scope.

#### Dispute 3: `CONTRIBUTING.md` vs. `AGENTS.md` as operational-guidance destination (R-13)

**The disagreement.** The candidate text at line 896 routes failed principles to "`CONTRIBUTING.md`, the relevant spec, `SKILL.md` instructions, or domain-specific reference documents." `CONTRIBUTING.md` does not exist in this repository. Principle XVII (Content Classification) explicitly routes contribution rules to `AGENTS.md`. The destination is wrong.

Governance-skeptic's surviving Recommendation 9 disambiguates `SKILL.md` as runtime-enforced but does not touch the `CONTRIBUTING.md` reference. Governance-skeptic's surviving Recommendation 10 adds a cross-reference to Principle XVII but again does not fix the destination. Practitioner's amended Recommendation #3 builds a routing table with a constitutional-remand branch but, in the revision, does not call out that the table's first entry must replace `CONTRIBUTING.md` with `AGENTS.md`. All three Phase 3 revisions skirt this fix.

This is the lowest-stakes dispute on the list and the easiest to resolve. The fix is a one-token edit: replace `CONTRIBUTING.md` with `AGENTS.md` in the operational-guidance routing block. It is independent of every other disputed element. Failing to make it ships an internal inconsistency: the constitution that defines content classification (Principle XVII) directs contribution rules to `AGENTS.md`, while §Governance directs failed principles to a file that does not exist and that, if created, would conflict with XVII's classification.

**My position**: R-13 stands. The candidate text MUST replace `CONTRIBUTING.md` with `AGENTS.md` in line 896 before merge. This is a non-negotiable internal-consistency fix that requires no calibration debate.

---

### Convergence

The Phase 3 revisions produced more agreement than the disagreement surface suggests. Five recommendations have effectively converged across all three reviewers and can be adopted without further disputation:

#### Convergence 1: Lift the gate to a subsection (R-12 / governance-skeptic R-1 / practitioner alignment)

All three reviewers agree the gate belongs in a `### Constitutional Inclusion Criteria` subsection, not buried as a third bullet under §Governance. Governance-skeptic's Recommendation 1 survives intact in their Phase 3 revision. Practitioner's revisions do not contest this. My R-12 endorses it. The structural fix is independent of every contested element and should land first. Adopt as written.

#### Convergence 2: Form-only CI lint with N/A acceptance (R-9 sharpened / practitioner #2 amended)

Practitioner's amended #2 (lint enforces form, accepts "N/A — justified because" as passing) and my sharpened R-9 (rubric must be specifically named, not generic) produce a coherent enforcement surface together. The lint greps for the four required Sync Impact Report sub-headings and accepts either a sketched check, a named rubric, or a justified N/A. Substance remains reviewer work; form is mechanical. Governance-skeptic's modified Recommendation 2 is compatible with this design (their two-surface framing — mechanical lint + substantive review — is exactly what this combination produces). Adopt the union.

#### Convergence 3: Verification deliberation with documented-disputes acceptance bar (practitioner amended #5)

Practitioner's amended #5 replaces "zero disputes blocks merge" with "every dispute documented in the Sync Impact Report with a rationale for non-incorporation." This resolves my DC-2 concern about variance-reducer lock-in and governance-skeptic's DC-2 about engineerable panel composition. The amended bar preserves bug-catching benefit (the v2.3.1 fix the original recommendation cited) without inverting Principle V's "warnings, not blocks" stance. Adopt as practitioner revised.

#### Convergence 4: Expedited path with rollback authority (practitioner amended #9)

Governance-skeptic's DC-3 caught the bypass (open-category author-defined emergency); practitioner's amended #9 closes it with explicit rollback authority on post-hoc verification finding. The 14-day window plus automatic rollback on material findings produces a one-way door in the right direction (failures revert; only re-proposed amendments land). I did not directly contest this in Phase 3; both reviewers' framings are consistent with my SA-3 concern about asymmetric procedural costs. Adopt as practitioner revised.

#### Convergence 5: Cross-link direction reversed (gate → XVII per governance-skeptic Recommendation 10 / practitioner amended #10)

Governance-skeptic's reference-topology argument (newer references older, not the reverse) is correct and practitioner accepted it in their amended #10. The cross-reference flows from the Constitutional Inclusion Criteria subsection to Principle XVII, inheriting XVII's Content Classification vocabulary. My Phase 2 review did not propose a cross-reference at all, so I have no dispute to register here; I adopt the governance-skeptic / practitioner convergence as written.

---

### Final Position Statement

#### Non-Negotiables (must land in v2.4.0)

**Non-Negotiable 1: Partial-OR on criterion 1, with closed-list enumeration.**

The gate MUST require criterion 2 AND criterion 3 AND at least one of (a) criterion 1 mechanical sketch OR (b) peer-review-rubric operationalization with cited precedent. The relaxed-criterion-1 path is bounded by a closed enumeration tied to existing principles VI, X, XVI, XVII, XVIII; expansion of the closed list itself requires its own MINOR amendment with worked-example justification. This addresses the form-constraint and meta-principle category exclusion that my entire review documents. Without this, the gate ships in a state where it would have rejected three of its own grandfathered principles, which is a structural failure visible in the document itself.

**Non-Negotiable 2: v2.4.0 Sync Impact Report with explicit grandfathering disclosure.**

The candidate file MUST publish a Sync Impact Report at the top describing the v2.3.1 → v2.4.0 transition, containing (a) the gate's introduction rationale, (b) a reflexive self-assessment of the gate against its own criteria, and (c) explicit enumeration of grandfathered principles failing each criterion (per spec 069 §5: VI, X, XVI fail criterion 1 absent the Non-Negotiable 1 fix). This is the only artifact future amendment authors are required to consume; calibration evidence belongs there or nowhere.

**Non-Negotiable 3: `AGENTS.md` replaces `CONTRIBUTING.md` in the operational-guidance routing.**

The candidate text at line 896 MUST replace `CONTRIBUTING.md` with `AGENTS.md` to align with Principle XVII's content classification. This is a one-token edit independent of every other disputed element and prevents an internal inconsistency from shipping with v2.4.0.

#### Flexibility (acceptable variations)

**Flexibility 1: Calibration trigger threshold and sunset date.**

R-5's calibration target (originally ≥90% retroactive admission, revised to ≥85% with v3.0.0 sunset) and R-10's loosening trigger (≥3 override invocations on the same criterion across consecutive MINORs) are mechanically tunable. I do not require these specific numbers. I require *some* calibration trigger and *some* sunset; the exact threshold can be set anywhere in the [80%, 90%] band and the sunset can land at any MAJOR transition v3.0.0 or later. Practitioner's NR-1 evidence-first review trigger is also acceptable as the calibration mechanism if it includes a sunset clause and a threshold below the historical reject-on-this-criterion rate.

**Flexibility 2: Routing-table structure and constitutional-remand branch.**

Practitioner's amended Recommendation #3 (five-way decision tree with constitutional-remand safety valve) is one acceptable form of the routing table; governance-skeptic's lighter parenthetical disambiguation (Recommendation 9) plus a Principle XVII cross-reference is another. I do not require the full decision tree; I require that the destination set explicitly include `AGENTS.md` (per Non-Negotiable 3) and that form-constraint principles have a documented remand path that does not silently demote them to a poor-fit destination. Either reviewer's framing satisfies this if Non-Negotiable 1's closed-list admission is also adopted (which substantially reduces the routing-table load).

**Flexibility 3: Precedent log mechanism (derived index vs. hand-maintained log).**

Practitioner's amended #8 (derived index from Sync Impact Reports, rebuilt on demand by the speckit pipeline) and governance-skeptic's NR-1 retrospective calibration trigger (recorded in Sync Impact Reports) are compatible. I do not require a separate `governance-decisions.md` file; the derived-index approach satisfies my R-6 retrospective-review goal at lower Principle XI risk. Either implementation is acceptable as long as the log is queryable and feeds the calibration trigger from Flexibility 1.

---

**Bottom line.** The Phase 3 revisions converged on five fixes and narrowed the disagreement surface to three points: the AND-coupling structural fix (Non-Negotiable 1), the grandfathering disclosure in the Sync Impact Report (Non-Negotiable 2), and the `AGENTS.md` destination correction (Non-Negotiable 3). The first is the substantive disagreement; the second is the calibration-anchor disagreement; the third is mechanical. All three are dispositive: ship the gate without them and v2.4.0 enshrines a stricter forward filter than the constitution has ever survived, with no in-document evidence that the discrepancy exists. The flexibility on calibration triggers, routing-table form, and precedent-log mechanism shows where I am willing to converge; the non-negotiables show where I am not.
