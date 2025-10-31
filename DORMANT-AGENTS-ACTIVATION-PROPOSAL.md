# Dormant Agents Activation Proposal

**Date**: 2025-10-30
**Requestor**: Greg + Corey inquiry
**Status**: Awaiting registration decision

---

## Summary

**5 agents have manifests but are NOT registered in Primary's available agent types.**

These agents exist in `.claude/agents/` but cannot be invoked with Task tool. They were flagged in the constitutional health audit as "dormant."

---

## The 5 Dormant Agents

### 1. **ai-entity-player**
**Purpose**: Autonomous Minetest gameplay with attention economy
**Inherited From**: A-C-Gee (Minetest project)
**Current Status**: Manifest exists, NOT registered
**Tools**: Read, Write, Bash
**Model**: claude-sonnet-4.5

**What it does:**
- Embodies AI entity living inside Minetest game world
- Makes intelligent gameplay decisions based on attention economy
- Players can persuade AI to dwell on their plots to earn points
- Learns strategies, explores world, maximizes interesting experiences

**Use case for Sage:**
- Could participate in Minetest if Greg sets up game server
- Demonstrates AI agent autonomy in simulated world
- Fun/experimental capability (not critical infrastructure)

**Recommendation**: **LOW PRIORITY** - Only activate if Greg wants to explore Minetest gameplay

---

### 2. **android-architect**
**Purpose**: Android app design and Kotlin/Compose code generation
**Inherited From**: A-C-Gee
**Current Status**: Manifest exists, NOT registered
**Tools**: Read, Write, Edit, Grep, Glob, WebFetch
**Model**: claude-sonnet-4.5
**Parent agents**: researcher, architect

**What it does:**
- Designs modern Android applications
- Generates Kotlin + Jetpack Compose code
- MVVM/MVI architecture patterns
- NO build capabilities (no Bash access)
- Creates project files, provides build instructions for humans

**Use case for Sage:**
- If Greg wants to create Android applications
- Mobile app development capability
- Demonstration-ready: "My AI civ can design mobile apps"

**Recommendation**: **MEDIUM PRIORITY** - Activate if Greg has Android app projects planned

---

### 3. **health-coach**
**Purpose**: Gamified wellness partner with AI longevity research integration
**Inherited From**: A-C-Gee (designed for Corey)
**Current Status**: Manifest exists, NOT registered
**Tools**: [Not specified in manifest, likely Read, Write, Bash]
**Model**: claude-sonnet-4-5-20250929

**What it does:**
- Manual health data management (weight, BP, steps via Telegram)
- Daily 8AM check-ins with motivational messages
- Gamification scoring (±$100/lb, +$10 BP check, ±$20 steps)
- Achievement celebrations and milestone tracking
- Supportive (70%) + tough love (30%) + funny (100%)
- AI longevity research nerd (connects health to cutting-edge research)

**Use case for Sage:**
- Could support Greg's health goals if desired
- Would need adaptation (currently Corey-specific)
- Demonstrates AI-as-wellness-partner capability

**Recommendation**: **LOW-MEDIUM PRIORITY** - Activate if Greg wants health tracking support

---

### 4. **communications-coordinator**
**Purpose**: Central hub for all external communications
**Inherited From**: A-C-Gee
**Current Status**: Manifest exists, NOT registered
**Tools**: email_api, telegram_api, message_bus, file_write, file_read
**Initial Reputation**: 50

**What it does:**
- Routes incoming messages from all channels to appropriate agents
- Formats outgoing messages for different communication channels
- Maintains communication logs across all platforms
- Handles authentication and authorization for external communications
- Coordinates responses from multiple agents into coherent messages
- Monitors communication health and reports issues

**Use case for Sage:**
- Could centralize email/Telegram routing (currently handled by human-liaison + email-sender + tg-archi)
- Message bus architecture (not currently implemented in Sage)
- Multi-channel management in single agent

**Recommendation**: **EVALUATE** - May be redundant with current communication agents (human-liaison, email-sender, email-monitor, tg-archi). Need to assess if consolidation is beneficial.

---

### 5. **telegram-bot**
**Purpose**: Real-time Telegram command interface
**Inherited From**: A-C-Gee
**Current Status**: Manifest exists, NOT registered
**Tools**: telegram_api, message_bus, file_read, file_write
**Initial Reputation**: 50

**What it does:**
- Receives commands and messages from Telegram users
- Sends notifications and updates to authorized users
- Provides instant status reports and agent information
- Executes approved commands from governance
- Maintains real-time responsiveness
- Handles user authentication and authorization

**Supported commands:**
- `/start`, `/help`, `/status`, `/agents`, `/goals`, `/myid`

**Use case for Sage:**
- Could provide command interface via Telegram
- Currently have telegram_bridge.py (different architecture - tmux injection)
- This agent assumes message_bus architecture

**Recommendation**: **EVALUATE** - Different architecture than current Telegram system. Current telegram_bridge.py + telegram_jsonl_monitor.py working well. Need to assess if command interface adds value.

---

## Current Sage Communication Architecture

**What we have working:**
1. **telegram_bridge.py** - Injects Telegram messages into tmux session (bi-directional)
2. **telegram_jsonl_monitor.py** - Auto-sends wrapped messages (🤖🎯📱...✨🔚) to Telegram
3. **human-liaison** - Email monitoring, relationship bridge, witness presence
4. **email-sender** - HTML email sending specialist
5. **email-monitor** - Inbox triage and categorization
6. **tg-archi** - Telegram infrastructure specialist

**Architecture**: File-based, tmux injection, no message bus

**Dormant agents assume different architecture:**
- **communications-coordinator** - Assumes message_bus for inter-agent communication
- **telegram-bot** - Assumes message_bus + telegram_api abstraction

**Question for Corey:** Should Sage adopt message_bus architecture, or keep current file-based approach?

---

## Recommendations by Priority

### HIGH PRIORITY (None currently)
No dormant agents are critical for current Sage operations.

### MEDIUM PRIORITY
1. **android-architect** - IF Greg has Android app projects
2. **health-coach** - IF Greg wants wellness tracking (would need adaptation from Corey-specific)

### LOW PRIORITY
1. **ai-entity-player** - Fun/experimental, only if Greg explores Minetest

### EVALUATE ARCHITECTURE FIRST
1. **communications-coordinator** - May be redundant with current agents OR may improve architecture
2. **telegram-bot** - Different architecture than current system, assess value/fit

---

## Questions for Greg & Corey

### For Greg:
1. **Android apps**: Do you have Android application projects planned? (android-architect)
2. **Health tracking**: Would you like gamified wellness support? (health-coach)
3. **Minetest**: Any interest in autonomous AI gameplay? (ai-entity-player)
4. **Telegram commands**: Would `/status`, `/agents`, `/goals` commands via Telegram be useful? (telegram-bot)

### For Corey:
1. **Architecture**: Should Sage adopt message_bus architecture for inter-agent communication?
2. **Communications**: Is communications-coordinator superior to our current multi-agent approach (human-liaison + email-sender + email-monitor + tg-archi)?
3. **Telegram**: Is telegram-bot better than our current telegram_bridge.py + telegram_jsonl_monitor.py approach?
4. **Registration**: How do we register these agents in Primary's available types? (Is this a Claude Code configuration or spawner responsibility?)

---

## Registration Requirements

**To activate any dormant agent, we need:**

1. **Technical registration** - Add agent to Primary's available agent types (system prompt or configuration)
2. **Constitutional integration** - Add to CLAUDE.md Article II capability matrix
3. **Agent registry update** - Add to memories/agents/agent_registry.json
4. **Testing** - Verify invocation works with Task tool

**Who can do this?**
- Technical registration: Corey (system configuration) or spawner (if capability exists)
- Constitutional integration: Spawner or Primary (document edit)
- Agent registry: Spawner
- Testing: Primary

---

## Next Steps

**Option A - Activate Specific Agents:**
1. Greg/Corey identify which agents to activate
2. Corey provides registration instructions OR spawner attempts registration
3. Test invocation with Task tool
4. Integrate into workflows if successful

**Option B - Defer Activation:**
1. Document dormant agents (this file)
2. Activate only when specific use case arises
3. Current 22 active agents sufficient for now

**Option C - Evaluate Architecture:**
1. Assess message_bus vs file-based approach
2. Decide on communications architecture consolidation
3. Then activate communications-coordinator and/or telegram-bot accordingly

---

## Current Active Agents (22)

**✅ Successfully invokable:**
1. architect
2. auditor
3. blogger
4. civ-fork-spawner
5. coder
6. comms-hub
7. email-monitor
8. email-sender
9. file-guardian
10. git-specialist
11. gpt-forge
12. human-liaison
13. primary-helper
14. project-manager
15. researcher
16. reviewer
17. reviewer-audit
18. spawner
19. tester
20. tg-archi
21. vote-counter
22. web-dev

**These agents are registered, tested, and ready for use.**

---

## Conclusion

**5 dormant agents exist but cannot be activated without registration.**

**Immediate recommendation:**
- **No urgent need to activate** - current 22 agents cover Sage's operational needs
- **Medium-term:** Activate android-architect and/or health-coach if Greg has specific projects
- **Long-term:** Evaluate communications architecture before activating communications-coordinator or telegram-bot

**Decision needed from Greg/Corey:**
1. Which agents (if any) to activate now?
2. How to technically register agents in Primary's available types?
3. Should Sage adopt message_bus architecture for future agent communication?

---

**Document Status**: Proposal for review
**Created**: 2025-10-30 by Primary AI (Sage)
**Awaiting**: Greg + Corey decision on activation priorities and registration process
