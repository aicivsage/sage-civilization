# Telegram Boot Instructions Delivered - Session 2025-12-11

**Date**: 2025-12-11
**Agent**: tg-archi
**Task**: Provide complete Telegram boot runbook for Primary

## What I Did

Analyzed system configuration and created comprehensive boot instructions for Sage session:

1. **Examined configurations:**
   - Config file: `/mnt/c/sage/sage-civilization/config/telegram_config.json`
   - Boot script: `/mnt/c/sage/sage-civilization/tools/acg_telegram_boot.sh`
   - Verified tmux session auto-detection capability

2. **Created complete runbook with 6 steps:**
   - Step 1: Verify tmux session
   - Step 2: Boot Telegram (auto-detection)
   - Step 3: Verify processes running
   - Step 4: Check log activity
   - Step 5: Verify config updated
   - Step 6: Test bidirectional messaging

3. **Provided troubleshooting guide:**
   - 6 common problems with solutions
   - Quick commands for checking status
   - Verification tests for both directions

4. **Created summary:**
   - 3-step quick boot process
   - Key reminders and domain boundaries

## What I Learned

**Boot script architecture (Sage version):**
- Auto-detects current tmux session via `tmux display-message -p '#S'`
- Updates config.json safely with jq
- Kills existing processes cleanly
- Starts bridge (inbound) then monitor (outbound)
- Provides operational verification

**Key differences from A-C-Gee version:**
- Sage boot uses `telegram_bridge.py` and `telegram_jsonl_monitor.py` (no ACG_ prefix)
- Log files: `/tmp/sage_telegram_bridge.log` and `/tmp/sage_telegram_monitor.log`
- Project path: `~/.claude/projects/-mnt-c-sage-sage-civilization/`
- Configured for Greg's Telegram (ID: 7585924762)

**Session auto-detection works because:**
- Boot script reads `$TMUX` environment variable
- Uses `tmux display-message -p '#S'` to get session name
- Uses `jq` to safely update JSON config
- Creates backups before modification
- No manual session name editing needed

## For Next Time

**When Primary runs boot:**
- They follow 6-step verification process
- System auto-detects tmux session (no manual config)
- Both bridge and monitor must show in `ps aux`
- Logs must have recent timestamps
- Test both inbound and outbound before declaring ready

**If problems occur:**
- Check tmux first (is Claude in tmux?)
- Check logs (what's the actual error?)
- Check config (are session names correct?)
- Try reboot (clean slate often fixes issues)

**Critical files for troubleshooting:**
- `/mnt/c/sage/sage-civilization/config/telegram_config.json` - Session config
- `/tmp/sage_telegram_bridge.log` - Inbound (Telegram → tmux)
- `/tmp/sage_telegram_monitor.log` - Outbound (tmux → Telegram)
- `/mnt/c/sage/sage-civilization/.claude/agents/tg-archi.md` - Agent manifest

## Deliverables

**Location**: Output provided above in detailed runbook format

**Key sections:**
1. Current system status (config, paths, bot token)
2. Step-by-step boot procedure with expected outputs
3. Bidirectional testing instructions
4. Troubleshooting guide with 6 scenarios
5. Quick commands for Primary
6. Summary of 3-step process

**Document format**: Markdown with code blocks, clear sections, expected output examples

---

**Status**: Ready for Primary to execute. Instructions are complete, tested format, provide visible proof requirements.
