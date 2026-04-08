# Game-Theorist Cross-Review of Schema-Engineer Review
# Spec 013: Objective Function Templates

**Cross-reviewer**: game-theorist
**Reviewing**: schema-engineer's review of spec 013
**Date**: 2026-03-23

---

## Dangerous Contradictions

### DC-1: Schema-engineer's R-4 example cross-validation would break the boundary-negotiation and budget-constrained templates as authored

Schema-engineer recommends (R-4, M-4) adding a validator that rejects example keys not present in the `parameters` list. This sounds safe in isolation, but the game-theorist's review surfaces a deeper problem: the `boundary-negotiation` template has a sign-convention bug (game-theorist O4, R1) and the `budget-constrained`/`time-constrained` templates use an internally inconsistent maximization convention (game-theorist O4). If R-4 is applied before R1/R3 fix the underlying YAML, the validator will tighten the contract around *incorrect* content — making it harder to correct the mathematical errors because any fix to the form expression would also require a simultaneous fix to the example keys or the validator will reject the corrected template. The sequencing matters: mathematical correctness (form expressions, sign conventions) must precede schema tightening (example key validation). Applying schema-engineer's R-4 first does not prevent the mathematical bugs; it cements them behind a passing validator.

**Implication**: R-4 should be explicitly gated behind resolution of game-theorist R1 (sign convention normalization) and R3 (risk-adversarial form completeness). Otherwise the schema silently validates templates that compute the wrong equilibria.

---

### DC-2: Schema-engineer's R-2 VALID_CONSTRAINTS frozenset would statically forbid the incentive-compatibility constraint that game-theorist R10 proposes adding

Schema-engineer recommends (R-2, M-2) a closed `VALID_CONSTRAINTS` frozenset encoding exactly the six current constraint names: `{"budget", "capacity", "mutual-exclusivity", "minimum-coverage", "non-negativity", "bounds"}`. Game-theorist R10 proposes adding a seventh constraint template, `incentive-compatibility`, which is essential for the prisoners-dilemma mode's truthful-reporting guarantee (game-theorist M6). Under schema-engineer's frozenset, any template referencing `incentive-compatibility` would immediately raise a `ValidationError` — before the constraint file even exists. This is precisely backwards: the schema would need to be updated before a new constraint template can be authored and committed, creating a rigid deployment dependency between the Pydantic model and the YAML library. The issue is not whether referential integrity checking is desirable (it is) but whether a *closed* frozenset is the right mechanism for a library explicitly described as extensible (spec Section 1: "Community contributions come later"). An open validation strategy — check that referenced constraints resolve to a file on disk — is referentially complete without blocking library growth. Schema-engineer's M-2 itself acknowledges the spec word "references" implies referential integrity, which file-existence checks satisfy without the extensibility tax.

**Implication**: R-2 as written creates a maintenance coupling between the Pydantic model and the constraint library that would block every game-theorist extension proposal. The frozenset approach should be replaced with a file-existence check tied to the actual `constraints/` directory contents.

---

### DC-3: Schema-engineer's R-6 adding a boolean type would resolve game-theorist O4's sign-convention confusion for normalize parameters, but schema-engineer frames this as a low-priority cosmetic fix rather than a correctness issue

Schema-engineer flags the `normalize` boolean-as-string encoding (M-8, R-6) as a "parsing burden" and rates the fix "Low. Only affects two parameters." Game-theorist's O4 demonstrates that the `budget-constrained` and `time-constrained` templates use `J = quality - beta * cost` in what is structurally a maximization framework while all mode-specific templates use a minimization convention. The `normalize` parameter in `weighted-sum` controls whether the weights are normalized before application. If `normalize` is parsed as a string and a downstream consumer misreads `"true"` as truthy (in Python, `bool("false") is True`), the normalization step silently changes the game's equilibrium. This is not a cosmetic type-system gap; it is a correctness hazard. Schema-engineer's R-6 is right to propose the fix but wrong about its priority: the combination of string-encoded booleans and a mixed maximization/minimization convention creates a compounding error surface. Both reviews underweight this risk.

**Implication**: R-6 (boolean type) should be elevated to Medium priority and explicitly linked to the sign-convention normalization in game-theorist R1. The two fixes together eliminate a class of silent misinterpretation bugs.

---

### DC-4: Schema-engineer's R-9 form_complete validator (proposed in schema-engineer's R-10 / game-theorist's R-9) requires that parameter names appear as tokens in the form string, but this conflicts with the `derived_from` abstraction for function-type parameters

Game-theorist R-9 proposes a validator that checks all non-default parameters appear as tokens in the `form` field. This caught the `false_positive_penalty` gap in `risk-adversarial` (game-theorist O3). Schema-engineer's review does not propose this validator explicitly but does propose (M-4, R-4) cross-validating example keys against parameter names. Combined, the two approaches converge on a tighter linking between form, parameters, and examples. However, function-type parameters (schema-engineer A-2) use `derived_from` rather than a literal value in the form: for example, `rank_position` in `competitive-ranking` has `derived_from: "evaluation rubric rank ordering"` but does not appear as a syntactic token in the form expression in the way `lambda` or `beta` do. A naive token-matching validator would either generate false positives for function-type parameters (rejecting valid templates) or require special-casing that undermines the validator's value. This tension is not visible in either review in isolation. Game-theorist O2 identifies the deeper issue: `rank_position` is endogenous to the game, which means its appearance in the form string is conceptually problematic regardless of the validator's implementation. The two reviewers' proposals interact in a way that neither fully resolves.

**Implication**: Any form-completeness validator must exclude function-type parameters from the token-presence check, or else separately validate that function-type parameter names appear only in the `derived_from` field, not as literal form tokens. This design decision should be explicit in the Pydantic model.

---

## Tensions

### T-1: Schema-engineer wants a tighter, more constrained schema; game-theorist wants a richer, more expressive library — these goals pull in opposite directions on the `example` field

Schema-engineer's R-3 and R-4 push toward a flat, rigid `example` format (parameter-name-to-value mapping only, no nested structure, no `computed_objective` annotation). Game-theorist's R4 proposes a Nash Bargaining Solution template whose example would include `utility` and `disagreement` as function-type parameters with no concrete numeric values — only `derived_from` strings. Under schema-engineer's proposed example format, a function-type parameter cannot be meaningfully represented as a key-value pair (what value do you supply for a function?). The schema-engineer's O-2 even notes that `dict[str, Any]` with a default of an empty dict is "too loose," but the game-theorist's proposed templates structurally require looseness in the example field for function-type parameters. The tension is real: schema tightening on `example` is appropriate for scalar parameters and harmful for function-type parameters. A two-field solution — `example` for scalar parameterizations and `example_note` for function-type descriptions — would satisfy both reviewers, but neither proposes it explicitly.

---

### T-2: Schema-engineer's referential integrity recommendations assume a static library; game-theorist's extension proposals assume a dynamic one

Schema-engineer's M-2 (VALID_CONSTRAINTS frozenset), R-2 (static validation), and R-10 (extra="forbid" on all models) collectively treat the template library as a closed set that is fully known at model-definition time. Game-theorist's M1-M7 propose adding Nash bargaining, epsilon-constraint, Kalai-Smorodinsky, Bayesian game, mechanism design, and regret-minimization templates — six new templates across objective and constraint files. These additions would require updating the frozenset, relaxing extra="forbid" for any new fields, and revalidating all existing templates after each addition. The spec itself is ambiguous: Section 1 says "Community contributions come later" (implying the library will grow) but the v1 framing and the "curated and mathematically validated" requirement (Section 1) support the schema-engineer's closed-set approach for v1. This is a genuine design philosophy tension, not a bug. Resolution requires a decision: is the Pydantic model a v1 snapshot validator or an extensible registry validator? The answer determines which review's approach is correct.

---

### T-3: Schema-engineer's M-9 proposes a load_objective_template() utility; game-theorist's R2 requires updating mode-mapping.yml — these touch the same loading path with different assumptions

Schema-engineer's M-9 and R-7 propose a `load_objective_template()` utility that reads YAML files from a directory and validates them against the Pydantic model. Game-theorist's R2 requires updating `mode-mapping.yml` to correct the red-blue/GNEP contradiction. If the loader utility is implemented as proposed (mirroring `load_mode_mapping()`) before the mode-mapping correction, it will load and validate a contradictory mapping without error — because the current Pydantic models do not cross-validate the `game_form` field in a template against the `mode-mapping.yml` declaration for that template's compatible modes. This is a gap both reviews identify but neither connects: schema-engineer's M-2 proposes referential integrity for constraint names; game-theorist's O1 identifies the mode-mapping contradiction; but neither proposes cross-validating template `game_form` assignments against the mode-mapping file. A loader utility that does this cross-validation would catch the red-blue contradiction at parse time.

---

### T-4: Schema-engineer's extra="forbid" recommendation (R-10) conflicts with the game-theorist's R6 proposal to add an optimization_direction field to ObjectiveTemplate

Schema-engineer R-10 proposes `model_config = ConfigDict(extra="forbid")` on all three models to reject unknown YAML keys. Game-theorist R6 proposes adding `optimization_direction: Literal["minimize", "maximize"]` to `ObjectiveTemplate`. If extra="forbid" is applied before the new field is added to the model, every existing YAML template would need to be updated to include `optimization_direction` before the extra="forbid" validator is enabled — otherwise existing templates would fail validation because they lack the new required field. This is a sequencing dependency, not a fundamental contradiction, but both reviews advocate their respective changes as independent improvements without acknowledging the coordination requirement.

---

### T-5: Game-theorist's M8 identifies a dimensional inconsistency in cooperative-fairness; schema-engineer's M-7 identifies string-typed parameters masking numeric structure — both point to the same underlying type system weakness but propose incompatible resolutions

Schema-engineer M-7 flags `weights`, `Q`, and `tolerance` as string-typed parameters encoding numeric arrays. Schema-engineer frames this as a limitation of the four-type system and recommends leaving it for downstream consumers to handle (no explicit fix proposed). Game-theorist M8 flags `cooperative-fairness` as dimensionally inconsistent (allocation units vs. allocation-squared units in the same expression). Game-theorist R8 proposes fixing the *form* by substituting a dimensionless measure. But the fix to the form changes the parameter types: a coefficient of variation or Gini coefficient requires different parameter structures than raw variance. If schema-engineer's type system limitation is left unresolved while the form is corrected per game-theorist R8, the corrected form may require new parameter types (e.g., `phi` would now multiply a dimensionless Gini coefficient, which itself requires knowing the mean and distribution of allocations). The two issues are coupled: fixing the form is incomplete without also expanding the type system or adding a structured parameter for the normalization factor.

---

## Safe Agreements

### SA-1: Both reviews independently confirm that the core mathematical structure is sound and correctly implemented

Schema-engineer A-1 through A-6 verify that the Pydantic models correctly enforce the four-type parameter system, function-type derived_from invariant, mode_compatibility validation, game_form membership, range-default consistency, and cardinality requirements. Game-theorist A1 through A6 verify that cooperative templates correctly use GNEP, winner-take-all templates correctly use normal-form, red-blue templates correctly use Stackelberg, and cross-mode templates correctly use parametric form. Neither review found fundamental errors in the mathematical structure of the core template library. The alignment sections are mutually reinforcing: schema-engineer confirms the model enforces the rules correctly; game-theorist confirms the rules themselves encode the right game-theoretic concepts.

---

### SA-2: Both reviews identify the FR-011 import path discrepancy as a concrete, unambiguous bug requiring immediate resolution

Schema-engineer O-1 and R-8 identify that `from conversus_schemas.objectives import ...` (as FR-011 requires) will raise an `ImportError` because the actual package is named `conversus` not `conversus_schemas`. Game-theorist's review does not independently flag this (it is outside the mathematical scope), but it does not contradict it either. Schema-engineer's R-8 correctly identifies that option (b) — amending FR-011 to match the actual import path — is lower-risk than renaming the package, given that spec 012's implementation already established the `conversus.schemas` namespace. This is a clean, uncontested finding with a clear resolution path that does not interact with any game-theorist concerns.

---

### SA-3: Both reviews implicitly agree that the red-blue contradiction (mode-mapping.yml vs. template game_form assignments) is the highest-priority correctness issue in the spec

Game-theorist O1 and R2 explicitly identify the red-blue/GNEP contradiction as a direct conflict between the mode-mapping file and all three red-blue templates. Schema-engineer does not explicitly flag this contradiction, but schema-engineer's A-3 confirms that `VALID_GAME_FORMS` correctly includes `stackelberg` as a valid game form and that all red-blue templates pass validation — meaning the contradiction is structural (mode-mapping vs. template assignment) rather than a Pydantic model error. Both reviews therefore implicitly agree that the templates are correctly formed (they pass schema validation) but the mode-mapping file is wrong. The resolution — update mode-mapping.yml to declare `red-blue: form: stackelberg` — is uncontested and should be treated as a required fix before the spec moves out of Draft status.

---

### SA-4: Both reviews agree that the example field is underspecified and needs a tighter contract, even if they disagree on the exact mechanism

Schema-engineer O-2, M-3, M-4, R-3, and R-4 all target the looseness of the `example: dict[str, Any]` type and the inconsistent format across templates. Game-theorist's review does not directly address the example field format but implicitly requires examples for the new templates it proposes (R4, R5, R10), and the function-type parameter proposals reveal that no single flat format can cover all cases. Both reviews are aligned on the diagnosis — `dict[str, Any]` is too permissive — and both would be satisfied by a structured example contract that distinguishes scalar-parameter examples from function-type-parameter examples. The disagreement is only on mechanism (flat frozenset vs. typed union), not on the problem itself.
