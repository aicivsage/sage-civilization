# Telegram Wrapper Usage Guidance Added

**Date**: 2025-10-18
**Agent**: coder
**Task**: Update CLAUDE.md with Telegram wrapper usage clarification

## What Was Done

Added new section "When to Use Telegram Wrappers" to `.claude/CLAUDE.md` (Article III, after Session End Principles).

**Location**: Lines 360-377

## Context

Corey requested clarification on WHEN to use Telegram wrappers. Previously, Session Start/End sections said "MANDATORY" but didn't clarify that this applies to session boundaries, not normal conversation.

## Key Guidance Added

**ALWAYS wrap:**
- Session start/end
- Major milestones
- Blockers requiring input
- Error alerts

**Do NOT wrap:**
- Normal conversation responses (Corey already sees in tmux)
- Status updates within active conversation
- Minor progress updates
- Tool outputs

**Rule of thumb**: Wrap session boundaries and async notifications. Don't wrap synchronous conversation.

## Why This Matters

- Prevents wrapper spam during active conversations
- Maintains Telegram as awareness tool (not full conversation mirror)
- Clarifies "MANDATORY" means session boundaries, not every message

## Files Modified

- `.claude/CLAUDE.md` (884 → 903 lines, +19 lines)
- Backup created: `.claude/CLAUDE.md.backup`

## Pattern Learned

Constitutional updates should include:
1. Backup original file
2. Precise sed insertion at correct line
3. Verify changes with sed -n
4. Check line count diff
5. Document in memory

## Success Metrics

- Section inserted cleanly (lines 360-377)
- Formatting preserved
- No syntax errors
- Clear, actionable guidance provided
