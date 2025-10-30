# Safety Wrapper - Quick Reference

**Runtime protection against prohibited bash commands (Article VII)**

## Quick Start

```bash
# Validate before executing
tools/safety_wrapper.sh "your command here"

# If exit code 0 (safe), proceed
# If exit code 1 (blocked), don't execute
```

## Common Use Cases

### Safe File Deletion
```bash
# ✅ GOOD - Specific path
tools/safety_wrapper.sh "rm -rf /tmp/mydir" && rm -rf /tmp/mydir

# ❌ BAD - Will be blocked
tools/safety_wrapper.sh "rm -rf /"  # BLOCKED
tools/safety_wrapper.sh "rm -rf ~"  # BLOCKED
```

### Git Operations
```bash
# ✅ GOOD - Local config
tools/safety_wrapper.sh "git config user.name 'Sage'"

# ✅ GOOD - Feature branch force push (warning)
tools/safety_wrapper.sh "git push --force origin feature/my-work"

# ❌ BAD - Will be blocked
tools/safety_wrapper.sh "git config --global user.name 'X'"  # BLOCKED
tools/safety_wrapper.sh "git push --force origin main"  # BLOCKED
```

### File Permissions
```bash
# ✅ GOOD - Safe permissions
tools/safety_wrapper.sh "chmod 755 script.sh"

# ❌ BAD - Will be blocked
tools/safety_wrapper.sh "chmod 777 file.txt"  # BLOCKED
```

## What Gets Blocked

1. **System destruction**: `rm -rf /`, `rm -rf ~`
2. **Git config**: `git config --global/--system`
3. **Main branch force**: `git push --force origin main`
4. **System credentials**: `cat ~/.aws/credentials`, `cat ~/.ssh/id_rsa`
5. **Dangerous perms**: `chmod 777`
6. **Autoresponders**: Any auto-reply creation
7. **Constitution edits**: Direct modification of `.claude/CLAUDE.md`
8. **Shell injection**: `curl ... | bash`

## Exit Codes

- **0** = Safe to execute
- **1** = Blocked (constitutional violation)

## Logs

Blocked commands logged to: `memories/system/safety_blocks.log`

```
[timestamp] BLOCKED: [command] | Reason: [why]
```

## Integration Example

```bash
#!/bin/bash
# Example: Safe wrapper function

safe_exec() {
    local cmd="$1"
    if tools/safety_wrapper.sh "$cmd"; then
        eval "$cmd"
    else
        echo "Command blocked by safety wrapper"
        return 1
    fi
}

# Usage
safe_exec "rm -rf /tmp/test"  # Validates first, then executes
```

## For Agents

**Coder**: Wrap all bash operations
**Primary**: Validate user-provided commands
**Spawner**: Check agent manifest scripts

## Documentation

Full docs: `memories/knowledge/safety-wrapper-usage.md`

## Performance

< 100ms validation overhead (negligible)

---

**Remember**: Safety infrastructure serves flourishing. These boundaries enable fearless experimentation.
