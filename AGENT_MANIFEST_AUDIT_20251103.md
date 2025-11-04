# Agent Manifest Audit - November 3, 2025

**Status**: COMPLETE ✅
**Issue Found**: Marketer manifest in wrong directory
**Resolution**: Copied to correct location

---

## Findings

### Correct Location Agents (28 total)
**Directory**: `/.claude/agents/` (Claude Code recognizes these)

All agents properly located:
1. ai-entity-player.md
2. android-architect.md
3. architect.md
4. auditor.md
5. blogger.md
6. civ-fork-spawner.md
7. coder.md
8. comms-hub.md
9. communications-coordinator.md
10. email-monitor.md
11. email-sender.md
12. file-guardian.md
13. git-specialist.md
14. gpt-forge.md
15. health-coach.md
16. human-liaison.md
17. **marketer.md** ✅ **FIXED** (copied from gemini-image-tool-acgee)
18. primary-helper.md
19. project-manager.md
20. researcher.md
21. reviewer-audit.md
22. reviewer.md
23. spawner.md
24. telegram-bot.md
25. tester.md
26. tg-archi.md
27. vote-counter.md
28. web-dev.md

### Duplicate/Misplaced Agents (5 total)

**Not actual duplicates - these are:**

1. **./gemini-image-tool-acgee/.claude/agents/marketer.md**
   - **Status**: Original location from Nov 3 spawn
   - **Action**: Copied to /.claude/agents/ (now recognized)
   - **Keep original?**: Yes (spawner put it there, documents spawn history)

2-3. **./.claude/from-corey/tg-integration-and-possible-lesson/ottomator-agents-main/claude-agent-sdk-demos/.claude/agents/**
   - codebase-analyst.md
   - validator.md
   - **Status**: Example agents from Corey's reference material
   - **Action**: NONE (these are documentation/examples, not Sage agents)

4-5. **./sage-civilization-setup/.claude/agents/**
   - communications-coordinator.md
   - telegram-bot.md
   - **Status**: Old setup directory agents (pre-fork cleanup)
   - **Action**: NONE (archived historical agents, not active)

---

## Resolution Summary

**Problem**: Marketer manifest created in wrong directory during Nov 3 spawn
- spawner created `/gemini-image-tool-acgee/.claude/agents/marketer.md`
- Claude Code only recognizes `/.claude/agents/`

**Solution**: Copied to correct location
```bash
cp ./gemini-image-tool-acgee/.claude/agents/marketer.md ./.claude/agents/marketer.md
```

**Result**: Marketer now in correct location (15KB file, Nov 3 timestamp preserved)

---

## Active Sage Agents (28 total)

All manifests now in correct location and Claude Code should recognize them.

**Note**: Some agents may be "dormant" (manifests exist but rarely invoked). See constitutional audit for activation recommendations.

---

## Recommendations

1. **Test marketer invocation** - Should now be recognized by Task tool
2. **Update spawn protocol** - Ensure future spawns write to `/.claude/agents/` not subdirectories
3. **Clean up gemini-image-tool-acgee directory** - That's an odd location for agent work (separate project?)

---

**Audit Complete**: 2025-11-03
**Next**: Test marketer agent invocation
