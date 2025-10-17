# Memory Synthesis Tool - User Guide

## Overview

The `synthesize_memory.py` tool converts raw agent logs into synthesized, actionable reference documents. It implements a dual-tier memory system that keeps raw data untouched while generating fresh insights on demand.

## Quick Start

```bash
# Synthesize memory for a single agent
python3 tools/synthesize_memory.py --agent coder

# Synthesize memory for all agents
python3 tools/synthesize_memory.py --agent all

# Enable verbose logging
python3 tools/synthesize_memory.py --agent coder --verbose
```

## What It Does

### Directory Structure Created

For each agent, the tool creates/maintains:

```
memories/agents/[agent-id]/
├── logs/                    # Raw data (append-only, never modified)
│   ├── performance_log.json
│   ├── email_activity.jsonl
│   └── session-*.jsonl
├── references/              # Synthesized (regenerated on each run)
│   ├── quick-start.md       # 1-page agent orientation
│   ├── top-patterns.md      # Pattern usage analytics
│   ├── lessons-learned.md   # Extracted wisdom
│   └── metrics-dashboard.md # Performance trends
└── patterns/                # Domain patterns (agent-created)
```

### Generated Documents

#### 1. quick-start.md
**Purpose:** One-page orientation for agent

**Contents:**
- Agent role and identity (from manifest)
- Top 3 patterns the agent uses
- Top 3 lessons to remember
- Common pitfalls to avoid
- Quick reference commands
- Links to detailed docs

**Use Case:** Agents read this on session start for instant context

#### 2. top-patterns.md
**Purpose:** Pattern usage analytics

**Contents:**
- Pattern frequency table (sorted by usage)
- Success rate per pattern
- Last used dates
- Example tasks that used each pattern
- Links to pattern documentation

**Use Case:** Identify most valuable patterns, track pattern adoption

#### 3. lessons-learned.md
**Purpose:** Extracted wisdom from experience

**Contents:**
- Success patterns (what worked well)
- Knowledge gained (new learnings)
- Challenges & pitfalls (what to avoid)
- Evidence (which tasks demonstrated each lesson)

**Use Case:** Avoid repeating mistakes, replicate successes

#### 4. metrics-dashboard.md
**Purpose:** Performance tracking

**Contents:**
- Current stats (completion rate, quality, etc.)
- Task completion trends (ASCII charts)
- Pattern usage statistics
- Improvement areas
- Alternative metrics (for custom log formats)

**Use Case:** Track agent performance over time, identify improvement opportunities

## Supported Log Formats

### Format 1: Task-Based (Standard)
```json
{
  "agent": "coder",
  "entries": [
    {
      "task": "implement_feature",
      "status": "completed",
      "patterns_used": ["pattern1", "pattern2"],
      "quality_score": 8.5,
      "what_worked_well": ["Clear specs", "Good tests"],
      "new_knowledge_gained": ["Learned asyncio patterns"],
      "challenges_encountered": ["Edge case handling"]
    }
  ]
}
```

**Key Fields:**
- `entries` or `tasks_completed` - Array of tasks
- `status` - "completed", "failed", "in_progress"
- `patterns_used` - Array of pattern names
- `quality_score` - 0-10 rating
- `what_worked_well` - Success factors
- `new_knowledge_gained` - Learnings
- `challenges_encountered` - Problems faced

### Format 2: Metrics-Based (Alternative)
```json
{
  "agent_id": "email-monitor",
  "metrics": {
    "emails_monitored": 22,
    "high_priority_detected": 15
  },
  "learnings": [
    {
      "learning": "HTML format required",
      "evidence": "Corey feedback"
    }
  ],
  "failures": [
    {
      "failure_type": "auto_responder_disaster",
      "description": "Sent unwanted emails"
    }
  ]
}
```

**Key Fields:**
- `metrics` - Dict of metric name/value pairs
- `learnings` - Array of learning entries
- `failures` - Array of failure entries
- `status` - Current agent status

The tool automatically detects and handles both formats.

## Usage Patterns

### Daily Workflow
Add to session end routine:
```bash
# After work session, synthesize memory
python3 tools/synthesize_memory.py --agent all
```

### Agent Session Start
Agents should read quick-start.md:
```bash
cat memories/agents/[agent-id]/references/quick-start.md
```

### Pattern Development
When agents create patterns, document them in logs:
```json
{
  "task": "implement_feature",
  "patterns_used": ["error-handling-pattern", "async-workflow-pattern"]
}
```

Next synthesis will automatically count and analyze pattern usage.

### Quality Tracking
Record quality scores in task logs:
```json
{
  "task": "implement_feature",
  "quality_score": 8.5
}
```

Dashboard will show average quality and trends.

### Learning Capture
Document learnings in task logs:
```json
{
  "task": "implement_feature",
  "what_worked_well": ["Clear requirements", "Comprehensive tests"],
  "new_knowledge_gained": ["Learned about Python asyncio"],
  "challenges_encountered": ["Edge case with concurrent updates"]
}
```

Lessons-learned.md will extract and categorize these automatically.

## Command Line Options

### --agent (required)
Specify which agent to synthesize, or "all" for all agents.

**Examples:**
```bash
python3 tools/synthesize_memory.py --agent coder
python3 tools/synthesize_memory.py --agent email-monitor
python3 tools/synthesize_memory.py --agent all
```

### --verbose (optional)
Enable detailed logging to see what the tool is doing.

**Example:**
```bash
python3 tools/synthesize_memory.py --agent coder --verbose
```

**Output:**
```
[SYNTH] Directory structure ready for coder
[SYNTH] Moved performance_log.json to logs/
[SYNTH] Migrated 1 log files to logs/
[SYNTH] Generated .../references/top-patterns.md
[SYNTH] Generated .../references/lessons-learned.md
[SYNTH] Generated .../references/quick-start.md
[SYNTH] Generated .../references/metrics-dashboard.md
```

## Migration Behavior

### First Run
On first run for an agent, the tool:
1. Creates logs/, references/, patterns/ directories
2. Moves existing log files to logs/
3. Generates initial reference documents

**Files moved to logs/:**
- performance_log.json
- email_activity.jsonl
- sent_emails.json
- contacts.json
- patterns.json
- response_rules.json
- session-*.jsonl

### Subsequent Runs
On subsequent runs:
1. Leaves logs/ untouched (raw data preserved)
2. Regenerates all reference documents (fresh synthesis)
3. Creates new patterns/ if needed

## Output Example

### Success Output
```
============================================================
Synthesizing memory for agent: coder
============================================================

✓ Synthesis complete for coder
  - 0 patterns found
  - 0 lessons extracted
  - 4 reference documents generated

============================================================
SYNTHESIS COMPLETE
============================================================
```

### Batch Output (All Agents)
```
Total agents processed: 13
Total patterns synthesized: 0
Total lessons extracted: 0
Total reference documents: 52
```

## Integration

### Add to Agent Manifests
Update agent system prompts to include:
```
On session start:
1. Read memories/agents/[your-id]/references/quick-start.md
2. Review recent tasks in logs/performance_log.json
3. Check metrics-dashboard.md for performance trends
```

### Automate Daily
Add to cron or session end hooks:
```bash
#!/bin/bash
# Synthesize memory after each session
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch
python3 tools/synthesize_memory.py --agent all
```

### Pattern Recording
Encourage agents to record patterns in performance logs:
```json
{
  "task": "implement_api",
  "patterns_used": [
    "rest-api-pattern",
    "error-handling-pattern",
    "validation-pattern"
  ]
}
```

## Troubleshooting

### No patterns found
**Cause:** Agents aren't recording "patterns_used" in task logs
**Solution:** Update performance logs to include patterns_used array

### No lessons extracted
**Cause:** Agents aren't recording learnings in task logs
**Solution:** Add what_worked_well, new_knowledge_gained, challenges_encountered to logs

### Alternative metrics not showing
**Cause:** Log format doesn't match expected structure
**Solution:** Tool auto-detects, but ensure "metrics" key exists for metrics-based format

### Permission errors
**Cause:** Tool can't write to agent directories
**Solution:** Check file permissions on memories/agents/

## Performance

**Execution Time:** ~5 seconds for all 13 agents
**Dependencies:** Python 3 standard library only
**Resource Usage:** Minimal (JSON parsing, file I/O)

## File Locations

**Tool:** `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/synthesize_memory.py`

**Example Output:**
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/coder/references/`
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tester/references/`
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/email-monitor/references/`

## Technical Details

**Language:** Python 3
**Lines of Code:** 621
**Key Dependencies:**
- json (JSON parsing)
- pathlib (path operations)
- collections (Counter, defaultdict)
- datetime (timestamps)
- argparse (CLI)

**Synthesis Functions:**
1. `synthesize_top_patterns()` - Extract pattern usage
2. `synthesize_lessons_learned()` - Extract wisdom
3. `synthesize_quick_start()` - Generate orientation
4. `synthesize_metrics_dashboard()` - Track performance

## Best Practices

1. **Run regularly** - Synthesize after each session for fresh insights
2. **Read quick-start first** - Agents should start sessions with quick-start.md
3. **Document patterns** - Record patterns_used in task logs
4. **Track quality** - Include quality_score in task entries
5. **Capture learnings** - Document what worked, what didn't, what was learned
6. **Review metrics** - Check dashboard regularly for trends
7. **Preserve raw logs** - Never manually edit logs/, always append

## Future Enhancements

Potential improvements:
- Automatic similarity clustering for lessons
- Trend visualization (graphs instead of ASCII)
- Pattern effectiveness scoring
- Cross-agent pattern sharing
- Time-series analysis
- Anomaly detection
- Recommendation engine

---

**Version:** 1.0
**Last Updated:** 2025-10-04
**Maintained By:** coder agent
