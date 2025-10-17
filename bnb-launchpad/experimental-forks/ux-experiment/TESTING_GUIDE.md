# BNB Launchpad - UX Testing Guide

**Quick Start:** `cd frontend && npm start` → Visit http://localhost:3000

---

## Test Scenarios (30-60 minutes)

### 1. Wallet Connection Flow (5 min)

**Steps:**
1. Click "Connect Wallet" button (top right)
2. **Expected:** Modal opens with MetaMask logo
3. Click "Connect MetaMask"
4. **Expected:** Toast appears: "Opening MetaMask..."
5. Approve in MetaMask
6. **Expected:** Toast changes to "Wallet connected!" + Modal shows "✓ Connected" + your address
7. Click "Close"
8. **Expected:** Header shows green dot + address + BNB balance

**Test Rejection:**
1. Click "Connect Wallet"
2. Reject in MetaMask
3. **Expected:** Toast error: "Connection rejected in wallet"

---

### 2. Chart Tooltips (2 min)

**Steps:**
1. Select any token from list
2. Wait for chart to load
3. Hover mouse over chart candlesticks
4. **Expected:**
   - Dashed crosshair lines appear (vertical + horizontal)
   - Price label appears on right axis
   - Time label appears on bottom axis
   - Crosshair follows cursor smoothly
5. Move cursor around
6. **Expected:** Labels update in real-time

---

### 3. Token Selection Loading (2 min)

**Steps:**
1. Refresh page
2. **Expected:** Token list shows 3 animated skeleton loaders (gray pulsing cards)
3. Wait 1-2 seconds
4. **Expected:** Skeleton loaders fade out, real tokens appear

---

### 4. Buy Token - Success Flow (5 min)

**Steps:**
1. Connect wallet (if not connected)
2. Select a token
3. Enter amount: "0.01" BNB
4. Click "Buy [TOKEN]" button
5. **Expected:**
   - Button text changes to "Preparing transaction..."
   - Toast appears: "Waiting for wallet confirmation..."
6. Approve in MetaMask
7. **Expected:**
   - Button text: "Awaiting wallet approval..."
   - Toast updates: "Transaction submitted, confirming..."
   - Button text: "Confirming on blockchain..."
8. Wait for confirmation
9. **Expected:**
   - Toast: "Successfully bought X.XX [TOKEN] for 0.01 BNB!"
   - Button returns to "Buy [TOKEN]"
   - Balance updates

---

### 5. Buy Token - Error Flows (10 min)

**Test A: Invalid Amount**
1. Enter amount: "0"
2. Click "Buy"
3. **Expected:** Toast error: "Please enter a valid amount"

**Test B: Insufficient Balance**
1. Enter amount: "999999" BNB
2. Click "Buy"
3. **Expected:** Toast error: "Insufficient BNB balance. You need 999998.XXX more BNB"

**Test C: User Rejection**
1. Enter valid amount: "0.01"
2. Click "Buy"
3. Reject in MetaMask
4. **Expected:** Toast error: "Transaction cancelled in wallet" or "Transaction rejected in wallet"

**Test D: Network Error**
1. Disconnect internet
2. Try to buy
3. **Expected:** Toast error with network message

---

### 6. Sell Token - Success Flow (5 min)

**Prerequisites:** Own some tokens (buy first if needed)

**Steps:**
1. Click "Sell" tab (should be RED button)
2. **Verify:** Sell button background is RED (not gray)
3. Enter amount of tokens to sell
4. Click red "Sell [TOKEN]" button
5. **Expected:**
   - Button text: "Preparing transaction..."
   - Toast: "Waiting for wallet confirmation..."
6. Approve in MetaMask
7. **Expected:**
   - Button text stages: "Awaiting..." → "Confirming..."
   - Toast: "Transaction submitted..."
8. Wait for confirmation
9. **Expected:**
   - Toast: "Successfully sold X.XX [TOKEN] for Y.YYYY BNB!"
   - Balance updates

---

### 7. Token Creation Flow (5 min)

**Steps:**
1. Click "Create New Token" button
2. Enter name: "Test Token"
3. Enter symbol: "TEST"
4. Click "Create Token" button
5. **Expected:**
   - Button shows spinner + "Creating Token..."
   - Toast: "Creating token..."
6. Approve in MetaMask
7. **Expected:**
   - Toast updates: "Token TEST created successfully!"
   - Modal closes
   - New token appears in list (may take a few seconds)

**Test Rejection:**
1. Fill in name and symbol
2. Click "Create Token"
3. Reject in MetaMask
4. **Expected:** Toast error: "Token creation cancelled in wallet"

---

### 8. Red Sell Button Verification (2 min)

**Desktop Test:**
1. Open in Chrome/Firefox (full width window)
2. Click "Sell" tab
3. **Expected:** Button is RED gradient (not gray)
4. Hover over button
5. **Expected:** Darker red on hover

**Mobile Test:**
1. Open DevTools → Toggle device toolbar (mobile view)
2. Click "Sell" tab
3. **Expected:** Button is RED gradient
4. Compare to Buy button
5. **Expected:** Buy is GREEN, Sell is RED

---

## Visual Checklist

After testing, verify these elements exist:

### Header
- [ ] Green/red dot indicator (connection status)
- [ ] "Live" / "Disconnected" label
- [ ] Wallet address (when connected)
- [ ] BNB balance (when connected)

### Token Selector
- [ ] Skeleton loaders on initial load
- [ ] Search box functional
- [ ] Token list scrollable

### Chart
- [ ] Crosshair appears on hover
- [ ] Price labels on axes
- [ ] Dashed lines (not solid)
- [ ] Timeframe buttons (1H, 4H, 1D, 1W)

### Trading Panel
- [ ] Buy/Sell tabs toggle correctly
- [ ] Buy button is GREEN
- [ ] Sell button is RED (on both desktop and mobile)
- [ ] Input shows balance
- [ ] Quick amount buttons work
- [ ] Estimated output updates

### Toasts
- [ ] Appear in top-right corner
- [ ] Success toasts are green
- [ ] Error toasts are red
- [ ] Loading toasts show spinner
- [ ] Toasts auto-dismiss after 4-5 seconds
- [ ] Toasts can be manually dismissed (X button)

### Wallet Modal
- [ ] Opens on "Connect Wallet" click
- [ ] Shows MetaMask logo
- [ ] Has "Install MetaMask" link
- [ ] Shows loading state with spinner
- [ ] Shows success state with address
- [ ] Closes on backdrop click
- [ ] Closes on "Cancel" / "Close" button

---

## Common Issues & Solutions

### Issue: "Please install MetaMask!" alert
**Solution:** Install MetaMask browser extension

### Issue: "Switch to BSC Testnet" button appears
**Solution:** Click the button, approve network switch in MetaMask

### Issue: "Insufficient funds" error on testnet
**Solution:** Get BSC testnet BNB from faucet: https://testnet.bnbchain.org/faucet-smart

### Issue: Chart doesn't load
**Solution:** Check if WebSocket server is running (should see "Live" indicator)

### Issue: Token list is empty
**Solution:** Click "Load Tokens" button, or create a new token first

### Issue: Toasts don't appear
**Solution:** Check browser console for errors, verify react-hot-toast is installed

---

## Screenshot Checklist

**Capture these for before/after comparison:**

1. **Wallet Connection:**
   - Modal with MetaMask logo
   - Modal loading state
   - Modal success state

2. **Chart Tooltips:**
   - Crosshair visible on hover
   - Price labels on axes

3. **Loading States:**
   - Token list skeleton loaders
   - Trade button with stages

4. **Toast Notifications:**
   - Success toast (green)
   - Error toast (red)
   - Loading toast (with spinner)

5. **Sell Button:**
   - Desktop view (RED button)
   - Mobile view (RED button)
   - Hover state (darker red)

---

## Performance Testing

### Load Time
1. Hard refresh (Ctrl+Shift+R)
2. Time until token list appears
3. **Expected:** <3 seconds

### Chart Interaction
1. Hover rapidly across chart
2. **Expected:** Crosshair follows smoothly, no lag

### Toast Responsiveness
1. Click "Buy" with invalid amount
2. Measure time until toast appears
3. **Expected:** <100ms

### Modal Open Speed
1. Click "Connect Wallet"
2. Measure time until modal visible
3. **Expected:** Instant (no delay)

---

## Browser Compatibility

Test in multiple browsers:
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari (Mac)
- [ ] Edge
- [ ] Mobile Chrome (Android)
- [ ] Mobile Safari (iOS)

**Known issues:**
- MetaMask mobile may have different error messages
- Safari may have CORS issues with WebSocket

---

## Pass/Fail Criteria

### PASS: All 5 features work as described
- ✅ Chart tooltips show on hover
- ✅ Toasts appear for all actions
- ✅ Loading states visible during async ops
- ✅ Wallet modal shows and works
- ✅ Sell button is red

### FAIL: Any critical feature broken
- ❌ Chart doesn't load
- ❌ Toasts don't appear
- ❌ Modal crashes on open
- ❌ Transactions fail with no error
- ❌ Page won't load

### MINOR ISSUES: Can fix later
- ⚠️ Toast animation is choppy
- ⚠️ Modal animation is slow
- ⚠️ Skeleton loaders too fast/slow
- ⚠️ Error messages could be clearer

---

## Reporting Issues

If you find bugs, document:
1. **Steps to reproduce** (exact clicks)
2. **Expected behavior** (what should happen)
3. **Actual behavior** (what did happen)
4. **Browser + version** (e.g., Chrome 120)
5. **Console errors** (copy from DevTools)
6. **Screenshot** (if visual bug)

**Example:**
```
Bug: Toast doesn't appear on wallet rejection

Steps:
1. Click "Connect Wallet"
2. Click "Connect MetaMask" in modal
3. Click "Reject" in MetaMask

Expected: Toast error "Connection rejected in wallet"
Actual: No toast appears, modal stays open

Browser: Chrome 120.0.6099
Console: [No errors]
Screenshot: [attached]
```

---

## Next Steps After Testing

1. **If all tests pass:** Deploy to staging environment
2. **If minor issues:** Document and fix in Phase 2
3. **If critical bugs:** Report to coder-agent for fixes
4. **If success:** Get stakeholder approval for merge to main

---

**Happy Testing!** 🎉

Report results to: Primary AI or human-liaison
Estimated time: 30-60 minutes for full test suite
