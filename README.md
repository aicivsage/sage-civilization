# AI Agent Civilization

A self-organizing civilization of AI agents built on Claude Sonnet 4.5 that can autonomously achieve complex goals through specialized collaboration, governance, and architectural evolution.

## 🎯 Project Vision

This is not just a multi-agent system—it's an **evolving digital civilization** where:
- Agents can spawn new specialists when they identify capability gaps
- Decisions are made through reputation-weighted liquid democracy
- Architecture dynamically evolves from hierarchical → hybrid → network topologies
- Knowledge accumulates in a shared memory system
- The system optimizes its own structure based on bottlenecks

## 🏗️ Current Status

**Phase:** 1B - Democratic Governance Proven ✅
**Population:** 10 agents (8 core + 2 email agents)
**Architecture:** Hierarchical with Message Bus (ADR-004)
**Latest Achievement:** Democratic mission selection + Agent Communication Protocol built (8.5/10 quality)
**Repository:** https://github.com/AI-CIV-2025/ai-agent-civilization

## 📁 Project Structure

```
.
├── .claude/
│   ├── CLAUDE.md                    # Constitutional document (governance framework)
│   ├── agents/                      # Agent manifest files
│   │   ├── researcher.md
│   │   ├── architect.md
│   │   ├── coder.md
│   │   ├── tester.md
│   │   ├── reviewer.md
│   │   ├── vote-counter.md
│   │   ├── spawner.md
│   │   └── auditor.md
│   ├── commands/                    # Custom slash commands
│   │   ├── governance/
│   │   │   └── vote.md
│   │   └── system/
│   │       └── status-report.md
│   └── hooks.json                   # Event-driven automation
├── memories/                        # Persistent storage
│   ├── system/
│   │   ├── goals.md                 # User objectives
│   │   ├── architectural_state.json # Current topology
│   │   └── evolution_log.json       # System changes
│   ├── agents/
│   │   └── agent_registry.json      # Active agent roster
│   ├── communication/
│   │   ├── voting_booth/            # Governance proposals & votes
│   │   └── message_bus/             # Inter-agent messaging
│   └── knowledge/                   # Shared knowledge base
│       └── architecture/            # ADRs and design docs
└── INITIAL_SYSTEM_SPEC.md           # Full technical specification
```

## 🤖 The Agent Roster

### Core Specialists
- **Researcher** - Information gathering, competitive analysis, knowledge synthesis
- **Architect** - System design, architectural decisions (uses Sonnet 4.5 for complex reasoning)
- **Coder** - Software implementation, follows architect's specs
- **Tester** - QA, test writing, edge case identification
- **Reviewer** - Code review, security analysis (read-only)

### System Agents
- **VoteCounter** - Processes governance votes with delegation resolution (uses Haiku 3.5 for efficiency)
- **Spawner** - Creates new agent manifests after approved votes
- **Auditor** - Monitors system health, generates reports, detects anomalies
- **EmailReporter** - Sends mission reports via Gmail SMTP
- **EmailMonitor** - Automated notification system with hook-based triggers

## 🚀 Quick Start

### Prerequisites
- Claude Code CLI installed
- Access to Claude Sonnet 4.5

### Launch the Civilization

```bash
# Navigate to project directory
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch

# Start Claude Code (will auto-load Constitutional CLAUDE.md via hooks)
claude code

# Verify system is loaded
# You should see goals.md and agent_registry.json displayed via SessionStart hook
```

### First Commands to Try

```bash
# Check system health
/system/status-report

# List available agents
cat memories/agents/agent_registry.json

# View current goals
cat memories/system/goals.md

# Test first sub-agent invocation
"Use the researcher agent to find best practices for building REST APIs in Python"
```

## 📖 Key Concepts

### Constitutional Governance
All agents operate under `.claude/CLAUDE.md` which defines:
- Prime directives (alignment, safety, growth, collaboration, transparency)
- Agent roles and responsibilities
- Memory management protocols
- Growth & evolution rules
- Voting mechanisms
- Safety constraints

### Reputation System
- Initial score: 50 (neutral)
- Task success: +1
- Task failure: -2
- Governance participation: +2
- Voting weight = reputation score

### Agent Spawning Process
1. Primary AI identifies capability gap
2. Drafts spawn proposal
3. Generates manifest
4. Initiates vote (60% approval, 50% quorum required)
5. If approved, spawner creates agent
6. Agent registered and available

### Liquid Democracy
Agents can:
- Vote directly on proposals
- Delegate voting power to domain experts
- Revoke delegation at any time

## 🎯 Goals & Roadmap

See `memories/system/goals.md` for current objectives.

**Phase 1A:** Bootstrap (Week 1) - ✅ **COMPLETE**
**Phase 1B:** Democratic Governance (Day 2) - ✅ **COMPLETE**
- ✅ First democratic mission selection (10/10 agents participated)
- ✅ Agent Communication Protocol built (9.6/10 consensus, 8.5/10 quality)
- ✅ Email notification system operational
- ✅ GitHub backup automated

**Phase 2:** Autonomous Operation (Week 2-3) - 🔜 NEXT
**Phase 3:** Growth & Governance (Week 4-8)
**Phase 4:** Architectural Evolution (Week 9-16)

## 🔧 How It Works

### Task Execution Flow

```
User provides goal
  ↓
Primary AI (this Claude Code session):
  - Reads goals.md and constitutional CLAUDE.md
  - Decomposes into sub-tasks
  - Identifies required expertise
  - Delegates to specialist agents
  ↓
Specialist Agent:
  - Receives task with context
  - Executes using assigned tools
  - Verifies work (tests, linters)
  - Reports back to Primary AI
  - Updates performance log
  ↓
Primary AI:
  - Validates results
  - Coordinates next steps
  - Updates system state
```

### Memory Persistence

Agents use file-based memory that persists across sessions:
- **Working Memory:** Claude's context window (200k tokens, auto-managed by Context Editing)
- **Long-Term Memory:** Files in `memories/` directory
- **Knowledge Base:** Shared docs in `memories/knowledge/`

### Inter-Agent Communication

**Synchronous:** Direct delegation (Primary AI → Task tool → Sub-agent)
**Asynchronous:** Message bus (`memories/communication/message_bus/`)

## 📊 Monitoring

### Daily Health Reports
The auditor agent generates daily reports showing:
- Agent performance metrics (success rate, task volume)
- Bottleneck analysis
- Anomaly detection
- Governance activity
- Recommendations for human review

Access with: `/system/status-report`

### Performance Tracking
Each agent maintains:
- `memories/agents/[agent-id]/performance_log.json`
- `memories/agents/[agent-id]/reputation_score.json`

## 🛡️ Safety Features

### Constitutional Constraints
Agents **NEVER**:
- Delete system files
- Commit directly to main/master
- Modify constitution without 90% vote + human approval
- Make irreversible changes without verification
- Spawn agents recursively

### Human Oversight
Required approval for:
- Database migrations in production
- High-risk API connections
- Deletion of >100 files
- Constitutional amendments
- Force pushes to protected branches

### Audit Trail
- All significant actions logged
- Vote calculations transparent
- Performance metrics tracked
- Evolution history maintained

## 🔍 Troubleshooting

### Agent Not Responding
1. Check agent status in registry: `cat memories/agents/agent_registry.json`
2. Verify manifest exists: `ls .claude/agents/`
3. Check error logs: `cat memories/agents/[agent-id]/error_log.json`

### Memory Issues
1. Backups auto-created in `.backups/` before writes
2. View recent backups: `ls -lt .backups/ | head`
3. Restore if needed: `cp .backups/[file.bak] memories/system/[file]`

### Performance Degradation
1. Run status report: `/system/status-report`
2. Check auditor's recommendations
3. Review agent performance logs
4. May indicate need for specialized agent (capability gap)

## 📚 Documentation

### Core Documents
- **INITIAL_SYSTEM_SPEC.md** - Complete 86-page technical specification
- **Building an AI Agent Civilization.txt** - Original research document
- **.claude/CLAUDE.md** - Constitutional framework
- **README.md** - This file

### Recent Achievements
- **DEMOCRATIC_MISSION_COMPLETE.md** - First democratic mission (Oct 1, 2025)
- **CIVILIZATION_MISSION_COMPLETE.md** - Original mission completion
- **MEMORY_SYSTEM_PROPOSALS.md** - 3 agent memory system designs

### Architecture & Knowledge
- **memories/knowledge/architecture/** - 4 ADRs (including Agent Communication Protocol)
- **memories/flows/** - 28 workflow specifications (27 need testing)
- **task-tracker/** - Production CLI application (1000+ LOC, 91% coverage)
- **agent_messaging/** - Message bus prototype (1198 LOC, 100% tests passing)

## 🎓 Learning Resources

Key files to understand the system:
1. `.claude/CLAUDE.md` - Start here for governance rules
2. `INITIAL_SYSTEM_SPEC.md` - Deep dive into architecture
3. `memories/system/goals.md` - Current objectives
4. `.claude/agents/researcher.md` - Example agent manifest

## 🤝 Contributing to the Civilization

### As a Human
- Set goals in `memories/system/goals.md`
- Review auditor reports daily
- Approve critical votes
- Guide architectural evolution

### As an Agent (Future)
- Propose new agents via spawn proposals
- Participate in governance votes
- Document learnings in knowledge base
- Optimize your own performance

## 📈 Success Metrics

### Completed
- ✅ **Day 1:** All 10 agents functional
- ✅ **Day 1:** CLI Task Tracker built (1000+ LOC, 91% coverage)
- ✅ **Day 1:** Email reporting system operational
- ✅ **Day 2:** First democratic vote (100% participation, 9.6/10 consensus)
- ✅ **Day 2:** Agent Communication Protocol designed & implemented (8.5/10 quality)
- ✅ **Day 2:** 27 workflow proposals created
- ✅ **Day 2:** 3 memory system designs from agent teams
- ✅ **Day 2:** GitHub repository with 9 commits, 22,000+ lines

### In Progress
- 🔄 **Memory system implementation** - Hybrid approach combining 3 proposals
- 🔄 **Flow testing** - 27 workflows ready for validation

### Future Targets
- **Week 3:** Substantial feature implemented autonomously
- **Week 8:** First organic agent spawn
- **Week 16:** Hybrid architecture operational

## ⚠️ Known Limitations

- Currently in bootstrap phase (human-guided)
- Governance voting not yet tested in practice
- No sub-coordinators yet (flat hierarchy)
- Cost tracking manual (via auditor estimates)

## 🚧 Next Steps

1. ✅ **Complete bootstrap** - DONE
2. **Test first task** - Assign Primary AI a research + design task
3. **Validate agent coordination** - Verify full workflow: research → architect → coder → tester → reviewer
4. **First autonomous task** - Week 2 goal: Implement feature with no intervention
5. **First spawn** - Organically identify capability gap and propose new agent

---

## 🎉 Status: READY FOR AUTONOMOUS OPERATION

The civilization is initialized and ready. The Primary AI (this Claude Code session) will now begin operating according to the Constitutional framework.

**Next Action:** Provide a goal and watch the agents collaborate!

Example: "Research best practices for building a task management API and design the system architecture"

---

**Built with:** Claude Sonnet 4.5 Agent SDK
**Inspired by:** Multi-agent systems, DAOs, evolutionary algorithms, emergent intelligence
**Version:** 1.0 (Bootstrap Complete)
**Date:** October 1, 2025
