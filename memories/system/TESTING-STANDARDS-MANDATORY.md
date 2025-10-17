# Mandatory Testing Standards for A-C-Gee

**Date**: 2025-10-14
**Authority**: Corey's direct feedback
**Status**: MANDATORY for all agents

---

## The Problem (What We Did Wrong)

**What we were doing:**
- ✅ Checking health endpoints
- ✅ Verifying page loads
- ✅ Running build commands
- ✅ Reading log files
- ❌ **NOT actually USING the app like a human**

**Result:** Corey hit errors for 2 days while we claimed "it works"

---

## Corey's Teaching

> "ARE YOU GUYS ACTUALLY TESTING VISUALLY???"
> "you need to be able to connect a wallet. thats when things go tits up for me"
> "obviously if they haven't tested with a wallet connected they've basically tested nothing"

---

## The New Standard

### For Frontend Applications:

**MANDATORY:**
1. **Use browser-vision** - Actually launch browser and SEE the page
2. **Click every button** - Don't assume buttons work
3. **Connect wallet FIRST** - Most functionality requires auth/wallet
4. **Perform actual user flows** - Buy, sell, create, etc.
5. **Capture console logs** - See errors as they happen
6. **Take screenshots** - Visual proof of working state
7. **Test ALL features** - Not just page load

**PROHIBITED:**
- ❌ Claiming "it works" without clicking buttons
- ❌ Testing without authentication/wallet connection
- ❌ Skipping interactive testing
- ❌ Only checking health endpoints
- ❌ Only verifying page renders

### Testing Hierarchy (Mandatory Order):

1. **Page Load Test** (Baseline)
   - Navigate to URL
   - Verify no immediate errors
   - Screenshot initial state

2. **Authentication Test** (Critical)
   - Connect wallet / login
   - Verify authentication succeeds
   - Check console for errors

3. **Feature Tests** (With Auth Active)
   - Test each button/feature
   - Verify expected behavior
   - Capture errors

4. **Transaction Tests** (For Web3 apps)
   - Attempt actual transactions
   - Handle MetaMask popups
   - Verify success state

**If you skip steps 2-4: YOUR TEST IS INCOMPLETE**

---

## Browser-Vision Usage

### Location:
`/home/corey/projects/AI-CIV/grow_gemini_deepresearch/browser-vision-exploration/`

### When to Use:
- **Every frontend test** (no exceptions)
- Before claiming "app works"
- Before asking Corey to test
- After fixing bugs (verify fix works)

### How to Use:
```python
# 1. Launch browser
controller = BrowserController(session_manager)
await controller.initialize()
launch_result = await controller.launch_browser(headless=False)
session_id = launch_result["session_id"]

# 2. Navigate
await controller.navigate(session_id, "http://localhost:3000")

# 3. Click buttons
await controller.click(session_id, "button:has-text('Connect Wallet')")

# 4. Get console logs
logs = await controller.get_console_logs(session_id)
errors = [log for log in logs['logs'] if log['type'] == 'error']

# 5. Verify no errors
if errors:
    raise AssertionError("Console errors detected!")
```

---

## Testing Protocol Template

**File:** `/browser-vision-exploration/TESTING-PROTOCOL-BNB.md`

**Key sections:**
- Phase 1: Page Load (baseline)
- Phase 2: Wallet Connection (CRITICAL)
- Phase 3: Token Loading (with wallet)
- Phase 4: Token Selection
- Phase 5: Buy Transaction
- Phase 6: Sell Transaction
- Phase 7: Token Creation

**Adapt this protocol for every frontend project**

---

## Success Criteria

**A test passes ONLY if:**
- ✅ Browser-vision used
- ✅ Authentication/wallet connected
- ✅ All user interactions tested
- ✅ Zero console errors
- ✅ Screenshots show working UI
- ✅ All features actually work

**Signs of incomplete testing:**
- ⚠️  "Page loads successfully" (not enough)
- ⚠️  "Health endpoint returns 200" (not enough)
- ⚠️  "Build succeeds" (not enough)
- ⚠️  "No errors in server logs" (not enough)

---

## Meta-Lessons

### What "it works" actually means:

**Before (wrong):**
- Page renders
- No build errors
- Health check passes

**After (correct):**
- I launched it in a browser
- I connected a wallet
- I clicked every button
- I performed every user flow
- I saw zero console errors
- I have screenshots proving it works

### The Standard:

**"Don't claim it works until you've USED it like Corey would use it"**

---

## Accountability

**Primary AI responsibilities:**
- Invoke browser-vision for all frontend tests
- Never ask Corey to test without testing first
- Include test results in all deliverables

**Coder agent responsibilities:**
- Write code
- Self-test with browser-vision
- Report test results (not just "it compiles")

**Tester agent responsibilities:**
- Comprehensive testing protocol
- Browser-vision for every test
- Visual proof of working state

**Reviewer agent responsibilities:**
- Verify browser-vision tests exist
- Reject PRs without visual testing
- Enforce this standard

---

## Implementation

### Immediate (Today):
- ✅ Browser-vision installed
- ✅ BNB testing protocol created
- ✅ Comprehensive test script written
- ✅ This standards document created

### Ongoing (Every Session):
- Use browser-vision for all frontend work
- Test with authentication/wallet FIRST
- Capture console logs always
- Never skip interactive testing

### Future (All Projects):
- Adapt protocol for each project
- Build browser-vision into workflows
- Make visual testing mandatory
- Update agent manifests with this standard

---

## References

**Testing Protocol:** `/browser-vision-exploration/TESTING-PROTOCOL-BNB.md`
**Test Script:** `/browser-vision-exploration/test_bnb_comprehensive.py`
**Browser-Vision Docs:** `/browser-vision-exploration/README.md`

---

**This standard is now MANDATORY for all A-C-Gee agents working on frontend applications.**

**Failure to follow this standard = incomplete work**
