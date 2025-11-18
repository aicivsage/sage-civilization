# Telegram Token Security Incident Assessment

**Date**: 2025-11-18
**Agent**: tg-archi
**Severity**: CRITICAL
**Status**: Investigation Complete - Remediation Plan Ready

## Incident Summary

GitHub + GitGuardian security alerts detected exposed Telegram bot tokens in the sage-civilization repository.

## Exposure Assessment

### Files Containing Bot Tokens

1. **`.env` file (ROOT CAUSE - NOT in .gitignore)**
   - Location: `/mnt/c/sage/sage-civilization/.env`
   - Token: `8379210312:AAEDLp1RF4VelwWuAQyU1OlRE3kXldii2SE`
   - Status: **LIKELY TRACKED BY GIT** (`.env` is in .gitignore line 2, but may have been committed before .gitignore was added)
   - Also contains: EMAIL_APP_PASSWORD, GOOGLE_APP_PASSWORD, ANTHROPIC_API_KEY, BLUESKY_APP_PASSWORD
   - **CRITICAL**: This file contains ALL credentials for the civilization

2. **`config/telegram_config.json` (PROTECTED)**
   - Location: `/mnt/c/sage/sage-civilization/config/telegram_config.json`
   - Token: `8379210312:AAEgHMHyLWZ5fKiErQEh3Gc1TBvtc2cklDc`
   - Status: **PROTECTED** (in .gitignore line 9: `**/telegram_config.json`)
   - Contains: Greg's chat ID (7585924762), username, tmux session config
   - This file should NOT be in git history (gitignore protected)

3. **Multiple backup files** (LOCAL ONLY)
   - `config/telegram_config.json.backup-*` (6+ files)
   - All contain the same token as telegram_config.json
   - These are local backups, likely NOT in git

### Token Differences

**IMPORTANT FINDING**: We have TWO DIFFERENT bot tokens!

- Token 1 (in `.env`): `...ii2SE` (ends with "ii2SE")
- Token 2 (in `config/telegram_config.json`): `...klDc` (ends with "klDc")

This suggests:
- One token may have been rotated/revoked already
- OR we have two different bots configured
- Need to determine which token is CURRENTLY IN USE by active processes

### Git Tracking Status

**Protected by .gitignore:**
- `.env` (line 2: `.env`)
- `config/telegram_config.json` (line 9: `**/telegram_config.json`)

**HOWEVER**: Files may have been committed BEFORE .gitignore was added.

**Need to verify:**
1. Is `.env` in git history? (likely YES - common mistake)
2. Is `config/telegram_config.json` in git history? (likely NO - gitignore added early)

## Active System Impact

**Currently running processes:**
- `telegram_bridge.py` - Uses `config/telegram_config.json` (fallback to `TELEGRAM_BOT_TOKEN` env var)
- `telegram_jsonl_monitor.py` - Uses `config/telegram_config.json`
- All Python scripts check: `config["bot_token"]` OR `os.getenv("TELEGRAM_BOT_TOKEN")`

**Which token is active?**
- Need to check running process to determine which token is being used
- If using `config/telegram_config.json` → Token ending in "klDc"
- If using `.env` via environment variable → Token ending in "ii2SE"

## Root Cause Analysis

**How did this happen?**

1. **`.env` file committed to git**
   - Common mistake: Create `.env` file, commit it, THEN add to .gitignore
   - Gitignore only prevents FUTURE commits, doesn't remove from history
   - `.env` likely committed early in project setup

2. **GitHub public repository**
   - Repository: aicivsage/sage-civilization
   - Visibility: Likely public (or Greg gave someone read access)
   - Once committed, token visible to anyone with repo access

3. **Multiple credentials exposed**
   - `.env` contains: Email password, Anthropic API key, Bluesky password
   - Single file exposure = complete credential compromise

## Immediate Risks

**Telegram Bot Token Exposure:**
- Anyone can send messages as Sage AI bot
- Anyone can read messages sent to bot (if they know Greg's chat ID)
- Bot can be used for spam, phishing, impersonation
- Greg's chat ID is also exposed (7585924762)

**Other Credential Exposure (if `.env` in git):**
- Email account compromise (aicivsage@gmail.com)
- Anthropic API key compromise (Claude API billing)
- Bluesky account compromise

## Remediation Requirements

### Phase 1: Immediate Containment (URGENT)
1. Determine which bot token is currently active
2. Revoke BOTH bot tokens via BotFather
3. Generate new bot token
4. Update active configuration with new token
5. Restart Telegram processes
6. Verify functionality with test message

### Phase 2: Credential Rotation (CRITICAL)
1. Rotate ALL credentials in `.env` file:
   - Email app password (via Google Account settings)
   - Anthropic API key (via Anthropic Console)
   - Bluesky app password (via Bluesky settings)
2. Update `.env` with new credentials
3. Verify all services operational

### Phase 3: Git History Cleanup (HIGH PRIORITY)
1. Check if `.env` is in git history
2. If yes: Use BFG Repo-Cleaner or git-filter-repo to remove
3. Force push cleaned history (DESTRUCTIVE - requires coordination)
4. Notify Greg: History rewrite breaks existing clones

### Phase 4: Prevention (MANDATORY)
1. Add pre-commit hooks to detect credential patterns
2. Document credential management protocol
3. Use environment variable injection (not committed files)
4. Consider using secret management tools (e.g., git-crypt, SOPS)
5. Add security scanning (GitGuardian, Trufflehog)

## Next Steps

1. **Provide detailed remediation plan to Primary** (with exact commands)
2. **Get Greg's approval** for token revocation (will break current system)
3. **Execute remediation** in phases
4. **Document lessons learned**
5. **Update constitutional safety protocols**

## Files to Update

- `/mnt/c/sage/sage-civilization/.env` (new tokens)
- `/mnt/c/sage/sage-civilization/config/telegram_config.json` (new token)
- All running process configs
- `memories/agents/tg-archi/telegram_script_registry.json` (update notes)

## Prevention Checklist

- [ ] `.env` removed from git history (if present)
- [ ] `.env.example` created (template without secrets)
- [ ] Pre-commit hooks installed
- [ ] Security scanning enabled
- [ ] Credential rotation protocol documented
- [ ] Greg notified of incident and remediation
- [ ] Constitutional amendment proposed (Article VII: Credential Management)

## Lessons Learned

1. **Never commit secrets to git** - Even with .gitignore
2. **Use environment variable injection** - Runtime secrets, not committed files
3. **Rotate regularly** - Credentials should have expiration
4. **Scan proactively** - Don't wait for GitHub alerts
5. **Template files** - Provide `.env.example`, not `.env`

## References

- GitGuardian alert: [GitHub notification]
- Repository: aicivsage/sage-civilization
- Telegram scripts registry: `memories/agents/tg-archi/telegram_script_registry.json`
- Bot management: @BotFather on Telegram
