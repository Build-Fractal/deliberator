# Architecture-Purist Cross-Review: non-tech-user-advocate Analysis

## Property Conflicts

### **Capability Parity Without Architectural Foundation**
- **non-tech-user-advocate recommends**: "Implementing capability parity requirements, adding MCP authentication tools" and expanding Desktop Extension from 3 to full tool coverage
- **architecture-purist's concern**: This recommendation treats the symptom (unequal tool counts) rather than the architectural disease (no single source of truth). Adding tools to MCP without addressing the underlying duplication creates more surface area to maintain and more places for implementation drift.
- **Why this is dangerous**: Each new MCP tool requires parallel implementation in CLI, documentation in three places, and introduces new opportunities for behavioral divergence. The O(n×m) maintenance cost scales with every capability added to every surface.
- **Resolution**: Implement the single-source capability registry first, then derive surface-appropriate tool sets mechanically. Capability parity becomes automatic rather than a maintenance burden.

### **Surface-Specific Solutions**
- **non-tech-user-advocate recommends**: "Creating a surface-appropriate design wizard" for Desktop Extension separate from the plugin's conversational wizard
- **architecture-purist's concern**: This violates the principle that surfaces should represent audiences, not implementations. The same capability (configuration guidance) implemented differently on different surfaces creates vendor lock-in and fragments the user mental model.
- **Why this is dangerous**: Users who switch between Claude Desktop and Claude Code will encounter different UX paradigms for the same logical operation. More critically, maintaining two wizards means feature drift is inevitable - one will become more powerful than the other.
- **Resolution**: The configuration wizard should be a single capability with surface-appropriate adapters. The MCP version can use structured prompts while the plugin version uses conversational flow, but both must produce equivalent outcomes.

### **Authentication Distribution Without Foundation**
- **non-tech-user-advocate recommends**: Adding `init`, `login`, `logout`, `status` tools to MCP for Desktop Extension users
- **architecture-purist's concern**: This recommendation adds authentication infrastructure to every surface without establishing the CLI as the foundational authentication layer. Each surface implementing its own auth logic creates security surface area and credential management complexity.
- **Why this is dangerous**: Authentication state becomes fragmented across surfaces. A user who logs in via MCP tools might not be authenticated for CLI operations, creating a confusing user experience and potential security vulnerabilities.
- **Resolution**: Authentication should remain centralized in the CLI layer, with MCP tools acting as thin wrappers that delegate to CLI auth commands. This preserves the single source of truth for security-critical operations.

### **Discovery Tools Proliferation**
- **non-tech-user-advocate recommends**: Discovery tools to expose conversus capabilities through MCP interface
- **architecture-purist's concern**: Hand-written discovery tools violate the introspection principle. The system should know its own capabilities through reflection on the capability registry, not through manually-maintained tool lists that will drift from reality.
- **Why this is dangerous**: Discovery tools become another maintenance surface that must be updated every time capabilities change. Worse, they can lie - showing capabilities that don't exist or hiding ones that do.
- **Resolution**: Discovery should be automatic introspection of the single capability registry. All surfaces get discovery "for free" by querying the same source of truth.

## Missed Vulnerabilities

### **Implementation Drift Inevitability**
- **Attack vector**: As the team adds features under the current architecture, CLI and MCP implementations of the same capability will gradually diverge in behavior, parameters, and error handling. Users will encounter inconsistent experiences and bugs that appear only on specific surfaces.
- **Why non-tech-user-advocate missed it**: Their focus on user equity leads them to recommend feature parity, but they don't address the architectural foundation needed to maintain that parity over time.
- **Impact**: High severity for maintainability. The team will spend increasing amounts of time debugging "works in CLI but not MCP" issues, and users will learn that some surfaces are more reliable than others.

### **Capability Registry Bypass**
- **Attack vector**: Future developers will add capabilities directly to one surface without updating others, because the current architecture makes it easier to modify a single surface than to properly implement across all surfaces.
- **Why non-tech-user-advocate missed it**: They assume good intentions and process adherence, but don't consider how architectural friction shapes developer behavior.
- **Impact**: The capability fragmentation will get worse over time, not better, unless the architecture makes the correct path easier than the incorrect path.

### **Surface Coupling Through Feature Dependencies**
- **Attack vector**: Features that work only when multiple surfaces are present (e.g., plugin wizard generating config that only CLI can run) create hidden dependencies between supposedly independent distribution surfaces.
- **Why non-tech-user-advocate missed it**: Their user-focused perspective sees surfaces as complementary without recognizing the coupling risks.
- **Impact**: Users who install only one surface get an incomplete experience, and the team cannot easily deprecate or modify any single surface without breaking cross-surface workflows.

## Reinforcing Analysis

### **Single-Source Capability Management**
- **Shared finding**: Both analyses identify that the current hand-maintained parallel implementation across surfaces is unsustainable. Architecture-purist calls this "O(n×m) maintenance costs" while non-tech-user-advocate identifies it as causing "future drift" between surfaces.
- **Combined evidence**: The user equity problems (capability gaps) and architectural problems (implementation duplication) have the same root cause - no single source of truth for what conversus can do.
- **Recommended action**: Implement the capability registry as the highest priority change. This simultaneously solves the user equity issues (automatic parity) and architectural issues (eliminates duplication).

### **Discovery Surface Inadequacy**
- **Shared finding**: Both analyses identify that the Desktop Extension's 3-tool install dialog misrepresents conversus capabilities. Architecture-purist calls this "discovery asymmetries" while non-tech-user-advocate calls it "discovery manipulation."
- **Combined evidence**: The install dialog is both architecturally wrong (manual tool list that can drift) and user-hostile (shows minimal capabilities to the least technical audience).
- **Recommended action**: The install dialog must reflect actual capabilities dynamically. This requires both the capability registry (architectural fix) and user-centric discovery tools (user experience fix).

### **CLI as Foundation Layer**
- **Shared finding**: Both analyses recognize that CLI commands should remain the canonical implementation. Architecture-purist explicitly calls for "CLI as the foundational layer" while non-tech-user-advocate accepts that MCP tools should "wrap CLI commands."
- **Combined evidence**: The CLI has the most complete capability set and most mature implementation. Other surfaces work best as projections of CLI functionality rather than independent implementations.
- **Recommended action**: Establish the CLI as the implementation layer with MCP/plugin surfaces as generated wrappers. This preserves architectural cleanness while solving user access problems.

## Impossibility Trade-offs

### **Surface Optimization vs. Implementation Unity**
- **Surface Optimization**: Each surface should provide the best possible UX for its specific environment (conversational wizard in plugin, structured forms in Desktop Extension, rich text in CLI).
- **Implementation Unity**: The same capability should behave identically across all surfaces to avoid user confusion and implementation drift.
- Why the mechanism cannot fully satisfy both: Optimal UX requires surface-specific adaptations that introduce implementation differences. Perfect behavioral consistency requires generic implementations that compromise surface-specific UX.
- **Best balance**: Define capabilities as abstract interfaces with surface-specific adapters. The core behavior (what happens) remains consistent while the interaction patterns (how it happens) can vary appropriately.

### **Discovery Completeness vs. Cognitive Load**
- **Discovery Completeness**: Users should be able to see all available capabilities to make informed decisions about what conversus can do for them.
- **Cognitive Load**: Too many tools in discovery interfaces (install dialog, slash command menu) overwhelm users and reduce the likelihood they'll try any capabilities.
- Why the mechanism cannot fully satisfy both: Complete capability exposure creates choice paralysis, but limited exposure misrepresents system value.
- **Best balance**: Implement progressive disclosure - show core capabilities prominently in discovery interfaces, with mechanisms to explore advanced capabilities for interested users. The single capability registry enables this by supporting both filtered views (essential tools) and complete views (power users).