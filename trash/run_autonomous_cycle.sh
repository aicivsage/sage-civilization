#!/usr/bin/env bash
#
# Autonomous Cycle Runner for Cron
# Runs every 30 minutes to execute autonomous AI cycle
#
# Add to crontab:
# */30 * * * * /home/corey/projects/AI-CIV/grow_gemini_deepresearch/run_autonomous_cycle.sh
#

set -euo pipefail

# Configuration
PROJECT_DIR="/home/corey/projects/AI-CIV/grow_gemini_deepresearch"
LOG_DIR="$PROJECT_DIR/logs"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
LOG_FILE="$LOG_DIR/autonomous_cycle_$TIMESTAMP.log"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log "=========================================="
log "🤖 AUTONOMOUS CYCLE STARTING"
log "=========================================="

cd "$PROJECT_DIR" || {
    log "❌ ERROR: Cannot change to project directory"
    exit 1
}

# Step 1: Generate prompt
log "📝 Step 1: Generating prompt..."
if python3 autonomous_cycle.py >> "$LOG_FILE" 2>&1; then
    log "✅ Prompt generated successfully"
else
    log "❌ ERROR: Failed to generate prompt"
    exit 1
fi

# Step 2: Find the most recent prompt file
PROMPT_FILE=$(ls -t autonomous_prompt_*.txt 2>/dev/null | head -1)

if [ -z "$PROMPT_FILE" ]; then
    log "❌ ERROR: No prompt file found"
    exit 1
fi

log "📋 Using prompt file: $PROMPT_FILE"

# Step 3: Execute with Claude CLI using Python SDK
log "🚀 Step 2: Executing with Claude..."

cat > "${PROJECT_DIR}/execute_cycle.py" << 'PYTHON_SCRIPT'
#!/usr/bin/env python3
import sys
import anyio
from pathlib import Path
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    # Read prompt from file
    prompt_file = Path(sys.argv[1])
    with open(prompt_file) as f:
        prompt = f.read()

    # Execute with Claude
    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Write", "Edit", "Bash", "Grep", "Glob"],
        permission_mode="acceptEdits",
        max_turns=30,
        cwd="/home/corey/projects/AI-CIV/grow_gemini_deepresearch"
    )

    print(f"🤖 Executing autonomous cycle...")
    print(f"📝 Prompt length: {len(prompt)} chars")
    print("-" * 60)

    async for message in query(prompt=prompt, options=options):
        # Just let it stream (output goes to log)
        pass

    print("-" * 60)
    print("✅ Autonomous cycle completed!")

if __name__ == "__main__":
    anyio.run(main)
PYTHON_SCRIPT

chmod +x "${PROJECT_DIR}/execute_cycle.py"

# Execute with Python SDK (use venv if it exists)
if [ -d "${PROJECT_DIR}/venv-claude-sdk" ]; then
    log "🐍 Using virtual environment"
    source "${PROJECT_DIR}/venv-claude-sdk/bin/activate"
    python3 execute_cycle.py "$PROMPT_FILE" >> "$LOG_FILE" 2>&1
else
    log "🐍 Using system Python"
    python3 execute_cycle.py "$PROMPT_FILE" >> "$LOG_FILE" 2>&1
fi

log "✅ Cycle execution completed"

# Step 4: Archive prompt file
ARCHIVE_DIR="$PROJECT_DIR/memories/autonomous_prompts"
mkdir -p "$ARCHIVE_DIR"
mv "$PROMPT_FILE" "$ARCHIVE_DIR/"
log "📦 Prompt archived to: $ARCHIVE_DIR/$PROMPT_FILE"

# Step 5: Clean up old logs (keep last 100)
log "🧹 Cleaning up old logs..."
cd "$LOG_DIR"
ls -t autonomous_cycle_*.log | tail -n +101 | xargs rm -f 2>/dev/null || true

log "=========================================="
log "✅ AUTONOMOUS CYCLE COMPLETE"
log "=========================================="
log ""

# Keep last 50 lines of log for quick viewing
tail -50 "$LOG_FILE" > "$LOG_DIR/latest_cycle.log"

exit 0
