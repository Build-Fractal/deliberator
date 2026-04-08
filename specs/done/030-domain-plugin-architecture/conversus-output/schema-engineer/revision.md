# Phase 3 Revision: schema-engineer

**Spec**: 030-domain-plugin-architecture

---

## Position Changes After Cross-Review

### Withdrawn: DomainScore.dimensions unboundedness (Info -> non-issue)

The architect correctly notes that scoring functions clamp all values to [0, 1] before storing them in dimensions. The model's flexibility is intentional. Withdrawing this concern.

### Withdrawn: DomainRecord.convergence as str (Info -> valid design choice)

The architect explains this is intentional for extensibility as the engine's convergence vocabulary evolves. I accept this reasoning. Withdrawing.

### Modified: scaffold_dir enforcement -- UPGRADED to Medium

I support the Medium upgrade. The confusing error when scaffold_dir is unset is a real footgun for domain authors. The fix (add __init_subclass__ check or runtime check in score()) is straightforward.

### New: scaffolds endpoint glob bug confirmed (Medium)

The architect's Concern #1 is confirmed. The API test creates JSON scaffolds so the test passes, but production YAML scaffolds would produce empty results.

### New: API submit endpoint error handling

The submit endpoint should catch FileNotFoundError from load_scaffold() and return HTTPException(400) for invalid scaffold names.
