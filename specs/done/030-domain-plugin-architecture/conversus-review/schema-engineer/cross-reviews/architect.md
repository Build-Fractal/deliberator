# Cross-Review: schema-engineer reviewing architect

**Spec**: 030-domain-plugin-architecture

---

## Agreement

The architect's review is comprehensive and architecturally sound. I agree with the following assessments:

- **Concern A (gate/get_router missing from ABC)**: Correct. The spec clearly shows these in the contract. This is the most significant gap.
- **Concern C (hard block string validation)**: I independently found the same issue from a schema perspective. Malformed condition strings are silently skipped, which masks scaffold errors.
- **Concern E (get() searches all domains)**: Correct. This is an O(N*M) lookup that should be O(1) with a domain hint.
- **Concern G (missing /gate endpoint)**: Correct and consistent with Concern A.

The coupling analysis is solid -- zero engine imports is verified and important for the plugin architecture to remain viable.

## Disagreements

### 1. Concern B (scaffold_dir not enforced) -- AGREE but LOWER severity

The architect rates Concern B as Low, and I agree with the rating. However, the proposed fix (`__init_subclass__`) is overkill. A simpler approach: make `scaffold_dir` a required parameter in `DomainPlugin.__init__()` with `ABC.__init__()` enforcement. But since the class uses attribute-level declaration (not `__init__`), the Python ABC mechanism cannot enforce it. The current approach is consistent with how `name` and `version` are declared -- none of the three attributes are enforced by the ABC. This is a convention, not a bug.

### 2. Concern I (score() hard-codes .json extension) -- should be MEDIUM

The architect rates this Low. I rate it **Medium** from a schema perspective. FR-018 says scaffolds MUST be YAML files. The `load_scaffold()` function supports YAML. But `DomainPlugin.score()` constructs `self.scaffold_dir / f"{scaffold}.json"` (line 447), which means only JSON scaffolds are discoverable by name. This is not just an inconsistency -- it contradicts the spec's explicit YAML requirement.

A domain that follows FR-018 and ships YAML scaffolds would need to override `score()` to change the extension, which defeats the generic scoring premise.

### 3. Concern F (JSONLStore scalability note) -- AGREE, trivially fixable

The architect correctly notes the scalability warning is in the module docstring but not the class docstring. This is a one-line fix. Agree with Low severity.

## Additions

The architect's analysis did not cover the `_linear_slope()` function's numerical stability. For very large value counts or very small differences, the OLS computation could accumulate floating-point errors. In practice, window sizes are small (10-20 records), so this is not a concern. But if the trend API is ever used with large windows (e.g., 10,000 records), the naive loop-based OLS could lose precision. A Kahan summation or iterative algorithm would be more robust. This is informational only.

The architect also did not note that `SQLiteStore` uses `check_same_thread=False` (store.py, line 404). This enables cross-thread access, which is necessary for FastAPI (async event loop + sync SQLite). However, it also means that concurrent writes from multiple threads could interleave within a transaction. SQLite's WAL mode (line 407) mitigates this for reads, but concurrent writes would serialize at the database level. For the expected scale (<10K records), this is fine. For production use with many concurrent API requests, a connection pool or async driver would be needed.
