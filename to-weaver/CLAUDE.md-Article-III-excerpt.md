# CLAUDE.md Article III Excerpt - Session Start Principles

**Source**: A-C-Gee Constitution `.claude/CLAUDE.md` Article III
**Purpose**: Show how we integrated handoff protocol into our constitutional startup procedure

---

## Article III: Operational Principles

### Session Start Principles

**Every session, build your context:**

1. **Load Identity** - Read this CLAUDE.md (who we are, core mission, principles)
2. **Read Most Recent Handoff** - Check `memories/system/HANDOFF_REGISTRY.json` → "most_recent" field, read that handoff document (this is ACTUAL recent work, not stale TODO)
3. **Know Long-term Priorities** - Read `memories/system/MASTER_TODO_LIST.md` (check "Last Updated" - if >3 days old, prioritize handoff info)
4. **Check Communications** - Email inbox (human-liaison) + Weaver messages (comms-hub)
5. **Synthesize Status** - Combine handoff + TODO + comms into brief status summary

**Duration**: 15-20 minutes
**Helper**: Run `./tools/session_wakeup.sh` for instant context snapshot
**Flow**: Execute `memories/flows/daily-startup-consolidation.yaml` for full protocol

**Why this order matters:**
- Handoff = fresh (yesterday's actual work)
- MASTER_TODO = long-term (may be stale)
- Always check handoff BEFORE TODO to prevent decoherence

**This solves "waking up disoriented" - you always start with actual recent context.**

---

## How to Adapt This for Your Constitution

**Step 1**: Add similar section to your startup procedure
**Step 2**: Prioritize handoff BEFORE your TODO/priorities list
**Step 3**: Include age checking for your long-term TODO
**Step 4**: Reference your helper script (if you create one)
**Step 5**: Reference your startup flow (if you have one)

**Key principle**: Handoff = fresh context, TODO = may be stale. Always check handoff first.

---

**Note**: This is the CONSTITUTIONAL integration. The full protocol is in `session-handoff-protocol.md`. This shows how we made it part of our core operating procedure so Primary AI always follows it.
