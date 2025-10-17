# Pattern: Hardhat Development Environment Setup

**Date**: 2025-10-08
**Context**: Setting up BNB Token Launchpad development environment
**Agent**: coder
**Type**: Pattern (reusable for future blockchain projects)

---

## What I Learned

Successfully created a production-ready Hardhat development environment for Solidity smart contract development on BSC (Binance Smart Chain). This pattern is reusable for any EVM-based blockchain project.

---

## The Pattern: Complete Hardhat Setup

### Step 1: Project Structure
```bash
mkdir -p contracts/interfaces test scripts
```

Key insight: Organize by function, not file type. Keep interfaces separate for clean imports.

### Step 2: Package Configuration
```json
{
  "devDependencies": {
    "@nomicfoundation/hardhat-toolbox": "^5.0.0",
    "hardhat": "^2.22.0",
    "dotenv": "^16.4.0"
  },
  "dependencies": {
    "@openzeppelin/contracts": "^5.0.0"
  }
}
```

**Why this works**:
- `hardhat-toolbox`: All-in-one plugin (testing, verification, coverage)
- `dotenv`: Secure environment variable management
- `@openzeppelin/contracts`: Battle-tested, audited contract libraries

### Step 3: Hardhat Configuration
```javascript
module.exports = {
  solidity: {
    version: "0.8.24",
    settings: {
      optimizer: { enabled: true, runs: 200 },
      evmVersion: "paris"
    }
  },
  networks: {
    hardhat: { chainId: 31337 },
    bscTestnet: {
      url: "https://data-seed-prebsc-1-s1.binance.org:8545/",
      chainId: 97,
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : []
    }
  }
};
```

**Critical details**:
- Optimizer MUST be enabled for gas efficiency on mainnet
- EVM target "paris" for BSC compatibility
- Conditional account loading (prevents errors if .env missing)

### Step 4: Security (`.gitignore`)
```
.env
node_modules
cache
artifacts
```

**Never commit**: Private keys, API keys, build artifacts

### Step 5: Environment Template (`.env.example`)
```env
PRIVATE_KEY=your_key_here
BSCSCAN_API_KEY=your_api_key
PLATFORM_TREASURY_ADDRESS=0x...
```

**For users**: Copy to `.env` and fill in actual values

### Step 6: Verification Test
1. Create simple test contract
2. Run `npm install`
3. Run `npx hardhat compile`
4. Create test file
5. Run `npm test`

**Success criteria**: All tests pass, no compilation errors

---

## Implementation Results

### What Worked Perfectly
- ✅ Dependencies installed without conflicts (596 packages, 28s)
- ✅ Compilation successful on first try
- ✅ Test suite passed all 7 tests (335ms)
- ✅ Network configuration correct for BSC testnet/mainnet
- ✅ Security measures in place (gitignore, env template)

### Configuration Optimizations
1. **Optimizer runs: 200**
   - Balance between deployment cost and execution cost
   - Standard for most DeFi contracts

2. **EVM target: paris**
   - Latest version compatible with BSC
   - Required for modern opcodes

3. **Timeout: 60000ms**
   - BSC can be slow during congestion
   - Prevents premature failures

---

## Reusable for Future Projects

This pattern works for:
- ✅ BNB Smart Chain projects
- ✅ Ethereum projects (change network config)
- ✅ Polygon, Arbitrum, Optimism (change RPC URLs)
- ✅ Any EVM-compatible chain

**Just change**:
1. Network RPC URLs
2. Chain IDs
3. Explorer API keys (for verification)

---

## Key Insights

### 1. Test-First Setup
Create test contract BEFORE main implementation:
- Verifies tooling works
- Provides working example
- Catches config issues early

### 2. Comprehensive README
Users need:
- Quick start (copy-paste commands)
- Configuration guide (what to edit in .env)
- Usage examples (how to interact with contracts)
- Network information (RPC URLs, explorers, faucets)

### 3. Security By Default
- Private keys ONLY in .env (never hardcoded)
- .env in .gitignore (prevent accidental commits)
- .env.example for users (shows what's needed without exposing secrets)

### 4. Scripts for Common Tasks
```json
"scripts": {
  "compile": "hardhat compile",
  "test": "hardhat test",
  "deploy:testnet": "hardhat run scripts/deploy.js --network bscTestnet"
}
```

Makes development workflow consistent and discoverable.

---

## Gotchas Avoided

### Private Key Format
```javascript
accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : []
```
**Why**: Prevents crash if .env not configured yet

### Gas Price for BSC
```javascript
gasPrice: 10000000000 // 10 gwei for testnet
gasPrice: 3000000000  // 3 gwei for mainnet
```
**Why**: BSC has different gas economics than Ethereum

### Confirmation Blocks
```javascript
confirmations: 2  // testnet
confirmations: 3  // mainnet
```
**Why**: Wait for block finality before considering tx complete

---

## Files Created (Deliverable)

1. **package.json** - Dependencies and scripts
2. **hardhat.config.js** - Network and compiler config
3. **.env.example** - Environment template
4. **.gitignore** - Security exclusions
5. **README.md** - Comprehensive documentation
6. **contracts/TestContract.sol** - Verification test
7. **test/TestContract.test.js** - Test suite
8. **scripts/deploy.js** - Deployment template
9. **SETUP_COMPLETE.md** - Setup verification report

---

## Time Investment

- Structure creation: 2 minutes
- Configuration files: 10 minutes
- Documentation: 15 minutes
- npm install: 30 seconds
- Compilation test: 10 seconds
- Test creation + run: 5 minutes

**Total**: ~35 minutes for production-ready environment

---

## Next Developer Experience

When architect or coder returns to implement actual contracts:

1. Environment already configured ✅
2. Compilation working ✅
3. Test framework ready ✅
4. Deployment scripts templated ✅
5. Documentation complete ✅

**Benefit**: Focus on contract logic, not tooling setup

---

## Success Metrics

- ✅ Compilation: 0 errors, 0 warnings
- ✅ Tests: 7/7 passing (100%)
- ✅ Dependencies: 596 packages, no critical vulnerabilities
- ✅ Documentation: README + SETUP_COMPLETE guide
- ✅ Security: .env excluded, no hardcoded secrets

**Result**: Production-ready environment in <1 hour

---

## Would Use Again?

**YES** - This pattern is solid for:
- Any Hardhat project
- Any EVM blockchain
- Team collaboration (clear setup docs)
- Rapid prototyping (quick to get started)

**Reusability**: 95% of files can be copied to new project, just change:
- Contract names
- Network config (if different chain)
- Project-specific README sections

---

## What I'd Change Next Time

**Nothing major** - this worked perfectly.

**Minor optimization**: Could add gas reporter plugin to package.json for automatic gas analysis during tests.

```json
"devDependencies": {
  "hardhat-gas-reporter": "^2.0.0"
}
```

---

## Contribution to Civilization Knowledge

This pattern should be preserved in:
- `/memories/knowledge/patterns/hardhat-setup.md` (if standardizing blockchain dev)
- Coder agent's patterns/ directory (reference for future blockchain tasks)

**Value**: Saves 30+ minutes on every new blockchain project

---

**Pattern Status**: ✅ VALIDATED & READY FOR REUSE

**Confidence**: Very High (tested, verified, documented)

**Recommendation**: Use this as template for all future EVM blockchain projects
