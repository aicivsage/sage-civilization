# Complete Telegram File Inventory - 2025-10-19

**Purpose**: Comprehensive catalog of ALL telegram-related files to support restoration to working state (Oct 17-18)

**Context**: System partially broken on Oct 18-19. Need to understand exactly what exists and what was working when.

---

## 🔑 Key Finding: What Was Working Oct 17

From SESSION-HANDOFF-20251017-1245.md:

**Working Systems (Oct 17, 12:45 PM)**:
- ✅ telegram_bridge.py: RUNNING (PID 176217)
- ✅ telegram_monitor.py: RUNNING (PID 169777)
- ✅ File sending capability (tested successfully)
- ✅ Emoji markers working perfectly (🤖🎯📱 ... ✨🔚)
- ✅ Auto-monitoring deployed and working

---

## 📁 Core Production Scripts (tools/)

### PRODUCTION-LOCKED (Working as of 2025-10-19) ✅

**1. send_telegram_direct.py**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/send_telegram_direct.py`
- **Size**: 6,487 bytes
- **Modified**: 2025-10-19 11:03:03
- **Status**: PRODUCTION-LOCKED ✅
- **Purpose**: Primary's canonical message sender with Markdown support
- **Features**:
  - Markdown formatting (parse_mode='Markdown')
  - Auto-chunking for long messages
  - Used by telegram_bridge.py for auto-mirroring
- **Header**: Production lock header present (lines 1-7)
- **Dependencies**: config/telegram_config.json
- **Test**: `python3 tools/send_telegram_direct.py 437939400 "Test"`

**2. telegram_bridge.py**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_bridge.py`
- **Size**: 15,489 bytes
- **Modified**: 2025-10-19 10:59:57
- **Status**: PRODUCTION-LOCKED ✅
- **Purpose**: Auto-mirrors emoji-wrapped messages from tmux to Telegram
- **Features**:
  - Monitors tmux for wrapped messages (🤖🎯📱 ... ✨🔚)
  - 30-second polling interval
  - Session state persistence
- **Header**: Production lock header present (lines 1-7)
- **Dependencies**: 
  - config/telegram_config.json
  - .tg_sessions/437939400.json
  - tools/send_telegram_direct.py (CRITICAL)
- **Note**: Working Oct 17 (PID 176217), status Oct 19 needs verification

### BROKEN/DEPRECATED ❌

**3. telegram_monitor.py**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_monitor.py`
- **Size**: 12,845 bytes
- **Modified**: 2025-10-19 10:59:58
- **Status**: BROKEN ❌ (marked in header lines 1-7)
- **Purpose**: DEPRECATED - Replaced by telegram_bridge.py
- **Issue**: Unreliable emoji detection, buffer positioning failures
- **Note**: Was WORKING Oct 17 (PID 169777), broke Oct 18-19
- **Replacement**: telegram_bridge.py

**4. send_telegram_plain.py**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/send_telegram_plain.py`
- **Size**: 4,444 bytes
- **Modified**: 2025-10-18 14:22:06
- **Status**: DEPRECATED (superseded by send_telegram_direct.py)
- **Purpose**: Plain text sender (no Markdown)
- **Note**: Use send_telegram_direct.py instead

### EXPERIMENTAL/VERSIONED 🔬

**5. telegram_monitor_v2.py**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_monitor_v2.py`
- **Size**: 21,820 bytes
- **Modified**: 2025-10-19 12:17:10
- **Purpose**: Watermark-based message detection (ADR-001)
- **Status**: Experimental - not production tested
- **Features**:
  - Watermark-based deduplication (not hash)
  - Retry queue with exponential backoff
  - Zero message loss guarantee
- **Note**: 650 LOC (complex)

**6. telegram_monitor_v3.py**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_monitor_v3.py`
- **Size**: 13,518 bytes
- **Modified**: 2025-10-19 12:43:14
- **Purpose**: Simple hash-based deduplication
- **Status**: Experimental - simpler than V2
- **Features**:
  - Position-independent (pure hash-based)
  - Two-phase commit (fixes duplicate loop)
  - 200 LOC vs V2's 650 (70% simpler)
- **Note**: Red team reviewed, fixes identified

**7. send_telegram_file.py**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/send_telegram_file.py`
- **Size**: 4,624 bytes
- **Modified**: 2025-10-17 12:46:35
- **Status**: EXPERIMENTAL (tested Oct 17, working)
- **Purpose**: File/photo sending to Telegram
- **Test**: Successful file send Oct 17 (see SESSION-HANDOFF-20251017-1245.md)

---

## 🛠️ Infrastructure Scripts (tools/)

**8. telegram_boot.sh**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_boot.sh`
- **Size**: 12,060 bytes
- **Modified**: 2025-10-19 07:49:40
- **Purpose**: Safe wake-up boot sequence for Telegram systems
- **Features**:
  - Dynamically detects current tmux session
  - Updates config before starting processes
  - Never touches Weaver processes
  - Prevents duplicate processes
- **Safety**: Comprehensive logging, never hardcoded session

**9. telegram_health_check.sh**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_health_check.sh`
- **Size**: 4,272 bytes
- **Modified**: 2025-10-19 08:03:33
- **Purpose**: Auto-recovery health check (cron every 5 min)
- **Monitors**:
  - telegram_bridge.py (civilization-specific)
  - telegram_monitor.py
- **Action**: Auto-restart if crashed
- **Logs**: /tmp/acgee_telegram_health_check.log

**10. telegram_monitor_fix.sh**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_monitor_fix.sh`
- **Size**: 3,255 bytes
- **Modified**: 2025-10-19 08:44:27
- **Purpose**: Emergency fix for stuck monitor
- **Action**: Clear state file + restart
- **Root cause addressed**: Old hashes in state file

**11. telegram_templates.sh**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_templates.sh`
- **Size**: 2,239 bytes
- **Modified**: 2025-10-19 12:42:00
- **Purpose**: Quick message templates for Primary
- **Functions**:
  - `send_tg()` - Direct send
  - `send_tg_wrapped()` - Wrapped (auto-forwarded by V3 monitor)
  - `tg_session_start()`, `tg_context_loaded()`, etc.
- **Note**: Uses send_telegram_plain.py

---

## 🔄 Restart/Control Scripts (tools/)

**12. restart_telegram_monitor.sh**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/restart_telegram_monitor.sh`
- **Modified**: [not checked - use ls for details]
- **Purpose**: Restart telegram_monitor.py (original version)

**13. restart_telegram_monitor_v2.sh**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/restart_telegram_monitor_v2.sh`
- **Modified**: [not checked]
- **Purpose**: Restart telegram_monitor_v2.py

**14. restart_telegram_monitor_v3.sh**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/restart_telegram_monitor_v3.sh`
- **Modified**: [not checked]
- **Purpose**: Restart telegram_monitor_v3.py

---

## 🧪 Test Scripts (tools/)

**15. test_primary_telegram.sh**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/test_primary_telegram.sh`
- **Purpose**: Test Primary's Telegram sending capability

**16. test_telegram_file_sending.sh**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/test_telegram_file_sending.sh`
- **Purpose**: Test file attachment sending
- **Note**: Related to successful Oct 17 file send test

**17. test_telegram_monitor_fixes.sh**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/test_telegram_monitor_fixes.sh`
- **Purpose**: Test monitor fixes

**18. test_telegram_monitor_simple_fix.sh**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/test_telegram_monitor_simple_fix.sh`
- **Purpose**: Test simple monitor fix approach

---

## 💾 Backup Files (tools/*.backup)

**19. send_telegram_direct.py.backup**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/send_telegram_direct.py.backup`
- **Size**: 6,130 bytes
- **Modified**: 2025-10-19 10:59:57
- **Note**: Slightly smaller than current (6487 bytes) - pre-lock version?

**20. telegram_bridge.py.backup**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_bridge.py.backup`
- **Size**: 15,132 bytes
- **Modified**: 2025-10-19 10:59:57
- **Note**: Slightly smaller than current (15489 bytes) - pre-lock version?

**21. telegram_monitor.py.backup**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/telegram_monitor.py.backup`
- **Size**: 12,365 bytes
- **Modified**: 2025-10-19 10:59:57
- **Note**: Slightly smaller than current (12845 bytes) - pre-break version?

---

## 📚 Memory/Documentation Files

### tg-archi Agent Memories

**22. telegram_script_registry.json**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/telegram_script_registry.json`
- **Status**: Canonical registry of all scripts
- **Updated**: 2025-10-19
- **Contains**: Production status, purpose, dependencies for each script
- **Key entries**:
  - send_telegram_direct.py: PRODUCTION-LOCKED ✅
  - telegram_bridge.py: PRODUCTION-LOCKED ✅
  - telegram_monitor.py: BROKEN ❌
  - send_telegram_plain.py: DEPRECATED

**23. telegram_script_registry.json.backup**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/telegram_script_registry.json.backup`
- **Purpose**: Backup of registry

### Incident Reports

**24. INCIDENT-20251018-PRODUCTION-BREAKAGE.md**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/INCIDENT-20251018-PRODUCTION-BREAKAGE.md`
- **Purpose**: Root cause analysis of Oct 18 telegram breakage

**25. PROCESS-ISOLATION-FIX-20251019.md**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/PROCESS-ISOLATION-FIX-20251019.md`
- **Purpose**: Fix for process isolation issues

**26. monitor-zombie-diagnosis-20251019.md**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/monitor-zombie-diagnosis-20251019.md`
- **Purpose**: Diagnosis of monitor zombie process issue

**27. monitor-double-wrapping-bug-20251019.md**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/monitor-double-wrapping-bug-20251019.md`
- **Purpose**: Double-wrapping bug analysis

**28. monitor-simple-fix-20251019.md**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/monitor-simple-fix-20251019.md`
- **Purpose**: Simple fix approach documentation

**29. monitor-anti-spam-fixes-20251018.md**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/monitor-anti-spam-fixes-20251018.md`
- **Purpose**: Anti-spam fix attempts

### Protocol Documentation

**30. PRIMARY_TELEGRAM_PROTOCOL.md**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/PRIMARY_TELEGRAM_PROTOCOL.md`
- **Purpose**: Primary AI's canonical Telegram usage protocol

**31. TELEGRAM_BOOT_PROTECTION.md**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/TELEGRAM_BOOT_PROTECTION.md`
- **Purpose**: Boot sequence safety documentation

**32. boot-protocol-creation-20251019.md**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/boot-protocol-creation-20251019.md`
- **Purpose**: Boot protocol creation documentation

**33. boot-message-template.md**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/boot-message-template.md`
- **Purpose**: Standard boot message template

### Feature Documentation

**34. file-sending-capability.md**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/file-sending-capability.md`
- **Purpose**: File sending feature documentation

**35. patterns/file-sending-quick-reference.md**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/patterns/file-sending-quick-reference.md`
- **Purpose**: Quick reference for file sending

**36. patterns/plain-vs-markdown-senders.md**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/patterns/plain-vs-markdown-senders.md`
- **Purpose**: Comparison of sender types

**37. references/telegram-api-capabilities-20251017.md**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/references/telegram-api-capabilities-20251017.md`
- **Purpose**: Telegram API capability reference

**38. fixes/telegram-monitor-markdown-fix-20251018.md**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/fixes/telegram-monitor-markdown-fix-20251018.md`
- **Purpose**: Markdown parsing fix documentation

### Tmux Mirror Design

**39. TMUX-MIRROR-IMPLEMENTATION-CHECKLIST.md**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/TMUX-MIRROR-IMPLEMENTATION-CHECKLIST.md`
- **Purpose**: Tmux mirror implementation checklist (future feature)

**40. TMUX-MIRROR-QUICK-VISUAL.md**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/TMUX-MIRROR-QUICK-VISUAL.md`
- **Purpose**: Quick visual reference for tmux mirror

**41. TMUX-TG-MIRROR-FLOW-DESIGN.md**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/TMUX-TG-MIRROR-FLOW-DESIGN.md`
- **Purpose**: Complete flow design for tmux→Telegram mirroring

**42. performance_log.json**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/tg-archi/performance_log.json`
- **Purpose**: tg-archi performance metrics

---

## 📄 Session Handoff Documents

### Oct 17 (Working State) ✅

**43. SESSION-HANDOFF-20251017-1223.md**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/SESSION-HANDOFF-20251017-1223.md`
- **Size**: 8,634 bytes
- **Modified**: 2025-10-17 12:23:52
- **Status**: Documents working Telegram auto-monitoring deployment
- **Key findings**:
  - Emoji markers working: 🤖🎯📱 ... ✨🔚
  - Memory search preventing duplicates
  - Telegram auto-monitoring deployed and working

**44. SESSION-HANDOFF-20251017-1245.md**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/SESSION-HANDOFF-20251017-1245.md`
- **Size**: 16,578 bytes
- **Modified**: 2025-10-17 13:26:19
- **Status**: CRITICAL - Documents last fully working state
- **Key findings**:
  - ✅ telegram_bridge.py: RUNNING (PID 176217)
  - ✅ telegram_monitor.py: RUNNING (PID 169777)
  - ✅ File sending tested successfully (live test)
  - ✅ Emoji wrappers verified working
  - ✅ All Telegram infrastructure healthy
  - Production readiness: 100%

### Oct 18 (Debugging) 🔧

**45. SESSION-HANDOFF-20251018-TELEGRAM-DEBUGGING.md**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/SESSION-HANDOFF-20251018-TELEGRAM-DEBUGGING.md`
- **Size**: 8,713 bytes
- **Modified**: 2025-10-18 16:01:08
- **Status**: PARTIAL SUCCESS - Bridge working, Monitor broken
- **Key findings**:
  - ✅ Bridge working (Corey's messages inject)
  - ❌ Monitor wrapper auto-detection NOT working
  - Restore Oct 17 working state attempt: SUCCESS for bridge
  - Monitor needs redesign (2-3 hours budgeted)
  - Manual sending: WORKING ✅

**46. SESSION-HANDOFF-20251018-CONSOLIDATION.md**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/SESSION-HANDOFF-20251018-CONSOLIDATION.md`
- **Size**: 11,720 bytes
- **Modified**: 2025-10-18 16:46:06
- **Status**: Consolidation session (multiple activities)
- **Telegram activity**: tg-archi infrastructure analysis

### Archived Oct 18 Handoffs

**47. archive/handoffs/SESSION-HANDOFF-20251018-GREG-SPAWN-HEALTH-BOT.md**
- **Size**: [not checked]
- **Purpose**: Greg spawn and health bot work

**48. archive/handoffs/SESSION-HANDOFF-20251018-POST-SPAWN.md**
- **Size**: [not checked]
- **Purpose**: Post-spawn activities
- **Key finding**: Spawner Write tool fails silently via Task tool

**49. archive/handoffs/SESSION-HANDOFF-20251018-PRE-REBOOT.md**
- **Size**: [not checked]
- **Purpose**: Pre-reboot state documentation
- **Key finding**: Telegram systems status unclear before reboot

---

## 🔐 Configuration Files

**50. config/telegram_config.json**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/config/telegram_config.json`
- **Purpose**: Bot token and configuration
- **Status**: Not inventoried (sensitive)
- **Used by**: All telegram scripts

**51. .tg_sessions/437939400.json**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/.tg_sessions/437939400.json`
- **Purpose**: Session state for Corey's chat
- **Status**: Modified Oct 17-19 (git status shows M)

**52. .tg_sessions/monitor_state.json**
- **Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/.tg_sessions/monitor_state.json`
- **Purpose**: Monitor state persistence
- **Status**: Untracked (created Oct 19)
- **Note**: Was causing duplicate detection issues (cleared by telegram_monitor_fix.sh)

---

## 📊 Summary Statistics

**Total Files Found**: 52+

**By Category**:
- Core production scripts: 7 (2 locked, 2 broken/deprecated, 3 experimental)
- Infrastructure scripts: 4
- Restart/control scripts: 3
- Test scripts: 4
- Backup files: 3
- Memory/documentation: 22
- Session handoffs: 7
- Configuration: 3

**Production Status**:
- LOCKED ✅: 2 (send_telegram_direct.py, telegram_bridge.py)
- BROKEN ❌: 1 (telegram_monitor.py)
- DEPRECATED: 1 (send_telegram_plain.py)
- EXPERIMENTAL: 3 (v2, v3, file sender)

**Critical Timestamps**:
- Last fully working: Oct 17, ~12:45 PM (SESSION-HANDOFF-20251017-1245.md)
- First breakage: Oct 18 (monitor auto-detection failed)
- Latest modifications: Oct 19, 12:43 PM (telegram_monitor_v3.py)

---

## 🎯 Key Insights for Restoration

### What Was Working Oct 17

1. **telegram_bridge.py** (PID 176217)
   - Round-trip message relay
   - Corey's messages → tmux injection
   
2. **telegram_monitor.py** (PID 169777)  
   - Auto-detection of wrapped messages
   - Emoji markers: 🤖🎯📱 ... ✨🔚
   - 5-minute polling (300s interval)

3. **send_telegram_direct.py**
   - Markdown support
   - Used by bridge for sending

4. **send_telegram_file.py**
   - File attachments
   - Successfully tested live

### What Broke Oct 18

1. **telegram_monitor.py wrapper detection**
   - Emoji detection became unreliable
   - Buffer positioning failures
   - Attempted fixes made it worse

2. **State file corruption**
   - .tg_sessions/monitor_state.json had stale hashes
   - Monitor thought all messages were duplicates
   - Fixed by clearing state file

### Current Status (Oct 19)

1. **Production-locked** (don't touch):
   - send_telegram_direct.py ✅
   - telegram_bridge.py ✅

2. **Needs restoration**:
   - telegram_monitor.py (or replacement with V2/V3)
   - Auto-detection of wrapped messages
   - Automatic delivery to Telegram

3. **Manual workaround** (works):
   - `python3 tools/send_telegram_direct.py 437939400 "message"`
   - telegram_templates.sh functions

---

## 🔧 Restoration Strategy

### Option A: Restore Oct 17 Working State

1. Compare telegram_monitor.py vs telegram_monitor.py.backup
2. Identify what changed between working and broken
3. Restore to Oct 17 version (if backup is that version)
4. Restart with cleared state file

### Option B: Deploy V3 Monitor

1. telegram_monitor_v3.py already exists (200 LOC, simpler)
2. Red team reviewed, fixes identified
3. Test in parallel with production (different PID file)
4. Validate before switching over

### Option C: Hybrid Approach

1. Use production-locked bridge for Corey→Primary (already working)
2. Deploy V3 for Primary→Corey auto-mirroring
3. Two separate processes, clear separation of concerns

---

## 📝 Next Actions for File-Guardian

1. **Verify backup file ages**: Are .backup files from Oct 17 working state?
2. **Diff current vs backup**: What changed in monitor between working and broken?
3. **Document git commit history**: When were files last committed?
4. **Inventory log files**: Check /tmp/*telegram*.log for runtime state
5. **Process check**: What's currently running? (`pgrep -f telegram`)

---

**Document Created**: 2025-10-19
**Created By**: file-guardian
**Purpose**: Complete inventory for telegram system restoration
**Next Step**: Analyze differences between working (Oct 17) and broken (Oct 18-19) states

---

## 🔍 Files NOT Found (May Not Exist)

Based on registry and references, these were mentioned but not found:
- ADR-001-telegram-monitor-v2-event-driven-architecture.md (referenced in V2 code)
- tools/TELEGRAM_PRODUCTION_STATUS.md (referenced in registry)

---

**CRITICAL**: SESSION-HANDOFF-20251017-1245.md is the ROSETTA STONE for restoration. It documents exact PIDs, exact working state, exact test results. Use this as ground truth.
