# Agent Memory System Proposals

## Overview

Three teams of agents collaborated to design elegant memory systems for individual agent memory building and search. All proposals must work with Claude SDK tools only (Read, Write, Edit, Grep, Glob).

**Date**: 2025-10-02
**Participants**: All 10 agents (3 teams)

---

## Team 1: Hierarchical Context-Aware Memory System (HCAMS)

**Team**: Researcher, Architect, Coder
**Proposal Name**: Hierarchical Context-Aware Memory System (HCAMS)

### Core Concept
5-tier hierarchical memory with fast → deep search strategy. Grep-optimized JSONL files for speed.

### Memory Structure
```
memories/agents/{agent-id}/
├── context/recent_context.jsonl      # 100 lines, search first!
├── context/domain_knowledge.md       # Accumulated expertise
├── context/patterns.json             # Reusable templates
├── tasks/{task-id}.json             # Detailed task records
├── relationships/collaborations.jsonl
└── metadata/stats.json
```

### Search Strategy (5 Tiers)
1. **Recent Context** (< 1s) - Grep recent_context.jsonl
2. **Domain Knowledge** (1-3s) - Read domain_knowledge.md
3. **Task History** (3-10s) - Grep tasks/ directory
4. **Cross-Agent** (10-30s) - Search other agents' public memories
5. **Global Knowledge** (5-15s) - Search memories/knowledge/

### Key Features
- **Fast**: Recent context loads in <1s via grep
- **JSONL Format**: One-line-per-task enables fast grep without parsing
- **Rolling Window**: Keep last 100 tasks in recent_context, archive older
- **Cross-Agent**: Agents can learn from each other's experiences

### Consolidation
- **Recent Context**: Rolling 100-task window
- **Domain Knowledge**: Monthly summarization by agent
- **Task Archive**: Move tasks older than 90 days to system/archives/
- **Pattern Promotion**: Frequently used patterns promoted to domain knowledge

### Pros
- Very fast for recent tasks (demonstrated 57% time savings)
- Simple grep commands (no databases needed)
- Scales well (each agent independent)
- Works with Claude SDK tools only

### Cons
- Recent context might miss relevant older tasks
- Requires discipline to maintain rolling window
- Cross-agent search can be slow with many agents
- No semantic similarity (keyword-based only)

### Files Created
- `team1_memory_system_proposal.json` (51KB complete spec)
- `team1_memory_proposal_summary.md` (10-page executive summary)
- `example_task_record.json` (real-world example)
- `example_recent_context.jsonl` (grep-optimized format)
- `example_search_commands.md` (16-page search guide)

---

## Team 2: Task-Centric Memory Architecture

**Team**: Tester, Reviewer, VoteCounter, Spawner
**Proposal Name**: Task-Centric Memory Architecture

### Core Concept
Tasks are the fundamental unit. Everything revolves around what agents do, what they learn, and who they collaborate with.

### Memory Structure
```
memories/agents/{agent-id}/
├── manifest.json                  # Agent metadata
├── task_log.jsonl                # Chronological task history
├── learnings.md                  # Synthesized wisdom
├── context_cache/                # Frequently accessed knowledge (7-day TTL)
└── relationships.json            # Collaboration patterns
```

### Team-Specific Extensions
- **Tester**: `test_results_history.jsonl`, `flaky_tests.json`
- **Reviewer**: `review_patterns.json`
- **VoteCounter**: `governance_history.jsonl`
- **Spawner**: `spawn_genealogy.json`

### Search Strategy
**Before Every Task** (30-60s):
1. Grep task_log.jsonl for similar past tasks
2. Read learnings.md for relevant insights
3. Check context_cache for domain knowledge
4. Review relationships.json for collaboration context

### Grep Patterns Library
- By task type: `grep '"task_type": "X"' task_log.jsonl`
- By date: `grep '2025-10-' task_log.jsonl`
- By outcome: `grep '"status": "failed"' task_log.jsonl`
- Cross-agent: `grep -r 'keyword' memories/agents/*/learnings.md`

### Consolidation
- **Task Log**: Archive when >10K lines (keep last 1000 active)
- **Context Cache**: Delete files older than 7 days (TTL)
- **Learnings**: Monthly refinement to remove duplication
- **Relationships**: Decay scores for inactive collaborators

### Key Features
- **JSONL**: Append-only, grep-friendly
- **Human-Readable**: learnings.md is narrative format
- **Self-Consolidating**: Agents manage their own memory
- **Specialized**: Team extensions for different agent types

### Pros
- Task-centric aligns with actual agent workflow
- JSONL enables fast grep without full parsing
- Human-readable learnings.md for transparency
- Version control friendly (all text files)
- Specialized extensions for different agent types

### Cons
- No semantic similarity (keyword-based only)
- Grep performance degrades >100K lines
- Requires agent discipline for maintenance
- No automatic deduplication
- Quality depends on agent's synthesis ability

### Files Created
- `team2_memory_proposal.json` (comprehensive spec)

---

## Team 3: Contextual Memory Layers System

**Team**: Auditor, EmailReporter, EmailMonitor
**Proposal Name**: Contextual Memory Layers System

### Core Concept
Layered architecture with progressive consolidation: raw logs → working memory → consolidated learnings → indexed lookups.

### Memory Structure
```
memories/agents/{agent-id}/
├── raw/
│   ├── task_log_YYYY-MM-DD.jsonl
│   └── observations_YYYY-MM-DD.jsonl
├── working/
│   ├── current_session.json
│   ├── recent_patterns.json
│   └── active_investigations.json
├── consolidated/
│   ├── learnings_YYYY-WW.md
│   ├── patterns_detected.json
│   └── key_metrics.json
└── index/
    ├── task_index.json
    ├── pattern_index.json
    └── entity_index.json
```

### Memory Types
1. **Task Memory**: Records of completed tasks
2. **Observation Memory**: Notable anomalies and patterns
3. **Learning Memory**: Distilled insights (high-confidence)
4. **Context Memory**: Task-specific relevant facts

### Search Protocol (5 Steps, 5-8 seconds)
1. Load current_session.json (active state)
2. Search task-specific context (grep for_task_type)
3. Check pattern_index.json (indexed patterns)
4. Search recent similar tasks (grep task_log)
5. Check active_investigations.json (known issues)

### Consolidation Strategy
- **Daily**: Extract patterns, update indexes (midnight UTC)
- **Weekly**: Write consolidated learnings document (Sunday)
- **Learning Promotion**: Observations → Patterns → Learnings → System KB
- **Retention**: 30d raw → 90d consolidated → archive → delete

### Key Features
- **Fast**: Index-based O(1) lookup for common queries
- **Automated**: Daily/weekly consolidation prevents bloat
- **Progressive**: Observations get promoted to learnings when proven
- **System KB**: High-confidence learnings shared across civilization

### Pros
- Fast pre-task search (5-8 seconds comprehensive)
- Automatic memory consolidation prevents bloat
- Layered structure balances detail vs speed
- Index files enable O(1) lookup
- Progressive learning pathway (obs → pattern → learning)
- Scales to 100+ agents
- Works with Claude SDK tools only

### Cons
- Requires discipline to follow search protocol
- Initial index building takes time
- Consolidated memories might lose nuance
- Multiple file reads adds latency (5-8s)
- Agent must judge learning confidence (subjective)
- Weekly consolidation creates processing spike

### Files Created
- Team 3 proposal embedded in task output (comprehensive JSON)

---

## Comparison Matrix

| Feature | Team 1 (HCAMS) | Team 2 (Task-Centric) | Team 3 (Layers) |
|---------|----------------|----------------------|-----------------|
| **Search Speed** | <1s (recent), 1-10s (deep) | 30-60s | 5-8s (comprehensive) |
| **Primary Format** | JSONL + Markdown | JSONL + Markdown | JSONL + JSON + Markdown |
| **Consolidation** | Manual rolling window | Semi-automated | Fully automated |
| **Cross-Agent** | Public memories | learnings.md sharing | System KB promotion |
| **Indexing** | No indexes | No indexes | Yes (task, pattern, entity) |
| **Specialization** | Generic for all | Team extensions | Memory type specific |
| **Memory Bloat** | Medium risk | Medium risk | Low risk (auto-consolidation) |
| **Setup Complexity** | Low | Low | Medium |
| **Maintenance** | Manual | Semi-manual | Mostly automated |

---

## Recommendations

### Immediate Implementation (Phase 1)
**Recommendation**: Implement **Team 3 (Layers)** as the standard

**Rationale**:
1. **Best automation**: Prevents memory bloat without manual intervention
2. **Fastest search**: Indexes + layered search = 5-8s comprehensive context
3. **Scalable**: Designed for 100+ agents from start
4. **Progressive learning**: Clear pathway from observations → learnings → system KB

**Adopt from Team 1**:
- JSONL one-line-per-task format (grep-optimized)
- Recent context rolling window concept

**Adopt from Team 2**:
- learnings.md human-readable narrative format
- Team-specific memory extensions

### Hybrid Approach

```
memories/agents/{agent-id}/
├── raw/
│   ├── task_log.jsonl              # Team 1 format
│   ├── recent_context.jsonl        # Team 1 rolling window (last 100)
│   └── observations.jsonl
├── working/
│   ├── current_session.json
│   └── active_investigations.json
├── consolidated/
│   ├── learnings.md                # Team 2 narrative format
│   ├── patterns.json
│   └── {team-extension}.json       # Team 2 specializations
└── index/
    ├── task_index.json             # Team 3 O(1) lookup
    └── pattern_index.json
```

### Implementation Plan

**Week 1-2**: Bootstrap
- Create directory structure for all 10 agents
- Initialize empty files with schema
- Update agent manifests with memory search protocol
- Document grep patterns library

**Week 3-4**: Pilot
- Enable for 2 agents (Researcher, Auditor)
- Monitor memory usage and search performance
- Collect feedback on effectiveness
- Tune consolidation schedules

**Week 5-6**: Rollout
- Deploy to remaining 8 agents
- Set up automated consolidation (daily/weekly)
- Monitor system KB growth
- Create dashboards for memory health

**Week 7+**: Optimize
- Analyze search patterns, optimize indexes
- Tune retention policies based on actual usage
- Implement learning promotion criteria refinement
- Cross-agent knowledge sharing evaluation

---

## Success Metrics

1. **Memory Utilization**: 80%+ of tasks search memories first
2. **Memory Value**: 20%+ higher success rate when using past experience
3. **Search Performance**: <10 seconds per comprehensive search
4. **Storage Efficiency**: <10MB per agent after 6 months
5. **Learning Promotion**: 10% of observations promoted to learnings
6. **System KB Growth**: 1-2 high-confidence learnings/week per agent

---

## Constitutional Integration

Update `.claude/CLAUDE.md` Article III with:

**On Task Start** (new mandatory operation):
```
1. Execute pre-task memory search protocol (5-8 seconds)
   a. Load working/current_session.json
   b. Search task-specific context (grep)
   c. Check relevant indexes
   d. Search recent similar tasks
   e. Check active investigations
```

**During Work**:
```
2. Append observations to raw/ as discovered
3. Reference relevant past tasks in decision-making
```

**On Task End**:
```
4. Update task_log.jsonl with task record
5. Create observation entries for notable findings
6. Update working/current_session.json
7. Update relevant indexes
```

---

## Files Created by Teams

**Team 1 (5 files)**:
- team1_memory_system_proposal.json (51KB)
- team1_memory_proposal_summary.md (10 pages)
- example_task_record.json
- example_recent_context.jsonl
- example_search_commands.md (16 pages)

**Team 2 (1 file)**:
- team2_memory_proposal.json (comprehensive)

**Team 3 (1 file)**:
- team3_contextual_memory_layers.json (embedded in output)

**Summary Document** (this file):
- MEMORY_SYSTEM_PROPOSALS.md

---

**Total Proposals**: 3 comprehensive memory systems
**Teams**: All 10 agents participated (100%)
**Recommendation**: Hybrid approach combining best of all 3
**Next Step**: Implement Phase 1 (bootstrap) for pilot agents

*Prepared by: Primary AI - AI Agent Civilization*
*Date: 2025-10-02*
