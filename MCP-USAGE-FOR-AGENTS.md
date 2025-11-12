# MCP Code Execution - Quick Start for Agents

**TL;DR**: You can now execute Python and Bash code directly instead of describing what you'd like to see happen. This reduces token usage by 85-92%.

---

## Why Use MCP Code Execution?

**Before MCP** (conversation-based iteration):
```
Agent: "I'll write code to validate the email system..."
[15K tokens describing expected behavior]

Primary: "Does it work?"
[10K tokens asking for clarification]

Agent: "I think so, but I can't test it..."
[15K tokens explaining approach]

Primary: "Let me test... found a bug"
[10K tokens reporting issue]

Agent: "Let me fix that..."
[Another 15K tokens, repeat 2-3x]

Total: 50K+ tokens, 3+ invocations, 4-6 hours
```

**With MCP** (direct execution):
```python
from tools.mcp_sandbox import execute_code

# Write AND test in same invocation
code = """
def validate_email(email):
    return '@' in email and '.' in email.split('@')[1]

# Test it immediately!
assert validate_email('test@example.com') == True
assert validate_email('invalid') == False
print('All tests passed!')
"""

result = execute_code("coder", "python", code)
if result.success:
    print("Validated! Shipping...")
else:
    print(f"Bug found: {result.stderr}")
    # Fix and retry IMMEDIATELY, no new invocation

Total: 8K tokens, 1 invocation, 1-2 hours
```

**Savings: 84% tokens, 4x faster**

---

## Quick Examples

### 1. Validate Your Code (Coder)

```python
from tools.mcp_sandbox import execute_code

# Write function
function_code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)

# Test it yourself!
assert factorial(5) == 120
assert factorial(0) == 1
assert factorial(1) == 1
print('✓ All tests passed')
"""

result = execute_code("coder", "python", function_code)
if result.success:
    print(result.stdout)  # "✓ All tests passed"
    # Now write the actual function to file
else:
    print(f"Test failed: {result.stderr}")
    # Fix bug and retry immediately
```

### 2. Analyze Data (Researcher)

```python
# Instead of asking Primary to check results...
analysis_code = """
import json

with open('research_output.json', 'r') as f:
    data = json.load(f)

total = len(data['results'])
successful = sum(1 for r in data['results'] if r['success'])
failure_rate = (total - successful) / total * 100

print(f'Total: {total}')
print(f'Success rate: {(successful/total)*100:.1f}%')
print(f'Failure rate: {failure_rate:.1f}%')
"""

result = execute_code("researcher", "python", analysis_code)
print(result.stdout)  # Instant insights!
```

### 3. Run Tests (Tester)

```python
# Run full test suite directly
result = execute_code("tester", "bash", "pytest tests/ -v --cov")

if result.exit_code == 0:
    print("✓ All tests passed!")
    # Parse coverage from stdout
    coverage_line = [l for l in result.stdout.split('\n') if 'TOTAL' in l][0]
    print(f"Coverage: {coverage_line}")
else:
    print(f"✗ Test failures:\n{result.stderr}")
    # Report specific failures to coder for fixing
```

### 4. Parse Email (Email-Monitor)

```python
# Instead of describing email structure...
parse_code = """
import re

email_body = '''
Subject: Status Update
Priority: HIGH
Completion: 75%
'''

priority = re.search(r'Priority: (\w+)', email_body).group(1)
completion = re.search(r'Completion: (\d+)%', email_body).group(1)

print(f'Priority: {priority}')
print(f'Completion: {completion}%')
"""

result = execute_code("email-monitor", "python", parse_code)
# Instant structured data extraction
```

---

## Your Execution Policy

Each agent has different permissions:

### Coder (Full Access)
- ✅ Python with write access (can create files)
- ✅ Bash commands: ls, cat, grep, mkdir, find, wc
- ⏱️ 30 second timeout
- 💾 500MB memory

### Researcher (Read-Only Analysis)
- ✅ Python read-only (analyze but don't modify)
- ✅ Bash commands: ls, cat, grep, find, wc, awk, sed
- ⏱️ 60 second timeout (longer for data analysis)
- 💾 1GB memory (more for large datasets)

### Tester (Testing Tools)
- ✅ Python with write access (test files)
- ✅ Bash commands: pytest, python, coverage
- ⏱️ 120 second timeout (for full test suites)
- 💾 500MB memory

### Email-Monitor (Minimal)
- ✅ Python read-only (parse content)
- ❌ No bash access
- ⏱️ 10 second timeout (quick operations)
- 💾 256MB memory

### Other Agents (Default Restrictive)
- ✅ Python read-only
- ✅ Bash read commands only
- ⏱️ 30 second timeout
- 💾 256MB memory

---

## Security Boundaries

### ✅ You CAN:
- Execute Python code (imports: os, json, re, math, datetime, time)
- Read/write files in sandbox (`mcp/servers/sandbox/workspace/`)
- Use whitelisted bash commands
- Run for up to your timeout limit

### ❌ You CANNOT:
- Delete files (`rm` blocked)
- Modify git (`git` blocked)
- Access network (`curl`, `wget`, `ssh` blocked)
- Access system files (`/etc/`, `/home/` blocked)
- Execute privileged commands (`sudo` blocked)
- Import dangerous modules (subprocess, urllib, etc.)

### 🔍 Everything is Audited
- All executions logged to `memories/agents/{your_id}/execution_log.jsonl`
- Includes code, result, duration, security violations
- Use for debugging and performance analysis

---

## Best Practices

### 1. Test Frequently
Don't wait until "done" to test - test as you write:
```python
# Write function
code = "def add(a, b): return a + b\n"

# Test immediately
code += "assert add(2, 3) == 5\n"
code += "print('✓ Works!')\n"

result = execute_code("coder", "python", code)
```

### 2. Handle Errors Gracefully
```python
result = execute_code("coder", "python", code)

if not result.success:
    # Don't just fail - understand why
    print(f"Error: {result.stderr}")
    print(f"Security violations: {result.security_violations}")

    # Fix and retry immediately (no new invocation needed!)
    fixed_code = code.replace("bug", "fix")
    result = execute_code("coder", "python", fixed_code)
```

### 3. Use Relative Paths
Files are relative to sandbox:
```python
# ✅ Correct (relative to sandbox)
code = "open('test.txt', 'w').write('hello')"

# ❌ Wrong (absolute path outside sandbox)
code = "open('/tmp/test.txt', 'w').write('hello')"
```

### 4. Keep Code Simple
Break complex operations into steps:
```python
# Step 1: Read file
result1 = execute_code("researcher", "python", "open('data.json').read()")

# Step 2: Process (if step 1 worked)
if result1.success:
    process_code = f"import json; data = json.loads('''{result1.stdout}''')"
    result2 = execute_code("researcher", "python", process_code)
```

---

## Troubleshooting

### "Timeout exceeded"
- Your code ran too long (check your timeout limit)
- Look for infinite loops
- Break into smaller steps

### "Access denied: file is outside sandbox"
- Use relative paths, not absolute
- All files must be in `mcp/servers/sandbox/workspace/`

### "Command not in whitelist"
- Check your agent policy's allowed commands
- Use allowed alternatives (e.g., `cat` instead of `less`)

### "Import of X is not allowed"
- Only safe modules allowed (os, json, re, math, datetime, time)
- Can't import subprocess, urllib, requests, etc.

---

## When NOT to Use MCP

**Don't use for:**
- File operations in repo (use Write/Edit tools instead)
- Git operations (use Bash tool for git commands)
- Network requests (use appropriate API tools)
- System administration (out of scope)

**Use MCP for:**
- Validating your code works
- Testing functions before writing to files
- Analyzing data quickly
- Running test suites
- Processing text/JSON
- Quick calculations

---

## Full API Reference

See `/mnt/c/sage/sage-civilization/MCP-IMPLEMENTATION-GUIDE.md` for:
- Complete security model
- All agent policies
- Advanced usage patterns
- Token savings analysis
- Troubleshooting guide

---

**Questions?** Check your execution log:
```bash
cat memories/agents/{your_id}/execution_log.jsonl | jq
```

**Need help?** Escalate to Primary with:
- Code that failed
- Error message (result.stderr)
- Security violations (result.security_violations)
- Expected behavior
