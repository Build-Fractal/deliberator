# Cross-Review: spec-compliance reviewing schema-engineer

**Spec**: 030-domain-plugin-architecture

---

## Agreement

The schema-engineer's review is precise and identifies genuine type safety gaps. I agree with:

- **Concern A (non-numeric variable handling)**: Valid. The asymmetry between `_compute_weighted_score()` (no try/except) and `_check_hard_blocks()` (has try/except) is a real inconsistency. From a compliance perspective, this does not violate any FR, but it degrades robustness.
- **Concern F (silent filter key ignoring)**: Valid. This is a usability issue, not a compliance issue, but it could cause confusion in production.
- **Frozen model verification**: Thorough and correct. The schema-engineer verified all 5 models, which I relied on for my FR-004 assessment.
- **Serialization round-trip**: Correctly identified the `convergence` field gap in tests.

## Disagreements

### 1. Concern C (zero total weight) -- should be Low, not Medium

The schema-engineer rates this Medium. I rate it **Low**. A scaffold with all-zero weights is a degenerate configuration that no reasonable user would create intentionally. The scorer returning 0.0 is a safe default. The real fix is scaffold validation at load time (warn on zero total weight), not runtime handling. From a compliance perspective, no FR requires handling degenerate scaffolds.

### 2. Concern D (exact threshold boundary) -- should be Info, not Medium

The schema-engineer rates this Medium. I rate it **Info**. The operators (`<`, `<=`, etc.) are standard mathematical comparisons. The scaffold author explicitly chooses which operator to use. If they write `"safety < 0.2"`, they mean strict less-than. If they want to include the boundary, they write `"safety <= 0.2"`. This is not ambiguous -- it is a feature. The documentation suggestion is valid but does not constitute a code concern.

### 3. Concern H (workspace path validation) -- AGREE, but note it is intentional

The schema-engineer notes that `SubmitRequest.workspace` is `str` and the API converts it to `Path` without validation. This is intentional: the `DomainContext` model does not validate workspace existence because extractors may need to handle non-existent workspaces (e.g., when reviewing deleted files). The API should validate that the string is a syntactically valid path, but checking existence would be overly restrictive.

## Additions

The schema-engineer did not assess how the models relate to the spec's section 4 (Frontend Contract). The spec defines a TypeScript `DomainAPI` interface:

```typescript
interface DomainAPI {
  submit(context: DomainContext): Promise<DomainScore>;
  getScore(id: string): Promise<DomainScore>;
  getHealth(): Promise<HealthMetrics>;
  getTrend(field: string, window?: number): Promise<TrendData>;
  runGate(id: string): Promise<GateResult>;
  listScaffolds(): Promise<Scaffold[]>;
}
```

The Python API response models (`SubmitResponse`, `HealthResponse`, `TrendResponse`, `ScaffoldInfo`) map well to this contract:
- `submit` -> `SubmitResponse` (verdict, overall, recommendations) -- maps to `DomainScore`
- `getScore` -> `get_record` returns full record -- maps to `DomainScore`
- `getHealth` -> `HealthResponse` -- maps to `HealthMetrics`
- `getTrend` -> `TrendResponse` -- maps to `TrendData`
- `listScaffolds` -> `list[ScaffoldInfo]` -- maps to `Scaffold[]`
- `runGate` -> not implemented -- maps to `GateResult`

The frontend contract is 5/6 implementable from the current API. The gate endpoint gap is the same one identified by all agents.

The schema-engineer also did not evaluate the `DomainContext.metadata` field type. It is `dict[str, Any]` which is maximally flexible but provides no schema for consumers. Each domain would need to document its expected metadata keys. This is acceptable for a plugin architecture (domains own their metadata schema) but could benefit from a `metadata_schema: dict[str, type]` class attribute on `DomainPlugin` for runtime validation.
