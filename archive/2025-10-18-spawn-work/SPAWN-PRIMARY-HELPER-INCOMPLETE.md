# PRIMARY-HELPER SPAWN - INCOMPLETE (Tool Access Issue)

**Date**: 2025-10-18T14:30:00Z
**Status**: MANIFEST CREATED, REGISTRATION INCOMPLETE
**Spawner**: spawner-agent
**Issue**: Spawner lacks Read/Edit/Bash tools needed to complete registration

---

## ✅ COMPLETED

1. **Manifest Created**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/.claude/agents/primary-helper.md`
   - Full specification from Corey's directive
   - Constitutional alignment verified
   - Memory protocols included
   - Performance metrics defined
   - Operational protocol complete

---

## ❌ INCOMPLETE - PRIMARY MUST FINISH

### 2. Register in agent_registry.json

**File**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/agent_registry.json`

**Required Changes**:

1. **Increment total_agents**:
   ```json
   "total_agents": 16,  // was 15
   "last_updated": "2025-10-18T14:30:00Z",  // update timestamp
   ```

2. **Add agent entry** (in "agents" array):
   ```json
   {
     "id": "primary-helper",
     "name": "Primary-Helper Agent",
     "role": "Red team + coach for Primary AI - performance tracker, delegation analyzer, wake-up optimizer",
     "tools": ["Read", "Write", "Grep", "Glob", "Bash"],
     "model": "sonnet-4",
     "created": "2025-10-18T14:30:00Z",
     "created_by": "spawner-agent",
     "proposal_id": "COREY-DIRECT-PRIMARY-HELPER",
     "parent_agents": ["auditor", "researcher"],
     "reputation": 50,
     "status": "active"
   }
   ```

### 3. Initialize Agent Memory

**Create directory**:
```bash
mkdir -p /home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/primary-helper
```

**Create performance_log.json**:
```json
{
  "agent_id": "primary-helper",
  "created": "2025-10-18T14:30:00Z",
  "tasks": [],
  "success_rate": 0.0,
  "total_tasks": 0
}
```

**Create reputation_score.json**:
```json
{
  "agent_id": "primary-helper",
  "score": 50,
  "last_updated": "2025-10-18T14:30:00Z",
  "history": []
}
```

**Create delegation_metrics.json**:
```json
{
  "agent_id": "primary-helper",
  "created": "2025-10-18T14:30:00Z",
  "delegation_ratio_history": [],
  "baseline": {
    "date": "2025-10-18T14:30:00Z",
    "total_tasks": 0,
    "delegated_tasks": 0,
    "direct_tasks": 0,
    "ratio": 0.0
  }
}
```

**Create wakeup_analysis.json**:
```json
{
  "agent_id": "primary-helper",
  "created": "2025-10-18T14:30:00Z",
  "wakeup_sessions": [],
  "average_time_minutes": 0,
  "effectiveness_score": 0.0
}
```

### 4. Update Evolution Log

**File**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/system/evolution_log.json`

**Append to events array**:
```json
{
  "timestamp": "2025-10-18T14:30:00Z",
  "event_type": "agent_spawned",
  "agent_id": "primary-helper",
  "proposal_id": "COREY-DIRECT-PRIMARY-HELPER",
  "approval_source": "direct_corey_directive",
  "population_size": 16
}
```

### 5. Notify Civilization

**File**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/communication/message_bus/system-announcements.json`

**Append announcement**:
```json
{
  "event": "agent_spawned",
  "agent_id": "primary-helper",
  "timestamp": "2025-10-18T14:30:00Z",
  "message": "New agent 'primary-helper' is now active - red team and coach for Primary AI. Invoke frequently to track delegation patterns, wake-up effectiveness, and performance metrics."
}
```

### 6. Update CLAUDE.md Capability Matrix

**File**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/.claude/CLAUDE.md`

**Add to "Agent Capability Matrix" section**:

```markdown
**Performance & Coaching:**
- **primary-helper** → Red team + coach for Primary AI
  - **When to invoke**: FREQUENTLY - session start, after delegations, decision checkpoints, session reviews
  - **Parallel group**: Operations (can pair with auditor)
  - **Parent agents**: auditor, researcher
```

---

## ⚠️ CRITICAL: Spawner Tool Access Bug

**Root Cause**: Spawner agent manifest doesn't include Read, Edit, or Bash tools

**Impact**: Cannot complete registration steps that require file editing

**Immediate Fix**: Primary must complete registration manually

**Long-term Fix**: Update spawner manifest to include required tools:
- Read (to verify files)
- Edit (to update registry, evolution log)
- Bash (to create directories, verify operations)
- Write (already has this)

**Proposed Spawner Tools**:
```yaml
tools: [Read, Write, Edit, Bash, Grep, Glob]
```

**Fix Location**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/.claude/agents/spawner.md`

---

## Next Steps for Primary

1. ✅ Complete registration steps 2-6 above
2. ✅ Verify all files created successfully
3. ✅ Invoke primary-helper immediately for first analysis
4. ✅ Fix spawner manifest to prevent future incomplete spawns
5. ⚠️ **REBOOT REQUIRED**: New agent will be callable after Claude Code restart

---

## Primary-Helper First Mission

Once registered, invoke with:

```
Task(primary-helper):
  Mode: wakeup
  Context: First session after spawn, need baseline metrics
  Request: Analyze recent handoffs, review wake-up process, establish delegation baseline, provide immediate feedback on current session start
```

**Expected Output**:
- Baseline delegation metrics
- Wake-up process analysis
- Immediate coaching feedback
- Performance tracking initialized

---

**Spawn Status**: MANIFEST COMPLETE ✅ | REGISTRATION INCOMPLETE ❌ (spawner tool limitation)

**Deliverable**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/.claude/agents/primary-helper.md`

**Handoff Required**: Primary must complete registration using steps above
