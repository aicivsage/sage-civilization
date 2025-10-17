# Potential Issues Analysis - BNB Launchpad Frontend

**Date**: 2025-10-14
**Status**: Analysis based on code review
**Next Step**: Test with proper error logging to see actual error

---

## Most Likely Crash Causes

Based on code review and the `[object Object]` error pattern, here are the most probable causes of the runtime crash:

### 1. WebSocket Connection Failure (HIGH PROBABILITY)

**Evidence**:
```typescript
// src/hooks/useWebSocket.ts
const newSocket = io(WS_CONFIG.URL, {
  reconnection: true,
  reconnectionAttempts: WS_CONFIG.RECONNECTION_ATTEMPTS,
  reconnectionDelay: WS_CONFIG.RECONNECTION_DELAY,
});
```

**Issue**: If the WebSocket backend isn't running on port 4000, socket.io can throw errors that crash the app.

**How to verify**:
```bash
# Check if backend is running
curl http://localhost:4000/health
# OR
netstat -tlnp | grep 4000
```

**Fix if backend not running**:
```bash
cd ../../backend
npm start
```

**Graceful handling** (if we want app to work without backend):
```typescript
newSocket.on('connect_error', (error) => {
  console.error('WebSocket connection error:', error);
  // Don't crash - just show disconnected state
});
```

---

### 2. MetaMask Not Installed (MEDIUM PROBABILITY)

**Evidence**:
```typescript
// src/hooks/useWallet.ts
const initializeProvider = useCallback(async () => {
  if (window.ethereum) {
    const web3Provider = new ethers.providers.Web3Provider(window.ethereum);
    // ...
  }
}, []);
```

**Issue**: If user doesn't have MetaMask installed, accessing `window.ethereum` properties might fail.

**Current protection**: Code checks `if (window.ethereum)` - should be safe

**Potential issue**: If MetaMask is installed but in a weird state (locked, error state), ethers.js constructor might throw.

**How to verify**: Open browser without MetaMask extension

**Better protection**:
```typescript
const initializeProvider = useCallback(async () => {
  if (!window.ethereum) {
    console.log('No Web3 provider detected');
    return;
  }

  try {
    const web3Provider = new ethers.providers.Web3Provider(window.ethereum);
    setProvider(web3Provider);

    const accounts = await web3Provider.listAccounts();
    // ... rest of logic
  } catch (error) {
    console.error('Failed to initialize Web3 provider:', error);
    // Don't crash - just show "Connect Wallet" button
  }
}, []);
```

---

### 3. Contract Address Invalid (MEDIUM PROBABILITY)

**Evidence**:
```typescript
// src/utils/constants.ts
export const CONTRACTS = {
  FACTORY: '0x5FD5a0914864B4A28fA7423b8BFAf436F210CEfC',
  // ...
};

// src/hooks/useContract.ts
const contract = new ethers.Contract(
  CONTRACTS.FACTORY,
  FACTORY_ABI,
  signer || provider
);
```

**Issue**: If contract isn't deployed at that address on the current network, calls to it will fail.

**How to verify**:
1. Check current network in MetaMask
2. Visit https://testnet.bscscan.com/address/0x5FD5a0914864B4A28fA7423b8BFAf436F210CEfC
3. See if contract exists

**Current protection**: Contract calls are in try-catch blocks - should be safe

**Potential issue**: Contract creation itself doesn't throw, but first call might crash React if not in try-catch.

---

### 4. Environment Variables Not Loaded (LOW PROBABILITY)

**Evidence**:
```typescript
// src/utils/constants.ts
export const WS_CONFIG = {
  URL: process.env.REACT_APP_WEBSOCKET_URL || process.env.REACT_APP_API_URL || 'http://localhost:4000',
  // ...
};
```

**Issue**: React requires env vars to start with `REACT_APP_` and be present at build time.

**How to verify**:
```bash
# Check if .env exists
cat .env

# Verify env vars are loaded (in browser console)
console.log(process.env.REACT_APP_WEBSOCKET_URL)
```

**Current protection**: Fallback to 'http://localhost:4000' - should be safe

**Note**: .env file exists and is properly configured, so this is unlikely.

---

### 5. React Strict Mode Double-Rendering (LOW PROBABILITY)

**Evidence**:
```typescript
// src/index.tsx
root.render(
  <React.StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </React.StrictMode>
);
```

**Issue**: React.StrictMode intentionally double-invokes effects and hooks in development to catch bugs.

**Potential problem**: If hooks have side effects that aren't properly cleaned up, this can cause issues.

**Current code review**:
- useWallet has cleanup: ✅
- useWebSocket has cleanup: ✅
- useContract has cleanup: ❌ (but contract creation is synchronous, so OK)

**Not likely the issue**, but could remove `<React.StrictMode>` for testing.

---

### 6. Circular Dependency or Import Order (LOW PROBABILITY)

**Issue**: If modules import each other in a circular way, JavaScript can throw errors during module initialization.

**How to verify**: Check build warnings
```bash
npm run build 2>&1 | grep -i "circular"
```

**Current status**: Build succeeded with only eslint warnings - no circular dependencies detected.

---

## Testing Plan (In Order of Likelihood)

### Step 1: Check WebSocket Backend
```bash
# From backend directory
npm start

# Verify it's running
curl http://localhost:4000/health
```

**Expected**: Should return `{"status":"ok"}` or similar

### Step 2: Open Browser Console
```bash
# Frontend should already be running on http://localhost:3000
# Open browser (Chrome/Firefox)
# Press F12 → Console tab
# Hard refresh: Ctrl+Shift+R
```

**Expected**: With new error logging, should see:
- `========== APP STATE DEBUG ==========` logs
- If crash: Full error with stack trace (not `[object Object]`)

### Step 3: Check MetaMask State
- Is MetaMask installed?
- Is it unlocked?
- Is it on BSC Testnet (Chain ID 97)?
- Does account have test BNB for gas?

### Step 4: Verify Contract Deployment
```bash
# Check if contract exists on BSC Testnet
curl "https://api-testnet.bscscan.com/api?module=contract&action=getabi&address=0x5FD5a0914864B4A28fA7423b8BFAf436F210CEfC&apikey=YourApiKeyToken"
```

---

## What Corey Should Share

With the new error logging, when the crash happens, Corey should share:

1. **Full console output** starting from page load
2. **Any `========== ERROR` blocks** (these will have the actual error)
3. **App state debug logs** (shows what state the app was in)
4. **Network tab** (F12 → Network) - any failed requests?
5. **MetaMask state**: Connected? Which network? Account balance?

---

## Quick Fixes to Try

### If WebSocket is the issue:
```typescript
// src/hooks/useWebSocket.ts
// Add at the top of the hook:
const [error, setError] = useState<string | null>(null);

// In connect_error handler:
newSocket.on('connect_error', (error) => {
  console.error('WebSocket connection error:', error);
  setError('Unable to connect to real-time server');
  // Don't throw - just set state
});

// Return error in hook result
return {
  // ... other values
  error,
};
```

### If it's a component rendering issue:
Add ErrorBoundary around each major component:
```tsx
<ErrorBoundary>
  <PriceChart ... />
</ErrorBoundary>
```

### If it's related to missing data:
Add defensive checks before rendering:
```tsx
{priceData ? (
  <div>Price: {priceData.price}</div>
) : (
  <div>Loading...</div>
)}
```

---

## My Prediction

**Most likely issue**: WebSocket backend not running or not accessible.

**Why**:
1. socket.io connection errors are notorious for causing crashes if not handled
2. The error happens at runtime (not build time) - suggests network/connection issue
3. Health endpoint returns OK (so backend exists) but app crashes - suggests missing service

**Second most likely**: MetaMask in weird state or wrong network

**Least likely**: Code logic error (would have been caught by TypeScript)

---

**Next Step**: Corey should refresh browser and share the ACTUAL error message that now appears in console. The days of `[object Object]` are over.
