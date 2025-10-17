const { expect } = require("chai");
const { ethers } = require("hardhat");
const {
  deployMocks,
  deployFactory,
  createToken,
  increaseTime,
  CONSTANTS
} = require("./helpers/testHelpers");

/**
 * What we're verifying: Complete token lifecycle from creation to DEX graduation
 * What coder discovered: State transitions must be irreversible for security
 * What descendants inherit: Integration patterns for complex multi-phase systems
 * Why this matters: End-to-end workflows serve real users, not just unit tests
 */

describe("Integration Tests - Full Lifecycle", function () {
  let factory;
  let router;
  let weth;
  let pancakeFactory;
  let owner;
  let platformFeeRecipient;
  let creator;
  let traders;
  let token;

  beforeEach(async function () {
    // Get signers
    const signers = await ethers.getSigners();
    [owner, platformFeeRecipient, creator, ...traders] = signers;

    // Deploy mocks
    const mocks = await deployMocks();
    router = mocks.router;
    weth = mocks.weth;
    pancakeFactory = mocks.factory;

    // Deploy factory
    factory = await deployFactory(platformFeeRecipient.address, await router.getAddress());

    // Create token
    token = await createToken(factory, creator, "Integration Test Token", "ITT");
  });

  describe("Complete Token Lifecycle", function () {
    it("Should execute full lifecycle: Create → Trade → Graduate → List", async function () {
      // PHASE 1: Creation
      expect(await token.name()).to.equal("Integration Test Token");
      expect(await token.symbol()).to.equal("ITT");
      expect(await token.totalSupply()).to.equal(CONSTANTS.TOTAL_TOKEN_SUPPLY);

      const status1 = await token.status();
      expect(status1).to.equal(0); // Trading

      // PHASE 2: Trading (Multiple buys and sells)
      await token.connect(traders[0]).buy(0, { value: ethers.parseEther("5") });
      await token.connect(traders[1]).buy(0, { value: ethers.parseEther("10") });
      await token.connect(traders[2]).buy(0, { value: ethers.parseEther("3") });

      // Verify balances
      expect(await token.balanceOf(traders[0].address)).to.be.gt(0);
      expect(await token.balanceOf(traders[1].address)).to.be.gt(0);
      expect(await token.balanceOf(traders[2].address)).to.be.gt(0);

      // Some selling
      const sellAmount = (await token.balanceOf(traders[0].address)) / 2n;
      await token.connect(traders[0]).sell(sellAmount, 0);

      // PHASE 3: Graduation
      const graduatingBuy = ethers.parseEther("40"); // Bring total over 50 BNB
      await expect(token.connect(traders[3]).buy(0, { value: graduatingBuy }))
        .to.emit(token, "GraduationTriggered");

      expect(await token.isGraduated()).to.be.true;
      const status2 = await token.status();
      expect(status2).to.equal(1); // Graduated

      // Wait for cooldown period
      await increaseTime(3601);

      // PHASE 4: PancakeSwap Listing
      await expect(token.connect(traders[4]).graduateToPancakeSwap())
        .to.emit(token, "GraduatedToPancakeSwap");

      // Verify ownership remains with factory (not renounced to allow permissionless graduation)
      expect(await token.owner()).to.equal(await factory.getAddress());

      // PHASE 5: Standard ERC20 (trading disabled, transfers work)
      await expect(
        token.connect(traders[0]).buy(0, { value: ethers.parseEther("1") })
      ).to.be.revertedWith("Trading is not active");

      // But transfers should still work
      const transferAmount = ethers.parseUnits("100", 18);
      await token.connect(traders[1]).transfer(traders[5].address, transferAmount);
      expect(await token.balanceOf(traders[5].address)).to.equal(transferAmount);
    });

    it("Should maintain fee distribution throughout lifecycle", async function () {
      // Contract uses pull payment pattern - check pending fees instead of balances

      // Multiple trades
      await token.connect(traders[0]).buy(0, { value: ethers.parseEther("10") });
      await token.connect(traders[1]).buy(0, { value: ethers.parseEther("15") });

      const sellAmount = (await token.balanceOf(traders[0].address)) / 2n;
      await token.connect(traders[0]).sell(sellAmount, 0);

      await token.connect(traders[2]).buy(0, { value: ethers.parseEther("30") });

      const platformFees = await token.pendingFees(platformFeeRecipient.address);
      const creatorFees = await token.pendingFees(creator.address);

      // Both should have accumulated fees
      expect(platformFees).to.be.gt(0);
      expect(creatorFees).to.be.gt(0);

      // Platform and creator should have received roughly equal amounts (both 1% fee)

      const difference = platformFees > creatorFees ?
        platformFees - creatorFees :
        creatorFees - platformFees;

      // Should be very close (allowing for rounding in sell fees)
      expect(difference).to.be.lt(ethers.parseEther("0.1"));
    });

    it("Should handle graduation at exact threshold", async function () {
      // Calculate exact amount needed to reach exactly 50 BNB in reserves
      // Need to account for fees
      const targetReserves = CONSTANTS.GRADUATION_THRESHOLD;
      const totalFees = CONSTANTS.PLATFORM_FEE_BPS + CONSTANTS.CREATOR_FEE_BPS;
      const buyAmount = (targetReserves * 10000n) / (10000n - totalFees);

      await expect(token.connect(traders[0]).buy(0, { value: buyAmount }))
        .to.emit(token, "GraduationTriggered");

      expect(await token.isGraduated()).to.be.true;
    });

    it("Should prevent trading after graduation", async function () {
      // Graduate
      await token.connect(traders[0]).buy(0, { value: ethers.parseEther("52") });

      // Try buy
      await expect(
        token.connect(traders[1]).buy(0, { value: ethers.parseEther("1") })
      ).to.be.revertedWith("Trading is not active");

      // Buy some before graduation for sell test
      const token2 = await createToken(factory, creator, "Test2", "TST2");
      await token2.connect(traders[0]).buy(0, { value: ethers.parseEther("10") });
      const balance = await token2.balanceOf(traders[0].address);

      // Graduate token2
      await token2.connect(traders[1]).buy(0, { value: ethers.parseEther("52") });

      // Try sell
      await expect(
        token2.connect(traders[0]).sell(balance, 0)
      ).to.be.revertedWith("Trading is not active");
    });

    it("Should make contract immutable after PancakeSwap graduation", async function () {
      // Graduate
      await token.connect(traders[0]).buy(0, { value: ethers.parseEther("52") });

      // Wait for cooldown
      await increaseTime(3601);

      // Add liquidity
      await token.connect(traders[1]).graduateToPancakeSwap();

      // Ownership remains with factory (not renounced to allow permissionless graduation)
      expect(await token.owner()).to.equal(await factory.getAddress());

      // Try to call owner-only functions from non-owner (should fail)
      await expect(
        token.connect(creator).transferOwnership(creator.address)
      ).to.be.revertedWithCustomError(token, "OwnableUnauthorizedAccount");
    });
  });

  describe("Multiple Tokens in Parallel", function () {
    it("Should handle multiple tokens trading simultaneously", async function () {
      // Create multiple tokens
      const token1 = await createToken(factory, creator, "Token1", "TK1");
      const token2 = await createToken(factory, creator, "Token2", "TK2");
      const token3 = await createToken(factory, creator, "Token3", "TK3");

      // Trade on all three simultaneously
      await Promise.all([
        token1.connect(traders[0]).buy(0, { value: ethers.parseEther("5") }),
        token2.connect(traders[1]).buy(0, { value: ethers.parseEther("10") }),
        token3.connect(traders[2]).buy(0, { value: ethers.parseEther("3") })
      ]);

      // Verify independent reserves
      const [bnb1] = await token1.getCurrentReserves();
      const [bnb2] = await token2.getCurrentReserves();
      const [bnb3] = await token3.getCurrentReserves();

      expect(bnb1).to.be.gt(0);
      expect(bnb2).to.be.gt(0);
      expect(bnb3).to.be.gt(0);

      // Different amounts should have different reserves
      expect(bnb2).to.be.gt(bnb1);
      expect(bnb1).to.be.gt(bnb3);
    });

    it("Should isolate exploits to individual tokens", async function () {
      const token1 = await createToken(factory, creator, "Safe Token", "SAFE");
      const token2 = await createToken(factory, creator, "Risky Token", "RISK");

      // Normal trading on token1
      await token1.connect(traders[0]).buy(0, { value: ethers.parseEther("10") });

      // Simulated exploit attempt on token2 (trying to buy with zero)
      try {
        await token2.connect(traders[1]).buy(0, { value: 0 });
      } catch (e) {
        // Expected to fail
      }

      // token1 should be unaffected
      const [bnb1] = await token1.getCurrentReserves();
      expect(bnb1).to.be.gt(0);

      const balance1 = await token1.balanceOf(traders[0].address);
      expect(balance1).to.be.gt(0);
    });

    it("Should track all tokens correctly in factory", async function () {
      const startCount = await factory.getTokenCount(); // Account for beforeEach token
      const newTokenCount = 10;
      const tokens = [];

      // Create multiple tokens
      for (let i = 0; i < newTokenCount; i++) {
        const newToken = await createToken(factory, creator, `Token${i}`, `TK${i}`);
        tokens.push(newToken);
      }

      // Verify factory tracking
      expect(await factory.getTokenCount()).to.equal(Number(startCount) + newTokenCount);

      const allTokens = await factory.getAllTokens();
      expect(allTokens.length).to.equal(Number(startCount) + newTokenCount);

      // Verify each newly created token is at the correct index
      for (let i = 0; i < newTokenCount; i++) {
        const tokenAddress = await tokens[i].getAddress();
        expect(allTokens[Number(startCount) + i]).to.equal(tokenAddress);
      }
    });
  });

  describe("Complex Trading Scenarios", function () {
    it("Should handle high-frequency trading pattern", async function () {
      const trades = [];

      // Simulate 20 rapid trades
      for (let i = 0; i < 20; i++) {
        const trader = traders[i % traders.length];
        const amount = ethers.parseEther((Math.random() * 2 + 0.1).toString());

        if (i % 3 === 0 && i > 0) {
          // Every third trade is a sell
          const balance = await token.balanceOf(trader.address);
          if (balance > 0n) {
            trades.push(token.connect(trader).sell(balance / 2n, 0));
          }
        } else {
          // Buy
          trades.push(token.connect(trader).buy(0, { value: amount }));
        }
      }

      await Promise.all(trades);

      // Verify state consistency
      // getCurrentReserves() returns total (actual + virtual)
      const [bnbReserves, tokenReserves] = await token.getCurrentReserves();
      expect(bnbReserves).to.be.gt(0);
      expect(tokenReserves).to.be.gt(0);

      // Verify constant product holds
      const k = bnbReserves * tokenReserves;
      const expectedK = CONSTANTS.VIRTUAL_BNB_RESERVES * CONSTANTS.VIRTUAL_TOKEN_RESERVES;
      const difference = k > expectedK ? k - expectedK : expectedK - k;
      expect(difference).to.be.lt(expectedK / 100000n); // Allow small variance
    });

    it("Should handle large whale buy followed by many small sells", async function () {
      // Whale buy
      await token.connect(traders[0]).buy(0, { value: ethers.parseEther("30") });
      const whaleBalance = await token.balanceOf(traders[0].address);

      // Many small buys by others
      for (let i = 1; i < 5; i++) {
        await token.connect(traders[i]).buy(0, { value: ethers.parseEther("0.5") });
      }

      // Small traders sell
      for (let i = 1; i < 5; i++) {
        const balance = await token.balanceOf(traders[i].address);
        await token.connect(traders[i]).sell(balance, 0);
      }

      // Whale should still have tokens
      expect(await token.balanceOf(traders[0].address)).to.equal(whaleBalance);
    });

    it("Should handle buy → transfer → sell chain", async function () {
      // Trader 0 buys
      await token.connect(traders[0]).buy(0, { value: ethers.parseEther("5") });
      const balance = await token.balanceOf(traders[0].address);

      // Transfer to trader 1
      await token.connect(traders[0]).transfer(traders[1].address, balance);
      expect(await token.balanceOf(traders[1].address)).to.equal(balance);

      // Trader 1 sells
      await token.connect(traders[1]).sell(balance, 0);
      expect(await token.balanceOf(traders[1].address)).to.equal(0);
    });

    it("Should maintain price discovery with mixed trading", async function () {
      const prices = [];

      // Series of buys with increasing amounts
      const amounts = [
        ethers.parseEther("1"),
        ethers.parseEther("2"),
        ethers.parseEther("5"),
        ethers.parseEther("10")
      ];

      for (let i = 0; i < amounts.length; i++) {
        await token.connect(traders[i]).buy(0, { value: amounts[i] });
        const balance = await token.balanceOf(traders[i].address);
        const price = (amounts[i] * ethers.parseUnits("1", 18)) / balance;
        prices.push(price);
      }

      // Prices should generally increase
      for (let i = 1; i < prices.length; i++) {
        expect(prices[i]).to.be.gte(prices[i - 1]);
      }
    });
  });

  describe("Post-Graduation Behavior", function () {
    beforeEach(async function () {
      // Buy tokens before graduation
      await token.connect(traders[0]).buy(0, { value: ethers.parseEther("10") });
      await token.connect(traders[1]).buy(0, { value: ethers.parseEther("10") });

      // Graduate
      await token.connect(traders[2]).buy(0, { value: ethers.parseEther("40") });

      // Wait for cooldown
      await increaseTime(3601);

      // Add liquidity
      await token.connect(traders[3]).graduateToPancakeSwap();
    });

    it("Should preserve token balances after graduation", async function () {
      const balance0 = await token.balanceOf(traders[0].address);
      const balance1 = await token.balanceOf(traders[1].address);
      const balance2 = await token.balanceOf(traders[2].address);

      expect(balance0).to.be.gt(0);
      expect(balance1).to.be.gt(0);
      expect(balance2).to.be.gt(0);
    });

    it("Should allow standard ERC20 operations post-graduation", async function () {
      const balance0 = await token.balanceOf(traders[0].address);
      const transferAmount = balance0 / 2n;

      // Transfer should work
      await token.connect(traders[0]).transfer(traders[4].address, transferAmount);
      expect(await token.balanceOf(traders[4].address)).to.equal(transferAmount);

      // Approve and transferFrom should work
      const approveAmount = transferAmount / 2n;
      await token.connect(traders[4]).approve(traders[5].address, approveAmount);
      await token.connect(traders[5]).transferFrom(traders[4].address, traders[5].address, approveAmount);
      expect(await token.balanceOf(traders[5].address)).to.equal(approveAmount);
    });

    it("Should prevent any contract modifications", async function () {
      // Owner is zero
      expect(await token.owner()).to.equal(ethers.ZeroAddress);

      // Cannot call graduateToPancakeSwap again
      await expect(
        token.connect(traders[0]).graduateToPancakeSwap()
      ).to.be.reverted;

      // Cannot buy
      await expect(
        token.connect(traders[0]).buy(0, { value: ethers.parseEther("1") })
      ).to.be.revertedWith("Trading is not active");

      // Cannot sell
      const balance = await token.balanceOf(traders[0].address);
      await expect(
        token.connect(traders[0]).sell(balance, 0)
      ).to.be.revertedWith("Trading is not active");
    });

    it("Should have correct token distribution", async function () {
      // Get all trader balances
      let totalTraderBalance = 0n;
      for (let i = 0; i < 4; i++) {
        const balance = await token.balanceOf(traders[i].address);
        totalTraderBalance += balance;
      }

      // Get contract balance (should have remainder)
      const contractBalance = await token.balanceOf(await token.getAddress());

      // Total should equal initial supply
      const totalSupply = await token.totalSupply();
      expect(totalTraderBalance + contractBalance).to.equal(totalSupply);
    });
  });

  describe("Edge Cases & Stress Tests", function () {
    it("Should handle graduation with minimal excess", async function () {
      // Buy almost to threshold (need to account for 2% fees)
      // 49 ETH * 0.98 = 48.02 ETH in reserves
      await token.connect(traders[0]).buy(0, { value: ethers.parseEther("49") });
      expect(await token.isGraduated()).to.be.false;

      // Push just over threshold (need 50 ETH in reserves, have 48.02, need 1.98 more)
      // 2.1 ETH * 0.98 = 2.058 ETH in reserves, total = 50.078 > 50
      await token.connect(traders[1]).buy(0, { value: ethers.parseEther("2.1") });
      expect(await token.isGraduated()).to.be.true;
    });

    it("Should handle immediate graduation in single buy", async function () {
      const massiveBuy = ethers.parseEther("100");

      await expect(token.connect(traders[0]).buy(0, { value: massiveBuy }))
        .to.emit(token, "GraduationTriggered");

      expect(await token.isGraduated()).to.be.true;
    });

    it("Should handle zero balance transfers", async function () {
      await token.connect(traders[0]).buy(0, { value: ethers.parseEther("1") });

      // Trader 1 has zero balance
      await token.connect(traders[1]).transfer(traders[2].address, 0);
      expect(await token.balanceOf(traders[2].address)).to.equal(0);
    });

    it("Should handle self-transfers", async function () {
      await token.connect(traders[0]).buy(0, { value: ethers.parseEther("1") });
      const balance = await token.balanceOf(traders[0].address);

      await token.connect(traders[0]).transfer(traders[0].address, balance);
      expect(await token.balanceOf(traders[0].address)).to.equal(balance);
    });

    it("Should handle very small sells", async function () {
      await token.connect(traders[0]).buy(0, { value: ethers.parseEther("10") });

      // MIN_TOKEN_AMOUNT is 1000 * 1e18, so use slightly above that
      const tinyAmount = ethers.parseUnits("1001", 18);
      await token.connect(traders[0]).sell(tinyAmount, 0);

      // Should succeed without reverting
      expect(await token.balanceOf(traders[0].address)).to.be.gt(0);
    });

    it("Should handle max uint256 approval", async function () {
      await token.connect(traders[0]).buy(0, { value: ethers.parseEther("10") });

      const maxApproval = ethers.MaxUint256;
      await token.connect(traders[0]).approve(traders[1].address, maxApproval);

      expect(await token.allowance(traders[0].address, traders[1].address)).to.equal(maxApproval);
    });
  });

  describe("Gas Optimization", function () {
    it("Should maintain reasonable gas costs for buys", async function () {
      const tx = await token.connect(traders[0]).buy(0, { value: ethers.parseEther("1") });
      const receipt = await tx.wait();

      console.log(`      Gas used for buy: ${receipt.gasUsed.toString()}`);
      expect(receipt.gasUsed).to.be.lt(200000n); // Should be under 200k gas
    });

    it("Should maintain reasonable gas costs for sells", async function () {
      await token.connect(traders[0]).buy(0, { value: ethers.parseEther("10") });
      const balance = await token.balanceOf(traders[0].address);

      const tx = await token.connect(traders[0]).sell(balance / 2n, 0);
      const receipt = await tx.wait();

      console.log(`      Gas used for sell: ${receipt.gasUsed.toString()}`);
      expect(receipt.gasUsed).to.be.lt(150000n); // Should be under 150k gas
    });

    it("Should have consistent gas costs across multiple operations", async function () {
      const gasUsages = [];

      for (let i = 0; i < 5; i++) {
        const tx = await token.connect(traders[i]).buy(0, { value: ethers.parseEther("1") });
        const receipt = await tx.wait();
        gasUsages.push(receipt.gasUsed);
      }

      // Gas should remain relatively constant (first call may be higher due to cold storage)
      const avgGas = gasUsages.reduce((a, b) => a + b, 0n) / BigInt(gasUsages.length);

      for (const gas of gasUsages) {
        const difference = gas > avgGas ? gas - avgGas : avgGas - gas;
        // Allow 50% variance to account for cold vs warm storage
        expect(difference).to.be.lt(avgGas / 2n);
      }
    });
  });
});
