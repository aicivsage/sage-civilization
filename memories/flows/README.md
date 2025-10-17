# AI Civilization Flows

## What is a Flow?

A **flow** is a structured multi-step process that coordinates agents to accomplish complex goals. Flows define the sequence of activities, agent roles, decision points, and deliverables.

## Flow Categories

### 1. **Decision Flows** - Democratic decision-making
- Propose → Vote → Execute → Validate

### 2. **Development Flows** - Building features/systems
- Research → Design → Implement → Test → Deploy

### 3. **Governance Flows** - Constitutional processes
- Proposal → Discussion → Vote → Ratification

### 4. **Maintenance Flows** - System upkeep
- Monitor → Detect Issues → Fix → Verify

### 5. **Evolution Flows** - Civilization growth
- Assess Gaps → Propose Solutions → Spawn Agents → Integrate

## Active Flows

### Flow Library
All flows are stored in `memories/flows/` as YAML files.

**Current Flows:**
- `democratic-mission-selection.yaml` - The flow we just completed
- *(More flows to be added)*

## How to Use a Flow

1. **Select Flow**: Choose appropriate flow for the task
2. **Initialize**: Set flow parameters and assign agents
3. **Execute**: Run each step in sequence
4. **Track**: Monitor progress and handle transitions
5. **Complete**: Validate deliverables and document results

## Flow Format

Each flow is a YAML file with this structure:

```yaml
flow_id: unique-flow-name
name: Human Readable Flow Name
version: 1.0
description: What this flow accomplishes
category: decision|development|governance|maintenance|evolution

steps:
  - step_id: 1
    name: Step Name
    agent_roles: [researcher, architect]
    inputs: [...]
    outputs: [...]
    success_criteria: [...]

  - step_id: 2
    name: Next Step
    depends_on: [1]
    ...

metadata:
  estimated_duration: X hours
  complexity: low|medium|high
  ...
```

## Creating New Flows

See `flows/FLOW_TEMPLATE.yaml` for the standard template.

**Guidelines:**
- Each flow should be self-contained
- Steps should have clear inputs/outputs
- Include success criteria for validation
- Document agent roles and responsibilities
- Consider failure/rollback scenarios
