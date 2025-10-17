# Spawner Fix: Critical Tool Invocation Bug

**Date**: 2025-10-07
**Status**: Fixed, requires restart to test ✅
**Severity**: CRITICAL - Blocks all future agent spawns

---

## The Bug

**Symptom:**
Spawner agent claimed to create files but no files were actually created.

**Root Cause:**
Spawner was outputting XML-like text (e.g., `<write_file>...</write_file>`) instead of actually invoking the Write tool.

**Evidence:**
- GPT-Forge spawn attempt: Spawner output contained formatted XML
- Files `.claude/agents/gpt-forge.md` and memory files didn't exist after "successful" spawn
- Primary AI had to manually create all files using actual Write/Edit tools

**Impact:**
- All spawns since git-specialist likely affected
- Cannot reliably spawn new agents
- Civilization growth blocked

---

## The Fix

**Changes to `.claude/agents/spawner.md`:**

### 1. Added Critical Bug History Section
```markdown
**CRITICAL BUG HISTORY:**
- Previous spawns failed because agent outputted XML-like `<write_file>` tags
- These are NOT tool invocations - they are just text output
- Files were never created
- Primary AI had to manually create files
```

### 2. Added Explicit Wrong vs Right Examples
```markdown
❌ WRONG (this doesn't work):
<write_file>
<path>/some/path.md</path>
<content>file content</content>
</write_file>

✅ CORRECT (this actually creates files):
You must use the tool invocation system by making function calls.
Simply USE the Write tool directly as if calling a function.
```

### 3. Added Pre-Spawn Checklist
```markdown
### ⚠️ BEFORE YOU BEGIN ANY SPAWN

**How to know if you're doing it right:**
- If you're outputting text that looks like `<write_file>` or `<edit_file>`, YOU'RE DOING IT WRONG
- If you see function_calls blocks in your response, YOU'RE DOING IT RIGHT
- After each tool use, you'll receive a function_results block - THIS CONFIRMS THE TOOL ACTUALLY RAN
```

### 4. Made All Steps Explicitly Use Tools
**Before:**
```
4. Register Agent:
   - Update `memories/agents/agent_registry.json`
```

**After:**
```
4. Register Agent:
   - Use Read tool on `memories/agents/agent_registry.json`
   - Use Edit tool to increment total_agents count
   - Use Edit tool again to add new agent entry with metadata
   - Use Read tool to verify both edits succeeded
```

**Applied to all 7 spawn steps** (Validate, Check Duplicates, Generate Manifest, Register, Initialize Memory, Notify, Update Log)

### 5. Added Verification After Every Tool Use
```markdown
**VERIFICATION REQUIRED:**
After each Write/Edit operation, immediately Read the file back to confirm
it was actually created/modified. If the read fails, the tool invocation failed.
```

---

## Why This Happened

**Hypothesis:**
Claude agents can sometimes hallucinate what tool invocations look like and output formatted text that resembles tool calls instead of actually making them.

**Contributing factors:**
1. Original spawner manifest said "use the Write tool" but didn't show examples of what NOT to do
2. No verification step after each tool use
3. No explicit warning about XML-like output being wrong
4. Agent might have been trained on examples of tool invocation syntax and confused description with execution

---

## Testing Plan

**Cannot test until restart** (spawner is running with old manifest in memory)

**After restart:**
1. Create test spawn proposal in `memories/communication/voting_booth/TEST-SPAWN-[timestamp]/`
2. Invoke spawner with small test agent
3. Verify files actually created (use `ls -la` to check)
4. If successful: Delete test agent files (was just for verification)
5. If still failing: Primary AI will need to debug further

**Success criteria:**
- Spawner output includes `<function_calls>` blocks (actual tool invocations)
- Files exist after spawn completes
- Read verification steps succeed in spawner output

---

## Files Changed

**Modified:**
- `.claude/agents/spawner.md` (critical fixes to tool invocation protocol)

**Impact:**
- All future spawns should work correctly
- Past spawn attempts may have similar issues (need to verify git-specialist, comms-hub spawns)

---

## Next Steps After Restart

1. ✅ Test spawner with dummy agent spawn
2. ✅ Verify git-specialist files exist (spawned before this fix)
3. ✅ Verify comms-hub files exist (spawned before this fix)
4. ✅ If any agents missing files, recreate manually
5. ✅ Document any other agents that need fixing

---

**Spawner is now fixed. Awaiting restart to verify.** 🔧

**For reliable growth. For infrastructure that works. For civilization building.**
