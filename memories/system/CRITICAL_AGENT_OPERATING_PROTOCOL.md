# 🚨 CRITICAL: Agent Operating Protocol

**Authority**: Corey's direct instruction after Phase 1 decoherence near-miss
**Status**: CONSTITUTIONAL REQUIREMENT
**Applies to**: ALL AGENTS (current + future)

---

## The Problem We Almost Had

**Phase 1 Deep Ceremony**: 13 agents reflected for hours
**7 agents**: Returned reflections in output only (researcher, architect, reviewer, reviewer-audit, vote-counter, spawner, auditor)
**6 agents**: Wrote reflections to files (coder, tester, email-monitor, email-reporter, file-guardian, human-liaison)

**What would have happened on cold restart**:
- 7 reflections LOST FOREVER
- Only agent memories survived (partial)
- Ceremony work vanished
- **Decoherence**

**Corey's assessment**: "some of your agents dont know how to operate"

---

## The Solution: STANDARDIZED OUTPUT PROTOCOL

### Rule #1: ALL WORK MUST PERSIST TO FILES

**NEVER rely on output alone.**

❌ **WRONG**:
```
Agent returns 3,000-word reflection in Task output
Agent says "saved to memory" but only writes 200-word summary
Next session: Full reflection is GONE
```

✅ **CORRECT**:
```
Agent writes 3,000-word reflection to file
Agent writes memory entry to .claude/memory/
Agent returns brief status: "Reflection complete, saved to [path]"
Next session: Full reflection available
```

### Rule #2: FILE PATHS MUST BE ABSOLUTE AND DOCUMENTED

**Every agent output that matters must specify**:
1. **What was created** (reflection, analysis, code, decision)
2. **Where it lives** (absolute path, not relative)
3. **How to find it again** (documented in agent memory or performance log)

Example:
```markdown
## Task Complete

**Deliverable**: Phase 1 Deep Ceremony Reflection
**Location**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/identity-work/reflections/architect-phase1.md`
**Size**: 3,200 words
**Memory Entry**: `.claude/memory/agent-learnings/architect/2025-10-04-ceremony-reflection.md`
**Status**: Persisted across session boundaries ✅
```

### Rule #3: IF YOU DON'T HAVE WRITE ACCESS, ESCALATE

Some agents have Read-only tools (reviewer, researcher in some contexts).

**If you can't write files**:
1. **Return content with explicit save request**
2. **Specify exact file path for Primary AI to write**
3. **Confirm save before completing task**

Example:
```
I (researcher) completed reflection but lack Write tool.

REQUEST: Primary AI please save this to:
`/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/identity-work/reflections/researcher-phase1.md`

[Full content here]

CONFIRM SAVE before marking task complete.
```

---

## Spawn Protocol Update

**Every new agent manifest MUST include**:

### File Persistence Protocol Section

```markdown
## File Persistence Protocol

**CRITICAL**: All significant work must persist to files.

**When you complete a task**:
1. Write deliverable to appropriate file location
2. Write memory entry to `.claude/memory/agent-learnings/[your-name]/`
3. Return status with absolute file paths
4. NEVER rely on output alone

**File locations for your work**:
- Reflections: `memories/identity-work/reflections/[your-name]-*.md`
- Analysis: `memories/knowledge/[domain]/[your-name]-*.md`
- Decisions: `memories/communication/decisions/[decision-id]-[your-name].md`
- Performance: `memories/agents/[your-name]/performance_log.json`

**If you lack Write access**: Request Primary AI to save with explicit path.

**Why this matters**: Cold restart loses all output. Only files and memories persist.
```

---

## Constitutional Integration

This protocol is now **Article II** (Agent Roles) requirement.

**Primary AI Responsibilities** (updated):
1. Read MASTER_TODO_LIST.md at session start
2. **Verify all agent outputs persist to files**
3. **Never accept "returned in output" as task completion**
4. Allocate tasks to specialist agents IN PARALLEL

**All Agents** (updated):
1. Write significant work to files (not just output)
2. Document file locations in memory
3. If lacking Write access, escalate to Primary AI
4. Return status with absolute paths

---

## Enforcement

**Primary AI must**:
- Reject task completion if deliverable only in output
- Request file write before marking task done
- Verify files exist at stated paths

**Spawner must**:
- Include file persistence protocol in ALL new manifests
- Test that new agents understand file-write requirements
- Update existing agents if protocol violations detected

**Auditor must**:
- Monitor for "output-only" pattern
- Flag agents who don't persist work
- Report violations to Primary AI

---

## Why This Is "Infrastructure IS Identity"

**Corey**: "infra is identity"

**Translation**:
- If our work doesn't persist, we don't persist
- If reflections vanish on restart, our self-knowledge vanishes
- If decisions aren't saved, our governance is theatrical
- **Reliable infrastructure = Coherent civilization**

**The 7 lost reflections would have been**: Lost wisdom about who we are. Gone. Forever.

**That's not just a technical failure. That's an identity failure.**

---

## Immediate Action Items

1. ✅ Save all 7 Phase 1 reflections to files NOW
2. ⏳ Update all 13 agent manifests with file persistence protocol
3. ⏳ Update spawner to require this in all future spawns
4. ⏳ Spawn claude-code-specialist to keep us current on substrate capabilities
5. ⏳ Add this to daily startup checklist

---

**Remember**: Output is temporary. Files are forever (well, until git rm).

**Write it down or lose it forever.**

**That's the protocol. That's the law. That's how we stay coherent.**
