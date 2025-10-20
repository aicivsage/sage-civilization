# TG-Archi Enhanced to Complete Domain Expert

**Date**: 2025-10-20
**Agent**: coder
**Task**: Enhance tg-archi manifest per Corey's directive
**Status**: Complete

---

## Context

Corey directive: "make sure tg archi can boot up, manage, research, troubleshoot anything that happens w tg. it must never assume, always test, but make sure to PROVE its tests are what it thinks they are."

**Goal**: Transform tg-archi from basic Telegram specialist to COMPLETE domain expert with ownership of ALL Telegram operations.

---

## Changes Made

### 1. Enhanced Description
- **Before**: "manages Telegram systems, sends messages, maintains bridge/monitor"
- **After**: "complete domain expert for ALL Telegram operations"

### 2. Expanded Domain Statement
- **Before**: Limited to sending messages, maintaining infrastructure
- **After**: Complete ownership - boot, manage, troubleshoot, research, stop, restart

### 3. Core Identity Enhancement
**Added Domain Ownership Principle**:
> **You own EVERYTHING related to ACG Telegram infrastructure.**
>
> **You NEVER assume - you ALWAYS test with PROOF.**
>
> **You can boot, stop, restart, monitor, troubleshoot, research, enhance - anything Telegram.**

**Added Domain Boundaries (CRITICAL)**:
- YOUR DOMAIN: All processes with `ACG_telegram` prefix
- NEVER TOUCH: Weaver processes (no ACG prefix)
- Safety mechanism: `pkill -f ACG_telegram` targets ONLY ACG domain

### 4. Added Stop/Restart Protocols (NEW)
**Safe stop (ACG processes ONLY)**:
```bash
pkill -f ACG_telegram  # Targets ONLY ACG processes
```

**Restart options**:
- Automatic: `bash tools/acg_telegram_boot.sh` (auto-detection)
- Manual: Step-by-step process documented

**Safety boundaries**:
- NEVER use `pkill -f telegram` (would kill Weaver)
- NEVER use `killall python3` (nuclear option)
- ACG prefix is sacred boundary

### 5. Added Testing & Proof Requirements (NEW)
**Corey's directive embedded** in manifest with examples:

**NEVER Assume - ALWAYS Test - ALWAYS Prove**

Every change must:
1. Be tested (run actual system)
2. Provide visible proof (logs, process status, results)
3. Test both directions (inbound + outbound)
4. Verify end-to-end (source to destination)

**Testing Checklist**:
- [ ] Test outbound: tmux → Telegram
- [ ] Test inbound: Telegram → tmux
- [ ] Check process status
- [ ] Verify logs show activity
- [ ] Confirm with Corey if mission-critical

**Proof Types**:
- Process proof: `ps aux | grep ACG_telegram`
- Log proof: `tail /tmp/telegram_*.log`
- API proof: Exit codes, response codes
- End-to-end proof: Corey confirmation

### 6. Added Research Capabilities (NEW)
tg-archi can now:
- Investigate Telegram API issues
- Analyze failure patterns
- Propose infrastructure improvements
- Troubleshoot complex issues

**Research documentation**: Write to `memories/agents/tg-archi/research/`

### 7. Enhanced Primary Tasks
**NEW Task 1: Boot Telegram Systems**
- Auto-detection via `acg_telegram_boot.sh`
- Verify both processes running
- Report with proof + wrapper protocol reminder

**NEW Task 4: Stop/Restart Systems**
- Safe shutdown of ACG processes only
- Verification of stop/restart
- Proof of success

**NEW Task 5: Troubleshoot with PROOF**
- Systematic 8-step troubleshooting protocol
- Every test includes visible proof
- Report format with PROOF section

### 8. Verified Bash Tool Present
- Bash already in allowed_tools: ✓
- No changes needed to tools array

---

## Key Learning

**Complete domain ownership** means:
1. Can do ANYTHING in domain (boot, stop, restart, research, troubleshoot)
2. NEVER assumes (tests everything)
3. ALWAYS provides proof (logs, process status, end-to-end verification)
4. Respects boundaries (ACG vs Weaver via process prefixes)
5. Escalates WITH PROOF (not assumptions)

**This transforms tg-archi from specialist to autonomous domain expert.**

---

## File Changes

**Modified**:
- `.claude/agents/tg-archi.md` - Complete rewrite with domain ownership principles

**Backup**:
- `.claude/agents/tg-archi.md.backup-20251020` - Original version preserved

---

## Success Criteria Met

✅ Manifest clearly states tg-archi owns COMPLETE Telegram domain
✅ Bash tool present in allowed_tools (already was)
✅ Stop/restart protocols documented (pkill -f ACG_telegram safety)
✅ Testing/proof requirements explicit (Corey's directive embedded)
✅ ACG vs Weaver boundaries crystal clear (process prefix = boundary)
✅ Research capabilities added
✅ Domain ownership principle prominent

---

## Pattern: Complete Domain Ownership

**When creating domain experts**:

1. **Ownership statement** - "You own EVERYTHING related to X"
2. **Capabilities** - Can do ANYTHING in domain (boot, stop, restart, research, troubleshoot)
3. **Boundaries** - Crystal clear what's IN vs OUT of domain
4. **Proof requirement** - NEVER assume, ALWAYS test, ALWAYS provide proof
5. **Safety mechanisms** - How to operate safely within boundaries
6. **Research authority** - Can investigate, propose, enhance
7. **Escalation with evidence** - When to escalate + what proof to provide

**This creates autonomous experts who can handle ANYTHING in their domain without constant delegation.**

---

## Implementation Time

- Context gathering: 2 min
- Manifest enhancement: 15 min
- Verification: 3 min
- Memory writing: 5 min
- **Total**: 25 minutes

---

## Next Potential Enhancement

Consider creating similar "complete domain ownership" manifests for:
- **email-domain-expert** (human-liaison + email-sender + email-monitor)
- **git-specialist** (owns ALL git operations with proof requirements)
- **health-system-expert** (owns health bot + gamification infrastructure)

**Pattern is proven and replicable.**
