I'll analyze the capability exposure boundaries proposal from the pragmatist-maintainer perspective, focusing on maintenance costs and long-term sustainability. Let me first read the proposal and then write my analysis.

I've completed my analysis as the pragmatist-maintainer, focusing on the long-term maintenance costs and sustainability of the capability exposure mechanism. The analysis identifies critical vulnerabilities in the current approach, particularly:

**Key findings:**
- **Implementation duplication** is creating 3x maintenance burden for core capabilities
- **Capability proliferation** without retirement processes leads to unbounded maintenance debt  
- **Discovery surface fragmentation** misleads users about system capabilities
- **O(capabilities × surfaces) scaling** is economically unsustainable for a small team

**Top recommendations:**
1. **Single-source-of-truth registry** to eliminate duplication and prevent drift
2. **Explicit capability retirement process** to bound maintenance debt
3. **Minimize MCP tool surface** to reduce cognitive load and maintenance cost
4. **Reject discovery tools** in favor of static documentation

The analysis emphasizes that every capability is a long-term maintenance liability, and the current trajectory of organic growth across multiple surfaces will become unmaintainable. The recommendations prioritize sustainability over feature completeness, which aligns with the pragmatic constraint of working with a small team that needs to ship and maintain software long-term.