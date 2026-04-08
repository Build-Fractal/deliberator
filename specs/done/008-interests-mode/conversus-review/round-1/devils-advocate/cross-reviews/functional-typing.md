# Cross-Review of functional-typing's Review

**Cross-reviewer**: devils-advocate
**Reviewing**: functional-typing's review of spec 008 implementation in SKILL.md
**Date**: 2026-03-22

---

## Dangerous Contradictions

### 1. functional-typing's P0 recommendation undermines the very improvement it acknowledges

functional-typing identifies that SKILL.md replaces the spec's `ambiguous` row (defaulting to `cooperative` at Low confidence) with heuristic signal detection, calls this "arguably more sophisticated," and then recommends fixing it by adding a fallback to `cooperative` when no signals are detected.

This contradicts my review's core challenge: the decision matrix's confidence labels are fabricated across the board, not just for the ambiguous case. functional-typing treats the four "High" confidence mappings as settled and only questions the missing fifth row. But the `ambiguous -> cooperative` default in the spec is itself an arbitrary choice — it asserts that when we know nothing, we should assume collaboration. That assumption is baseless. Many ambiguous problems turn out to be selection problems where cooperative mode produces mushy consensus instead of a clear winner.

The dangerous contradiction: functional-typing's P0 fix would hardcode a fallback that enshrines bad defaults. If heuristic detection finds no signals, the honest answer is "I cannot determine the right mode" — not "default to cooperative." Adding the spec's `cooperative` fallback would make the SKILL.md implementation worse, not better, by replacing the current behavior (which asks the user to choose via mixed-signal handling) with an unearned default. functional-typing's own analysis notes that the mixed-signal handling "asks the user to choose rather than defaulting to cooperative" — and frames this as a problem. It is a feature.

**Resolution needed**: The spec should drop the `ambiguous` row entirely and replace it with an explicit "ask the user" directive when heuristic detection is inconclusive. The SKILL.md already does this correctly. The spec should catch up, not the other way around.

### 2. functional-typing accepts FR-011 compliance at face value while the Preset field violates it

functional-typing's FR-011 verdict is "Fully covered, verbatim match" — SKILL.md line 1231 says "The file MUST use the exact same schema as hand-crafted configs. No schema extensions." functional-typing then separately flags the `Preset` field in `interests.md` as a P1 issue (schema divergence from the spec).

But there is a deeper problem that functional-typing does not flag: SKILL.md line 1260 says "If an interest referenced a preset, include `preset: <category/preset-name>` on the agent entry instead of inlining the prompt." This means the generated `conversus.yml` would contain a `preset:` key on agent entries. Is `preset:` part of the "exact same schema as hand-crafted configs"? The run engine schema (SKILL.md lines 52-104) does support preset resolution, so this may be valid — but functional-typing declares FR-011 "fully covered" without verifying that `preset:` on an agent entry is part of the established schema. If it is not, then the generated YAML does extend the schema, and FR-011 is violated by the implementation's own design.

This contradiction matters because functional-typing's review gives the impression that schema compliance is clean when it may not be. The `Preset` field in `interests.md` is flagged as a P1, but the `preset:` key in the generated `conversus.yml` — which is the actual machine-consumed output — gets no scrutiny at all.

### 3. functional-typing recommends adding the Preset field to the spec schema, but this creates a new consistency obligation it does not account for

functional-typing's P1 recommendation says: "Add `Preset` field to spec schema (spec.md ~line 87)." The reasoning is that FR-006 already mandates preset support, so the schema should reflect it.

But adding `Preset` to the `interests.md` schema creates a new staleness vector that neither the spec nor functional-typing's review addresses. If a preset is updated or deleted after `interests.md` is written, the `Preset` reference becomes stale. The spec's staleness detection (FR-013) only tracks `interests.md` vs `conversus.yml` modification times. It does not track preset changes vs `interests.md`. functional-typing's recommendation introduces a new coupling surface without requiring corresponding staleness detection — precisely the kind of silent coupling my review warns about in the `interests.md` artifact generally.

---

## Tensions

### 1. functional-typing's "additive and conservative" verdict vs. my "coupling artifact" concern

functional-typing's Off-Base Assumptions section concludes: "The SKILL.md implementation is conservative and additive. Every extension beyond the spec is operationally necessary detail." My review argues the opposite about `interests.md` specifically — that it is a coupling artifact with unclear value, duplicating information that ends up in `conversus.yml` and introducing staleness tracking overhead without a demonstrated workflow benefit.

These positions are in genuine tension. functional-typing views the three-file chain (`problem.md` -> `interests.md` -> `conversus.yml`) as a faithful implementation of the spec's intended workflow. I view it as unnecessary indirection. Neither of us is provably wrong, but we cannot both be right about whether `interests.md` as a separate file is "operationally necessary."

The resolution likely depends on real usage data. If users routinely edit `interests.md` between `interests` and `mode` runs — reordering interests, tweaking prompts, adding docs — then the separate file earns its keep. If users always run `interests` then immediately run `mode` without touching the intermediate file, it is ceremony.

### 2. functional-typing treats the `--output` flag as benign; it may not be

functional-typing notes the `--output` flag as "a practical convenience" that "does not conflict with the spec." But `--output` changes where `problem.md` is read from (SKILL.md line 949: "Also changes where `problem.md` is read from"). This means `--output` is not just a write-path override — it is a read-path override that changes the command's input sources. A user could run `/conversus interests --output /some/other/dir` expecting to write interests there while reading `problem.md` from the current directory, and instead get "No problem.md found" because the flag redirected the read path.

This is not a contradiction between our reviews, but functional-typing's framing as "benign undocumented extension" understates the risk. The dual read/write semantics of `--output` are a footgun that the spec should either explicitly define or the implementation should split into `--output` (write) and `--input` (read) flags.

### 3. CLARIFY-tag handling: functional-typing's recommendation may conflict with the define handler's intent

functional-typing recommends (P1 item 3): "If the Type field contains a `[CLARIFY: ...]` tag, extract the best-guess type from the tag text and use it for calibration. Warn the user that the problem type is unconfirmed."

My review raises a related but distinct concern: the define spec says status is "a factual annotation — whether downstream commands treat `draft` as blocking is defined by those commands' specs" (SKILL.md line 889), and spec 008 never defines this. functional-typing's recommendation would have the interests command silently proceed with an unresolved CLARIFY tag, treating it as a usable (if unconfirmed) type. But the original define handler's use of `[CLARIFY: ...]` implies "this needs human resolution" — not "use the best guess and move on." If the interests command extracts a type from a CLARIFY tag without requiring the user to resolve it, it undermines the define handler's intentional ambiguity marker.

The tension is between functional-typing's pragmatic "keep moving" approach and the define handler's signal that unresolved questions should stay unresolved until the user addresses them. The safer behavior is to treat CLARIFY-tagged types as equivalent to "ambiguous" and trigger heuristic detection, rather than extracting a guess.

### 4. Scope of review: functional-typing audits FR compliance, my review questions the FRs themselves

functional-typing's review is structured as a point-by-point FR compliance check. It asks: "Does the SKILL.md implement what the spec requires?" My review asks: "Should the spec require what it requires?" These are complementary but occasionally conflicting lenses. functional-typing marks FR-007 as "Partially covered" because SKILL.md omits the `ambiguous` row — treating the spec as authoritative. My review argues the spec's `ambiguous` row is wrong and should be removed — treating the spec as challengeable.

This tension is methodological, not substantive, but it affects how the recommendations should be weighted. functional-typing's recommendations drive toward spec-implementation alignment. My recommendations drive toward spec improvement. When these conflict (as in the `ambiguous` row case), the question is whether we are optimizing for consistency with a flawed spec or for correctness of the resulting system.

---

## Safe Agreements

### 1. FR-011 schema identity is the right constraint

Both reviews agree that FR-011 (generated YAML uses the same schema as hand-crafted configs, no extensions) is correct and important. functional-typing notes the verbatim match. My review cites it as "the right call — no schema extensions means no bifurcation." Schema identity between generated and hand-crafted configs prevents a two-tier ecosystem where generated configs have different capabilities or limitations.

### 2. User confirmation gates are necessary and correctly placed

Both reviews agree that the user confirmation requirements (spec lines 38, 55, 103-104; SKILL.md lines 1020, 1210) are correctly implemented and necessary. functional-typing traces the confirmation gates through FR-005, FR-009, FR-012. My review acknowledges that these gates are "already provided" and that "the spec already requires confirmation." Neither review suggests removing or weakening any confirmation gate.

### 3. The spec's existing-file handling is solid

functional-typing's FR-005 and FR-012 verdicts are "Fully covered." My review does not challenge the existing-file handling for either `interests.md` or `conversus.yml`. The three-option pattern (add/remove/modify for interests, overwrite/cancel for config) with mandatory diff display is reasonable UX that both reviews implicitly endorse.

### 4. Preset integration should remain optional

functional-typing notes that FR-006 is "Fully covered" with preset matching as "best-effort and optional." My review agrees: "The soft dependency on spec 004 is appropriate — the interests command works without presets but is better with them." Both reviews treat the MAY in FR-006 as correctly calibrated.

### 5. SC-005 prerequisite routing is correctly implemented

functional-typing explicitly calls out that SC-005 (routing to `/conversus define` when `problem.md` is missing) is "correctly implemented" and notes the SKILL.md's three-case dispatch as "a positive addition." My review does not challenge this behavior. The prerequisite chain is sound.

### 6. Agent name validation is consistent

functional-typing notes the `[a-z0-9][a-z0-9-_]*` pattern match between spec line 964 and SKILL.md line 198. My review also cites this as consistent (devil's advocate alignment item 4). Both reviews agree the validation pattern is properly shared between the interests handler and the run engine.

### 7. The spec correctly avoids game-theory jargon in user-facing output

Constraint line 103 ("Must NOT require game theory knowledge") is reflected in SKILL.md's plain-language descriptions and the "Do not use game theory terminology" directive (line 1176). Neither review challenges this constraint. functional-typing's FR-007 analysis notes the "Plain-Language Description" column as an addition. My review does not question the plain-language approach. Both reviews implicitly agree that the abstraction layer between internal mode names and user-facing descriptions is appropriate.
