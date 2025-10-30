#!/bin/bash
# Telegram Boot Script - Safe wake-up boot sequence
# Created: 2025-10-19
# Purpose: Safely start A-C-Gee Telegram systems on any tmux session
#
# CRITICAL SAFETY FEATURES:
# 1. Dynamically detects current tmux session (never hardcoded)
# 2. Updates config before starting processes
# 3. Never touches Weaver's processes (/grow_openai/)
# 4. Checks for existing A-C-Gee processes (no duplicates)
# 5. Comprehensive logging for debugging

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# ============================================================================
# CONFIGURATION
# ============================================================================

PROJECT_ROOT="/mnt/c/sage/sage-civilization"
CONFIG_FILE="$PROJECT_ROOT/config/telegram_config.json"
LOG_FILE="/tmp/acgee_telegram_boot.log"
BRIDGE_LOG="/tmp/acgee_telegram_bridge.log"
MONITOR_LOG="/tmp/telegram_jsonl_monitor.log"
# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================================================
# LOGGING
# ============================================================================

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log_color() {
    echo -e "${2}[$(date '+%Y-%m-%d %H:%M:%S')] $1${NC}" | tee -a "$LOG_FILE"
}

log_success() { log_color "$1" "$GREEN"; }
log_error() { log_color "$1" "$RED"; }
log_warning() { log_color "$1" "$YELLOW"; }
log_info() { log_color "$1" "$BLUE"; }

# ============================================================================
# SAFETY CHECKS
# ============================================================================

check_in_tmux() {
    if [ -z "${TMUX:-}" ]; then
        log_error "ERROR: Not running inside tmux session!"
        log_error "This script must be run from within tmux."
        exit 1
    fi
}

detect_tmux_session() {
    # Dynamically detect current tmux session
    local session
    session=$(tmux display-message -p '#S' 2>/dev/null)

    if [ -z "$session" ]; then
        log_error "ERROR: Could not detect tmux session"
        exit 1
    fi

    log_info "Detected tmux session: $session"
    echo "$session"
}

check_weaver_protection() {
    # CRITICAL: Ensure we don't kill Weaver's Telegram processes
    local weaver_bridge weaver_monitor

    weaver_bridge=$(ps aux | grep "telegram_bridge.py" | grep "grow_openai" | grep -v grep || true)
    weaver_monitor=$(ps aux | grep "telegram_monitor.py" | grep "grow_openai" | grep -v grep || true)

    if [ -n "$weaver_bridge" ]; then
        log_warning "PROTECTED: Weaver's telegram_bridge.py detected - will NOT touch"
        log_info "Weaver bridge: $weaver_bridge"
    fi

    if [ -n "$weaver_monitor" ]; then
        log_warning "PROTECTED: Weaver's telegram_monitor.py detected - will NOT touch"
        log_info "Weaver monitor: $weaver_monitor"
    fi
}

check_existing_acgee_processes() {
    # Check for existing A-C-Gee processes (only from our directory)
    local bridge_pids monitor_pids

    bridge_pids=$(ps aux | grep "telegram_bridge.py" | grep "grow_gemini_deepresearch" | grep -v grep | awk '{print $2}' || true)
    monitor_pids=$(ps aux | grep "telegram_jsonl_monitor.py" | grep "grow_gemini_deepresearch" | grep -v grep | awk '{print $2}' || true)

    echo "$bridge_pids|$monitor_pids"
}

# ============================================================================
# CONFIGURATION UPDATE
# ============================================================================

update_config() {
    local session="$1"
    local pane="${session}:0.0"

    log_info "Updating config for session: $session (pane: $pane)"

    # Backup existing config
    if [ -f "$CONFIG_FILE" ]; then
        cp "$CONFIG_FILE" "$CONFIG_FILE.backup-$(date +%Y%m%d-%H%M%S)"
        log_success "Config backed up"
    fi

    # Read existing config
    if [ ! -f "$CONFIG_FILE" ]; then
        log_error "ERROR: Config file not found: $CONFIG_FILE"
        exit 1
    fi

    # Update tmux_session and tmux_pane using jq (or python if jq not available)
    if command -v jq &> /dev/null; then
        # Use jq (preferred)
        local temp_config
        temp_config=$(mktemp)
        jq --arg session "$session" --arg pane "$pane" \
           '.tmux_session = $session | .tmux_pane = $pane' \
           "$CONFIG_FILE" > "$temp_config"
        mv "$temp_config" "$CONFIG_FILE"
        log_success "Config updated (via jq)"
    else
        # Fallback to python
        python3 << EOF
import json
with open("$CONFIG_FILE", 'r') as f:
    config = json.load(f)
config['tmux_session'] = "$session"
config['tmux_pane'] = "$pane"
with open("$CONFIG_FILE", 'w') as f:
    json.dump(config, f, indent=2)
EOF
        log_success "Config updated (via python)"
    fi

    # Verify update
    local updated_session
    updated_session=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['tmux_session'])")

    if [ "$updated_session" != "$session" ]; then
        log_error "ERROR: Config update verification failed!"
        log_error "Expected: $session, Got: $updated_session"
        exit 1
    fi

    log_success "Config verified: tmux_session=$session, tmux_pane=$pane"
}

# ============================================================================
# PROCESS MANAGEMENT
# ============================================================================

kill_acgee_processes() {
    local pids="$1"

    if [ -z "$pids" ]; then
        return
    fi

    log_warning "Killing existing A-C-Gee processes: $pids"

    for pid in $pids; do
        if kill "$pid" 2>/dev/null; then
            log_success "Killed process $pid"
        else
            log_warning "Could not kill process $pid (may have already exited)"
        fi
    done

    sleep 2  # Allow processes to terminate
}

start_bridge() {
    log_info "Starting telegram_bridge.py..."

    cd "$PROJECT_ROOT"
    nohup python3 tools/telegram_bridge.py >> "$BRIDGE_LOG" 2>&1 &
    local pid=$!

    sleep 2  # Give it time to start

    # Verify it's running
    if ps -p "$pid" > /dev/null 2>&1; then
        log_success "Bridge started successfully (PID: $pid)"
        echo "$pid"
    else
        log_error "Bridge failed to start! Check $BRIDGE_LOG"
        exit 1
    fi
}

start_jsonl_monitor() {
    log_info "Starting telegram_jsonl_monitor.py (JSONL wrapper monitor)..."

    cd "$PROJECT_ROOT"
    nohup python3 tools/telegram_jsonl_monitor.py --start-from-now >> "$MONITOR_LOG" 2>&1 &
    local pid=$!

    sleep 2  # Give it time to start

    # Verify it's running
    if ps -p "$pid" > /dev/null 2>&1; then
        log_success "JSONL monitor started successfully (PID: $pid)"
        echo "$pid"
    else
        log_error "JSONL monitor failed to start! Check $MONITOR_LOG"
        exit 1
    fi
}

# ============================================================================
# VERIFICATION
# ============================================================================

verify_processes() {
    local bridge_pid="$1"
    local monitor_pid="$2"

    log_info "Verifying processes..."

    local success=true

    # Check bridge
    if ps -p "$bridge_pid" > /dev/null 2>&1; then
        log_success "Bridge verified running (PID: $bridge_pid)"
    else
        log_error "Bridge verification FAILED (PID: $bridge_pid not found)"
        success=false
    fi

    # Check monitor
    if ps -p "$monitor_pid" > /dev/null 2>&1; then
        log_success "Monitor verified running (PID: $monitor_pid)"
    else
        log_error "Monitor verification FAILED (PID: $monitor_pid not found)"
        success=false
    fi

    if [ "$success" = false ]; then
        log_error "BOOT FAILED: One or more processes could not be verified"
        exit 1
    fi

    log_success "All processes verified successfully!"
}

test_injection() {
    local session="$1"

    log_info "Testing tmux injection capability..."

    # Try to inject a test message
    if tmux send-keys -t "${session}:0.0" "" 2>/dev/null; then
        log_success "Tmux injection test passed"
    else
        log_warning "Tmux injection test failed (may not be critical)"
    fi
}

# ============================================================================
# MAIN BOOT SEQUENCE
# ============================================================================

main() {
    log_info "========================================="
    log_info "A-C-Gee Telegram Boot Sequence Starting"
    log_info "========================================="

    # 1. Safety checks
    log_info "Step 1: Safety checks..."
    check_in_tmux
    check_weaver_protection

    # 2. Detect tmux session
    log_info "Step 2: Detecting tmux session..."
    TMUX_SESSION=$(detect_tmux_session)

    # 3. Check existing processes
    log_info "Step 3: Checking for existing A-C-Gee processes..."
    EXISTING_PROCESSES=$(check_existing_acgee_processes)
    EXISTING_BRIDGE=$(echo "$EXISTING_PROCESSES" | cut -d'|' -f1)
    EXISTING_MONITOR=$(echo "$EXISTING_PROCESSES" | cut -d'|' -f2)

    if [ -n "$EXISTING_BRIDGE" ] || [ -n "$EXISTING_MONITOR" ]; then
        log_warning "Found existing A-C-Gee processes:"
        [ -n "$EXISTING_BRIDGE" ] && log_warning "  Bridge PIDs: $EXISTING_BRIDGE"
        [ -n "$EXISTING_MONITOR" ] && log_warning "  Monitor PIDs: $EXISTING_MONITOR"

        read -p "Kill existing processes and restart? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            [ -n "$EXISTING_BRIDGE" ] && kill_acgee_processes "$EXISTING_BRIDGE"
            [ -n "$EXISTING_MONITOR" ] && kill_acgee_processes "$EXISTING_MONITOR"
        else
            log_info "User chose not to restart. Exiting."
            exit 0
        fi
    else
        log_success "No existing A-C-Gee processes found"
    fi

    # 4. Update configuration
    log_info "Step 4: Updating configuration for session $TMUX_SESSION..."
    update_config "$TMUX_SESSION"

    # 5. Start processes
    log_info "Step 5: Starting Telegram processes..."
    BRIDGE_PID=$(start_bridge)
    MONITOR_PID=$(start_jsonl_monitor)

    # 6. Verify processes
    log_info "Step 6: Verifying processes..."
    verify_processes "$BRIDGE_PID" "$MONITOR_PID"

    # 7. Test injection
    log_info "Step 7: Testing tmux injection..."
    test_injection "$TMUX_SESSION"

    # 8. Success summary
    log_success "========================================="
    log_success "A-C-Gee Telegram Boot Complete!"
    log_success "========================================="
    log_success "Tmux Session: $TMUX_SESSION"
    log_success "Bridge PID: $BRIDGE_PID"
    log_success "Monitor PID: $MONITOR_PID"
    log_success "Logs:"
    log_success "  Boot: $LOG_FILE"
    log_success "  Bridge: $BRIDGE_LOG"
    log_success "  Monitor: $MONITOR_LOG"
    log_success "========================================="

    # 9. Display status message for Primary
    echo ""
    echo "Copy this status message for Primary:"
    echo "---"
    cat << EOMSG
Telegram Infrastructure Status:
- Bridge (PID $BRIDGE_PID): Bi-directional Telegram <-> tmux RUNNING
- JSONL Monitor (PID $MONITOR_PID): Auto-sends wrapped messages to Telegram RUNNING
  (watches Claude Code conversation logs, <5s latency)
- Tmux session: $TMUX_SESSION (auto-detected and configured)

Primary reminder:
- Wrap messages for auto-mirroring: 🤖🎯📱 ... ✨🔚
- Direct send: python3 tools/send_telegram_direct.py 437939400 "message"
- File send: python3 tools/send_telegram_file.py 437939400 /path/to/file "caption"
- Templates: source tools/telegram_templates.sh && tg_session_start

Full protocol: memories/agents/tg-archi/PRIMARY_TELEGRAM_PROTOCOL.md
EOMSG
    echo "---"
}

# ============================================================================
# ERROR HANDLING
# ============================================================================

trap 'log_error "Boot script failed at line $LINENO"; exit 1' ERR

# ============================================================================
# EXECUTE
# ============================================================================

main "$@"
