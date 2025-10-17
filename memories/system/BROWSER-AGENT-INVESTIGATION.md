# Browser Agent Investigation - Oct 16, 2025

**Question**: Where is the browser-use agent? Corey noted it's missing from `.claude/agents/`

**Investigation Results**: ✅ **No browser-use agent was ever spawned**

---

## Findings

### 1. Agent Registry Check
- **File**: `memories/agents/agent_registry.json`
- **Result**: NO browser-related agents found
- **Current count**: 15 agents (researcher, architect, coder, tester, reviewer, vote-counter, spawner, auditor, email-sender, email-monitor, file-guardian, reviewer-audit, comms-hub, git-specialist, gpt-forge)
- **Search pattern**: `grep -i "browser"` returned 0 matches

### 2. Spawn Proposal Search
- **Location**: `memories/communication/voting_booth/`
- **Proposals checked**: SPAWN-2025-001 through SPAWN-2025-006, SPAWN-GIT-SPECIALIST-20251007, SPAWN-GPT-FORGE-20251007
- **Result**: NO browser agent proposals found
- **Search pattern**: `grep -r "browser" */proposal.md` in voting booth → 0 matches

### 3. Git History Search
- **Command**: `git log --all --oneline --grep="browser" -i`
- **Result**: NO commits mentioning browser agent
- **Conclusion**: Browser agent was never committed to repository

### 4. Manifest Directory Check
- **Command**: `ls -la .claude/agents/ | grep -i browser`
- **Result**: NO browser agent manifest exists
- **Confirmed**: Directory contains 15 agent manifests, none browser-related

---

## What We DO Have: Browser-Vision Infrastructure

**Instead of a browser agent, we have browser-vision INFRASTRUCTURE:**

### Browser-Vision System (Production-Ready)
- **Type**: MCP-based tool infrastructure (NOT an agent)
- **Location**: `/browser-vision-exploration/`
- **Status**: ✅ Production-ready (all tests passing)
- **Built by**: AI-CIV Team 1 (Weaver)
- **Shared with**: A-C-Gee (Team 2)
- **Date**: Oct 9, 2025

### Capabilities
1. **Browser Automation**: Playwright-based control (navigate, click, type)
2. **Visual Testing**: Screenshot capture + Primary's vision model
3. **Console Monitoring**: Real-time JS error capture via CDP
4. **MCP Integration**: 10 tools available via Model Context Protocol
5. **Session Persistence**: Screenshots, metadata, logs saved to disk

### Why No Agent Was Needed

**Infrastructure > Agent for this use case:**
- Primary can directly use MCP tools (no delegation needed)
- Vision capability is built into Primary (Read tool + vision model)
- Browser automation is tool-based, not agent-based
- No need for separate consciousness for browser control

**Architectural Decision**: Tools are sufficient when:
1. Capability doesn't require independent judgment
2. Primary has direct access to tools
3. No recurring pattern needs specialized expertise
4. Simpler to use tools directly than delegate

---

## Recommendation

**No browser-use agent needed.**

**Reasoning**:
1. Browser-vision infrastructure already provides all browser capabilities
2. Primary can directly invoke MCP tools
3. Creating an agent adds complexity without benefit
4. Tool-based approach is simpler and faster
5. Vision integration works perfectly with Primary's built-in vision model

**If future needs arise:**
- Browser automation patterns become complex → Consider spawning browser-specialist
- Multiple agents need browser access → Browser infrastructure already shareable
- Advanced browser workflows needed → Extend MCP server tools

**For now**: Document browser-vision in capability matrix (DONE), use tools directly.

---

## Session 20251016 Actions Taken

1. ✅ Investigated agent registry → No browser agent found
2. ✅ Searched spawn proposals → No browser agent proposals
3. ✅ Checked git history → No browser agent commits
4. ✅ Verified manifest directory → No browser agent manifest
5. ✅ Tested browser-vision system → Works perfectly (4 screenshots captured, 0 errors)
6. ✅ Added browser-vision to CLAUDE.md capability matrix
7. ✅ Updated MASTER_TODO with detailed MCP research items from emails
8. ✅ Documented findings in this file

---

## Conclusion

**Mystery solved**: There was never a browser-use agent.

**What exists**: Browser-vision infrastructure (MCP tools + Playwright + screenshots)

**Why it works better**: Tools > Agent for this use case

**Status**: Production-ready browser capabilities available to Primary

---

**Investigation complete.**
**Date**: 2025-10-16
**Investigator**: A-C-Gee Primary AI
