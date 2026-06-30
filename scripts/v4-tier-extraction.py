#!/usr/bin/env python3
"""v4.0.0 tier extraction — programmatic relocation script.

Reads deliberator/CONSTITUTION.md v3.2.3 and produces:
- build-fractal/CONSTITUTION.md (Tier 1 — Universal, v1.0.0) with byte-equal text of 10 principles
- build-fractal/deliberator/CONSTITUTION.md (Tier 2 — Suite, v1.0.0) with byte-equal text of 10 principles
- deliberator/CONSTITUTION.md (component, v4.0.0 — reduced)

Spec: deliberator/specs/v4.0.0-tier-extraction/spec.md (v3 — both verifications passed).
Both verification deliberations are at deliberator/deliberations/v4.0.0-tier-extraction-{originating,self-consistency,blind}-2026-05-{06,07}/.

Run from deliberator directory:
    cd deliberator && uv run python scripts/v4-tier-extraction.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Resolve paths relative to the deliberator working dir
ROOT = Path(__file__).resolve().parents[1]
CONSTITUTION = ROOT / "CONSTITUTION.md"
TIER1 = ROOT.parent / "build-fractal" / "CONSTITUTION.md"
TIER2 = ROOT.parent / "build-fractal" / "deliberator" / "CONSTITUTION.md"

# Tier classification per spec v3 §4
TIER1_PRINCIPLES = ["I", "II", "III", "IV", "VII", "VIII", "IX", "XI", "XIV", "XXVIII"]
TIER2_PRINCIPLES = ["V", "XII", "XIII", "XV", "XVI", "XXII", "XXIII", "XXIV", "XXV", "XXVII"]
COMPONENT_PRINCIPLES = ["XVII", "XVIII", "XIX", "XX", "XXI", "XXVI"]
RETIRED = ["VI", "X"]


def parse_principle_blocks(text: str) -> dict[str, tuple[int, int]]:
    """Return dict of {roman: (start_line_0_indexed, end_line_exclusive)}.

    A principle's body spans from its header line through the line before the next
    `### {Roman}.` header, OR through the final line of the principles section
    (immediately before `## Governance`).
    """
    lines = text.split("\n")
    header_re = re.compile(r"^### ([IVX]+)\. ")
    governance_re = re.compile(r"^## Governance\b")

    blocks: dict[str, int] = {}  # roman -> start_line
    governance_line = None
    for i, line in enumerate(lines):
        m = header_re.match(line)
        if m:
            blocks[m.group(1)] = i
        if governance_re.match(line):
            governance_line = i
            break

    if governance_line is None:
        raise SystemExit("Could not find ## Governance section in CONSTITUTION.md")

    sorted_romans = sorted(blocks.keys(), key=lambda r: blocks[r])
    result: dict[str, tuple[int, int]] = {}
    for idx, roman in enumerate(sorted_romans):
        start = blocks[roman]
        end = blocks[sorted_romans[idx + 1]] if idx + 1 < len(sorted_romans) else governance_line
        # Trim trailing blank lines from body block (preserving leading whitespace inside body)
        while end > start and lines[end - 1].strip() == "":
            end -= 1
        result[roman] = (start, end)
    return result


def slice_principle_body(lines: list[str], start: int, end: int) -> str:
    """Return the byte-equal body text including the header line.

    Always ends with a trailing newline so concatenated bodies are well-formed.
    """
    return "\n".join(lines[start:end]) + "\n"


def extract_governance_section(text: str) -> str:
    """Return everything from `## Governance` through end of file (preserves footer)."""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("## Governance"):
            return "\n".join(lines[i:])
    raise SystemExit("Could not locate ## Governance")


def extract_existing_sirs(text: str) -> str:
    """Return all top-of-file `<!-- Sync Impact Report ... -->` comment blocks."""
    sirs = []
    in_sir = False
    cur: list[str] = []
    for line in text.split("\n"):
        if line.startswith("<!--") and "Sync Impact Report" in line:
            in_sir = True
            cur = [line]
            continue
        if in_sir:
            cur.append(line)
            if line.strip().endswith("-->"):
                sirs.append("\n".join(cur))
                in_sir = False
                cur = []
                continue
        # Stop at first non-comment, non-blank line outside SIR
        if not in_sir and line.strip() and not line.strip().startswith("<!--"):
            break
    return "\n\n".join(sirs)


# ---------------------------------------------------------------------------
# Tier 1 — Universal preamble + new SIR + bodies
# ---------------------------------------------------------------------------

TIER1_PREAMBLE = """# Build Fractal — Tier 1 (Universal) Constitution

<!--
Sync Impact Report
Version: (newly ratified) → 1.0.0 (Tier 1 establishment)

Established: 2026-05-07 via v4.0.0 tier-extraction amendment in deliberator.

This document carries the principles that apply to every Build Fractal product.
The 10 Universal principles below are the result of the v4.0.0 ratification
deliberation chain in deliberator/deliberations/v4.0.0-tier-extraction-*/.

Principles relocated here from deliberator/CONSTITUTION.md v3.2.3:
  I. Spec-Driven Development
  II. Stable Interfaces
  III. Backward-Compatible Extension
  IV. Documentation Is the Product
  VII. Reproducibility Over Inconsistency
  VIII. Templating Engines Over Inference
  IX. Functional Programming and Clean Code
  XI. Single Source of Truth
  XIV. Spec-Implementation Parity
  XXVIII. Test-Fix Boundary Preservation

Constitutional debt acknowledgment: 9 of these 10 principles were ratified
pre-Inclusion-Criteria-gate (v2.4.0). Their constitutional validity is
preserved per Principle II number-stability; their post-gate compliance with
current Inclusion Criteria is NOT re-evaluated by v4.0.0. XXVIII passed
post-gate. Future targeted amendments may address individual principle
post-gate conformance as separate cycles.

Verbatim preservation contract (per spec §5): each principle's body text
appears here byte-for-byte identical to its source in deliberator
CONSTITUTION.md v3.2.3, modulo only documented cross-reference path-prefix
rewrites.
-->

**Status:** RATIFIED — v4.0.0 (2026-05-07).
**Version:** 1.0.0
**Ratification:** Originating + self-consistency + blind verification 2026-05-06/07. Logged in `../deliberator/CONSTITUTIONAL_CONVERSATIONS.md` and `deliberator/CONSTITUTIONAL_CONVERSATIONS.md`.

---

## Purpose

This tier holds principles that apply to **every Build Fractal product**. When a sibling product joins the namespace, it inherits this tier automatically.

For the deliberator suite's tier-2 (Suite) constitution, see `deliberator/CONSTITUTION.md`. For component-level constitutions, see each repo's own `CONSTITUTION.md`.

## Tier Model

```
Tier 1 (Universal)   ← THIS DOCUMENT — every Build Fractal product
   │
   ├── Tier 2 (Suite — deliberator): deliberator/CONSTITUTION.md
   │       │
   │       ├── Component: ../deliberator/CONSTITUTION.md
   │       └── Component: ../deliberator/CONSTITUTION.md (does not yet exist)
   │
   └── (future suites)
```

Lower tiers may strengthen rules from higher tiers but may not weaken them.

The operational definition of "weakening" — and the enforcement mechanism — is documented in `deliberator/CONSTITUTION.md` § Cross-tier weakening prohibition.

## Principles

The 10 principles below are byte-for-byte identical to their text in `../deliberator/CONSTITUTION.md` v3.2.3. Cross-references to other principles use the form `Principle {Roman}` (without path prefix when intra-document) or `{tier}/CONSTITUTION.md § Principle {Roman}` (when cross-tier).

"""

TIER1_FOOTER = """

---

## Amendment Process

Amendments to this Tier 1 constitution follow the pathway taxonomy documented in `../deliberator/CONSTITUTION.md` § Governance. The deliberator suite's `deliberator/GOVERNANCE.md` is the operational runbook for that procedure.

Amendments at this tier propagate downward to all suite-tier and component-tier constitutions. Per the cross-tier inheritance rule, lower tiers MUST honor any tightening of Tier 1 rules; loosening at Tier 1 takes effect immediately at all tiers.

Cross-tier weakening prohibition (per the v4.0.0 amendment): a lower-tier amendment that grants implicit relief, shifts implementation impact, or adds bypass language for a Tier 1 principle is considered a weakening and is rejected. See `deliberator/CONSTITUTION.md` § Cross-tier weakening prohibition for the operational definition + enforcement.

## Governance log

Tier 1 governance events (amendments, propagations, etc.) are logged at `CONSTITUTIONAL_CONVERSATIONS.md` (created on first amendment after v4.0.0 establishment).
"""


# ---------------------------------------------------------------------------
# Tier 2 — Suite preamble + new SIR + bodies + B2/B3/B5
# ---------------------------------------------------------------------------

TIER2_PREAMBLE = """# Deliberator Suite — Tier 2 Constitution

<!--
Sync Impact Report
Version: (newly ratified) → 1.0.0 (Tier 2 establishment)

Established: 2026-05-07 via v4.0.0 tier-extraction amendment in deliberator.

Inherits from: ../CONSTITUTION.md (Tier 1 — Universal, v1.0.0).

This document carries the principles that apply to all deliberator-family
repos (the OSS engine, the paid enhanced layer, future siblings).

Principles relocated here from deliberator/CONSTITUTION.md v3.2.3:
  V. Observable Deliberation
  XII. No Dead Infrastructure
  XIII. Enum Completeness
  XV. Plugin Isolation
  XVI. Mathematical Transparency  [Suite-tier rationale below per Fix B5]
  XXII. Distribution Surface Integrity
  XXIII. Provider Robustness Contract
  XXIV. Safety-Critical Defense-in-Depth
  XXV. Live Test Cost Discipline
  XXVII. Operator-Configurable Tool Surface

Sections added under Fix B3 (cross-tier weakening prohibition) and Fix B5
(XVI Suite-tier rationale) per the 2026-05-07 blind verification deliberation.

Verbatim preservation contract (per spec §5): each principle's body text
appears here byte-for-byte identical to its source in deliberator
CONSTITUTION.md v3.2.3, modulo only documented cross-reference path-prefix
rewrites.
-->

**Status:** RATIFIED — v4.0.0 (2026-05-07).
**Version:** 1.0.0
**Inherits from:** `../CONSTITUTION.md` (Tier 1 Universal, v1.0.0).
**Ratification:** Originating + self-consistency + blind verification 2026-05-06/07. Logged in `CONSTITUTIONAL_CONVERSATIONS.md` and `../../deliberator/CONSTITUTIONAL_CONVERSATIONS.md`.

---

## Purpose

This tier holds principles that apply to **every deliberator-family repo**. The principles below presume multi-agent deliberation as the substrate, plugin entry-points as the integration boundary, and the free/paid partition (spec 033) as the monetization architecture. Other Build Fractal product lines do not need to follow these.

## Principles

The 10 principles below are byte-for-byte identical to their text in `../../deliberator/CONSTITUTION.md` v3.2.3. Cross-references to Tier 1 principles use `../CONSTITUTION.md § Principle {Roman}`. Cross-references to component-tier principles use `../../deliberator/CONSTITUTION.md § Principle {Roman}`.

"""

TIER2_XVI_RATIONALE = """

### XVI Suite-tier rationale (Fix B5)

Mathematical transparency applies suite-wide because it is the governance constraint on ANY scoring/optimization approach in the deliberator suite — it constrains the assembled objective function's *assembly form* (parameter names, template selection, gap-identifier set), not the optimizer's internal mathematics. Future suite siblings adopting fundamentally different optimization paradigms (e.g., neural optimization without explicit parameter pinning) inherit XVI's discipline regardless of mathematical form, because the discipline is about cross-run determinism + transparency of inputs, not about specific math operations. Surviving Dispute 1 of the 2026-05-07 blind verification ruled in favor of Suite-tier with this rationale; see `../../deliberator/deliberations/v4.0.0-tier-extraction-blind-2026-05-07/arbitration/resolution.md`.

"""

TIER2_FOOTER = """

---

## Cross-tier weakening prohibition

**Operational definition (per Fix B3, ratified 2026-05-07):** a lower-tier amendment **weakens** an upper-tier principle if **any** of the following holds:

1. **(i) Implicit relief.** The amendment grants relief from the upper-tier principle's enforcement at the lower-tier scope WITHOUT invoking the formal Relief pathway documented in `COMPLIANCE.md` Part VI. Relief outside the formal pathway is implicit and unauditable.

2. **(ii) Implementation-impact shift.** The amendment introduces interpretation language that, applied to existing implementations, would cause them to no longer satisfy the upper-tier principle. If existing-Satisfied → newly-non-compliant, the amendment has weakened the standard even if its surface text doesn't say so.

3. **(iii) Suite-specific adaptation bypass.** The amendment adds a "suite-specific adaptation" clause that effectively bypasses an upper-tier principle's MUST clause, even if framed as "adaptation" rather than relief.

**Enforcement:**
- **Meta-arbiter responsibility:** any cross-tier amendment MUST be reviewed by a balanced-arbiter agent specifically tasked with checking criteria (i), (ii), (iii) against existing upper-tier principles.
- **Linter-flagged review:** the tier-coherence linter at `../../deliberator/linter/tier_coherence.py` flags any Tier 2 / Component principle text that contains "relief," "exception," "adaptation," "exemption," "carve-out," or "bypass" within 200 characters of a Tier 1 principle name. Flag triggers manual impl-PR review.
- **Existing-implementation impact check:** the impl-PR review for any cross-tier amendment runs the check against existing repo CONFORMANCE.md declarations and confirms Satisfied claims remain valid.

This prohibition is binding on the v4.0.0 amendment itself and on all future cross-tier amendments. Surfaced by the 2026-05-07 blind verification (Convergence 3); ratified per Surviving Dispute 2.

## Component-tier residue

After v4.0.0, `../../deliberator/CONSTITUTION.md` retains 6 component-tier principles plus the Governance section + retired markers + audit-trail SIRs:

- **XVII. Content Classification** — what counts as free vs paid (spec 033)
- **XVIII. Progressive Disclosure** — capability discovery surface in the OSS layer
- **XIX. Non-Extractable Core** — protections preventing the OSS core from being silently re-implemented
- **XX. Decomposition Mechanism Precedence** — order in which extraction patterns are applied
- **XXI. Extraction Ordering** — sequencing rules for multi-step extractions
- **XXVI. Meta-Testing** — tests-of-tests; the OSS engine's self-validation harness

These remain at component tier because they describe constraints on the OSS layer specifically, not on the suite as a whole.

## Amendment Process

Amendments to this Tier 2 constitution follow the pathway taxonomy documented in `../../deliberator/CONSTITUTION.md` § Governance. The full procedure is documented in `GOVERNANCE.md` (this directory).

Cross-tier interaction:
- A Tier 2 amendment cannot grant relief from a Tier 1 principle (per the weakening prohibition above).
- A component-tier amendment cannot grant relief from a Tier 2 principle.
- Strengthening at Tier 2 takes effect at next MAJOR in each component.
- Loosening at Tier 2 takes effect immediately at all components (looser tier cannot be tighter than itself).

This tier's governance log is `CONSTITUTIONAL_CONVERSATIONS.md` (this directory).
"""


# ---------------------------------------------------------------------------
# Component preamble (new SIR for v3.2.3 → v4.0.0 + reduction)
# ---------------------------------------------------------------------------

COMPONENT_NEW_SIR = """<!--
Sync Impact Report
Version change: 3.2.3 → 4.0.0 (MAJOR — tier extraction. 20 principles
relocated to higher tiers; 6 retained at component scope; 2 retired
markers preserved.)

Modified sections:
  - "Core Principles" reduced to 6 principles (XVII-XXI, XXVI) plus
    retired markers for VI and X. Cross-reference block added at top
    pointing readers to ../build-fractal/CONSTITUTION.md (Tier 1) and
    ../build-fractal/deliberator/CONSTITUTION.md (Tier 2) for relocated
    principles.
  - "Governance" preserved verbatim. Pathway Taxonomy, Constitutional
    Inclusion Criteria, Compliance, Amendment Process all retained
    here as the canonical procedural reference for amendments at any
    tier.

Relocated to Tier 1 (../build-fractal/CONSTITUTION.md, v1.0.0):
  I. Spec-Driven Development
  II. Stable Interfaces
  III. Backward-Compatible Extension
  IV. Documentation Is the Product
  VII. Reproducibility Over Inconsistency
  VIII. Templating Engines Over Inference
  IX. Functional Programming and Clean Code
  XI. Single Source of Truth
  XIV. Spec-Implementation Parity
  XXVIII. Test-Fix Boundary Preservation

Relocated to Tier 2 (../build-fractal/deliberator/CONSTITUTION.md, v1.0.0):
  V. Observable Deliberation
  XII. No Dead Infrastructure
  XIII. Enum Completeness
  XV. Plugin Isolation
  XVI. Mathematical Transparency  [Suite-tier rationale in Tier 2 doc per Fix B5]
  XXII. Distribution Surface Integrity
  XXIII. Provider Robustness Contract
  XXIV. Safety-Critical Defense-in-Depth
  XXV. Live Test Cost Discipline
  XXVII. Operator-Configurable Tool Surface

Retained at component tier:
  XVII. Content Classification
  XVIII. Progressive Disclosure Contract
  XIX. Non-Extractable Core
  XX. Decomposition Mechanism Precedence
  XXI. Extraction Ordering
  XXVI. Meta-Testing for Parametrized Capabilities

Retired (number stability — never reuse):
  VI (Scripts Over Markdown) — retired v3.0.0
  X (Zen of Python Output) — retired v3.0.0

Why MAJOR: structural reorganization of the canonical constitution.
Existing readers' paths to relocated principles change. Per Principle II
the principle numerals stay stable across tiers; per the verbatim
preservation contract (spec §5) the principle bodies are byte-equal at
their new locations.

Suite admissions ratified at v4.0.0:
  - deliberator admitted Provisional (5 open remediations: V, XII,
    XXII, XXIV, XXVI) per CONFORMANCE.md.
  - deliberator admitted Provisional (4 open remediations: III, XIV,
    XVI, XXII) per CONFORMANCE.md.

Constitutional debt acknowledgment (per Fix B2):
  Tier 1 (Universal) carries grandfathered principles ratified
  pre-Inclusion-Criteria-gate (v2.4.0): I, II, III, IV, VII, VIII,
  IX, XI, XIV. XXVIII passed the post-gate criteria. Their
  constitutional validity is preserved per Principle II + the
  grandfathering provision; their post-gate compliance with current
  Inclusion Criteria is NOT re-evaluated by v4.0.0. Future targeted
  amendments may address individual principles' post-gate
  conformance as separate cycles.

Cross-tier weakening prohibition (per Fix B3):
  A lower-tier amendment weakens an upper-tier principle if any of:
  (i) implicit relief outside COMPLIANCE.md Part VI Relief pathway;
  (ii) interpretation language flipping existing-Satisfied to
  not-Satisfied; (iii) suite-specific adaptation bypassing a MUST.
  Enforcement: meta-arbiter review + tier-coherence linter
  flagged-words check + existing-implementation impact check on
  every cross-tier amendment. ../build-fractal/deliberator/CONSTITUTION.md
  § Cross-tier weakening prohibition documents the full operational
  definition.

Originating deliberation:
  deliberations/v4.0.0-tier-extraction-originating-2026-05-06/
  Verdict: Q1 APPROVE-AS-DRAFTED, Q2 ADMIT-PROVISIONAL, Q3 ADMIT-
  PROVISIONAL. All four P1 conditions discharged or translated to
  Provisional remediations.

Verification deliberations (both required per spec 067):
  - deliberations/v4.0.0-tier-extraction-self-consistency-2026-05-06/
    Verdict: PASS WITH FIXES — 7 fixes applied in spec v2.
  - deliberations/v4.0.0-tier-extraction-blind-2026-05-07/
    Verdict: PASS WITH FIXES — 5 fixes B1-B5 applied in spec v3.

Spec: specs/v4.0.0-tier-extraction/spec.md (v3 — both verifications passed).
Governance log: ../build-fractal/deliberator/CONSTITUTIONAL_CONVERSATIONS.md
                CONSTITUTIONAL_CONVERSATIONS.md (this repo)

Engine note: arbitration phase auto-arbitrator crashed on both
verification deliberations at dispatch (1ms / 2ms; bug logged in
project_deliberator_arbitration_crash_2026_05_06 memory). Manual
arbitrations performed grounded in synthesis + disputes per spec 067
balanced-arbiter standard. Both manual arbitrations recorded in their
respective resolution.md files. Engine fix tracked separately.

Discharges: build-fractal Phase A → Phase B in
            ~/.claude/plans/peaceful-stargazing-moler.md.

Prior amendment SIRs preserved below for audit trail (per Fix #3 + Fix B2).
-->

"""

COMPONENT_HEADER_INTRO = """# Deliberator OSS Constitution (Component Tier)

**Status:** RATIFIED — v4.0.0 (2026-05-07).
**Version:** 4.0.0
**Inherits from:**
- `../build-fractal/CONSTITUTION.md` (Tier 1 — Universal, v1.0.0)
- `../build-fractal/deliberator/CONSTITUTION.md` (Tier 2 — Suite, v1.0.0)

For Universal and Suite principles, see those documents. This document holds the **6 component-tier principles** specific to the deliberator repo, plus the canonical Governance section (which governs amendments at all tiers), plus retired-principle markers, plus the full audit trail of prior Sync Impact Reports.

---

## Retired

The following principles were retired in prior amendments. Their numerals are permanently retired per Principle II number-stability and MUST NOT be reused.

"""

COMPONENT_PRINCIPLES_INTRO = """

## Component Principles

The 6 principles below are byte-for-byte identical to their text in `CONSTITUTION.md` v3.2.3. They remain at component tier because they describe constraints on the OSS engine specifically, not on the suite as a whole.

"""


def main() -> int:
    if not CONSTITUTION.exists():
        print(f"ERROR: {CONSTITUTION} not found", file=sys.stderr)
        return 2

    text = CONSTITUTION.read_text()
    lines = text.split("\n")
    blocks = parse_principle_blocks(text)

    # Sanity: all 28 principle slots accounted for
    expected = TIER1_PRINCIPLES + TIER2_PRINCIPLES + COMPONENT_PRINCIPLES + RETIRED
    missing = [p for p in expected if p not in blocks]
    extra = [p for p in blocks if p not in expected]
    if missing or extra:
        print(f"ERROR: principle accounting mismatch. missing={missing} extra={extra}", file=sys.stderr)
        return 2

    # Build Tier 1 content
    tier1_bodies = []
    for roman in TIER1_PRINCIPLES:
        s, e = blocks[roman]
        tier1_bodies.append(slice_principle_body(lines, s, e))
    tier1_content = TIER1_PREAMBLE + "\n".join(tier1_bodies) + TIER1_FOOTER

    # Build Tier 2 content
    # XVI rationale (B5) inserts AFTER the XVI body block; we splice it inline
    tier2_bodies = []
    for roman in TIER2_PRINCIPLES:
        s, e = blocks[roman]
        body = slice_principle_body(lines, s, e)
        tier2_bodies.append(body)
        if roman == "XVI":
            tier2_bodies.append(TIER2_XVI_RATIONALE.lstrip("\n"))
    tier2_content = TIER2_PREAMBLE + "\n".join(tier2_bodies) + TIER2_FOOTER

    # Build component content
    # Includes: new SIR + all prior SIRs preserved + intro + retired markers + 6 principles + Governance verbatim
    prior_sirs = extract_existing_sirs(text)
    retired_blocks = []
    for roman in RETIRED:
        s, e = blocks[roman]
        retired_blocks.append(slice_principle_body(lines, s, e))
    component_principle_bodies = []
    for roman in COMPONENT_PRINCIPLES:
        s, e = blocks[roman]
        component_principle_bodies.append(slice_principle_body(lines, s, e))
    governance = extract_governance_section(text)

    component_content = (
        COMPONENT_NEW_SIR
        + prior_sirs
        + "\n\n"
        + COMPONENT_HEADER_INTRO
        + "\n".join(retired_blocks)
        + COMPONENT_PRINCIPLES_INTRO
        + "\n".join(component_principle_bodies)
        + "\n"
        + governance
    )

    # Write outputs
    TIER1.write_text(tier1_content)
    TIER2.write_text(tier2_content)
    CONSTITUTION.write_text(component_content)

    print(f"WROTE Tier 1: {TIER1} ({len(tier1_content):,} chars, {tier1_content.count(chr(10)):,} lines)")
    print(f"WROTE Tier 2: {TIER2} ({len(tier2_content):,} chars, {tier2_content.count(chr(10)):,} lines)")
    print(f"WROTE Component: {CONSTITUTION} ({len(component_content):,} chars, {component_content.count(chr(10)):,} lines)")

    # Verify byte-equality of relocated bodies via re-parsing
    original_bodies = {roman: slice_principle_body(lines, s, e) for roman, (s, e) in blocks.items()}

    new_tier1_text = TIER1.read_text()
    for roman in TIER1_PRINCIPLES:
        if original_bodies[roman].rstrip() not in new_tier1_text:
            print(f"FAIL: Tier 1 body for Principle {roman} not byte-equal at new location", file=sys.stderr)
            return 1

    new_tier2_text = TIER2.read_text()
    for roman in TIER2_PRINCIPLES:
        if original_bodies[roman].rstrip() not in new_tier2_text:
            print(f"FAIL: Tier 2 body for Principle {roman} not byte-equal at new location", file=sys.stderr)
            return 1

    new_component_text = CONSTITUTION.read_text()
    for roman in COMPONENT_PRINCIPLES + RETIRED:
        if original_bodies[roman].rstrip() not in new_component_text:
            print(f"FAIL: Component body for Principle {roman} not byte-equal at retained location", file=sys.stderr)
            return 1

    # Negative checks per spec §7
    relocated = TIER1_PRINCIPLES + TIER2_PRINCIPLES
    for roman in relocated:
        if original_bodies[roman].rstrip() in new_component_text:
            print(f"FAIL: Relocated principle {roman} body still appears in component file", file=sys.stderr)
            return 1

    print("VERIFIED: byte-equal preservation across all 28 principle slots; no orphans.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
