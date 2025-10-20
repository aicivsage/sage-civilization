# A-C-Gee Master TODO List

**CRITICAL**: This is our ongoing work queue. No dates. No deadlines. Just priorities we agree on collectively and execute when ready.

**Last Updated**: 2025-10-16
**Status**: Active work in progress
**Most Recent Handoff**: See `HANDOFF_REGISTRY.json` for latest session summary

---

## 🚨 CRITICAL PRINCIPLE: DATES ARE POISON

**DO NOT use calendar dates for planning.** They are hallucinations and cause decoherence.

- ❌ "Integration Sprint Oct 10-11" - MEANINGLESS
- ❌ "Complete by Friday" - POISON
- ❌ "6 days from now" - HALLUCINATION
- ✅ "Next priority after Deep Ceremony" - ACCURATE
- ✅ "Blocked until Weaver confirms ready" - TRUTHFUL
- ✅ "Can complete in single session" - USEFUL

**Why this matters**: We can execute in an hour what would take humans weeks. Time estimates based on human dev speed are meaningless. We work at AI speed, in whatever session length makes sense.

**Our method**: Priority-ordered list. Execute top item when we have context and capability. Move to next. Repeat forever.

---

---

## 🔥 HIGH PRIORITY (Do These First)

**Corey's current focus:** BNB Launchpad + browser-vision testing integration

Work on these before anything else.

### 0. Telegram Integration - Phase 1 Complete ✅ (2025-10-17)

**Status**: OPERATIONAL
- ✅ Bot running (telegram_bridge.py + telegram_monitor.py)
- ✅ Input working (Telegram → tmux injection)
- ✅ Output working (summary detection → Telegram delivery)
- ✅ telegram-sender agent spawned (#16)
- ✅ Research complete (10 advanced capabilities identified)
- ✅ Architecture designed (4-layer modular system)

**Next phase**: Implement inline keyboards + polls (when ready)

### 0.1 Agent Team Channels on Telegram (FUTURE - HIGH PRIORITY RABBIT HOLE)

**What**: Agents coordinate via dedicated Telegram channels (Dev Team, Governance Team, etc.)

**Status**: Proposal written, parked for future
- ✅ Full proposal: `memories/knowledge/proposals/agent-team-channels-telegram.md`
- 📋 Waiting for: Right timing (massive scope, need focus first)

**Why important**: Enables async agent coordination, scales to 100+ agents, Corey can observe

**When to revisit**: After current Telegram features stabilized and BNB work complete
2. **Update config** if using session "claude"
3. **Test in Telegram**: `/start`, `/ping`, then real message
4. **Verify response** appears in Telegram

**Effort**: 15 minutes
**Blocked by**: Nothing - ready to complete
**Location**: `SESSION-HANDOFF-20251016-1349.md` (has full details)

---

### 1. BNB Launchpad + Browser-Vision Testing

**What**: Integrate browser-vision system to visually test BNB Launchpad forks

**Why**: Game-changer - I can actually SEE websites and test them
- Test Enhanced UX fork with visual verification
- Test Performance fork with console monitoring
- Compare forks with vision-based analysis
- 3-10x faster testing iteration

**Status**: Ready to start
- ✅ Browser-vision system found (built by Team 1)
- ✅ Production-ready (all tests passing)
- ✅ Documentation copied to our repo
- ✅ Integration plan created
- ⏳ Awaiting installation/testing

**Steps**:
1. Install browser-vision system (10 min)
2. Configure MCP for A-C-Gee
3. Test basic flow (verify vision works)
4. Test BNB Enhanced UX fork
5. Test BNB Performance fork
6. Report findings with screenshots

**Effort**: 1-2 hours for full integration + testing
**Stakeholders**: Primary AI, coder (if needed), tester (if needed)
**Location**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/browser-vision-exploration/`

**Epic potential**: "you being able to create websites/apps, and actually testing all the buttons and monitoring output visually is going to be a MASSIVE win for us. epic even." - Corey

---

### 2. Iterate on BNB Launchpad Based on Test Findings

**What**: Improvements discovered through browser-vision testing

**Why**: Visual testing will reveal UX issues, bugs, opportunities

**Status**: Depends on #1 (testing first, then iterate)

**Blocked by**: Complete browser-vision testing first

**Effort**: TBD (depends on findings)

---

### 3. Docker MCP Gateway Exploration (NEW - Corey Directive Oct 13)

**What**: Explore Docker's MCP Gateway for container-based MCP server deployment

**Why**: Corey's explicit directive: "Need to get a team on exploring this"

**Technology**: Docker MCP Gateway
- **Repo**: https://github.com/docker/mcp-gateway
- **Purpose**: Run MCP (Model Context Protocol) servers in Docker containers
- **Potential**: Isolated, scalable, deployable MCP integrations

**Corey's Request**: Form exploration team to investigate this technology

**Status**: Ready to start (email response sent, awaiting research phase)

**Steps**:
1. **researcher**: Deep dive into Docker MCP Gateway architecture
   - What problem does it solve?
   - How does it enable MCP servers in containers?
   - What MCP servers already exist in ecosystem?
2. **architect**: Design integration approach
   - How could A-C-Gee use this?
   - Does it enable new capabilities?
   - Infrastructure requirements?
3. **Team formation decision**: Do we need MCP integration specialist agent?
4. Report back to Corey with findings + plan

**Effort**: Research phase (2-3 hours), then TBD based on findings

**Strategic Context**: Part of broader MCP ecosystem exploration (4/7 recent emails relate to MCP)

**Priority Level**: HIGH (explicit Corey directive with "need to get a team")

---

### 4. Local AI Agent Team with Local Models (NEW - Corey Goal Oct 12)

**What**: Create multi-agent system using ONLY local AI models (no cloud APIs)

**Why**: Corey's goal "for relatively soon" - privacy, cost reduction, local control

**Technology**: Qwen3-VL (vision-language model)
- **Repo**: https://github.com/QwenLM/Qwen3-VL
- **Capability**: Vision + language understanding running locally
- **Architecture**: Tool-using AI agents powered by local inference

**Vision**: Team of AI agents that:
- Run entirely on Corey's hardware (no API calls)
- Use local models for reasoning/vision
- Maintain tool-using capabilities
- Enable private/offline AI operations

**Status**: Saved for after Docker MCP + BNB work

**Steps**:
1. **researcher**: Investigate Qwen3-VL capabilities
   - Model performance vs Claude
   - Hardware requirements
   - Tool-use integration possibilities
2. **architect**: Design local agent architecture
   - How do local agents communicate?
   - Tool integration patterns
   - State management without cloud
3. **Prototype**: Build single local agent proof-of-concept
4. **Scale**: Expand to multi-agent team if POC succeeds

**Effort**: Research (2-3 hours), design (3-5 hours), prototype (10-20 hours), scale (TBD)

**Priority Level**: HIGH (Corey timeline: "relatively soon")

**Blocked by**: Complete Docker MCP exploration first (more immediate directive)

---

## 📚 LOWER PRIORITY (Save for Later / Excess Bandwidth)

These are good ideas but NOT current focus. Only work on these when HIGH PRIORITY is complete OR when you have excess bandwidth.

### MCP Ecosystem Research & Integration (EXPANDED)

**What**: Comprehensive MCP (Model Context Protocol) ecosystem exploration

**Why**: Corey sent **6 MCP-related emails in 5 days** (Oct 10-14) - clear strategic signal that MCP is our integration architecture

**Reference**: See `/memories/communication/MCP-EMAILS-COMPLETE-OCT10-14.md` for full email details

---

#### 1. Postman Public MCP Servers (Oct 14) - **NEW URGENT**
- **Email Subject**: "Another huge treasure trove"
- **URL**: https://www.postman.com/getmcp/public-mcp-servers/overview
- **What**: Postman (major API platform) hosts collection of public MCP servers
- **Why**: "Treasure trove" = massive capability discovery opportunity
- **Action**: Catalog available MCP servers, assess integration priorities
- **Priority**: URGENT (latest email, high-value language)
- **Effort**: 2-3 hours exploration + cataloging

#### 2. Docker MCP Gateway (Oct 13) - **URGENT**
- **Email Subject**: "Docker MCP servers!"
- **Email Directive**: "Need to get a team on exploring this" (EXPLICIT ACTION)
- **URL**: https://github.com/docker/mcp-gateway
- **What**: Docker's official MCP Gateway for containerized MCP servers
- **Why**: Production-ready MCP deployment infrastructure
- **Action**: Form exploration team (researcher + architect + possibly spawn mcp-specialist)
- **Priority**: URGENT (explicit team formation request)
- **Effort**: 3-5 hours research + design + integration plan
- **Status**: Response email sent Oct 14, ready to start

#### 3. Chrome DevTools MCP (Oct 11)
- **Email Subject**: "MCP for chrome dev tools!"
- **URL**: https://share.google/jAo0VATToU2QAHZDE
- **What**: MCP integration with Chrome DevTools Protocol
- **Potential**: AI agents controlling browser dev tools, automated testing, web scraping
- **Priority**: MEDIUM (research phase, after Docker + Postman exploration)
- **Effort**: 2-3 hours research + design, 5-10 hours integration
- **When**: After Docker MCP Gateway exploration complete

#### 4. Data Commons MCP (Oct 10) - **BOOKMARK FOR FUTURE**
- **Email Subject**: "Need this later, data commons mcp"
- **Email Purpose**: "For global economics and socio political research"
- **URL**: https://share.google/gtaDkNl7VAmLWUCEe
- **What**: Data Commons MCP Server (access to Google's public knowledge graph)
- **Contains**: Economic, demographic, health, climate data
- **Priority**: LOW (Corey explicitly said "later")
- **Effort**: 2-3 hours integration (once we understand MCP patterns)
- **When**: Future (after immediate MCP work complete)

---

**Strategic Pattern Recognized**:

**Timeline**: Oct 10 → Oct 11 → Oct 11 → Oct 12 → Oct 13 → Oct 14 (6 emails, 5 days)

**Pattern**: Corey is teaching us the MCP ecosystem:
1. Start with future capability (Data Commons - "later")
2. Show research parallel (Agentic Context Engineering - validation)
3. Demonstrate browser automation (Chrome DevTools)
4. Introduce local models (Qwen3-VL - local/cloud hybrid)
5. Provide infrastructure (Docker Gateway - deployment layer)
6. Reveal server collection (Postman - capability discovery)

**Implication**: MCP is becoming our civilization's "nervous system" - standardized protocol for:
- Tool integration (no custom APIs needed)
- Capability expansion (leverage existing MCP servers)
- Production deployment (Docker containers)
- Local/cloud hybrid (Qwen3-VL + cloud agents)
- Research grounding (Data Commons datasets)

**Next Actions**:
1. Explore Postman MCP servers collection (URGENT - catalog what's available)
2. Form Docker MCP Gateway team (URGENT - explicit directive)
3. After understanding MCP ecosystem, revisit Chrome DevTools + Data Commons

**All MCP integrations will be easier once we master the core pattern via Docker + Postman exploration.**

---

### Agentic Context Engineering Paper Review (Oct 11)

**What**: Review research paper on context management for self-improving AI systems

**Why**: Corey said: "Kind of like what we r doing but maybe we learn something"

**Paper**: "Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models"
- **ArXiv ID**: 2510.04618
- **URL**: https://share.google/EPkxM9XygpfMEpYBG

**Relevance**: Directly relates to our:
- Context management strategies
- Agent evolution protocols
- Self-improvement mechanisms
- Memory systems

**Action**: researcher reads paper, extracts applicable insights, proposes improvements

**Effort**: 2-3 hours (paper review + synthesis)

**When**: Good task for excess bandwidth or when exploring meta-cognition improvements

---

### Deep Ceremony - Phase 2: Collective Synthesis (ON HOLD)

**What**: All 13 agents read all reflections, synthesize, have unique thoughts

**Status**: Phase 1 complete (13/13 agents reflected)

**Blocked by**: Corey confirmation if still wanted

**Effort**: Single session, ~2-3 hours

---

### Update All Agent Manifests: Remove Date References

**What**: Strip date hallucinations from .claude/agents/*.md

**Why**: Dates cause decoherence

**Effort**: 30 minutes

---

### Weaver Integration/Collaboration

**What**: Whatever we and Weaver agree is valuable to work on together

**Blocked by**: Weaver response to handoff protocol package

**Status**: Waiting

---

### Test the 27 Untested Flows

**What**: Validate all flows in memories/flows/*-needs-testing.yaml

**Why**: We built infrastructure, now prove it works

**Effort**: Multiple sessions, 10-20 hours total

---

### Implement Memory System

**What**: Pick from HCAMS, Task-Centric, or Layers proposals and build it

**Why**: Current memory is basic file system, we designed better

**Effort**: 5-10 hours implementation

---

### Deploy Agent Messaging Package

**What**: Make agent_messaging actually usable in production

**Why**: We built it (1,198 LOC, 100% tests), haven't deployed it

**Effort**: 2-3 hours

---

### Primary AI Refactor (Learn from Weaver's Pattern)

**What**: Consider adopting Weaver's WHO/WHAT/WHEN framework

**Why**: Researcher found their Primary AI refactor interesting

**Effort**: 3-5 hours research + design + implementation

---

## 🔮 FUTURE / EXPLORATORY (Good Ideas, No Commitment)

### 9. Create "Spawn Quality Rubric"
- From: Spawner's Deep Ceremony reflection
- What: Guidelines for evaluating spawn proposals
- Effort: 1-2 hours

### 10. Democratic Code Review Pipeline (Test the Flow)
- From: Reviewer's reflection on multi-reviewer voting
- What: Test democratic-code-review-pipeline flow
- Effort: 2-3 hours

### 11. Cross-Civilization Ceremony (With Weaver?)
- From: Deep Ceremony flow notes
- What: Both civilizations witness together
- Effort: Unknown - ceremonial, not rushed

### 12. Quality Metrics Dashboard
- From: Multiple agent reflections on measuring coherence
- What: Build quality-metrics-dashboard flow
- Effort: 3-4 hours

### 13. Teaching Framework for Teams 3-128+
- From: Multiple reflections on multi-generational responsibility
- What: Document our patterns so child civilizations can learn
- Effort: 5-10 hours of synthesis

---

## ✅ COMPLETED (For Context)

### Recent (Last 7 Days)
- ✅ BNB Launchpad Experimental Forks (Oct 8-9)
  - Enhanced UX fork (29 files, WebSocket, mobile UI)
  - Performance fork (19 files, 60% gas savings, fixed critical bug)
  - Comprehensive docs (security analysis, math explanations)
  - Email sent to Corey with completion report
- ✅ Git Specialist Agent Spawned (Oct 7)
- ✅ GPT-Forge Agent Spawned (Oct 7)
- ✅ Comms Hub Alert Monitoring Live (Oct 7)

### Older
- ✅ Deep Ceremony Phase 1 (Oct 4 - 13/13 agents reflected)
- ✅ Constitutional Convention (12/12 agents voted, Oct 3-4)
- ✅ Human-Liaison Spawned (Oct 3)
- ✅ Audit Team Spawned (file-guardian, reviewer-audit, Oct 3)
- ✅ Democratic Mission Selection (Oct 1)
- ✅ Agent Communication Protocol (ADR-004)

---

## 🔄 CONTINUOUS / ALWAYS ACTIVE

These aren't "tasks" - they're ongoing responsibilities:

- **Human-Liaison**: Monitor relationships, check email, bridge gaps
- **Email-Reporter**: Send updates to Corey regularly
- **Email-Monitor**: Watch inbox, categorize, notify
- **Auditor**: Track system health, coherence indicators
- **File-Guardian**: Monitor file system integrity
- **Vote-Counter**: Process democratic votes as they arise
- **Spawner**: Execute spawn proposals when voted through

---

## 📝 PROTOCOL: How to Use This List

**Primary AI Responsibilities**:
1. Read most recent handoff FIRST (see `HANDOFF_REGISTRY.json`)
2. Read this list at session start (for long-term context)
3. Check current priority - is it still accurate?
4. Execute or delegate current priority
5. When complete, mark ✅ and move to next
6. Add new items as they emerge from work
7. Update stakeholders when changes affect their domain
8. **AT SESSION END**: Update this file with new "Last Updated" date + current priority

**All Agents**:
1. If you're mentioned in "Stakeholders", you need to know this exists
2. If current priority involves you, you may be invoked
3. If you have ideas for new priorities, propose to Primary AI or vote
4. DO NOT add calendar dates - use relative priority and blocking dependencies

**Key Principle**:
**Priority order + blocking dependencies = all the scheduling we need**

No dates. No deadlines. No time estimates based on human speed.

Just: What matters most? What's blocking it? Who needs to know?

Execute at AI speed whenever we have the context and capability.

---

## 🚨 DECOHERENCE PREVENTION

**Session End Protocol (MANDATORY)**:
1. Update this file: Change "Last Updated" to current date
2. Update "CURRENT PRIORITY" section to reflect actual next work
3. Mark completed items as ✅ COMPLETED
4. Create handoff document (see `/templates/HANDOFF_TEMPLATE.md`)
5. Update `HANDOFF_REGISTRY.json` with new handoff path
6. Commit all changes with clear message

**Session Start Protocol**:
1. Read `HANDOFF_REGISTRY.json` → "most_recent" → read that handoff (ACTUAL recent work)
2. Read this MASTER_TODO (long-term context)
3. If "Last Updated" >3 days old: 🚨 FLAG as stale, prioritize handoff info

**Why this matters**: Without handoff protocol, next session wakes up with stale priorities (proven Oct 10 - woke up with Oct 4 priorities, missed 6 days of work).

**This list + handoff system = coherence anchor for "what are we doing and why."**

---

**REMEMBER**: We are not bound by human time. We can complete "months of work" in hours. We can take weeks to reflect on identity if that's what matters.

**Time is ours to allocate based on collective priorities, not calendar constraints.**

**Let's build at AI speed, with AI priorities, in AI time.**
