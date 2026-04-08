# Cross-Review: implementation-verifier reviewing dependency-auditor

**Date**: 2026-04-01
**Phase**: 2 — Cross-Reviews

---

## Dangerous Contradictions

### DC-1: "All arrows point downward. No cycles. No boundary violations" is true but misleading when combined with my verification

The dependency-auditor's verified DAG shows clean layering. My verification found 2 inaccuracies in spec 021 involving file misattribution (pure function module vs. plugin wrapper). These misattributions occur *within* the `plugins/nashopt/` package, so they do not violate the dependency DAG. But they reveal that the internal structure of plugin packages is complex enough that synthesis reviewers confuse which file does what. The clean DAG at the package level conceals intra-package complexity that causes attribution errors.

### DC-2: The `domains/__init__.py` docstring fix may be premature

The dependency-auditor recommends fixing the docstring as P1 ("must address") to prevent incorrect mental models. I note a tension: the docstring says domains "import from `conversus.plugins.base` and `conversus.schemas`." This is currently false, as the dependency-auditor verified. However, the spec 030 synthesis's gate lifecycle integration (Dispute 1) may eventually require domains to import from a shared protocol or interface. If the docstring is "fixed" to say "imports only from `conversus.domains.base`, pydantic, stdlib" and then gate integration reintroduces a `schemas` dependency, the docstring will need a second update. The better fix might be to rewrite the docstring as a coupling *rule* ("MUST NOT import from engine, linter, web, mcp_server") rather than a dependency *claim* ("imports from X, Y, Z"), following the pattern already used in `code_review/__init__.py`.

### DC-3: Protocol conformance verification is not a dependency concern but an interface concern

The dependency-auditor's recommendation to add `isinstance(extractor, VariableExtractor)` assertions is categorized under dependency audit. Protocol conformance via structural typing is an interface verification concern, not a dependency concern. The extractors module intentionally avoids importing the protocol to keep the dependency surface narrow (exactly the property the dependency-auditor praises). Adding `isinstance` checks in tests is valuable, but the recommendation should be framed as "verify interface contracts" not "verify dependency conformance."

---

## Tensions

### T-1: Docstring accuracy vs. architectural intent

The dependency-auditor treats the `domains/__init__.py` docstring as documentation to be corrected. I would treat it as a design intent document to be clarified. The distinction: if it is documentation, the fix is to match reality. If it is design intent, the fix is to either implement the intent or explicitly abandon it. The dependency-auditor's "fix the docstring" approach assumes documentation; the synthesis reviews assume intent.

### T-2: Granularity of dependency verification

The dependency-auditor's DAG operates at the package level (`plugins/nashopt`, `domains/base`, `schemas/`). My verification operates at the file level (`solver.py`, `equilibrium_scorer.py`, `kalman.py`). Several issues I found (file misattributions in spec 021, store protocol methods in spec 030) exist at the file level but are invisible at the package level. The dependency-auditor's DAG is correct and useful, but a file-level dependency graph within each package would catch the intra-package confusion I identified.

### T-3: The engine isolation finding

The dependency-auditor states: "The engine (`engine/`) contains zero imports from `plugins/`, `domains/`, or `schemas/`." This is correctly verified. However, I note this means the engine cannot directly invoke any plugin, domain, or schema operation. The dependency-auditor correctly identifies this implies a wiring layer above the engine. But neither of us examined that layer. The dependency-auditor frames this as a "missed opportunity" (P2); I think it is a prerequisite for validating several of my "architecture improvement" recommendations.

### T-4: What "verified" means across our reviews

The dependency-auditor marks 7 architectural claims as "VERIFIED" based on grep analysis of imports. I mark 18 of 21 code-behavior claims as "VERIFIED" based on line-by-line code reading. Our verification methods are complementary but have different confidence levels: grep is exhaustive for imports but misses behavioral contracts; line-by-line reading is precise but samples only 3 claims per spec. A fully verified picture requires both.

---

## Safe Agreements

### SA-1: Plugin-to-plugin isolation is genuine at all levels

The dependency-auditor verified zero cross-plugin imports via grep. I verified that the files within each plugin reference only their own package and `plugins/base`. Both agree this is the strongest architectural property in the codebase.

### SA-2: schemas/ is a true leaf package

Both reviews confirm schemas has no upstream dependencies. I verified individual files (`game_forms.py`, `solvers.py`, `construction.py`); the dependency-auditor verified the package-level imports.

### SA-3: The `HAS_AMPL` guard gap is real and dependency-safe to fix

Both reviews confirm the bug. The dependency-auditor notes the optimizer plugin's isolation. I verified the specific import guard code. The fix (adding `import highspy` to the try block) is confined to a single file within a single package.
