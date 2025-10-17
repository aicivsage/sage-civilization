# MetaMask Integration - Complete Guide

**Status**: Production-Ready Reference
**Date**: October 9, 2025
**Purpose**: Permanent resource for bulletproof MetaMask integration

---

## 🎯 Quick Summary

Your current implementation at `/frontend/app.js` has **5 critical bugs** causing "Internal JSON-RPC error" and "disconnect to connect different wallet" issues:

1. **Auto-reconnect creates double connection** (lines 44-50)
2. **Event listeners never cleaned up** (memory leak)
3. **Provider created twice without cleanup** (lines 98, 111)
4. **No connection state guard** (rapid clicks cause duplicates)
5. **localStorage flag confusion** (inverted logic)

**Solution**: Use the WalletConnectionManager class (below) which handles all edge cases.

---

## 📋 Table of Contents

1. [Root Cause Analysis](#root-cause-analysis)
2. [MetaMask Best Practices](#metamask-best-practices)
3. [Production-Ready Implementation](#production-ready-implementation)
4. [Integration Guide](#integration-guide)
5. [Testing Checklist](#testing-checklist)

---

## 🐛 Root Cause Analysis

### Current Implementation Bugs

#### Bug 1: Double Connection Race Condition
**Location**: `app.js` lines 44-50

```javascript
// BROKEN CODE:
const wasDisconnected = localStorage.getItem('walletDisconnected') === 'true';
if (window.ethereum && !wasDisconnected) {
    const accounts = await window.ethereum.request({ method: 'eth_accounts' });
    if (accounts.length > 0) {
        await connectWallet();  // ← Calls eth_requestAccounts AGAIN!
    }
}
```

**Problem**: `eth_accounts` already returns the connected account, but code calls `connectWallet()` which triggers `eth_requestAccounts` again. MetaMask receives 2 requests → Internal JSON-RPC error.

**Fix**: Just restore state without calling `connectWallet()`:
```javascript
if (accounts.length > 0) {
    // Already connected - restore state without new request
    userAddress = accounts[0];
    provider = new ethers.providers.Web3Provider(window.ethereum, 'any');
    signer = provider.getSigner();
    await initializeContracts();
}
```

#### Bug 2: Event Listener Leak
**Location**: `app.js` lines 130-131

```javascript
// BROKEN: Adds listeners but NEVER removes them
window.ethereum.on('accountsChanged', handleAccountsChanged);
window.ethereum.on('chainChanged', () => window.location.reload());
```

**Problem**: `disconnectWallet()` doesn't remove these. Every connect/disconnect cycle adds MORE listeners. After 5 cycles = 10 listeners firing simultaneously.

**Fix**: Store references and clean up:
```javascript
// Store handler reference
let chainChangedHandler = () => window.location.reload();

// Add listeners
window.ethereum.on('accountsChanged', handleAccountsChanged);
window.ethereum.on('chainChanged', chainChangedHandler);

// Remove in disconnect
function disconnectWallet() {
    window.ethereum.removeListener('accountsChanged', handleAccountsChanged);
    window.ethereum.removeListener('chainChanged', chainChangedHandler);
}
```

#### Bug 3: Orphaned Provider
**Location**: `app.js` lines 98, 111

```javascript
// First provider
provider = new ethers.providers.Web3Provider(window.ethereum, 'any');

// Later, after network switch - OLD PROVIDER STILL EXISTS!
provider = new ethers.providers.Web3Provider(window.ethereum, 'any');
```

**Problem**: First provider has event listeners attached but is orphaned. Both providers try to handle MetaMask events.

**Fix**: Clean up old provider before creating new one:
```javascript
if (provider) {
    await provider.removeAllListeners();
}
provider = new ethers.providers.Web3Provider(window.ethereum, 'any');
```

#### Bug 4: No Connection State Guard
**Location**: `app.js` line 75

```javascript
async function connectWallet() {
    // NO CHECK if already connecting!
    const accounts = await window.ethereum.request({
        method: 'eth_requestAccounts'
    });
}
```

**Problem**: User double-clicks button → 2 requests sent → Internal error

**Fix**: Add connecting flag:
```javascript
if (window.connectingWallet) {
    console.log('Connection already in progress');
    return;
}
window.connectingWallet = true;

try {
    // ... connection logic
} finally {
    window.connectingWallet = false;
}
```

#### Bug 5: localStorage Confusion
**Location**: Various

```javascript
// Sets flag on disconnect
localStorage.setItem('walletDisconnected', 'true');

// Clears on connect
localStorage.removeItem('walletDisconnected');

// Checks on load
const wasDisconnected = localStorage.getItem('walletDisconnected') === 'true';
```

**Problem**: Flag cleared on connect, but if user refreshes, flag is missing and auto-reconnect triggers even though MetaMask still connected.

**Fix**: Store positive connection state, not negative:
```javascript
// Store when connected
localStorage.setItem('walletConnected', 'true');

// Clear when disconnected
localStorage.removeItem('walletConnected');

// Check on load
const wasConnected = localStorage.getItem('walletConnected') === 'true';
```

---

## ✅ MetaMask Best Practices

### Connection Flow

**NEVER do this:**
```javascript
// BAD: Always triggers popup even if already connected
await window.ethereum.request({ method: 'eth_requestAccounts' });
```

**ALWAYS do this:**
```javascript
// GOOD: Check silently first, only popup if needed
const accounts = await window.ethereum.request({ method: 'eth_accounts' });

if (accounts.length === 0) {
    // Not connected - show popup
    await window.ethereum.request({ method: 'eth_requestAccounts' });
} else {
    // Already connected - use existing permission
    // NO POPUP!
}
```

### Event Handling (4 Critical Events)

```javascript
// 1. Account changed (user switched accounts)
window.ethereum.on('accountsChanged', (accounts) => {
    if (accounts.length === 0) {
        // User disconnected
        handleDisconnect();
    } else {
        // User switched account
        updateAccount(accounts[0]);
    }
});

// 2. Network changed (ALWAYS reload - recommended by MetaMask)
window.ethereum.on('chainChanged', (chainId) => {
    window.location.reload(); // Safest approach
});

// 3. Provider connected
window.ethereum.on('connect', (connectInfo) => {
    console.log('Connected to chain:', connectInfo.chainId);
});

// 4. Provider disconnected
window.ethereum.on('disconnect', (error) => {
    handleDisconnect();
});

// CRITICAL: Clean up listeners
function cleanup() {
    window.ethereum.removeListener('accountsChanged', handleAccountsChanged);
    window.ethereum.removeListener('chainChanged', handleChainChanged);
    window.ethereum.removeListener('connect', handleConnect);
    window.ethereum.removeListener('disconnect', handleDisconnect);
}
```

### Error Handling

```javascript
try {
    await window.ethereum.request({ method: 'eth_requestAccounts' });
} catch (error) {
    switch (error.code) {
        case 4001:
            alert('You rejected the connection. Please try again.');
            break;
        case -32002:
            alert('A connection request is already pending. Check MetaMask.');
            break;
        case -32603:
            alert('MetaMask encountered an internal error. Please try again.');
            break;
        default:
            alert(`Error: ${error.message}`);
    }
}
```

### Network Switching

```javascript
async function switchToNetwork(chainId) {
    try {
        await window.ethereum.request({
            method: 'wallet_switchEthereumChain',
            params: [{ chainId }],
        });
    } catch (switchError) {
        // Error 4902: Chain not added to MetaMask
        if (switchError.code === 4902) {
            // Add the network
            await window.ethereum.request({
                method: 'wallet_addEthereumChain',
                params: [{
                    chainId: '0x61',
                    chainName: 'BSC Testnet',
                    nativeCurrency: {
                        name: 'BNB',
                        symbol: 'BNB',
                        decimals: 18
                    },
                    rpcUrls: ['https://data-seed-prebsc-1-s1.bnbchain.org:8545/'],
                    blockExplorerUrls: ['https://testnet.bscscan.com']
                }],
            });
        } else {
            throw switchError;
        }
    }
}
```

---

## 🚀 Production-Ready Implementation

See `WalletConnectionManager.js` for complete implementation.

### Key Features

✅ Single source of truth for wallet state
✅ Automatic connection detection (no popup)
✅ Proper event listener lifecycle
✅ Comprehensive error handling
✅ State persistence with auto-cleanup
✅ Network validation
✅ Connection timeout protection
✅ Duplicate request prevention

### Quick Start

```javascript
// 1. Initialize
const walletManager = new WalletConnectionManager({
    autoConnect: true,
    supportedChainIds: ['0x38', '0x61'], // BSC Mainnet, Testnet
    preferredChainId: '0x38',
    connectionTimeout: 30000
});

// 2. Subscribe to changes
walletManager.onStateChange((state) => {
    updateUI(state);
});

// 3. Connect
async function handleConnect() {
    try {
        const result = await walletManager.connect();
        console.log('Connected:', result);
    } catch (error) {
        console.error('Failed:', error.message);
    }
}

// 4. Disconnect
function handleDisconnect() {
    walletManager.disconnect();
}

// 5. Cleanup (on page unload)
window.addEventListener('beforeunload', () => {
    walletManager.cleanup();
});
```

---

## 📦 Integration Guide

### Step 1: Add WalletConnectionManager

Save the complete `WalletConnectionManager` class to:
```
/frontend/js/WalletConnectionManager.js
```

### Step 2: Update HTML

```html
<!-- Add before your app.js -->
<script src="js/WalletConnectionManager.js"></script>
<script src="js/app.js"></script>
```

### Step 3: Replace Connection Code

**Replace lines 44-200 in app.js with:**

```javascript
// Initialize wallet manager
let walletManager;

async function initWallet() {
    walletManager = new WalletConnectionManager({
        autoConnect: true,
        supportedChainIds: ['0x38', '0x61'],
        preferredChainId: '0x61', // BSC Testnet
        storageKey: 'bnb_launchpad_wallet'
    });

    // Subscribe to state changes
    walletManager.onStateChange((state) => {
        if (state.status === 'connected') {
            userAddress = state.account;
            updateConnectionUI();
            initializeContracts();
        } else if (state.status === 'disconnected') {
            userAddress = null;
            updateConnectionUI();
        } else if (state.status === 'error') {
            alert(state.error.message);
        }
    });
}

// Connect button handler
async function connectWallet() {
    try {
        const result = await walletManager.connect();
        console.log('Connected to:', result.account);
    } catch (error) {
        console.error('Connection failed:', error);
    }
}

// Disconnect button handler
function disconnectWallet() {
    walletManager.disconnect();
}

// Initialize on page load
initWallet();
```

### Step 4: Update Contract Initialization

```javascript
async function initializeContracts() {
    const state = walletManager.getState();

    if (!state.account) {
        console.error('No account connected');
        return;
    }

    // Verify correct network
    if (state.chainId !== '0x61') {
        await walletManager.switchChain('0x61');
    }

    // Initialize contracts
    provider = new ethers.providers.Web3Provider(window.ethereum, 'any');
    signer = provider.getSigner();

    // ... rest of contract setup
}
```

---

## ✅ Testing Checklist

### Basic Connection
- [ ] Page loads without errors
- [ ] "Connect Wallet" button visible when disconnected
- [ ] Clicking connect opens MetaMask popup
- [ ] After approval, shows connected account
- [ ] Disconnect button works

### Auto-Connection
- [ ] Connect wallet, refresh page → Auto-reconnects (no popup)
- [ ] Disconnect, refresh page → Stays disconnected
- [ ] Close MetaMask, refresh page → Shows disconnected

### Account Switching
- [ ] Switch account in MetaMask → App updates automatically
- [ ] Lock MetaMask → App shows disconnected
- [ ] Unlock with different account → App updates

### Network Switching
- [ ] Switch network in MetaMask → App updates
- [ ] Try transaction on wrong network → Shows network warning
- [ ] Switch network button → Changes network successfully

### Error Scenarios
- [ ] Reject connection → Shows "Request rejected" message
- [ ] Double-click connect → No duplicate requests
- [ ] Open MetaMask popup, click connect again → Shows "pending" message
- [ ] MetaMask not installed → Shows install prompt

### Edge Cases
- [ ] Connect, disconnect, connect again → Works without errors
- [ ] Multiple tabs open → All tabs sync state
- [ ] Page refresh during connection → Handles gracefully
- [ ] Network switch during transaction → Handles gracefully

### Memory & Performance
- [ ] Connect/disconnect 10 times → No memory leak
- [ ] Check browser console → No orphaned listeners
- [ ] Page unload → Cleanup runs properly

---

## 🔍 Debugging Tips

### Enable Debug Logging

```javascript
const walletManager = new WalletConnectionManager({
    debug: true, // Add debug flag
    // ... other options
});
```

### Check Current State

```javascript
// In browser console
console.log('Wallet state:', walletManager.getState());

// Check MetaMask directly
const accounts = await window.ethereum.request({ method: 'eth_accounts' });
console.log('MetaMask accounts:', accounts);

const chainId = await window.ethereum.request({ method: 'eth_chainId' });
console.log('MetaMask chain:', chainId);
```

### Common Issues & Solutions

**Issue**: "Already pending" error
**Solution**: Wait for current request to complete, or reload page

**Issue**: Shows connected but MetaMask shows disconnected
**Solution**: Clear localStorage and refresh page

**Issue**: Network warning persists after switching
**Solution**: Reload page (MetaMask recommends this)

**Issue**: Account doesn't update after switch
**Solution**: Check accountsChanged listener is active

---

## 📚 References

- [MetaMask Docs - Connection Guide](https://docs.metamask.io/wallet/how-to/connect/)
- [MetaMask Provider API](https://docs.metamask.io/wallet/reference/provider-api/)
- [EIP-1193 Standard](https://eips.ethereum.org/EIPS/eip-1193)
- [Error Codes Reference](https://docs.metamask.io/wallet/reference/provider-api/#errors)

---

## 🎉 Expected Results

After integration:

✅ **No more "Internal JSON-RPC error"** - Duplicate requests prevented
✅ **No more "disconnect to connect"** - Proper permission handling
✅ **Automatic reconnection** - Silent check on page load
✅ **Real-time updates** - Account/network changes sync instantly
✅ **Clean state** - No memory leaks or orphaned listeners
✅ **User-friendly errors** - Clear messages for all error cases
✅ **Reliable operation** - Handles all edge cases gracefully

---

**Status**: Ready for Production
**Last Updated**: October 9, 2025
**Version**: 1.0.0
