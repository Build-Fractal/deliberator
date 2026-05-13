# Feature Specification: v4.2.0 Structured Deliberation Outputs (XML Schema)

**Feature ID:** `v4.2.0-structured-deliberation-outputs`
**Created:** 2026-05-12
**Status:** **v1 / draft / pre-originating-deliberation**
**Depends On:** v4.1.0-persistence-contract-discipline (Tier 2 Principle XXVIII must be ratified; that ratification — commit `551f647` in `clariti-care/payer-index-mono`, `build-fractal/conversus/CONSTITUTION.md` L490-644 — is the doctrinal anchor this spec implements).
**Governed by:** `https://github.com/clariti-care/payer-index-mono/blob/main/build-fractal/conversus/GOVERNANCE.md` § Pathway Taxonomy (**MINOR** pathway — additive component-tier discipline; no existing principle removed, renamed, or substantively re-scoped).
**Pathway:** MINOR
**Tier target:** **Component (Tier 3)** — conversus-oss-specific implementation of Tier 2 Principle XXVIII. *(See § 13 for the open question about whether suite-wide Tier 2 placement is more appropriate; the originating deliberation should resolve this.)*

---

## 1. Motivation

Tier 2 Principle XXVIII ("Persistence Contract Discipline") was ratified 2026-05-12 (`build-fractal/conversus/CONSTITUTION.md` L490-644) with a universal 2026-12-01 remediation deadline for all conversus-suite products. The principle mandates: declared schemas with `schema_version` (SemVer), mechanical CI enforcement, versioning bump procedure, cross-product `CONSUMER-CONTRACT.md` files declaring stable surfaces, and explicit declaration scope. Schema declaration without mechanical enforcement is itself a violation.

Conversus-oss's load-bearing persistent state surface is the **deliberation output set** — six output types produced per phase per deliberation. These outputs are persisted to disk under `deliberations/{deliberation-id}/`, consumed by:
- Subsequent phases within the same deliberation (e.g., phase 5 synthesis reads phases 1-4 outputs);
- The arbiter's grep-based triggers (e.g., `disputes_remain`);
- The spec-kit-orc adapter (`scripts/dispatch/adapters/tool/conversus.sh`), which currently parses markdown headings to extract verdicts;
- Human readers reviewing the audit trail.

Today the contract between producer (agent prose) and consumers (engine triggers, downstream phases, spec-kit-orc adapter) lives in **display text** — markdown headings, prose patterns, and parser-grep regexes — and silently short-circuits when prose drifts. This spec is the first concrete implementation of Principle XXVIII for conversus-oss.

### 1.1 Three recurring production bugs this spec addresses

These are the load-bearing motivation. The spec must cite each one as an existence proof that the current display-text contract is broken.

**Bug A — Phase 5 prompt-overflow crash (recurring).** Synthesis prompt assembles all phase 1-4 outputs as free-form markdown concatenation. Two production incidents documented:
- 2026-05-06 arbitration silent-failure: synthesis prompt exceeded ~230K chars, arbitration phase dispatched then crashed silently in ~1ms (memory: `project_conversus_arbitration_crash_2026_05_06.md`). Phases 1-5 succeeded; only arbitration crashed at dispatch.
- v4.1.0 originating deliberation (2026-05-11): same class of overflow, different manifestation — rate-limit response surfaced rather than silent crash, but root cause identical (unbounded prose concatenation).

Both incidents stem from synthesis output being unbounded prose. XML structure constrains the prompt assembly path: the engine can serialize only specific fields (e.g., `<verdict>` + `<conditions>` without `<rationale>` prose), bounding synthesis prompt size deterministically.

**Bug B — Phase 2 cross-review persistence quirk.** Engine warnings show cross-review files expected at `{agent}/cross-reviews/{other-agent}.md` sometimes don't persist to disk; downstream phases consume "in-memory" cross-reviews that aren't on disk. Format-contract drift between agents' emitted markdown structure and engine's file-storage expectations: agents emit headings/structure that the engine's writer doesn't recognize as a valid cross-review, so the writer silently elides them. This is a class-of-bug expression of "contract lives in display text" — the storage layer's parse contract is undocumented and grep-fragile.

**Bug C — Phase 6 `disputes_remain` trigger silently missed.** The v4.1.0 blind-verification synthesis used "Critical Unresolved Tensions" terminology where the engine grep-matches for `DISPUTES_BEGIN`/`DISPUTES_END` markers. Arbiter didn't fire even though tensions existed; manual arbitration was required (memory: `project_conversus_pr23_meta_cl.md`, "manual challenge-loop orchestration pattern"). **This bug is the cleanest example of why XML schema enforcement matters** — an agent emitting prose that happens not to match the engine's parser regex causes the engine to silently skip the dispute-resolution phase. Under XML schema, the trigger becomes `count(synthesis/disputes/dispute) > 0` — structural, not regex.

### 1.2 Doctrinal anchor

Principle XXVIII sub-clause 1 mandates declared schemas in a discoverable location. Sub-clause 2 mandates mechanical CI enforcement. Sub-clause 3 mandates `schema_version` (SemVer by default). Sub-clause 4 mandates `CONSUMER-CONTRACT.md` declaring stable surfaces consumed by cross-product code. Sub-clause 5 mandates explicit declaration of display-text surfaces (or migration off them). This spec satisfies all five sub-clauses for the conversus-oss deliberation output set.

---

## 2. Goals

1. **Single XML schema family** defining all six conversus deliberation output types, with a common envelope (agent identity, deliberation context, timestamp, target file refs, `schema_version`) plus per-type bodies. Namespace `https://build-fractal.org/conversus/schema/v1`.
2. **`schema_version` field on every output**, populated by the engine at write time, conforming to Principle XXVIII sub-clause 3 (SemVer with documented total ordering).
3. **PR-required CI gate** validating every agent output against the schema before commit, per Principle XXVIII sub-clause 2. The gate runs in `conversus-oss` CI on every PR that touches `deliberations/**` or `engine/**`; failures block merge.
4. **Backward-compatibility / migration path** for existing markdown-format deliberation outputs. The v4.1.0 audit trail (4 deliberations, ~150 markdown files) must remain readable. Migration strategy in § 11.
5. **Human-readable rendering path.** XML outputs include an inline XSLT reference (or are accompanied by an engine-generated `.md` companion) so the audit trail is human-readable without specialized tooling. Default: XML is canonical; companion `.md` is rendered-for-humans, regenerable from XML.
6. **`CONSUMER-CONTRACT.md`** at conversus-oss repo root declaring the XML schema as a stable surface consumed by the spec-kit-orc adapter (and any future conversus-suite consumer), per Principle XXVIII sub-clause 4.

---

## 3. Non-goals

- **Not** proposing XML for non-deliberation conversus artifacts (engine state, provider auth tokens, evaluation results, mode templates). Those are separate persistent state surfaces with their own contract decisions to make.
- **Not** mandating XML for `CONSTITUTION.md`, `CONFORMANCE.md`, `COMPLIANCE.md`, or `GOVERNANCE.md`. Constitutional documents have their own conventions (markdown with structured headings) and are out of scope.
- **Not** requiring agents to write XML directly in their prose. Agents emit structured prose in defined slots; the engine wraps in XML envelope on write. Agent prompts change; agent output format from the agent's perspective stays close to current prose conventions (with explicit field markers).
- **Not** replacing the engine dispatch architecture, the phase pipeline, or the agent abstraction. This spec changes only the format of the artifacts written to disk and consumed by downstream phases + external consumers.
- **Not** prescribing XSD vs RelaxNG vs JSON Schema for the validator. Per Principle XXVIII's format-choice non-mandate, the spec proposes XML as the wire format, with the validator implementation TBD (XSD is the strawman; alternatives evaluated in § 5).
- **Not** retroactively re-emitting historical deliberation outputs in XML. The migration path (§ 11) is forward-only: new deliberations use XML; historical markdown deliberations remain as-is and continue to render readably.

---

## 4. Schema

### 4.1 Common envelope

Every output document is wrapped in `<conversus-output>` with the following attributes:

```xml
<conversus-output xmlns="https://build-fractal.org/conversus/schema/v1"
                  schema_version="1.0.0"
                  output_type="review|cross-review|revision|disputes|synthesis|arbitration"
                  agent_name="pragmatist|tier-coherence-auditor|..."
                  deliberation_id="v4.2.0-structured-deliberation-outputs-originating-2026-05-12"
                  phase_iteration="1"
                  timestamp="2026-05-12T15:42:08Z"
                  target_files="specs/v4.2.0-structured-deliberation-outputs/spec.md">
  <!-- per-type body -->
</conversus-output>
```

Required attributes: `xmlns`, `schema_version`, `output_type`, `agent_name`, `deliberation_id`, `timestamp`. Optional: `phase_iteration` (omitted for single-iteration phases), `target_files` (comma-separated list of paths relative to repo root; omitted for synthesis/arbitration where the target is the deliberation as a whole).

`output_type` MUST be one of the six enum values. Validator rejects all other values.

### 4.2 `<review>` (Phase 1 — initial review per agent)

```xml
<review>
  <summary_assessment>One-paragraph high-level take on the target docs.</summary_assessment>
  <strengths>
    <point id="S1">...</point>
    <point id="S2">...</point>
  </strengths>
  <concerns>
    <point id="C1" severity="blocking|substantive|nit">...</point>
  </concerns>
  <questions>
    <question id="Q1">...</question>
  </questions>
  <recommendation>APPROVE-AS-DRAFTED|APPROVE-WITH-FIXES|BLOCK|ABSTAIN</recommendation>
</review>
```

`severity` is an enum: `blocking` (must-fix for ratification), `substantive` (should-fix), `nit` (cosmetic). The engine routes blocking concerns into the dispute set for phase 2.

### 4.3 `<cross-review>` (Phase 2 — agent X reviews agent Y's review)

```xml
<cross-review reviewing_agent="pragmatist">
  <agreement_points>
    <point ref="S1">Agree with strength S1: ...</point>
  </agreement_points>
  <disagreement_points>
    <point ref="C2" stance="disagree|partial-disagree">
      <our_position>...</our_position>
      <their_position>...</their_position>
    </point>
  </disagreement_points>
  <new_concerns_raised>
    <point id="CR1" severity="blocking|substantive|nit">...</point>
  </new_concerns_raised>
</cross-review>
```

`reviewing_agent` names whose review is being cross-reviewed; the wrapper `agent_name` in the envelope names the cross-reviewer. The `ref` attribute on `<point>` lets phase 5 trace dispute lineage back to phase 1 origins. **This fixes Bug B**: cross-review files have a deterministic structure the engine writer recognizes; format drift can't elide them.

### 4.4 `<revision>` (Phase 3 — agent updates own position)

```xml
<revision iteration="1">
  <position_changes>
    <change ref="C1" delta="strengthened|softened|withdrawn|unchanged">
      <prior>...</prior>
      <revised>...</revised>
      <triggered_by>cross-review:tier-coherence-auditor</triggered_by>
    </change>
  </position_changes>
  <updated_recommendation>APPROVE-AS-DRAFTED|APPROVE-WITH-FIXES|BLOCK|ABSTAIN</updated_recommendation>
</revision>
```

`iteration` attribute on `<revision>` matches `phase_iteration` on the envelope; multiple revision iterations are supported (e.g., `revision.md` + `revision_2.md`).

### 4.5 `<disputes>` (Phase 4 — agent consolidates remaining disagreements)

```xml
<disputes>
  <dispute id="D1" severity="blocking|substantive">
    <topic>...</topic>
    <our_position>...</our_position>
    <opposing_positions>
      <position agent="pragmatist" stance="..."/>
      <position agent="strict-reader" stance="..."/>
    </opposing_positions>
    <proposed_resolution>...</proposed_resolution>
    <fallback_if_unresolved>...</fallback_if_unresolved>
  </dispute>
</disputes>
```

### 4.6 `<synthesis>` (Phase 5 — single agent integrates all prior outputs)

```xml
<synthesis>
  <agreement_areas>
    <area>...</area>
  </agreement_areas>
  <disputes>
    <dispute id="D1" severity="blocking|substantive">
      <topic>...</topic>
      <positions>
        <position agent="pragmatist" stance="..."/>
        <position agent="tier-coherence-auditor" stance="..."/>
      </positions>
      <synthesizer_assessment>...</synthesizer_assessment>
    </dispute>
  </disputes>
  <emergent_patterns>
    <pattern>...</pattern>
  </emergent_patterns>
  <recommendation_to_arbiter>...</recommendation_to_arbiter>
</synthesis>
```

**This fixes Bug C**: the engine's `disputes_remain` trigger becomes the XPath expression `count(/conversus-output/synthesis/disputes/dispute[@severity='blocking']) > 0`. Structural, not regex. No prose drift can hide a dispute from the trigger.

**This also fixes Bug A**: the engine's synthesis-prompt assembler can serialize only specific subtrees per downstream consumer — e.g., the arbitration prompt receives `<disputes>` + `<recommendation_to_arbiter>` only, not the full `<agreement_areas>` + `<emergent_patterns>` prose. Synthesis prompt size becomes bounded by the union of dispute count × per-dispute schema-cap, not by free prose.

### 4.7 `<arbitration>` (Phase 6 — arbiter's binding verdict)

```xml
<arbitration>
  <process_note>One paragraph describing how the arbiter weighed evidence.</process_note>
  <decision_framework>One paragraph describing the framework applied (per spec QUESTION.md).</decision_framework>
  <per_question_rulings>
    <ruling question="Q1">
      <verdict>APPROVE-AS-DRAFTED|APPROVE-WITH-FIXES|BLOCK|PASS-WITH-CLARIFICATIONS|FAIL-OVERSTRETCH</verdict>
      <rationale>...</rationale>
      <conditions>
        <condition id="C1" priority="P1|P2">
          <description>...</description>
          <applies_to_section>§ 4 sub-clause 3</applies_to_section>
        </condition>
      </conditions>
    </ruling>
    <ruling question="Q2">...</ruling>
    <ruling question="Q3">...</ruling>
  </per_question_rulings>
  <combined_disposition>PROCEED-TO-RATIFICATION|PROCEED-TO-NEXT-STAGE|RETURN-TO-REVIEW|BLOCK</combined_disposition>
  <ruling_lines>
    <ruling_line question="Q1" verdict="..." rationale="..."/>
    <ruling_line question="Q2" verdict="..." rationale="..."/>
    <ruling_line question="Q3" verdict="..." rationale="..."/>
  </ruling_lines>
</arbitration>
```

`<verdict>` enum is intentionally union-typed across the verdict vocabularies used by originating, self-consistency, and blind verification stages (cf. v4.1.0 spec's verdict vocabulary). The enum is closed; new verdict values require a schema MINOR bump.

The redundant `<ruling_lines>` block (a denormalized projection of `<per_question_rulings>`) exists for adapter convenience — spec-kit-orc currently grep-extracts one-line ruling summaries and benefits from a flat list. Validator enforces that `<ruling_lines>` entries match the question/verdict pairs in `<per_question_rulings>`.

### 4.8 Schema versioning

The wire format version is named in the envelope's `schema_version` attribute. Initial release: `1.0.0`. Bumps follow Principle XXVIII sub-clause 3 (SemVer):
- **MAJOR**: removed elements, removed enum values, type narrowing of existing fields.
- **MINOR**: added optional elements, added enum values, new output types.
- **PATCH**: clarifying restrictions that don't break existing conformant outputs (e.g., tightened regex on a string field that no real output violates).

The validator carries a single `current_supported_versions` allowlist (per Principle XXVIII C2 versioning gate). Outputs with `schema_version` outside the allowlist fail validation.

---

## 5. Implementation

### 5.1 Engine changes (`conversus-oss/engine/`)

- **`engine/schema/v1/*.xsd`** (or `*.json` if JSON Schema chosen) — schema files, one per output type plus the envelope, anchored at namespace `https://build-fractal.org/conversus/schema/v1`. XSD is the strawman per § 3 non-mandate. Alternative validators (Pydantic XML, lxml RelaxNG) acceptable provided they meet Principle XXVIII C2 mechanical-enforceability bar (binary pass/fail, field-presence check, type check, value-constraint check).
- **`engine/schema_validator.py`** — single entry point invoked on every agent output write. Signature: `validate_output(path: Path, content: str) -> ValidationResult`. Failure raises `SchemaViolation` exception; engine logs to deliberation event stream and aborts the phase (does not write the malformed file).
- **`engine/persistence.py`** — modified to call `validate_output` before `Path.write_text`. Atomic: validation success precedes file write; failure leaves no partial state.
- **`engine/templates.py` + `templates/{mode}/`** — mode templates updated so agent prompts emit prose in explicit slots (e.g., `<<<STRENGTHS_BEGIN>>> ... <<<STRENGTHS_END>>>`). The engine's output wrapper parses agent prose, extracts slot values, and wraps in XML envelope. Agents do NOT emit XML directly; the engine wraps.
- **`engine/cli/run.py`** — adds `--validate-outputs` flag (default `true`). `--no-validate-outputs` disables for debugging; the engine logs a prominent warning when disabled and records the disable in the deliberation event stream (so post-hoc audits can detect bypassed validation).

### 5.2 Companion markdown rendering

- **`engine/render_md.py`** — pure function `xml_to_md(xml_path: Path) -> str`. The engine writes both `phase-1/review.xml` (canonical) and `phase-1/review.md` (rendered companion) on every phase. The `.md` companion is regenerable from XML; if someone edits `.md` directly, CI gates fail (the renderer is the only sanctioned writer of `.md` files under `deliberations/**`).
- Default rendering: section headings per output type, agent identity in the H1, structured body as nested H2/H3, enum values in backticks. The rendering is deterministic and reproducible.
- Alternative considered: inline XSLT reference in the XML. Rejected as strawman because XSLT tooling is non-uniform; a pure Python renderer is more portable.

### 5.3 Three worked-example fixtures (per Principle XXVIII C6)

- `engine/tests/fixtures/schema/arbitration_conformant.xml` — a passing arbitration output with all required elements.
- `engine/tests/fixtures/schema/arbitration_missing_ruling.xml` — non-conformant: missing required `<ruling>` element. Validator returns specific error path (e.g., `/conversus-output/arbitration/per_question_rulings`).
- `engine/tests/fixtures/schema/arbitration_wrong_verdict_type.xml` — non-conformant: `<verdict>MAYBE</verdict>` (value outside enum). Validator returns specific error citing the enum.

Each fixture is paired with an expected validator output assertion in `engine/tests/test_schema_validator.py`. CI failure on any fixture mismatch blocks merge.

### 5.4 CI gate

- New GitHub Actions workflow `.github/workflows/schema-validate.yml`:
  - Triggers on `pull_request` paths `deliberations/**`, `engine/schema/**`, `engine/schema_validator.py`, `engine/render_md.py`, `engine/tests/fixtures/schema/**`.
  - Runs `python -m engine.schema_validator --all deliberations/` — validates every XML file under `deliberations/` against the current schema.
  - Runs `pytest engine/tests/test_schema_validator.py` — the three worked-example fixtures + the renderer round-trip test (XML → MD → XML must be bit-identical for canonical-form XML).
  - Pass/fail is binary; failure blocks merge. Required-check setting enforced on the `main` branch.

---

## 6. File edits per repo

### 6.1 `Build-Fractal/conversus-oss/` (this repo)

- `engine/schema/v1/*.xsd` (new) — schema files.
- `engine/schema_validator.py` (new).
- `engine/render_md.py` (new).
- `engine/persistence.py` (modified) — adds validate-then-write.
- `engine/cli/run.py` (modified) — adds `--validate-outputs`.
- `engine/templates.py` + `templates/{mode}/*.md` (modified) — adds slot markers to agent prompts.
- `engine/tests/test_schema_validator.py` (new) + `engine/tests/fixtures/schema/*.xml` (new).
- `.github/workflows/schema-validate.yml` (new).
- `CONSUMER-CONTRACT.md` (new, repo root) — declares the XML schema as a stable surface; lists allowed `schema_version` values; states that the namespace URI `https://build-fractal.org/conversus/schema/v1` is stable across PATCH and MINOR bumps; documents the deprecation policy for retired versions.
- `STATE-FILES.md` (modified, if extant) — updates the deliberation-output entries to reference the new XML schema location.
- `CLAUDE.md` (modified, repo root) — adds a "Persistence Contract" section linking to `CONSUMER-CONTRACT.md` per Principle XXVIII C1 discoverability requirement (E3 in v4.1.0 — must link from CLAUDE.md and README.md).
- `README.md` (modified, repo root) — adds the same link.

### 6.2 `Build-Fractal/orchestrator/` (spec-kit-orc)

- `scripts/dispatch/adapters/tool/conversus.sh` (modified) — replaces the existing grep-of-markdown parser with an XML parser. New parser invokes `xmllint --xpath "//ruling_line/@verdict" {arbitration.xml}` (or equivalent Python `lxml`) to extract verdict lines. Markdown-format outputs are still consumed for backward compatibility during the migration window (§ 11); XML is preferred when both are present.
- `scripts/dispatch/adapters/tool/conversus.adapter.md` (new or modified) — declares the adapter's dependency on the conversus-oss XML schema, names the version range it supports, and references conversus-oss's `CONSUMER-CONTRACT.md`. Mirrors Principle XXVIII C3 (consumer-side declaration).
- Adapter CI: spec-kit-orc CI gains a "conversus-XML-fixture" job that runs the adapter against a vendored copy of conversus-oss's fixture set; failure blocks merge in spec-kit-orc.

### 6.3 `clariti-care/payer-index-mono/build-fractal/conversus/CONFORMANCE.md`

- Update the conversus-oss row to reflect that this spec is the active satisfaction track for Principle XXVIII. Status moves from "Remediation-Blocked" (current, per v4.1.0) to "Remediation-In-Progress" on spec ratification, and to "Compliant" on completion of § 11 step 6.

---

## 7. Cross-product implications

The spec-kit-orc adapter is the load-bearing consumer-side surface. Today the adapter (`scripts/dispatch/adapters/tool/conversus.sh`) hardcodes three brittle paths and grep patterns against conversus-oss outputs. Principle XXVIII C3 mandates `CONSUMER-CONTRACT.md` on the producer side declaring stable surfaces consumed by cross-product code; this spec produces that file.

After ratification:
1. Conversus-oss `CONSUMER-CONTRACT.md` declares the XML schema as stable.
2. spec-kit-orc's adapter declares it consumes that schema (version range `>=1.0.0,<2.0.0` initially).
3. Both products' CI verifies the contract — conversus-oss CI validates every emitted XML; spec-kit-orc CI validates that its adapter correctly parses a vendored fixture set.
4. A schema MAJOR bump in conversus-oss requires coordinated adapter update in spec-kit-orc, sequenced via the cross-repo CI pattern in `build-fractal/conversus/CLAUDE.md` ("Cross-repo work" section).

No other suite product currently consumes deliberation outputs structurally (conversus-enhanced consumes solver outputs, not deliberation outputs). If a future sibling adds a consumer, it inherits the same `CONSUMER-CONTRACT.md` pattern.

---

## 8. Inclusion Criteria (Principle XXVIII satisfaction check)

Per Principle XXVIII's three-prong test and spec 070 (Constitutional Inclusion Criteria):

- **Universal applicability within conversus-oss:** Every deliberation produces all six output types. Schema applies universally to conversus-oss deliberations without exception. The migration window (§ 11) is bounded and time-limited; no permanent carve-out.
- **Mechanical verifiability:** XML schema validation is the canonical mechanical-enforcement primitive (binary pass/fail, field-presence check, type check, value-constraint check). Three worked-example fixtures (§ 5.3) demonstrate enforcement bite per Principle XXVIII C6.
- **Non-redundance with existing principles:** No existing principle mandates a deliberation output schema. The current markdown templates document expectations but do not enforce them (Bug B and Bug C are existence proofs of unenforced expectations).

---

## 9. Verification methodology

Run the standard four-stage methodology per spec 067, mirroring v4.1.0:

1. **Originating deliberation** (4 agents). Anchor: this spec's content + Principle XXVIII grounding. Agents: pragmatist, tier-coherence-auditor, strict-reader, precedent-auditor (or current mode-default set). Output: `deliberations/v4.2.0-structured-deliberation-outputs-originating-2026-05-12/`.
2. **Self-consistency verification** (4 different agents). Focus: contradiction with existing engine architecture, mode-template constraints, plugin entry-point partition (free/paid boundary per spec 033). Output: `deliberations/v4.2.0-structured-deliberation-outputs-self-consistency-2026-05-12/`.
3. **Blind verification** (4 fresh agents, no prior context). Focus: pure-reading review of the spec without prior deliberation context. Output: `deliberations/v4.2.0-structured-deliberation-outputs-blind-2026-05-12/`.
4. **Ratification.** If combined disposition across all stages is PROCEED-TO-RATIFICATION, the spec promotes to `Build-Fractal/conversus-oss/CONSTITUTION.md` Component-tier principle (or to suite Tier 2 per § 13 open question).

Per v4.1.0 D-conditions D1 and D3: within each verification stage, Q1 constitutional coherence assessment MUST complete before Q2 evidence base adequacy analysis; ratification-blocking issues must be evaluated before enforcement-mechanism design issues.

### 9.1 Methodological recursion note

This spec is being verified using the very methodology whose outputs it schematizes. The originating verification runs against the current (markdown-format) templates and produces markdown outputs. The blind verification will likely surface the question: *should this spec require XML for its own verification outputs?* That question is left to § 13 and to the originating arbiter.

---

## 10. Conditions placeholder

Empty for v1. Conditions C1, C2, C3, ... populated by the originating arbitration ruling, then by self-consistency D-conditions, then by blind-verification E-conditions per the v4.1.0 pattern.

---

## 11. Implementation order

1. **Verify spec** via the four-stage methodology (§ 9).
2. **Add schemas + validator + renderer** to conversus-oss. Land as one PR with the three worked-example fixtures and CI gate.
3. **Migrate mode templates** to slot-marker form. Land per-mode as separate PRs (one per mode under `templates/`). Each PR is independently testable: emit a fixture deliberation in that mode, validate the XML, regenerate the MD, diff against expected.
4. **Migrate spec-kit-orc adapter** to XML consumer. Coordinated with conversus-oss `CONSUMER-CONTRACT.md` declaration.
5. **Re-render v4.1.0 audit trail as XML.** This is the validation milestone: take the existing 4 deliberations (originating, self-consistency, self-consistency-rerun, blind) for v4.1.0 — about 150 markdown files — and re-emit each as XML using a one-time `engine/migrate_md_to_xml.py` tool. Validate every emitted XML against the schema. This both backfills the audit trail and proves the schema accommodates real production deliberation outputs.
6. **Update conversus-oss CONFORMANCE.md row to Compliant.** Closes the Principle XXVIII remediation track ahead of the 2026-12-01 universal deadline.
7. **Deprecate markdown-format mode templates.** Announce deprecation date (proposed: 2026-09-01). Archive markdown templates under `templates/_archived_pre_xml/` on the deprecation date. After 2026-12-01, the markdown templates are removed entirely; XML is the only supported output format.

### 11.1 Backward-compatibility window

Between ratification and 2026-12-01:
- New deliberations: XML canonical + MD companion (per § 5.2).
- Historical deliberations (pre-ratification): markdown stays as-is. Optional: re-render via step 5 above.
- Engine reads both formats during the window. The persistence layer prefers XML when both are present.
- spec-kit-orc adapter supports both formats during the window (per § 6.2).
- After 2026-12-01: engine reads XML only. Markdown reading code paths removed.

---

## 12. Open questions for the originating arbitration

The arbiter should rule on the following before § 10 conditions are finalized:

- **OQ1 — Tier placement (Component vs Suite).** This spec defaults to Component (Tier 3) — conversus-oss-specific. The originating arbiter should examine whether Tier 2 (suite-wide) placement is more appropriate. The Tier 2 case: deliberation outputs are the load-bearing persistence surface for every conversus product that runs deliberations (today only conversus-oss; conversus-enhanced runs solvers, not deliberations). The Tier 3 case: only conversus-oss produces these outputs, so suite-wide mandate over-stretches universality. **Recommendation lean: Component (Tier 3).** Re-evaluate at the first conversus-suite sibling that produces deliberation-like artifacts.
- **OQ2 — XSD vs JSON Schema vs Pydantic-XML for the validator.** § 3 non-mandates the choice; § 5.1 strawmans XSD. The arbiter should rule on whether the validator format is left to product-choice (per Principle XXVIII non-format-mandate) or constrained for cross-suite consistency. **Recommendation lean: leave to product-choice; XSD is the default.**
- **OQ3 — Companion MD generation: XSLT inline vs Python renderer.** § 5.2 strawmans the Python renderer. The arbiter should rule on whether portability (Python) outweighs declarativity (XSLT). **Recommendation lean: Python renderer.**
- **OQ4 — Deprecation cliff date.** § 11 proposes 2026-12-01 (alignment with Principle XXVIII universal remediation deadline). The arbiter should rule on whether the cliff date should be earlier (forcing faster migration) or later (allowing longer dual-format window). **Recommendation lean: 2026-12-01 (aligned).**
- **OQ5 — Methodological recursion.** Should this spec mandate XML for its own verification outputs (§ 9.1)? If yes, the originating deliberation runs against this spec but produces markdown outputs — those outputs would be retroactively non-conformant once the spec ratifies. **Recommendation lean: NO. The originating + self-consistency + blind verifications for this spec produce markdown (the format extant at deliberation-time). Subsequent specs that ratify AFTER this one produce XML. The verification trail for v4.2.0 itself stays markdown — a fixed point in the migration.**

---

## 13. Footnote: methodology recursion + meta-signal

Running this spec through the four-stage verification uses the methodology whose outputs it schematizes. Two meta-signals to watch for:

- **If the methodology can't sustain its own self-improvement at this stage** — e.g., if the originating deliberation hits Bug A (prompt overflow) while reviewing the very spec that fixes Bug A — that's a strong signal the migration is overdue and should be sequenced ahead of further v4.x amendments.
- **If the blind verification surfaces "should this spec require XML for ITS OWN verification outputs?"** as a load-bearing question, the answer should be deferred to v2 or v3 of the spec (per OQ5 lean), not resolved in v1. The current verification trail is markdown by necessity (the engine doesn't yet emit XML); enforcing XML retroactively on the deliberation that ratifies XML emission is a chicken-and-egg violation of Principle VII (no retroactive obligations on outputs that predate the rule).

---

## Document status checklist

- [x] § 1 Motivation grounded in three concrete bugs with citations.
- [x] § 2 Goals enumerated (6 goals, each tied to Principle XXVIII sub-clause).
- [x] § 3 Non-goals enumerated (6 non-goals scoping the spec down).
- [x] § 4 Schema specified with inline XML examples for all six output types + envelope.
- [x] § 5 Implementation specified with engine file paths + CI gate.
- [x] § 6 File edits per repo enumerated (conversus-oss + orchestrator + payer-index-mono).
- [x] § 7 Cross-product implications mapped (spec-kit-orc adapter migration).
- [x] § 8 Inclusion criteria checked against Principle XXVIII three-prong test.
- [x] § 9 Verification methodology specified (four stages + recursion note).
- [x] § 10 Conditions placeholder empty (per draft convention).
- [x] § 11 Implementation order specified (7 steps + backward-compat window).
- [x] § 12 Open questions enumerated for the originating arbiter (5 OQs).
- [x] § 13 Methodological recursion meta-signal documented.

End of v1 draft.
