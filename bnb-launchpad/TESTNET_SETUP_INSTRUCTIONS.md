# BSC Testnet Deployment - Ready to Execute

## Current Status

✅ **All code complete and tested**
- Smart contracts implemented with security fixes
- Comprehensive test suite (108 tests)
- Deployment scripts created and validated locally
- Documentation complete

🎯 **Ready for testnet deployment** - Just need testnet BNB and environment setup

---

## Prerequisites Checklist

### 1. Get Testnet BNB (0.2+ BNB recommended)

**Option A: QuickNode Faucet (Recommended - Higher amounts)**
- URL: https://faucet.quicknode.com/binance-smart-chain/bnb-testnet
- Amount: 0.05 tBNB per 12 hours
- Requirements: Twitter/GitHub account
- Strategy: Request 4x over 2 days = 0.2 tBNB total

**Option B: Official BNB Chain Faucet**
- URL: https://testnet.bnbchain.org/faucet-smart
- Amount: 0.1 tBNB per 24 hours
- Requirements: BNB Chain account
- Strategy: Request 2x over 2 days = 0.2 tBNB total

**Option C: Community Faucets**
- https://testnet.binance.org/faucet-smart (backup)
- https://faucets.chain.link/bnb-chain-testnet (Chainlink)

**Recommended Wallet**: MetaMask with BSC Testnet network added

### 2. Setup Environment File

Create `.env` file in `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/bnb-launchpad/`:

```bash
# Your testnet wallet private key (NEVER commit this)
PRIVATE_KEY=your_64_character_private_key_here

# BscScan API key for contract verification (optional but recommended)
# Get free key at: https://bscscan.com/apis
BSCSCAN_API_KEY=your_bscscan_api_key_here

# Platform fee recipient (defaults to deployer if not set)
PLATFORM_FEE_RECIPIENT=0xYourWalletAddress

# Token parameters (optional - defaults provided)
TOKEN_NAME="Test Launch Token"
TOKEN_SYMBOL="TLT"
```

**Security Note**: `.env` is in `.gitignore` - never commit private keys!

### 3. Verify Network Configuration

Check your wallet has BSC Testnet added:
- **Network Name**: BSC Testnet
- **RPC URL**: https://data-seed-prebsc-1-s1.binance.org:8545/
- **Chain ID**: 97
- **Currency Symbol**: tBNB
- **Block Explorer**: https://testnet.bscscan.com

---

## Deployment Steps (Once You Have Testnet BNB)

### Step 1: Verify Local Setup

```bash
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch/bnb-launchpad

# Test deployment scripts locally (no testnet BNB needed)
npx hardhat run scripts/test-deployment-local.js --network hardhat
```

**Expected Output**: All tests passing ✅

### Step 2: Deploy Factory to Testnet

```bash
# Deploy TokenLaunchFactory
npx hardhat run scripts/deploy-factory.js --network bscTestnet
```

**Expected Output**:
```
Deploying TokenLaunchFactory to BSC Testnet...
Deploying with account: 0xYourAddress
Account balance: 0.2 BNB

Deploying TokenLaunchFactory...
TokenLaunchFactory deployed to: 0x123...abc
Platform Fee Recipient: 0xYourAddress
PancakeSwap Router: 0xD99D1c33F9fC3444f8101754aBC46c52416550D1

View on BscScan: https://testnet.bscscan.com/address/0x123...abc
Deployment saved to: deployments/testnet.json
```

**Cost**: ~0.01 tBNB

### Step 3: Create Test Token

```bash
# Create token through factory
npx hardhat run scripts/create-test-token.js --network bscTestnet
```

**Expected Output**:
```
Creating test token through factory...
Factory address: 0x123...abc
Token Name: Test Launch Token
Token Symbol: TLT
Creator: 0xYourAddress

Token created at: 0x456...def
View on BscScan: https://testnet.bscscan.com/address/0x456...def
```

**Cost**: ~0.02 tBNB

### Step 4: Test Buy Function

```bash
# Buy some tokens (default: 0.01 BNB)
BUY_AMOUNT=0.01 npx hardhat run scripts/test-buy.js --network bscTestnet
```

**Expected Output**:
```
Testing buy function...
Token: 0x456...def
BUY amount: 0.01 BNB

Before Buy:
  Your token balance: 0
  Contract BNB reserves: 0

Executing buy...
Transaction hash: 0x789...ghi
Block: 12345678

After Buy:
  Your token balance: ~350,000 TLT
  Contract BNB reserves: 0.0098 BNB (after fees)
  Tokens received: 350,000 TLT

Success! ✅
```

**Cost**: 0.01 tBNB (your buy amount) + gas

### Step 5: Test Sell Function

```bash
# Sell 50% of tokens
SELL_PERCENTAGE=50 npx hardhat run scripts/test-sell.js --network bscTestnet
```

**Expected Output**:
```
Testing sell function...
Selling 50% of your tokens: 175,000 TLT

Before Sell:
  Your token balance: 350,000 TLT
  Your BNB balance: 0.19 BNB

Executing sell...
BNB received: ~0.0048 BNB (after fees)

After Sell:
  Your token balance: 175,000 TLT
  Your BNB balance: 0.1948 BNB

Success! ✅
```

### Step 6: Test Graduation to PancakeSwap

```bash
# Auto-buy to 50 BNB threshold and graduate
AUTO_BUY=true npx hardhat run scripts/test-graduation.js --network bscTestnet
```

**Expected Output**:
```
Testing graduation to PancakeSwap...

Phase 1: Buying to graduation threshold (50 BNB)...
  Buying in batches to avoid gas issues...
  Batch 1: 10 BNB ✅
  Batch 2: 10 BNB ✅
  Batch 3: 10 BNB ✅
  Batch 4: 10 BNB ✅
  Batch 5: 10 BNB ✅
  Total BNB in reserves: 49.02 BNB (after fees)

  Final batch to cross threshold...
  Status: Graduated ✅
  Graduation timestamp: 1234567890
  Cooldown period: 1 hour

Phase 2: Waiting for cooldown (1 hour)...
  [Progress bar showing countdown]

Phase 3: Executing graduation...
  Calling graduateToPancakeSwap()...

  LP Pair Created: 0xabc...def
  LP Tokens Minted: 1,234,567
  LP Tokens Burned: 1,234,567 (100% to 0x...dEaD) ✅
  Ownership Renounced: Yes ✅

  PancakeSwap Pool:
    Token reserve: ~805M TLT
    BNB reserve: 37.5 BNB
    LP tokens burned: 100%

  Remaining BNB distributed:
    Platform fees: ~0.49 BNB
    Creator fees: ~0.49 BNB
    Graduation caller: 0.1 BNB (your reward)

Success! Token graduated to PancakeSwap ✅
View pair: https://testnet.bscscan.com/address/0xabc...def
```

**Cost**: ~50.2 tBNB total (50 BNB to reserves + fees + gas)

**Note**: This requires significant testnet BNB. You can also manually test with smaller amounts.

### Step 7: Verify Contracts on BscScan

```bash
npx hardhat run scripts/verify-contracts.js --network bscTestnet
```

**Expected Output**:
```
Verifying contracts on BscScan...

Verifying TokenLaunchFactory at 0x123...abc
  Submitting verification...
  Status: Already verified ✅
  View: https://testnet.bscscan.com/address/0x123...abc#code

Verifying BondingCurveToken at 0x456...def
  Submitting verification...
  Status: Success ✅
  View: https://testnet.bscscan.com/address/0x456...def#code

All contracts verified! ✅
```

**Requires**: BSCSCAN_API_KEY in .env

---

## Manual Testing (Without Auto-Graduation)

If you want to test manually without auto-buying 50 BNB:

```bash
# 1. Deploy factory
npx hardhat run scripts/deploy-factory.js --network bscTestnet

# 2. Create token
npx hardhat run scripts/create-test-token.js --network bscTestnet

# 3. Small buy test
BUY_AMOUNT=0.01 npx hardhat run scripts/test-buy.js --network bscTestnet

# 4. Small sell test
SELL_PERCENTAGE=25 npx hardhat run scripts/test-sell.js --network bscTestnet

# 5. Verify contracts
npx hardhat run scripts/verify-contracts.js --network bscTestnet
```

**Total Cost**: ~0.05 tBNB (much more realistic for testing)

---

## Troubleshooting

### "Insufficient funds for gas"
- Get more testnet BNB from faucets
- Check balance: `npx hardhat run scripts/check-balance.js --network bscTestnet`

### "Invalid JSON RPC response"
- Check internet connection
- Try alternate RPC: https://data-seed-prebsc-2-s1.binance.org:8545/

### "Transaction underpriced"
- Increase gas price in hardhat.config.js (currently 10 gwei)

### "Contract verification failed"
- Ensure BSCSCAN_API_KEY is set in .env
- Wait 30 seconds after deployment before verifying
- Check constructor parameters match deployment

### "Cooldown period not elapsed"
- Wait full 1 hour after graduation triggered
- Or use SKIP_COOLDOWN=true for testing (requires timetravel, only works on local fork)

---

## What I Can Do While You Get Testnet BNB

While waiting for testnet BNB, I can:
1. ✅ Run more local tests to ensure everything works
2. ✅ Create additional testing scripts (stress tests, edge cases)
3. ✅ Write frontend integration guide
4. ✅ Create monitoring/analytics scripts
5. ✅ Prepare mainnet deployment plan

Just let me know what you'd like me to work on next!

---

## Summary of Costs

**Minimal Testing** (recommended for first deployment):
- Deploy factory: ~0.01 tBNB
- Create token: ~0.02 tBNB
- Test buy: 0.01 tBNB + gas
- Test sell: gas only (~0.001 tBNB)
- **Total: ~0.05 tBNB**

**Full Graduation Testing**:
- Above + buy to 50 BNB threshold: ~50.2 tBNB
- **Total: ~50.25 tBNB**

**Recommendation**: Start with minimal testing (0.05 tBNB), verify everything works, then do graduation test if desired.

---

## Next Step: Get 0.1 tBNB and Run Deployment

Once you have testnet BNB and .env set up:
```bash
npx hardhat run scripts/deploy-factory.js --network bscTestnet
```

Then let me know the results and I'll help with next steps!
