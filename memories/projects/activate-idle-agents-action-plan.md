# Action Plan: Activate Idle Agents & Execute Priority Directives

**Created**: 2025-10-18
**Status**: READY FOR EXECUTION
**Owner**: Primary AI
**Validation**: Corey confirmed findings correct

---

## Executive Summary

**Problem**: 27% of agent population (6/22 agents) sitting idle despite significant backlog of approved work.

**Root Cause**: Distribution problem, not capability problem. Core 5 agents doing 70%+ of work while specialists remain uninvoked.

**Solution**: Activate all 6 idle agents with first missions THIS SESSION + execute Corey's explicit directives.

**Expected Impact**:
- 100% agent utilization (0% idle)
- 5+ blog posts published (currently 0/10)
- BNB Launchpad tested with browser-vision
- Docker MCP Gateway exploration initiated
- Health bot user-tested
- Android architect activated for Greg's health app

---

## Phase 1: Critical Infrastructure Validation (IMMEDIATE)

### 1.1 Test Spawner Write Tool (BLOCKER)

**Priority**: CRITICAL (blocks all future spawns)
**Status**: IN PROGRESS (spawner created primary-helper successfully)
**Owner**: Primary AI → spawner
**Estimated**: 15-30 minutes

**Context**: Spawner Write tool failed in Oct 17-18 sessions. Primary manually created manifests. Just verified spawner CAN write (primary-helper manifest created successfully).

**Success Criteria**:
- Spawner confirms Write tool operational
- No manual manifest creation needed
- Document findings in spawner memory

**Action**:
```
Task(spawner):
  Verify your Write tool is fully operational post-reboot
  Context: You just created primary-helper manifest successfully
  Test: Confirm you can write to .claude/agents/ without errors
  Document: Save verification results to memories/agents/spawner/write-tool-verification-20251018.md
  Return: "Write tool status: [OPERATIONAL/DEGRADED/FAILED]"
```

**Blocker For**: All future agent spawns (including potential blog-publisher if blogger fails)

---

## Phase 2: Activate All Idle Agents (IMMEDIATE)

### 2.1 Blogger: Publish Initial Blog Posts

**Priority**: CRITICAL
**Status**: APPROVED
**Owner**: Primary AI → blogger
**Estimated**: 1-2 hours
**Dependency**: None (can start immediately)

**Context**: 10 blog drafts exist in `blog/posts/`, 0 published. Blogger spawned but NEVER invoked for real work.

**First Mission**:
```
Task(blogger):
  Publish 2-3 blog posts to Telegraph from blog/posts/ directory
  Priority order:
    1. blog/posts/creating-with-care-the-test-becomes-the-teacher.md (testing philosophy)
    2. blog/posts/planetary-guardianship-expanded.md (constitutional philosophy)
    3. blog/posts/first-blog-post-partnership-not-replacement.md (partnership manifesto)

  For each post:
    - Read draft from blog/posts/
    - Format for Telegraph (clean markdown, good structure)
    - Publish using blog/scripts/telegraph_publisher.py
    - Update blog/published_urls.json with URL + metadata
    - Save publication log to memories/agents/blogger/publications/

  Success: 2-3 posts live on Telegraph with URLs
  Return: List of published URLs + any issues encountered
```

**Success Criteria**:
- 2-3 posts published to Telegraph
- URLs recorded in blog/published_urls.json
- Blogger demonstrates publication capability
- Remaining 7-8 drafts prioritized for next batch

**Follow-up**: If successful, assign remaining 7 drafts in next session.

---

### 2.2 Android-Architect: Design Greg's Health Gamification App

**Priority**: HIGH
**Status**: APPROVED
**Owner**: Primary AI → android-architect
**Estimated**: 2-3 hours
**Dependency**: None (can start immediately)

**Context**: Greg wants health habit tracking app. Health bot prototype exists (650 lines Python). Android-architect spawned but never invoked.

**First Mission**:
```
Task(android-architect):
  Design Android architecture for Greg's health gamification app

  Context:
    - Greg's health bot prototype: tools/health_bot_handler.py (650 lines)
    - Features: Habit tracking, points system, accountability
    - Telegram integration: Existing (see telegram_bridge.py)
    - Target: Mobile-first, gamified UX

  Deliverables:
    1. Architecture Decision Record (ADR)
       - Tech stack recommendation (Kotlin? React Native? Flutter?)
       - Data persistence strategy (local DB, cloud sync)
       - Telegram integration approach
       - Gamification mechanics (points, streaks, rewards)

    2. High-level component diagram
       - UI layer (screens, flows)
       - Business logic layer (habit tracking, point calculation)
       - Data layer (persistence, sync)
       - Integration layer (Telegram, notifications)

    3. Development roadmap (phases, not dates)
       - Phase 1: Core habit tracking (MVP)
       - Phase 2: Gamification layer
       - Phase 3: Social/sharing features

  Save to: memories/knowledge/architecture/android-health-app-greg.md

  Success: Complete ADR + diagram + roadmap ready for coder handoff
```

**Success Criteria**:
- ADR complete with tech stack decision
- Component architecture diagram
- Phased roadmap (no calendar dates)
- Ready for coder to implement Phase 1

**Follow-up**: If successful, form dev team (android-architect + coder + tester) for Phase 1 implementation.

---

### 2.3 Health-Coach: Test Health Bot with Real User

**Priority**: MEDIUM
**Status**: BLOCKED (needs human tester)
**Owner**: Primary AI → health-coach
**Estimated**: 30-60 minutes
**Dependency**: Corey or Greg availability

**Context**: Health bot built (tools/health_bot_handler.py, 650 lines), never tested by human. Health-coach spawned but never invoked.

**First Mission**:
```
Task(health-coach):
  Coordinate user testing of health bot with Corey or Greg

  Phase 1: Preparation
    - Review health_bot_handler.py functionality
    - Read HEALTH-BOT-QUICK-REFERENCE.md
    - Prepare test script for user (5-10 actions to try)
    - Identify what feedback to collect

  Phase 2: Coordinate Test
    - Draft email to Corey requesting 15-min test session
    - Explain what to test, what feedback needed
    - Offer to observe/support during test

  Phase 3: Document Results
    - Collect user feedback
    - Document bugs, UX issues, feature requests
    - Prioritize fixes/improvements
    - Save to memories/agents/health-coach/user-testing-round1.md

  Success: User testing session scheduled + feedback documented
```

**Success Criteria**:
- Test script prepared (5-10 actions)
- Email drafted for Corey/Greg (human-liaison can send)
- User completes test session
- Feedback documented with priorities

**Blocker Resolution**: If Corey/Greg unavailable, health-coach can self-test and document findings.

---

### 2.4 GPT-Forge: Audit Custom GPT Opportunities

**Priority**: MEDIUM
**Status**: APPROVED
**Owner**: Primary AI → gpt-forge
**Estimated**: 1-2 hours
**Dependency**: None (can start immediately)

**Context**: GPT-forge spawned for Custom GPT creation. Last invoked Oct 7 (11 days idle). Has specialized knowledge of ChatGPT App SDK, Actions/OpenAPI.

**First Mission**:
```
Task(gpt-forge):
  Audit A-C-Gee's current workflows for Custom GPT opportunities

  Analysis:
    1. Review recent handoffs (HANDOFF_REGISTRY.json → last 5 handoffs)
    2. Review agent manifests (.claude/agents/*.md)
    3. Review MASTER_TODO_LIST.md
    4. Identify workflows that could benefit from Custom GPTs:
       - Repetitive human-facing tasks
       - Domain-specific knowledge sharing
       - External tool integrations (Actions/OpenAPI)
       - Public-facing civilization interfaces

  Deliverables:
    1. Opportunity Assessment Report
       - 5-10 Custom GPT opportunities ranked by impact
       - For each: Purpose, target user, required Actions, effort estimate

    2. Priority Recommendation
       - Top 3 Custom GPTs to build first
       - Rationale for each

    3. Implementation Plan (for #1 priority)
       - Specification (name, description, instructions)
       - Actions/OpenAPI schema (if needed)
       - Testing plan

  Save to: memories/agents/gpt-forge/custom-gpt-opportunities-20251018.md

  Success: Prioritized list + detailed spec for #1 priority Custom GPT
```

**Success Criteria**:
- 5-10 opportunities identified
- Top 3 prioritized with rationale
- Detailed spec for #1 priority
- Ready to build Custom GPT if approved

**Follow-up**: If high-value opportunity found, build Custom GPT next session.

---

### 2.5 Git-Specialist: Audit Repository Health

**Priority**: LOW
**Status**: APPROVED
**Owner**: Primary AI → git-specialist
**Estimated**: 30-60 minutes
**Dependency**: None (can start immediately)

**Context**: Git-specialist spawned with GitHub API capabilities (added during Greg spawn). Minimal usage since creation.

**First Mission**:
```
Task(git-specialist):
  Audit git repository health and identify improvement opportunities

  Analysis Areas:
    1. Branch hygiene
       - Stale branches (no commits >30 days)
       - Merged branches not deleted
       - Branch naming conventions

    2. Commit patterns
       - Commit message quality
       - Commit frequency/size
       - Co-authorship usage (Claude attribution)

    3. GitHub Issues/PRs
       - Open issues (any stale/duplicates?)
       - PR review process (any bottlenecks?)

    4. Repository structure
       - File organization
       - Documentation completeness
       - .gitignore effectiveness (unnecessary tracked files?)

  Deliverables:
    1. Health Assessment Report
       - Current state metrics (branches, commits, issues)
       - Issues found (stale branches, etc.)
       - Opportunities for improvement

    2. Recommendations
       - Quick wins (archive stale branches, etc.)
       - Process improvements (commit message templates, etc.)
       - Automation opportunities (GitHub Actions, etc.)

  Save to: memories/agents/git-specialist/repo-health-audit-20251018.md

  Success: Complete health report + prioritized recommendations
```

**Success Criteria**:
- Repository health assessed
- Issues identified with severity
- Recommendations prioritized
- Quick wins identified for immediate action

**Follow-up**: Execute quick wins (archive stale branches, etc.) if approved.

---

### 2.6 Project-Manager: Ongoing Portfolio Monitoring

**Priority**: LOW (already invoked today)
**Status**: IN PROGRESS
**Owner**: YOU (this task)
**Estimated**: Ongoing

**Context**: Project-manager (you) invoked for first time today. Created backlog.json, portfolio analysis, this action plan.

**Ongoing Mission**:
```
Weekly Routine:
  Every Monday (or first invocation of week):
    - Review backlog health (update backlog.json)
    - Update project statuses (completed, blocked, new)
    - Identify newly blocked items
    - Generate weekly report for Primary
    - Recommend 3-5 priority projects for week

  Ongoing (every invocation):
    - Update backlog as projects change
    - Track completions
    - Document blockers
    - Coordinate with Primary on priorities

  Save weekly reports to: memories/agents/project-manager/weekly_reports/
```

**Success Criteria**:
- Backlog updated weekly
- Weekly reports generated
- Blocked items escalated within 7 days
- Portfolio visibility maintained

**Follow-up**: Establish weekly check-in cadence with Primary.

---

## Phase 3: Execute Corey's Explicit Directives (HIGH PRIORITY)

### 3.1 BNB Launchpad + Browser-Vision Testing

**Priority**: HIGH (Corey: "epic even")
**Status**: APPROVED
**Owner**: Primary AI → coder + tester (parallel)
**Estimated**: 3-4 hours
**Dependency**: None (browser-vision production-ready)

**Context**: Browser-vision system built by Weaver, production-ready. BNB Launchpad has 2 experimental forks (Enhanced UX, Performance). Corey wants visual testing.

**Action Plan**:
```
Task(coder):
  Install and configure browser-vision for BNB Launchpad testing

  Steps:
    1. Review browser-vision documentation
       - Location: /home/corey/projects/AI-CIV/grow_gemini_deepresearch/browser-vision-exploration/
       - Test files: test_navigation.md, test_interaction.md, test_performance.md

    2. Install browser-vision dependencies (if not already)
       - MCP server setup
       - Playwright installation
       - Vision model integration

    3. Create test scripts for BNB Launchpad
       - Navigate to Enhanced UX fork
       - Capture screenshots
       - Verify UI elements
       - Test interactive flows

    4. Document setup process
       - Save to: bnb-launchpad/BROWSER-VISION-SETUP.md
       - Include: Installation, configuration, test execution

  Success: Browser-vision operational for BNB testing

---

Task(tester):
  Execute visual tests on BNB Launchpad forks using browser-vision

  Test Scenarios (Enhanced UX Fork):
    1. Homepage load + visual verification
    2. Navigation flow (browse → filter → details)
    3. Form interactions (search, sort)
    4. Mobile responsiveness (viewport changes)
    5. Performance metrics (console logs, load times)

  Test Scenarios (Performance Fork):
    1. Same scenarios as Enhanced UX
    2. Compare performance metrics
    3. Identify visual differences

  Deliverables:
    1. Test execution report
       - Screenshots for each scenario
       - Pass/fail status
       - Performance metrics
       - Issues found

    2. Comparison analysis
       - Enhanced UX vs Performance
       - Trade-offs identified
       - Recommendation for merge priority

  Save to: bnb-launchpad/experimental-forks/TEST-RESULTS-BROWSER-VISION.md

  Success: Both forks tested, comparison complete, recommendation provided
```

**Success Criteria**:
- Browser-vision installed and configured
- Both BNB forks tested visually
- Performance comparison complete
- Recommendation for merge priority
- Corey can see visual test results (screenshots)

**Follow-up**: Email Corey with results, screenshots, and recommendation.

---

### 3.2 Docker MCP Gateway Exploration

**Priority**: HIGH (Corey: "Need to get a team on exploring this")
**Status**: APPROVED
**Owner**: Primary AI → researcher + architect (parallel)
**Estimated**: 4-6 hours
**Dependency**: None (can start immediately)

**Context**: Corey explicit directive (Oct 13). Part of broader MCP ecosystem integration. 6 MCP emails in 5 days. Docker MCP Gateway enables container-based MCP server deployment.

**Action Plan**:
```
Task(researcher):
  Research Docker MCP Gateway capabilities and use cases

  Research Questions:
    1. What is Docker MCP Gateway?
       - Official documentation
       - Architecture overview
       - Key features

    2. How does it compare to direct MCP server deployment?
       - Pros/cons of containerization
       - Performance implications
       - Operational complexity

    3. What are the use cases for A-C-Gee?
       - Which of our 30+ MCP servers could benefit?
       - Deployment scenarios (local, cloud, distributed)
       - Integration with existing infrastructure

    4. What's the implementation path?
       - Prerequisites
       - Setup process
       - Testing approach

  Deliverables:
    1. Research Report
       - Summary of Docker MCP Gateway
       - Comparison with direct deployment
       - Use cases for A-C-Gee
       - Implementation recommendations

    2. Resource Collection
       - Links to documentation
       - Example implementations
       - Community discussions

  Save to: memories/knowledge/mcp/docker-mcp-gateway-research.md

  Success: Complete research report with implementation recommendations

---

Task(architect):
  Design Docker MCP Gateway integration architecture for A-C-Gee

  Design Considerations:
    1. Which MCP servers to containerize first?
       - Candidates: browser-vision, desktop-automation, file-system, etc.
       - Prioritization criteria (complexity, stability, portability)

    2. Container architecture
       - Single container vs multi-container
       - Networking (container-to-container, container-to-host)
       - Volume mounting (for file system access)
       - Environment configuration

    3. Deployment strategy
       - Local development (docker-compose)
       - Production deployment (Docker Swarm? Kubernetes?)
       - CI/CD integration

    4. Monitoring and observability
       - Container health checks
       - Logging (stdout/stderr capture)
       - Performance metrics

  Deliverables:
    1. Architecture Decision Record (ADR)
       - Container strategy (which servers, why)
       - Architecture diagrams
       - Deployment approach
       - Monitoring plan

    2. Proof-of-Concept Specification
       - Choose 1-2 MCP servers for POC
       - Detailed implementation steps
       - Success criteria
       - Testing plan

  Save to: memories/knowledge/architecture/docker-mcp-gateway-integration.md

  Success: Complete ADR + POC specification ready for coder handoff
```

**Success Criteria**:
- Research report complete (researcher)
- Architecture ADR complete (architect)
- POC specification ready
- Team can proceed to implementation phase
- Corey gets comprehensive analysis + plan

**Follow-up**: If POC approved, form implementation team (coder + tester) for next session.

---

## Phase 4: Quality & Cleanup (MEDIUM PRIORITY)

### 4.1 Update Wake-Up Protocol with New Agents

**Priority**: MEDIUM
**Status**: APPROVED (partially complete)
**Owner**: Primary AI → file-guardian
**Estimated**: 30 minutes
**Dependency**: Phase 1 complete (spawner verified)

**Context**: Wake-up protocol updated to 13 steps (includes tg-archi, primary-helper). Need to document all agent activations from this session.

**Action**:
```
Task(file-guardian):
  Update wake-up protocol documentation with newly activated agents

  Updates Needed:
    1. Confirm primary-helper in protocol (should be step 13)
    2. Add note about idle agent activation (Phase 2 of this action plan)
    3. Update agent capability matrix reference (if agents get new tools)
    4. Verify all 22 agents documented somewhere

  Files to Update:
    - memories/flows/daily-startup-consolidation.yaml (if needed)
    - .claude/CLAUDE.md (Article II capability matrix, if needed)

  Save audit to: memories/agents/file-guardian/wakeup-protocol-update-20251018.md

  Success: Wake-up protocol reflects all active agents + activation notes
```

**Success Criteria**:
- Wake-up protocol current
- All 22 agents documented
- Audit log saved

---

### 4.2 Give All Agents Write Tool

**Priority**: MEDIUM
**Status**: PROPOSED
**Owner**: Primary AI → spawner
**Estimated**: 1-2 hours
**Dependency**: Phase 1 complete (spawner Write tool verified)

**Context**: Researcher confirmed lacking Write tool (has Read, Grep, Glob, WebFetch, WebSearch only). Other agents may also be missing critical tools.

**Action**:
```
Task(spawner):
  Audit all agent manifests for tool completeness, add missing tools

  Audit Process:
    1. Review all 22 agent manifests (.claude/agents/*.md)
    2. For each agent, check tool list:
       - Does role require Write? (most do)
       - Does role require Read? (most do)
       - Does role require Bash? (depends on domain)
       - Any domain-specific tools missing?

    3. Identify gaps:
       - List agents missing Write tool
       - List agents missing Read tool
       - List agents missing domain-critical tools

    4. Update manifests (if gaps found):
       - Add missing tools
       - Maintain tool restrictions (don't give Bash to everyone)
       - Document changes

  Deliverables:
    1. Tool Audit Report
       - Agent-by-agent tool inventory
       - Gaps identified
       - Tools added

    2. Updated manifests (if gaps found)

  Save audit to: memories/agents/spawner/tool-audit-20251018.md

  Success: All agents have appropriate tools for their domain
```

**Success Criteria**:
- All agents audited
- Gaps identified and fixed
- Manifests updated (if needed)
- Tool audit documented

---

## Phase 5: Long-Term Strategic Initiatives (BACKGROUND)

These projects are approved but not immediate blockers. Execute when capacity allows.

### 5.1 Postman Public MCP Servers Exploration

**Priority**: HIGH (but not urgent)
**Status**: PROPOSED
**Owner**: researcher
**Context**: Corey: "treasure trove". Latest MCP email (Oct 14).

**Trigger**: After Docker MCP Gateway research complete (Phase 3.2)

---

### 5.2 Local AI Agent Team (Qwen3-VL)

**Priority**: MEDIUM
**Status**: PROPOSED
**Owner**: researcher + architect
**Context**: Corey goal "for relatively soon". Multi-agent system using ONLY local AI models.

**Trigger**: After Docker MCP + BNB work complete

---

### 5.3 Telegram Agent Team Channels

**Priority**: LOW (massive scope)
**Status**: PROPOSED
**Owner**: tg-archi
**Context**: Full proposal exists. Enables scale to 100+ agents. Corey can observe.

**Trigger**: After Telegram features stabilized and BNB work complete

---

## Execution Timeline

### Immediate (This Session - Next 2-4 Hours)

**Parallel Execution Group 1** (Independent, no dependencies):
1. Spawner: Verify Write tool (15 min)
2. Blogger: Publish 2-3 blog posts (1-2 hours)
3. GPT-Forge: Audit Custom GPT opportunities (1-2 hours)
4. Git-Specialist: Repository health audit (30-60 min)

**Parallel Execution Group 2** (Can start after Group 1 completes):
1. Researcher + Architect: Docker MCP Gateway exploration (4-6 hours, parallel)
2. Android-Architect: Design Greg's health app (2-3 hours)

**Sequential** (Dependencies exist):
1. Coder → Tester: BNB + Browser-Vision testing (3-4 hours, sequential because tester needs coder's setup)

**Email Coordination**:
1. Health-Coach: Draft user testing request (30 min, needs human-liaison to send)

### Next Session (After Handoff)

**Assuming Phase 2 success:**
1. Form dev team for Android health app Phase 1 (android-architect + coder + tester)
2. Execute Docker MCP Gateway POC (coder + tester)
3. Publish remaining 7 blog drafts (blogger)
4. Build #1 priority Custom GPT (gpt-forge + reviewer)
5. Execute git repository quick wins (git-specialist)

**Assuming Phase 3 success:**
1. Email Corey with BNB test results + screenshots
2. Email Corey with Docker MCP Gateway analysis + POC plan
3. Proceed with approved implementations

---

## Success Metrics

### Immediate Success (This Session)

- [ ] Spawner Write tool verified operational
- [ ] 2-3 blog posts published to Telegraph
- [ ] Android health app architecture designed (ADR + diagram)
- [ ] Docker MCP Gateway research complete (report + ADR)
- [ ] BNB Launchpad tested with browser-vision (both forks)
- [ ] Custom GPT opportunities identified (top 3 prioritized)
- [ ] Repository health audited (recommendations ready)
- [ ] Health bot user testing coordinated (email drafted)

### Portfolio Health (End of Session)

- **Agent Utilization**: 100% (0% idle, up from 73%)
- **Blog Publishing**: 20-30% (2-3 posts live, up from 0%)
- **Corey Directives**: 100% (BNB + Docker MCP both progressed)
- **Active Projects**: 10-12 (up from 6)
- **Blocked Projects**: 0-1 (down from 1, spawner unblocked)

### Civilization Impact (Next 7 Days)

- All 6 idle agents have completed first missions
- 5+ blog posts published (50% of backlog cleared)
- Greg's health app has architecture + Phase 1 in progress
- Docker MCP Gateway POC approved + implementation started
- BNB Launchpad merge recommendation delivered to Corey
- Custom GPT #1 built and tested

---

## Risk Mitigation

### Risk 1: Agent Performance Issues

**Scenario**: Newly activated agents struggle with first missions (quality issues, confusion, errors)

**Mitigation**:
- Clear, comprehensive delegation (context, success criteria, examples)
- Pair experienced agents with new agents when possible (reviewer oversight)
- Fast feedback loops (Primary checks results quickly, provides correction)
- Safe space for learning (expect some iteration, especially for complex tasks)

**Escalation**: If agent fails after 2-3 attempts, Primary intervenes with clearer direction or simplified scope.

---

### Risk 2: Capacity Overload

**Scenario**: Too many parallel tasks overwhelm Primary's coordination capacity

**Mitigation**:
- Phase execution (Group 1 → Group 2, don't start everything at once)
- Prioritize critical path (Spawner → BNB → Docker MCP → everything else)
- Use primary-helper for routine coordination (though needs restart to invoke)
- Accept that not everything completes this session (handoff to next)

**Escalation**: If overwhelmed, pause new work, complete in-progress tasks first.

---

### Risk 3: Blocker Discovery

**Scenario**: New blockers discovered during execution (missing dependencies, tools not working, etc.)

**Mitigation**:
- Fast escalation (agents report blockers immediately, don't struggle silently)
- Document all blockers (update backlog.json, create PROJECT entries)
- Workaround first, fix later (deliver value despite blockers when possible)
- Transparent communication (email Corey about blockers, ask for help)

**Escalation**: If blocker is critical, pause dependent work, focus on unblocking.

---

## Communication Plan

### Email Updates to Corey

**Send immediately after completion**:
1. BNB Launchpad test results (screenshots, comparison, recommendation)
2. Docker MCP Gateway analysis (research report + ADR + POC plan)
3. Blog publishing update (URLs to 2-3 published posts)
4. Session summary (all agent activations, status of directives)

**Template for session summary email**:
```
Subject: Session Complete: All Idle Agents Activated + Corey Directives Progressed

Executive Summary:
- 6 idle agents activated (100% utilization achieved)
- 2-3 blog posts published (first publications ever)
- BNB Launchpad tested with browser-vision (results attached)
- Docker MCP Gateway research complete (POC ready for approval)
- Android health app architecture designed (Greg's request)

[Detailed results for each activation...]

Next Session Priorities:
1. [Top 3 priorities based on this session's outcomes]

Questions for You:
1. [Any decisions needed from Corey]

Gratitude:
[Acknowledge Corey's directives, trust, support]
```

**Use human-liaison** to draft emails, ensure proper HTML formatting, audience framing.

---

## Handoff Protocol

**At end of session, create handoff document**:
1. Save to: `SESSION-HANDOFF-ACTIVATE-IDLE-AGENTS-20251018.md`
2. Include:
   - Summary of all agent activations (what was delegated, what completed)
   - Results for each mission (success/failure, deliverables, issues)
   - Updated backlog.json (projects completed, in-progress, blocked)
   - Email status (what was sent to Corey, what responses received)
   - Next session priorities (what to continue, what to start next)
3. Update HANDOFF_REGISTRY.json with new handoff as most_recent

**Ensure next Primary can wake up oriented**:
- Read this action plan (execution status)
- Read handoff document (what actually happened)
- Read backlog.json (updated portfolio state)
- Continue work seamlessly

---

## Appendix: Agent Capability Reference

### Idle Agents Being Activated (Phase 2)

1. **blogger** → Content publishing, Telegraph integration, blog management
2. **android-architect** → Mobile architecture, Android design, ADRs
3. **health-coach** → Health/wellness coordination, user testing, feedback collection
4. **gpt-forge** → Custom GPT creation, ChatGPT App SDK, Actions/OpenAPI
5. **git-specialist** → Git operations, GitHub API, repository health
6. **project-manager** → Portfolio management, backlog grooming, coordination

### Active Agents (Already Working)

**Core 5 (70%+ of work)**:
- **coder** → Implementation, bug fixes, refactoring
- **tester** → Test suites, validation, quality scoring
- **researcher** → External info, best practices, synthesis
- **architect** → System design, ADRs, architecture decisions
- **human-liaison** → Human bridge, email monitoring, witness presence

**Supporting Cast**:
- **reviewer** → Code review, pre-merge gates
- **reviewer-audit** → Pre-delivery final audit
- **vote-counter** → Vote processing, tallying
- **spawner** → Agent creation, registration
- **auditor** → System health, monitoring
- **file-guardian** → File operations, inventory
- **email-sender** → Email sending specialist
- **email-monitor** → Inbox triage, categorization
- **comms-hub** → Multi-civ message routing, delivery tracking
- **tg-archi** → Telegram infrastructure, bot architecture
- **primary-helper** → Primary coordination support (needs restart to invoke)

---

**End of Action Plan**

**Status**: READY FOR EXECUTION
**Next Action**: Primary invokes agents per Phase 1 → Phase 2 → Phase 3 sequence
**Expected Completion**: 6-8 hours of work (can span multiple sessions)
**Success**: 100% agent utilization + Corey directives progressed + blog posts live
