I'll read all the target files and analyze the capability exposure mechanism from the non-technical user advocate perspective. Let me start by reading the proposal and any documentation.

Now let me check for any documentation or other files in the deliberations directory to understand the full context:

Let me check the main conversus-oss directory for documentation files:

Let me read key documentation files to understand the user experience and system:

I've completed the mechanism design review from the non-technical user advocate perspective. The analysis reveals that the current capability exposure mechanism systematically disadvantages non-technical users by:

1. **Violating individual rationality** - Desktop Extension users get only 3 tools while needing terminal access for basic setup (init, login, status)

2. **Creating discovery manipulation** - The install dialog shows minimal capabilities, causing users to dismiss conversus as "just a decide tool" when it supports 8 deliberation modes

3. **Fragmenting essential features** - The guided design wizard exists only in the plugin, completely excluding Claude Desktop users from custom deliberations

4. **Forcing terminal fallbacks** - Authentication and setup require CLI access, violating the "double-click install, self-contained" promise

The review provides 8 prioritized recommendations to fix these issues, including implementing capability parity requirements, adding MCP authentication tools, creating a surface-appropriate design wizard, and establishing single-source capability management to prevent future drift.

The key insight is that the mechanism currently optimizes for developer convenience rather than user value maximization, particularly harming the largest potential user segment (knowledge workers) who could benefit most from structured deliberation tools but receive the most limited access.