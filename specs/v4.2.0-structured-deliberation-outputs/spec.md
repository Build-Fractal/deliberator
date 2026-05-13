# Feature Specification: v4.2.0 Structured Deliberation Outputs (JSON Schema)

**Feature ID:** `v4.2.0-structured-deliberation-outputs`
**Created:** 2026-05-12
**Status:** **v2 / post-originating-arbitration / pre-self-consistency-verification** (2026-05-13)
**Depends On:** v4.1.0-persistence-contract-discipline (Tier 2 Principle XXVIII must be ratified; that ratification — commit `551f647` in `clariti-care/payer-index-mono`, `build-fractal/conversus/CONSTITUTION.md` L490-644 — is the doctrinal anchor this spec implements).
**Governed by:** `https://github.com/clariti-care/payer-index-mono/blob/main/build-fractal/conversus/GOVERNANCE.md` § Pathway Taxonomy (**MINOR** pathway — additive component-tier discipline; no existing principle removed, renamed, or substantively re-scoped).
**Pathway:** MINOR
**Tier target:** **Component (Tier 3)** — conversus-oss-specific implementation of Tier 2 Principle XXVIII. Tier placement was **TIER-3-CONFIRMED** by the originating arbitration (`deliberations/v4.2.0-structured-deliberation-outputs-originating-2026-05-12/arbitration/resolution.md` Q3).

---

## Changelog: v1 → v2

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

A schema bump that *would* be MINOR by raw schema diff but breaks consumers because of a field-name dependency is classified MAJOR. The validator carries a single `current_supported_versions` allowlist (per Principle XXVIII C2 versioning gate). Outputs with `schema_version` outside the allowlist fail validation.

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

### 5.1 Engine changes (`conversus-oss/engine/`)

- **`engine/schema/v1/*.schema.json`** — JSON Schema files, one per output type plus the envelope plus the validator-error schema, anchored at `$id` base `https://build-fractal.org/conversus/schema/v1/`. JSON Schema Draft 2020-12. The Python `jsonschema` library (>= 4.x) is the canonical validator; it satisfies Principle XXVIII C2's mechanical-enforceability bar (binary pass/fail, field-presence check, type check, value-constraint check) without the XSD strawman's CDATA-escaping defect.
- **`engine/schema_validator.py`** — single entry point invoked on every agent output write. Signature: `validate_output(path: Path, content: bytes) -> ValidationResult`. Implementation uses `jsonschema.Draft202012Validator` against the envelope schema (which `$ref`s the per-type body schemas via the `allOf`/`if`/`then` discriminator pattern). Failure raises `SchemaViolation` carrying an array of `ValidatorError` objects conformant to § 4.9. The engine logs the error array to the deliberation event stream and aborts the phase (does not write the malformed file).
- **`engine/persistence.py`** — modified to call `validate_output` before `Path.write_bytes`. Atomic: validation success precedes file write; failure leaves no partial state.
- **`engine/templates.py` + `templates/{mode}/`** — mode templates updated so agent prompts emit prose in explicit slots (e.g., `<<<STRENGTHS_BEGIN>>> ... <<<STRENGTHS_END>>>`). The engine's output wrapper parses agent prose, extracts slot values, and assembles a JSON envelope. Agents do NOT emit JSON directly; the engine assembles.
- **`engine/cli/run.py`** — adds `--validate-outputs` flag (default `true`). `--no-validate-outputs` disables for debugging; the engine logs a prominent warning when disabled and records the disable in the deliberation event stream (so post-hoc audits can detect bypassed validation).

**Performance budget (C2): validation MUST complete in <100ms per output.** This is a hard ceiling for write-time validation against the envelope schema with embedded per-type body validation. The `jsonschema` library on representative production-sized outputs (~20-50KB JSON) routinely completes in single-digit milliseconds; the 100ms ceiling provides ~10-20× headroom. **If a validator implementation exceeds 100ms, the validator is the bug, not the schema** — fix the validator (caching compiled schemas, profiling hot paths) before relaxing the budget. The performance budget is enforced by a CI gate that runs the validator over the worked-example fixture corpus and asserts P99 latency < 100ms.

Advanced validations beyond write-time scope — cross-reference integrity (does `ruling_lines[i].question` match a real `per_question_rulings[j].question`?), full constraint validation across documents — run at a separate CI-time phase, not at write time, per C5's tiered staging.

### 5.2 Companion markdown rendering

- **`engine/render_md.py`** — pure function `json_to_md(json_path: Path) -> str`. The engine writes both `phase-1/review.json` (canonical) and `phase-1/review.md` (rendered companion) on every phase. The `.md` companion is regenerable from JSON; if someone edits `.md` directly, CI gates fail (the renderer is the only sanctioned writer of `.md` files under `deliberations/**`).
- Default rendering: section headings per output type, agent identity in the H1, structured body as nested H2/H3, enum values in backticks. The rendering is deterministic and reproducible.

### 5.3 Three worked-example fixtures (per Principle XXVIII C6)

- `engine/tests/fixtures/schema/arbitration_conformant.json` — a passing arbitration output with all required elements.
- `engine/tests/fixtures/schema/arbitration_missing_ruling.json` — non-conformant: missing required `per_question_rulings` entry for `Q3`. Validator returns `field_path=/body/per_question_rulings`, `error_code=REQUIRED_FIELD_MISSING` (or `ARRAY_MIN_ITEMS_VIOLATION` depending on shape).
- `engine/tests/fixtures/schema/arbitration_wrong_verdict_type.json` — non-conformant: `"verdict": "MAYBE"` (value outside enum). Validator returns `field_path=/body/per_question_rulings/0/verdict`, `error_code=ENUM_VIOLATION`, `expected_type` listing the enum, `suggested_fix` proposing the closest valid value.

Each fixture is paired with an expected validator output assertion in `engine/tests/test_schema_validator.py`. CI failure on any fixture mismatch blocks merge.

### 5.4 CI gate

- New GitHub Actions workflow `.github/workflows/schema-validate.yml`:
  - Triggers on `pull_request` paths `deliberations/**`, `engine/schema/**`, `engine/schema_validator.py`, `engine/render_md.py`, `engine/tests/fixtures/schema/**`.
  - Runs `python -m engine.schema_validator --all deliberations/` — validates every JSON file under `deliberations/` against the current schema.
  - Runs `pytest engine/tests/test_schema_validator.py` — the three worked-example fixtures + the renderer round-trip test (JSON → MD → JSON must be bit-identical for canonical-form JSON) + the C2 performance budget assertion (P99 < 100ms).
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
- `CONSUMER-CONTRACT.md` (new, repo root) — declares the JSON Schema as a stable surface; lists allowed `schema_version` values; states that the `$id` base URI `https://build-fractal.org/conversus/schema/v1/` is stable across PATCH and MINOR bumps; documents the deprecation policy for retired versions.
- `STATE-FILES.md` (modified, if extant) — updates the deliberation-output entries to reference the new JSON schema location.
- `CLAUDE.md` (modified, repo root) — adds a "Persistence Contract" section linking to `CONSUMER-CONTRACT.md` per Principle XXVIII C1 discoverability requirement (E3 in v4.1.0 — must link from CLAUDE.md and README.md).
- `README.md` (modified, repo root) — adds the same link.

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

---

## 8. Inclusion Criteria (Principle XXVIII satisfaction check)

Per Principle XXVIII's three-prong test and spec 070 (Constitutional Inclusion Criteria):

- **Universal applicability within conversus-oss:** Every deliberation produces all six output types. Schema applies universally to conversus-oss deliberations without exception. The migration window (§ 11) is bounded and time-limited; no permanent carve-out.
- **Mechanical verifiability:** JSON Schema validation is the canonical mechanical-enforcement primitive (binary pass/fail, field-presence check, type check, value-constraint check) with a sub-100ms runtime budget (C2). Three worked-example fixtures (§ 5.3) demonstrate enforcement bite per Principle XXVIII C6.
- **Non-redundance with existing principles:** No existing principle mandates a deliberation output schema. The current markdown templates document expectations but do not enforce them (Bug B and Bug C are existence proofs of unenforced expectations).

---

## 9. Verification methodology

Run the standard four-stage methodology per spec 067, mirroring v4.1.0:

1. **Originating deliberation** (4 agents). Anchor: this spec's content + Principle XXVIII grounding. Agents: engineer, schema-design-expert, adapter-consumer, devils-advocate. Output: `deliberations/v4.2.0-structured-deliberation-outputs-originating-2026-05-12/`. **Status: COMPLETE; APPROVE-WITH-FIXES on Q1+Q2, TIER-3-CONFIRMED + RECURSION-EXEMPTED on Q3; conditions C1-C10 applied to produce this v2.**
2. **Self-consistency verification** (4 different agents). Focus: contradiction with existing engine architecture, mode-template constraints, plugin entry-point partition (free/paid boundary per spec 033). Output: `deliberations/v4.2.0-structured-deliberation-outputs-self-consistency-2026-05-13/`.
3. **Blind verification** (4 fresh agents, no prior context). Focus: pure-reading review of the spec without prior deliberation context.
4. **Ratification.** If combined disposition across all stages is PROCEED-TO-RATIFICATION, the spec promotes to `Build-Fractal/conversus-oss/CONSTITUTION.md` Component-tier principle.

Per v4.1.0 D-conditions D1 and D3: within each verification stage, Q1 constitutional coherence assessment MUST complete before Q2 evidence base adequacy analysis; ratification-blocking issues must be evaluated before enforcement-mechanism design issues.

### 9.1 Methodological recursion — RECURSION-EXEMPTED (per Q3 ruling)

The originating arbitration ruled this spec's own verification trail produces markdown, not JSON: "Implementation proceeds with markdown verification for this spec, JSON mandatory for subsequent specs." (See `deliberations/v4.2.0-structured-deliberation-outputs-originating-2026-05-12/arbitration/resolution.md` Q3.) The verification trail for v4.2.0 itself stays markdown — a fixed point in the migration. This is consistent with Tier 1 Principle II (stable interfaces): asking the verification methodology to migrate its substrate mid-deliberation is exactly the kind of mid-flight interface change Principle II forbids. The methodological-recursion question is logged for post-ratification governance review.

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
| T3 | Blocking CI on structured format | 2026-10-01 | CI blocks merge on schema violations. All new deliberations must be JSON-conformant. Markdown-only paths get explicit deprecation warnings in CI logs. |
| T4 | Markdown deprecation | 2026-12-01 | Engine reads JSON only. Markdown-reading code paths removed. Aligns with Principle XXVIII universal remediation deadline. |

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
- **OQ5 — Methodological recursion.** **RESOLVED: RECURSION-EXEMPTED.** Markdown verification trail stays for v4.2.0; JSON mandatory for subsequent specs. *(Q3 ruling.)*

---

## 13. Footnote: methodology recursion + meta-signal

Running this spec through the four-stage verification uses the methodology whose outputs it schematizes. Two meta-signals to watch for:

- **If the methodology can't sustain its own self-improvement at this stage** — e.g., if the originating deliberation hits Bug A (prompt overflow) or Bug C (trigger miss) while reviewing the very spec that fixes them — that is a strong signal the migration is overdue and should be sequenced ahead of further v4.x amendments. **Status:** Bug C *did* manifest in the originating arbitration (the Phase 5 synthesizer wrote "Remaining Disputes" rather than the engine's expected marker pair; the arbiter dispatch silently missed; manual arbitration was produced — see `deliberations/v4.2.0-structured-deliberation-outputs-originating-2026-05-12/arbitration/resolution.md` "Process Note"). This is real-time confirmation that the spec's structural-detection thesis is correct.
- **If the blind verification surfaces "should this spec require JSON for ITS OWN verification outputs?"** as a load-bearing question, the answer is RECURSION-EXEMPTED per Q3. The verification trail for v4.2.0 itself stays markdown — a fixed point in the migration.

---

## 17. Fix ledger

| Version | Date | Change | Source |
|---|---|---|---|
| v1 | 2026-05-12 | Initial draft. XSD strawman. | Author. |
| v2 | 2026-05-13 | Applied C1-C10 from originating arbitration. C1: format flipped XML+XSD → JSON + JSON Schema (all six body schemas + envelope rewritten in §§ 4.1-4.7; § 5.1 validator architecture rewritten around Python `jsonschema`; § 7 adapter parsing migrated grep/`xmllint` → `jq`/Python `json.load`). C2: <100ms validation budget (§ 5.1) with P99 CI assertion (§ 5.4). C3: dependency-ordered template migration with cooperative-mode pilot (§ 11 step 3). C4: semantic equivalence CI gate during migration window (§ 11.1). C5: four-tier rollout (§ 11). C6: three additional required envelope fields (§ 4.1). C8: SemVer bump qualification with consumer-impact rule (§ 4.8). C9: validator error-object schema (§ 4.9 new). C10: initial schema version `1.0.0-rc.1` (§ 4.8, § 2 goal 2). | `deliberations/v4.2.0-structured-deliberation-outputs-originating-2026-05-12/arbitration/resolution.md` |

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
- [x] § 9 Verification methodology specified; originating stage marked COMPLETE.
- [x] § 10 Conditions C1-C10 populated and marked Applied in v2.
- [x] § 11 Implementation order with dependency-ordered migration + tiered rollout.
- [x] § 12 Open questions resolved by originating arbitration.
- [x] § 13 Methodological recursion meta-signal documented; recursion-exempted per Q3.
- [x] § 17 Fix ledger entry for v1 → v2.

End of v2 draft. PROCEED-TO-SELF-CONSISTENCY.
