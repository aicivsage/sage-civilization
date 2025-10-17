# BNB Token Launchpad - Deployment Scripts

Complete suite of deployment and testing scripts for the BNB Token Launchpad.

## Quick Start

```bash
# 1. Setup environment
cp .env.example .env
# Edit .env with your private key and API key

# 2. Test locally
npx hardhat run scripts/test-deployment-local.js --network hardhat

# 3. Deploy to testnet
npx hardhat run scripts/deploy-factory.js --network bscTestnet
npx hardhat run scripts/create-test-token.js --network bscTestnet
npx hardhat run scripts/test-buy.js --network bscTestnet
npx hardhat run scripts/test-sell.js --network bscTestnet
npx hardhat run scripts/test-graduation.js --network bscTestnet
npx hardhat run scripts/verify-contracts.js --network bscTestnet
```

## Scripts Overview

### Core Deployment Scripts

#### 1. `deploy-factory.js`
Deploys the TokenLaunchFactory contract.

**Usage:**
```bash
npx hardhat run scripts/deploy-factory.js --network bscTestnet
```

**Environment Variables:**
- `PLATFORM_FEE_RECIPIENT` - Address to receive platform fees (defaults to deployer)

**What it does:**
- Verifies sufficient balance
- Deploys TokenLaunchFactory with PancakeSwap router
- Verifies deployment by calling view functions
- Saves deployment address to `deployments/testnet.json`
- Prints next steps and verification command

**Output:**
- Factory contract address
- BscScan explorer URL
- Deployment summary

---

#### 2. `create-test-token.js`
Creates a test token through the factory.

**Usage:**
```bash
npx hardhat run scripts/create-test-token.js --network bscTestnet
```

**Environment Variables:**
- `TOKEN_NAME` - Token name (default: "Test Meme Token")
- `TOKEN_SYMBOL` - Token symbol (default: "TESTMEME")

**What it does:**
- Loads factory address from deployments
- Creates new BondingCurveToken
- Extracts token address from TokenCreated event
- Verifies token deployment
- Saves token address to deployments

**Output:**
- Token contract address
- Token name and symbol
- BscScan explorer URL

---

### Testing Scripts

#### 3. `test-buy.js`
Tests buying tokens from the bonding curve.

**Usage:**
```bash
# Buy with default amount (0.01 BNB)
npx hardhat run scripts/test-buy.js --network bscTestnet

# Buy with custom amount
BUY_AMOUNT=0.05 npx hardhat run scripts/test-buy.js --network bscTestnet
```

**Environment Variables:**
- `BUY_AMOUNT` - BNB amount to buy (default: "0.01")

**What it does:**
- Shows reserves before purchase
- Executes buy transaction
- Shows tokens received
- Calculates effective price
- Shows graduation progress

**Output:**
- Before/after state comparison
- Tokens received
- BNB spent (including gas)
- Effective price per token
- Graduation progress percentage

---

#### 4. `test-sell.js`
Tests selling tokens back to the bonding curve.

**Usage:**
```bash
# Sell 50% of holdings (default)
npx hardhat run scripts/test-sell.js --network bscTestnet

# Sell custom percentage
SELL_PERCENTAGE=25 npx hardhat run scripts/test-sell.js --network bscTestnet
```

**Environment Variables:**
- `SELL_PERCENTAGE` - Percentage of holdings to sell (default: "50")

**What it does:**
- Checks token balance
- Approves tokens for sale
- Executes sell transaction
- Shows BNB received
- Updates graduation progress

**Output:**
- Before/after state comparison
- Tokens sold
- BNB received (after gas)
- Effective price per token
- Graduation progress update

---

#### 5. `test-graduation.js`
Tests the full graduation flow to PancakeSwap.

**Usage:**
```bash
# Manual graduation (requires threshold reached)
npx hardhat run scripts/test-graduation.js --network bscTestnet

# Auto-buy to threshold then graduate
AUTO_BUY=true npx hardhat run scripts/test-graduation.js --network bscTestnet

# Skip cooldown check (may still fail if enforced)
SKIP_COOLDOWN=true npx hardhat run scripts/test-graduation.js --network bscTestnet
```

**Environment Variables:**
- `AUTO_BUY` - Automatically buy to threshold (default: false)
- `SKIP_COOLDOWN` - Skip cooldown wait (default: false)

**What it does:**
- Checks if graduation threshold reached (50 BNB)
- Optionally buys tokens to reach threshold
- Waits for cooldown period (5 minutes)
- Executes graduateToPancakeSwap()
- Verifies LP creation
- Verifies LP tokens burned to dead address
- Confirms ownership renounced

**Output:**
- Graduation progress
- LP pair address
- BNB and tokens added to liquidity
- LP burn verification
- Ownership status
- PancakeSwap trading URL

---

### Verification Scripts

#### 6. `verify-contracts.js`
Verifies contracts on BscScan.

**Usage:**
```bash
npx hardhat run scripts/verify-contracts.js --network bscTestnet
```

**Environment Variables:**
- `BSCSCAN_API_KEY` - BscScan API key (required)

**What it does:**
- Loads deployment addresses
- Verifies factory contract
- Verifies token contract (if exists)
- Provides BscScan URLs

**Output:**
- Verification status for each contract
- BscScan explorer URLs
- Manual verification commands if needed

---

### Utility Scripts

#### 7. `test-deployment-local.js`
Tests all deployment scripts on local Hardhat network.

**Usage:**
```bash
npx hardhat run scripts/test-deployment-local.js --network hardhat
```

**What it does:**
- Deploys mock PancakeSwap contracts
- Deploys factory
- Creates test token
- Tests buy and sell functions
- Verifies all core functionality

**Output:**
- Success/failure status for each step
- Comprehensive test results

---

## Helper Utilities

### `scripts/utils/helpers.js`

Shared utility functions used by all scripts:

**File Operations:**
- `saveDeployment(network, contractName, address, extras)` - Save deployment info
- `loadDeployment(network)` - Load deployment data

**Contract Operations:**
- `getContract(contractName, address, ethers)` - Get contract instance
- `waitForTx(tx, description)` - Wait for transaction with logging
- `findEvent(receipt, eventName)` - Find event in receipt

**Formatting:**
- `formatBNB(amount, ethers)` - Format wei to BNB string
- `parseBNB(amount, ethers)` - Parse BNB string to wei
- `getExplorerUrl(network, type, value)` - Generate BscScan URL
- `printDeploymentSummary(deployments, network)` - Print formatted summary

**Validation:**
- `verifyBalance(signer, minBalance, ethers)` - Check sufficient balance

**Other:**
- `sleep(ms)` - Delay execution

---

## Deployment Files

### `deployments/testnet.json`
Stores all testnet deployment addresses:

```json
{
  "factory": "0x...",
  "testToken": "0x...",
  "deployer": "0x...",
  "platformFeeRecipient": "0x...",
  "pancakeRouter": "0xD99D1c33F9fC3444f8101754aBC46c52416550D1",
  "wbnb": "0xae13d989daC2f0dEbFf460aC112a837C89BAa7cd",
  "testTokenName": "Test Meme Token",
  "testTokenSymbol": "TESTMEME",
  "testTokenCreator": "0x...",
  "deployedAt": "2025-10-08T12:34:56.789Z",
  "lastUpdated": "2025-10-08T12:45:00.000Z",
  "network": "bscTestnet",
  "chainId": 97
}
```

### `deployments/mainnet.json`
Stores mainnet deployments (same structure).

---

## Environment Variables

### Required
- `PRIVATE_KEY` - Deployer private key (without 0x prefix)
- `BSCSCAN_API_KEY` - For contract verification

### Optional Deployment
- `PLATFORM_FEE_RECIPIENT` - Platform fee recipient address
- `BSC_TESTNET_RPC` - Custom testnet RPC
- `BSC_MAINNET_RPC` - Custom mainnet RPC

### Optional Token Creation
- `TOKEN_NAME` - Token name
- `TOKEN_SYMBOL` - Token symbol

### Optional Testing
- `BUY_AMOUNT` - BNB amount for test buys
- `SELL_PERCENTAGE` - Percentage to sell in test
- `AUTO_BUY` - Auto-buy to graduation threshold
- `SKIP_COOLDOWN` - Skip cooldown wait

---

## Network Configuration

### BSC Testnet (Chain ID: 97)
- RPC: https://data-seed-prebsc-1-s1.binance.org:8545/
- Explorer: https://testnet.bscscan.com
- Faucet: https://testnet.bnbchain.org/faucet-smart
- PancakeSwap Router: `0xD99D1c33F9fC3444f8101754aBC46c52416550D1`
- WBNB: `0xae13d989daC2f0dEbFf460aC112a837C89BAa7cd`

### BSC Mainnet (Chain ID: 56)
- RPC: https://bsc-dataseed1.binance.org/
- Explorer: https://bscscan.com
- PancakeSwap Router: `0x10ED43C718714eb63d5aA57B78B54704E256024E`
- WBNB: `0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c`

---

## Common Workflows

### Full Testnet Deployment
```bash
# 1. Deploy factory
npx hardhat run scripts/deploy-factory.js --network bscTestnet

# 2. Create token
npx hardhat run scripts/create-test-token.js --network bscTestnet

# 3. Test trading
BUY_AMOUNT=0.1 npx hardhat run scripts/test-buy.js --network bscTestnet
SELL_PERCENTAGE=30 npx hardhat run scripts/test-sell.js --network bscTestnet

# 4. Test graduation
AUTO_BUY=true npx hardhat run scripts/test-graduation.js --network bscTestnet

# 5. Verify contracts
npx hardhat run scripts/verify-contracts.js --network bscTestnet
```

### Quick Local Test
```bash
# Test everything locally (no testnet BNB needed)
npx hardhat run scripts/test-deployment-local.js --network hardhat
```

### Create Multiple Test Tokens
```bash
# Token 1
TOKEN_NAME="Doge Coin" TOKEN_SYMBOL="DOGE" \
  npx hardhat run scripts/create-test-token.js --network bscTestnet

# Token 2
TOKEN_NAME="Pepe Coin" TOKEN_SYMBOL="PEPE" \
  npx hardhat run scripts/create-test-token.js --network bscTestnet
```

### Simulate Full Trading Lifecycle
```bash
# Buy incrementally
BUY_AMOUNT=1.0 npx hardhat run scripts/test-buy.js --network bscTestnet
BUY_AMOUNT=5.0 npx hardhat run scripts/test-buy.js --network bscTestnet
BUY_AMOUNT=10.0 npx hardhat run scripts/test-buy.js --network bscTestnet

# Sell some
SELL_PERCENTAGE=20 npx hardhat run scripts/test-sell.js --network bscTestnet

# Buy more
BUY_AMOUNT=20.0 npx hardhat run scripts/test-buy.js --network bscTestnet

# Graduate
AUTO_BUY=true npx hardhat run scripts/test-graduation.js --network bscTestnet
```

---

## Troubleshooting

### Common Issues

**"Insufficient balance"**
- Get testnet BNB from faucet
- Check balance in wallet

**"Factory not deployed"**
- Run `deploy-factory.js` first
- Check `deployments/testnet.json` exists

**"Test token not found"**
- Run `create-test-token.js` first
- Check `deployments/testnet.json` has `testToken` field

**"Seller has no tokens"**
- Run `test-buy.js` before `test-sell.js`

**"Graduation threshold not reached"**
- Use `AUTO_BUY=true` flag
- Or manually buy more: `BUY_AMOUNT=50.0 npx hardhat run scripts/test-buy.js`

**"Verification failed"**
- Check `BSCSCAN_API_KEY` is set
- Try manual verification (script provides command)
- Wait a few minutes and retry

### Debug Mode

Add `--verbose` flag for detailed output:
```bash
npx hardhat run scripts/deploy-factory.js --network bscTestnet --verbose
```

View transaction details on BscScan:
- All scripts output transaction hashes
- All scripts output BscScan explorer URLs

---

## Security Notes

1. **Never commit private keys** - Use `.env` file (gitignored)
2. **Use dedicated wallets** - Don't use main wallet for testing
3. **Test thoroughly on testnet** - Before mainnet deployment
4. **Verify all contracts** - Transparency and trust
5. **Start with small amounts** - Test incrementally
6. **Monitor transactions** - Check BscScan during execution

---

## Support

For detailed deployment instructions, see: [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)

For contract documentation, see:
- [CONTRACTS_COMPLETE.md](./CONTRACTS_COMPLETE.md)
- [TEST_SUITE_DELIVERY.md](./TEST_SUITE_DELIVERY.md)

---

**All scripts tested and working! Ready for BSC Testnet deployment.**
