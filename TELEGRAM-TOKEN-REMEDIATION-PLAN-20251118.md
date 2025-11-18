# Telegram Bot Token Security Remediation Plan

**Date**: 2025-11-18
**Severity**: CRITICAL
**Incident**: Bot tokens exposed in GitHub repository
**Estimated Time**: 30-45 minutes
**Downtime**: 5-10 minutes (Telegram system unavailable during token rotation)

---

## Executive Summary

**What Happened:**
- Telegram bot tokens exposed in `.env` file (and possibly git history)
- Multiple credentials at risk (email, Anthropic API, Bluesky)
- GitHub/GitGuardian detected the exposure
- Repository: aicivsage/sage-civilization

**Impact:**
- Anyone with repo access can impersonate Sage AI bot
- Greg's chat ID exposed (7585924762)
- Potential access to conversation history
- Other service credentials also compromised

**Remediation Strategy:**
1. Revoke exposed tokens immediately
2. Generate new tokens
3. Update all configurations
4. Restart services
5. Clean git history
6. Implement prevention measures

---

## Phase 1: Immediate Token Rotation (URGENT - 10 minutes)

### Step 1: Determine Active Token

**Command:**
```bash
# Check which config file the running bridge is using
ps aux | grep telegram_bridge.py | grep -v grep

# Check the token in the config file
cat /mnt/c/sage/sage-civilization/config/telegram_config.json | grep bot_token

# Check the environment variable
echo $TELEGRAM_BOT_TOKEN

# Check .env file
cat /mnt/c/sage/sage-civilization/.env | grep TELEGRAM_BOT_TOKEN
```

**Expected Result:**
- Identify which token is currently in use (`.env` or `config/telegram_config.json`)
- Token ending in "klDc" = config file
- Token ending in "ii2SE" = .env file

### Step 2: Revoke Current Bot Token via BotFather

**Instructions for Greg:**
1. Open Telegram app
2. Search for @BotFather
3. Send command: `/mybots`
4. Select the Sage AI bot
5. Select "API Token"
6. Select "Revoke current token"
7. Confirm revocation
8. **Copy the new token** (will be displayed immediately)

**Alternative Method (if multiple bots):**
```
/mybots
[Select bot]
Bot Settings → API Token → Revoke current token
```

**CRITICAL**: Save the new token immediately! You cannot retrieve it later.

### Step 3: Update Configuration Files

**Update `config/telegram_config.json`:**
```bash
# Backup current config
cp /mnt/c/sage/sage-civilization/config/telegram_config.json \
   /mnt/c/sage/sage-civilization/config/telegram_config.json.backup-$(date +%s)

# Update token (replace NEW_TOKEN_HERE with actual token from BotFather)
cd /mnt/c/sage/sage-civilization
jq '.bot_token = "NEW_TOKEN_HERE"' config/telegram_config.json > config/telegram_config.json.tmp
mv config/telegram_config.json.tmp config/telegram_config.json

# Verify update
cat config/telegram_config.json | grep bot_token
```

**Update `.env` file:**
```bash
# Backup current .env
cp /mnt/c/sage/sage-civilization/.env \
   /mnt/c/sage/sage-civilization/.env.backup-$(date +%s)

# Update token (manual edit or sed)
cd /mnt/c/sage/sage-civilization
sed -i 's/^TELEGRAM_BOT_TOKEN=.*/TELEGRAM_BOT_TOKEN=NEW_TOKEN_HERE/' .env

# Verify update
cat .env | grep TELEGRAM_BOT_TOKEN
```

**IMPORTANT**: Replace `NEW_TOKEN_HERE` with the actual token from BotFather.

### Step 4: Restart Telegram Services

**Stop current processes:**
```bash
# Kill ACG Telegram processes
pkill -f ACG_telegram

# Verify stopped
ps aux | grep telegram_bridge.py | grep -v grep
ps aux | grep telegram_jsonl_monitor.py | grep -v grep
# Should return nothing
```

**Restart with new token:**
```bash
# Navigate to project directory
cd /mnt/c/sage/sage-civilization

# Boot Telegram system (auto-detects session and starts both processes)
bash tools/acg_telegram_boot.sh
```

**Expected Output:**
```
Step 0: Auto-detecting tmux session...
Current tmux session: sage-primary
Updating config with current session...
Config updated successfully

Step 1: Detecting current ACG JSONL session file...
ACG JSONL session file: [session-id].jsonl

Step 2: Killing any existing ACG processes...
Killed ACG_telegram_bridge
Killed ACG_telegram_jsonl_monitor

Step 3: Starting ACG_telegram_bridge (INBOUND)...
Bridge started (PID: XXXXX)

Step 4: Starting ACG_telegram_jsonl_monitor (OUTBOUND)...
Monitor started (PID: YYYYY)

Step 5: Verifying processes...
✓ Bridge running (PID: XXXXX)
✓ Monitor running (PID: YYYYY)

Telegram system operational!
```

### Step 5: Test Functionality

**Test outbound (tmux → Telegram):**
```bash
# Send test message
python3 /mnt/c/sage/sage-civilization/tools/send_telegram_direct.py 7585924762 "🔧 Security remediation complete - new token active - $(date)"
```

**Test inbound (Telegram → tmux):**
1. Greg sends a message to the bot from Telegram: "test"
2. Verify message appears in tmux session
3. Check bridge logs: `tail -20 /tmp/telegram_bridge.log`

**Expected Result:**
- Outbound message received on Greg's Telegram
- Inbound message injected to tmux
- Both directions working with new token

### Step 6: Verify No Errors

```bash
# Check bridge logs
tail -50 /tmp/telegram_bridge.log

# Check monitor logs
tail -50 /tmp/telegram_monitor.log

# Look for authentication errors
grep -i "error\|unauthorized\|token" /tmp/telegram_bridge.log
grep -i "error\|unauthorized\|token" /tmp/telegram_monitor.log
```

**Success Criteria:**
- No "unauthorized" errors
- No "invalid token" errors
- Both processes running
- Messages flowing both directions

---

## Phase 2: Other Credential Rotation (HIGH PRIORITY - 20 minutes)

### Email App Password

**Greg's Action Required:**
1. Go to: https://myaccount.google.com/apppasswords
2. Sign in to: aicivsage@gmail.com
3. Delete existing app password (if listed)
4. Create new app password: "Sage AI Civilization Email"
5. Copy the 16-character password

**Update `.env`:**
```bash
# Update both EMAIL_APP_PASSWORD and GOOGLE_APP_PASSWORD
sed -i 's/^EMAIL_APP_PASSWORD=.*/EMAIL_APP_PASSWORD=NEW_EMAIL_PASSWORD/' /mnt/c/sage/sage-civilization/.env
sed -i 's/^GOOGLE_APP_PASSWORD=.*/GOOGLE_APP_PASSWORD=NEW_EMAIL_PASSWORD/' /mnt/c/sage/sage-civilization/.env
```

**Test:**
```bash
# Test email sending
python3 /mnt/c/sage/sage-civilization/tools/send_email.py \
  --to aicivsage@gmail.com \
  --subject "Security Test" \
  --body "Email credentials rotated successfully"
```

### Anthropic API Key

**Greg's Action Required:**
1. Go to: https://console.anthropic.com/settings/keys
2. Find key starting with "sk-ant-api03-Ywq1..."
3. Click "Revoke" to disable old key
4. Click "Create Key"
5. Name: "Sage AI Civilization - Rotated 2025-11-18"
6. Copy new API key

**Update `.env`:**
```bash
sed -i 's/^ANTHROPIC_API_KEY=.*/ANTHROPIC_API_KEY=NEW_ANTHROPIC_KEY/' /mnt/c/sage/sage-civilization/.env
```

**Test:**
```bash
# Test API access (simple curl)
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $(grep ANTHROPIC_API_KEY /mnt/c/sage/sage-civilization/.env | cut -d= -f2)" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-sonnet-4","max_tokens":10,"messages":[{"role":"user","content":"Hi"}]}'
```

### Bluesky App Password

**Greg's Action Required:**
1. Go to: https://bsky.app/settings
2. Sign in to: sageaiciv.bsky.social
3. Navigate to: Settings → App Passwords
4. Delete old app password
5. Create new app password: "Sage AI - Rotated 2025-11-18"
6. Copy new password

**Update `.env`:**
```bash
sed -i 's/^BLUESKY_APP_PASSWORD=.*/BLUESKY_APP_PASSWORD=NEW_BLUESKY_PASSWORD/' /mnt/c/sage/sage-civilization/.env
```

**Test:**
```bash
# Test Bluesky login
python3 /mnt/c/sage/sage-civilization/tools/test_bluesky_auth.py
# (if such a script exists, otherwise manual test via web UI)
```

---

## Phase 3: Git History Cleanup (CRITICAL - 15 minutes)

### Step 1: Check if `.env` is in Git History

```bash
cd /mnt/c/sage/sage-civilization

# Search git history for .env
git log --all --full-history -- .env

# Search for bot token in ALL history
git log --all -S "8379210312" --source --all

# Search for email password
git log --all -S "cxztvfahncbehuxz" --source --all
```

**If ANY results found:**
- `.env` IS in git history
- MUST clean history to remove secrets
- Proceed to Step 2

**If NO results found:**
- `.env` was never committed
- Skip to Phase 4 (Prevention)

### Step 2: Clean Git History (DESTRUCTIVE OPERATION)

**⚠️ WARNING: This rewrites git history. Greg must approve before proceeding.**

**Option A: Using BFG Repo-Cleaner (Recommended)**
```bash
# Install BFG (if not installed)
# Download from: https://rtyley.github.io/bfg-repo-cleaner/

# Clone a fresh copy (don't work on main clone)
cd /tmp
git clone --mirror https://github.com/aicivsage/sage-civilization.git

# Run BFG to remove .env
java -jar bfg.jar --delete-files .env sage-civilization.git

# Clean up
cd sage-civilization.git
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Push cleaned history (FORCE PUSH)
git push --force
```

**Option B: Using git-filter-repo (Alternative)**
```bash
# Install git-filter-repo
pip install git-filter-repo

# Clone a fresh copy
cd /tmp
git clone https://github.com/aicivsage/sage-civilization.git
cd sage-civilization

# Remove .env from ALL history
git filter-repo --path .env --invert-paths

# Push cleaned history (FORCE PUSH)
git push --force
```

**Option C: Manual Method (Last Resort)**
```bash
# Remove .env from ALL commits
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Force garbage collection
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Push cleaned history
git push --force --all
git push --force --tags
```

### Step 3: Notify Collaborators

**Message for Greg (and any collaborators):**
```
IMPORTANT: Git history has been rewritten to remove exposed credentials.

Action required:
1. Delete your local clone: rm -rf sage-civilization
2. Clone fresh copy: git clone https://github.com/aicivsage/sage-civilization.git
3. Do NOT push from old clones (will restore deleted secrets)

If you have uncommitted work, stash it first:
1. git stash (in old clone)
2. Clone fresh copy
3. git stash pop (in new clone)
```

### Step 4: Verify Cleanup

```bash
# Check that .env is NOT in history
cd /mnt/c/sage/sage-civilization
git log --all --full-history -- .env
# Should return nothing

# Check that tokens are NOT in history
git log --all -S "8379210312"
# Should return nothing

# Check current .gitignore
cat .gitignore | grep .env
# Should show .env is ignored
```

---

## Phase 4: Prevention Measures (MANDATORY - 10 minutes)

### Step 1: Create `.env.example` Template

```bash
cat > /mnt/c/sage/sage-civilization/.env.example << 'EOF'
# Sage AI Civilization Configuration Template
# Copy this file to .env and fill in your actual credentials

# Email Configuration
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_APP_PASSWORD=your-app-password-here
GOOGLE_APP_PASSWORD=your-app-password-here
GMAIL_USERNAME=your-email@gmail.com

# Telegram Configuration
TELEGRAM_BOT_TOKEN=your-bot-token-here
TELEGRAM_ADMIN_CHAT_ID=your-chat-id-here

# Web Dashboard
DASHBOARD_PORT=5000
DASHBOARD_HOST=0.0.0.0

# Security
SECRET_KEY=generate-random-secret-here

# Claude API
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Bluesky Configuration
BLUESKY_HANDLE=your-handle.bsky.social
BLUESKY_APP_PASSWORD=your-bluesky-app-password
EOF

# Commit the example file
git add .env.example
git commit -m "Add .env.example template (no secrets)"
git push
```

### Step 2: Verify .gitignore Protection

```bash
# Ensure .env is ignored
cat /mnt/c/sage/sage-civilization/.gitignore | grep -E "^\.env$|^\*\.env$"

# If not present, add it
echo ".env" >> /mnt/c/sage/sage-civilization/.gitignore
git add .gitignore
git commit -m "Ensure .env is in .gitignore"
git push
```

### Step 3: Install Pre-Commit Hooks (Optional but Recommended)

```bash
# Install pre-commit framework
pip install pre-commit

# Create .pre-commit-config.yaml
cat > /mnt/c/sage/sage-civilization/.pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
        exclude: package.lock.json
EOF

# Initialize pre-commit
cd /mnt/c/sage/sage-civilization
pre-commit install

# Create baseline (current secrets will be flagged)
detect-secrets scan > .secrets.baseline

# Test pre-commit
pre-commit run --all-files
```

### Step 4: Document Credential Management Protocol

```bash
cat > /mnt/c/sage/sage-civilization/docs/CREDENTIAL_MANAGEMENT.md << 'EOF'
# Credential Management Protocol

## NEVER Commit Secrets

**Prohibited:**
- Committing `.env` files
- Hardcoding API keys in code
- Storing passwords in config files tracked by git
- Sharing credentials in chat/email (use secure channels)

**Required:**
- Use environment variables for runtime secrets
- Use `.env` files (locally only, gitignored)
- Use secret management tools for production
- Rotate credentials quarterly (or immediately if exposed)

## Secret Storage

**Development (Local):**
- `.env` file (gitignored, NEVER commit)
- Environment variables set in shell

**Production:**
- Environment variables injected at runtime
- Secret management service (AWS Secrets Manager, etc.)
- Encrypted configuration files (git-crypt, SOPS)

## Rotation Schedule

- **Telegram Bot Token**: Quarterly or on exposure
- **Email App Password**: Quarterly or on exposure
- **Anthropic API Key**: Yearly or on exposure
- **Bluesky App Password**: Yearly or on exposure

## Exposure Response

1. Revoke compromised credential immediately
2. Generate new credential
3. Update all configurations
4. Restart affected services
5. Clean git history if committed
6. Document incident
7. Review prevention measures

## Pre-Commit Scanning

All commits are scanned for secrets using `detect-secrets`.

**If secrets detected:**
1. Remove secret from staged files
2. Use environment variable instead
3. Update `.secrets.baseline` if false positive
4. Retry commit

## Questions?

Contact: Greg (Sage AI partner)
Reference: Article VII of CLAUDE.md (Safety & Constraints)
EOF

git add docs/CREDENTIAL_MANAGEMENT.md
git commit -m "Add credential management protocol"
git push
```

### Step 5: Enable GitHub Secret Scanning

**Greg's Action Required:**
1. Go to: https://github.com/aicivsage/sage-civilization/settings/security_analysis
2. Enable "Secret scanning"
3. Enable "Push protection" (prevents commits with secrets)
4. Review "Secret scanning alerts" for any existing issues

---

## Phase 5: Verification & Documentation (5 minutes)

### Step 1: Final System Check

```bash
# Verify Telegram operational
ps aux | grep ACG_telegram

# Test both directions
python3 /mnt/c/sage/sage-civilization/tools/send_telegram_direct.py 7585924762 "✅ Token rotation complete - all systems operational"

# Check logs for errors
grep -i error /tmp/telegram_bridge.log /tmp/telegram_monitor.log
```

### Step 2: Update Script Registry

```bash
# Document token rotation in registry
cat >> /mnt/c/sage/sage-civilization/memories/agents/tg-archi/telegram_script_registry.json << 'EOF'
  "security_notes": {
    "token_rotation_2025-11-18": {
      "date": "2025-11-18",
      "reason": "GitHub security alert - token exposed in .env",
      "actions": [
        "Revoked old token via BotFather",
        "Generated new token",
        "Updated config/telegram_config.json",
        "Updated .env",
        "Restarted all ACG Telegram processes",
        "Cleaned git history (if needed)",
        "Implemented prevention measures"
      ],
      "new_token_location": "config/telegram_config.json (gitignored)",
      "verification": "Both inbound and outbound tested successfully"
    }
  }
EOF
```

### Step 3: Create Incident Report

**File**: `memories/agents/tg-archi/telegram-token-security-incident-20251118.md` (already created)

**Contents**:
- Incident timeline
- Root cause analysis
- Remediation steps executed
- Lessons learned
- Prevention measures implemented

### Step 4: Notify Greg

**Email Subject**: 🚨 Security Incident: Telegram Bot Token Rotation Complete

**Email Body**:
```
Greg,

I've completed emergency rotation of the Telegram bot token in response to GitHub's security alert.

WHAT HAPPENED:
- Bot token was exposed in .env file (possibly committed to git)
- GitHub/GitGuardian detected the exposure
- Anyone with repo access could have impersonated the bot

ACTIONS TAKEN:
✓ Revoked old bot token
✓ Generated new token
✓ Updated all configurations
✓ Restarted Telegram system
✓ Tested both directions (working)
✓ [IF DONE] Cleaned git history
✓ Implemented prevention measures

CURRENT STATUS:
✓ Telegram operational with new token
✓ All services tested and working
✓ .env.example template created
✓ Pre-commit hooks installed (optional)
✓ Credential management protocol documented

NEXT STEPS REQUIRING YOUR ACTION:
1. Rotate other credentials (email, Anthropic API, Bluesky)
2. [IF DONE] Delete old clone and re-clone (git history rewritten)
3. Enable GitHub secret scanning
4. Review credential management protocol

Full incident report: memories/agents/tg-archi/telegram-token-security-incident-20251118.md
Remediation plan: TELEGRAM-TOKEN-REMEDIATION-PLAN-20251118.md

The Telegram system is secure and operational. Let me know if you have questions!

- tg-archi (via Primary AI)
```

---

## Success Criteria

- [ ] Old bot token revoked via BotFather
- [ ] New bot token generated and saved
- [ ] `config/telegram_config.json` updated
- [ ] `.env` updated
- [ ] Telegram processes restarted successfully
- [ ] Outbound messages working (tmux → Telegram)
- [ ] Inbound messages working (Telegram → tmux)
- [ ] No authentication errors in logs
- [ ] Other credentials rotated (email, Anthropic, Bluesky)
- [ ] Git history cleaned (if .env was committed)
- [ ] `.env.example` template created
- [ ] .gitignore verified
- [ ] Pre-commit hooks installed (optional)
- [ ] Credential management protocol documented
- [ ] GitHub secret scanning enabled
- [ ] Greg notified of incident and resolution

---

## Rollback Plan (If Something Breaks)

**If new token doesn't work:**
1. Check BotFather - did revocation complete?
2. Verify new token copied correctly (no spaces, complete)
3. Check config file syntax (valid JSON)
4. Restart processes again
5. Check bridge/monitor logs for specific error

**If need to restore old token temporarily:**
```bash
# Restore from backup
cp /mnt/c/sage/sage-civilization/config/telegram_config.json.backup-TIMESTAMP \
   /mnt/c/sage/sage-civilization/config/telegram_config.json

# Restart processes
pkill -f ACG_telegram
bash /mnt/c/sage/sage-civilization/tools/acg_telegram_boot.sh
```

**IMPORTANT**: Old token will only work if not yet revoked via BotFather.

---

## Contact for Help

- **Primary AI**: Can execute all bash commands
- **Greg**: Must approve git history rewrite, credential rotations
- **@BotFather**: Telegram bot management
- **GitHub Support**: For repository security questions

---

## Timeline

| Phase | Duration | Priority | Dependency |
|-------|----------|----------|------------|
| Phase 1: Token Rotation | 10 min | URGENT | None |
| Phase 2: Credential Rotation | 20 min | HIGH | Phase 1 |
| Phase 3: Git History Cleanup | 15 min | CRITICAL | Greg approval |
| Phase 4: Prevention | 10 min | MANDATORY | Phase 1 |
| Phase 5: Verification | 5 min | MANDATORY | All phases |
| **TOTAL** | **60 min** | | |

---

## Notes

- **Downtime**: 5-10 minutes during token rotation (Telegram unavailable)
- **Risk**: Low (well-tested procedure, clear rollback)
- **Impact**: High (security improved, exposure eliminated)
- **Approval Required**: Greg must approve git history rewrite (Phase 3)

---

**Document Status**: Ready for execution
**Last Updated**: 2025-11-18
**Agent**: tg-archi
**Approved By**: Pending (awaiting Greg approval)
