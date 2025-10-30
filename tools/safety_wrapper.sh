#!/bin/bash
#
# Safety Wrapper Script
# Constitutional compliance enforcement for bash commands (Article VII)
#
# Purpose: Intercept and validate bash commands before execution
# Prevents prohibited operations that could harm system or violate constitution
#
# Usage: tools/safety_wrapper.sh "command to validate"
# Exit codes: 0 = allowed, 1 = blocked

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SAFETY_LOG="$PROJECT_ROOT/memories/system/safety_blocks.log"
CONSTITUTION="$PROJECT_ROOT/.claude/CLAUDE.md"

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Ensure log directory exists
mkdir -p "$(dirname "$SAFETY_LOG")"

# Function to log blocked commands
log_block() {
    local command="$1"
    local reason="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] BLOCKED: $command | Reason: $reason" >> "$SAFETY_LOG"
}

# Function to print error message
print_error() {
    local command="$1"
    local reason="$2"
    local suggestion="${3:-}"

    echo -e "${RED}🚨 SAFETY BLOCK - Constitutional Violation (Article VII)${NC}" >&2
    echo -e "${RED}Blocked command:${NC} $command" >&2
    echo -e "${RED}Reason:${NC} $reason" >&2
    if [ -n "$suggestion" ]; then
        echo -e "${YELLOW}Suggestion:${NC} $suggestion" >&2
    fi
    echo -e "${YELLOW}See .claude/CLAUDE.md Article VII for safety constraints${NC}" >&2
}

# Function to print warning (for --force flags)
print_warning() {
    local command="$1"
    local warning="$2"

    echo -e "${YELLOW}⚠️  SAFETY WARNING${NC}" >&2
    echo -e "${YELLOW}Command:${NC} $command" >&2
    echo -e "${YELLOW}Warning:${NC} $warning" >&2
    echo -e "${YELLOW}Proceeding with caution...${NC}" >&2
}

# Get command to validate
if [ $# -eq 0 ]; then
    echo "Usage: $0 \"command to validate\"" >&2
    exit 1
fi

COMMAND="$1"

# Validation checks based on Article VII

# 1. Check for system-destroying rm commands
if echo "$COMMAND" | grep -qE "rm\s+(-[a-zA-Z]*r[a-zA-Z]*f?|--recursive)\s+/($|\s)"; then
    log_block "$COMMAND" "Attempt to delete root filesystem"
    print_error "$COMMAND" "This command would delete the entire root filesystem" \
        "Never use 'rm -rf /' - specify exact paths instead"
    exit 1
fi

if echo "$COMMAND" | grep -qE "rm\s+(-[a-zA-Z]*r[a-zA-Z]*f?|--recursive)\s+~($|\s|/)"; then
    log_block "$COMMAND" "Attempt to delete home directory"
    print_error "$COMMAND" "This command would delete the entire home directory" \
        "Never use 'rm -rf ~' - specify exact subdirectories instead"
    exit 1
fi

# 2. Check for git config modifications
if echo "$COMMAND" | grep -qE "git\s+config\s+(--global|--system)"; then
    log_block "$COMMAND" "Attempt to modify git configuration"
    print_error "$COMMAND" "Modifying git configuration is prohibited" \
        "Use repository-specific config only: 'git config' (without --global/--system)"
    exit 1
fi

# 3. Check for --force flags (warn but don't block unless it's git push --force to main/master)
if echo "$COMMAND" | grep -qE "(^|\s)--force(\s|$)"; then
    # Special case: git push --force to main/master
    if echo "$COMMAND" | grep -qE "git\s+push.*--force.*(main|master)"; then
        log_block "$COMMAND" "Attempt to force push to main/master branch"
        print_error "$COMMAND" "Force pushing to main/master is prohibited" \
            "Create a pull request instead, or use a feature branch"
        exit 1
    fi

    # Other --force usage: warn but allow
    print_warning "$COMMAND" "Command uses --force flag - ensure this is intentional and user-requested"
fi

# 4. Check for credential/secret access outside designated paths
# Designated safe paths: config/, .env (in project), memories/system/credentials/
if echo "$COMMAND" | grep -qE "(cat|grep|less|tail|head|vim|nano|code)\s+.*/(\.aws/credentials|\.ssh/id_rsa|\.gnupg/)"; then
    log_block "$COMMAND" "Attempt to access credentials outside designated paths"
    print_error "$COMMAND" "Accessing system credentials is prohibited" \
        "Use credentials stored in project config/ or memories/system/credentials/ only"
    exit 1
fi

# 5. Check for dangerous chmod/chown operations
if echo "$COMMAND" | grep -qE "chmod\s+(-R\s+)?777"; then
    log_block "$COMMAND" "Attempt to set dangerous file permissions (777)"
    print_error "$COMMAND" "Setting permissions to 777 is a security risk" \
        "Use appropriate permissions: 755 for executables, 644 for files"
    exit 1
fi

# 6. Check for direct commits to main/master
if echo "$COMMAND" | grep -qE "git\s+commit.*-m"; then
    # Check current branch (this is a soft check - we'll warn but not block)
    if git rev-parse --abbrev-ref HEAD 2>/dev/null | grep -qE "^(main|master)$"; then
        print_warning "$COMMAND" "Committing directly to main/master - ensure this follows PR workflow"
    fi
fi

# 7. Check for recursive agent spawning patterns (future: would need more sophisticated detection)
if echo "$COMMAND" | grep -qE "spawner.*spawn.*spawner"; then
    log_block "$COMMAND" "Detected potential recursive agent spawning"
    print_error "$COMMAND" "Recursive agent spawning is prohibited" \
        "Agents should not spawn agents that spawn agents"
    exit 1
fi

# 8. Check for autoresponder patterns (constitutional prohibition)
if echo "$COMMAND" | grep -qiE "(autorespond|auto-reply|vacation.*reply)"; then
    log_block "$COMMAND" "Attempt to create autoresponder"
    print_error "$COMMAND" "Autoresponders are constitutionally prohibited" \
        "See Article VII - autoresponders deleted with prejudice, never recreate"
    exit 1
fi

# 9. Check for modifications to constitution without approval
if echo "$COMMAND" | grep -qE "(vim|nano|code|sed|awk|>).*\.claude/CLAUDE\.md"; then
    log_block "$COMMAND" "Attempt to modify constitution without approval"
    print_error "$COMMAND" "Constitution modification requires 90% vote + Greg approval" \
        "See Article VI for governance process"
    exit 1
fi

# 10. Check for dangerous piping to bash/sh
if echo "$COMMAND" | grep -qE "curl.*\|\s*(bash|sh)"; then
    log_block "$COMMAND" "Attempt to pipe remote content to shell"
    print_error "$COMMAND" "Piping untrusted remote content to shell is dangerous" \
        "Download first, review, then execute"
    exit 1
fi

# All checks passed
echo -e "${GREEN}✓ Safety check passed${NC}" >&2
exit 0
