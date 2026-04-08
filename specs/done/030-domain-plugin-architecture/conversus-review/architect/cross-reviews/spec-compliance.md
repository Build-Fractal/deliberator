# Cross-Review: architect reviewing spec-compliance

**Spec**: 030-domain-plugin-architecture

---

## Agreement

The spec-compliance audit is rigorous and well-evidenced. I agree with the assessments for FR-001 through FR-019 and SC-001 through SC-005, with the following exceptions.

The identification of FR-002 (importlib loading) and FR-003 (graceful failure on missing packages) as NOT MET is correct. I should have called this out more prominently in my review -- the plugin discovery mechanism is a gap I noted only indirectly through the missing `gate()` and `get_router()` methods.

The FR-008 (append-only semantics) assessment as MET is correct and well-evidenced. Neither store exposes mutation methods, and the protocol design enforces this at the contract level.

## Disagreements

### 1. FR-007 (Backend selection via configuration) -- should be NOT MET, not PARTIALLY MET

The spec-compliance agent rates FR-007 as PARTIALLY MET because "the API router factory accepts a store parameter, enabling injection." I disagree. FR-007 says backend selection must be via *configuration*, not code changes. Currently, choosing a backend requires calling `JSONLStore()` or `SQLiteStore()` in code -- the configuration-to-store mapping does not exist. Dependency injection readiness is not the same as configuration-driven selection. This should be NOT MET.

### 2. SC-001 assessment is too generous

The spec-compliance agent rates SC-001 as MET based on the existence of `CodeReviewDomain`. However, SC-001 says "with zero infrastructure code." The code-review domain does import from `conversus.domains.base` and uses the generic scoring, so the infrastructure claim is largely correct. But the code-review domain also has its own `extractors.py` and `domain.py` files -- these are domain-specific code, not infrastructure code. The distinction is valid and SC-001 is indeed MET. I withdraw this disagreement.

### 3. FR-019 rating should be NOT MET

The spec-compliance agent rates FR-019 as PARTIALLY MET because scaffolds are "plain files that can be created, shared, and versioned via git." This is true of literally any file format. FR-019 requires active support: "Users MUST be able to create, share, and version custom scaffolds." This implies tooling or at minimum documentation of the scaffold format. Currently, users would need to reverse-engineer the `Scaffold` model fields from code. I would rate this NOT MET -- the capability exists in theory but is not exposed or documented for users.

## Additions

The spec-compliance agent did not assess the constraint from section 8: "Domain plugins MUST NOT depend on each other. Each is independently installable." This is satisfied by design -- `conversus.domains.base` and `conversus.domains.store` have no domain-specific imports, and the code-review domain only imports from the base layer. Worth noting as a structural win.

The constraint "The core conversus package MUST NOT depend on any domain plugin" is also satisfied -- `conversus/domains/__init__.py` imports only from `base` and `store`, not from `code_review/`.
