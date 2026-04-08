# Feature Specification: Agent Antipattern Steering

**Feature Branch**: `010-antipattern-steering`
**Created**: 2026-03-20
**Status**: Draft
**Input**: Observed agent behavioral regression where deliberation agents invented a manually-maintained status cache (STATUS.md taxonomy) duplicating speckit's existing task-checkbox tracking, then spent multiple deliberation cycles maintaining the cache instead of doing substantive work.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Record Observed Antipatterns (Priority: P1)

A project maintainer observes an agent behavioral pattern that wasted effort — like creating a tracking artifact that duplicates existing infrastructure. The maintainer wants to record this antipattern with its context, symptoms, root cause, and correction so that future agents avoid repeating the same mistake.

**Why this priority**: Without a place to record antipatterns, the same mistakes recur across conversations and deliberations. Each recurrence burns agent cycles and human review time. This is the foundational capability — everything else builds on having a catalog.

**Independent Test**: Record one antipattern entry and verify it contains enough context for an agent to recognize the pattern and avoid it.

**Acceptance Scenarios**:

1. **Given** no antipattern catalog exists, **When** the maintainer records the "redundant-cache" antipattern, **Then** a catalog entry is created with: name, symptoms, root cause, example, and correction.
2. **Given** an antipattern entry exists, **When** a new contributor reads it, **Then** they can identify whether their current work exhibits the same pattern without having seen the original incident.
3. **Given** multiple antipatterns are recorded, **When** a contributor browses the catalog, **Then** entries are scannable by name and one-line summary without reading full details.

---

### User Story 2 - Agent Pre-Task Steering (Priority: P1)

A deliberation agent is about to propose creating a new tracking document. Before committing to the approach, the agent checks whether this pattern matches any known antipatterns. If it matches "redundant-cache," the agent adjusts its approach — using existing speckit artifacts instead of creating a new one.

**Why this priority**: Recording antipatterns has no value if agents don't consult them. Pre-task steering is the mechanism that closes the loop between observation and prevention.

**Independent Test**: An agent prompt includes an instruction to check antipatterns before proposing new artifacts. The agent reads the catalog and adjusts behavior accordingly.

**Acceptance Scenarios**:

1. **Given** the antipattern catalog contains "redundant-cache," **When** an agent considers creating a new status-tracking document, **Then** the agent recognizes the pattern and proposes using existing task checkboxes instead.
2. **Given** the antipattern catalog is empty or the agent's current work doesn't match any entries, **When** the agent checks, **Then** no false positives are raised and the agent proceeds normally.
3. **Given** the catalog grows beyond 10 entries, **When** an agent checks it, **Then** the check remains fast — the agent reads a summary index, not every full entry.

---

### User Story 3 - Contextual Retrieval (Priority: P2)

As the antipattern catalog grows, loading all entries into agent context becomes wasteful. A contributor or agent needs to retrieve only the antipatterns relevant to what they're currently doing — for example, when working on status tracking changes, retrieve antipatterns tagged with "status tracking" or "artifact duplication."

**Why this priority**: At small catalog sizes (<10 entries), a flat file works. Beyond that, retrieval by relevance prevents context bloat. This is a scaling concern, not a launch blocker.

**Independent Test**: Tag an antipattern with keywords, then retrieve it by keyword match. Verify irrelevant entries are excluded.

**Acceptance Scenarios**:

1. **Given** 15 antipatterns exist with keyword tags, **When** an agent searches for "tracking" or "cache," **Then** only entries tagged with those keywords are returned.
2. **Given** an agent is working on a conversus deliberation task, **When** it queries the catalog with task-derived keywords, **Then** relevant antipatterns surface without loading the full catalog.

---

### Edge Cases

- What happens when two antipatterns conflict (e.g., "don't create tracking documents" vs. "always document cross-cutting status")? Each entry includes a "when this does NOT apply" section to bound its scope.
- What happens when an antipattern is later determined to be wrong? Entries can be deprecated with a note explaining why the guidance changed.
- What happens when the catalog itself becomes a maintenance burden? The catalog is append-mostly and entries are self-contained — no cross-referencing obligations.

## Requirements *(mandatory)*

### Functional Requirements

#### Catalog Structure (P1)

- **FR-001**: An antipattern catalog MUST exist as a structured document in the project
- **FR-002**: Each antipattern entry MUST include: name, one-line summary, symptoms (how to recognize it), root cause (why agents do this), example (specific observed instance with references), correction (what to do instead), and scope (when this does NOT apply)
- **FR-003**: The catalog MUST include a summary index at the top listing each antipattern by name and one-line summary for quick scanning
- **FR-004**: Antipattern entries MUST be self-contained — reading one entry provides full context without cross-referencing other entries

#### Agent Integration (P1)

- **FR-005**: Conversus agent prompts MUST include an instruction to check the antipattern catalog before proposing new artifacts, tracking documents, or process changes
- **FR-006**: The antipattern check instruction MUST reference the catalog location and specify that agents read the summary index first, then full entries only for matches

#### Contextual Retrieval (P2)

- **FR-007**: Each antipattern entry MUST include keyword tags for retrieval
- **FR-008**: A retrieval mechanism MUST exist that returns only entries matching provided keywords, without requiring the full catalog to be loaded into context

#### Catalog Maintenance (P2)

- **FR-009**: Antipattern entries MAY be deprecated by adding a deprecation note — deprecated entries remain in the catalog but are excluded from the summary index
- **FR-010**: New entries MUST NOT require modifying existing entries — the catalog is append-mostly

### Key Entities

- **Antipattern Entry**: A structured record describing one observed agent behavioral mistake. Contains name, summary, symptoms, root cause, example, correction, scope, and keyword tags.
- **Summary Index**: A scannable list at the top of the catalog showing antipattern names and one-line summaries. This is what agents read first to determine relevance.
- **Keyword Tag**: A term associated with an antipattern entry enabling retrieval by topic (e.g., "tracking," "cache," "artifact-creation," "deliberation-drift").

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: An agent encountering a known antipattern scenario can identify the match and adjust its approach within one check — zero repeated instances of previously cataloged antipatterns
- **SC-002**: The antipattern check adds less than 30 seconds of overhead to an agent's task startup — agents read a summary index, not full entries
- **SC-003**: The catalog supports at least 50 entries before retrieval performance degrades — keyword-based retrieval scales linearly
- **SC-004**: 100% of cataloged antipatterns include a concrete example from an observed incident — no hypothetical-only entries

## Assumptions

- The initial catalog is seeded with the "redundant-cache" antipattern observed during the STATUS.md/specs 007-008 incident. Additional entries are added as antipatterns are observed.
- The catalog lives in the conversus project directory, accessible to all agents spawned for deliberations.
- For P1, keyword retrieval is a simple text match (grep-equivalent). Semantic search is a future enhancement when the catalog exceeds the size where text match is sufficient.
- Agent prompt integration means adding a brief instruction to conversus SKILL.md or templates — not modifying the agents' core behavior.
- The antipattern catalog is descriptive (observed patterns from real incidents), not prescriptive (hypothetical rules). Every entry must reference a real example.
