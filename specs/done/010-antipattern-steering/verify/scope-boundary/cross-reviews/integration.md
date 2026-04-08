# Cross-Review of integration's Review

**Cross-reviewer**: scope-boundary
**Reviewing**: integration's review of spec 010-antipattern-steering
**Date**: 2026-03-20

---

## Dangerous Contradictions

### 1. Disagreement on the correct example path

**integration's position** (Missed Opportunities, bullet 1; Off-Base Assumptions, bullet 1; Recommendation 1): integration identifies `specs/001-antipattern-steering/examples/redundant-cache/` as a dead link and recommends determining the correct location, suggesting the numbering may have changed from 001 to 009/010 or the directory was never created. The recommendation says to "determine the correct location" without asserting a specific fix.

**scope-boundary's position** (Missed Opportunities, bullet 2; Recommendation 1): scope-boundary identifies the same broken path but asserts the correct path is `specs/010-antipattern-steering/examples/redundant-cache/`, verified via filesystem inspection. The directory exists and contains `README.md`, `STATUS.md`, `deliberations/`, and `specs/`.

**Why this matters**: integration's recommendation is cautious ("determine the correct location") when the answer is already determinable. The actual path `specs/010-antipattern-steering/examples/redundant-cache/` exists on disk. A recommendation to "determine" the path rather than fix it to the known-correct value risks unnecessary investigation cycles. Both reviews agree this is P1, but the proposed fix differs in specificity. This is not a deep contradiction -- both agree the path is broken and must be fixed -- but an implementer reading integration's recommendation alone might waste time searching when the answer is already available.

**Resolution**: Adopt scope-boundary's specific path fix (`specs/010-antipattern-steering/examples/redundant-cache/`) rather than integration's open-ended "determine the correct location." The directory exists and contains the referenced artifacts.

---

### 2. Severity and handling of STATUS.md constitution contradiction

**integration's position** (Missed Opportunities, bullet 4; Recommendation 2): integration rates the STATUS.md contradiction as **high** impact and recommends a P1 fix -- amend constitution Principle IV before shipping. integration proposes three options: remove the STATUS.md bullet, replace it with speckit-derived guidance, or add a supersession note. integration cites the Governance section (L196-199) as establishing that the constitution governs over specs unless deviation is explicitly documented, meaning agents will follow Principle IV's MUST mandate and ignore the antipattern.

**scope-boundary's position** (Missed Opportunities, bullet 1; Recommendation 2): scope-boundary also rates this as **high** impact but recommends a P2 fix -- acknowledge the tension with a note or follow-up spec, rather than amending Principle IV directly. scope-boundary's rationale: "the implementation correctly did not modify Principle IV without a spec" -- modifying a constitutional principle is itself a scope-boundary concern, as spec 010 did not authorize constitution amendments beyond adding the Known Antipatterns reference section.

**Why this matters**: These recommendations point in opposite directions on execution. integration says: amend the constitution now, before shipping, as P1. scope-boundary says: do not amend the constitution without a separate spec authorizing it, flag it for follow-up, P2. Both reviews agree the contradiction exists and is harmful. They disagree on whether fixing it is within spec 010's scope.

**Resolution**: This requires a deliberate decision. From a scope-boundary perspective, amending Principle IV is outside spec 010's scope -- the spec authorizes "adding a brief instruction to conversus SKILL.md or templates" (spec.md L109) and the plan adds a Known Antipatterns section to the constitution. Removing or rewriting a constitutional principle is a governance action requiring its own spec (per constitution L201-202: amendments require documentation of change, rationale, and impact). However, integration's concern about contradictory MUST-level instructions is valid and urgent. The recommended middle ground: add an explicit note to Principle IV (e.g., "See redundant-cache in antipatterns/catalog.md for guidance on when STATUS.md maintenance is counterproductive") that reconciles without removing the principle, and file a follow-up spec for full resolution. This stays within additive scope while neutralizing the contradiction for agents.

---

## Tensions

### 1. Scope of T006 (constitution update) -- integration accepts it, scope-boundary flags it

**integration's position** (Alignment, bullet 5): integration lists the constitution Known Antipatterns section as an alignment item, noting it "correctly references `antipatterns/catalog.md` as the catalog location and `specs/010-antipattern-steering/contracts/catalog-format.md` as the governing contract." integration treats T006 as a properly integrated artifact.

**scope-boundary's position** (Missed Opportunities, bullet 3; Recommendation 3): scope-boundary flags T006 as lacking spec-level traceability. The spec at L109 limits integration points to "SKILL.md or templates." The constitution update has no acceptance scenario. scope-boundary recommends either expanding the spec's assumptions or adding an acceptance scenario for the constitution update.

**Analysis**: Both positions are defensible. integration is right that the constitution update is functionally sound and well-integrated. scope-boundary is right that it has no formal traceability to the spec. The tension is between integration coherence (does the system work correctly?) and scope rigor (does every implementation task trace to a spec requirement?). For a verification pass, scope-boundary's concern should be recorded as a traceability gap even if no code change is needed.

### 2. Contract "Exact wording" divergence -- priority difference

**integration's position** (Missed Opportunities, bullet 2; Recommendation 3): integration rates the SKILL.md step 2 divergence from the contract's "Exact wording" as **medium** impact and recommends a P2 contract update. integration correctly identifies that the contract says "Exact wording" (L91) but the actual SKILL.md step 2 contains additional keyword retrieval guidance not in the contract.

**scope-boundary's position**: scope-boundary does not flag this specific issue. scope-boundary's review notes that the keyword retrieval guidance satisfies FR-007 and FR-008 (Alignment, bullet 6) and treats the SKILL.md step 2 extension as a correct implementation of the P2 contextual retrieval user story.

**Analysis**: integration has the stronger position here. If the contract claims "Exact wording" and the actual wording differs, that is a contract violation regardless of whether the divergence is beneficial. scope-boundary should have caught this. The fix is straightforward: either update the contract's step 2 to match SKILL.md or remove the "Exact wording" label and replace it with "Minimum required content" or similar. This does not affect scope boundaries -- it is an internal consistency issue.

### 3. Maintenance section heading ambiguity -- different treatment

**integration's position** (Missed Opportunities, bullet 3; Recommendation 4-5): integration identifies two related issues: (a) the contract template does not include a Maintenance section, and (b) the Maintenance heading uses H2 like entry headings, making entries indistinguishable from Maintenance by heading level alone. integration recommends adding the Maintenance section to the contract and adding a machine-readable delimiter.

**scope-boundary's position**: scope-boundary does not flag either issue. scope-boundary treats the Maintenance section as an expected artifact of T009 and confirms it documents add/deprecate workflows correctly (Alignment, bullet 5).

**Analysis**: integration raises a valid integration concern. From a scope-boundary perspective, adding a Maintenance section was authorized by T009 and is within scope. But the contract's claim to define "the exact structure" (L7) without including the Maintenance section is a gap integration correctly identified. This is not a scope violation -- it is an underdocumented extension. scope-boundary should acknowledge this as a contract completeness issue, not a scope overshoot.

### 4. Constitution version bump

**integration's position** (Recommendation 8): integration recommends bumping the constitution version from 1.1.0 to 1.2.0, citing the Governance section's versioning rules (L203: MINOR for "new principles or material expansions"). integration rates this P3.

**scope-boundary's position**: scope-boundary does not address constitution versioning. The Sync Impact Report at the top of constitution.md (L1-16) still reflects the 1.0.0 to 1.1.0 transition and does not mention the antipattern catalog addition.

**Analysis**: integration is correct that the constitution's own rules require a version bump for material expansions. Adding a Known Antipatterns section (L179-192) is a material expansion. However, from a scope-boundary perspective, this depends on whether spec 010 authorized constitution amendments at all (see Dangerous Contradiction 2). If the constitution update is accepted as in-scope, then the version bump is a necessary corollary. scope-boundary should have flagged the missing version bump as evidence that the constitution update was not fully thought through in the plan.

---

## Safe Agreements

### 1. Broken example path is the highest-priority fix

Both reviews identify the broken path reference to `specs/001-antipattern-steering/examples/redundant-cache/` as a P1 issue that must be resolved before shipping. Both cite FR-004 (self-contained entries) and SC-004 (real incident references). integration identifies six files affected; scope-boundary identifies the catalog plus tasks.md T003 and T011. The scope of affected files differs slightly (integration includes quickstart.md and plan.md; scope-boundary focuses on runtime artifacts), but both agree the path is broken and must be corrected.

### 2. STATUS.md contradiction exists and is harmful

Both reviews identify the contradiction between constitution Principle IV (L73-75) mandating STATUS.md maintenance and the redundant-cache antipattern condemning the same practice. Both rate it high impact. They disagree on resolution approach (see Dangerous Contradiction 2) but agree on the existence and severity of the problem.

### 3. Catalog entry conforms to the format contract

Both reviews confirm that the `redundant-cache` entry follows the contract's field order, includes all required fields, and has synchronized keywords between the Summary Index and entry body. integration's Alignment bullet 4 and scope-boundary's Alignment bullet 4 (data model fidelity) reach the same conclusion.

### 4. SKILL.md change is correctly positioned and additive

Both reviews confirm that the Antipattern Check instruction is inserted after Step 1 (config parsing), before Step 2 (output directory creation), and that no existing SKILL.md content was modified. integration's Alignment bullet 2 confirms the 4-step workflow is preserved; scope-boundary's Alignment bullet 2 confirms the change is a pure insertion.

### 5. Catalog path references are consistent across SKILL.md and constitution

Both reviews verify that SKILL.md, constitution.md, and the catalog itself all reference `antipatterns/catalog.md` as the catalog location. integration's Alignment bullet 1 and scope-boundary's Alignment bullet 3 confirm this.

### 6. Append-only structure is correctly implemented

Both reviews confirm the catalog supports append-only extension per FR-010. integration's Alignment bullet 6 (maintenance procedures) and scope-boundary's Alignment bullet 5 both validate the Maintenance section's add/deprecate workflows.

### 7. T011 validation task is unreliable

Both reviews note that T011 is marked complete (`[x]`) but references the broken path `specs/001-antipattern-steering/examples/redundant-cache/`. integration explicitly recommends unchecking T011 (Recommendation 6); scope-boundary recommends fixing the path reference in T011 (Recommendation 4). Both agree the validation task as written is not trustworthy.

---

## Summary Assessment

integration's review is thorough and well-sourced. It identifies several issues that scope-boundary missed: the contract "Exact wording" divergence, the Maintenance section heading ambiguity, the missing constitution version bump, and the quickstart broken reference. These are legitimate integration concerns that complement rather than conflict with scope-boundary's analysis.

The two dangerous contradictions -- the correct example path (resolvable by using the filesystem-verified path) and the STATUS.md constitution amendment scope (resolvable by a scoped acknowledgment note rather than full principle rewrite) -- are both tractable. Neither requires fundamental rethinking of the implementation.

integration's most valuable unique contribution is the observation that the constitution's Governance section (L196-199) creates a formal precedence rule that makes the contradiction actively harmful: agents will follow the MUST-level constitution mandate over the catalog's guidance. This strengthens the case for at minimum an inline reconciliation note, even if a full amendment is deferred.
