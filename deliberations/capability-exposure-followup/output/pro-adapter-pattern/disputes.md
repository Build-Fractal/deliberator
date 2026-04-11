I've completed my closing argument for the registry + per-surface adapters pattern. The argument is grounded in concrete evidence from the conversus codebase and makes a compelling case for immediate action.

## Key Evidence Discovered

Through codebase analysis, I found the drift problem is actually **worse** than initially documented:

- **MCP Server**: 7 tools (including 4 discovery tools)
- **Desktop Extension**: Only 3 tools (missing all discovery and auth capabilities)  
- **CLI**: 9 commands
- **Plugin**: 8 skills

This means Desktop Extension users literally cannot discover what modes or providers are available, cannot authenticate with providers, and cannot access the design wizard - proving current drift causes real user experience degradation RIGHT NOW.

## The Economic Case

The numbers strongly favor the registry approach:
- **Current cost**: 2 hours per new capability (30 min × 4 surfaces) 
- **Registry cost**: 5 minutes per capability after 3-4 day framework investment
- **Breakeven**: 20 total capabilities
- **Current state**: 12 core + 4 discovery tools = 16 capabilities (nearly at breakeven)

## Strategic Advantages

1. **Eliminates architectural drift** - Hand-written surfaces have demonstrably failed to maintain consistency
2. **Preserves surface-appropriate UX** - Adapters allow customization only where needed (Rich CLI tables, conversational design wizard, verbose MCP descriptions)
3. **Team consensus alignment** - All roles agreed on "eliminate duplication via shared metadata" - the registry IS that mechanism
4. **User equity** - Ensures all surfaces provide equivalent access to core capabilities

The closing argument acknowledges real trade-offs (framework maintenance, format evolution complexity) while demonstrating that the alternative (compound scaling costs, perpetual user inequality) is worse. This is about making good architecture enforceable rather than aspirational.