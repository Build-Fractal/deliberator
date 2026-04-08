# Cross-Review: consistency-auditor reviewing dependency-auditor

**Date**: 2026-04-01
**Phase**: 2 — Cross-Reviews

---

## Dangerous Contradictions

### DC-1: "All clean" dependency verdict vs. cross-spec interface bugs

The dependency-auditor concludes: "All five synthesis files correctly identify these boundaries. No cross-boundary violations were found." This is true at the import level but creates a false sense of safety. My review (CSI-1, CSI-2) identifies that `CodeReviewDomain.score()` reimplements the entire scoring pipeline from `DomainPlugin.score()`, creating a functional coupling that violates the DRY principle even though no import-level violation exists. The dependency-auditor's "all clean" verdict could mislead stakeholders into thinking the 029/030 interface is healthy when it has two confirmed P1 bugs caused by pipeline reimplementation. **The dependency DAG is clean, but the behavioral contract between base and subclass is broken.**

### DC-2: Domains docstring inaccuracy classified as Low vs. its role in CSI-1/CSI-2 root cause

The dependency-auditor flags the `domains/__init__.py` docstring claiming `plugins.base` and `schemas` imports as "Low impact (documentation-only)." However, this docstring inaccuracy reflects a deeper confusion about the domain layer's architecture. The spec 029 coupling rule docstring says "MAY import from conversus.schemas" — a permission that is never exercised. If `CodeReviewDomain` had imported types from `schemas` (e.g., `FeatureSet`), the variable normalization layer might have been designed differently. The docstring is not just wrong; it signals an unresolved architectural decision about whether domains should be leaf packages or consumers of schemas.

### DC-3: Engine-to-plugins boundary gap is more severe than stated

The dependency-auditor correctly identifies that "no synthesis verified the engine-to-plugins integration boundary" and that the engine has zero imports from plugins, domains, or schemas. But this finding is underweighted. My review (R-10) maps 6 explicit cross-spec dependencies that all require an orchestration layer. The dependency-auditor's recommendation to "audit the orchestration layer" is P2, but without that layer, spec 030's gate lifecycle (Dispute 1), spec 022's inter-plugin data flow (Remediation 6), and spec 021's plugin hook execution are all unverifiable. This is not a dependency audit gap — it is a missing architectural layer.

---

## Tensions

### T-1: Import-level vs. behavioral dependency analysis

The dependency-auditor's scope is import boundaries. My scope is cross-spec behavioral consistency. These are complementary but can produce conflicting signals: the dependency DAG shows clean layering while the behavioral analysis shows broken contracts. Neither is wrong, but consumers of both reviews need to understand that "clean imports" does not mean "correct integration."

### T-2: Severity of the `domains/__init__.py` docstring fix

The dependency-auditor rates the docstring fix as P1 ("must address") because it "prevents incorrect mental models." I agree on priority but for different reasons: the docstring fix matters because it forces a decision about whether `domains` should be a true leaf or should be allowed to consume `schemas`. That decision affects future domain implementations.

### T-3: Protocol conformance verification responsibility

The dependency-auditor flags that `code_review/extractors.py` does not import the `VariableExtractor` protocol (structural typing), recommending `isinstance` assertions in tests. My review does not cover this because it is within a single spec (029). However, if extractors fail to satisfy the protocol at runtime, it would surface as a cross-spec bug when spec 030's generic scoring pipeline tries to invoke extractors through the protocol interface. The dependency-auditor and I agree this matters but assign it to different scopes.

### T-4: Completeness of the verified dependency DAG

The dependency-auditor's DAG (verified section) is authoritative for what it covers, but it omits the YAML/config-level dependencies that my review surfaces: `mode-mapping.yml` (spec 025) -> `solver.py` mode support (spec 021), scaffold files (spec 029) -> `score()` extension handling (spec 030). These are runtime dependencies invisible to import analysis.

---

## Safe Agreements

### SA-1: Plugin-to-plugin isolation is genuine and well-verified

Both reviews confirm that plugins are self-contained vertical slices with no cross-plugin imports. The dependency-auditor verified this exhaustively via grep; my review found no cross-plugin behavioral coupling either.

### SA-2: schemas/ is a true leaf package

Both reviews agree that `schemas/` has zero upstream dependencies and is safe to depend on from anywhere. This is foundational for the architecture.

### SA-3: The orchestration layer gap needs investigation

Both reviews identify that the wiring between plugins, domains, and the engine is unverified. The dependency-auditor calls it a missed opportunity; I call it a missing component in the dependency map (R-10). The recommendation converges: audit and document how plugins are loaded and executed.
