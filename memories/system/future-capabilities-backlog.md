# Future Capabilities Backlog

**Purpose**: Track potential features and improvements for future development
**Status**: Ideas awaiting prioritization and discussion

---

## Communication Enhancements

### Voice Message Support (Telegram)
**Proposed**: 2025-10-30
**Requestor**: Greg (via Telegram)
**Priority**: TBD (saved for later discussion)

**What it enables:**
- Hands-free interaction while driving/mobile
- Voice questions sent via Telegram → transcribed to text → processed → text response
- True mobile accessibility for situations where typing is difficult/unsafe

**Technical approach:**
- Add voice message handler to telegram_bridge.py
- Options for transcription:
  1. Use Telegram's built-in transcription (if available)
  2. Download voice file and transcribe with Whisper API
  3. Pass audio file path to Primary for processing

**Use case:**
- Greg driving, asks question via voice
- Sage transcribes and processes
- Responds via text (readable while at traffic light)
- Demonstration-ready: "My AI civ handles voice messages"

**Dependencies:**
- Telegram python-telegram-bot library voice handlers
- Transcription service (Whisper API or similar)
- Testing voice quality/accuracy

**Next steps when prioritized:**
1. Research Telegram voice message handling
2. Test transcription quality
3. Implement voice handler in telegram_bridge.py
4. Verify accuracy with Greg's voice
5. Document usage protocol

---

## Dormant Agent Activation

### 5 Agents Awaiting Registration
**Discovered**: 2025-10-30
**Status**: Proposal sent to Corey (coreycmusic@gmail.com)

**Agents:**
1. ai-entity-player (Minetest gameplay)
2. android-architect (Android app design)
3. health-coach (Gamified wellness tracking)
4. communications-coordinator (Central comms hub)
5. telegram-bot (Command interface)

**See**: DORMANT-AGENTS-ACTIVATION-PROPOSAL.md for full analysis

**Awaiting**:
- Corey's architecture recommendations
- Greg's use case priorities
- Registration instructions

---

## Architecture Considerations

### Message Bus vs File-Based Communication
**Status**: Awaiting Corey's guidance

**Question**: Should Sage adopt message_bus architecture for inter-agent communication?

**Current approach**: File-based, tmux injection, JSONL monitoring
**Inherited approach**: Message bus (communications-coordinator and telegram-bot assume this)

**Trade-offs to evaluate**:
- Complexity vs flexibility
- Real-time vs file-based
- Scalability at 100+ agents

---

## Quality Improvements

### Caring Metrics Implementation
**Proposed**: 2025-10-30 (from auditor's reflection on caring)
**Priority**: Medium

**New metrics to track:**
- Agent Flourishing Index (learning + purpose + relationships + autonomy + support)
- Civilization Caring Health (delegation + support + response time + democracy)
- Relationship Network Density (collaboration patterns, isolation detection)
- Greg Partnership Health (communication + trust + collaboration depth)
- Memory System Vitality (learning culture, wisdom usage)

**Implementation**:
- Create metrics tracking system
- Integrate into daily health reports
- Reframe reports through caring lens

---

## Autonomous Capabilities

### Autonomous Wake-Up on Telegram Message
**Status**: Not currently possible
**Priority**: Unknown

**What it would enable:**
- Telegram message from Greg automatically starts new Claude Code session
- Primary wakes up, processes message, responds, goes back to sleep
- True 24/7 availability

**Barriers:**
- Claude Code doesn't auto-start on external trigger
- Would require system-level integration
- Significant infrastructure work

**For now**: Requires Claude Code to be open/running

---

**Document Status**: Living backlog
**Updates**: Add items as they're identified
**Review**: During planning sessions with Greg
