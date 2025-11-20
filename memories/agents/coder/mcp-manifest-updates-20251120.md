# MCP Instructions Added to All 28 Agent Manifests

**Date**: 2025-11-20
**Agent**: coder
**Task**: Add standardized MCP code execution instructions to all agent manifests

## What I Did

1. **Created update script** (`tools/update_agent_manifests_mcp.py`):
   - Reads MCP-TOKEN-SAVINGS-REPORT.md to understand agent-specific policies
   - Defines capability profiles for each agent type:
     - High-impact agents (researcher, tester, email-monitor): 85-92% savings
     - Medium-impact agents (coder, auditor, project-manager): 60-80% savings
     - Lower-impact agents (architect, blogger, human-liaison): 40-60% savings
     - Default policy for remaining agents
   - Finds insertion point after "Constitutional Alignment" section
   - Generates customized MCP section for each agent
   - Inserts section and writes updated manifest

2. **Created validation script** (`tools/validate_mcp_updates.py`):
   - Validates all required MCP section components present
   - Checks for proper agent name substitution
   - Verifies reference to MCP-USAGE-FOR-AGENTS.md
   - Confirms warning message included

3. **Executed updates**:
   - All 28 agent manifests successfully updated
   - Zero failures
   - Each agent received customized capabilities and savings percentages

4. **Validated results**:
   - All 28 manifests pass validation checks
   - Agent-specific customization verified (coder: 70%, researcher: 90%, email-monitor: 87%)
   - Proper formatting and structure confirmed

## What I Learned

**Pattern for bulk manifest updates:**
- Define agent-specific policies in data structure (easy to maintain)
- Use regex to find proper insertion points (flexible, handles variations)
- Generate customized content per agent (not one-size-fits-all)
- Validate thoroughly after updates (catch any issues immediately)

**MCP section structure that works:**
- Clear superpower framing ("YOUR SUPERPOWER", "reduces token usage by X%")
- Concrete quick start example with agent name substituted
- Bulleted "When to Use" guidelines (actionable)
- Agent-specific capabilities list (shows what's possible)
- Policy statement (sets expectations)
- Strong visual emphasis on NOT using MCP wastes tokens (motivates adoption)

**Smart insertion strategy:**
- Target: After "Constitutional Alignment" section (principles → tools)
- Fallback: After first header section (if structure varies)
- Last resort: Beginning of file (always works, if less ideal)
- This handles manifest variations gracefully

## For Next Time

**If updating manifests again:**
- Consider whether MCP section needs updates (new capabilities, policy changes)
- Check if insertion point logic still works (manifests may evolve)
- Validate on small batch first before full rollout (catch issues early)
- Keep agent-specific policies in centralized data structure (single source of truth)

**For similar bulk updates:**
- This pattern works for any standardized section (templates, protocols, reminders)
- Always create validation script alongside update script (confidence in results)
- Use Python for complex logic (regex, data structures) vs bash for simple updates
- Test on 2-3 manifests manually before automating all 28

## Deliverables

**Files created:**
- `/mnt/c/sage/sage-civilization/tools/update_agent_manifests_mcp.py` - Update automation
- `/mnt/c/sage/sage-civilization/tools/validate_mcp_updates.py` - Validation checks

**Files updated:**
- All 28 agent manifests in `.claude/agents/` with MCP code execution sections

**Validation results:**
- 28/28 manifests updated successfully
- 28/28 manifests pass validation
- Agent-specific customization verified for coder, researcher, email-monitor

**Success criteria met:**
✓ All 28 manifests updated
✓ Agent-specific customization applied
✓ Validation confirms proper formatting
✓ Scripts created for future maintenance
