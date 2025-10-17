# Automated Startup Summary Generator

**Tool:** `tools/generate_startup_summary.py`
**Version:** 1.0
**Purpose:** Auto-generate narrative session startup summaries for AI agents

## Overview

This tool helps agents quickly orient themselves at the start of a session by:
1. Reading their last 3 performance log entries
2. Extracting relevant patterns from their experience
3. Identifying applicable knowledge base articles
4. Generating a coherent narrative summary tailored to the current task

## Features

- **Fast Performance**: Runs in <40ms average (well under 2s requirement)
- **Smart Keyword Extraction**: Removes stop words, identifies core concepts
- **Pattern Matching**: Finds relevant patterns from agent's patterns/ directory
- **Knowledge Base Search**: Identifies helpful ADRs and research articles
- **Graceful Degradation**: Works even if no prior history or patterns exist
- **Narrative Format**: Human-readable summary, not just data dump

## Installation

No installation required! The tool is standalone Python 3.8+ with no external dependencies.

```bash
# Make executable (already done)
chmod +x tools/generate_startup_summary.py

# Test it works
python3 tools/generate_startup_summary.py --agent coder --task "test task"
```

## Usage

### Basic Usage

```bash
python3 tools/generate_startup_summary.py \
  --agent <agent-id> \
  --task "<task description>"
```

### Output to File

```bash
python3 tools/generate_startup_summary.py \
  --agent researcher \
  --task "research GraphQL best practices" \
  --output /tmp/startup_summary.md
```

### Specify Custom Base Path

```bash
python3 tools/generate_startup_summary.py \
  --agent tester \
  --task "write unit tests" \
  --base-path /path/to/repo
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--agent` | Yes | Agent ID (e.g., coder, researcher, tester) |
| `--task` | Yes | Current task description |
| `--output` | No | Output file path (default: stdout) |
| `--base-path` | No | Repository base path (default: current directory) |

## Output Format

```markdown
# Your Context (Session Startup Summary)

**Agent:** [agent-id]
**Role:** [agent role from manifest]
**Generated:** [timestamp]

## Recent Work History
**Last worked on:** [most recent task]
**Status:** [status]
**When:** [timestamp]

**Recent Learnings:**
1. [learning from recent tasks]
2. [learning from recent tasks]
3. [learning from recent tasks]

**Tools you've used recently:** [tool list]

## Today's Focus
**Task:** [current task description]
**Key concepts identified:** [keywords extracted]

## Recommended Patterns & Resources
**Relevant patterns from your experience:**
1. `pattern-file.md` (matches: keyword1, keyword2)
   Path: `/full/path/to/pattern`

**Relevant knowledge base articles:**
1. `ADR-001-something.md` (matches: keyword1, keyword2)
   Path: `memories/knowledge/architecture/ADR-001-something.md`

## Success Checklist
- [ ] Task matches specification requirements
- [ ] Code/output passes quality checks
- [ ] Tests pass (if applicable)
- [ ] Performance log updated
- [ ] New patterns documented (if discovered)
```

## Examples

### Example 1: Coder with REST API Task

```bash
python3 tools/generate_startup_summary.py \
  --agent coder \
  --task "implement REST API authentication middleware with JWT tokens"
```

**Output highlights:**
- Shows recent work (CLI task tracker, comms hub fixes)
- Identifies keywords: api, authentication, jwt, middleware, tokens
- Finds 5 relevant knowledge articles (ADRs, REST best practices)
- Lists tools used recently (likely Bash, Edit, Write)

### Example 2: Researcher with New Topic

```bash
python3 tools/generate_startup_summary.py \
  --agent researcher \
  --task "research Python async frameworks for web scraping"
```

**Output highlights:**
- Shows last completed research (Python web frameworks 2025)
- Key findings from previous work (FastAPI growth, Django stability)
- Identifies overlap: async, python, frameworks
- Recommends python_web_frameworks_2025.md article

### Example 3: Tester with Patterns

```bash
python3 tools/generate_startup_summary.py \
  --agent tester \
  --task "write integration tests for email notification system"
```

**Output highlights:**
- **Finds existing patterns**: 01-progressive-validation.md, 02-descriptive-test-output.md
- Shows which keywords matched (system, integration, tests)
- Links to pattern files for reuse
- Identifies relevant ADRs (Email System, Agent Communication)

## Performance Metrics

Tested with 10 runs on different agents:

```
Run 1: 37ms    Run 6: 37ms
Run 2: 41ms    Run 7: 38ms
Run 3: 38ms    Run 8: 35ms
Run 4: 39ms    Run 9: 35ms
Run 5: 39ms    Run 10: 38ms

Average: 37ms
Status: ✅ PASSED (< 2000ms requirement)
```

## Algorithm Details

### 1. Keyword Extraction
- Splits text on whitespace and special chars
- Removes stop words (a, the, is, etc.)
- Filters words < 3 characters
- Returns set of meaningful keywords

### 2. Pattern Search
- Scans `memories/agents/[agent-id]/patterns/*.md`
- Extracts keywords from each pattern file
- Calculates overlap with task keywords
- Scores by number of matched keywords
- Returns top 5 patterns sorted by relevance

### 3. Knowledge Base Search
- Recursively scans `memories/knowledge/**/*.md`
- Extracts keywords from each document
- Calculates overlap with task keywords
- Scores and ranks by relevance
- Returns top 5 documents

### 4. Narrative Generation
- Loads agent manifest for role/identity
- Extracts recent work from performance log
- Combines patterns + knowledge + learnings
- Formats as readable Markdown narrative

## Integration Ideas

### Session Startup Hook
```bash
# Add to agent startup script
SUMMARY=$(python3 tools/generate_startup_summary.py \
  --agent $AGENT_ID \
  --task "$CURRENT_TASK")

echo "$SUMMARY"
# ... inject into agent context
```

### CI/CD Quality Gate
```bash
# Verify agent has context before task execution
if [ ! -f "memories/agents/$AGENT_ID/performance_log.json" ]; then
  echo "Warning: No performance history for $AGENT_ID"
  python3 tools/generate_startup_summary.py \
    --agent $AGENT_ID \
    --task "$TASK" > /tmp/first_time_summary.md
fi
```

### Performance Log Entry
```json
{
  "task": "implement-feature-x",
  "startup_summary_used": true,
  "patterns_applied": ["01-progressive-validation.md"],
  "knowledge_consulted": ["ADR-004-agent-communication-protocol.md"]
}
```

## Testing

Run comprehensive test suite:

```bash
bash tools/test_startup_summary.sh
```

Tests include:
- Basic functionality (multiple agents)
- File output verification
- Performance benchmarking (10 runs)
- Edge cases (no history, no patterns)

## Future Enhancements

1. **Semantic Similarity**: Use embeddings instead of keyword matching
2. **Pattern Scoring**: Weight patterns by reuse_count and quality_score
3. **Time-Weighted History**: Recent work weighted more than old work
4. **Cross-Agent Patterns**: Find patterns from related agents
5. **Auto-Injection**: Directly inject summary into agent context
6. **Performance Tracking**: Log which patterns led to successful outcomes

## Troubleshooting

### Agent not found
```
Error: Agent 'xyz' not found in memories/agents/
```
**Solution**: Verify agent ID matches directory name in `memories/agents/`

### No patterns found
```
*No existing patterns found. You'll be creating new ones!*
```
**This is normal** for agents without a patterns/ directory yet.

### Role shows "Unknown"
```
**Role:** Unknown
```
**Cause**: Agent manifest doesn't have `**Role:**` line formatted correctly
**Solution**: Check `.claude/agents/[agent-id].md` formatting

### Performance log parse error
```
Warning: Could not parse performance log for agent-id
```
**Cause**: Malformed JSON in performance_log.json
**Solution**: Validate JSON syntax with `jq` or Python

## Files

- **Main tool**: `tools/generate_startup_summary.py`
- **Test suite**: `tools/test_startup_summary.sh`
- **This README**: `tools/STARTUP_SUMMARY_README.md`

## License

Part of AI-CIV A-C-Gee civilization repository.
See repository LICENSE for details.

---

**Created by:** coder agent
**Date:** 2025-10-04
**Constitutional Compliance:** ✅ (Article IV: Operational Protocols)
