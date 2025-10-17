# BNB Token Launchpad - Frontend

A beautiful, functional frontend for the BNB Token Launchpad on BSC Testnet.

## Features

✅ **Wallet Integration**
- MetaMask connection
- Auto-switch to BSC Testnet
- Real-time balance updates

✅ **Token Creation**
- Create new tokens through factory
- Instant deployment to bonding curve
- Auto-refresh token list

✅ **Trading Interface**
- Buy tokens with BNB
- Sell tokens back for BNB
- Real-time price estimates
- Slippage protection

✅ **Fee Tracking**
- Track creator fees earned (1%)
- Track platform fees earned (1%)
- One-click fee withdrawal
- Real-time updates

✅ **Analytics & Visualization**
- Live price chart (updates every 10 seconds)
- Trading volume bar chart
- Graduation progress bar (toward 50 BNB)
- Market cap calculation

✅ **Activity Feed**
- Recent transactions
- Success/error notifications
- Timestamped events

## Quick Start

### 1. Open in Browser

Simply open `index.html` in your browser (Chrome/Brave recommended):

```bash
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch/bnb-launchpad/frontend
open index.html  # Mac
xdg-open index.html  # Linux
start index.html  # Windows
```

Or use a simple HTTP server:

```bash
# Python
python3 -m http.server 8000

# Node.js
npx http-server

# Then open: http://localhost:8000
```

### 2. Connect MetaMask

- Click "Connect Wallet"
- Approve MetaMask connection
- Auto-switches to BSC Testnet (or prompts to add it)

### 3. Create a Token

- Enter token name (e.g., "Meme Coin")
- Enter symbol (e.g., "MEME")
- Click "Create Token" (costs ~0.02 tBNB)
- Wait for confirmation
- Token appears in dropdown

### 4. Trade

**Buy Tokens:**
- Select your token from dropdown
- Enter BNB amount (min 0.001)
- See estimated tokens you'll receive
- Click "Buy Tokens"

**Sell Tokens:**
- Enter token amount to sell (min 1000)
- See estimated BNB you'll receive
- Click "Sell Tokens"

### 5. Track Earnings

- **Creator Fees**: Earned as creator of a token (1% of all trades)
- **Platform Fees**: Earned as platform operator (1% of all trades)
- Click "Withdraw" buttons to claim fees

## Configuration

Contract addresses are in `config.js`:

```javascript
CONTRACTS: {
    factory: '0x5FD5a0914864B4A28fA7423b8BFAf436F210CEfC',
    pancakeRouter: '0xD99D1c33F9fC3444f8101754aBC46c52416550D1'
}
```

To change networks (mainnet vs testnet), update the `NETWORK` section.

## Screenshots

### Main Interface
- **Left**: Token creation & fee dashboard
- **Center**: Token stats & buy/sell interface
- **Right**: Price chart, volume chart, activity feed

### Key Metrics Displayed
- Current token price (BNB per token)
- BNB reserves in bonding curve
- Your token balance
- Market cap
- Graduation progress (to 50 BNB)

## Technical Stack

- **Frontend**: Pure HTML/CSS/JavaScript (no build required)
- **Styling**: Tailwind CSS (via CDN)
- **Web3**: Ethers.js v5
- **Charts**: Chart.js
- **Network**: BSC Testnet

## File Structure

```
frontend/
├── index.html      # Main UI
├── app.js          # Application logic
├── config.js       # Contract addresses & ABIs
└── README.md       # This file
```

## Contract Interactions

### Factory Contract
- `createToken()` - Deploy new token
- `getAllTokens()` - List all tokens
- `getTokenCount()` - Total tokens created

### Token Contract
- `buy()` - Purchase tokens with BNB
- `sell()` - Sell tokens for BNB
- `withdrawFees()` - Claim earned fees
- `balanceOf()` - Check token balance
- `bnbReserves()` - Check BNB in curve
- `pendingFees()` - Check unclaimed fees

## Fee Structure

**Every trade (buy/sell):**
- 1% → Token Creator
- 1% → Platform
- 98% → Bonding Curve Reserves

Fees are stored in contract and withdrawn on-demand via "Withdraw" buttons.

## Bonding Curve Math

**Constant Product Formula**: `x * y = k`
- x = BNB reserves (+ 30 virtual BNB)
- y = Token reserves (+ 1.073B virtual tokens)
- k = 32,190,005,730 (constant)

**Price increases as BNB reserves grow.**

**Graduation**: At 50 BNB reserves, token graduates to PancakeSwap with automated liquidity provision.

## Testing with Multiple Wallets

To test the full flow:

1. **Wallet 1 (Creator)**:
   - Create token
   - Buy some tokens
   - Check creator fees earned

2. **Wallet 2 (Trader)**:
   - Buy tokens from same contract
   - Sell tokens
   - Watch creator fees increase

3. **Both Wallets**:
   - Watch live price chart update
   - See volume accumulate
   - Track graduation progress

## Troubleshooting

### "Please install MetaMask"
- Install MetaMask browser extension

### "Wrong network" / Auto-switch fails
- Manually add BSC Testnet to MetaMask:
  - Network Name: BSC Testnet
  - RPC URL: https://data-seed-prebsc-1-s1.binance.org:8545/
  - Chain ID: 97
  - Currency: tBNB
  - Explorer: https://testnet.bscscan.com

### "Insufficient funds"
- Get testnet BNB from faucets (see main README)

### Transactions failing
- Check you have enough BNB for gas
- Check minimum amounts (0.001 BNB for buys, 1000 tokens for sells)
- Check slippage if someone traded right before you

### Charts not updating
- Charts auto-update when you select a token
- Manual refresh: select another token, then select yours again

## Security Notes

⚠️ **Testnet Only**: This is configured for BSC Testnet. Never use real funds on testnet!

⚠️ **Smart Contract Risk**: Contracts are unaudited. Use at your own risk.

⚠️ **Private Keys**: Never share your private key or seed phrase. Frontend only uses MetaMask - never asks for keys.

## Next Steps

**For Production:**
1. Professional security audit
2. Update contract addresses for mainnet
3. Add mainnet RPC endpoints
4. Implement proper error handling
5. Add transaction history API
6. Add token metadata (logos, descriptions)
7. Implement advanced charts (TradingView)
8. Add wallet connection options (WalletConnect, Coinbase)

## Links

- **Testnet Explorer**: https://testnet.bscscan.com
- **Factory**: https://testnet.bscscan.com/address/0x5FD5a0914864B4A28fA7423b8BFAf436F210CEfC
- **Test Token**: https://testnet.bscscan.com/address/0x0B7145f6c99Ec2410e9147F0055D075A3fFEFEc1
- **PancakeSwap Testnet**: https://pancake.kiemtienonline360.com/ (testnet UI)

## Support

Issues? Questions?
- Check contract addresses in `config.js`
- Verify you're on BSC Testnet (Chain ID 97)
- Check browser console for errors (F12)
- Ensure MetaMask is unlocked

---

**Built with ❤️ for the BNB Chain community**

Version: 1.0.0
Last Updated: 2025-10-08
