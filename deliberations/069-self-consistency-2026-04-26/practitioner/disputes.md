# Practitioner Disputes — Phase 4

**Persona**: Pragmatist (future amendment author lens)
**Phase 4 (disputes after revision)**
**Position carried forward from revision**: ship the gate with amended enforcement scaffolding (template inside the Sync Impact Report, form-only CI lint, derived precedent log, v2.4.0 sync impact report with grandfathering disclosure, criterion 2 wording fix with explicit-coordination extension, expedited path with rollback authority, XVII cross-link in the corrected direction, verification deliberation with documented-disputes acceptance bar, panel-composition disclosure, 14-day cooling-off). The Phase 3 cross-revisions sharpened my position on form-vs-substance enforcement and on derived-vs-maintained precedent logs; they did not move me on the central disagreement with strictness-skeptic over AND→partial-OR restructuring versus evidence-triggered loosening.

---

### Remaining Disputes

#### Dispute 1: Structural restructure of criterion AND-coupling (R-1) versus evidence-triggered loosening (my NR-1)

This is the deepest unresolved disagreement and the one most likely to determine whether v2.4.0 ships with a coherent gate or a contested one. Strictness-skeptic's revised R-1 ("criterion 2 AND criterion 3 required, criterion 1 substitutable via mechanical-sketch OR peer-review-rubric") is structurally elegant but bakes a categorical judgment — "this is the kind of principle that gets the rubric branch" — into every future amendment review. My counter-position is that the right place for that categorical judgment is *retrospective evidence*, not *prospective gate structure*. If three amendments are rejected by criterion 1 alone over a MAJOR cycle, that pattern itself is the calibration signal — we then loosen the gate with worked examples derived from the actual rejected proposals, not from hypothetical form-constraint scenarios.

Strictness-skeptic's revised position narrows the open-class problem (closed enumeration of relaxed-criterion-1 principles tied to VI, X, XVI, XVII, XVIII), and that narrowing is real progress. But the closed list itself is a frozen artifact: future principles outside that list face the unmodified bar, while the listed principles get a structural pass. This creates a two-tier constitution where some grandfathered principles enjoy permanent special-case status. My evidence-triggered alternative produces the same outcome (criterion 1 gets loosened when evidence accumulates) without freezing the special-case list at v2.4.0.

The arbitration question for the synthesis pass: does the constitution accept *prospective categorical loosening* (strictness-skeptic) or *retrospective evidence-triggered loosening* (me)? Governance-skeptic's NR-1 (calibration review when ≥3 rejections in a MAJOR cycle) is structurally identical to my NR-1, which suggests the evidence-triggered path has independent support. I believe the synthesis should adopt evidence-triggered loosening and reject the closed-list restructure on the grounds that the closed list is itself a calibration claim made without empirical evidence — exactly what strictness-skeptic argues against doing in R-2's worked-example requirement. Strictness-skeptic's R-1 is theory-first restructuring that violates strictness-skeptic's own R-5 sequencing principle.

#### Dispute 2: Sync Impact Report self-assessment as authoritative versus derived precedent log as the queryable surface

Governance-skeptic's revised R-2 (self-assessment in Sync Impact Report) and my amended #8 (derived precedent log) describe overlapping but non-identical artifacts. Governance-skeptic treats the per-amendment self-assessment as the load-bearing artifact, with reviewer judgment as the substantive enforcement. I treat the cross-amendment precedent log as the load-bearing artifact, with the per-amendment self-assessment as the input format that the log derives from. The two views differ on what is queryable at amendment time.

Under governance-skeptic's framing, a future amendment author writes their self-assessment by reading the constitution gate text and answering its three questions. Under my framing, they additionally read the derived precedent log to see how prior amendment authors answered each criterion in similar cases — the log functions as a stare-decisis surface. Governance-skeptic's NR-1 (retrospective recalibration trigger when ≥3 rejections accumulate) implicitly requires the precedent log to exist to count rejections, so the disagreement may be more about emphasis than substance. But it has practical consequences: if the precedent log is "nice to have," it will not be built; if it is required for the recalibration trigger to function, it is load-bearing infrastructure that should be specified in the gate.

The arbitration question: is the precedent log *required infrastructure* (my position — needed for recalibration triggers, panel-composition aggregation, criterion-rejection counts) or *helpful tooling* (governance-skeptic's implicit position — Sync Impact Reports are sufficient and the log is downstream)? I argue the gate text should reference the derived log explicitly so its construction is mandatory, not optional. Without that, the recalibration triggers (mine and governance-skeptic's) have no source data.

#### Dispute 3: Acceptance bar for verification deliberation — documented-disputes (mine) versus zero-disputes (original) versus governance-skeptic-silent

Governance-skeptic's revision did not directly engage with my amended #5 (documented-disputes acceptance bar replaces zero-disputes blocker). Strictness-skeptic's revision implicitly endorsed my framing via SA-2's "all disputes documented and addressed in the Sync Impact Report." But the candidate constitution as written does not reference verification deliberation at all — that is a separate question from the inclusion criteria gate. The dispute is whether v2.4.0 should codify any verification-deliberation requirement, or whether that should be a follow-up amendment.

I argue v2.4.0 should land the verification-deliberation requirement *with* the gate, because the gate's substantive enforcement (reviewer judgment of criterion-1 sketches and criterion-3 distinctness arguments) lives precisely in the verification deliberation. Without codifying verification deliberation in the same amendment, the gate is procedurally enforceable (CI lint on form) but not substantively enforceable (no required venue for substantive review). That is the calibration-fragility scenario strictness-skeptic correctly flagged in R-2.

The arbitration question: bundle verification deliberation into v2.4.0 (creates a complete enforcement chain), or defer to v2.5.0 (preserves the smaller-amendment principle)? My position is bundle, with the documented-disputes acceptance bar to defang the single-veto failure mode governance-skeptic correctly identified.

---

### Convergence

#### Convergence 1: Lift the gate to its own subsection, not a Governance bullet

All three reviewers converged on this in Phase 2 and held through Phase 3. Governance-skeptic R-1 (surviving), strictness-skeptic R-12 (new in revision but matches), my SA-3 (original review). The mechanical change is small (replace `### Governance` bullet 3 with a sibling `### Constitutional Inclusion Criteria` subsection); the audit-trail benefit is large (`/speckit.constitution check` can grep for the heading). No remaining disagreement.

#### Convergence 2: Ship the v2.4.0 Sync Impact Report at the top of the candidate file with explicit grandfathering disclosure

All three reviewers converged. Governance-skeptic NR-2, strictness-skeptic R-11, my #6 (strengthened). The constitution's own discipline (Principle XII / Versioning) requires this; the candidate file violates that discipline by carrying a v2.3.0→v2.3.1 report at the top instead of a v2.3.1→v2.4.0 report. The strengthened version (per strictness-skeptic's T-3 and my revision) explicitly enumerates which grandfathered principles fail the new gate (per spec 069 §5: VI, X, XVI), making calibration evidence permanent and visible. This is the single largest self-consistency fix in the deliberation and should land regardless of how Disputes 1-3 resolve.

#### Convergence 3: PATCH carve-out is dead; replace with lightweight "N/A — typo fix" answer in the self-assessment

I withdrew this in Phase 3 in response to governance-skeptic's DC-1 and strictness-skeptic's DC-3. Governance-skeptic's modified Recommendation 7 explicitly endorses the "cost scales with materiality" pattern. The mechanical artifact is a Sync Impact Report that contains four sub-headings (Mechanical Verification, Falsifiable Scope, Distinctness, Routing Decision) with "N/A — justified because {rationale}" as a permitted answer for any criterion when the amendment is not adding or redefining a principle. This converges cleanly across all three reviewers and the form-only CI lint enforces the structural shape without substantive over-reach.

#### Convergence 4: Cross-link from gate to Principle XVII (not the reverse)

Governance-skeptic SA-4 (surviving), strictness-skeptic noted but did not contest, my revised #10 (direction corrected). The constitution's reference topology (newer references older, never the reverse) makes this the only correct direction. Cross-link wording: "Constitutional Inclusion Criteria inherits Principle XVII's Content Classification vocabulary; routing decisions to operational guidance follow XVII's execution-logic vs. contribution-guidelines distinction." The downstream pressure strictness-skeptic noted in their T-5 (XVII's clean two-way split versus the gate's fuzzier four-way fan-out) is a feature: future amendment authors will notice the asymmetry and have a legitimate basis for proposing a tightening of the routing table.

#### Convergence 5: Routing destination must be `AGENTS.md` (not `CONTRIBUTING.md`)

Strictness-skeptic R-13 caught this in their revision; the candidate file references `CONTRIBUTING.md` which does not exist in the repo. Principle XVII routes contribution rules to `AGENTS.md`. I did not flag this in my original review and did not engage with it in my Phase 3 revision; on reflection it is a clean pre-merge fix independent of the larger calibration debate. Adopt as drafted in strictness-skeptic R-13.

---

### Final Position Statement

#### Non-Negotiables

**NN-1 — The gate ships with at least minimal enforcement scaffolding, not gate text alone.** A constitutional gate text that is not accompanied by (a) a Sync Impact Report self-assessment requirement, (b) a form-only CI lint, and (c) a v2.4.0 Sync Impact Report at the top of the constitution itself is a gate that exists nowhere except in prose. Future amendment authors cannot use a gate that has no template to fill, no machine-checkable artifact to produce, and no precedent to compare against. My PR-author lens sees this clearly: I have spent multiple cycles proposing principles that were declined by deliberation arbiters, and the difference between a useful rejection and a frustrating one is whether the rejection cites a documented criterion against a documented prior decision. Without the scaffolding, the gate fires capriciously.

**NN-2 — The Sync Impact Report self-assessment MUST explicitly enumerate grandfathered principles that fail the new gate.** Spec 069 §5 identifies VI, X, XVI as failing under the strict reading. That enumeration cannot live only in the deliberation folder — it must live in the constitution's own change-tracking record, attached to v2.4.0 itself, so every future amendment author reads the calibration evidence as part of reading the gate. Without this, the gate's bar is rhetorical; with it, the bar is empirical and self-documenting. Strictness-skeptic and I converged on this independently and it is the strongest signal in the deliberation.

**NN-3 — The expedited amendment path MUST carry rollback authority, not just post-hoc verification.** Governance-skeptic's DC-3 against my original #9 caught a real bypass: as drafted, "license-compliance issues" and "regulatory changes" are author-defined open categories where verification findings only "land as a follow-up amendment" — meaning the bypass is a one-way door. The fix (post-hoc verification deliberation within 14 days WITH explicit rollback authority on material findings) closes the bypass while preserving the incident-response use case. Without rollback authority, the expedited path becomes the laundering channel for any amendment whose author classifies it as urgent, and the entire gate is bypassable on a single classification decision.

#### Flexibility

**F-1 — I can accept strictness-skeptic's closed-list R-3/R-7 collapse if Dispute 1 cannot be resolved by adopting evidence-triggered loosening.** My NR-1 (evidence-triggered calibration after ≥3 criterion-1-only rejections) is my preferred path because it avoids freezing a special-case list at amendment time. But if synthesis pressure pushes toward strictness-skeptic's closed enumeration of VI, X, XVI, XVII, XVIII as relaxed-criterion-1 principles, I can live with it provided the list is annotated as "reviewable at v3.0.0" — the sunset clause strictness-skeptic accepted in their R-5 revision generalizes to R-3 cleanly. The closed list is worse than evidence-triggered loosening; it is better than no provision at all for form-constraint and meta-principle categories.

**F-2 — I can drop the 14-day cooling-off period (my NR-2) if the panel-composition disclosure (NR-3) lands.** The cooling-off period and the panel-disclosure requirement target the same risk (deliberation-skew effects from panel composition) via different mechanisms. The cooling-off period is wall-clock-time pressure for fresh-eyes review; the panel disclosure is auditable transparency that creates back-pressure against panel-stacking. They compose well, but if synthesis treats one as redundant with the other, panel disclosure is the higher-value half because it produces a queryable artifact (every Sync Impact Report names the panel) that future deliberations can review. The cooling-off period only matters if someone uses it; the disclosure matters even when no one objects, because it accumulates into the precedent log.

**F-3 — I can accept verification-deliberation codification as a v2.5.0 follow-up amendment rather than bundling into v2.4.0 (Dispute 3).** My preference is to bundle, because the gate's substantive enforcement lives in the verification deliberation and the amendment loses coherence without it. But if synthesis judges v2.4.0's scope is already too large (the constitution typically lands smaller amendments), a v2.4.0 that codifies the gate text + Sync Impact Report scaffolding + form-only CI lint + grandfathering disclosure, followed immediately by v2.5.0 codifying verification deliberation with documented-disputes acceptance bar, is acceptable. The risk is that v2.5.0 stalls and the gate's substantive enforcement never lands; the mitigation is to make the v2.5.0 amendment a TODO entry in the v2.4.0 Sync Impact Report's Follow-up section, anchoring the commitment in the constitution's own audit trail.

---

The smaller framing of this revision against my original review: the cross-reviews moved me toward enforcement that is both lighter (form-only lint, derived precedent log) and more durable (grandfathering disclosure baked into the Sync Impact Report, panel-composition transparency). What I retained against pressure is the conviction that future amendment authors need infrastructure, not just text — a conviction strengthened, not weakened, by strictness-skeptic's calibration concerns. The gate's purpose is to discriminate principles from operational guidance; the scaffolding's purpose is to make that discrimination usable, auditable, and self-correcting. Ship v2.4.0 with the convergent fixes, resolve the three remaining disputes via synthesis arbitration, and treat the candidate file's missing v2.4.0 Sync Impact Report as a load-bearing self-consistency failure that must be fixed before merge regardless of any other outcome.
