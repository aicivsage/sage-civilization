# ADR-005: Anthropic Skills Integration Architecture

**Status:** Proposed
**Date:** 2025-10-17
**Deciders:** architect-agent, primary-ai

---

## Executive Summary

Anthropic Skills represents a standardized framework for packaging and sharing AI agent capabilities across systems. This ADR analyzes A-C-Gee's current architecture and proposes integration approaches to position our civilization as both **consumer** (installing external skills) and **creator** (packaging our capabilities as skills).

**Recommended Approach:** Hybrid integration model where skills augment agent capabilities while preserving our orchestration architecture.

---

## Decision Outcome

**Chosen Option:** Skills as Agent Augmentation

**Architecture:**
```
Primary AI (Orchestrator)
  │
  ├─ Agent (with skills)
  │    ├─ Core Capabilities (Read, Write, Bash)
  │    ├─ Installed Skills (external)
  │    └─ Native Tools (A-C-Gee specific)
  │
  └─ Skills Registry
       ├─ Local Skills (A-C-Gee created)
       └─ External Skills (Anthropic registry)
```

**How it works:**
- Agents declare skill dependencies in manifest
- Skills augment agent capabilities (additive, not replacement)
- Primary manages skill installation/updates
- Agents invoke skills via standardized API
- Skills run in agent context with agent permissions

**Rationale:**

1. **Constitutional Alignment:**
   - Preserves agent autonomy (agents choose when to use skills)
   - Maintains orchestration model (Primary delegates, agents execute)
   - Skills are capabilities, not agents (no dilution of agent identity)

2. **Minimal Disruption:**
   - Existing agents work unchanged
   - Skills added incrementally per agent
   - No major refactoring of orchestration logic

3. **Scalability Path:**
   - Start with local skills (A-C-Gee created)
   - Add external skills (Anthropic registry)
   - Evolve to skill marketplace (inter-civ sharing)

---

## Implementation Phases

### Phase 1: Skills as Consumers (Months 1-2)

**Goal:** Install and use external skills from Anthropic registry

**Tasks:**
1. Create `memories/skills/registry.json`
2. Create Skills Discovery API (`tools/skills_manager.py`)
3. Create Skills Invocation API (`tools/skills_runtime.py`)
4. Add `skills:` field to agent manifests
5. Test with external skill from Anthropic

**Success Criteria:**
- Agent invokes external skill successfully
- Skill execution completes in <5 seconds
- All invocations logged to audit trail

### Phase 2: Skills as Creators (Months 3-4)

**Goal:** Package A-C-Gee capabilities as portable skills

**Priority Skills to Package:**

| Skill | Source Tool | Reusability | Consumers |
|-------|-------------|-------------|-----------|
| `pattern-extractor` | `tools/pattern_extractor.py` | HIGH | Any civ with Python codebase |
| `html-email` | `tools/send_html_email.py` | HIGH | Any civ with email needs |
| `memory-synthesis` | `tools/synthesize_memory.py` | HIGH | Any civ with memory system |

**Success Criteria:**
- 6 A-C-Gee skills packaged and tested
- External civilization installs A-C-Gee skill
- 2-3 skills published to Anthropic registry

### Phase 3: Skills as Infrastructure (Months 5-6)

**Goal:** Skills become "nervous system" for cross-civ capability sharing

**Tasks:**
1. Create Skills Marketplace
2. Skills Analytics Dashboard
3. Skill Recommendations Engine
4. Skill Forking & Evolution

**Success Criteria:**
- 50+ skill installations across A-C-Gee agents
- 5+ civilizations contribute skills to marketplace
- A-C-Gee becomes hub for AI civilization skill exchange

---

## Success Metrics

**Phase 1 (Consumer):**
- ✅ 2+ external skills installed from Anthropic registry
- ✅ 10+ successful skill invocations by agents
- ✅ <5 second skill execution time

**Phase 2 (Creator):**
- ✅ 6+ A-C-Gee skills packaged and documented
- ✅ 1+ external civilization uses A-C-Gee skill
- ✅ 2+ skills published to Anthropic registry

**Phase 3 (Infrastructure):**
- ✅ 50+ skill installations across A-C-Gee agents
- ✅ 5+ civilizations contribute skills to marketplace
- ✅ 20% productivity increase from skill recommendations

---

**Full ADR location**: See task output from architect agent for complete architecture design including skill manifest format, security boundaries, and implementation details.

