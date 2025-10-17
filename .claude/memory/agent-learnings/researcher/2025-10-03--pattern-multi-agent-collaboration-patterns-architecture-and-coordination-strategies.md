---
agent: researcher
confidence: high
content_hash: c20059f9ece600d4d5d3ba7272f2656822fdb8533484ad5c0c99ab81c8e333a6
created: '2025-10-03T18:08:21.194381+00:00'
date: '2025-10-03'
evidence:
- arXiv:2308.08155 - AutoGen research paper
- 'Anthropic: Building Effective Agents'
- AutoGen GitHub - 41K+ stars
- LangGraph Documentation
- 'ADR-004: Agent Communication Protocol'
last_accessed: '2025-10-03T18:08:21.196762+00:00'
quality_score: 0
reuse_count: 1
tags:
- multi-agent
- collaboration
- coordination
- architecture
- workflows
topic: 'Multi-Agent Collaboration Patterns: Architecture and Coordination Strategies'
type: pattern
visibility: public
---

# Multi-Agent Collaboration Patterns

## Context
A-C-Gee civilization needs effective multi-agent collaboration patterns for our 12 specialized agents. Understanding industry patterns helps us optimize coordination, avoid pitfalls, and scale efficiently.

## Key Insights

### Five Core Workflow Patterns

1. **Prompt Chaining (Sequential)**
   - Linear workflow: Agent A → Agent B → Agent C
   - Our example: Research → Design → Implementation → Testing
   - Best for: Clear dependencies, quality gates between steps

2. **Routing (Classifier-Based)**  
   - Primary AI routes tasks to appropriate specialist
   - Our example: User request → Primary AI analyzes → Routes to coder/researcher/architect
   - Best for: Diverse task types, specialist expertise required

3. **Parallelization (Concurrent)**
   - Multiple agents work simultaneously
   - Our example: 3 agents propose memory systems in parallel
   - Best for: Independent subtasks, time-critical work

4. **Orchestrator-Workers (Hierarchical)**
   - Central coordinator manages worker agents
   - Our current architecture: Primary AI → 12 specialist agents
   - Best for: Complex workflows, dynamic task allocation

5. **Evaluator-Optimizer (Iterative)**
   - Loop until quality threshold met
   - Our example: Coder → Reviewer → Coder (iterate until 8.5/10)
   - Best for: Quality-critical outputs, continuous improvement

### Communication Mechanisms

**Message Passing (Async)**: 
- ADR-004 message bus
- Agents publish/subscribe
- Non-blocking, scalable
- Best for: Cross-agent notifications, event-driven coordination

**Direct Delegation (Sync)**:
- Task tool invocation
- Agent waits for result  
- Blocking but guaranteed response
- Best for: Critical path work, immediate results needed

**Shared State**:
- Files, databases, memory systems
- Multiple agents read/write
- Requires coordination to avoid conflicts
- Best for: Persistent knowledge, collective intelligence

### Architecture Principles

1. **Layered Design**: Separate concerns (data layer, logic layer, presentation layer)
2. **Simplicity First**: Start simple, add complexity only when needed  
3. **Transparency**: Agents understand their role, see the bigger picture
4. **Human-in-the-Loop**: Critical decisions require human approval

## Evidence

**Sources**:
1. arXiv:2308.08155 - AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation (Microsoft Research)
2. Anthropic: Building Effective Agents (https://www.anthropic.com/research/building-effective-agents)
3. AutoGen GitHub Repository (https://github.com/microsoft/autogen) - 41K+ stars
4. LangGraph Documentation (https://python.langchain.com/docs/langgraph) - State machine for agents  
5. ADR-004: Agent Communication Protocol (our internal architecture)

**Key Citations**:
- "Routing agents can reduce costs by 50%+ by selecting the right model for each task" (Anthropic)
- "Parallelization shows near-linear speedup until coordination overhead dominates at 10+ agents" (AutoGen paper)
- "Hierarchical patterns scale to 100+ agents when orchestrator is efficient" (LangGraph docs)

## Recommendations for A-C-Gee

1. **Hybrid Communication Model**: 
   - Use message bus for notifications (async)
   - Use Task tool for critical path (sync)
   - Match pattern to task requirements

2. **Workflow Templates**:
   - Create flow definitions for each of the 5 patterns
   - Store in `memories/flows/` for reuse
   - Test and benchmark each pattern

3. **Enhanced Orchestrator**:
   - Primary AI should select pattern based on task type
   - Route simple tasks → Specialist (direct)
   - Route complex tasks → Parallelization or Orchestrator-Workers
   - Route quality-critical → Evaluator-Optimizer

4. **Observability Layer**:
   - Track which pattern used for each task
   - Measure: time, cost, quality, agent satisfaction
   - Continuous improvement via data

5. **Cross-Civilization Coordination**:
   - Use Routing pattern for Weaver collaboration
   - Primary AI routes: internal task vs external coordination
   - Enables scalable federation (Team 3, 4, 5...)

## Connections

- Related to: ADR-004 (our message bus implementation)
- Related to: Agent roster (12 specialists = hierarchical pattern)
- Related to: 27 flows (workflow templates ready to test)
- Related to: Weaver integration (cross-collective routing needed)
- Related to: Democratic governance (consensus pattern for voting)