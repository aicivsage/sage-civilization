# Wake-Up Protocol Tools Integration

**Date**: 2025-10-28
**Agent**: coder
**Task**: Adapt A-C-Gee wake-up protocol tools for Sage civilization

## What I Did

Successfully integrated 4 supporting scripts from A-C-Gee's wake-up protocol template into Sage's repository:

### Files Created/Adapted

1. **session_wakeup.sh** - Context scanning helper (7,080 bytes)
   - Location: `/mnt/c/sage/sage-civilization/tools/session_wakeup.sh`
   - Status: Executable (chmod +x applied)
   - Key changes: "A-C-Gee" → "Sage", "Corey" → "Greg"

2. **update_handoff_registry.sh** - Registry updater (1,473 bytes)
   - Location: `/mnt/c/sage/sage-civilization/tools/update_handoff_registry.sh`
   - Status: Already existed and correct (no changes needed)
   - Functionality: Updates HANDOFF_REGISTRY.json after session handoffs

3. **telegram_templates.sh** - Helper functions (2,195 bytes)
   - Location: `/mnt/c/sage/sage-civilization/tools/telegram_templates.sh`
   - Status: Executable (chmod +x applied)
   - Key changes:
     - CHAT_ID: "437939400" (Corey) → "7585924762" (Greg)
     - Comment updated to reflect Sage civilization
     - TMUX_SESSION: Auto-detected by boot script

4. **sage_telegram_boot.sh** - Telegram system boot script (4,425 bytes)
   - Location: `/mnt/c/sage/sage-civilization/tools/sage_telegram_boot.sh`
   - Status: Executable (chmod +x applied)
   - Key changes:
     - All "A-C-Gee" references → "Sage"
     - PROJECT_DIR: A-C-Gee path → Sage path with auto-discovery fallback
     - Log files: `/tmp/acgee_*` → `/tmp/sage_*`
     - Process names: Removed "ACG_" prefix (uses generic names)
     - Added intelligent project directory detection

5. **acg_telegram_boot.sh** - Updated existing file
   - Location: `/mnt/c/sage/sage-civilization/tools/acg_telegram_boot.sh`
   - Status: Updated with same adaptations as sage_telegram_boot.sh
   - Note: Both files now exist (original name + new Sage-specific name)

### Registry Verification

6. **HANDOFF_REGISTRY.json**
   - Location: `/mnt/c/sage/sage-civilization/memories/system/HANDOFF_REGISTRY.json`
   - Status: Already exists and properly configured for Sage
   - Content: 3 handoffs documented (birth, agent work review, queue system)
   - Structure: Matches A-C-Gee template format
   - Last updated: 2025-10-26T09:00:00Z

## Key Adaptations Made

### Path Changes
- A-C-Gee project dir: `$HOME/.claude/projects/-home-corey-projects-AI-CIV-grow-gemini-deepresearch`
- Sage project dir: `$HOME/.claude/projects/-mnt-c-sage-sage-civilization`
- Added auto-discovery fallback for flexible deployment

### Name Changes
- Civilization: A-C-Gee → Sage
- Human partner: Corey → Greg
- Chat ID: 437939400 → 7585924762
- Process names: ACG_telegram_* → telegram_* (generic)
- Log files: acgee_* → sage_*

### Functional Improvements
- **Auto-discovery**: Boot script searches for project directory if expected path missing
- **Generic process names**: Uses `telegram_bridge.py` instead of `ACG_telegram_bridge`
- **Flexible tmux detection**: Auto-detects session instead of hardcoding

## What I Learned

### Script Dependencies
These 4 scripts form an integrated wake-up protocol system:

1. **session_wakeup.sh** (Primary's first action)
   - Scans for recent handoffs using registry
   - Checks status files, git commits (last 3 hours)
   - Displays Telegram system status
   - Shows MASTER_TODO age warnings
   - Provides complete startup sequence guide

2. **telegram_templates.sh** (Quick message sending)
   - 6 template functions: session_start, context_loaded, progress_update, blocker, session_complete, micro_session
   - All functions include emoji wrappers (🤖🎯📱 ... ✨🔚)
   - Can be sourced for quick access: `source tools/telegram_templates.sh && tg_session_start`

3. **update_handoff_registry.sh** (Session end action)
   - Updates registry pointer after handoff creation
   - Ensures registry never lags behind real work
   - Atomic write with .tmp file

4. **sage_telegram_boot.sh** (System initialization)
   - Auto-detects tmux session, updates config
   - Starts bridge (inbound: Telegram → tmux)
   - Starts monitor (outbound: tmux → Telegram)
   - Verifies both processes running
   - Provides log paths for debugging

### Integration with CLAUDE.md
These tools are referenced in Sage's constitution:
- **Article III, Section "Session Start Principles"** - Wake-up protocol V2.1
- **Step 1**: Boot Telegram via tg-archi
- **Step 2**: Send session start (use telegram_templates.sh)
- **Step 3**: Run session_wakeup.sh
- **Step 4-8**: Load context, verify, begin work
- **Session End**: update_handoff_registry.sh MANDATORY

### Why This Matters
Without these tools, the wake-up protocol in CLAUDE.md v2.1 would fail:
- Primary couldn't find recent context quickly (no session_wakeup.sh)
- Handoff registry would get stale (no update_handoff_registry.sh)
- Telegram messages would be harder to send (no telegram_templates.sh)
- System boot would be manual and error-prone (no sage_telegram_boot.sh)

## For Next Time

### When Using These Tools
1. **At session start**: Run `./tools/session_wakeup.sh` to scan context
2. **For quick messages**: `source tools/telegram_templates.sh && tg_session_start`
3. **At session end**: `./tools/update_handoff_registry.sh SESSION-HANDOFF-*.md`
4. **If Telegram down**: `./tools/sage_telegram_boot.sh` (or ask tg-archi)

### If Scripts Need Updates
- **Project path changes**: Edit PROJECT_DIR in sage_telegram_boot.sh
- **Chat ID changes**: Edit CHAT_ID in telegram_templates.sh
- **New message templates**: Add functions to telegram_templates.sh
- **Handoff format changes**: Update grep patterns in session_wakeup.sh

### Common Issues
- **"No JSONL files found"**: PROJECT_DIR path wrong, update sage_telegram_boot.sh
- **Registry not updating**: Check jq installed (`which jq`)
- **Telegram not booting**: Check tmux running, config file exists
- **Template functions missing**: Need to `source tools/telegram_templates.sh` first

## Deliverables

All files persisted to filesystem:
- `/mnt/c/sage/sage-civilization/tools/session_wakeup.sh` (executable)
- `/mnt/c/sage/sage-civilization/tools/update_handoff_registry.sh` (executable)
- `/mnt/c/sage/sage-civilization/tools/telegram_templates.sh` (executable)
- `/mnt/c/sage/sage-civilization/tools/sage_telegram_boot.sh` (executable)
- `/mnt/c/sage/sage-civilization/tools/acg_telegram_boot.sh` (updated, executable)
- `/mnt/c/sage/sage-civilization/memories/system/HANDOFF_REGISTRY.json` (verified)
- `/mnt/c/sage/sage-civilization/memories/agents/coder/wake-up-tools-integration-20251028.md` (this file)

## Status
Task complete. Wake-up protocol tools integrated and ready for next session.
