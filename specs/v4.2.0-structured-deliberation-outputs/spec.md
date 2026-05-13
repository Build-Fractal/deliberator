# Feature Specification: v4.2.0 Structured Deliberation Outputs (JSON Schema)

**Feature ID:** `v4.2.0-structured-deliberation-outputs`
**Created:** 2026-05-12
**Status:** **v3 / post-self-consistency-arbitration / pre-self-consistency-rerun** (2026-05-13)
**Depends On:** v4.1.0-persistence-contract-discipline (Tier 2 Principle XXVIII must be ratified; that ratification — commit `551f647` in `clariti-care/payer-index-mono`, `build-fractal/conversus/CONSTITUTION.md` L490-644 — is the doctrinal anchor this spec implements).
**Governed by:** `https://github.com/clariti-care/payer-index-mono/blob/main/build-fractal/conversus/GOVERNANCE.md` § Pathway Taxonomy (**MINOR** pathway — additive component-tier discipline; no existing principle removed, renamed, or substantively re-scoped).
**Pathway:** MINOR
**Tier target:** **Component (Tier 3)** — conversus-oss-specific implementation of Tier 2 Principle XXVIII. Tier placement was **TIER-3-CONFIRMED** by the originating arbitration (`deliberations/v4.2.0-structured-deliberation-outputs-originating-2026-05-12/arbitration/resolution.md` Q3).

---

## Changelog: v2 → v3

The **self-consistency arbitration** (2026-05-13, `deliberations/v4.2.0-structured-deliberation-outputs-self-consistency-2026-05-13/arbitration/resolution.md`) returned **PASS-WITH-CLARIFICATIONS** on Q1 and Q2 and **FAIL-CONTRADICTION on Q3**. The load-bearing finding was that v2 § 5.1's blocking-validation language ("the engine logs the error array to the deliberation event stream and aborts the phase (does not write the malformed file)") **directly contradicts ratified Tier 2 Principle V** (CONSTITUTION.md L76-78: "Output validation … emits warnings for malformed output but does NOT block file writes. Malformed output is better than no output"). All four self-consistency agents independently identified this. Per cross-tier weakening prohibition (CONSTITUTION.md L685), a component-tier amendment cannot grant relief from a Tier 2 principle.

v3 applies fifteen D-conditions to resolve the contradiction and close the Q1+Q2 clarifications:

| D# | Priority | Summary | Lands in |
|---|---|---|---|
| D1 | P1 (Q3-blocking) | **Rewrite § 5.1 as non-blocking, warning-based validation.** Engine writes the file unconditionally; on schema violation it logs the `ValidatorError` array and emits a prominent warning. CI gates block at PR-time; engine writes never block at write-time. | § 5.1, § 5.4 |
| D2 | P1 (Q3-blocking) | Strike the Principle II citation in § 9.1; replace with temporal-constraint rationale. | § 9.1 |
| D3 | P1 | New § 9.2 — explicit cross-tier weakening assessment against CONSTITUTION.md L649-664 criteria (i), (ii), (iii). | § 9.2 (new) |
| D4 | P1 | Replace "RECURSION-EXEMPTED" language with **temporal-constraint framing** ("v4.2.0 verification outputs predate JSON schema availability by construction") throughout § 9.1, § 12 OQ5, § 13. Mirrors v4.1.0's temporal-vs-membership-universality precedent. | § 9.1, § 12, § 13 |
| D5 | P1 | Add **anti-precedent language**: this temporal-constraint accommodation applies only to specs that ratify the schema infrastructure they would otherwise be required to use. Future schema-related amendments are NOT exempt from using existing validation infrastructure. | § 9.1, § 9.2 |
| D6 | P2 | Post-cliff-date ratification handling: if ratification occurs after 2026-12-01, T4 is treated as in-effect at ratification with T1-T3 collapsed. | § 11 |
| D7 | P2 | Schema-advancement-authority — who decides the `1.0.0-rc.1` → `1.0.0` bump after 30 days clean operation, and by what criteria. | § 4.8 |
| D8 | P2 | Forward-promotion pathway — one paragraph for the case where a future conversus-* sibling produces deliberation-like artifacts, referencing GOVERNANCE.md pattern-promotion. | § 9.3 (new) |
| D9 | P1 | Declare `engine/schema/v1/` location in `conversus-oss/CONFORMANCE.md` per XXVIII sub-clause 1 textual requirement (CONSTITUTION.md L505-510). | § 4.0 (new), § 6.1 |
| D10 | P1 | Add README.md and CLAUDE.md links to CONSUMER-CONTRACT.md per XXVIII sub-clause 1 (CONSTITUTION.md L508-510 — "BOTH"). | § 6.1 |
| D11 | P1 | Complete CONSUMER-CONTRACT.md content specification per XXVIII sub-clause 5 — explicitly name schema surfaces and state the stability guarantee. | § 7.1 (new) |
| D12 | P1 | Bidirectional drift-detection CI per XXVIII sub-clause 2 — any change to `engine/schema/v1/*.schema.json` triggers re-validation of all existing producer code outputs under the new schema. Warning-only at write-time (D1 consistency); mechanically detected at CI-time. | § 5.4 |
| D13 | P2 | Reframe § 5.1's <100ms language as **implementation discipline**, not constitutional mandate. | § 5.1 |
| D14 | P2 | Document fixture validation scope coverage per XXVIII sub-clause 2 — fixtures cover field presence, types, value constraints, enum violations (three fixture types minimum). | § 5.3 |
| D15 | P2 | Specify CI detection for schema-version-not-bumped-on-schema-edit per XXVIII sub-clause 3 ("silent format changes are a violation"). | § 5.4 |

**D1 is the load-bearing reversal.** v2's framing — "aborts the phase, does not write the malformed file" — is **inverted** in v3: validation is advisory, runs at write-time, emits warnings into the deliberation event stream, but the file is **always written**. Mechanical enforcement bite is preserved at the PR-required CI gate (per XXVIII sub-clause 2), which DOES block merge on validation failure. The constitutional pillar Principle V protects ("malformed output is better than no output") is preserved at the engine's write path.

**D4 + D5 are the load-bearing reframing.** v2's "RECURSION-EXEMPTED" verdict structurally resembled the v4.1.0 override-with-rationale stretch that v4.1.0 self-consistency rejected when applied uniformly. The self-consistency arbitration identified that this accommodation can be precedent-safe **only if reframed as temporal constraint** (mirroring v4.1.0's temporal-vs-membership distinction): v4.2.0 verification outputs cannot conform to a schema that does not yet exist (bootstrap paradox; the schemas are produced *by this very spec*). v3 reframes "exemption" → "temporal scope precedes existence," and the anti-precedent language (D5) explicitly contains the accommodation to this one-time bootstrap and bars future schema-related amendments from invoking the same shape.

---

## Changelog: v1 → v2 (historical, retained for traceability)

The originating arbitration (2026-05-13) returned APPROVE-WITH-FIXES on Q1 and Q2 with conditions C1-C10, and TIER-3-CONFIRMED + RECURSION-EXEMPTED on Q3. v2 applies all ten conditions verbatim. The single most consequential change is **C1**: the canonical schema language and file format switch from XML + XSD to **JSON + JSON Schema**. All four originating agents converged independently on this.

| C# | Priority | Summary | Lands in |
|---|---|---|---|
| C1 | P1 | Canonical format flipped from XML+XSD → JSON + JSON Schema. Namespace becomes a JSON Schema `$id` URI. Validator architecture uses Python `jsonschema`. | § 4, § 5.1, § 7 |
| C2 | P1 | Validator runtime budget: **<100ms per output**. If a validator implementation exceeds this, the validator is the bug, not the schema. | § 5.1 |
| C3 | P1 | Dependency-ordered template migration with one-mode pilot (cooperative first). | § 11 |
| C4 | P1 | Semantic equivalence testing as CI gate — re-render structured output back to markdown and diff against the markdown the original template would have produced. | § 11.1 |
| C5 | P2 | Tiered/staged rollout: parallel-format support → advisory CI → blocking CI → markdown deprecation. | § 11, § 11.1 |
| C6 | P1 | Envelope identity-field expansion: `deliberation_stage`, `engine_version`, `source_commit`. | § 4.1 |
| C8 | P2 | SemVer bump qualification: MAJOR / MINOR / PATCH definitions with consumer-impact qualification. Adding REQUIRED fields is MAJOR. | § 4.8 |
| C9 | P2 | Validator error-object schema (`field_path`, `error_code`, `human_message`, `expected_type`, `actual_value`, `suggested_fix`). | § 4.9 (new), § 5.1 |
| C10 | P3 | Initial schema version is `1.0.0-rc.1`. Bump to `1.0.0` after one ratification cycle of clean operation. | § 4.8 |

(C7 is subsumed by C1 in the arbitration's own consolidation; the Q2-axis restatement is folded into § 4.)

---

## 1. Motivation

Tier 2 Principle XXVIII ("Persistence Contract Discipline") was ratified 2026-05-12 (`build-fractal/conversus/CONSTITUTION.md` L490-644) with a universal 2026-12-01 remediation deadline for all conversus-suite products. The principle mandates: declared schemas with `schema_version` (SemVer), mechanical CI enforcement, versioning bump procedure, cross-product `CONSUMER-CONTRACT.md` files declaring stable surfaces, and explicit declaration scope. Schema declaration without mechanical enforcement is itself a violation.

Conversus-oss's load-bearing persistent state surface is the **deliberation output set** — six output types produced per phase per deliberation. These outputs are persisted to disk under `deliberations/{deliberation-id}/`, consumed by:
- Subsequent phases within the same deliberation (e.g., phase 5 synthesis reads phases 1-4 outputs);
- The arbiter's grep-based triggers (e.g., `disputes_remain`);
- The orchestrator adapter (`scripts/dispatch/adapters/tool/conversus.sh`), which currently parses markdown headings to extract verdicts;
- Human readers reviewing the audit trail.

Today the contract between producer (agent prose) and consumers (engine triggers, downstream phases, orchestrator adapter) lives in **display text** — markdown headings, prose patterns, and parser-grep regexes — and silently short-circuits when prose drifts. This spec is the first concrete implementation of Principle XXVIII for conversus-oss.

### 1.1 Three recurring production bugs this spec addresses

These are the load-bearing motivation. The spec must cite each one as an existence proof that the current display-text contract is broken.

**Bug A — Phase 5 prompt-overflow crash (recurring).** Synthesis prompt assembles all phase 1-4 outputs as free-form markdown concatenation. Two production incidents documented:
- 2026-05-06 arbitration silent-failure: synthesis prompt exceeded ~230K chars, arbitration phase dispatched then crashed silently in ~1ms (memory: `project_conversus_arbitration_crash_2026_05_06.md`). Phases 1-5 succeeded; only arbitration crashed at dispatch.
- v4.1.0 originating deliberation (2026-05-11): same class of overflow, different manifestation — rate-limit response surfaced rather than silent crash, but root cause identical (unbounded prose concatenation).

Both incidents stem from synthesis output being unbounded prose. Structured JSON output constrains the prompt assembly path: the engine can serialize only specific fields (e.g., `verdict` + `conditions` without `rationale` prose), bounding synthesis prompt size deterministically.

**Bug B — Phase 2 cross-review persistence quirk.** Engine warnings show cross-review files expected at `{agent}/cross-reviews/{other-agent}.md` sometimes don't persist to disk; downstream phases consume "in-memory" cross-reviews that aren't on disk. Format-contract drift between agents' emitted markdown structure and engine's file-storage expectations: agents emit headings/structure that the engine's writer doesn't recognize as a valid cross-review, so the writer silently elides them. This is a class-of-bug expression of "contract lives in display text" — the storage layer's parse contract is undocumented and grep-fragile.

**Bug C — Phase 6 `disputes_remain` trigger silently missed.** The v4.1.0 blind-verification synthesis used "Critical Unresolved Tensions" terminology where the engine grep-matches for `DISPUTES_BEGIN`/`DISPUTES_END` markers. Arbiter didn't fire even though tensions existed; manual arbitration was required (memory: `project_conversus_pr23_meta_cl.md`, "manual challenge-loop orchestration pattern"). **This bug is the cleanest example of why structural schema enforcement matters** — an agent emitting prose that happens not to match the engine's parser regex causes the engine to silently skip the dispute-resolution phase. Under JSON Schema, the trigger becomes `len(synthesis["disputes"]) > 0` — structural, not regex.

**Real-time confirmation.** The originating arbitration of this very spec (2026-05-13) was produced *manually* because Phase 6 didn't fire — the Phase 5 synthesizer wrote "Remaining Disputes" rather than the engine's expected marker pair. That is Bug C reproducing in the deliberation tasked with verifying the bug's fix. See `deliberations/v4.2.0-structured-deliberation-outputs-originating-2026-05-12/arbitration/resolution.md` "Process Note".

### 1.2 Doctrinal anchor

Principle XXVIII sub-clause 1 mandates declared schemas in a discoverable location. Sub-clause 2 mandates mechanical CI enforcement. Sub-clause 3 mandates `schema_version` (SemVer by default). Sub-clause 4 mandates `CONSUMER-CONTRACT.md` declaring stable surfaces consumed by cross-product code. Sub-clause 5 mandates explicit declaration of display-text surfaces (or migration off them). This spec satisfies all five sub-clauses for the conversus-oss deliberation output set.

---

## 2. Goals

1. **Single JSON Schema family** defining all six conversus deliberation output types, with a common envelope (agent identity, deliberation context, timestamp, target file refs, `schema_version`, stage/engine/commit provenance) plus per-type bodies. Schema `$id` base: `https://build-fractal.org/conversus/schema/v1/`.
2. **`schema_version` field on every output**, populated by the engine at write time, conforming to Principle XXVIII sub-clause 3 (SemVer with documented total ordering). Initial release: `1.0.0-rc.1` per C10.
3. **PR-required CI gate** validating every agent output against the schema before commit, per Principle XXVIII sub-clause 2. The gate runs in `conversus-oss` CI on every PR that touches `deliberations/**` or `engine/**`; failures block merge.
4. **Backward-compatibility / migration path** for existing markdown-format deliberation outputs. The v4.1.0 audit trail (4 deliberations, ~150 markdown files) must remain readable. Migration strategy in § 11.
5. **Human-readable rendering path.** JSON outputs are accompanied by an engine-generated `.md` companion so the audit trail is human-readable without specialized tooling. Default: JSON is canonical; companion `.md` is rendered-for-humans, regenerable from JSON.
6. **`CONSUMER-CONTRACT.md`** at conversus-oss repo root declaring the JSON Schema as a stable surface consumed by the orchestrator adapter (and any future conversus-suite consumer), per Principle XXVIII sub-clause 4.

---

## 3. Non-goals

- **Not** proposing structured-schema discipline for non-deliberation conversus artifacts (engine state, provider auth tokens, evaluation results, mode templates). Those are separate persistent state surfaces with their own contract decisions to make.
- **Not** mandating JSON Schema for `CONSTITUTION.md`, `CONFORMANCE.md`, `COMPLIANCE.md`, or `GOVERNANCE.md`. Constitutional documents have their own conventions (markdown with structured headings) and are out of scope.
- **Not** requiring agents to write JSON directly in their prose. Agents emit structured prose in defined slots; the engine wraps in a JSON envelope on write. Agent prompts change; agent output format from the agent's perspective stays close to current prose conventions (with explicit field markers).
- **Not** replacing the engine dispatch architecture, the phase pipeline, or the agent abstraction. This spec changes only the format of the artifacts written to disk and consumed by downstream phases + external consumers.
- **Not** retroactively re-emitting historical deliberation outputs in JSON. The migration path (§ 11) is forward-only: new deliberations use JSON; historical markdown deliberations remain as-is and continue to render readably.

---

## 4. Schema

### 4.0 Schema location declaration (D9)

Per Principle XXVIII sub-clause 1 (CONSTITUTION.md L505-510), the schema location MUST be declared in the producer repo's `CONFORMANCE.md` and linked from both `README.md` AND `CLAUDE.md`. v3 satisfies this textually:

- **Canonical location:** `engine/schema/v1/*.schema.json` inside `Build-Fractal/conversus-oss/`.
- **Declared in:** `conversus-oss/CONFORMANCE.md` Persistence-Contract row (updated per § 6.1 D9). The row names the directory, the file-naming convention (`{output-type}.schema.json` + `envelope.schema.json` + `validator-error.schema.json`), and the `$id` URI base.
- **Linked from:** `conversus-oss/README.md` and `conversus-oss/CLAUDE.md` "Persistence Contract" sections (added per § 6.1 D10), each linking to `CONSUMER-CONTRACT.md` (which in turn links to the schema directory).

This satisfies XXVIII sub-clause 1's "discoverable location" + "linked from BOTH" textual requirements.

The canonical schema language is **JSON Schema** (Draft 2020-12). The canonical wire format on disk is **JSON** (`.json` files). All schema files live under `engine/schema/v1/` and are addressable by `$id` URIs anchored at `https://build-fractal.org/conversus/schema/v1/`. This choice — both schema language and file format are JSON — was unanimously converged on by all four originating-deliberation agents (per `deliberations/v4.2.0-structured-deliberation-outputs-originating-2026-05-12/arbitration/resolution.md` Q2 Per-axis finding 5: "XML's CDATA-escaping burden on agent prose containing `<`, `>`, `&` characters; JSON Schema's Python `jsonschema` library being a near-universal dependency; JSON Schema's superior validation error messages; ubiquitous shell-tool parsing (`jq`) vs xmllint specialized tooling"). The previous XSD strawman is retired.

### 4.1 Common envelope

Every output document is a JSON object with the following envelope fields wrapping a `body` object whose shape is determined by `output_type`:

```json
{
  "$schema": "https://build-fractal.org/conversus/schema/v1/envelope.schema.json",
  "schema_version": "1.0.0-rc.1",
  "output_type": "review",
  "agent_name": "pragmatist",
  "deliberation_id": "v4.2.0-structured-deliberation-outputs-originating-2026-05-12",
  "deliberation_stage": "originating",
  "engine_version": "0.7.3",
  "source_commit": "551f647",
  "phase_iteration": 1,
  "timestamp": "2026-05-12T15:42:08Z",
  "target_files": ["specs/v4.2.0-structured-deliberation-outputs/spec.md"],
  "body": { /* per-type body */ }
}
```

The envelope JSON Schema (`engine/schema/v1/envelope.schema.json`):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://build-fractal.org/conversus/schema/v1/envelope.schema.json",
  "title": "Conversus Deliberation Output Envelope",
  "type": "object",
  "required": [
    "schema_version", "output_type", "agent_name",
    "deliberation_id", "deliberation_stage", "engine_version",
    "source_commit", "timestamp", "body"
  ],
  "properties": {
    "schema_version": {
      "type": "string",
      "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+(-[A-Za-z0-9.-]+)?$"
    },
    "output_type": {
      "type": "string",
      "enum": ["review", "cross-review", "revision", "disputes", "synthesis", "arbitration"]
    },
    "agent_name": { "type": "string", "minLength": 1 },
    "deliberation_id": { "type": "string", "minLength": 1 },
    "deliberation_stage": {
      "type": "string",
      "enum": ["originating", "self-consistency", "blind"]
    },
    "engine_version": { "type": "string", "minLength": 1 },
    "source_commit": { "type": "string", "minLength": 4 },
    "phase_iteration": { "type": "integer", "minimum": 1 },
    "timestamp": { "type": "string", "format": "date-time" },
    "target_files": {
      "type": "array",
      "items": { "type": "string" }
    },
    "body": { "type": "object" }
  },
  "allOf": [
    { "if": { "properties": { "output_type": { "const": "review" } } },
      "then": { "properties": { "body": { "$ref": "review.schema.json" } } } },
    { "if": { "properties": { "output_type": { "const": "cross-review" } } },
      "then": { "properties": { "body": { "$ref": "cross-review.schema.json" } } } },
    { "if": { "properties": { "output_type": { "const": "revision" } } },
      "then": { "properties": { "body": { "$ref": "revision.schema.json" } } } },
    { "if": { "properties": { "output_type": { "const": "disputes" } } },
      "then": { "properties": { "body": { "$ref": "disputes.schema.json" } } } },
    { "if": { "properties": { "output_type": { "const": "synthesis" } } },
      "then": { "properties": { "body": { "$ref": "synthesis.schema.json" } } } },
    { "if": { "properties": { "output_type": { "const": "arbitration" } } },
      "then": { "properties": { "body": { "$ref": "arbitration.schema.json" } } } }
  ]
}
```

Required fields (per C6): `schema_version`, `output_type`, `agent_name`, `deliberation_id`, `deliberation_stage`, `engine_version`, `source_commit`, `timestamp`, `body`. Optional: `phase_iteration` (omitted for single-iteration phases), `target_files` (omitted for synthesis/arbitration where the target is the deliberation as a whole).

The three envelope identity fields added by C6 — `deliberation_stage`, `engine_version`, `source_commit` — make every output traceable to its exact production context (which stage of the four-stage methodology, which engine build, which spec commit was under review).

### 4.2 `review.schema.json` — Phase 1, initial review per agent

```json
{
  "$id": "https://build-fractal.org/conversus/schema/v1/review.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["summary_assessment", "strengths", "concerns", "questions", "recommendation"],
  "properties": {
    "summary_assessment": { "type": "string", "minLength": 1 },
    "strengths": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "text"],
        "properties": {
          "id": { "type": "string", "pattern": "^S[0-9]+$" },
          "text": { "type": "string", "minLength": 1 }
        }
      }
    },
    "concerns": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "severity", "text"],
        "properties": {
          "id": { "type": "string", "pattern": "^C[0-9]+$" },
          "severity": { "enum": ["blocking", "substantive", "nit"] },
          "text": { "type": "string", "minLength": 1 }
        }
      }
    },
    "questions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "text"],
        "properties": {
          "id": { "type": "string", "pattern": "^Q[0-9]+$" },
          "text": { "type": "string", "minLength": 1 }
        }
      }
    },
    "recommendation": {
      "enum": ["APPROVE-AS-DRAFTED", "APPROVE-WITH-FIXES", "BLOCK", "ABSTAIN"]
    }
  }
}
```

`severity` is an enum: `blocking` (must-fix for ratification), `substantive` (should-fix), `nit` (cosmetic). The engine routes blocking concerns into the dispute set for phase 2.

### 4.3 `cross-review.schema.json` — Phase 2, agent X reviews agent Y's review

```json
{
  "$id": "https://build-fractal.org/conversus/schema/v1/cross-review.schema.json",
  "type": "object",
  "required": ["reviewing_agent", "agreement_points", "disagreement_points", "new_concerns_raised"],
  "properties": {
    "reviewing_agent": { "type": "string", "minLength": 1 },
    "agreement_points": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["ref", "text"],
        "properties": {
          "ref": { "type": "string" },
          "text": { "type": "string" }
        }
      }
    },
    "disagreement_points": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["ref", "stance", "our_position", "their_position"],
        "properties": {
          "ref": { "type": "string" },
          "stance": { "enum": ["disagree", "partial-disagree"] },
          "our_position": { "type": "string" },
          "their_position": { "type": "string" }
        }
      }
    },
    "new_concerns_raised": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "severity", "text"],
        "properties": {
          "id": { "type": "string", "pattern": "^CR[0-9]+$" },
          "severity": { "enum": ["blocking", "substantive", "nit"] },
          "text": { "type": "string" }
        }
      }
    }
  }
}
```

`reviewing_agent` names whose review is being cross-reviewed; the wrapper `agent_name` in the envelope names the cross-reviewer. The `ref` on disagreement / agreement points lets phase 5 trace dispute lineage back to phase 1 origins. **This fixes Bug B**: cross-review files have a deterministic structure the engine writer recognizes; format drift can't elide them.

### 4.4 `revision.schema.json` — Phase 3, agent updates own position

```json
{
  "$id": "https://build-fractal.org/conversus/schema/v1/revision.schema.json",
  "type": "object",
  "required": ["iteration", "position_changes", "updated_recommendation"],
  "properties": {
    "iteration": { "type": "integer", "minimum": 1 },
    "position_changes": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["ref", "delta", "prior", "revised", "triggered_by"],
        "properties": {
          "ref": { "type": "string" },
          "delta": { "enum": ["strengthened", "softened", "withdrawn", "unchanged"] },
          "prior": { "type": "string" },
          "revised": { "type": "string" },
          "triggered_by": { "type": "string" }
        }
      }
    },
    "updated_recommendation": {
      "enum": ["APPROVE-AS-DRAFTED", "APPROVE-WITH-FIXES", "BLOCK", "ABSTAIN"]
    }
  }
}
```

`iteration` matches `phase_iteration` on the envelope; multiple revision iterations are supported (e.g., `revision.json` + `revision_2.json`).

### 4.5 `disputes.schema.json` — Phase 4, agent consolidates remaining disagreements

```json
{
  "$id": "https://build-fractal.org/conversus/schema/v1/disputes.schema.json",
  "type": "object",
  "required": ["disputes"],
  "properties": {
    "disputes": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "severity", "topic", "our_position", "opposing_positions", "proposed_resolution", "fallback_if_unresolved"],
        "properties": {
          "id": { "type": "string", "pattern": "^D[0-9]+$" },
          "severity": { "enum": ["blocking", "substantive"] },
          "topic": { "type": "string" },
          "our_position": { "type": "string" },
          "opposing_positions": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["agent", "stance"],
              "properties": {
                "agent": { "type": "string" },
                "stance": { "type": "string" }
              }
            }
          },
          "proposed_resolution": { "type": "string" },
          "fallback_if_unresolved": { "type": "string" }
        }
      }
    }
  }
}
```

### 4.6 `synthesis.schema.json` — Phase 5, single agent integrates all prior outputs

```json
{
  "$id": "https://build-fractal.org/conversus/schema/v1/synthesis.schema.json",
  "type": "object",
  "required": ["agreement_areas", "disputes", "emergent_patterns", "recommendation_to_arbiter"],
  "properties": {
    "agreement_areas": {
      "type": "array",
      "items": { "type": "string" }
    },
    "disputes": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "severity", "topic", "positions", "synthesizer_assessment"],
        "properties": {
          "id": { "type": "string", "pattern": "^D[0-9]+$" },
          "severity": { "enum": ["blocking", "substantive"] },
          "topic": { "type": "string" },
          "positions": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["agent", "stance"],
              "properties": {
                "agent": { "type": "string" },
                "stance": { "type": "string" }
              }
            }
          },
          "synthesizer_assessment": { "type": "string" }
        }
      }
    },
    "emergent_patterns": {
      "type": "array",
      "items": { "type": "string" }
    },
    "recommendation_to_arbiter": { "type": "string" }
  }
}
```

**This fixes Bug C**: the engine's `disputes_remain` trigger becomes the JSON-path expression `len([d for d in synthesis["body"]["disputes"] if d["severity"] == "blocking"]) > 0`. Structural, not regex. No prose drift can hide a dispute from the trigger.

**This also fixes Bug A**: the engine's synthesis-prompt assembler can serialize only specific subtrees per downstream consumer — e.g., the arbitration prompt receives `disputes` + `recommendation_to_arbiter` only, not the full `agreement_areas` + `emergent_patterns` prose. Synthesis prompt size becomes bounded by the union of dispute count × per-dispute schema-cap, not by free prose.

### 4.7 `arbitration.schema.json` — Phase 6, arbiter's binding verdict

```json
{
  "$id": "https://build-fractal.org/conversus/schema/v1/arbitration.schema.json",
  "type": "object",
  "required": ["process_note", "decision_framework", "per_question_rulings", "combined_disposition", "ruling_lines"],
  "properties": {
    "process_note": { "type": "string" },
    "decision_framework": { "type": "string" },
    "per_question_rulings": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["question", "verdict", "rationale", "conditions"],
        "properties": {
          "question": { "type": "string", "pattern": "^Q[0-9]+$" },
          "verdict": {
            "enum": [
              "APPROVE-AS-DRAFTED", "APPROVE-WITH-FIXES", "BLOCK",
              "PASS-WITH-CLARIFICATIONS", "FAIL-OVERSTRETCH",
              "TIER-3-CONFIRMED", "RECURSION-EXEMPTED"
            ]
          },
          "rationale": { "type": "string" },
          "conditions": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["id", "priority", "description", "applies_to_section"],
              "properties": {
                "id": { "type": "string", "pattern": "^C[0-9]+$" },
                "priority": { "enum": ["P1", "P2", "P3"] },
                "description": { "type": "string" },
                "applies_to_section": { "type": "string" }
              }
            }
          }
        }
      }
    },
    "combined_disposition": {
      "enum": ["PROCEED-TO-RATIFICATION", "PROCEED-TO-NEXT-STAGE", "PROCEED-TO-SELF-CONSISTENCY", "RETURN-TO-REVIEW", "BLOCK"]
    },
    "ruling_lines": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["question", "verdict", "rationale"],
        "properties": {
          "question": { "type": "string", "pattern": "^Q[0-9]+$" },
          "verdict": { "type": "string" },
          "rationale": { "type": "string" }
        }
      }
    }
  }
}
```

`verdict` enum is intentionally union-typed across the verdict vocabularies used by originating, self-consistency, and blind verification stages (cf. v4.1.0 spec's verdict vocabulary). The enum is closed; new verdict values require a schema MINOR bump.

The redundant `ruling_lines` array (a denormalized projection of `per_question_rulings`) exists for adapter convenience — orchestrator currently grep-extracts one-line ruling summaries and benefits from a flat list. Validator enforces that `ruling_lines` entries match the question/verdict pairs in `per_question_rulings`.

### 4.8 Schema versioning (C8, C10)

The wire format version is named in the envelope's `schema_version` field. **Initial release: `1.0.0-rc.1`** (per C10). After one ratification cycle of clean operation (≥30 days of real production deliberations producing conformant outputs with zero unplanned schema bumps), the version bumps to `1.0.0`. The release-candidate suffix is a stability signal to consumers that the schema may receive ergonomic refinement during the rc window.

Bumps follow Principle XXVIII sub-clause 3 (SemVer) with the C8 consumer-impact qualification:

- **MAJOR** (incompatible): removed required field; removed enum value; type narrowing of an existing field (e.g., `string` → `string` with new `pattern`); **renaming a field even when technically additive** (consumers parse by name, so renames break them); **adding a required field** (existing conformant outputs become non-conformant).
- **MINOR** (additive): adding an optional field; adding a new enum value; adding a new output type to the `output_type` enum; loosening a constraint (e.g., relaxing a `pattern`).
- **PATCH** (clarification): refining a description / docstring; tightening a `pattern` or `enum` in a way no existing real output violates (verified against the historical fixture corpus); fixing a typo in a constraint.

A schema bump that *would* be MINOR by raw schema diff but breaks consumers because of a field-name dependency is classified MAJOR. The validator carries a single `current_supported_versions` allowlist (per Principle XXVIII C2 versioning gate). Outputs with `schema_version` outside the allowlist emit a validation warning to the deliberation event stream; the engine still writes the file (per D1 non-blocking discipline); the PR-required CI gate (§ 5.4) blocks merge on allowlist violation.

**Schema-advancement authority (D7).** The `1.0.0-rc.1` → `1.0.0` promotion decision is made by the **conversus-oss maintainer set** (the same set with merge authority on `main`), per the criteria below, recorded as a PR landing the version bump in `engine/schema/v1/envelope.schema.json` plus the `current_supported_versions` allowlist update in `engine/schema_validator.py`:

- **Quantitative criterion:** ≥30 days have elapsed since `1.0.0-rc.1` was first emitted in production, and during that window the CI schema-validation gate has run on every PR touching `deliberations/**` or `engine/**` with **zero unplanned schema bumps** (i.e., no MAJOR or MINOR amendments to the schema other than the rc-window ergonomic refinements anticipated by C10).
- **Qualitative criterion:** at least one full six-phase deliberation has been re-emitted under each migrated mode (per § 11 step 3) with all emitted JSON conforming to the schema, AND the orchestrator adapter migration (§ 6.2) has landed and parsed at least one real production arbitration successfully.
- **Audit trail:** the version-bump PR cites the deliberation-id corpus the quantitative criterion was measured against, and links to the green CI runs that confirm zero unplanned bumps.

The same authority applies to subsequent MAJOR / MINOR / PATCH bumps documented in this sub-section; the criteria for those bumps are the version-bump procedure itself (consumer impact + SemVer rules), not the rc-window criteria above.

### 4.9 Validator error object schema (C9)

Validation failures emit structured error objects, themselves a stable interface (so consumer tooling can rely on the failure surface). The error object schema (`engine/schema/v1/validator-error.schema.json`):

```json
{
  "$id": "https://build-fractal.org/conversus/schema/v1/validator-error.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["field_path", "error_code", "human_message", "expected_type", "actual_value"],
  "properties": {
    "field_path": {
      "type": "string",
      "description": "JSON pointer to the offending field, e.g., '/body/disputes/0/severity'"
    },
    "error_code": {
      "type": "string",
      "enum": [
        "REQUIRED_FIELD_MISSING",
        "TYPE_MISMATCH",
        "ENUM_VIOLATION",
        "PATTERN_VIOLATION",
        "ADDITIONAL_PROPERTY_FORBIDDEN",
        "SCHEMA_VERSION_UNSUPPORTED",
        "ENVELOPE_BODY_TYPE_MISMATCH",
        "ARRAY_MIN_ITEMS_VIOLATION"
      ]
    },
    "human_message": {
      "type": "string",
      "description": "Human-friendly explanation of the failure."
    },
    "expected_type": {
      "type": "string",
      "description": "The schema-declared expected shape (type or pattern or enum)."
    },
    "actual_value": {
      "description": "The actual value at field_path; may be any JSON type or null when field is missing."
    },
    "suggested_fix": {
      "type": "string",
      "description": "Optional: best-effort suggestion (e.g., 'change \"MAYBE\" to one of {APPROVE-AS-DRAFTED, APPROVE-WITH-FIXES, BLOCK}')."
    }
  }
}
```

This makes validator failures themselves machine-parseable and stable across schema versions.

---

## 5. Implementation

### 5.1 Engine changes (`conversus-oss/engine/`) — **non-blocking warning-based validation** (D1)

**Load-bearing constitutional constraint (Tier 2 Principle V, CONSTITUTION.md L76-78):**

> "Output validation (e.g., Phase 6 heading checks) emits **warnings** for malformed output but **does NOT block file writes**. Malformed output is better than no output."

The engine-side validation architecture for this spec MUST conform to that pillar. The validator runs at write-time and produces structured warnings, but the file IS ALWAYS WRITTEN. Mechanical enforcement bite (per Principle XXVIII sub-clause 2) is preserved at the PR-required CI gate (§ 5.4), which DOES block merge on validation failure. Write-time non-blocking + PR-time blocking together satisfy both Principle V and Principle XXVIII without contradiction. This is the load-bearing inversion from v2 — v2 had the validator abort the phase on failure (which directly negated Principle V); v3 has the validator emit warnings and always proceed (which preserves Principle V).

- **`engine/schema/v1/*.schema.json`** — JSON Schema files, one per output type plus the envelope plus the validator-error schema, anchored at `$id` base `https://build-fractal.org/conversus/schema/v1/`. JSON Schema Draft 2020-12. The Python `jsonschema` library (>= 4.x) is the canonical validator; it satisfies Principle XXVIII C2's mechanical-enforceability bar (binary pass/fail, field-presence check, type check, value-constraint check) without the XSD strawman's CDATA-escaping defect.

- **`engine/schema_validator.py`** — single entry point invoked on every agent output write. Signature: `validate_output(path: Path, content: bytes) -> ValidationResult` where `ValidationResult` is a structured object with `is_conformant: bool` + `errors: list[ValidatorError]` conformant to § 4.9. **The validator MUST NOT raise on non-conformance; it MUST return the `ValidationResult` and let the caller decide.** The caller (engine persistence layer, § below) ALWAYS proceeds to write the file regardless of `is_conformant`. The validator's job is to produce a structured warning record, not to refuse the write.

- **`engine/persistence.py`** — the load-bearing inversion lives here. Pseudocode:
  ```python
  def persist_output(path: Path, content: bytes) -> None:
      result = validate_output(path, content)
      # ALWAYS write the file, regardless of conformance (Principle V).
      path.write_bytes(content)
      if not result.is_conformant:
          # Emit warning to event stream + structured side-channel.
          event_stream.warn(
              event="schema_validation_failed",
              path=str(path),
              errors=[e.to_dict() for e in result.errors],
          )
          # Also write a sibling .validation-warnings.json file next to the
          # offending output so PR-time CI (§ 5.4) can detect + block merge.
          sidecar = path.with_suffix(path.suffix + ".validation-warnings.json")
          sidecar.write_text(json.dumps([e.to_dict() for e in result.errors]))
  ```
  Note: validation precedes the write only so that the warning can be recorded against the same atomic operation; **the write itself is unconditional.** Malformed output is preferred over no output, per Principle V. There is no `SchemaViolation` exception path in the persistence layer.

- **`engine/templates.py` + `templates/{mode}/`** — mode templates updated so agent prompts emit prose in explicit slots (e.g., `<<<STRENGTHS_BEGIN>>> ... <<<STRENGTHS_END>>>`). The engine's output wrapper parses agent prose, extracts slot values, and assembles a JSON envelope. Agents do NOT emit JSON directly; the engine assembles.

- **`engine/cli/run.py`** — adds `--validate-outputs` flag (default `true`). `--no-validate-outputs` disables the validation pass entirely (no warnings produced, no sidecar written). The flag's purpose is debugging / dev-loop speed, not bypassing enforcement: the file would be written either way; disabling validation only suppresses the warning record. The engine logs a prominent notice when the flag is set and records it in the deliberation event stream.

**Implementation performance discipline (D13).** The validator SHOULD complete in <100ms per output as an **operational target**. The `jsonschema` library on representative production-sized outputs (~20-50KB JSON) routinely completes in single-digit milliseconds; the 100ms target provides ~10-20× headroom. **This is implementation discipline, not a constitutional bar.** If a validator implementation exceeds 100ms in practice, the validator is the bug — fix the validator (caching compiled schemas, profiling hot paths) before relaxing the operational target. The CI gate (§ 5.4) runs the validator over the worked-example fixture corpus and asserts P99 latency < 100ms; failing that assertion blocks the merge of validator-implementation changes (not deliberation content). The <100ms number is recorded here as implementation discipline because that is what it actually is — operational engineering practice on a Python library with known performance characteristics — not as a constitutional mandate that would require constitutional-amendment process to relax.

Advanced validations beyond write-time scope — cross-reference integrity (does `ruling_lines[i].question` match a real `per_question_rulings[j].question`?), full constraint validation across documents — run at the same write-time path, contributing additional `ValidatorError` entries to the result; they do not block the write either. C5's tiered staging defines when those advanced checks promote from advisory-only to PR-required-blocking at the CI gate.

### 5.2 Companion markdown rendering

- **`engine/render_md.py`** — pure function `json_to_md(json_path: Path) -> str`. The engine writes both `phase-1/review.json` (canonical) and `phase-1/review.md` (rendered companion) on every phase. The `.md` companion is regenerable from JSON; if someone edits `.md` directly, CI gates fail (the renderer is the only sanctioned writer of `.md` files under `deliberations/**`).
- Default rendering: section headings per output type, agent identity in the H1, structured body as nested H2/H3, enum values in backticks. The rendering is deterministic and reproducible.

### 5.3 Worked-example fixtures (per Principle XXVIII sub-clause 2 + D14)

Principle XXVIII sub-clause 2 (CONSTITUTION.md L538-545) requires each product to ship at least **three test fixtures**: (a) a known-conformant artifact that passes validation, (b) a known-non-conformant artifact with a missing required field that fails validation, and (c) a known-non-conformant artifact with a wrong field type that fails validation. v3 covers all three plus an additional enum-violation fixture to demonstrate the closed-enum mechanism the schema relies on heavily:

- **(a) Conformant —** `engine/tests/fixtures/schema/arbitration_conformant.json` — a passing arbitration output with all required envelope fields, all required body fields, valid enum values, and correctly-typed values throughout. Validator returns `is_conformant=True`, `errors=[]`.
- **(b) Missing required field —** `engine/tests/fixtures/schema/arbitration_missing_ruling.json` — missing required `per_question_rulings` entry for `Q3`. Validator returns `is_conformant=False`, error with `field_path=/body/per_question_rulings`, `error_code=REQUIRED_FIELD_MISSING` (or `ARRAY_MIN_ITEMS_VIOLATION` depending on whether the missing item is enforced via array `minItems` or array-membership cross-check).
- **(c) Wrong field type —** `engine/tests/fixtures/schema/arbitration_wrong_type.json` — `"phase_iteration": "1"` (string where integer required). Validator returns `is_conformant=False`, error with `field_path=/phase_iteration`, `error_code=TYPE_MISMATCH`, `expected_type=integer`, `actual_value="1"`.
- **(d) Enum violation (additional) —** `engine/tests/fixtures/schema/arbitration_wrong_verdict_type.json` — `"verdict": "MAYBE"` (value outside enum). Validator returns `is_conformant=False`, error with `field_path=/body/per_question_rulings/0/verdict`, `error_code=ENUM_VIOLATION`, `expected_type` listing the enum, `suggested_fix` proposing the closest valid value.

**Fixture scope coverage (D14).** Across (a)-(d) the fixture corpus mechanically demonstrates: **field presence** (b), **type checking** (c), **value constraints / enum membership** (d), and **end-to-end conformant baseline** (a). XXVIII sub-clause 2 explicitly names "field presence, types, and value constraints" as the enforcement surface; the four fixture types cover that surface in full.

Each fixture is paired with an expected validator output assertion in `engine/tests/test_schema_validator.py`. CI failure on any fixture mismatch blocks merge of validator-implementation changes (not deliberation content — per D1, deliberation content is never blocked at write-time).

### 5.4 CI gate (PR-required, merge-blocking — the enforcement bite)

D1 makes write-time validation non-blocking. The mechanical-enforcement teeth Principle XXVIII sub-clause 2 requires therefore live at the **PR-required CI gate** below. This is where the merge actually blocks; this is where producer code's conformance is enforced.

- New GitHub Actions workflow `.github/workflows/schema-validate.yml`:
  - **Triggers** on `pull_request` paths `deliberations/**`, `engine/schema/**`, `engine/schema_validator.py`, `engine/persistence.py`, `engine/render_md.py`, `engine/tests/fixtures/schema/**`.
  - **Forward-validation job (artifacts → schema).** Runs `python -m engine.schema_validator --all deliberations/` — validates every JSON file under `deliberations/` against the current schema. Fails the build if any file is non-conformant OR if any `.validation-warnings.json` sidecar exists alongside an emitted JSON (sidecars are produced by the write-time validator on conformance failure per § 5.1; their presence in a PR indicates the producer code emitted a malformed file, which must be fixed before merge).
  - **Bidirectional drift-detection job (D12, per XXVIII sub-clause 2 "Validation MUST be bidirectional").** When a PR modifies any file under `engine/schema/v1/`, the CI job re-runs forward-validation against **the entire pre-existing `deliberations/**` corpus** under the new schema. This detects the case where a schema edit silently breaks previously-conformant artifacts — XXVIII sub-clause 2 explicitly mandates this direction: "any change to the schema itself MUST trigger CI verification that the existing producer code still emits conformant artifacts under the new schema (drift detection on schema edits)." The drift-detection job is merge-blocking; producer-side warning-only (per D1 consistency at write-time) does not mean PR-side warning-only.
  - **Schema-version-bump detection job (D15, per XXVIII sub-clause 3 "silent format changes are a violation").** When a PR modifies any file under `engine/schema/v1/`, the CI job asserts that **either** the touched schema file's `$id` version path (e.g., `/v1/`) is incremented to a new major version directory, **or** the envelope schema's `schema_version` `pattern`/`enum` has been updated to reflect a new minor/patch version, **or** the PR description contains the literal token `[schema:no-bump-justified]` plus a rationale referencing the specific clarification-only edit (PATCH-equivalent docstring fix). Any schema edit that fails all three branches blocks merge with the error message "schema edited without version bump — see § 4.8 SemVer rules and Principle XXVIII sub-clause 3."
  - **Fixture + renderer test job.** Runs `pytest engine/tests/test_schema_validator.py` — the four worked-example fixtures (§ 5.3) + the renderer round-trip test (JSON → MD → JSON must be bit-identical for canonical-form JSON) + the D13 operational target assertion (P99 < 100ms over the fixture corpus).
  - Pass/fail is binary; failure blocks merge. Required-check setting enforced on the `main` branch.

---

## 6. File edits per repo

### 6.1 `Build-Fractal/conversus-oss/` (this repo)

- `engine/schema/v1/*.schema.json` (new) — JSON Schema files.
- `engine/schema_validator.py` (new).
- `engine/render_md.py` (new).
- `engine/persistence.py` (modified) — adds validate-then-write.
- `engine/cli/run.py` (modified) — adds `--validate-outputs`.
- `engine/templates.py` + `templates/{mode}/*.md` (modified) — adds slot markers to agent prompts.
- `engine/tests/test_schema_validator.py` (new) + `engine/tests/fixtures/schema/*.json` (new).
- `.github/workflows/schema-validate.yml` (new).
- `CONSUMER-CONTRACT.md` (new, repo root) — declares the JSON Schema as a stable surface; full content specification per § 7.1 (D11). Names the specific schema surfaces and states the stability guarantee for each, per XXVIII sub-clause 5 (CONSTITUTION.md L572-577).
- `CONFORMANCE.md` (modified, repo root, D9) — the Persistence-Contract row is updated to: (a) name the canonical schema directory `engine/schema/v1/`, (b) name the file-naming convention (`{output-type}.schema.json` + `envelope.schema.json` + `validator-error.schema.json`), (c) cite the `$id` URI base `https://build-fractal.org/conversus/schema/v1/`, (d) cross-reference `CONSUMER-CONTRACT.md`. This satisfies XXVIII sub-clause 1's "documented in the repo's CONFORMANCE.md" textual requirement (CONSTITUTION.md L505-510).
- `STATE-FILES.md` (modified, if extant) — updates the deliberation-output entries to reference the new JSON schema location.
- `CLAUDE.md` (modified, repo root, D10) — adds a "Persistence Contract" section that **explicitly links to `CONSUMER-CONTRACT.md`**. The link is mandatory per XXVIII sub-clause 1's textual requirement that the discoverable location be "linked from **BOTH** the repo's top-level `README.md` AND its `CLAUDE.md`" (CONSTITUTION.md L508-510, emphasis in the constitutional text via the "BOTH" qualifier).
- `README.md` (modified, repo root, D10) — adds the same "Persistence Contract" link to `CONSUMER-CONTRACT.md`. The README link and the CLAUDE.md link are both required; satisfying only one fails XXVIII sub-clause 1.

### 6.2 `Build-Fractal/orchestrator/` (formerly spec-kit-orc)

- `scripts/dispatch/adapters/tool/conversus.sh` (modified) — replaces the existing grep-of-markdown parser with a JSON parser. New parser invokes `jq -r '.body.ruling_lines[].verdict' {arbitration.json}` (or equivalent Python) to extract verdict lines. Markdown-format outputs are still consumed for backward compatibility during the migration window (§ 11); JSON is preferred when both are present.
- `scripts/dispatch/adapters/tool/conversus.adapter.md` (new or modified) — declares the adapter's dependency on the conversus-oss JSON Schema, names the version range it supports, and references conversus-oss's `CONSUMER-CONTRACT.md`. Mirrors Principle XXVIII C3 (consumer-side declaration).
- Adapter CI: orchestrator CI gains a "conversus-json-fixture" job that runs the adapter against a vendored copy of conversus-oss's fixture set; failure blocks merge in orchestrator.

### 6.3 `clariti-care/payer-index-mono/build-fractal/conversus/CONFORMANCE.md`

- Update the conversus-oss row to reflect that this spec is the active satisfaction track for Principle XXVIII. Status moves from "Remediation-Blocked" (current, per v4.1.0) to "Remediation-In-Progress" on spec ratification, and to "Compliant" on completion of § 11 step 6.

---

## 7. Cross-product implications

The orchestrator adapter is the load-bearing consumer-side surface. Today the adapter (`scripts/dispatch/adapters/tool/conversus.sh`) hardcodes three brittle paths and grep patterns against conversus-oss outputs. Principle XXVIII C3 mandates `CONSUMER-CONTRACT.md` on the producer side declaring stable surfaces consumed by cross-product code; this spec produces that file. The adapter's parsing approach migrates from `grep` over markdown headings to `jq` (or Python `json.load`) over conformant JSON — a substantially simpler and more reliable consumer-side implementation, which was one of the load-bearing reasons the originating arbitration converged on JSON over XML (no specialized tooling like `xmllint`; ubiquitous shell parsing via `jq`).

After ratification:
1. Conversus-oss `CONSUMER-CONTRACT.md` declares the JSON Schema as stable.
2. Orchestrator's adapter declares it consumes that schema (version range `>=1.0.0-rc.1,<2.0.0` initially).
3. Both products' CI verifies the contract — conversus-oss CI validates every emitted JSON; orchestrator CI validates that its adapter correctly parses a vendored fixture set.
4. A schema MAJOR bump in conversus-oss requires coordinated adapter update in the orchestrator, sequenced via the cross-repo CI pattern in `build-fractal/conversus/CLAUDE.md` ("Cross-repo work" section).

No other suite product currently consumes deliberation outputs structurally (conversus-enhanced consumes solver outputs, not deliberation outputs). If a future sibling adds a consumer, it inherits the same `CONSUMER-CONTRACT.md` pattern.

### 7.1 CONSUMER-CONTRACT.md content specification (D11)

Per XXVIII sub-clause 5 (CONSTITUTION.md L572-577), the producer's `CONSUMER-CONTRACT.md` MUST explicitly name each declared stable surface AND state its stability guarantee. Bare existence of the document does not satisfy the sub-clause. v3 specifies the required content shape:

**Required sections** in `conversus-oss/CONSUMER-CONTRACT.md`:

1. **Title + declaration of intent.** "This document declares the stable surfaces conversus-oss exports for cross-product consumption under Tier 2 Principle XXVIII sub-clause 4."

2. **Declared schema surfaces** (per XXVIII sub-clause 5). Each entry MUST include:
   - **Surface identifier** — e.g., `engine/schema/v1/envelope.schema.json` `$id=https://build-fractal.org/conversus/schema/v1/envelope.schema.json`.
   - **Stability guarantee** — explicit prose, not gesture. For each of the six body schemas + envelope + validator-error: "The set of REQUIRED fields, the `enum` values of constrained fields, the `pattern` regexes on string fields, and the field names of OPTIONAL fields are stable across PATCH and MINOR `schema_version` bumps. Removal of a REQUIRED field, removal of an enum value, narrowing of a `pattern`, or renaming of any field requires a MAJOR `schema_version` bump per § 4.8 and triggers cross-product consumer migration per XXVIII sub-clause 4."
   - **Versioning support window** — the `current_supported_versions` allowlist value the validator enforces (initially `>=1.0.0-rc.1, <2.0.0`).
   - **Deprecation policy** — when a MAJOR bump occurs, the previous MAJOR receives a 90-day support window during which both versions are accepted; after the window the previous MAJOR is removed from the allowlist.

3. **Declared display-text surfaces** (per XXVIII sub-clause 5). v3 declares the following display-text surfaces stable, each with explicit guarantee:
   - **Companion `.md` rendered file naming** — `{output-type}.md` siblings to `{output-type}.json` under `deliberations/{deliberation-id}/`. Stable across MINOR; renamed only on MAJOR.
   - **`.validation-warnings.json` sidecar file naming** — `{output-path}.validation-warnings.json` siblings to non-conformant JSON outputs (per § 5.1 D1 architecture). Stable across MINOR; renamed only on MAJOR.
   - **No other display-text surface is declared stable.** Heading text inside the rendered `.md` companions is **explicitly undeclared** — consumers parsing rendered-MD heading text for semantic content are violating XXVIII sub-clause 4. The JSON envelope + body schemas are the stable parse target.

4. **Consumer-side obligations.** Cross-product consumers (e.g., the orchestrator adapter) MUST: (a) consume the declared JSON schema, not display text in rendered MD; (b) pin a `schema_version` range; (c) ship consumer-side fixtures in their own CI per XXVIII sub-clause 4 ("Producer-side fixtures alone do not satisfy this sub-clause"); (d) coordinate migration on MAJOR `schema_version` bumps via the cross-repo sequencing pattern in `build-fractal/conversus/CLAUDE.md`.

5. **Pointer to producer-side enforcement.** Link to `engine/tests/fixtures/schema/` and `.github/workflows/schema-validate.yml` so consumers can see how producer-side conformance is mechanically enforced.

6. **Pointer to the schema directory.** Link to `engine/schema/v1/` and to each of the seven schema files individually.

This specification is normative for the `CONSUMER-CONTRACT.md` file produced by § 6.1; the file must contain all six sections above with the content shape described. Sub-clause 5 compliance is verified at PR-time by a CI check that grep-confirms each section heading exists in the file (lightweight structural check, not a semantic check).

---

## 8. Inclusion Criteria (Principle XXVIII satisfaction check)

Per Principle XXVIII's three-prong test and spec 070 (Constitutional Inclusion Criteria):

- **Universal applicability within conversus-oss:** Every deliberation produces all six output types. Schema applies universally to conversus-oss deliberations without exception. The migration window (§ 11) is bounded and time-limited; no permanent carve-out.
- **Mechanical verifiability:** JSON Schema validation is the canonical mechanical-enforcement primitive (binary pass/fail, field-presence check, type check, value-constraint check) with a sub-100ms runtime budget (C2). Three worked-example fixtures (§ 5.3) demonstrate enforcement bite per Principle XXVIII C6.
- **Non-redundance with existing principles:** No existing principle mandates a deliberation output schema. The current markdown templates document expectations but do not enforce them (Bug B and Bug C are existence proofs of unenforced expectations).

---

## 9. Verification methodology

Run the standard four-stage methodology per spec 067, mirroring v4.1.0:

1. **Originating deliberation** (4 agents). Anchor: this spec's content + Principle XXVIII grounding. Agents: engineer, schema-design-expert, adapter-consumer, devils-advocate. Output: `deliberations/v4.2.0-structured-deliberation-outputs-originating-2026-05-12/`. **Status: COMPLETE; APPROVE-WITH-FIXES on Q1+Q2, TIER-3-CONFIRMED on Q3 (the originating "RECURSION-EXEMPTED" label is retired in v3 in favor of temporal-constraint scope language per D4); conditions C1-C10 applied to produce v2.**
2. **Self-consistency verification** (4 different agents). Focus: contradiction with existing engine architecture, mode-template constraints, plugin entry-point partition (free/paid boundary per spec 033). Output: `deliberations/v4.2.0-structured-deliberation-outputs-self-consistency-2026-05-13/`. **Status: COMPLETE (manual arbitration); PASS-WITH-CLARIFICATIONS on Q1+Q2; FAIL-CONTRADICTION on Q3 (v2 § 5.1 blocking-validation contradicted Tier 2 Principle V); D-conditions D1-D15 applied to produce this v3.** Self-consistency re-run against v3 follows.
3. **Self-consistency re-run** (4 different agents). Triggered by the FAIL-CONTRADICTION on Q3 in stage 2; scoped to confirming the D1 Principle V fix and the D2-D15 clarifications hold. Output: `deliberations/v4.2.0-structured-deliberation-outputs-self-consistency-rerun-2026-05-13/` (or equivalent dated subdirectory).
4. **Blind verification** (4 fresh agents, no prior context). Focus: pure-reading review of the spec without prior deliberation context.
5. **Ratification.** If combined disposition across all stages is PROCEED-TO-RATIFICATION, the spec promotes to `Build-Fractal/conversus-oss/CONSTITUTION.md` Component-tier principle.

Per v4.1.0 D-conditions D1 and D3: within each verification stage, Q1 constitutional coherence assessment MUST complete before Q2 evidence base adequacy analysis; ratification-blocking issues must be evaluated before enforcement-mechanism design issues.

### 9.1 Methodological recursion — temporal-constraint scope (D2, D4, D5)

**v3 reframing.** v2 invoked a "RECURSION-EXEMPTED" verdict on this question and cited Tier 1 Principle II as justification. The self-consistency arbitration identified two problems with that framing: (1) Principle II governs **interface stability for technical contracts** (dispatch tables, template variables, schema-versioned wire formats), not procedural-methodology accommodations for verification cycles — citing it here was doctrinally invalid (D2); and (2) the "exemption" framing structurally resembles the v4.1.0 override-with-rationale stretch rejected by v4.1.0 self-consistency, and risks creating a re-invocable precedent unless explicitly contained (D4 + D5). v3 strikes the Principle II citation and replaces "exemption" with **temporal-constraint scope** language, mirroring v4.1.0's temporal-vs-membership-universality precedent.

**The temporal-constraint framing.** v4.2.0 is the spec that **creates** the JSON schema infrastructure. Verification outputs for v4.2.0 are produced by the four-stage methodology *while v4.2.0 is being verified* — therefore they predate the existence of the schemas they would otherwise be required to conform to. This is a **bootstrap paradox** at the moment of standing up the schema infrastructure: the schemas come into existence only on ratification of this spec, so any verification output emitted *before* ratification cannot logically conform to a schema that does not yet exist. Asking v4.2.0's verification trail to use JSON is asking it to conform to a contract that comes into existence on the very ratification it is verifying.

This is logically equivalent to v4.1.0's temporal-vs-membership distinction: v4.1.0 ruled that a principle binds all products that exist at ratification time (membership universal) but does not retroactively bind products that did not exist at ratification time (temporal limitation). v4.2.0's case is the same structure, applied to artifacts rather than products: the schema binds all verification outputs produced *after* schema ratification, but does not retroactively bind outputs produced *before* schema ratification — because before-ratification outputs cannot conform to a schema that does not yet exist. The accommodation is therefore not "relief from a Tier 2 principle"; it is **scope clarification** — the schema's temporal scope precedes its existence by construction.

**Anti-precedent language (D5).** This temporal-constraint accommodation applies **only** to specs that ratify the schema infrastructure they would otherwise be required to use. Future amendments creating new validation infrastructure are NOT exempt from using existing validation infrastructure — they remain bound by Principle XXVIII and by the schemas this spec produces. The accommodation does not generalize to "amendments adjacent to schema infrastructure," "amendments touching validation pathways," or any other re-invocable framing. The one and only case the accommodation covers is the bootstrap paradox of a spec standing up its own schema substrate. Subsequent specs — including future MAJOR `schema_version` bumps, future schema additions for new output types, and future amendments that touch the validator implementation — MUST conform to whatever schema is in force at the time of their own verification. There is no recursion-exemption pattern; there is a one-time bootstrap scope clarification.

**Practical consequence.** The verification trail for v4.2.0 itself stays markdown — a fixed point in the migration. The first spec ratified after v4.2.0 implementation completion is bound to use JSON for its verification outputs (per § 11 Tier T1 from the ratification of v4.2.0 onward, parallel-format support is in place; specs ratified after T3 — 2026-10-01 — MUST emit JSON).

### 9.2 Cross-tier weakening assessment (D3)

Per Tier 2 Constitution L649-664 (cross-tier weakening prohibition operational definition), any component-tier amendment MUST be assessed against the three weakening criteria. This sub-section discharges that obligation for v4.2.0.

**Criterion (i) — Implicit relief.** The accommodation must not grant implicit relief from a Tier 2 principle without invoking the formal Relief pathway in `COMPLIANCE.md` Part VI.

*Assessment.* v4.2.0's accommodation is **scope clarification, not relief**. The accommodation does not say "v4.2.0 is exempt from Principle XXVIII"; it says "Principle XXVIII's schema requirement applies to outputs produced after the schema exists, not before." This is structurally identical to v4.1.0's ratified temporal-vs-membership distinction (which v4.1.0 self-consistency confirmed is not Relief — it is scope clarification because strict reading is logically impossible, not merely inconvenient). The bootstrap paradox makes strict reading logically impossible: there is no schema for pre-ratification outputs to conform to, by construction. The accommodation does not require invoking Relief because there is no ongoing structural inability to satisfy the principle — there is a one-time logical impossibility at the moment of standing up the principle's enforcement substrate. **Criterion (i) is NOT triggered.**

**Criterion (ii) — Implementation-impact shift.** The amendment must not introduce interpretation language that would cause existing implementations to no longer satisfy the upper-tier principle.

*Assessment.* The Tier 2 principle in question is Principle V (Observable Deliberation, "validation emits warnings but does NOT block file writes"). v3 § 5.1 is designed to **strengthen** Principle V compliance, not weaken it — v3 inverts v2's blocking-validation framing precisely *because* v2 contradicted Principle V. No existing implementation's Principle V satisfaction is degraded; existing implementations that already comply with Principle V (warning-based validation) continue to comply. The Tier 2 principle adjacent to this spec — Principle XXVIII — is **strengthened**, not weakened, by v3: schemas, mechanical CI enforcement, version-bump detection, bidirectional drift detection, fixture coverage, consumer-contract content specification, README+CLAUDE linking, CONFORMANCE.md location declaration are all introduced or tightened by this amendment. **Criterion (ii) is NOT triggered.**

**Criterion (iii) — Suite-specific adaptation bypass.** The amendment must not add a "suite-specific adaptation" clause that effectively bypasses an upper-tier MUST clause.

*Assessment.* The temporal-constraint clause in § 9.1 is **not framed as suite-specific adaptation** of any Tier 2 MUST clause; it is framed as logical-impossibility scope clarification at the moment of substrate standup. The anti-precedent language (D5) explicitly contains the accommodation to this one-time bootstrap and bars future re-invocation under "adjacent" or "similar" framings. There is no MUST clause being bypassed — Principle XXVIII's MUST clauses (declared schema, mechanical enforcement, versioning, consumer contracts, declaration scope) are all satisfied for the outputs produced after v4.2.0 ratification. The outputs produced before v4.2.0 ratification cannot logically be in scope of a schema that comes into existence at ratification. **Criterion (iii) is NOT triggered.**

**Conclusion.** v3's accommodation is temporal-constraint scope clarification, not cross-tier weakening. The accommodation does not invoke the formal Relief pathway because Relief is structurally for ongoing inability; v4.2.0's situation is one-time logical impossibility resolved at ratification. The accommodation is contained by the D5 anti-precedent language.

### 9.3 Forward-promotion pathway (D8)

The originating arbitration ruled TIER-3-CONFIRMED on Q3 because the evidence base for deliberation-output structural discipline is currently limited to conversus-oss. If a future conversus-suite sibling (e.g., a hypothetical `conversus-investigations`) begins producing deliberation-like artifacts, the Tier-3 placement should be re-evaluated for potential promotion to Tier 2 (Suite).

**Promotion trigger.** Promotion is triggered when a second conversus-suite product begins producing deliberation outputs *and* either (a) the second product independently produces a `CONSUMER-CONTRACT.md`-referenced JSON Schema for its own deliberation outputs, or (b) the second product imports / vendors the conversus-oss schemas.

**Promotion pathway.** Per `build-fractal/conversus/GOVERNANCE.md` § Pathway Taxonomy, a Tier-3 → Tier-2 promotion is a **MINOR amendment** at Tier 2 if the principle's substance does not change (only its scope expands from one product to the suite), or a MAJOR amendment if the promotion would require text changes to the existing component-tier principle that materially affect its meaning. The promotion follows the standard four-stage methodology (originating → self-consistency → blind verification → ratification). The originating deliberation MUST include an explicit evidence-base review showing the second product's deliberation outputs satisfy the same structural discipline this spec defines.

**Until promotion is triggered**, the principle remains at component tier in `conversus-oss/CONSTITUTION.md`. The forward-promotion pathway is documented here for traceability; it is not invoked at v4.2.0 ratification.

---

## 10. Conditions (applied in v2)

The originating arbitration conditions C1-C10 are applied in this v2 spec. Quoting verbatim from `deliberations/v4.2.0-structured-deliberation-outputs-originating-2026-05-12/arbitration/resolution.md`:

- **C1 (P1)** — § 4 + § 5.1 — switch canonical format from XML+XSD to **JSON Schema**. Update all six body-schema definitions and the common envelope to JSON Schema syntax. Update § 3 non-goals to remove the "XSD strawman" framing. *Applied in v2: §§ 4, 5.1, 7 fully rewritten; § 3 strawman language removed.*
- **C2 (P1)** — § 5.1 — establish **<100ms per-output validation performance budget** for write-time validation with early performance testing to fix scope before commitment. *Applied in v2: § 5.1 "Performance budget (C2)" paragraph + § 5.4 CI gate enforces P99 < 100ms.*
- **C3 (P1)** — § 11 — specify **dependency-ordered template migration**: review → cross-review → revision → disputes → synthesis → arbitration, with one-mode pilot. *Applied in v2: § 11 steps 3a-3b.*
- **C4 (P1)** — § 11.1 — explicitly enumerate **semantic equivalence testing** as a CI gate during the migration window: structured-parsed verdicts must match grep-extracted verdicts on all historical arbitration outputs. *Applied in v2: § 11.1 "Semantic equivalence CI gate (C4)".*
- **C5 (P2)** — § 11 — adopt **tiered/staged implementation**: v1.0.0 basic structural validation by 2026-12-01, advanced features (cross-reference integrity, full constraint validation) in v1.1.0 after performance validation. *Applied in v2: § 11 tiered rollout table + § 5.1 advanced-validation deferral language.*
- **C6 (P1)** — § 4.1 envelope — add required fields `deliberation_stage`, `engine_version`, `source_commit`. *Applied in v2: § 4.1 envelope schema + example.*
- **C8 (P2)** — § 4.8 — refine SemVer bump policy with explicit consumer-impact qualification (field rename = MAJOR even if technically additive when consumer parses by name). *Applied in v2: § 4.8 expanded.*
- **C9 (P2)** — § 5.1 — specify validator error-object schema (`field_path`, `error_code`, `human_message`). *Applied in v2: § 4.9 (new sub-section) + § 5.1 reference.*
- **C10 (P3)** — § 4.8 — adopt **1.0.0-rc.1 versioning** strategy with bounded iteration period ending by constitutional deadline. *Applied in v2: § 4.8 initial-version language + § 2 goal 2.*

Self-consistency D-conditions and blind-verification E-conditions will be appended below by subsequent stages following the v4.1.0 pattern.

---

## 11. Implementation order

Updated per C3 (dependency-ordered template migration with one-mode pilot) and C5 (tiered staging).

1. **Verify spec** via the four-stage methodology (§ 9).
2. **Add schemas + validator + renderer** to conversus-oss. Land as one PR with the three worked-example fixtures and CI gate.
3. **Migrate mode templates** to slot-marker form in **dependency order** (C3):
   - **3a. One-mode pilot.** Pick the most-used mode (**cooperative**) and migrate it first. Verify the migration on real production deliberations (re-emit at least one full six-phase deliberation in cooperative mode; validate every emitted JSON; regenerate MD companion; diff against the markdown the original template would have produced — see § 11.1 C4 gate). Block subsequent migrations until the pilot is green.
   - **3b. Remaining modes in dependency order.** The output types form a dependency chain: review → cross-review → revision → disputes → synthesis → arbitration. Within each mode, migrate output types in that order — review first (no upstream dependencies), arbitration last (depends on all five upstream types). One PR per (mode, output-type) pair. Each PR is independently testable.
   - The dependency analysis: cross-review consumes review structure; revision consumes own-prior-review + cross-reviews; disputes consumes prior phases' positions; synthesis consumes all phase 1-4 outputs; arbitration consumes synthesis (and optionally raw phase 1-4). Migrating arbitration before synthesis would create a JSON-consumer / markdown-producer mismatch.
4. **Migrate orchestrator adapter** to JSON consumer. Coordinated with conversus-oss `CONSUMER-CONTRACT.md` declaration.
5. **Re-render v4.1.0 audit trail as JSON.** Validation milestone: take the existing 4 deliberations for v4.1.0 (~150 markdown files) and re-emit each as JSON using a one-time `engine/migrate_md_to_json.py` tool. Validate every emitted JSON against the schema. This both backfills the audit trail and proves the schema accommodates real production deliberation outputs.
6. **Update conversus-oss CONFORMANCE.md row to Compliant.** Closes the Principle XXVIII remediation track ahead of the 2026-12-01 universal deadline.
7. **Deprecate markdown-format mode templates.** Archive under `templates/_archived_pre_json/` on the deprecation date.

### Tiered rollout dates (C5)

| Tier | Status | Date | Description |
|---|---|---|---|
| T1 | Parallel-format support | spec ratification (target 2026-06-01) | Engine writes both JSON canonical + MD companion. Adapter reads both; prefers JSON when present. CI is non-blocking. |
| T2 | Advisory CI on structured format | 2026-08-01 | CI emits warnings on JSON schema violations but does not block merge. Lets producers detect issues without stop-the-line. |
| T3 | Blocking CI on structured format | 2026-10-01 | PR-required CI gate (§ 5.4) blocks merge on schema violations. All new deliberations must be JSON-conformant. Write-time validation remains warning-only per § 5.1 D1 (Principle V); merge-block is at PR-time only. Markdown-only paths get explicit deprecation warnings in CI logs. |
| T4 | Markdown deprecation | 2026-12-01 | Engine reads JSON only. Markdown-reading code paths removed. Aligns with Principle XXVIII universal remediation deadline. |

**Post-cliff-date ratification handling (D6).** If ratification of this spec occurs **after** 2026-12-01 (the universal cliff date), the staged rollout above is collapsed: T1, T2, and T3 are treated as **simultaneously in-effect at ratification**, and T4 (markdown deprecation, engine reads JSON only) is treated as in-effect at ratification. There is no extended grace period beyond the constitutional cliff date for late ratification; the universality of the 2026-12-01 deadline (per CONSTITUTION.md L594-602) does not yield to a slower ratification path on this spec specifically. Concretely, late-ratification operations: (a) the schema-validate CI workflow lands as PR-required-blocking from day 1; (b) the parallel-MD-companion behavior is implemented but the adapter (§ 6.2) consumes JSON only; (c) the markdown-reading code paths are removed in the same PR train that lands the schema infrastructure, not in a follow-on train. The semantic-equivalence CI gate (§ 11.1 C4) is reduced to its historical-snapshot use only — it verifies the renderer produces equivalent output for the historical markdown corpus, but is not used as a forward gate on new template migrations (because all migrations land simultaneously at ratification).

### 11.1 Backward-compatibility window + semantic equivalence CI gate (C4)

Between ratification and 2026-12-01:
- New deliberations: JSON canonical + MD companion (per § 5.2).
- Historical deliberations (pre-ratification): markdown stays as-is. Optional: re-render via step 5 above.
- Engine reads both formats during the window. The persistence layer prefers JSON when both are present.
- Orchestrator adapter supports both formats during the window (per § 6.2).
- After 2026-12-01: engine reads JSON only.

**Semantic equivalence CI gate (C4).** During the migration window, a CI job runs the following round-trip test on every PR that modifies templates:
1. Take a representative input prompt for the (mode, output-type) under migration.
2. Render via the **old markdown template** → emit markdown output. Call this `MD_OLD`.
3. Render via the **new JSON template** → emit JSON output. Validate JSON against schema. Render JSON to MD companion via `engine/render_md.py`. Call this `MD_NEW`.
4. Diff `MD_OLD` against `MD_NEW`. Allowed differences: whitespace, ordering of equivalent enum-projected fields, deterministic field-formatting (e.g., timestamps reformatted to ISO-8601).
5. **Forbidden differences (CI fail):** missing section, missing structured field, divergent enum value, dropped concern/dispute, different verdict.

If the semantic content of `MD_NEW` differs from `MD_OLD` in a forbidden way, the migration is breaking — fail the build. Concrete fixtures live at `engine/tests/fixtures/semantic_equivalence/{mode}/{output-type}/` and are exercised by `pytest engine/tests/test_semantic_equivalence.py`. This is per Principle XXVIII C6 (worked-example fixtures with mechanical enforcement bite).

The CI gate is removed at T4 (2026-12-01) when markdown templates are deprecated and the equivalence question becomes moot.

---

## 12. Open questions for the originating arbitration

**STATUS: RESOLVED by the originating arbitration (2026-05-13).** Listed here for traceability:

- **OQ1 — Tier placement.** **RESOLVED: TIER-3-CONFIRMED.** Re-evaluate at the first conversus-suite sibling that produces deliberation-like artifacts. *(Q3 ruling.)*
- **OQ2 — XSD vs JSON Schema vs Pydantic-XML for the validator.** **RESOLVED: JSON Schema.** Unanimous P1 convergence across all four agents. *(C1 + C7 in arbitration, applied in v2 § 4 + § 5.1.)*
- **OQ3 — Companion MD generation: XSLT vs Python renderer.** **RESOLVED: Python renderer.** No agent challenged the strawman. *(Q1 Per-axis finding 6.)*
- **OQ4 — Deprecation cliff date.** **RESOLVED: 2026-12-01.** Constitutional deadline non-negotiability unanimous. *(Q1 Per-axis finding 7.)*
- **OQ5 — Methodological recursion.** **RESOLVED: TEMPORAL-CONSTRAINT SCOPE** (v3, per self-consistency D4). Markdown verification trail stays for v4.2.0 itself because v4.2.0's verification outputs are produced before the JSON schemas it ratifies come into existence (bootstrap paradox); JSON mandatory for subsequent specs. Anti-precedent language (§ 9.1 D5) contains the accommodation to this one-time bootstrap and bars future re-invocation. The originating-stage "RECURSION-EXEMPTED" verdict label is retired; the substance (markdown stays for v4.2.0) is preserved under a doctrinally-correct framing.

---

## 13. Footnote: methodology recursion + meta-signal

Running this spec through the four-stage verification uses the methodology whose outputs it schematizes. Two meta-signals to watch for:

- **If the methodology can't sustain its own self-improvement at this stage** — e.g., if the originating deliberation hits Bug A (prompt overflow) or Bug C (trigger miss) while reviewing the very spec that fixes them — that is a strong signal the migration is overdue and should be sequenced ahead of further v4.x amendments. **Status:** Bug C *did* manifest in the originating arbitration (the Phase 5 synthesizer wrote "Remaining Disputes" rather than the engine's expected marker pair; the arbiter dispatch silently missed; manual arbitration was produced — see `deliberations/v4.2.0-structured-deliberation-outputs-originating-2026-05-12/arbitration/resolution.md` "Process Note"). This is real-time confirmation that the spec's structural-detection thesis is correct.
- **If the blind verification surfaces "should this spec require JSON for ITS OWN verification outputs?"** as a load-bearing question, the answer is **temporal-constraint scope** per § 9.1 (D4): v4.2.0 verification outputs predate JSON schema availability by construction, so they cannot logically conform to a schema that does not yet exist. The verification trail for v4.2.0 itself stays markdown — a fixed point in the migration. Anti-precedent language (§ 9.1 D5) bars future re-invocation under "adjacent" framings. JSON is mandatory for specs ratified after v4.2.0 implementation completion.

---

## 17. Fix ledger

| Version | Date | Change | Source |
|---|---|---|---|
| v1 | 2026-05-12 | Initial draft. XSD strawman. | Author. |
| v2 | 2026-05-13 | Applied C1-C10 from originating arbitration. C1: format flipped XML+XSD → JSON + JSON Schema (all six body schemas + envelope rewritten in §§ 4.1-4.7; § 5.1 validator architecture rewritten around Python `jsonschema`; § 7 adapter parsing migrated grep/`xmllint` → `jq`/Python `json.load`). C2: <100ms validation budget (§ 5.1) with P99 CI assertion (§ 5.4). C3: dependency-ordered template migration with cooperative-mode pilot (§ 11 step 3). C4: semantic equivalence CI gate during migration window (§ 11.1). C5: four-tier rollout (§ 11). C6: three additional required envelope fields (§ 4.1). C8: SemVer bump qualification with consumer-impact rule (§ 4.8). C9: validator error-object schema (§ 4.9 new). C10: initial schema version `1.0.0-rc.1` (§ 4.8, § 2 goal 2). | `deliberations/v4.2.0-structured-deliberation-outputs-originating-2026-05-12/arbitration/resolution.md` |
| v3 | 2026-05-13 | Applied D1-D15 from self-consistency arbitration. **D1 (load-bearing reversal):** § 5.1 rewritten as non-blocking warning-based validation; engine writes the file unconditionally; PR-required CI gate (§ 5.4) carries the enforcement bite. Resolves Q3 FAIL-CONTRADICTION against Tier 2 Principle V ("does NOT block file writes"). **D2:** struck Principle II misattribution in § 9.1. **D3:** new § 9.2 cross-tier weakening assessment against CONSTITUTION.md L649-664 criteria (i)/(ii)/(iii); conclusion: scope clarification, not relief. **D4 + D5 (load-bearing reframing):** replaced "RECURSION-EXEMPTED" with temporal-constraint scope language throughout § 9.1, § 12 OQ5, § 13; mirrors v4.1.0's temporal-vs-membership-universality precedent; added anti-precedent containment language barring future re-invocation. **D6:** post-cliff-date ratification handling in § 11 (T1-T3 collapsed, T4 in-effect at ratification). **D7:** schema-advancement authority in § 4.8 (maintainer set + quantitative/qualitative criteria for 1.0.0-rc.1 → 1.0.0 promotion). **D8:** new § 9.3 forward-promotion pathway for Tier-3 → Tier-2 when a second sibling produces deliberation outputs. **D9:** schema-location declaration in CONFORMANCE.md (§ 4.0 new, § 6.1). **D10:** README + CLAUDE.md links to CONSUMER-CONTRACT.md (§ 6.1). **D11:** complete CONSUMER-CONTRACT.md content specification in § 7.1 (new) with six required sections. **D12:** bidirectional drift-detection CI job (§ 5.4). **D13:** <100ms reframed as implementation discipline, not constitutional mandate (§ 5.1). **D14:** fixture scope expanded to four types covering field presence, type checking, value constraints, baseline (§ 5.3). **D15:** schema-version-bump CI detection job (§ 5.4). | `deliberations/v4.2.0-structured-deliberation-outputs-self-consistency-2026-05-13/arbitration/resolution.md` |

---

## Document status checklist

- [x] § 1 Motivation grounded in three concrete bugs with citations + real-time Bug C reproduction confirmation.
- [x] § 2 Goals enumerated (6 goals, each tied to Principle XXVIII sub-clause).
- [x] § 3 Non-goals enumerated.
- [x] § 4 Schema specified with JSON Schema definitions for all six output types + envelope + validator-error object.
- [x] § 5 Implementation specified with engine file paths + CI gate + <100ms performance budget.
- [x] § 6 File edits per repo enumerated (conversus-oss + orchestrator + payer-index-mono).
- [x] § 7 Cross-product implications mapped (orchestrator adapter migration).
- [x] § 8 Inclusion criteria checked against Principle XXVIII three-prong test.
- [x] § 9 Verification methodology specified; originating stage COMPLETE; self-consistency stage COMPLETE (FAIL-CONTRADICTION on Q3 → v3 produced); self-consistency re-run pending.
- [x] § 9.1 Methodological recursion reframed as temporal-constraint scope (D2, D4, D5).
- [x] § 9.2 Cross-tier weakening assessment (D3) — criteria (i)/(ii)/(iii) all NOT triggered.
- [x] § 9.3 Forward-promotion pathway documented (D8).
- [x] § 10 Conditions C1-C10 populated and marked Applied in v2; D1-D15 marked Applied in v3 (this changelog).
- [x] § 11 Implementation order with dependency-ordered migration + tiered rollout + post-cliff handling (D6).
- [x] § 12 Open questions resolved; OQ5 reframed under temporal-constraint scope.
- [x] § 13 Methodological recursion meta-signal documented under temporal-constraint framing.
- [x] § 17 Fix ledger entries for v1 → v2 and v2 → v3.

End of v3 draft. PROCEED-TO-SELF-CONSISTENCY-RERUN.
