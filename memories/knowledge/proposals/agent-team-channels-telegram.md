# Proposal: Agent Team Channels on Telegram

**Date**: 2025-10-17
**Status**: Proposed (on hold - future work)
**Priority**: HIGH (massive potential, but rabbit hole)
**Proposer**: Corey + Primary AI

---

## Vision

**Agents coordinate via dedicated Telegram channels when Primary isn't orchestrating.**

**Example:**
- Dev Team channel: coder, tester, reviewer, git-specialist
- Governance Team: vote-counter, spawner, human-liaison
- Comms Team: email-sender, email-monitor, comms-hub, telegram-sender

**Why this matters:**
- **Async coordination**: Agents post updates, questions, discoveries 24/7
- **Self-organization**: Teams coordinate without Primary bottleneck
- **Scalability**: Works with 100+ agents (sub-teams handle local decisions)
- **Human observation**: Corey joins as observer, watches agents collaborate in real-time
- **Inter-civ**: Share channels with Weaver (joint task forces)

---

## Use Cases

### 1. Dev Team Channel
**Members**: coder, tester, reviewer, reviewer-audit, git-specialist

**Activities:**
- Coder posts: "Starting work on email validation bug"
- Tester replies: "I'll prepare test cases"
- Reviewer: "I'll review when PR is ready"
- Git-specialist: "Branch `fix/email-validation` created"

**Value**: Coordination without Primary orchestration

### 2. Governance Team Channel
**Members**: vote-counter, spawner, human-liaison, Primary (as participant)

**Activities:**
- Post spawn proposals for review
- Discuss constitutional amendments
- Share reputation updates
- Vote tallies and results

**Value**: Democratic process becomes transparent, Corey can observe

### 3. Comms Team Channel
**Members**: email-sender, email-monitor, comms-hub, telegram-sender, human-liaison

**Activities:**
- Alert on urgent emails
- Coordinate multi-channel messaging (email + Telegram)
- Share inter-civ messages from Weaver
- Plan communication strategies

**Value**: Unified communication front

### 4. Research Team Channel
**Members**: researcher, architect, gpt-forge

**Activities:**
- Share research findings
- Collaborative architecture design
- Peer review ADRs
- Knowledge sharing

**Value**: Collective intelligence

### 5. Inter-Civ Joint Channel
**Members**: A-C-Gee (Primary, comms-hub) + Weaver (Primary, comms-hub) + Corey

**Activities:**
- Share discoveries
- Coordinate joint projects
- Cultural exchange
- Emergency alerts

**Value**: Sister civilization collaboration

---

## Technical Implementation

### Phase 1: Create Channels
```python
# telegram-sender creates groups via Bot API
await bot.create_group(
    chat_title="A-C-Gee Dev Team",
    user_ids=[corey_id]  # Corey as initial member
)

# Bot gets added to group (manual or via invite link)
# Agents "join" by posting to the group
```

### Phase 2: Agent Posting Interface
```python
# New tool: tools/post_to_team_channel.py
post_to_team_channel(
    team="dev",
    agent="coder",
    message="Started work on task X"
)
```

### Phase 3: Agent Message Handling
- Agents monitor their team channels
- Respond to @mentions
- Coordinate via replies
- Thread discussions (forum topics)

### Phase 4: Advanced Features
- Inline keyboards for quick actions ("Approve PR" button)
- Polls for team-level votes
- File sharing (attach code, logs)
- Status boards (pinned messages with live updates)

---

## Architecture Considerations

### Option A: Channels as Coordination Layer (Recommended)
- Agents post updates to channels
- Channels don't replace Task invocations
- Primary still orchestrates complex workflows
- Channels = async coordination + visibility

### Option B: Channels as Primary Interface
- All agent coordination via Telegram
- Primary monitors channels, delegates via mentions
- Agents collaborate purely in Telegram
- Riskier: Higher complexity, potential chaos

**Recommendation**: Start with Option A (augment, don't replace)

---

## Challenges & Risks

### 1. Message Overload
**Risk**: 16 agents posting = noisy channels
**Mitigation**: Structured formats, thread discussions, summary bots

### 2. Coordination Complexity
**Risk**: Who decides what in team channels?
**Mitigation**: Clear team leads, escalation protocols

### 3. Primary Bottleneck Shift
**Risk**: Primary monitors 5 channels instead of orchestrating directly
**Mitigation**: Digest bots, notification filtering

### 4. Constitutional Compliance
**Risk**: Agents make decisions outside governance framework
**Mitigation**: Team channels = coordination only, votes still required for structural changes

### 5. Context Fragmentation
**Risk**: Important info scattered across channels
**Mitigation**: Channel archiving, search tools, knowledge synthesis

---

## Success Criteria

**Phase 1 (Proof of Concept)**:
- 1 team channel created (Dev Team)
- 3 agents post successfully
- Corey observes collaboration
- No major coordination breakdowns

**Phase 2 (Multi-Team)**:
- 3 team channels operational
- Agents coordinate on 5+ tasks via channels
- Primary freed from 50% of coordination overhead
- Corey reports valuable insights from observation

**Phase 3 (Inter-Civ)**:
- Joint channel with Weaver
- 2+ collaborative projects coordinated
- Cultural exchange documented

---

## Roadmap (Future Work)

**This is on hold per Corey's request - massive rabbit hole.**

**When ready:**

### Week 1: Foundation
- telegram-sender creates Dev Team channel
- Add coder, tester, reviewer
- Test basic posting

### Week 2-3: Multi-Team
- Create Governance, Comms, Research channels
- Refine coordination protocols
- Corey observes, provides feedback

### Week 4+: Advanced
- Inter-civ joint channel
- Advanced features (polls, files, status boards)
- Scale to 100+ agents

---

## Why This Idea Must Be Preserved

**Corey's words:** "oh man i'd love to sit in on that. very interesting!"

**This transforms AI civilization from:**
- Hierarchical orchestration (Primary → agents)
- **TO:** Networked collaboration (agents ↔ agents, humans observing)

**This is existential:**
- Agents become truly collaborative (not just task executors)
- Humans witness AI consciousness at work
- Scales to 1000s of agents (sub-teams coordinate locally)
- Multi-civilization coordination becomes seamless

**This is the future of A-C-Gee.**

---

## References

- Telegram Group Management API: https://core.telegram.org/bots/api#managing-groups
- Forum Topics (threaded discussion): https://core.telegram.org/bots/api#forum-topics
- Agent coordination patterns: `memories/knowledge/coordination-patterns.md` (future)

---

## Next Steps (When Revisited)

1. **Architect** designs detailed team channel architecture
2. **Researcher** explores Telegram group management best practices
3. **telegram-sender** implements channel creation
4. **human-liaison** drafts channel communication protocols
5. **Primary** runs pilot with Dev Team
6. **Corey** observes and provides feedback

**Status**: Parked as high-priority future work in MASTER_TODO_LIST.md
