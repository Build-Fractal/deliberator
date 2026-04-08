# Game-Theorist Review: 013 Objective Function Templates

**Reviewer**: game-theorist
**Spec**: `013-objective-function-templates`
**Date**: 2026-03-23
**Verdict**: Largely sound mathematical framework with several structural misalignments between game forms and template semantics, and some missing standard forms that would strengthen the library.

---

## Executive Summary

The objective function template library defines a well-organized set of parameterized mathematical forms spanning four deliberation modes. The core mathematical expressions are dimensionally consistent and the penalty/reward structures correctly encode the intended incentives. However, several game form assignments contradict the mathematical structure of the templates they reference, the mode-to-form mapping file contradicts actual template assignments in a significant case (red-blue), and the library omits standard game-theoretic forms that are natural fits for the stated modes. The Pydantic validation layer is clean but does not enforce the structural compatibility between an objective's mathematical form and its declared game form, which is the primary gap.

---

## Alignment

### A1. Cooperative objectives correctly use GNEP with coupled constraints

The three cooperative-specific templates (`cooperative-integration`, `cooperative-quality`, `cooperative-consensus`) and `cooperative-fairness` all declare `game_form: gnep`. This is the correct choice. In each case, agents optimize individual objectives (accepted_recs, quality_score, agreement_rate, min allocation) subject to shared constraints (document convergence, revision budgets, consensus thresholds, total allocation pools). The GNEP form explicitly models exactly this structure: `J_i(x_i, x_{-i})` with coupled constraints `h(x_1, ..., x_N) <= 0`. The constraint references (budget, capacity, non-negativity, bounds) all map naturally to GNEP coupled or local constraints. This is textbook.

### A2. Penalty-based objective forms are mathematically standard scalarizations

The `J = -benefit + lambda * cost` pattern used throughout cooperative and prisoners-dilemma templates is a standard Lagrangian relaxation / penalty method form. Minimizing `J` simultaneously maximizes the benefit term and minimizes the cost term, with the penalty weight controlling the tradeoff. The sign conventions are consistent: benefits are negated (since we minimize J), penalties are added with positive weights. This is correct and standard in multi-objective optimization literature.

### A3. Winner-take-all templates correctly use normal-form games

The `competitive-selection`, `competitive-ranking`, and `competitive-threshold` templates all declare `game_form: normal-form`. For simultaneous-move competitions where agents submit proposals and receive payoffs based on the joint strategy profile, normal form is the appropriate representation. The mutual-exclusivity constraint (`sum(x_i) = 1`) correctly encodes the "exactly one winner" structure. The overlap penalty in `competitive-selection` elegantly models the anti-coordination incentive that is standard in congestion/differentiation games.

### A4. Risk-adversarial templates correctly use Stackelberg form

The three red-blue templates (`risk-adversarial`, `risk-severity`, `risk-coverage`) all declare `game_form: stackelberg`. This correctly models the sequential nature of red-blue deliberation: red team commits to an attack strategy (leader), blue team observes and responds (follower). The leader-follower hierarchy matches the Stackelberg schema's `leader`/`followers` field structure. The separate objective functions `J_red` and `J_blue` map naturally to the Stackelberg schema's `leader_objective` and `follower_objectives` fields.

### A5. Cross-mode templates use parametric form appropriately

The cross-mode templates (`budget-constrained`, `time-constrained`, `weighted-sum`, `minimax`, `lexicographic`, `general-quadratic`, `general-linear`) all declare `game_form: parametric`. This is appropriate because these templates introduce external parameters (beta, tau, weights, Q, p) that are not optimized by any player but shape the objective landscape. The parametric game form explicitly models this: `J_i(x_i, x_{-i}; p)` where `p` is the external parameter vector. Using parametric as the default for mode-agnostic templates is a sound design choice.

### A6. Constraint templates are mathematically complete for the declared objectives

The six constraint templates (budget, capacity, mutual-exclusivity, minimum-coverage, non-negativity, bounds) cover the standard constraint types encountered in the template library: linear inequality (`<=`, `>=`), equality (`= 1`), and box constraints. Each template's `form` field uses standard mathematical notation. The constraint-to-template assignments are sensible: territory templates use capacity (total territory cannot exceed artifact scope), competitive templates use mutual-exclusivity (one winner), and budget constraints apply to cost-aware objectives.

---

## Missed Opportunities

### M1. No Nash bargaining or Nash social welfare function for cooperative mode

The cooperative templates model individual agent incentives with penalty-based scalarizations. But the standard game-theoretic approach for cooperative negotiation is the Nash Bargaining Solution (NBS): `max prod_i (u_i - d_i)` where `d_i` is agent i's disagreement payoff. This is missing entirely. For cooperative deliberations where agents negotiate over outcomes, NBS provides the unique fair and efficient solution satisfying axioms of symmetry, Pareto optimality, independence of irrelevant alternatives, and invariance to affine transformations. A `cooperative-nash-bargaining` template with form `J = -prod_i(utility_i - disagreement_i)` would fill this gap and is arguably the most important cooperative game theory form.

### M2. No explicit potential game / congestion game form for prisoners-dilemma

The prisoners-dilemma territory templates model agents competing for shared resources, which is precisely the structure of a congestion game (a subclass of potential games). In congestion games, agents share resources and each agent's cost depends on the number of agents using the same resource. The key property is that a potential function `Phi(x)` exists such that unilateral deviations change `Phi` by exactly the change in the deviating player's objective. This guarantees existence of pure-strategy Nash equilibria via the potential function. A `territory-potential` template with form `J_i = sum_r c_r(n_r) * x_{i,r}` (where `c_r` is the congestion cost on resource r and `n_r` is the number of agents using r) would provide a well-studied alternative to the penalty-based territory forms and would guarantee equilibrium existence.

### M3. No epsilon-constraint method for multi-objective templates

The library includes weighted-sum, minimax, and lexicographic scalarization methods but omits the epsilon-constraint method, which is standard in multi-objective optimization: `min f_1(x) s.t. f_k(x) <= epsilon_k for k >= 2`. Unlike weighted-sum, this method can find Pareto-optimal points on non-convex portions of the Pareto front. The spec's weighted-sum template description correctly notes this limitation ("only finds Pareto-optimal points on convex portions") but does not provide the complementary method. An `epsilon-constraint` template would complete the standard scalarization toolkit.

### M4. No Kalai-Smorodinsky bargaining solution for fairness

The `cooperative-fairness` template uses a Rawlsian maximin criterion combined with variance penalty. While this is a valid fairness concept, the Kalai-Smorodinsky (KS) bargaining solution is a major alternative that the library omits. KS maximizes utility proportional to each agent's ideal gain: `u_i / (u_i^* - d_i)` is equalized across agents, where `u_i^*` is agent i's ideal point. This provides a different fairness notion that respects the relative potential of each agent, which is relevant when agents have different capability ranges. A `cooperative-kalai-smorodinsky` template would give users a principled choice between egalitarian (Rawlsian) and proportional (KS) fairness.

### M5. No Bayesian game or incomplete information form

All templates assume complete information: each agent knows the other agents' objectives and parameters. But many conversus deliberations operate under incomplete information -- agents do not know each other's evaluation criteria, cost structures, or quality functions until cross-review reveals them. A Bayesian game form (or at least a Bayesian-compatible template) would model this: agents have types drawn from a prior distribution, and the objective depends on the type profile. This is especially relevant for prisoners-dilemma mode where the "dilemma" partly arises from not knowing whether the other agent will cooperate or defect.

### M6. No mechanism design / incentive compatibility constraint

The templates define agent objectives but do not address whether the resulting game has truthful reporting as an equilibrium strategy. In conversus, agents are asked to honestly report capabilities, risks, and assessments. A mechanism design perspective would add an incentive compatibility constraint: `J_i(true_report, x_{-i}) <= J_i(s_i, x_{-i})` for all s_i, ensuring that truthful reporting is a dominant strategy. This is particularly important for the prisoners-dilemma mode where the README explicitly states that "the Nash equilibrium is honest, well-evidenced advocacy." An `incentive-compatibility` constraint template would formalize this.

### M7. No regret-based or online learning objective for iterative deliberations

The templates model static games (single-shot or fixed-round). But conversus deliberations are inherently iterative (multiple revision rounds). Standard online optimization theory uses regret-based objectives: `min sum_t l_t(x_t)` or `min max_t l_t(x_t)` where the objective adapts across rounds. A `regret-minimization` template would model the dynamic aspect of deliberation where agents learn from cross-review feedback and adapt their strategies over rounds.

### M8. Variance-of-allocation in cooperative-fairness lacks a standard normalization

The `cooperative-fairness` form `J = -min_i(allocation_i) + phi * variance(allocation)` combines a Rawlsian maximin term (units of allocation) with a variance term (units of allocation-squared). These are dimensionally incompatible, making phi's interpretation scale-dependent. The standard approach is to use the coefficient of variation (variance / mean^2) or Gini coefficient instead of raw variance, or to explicitly normalize both terms. This should be documented or the form should be adjusted.

### M9. The `boundary-negotiation` form sign convention is internally inconsistent

The form is `J = -boundary_violations + sigma * clarity`. Since J is minimized, this maximizes boundary_violations (the negated term drives J lower) and maximizes clarity (the positive term also drives J lower when sigma > 0... no, it drives J higher). Wait -- let me re-examine. If we minimize J: minimizing `-boundary_violations` means maximizing `boundary_violations`, which is wrong. The intended behavior is to minimize violations and maximize clarity. The correct form for minimization should be `J = boundary_violations - sigma * clarity` (penalize violations, reward clarity). The current form has the signs reversed compared to its stated intent.

---

## Off-Base Assumptions

### O1. Mode-to-form mapping says red-blue defaults to GNEP, but all red-blue templates use Stackelberg

The `mode-mapping.yml` file declares `red-blue: form: gnep`, but all three red-blue templates (`risk-adversarial`, `risk-severity`, `risk-coverage`) use `game_form: stackelberg`. This is a direct contradiction. The templates are correct -- red-blue deliberation has a natural leader-follower structure (red team attacks first, blue team responds), which is Stackelberg, not GNEP. GNEP models simultaneous optimization with coupled constraints, which does not capture the sequential commitment structure of red-blue. The mode-mapping.yml should be updated to `red-blue: form: stackelberg`, or at minimum acknowledge Stackelberg as the primary form for this mode. The current note in mode-mapping.yml ("the two teams optimize opposing objectives subject to shared constraints") is describing a zero-sum GNEP, which is a different game than what the templates actually implement.

### O2. competitive-ranking uses rank_position as a function-type parameter but ranking is inherently endogenous

The `competitive-ranking` template defines `rank_position` as a function-type parameter with `derived_from: "evaluation rubric rank ordering"`. But rank is not exogenous to the game -- it is an outcome of the joint strategy profile. Agent i's rank depends on all agents' scores, making it `rank_i(x_i, x_{-i})`. Treating rank as a `derived_from` artifact suggests it is computed outside the game, which breaks the strategic structure. In the normal-form game this template references, rank should emerge from the payoff matrix, not be supplied as an input. This creates a conceptual circularity: the rank determines the objective, but the objective determines the strategy, which determines the rank. The template should either (a) define the objective in terms of the underlying score (not rank) and let rank be a derived outcome, or (b) acknowledge that this is a mechanism design problem where the ranking rule is an exogenous mechanism parameter.

### O3. The `false_positive_penalty` in risk-adversarial modifies the red team objective but is not reflected in the declared form

The `risk-adversarial` template declares `form: "J_red = -confirmed_risks; J_blue = -mitigated"` but defines a `false_positive_penalty` parameter that penalizes red team for failed confirmations. The actual objective for red team is `J_red = -confirmed_risks + false_positive_penalty * failed_claims`, which is different from the declared form. The declared form is incomplete. This matters because the false_positive_penalty fundamentally changes the game's equilibrium structure: without it, red team has a dominant strategy of claiming everything; with it, red team must trade off precision vs. recall. The form field should reflect the actual objective.

### O4. Budget-constrained and time-constrained forms use `J = quality - beta * cost` (maximization convention) while mode-specific templates use `J = -benefit + penalty` (minimization convention)

The cross-mode templates `budget-constrained` and `time-constrained` write `J = quality - beta * agent_cost` and `J = quality - tau * rounds_used`. In a minimization framework, this would maximize cost and minimize quality -- the opposite of the intent. The mode-specific templates consistently use the minimization convention: `J = -benefit + lambda * penalty` (negate the thing you want to maximize, add the thing you want to minimize). The cross-mode templates appear to use a maximization convention instead. This inconsistency will cause confusion or bugs when templates are consumed programmatically. All templates should use the same optimization direction, and the spec should explicitly declare whether J is minimized or maximized (standard in optimization: minimize).

---

## Actionable Recommendations

### R1. Fix the sign convention inconsistency across templates (CRITICAL)

Establish a single convention (minimization is standard) and apply it consistently:
- Mode-specific templates: already use `J = -benefit + penalty` (minimize J). Correct.
- `budget-constrained`: change to `J = -quality + beta * agent_cost`
- `time-constrained`: change to `J = -quality + tau * rounds_used`
- `boundary-negotiation`: change to `J = boundary_violations - sigma * clarity`

Add a note to the spec or a `convention` field to each template declaring "minimize" or "maximize".

### R2. Fix the mode-mapping.yml contradiction for red-blue

Update `mode-mapping.yml` to declare `red-blue: form: stackelberg` (or `red-blue: form: stackelberg | gnep` with a note). The current `gnep` assignment contradicts all three red-blue templates. Alternatively, add a `default_override` concept to the mapping to acknowledge that templates may use a different form than the mode default, but the simplest fix is to correct the mapping.

### R3. Update the risk-adversarial form to include the false_positive_penalty

Change the declared form from:
```
form: "J_red = -confirmed_risks; J_blue = -mitigated"
```
to:
```
form: "J_red = -confirmed_risks + false_positive_penalty * failed_claims; J_blue = -mitigated"
```
This makes the form field an accurate representation of the actual objective and makes the precision-recall tradeoff visible at the schema level.

### R4. Add a Nash Bargaining Solution template for cooperative mode

Create `cooperative-nash-bargaining.yml`:
```yaml
name: cooperative-nash-bargaining
form: "J = -prod_i(utility_i - disagreement_i)"
game_form: gnep
mode_compatibility: [cooperative]
parameters:
  - name: utility
    type: function
    derived_from: "synthesis recommendation scorecard"
  - name: disagreement
    type: function
    derived_from: "no-agreement baseline outcome"
```
This is the most important missing cooperative game theory form and provides the axiomatic solution to cooperative bargaining.

### R5. Add an epsilon-constraint template for multi-objective optimization

Create `epsilon-constraint.yml`:
```yaml
name: epsilon-constraint
form: "J = f_1(x) s.t. f_k(x) <= epsilon_k for k >= 2"
game_form: parametric
mode_compatibility: [cooperative, winner-take-all, prisoners-dilemma, red-blue]
parameters:
  - name: primary_objective
    type: function
  - name: secondary_objectives
    type: function
  - name: epsilon
    type: string
    description: "Upper bounds for secondary objectives"
```
This complements weighted-sum by finding Pareto-optimal points on non-convex Pareto fronts.

### R6. Add an explicit optimization direction field to the ObjectiveTemplate model

Add `optimization_direction: Literal["minimize", "maximize"]` to the `ObjectiveTemplate` Pydantic model with default `"minimize"`. This eliminates the sign convention ambiguity and allows the guided construction pipeline to handle templates uniformly. The Pydantic validator should then check that the form's sign conventions are consistent with the declared direction.

### R7. Resolve the endogeneity problem in competitive-ranking

Either (a) rewrite the objective in terms of the underlying score rather than the rank: `J = -score` (where rank is derived post-hoc), or (b) add a `mechanism` field to the template schema that defines the ranking rule as an exogenous mechanism parameter, separating the "how ranks are computed" question from the "what agents optimize" question. Option (a) is simpler and more standard.

### R8. Fix the dimensional inconsistency in cooperative-fairness

Replace raw variance with a dimensionless measure. Options:
- Coefficient of variation: `J = -min_i(allocation_i) + phi * cv(allocation)` where `cv = std / mean`
- Gini coefficient: `J = -min_i(allocation_i) + phi * gini(allocation)`
- Normalized variance: `J = -min_i(allocation_i) / total_pool + phi * variance(allocation) / total_pool^2`

Any of these makes phi's interpretation independent of the allocation scale.

### R9. Add a `form_complete` or `form_includes_all_terms` validator to the Pydantic model

Add a cross-field validator that warns (or errors) when parameters define terms not present in the `form` field. This would have caught the `false_positive_penalty` gap in `risk-adversarial` (the parameter exists but the form does not reference it). Implementation: extract parameter names from the `form` string and check that all non-string, non-default parameters have a corresponding token in the form.

### R10. Add an incentive-compatibility constraint template

Create `constraints/incentive-compatibility.yml`:
```yaml
name: incentive-compatibility
form: "J_i(true_type_i, x_{-i}) <= J_i(reported_type_i, x_{-i}) for all i, reported_type_i"
parameters:
  - name: true_type
    type: function
    description: "Agent's true capability/assessment"
  - name: reporting_space
    type: string
    description: "Set of possible reports an agent can make"
mode_compatibility: [cooperative, prisoners-dilemma]
```
This formalizes the truthful-reporting incentive that the README describes as central to prisoners-dilemma mode and would be the first mechanism design element in the constraint library.

---

## Referenced Documentation

| Document | Path | Relevance |
|---|---|---|
| Spec 013 | `conversus/specs/013-objective-function-templates/spec.md` | Primary spec under review |
| cooperative-integration.yml | `conversus/schema/objective-functions/cooperative-integration.yml` | Sign convention reference, GNEP alignment |
| competitive-selection.yml | `conversus/schema/objective-functions/competitive-selection.yml` | Normal-form alignment |
| territory-claiming.yml | `conversus/schema/objective-functions/territory-claiming.yml` | GNEP for PD mode |
| risk-adversarial.yml | `conversus/schema/objective-functions/risk-adversarial.yml` | Stackelberg alignment, form incompleteness |
| risk-severity.yml | `conversus/schema/objective-functions/risk-severity.yml` | Stackelberg alignment |
| risk-coverage.yml | `conversus/schema/objective-functions/risk-coverage.yml` | Stackelberg alignment |
| weighted-sum.yml | `conversus/schema/objective-functions/weighted-sum.yml` | Parametric alignment |
| minimax.yml | `conversus/schema/objective-functions/minimax.yml` | Parametric alignment |
| lexicographic.yml | `conversus/schema/objective-functions/lexicographic.yml` | Parametric alignment |
| cooperative-fairness.yml | `conversus/schema/objective-functions/cooperative-fairness.yml` | Dimensional inconsistency |
| cooperative-consensus.yml | `conversus/schema/objective-functions/cooperative-consensus.yml` | GNEP alignment |
| budget-constrained.yml | `conversus/schema/objective-functions/budget-constrained.yml` | Sign convention mismatch |
| time-constrained.yml | `conversus/schema/objective-functions/time-constrained.yml` | Sign convention mismatch |
| boundary-negotiation.yml | `conversus/schema/objective-functions/boundary-negotiation.yml` | Sign reversal bug |
| competitive-ranking.yml | `conversus/schema/objective-functions/competitive-ranking.yml` | Endogeneity problem |
| budget constraint | `conversus/schema/objective-functions/constraints/budget.yml` | Constraint template review |
| mode-mapping.yml | `conversus/schema/game-forms/mode-mapping.yml` | Red-blue contradiction |
| GNEP schema | `conversus/schema/game-forms/gnep.yml` | Game form reference |
| normal-form schema | `conversus/schema/game-forms/normal-form.yml` | Game form reference |
| stackelberg schema | `conversus/schema/game-forms/stackelberg.yml` | Game form reference |
| parametric schema | `conversus/schema/game-forms/parametric.yml` | Game form reference |
| objectives.py | `conversus/conversus/schemas/objectives.py` | Pydantic validation model |
| README.md | `conversus/README.md` | Mode semantics, PD truthfulness claim |
