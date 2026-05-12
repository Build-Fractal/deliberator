# v4.1.0 Self-Consistency Verification — Three Questions

This is **stage 2 of 3** in the v4.1.0 verification protocol per spec 067 (originating ✓ → **self-consistency** → blind). The originating-stage arbitration (`../v4.1.0-persistence-contract-discipline-originating-2026-05-11/arbitration/resolution.md`) returned APPROVE-WITH-FIXES on all three originating questions. Eight conditions C1-C8 were applied in spec v2 (commit `3d00bda` on branch `spec/v4.1.0-persistence-contract-discipline`).

This stage examines a DIFFERENT class of question. Where the originating asked "does the amendment have merit?", self-consistency asks "given the amendment passes, does the rest of the constitution still cohere?" The agents in this stage default to **defending the status quo** — the bias to ratify is naturally strong by this stage, and the verification's job is to surface where ratification would create inconsistency, not validate it.

The agent composition for this stage is intentionally orthogonal to the originating stage:
- **No agent from the originating four** (pragmatist, devils-advocate, persistence-expert, ci-expert) reappears.
- All agents focus on internal coherence of the constitution as a whole, not merits of the amendment.

---

## Q1 — Internal contradiction check

**Question:** Does spec v2 § 4 (the amendment text) contradict, override, or implicitly modify any existing principle in Tier 1 `build-fractal/CONSTITUTION.md` or Tier 2 `build-fractal/conversus/CONSTITUTION.md`?

The amendment appends a five-point sub-clause to Tier 1 Principle II (Stable Interfaces). It mandates: declared schemas with version fields, mechanical CI enforcement (PR-required), versioning bump procedure, cross-product CONSUMER-CONTRACT.md surfaces, and explicit declaration scope (display text is not a stable contract).

For each existing principle, ask: does the new sub-clause as drafted (after C1-C8 are applied) clash with the principle's stated requirements, exceptions, or implicit invariants?

Particular vectors of concern:
- **Tier 1 Principle II's named-surface list** itself — the sub-clause adds "persistent state" as a surface category. Does this generalize cleanly or are there named surfaces (e.g., template variables, structural markers) where the new mechanical-enforcement rule would be over-restrictive?
- **Tier 1 Principle VII or VIII** (whichever covers experimentation / xfail surfaces) — the V un-xfail in conversus-oss is one of the deadlines this amendment binds. Does the amendment implicitly modify Principle VII/VIII's allowance for declared-xfail modes?
- **Tier 2 conversus-specific principles** (XII, XIII, XV, XVI, XXII, XXIII, XXIV, XXV, XXVII per the tier classification) — the amendment is universal, but conversus already has fine-grained suite-level rules about persistence in places (e.g., XXII session graphs, XXIV mode templates). Are there surfaces where the new universal rule duplicates or weakens a finer-grained Tier 2 rule?

Output: a per-principle finding. For each principle examined, state whether the amendment contradicts, overrides, modifies, or harmonizes with it — with evidence (quoted text from the principle vs. quoted text from spec v2 § 4). If no contradictions found anywhere, say so explicitly with the list of principles examined.

---

## Q2 — Tier placement coherence

**Question:** Does Tier 1 placement match the evidence base, or should this be a Tier 2 (Conversus Suite) amendment?

Spec v2 § 1 motivates the amendment with two concrete gaps:
1. Conversus-oss output parse contract lives in display text (V xfail evidence — 6 of 8 modes).
2. Spec-kit-orc adapter hardcodes paths/heading-grep/English error strings + state-files.md drifted from production data.

Both are conversus + spec-kit-orc surfaces. The amendment is positioned as Tier 1 (Universal — applies to every Build Fractal product) but the evidence is from two products in one product family.

Self-consistency questions:
- Are there cases where a non-conversus Build Fractal product would have a different appropriate persistence discipline that Tier 1 would over-constrain?
- Should the amendment instead live at Tier 2 with a forward-pointer noting "elevate to Tier 1 when a second product family's evidence accumulates"?
- Does the tier-classification draft in memory (`project_build_fractal_namespace.md`: "Universal: I, II, III, IV, VII, VIII, IX, XI, XIV, XXVIII") justify Principle II being Tier 1 to begin with? If yes, does the sub-clause inherit Tier 1 status automatically or require its own justification?

Output: a verdict (TIER-1-JUSTIFIED / TIER-2-MORE-APPROPRIATE / NEEDS-MORE-EVIDENCE) with concrete reasoning grounded in the existing tier-classification logic.

---

## Q3 — Override-with-rationale precedent fit

**Question:** Does the originating arbitration's invocation of override-with-rationale (against pragmatist's Q2 technology mandate) follow the established precedent pattern correctly, or does its uniform application risk shrinking other principles?

The established precedent (memory `feedback_amendment_override_precedent.md`): "When a blind verification verdict applies a strict reading whose uniform application would shrink existing ratified principles, override-with-rationale (logged in 3 places: SIR + governance log + spec status) is the correct response — not iterate, not demote."

The originating arbitration applied this precedent at Q2, overriding the pragmatist's "JSON Schema / XSD / Pydantic only" non-negotiable on three grounds: (a) the strict reading would shrink the spec § 3 non-goal (deliberately drafted flexibility), (b) three independent technical experts converged against the strict reading on different grounds, (c) the strict reading's substantive concern (gaming) is addressed by C5+C6 wording without the strict-reading remedy.

Self-consistency questions:
- Did the originating arbitration log the override-with-rationale in the three required places? (Resolution.md ✓; governance log entry — pending; spec v2 status — added in changelog section.) Audit each log location.
- Is the rationale grounding (the three converging arguments) substantively distinct from "majority vote" — i.e., a true rationale that survives the precedent's "is this just composition bias dressed up?" test?
- If this override pattern is applied uniformly to future amendments, does it create an erosion vector where minority strict-reading positions are systematically overridden against their substantive merits? Or is the precedent narrow enough (specifically: "strict reading would shrink existing ratified scope") that it cannot generalize that way?

Output: a verdict (PRECEDENT-CORRECTLY-APPLIED / PRECEDENT-OVERSTRETCHED / NEEDS-RATIFICATION-BIAS-DEFENSE) with specific evidence from arbitration/resolution.md vs. the established precedent text.

---

## Arbiter ruling format

For each question, one of:

**Q1 (Internal contradiction check):**
- PASS — no contradictions found across examined principles.
- PASS-WITH-CLARIFICATIONS — minor harmonization needed in spec v2; specify edits as numbered conditions D1, D2, ...
- FAIL — substantive contradiction exists; specify which principle and what evidence would change the verdict.

**Q2 (Tier placement coherence):**
- PASS — Tier 1 justified by the evidence.
- DEMOTE-TO-TIER-2 — evidence is conversus-family-only; amendment should live in Tier 2.
- PASS-WITH-FORWARD-POINTER — Tier 1 acceptable but the spec should note the elevation-evidence threshold.

**Q3 (Override-with-rationale precedent fit):**
- PASS — precedent correctly applied; logging complete or pending-and-tracked.
- PASS-WITH-LOGGING-FIX — precedent applied but one of the three logs is missing; specify which.
- FAIL-OVERSTRETCH — precedent invocation is not justified by the existing precedent text; recommend either iterate Q2 or accept pragmatist's position.

The combined verdict determines the next stage:
- Q1 PASS (any variant) + Q2 PASS (any variant) + Q3 PASS (any variant): proceed to **blind verification** with any specified fixes applied to produce spec v3.
- Any FAIL: spec returns to v2 review; blind verification does not run until the FAIL is addressed.
- DEMOTE-TO-TIER-2: spec rewrites under different tier; this verification stage re-runs at the new tier.
