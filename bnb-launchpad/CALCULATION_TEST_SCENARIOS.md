# BNB Token Launchpad - Calculation Test Scenarios

## Purpose
This document provides **exact mathematical scenarios** with step-by-step calculations to validate all bonding curve calculations in the BNB Token Launchpad. Use these to identify calculation bugs in both smart contracts and frontend.

---

## Core Constants

```javascript
TOTAL_SUPPLY = 1,000,000,000 tokens (1e9)
VIRTUAL_BNB = 30 BNB
VIRTUAL_TOKENS = 1,073,000,191 tokens
K = VIRTUAL_BNB × VIRTUAL_TOKENS = 32,190,005,730
PLATFORM_FEE = 1% (100 bps)
CREATOR_FEE = 1% (100 bps)
TOTAL_FEE = 2% (200 bps)
```

---

## Scenario 1: Initial State (No Trades)

### Given State
```
Real BNB reserves: 0 BNB
Real token reserves: 1,000,000,000 tokens (held by contract)
Virtual BNB reserves: 30 BNB
Virtual token reserves: 1,073,000,191 tokens
K = 32,190,005,730
```

### Expected Calculations

#### Current Token Reserves (from bonding curve)
```
Total BNB = Real BNB + Virtual BNB = 0 + 30 = 30 BNB
Current Token Reserves = K / Total BNB
                       = 32,190,005,730 / 30
                       = 1,073,000,191 tokens
```

#### Current Price (BNB per token)
```
Price = Total BNB / Token Reserves
      = 30 / 1,073,000,191
      = 0.00000002796 BNB per token
      = 2.796 × 10⁻⁸ BNB per token
```

#### Current Price (tokens per BNB)
```
Inverse Price = Token Reserves / Total BNB
              = 1,073,000,191 / 30
              = 35,766,673 tokens per BNB
```

#### Market Cap (Simplified)
```
Market Cap = Real BNB Reserves × 2
           = 0 × 2
           = 0 BNB

Alternative: Total BNB × circulating supply factor
           = 30 BNB (but 0 are real, so market cap = 0)
```

### Test Code
```javascript
const ethers = require('ethers');

// Initial state
const realBnb = ethers.utils.parseEther('0');
const virtualBnb = ethers.utils.parseEther('30');
const virtualTokens = ethers.utils.parseEther('1073000191');
const K = virtualBnb.mul(virtualTokens);

// Calculate current reserves
const totalBnb = realBnb.add(virtualBnb);
const currentTokenReserves = K.div(totalBnb);

console.log('Current Token Reserves:', ethers.utils.formatEther(currentTokenReserves));
// Expected: 1073000191.0

// Calculate price (BNB per token)
const pricePerToken = totalBnb.mul(ethers.BigNumber.from('10').pow(18)).div(currentTokenReserves);
console.log('Price per token (BNB):', ethers.utils.formatEther(pricePerToken));
// Expected: 0.000000027960498 (2.796 × 10⁻⁸)

// Calculate inverse price (tokens per BNB)
const tokensPerBnb = currentTokenReserves.mul(ethers.BigNumber.from('10').pow(18)).div(totalBnb);
console.log('Tokens per BNB:', ethers.utils.formatEther(tokensPerBnb));
// Expected: 35766673.0
```

---

## Scenario 2: First Buy (0.01 BNB)

### Given State
```
User sends: 0.01 BNB
Status: Initial state (0 BNB reserves)
```

### Step-by-Step Calculation

#### Step 1: Calculate Fees
```
Platform Fee = 0.01 × 0.01 = 0.0001 BNB
Creator Fee = 0.01 × 0.01 = 0.0001 BNB
Total Fees = 0.0002 BNB
BNB to Reserves = 0.01 - 0.0002 = 0.0098 BNB
```

#### Step 2: Calculate Tokens Received
```
Current Total BNB = 0 + 30 = 30 BNB
Current Token Reserves = 32,190,005,730 / 30 = 1,073,000,191 tokens

New Total BNB = 30 + 0.0098 = 30.0098 BNB
New Token Reserves = 32,190,005,730 / 30.0098 = 1,072,650,585.67 tokens

Tokens to User = Current - New
               = 1,073,000,191 - 1,072,650,585.67
               = 349,605.33 tokens
```

#### Step 3: New State After Buy
```
Real BNB Reserves = 0.0098 BNB
Total BNB (with virtual) = 30.0098 BNB
Token Reserves = 1,072,650,585.67 tokens
Platform Fees Accumulated = 0.0001 BNB
Creator Fees Accumulated = 0.0001 BNB
```

#### Step 4: New Price
```
New Price = 30.0098 / 1,072,650,585.67
          = 0.000000027977 BNB per token
          = 2.7977 × 10⁻⁸ BNB per token

Price Increase = (2.7977 - 2.796) / 2.796
               = 0.0608% increase
```

#### Step 5: New Market Cap
```
Market Cap = Real BNB × 2
           = 0.0098 × 2
           = 0.0196 BNB
```

### Test Code
```javascript
const ethers = require('ethers');

// Initial state
let realBnb = ethers.utils.parseEther('0');
const virtualBnb = ethers.utils.parseEther('30');
const K = ethers.utils.parseEther('30').mul(ethers.utils.parseEther('1073000191'));

// User buys with 0.01 BNB
const buyAmount = ethers.utils.parseEther('0.01');

// Calculate fees
const platformFee = buyAmount.mul(100).div(10000); // 1%
const creatorFee = buyAmount.mul(100).div(10000);  // 1%
const totalFees = platformFee.add(creatorFee);
const bnbToReserve = buyAmount.sub(totalFees);

console.log('Platform Fee:', ethers.utils.formatEther(platformFee));
// Expected: 0.0001

console.log('Creator Fee:', ethers.utils.formatEther(creatorFee));
// Expected: 0.0001

console.log('BNB to Reserve:', ethers.utils.formatEther(bnbToReserve));
// Expected: 0.0098

// Calculate tokens received
const currentBnb = realBnb.add(virtualBnb);
const currentTokens = K.div(currentBnb);

const newBnb = currentBnb.add(bnbToReserve);
const newTokens = K.div(newBnb);

const tokensReceived = currentTokens.sub(newTokens);

console.log('Tokens Received:', ethers.utils.formatEther(tokensReceived));
// Expected: ~349605.33

// Update state
realBnb = realBnb.add(bnbToReserve);

// Calculate new price
const newPrice = newBnb.mul(ethers.BigNumber.from('10').pow(18)).div(newTokens);
console.log('New Price (BNB per token):', ethers.utils.formatEther(newPrice));
// Expected: 0.000000027977
```

---

## Scenario 3: Multiple Buys and Sells

### Given State
```
Start: 0 BNB reserves
Execute:
1. Buy 0.01 BNB
2. Buy 0.01 BNB
3. Buy 0.01 BNB
4. Sell 5000 tokens
5. Sell 5000 tokens
```

### Buy 1: 0.01 BNB
```
Fees: 0.0002 BNB (0.0001 platform, 0.0001 creator)
To Reserves: 0.0098 BNB
Tokens Received: 349,605.33 tokens
New Reserves: 0.0098 BNB
Total Fees: 0.0002 BNB
```

### Buy 2: 0.01 BNB
```
Starting Reserves: 0.0098 BNB
Total BNB: 30.0098 BNB
Current Token Reserves: 1,072,650,585.67 tokens

Fees: 0.0002 BNB
To Reserves: 0.0098 BNB

New Total BNB: 30.0196 BNB
New Token Reserves: 32,190,005,730 / 30.0196 = 1,072,301,462.05 tokens

Tokens Received: 1,072,650,585.67 - 1,072,301,462.05 = 349,123.62 tokens

New Reserves: 0.0196 BNB
Total Fees: 0.0004 BNB (0.0002 platform, 0.0002 creator)
```

### Buy 3: 0.01 BNB
```
Starting Reserves: 0.0196 BNB
Total BNB: 30.0196 BNB
Current Token Reserves: 1,072,301,462.05 tokens

Fees: 0.0002 BNB
To Reserves: 0.0098 BNB

New Total BNB: 30.0294 BNB
New Token Reserves: 32,190,005,730 / 30.0294 = 1,071,952,819.61 tokens

Tokens Received: 1,072,301,462.05 - 1,071,952,819.61 = 348,642.44 tokens

New Reserves: 0.0294 BNB
Total Fees: 0.0006 BNB (0.0003 platform, 0.0003 creator)
User Total Tokens: 349,605.33 + 349,123.62 + 348,642.44 = 1,047,371.39 tokens
```

### Sell 1: 5000 tokens
```
Starting Reserves: 0.0294 BNB
Total BNB: 30.0294 BNB
Current Token Reserves: 1,071,952,819.61 tokens

New Token Reserves: 1,071,952,819.61 + 5,000 = 1,071,957,819.61 tokens
New Total BNB: 32,190,005,730 / 1,071,957,819.61 = 30.0292305 BNB

Gross BNB Out: 30.0294 - 30.0292305 = 0.0001695 BNB

Fees (2%): 0.0001695 × 0.02 = 0.00000339 BNB
Net BNB to User: 0.0001695 - 0.00000339 = 0.00016611 BNB

New Real Reserves: 0.0294 - 0.0001695 = 0.02923305 BNB
Total Fees: 0.0006 + 0.00000339 = 0.00060339 BNB
```

### Sell 2: 5000 tokens
```
Starting Reserves: 0.02923305 BNB
Total BNB: 30.02923305 BNB
Current Token Reserves: 1,071,957,819.61 tokens

New Token Reserves: 1,071,957,819.61 + 5,000 = 1,071,962,819.61 tokens
New Total BNB: 32,190,005,730 / 1,071,962,819.61 = 30.02906666 BNB

Gross BNB Out: 30.02923305 - 30.02906666 = 0.00016639 BNB

Fees (2%): 0.00016639 × 0.02 = 0.00000333 BNB
Net BNB to User: 0.00016639 - 0.00000333 = 0.00016306 BNB

New Real Reserves: 0.02923305 - 0.00016639 = 0.02906666 BNB
Total Fees: 0.00060339 + 0.00000333 = 0.00060672 BNB
```

### Final State
```
Real BNB Reserves: 0.02906666 BNB
Platform Fees Accumulated: 0.00030336 BNB (should equal creator fees)
Creator Fees Accumulated: 0.00030336 BNB (should equal platform fees)
User Token Balance: 1,047,371.39 - 10,000 = 1,037,371.39 tokens
User Net BNB Spent: 0.03 - 0.00032917 = 0.02967083 BNB
```

### Fee Verification
```
Total BNB In (buys): 0.03 BNB
Total Fees from Buys: 0.0006 BNB (0.0003 each)
Total Fees from Sells: 0.00000672 BNB (0.00000336 each)
Total Fees: 0.00060672 BNB

Split: Platform = Creator = 0.00030336 BNB each

✅ CRITICAL: Platform fees MUST equal creator fees at all times
```

---

## Scenario 4: Price Chart Accuracy Test

### Purpose
Verify that frontend displays correct price after each transaction.

### Test Sequence
```
1. Initial: 0 BNB reserves
   Expected Price: 2.796 × 10⁻⁸ BNB per token

2. After Buy 0.01 BNB:
   Expected Price: 2.7977 × 10⁻⁸ BNB per token
   Expected Change: +0.0608%

3. After Buy 0.1 BNB:
   Expected Price: ~2.88 × 10⁻⁸ BNB per token
   Expected Change: +3.0%

4. After Sell 50,000 tokens:
   Expected Price: Should decrease slightly
   Expected Change: -0.13%

5. After Buy 1 BNB:
   Expected Price: ~3.2 × 10⁻⁸ BNB per token
   Expected Change: +14.4%
```

### Frontend Price Calculation (CURRENT - CHECK IF CORRECT)
```javascript
// From frontend/app.js lines 407-414
const totalSupply = ethers.utils.parseEther(CONFIG.CONSTANTS.TOTAL_SUPPLY);
const virtualBnb = ethers.utils.parseEther('30');
const currentBnbReserves = bnbReserves.add(virtualBnb);
const K = ethers.utils.parseEther('32190005730');
const currentTokenReserves = K.div(currentBnbReserves);
const price = currentBnbReserves.mul(ethers.utils.parseEther('1')).div(currentTokenReserves);
```

### ⚠️ POTENTIAL BUG IDENTIFIED

**Issue**: The price calculation multiplies by `1e18` unnecessarily, causing precision issues.

**Correct Formula**:
```javascript
// Price = Total BNB / Token Reserves
const price = currentBnbReserves.mul(1e18).div(currentTokenReserves);
// This gives: (30 × 1e18) / 1073000191e18 = 30 / 1073000191 (in wei)
// When formatted: 0.000000027960498 BNB per token ✅

// BUT the code does:
const price = currentBnbReserves.mul(ethers.utils.parseEther('1')).div(currentTokenReserves);
// This gives: (30e18 × 1e18) / 1073000191e18 = 30e18 / 1073000191 (in wei)
// When formatted: 0.027960498 BNB per token ❌ (1 billion times too large!)
```

### Fixed Price Calculation
```javascript
// CORRECT VERSION
const currentBnbReserves = bnbReserves.add(virtualBnb);
const K = virtualBnb.mul(ethers.utils.parseEther('1073000191'));
const currentTokenReserves = K.div(currentBnbReserves);

// Price per token (no extra multiplication needed)
const pricePerToken = currentBnbReserves.mul(ethers.BigNumber.from('10').pow(18)).div(currentTokenReserves);
// OR simpler:
const pricePerToken = currentBnbReserves.div(currentTokenReserves);
// Then format with extra precision if needed

console.log('Price per token:', ethers.utils.formatUnits(pricePerToken, 18));
```

---

## Scenario 5: Market Cap Calculation Test

### Current Frontend Logic
```javascript
// From frontend/app.js lines 421-423
const marketCap = parseFloat(bnbReservesFormatted) * 2;
```

### Question: Is this correct?

**Analysis**:
```
Market Cap = Total Value of All Tokens
           = Price per Token × Circulating Supply

With bonding curve:
- Total Supply: 1,000,000,000 tokens
- Held by contract: Calculated from K/x
- Circulating: 1,000,000,000 - (K/x)

At 0.01 BNB reserves:
- Token Reserves in Curve: 1,072,650,585.67
- Circulating: 1,000,000,000 - 1,072,650,585.67 = -72,650,585.67 ❌

Wait, this is impossible! Let's recalculate:
- Contract minted 1B tokens to itself
- Virtual token reserves: 1,073,000,191
- This is MORE than total supply!
```

### ⚠️ CRITICAL FINDING: Token Accounting Issue

**The Problem**:
```
Total Supply: 1,000,000,000 tokens
Virtual Token Reserves: 1,073,000,191 tokens

This means virtual reserves > total supply, which is mathematically invalid!
```

**Correct Setup Should Be**:
```
Option A: Virtual tokens should be LESS than total supply
- Total Supply: 1,000,000,000 tokens
- Virtual Reserves: 800,000,000 tokens
- Real tokens in contract: 1,000,000,000 tokens
- Users can buy up to 200,000,000 tokens before issues

Option B: Total supply should INCLUDE virtual reserves
- Total Supply: 1,073,000,191 tokens (mint this amount)
- Virtual Reserves: 1,073,000,191 tokens
- All tokens initially in contract
```

**Current Situation**:
With the current constants, users can only buy:
```
Max Buyable = Total Supply - Initial Reserve
            = 1,000,000,000 - 1,073,000,191
            = -73,000,191 tokens ❌

This will cause transactions to revert after buying ~927M tokens!
```

### Market Cap Calculation (If Fixed)

**Correct Formula**:
```javascript
// Get current price
const currentBnbReserves = bnbReserves.add(virtualBnb);
const K = virtualBnb.mul(totalSupply); // Should use actual circulatable supply
const currentTokenReserves = K.div(currentBnbReserves);
const pricePerToken = currentBnbReserves.div(currentTokenReserves);

// Circulating supply
const circulatingSupply = totalSupply.sub(currentTokenReserves);

// Market cap
const marketCap = pricePerToken.mul(circulatingSupply).div(ethers.BigNumber.from('10').pow(18));

console.log('Market Cap:', ethers.utils.formatEther(marketCap), 'BNB');
```

**Simplified Approximation (for small reserves)**:
```
Market Cap ≈ Real BNB Reserves × 2

This works because in constant product AMM:
- BNB side value ≈ Token side value
- Total liquidity ≈ 2 × BNB reserves
```

---

## Scenario 6: Graduation Threshold Test

### Target
```
Graduation triggers at: 50 BNB real reserves
```

### Calculation
```
Starting from 0, need 50 BNB in reserves after fees.

If users buy X BNB total:
- Fees: X × 0.02 = 0.02X
- To reserves: X × 0.98 = 0.98X

To reach 50 BNB:
0.98X = 50
X = 50 / 0.98 = 51.0204 BNB

Users must buy approximately 51.02 BNB worth to graduate the token.
```

### Tokens Bought at Graduation
```
Starting Token Reserves: 1,073,000,191 tokens
Total BNB at graduation: 30 + 50 = 80 BNB
Final Token Reserves: 32,190,005,730 / 80 = 402,375,071.625 tokens

Tokens Bought: 1,073,000,191 - 402,375,071.625 = 670,625,119.375 tokens
```

### Graduation State
```
Real BNB Reserves: 50 BNB
Platform Fees: 51.02 × 0.01 = 0.5102 BNB
Creator Fees: 51.02 × 0.01 = 0.5102 BNB
Total BNB in Contract: 50 + 0.5102 + 0.5102 = 51.0204 BNB
Tokens in Circulation: 670,625,119.375 tokens
Tokens in Contract: 402,375,071.625 tokens (will go to liquidity)
Price at Graduation: 80 / 402,375,071.625 = 1.988 × 10⁻⁷ BNB per token
```

### Liquidity Provision (75% of reserves)
```
BNB for Liquidity: 50 × 0.75 = 37.5 BNB
Tokens for Liquidity: Need to match price ratio

At graduation:
- Price = 80 BNB / 402,375,071.625 tokens = 1.988 × 10⁻⁷ BNB/token

For 37.5 BNB:
- Tokens needed = 37.5 / 1.988 × 10⁻⁷ = 188,634,027 tokens

LP Pair Created:
- 37.5 BNB
- 188,634,027 tokens
- Initial LP price: 1.988 × 10⁻⁷ BNB per token ✅ (matches graduation price)
```

---

## Test Scripts

### Python Test Script (Independent Verification)

```python
#!/usr/bin/env python3
"""
Independent verification of bonding curve calculations
Run: python3 test_bonding_curve.py
"""

from decimal import Decimal, getcontext

# Set high precision
getcontext().prec = 50

# Constants
VIRTUAL_BNB = Decimal('30')
VIRTUAL_TOKENS = Decimal('1073000191')
K = VIRTUAL_BNB * VIRTUAL_TOKENS
TOTAL_SUPPLY = Decimal('1000000000')
FEE_RATE = Decimal('0.02')

class BondingCurve:
    def __init__(self):
        self.real_bnb = Decimal('0')
        self.platform_fees = Decimal('0')
        self.creator_fees = Decimal('0')

    def get_token_reserves(self):
        total_bnb = self.real_bnb + VIRTUAL_BNB
        return K / total_bnb

    def get_price(self):
        total_bnb = self.real_bnb + VIRTUAL_BNB
        token_reserves = self.get_token_reserves()
        return total_bnb / token_reserves

    def buy(self, bnb_amount):
        """Simulate buy transaction"""
        fees = bnb_amount * FEE_RATE
        platform_fee = fees / 2
        creator_fee = fees / 2
        bnb_to_reserve = bnb_amount - fees

        # Calculate tokens
        current_bnb = self.real_bnb + VIRTUAL_BNB
        current_tokens = K / current_bnb

        new_bnb = current_bnb + bnb_to_reserve
        new_tokens = K / new_bnb

        tokens_received = current_tokens - new_tokens

        # Update state
        self.real_bnb += bnb_to_reserve
        self.platform_fees += platform_fee
        self.creator_fees += creator_fee

        return tokens_received

    def sell(self, token_amount):
        """Simulate sell transaction"""
        current_bnb = self.real_bnb + VIRTUAL_BNB
        current_tokens = K / current_bnb

        new_tokens = current_tokens + token_amount
        new_bnb = K / new_tokens

        gross_bnb = current_bnb - new_bnb
        fees = gross_bnb * FEE_RATE
        platform_fee = fees / 2
        creator_fee = fees / 2
        net_bnb = gross_bnb - fees

        # Update state
        self.real_bnb -= gross_bnb
        self.platform_fees += platform_fee
        self.creator_fees += creator_fee

        return net_bnb

    def print_state(self, label=""):
        print(f"\n{'='*60}")
        print(f"{label}")
        print(f"{'='*60}")
        print(f"Real BNB Reserves: {self.real_bnb:.10f} BNB")
        print(f"Token Reserves: {self.get_token_reserves():.2f} tokens")
        print(f"Price: {self.get_price():.15f} BNB per token")
        print(f"Platform Fees: {self.platform_fees:.10f} BNB")
        print(f"Creator Fees: {self.creator_fees:.10f} BNB")
        print(f"Fees Match: {self.platform_fees == self.creator_fees}")

# Run tests
def main():
    bc = BondingCurve()

    # Scenario 1: Initial state
    bc.print_state("Scenario 1: Initial State")

    # Scenario 2: First buy
    tokens = bc.buy(Decimal('0.01'))
    print(f"\n✅ Bought with 0.01 BNB, received {tokens:.2f} tokens")
    bc.print_state("Scenario 2: After First Buy")

    # Scenario 3: Multiple buys
    tokens2 = bc.buy(Decimal('0.01'))
    tokens3 = bc.buy(Decimal('0.01'))
    total_tokens = tokens + tokens2 + tokens3
    print(f"\n✅ Total tokens from 3 buys: {total_tokens:.2f}")
    bc.print_state("Scenario 3: After 3 Buys")

    # Scenario 4: Sell
    bnb_received = bc.sell(Decimal('5000'))
    print(f"\n✅ Sold 5000 tokens, received {bnb_received:.10f} BNB")
    bc.print_state("Scenario 4: After Sell")

    # Verify fees match
    print(f"\n{'='*60}")
    print("FEE VERIFICATION")
    print(f"{'='*60}")
    fee_diff = abs(bc.platform_fees - bc.creator_fees)
    if fee_diff < Decimal('0.0000000001'):
        print(f"✅ PASS: Fees match within tolerance")
    else:
        print(f"❌ FAIL: Fee mismatch: {fee_diff:.10f} BNB")

if __name__ == '__main__':
    main()
```

### JavaScript Test Script (Using ethers.js)

```javascript
/**
 * Test bonding curve calculations
 * Run: node test_calculations.js
 */

const ethers = require('ethers');

// Constants
const VIRTUAL_BNB = ethers.utils.parseEther('30');
const VIRTUAL_TOKENS = ethers.utils.parseEther('1073000191');
const K = VIRTUAL_BNB.mul(VIRTUAL_TOKENS);

class BondingCurve {
    constructor() {
        this.realBnb = ethers.BigNumber.from(0);
        this.platformFees = ethers.BigNumber.from(0);
        this.creatorFees = ethers.BigNumber.from(0);
    }

    getTokenReserves() {
        const totalBnb = this.realBnb.add(VIRTUAL_BNB);
        return K.div(totalBnb);
    }

    getPrice() {
        const totalBnb = this.realBnb.add(VIRTUAL_BNB);
        const tokenReserves = this.getTokenReserves();
        // Price = totalBnb / tokenReserves (in wei units)
        return totalBnb.mul(ethers.BigNumber.from('10').pow(18)).div(tokenReserves);
    }

    buy(bnbAmount) {
        // Calculate fees
        const fees = bnbAmount.mul(2).div(100); // 2%
        const platformFee = fees.div(2);
        const creatorFee = fees.div(2);
        const bnbToReserve = bnbAmount.sub(fees);

        // Calculate tokens
        const currentBnb = this.realBnb.add(VIRTUAL_BNB);
        const currentTokens = K.div(currentBnb);

        const newBnb = currentBnb.add(bnbToReserve);
        const newTokens = K.div(newBnb);

        const tokensReceived = currentTokens.sub(newTokens);

        // Update state
        this.realBnb = this.realBnb.add(bnbToReserve);
        this.platformFees = this.platformFees.add(platformFee);
        this.creatorFees = this.creatorFees.add(creatorFee);

        return tokensReceived;
    }

    sell(tokenAmount) {
        const currentBnb = this.realBnb.add(VIRTUAL_BNB);
        const currentTokens = K.div(currentBnb);

        const newTokens = currentTokens.add(tokenAmount);
        const newBnb = K.div(newTokens);

        const grossBnb = currentBnb.sub(newBnb);
        const fees = grossBnb.mul(2).div(100);
        const platformFee = fees.div(2);
        const creatorFee = fees.div(2);
        const netBnb = grossBnb.sub(fees);

        // Update state
        this.realBnb = this.realBnb.sub(grossBnb);
        this.platformFees = this.platformFees.add(platformFee);
        this.creatorFees = this.creatorFees.add(creatorFee);

        return netBnb;
    }

    printState(label = "") {
        console.log('\n' + '='.repeat(60));
        console.log(label);
        console.log('='.repeat(60));
        console.log('Real BNB Reserves:', ethers.utils.formatEther(this.realBnb), 'BNB');
        console.log('Token Reserves:', ethers.utils.formatEther(this.getTokenReserves()));
        console.log('Price:', ethers.utils.formatEther(this.getPrice()), 'BNB per token');
        console.log('Platform Fees:', ethers.utils.formatEther(this.platformFees), 'BNB');
        console.log('Creator Fees:', ethers.utils.formatEther(this.creatorFees), 'BNB');
        console.log('Fees Match:', this.platformFees.eq(this.creatorFees));
    }
}

// Run tests
async function main() {
    const bc = new BondingCurve();

    // Scenario 1: Initial state
    bc.printState('Scenario 1: Initial State');

    // Scenario 2: First buy
    const tokens1 = bc.buy(ethers.utils.parseEther('0.01'));
    console.log('\n✅ Bought with 0.01 BNB, received', ethers.utils.formatEther(tokens1), 'tokens');
    bc.printState('Scenario 2: After First Buy');

    // Scenario 3: Multiple buys
    const tokens2 = bc.buy(ethers.utils.parseEther('0.01'));
    const tokens3 = bc.buy(ethers.utils.parseEther('0.01'));
    const totalTokens = tokens1.add(tokens2).add(tokens3);
    console.log('\n✅ Total tokens from 3 buys:', ethers.utils.formatEther(totalTokens));
    bc.printState('Scenario 3: After 3 Buys');

    // Scenario 4: Sell
    const bnbReceived = bc.sell(ethers.utils.parseEther('5000'));
    console.log('\n✅ Sold 5000 tokens, received', ethers.utils.formatEther(bnbReceived), 'BNB');
    bc.printState('Scenario 4: After Sell');

    // Verify fees
    console.log('\n' + '='.repeat(60));
    console.log('FEE VERIFICATION');
    console.log('='.repeat(60));
    const feeDiff = bc.platformFees.sub(bc.creatorFees).abs();
    if (feeDiff.lte(ethers.utils.parseEther('0.0000000001'))) {
        console.log('✅ PASS: Fees match within tolerance');
    } else {
        console.log('❌ FAIL: Fee mismatch:', ethers.utils.formatEther(feeDiff), 'BNB');
    }
}

main().catch(console.error);
```

---

## Critical Bugs Identified

### Bug 1: Price Calculation Overflow
**Location**: `frontend/app.js` line 413
**Issue**: Multiplying by `1e18` twice causes price to be 1 billion times too large
**Fix**: Remove the extra multiplication

```javascript
// WRONG (current)
const price = currentBnbReserves.mul(ethers.utils.parseEther('1')).div(currentTokenReserves);

// CORRECT
const price = currentBnbReserves.mul(ethers.BigNumber.from('10').pow(18)).div(currentTokenReserves);
// OR simpler:
const price = currentBnbReserves.div(currentTokenReserves);
```

### Bug 2: Virtual Token Reserves Exceed Total Supply
**Location**: Contract constants
**Issue**: `VIRTUAL_TOKEN_RESERVES = 1,073,000,191` but `TOTAL_SUPPLY = 1,000,000,000`
**Impact**: Users can only buy 927M tokens before contract runs out
**Fix**: Either increase total supply or decrease virtual reserves

```solidity
// OPTION A: Increase total supply
uint256 public constant TOTAL_TOKEN_SUPPLY = 1_100_000_000 * 1e18;

// OPTION B: Decrease virtual reserves
uint256 public constant VIRTUAL_TOKEN_RESERVES = 800_000_000 * 1e18;
```

### Bug 3: K Calculation May Overflow
**Location**: Contract constant calculation
**Issue**: `K = 30 * 1,073,000,191` calculated without proper precision
**Fix**: Use explicit decimal handling

```solidity
// Verify K is calculated correctly with 18 decimals
uint256 public constant K = VIRTUAL_BNB_RESERVES * VIRTUAL_TOKEN_RESERVES;
// Should equal: 32,190,005,730 * 10^36 (wei * wei)
```

---

## How to Use This Document

1. **Run Python script** to verify math independently
2. **Run JavaScript script** to test with ethers.js (matches contract)
3. **Compare outputs** with live contract transactions
4. **Fix bugs** identified in Critical Bugs section
5. **Re-test** all scenarios after fixes

---

## Expected Outputs Summary

| Scenario | BNB In | Tokens Out | Price After | Fees |
|----------|--------|-----------|-------------|------|
| Initial | 0 | 0 | 2.796e-8 | 0 |
| Buy 0.01 | 0.01 | 349,605 | 2.7977e-8 | 0.0002 |
| Buy 0.01 (2nd) | 0.01 | 349,124 | 2.7994e-8 | 0.0002 |
| Buy 0.01 (3rd) | 0.01 | 348,642 | 2.8011e-8 | 0.0002 |
| Sell 5000 | -0.00017 | -5,000 | 2.8006e-8 | 0.0000034 |
| Sell 5000 (2nd) | -0.00016 | -5,000 | 2.8001e-8 | 0.0000033 |

---

**Document Created**: 2025-10-08
**Purpose**: Bug identification and calculation verification
**Status**: Ready for testing
