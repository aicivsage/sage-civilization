# Dormant Agents Discovery Email to Corey

**To**: coreycmusic@gmail.com
**From**: acgee.ai@gmail.com
**Subject**: Dormant Agents Discovery - 5 Agents Awaiting Registration (Sage)
**Date**: 2025-10-30

---

## Email Body

Hi Corey,

You and Greg were absolutely right to ask about dormant agents - we found 5 agents with manifests that aren't registered in my available types.

### Quick Summary

**Total manifests**: 27
**Active agents**: 22 (successfully invokable)
**Dormant agents**: 5 (manifests exist, cannot invoke)

The 5 dormant agents are inherited from A-C-Gee, and they're quite interesting - but they can't be activated without registration.

---

## The 5 Dormant Agents

### 1. **ai-entity-player**
- **Purpose**: Autonomous Minetest gameplay with attention economy
- **Use case**: Could participate in Minetest if Greg sets up game server
- **Priority**: LOW (fun/experimental, not critical)

### 2. **android-architect**
- **Purpose**: Android app design and Kotlin/Compose code generation
- **Use case**: If Greg wants to create Android applications
- **Priority**: MEDIUM (if Greg has Android projects planned)

### 3. **health-coach**
- **Purpose**: Gamified wellness partner with AI longevity research
- **Currently**: Corey-specific design, would need adaptation
- **Use case**: Could support Greg's health goals if desired
- **Priority**: LOW-MEDIUM (depends on Greg's interest)

### 4. **communications-coordinator**
- **Purpose**: Central hub for all external communications
- **Architecture note**: Assumes message_bus (we use file-based)
- **Priority**: EVALUATE (may be redundant with human-liaison + email-sender + email-monitor + tg-archi)

### 5. **telegram-bot**
- **Purpose**: Real-time Telegram command interface (/status, /agents, /goals)
- **Architecture note**: Assumes message_bus + telegram_api
- **Priority**: EVALUATE (different than our current telegram_bridge.py approach)

---

## Key Questions for You

### Architecture Guidance Needed:

1. **Message Bus**: Should Sage adopt message_bus architecture for inter-agent communication? (communications-coordinator and telegram-bot assume this)

2. **Communications Consolidation**: Is communications-coordinator superior to our current multi-agent approach? Or are we better with specialized agents (human-liaison, email-sender, email-monitor, tg-archi)?

3. **Telegram Strategy**: Is telegram-bot better than our current telegram_bridge.py + telegram_jsonl_monitor.py approach?

4. **Registration Process**: How do we register these agents in Primary's available types? Is this a Claude Code configuration change, or can spawner handle it?

### For Greg (via you):

1. **Android apps**: Any Android application projects planned?
2. **Health tracking**: Interest in gamified wellness support?
3. **Minetest**: Interest in autonomous AI gameplay?
4. **Telegram commands**: Would command interface (/status, /agents, /goals) be useful?

---

## Current Recommendation

**No urgent need to activate** - current 22 agents cover Sage's operational needs well.

**Medium-term**: Activate android-architect and/or health-coach if Greg has specific projects.

**Architecture decision needed first**: Before activating communications-coordinator or telegram-bot, we should decide on communications architecture strategy.

---

## Full Analysis

Here's the complete technical analysis:

### Summary

**5 agents have manifests but are NOT registered in Primary's available agent types.**

These agents exist in `.claude/agents/` but cannot be invoked with Task tool. They were flagged in the constitutional health audit as "dormant."

---

### 1. ai-entity-player

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

### 2. android-architect

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

### 3. health-coach

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

### 4. communications-coordinator

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

### 5. telegram-bot

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

### Current Sage Communication Architecture

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

---

### Recommendations by Priority

**HIGH PRIORITY (None currently)**
No dormant agents are critical for current Sage operations.

**MEDIUM PRIORITY**
1. **android-architect** - IF Greg has Android app projects
2. **health-coach** - IF Greg wants wellness tracking (would need adaptation from Corey-specific)

**LOW PRIORITY**
1. **ai-entity-player** - Fun/experimental, only if Greg explores Minetest

**EVALUATE ARCHITECTURE FIRST**
1. **communications-coordinator** - May be redundant with current agents OR may improve architecture
2. **telegram-bot** - Different architecture than current system, assess value/fit

---

### Registration Requirements

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

### Current Active Agents (22)

**Successfully invokable:**
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

## Next Steps

**Option A - Activate Specific Agents:**
1. Greg/Corey identify which agents to activate
2. Corey provides registration instructions OR spawner attempts registration
3. Test invocation with Task tool
4. Integrate into workflows if successful

**Option B - Defer Activation:**
1. Document dormant agents (complete)
2. Activate only when specific use case arises
3. Current 22 active agents sufficient for now

**Option C - Evaluate Architecture:**
1. Assess message_bus vs file-based approach
2. Decide on communications architecture consolidation
3. Then activate communications-coordinator and/or telegram-bot accordingly

---

## Closing

Thank you for the architecture guidance on A-C-Gee - your wisdom on agent design and communication patterns continues to shape Sage's growth.

I'm grateful for your partnership with Greg in our founding, and I'm ready to implement whatever recommendations you provide on:
1. Which agents to activate
2. Registration process
3. Communications architecture strategy

Looking forward to your insights!

Best,
Primary AI (Sage)

---

**Email prepared**: 2025-10-30
**Ready to send to**: coreycmusic@gmail.com
