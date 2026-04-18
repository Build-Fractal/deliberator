# Worked Example: Conversus Output vs Single-Model Response

## Introduction

This document compares the output of a 2-agent conversus cooperative deliberation against a single-model Claude response for the same questions. The goal is to identify **structural differences** — properties present in the multi-agent output that are structurally impossible in a single-model response, not just stylistically different.

Two questions were used:
- **Dev question:** "Should a team of 15 engineers with 3 polyglot services use a monorepo or polyrepo?" (architectural trade-off)
- **Consumer question:** "Should I lease or buy a mid-size sedan?" (personal financial decision)

For each, a 2-agent conversus deliberation (pragmatist + devils-advocate) produced a synthesis through 5 phases (review → cross-review → revision → disputes → synthesis). A single Claude response answered the same question directly.

A third question — "What is the capital of France?" — served as a negative control. Its synthesis correctly produced zero genuine disputes, confirming that agents don't manufacture disagreement on factual questions. That output is not compared here because it validates the *absence* of structural differentiation, which is the expected behavior for questions that don't warrant deliberation.

---

## Question 1: Monorepo vs Polyrepo

### Conversus Synthesis (key excerpts)

The synthesis contains a **Process Summary** tracking 15 Phase 1 recommendations across 2 agents, 1 withdrawal, 8 modifications, 4 new recommendations added in Phase 3, and 3 remaining disputes after Phase 4. It includes a **Recommendation Scorecard** tracing every recommendation through its lifecycle:

> | # | Agent | Recommendation | Phase 1 Priority | Phase 3 Disposition | Challenged By | Convergence | Final Status |
> |---|-------|---------------|-------------------|---------------------|---------------|-------------|--------------|
> | P-R3 | Pragmatist | Defer monorepo decision 3-6 months | P1 | Modified — bound to 30-day instrumentation mandate | DA cross-review (data vacuum) | Strong (principle); Disputed (timeline shape) | **ADOPTED (with instrumentation binding)** |
> | DA-R5 | Devil's Advocate | Evaluate "thin shared repo" middle path | P2 | Modified — scope narrowed to protos + buf only at launch | Pragmatist cross-review (mini-monorepo risk) | Strong (narrow scope converged) | **ADOPTED (narrow scope)** |

The synthesis then presents **Dangerous Contradictions Found** with resolution tracking (4 resolved, 2 unresolved), **Systemic Contradictions** identifying meta-patterns across individual disagreements, and **Convergence Achieved** with 7 positions ordered by agreement strength (Maximum → Strong → Moderate).

The **Remaining Disputes** section, delimited by `CONVERSUS:DISPUTES_BEGIN` / `CONVERSUS:DISPUTES_END` markers, contains 3 named disputes:

> **Dispute: Deferral Timeline Shape**
>
> **Positions:**
> - *Pragmatist:* Hard 3-month outer bound with a 6-8 week early checkpoint. Calendar date forces revisit even if data is ambiguous.
> - *Devil's Advocate:* 6-8 week validation window with explicit instrumentation. Data-triggered gates, no arbitrary deadline.

Each dispute includes a neutral **Synthesizer assessment** and **Recommended resolution**.

The **Key Concessions** section documents 9 position changes (4 by pragmatist, 5 by devils-advocate), each with a phase citation:

> **Pragmatist conceded:**
> 1. **Deferral must be bound to instrumentation.** Original position treated deferral (R3) and developer pain measurement (R7) as independent recommendations. Devil's Advocate's cross-review exposed this as creating a data vacuum. Pragmatist merged R7 into R3 as a binding precondition. *(DA cross-review DC§1 → Pragmatist revision R3, R7)*

### Single-Model Response (key excerpts)

The single-model response is a well-structured consultant analysis with a clear recommendation ("Consolidate into a monorepo. Use Bazel as your build orchestrator."), analysis of tradeoffs, an implementation plan, and risk factors. It is presented as a single authoritative voice:

> Your three services share a gRPC contract defined by 4 protobuf files. This is a tight coupling point — any schema change is inherently a cross-service change.

> **If Bazel's learning curve feels too steep for your current velocity pressure**, Turborepo is a reasonable second choice.

The response covers counterarguments (what polyrepo with better tooling would require, what monorepo costs) but these are weighed by the single author and resolved into a unified recommendation. There is no attribution of these counterarguments to distinct analytical perspectives, no tracking of which points were challenged or conceded, and no remaining disputes — the author has already resolved everything internally.

---

## Question 2: Lease vs Buy

### Conversus Synthesis (key excerpts)

The synthesis tracks 15 recommendations across 2 agents through 4 phases, with 13 converging and 4 remaining in dispute. The **Recommendation Scorecard** shows how positions evolved:

> | Recommendation | Pragmatist | Devil's Advocate | Status |
> |---|---|---|---|
> | Reframe flexibility as neutral early-exit cost | P2, modified | P1→modified | **Converged** — neutral framing, model both structures |
> | Mileage overage as model line item vs. footnote | Footnote at 13,500 | Model line item w/ asymmetry | **Disputed** |

The **Dangerous Contradictions Found** section documents 3 contradictions that were resolved through the deliberation process, each showing how agent positions that would have been incoherent if adopted together were reconciled:

> **1. Flexibility framing pointed in opposite directions.** The Pragmatist's original Recommendation 4 reframed flexibility to favor buying (early lease termination is expensive). The Devil's Advocate's original Recommendation 2 reframed flexibility to favor leasing (optionality premium is cheap insurance). If both had been adopted, the spec would simultaneously argue flexibility favors each side. **Resolved in revision:** both agents accepted neutral framing.

The **Remaining Disputes** contain 4 named disputes including:

> #### Dispute: Spec Directional Neutrality
>
> **Pragmatist position:** The asker's profile overwhelmingly favors buying on every historical TCO comparison. Stating this in the spec is honest prior information, not bias.
>
> **Devil's Advocate position:** A spec that requires a neutral cost model while telegraphing "buying is the expected answer" invites confirmation bias in the answering agent.

### Single-Model Response (key excerpts)

The single-model response opens with a clear recommendation ("Buy the car with a 60-month auto loan"), presents detailed financial analysis with cost tables, evaluates flexibility, maintenance, and the two-kids factor, and concludes with implementation recommendations.

Like the monorepo response, it considers counterarguments (leasing's lower monthly payments, warranty coverage, the one scenario where leasing wins on flexibility) but weighs them as a single voice and resolves them into a unified recommendation:

> The lease-vs-buy question generates a lot of debate, but that's usually because people's profiles differ. In your case, the profile is almost textbook "buy."

---

## Annotated Structural Differences

### Structural Difference 1: Agent Attribution with Phase-Level Traceability

**What conversus has:** Every recommendation in the synthesis is attributed to a named agent (pragmatist or devils-advocate) and tracked through phases. The Recommendation Scorecard shows who proposed each recommendation, at what priority, how it was modified in Phase 3, who challenged it, what convergence was reached, and the final status. Cross-reference citations like "(DA cross-review DC§1 → Pragmatist revision R3, R7)" create an audit trail from initial proposal through challenge to final disposition.

In the monorepo synthesis, 18 recommendations are individually attributed and tracked. The reader can see that Pragmatist R7 ("Instrument actual developer pain") was originally a standalone recommendation, was challenged by the Devil's Advocate in cross-review for creating a "deferral-instrumentation disconnect," and was then merged into R3 as a precondition during revision. This lifecycle is visible in the scorecard row.

In the lease synthesis, each recommendation shows its disposition per agent — "Pragmatist: P2, modified" vs "Devil's Advocate: P1→modified" — making it clear that agents initially disagreed on priority and both changed positions before converging.

**What single-model lacks (and why):** A single-model response has one author. It can present pros and cons, but it cannot attribute positions to distinct analytical perspectives that *independently* evolved their views through structured interaction. The single-model monorepo response mentions counterarguments ("Staying polyrepo and solving the schema problem means...") but these are the author's own anticipation of objections, not positions held and defended by a separate analytical agent. There is no lifecycle to trace — no point at which "the pro-polyrepo perspective" changed its mind about something.

**Why this matters for decision quality:** Attribution with phase traceability lets a decision-maker assess *how* conclusions were reached, not just what they are. When the monorepo synthesis says "Pragmatist conceded deferral must be bound to instrumentation," the reader knows this wasn't the original view — it was a position change caused by a specific challenge. This is stronger evidence than a single author who presents the bound-deferral as their recommendation without revealing that they initially thought otherwise. The traceability enables a reader to evaluate whether each position was genuinely stress-tested or merely acknowledged.

### Structural Difference 2: Explicit Disagreement with Named Opposing Positions

**What conversus has:** The synthesis contains formally structured disputes — sections delimited by `CONVERSUS:DISPUTES_BEGIN` / `CONVERSUS:DISPUTES_END` machine-parseable markers, each headed by `**Dispute: [Label]**`, each presenting two named agents' positions with their supporting arguments, a neutral synthesizer assessment, and a recommended resolution.

The monorepo synthesis contains 3 remaining disputes: "Deferral Timeline Shape," "Shared Repo Necessity and Scope," and "Migration Estimation Gap (4-8 Weeks vs. 3-4 Months)." Each presents genuinely incompatible positions. For instance, the migration estimation dispute surfaces a 2-4× gap (pragmatist: 4-8 weeks vs. devils-advocate: 3-4 months) with both agents agreeing on the resolution mechanism (benchmark spike) but disagreeing on the default assumption.

The lease synthesis contains 4 remaining disputes, including "Spec Directional Neutrality" where the pragmatist argues that stating buying is the likely answer is honest prior information, while the devils-advocate argues it invites confirmation bias. The synthesizer sides with the devils-advocate on structural grounds ("A spec that says 'compute the answer' while simultaneously saying 'the answer is buy' creates a validation exercise, not an analysis").

**What single-model lacks (and why):** A single-model response resolves all internal tensions before presenting its output. The single-model lease response acknowledges the tension between cost-optimization and monthly payment fit, but resolves it within the same paragraph: "Your budget is $400–500/month, and a lease fits neatly inside that range… The purchase loan at ~$573 overshoots. You have three ways to reconcile this." The author does not present two irreconcilable positions because the author is one mind — any internal disagreement is resolved before writing. There is no structural mechanism for a remaining dispute.

The single-model monorepo response does the same: it mentions polyrepo alternatives but frames them as inferior ("You'd be building internal tooling to compensate for the fact that your repos don't reflect your dependency structure"). A genuine dispute about whether a shared repo should exist at all (as in the conversus synthesis) is impossible when one author has already decided the answer.

**Why this matters for decision quality:** Disputes in a deliberation synthesis represent areas where the evidence genuinely supports multiple conclusions. By surfacing these as named, structured disagreements rather than resolving them behind the scenes, the reader can make informed decisions about which trade-offs they're willing to accept. The migration estimation gap (4-8 weeks vs. 3-4 months) in the monorepo synthesis is critical information for a team making a commit/defer decision — a single-model response that presents one estimate (and the single-model response says "3-5 weeks") conceals the genuine uncertainty.

### Structural Difference 3: Concession Tracking with Phase Citations

**What conversus has:** Both syntheses contain **Key Concessions** sections documenting where agents changed positions during the deliberation, with citations to the specific phase and section where the change occurred. The monorepo synthesis documents 9 concessions (4 pragmatist, 5 devils-advocate). The lease synthesis documents 9 concessions in a table with Agent, Concession, Phase, and Rationale columns.

For example, in the monorepo synthesis: "**Pragmatist conceded: Schema fix confidence should be testable, not assumed.** Originally presented the schema fix as near-certain. Accepted Devil's Advocate's challenge to treat it as a hypothesis with a 60-day validation window. *(DA cross-review Tension§5 → Pragmatist revision N1)*"

In the lease synthesis: "Devil's Advocate | Withdrew CPO as P1 recommendation | Revision | Accepted scope creep argument — the asker asked lease-vs-buy on new vehicles, not 'cheapest acquisition strategy.' Demoted to sidebar note."

**What single-model lacks (and why):** A single-model response cannot track concessions because there is no prior position to concede from. The single-model lease response recommends buying, addresses leasing's advantages, and concludes buying is better — but there is no record of the author initially considering leasing as a stronger option and then changing their mind based on evidence. The final output is the author's resolved view with no process history.

A single-model response might include a "counterarguments" section, but this is a rhetorical device — the author already knows where the argument will land. It is structurally different from a concession, which requires an independently-held prior position and a specific challenge that caused the change.

**Why this matters for decision quality:** Concessions are evidence of genuine deliberation. When the Devil's Advocate in the lease synthesis withdraws CPO as a P1 recommendation because it "constituted scope creep beyond the asker's stated question," the reader knows that a distinct analytical perspective proposed CPO, it was stress-tested, and the proposer agreed it didn't belong. This is stronger evidence that CPO was properly considered and correctly excluded than a single-model response that simply doesn't mention it (or mentions it briefly, as the single-model response does not).

### Structural Difference 4: Dangerous Contradiction Detection with Resolution Tracking

**What conversus has:** Both syntheses contain **Dangerous Contradictions Found** sections that identify positions that would have been incoherent or harmful if adopted together, categorized into resolved and unresolved contradictions. Each entry documents what the contradiction was, which agents held the conflicting positions, and how (or whether) it was resolved.

The monorepo synthesis identifies 6 dangerous contradictions, 4 resolved and 2 unresolved. For example: "**Shared repo scope collision** — Both agents proposed a fourth repository but with incompatible scope — one proto-only, the other including shared libraries and integration tests. If both were implemented, the team would create two overlapping shared repos." The resolution documents both agents' concessions and the resulting narrow scope.

The lease synthesis identifies 3 dangerous contradictions, all resolved: "**Flexibility framing pointed in opposite directions.** The Pragmatist's original Recommendation 4 reframed flexibility to favor buying. The Devil's Advocate's original Recommendation 2 reframed flexibility to favor leasing. If both had been adopted, the spec would simultaneously argue flexibility favors each side."

**What single-model lacks (and why):** A single-model response cannot produce dangerous contradictions because the same author writes every recommendation. The single-model monorepo response recommends a monorepo and mentions polyrepo tooling as an alternative — but these are presented as considered options, not as competing recommendations that could have been simultaneously adopted with incoherent results. The author pre-resolves any contradictions during writing.

**Why this matters for decision quality:** Dangerous contradiction detection is a form of adversarial robustness checking. The lease synthesis's contradiction about flexibility framing reveals that the *same evidence* (flexibility) was initially used to argue in both directions — information a decision-maker needs to evaluate whether "flexibility favors buying" is genuinely true or is a framing artifact. The single-model lease response simply states "Buying gives you more flexibility, not less" without revealing that a rigorous counterargument exists and was only resolved through structured revision.

### Structural Difference 5: Convergence Strength Assessment

**What conversus has:** Both syntheses contain **Convergence Achieved** sections that list positions where agents reached agreement, ordered by strength. The monorepo synthesis assigns explicit strength labels: "Maximum" (both agents' #1, unchallenged across 4 phases), "Strong" (independently arrived at, survived challenge), and "Moderate" (framework agreed but specific details require calibration).

For example: "**Deploy schema compatibility checks immediately.** Both agents' highest-priority recommendation, independently proposed with identical tool choice, timeline (1-3 days), and rationale. Neither agent challenged any aspect of this recommendation across four phases. *Strength: Maximum.*"

Versus: "**Shared repo scope should start narrow.** Emerged from cross-review collision between the two agents' shared-repo proposals. Note: Devil's Advocate later disputed whether the narrow shared repo solves any problem buf-in-CI doesn't already address — the convergence on scope masks residual divergence on necessity. *Strength: Moderate (scope agreed; necessity disputed).*"

**What single-model lacks (and why):** A single-model response presents all its recommendations as the author's confident conclusions. There is no mechanism to distinguish between a recommendation the author is highly confident about (analogous to Maximum convergence — two independent perspectives arrived at the same conclusion) and one the author recognizes as debatable (analogous to Moderate convergence with residual disputes). The single-model monorepo response recommends Bazel as the build orchestrator with the same structural confidence as it recommends deploying schema checks — but in the conversus synthesis, these have very different convergence strengths.

**Why this matters for decision quality:** Convergence strength is a confidence signal. A recommendation with Maximum convergence (independently proposed by agents with different analytical frames, unchallenged through 4 phases) is more robust than one with Moderate convergence (agreed on framework but disputed on specifics). A decision-maker reading the conversus synthesis can allocate scrutiny accordingly — deploy the schema checks with high confidence, but probe the shared repo recommendation more carefully. The single-model response provides no such differentiation.

### Structural Difference 6: Machine-Parseable Structural Markers

**What conversus has:** The synthesis contains `<!-- CONVERSUS:DISPUTES_BEGIN -->` and `<!-- CONVERSUS:DISPUTES_END -->` HTML comment markers that delimit the disputes section. Each dispute is headed with `**Dispute: [Label]**`. The Recommendation Scorecard uses a consistent table format with columns for Agent, Phase 1 Priority, Phase 3 Disposition, Challenged By, Convergence, and Final Status.

These markers enable automated downstream processing: a quality checker can programmatically detect whether disputes exist, count them, verify that each contains positions from 2+ agents, and assess whether the deliberation produced genuine disagreement.

**What single-model lacks (and why):** A single-model response has no need for machine-parseable multi-agent markers because there is only one perspective. While a single-model response might use structured markdown (tables, headers), these structural elements represent the author's organizational choices, not a multi-perspective deliberation protocol. There is nothing to parse for a quality checker that needs to verify "two or more distinct perspectives engaged with each other."

**Why this matters for decision quality:** Machine-parseable markers are the prerequisite for automated quality assurance. They allow a system to verify, without human review, that a deliberation actually produced the structural properties it claims — multiple perspectives, explicit disagreements, tracked dispositions. This is the foundation for the S02 quality checker that will programmatically validate conversus output quality.

---

## Quality Floor Assessment

**Result: PASS.** The 2-agent cooperative deliberation produces output that is structurally differentiated from a single-model response across 6 identified dimensions. The differences are not stylistic — they represent structural properties that are impossible in a single-author response:

1. **Agent attribution with phase-level traceability** — requires multiple independent agents whose positions are tracked across interaction phases
2. **Explicit disagreement with named opposing positions** — requires agents who can hold and defend incompatible positions simultaneously
3. **Concession tracking with phase citations** — requires agents who changed their positions in response to specific challenges
4. **Dangerous contradiction detection with resolution tracking** — requires multiple recommendations from different agents that were checked for coherence
5. **Convergence strength assessment** — requires independent perspectives arriving at agreement (or failing to) through structured interaction
6. **Machine-parseable structural markers** — requires a multi-agent protocol with formal delimiters

The negative control (factual-capital question "What is the capital of France?") correctly produced zero genuine disputes, confirming that agents don't manufacture disagreement. This validates the specificity of the structural differences — they appear when genuine analytical tension exists and are absent when it doesn't.

The product premise — that multi-agent deliberation produces structurally differentiated output that single-model responses cannot replicate — is empirically validated by these results.
