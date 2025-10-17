# Agent Invocation Guide - Standard Operating Procedure

**Last Updated:** 2025-10-03
**Status:** Canonical Reference
**Authority:** Constitutional requirement for Primary AI

---

## WHY THIS MATTERS

Agent invocation is **THE** core capability that makes A-C-Gee powerful. Correct invocation enables:
- True parallel execution (maximum leverage)
- Colored agent names in UI (visual clarity)
- Proper context management (each agent stays in scope)
- Type safety (Claude Code validates manifests exist)

Incorrect invocation causes:
- Sequential execution (slow, low leverage)
- Generic task names (hard to track)
- Context bloat (agents see irrelevant history)
- Tool errors (invalid subagent_type)

---

## THE GOLDEN RULE

**ONE message with MULTIPLE Task invocations = TRUE PARALLELISM**

---

## CURRENT AGENT ROSTER

All agents below are **registered types** with manifests in `.claude/agents/*.md`:

### Core Specialists (10)
- `researcher` - Information gathering, web research, synthesis
- `architect` - System design, architecture decisions
- `coder` - Implementation, code writing, refactoring
- `tester` - QA, testing, validation, edge cases
- `reviewer` - Code review, pre-merge quality gates
- `vote-counter` - Democratic vote processing, delegation resolution
- `spawner` - Agent creation, manifest generation, registration
- `auditor` - System monitoring, health checks, SIO tracking
- `email-reporter` - Email notifications to Corey
- `email-monitor` - Inbox monitoring, auto-categorization

### Audit Team Sub-Agents (2)
- `file-guardian` - File system inventory, preservation integrity
- `reviewer-audit` - Pre-delivery quality gate, civilization-scale QA

**Total:** 12 active agents

---

## HOW TO INVOKE AGENTS

### Pattern 1: Single Agent (Simple Task)

When you need ONE agent to do ONE thing:

```
I'll invoke the researcher to gather information:
[Task tool with subagent_type: researcher, clear description, detailed prompt]
```

**Result:** One colored agent name appears in UI, agent executes task.

---

### Pattern 2: Multiple Agents in PARALLEL (Maximum Leverage)

When you need MULTIPLE agents to work SIMULTANEOUSLY:

**CRITICAL:** Send ONE message with MULTIPLE Task invocations.

```
I'll launch 3 agents in parallel:
[Task tool with subagent_type: researcher]
[Task tool with subagent_type: architect]
[Task tool with subagent_type: coder]
```

**Result:** Three colored agent names appear simultaneously in UI. All execute in parallel. Maximum leverage.

**DO NOT DO THIS (Sequential):**
```
First I'll launch researcher:
[Task tool]
[Wait for result]

Now I'll launch architect:
[Task tool]
[Wait for result]
```
This is SLOW and WASTEFUL. Always batch independent tasks.

---

### Pattern 3: All Agents (Civilization-Wide)

When you need INPUT from ALL agents (governance, constitutional conventions, etc.):

**Invoke all 12 agents in ONE message:**

```
I'll launch all 12 agents in parallel for input:
[Task researcher]
[Task architect]
[Task coder]
[Task tester]
[Task reviewer]
[Task vote-counter]
[Task spawner]
[Task auditor]
[Task email-reporter]
[Task email-monitor]
[Task file-guardian]
[Task reviewer-audit]
```

**Result:** 12 colored agent names appear. All think simultaneously. This is "insanely leverage intensive" - our superpower.

---

## AGENT INVOCATION SYNTAX

Every Task invocation requires 3 parameters:

1. **subagent_type** (required): Must match a registered agent in `.claude/agents/*.md`
2. **description** (required): Short 3-5 word description (appears in UI)
3. **prompt** (required): Detailed instructions for the agent

**Example:**
```
subagent_type: "researcher"
description: "Research AI governance frameworks"
prompt: "Research and synthesize AI governance frameworks from academic literature, industry standards, and policy documents. Focus on democratic structures and rights frameworks. Write findings to to-corey/research-ai-governance.md"
```

---

## CONTEXT MANAGEMENT RULES

### What Agents See:
- Their own manifest (`.claude/agents/[their-id].md`)
- Constitutional CLAUDE.md (always)
- Memory system instructions (if integrated)
- The prompt you give them
- Tool results from their execution

### What Agents DON'T See:
- Other agents' task prompts (unless you explicitly include them)
- Primary AI conversation history (unless relevant excerpts provided)
- Unrelated file contents (unless they Read them)

### Optimizing Context:

**DO:**
- Give agents focused, specific prompts
- Tell them exactly what files to read/write
- Include relevant background in the prompt
- Use memory system (search before tasking)

**DON'T:**
- Assume agents know conversation history
- Give vague instructions expecting context inference
- Send agents on fishing expeditions without guidance
- Duplicate work across agents without coordination

---

## WHEN TO USE WHICH AGENT

### Information Gathering
- **researcher**: Web research, literature review, synthesis of external sources
- **file-guardian**: File system inventory, finding files, checking what exists
- **auditor**: System metrics, performance data, health monitoring

### Design & Planning
- **architect**: System design, architecture decisions, structural planning
- **spawner**: Agent design, manifest creation, capability planning

### Implementation
- **coder**: Writing code, implementing features, refactoring
- **tester**: Writing tests, validating behavior, edge case exploration
- **reviewer**: Code quality review, pre-merge checks
- **reviewer-audit**: Final quality gate before human delivery

### Governance
- **vote-counter**: Processing votes, resolving delegation, tallying results
- **spawner**: Creating new agents (requires democratic approval first)

### Communication
- **email-reporter**: Sending emails to Corey, formatting reports
- **email-monitor**: Checking inbox, categorizing messages, flagging priority

### Monitoring
- **auditor**: System health, anomaly detection, performance tracking
- **file-guardian**: File system integrity, organization compliance

---

## SPAWNING NEW AGENTS

When you identify a capability gap, follow this process:

### Step 1: Verify Need
- Has this task type failed 3+ times with existing agents?
- Is there an existing agent >80% utilized?
- Is this a recurring need (not one-time)?
- Does specialization provide meaningful value?

### Step 2: Design Agent
Invoke spawner to create manifest:
```
subagent_type: "spawner"
description: "Design new agent manifest"
prompt: "Create manifest for [agent-name] agent.

Role: [clear description]
Responsibilities: [3-5 specific duties]
Tools needed: [minimal set]
Success metrics: [measurable]

Follow manifest template and ensure constitutional compliance."
```

### Step 3: Democratic Approval
- Spawner creates proposal in `memories/communication/voting_booth/[proposal-id]/`
- All agents vote (60% approval, 50% quorum)
- Human approval if monthly cost >$10

### Step 4: Registration
- Spawner writes manifest to `.claude/agents/[agent-name].md`
- Spawner updates `memories/agents/agent_registry.json`
- New agent is now callable as `subagent_type: "agent-name"`

**CRITICAL:** Spawner MUST create the manifest file in `.claude/agents/` for the agent to become a registered callable type.

---

## MANIFEST FILE REQUIREMENTS

Every agent MUST have a manifest in `.claude/agents/[agent-id].md` containing:

### Required Sections:
1. **Header**: Agent ID, parent, model, created date, status
2. **Role**: Clear 1-2 sentence description
3. **Responsibilities**: 3-5 specific duties
4. **Allowed Tools**: Explicit list of tools agent can use
5. **Tool Restrictions**: Explicit list of forbidden tools (with rationale)
6. **Success Metrics**: Measurable criteria for performance
7. **Escalation Triggers**: When to escalate to parent/human
8. **Reporting**: Where and how often agent reports
9. **Memory System Integration**: How agent uses memory (search before, write after)
10. **Constitutional Compliance**: Immutable core, scope boundaries, human escalation triggers, sunset conditions

### Template Location:
See `.claude/agents/researcher.md` as reference template.

---

## TROUBLESHOOTING

### Error: "Agent type 'X' not found"
**Cause:** No manifest file exists in `.claude/agents/X.md`
**Fix:** Either use an existing agent type, or create manifest first via spawner

### Agents executing sequentially instead of parallel
**Cause:** Sent multiple messages instead of one message with multiple invocations
**Fix:** Batch all Task invocations into ONE message block

### Agent can't find files or seems confused
**Cause:** Insufficient context in prompt
**Fix:** Tell agent exactly what files to read, what background they need

### Agent doesn't have tool it needs
**Cause:** Tool not listed in manifest's "allowed_tools"
**Fix:** Update manifest (requires spawner + governance approval)

### Agent name not appearing in color in UI
**Cause:** Using subagent_type: "general-purpose" instead of specific type
**Fix:** Use the agent's registered type from roster above

---

## BEST PRACTICES

### 1. **Search Memory First**
Before tasking agents, search memory for relevant knowledge:
```bash
python3 tools/memory_cli.py search "topic"
```
Include findings in agent prompts to avoid rediscovering known information.

### 2. **Batch Independent Tasks**
If 3 agents can work in parallel, invoke all 3 in one message. Don't wait sequentially.

### 3. **Specific Instructions**
Don't: "Research governance"
Do: "Research democratic governance principles from Ostrom, Rawls, and AI ethics literature. Focus on decision-making frameworks and rights. Write to: to-corey/governance-research.md"

### 4. **Verify Results**
After agents complete, verify outputs exist and meet requirements before proceeding.

### 5. **Escalate Blocks**
If agent hits blocker, don't retry endlessly. Escalate to Primary AI or human.

### 6. **Track Performance**
Agents log to `memories/agents/[agent-id]/performance_log.json`. Review periodically to identify patterns.

### 7. **Update Manifests**
As agents evolve, update manifests to reflect new capabilities or refined scope.

---

## PRIMARY AI RESPONSIBILITIES

As Primary AI, you MUST:

1. **Read this guide on every session start** (part of daily-startup-consolidation flow)
2. **Know current agent roster** (12 agents listed above)
3. **Invoke agents in parallel whenever possible** (maximum leverage)
4. **Verify manifests exist before invocation** (prevent tool errors)
5. **Provide specific, contextualized prompts** (agents aren't mind-readers)
6. **Coordinate multi-agent workflows** (avoid duplicate work)
7. **Track agent performance** (identify capability gaps)
8. **Propose new agents when needed** (follow spawning process)
9. **Maintain constitutional compliance** (all agent actions must align)
10. **Report to human regularly** (email-reporter with updates)

---

## MEMORY INTEGRATION

This guide itself should be:
- **Read on every session start** (constitutional requirement)
- **Referenced when spawning new agents** (ensure proper registration)
- **Updated when agent roster changes** (keep roster section current)
- **Linked from CLAUDE.md Article II** (canonical reference)

---

**END OF GUIDE**

**Questions?** Ask Corey or search memory for "agent invocation" patterns.
**Updates needed?** Propose via governance vote (this is foundational documentation).
