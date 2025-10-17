# Quick Start Guide - BNB Launchpad Development

## TL;DR - Setup Complete! ✅

The Hardhat environment is ready. Here's how to use it:

---

## Immediate Next Steps

### 1. Configure Environment (One-time)
```bash
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch/bnb-launchpad
cp .env.example .env
# Edit .env with your wallet private key and BSCScan API key
```

### 2. Verify Setup Works
```bash
npm test
# Should show: 7 passing
```

### 3. Start Development
Ready to implement the actual launchpad contracts!

---

## Development Workflow

### Compile Contracts
```bash
npm run compile
```

### Run Tests
```bash
npm test
```

### Deploy to Testnet
```bash
npm run deploy:testnet
```

### Start Local Node
```bash
npm run node
# In another terminal: deploy and test locally
```

---

## Project Structure

```
bnb-launchpad/
├── contracts/              # Put your .sol files here
│   ├── interfaces/        # Contract interfaces
│   └── TestContract.sol   # Example (can delete later)
│
├── test/                  # Put test files here
│   └── TestContract.test.js  # Example
│
├── scripts/               # Deployment scripts
│   └── deploy.js         # Template (update for your contracts)
│
├── hardhat.config.js     # Network config (BSC testnet/mainnet)
├── package.json          # Dependencies
└── .env                  # Your secrets (DO NOT COMMIT)
```

---

## Common Commands

### Development
```bash
npm run compile           # Compile all contracts
npm test                  # Run test suite
npm run node             # Start local Hardhat node
```

### Deployment
```bash
npm run deploy:testnet   # Deploy to BSC testnet
npm run verify           # Verify on BSCScan
```

### Testing
```bash
npx hardhat test                    # All tests
npx hardhat test test/MyTest.js    # Specific test
REPORT_GAS=true npm test           # With gas report
```

---

## Network Information

### BSC Testnet
- **Chain ID**: 97
- **RPC**: https://data-seed-prebsc-1-s1.binance.org:8545/
- **Explorer**: https://testnet.bscscan.com
- **Faucet**: https://testnet.bnbchain.org/faucet-smart (get testnet BNB)

### BSC Mainnet
- **Chain ID**: 56
- **RPC**: https://bsc-dataseed1.binance.org/
- **Explorer**: https://bscscan.com

---

## What's Already Done

✅ Hardhat installed and configured
✅ BSC testnet/mainnet networks configured
✅ OpenZeppelin contracts available
✅ Test framework ready (Mocha + Chai)
✅ Deployment script template
✅ Environment configuration template
✅ Security measures (.gitignore, .env)
✅ Compilation verified (working)
✅ Tests verified (7 passing)

---

## What's Next

### Phase 1: Implement Core Contracts
1. Create `contracts/interfaces/IPancakeRouter02.sol`
2. Create `contracts/BondingCurveToken.sol`
3. Create `contracts/TokenLaunchFactory.sol`

See ARCHITECTURE.md for full specifications.

### Phase 2: Write Tests
1. Unit tests for BondingCurveToken
2. Unit tests for TokenLaunchFactory
3. Integration tests for full flow

### Phase 3: Deploy & Verify
1. Deploy to testnet
2. Test with real transactions
3. Verify contracts on BSCScan
4. Deploy to mainnet (after audit)

---

## Getting Help

### Documentation
- **This Project**: See README.md and ARCHITECTURE.md
- **Hardhat**: https://hardhat.org/docs
- **OpenZeppelin**: https://docs.openzeppelin.com/contracts
- **BSC**: https://docs.bnbchain.org/

### Troubleshooting

**"Cannot find module"**
```bash
npm install
```

**"Invalid nonce" or transaction errors**
```bash
npx hardhat clean
rm -rf cache artifacts
npm run compile
```

**"Insufficient funds"**
- Get testnet BNB from faucet (link above)
- Check wallet has BNB for gas

---

## Security Reminders

⚠️ **NEVER commit `.env` file** (contains private key)
⚠️ **Use testnet first** before mainnet deployment
⚠️ **Verify contract source** on BSCScan after deployment
⚠️ **Test thoroughly** with small amounts first

---

**Status**: ✅ Environment Ready
**Time to implement contracts**: Estimated 4-6 hours (based on ARCHITECTURE.md)
**Built by**: A-C-Gee Civilization
