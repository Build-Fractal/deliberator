# v4.0.0 Originating Deliberation — Verdict & Empirical Follow-through

**Deliberation ID:** v4.0.0-tier-extraction-originating-2026-05-06
**Pathway:** MAJOR (per CONSTITUTION.md § Pathway Taxonomy)
**Stage:** Originating (per GOVERNANCE.md Part VIII step 3)
**Engine output:** `arbitration/resolution.md` + `summary/final.md`

---

## Arbiter rulings

| Question | Verdict |
|---|---|
| Q1 — Tier classification (10/10/6) | **APPROVE-AS-DRAFTED** — proceeds contingent on empirical templating-surface audit |
| Q2 — conversus-oss admission | **ADMIT-PROVISIONAL** — verification of audit findings + coordination infra |
| Q3 — conversus admission | **ADMIT-PROVISIONAL** — Plugin Isolation + templating-surface verification post-PR-#30 |

Net outcome: **ratification proceeds with four P1 conditions to address.**

## P1 conditions and empirical responses (2026-05-06)

### Condition 1+4 — Empirical templating-surface audit

**Concern:** tier-classifier disputed conversus's Principle VIII N/A claim; arbiter ruled empirical audit must precede tier finalization (Dispute 4).

**Audit performed:**
```
$ grep -rEl "Template|Jinja|render|format_map|f\"\"\"" --include="*.py" conversus/conversus_enhanced/
(no matches)
```

**Finding:** conversus_enhanced/ contains no templating code. The N/A claim is empirically supported. Principle VIII Universal-tier classification stands; conversus's N/A claim stands.

**conversus-oss templating surface (separately):** templates/ directory contains 7 mode subdirectories × 7 phase templates = 49 template files. Principle VIII Suite-tier (proposed Universal) responsibility lives entirely in conversus-oss; classifying VIII as Universal does not require conversus to gain a templating surface.

**Recommendation:** keep VIII at Universal. Note in the v4.0.0 spec that conversus's N/A on VIII is structural (not templating-tier-shifted away) and re-audits if conversus ever gains code-generation surface.

### Condition for Q3 — Plugin Isolation post-PR-#30 verification

**Concern:** admission-auditor-enhanced challenged whether PR #30's framework deletion was complete; "framework duplicates" finding noted in synthesis.

**Audit performed:**
```
$ grep -rEn "from conversus\.(schemas|plugins|domains|paths)|import conversus\.(schemas|plugins|domains|paths)" --include="*.py" conversus/
./linter/validate.py:99:    from conversus.paths import resolve_package_path
./tests/test_optimizer.py:29: from conversus.plugins.base import (...)
./tests/test_payoffs.py:24: from conversus.schemas.features import AgentFeatures, RoundFeatures
./tests/test_validation.py:27: from conversus.schemas.validation import (...)
./tests/test_plugins.py:30: from conversus.plugins.base import (...)
[plus 5 more test imports]
```

**Finding:** All matches are imports of the conversus-oss package (`conversus` is the package name OSS publishes). PR #30 deleted the LOCAL `conversus/{schemas,plugins,domains,paths}` modules — the imports above resolve to the installed OSS package via `pyproject.toml` dependency. This is exactly Plugin Isolation working as designed: conversus_enhanced consumes the OSS framework as an external dependency rather than vendoring it locally.

```
$ ls conversus/conversus/
self-audit/  self-review/
```

**Finding:** The local `conversus/` directory inside the conversus repo contains only `self-audit/` and `self-review/` — private deliberation artifacts that PR #30 explicitly kept (per its description). NOT a Python package; no `__init__.py`. Cannot collide with the OSS `conversus.*` namespace.

**Recommendation:** Plugin Isolation Satisfied claim stands. No change to conversus's CONFORMANCE.md needed.

### Condition for Q2 — Coordination infrastructure for cross-repo XXII remediation

**Concern:** admission-auditor-oss argued coordinated 2026-08-01 deadlines on Principle XXII (both repos) lack actual coordination infrastructure beyond shared tracking.

**Status:** Open. The two CONFORMANCE.md drafts both reference a `TBD spec 077` for the coordinated XXII work. That placeholder is honest about the gap; closing it requires either:
- (a) Writing spec 077 as a real coordinated spec with explicit dependency ordering before the XXII deadlines bind, OR
- (b) Decoupling the XXII remediations across repos (each repo addresses its own surface independently, no atomic delivery promise).

**Recommendation:** Adopt (b) for the v4.0.0 spec — explicitly decouple XXII remediation across the two repos. Each repo addresses its distribution-surface principles independently:
- conversus-oss XXII: codify .mcpb / PyPI / plugin-marketplace per-channel vendoring rules in conversus-oss CI.
- conversus XXII: codify conversus's own publication channels in conversus CI.

If the .mcpb bundle ever needs to vendor BOTH repos' content (per `project_mcpb_vendoring_concern` memory), that's a separate spec that depends on both repos' XXII being individually complete first. Drafting that follow-on spec is NOT a v4.0.0 prerequisite.

**Update needed in CONFORMANCE.md drafts:** Replace "TBD spec 077 (coordinated)" with "this repo's own per-channel vendoring CI". Drop the "coordinated" framing.

### Condition for Q2 — Verification of audit findings

**Concern:** admission-auditor-oss's specific findings (V cross-mode coverage, XXIV named perimeters, XXVI parametrization breadth) need translation into Provisional remediations.

**Recommendation:** Update conversus-oss/CONFORMANCE.md to add three specific Provisional items based on these findings:
- **V (Observable Deliberation):** "Add cross-mode test coverage for output_contract validation" — 2026-08-01.
- **XXIV (Safety-Critical Defense-in-Depth):** "Enumerate named perimeters and their independent guards in CONSTITUTION.md or a sibling SAFETY.md" — 2026-09-01.
- **XXVI (Meta-Testing):** "Confirm test_skill_engine.py parametrization covers (mode × provider) cells, not just cooperative × mock" — 2026-08-01.

These flip from Satisfied to Provisional in the v4.0.0 spec implementation.

## Net amendments to make before drafting the v4.0.0 spec

1. ✅ Empirical audits complete (templating, Plugin Isolation).
2. Update `conversus-oss/CONFORMANCE.md`: add V/XXIV/XXVI Provisional items; revise XXII remediation to "this repo's own per-channel CI" (decouple from conversus).
3. Update `conversus/CONFORMANCE.md`: revise XXII remediation likewise.
4. Update `build-fractal/conversus/COMPLIANCE.md` Part VII snapshot to reflect post-deliberation Provisional counts.
5. Log this deliberation in `build-fractal/conversus/CONSTITUTIONAL_CONVERSATIONS.md` (suite tier) and `conversus-oss/CONSTITUTIONAL_CONVERSATIONS.md` (component log).

## Next stages (per GOVERNANCE.md Part VIII)

After the above amendments land:
- **Step 4:** Draft `conversus-oss/specs/v4.0.0-tier-extraction/spec.md` with verbatim amendment text.
- **Step 5:** Run self-consistency verification deliberation (markers visible, ~26 LLM launches).
- **Step 6:** Run blind verification deliberation (markers stripped via `scripts/strip-constitution-for-blind.py`, ~26 LLM launches).
- **Step 7:** Open implementation PR. Mergeable only when both verifications pass.
- **Step 8:** Log all four deliberations (originating + self-consistency + blind + verification of override if any) in CONSTITUTIONAL_CONVERSATIONS.md at appropriate tiers.

## Quality indicators (engine-reported)

- Phases completed: 5
- Agent count: 4
- Cross-reviews performed: 12
- Major withdrawals during deliberation: 4 (tier-classifier dropped XII Universal promotion + XXVI Suite expansion; admission-auditor-enhanced dropped admission deferral; inclusion-criteria-auditor dropped Universal verification feasibility audit)
- Surviving disputes: 4 (all addressed by arbiter rulings; all four flagged as P1 with addressable conditions)

The deliberation surfaced genuine tension and produced actionable conditions rather than rubber-stamp approval. The methodological discipline (cross-review forced position withdrawals before disputes phase) demonstrates the engine working as designed.
