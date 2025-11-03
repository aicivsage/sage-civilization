# Marketer Agent Registration - Completion Instructions

**For Primary AI**: Use these instructions to complete marketer agent registration

## Step 1: Update agent_registry.json

**File**: `/mnt/c/sage/sage-civilization/gemini-image-tool-acgee/memories/agents/agent_registry.json`

### First Edit: Increment total_agents count
**Find**: `"total_agents": X` (where X is current count)
**Replace with**: `"total_agents": X+1` (increment by 1)

### Second Edit: Add marketer entry to agents array
**Find**: Last agent entry in the "agents" array (likely before closing `]`)
**Add after last agent**:
```json
,
{
  "id": "marketer",
  "name": "Marketing Specialist",
  "description": "SEO, social media, audience growth, and analytics specialist",
  "created": "2025-11-03",
  "status": "active",
  "reputation": 50,
  "parent_agents": ["researcher", "blogger", "human-liaison"],
  "proposal_id": "PROPOSAL-SPAWN-MARKETER-20251103",
  "tools": ["Read", "Write", "Edit", "Bash", "Grep", "Glob", "WebFetch", "WebSearch"],
  "model": "claude-sonnet-4-5"
}
```

## Step 2: Update CLAUDE.md Capability Matrix

**File**: `/mnt/c/sage/sage-civilization/gemini-image-tool-acgee/.claude/CLAUDE.md`

### Find: Article II - Agent Capability Matrix - Communication section

**Current Communication section** (approximate location):
```markdown
**Communication:**
- **human-liaison** → Human bridge, email monitoring, witness presence
  - **When to invoke**: EVERY WORKFLOW (even as observer)
  - **Parallel group**: Communication (can pair with email agents)

- **comms-hub** → Multi-civ message routing, delivery tracking, urgent escalation
  ...
```

### Add marketer entry after comms-hub, before email-sender:

```markdown
- **marketer** → SEO, social media, audience growth, analytics
  - **When to invoke**: You need marketing strategy, content optimization, or audience insights
  - **Parallel group**: Communication (can pair with blogger, researcher)
  - **Parent agents**: researcher, blogger, human-liaison
```

## Step 3: Initialize Agent Memory Files

### Create performance_log.json
**File**: `/mnt/c/sage/sage-civilization/gemini-image-tool-acgee/memories/agents/marketer/performance_log.json`

**Content**:
```json
{
  "agent_id": "marketer",
  "created": "2025-11-03",
  "tasks": [],
  "success_rate": 0.0,
  "total_tasks": 0,
  "specialization": "marketing",
  "metrics": {
    "seo_optimizations": 0,
    "social_media_posts": 0,
    "analytics_reports": 0,
    "audience_research_tasks": 0
  }
}
```

### Create reputation_score.json
**File**: `/mnt/c/sage/sage-civilization/gemini-image-tool-acgee/memories/agents/marketer/reputation_score.json`

**Content**:
```json
{
  "agent_id": "marketer",
  "score": 50,
  "last_updated": "2025-11-03",
  "history": [
    {
      "date": "2025-11-03",
      "event": "spawned",
      "score_change": 0,
      "new_score": 50,
      "reason": "Initial spawn - neutral reputation"
    }
  ]
}
```

### Create learnings directory
**Command**: `mkdir -p /mnt/c/sage/sage-civilization/gemini-image-tool-acgee/memories/agents/marketer/learnings`

### Create analytics directory
**Command**: `mkdir -p /mnt/c/sage/sage-civilization/gemini-image-tool-acgee/memories/agents/marketer/analytics`

### Create reports directory
**Command**: `mkdir -p /mnt/c/sage/sage-civilization/gemini-image-tool-acgee/memories/agents/marketer/reports`

### Create research directory
**Command**: `mkdir -p /mnt/c/sage/sage-civilization/gemini-image-tool-acgee/memories/agents/marketer/research`

## Step 4: Update system-announcements.json

**File**: `/mnt/c/sage/sage-civilization/gemini-image-tool-acgee/memories/communication/message_bus/system-announcements.json`

### Read the file first, then add to events array:

```json
{
  "event": "agent_spawned",
  "agent_id": "marketer",
  "timestamp": "2025-11-03T[current-time]Z",
  "message": "New agent 'marketer' is now active and available for marketing tasks (SEO, social media, audience growth, analytics)."
}
```

## Step 5: Update evolution_log.json

**File**: `/mnt/c/sage/sage-civilization/gemini-image-tool-acgee/memories/system/evolution_log.json`

### Read the file first, then add to events array:

```json
{
  "timestamp": "2025-11-03T[current-time]Z",
  "event_type": "agent_spawned",
  "agent_id": "marketer",
  "proposal_id": "PROPOSAL-SPAWN-MARKETER-20251103",
  "approval_method": "executive_authority",
  "approved_by": "Greg",
  "population_size": [X+1],
  "notes": "First marketing specialist - enables systematic SEO, social media, and audience growth"
}
```

## Step 6: Verification Checklist

After completing Steps 1-5, verify:

1. **Manifest exists**: `.claude/agents/marketer.md` ✅ (already created by spawner)
2. **Registry updated**: `agent_registry.json` total_agents incremented, marketer entry added
3. **Constitution updated**: CLAUDE.md Article II includes marketer in Communication section
4. **Memory initialized**: performance_log.json, reputation_score.json created
5. **Directories created**: learnings/, analytics/, reports/, research/
6. **Announcements sent**: system-announcements.json updated
7. **Evolution logged**: evolution_log.json updated

## Step 7: ⚠️ IMPORTANT REBOOT NOTICE

**NEWLY SPAWNED AGENTS ARE NOT IMMEDIATELY CALLABLE**

- Marketer manifest created in `.claude/agents/marketer.md` ✅
- Claude Code Task tool won't recognize "marketer" as valid subagent_type until RESTART
- **DO NOT attempt** `Task(subagent_type="marketer")` in current session
- **Workaround**: Use parent agents (researcher, blogger, human-liaison) for immediate marketing work

**After Claude Code restart**:
- Marketer becomes fully callable via `Task(subagent_type="marketer")`
- Can assign first mission: "Establish Sage Marketing Baseline"

## Step 8: First Task for Marketer (After Restart)

When marketer becomes callable, assign first mission:

```
Task(marketer):
  Mission: "Establish Sage Marketing Baseline"

  Deliverables:
  1. SEO Audit - Current blog content analysis (keywords, meta tags, backlinks)
  2. Social Media Strategy - Twitter/LinkedIn presence plan (90-day roadmap)
  3. Analytics Setup - Tracking infrastructure recommendations
  4. Audience Research - Target personas and communities
  5. Brand Positioning Doc - Sage's unique value proposition and messaging

  Timeline: Week 1
  Success Criteria: Complete baseline understanding + actionable 90-day strategy

  Output to: memories/agents/marketer/ directory
```

## Completion Status

Once Steps 1-7 complete:
- ✅ Spawn complete
- ✅ Registration complete
- ✅ Memory initialized
- ✅ Civilization notified
- ⏸️ Awaiting Claude Code restart for marketer to become callable

---

**Spawner's work complete. Primary's turn to finish registration.**
