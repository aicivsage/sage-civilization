# BNB Token Launchpad - Deployment Guide

Complete guide for deploying the BNB Token Launchpad to BSC Testnet and Mainnet.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Deployment Steps](#deployment-steps)
4. [Testing Deployed Contracts](#testing-deployed-contracts)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)
7. [Script Reference](#script-reference)

---

## Prerequisites

### 1. Get Testnet BNB
For BSC Testnet deployment, you need testnet BNB:
- Visit: https://testnet.bnbchain.org/faucet-smart
- Connect your wallet
- Request testnet BNB (you'll need ~0.5 BNB for full testing)

### 2. Get BscScan API Key
For contract verification:
1. Create account at https://testnet.bscscan.com/ (or https://bscscan.com for mainnet)
2. Go to "API-KEYs" section
3. Create new API key
4. Save the key for configuration

### 3. Prepare Wallet
- Have your private key ready (without 0x prefix)
- **NEVER share or commit your private key**
- Consider using a dedicated deployment wallet for security

---

## Initial Setup

### 1. Clone and Install
```bash
cd bnb-launchpad
npm install
```

### 2. Configure Environment
Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` with your values:
```env
# Required
PRIVATE_KEY=your_private_key_without_0x_prefix
BSCSCAN_API_KEY=your_bscscan_api_key

# Optional - customize platform fee recipient
PLATFORM_FEE_RECIPIENT=0xYourAddressHere

# Optional - customize test token
TOKEN_NAME=My Awesome Token
TOKEN_SYMBOL=AWESOME
TOKEN_DESCRIPTION=The most awesome token ever
TOKEN_IMAGE=https://example.com/awesome.png
```

### 3. Verify Setup
Test that everything is configured correctly:
```bash
# Compile contracts
npx hardhat compile

# Run local tests
npx hardhat test

# Check network connection
npx hardhat run scripts/deploy-factory.js --network hardhat
```

---

## Deployment Steps

### Step 1: Deploy Factory Contract

Deploy the TokenLaunchFactory to BSC Testnet:

```bash
npx hardhat run scripts/deploy-factory.js --network bscTestnet
```

**What this does:**
- Deploys TokenLaunchFactory with your platform fee recipient
- Configures PancakeSwap Router (testnet: 0xD99D...6550D1)
- Saves deployment address to `deployments/testnet.json`
- Verifies deployment by calling view functions

**Expected output:**
```
=============================================================
DEPLOYING TOKENLAUNCHFACTORY
=============================================================
Network: bscTestnet
Chain ID: 97
-------------------------------------------------------------
Deployer: 0xYourAddress
Account Balance: X.XXXX BNB
✅ Sufficient balance for deployment

Deployment Configuration:
  Platform Fee Recipient: 0xYourAddress
  PancakeSwap Router: 0xD99D...6550D1
  WBNB Address: 0xae13...a7cd
-------------------------------------------------------------

📦 Deploying TokenLaunchFactory...
   Sending deployment transaction...
   Waiting for deployment confirmation...

✅ TokenLaunchFactory deployed!
   Address: 0x...
   Explorer: https://testnet.bscscan.com/address/0x...
```

**Troubleshooting:**
- "Insufficient balance" → Get more testnet BNB from faucet
- "Network error" → Check your RPC endpoint in hardhat.config.js
- "Nonce too high" → Clear pending transactions or wait

---

### Step 2: Create Test Token

Create a test token through the factory:

```bash
npx hardhat run scripts/create-test-token.js --network bscTestnet
```

**What this does:**
- Reads factory address from deployments
- Creates a new BondingCurveToken
- Pays creation fee (0.0001 BNB)
- Extracts token address from event logs
- Saves token address to `deployments/testnet.json`

**Customize token parameters:**
```bash
TOKEN_NAME="Cool Meme" \
TOKEN_SYMBOL="COOL" \
TOKEN_DESCRIPTION="The coolest meme token" \
npx hardhat run scripts/create-test-token.js --network bscTestnet
```

**Expected output:**
```
=============================================================
CREATING TEST TOKEN
=============================================================
...
✅ Token created successfully!
   Address: 0x...
   Explorer: https://testnet.bscscan.com/token/0x...
```

---

### Step 3: Test Buying Tokens

Execute a test purchase:

```bash
npx hardhat run scripts/test-buy.js --network bscTestnet
```

**What this does:**
- Reads token address from deployments
- Executes buy transaction (default: 0.01 BNB)
- Shows before/after state
- Calculates effective price
- Shows graduation progress

**Customize buy amount:**
```bash
BUY_AMOUNT=0.05 npx hardhat run scripts/test-buy.js --network bscTestnet
```

**Expected output:**
```
📊 State BEFORE purchase:
   BNB Reserve: 0.0 BNB
   Token Reserve: 1000000000.0 tokens
   Buyer Token Balance: 0.0 tokens

🛒 Executing purchase...
✅ Token purchase confirmed!

📊 State AFTER purchase:
   BNB Reserve: 0.00999 BNB (0.1% fee)
   Token Reserve: 999950000.0 tokens
   Buyer Token Balance: 50000.0 tokens

🎓 Graduation Progress:
   Current: 0.00999 BNB
   Target: 50.0 BNB
   Progress: 0.02%
```

---

### Step 4: Test Selling Tokens

Execute a test sale:

```bash
npx hardhat run scripts/test-sell.js --network bscTestnet
```

**What this does:**
- Checks your token balance
- Sells percentage of holdings (default: 50%)
- Shows BNB received
- Updates graduation progress

**Customize sell percentage:**
```bash
SELL_PERCENTAGE=25 npx hardhat run scripts/test-sell.js --network bscTestnet
```

---

### Step 5: Test Graduation

Test the full graduation flow to PancakeSwap:

```bash
# Manual graduation (requires buying to threshold first)
npx hardhat run scripts/test-graduation.js --network bscTestnet

# Auto-buy to threshold then graduate
AUTO_BUY=true npx hardhat run scripts/test-graduation.js --network bscTestnet
```

**What this does:**
- Checks if graduation threshold reached (50 BNB)
- If AUTO_BUY=true, buys tokens until threshold
- Waits for cooldown period (5 minutes on testnet)
- Calls graduateToPancakeSwap()
- Verifies LP creation and LP tokens burned
- Confirms ownership renounced

**Expected output:**
```
🎓 Attempting graduation to PancakeSwap...
✅ Graduation confirmed!

📊 State AFTER graduation:
   Is Graduated: true
   LP Pair: 0x...
   BNB Reserve: 0.0 BNB
   Token Reserve: 0.0 tokens
   Owner: 0x0000...0000 (renounced)

🔥 Verifying LP tokens burned...
   LP Total Supply: 1234.5678
   LP Burned: 1234.5678
   Burn %: 100.00%

=============================================================
PANCAKESWAP TRADING INFO
=============================================================
Token: TESTMEME
Trade on PancakeSwap:
https://pancakeswap.finance/?chain=bscTestnet
```

---

## Verification

### Verify Contracts on BscScan

Verify deployed contracts to enable interaction on BscScan:

```bash
npx hardhat run scripts/verify-contracts.js --network bscTestnet
```

**What this does:**
- Reads addresses from deployments
- Verifies factory contract
- Verifies test token contract
- Provides BscScan URLs

**Expected output:**
```
🔍 Verifying TokenLaunchFactory...
✅ TokenLaunchFactory verified successfully!

🔍 Verifying BondingCurveToken...
✅ BondingCurveToken verified successfully!

VIEW ON BSCSCAN:
Factory: https://testnet.bscscan.com/address/0x...
Test Token: https://testnet.bscscan.com/token/0x...
```

**Manual verification (if script fails):**
```bash
npx hardhat verify --network bscTestnet \
  FACTORY_ADDRESS \
  "PLATFORM_FEE_RECIPIENT" \
  "PANCAKE_ROUTER_ADDRESS"
```

---

## Testing Deployed Contracts

### Complete Testing Flow

Run through the complete lifecycle:

```bash
# 1. Deploy factory
npx hardhat run scripts/deploy-factory.js --network bscTestnet

# 2. Create token
TOKEN_NAME="Test Meme" \
TOKEN_SYMBOL="TEST" \
npx hardhat run scripts/create-test-token.js --network bscTestnet

# 3. Initial buy
BUY_AMOUNT=1.0 \
npx hardhat run scripts/test-buy.js --network bscTestnet

# 4. Multiple buys to test curve
BUY_AMOUNT=5.0 \
npx hardhat run scripts/test-buy.js --network bscTestnet

# 5. Test selling
SELL_PERCENTAGE=30 \
npx hardhat run scripts/test-sell.js --network bscTestnet

# 6. Buy more
BUY_AMOUNT=10.0 \
npx hardhat run scripts/test-buy.js --network bscTestnet

# 7. Graduate when ready
AUTO_BUY=true \
npx hardhat run scripts/test-graduation.js --network bscTestnet

# 8. Verify all contracts
npx hardhat run scripts/verify-contracts.js --network bscTestnet
```

### Monitor Deployment State

Check current deployment status:
```bash
cat deployments/testnet.json
```

Example output:
```json
{
  "factory": "0x...",
  "testToken": "0x...",
  "deployer": "0x...",
  "platformFeeRecipient": "0x...",
  "pancakeRouter": "0xD99D1c33F9fC3444f8101754aBC46c52416550D1",
  "wbnb": "0xae13d989daC2f0dEbFf460aC112a837C89BAa7cd",
  "testTokenName": "Test Meme",
  "testTokenSymbol": "TEST",
  "deployedAt": "2025-10-08T12:34:56.789Z",
  "lastUpdated": "2025-10-08T12:45:00.000Z"
}
```

---

## Troubleshooting

### Common Issues

#### "Insufficient balance"
**Problem:** Not enough BNB for gas fees
**Solution:**
- Get more testnet BNB from faucet
- Check balance: `npx hardhat run scripts/deploy-factory.js --network bscTestnet` (shows balance)

#### "Nonce too high"
**Problem:** Pending transactions or network issues
**Solution:**
- Wait for pending transactions to complete
- Clear pending transactions in wallet
- Try with different account

#### "Factory not deployed"
**Problem:** Running test scripts before deploying factory
**Solution:**
```bash
# Deploy factory first
npx hardhat run scripts/deploy-factory.js --network bscTestnet
```

#### "Test token not found"
**Problem:** Running buy/sell scripts before creating token
**Solution:**
```bash
# Create token first
npx hardhat run scripts/create-test-token.js --network bscTestnet
```

#### "Seller has no tokens"
**Problem:** Running sell script before buying
**Solution:**
```bash
# Buy tokens first
npx hardhat run scripts/test-buy.js --network bscTestnet
```

#### "Graduation threshold not reached"
**Problem:** Trying to graduate before 50 BNB raised
**Solution:**
```bash
# Auto-buy to threshold
AUTO_BUY=true npx hardhat run scripts/test-graduation.js --network bscTestnet
```

#### "Cooldown period not complete"
**Problem:** Trying to graduate during cooldown
**Solution:**
- Wait 5 minutes after first reaching threshold
- Or use: `SKIP_COOLDOWN=true` (may still fail if cooldown enforced)

#### "Verification failed"
**Problem:** BscScan verification issues
**Solution:**
- Check BSCSCAN_API_KEY is set correctly
- Try manual verification with exact constructor args
- Wait a few minutes and retry (sometimes BscScan needs time)

### Getting Help

If you encounter issues not covered here:

1. Check transaction on BscScan for error details
2. Review logs for specific error messages
3. Verify environment variables in `.env`
4. Ensure sufficient testnet BNB balance
5. Check network connectivity to BSC RPC

---

## Script Reference

### Available Scripts

| Script | Purpose | Key Environment Variables |
|--------|---------|--------------------------|
| `deploy-factory.js` | Deploy TokenLaunchFactory | `PLATFORM_FEE_RECIPIENT` |
| `create-test-token.js` | Create token via factory | `TOKEN_NAME`, `TOKEN_SYMBOL`, `TOKEN_DESCRIPTION`, etc. |
| `test-buy.js` | Buy tokens from bonding curve | `BUY_AMOUNT` (default: 0.01) |
| `test-sell.js` | Sell tokens back to curve | `SELL_PERCENTAGE` (default: 50) |
| `test-graduation.js` | Graduate token to PancakeSwap | `AUTO_BUY`, `SKIP_COOLDOWN` |
| `verify-contracts.js` | Verify contracts on BscScan | `BSCSCAN_API_KEY` |

### Helper Utilities

Located in `scripts/utils/helpers.js`:

- `saveDeployment()` - Save deployment addresses
- `loadDeployment()` - Load deployment data
- `getContract()` - Get contract instance
- `formatBNB()` - Format wei to BNB
- `parseBNB()` - Parse BNB to wei
- `waitForTx()` - Wait for transaction with logging
- `getExplorerUrl()` - Generate BscScan URLs
- `verifyBalance()` - Check sufficient balance
- `findEvent()` - Extract event from receipt

---

## Mainnet Deployment

**⚠️ WARNING: Mainnet deployment uses real BNB and is irreversible!**

### Pre-Mainnet Checklist

Before deploying to mainnet:

- [ ] Thoroughly tested on testnet
- [ ] All tests passing: `npx hardhat test`
- [ ] Security audit completed (recommended)
- [ ] Sufficient BNB for deployment (~0.5 BNB)
- [ ] Platform fee recipient address confirmed
- [ ] Emergency pause mechanism tested
- [ ] Team aware of deployment

### Mainnet Deployment

```bash
# Deploy to mainnet (use with caution!)
npx hardhat run scripts/deploy-factory.js --network bscMainnet

# Verify on mainnet BscScan
npx hardhat run scripts/verify-contracts.js --network bscMainnet
```

**Mainnet Configuration:**
- PancakeSwap Router: `0x10ED43C718714eb63d5aA57B78B54704E256024E`
- WBNB: `0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c`
- Higher gas prices recommended
- More BNB required for deployment

---

## Network Information

### BSC Testnet
- Chain ID: 97
- RPC: https://data-seed-prebsc-1-s1.binance.org:8545/
- Explorer: https://testnet.bscscan.com
- Faucet: https://testnet.bnbchain.org/faucet-smart
- PancakeSwap Router: 0xD99D1c33F9fC3444f8101754aBC46c52416550D1
- WBNB: 0xae13d989daC2f0dEbFf460aC112a837C89BAa7cd

### BSC Mainnet
- Chain ID: 56
- RPC: https://bsc-dataseed1.binance.org/
- Explorer: https://bscscan.com
- PancakeSwap Router: 0x10ED43C718714eb63d5aA57B78B54704E256024E
- WBNB: 0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c

---

## Security Best Practices

1. **Never commit private keys** - Use .env and .gitignore
2. **Use dedicated wallets** - Don't use your main wallet for deployment
3. **Test thoroughly** - Complete all tests on testnet first
4. **Verify contracts** - Always verify on BscScan for transparency
5. **Check balances** - Ensure sufficient BNB before deploying
6. **Backup deployments** - Save `deployments/*.json` files
7. **Monitor transactions** - Watch BscScan during deployment
8. **Start small** - Test with small amounts first

---

## Support

For issues or questions:
- Review troubleshooting section
- Check BscScan transaction details
- Verify environment configuration
- Test on local hardhat network first

---

**Happy Deploying! 🚀**
