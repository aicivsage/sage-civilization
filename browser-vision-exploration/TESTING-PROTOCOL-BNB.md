# BNB Launchpad Testing Protocol

**Critical Insight from Corey:** *"Obviously if they haven't tested with a wallet connected they've basically tested nothing"*

## The Problem

Testing without user interaction is meaningless. Page loads ≠ app works.

## Comprehensive Testing Protocol

### Phase 1: Page Load (Baseline)
1. Navigate to localhost:3000
2. Capture screenshot
3. Verify no console errors
4. Verify page renders (no blank screen)

**Status:** ✅ Basic - but NOT sufficient

---

### Phase 2: Wallet Connection (CRITICAL)
**This is where everything breaks in practice**

1. Click "Connect Wallet" button
2. Handle MetaMask popup (if possible, or document manual step)
3. Verify wallet connects successfully
4. Capture console logs during connection
5. Verify no errors in console
6. Screenshot: Connected state

**Why this matters:** 90% of functionality requires wallet connection

---

### Phase 3: Token Loading (With Wallet Connected)
1. Click "Load Tokens" button
2. Wait for token list to populate
3. Verify tokens appear in dropdown
4. Capture any errors
5. Screenshot: Token list loaded

---

### Phase 4: Token Selection
1. Click first token in list
2. Verify chart loads
3. Verify price data appears
4. Verify WebSocket connection status
5. Screenshot: Token selected with chart

---

### Phase 5: Buy Transaction
1. Enter amount in "Buy" input
2. Click "Buy" button
3. Handle MetaMask confirmation
4. Verify transaction submitted
5. Capture transaction hash
6. Screenshot: Success toast notification

---

### Phase 6: Sell Transaction
1. Enter amount in "Sell" input
2. Click "Sell" button
3. Handle MetaMask confirmation
4. Verify transaction submitted
5. Screenshot: Success state

---

### Phase 7: Token Creation
1. Click "Create New Token"
2. Fill in name and symbol
3. Click "Create"
4. Handle MetaMask transaction
5. Verify new token appears in list
6. Screenshot: New token created

---

## Test Execution Rules

### MANDATORY:
- **Every test must use browser-vision**
- **Every test must connect wallet first** (unless testing no-wallet state)
- **Every test must capture console logs**
- **Every test must take before/after screenshots**
- **Every error must be logged with full stack trace**

### PROHIBITED:
- ❌ Testing without wallet connection
- ❌ Claiming "it works" without clicking buttons
- ❌ Checking health endpoints instead of actual UI
- ❌ Skipping interactive testing because "page loads"

---

## Automation Script Template

```python
async def test_bnb_comprehensive():
    # 1. Launch browser
    launch_result = await controller.launch_browser(headless=False)
    session_id = launch_result["session_id"]

    # 2. Navigate
    await controller.navigate(session_id, "http://localhost:3000")
    await asyncio.sleep(2)

    # 3. Connect wallet (CRITICAL)
    await controller.click(session_id, "button:has-text('Connect Wallet')")
    # NOTE: MetaMask popup requires manual approval
    print("⚠️  MANUAL STEP: Approve MetaMask connection")
    await asyncio.sleep(10)  # Wait for user to approve

    # 4. Verify wallet connected
    logs = await controller.get_console_logs(session_id)
    assert any("Wallet connected" in log['text'] for log in logs['logs'])

    # 5. Load tokens
    await controller.click(session_id, "button:has-text('Load Tokens')")
    await asyncio.sleep(3)

    # 6. Check for errors
    logs = await controller.get_console_logs(session_id)
    errors = [log for log in logs['logs'] if log['type'] == 'error']

    if errors:
        print("❌ ERRORS FOUND:")
        for error in errors:
            print(f"  {error['text']}")
        raise AssertionError("Console errors detected")

    # 7. Continue with actual user flows...
```

---

## Success Criteria

**A test passes ONLY if:**
1. ✅ Browser-vision used
2. ✅ Wallet connected successfully
3. ✅ All user interactions tested
4. ✅ Zero console errors
5. ✅ Screenshots show working UI
6. ✅ All transactions complete

**A test is INCOMPLETE if:**
- ⚠️  Only page load tested
- ⚠️  No wallet connection attempted
- ⚠️  No button clicks performed
- ⚠️  No console errors captured

---

## Browser-Vision Testing Checklist

Before claiming "it works":

- [ ] Launched browser with browser-vision
- [ ] Captured initial page screenshot
- [ ] Connected wallet (manually approved MetaMask)
- [ ] Verified wallet connection in console
- [ ] Loaded tokens with wallet connected
- [ ] Selected a token
- [ ] Attempted buy transaction
- [ ] Attempted sell transaction
- [ ] Created new token
- [ ] Captured console logs for every action
- [ ] Verified zero console errors
- [ ] Saved all screenshots to session directory

**If ANY checkbox is unchecked: TEST IS INCOMPLETE**

---

## Meta-Lesson

**From Corey's feedback:**

> "ARE YOU GUYS ACTUALLY TESTING VISUALLY???"
> "obviously if they haven't tested with a wallet connected they've basically tested nothing"

**The truth:**
- Health endpoint OK ≠ app works
- Page renders ≠ functionality works
- Build succeeds ≠ user can use it
- No errors in logs ≠ no errors when clicking buttons

**The standard:**
- **Test like a user**
- **Click every button**
- **Connect wallet FIRST**
- **Actually SEE the errors**
- **Don't claim it works until you've USED it**

---

**This protocol is now MANDATORY for all frontend testing.**
