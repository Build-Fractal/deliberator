# Synthesis: Monorepo vs Polyrepo Decision

**Deliberation mode:** Cooperative
**Target:** monorepo-vs-polyrepo.md — Should a team of 15 engineers with 3 polyglot services use a monorepo or polyrepo?
**Synthesizer:** Neutral (no agent affiliation)

---

### Process Summary

| Metric | Value |
|--------|-------|
| Agents | 2 (pragmatist, devils-advocate) |
| Total artifacts produced | 10 (1 target + 2 reviews + 2 cross-reviews + 2 revisions + 2 dispute filings + 1 synthesis) |
| Phase 1 recommendations proposed | 15 (pragmatist: 7, devils-advocate: 8) |
| Recommendations withdrawn | 1 (pragmatist R7 merged into R3) |
| Recommendations modified | 8 (pragmatist: R2, R3, R5, R6, R7; devils-advocate: R2, R4, R5, R7, R8) |
| Recommendations surviving unchanged | 6 (pragmatist: R1, R4; devils-advocate: R1, R3, R6) |
| New recommendations added in Phase 3 | 4 (pragmatist: N1, N2; devils-advocate: N1, N2) |
| Disputes remaining after Phase 4 | 3 from each agent (6 filings, 3 distinct disputes with overlap) |
| Convergence points | 5 formally declared by each agent (5 distinct, fully overlapping) |

Both agents exhibited strong cooperative behavior: concessions were substantive (not cosmetic), cross-review challenges were adopted where valid, and new recommendations emerged from genuine synthesis rather than log-rolling. The deliberation's most productive dynamic was the cross-review phase, which surfaced a scope conflict in the shared-repo proposals that neither agent had identified independently.

---

### Recommendation Scorecard

| # | Agent | Recommendation | Phase 1 Priority | Phase 3 Disposition | Challenged By | Convergence | Final Status |
|---|-------|---------------|-------------------|---------------------|---------------|-------------|--------------|
| P-R1 | Pragmatist | Deploy schema compatibility checks (Buf) | P1 | Surviving | — | Strong (both agents' #1) | **ADOPTED** |
| P-R2 | Pragmatist | Add cross-repo integration CI | P1 | Modified — integration tests moved into shared-contracts repo | DA cross-review (scope conflict) | Partial | **ADOPTED (modified scope)** |
| P-R3 | Pragmatist | Defer monorepo decision 3-6 months | P1 | Modified — bound to 30-day instrumentation mandate | DA cross-review (data vacuum) | Strong (principle); Disputed (timeline shape) | **ADOPTED (with instrumentation binding)** |
| P-R4 | Pragmatist | Evaluate platform team need before monorepo | P2 | Surviving | DA (severity framing: weight vs. gate) | Strong | **ADOPTED** |
| P-R5 | Pragmatist | Benchmark monorepo build tooling for polyglot | P2 | Modified — merged with DA-R4 into single spike | DA cross-review (resource contention) | Moderate | **ADOPTED (merged with DA-R4)** |
| P-R6 | Pragmatist | Define rollback criteria for any migration | P2 | Modified — adopted DA's quantitative thresholds | DA cross-review (vague criteria) | Strong | **ADOPTED (unified framework)** |
| P-R7 | Pragmatist | Instrument actual developer pain | P3 | Withdrawn — merged into P-R3 as precondition | DA cross-review (deferral-instrumentation disconnect) | N/A | **MERGED into P-R3** |
| DA-R1 | Devil's Advocate | Isolate the schema problem | P1 | Surviving | — | Strong (both agents' #1) | **ADOPTED** |
| DA-R2 | Devil's Advocate | Require asymmetric risk assessment | P1 | Modified — gates only the monorepo decision, not the schema fix | Pragmatist cross-review (analysis overkill for cheap fix) | Moderate | **ADOPTED (scoped to monorepo)** |
| DA-R3 | Devil's Advocate | Decompose migration cost into workstreams | P1 | Surviving | Pragmatist (mixed signals with deferral) | Moderate | **ADOPTED (as estimation tool)** |
| DA-R4 | Devil's Advocate | Benchmark CI duration under monorepo | P2 | Modified — sequenced after validation window, merged with P-R5 | Pragmatist (premature if deferred) | Moderate | **ADOPTED (conditional + merged)** |
| DA-R5 | Devil's Advocate | Evaluate "thin shared repo" middle path | P2 | Modified — scope narrowed to protos + buf only at launch | Pragmatist cross-review (mini-monorepo risk) | Strong (narrow scope converged) | **ADOPTED (narrow scope)** |
| DA-R6 | Devil's Advocate | Stress-test the scaling argument | P2 | Surviving | Pragmatist (speculative, defer) | Moderate | **ADOPTED (deferred to revisit)** |
| DA-R7 | Devil's Advocate | Define rollback criteria | P2 | Modified — unified with P-R6, broadened scope | Pragmatist (narrow scope) | Strong | **MERGED with P-R6** |
| DA-R8 | Devil's Advocate | Name the opportunity cost | P3 | Modified — conditional, activates only for monorepo consideration | Pragmatist (overkill for schema fix) | Weak | **ADOPTED (conditional)** |
| P-N1 | Pragmatist | Validate schema fix with 60-day window | P1 | New in Phase 3 | DA (disputes sufficiency) | Moderate | **ADOPTED** |
| P-N2 | Pragmatist | Unify shared repo scope before implementation | P1 | New in Phase 3 | DA (disputes premature convergence) | Disputed | **ADOPTED (with DA's binary-question gate)** |
| DA-N1 | Devil's Advocate | Mandate validation window with instrumentation | P1 | New in Phase 3 | Pragmatist (timeline shape) | Strong (principle); Disputed (mechanism) | **ADOPTED (within 3-month outer bound)** |
| DA-N2 | Devil's Advocate | Unify shared repo scope decision | P1 | New in Phase 3 | — | Strong | **MERGED with P-N2** |

---

### Dangerous Contradictions Found

**Resolved:**

1. **Shared repo scope collision (Pragmatist's narrow proto repo vs. Devil's Advocate's broad shared repo).** Both agents proposed a fourth repository but with incompatible scope — one proto-only, the other including shared libraries and integration tests. If both were implemented, the team would create two overlapping shared repos. **Resolution:** Both agents converged on narrow scope (proto files + buf validation only at launch). Devil's Advocate conceded integration tests belong in CI pipelines, not in the shared repo. Pragmatist conceded shared libraries should stay in current locations. Scope expansion requires explicit team agreement. *(Pragmatist cross-review DC§1, DA cross-review DC§2)*

2. **Asymmetric risk assessment vs. "just ship the fix."** Devil's Advocate's original P1 recommendation for probabilistic risk assessment before any action conflicted with the Pragmatist's "deploy the 2-day fix now" urgency. **Resolution:** Devil's Advocate conceded the risk assessment gates only the monorepo decision, not the schema fix. Cheap, reversible actions don't need formal risk analysis. *(Pragmatist cross-review DC§2, DA revision R2)*

3. **Coordinated PRs as safety mechanism vs. friction source.** Devil's Advocate argued cross-repo PRs force healthy communication; Pragmatist argued the coordination gap is where production breaks. **Resolution:** Not explicitly resolved, but rendered moot by convergence on the shared-contracts repo with CI enforcement — which provides the review gate Devil's Advocate values while eliminating the coordination gap the Pragmatist identified. *(Pragmatist cross-review DC§3)*

4. **Rollback criteria scope conflict (any migration vs. monorepo-only).** **Resolution:** Unified into a single framework with quantitative triggers (from Devil's Advocate) and qualitative escape valve (from Pragmatist), applicable to whichever path is chosen. *(Pragmatist cross-review DC§4, DA cross-review DC§4)*

**Unresolved:**

5. **Migration estimation gap (4-8 weeks vs. 3-4 months).** The Pragmatist estimates a monorepo migration at 4-8 weeks; Devil's Advocate's workstream decomposition yields 3-4 months. Both agents agree the decomposition framework is the right tool but did not reconcile the estimates. This 2-4x gap is dormant while the decision is deferred but becomes dangerous if the monorepo decision resurfaces under pressure. *(DA cross-review DC§3, DA Phase 4 Dispute§3)*

6. **Shared repo necessity.** Devil's Advocate's Phase 4 dispute argues the converged narrow-scope shared repo (proto files + buf validation) may be redundant — buf-in-CI can validate schemas without a dedicated repository. The Pragmatist's position treats the shared repo as a single source of truth. This was raised late and not fully adjudicated. *(DA Phase 4 Dispute§2)*

---

### Systemic Contradictions

1. **Incident-driven urgency vs. structural analysis.** The Pragmatist optimizes for stopping the bleeding (fix schema mismatches now, think later). Devil's Advocate optimizes for accurate diagnosis (understand the full coordination failure surface before committing to any path). Both are valid but produce different sequencing — and a team following both simultaneously gets conflicting signals about whether to act or analyze first. The synthesis resolves this by sequencing: act on the schema fix immediately, then analyze during a structured validation window.

2. **Deferral as strategy vs. deferral as avoidance.** Both agents agree the monorepo decision should be deferred, but they assign opposite risks to the deferral itself. The Pragmatist fears the team will make a rash structural decision under incident pressure. Devil's Advocate fears the team will defer indefinitely and never revisit the question with data. These fears are both well-founded and cannot both be fully mitigated — the instrumentation-bound deferral is a compromise, not a resolution.

3. **Narrow scope as safety vs. narrow scope as inadequacy.** Both agents converged on a narrow shared repo, but for opposite reasons. The Pragmatist narrowed scope to prevent the mini-monorepo failure mode. Devil's Advocate narrowed scope to concede gracefully but then challenged whether the resulting artifact solves any problem that buf-in-CI doesn't already address. The convergence on scope masks a divergence on whether the shared repo should exist at all.

4. **Scaling projections: input to the decision vs. distraction from the decision.** The Pragmatist treats the 15→30 growth trajectory as speculative noise that shouldn't drive today's decision. Devil's Advocate treats it as a factor that must be stress-tested in both directions because it's the monorepo's strongest post-schema-fix justification. The original question explicitly asks the team to account for growth — dismissing it entirely is non-responsive, but over-weighting hypothetical futures against concrete present pain is analysis paralysis.

5. **Confidence calibration on the schema fix.** The Pragmatist presents the schema fix with high confidence ("deployable in 1-3 days," "directly addresses both incidents"). Devil's Advocate frames it as a hypothesis to validate ("if this solves the pattern"). Both agents agreed on a validation window, but the underlying confidence divergence means they would react very differently if the first month shows ambiguous results — the Pragmatist would likely extend the deferral, the Devil's Advocate would likely reopen the structural question.

---

### Convergence Achieved

Ordered by strength of agreement:

1. **Deploy schema compatibility checks immediately (Buf-based breaking-change detection in CI).** Both agents' highest-priority recommendation, independently proposed with identical tool choice, timeline (1-3 days), and rationale. Identified as the strongest agreement in all four cross-review documents. Neither agent challenged any aspect of this recommendation across four phases. *Strength: Maximum.*

2. **A monorepo without adequate tooling and platform support is the worst possible outcome.** Both agents independently concluded that a partial or under-tooled monorepo is worse than either a well-maintained polyrepo or a fully committed monorepo. The Pragmatist frames this as "shared liability with no steward"; Devil's Advocate frames it as "the most common monorepo failure mode." Directionally identical despite different severity framing (weight vs. gate). *Strength: Strong.*

3. **The monorepo decision should not be made under incident pressure.** The Pragmatist: "Decisions made under incident pressure optimize for the last failure, not the next one." Devil's Advocate: the incidents are symptoms of a CI gap, not evidence for a structural migration. Both agree: stabilize first, then evaluate architecture. *Strength: Strong.*

4. **Deferral without instrumentation is procrastination.** Emerged from the cross-review process as a sharpened joint position. Devil's Advocate landed the challenge; Pragmatist incorporated it by binding developer friction measurement to the first 30 days of the deferral. Both revised positions require quantitative coordination-cost data before the structural decision is revisited. *Strength: Strong.*

5. **Monorepo tooling options (Nx, Turborepo, Bazel) are all problematic for this polyglot stack without a platform team.** Both agents independently concluded none of the three named tools are a good fit. Nx and Turborepo lack polyglot support; Bazel has a prohibitive learning curve for a team without platform engineers. This shared assessment was unchallenged across all phases. *Strength: Strong.*

6. **Rollback criteria must be quantitative and pre-committed.** Converged during the revision phase. Devil's Advocate contributed concrete thresholds (CI >20 min, >5 merge conflicts/week, >10% engineer time on build tooling); Pragmatist contributed broader scope (apply to any path, not just monorepo) and qualitative escape valve. *Strength: Moderate — framework agreed, specific threshold values require team calibration.*

7. **Shared repo scope should start narrow.** Emerged from cross-review collision between the two agents' shared-repo proposals. Both conceded to proto files + buf validation only at launch, with scope expansion requiring explicit team agreement. Note: Devil's Advocate later disputed whether the narrow shared repo solves any problem buf-in-CI doesn't already address — the convergence on scope masks residual divergence on necessity. *Strength: Moderate (scope agreed; necessity disputed).*

---

<!-- DELIBERATOR:DISPUTES_BEGIN -->
### Remaining Disputes

---

**Dispute: Deferral Timeline Shape**

**Positions:**
- *Pragmatist:* Hard 3-month outer bound with a 6-8 week early checkpoint. Calendar date forces revisit even if data is ambiguous. Prevents organizational inertia from converting "defer" into "never decide."
- *Devil's Advocate:* 6-8 week validation window with explicit instrumentation. Data-triggered gates, no arbitrary deadline. If signal is clear at week 8, a month-6 deadline wastes decision bandwidth.

**Arguments:**
- Pragmatist: Teams under delivery pressure will stop checking dashboards after two weeks. A calendar date on the roadmap is harder to ignore than a conditional trigger. Ambiguous data at month 3 still forces a conversation.
- Devil's Advocate: Fixed deadlines are arbitrary. If data clearly shows no coordination pain at week 8, waiting until month 6 is waste. If pain emerges at week 4, a fixed timeline delays response.

**Synthesizer assessment:** Both agents offered a proposed resolution in their dispute filings that substantially overlaps: the Pragmatist proposed adopting the 6-8 week validation window as the first gate *within* a hard 3-month outer bound. Devil's Advocate stated the Pragmatist's "30-day instrumentation + 3-month review cadence is a workable structure." This dispute is effectively resolved — both agents can accept the nested structure. The remaining gap is cosmetic, not substantive.

**Recommended resolution:** Adopt the nested structure both agents described: 30-day instrumentation sprint → 6-8 week validation checkpoint → 3-month hard outer bound. If the 6-8 week checkpoint produces clear signal, the team can formally close or reopen the monorepo question early. If signal is ambiguous, the 3-month deadline forces the conversation. This captures both agents' core concerns (data-driven gates + inertia prevention).

---

**Dispute: Shared Repo Necessity and Scope**

**Positions:**
- *Pragmatist:* A shared-contracts repo (proto files + buf validation) provides a single source of truth for schema definitions and a natural home for integration smoke tests if needed later. Start narrow, expand deliberately.
- *Devil's Advocate:* The narrow shared repo may be a glorified git submodule that adds a coordination point without adding validation capability beyond what buf-in-CI already provides. The team should articulate what problem the repo solves that buf alone doesn't before creating it.

**Arguments:**
- Pragmatist: Centralizing proto definitions eliminates the current multi-copy pattern. Even without integration tests, a single source of truth simplifies schema evolution. The repo is cheap to create and easy to abandon.
- Devil's Advocate: A fourth repo means a fourth place to coordinate. Buf can validate against a schema registry or a git-based source of truth without a dedicated repository. Creating infrastructure by default rather than by necessity is how teams accumulate coordination overhead.

**Synthesizer assessment:** This is a genuine dispute about organizational philosophy — whether a lightweight structural artifact (a dedicated repo) or a lightweight process artifact (buf validation in existing CI) is the better carrier for schema governance. The Pragmatist's position is lower-risk (the repo is cheap and reversible). The Devil's Advocate's position is more rigorous (solve a stated problem, not an assumed one). Both have merit.

**Recommended resolution:** Adopt Devil's Advocate's binary-question gate: before creating the shared repo, the team must answer "Does the current multi-copy proto pattern cause problems beyond the two schema incidents that buf-in-CI would not already solve?" If yes (e.g., conflicting local edits, unclear canonical version), create the shared repo with narrow scope. If no, run buf validation against a designated canonical location within one of the existing repos and revisit if that proves insufficient. This avoids creating infrastructure by default while preserving the Pragmatist's option to centralize if evidence warrants it.

---

**Dispute: Migration Estimation Gap (4-8 Weeks vs. 3-4 Months)**

**Positions:**
- *Pragmatist:* 4-8 weeks is realistic for 3 services, 4 proto files, and 15 engineers. The decomposition is a useful tool but shouldn't inflate the estimate based on worst-case assumptions.
- *Devil's Advocate:* 3-4 months is the realistic floor once the migration is decomposed into workstreams (build tooling, CI, ownership, developer workflow). Aggregated estimates hide complexity and produce budget overruns.

**Arguments:**
- Pragmatist: Small surface area bounds the scope. The decomposition framework should be populated with team-specific data from a benchmark spike, not pre-loaded with worst-case assumptions. The spike will break the tie.
- Devil's Advocate: The gap is not a difference of optimism — it reflects incompatible scope definitions. Deferral doesn't resolve estimation gaps; they widen as codebases grow. A 2-4x gap at commitment time is how teams blow budgets.

**Synthesizer assessment:** Both agents agree the decomposition framework is the right estimation tool and that a benchmark spike should produce actual numbers. The dispute is about what the default assumption should be *before* the spike. This is a reasonable disagreement that cannot be resolved without empirical data from the team. Both agents proposed the same resolution mechanism (benchmark spike + bottom-up estimate). The dispute is about framing risk, not about the resolution path.

**Recommended resolution:** Document the estimation gap (4-8 weeks vs. 3-4 months) as an explicit risk in any future monorepo evaluation. If the monorepo decision becomes live, the first action is a 2-day estimation spike using the workstream decomposition, producing a bottom-up estimate. No migration commitment without a reconciled estimate. Both agents proposed essentially this resolution — the dispute is already resolved on mechanism, if not on priors.

---
<!-- DELIBERATOR:DISPUTES_END -->

### Actionable Spec Changes

**P1 — Must Implement:**

1. **Deploy Buf-based schema compatibility checks in CI across all three repos.** Run `buf breaking` and `buf lint` against all 4 shared proto files on every PR in any repo. Target: operational within 1-3 days. *(Source: Pragmatist R1, DA R1 — strongest convergence point)*

2. **Establish a 60-day validation window with instrumentation.** Track: (a) schema-related incidents (target: zero), (b) cross-repo coordination time per cross-cutting change (PR open to last PR merged), (c) developer-reported friction via structured survey within first 30 days. If incidents recur or coordination pain persists, escalate to structural evaluation. *(Source: Pragmatist N1, DA N1 — converged with complementary instrumentation)*

3. **Resolve the shared repo question before implementation.** Apply Devil's Advocate's binary-question gate: does the multi-copy proto pattern cause problems beyond the schema incidents? If yes → create narrow shared-contracts repo (proto files + buf config only). If no → designate a canonical proto location in an existing repo and validate from there. *(Source: Pragmatist N2, DA N2, DA Phase 4 Dispute§2)*

4. **Define quantitative rollback criteria before committing to any structural change.** Thresholds: CI time >20 min, >5 merge conflicts/week on shared trunk, >10% of any engineer's time on build tooling maintenance. Include structured developer survey at 4 and 8 weeks as qualitative escape valve. *(Source: Pragmatist R6 modified, DA R7 modified — converged)*

**P2 — Should Implement:**

5. **Require platform ownership model before any monorepo commitment.** Identify 1-2 engineers for platform responsibility (dedicated or rotational) who will own build tooling, CI infrastructure, and CODEOWNERS enforcement. A monorepo without a platform steward is the worst possible outcome. *(Source: Pragmatist R4, DA convergence§2)*

6. **Run a combined tooling + CI benchmark spike if the monorepo decision becomes live.** 2-3 days per candidate tool (Nx, Turborepo, Bazel) against the actual Node + Python + Go stack. Measure: setup time, build correctness, selective CI accuracy, end-to-end CI times on representative changesets, and developer onboarding friction. *(Source: Pragmatist R5 modified, DA R4 modified — merged)*

7. **Decompose migration cost into workstreams for honest estimation.** Six workstreams: (a) repo consolidation + history preservation, (b) build system adoption + config, (c) CI/CD pipeline rewrite, (d) developer tooling updates, (e) CODEOWNERS + review process redesign, (f) deployment pipeline changes. Produce bottom-up estimate before any commitment. *(Source: DA R3)*

8. **Stress-test the scaling argument in both directions at the 3-month revisit.** Project whether observed coordination friction would compound at 25-30 engineers under both monorepo and polyrepo scenarios. Use real data from the validation window, not hypothetical projections. *(Source: DA R6, Pragmatist convergence§5)*

**P3 — Consider:**

9. **Name the opportunity cost if a monorepo migration is considered.** Explicitly identify 2-3 product features or infrastructure improvements that would be delayed by the migration timeline. Frame as: "We are choosing repository infrastructure instead of [X, Y, Z] for the next N months." *(Source: DA R8 modified — conditional on monorepo consideration)*

10. **Require asymmetric risk assessment for the monorepo decision.** If the monorepo path becomes live, explicitly estimate probability of successful implementation vs. probability of a stalled partial migration — which both agents identified as the worst possible outcome. *(Source: DA R2 modified)*

---

### Key Concessions

**Pragmatist conceded:**

1. **Deferral must be bound to instrumentation.** Original position treated deferral (R3) and developer pain measurement (R7) as independent recommendations. Devil's Advocate's cross-review exposed this as creating a data vacuum. Pragmatist merged R7 into R3 as a binding precondition — the deferral only works if measurement happens in the first 30 days. *(DA cross-review DC§1 → Pragmatist revision R3, R7)*

2. **Rollback criteria must be quantitative.** Original "developer satisfaction drops below threshold" was unmeasurable. Adopted Devil's Advocate's concrete thresholds (CI >20 min, >5 merge conflicts/week, >10% engineer time). *(DA cross-review DC§4 → Pragmatist revision R6)*

3. **Schema fix confidence should be testable, not assumed.** Originally presented the schema fix as near-certain. Accepted Devil's Advocate's challenge to treat it as a hypothesis with a 60-day validation window. *(DA cross-review Tension§5 → Pragmatist revision N1)*

4. **Tooling and CI benchmarks should be a single spike.** Originally proposed separate spikes for build tooling (R5) and CI measurement. Accepted resource-contention argument and merged into one spike. *(DA cross-review Tension§4 → Pragmatist revision R5)*

**Devil's Advocate conceded:**

1. **Shared repo scope must start narrow.** Original position included shared libraries and integration tests in the shared repo. Accepted Pragmatist's challenge that this risks recreating a mini-monorepo. Narrowed to proto files + buf validation only. *(Pragmatist cross-review DC§1 → DA revision R5)*

2. **Asymmetric risk assessment doesn't apply to cheap fixes.** Original position implied formal probabilistic analysis before any action. Accepted that the schema fix (2-day, reversible, obvious upside) doesn't need it. Scoped the risk assessment to gate only the monorepo decision. *(Pragmatist cross-review DC§2 → DA revision R2)*

3. **Opportunity cost analysis doesn't apply to cheap fixes.** Original P3 recommendation to name displaced features was calibrated for a multi-month migration. Accepted it's overkill for a 2-day schema CI gate. Made it conditional on the monorepo path being under serious consideration. *(Pragmatist cross-review DC§4 → DA revision R8)*

4. **CI benchmark should be sequenced, not run in parallel.** Original position implied running CI benchmarks alongside the schema fix. Accepted Pragmatist's argument that this is premature if the monorepo decision is deferred. Sequenced it after the validation window. *(Pragmatist cross-review Tension§3 → DA revision R4)*

5. **Softer framing on the scaling argument.** Originally characterized the scaling argument as "actively misleading." Accepted Pragmatist's "speculative, validate before relying on it" framing as equally cautious but less confrontational. *(Phase 4 Flexibility§2)*
