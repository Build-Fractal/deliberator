# Q06: Objective function template library — open or curated?

**Status**: Decided
**Decision**: Curated for v1 (~29 canonical forms), open contributions added long-term

---

## Context

Open Question #6 from spec 007 Section 13:

> "Should third parties contribute objective function templates (like presets), or should they be curated to maintain mathematical validity?"

## Options Considered

- **A: Curated only** — maintained internally, mathematically validated
- **B: Open contributions** — third parties submit via PR, reviewed for validity
- **C: Two tiers** — official (curated) + community (unvalidated)
- **D: User-defined only** — ship canonical templates, users define custom locally

## Decision

**v1: Curated (Option A). Ship ~29 canonical objective function forms. Prove the math works.**

The priority is proving that objective function templates produce valid, meaningful game-theoretic analysis. This means:
- Ship the full library of ~29 canonical forms (not the 5 sketched in the spec — expand to cover real use cases)
- Each template is mathematically validated against known equilibria
- Templates are tested against real deliberation data (spec 004 stress test artifacts)
- The library proves conversus-nashopt delivers on its promise before opening to contributions

**Long-term: Add open contributions (Option A + B).** Once the canonical library is proven and the template format is stable, accept community templates via PR with mathematical review. The curated set remains the "official" library; community additions expand coverage.

### Why Not Open From Day One

- A bad objective function template produces confidently wrong equilibrium scores — this isn't cosmetic
- The template YAML format itself may evolve as we learn what works
- Review burden for mathematical validity is high — need to establish what "valid" means first
- Opening contributions before proving the canonical set works puts the cart before the horse

### Evolution Path

| Phase | Library | Contributions |
|-------|---------|---------------|
| **v1** | ~29 curated canonical forms | Internal only |
| **v2** | Canonical forms proven against real data | Accept PRs with mathematical review |
| **v3** | Official + community tiers | Community templates labeled, review process documented |

## Rejected Alternatives

- **Option C (two tiers)** rejected for v1: premature tier system before the canonical library is proven
- **Option D (user-defined only)** rejected: we should be providing the forms and proving they work, not pushing that burden to users. The ~29 forms are the product.
