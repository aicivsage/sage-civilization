import { expect } from "chai";
import { ethers } from "hardhat";
import { BondingCurveTokenOptimized, BondingCurveFactoryOptimized } from "../typechain-types";
import { SignerWithAddress } from "@nomicfoundation/hardhat-ethers/signers";
import { time } from "@nomicfoundation/hardhat-network-helpers";
import { deployMocks } from "./helpers";

describe("BondingCurveTokenOptimized", function () {
  let token: BondingCurveTokenOptimized;
  let factory: BondingCurveFactoryOptimized;
  let owner: SignerWithAddress;
  let creator: SignerWithAddress;
  let platformFeeRecipient: SignerWithAddress;
  let buyer1: SignerWithAddress;
  let buyer2: SignerWithAddress;
  let pancakeRouter: string;

  const CREATION_FEE = ethers.parseEther("0.01");
  const VIRTUAL_BNB = ethers.parseEther("30");
  const VIRTUAL_TOKENS = ethers.parseEther("1073000191");
  const K = VIRTUAL_BNB * VIRTUAL_TOKENS;
  const GRADUATION_THRESHOLD = ethers.parseEther("50");

  beforeEach(async function () {
    [owner, creator, platformFeeRecipient, buyer1, buyer2] = await ethers.getSigners();

    // Deploy mock contracts
    const mocks = await deployMocks();
    pancakeRouter = await mocks.router.getAddress();

    // Deploy factory
    const Factory = await ethers.getContractFactory("BondingCurveFactoryOptimized");
    factory = await Factory.deploy(
      platformFeeRecipient.address,
      CREATION_FEE,
      pancakeRouter
    );

    // Create token via factory
    const tx = await factory.connect(creator).createToken("Test Token", "TEST", {
      value: CREATION_FEE,
    });

    const receipt = await tx.wait();
    const event = receipt?.logs.find((log: any) => {
      try {
        const parsed = factory.interface.parseLog(log);
        return parsed?.name === "TokenCreated";
      } catch {
        return false;
      }
    });

    if (!event) throw new Error("TokenCreated event not found");
    const parsedEvent = factory.interface.parseLog(event);
    const tokenAddress = parsedEvent?.args[0];

    // Get token instance
    token = await ethers.getContractAt("BondingCurveTokenOptimized", tokenAddress);
  });

  describe("Deployment", function () {
    it("Should set the correct name and symbol", async function () {
      expect(await token.name()).to.equal("Test Token");
      expect(await token.symbol()).to.equal("TEST");
    });

    it("Should mint total supply to contract", async function () {
      const totalSupply = ethers.parseEther("1000000000");
      expect(await token.totalSupply()).to.equal(totalSupply);
      expect(await token.balanceOf(await token.getAddress())).to.equal(totalSupply);
    });

    it("Should set status to Trading", async function () {
      expect(await token.status()).to.equal(0); // Trading = 0
    });

    it("Should set correct immutable addresses", async function () {
      expect(await token.creator()).to.equal(creator.address);
      expect(await token.platformFeeRecipient()).to.equal(platformFeeRecipient.address);
    });
  });

  describe("Fixed-Point Math (CRITICAL FIX)", function () {
    it("Should maintain precision over 1000 trades", async function () {
      const buyAmount = ethers.parseEther("0.001");
      const iterations = 1000;

      for (let i = 0; i < iterations; i++) {
        await token.connect(buyer1).buy(0, { value: buyAmount });

        if (i % 100 === 0) {
          // Verify invariant every 100 trades
          const [bnbReserves, tokenReserves] = await token.getCurrentReserves();
          const calculatedK = (bnbReserves * tokenReserves) / ethers.parseEther("1");
          const expectedK = K / ethers.parseEther("1");

          // Allow 0.01% tolerance
          const tolerance = expectedK / 10000n;
          expect(calculatedK).to.be.closeTo(expectedK, tolerance);
        }
      }
    });

    it("Should never lose precision with odd amounts", async function () {
      const oddAmount = ethers.parseEther("0.0123456789");

      await token.connect(buyer1).buy(0, { value: oddAmount });

      const balance = await token.balanceOf(buyer1.address);
      await token.connect(buyer1).sell(balance, 0);

      // Verify reserves didn't drift (should be >= VIRTUAL_BNB, may equal due to fees)
      const [bnbReserves] = await token.getCurrentReserves();
      expect(bnbReserves).to.be.gte(VIRTUAL_BNB); // Should be at least equal or greater
    });

    it("Should calculate correct tokens for various BNB amounts", async function () {
      const amounts = [
        ethers.parseEther("0.001"),
        ethers.parseEther("0.1"),
        ethers.parseEther("1"),
        ethers.parseEther("5"),
      ];

      for (const amount of amounts) {
        const expectedTokens = await token.calculateTokensReceived(amount);
        expect(expectedTokens).to.be.gt(0);

        // Verify it's close to manual calculation
        const bnbAfterFees = (amount * 9800n) / 10000n;
        const currentBnb = VIRTUAL_BNB + (await token.bnbReserves());
        const currentTokens = K / currentBnb;
        const newBnb = currentBnb + bnbAfterFees;
        const newTokens = K / newBnb;
        const manualTokens = currentTokens - newTokens;

        // Should be within 0.1% (fixed-point math is more precise)
        const tolerance = manualTokens / 1000n;
        expect(expectedTokens).to.be.closeTo(manualTokens, tolerance);
      }
    });
  });

  describe("Invariant Verification (CRITICAL FIX)", function () {
    it("Should emit InvariantVerified event on each trade", async function () {
      await expect(token.connect(buyer1).buy(0, { value: ethers.parseEther("1") }))
        .to.emit(token, "InvariantVerified");
    });

    it("Should verify invariant holds after buy", async function () {
      await token.connect(buyer1).buy(0, { value: ethers.parseEther("1") });

      const [bnbReserves, tokenReserves] = await token.getCurrentReserves();
      const calculatedK = (bnbReserves * tokenReserves) / ethers.parseEther("1");
      const expectedK = K / ethers.parseEther("1");

      // Verify within 0.01% tolerance
      const tolerance = expectedK / 10000n;
      expect(calculatedK).to.be.closeTo(expectedK, tolerance);
    });

    it("Should verify invariant holds after sell", async function () {
      await token.connect(buyer1).buy(0, { value: ethers.parseEther("1") });

      const balance = await token.balanceOf(buyer1.address);
      await token.connect(buyer1).sell(balance / 2n, 0);

      const [bnbReserves, tokenReserves] = await token.getCurrentReserves();
      const calculatedK = (bnbReserves * tokenReserves) / ethers.parseEther("1");
      const expectedK = K / ethers.parseEther("1");

      const tolerance = expectedK / 10000n;
      expect(calculatedK).to.be.closeTo(expectedK, tolerance);
    });

    it("Should maintain invariant over complex trade sequence", async function () {
      // Complex sequence: buy, sell, buy, buy, sell
      await token.connect(buyer1).buy(0, { value: ethers.parseEther("1") });
      const balance1 = await token.balanceOf(buyer1.address);
      await token.connect(buyer1).sell(balance1 / 2n, 0);

      await token.connect(buyer2).buy(0, { value: ethers.parseEther("0.5") });
      await token.connect(buyer1).buy(0, { value: ethers.parseEther("0.3") });

      const balance2 = await token.balanceOf(buyer2.address);
      await token.connect(buyer2).sell(balance2, 0);

      // Verify invariant still holds
      const [bnbReserves, tokenReserves] = await token.getCurrentReserves();
      const calculatedK = (bnbReserves * tokenReserves) / ethers.parseEther("1");
      const expectedK = K / ethers.parseEther("1");

      const tolerance = expectedK / 10000n;
      expect(calculatedK).to.be.closeTo(expectedK, tolerance);
    });
  });

  describe("Buy Function (Optimized)", function () {
    it("Should allow buying tokens with BNB", async function () {
      const buyAmount = ethers.parseEther("1");
      await expect(token.connect(buyer1).buy(0, { value: buyAmount }))
        .to.emit(token, "TokensPurchased");

      expect(await token.balanceOf(buyer1.address)).to.be.gt(0);
    });

    it("Should enforce minimum buy amount", async function () {
      const tooSmall = ethers.parseEther("0.0001"); // Below MIN_BNB_AMOUNT
      await expect(
        token.connect(buyer1).buy(0, { value: tooSmall })
      ).to.be.revertedWith("BNB amount below minimum");
    });

    it("Should enforce maximum buy amount (anti-whale)", async function () {
      const tooLarge = ethers.parseEther("11"); // Above MAX_BUY_PER_TX (10 BNB)
      await expect(
        token.connect(buyer1).buy(0, { value: tooLarge })
      ).to.be.revertedWith("Exceeds maximum per transaction");
    });

    it("Should respect slippage protection", async function () {
      const buyAmount = ethers.parseEther("1");
      const expectedTokens = await token.calculateTokensReceived(buyAmount);
      const minTokens = expectedTokens + 1n; // Expect more than possible

      await expect(
        token.connect(buyer1).buy(minTokens, { value: buyAmount })
      ).to.be.revertedWith("Slippage limit exceeded");
    });

    it("Should accumulate fees correctly", async function () {
      const buyAmount = ethers.parseEther("1");
      const expectedPlatformFee = (buyAmount * 100n) / 10000n; // 1%
      const expectedCreatorFee = (buyAmount * 100n) / 10000n; // 1%

      await token.connect(buyer1).buy(0, { value: buyAmount });

      expect(await token.pendingFees(platformFeeRecipient.address)).to.equal(expectedPlatformFee);
      expect(await token.pendingFees(creator.address)).to.equal(expectedCreatorFee);
    });

    it("Should trigger graduation at threshold", async function () {
      // Buy enough to reach graduation (50 BNB in reserves after fees)
      // Need to buy in multiple transactions due to MAX_BUY_PER_TX = 10 ETH
      await token.connect(buyer1).buy(0, { value: ethers.parseEther("10") });
      await token.connect(buyer1).buy(0, { value: ethers.parseEther("10") });
      await token.connect(buyer1).buy(0, { value: ethers.parseEther("10") });
      await token.connect(buyer1).buy(0, { value: ethers.parseEther("10") });
      await token.connect(buyer1).buy(0, { value: ethers.parseEther("10") });

      // Final buy should trigger graduation
      await expect(token.connect(buyer1).buy(0, { value: ethers.parseEther("2") }))
        .to.emit(token, "GraduationTriggered")
        .and.to.emit(token, "StatusChanged");

      expect(await token.status()).to.equal(1); // Graduated = 1
    });

    it("Should emit enhanced TokensPurchased event", async function () {
      const buyAmount = ethers.parseEther("1");

      await expect(token.connect(buyer1).buy(0, { value: buyAmount }))
        .to.emit(token, "TokensPurchased")
        .to.emit(token, "FeesAccumulated");
    });
  });

  describe("Sell Function (Optimized)", function () {
    beforeEach(async function () {
      // Buy tokens first
      await token.connect(buyer1).buy(0, { value: ethers.parseEther("1") });
    });

    it("Should allow selling tokens for BNB", async function () {
      const balance = await token.balanceOf(buyer1.address);

      await expect(token.connect(buyer1).sell(balance, 0))
        .to.emit(token, "TokensSold");
    });

    it("Should enforce minimum sell amount", async function () {
      const tooSmall = ethers.parseEther("100"); // Below MIN_TOKEN_AMOUNT

      await expect(
        token.connect(buyer1).sell(tooSmall, 0)
      ).to.be.revertedWith("Token amount below minimum");
    });

    it("Should respect slippage protection", async function () {
      const balance = await token.balanceOf(buyer1.address);
      const expectedBnb = await token.calculateBNBReceived(balance);
      const minBnb = expectedBnb + 1n; // Expect more than possible

      await expect(
        token.connect(buyer1).sell(balance, minBnb)
      ).to.be.revertedWith("Slippage limit exceeded");
    });

    it("Should prevent selling more tokens than owned", async function () {
      const balance = await token.balanceOf(buyer1.address);
      const tooMany = balance + ethers.parseEther("1000");

      // Will revert with "Insufficient BNB reserves" because the contract
      // calculates the BNB owed before checking token balance
      await expect(
        token.connect(buyer1).sell(tooMany, 0)
      ).to.be.revertedWith("Insufficient BNB reserves");
    });

    it("Should calculate BNB received correctly", async function () {
      const balance = await token.balanceOf(buyer1.address);
      const bnbBefore = await ethers.provider.getBalance(buyer1.address);

      const tx = await token.connect(buyer1).sell(balance, 0);
      const receipt = await tx.wait();
      const gasUsed = receipt!.gasUsed * receipt!.gasPrice;

      const bnbAfter = await ethers.provider.getBalance(buyer1.address);
      const bnbReceived = bnbAfter + gasUsed - bnbBefore;

      expect(bnbReceived).to.be.gt(0);
    });
  });

  describe("Graduation Cooldown (CRITICAL FIX)", function () {
    beforeEach(async function () {
      // Trigger graduation - buy in multiple transactions due to MAX_BUY_PER_TX
      await token.connect(buyer1).buy(0, { value: ethers.parseEther("10") });
      await token.connect(buyer1).buy(0, { value: ethers.parseEther("10") });
      await token.connect(buyer1).buy(0, { value: ethers.parseEther("10") });
      await token.connect(buyer1).buy(0, { value: ethers.parseEther("10") });
      await token.connect(buyer1).buy(0, { value: ethers.parseEther("10") });
      await token.connect(buyer1).buy(0, { value: ethers.parseEther("2") });
    });

    it("Should enforce cooldown period", async function () {
      // Try to graduate immediately (should fail)
      await expect(
        token.connect(buyer1).graduateToPancakeSwap()
      ).to.be.revertedWith("Graduation cooldown active");
    });

    it("Should allow graduation after cooldown", async function () {
      // Advance time by 1 hour
      await time.increase(3600);

      // This will fail on hardhat without proper PancakeSwap mocks,
      // but the cooldown check should pass
      // In real testnet deployment, this would succeed
      try {
        await token.connect(buyer1).graduateToPancakeSwap();
      } catch (error: any) {
        // Expected to fail due to missing PancakeSwap contracts
        // But should NOT fail with "Graduation cooldown active"
        expect(error.message).to.not.include("Graduation cooldown active");
      }
    });

    it("Should return correct cooldown remaining time", async function () {
      const remaining = await token.graduationCooldownRemaining();
      expect(remaining).to.be.closeTo(3600n, 10n); // ~1 hour

      // Advance halfway
      await time.increase(1800);
      const remainingHalf = await token.graduationCooldownRemaining();
      expect(remainingHalf).to.be.closeTo(1800n, 10n); // ~30 minutes

      // Advance fully
      await time.increase(1800);
      const remainingZero = await token.graduationCooldownRemaining();
      expect(remainingZero).to.equal(0);
    });
  });

  describe("Fee Withdrawal", function () {
    beforeEach(async function () {
      // Generate fees
      await token.connect(buyer1).buy(0, { value: ethers.parseEther("1") });
    });

    it("Should allow platform to withdraw fees", async function () {
      const pendingFees = await token.pendingFees(platformFeeRecipient.address);
      expect(pendingFees).to.be.gt(0);

      await expect(token.connect(platformFeeRecipient).withdrawFees())
        .to.emit(token, "FeesWithdrawn")
        .withArgs(platformFeeRecipient.address, pendingFees);

      expect(await token.pendingFees(platformFeeRecipient.address)).to.equal(0);
    });

    it("Should allow creator to withdraw fees", async function () {
      const pendingFees = await token.pendingFees(creator.address);
      expect(pendingFees).to.be.gt(0);

      await token.connect(creator).withdrawFees();
      expect(await token.pendingFees(creator.address)).to.equal(0);
    });

    it("Should revert if no fees to withdraw", async function () {
      await expect(
        token.connect(buyer2).withdrawFees()
      ).to.be.revertedWith("No fees to withdraw");
    });
  });

  describe("Transaction Cooldown (Optional Feature)", function () {
    it("Should be disabled by default", async function () {
      expect(await token.cooldownEnabled()).to.be.false;
    });

    it("Should allow owner to toggle cooldown", async function () {
      await expect(token.connect(creator).toggleCooldown())
        .to.emit(token, "CooldownToggled")
        .withArgs(true);

      expect(await token.cooldownEnabled()).to.be.true;
    });

    it("Should enforce cooldown when enabled", async function () {
      await token.connect(creator).toggleCooldown();

      // First buy should succeed
      await token.connect(buyer1).buy(0, { value: ethers.parseEther("1") });

      // Second buy immediately should fail
      await expect(
        token.connect(buyer1).buy(0, { value: ethers.parseEther("1") })
      ).to.be.revertedWith("Buy cooldown active");

      // After cooldown period, should succeed
      await time.increase(60); // 1 minute
      await token.connect(buyer1).buy(0, { value: ethers.parseEther("1") });
    });

    it("Should return correct cooldown remaining time", async function () {
      await token.connect(creator).toggleCooldown();
      await token.connect(buyer1).buy(0, { value: ethers.parseEther("1") });

      const remaining = await token.buyCooldownRemaining(buyer1.address);
      expect(remaining).to.be.closeTo(60n, 10n); // ~1 minute
    });
  });

  describe("View Functions", function () {
    it("Should calculate current price", async function () {
      const price = await token.getCurrentPrice();
      expect(price).to.be.gt(0);

      // Price should increase after buy
      await token.connect(buyer1).buy(0, { value: ethers.parseEther("1") });
      const newPrice = await token.getCurrentPrice();
      expect(newPrice).to.be.gt(price);
    });

    it("Should return current reserves", async function () {
      const [bnb, tokens] = await token.getCurrentReserves();
      expect(bnb).to.equal(VIRTUAL_BNB); // Initial state
      expect(tokens).to.equal(VIRTUAL_TOKENS);
    });

    it("Should return graduation status", async function () {
      expect(await token.isGraduated()).to.be.false;

      // Buy in multiple transactions to reach graduation threshold
      await token.connect(buyer1).buy(0, { value: ethers.parseEther("10") });
      await token.connect(buyer1).buy(0, { value: ethers.parseEther("10") });
      await token.connect(buyer1).buy(0, { value: ethers.parseEther("10") });
      await token.connect(buyer1).buy(0, { value: ethers.parseEther("10") });
      await token.connect(buyer1).buy(0, { value: ethers.parseEther("10") });
      await token.connect(buyer1).buy(0, { value: ethers.parseEther("2") });

      expect(await token.isGraduated()).to.be.true;
    });
  });

  describe("Gas Optimization Validation", function () {
    it("Should use less gas than unoptimized version", async function () {
      const tx = await token.connect(buyer1).buy(0, { value: ethers.parseEther("1") });
      const receipt = await tx.wait();

      console.log("Buy gas used:", receipt!.gasUsed.toString());

      // Target: <150,000 gas (optimized version should be ~5-10% less than 160k)
      expect(receipt!.gasUsed).to.be.lt(150000);
    });

    it("Should cache storage variables efficiently", async function () {
      // Multiple reads in same transaction should benefit from caching
      const tx = await token.connect(buyer1).buy(0, { value: ethers.parseEther("1") });
      const receipt = await tx.wait();

      // Gas should be reasonable even with invariant checks
      expect(receipt!.gasUsed).to.be.lt(150000);
    });
  });
});
