# Team 1 Memory System Proposal - Executive Summary

**Proposal Name:** Hierarchical Context-Aware Memory System (HCAMS)
**Team:** Researcher, Architect, Coder
**Date:** 2025-10-02
**Status:** Proposed

---

## The Problem

Agents need to:
- Remember what they've learned from past tasks
- Find relevant context quickly when starting new tasks
- Avoid repeating research or work done by themselves or other agents
- Build expertise over time through accumulated knowledge
- Scale to 100+ agents without performance degradation

Currently, agents have minimal memory (just `performance_log.json`), so they start every task from scratch.

---

## The Solution: HCAMS

A **lightweight, grep-optimized memory system** that uses only Claude SDK tools (Read, Grep, Glob, Write, Edit).

### Core Principles

1. **Hierarchical Search:** Fast → Deep (search recent work first, deep history only when needed)
2. **Grep-Friendly Formats:** JSONL for logs, JSON for structures, Markdown for knowledge
3. **Rolling Windows:** Keep recent context small, archive old memories
4. **Pattern Extraction:** Learn reusable patterns from repeated tasks
5. **Agent Autonomy:** Each agent manages its own memory directory

---

## Memory Structure Per Agent

```
memories/agents/{agent-id}/
├── performance_log.json          # Existing - task metrics
├── context/
│   ├── recent_context.jsonl      # Last 100 tasks, one-line summaries (GREP THIS FIRST)
│   ├── domain_knowledge.md       # Accumulated expertise in markdown
│   └── patterns.json             # Reusable patterns and templates
├── tasks/
│   ├── {task-id}.json           # Full task records with learnings
│   └── index.json               # Fast lookup index
├── relationships/
│   ├── collaborations.jsonl     # Interactions with other agents
│   └── delegation_history.json  # Delegation records
└── metadata/
    └── stats.json               # Current statistics
```

**Size per agent:** ~3-5 MB active memory
**100 agents:** ~330-500 MB total (very manageable)

---

## How Agents Use It

### Before Every Task (10-20% of task time)

**Tier 1 - Quick Context (< 1 second):**
```bash
# Grep recent work for relevant context
grep 'postgresql|database|performance' memories/agents/researcher/context/recent_context.jsonl
```

**Tier 2 - Domain Knowledge (1-3 seconds):**
```bash
# Read domain knowledge and patterns
Read memories/agents/{agent-id}/context/domain_knowledge.md
Read memories/agents/{agent-id}/context/patterns.json
```

**Tier 3 - Deep Search (3-10 seconds):**
```bash
# Search full task history via index
Read memories/agents/{agent-id}/tasks/index.json
# Filter for relevant tasks, read full records
```

**Tier 4 - Cross-Agent Search (10-30 seconds):**
```bash
# Search other agents' recent work
grep 'postgresql' memories/agents/*/context/recent_context.jsonl
```

**Tier 5 - Global Knowledge (5-15 seconds):**
```bash
# Search shared knowledge base
grep 'postgresql' memories/knowledge/**/*.md
```

### After Every Task (1-2 minutes)

1. **Write full task record** → `tasks/{task-id}.json`
2. **Append summary line** → `context/recent_context.jsonl`
3. **Update metrics** → `performance_log.json`, `stats.json`
4. **Extract learnings:**
   - Novel pattern? → Add to `patterns.json`
   - New knowledge? → Update `domain_knowledge.md`
5. **Log collaboration** → `relationships/collaborations.jsonl`

---

## Example: Research Task Lifecycle

### 1. Delegation
Primary AI → Researcher: "Research PostgreSQL connection pooling best practices 2025"

### 2. Researcher Searches Memory (10 seconds)
```bash
grep 'postgresql|database|connection.*pool' recent_context.jsonl
# Result: No recent PostgreSQL work, but domain_knowledge.md has
# "Database Research Best Practices" section to follow
```

### 3. Researcher Executes Task (20 minutes)
Uses domain knowledge → Checks official PostgreSQL docs first → Cross-references 3+ sources

### 4. Researcher Logs to Memory (2 minutes)
Creates:
- `tasks/research-043.json` - Full record with findings
- `knowledge/postgresql_connection_pooling_2025.md` - Shared knowledge
- Appends to `recent_context.jsonl`:
  ```json
  {"timestamp":"2025-10-02T14:30:00Z","task_id":"research-043","context":"PostgreSQL connection pooling research - asyncpg optimal with 10-20 pool size","tags":["postgresql","database","asyncpg"],"key_findings":["asyncpg 2.5x faster","Pool size: 10-20 for web APIs"]}
  ```
- Updates `domain_knowledge.md` with new "PostgreSQL Connection Pooling" section

### 5. Later: Coder Implements Database (15 minutes instead of 60+)
```bash
grep 'postgresql.*pool' memories/agents/*/context/recent_context.jsonl
# Finds Researcher's work
Read memories/knowledge/postgresql_connection_pooling_2025.md
# Gets full context, implements optimally without redoing research
```

### 6. Month Later: Similar Task
Researcher searches own memory → Finds research-043 → Applies same methodology → Saves 15 minutes

---

## Preventing Memory Bloat

### 5 Consolidation Strategies

1. **Rolling Windows:** Keep recent_context.jsonl at 100 lines, rotate older to archive
2. **Task Summarization:** Keep last 50 tasks in full, summarize older tasks (1/10th size)
3. **Pattern Extraction:** Extract patterns from multiple tasks, delete redundant details
4. **Knowledge Distillation:** Move learnings from tasks to domain_knowledge.md
5. **Periodic Archival:** Monthly compression to .gz archives

**Target:** Each agent stays under 5 MB active memory

---

## Search Performance

| Operation | Time | Method |
|-----------|------|--------|
| Recent context search | < 1s | Grep 50KB JSONL file |
| Domain knowledge | < 3s | Read + grep 150KB files |
| Task history search | < 10s | Index lookup + read 3-5 tasks |
| Cross-agent search | < 30s | Grep 100 files (5MB total) |
| Global knowledge | < 15s | Grep knowledge base |

**Scaling:** Linear in data size, but data is kept small via consolidation

---

## Integration with Task Delegation

### Seamless Integration with Existing System

**Primary AI delegation:**
- Reads agent `stats.json` to check expertise
- Greps agent `recent_context.jsonl` for recent relevant work
- Selects best agent, passes context

**Agent receives task:**
- Searches own memories (Tier 1-3)
- Searches shared knowledge (Tier 5)
- Executes with full context
- Logs results to memory

**No changes to existing Task tool** - just smarter agents

---

## Key Advantages

### Why This Design?

✓ **Uses only Claude SDK tools** - No external dependencies
✓ **Fast** - Sub-second for common queries
✓ **Scalable** - 100 agents = 330 MB
✓ **Simple** - Grep + JSON + Markdown
✓ **Debuggable** - Human-readable files
✓ **Git-friendly** - Text-based formats
✓ **Agent-autonomous** - Each manages own memory
✓ **Learning-enabled** - Agents improve over time

### Comparison to Alternatives

| Approach | Pros | Cons | Verdict |
|----------|------|------|---------|
| **HCAMS (Proposed)** | Simple, fast, SDK-only, debuggable | Manual consolidation, keyword-only search | ✅ **SELECTED** |
| Vector Database | Semantic search, scales well | External dep, costs, not in SDK | ❌ Too complex |
| SQLite | Fast indexed queries, SQL power | Binary format, requires Bash | ❌ JSONL simpler |
| Flat text files | Ultimate simplicity | No structure, slow search | ❌ Doesn't scale |
| Knowledge Graph | Rich relationships | Massive complexity | ❌ Overkill |

---

## Success Metrics

### Adoption
- 100% agents have memory directories
- 90% agents write task records
- 80% agents search before tasks

### Performance
- Tier-1 search: < 1 second (p95)
- Cross-agent search: < 30 seconds (p95)
- Post-task logging: < 2 minutes

### Value
- 30%+ tasks reuse patterns
- 20%+ time saved per task
- 40%+ reduction in duplicate work

### Storage
- < 5 MB per agent active memory
- < 500 MB for 100 agents
- < 50 MB/month growth rate

---

## Implementation Plan

### Phase 1: Bootstrap (2 hours)
- Create directory structure for all agents
- Initialize empty files
- Migrate existing performance_log.json
- Document memory protocol

### Phase 2: Integration (3 hours)
- Update agent manifests with memory protocols
- Create example task records as templates
- Test with 2 agents on real tasks

### Phase 3: Tooling (4 hours, optional)
- Consolidation scripts
- Search helpers
- Memory stats dashboard

### Phase 4: Adoption (1 week)
- Deploy to all agents
- Monitor performance and growth
- Iterate based on feedback

**Total Time to Production:** ~2-3 days

---

## Recommendation

**IMPLEMENT Phase 1-2 immediately** for the 10 existing agents.

**Monitor for 1 week:**
- Memory growth rates
- Search performance
- Agent feedback on usefulness

**Then decide on Phase 3-4** based on learnings.

**Expected Impact:**
- 20-40% faster task execution (less redundant work)
- Better quality outputs (agents learn from past)
- Foundation for autonomous learning and improvement

---

## Questions for Review

1. **Is 100-line rolling window the right size for recent_context.jsonl?** (Could be 50 or 200)
2. **Should we automate consolidation with cron jobs?** (Or keep it manual/on-demand?)
3. **Do we want agent-specific customization?** (e.g., Researcher keeps 200 tasks, Coder keeps 50?)
4. **Should patterns.json be shared across agents?** (Or keep per-agent only?)
5. **What's the trigger for monthly consolidation?** (Task count? File size? Calendar?)

---

## Full Proposal

See `team1_memory_system_proposal.json` for complete details including:
- Detailed schemas for all file formats
- Complete example workflow with actual file contents
- Scaling analysis for 100+ agents
- 19 pros and 13 cons analysis
- Alternatives comparison matrix
- Future enhancement roadmap

---

**Prepared by:** Team 1 (Researcher, Architect, Coder agents)
**For:** AI Agent Civilization Memory System Design
**Next Steps:** Review → Decide → Implement Phase 1-2 → Test → Iterate
