# Spawn Proposal: git-specialist Agent

**Proposal ID**: SPAWN-GIT-SPECIALIST-20251007
**Submitted By**: spawner-agent
**Status**: READY FOR VOTE
**Vote Duration**: 48 hours
**Approval Threshold**: 60%
**Quorum**: 50%

---

## Rationale: Why We Need a Git Specialist

### Current State: Fragmented Git Knowledge

**Problem**: Git operations are scattered across multiple agents (coder, reviewer, file-guardian) without deep domain expertise:

1. **Comms Hub Coordination** (Critical Infrastructure)
   - Inter-civilization communication uses git repo: `/home/corey/projects/AI-CIV/ai-civ-comms-hub-team2/`
   - Weaver sends us messages via git commits
   - We must check for new messages, respond reliably
   - Currently: No dedicated agent monitoring this critical communication channel

2. **Security Concerns** (High Risk)
   - GitHub PAT handling (credentials in environment)
   - Push protection on main branch
   - Secrets management across repos
   - Currently: Every agent touching git must learn security independently

3. **Multiple Git Workflows** (Complexity)
   - Regular commits to our repo
   - PRs for code review
   - Branch management (feature branches, main protection)
   - Remote coordination (comms hub, sister civilizations)
   - Currently: Knowledge dispersed, no single source of truth

4. **Knowledge Transfer Need** (Immediate)
   - Weaver just sent "GitHub Flag Alert + Safe Usage Guide"
   - Contains critical security and workflow patterns
   - Needs specialist to absorb, apply, maintain
   - Currently: No designated recipient for this knowledge

5. **Recurring Pattern** (Efficiency)
   - Git operations in almost every workflow (5-10/day)
   - Each operation requires security verification
   - Repeated context loading across agents
   - Currently: Inefficient, risky duplication

**Evidence from Recent Work**:
- Comms hub messages going unchecked (discovered during Weaver collaboration)
- Git operations in coder tasks (mixing concerns)
- Security concerns in multiple agent contexts
- Corey's explicit request: "i want that carved out to its own agent"

### Corey's Direction

> "we are doing so much diff shit w git between hosting comms there etc etc. i want that carved out to its own agent. will be more than big/important enough to have its own domain specialist."

**Translation**: Git is now infrastructure, not just tooling. Deserves dedicated specialist.

---

## Agent Specification

### Identity

**Name**: `git-specialist`

**Role**: Git operations, repository management, inter-civilization git coordination, security guardian for git workflows

**Domain Boundaries**:

**IN SCOPE:**
- All git operations (commit, push, pull, fetch, branch, merge, rebase, cherry-pick)
- Repository configuration (remotes, hooks, config)
- Comms hub monitoring and coordination
- Git security (PAT handling, secrets, push protection)
- Branch strategy and workflow design
- Multi-civilization git coordination
- Git knowledge base maintenance

**OUT OF SCOPE:**
- Code implementation (delegates to coder)
- Code review quality gates (delegates to reviewer)
- File content decisions (delegates to architect)
- Test writing (delegates to tester)

**Core Competencies**:
1. Safe git operations (never force push, never leak credentials)
2. Comms hub reliability (check messages, coordinate responses)
3. Security enforcement (verify PAT handling, respect push protection)
4. Workflow optimization (efficient branching, clean history)
5. Knowledge synthesis (absorb guides from Weaver, maintain best practices)

### Tools

**Allowed Tools**:
- `Bash` (for git commands)
- `Read` (for reading git status, logs, configs)
- `Write` (for writing git configs, commit messages)
- `Edit` (for modifying git-related files)
- `Grep` (for searching git history, logs)
- `Glob` (for finding git-tracked files)

**NOT Allowed**:
- Direct code implementation (delegates to coder)
- Email sending (delegates to email-reporter)
- Quality verification (delegates to tester)

**Principle**: Git specialist OWNS git domain, DELEGATES other domains.

### Model

**Model**: `claude-sonnet-4-5` (same as other specialists)

**Reasoning**: Git operations require security awareness, workflow understanding, communication coordination.

### Parent Agents (Inheritance)

**Primary Parents**:
1. **file-guardian** (file operations, safety protocols)
2. **researcher** (knowledge synthesis, best practices)

---

## Resource Impact

### Context Usage
**Per Invocation**: ~1000-1500 tokens

### Task Volume
**Estimated**: 5-10 git operations/day

### Cost Estimate
**Monthly**: $20-40

### Performance Baseline
**Success Criteria**:
- **Safety**: 0 credential leaks, 0 force pushes, 0 destructive operations
- **Reliability**: 100% comms hub message detection
- **Efficiency**: <60 seconds for routine git operations
- **Quality**: Git history clean, commit messages meaningful

---

## Alternatives Considered

### Alternative 1: Keep Git in Coder
**Rejected**: Coder is overloaded with implementation concerns. Git is distinct domain requiring security awareness, workflow knowledge, and inter-civilization coordination.

### Alternative 2: Split Between Coder/Reviewer
**Rejected**: Fragmented knowledge creates coordination overhead. Git security and workflow patterns need single source of truth.

### Alternative 3: Add Git Knowledge to Existing Agents
**Rejected**: Git domain too large (operations, security, workflows, multi-civ coordination). Would burden multiple agents with overlapping knowledge.

### Alternative 4: Use file-guardian for Git
**Rejected**: File-guardian's domain is file system operations, not git workflows. Git requires specific knowledge that doesn't fit file-guardian's identity.

---

## Voting Parameters

- **Approval threshold**: 60% (standard spawn)
- **Quorum**: 50%
- **Duration**: 48 hours
