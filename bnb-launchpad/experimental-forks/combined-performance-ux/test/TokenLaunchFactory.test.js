const { expect } = require("chai");
const { ethers } = require("hardhat");
const { deployMocks, deployFactory, CONSTANTS } = require("./helpers/testHelpers");

/**
 * What we're verifying: Factory pattern enables secure, isolated token deployments
 * What coder discovered: Factory creates independent contracts, not shared state
 * What descendants inherit: Safe multi-token architecture patterns
 * Why this matters: Prevents cross-contamination exploits between tokens
 */

describe("TokenLaunchFactory", function () {
  let factory;
  let router;
  let owner;
  let platformFeeRecipient;
  let creator1;
  let creator2;
  let user1;

  beforeEach(async function () {
    // Get signers
    [owner, platformFeeRecipient, creator1, creator2, user1] = await ethers.getSigners();

    // Deploy mocks
    const mocks = await deployMocks();
    router = mocks.router;

    // Deploy factory
    factory = await deployFactory(platformFeeRecipient.address, await router.getAddress());
  });

  describe("Deployment", function () {
    it("Should set the correct platform fee recipient", async function () {
      expect(await factory.platformFeeRecipient()).to.equal(platformFeeRecipient.address);
    });

    it("Should set the correct owner", async function () {
      expect(await factory.owner()).to.equal(owner.address);
    });

    it("Should initialize with zero tokens", async function () {
      expect(await factory.getTokenCount()).to.equal(0);
    });

    it("Should have empty allTokens array", async function () {
      const tokens = await factory.getAllTokens();
      expect(tokens.length).to.equal(0);
    });
  });

  describe("Token Creation", function () {
    it("Should successfully create a token", async function () {
      const tx = await factory.connect(creator1).createToken("My Token", "MTK");
      const receipt = await tx.wait();

      // Verify TokenCreated event
      const event = receipt.logs.find(log => {
        try {
          return factory.interface.parseLog(log).name === "TokenCreated";
        } catch {
          return false;
        }
      });

      expect(event).to.not.be.undefined;

      const parsedEvent = factory.interface.parseLog(event);
      expect(parsedEvent.args.creator).to.equal(creator1.address);
      expect(parsedEvent.args.name).to.equal("My Token");
      expect(parsedEvent.args.symbol).to.equal("MTK");
    });

    it("Should increment token count after creation", async function () {
      await factory.connect(creator1).createToken("Token1", "TK1");
      expect(await factory.getTokenCount()).to.equal(1);

      await factory.connect(creator1).createToken("Token2", "TK2");
      expect(await factory.getTokenCount()).to.equal(2);

      await factory.connect(creator2).createToken("Token3", "TK3");
      expect(await factory.getTokenCount()).to.equal(3);
    });

    it("Should add token to allTokens array", async function () {
      const tx = await factory.connect(creator1).createToken("Test", "TST");
      const receipt = await tx.wait();

      const event = receipt.logs.find(log => {
        try {
          return factory.interface.parseLog(log).name === "TokenCreated";
        } catch {
          return false;
        }
      });

      const tokenAddress = factory.interface.parseLog(event).args.tokenAddress;

      const allTokens = await factory.getAllTokens();
      expect(allTokens.length).to.equal(1);
      expect(allTokens[0]).to.equal(tokenAddress);
    });

    it("Should create token with correct parameters", async function () {
      const tx = await factory.connect(creator1).createToken("My Token", "MTK");
      const receipt = await tx.wait();

      const event = receipt.logs.find(log => {
        try {
          return factory.interface.parseLog(log).name === "TokenCreated";
        } catch {
          return false;
        }
      });

      const tokenAddress = factory.interface.parseLog(event).args.tokenAddress;

      // Get token instance
      const BondingCurveToken = await ethers.getContractFactory("BondingCurveToken");
      const token = BondingCurveToken.attach(tokenAddress);

      // Verify token properties
      expect(await token.name()).to.equal("My Token");
      expect(await token.symbol()).to.equal("MTK");
      expect(await token.creator()).to.equal(creator1.address);
      expect(await token.platformFeeRecipient()).to.equal(platformFeeRecipient.address);
      expect(await token.totalSupply()).to.equal(CONSTANTS.TOTAL_TOKEN_SUPPLY);
    });

    it("Should create isolated tokens with independent state", async function () {
      // Create two tokens
      const tx1 = await factory.connect(creator1).createToken("Token1", "TK1");
      const receipt1 = await tx1.wait();
      const event1 = receipt1.logs.find(log => {
        try {
          return factory.interface.parseLog(log).name === "TokenCreated";
        } catch {
          return false;
        }
      });
      const token1Address = factory.interface.parseLog(event1).args.tokenAddress;

      const tx2 = await factory.connect(creator2).createToken("Token2", "TK2");
      const receipt2 = await tx2.wait();
      const event2 = receipt2.logs.find(log => {
        try {
          return factory.interface.parseLog(log).name === "TokenCreated";
        } catch {
          return false;
        }
      });
      const token2Address = factory.interface.parseLog(event2).args.tokenAddress;

      // Verify different addresses
      expect(token1Address).to.not.equal(token2Address);

      // Get token instances
      const BondingCurveToken = await ethers.getContractFactory("BondingCurveToken");
      const token1 = BondingCurveToken.attach(token1Address);
      const token2 = BondingCurveToken.attach(token2Address);

      // Verify independent creators
      expect(await token1.creator()).to.equal(creator1.address);
      expect(await token2.creator()).to.equal(creator2.address);

      // Buy from token1 - should not affect token2
      await token1.connect(user1).buy(0, { value: ethers.parseEther("1") });

      const [bnb1] = await token1.getCurrentReserves();
      const [bnb2] = await token2.getCurrentReserves();

      // bnb1 should have increased (virtual + actual)
      expect(bnb1).to.be.gt(CONSTANTS.VIRTUAL_BNB_RESERVES);
      // bnb2 should still only have virtual reserves
      expect(bnb2).to.equal(CONSTANTS.VIRTUAL_BNB_RESERVES);
    });

    it("Should allow multiple tokens from same creator", async function () {
      await factory.connect(creator1).createToken("Token1", "TK1");
      await factory.connect(creator1).createToken("Token2", "TK2");
      await factory.connect(creator1).createToken("Token3", "TK3");

      expect(await factory.getTokenCount()).to.equal(3);

      const allTokens = await factory.getAllTokens();
      expect(allTokens.length).to.equal(3);

      // Verify all have same creator
      const BondingCurveToken = await ethers.getContractFactory("BondingCurveToken");
      for (const tokenAddress of allTokens) {
        const token = BondingCurveToken.attach(tokenAddress);
        expect(await token.creator()).to.equal(creator1.address);
      }
    });

    it("Should allow permissionless token creation", async function () {
      // Anyone can create tokens without permission
      await factory.connect(user1).createToken("User Token", "UTK");
      expect(await factory.getTokenCount()).to.equal(1);
    });
  });

  describe("Token Tracking", function () {
    beforeEach(async function () {
      // Create some tokens
      await factory.connect(creator1).createToken("Token1", "TK1");
      await factory.connect(creator2).createToken("Token2", "TK2");
      await factory.connect(creator1).createToken("Token3", "TK3");
    });

    it("Should return correct token count", async function () {
      expect(await factory.getTokenCount()).to.equal(3);
    });

    it("Should return all token addresses", async function () {
      const allTokens = await factory.getAllTokens();
      expect(allTokens.length).to.equal(3);

      // Verify all addresses are valid contracts
      for (const tokenAddress of allTokens) {
        const code = await ethers.provider.getCode(tokenAddress);
        expect(code).to.not.equal("0x");
      }
    });

    it("Should maintain correct order in allTokens array", async function () {
      const tokens = [];
      const startIndex = await factory.getTokenCount(); // Get current count (3 from beforeEach)

      for (let i = 0; i < 3; i++) {
        const tx = await factory.connect(creator1).createToken(`TokenNew${i}`, `TKN${i}`);
        const receipt = await tx.wait();
        const event = receipt.logs.find(log => {
          try {
            return factory.interface.parseLog(log).name === "TokenCreated";
          } catch {
            return false;
          }
        });
        tokens.push(factory.interface.parseLog(event).args.tokenAddress);
      }

      const allTokens = await factory.getAllTokens();
      // Check that newly created tokens are in the correct positions
      for (let i = 0; i < tokens.length; i++) {
        expect(allTokens[Number(startIndex) + i]).to.equal(tokens[i]);
      }
    });

    it("Should allow accessing tokens by index", async function () {
      const tokenAddress = await factory.allTokens(0);
      expect(tokenAddress).to.be.properAddress;

      const code = await ethers.provider.getCode(tokenAddress);
      expect(code).to.not.equal("0x");
    });
  });

  describe("Access Control", function () {
    it("Should allow owner to transfer ownership", async function () {
      await factory.connect(owner).transferOwnership(creator1.address);
      expect(await factory.owner()).to.equal(creator1.address);
    });

    it("Should prevent non-owner from transferring ownership", async function () {
      await expect(
        factory.connect(creator1).transferOwnership(creator2.address)
      ).to.be.revertedWithCustomError(factory, "OwnableUnauthorizedAccount");
    });

    it("Should allow owner to renounce ownership", async function () {
      await factory.connect(owner).renounceOwnership();
      expect(await factory.owner()).to.equal(ethers.ZeroAddress);
    });
  });

  describe("Edge Cases", function () {
    it("Should handle empty string names and symbols", async function () {
      const tx = await factory.connect(creator1).createToken("", "");
      const receipt = await tx.wait();

      const event = receipt.logs.find(log => {
        try {
          return factory.interface.parseLog(log).name === "TokenCreated";
        } catch {
          return false;
        }
      });

      expect(event).to.not.be.undefined;

      const tokenAddress = factory.interface.parseLog(event).args.tokenAddress;
      const BondingCurveToken = await ethers.getContractFactory("BondingCurveToken");
      const token = BondingCurveToken.attach(tokenAddress);

      expect(await token.name()).to.equal("");
      expect(await token.symbol()).to.equal("");
    });

    it("Should handle very long names and symbols", async function () {
      const longName = "A".repeat(100);
      const longSymbol = "B".repeat(50);

      const tx = await factory.connect(creator1).createToken(longName, longSymbol);
      const receipt = await tx.wait();

      const event = receipt.logs.find(log => {
        try {
          return factory.interface.parseLog(log).name === "TokenCreated";
        } catch {
          return false;
        }
      });

      const tokenAddress = factory.interface.parseLog(event).args.tokenAddress;
      const BondingCurveToken = await ethers.getContractFactory("BondingCurveToken");
      const token = BondingCurveToken.attach(tokenAddress);

      expect(await token.name()).to.equal(longName);
      expect(await token.symbol()).to.equal(longSymbol);
    });

    it("Should handle special characters in names", async function () {
      const specialName = "Token™ 🚀 测试";
      const tx = await factory.connect(creator1).createToken(specialName, "SPEC");
      const receipt = await tx.wait();

      const event = receipt.logs.find(log => {
        try {
          return factory.interface.parseLog(log).name === "TokenCreated";
        } catch {
          return false;
        }
      });

      const tokenAddress = factory.interface.parseLog(event).args.tokenAddress;
      const BondingCurveToken = await ethers.getContractFactory("BondingCurveToken");
      const token = BondingCurveToken.attach(tokenAddress);

      expect(await token.name()).to.equal(specialName);
    });

    it("Should handle rapid consecutive creations", async function () {
      const promises = [];
      for (let i = 0; i < 10; i++) {
        promises.push(factory.connect(creator1).createToken(`Token${i}`, `TK${i}`));
      }

      await Promise.all(promises);
      expect(await factory.getTokenCount()).to.equal(10);
    });
  });

  describe("Gas Optimization", function () {
    it("Should be gas efficient for token creation", async function () {
      const tx = await factory.connect(creator1).createToken("Gas Test", "GAS");
      const receipt = await tx.wait();

      // Log gas used for monitoring (not a strict requirement)
      console.log(`      Gas used for token creation: ${receipt.gasUsed.toString()}`);

      // Ensure it's within reasonable bounds (<5M gas)
      expect(receipt.gasUsed).to.be.lt(5000000n);
    });

    it("Should scale efficiently with multiple tokens", async function () {
      const gasUsages = [];

      for (let i = 0; i < 5; i++) {
        const tx = await factory.connect(creator1).createToken(`Token${i}`, `TK${i}`);
        const receipt = await tx.wait();
        gasUsages.push(receipt.gasUsed);
      }

      // Gas should remain relatively constant (not grow significantly)
      const firstGas = gasUsages[0];
      const lastGas = gasUsages[gasUsages.length - 1];
      const difference = lastGas > firstGas ? lastGas - firstGas : firstGas - lastGas;

      // Allow <10% variance
      expect(difference).to.be.lt(firstGas / 10n);
    });
  });
});
