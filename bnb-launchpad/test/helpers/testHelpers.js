const { ethers } = require("hardhat");

/**
 * Test Helper Utilities for BNB Token Launchpad
 * Provides common functions for testing bonding curve mechanics
 */

/**
 * Deploy all necessary mock contracts for testing
 * @returns {Object} Deployed contract instances
 */
async function deployMocks() {
  // Deploy mock WETH
  const MockWETH = await ethers.getContractFactory("MockWETH");
  const weth = await MockWETH.deploy();
  await weth.waitForDeployment();

  // Deploy mock PancakeFactory
  const MockPancakeFactory = await ethers.getContractFactory("MockPancakeFactory");
  const factory = await MockPancakeFactory.deploy();
  await factory.waitForDeployment();

  // Deploy mock PancakeRouter
  const MockPancakeRouter = await ethers.getContractFactory("MockPancakeRouter");
  const router = await MockPancakeRouter.deploy(
    await weth.getAddress(),
    await factory.getAddress()
  );
  await router.waitForDeployment();

  return { weth, factory, router };
}

/**
 * Deploy TokenLaunchFactory
 * @param {string} platformFeeRecipient - Address to receive platform fees
 * @param {string} pancakeRouter - PancakeSwap router address
 * @returns {Object} Deployed factory contract
 */
async function deployFactory(platformFeeRecipient, pancakeRouter) {
  const TokenLaunchFactory = await ethers.getContractFactory("TokenLaunchFactory");
  const factory = await TokenLaunchFactory.deploy(platformFeeRecipient, pancakeRouter);
  await factory.waitForDeployment();
  return factory;
}

/**
 * Create a new token through the factory
 * @param {Object} factory - TokenLaunchFactory instance
 * @param {Object} creator - Signer who creates the token
 * @param {string} name - Token name
 * @param {string} symbol - Token symbol
 * @returns {Object} Deployed token contract instance
 */
async function createToken(factory, creator, name = "Test Token", symbol = "TEST") {
  const tx = await factory.connect(creator).createToken(name, symbol);
  const receipt = await tx.wait();

  // Extract token address from event
  const event = receipt.logs.find(log => {
    try {
      return factory.interface.parseLog(log).name === "TokenCreated";
    } catch {
      return false;
    }
  });

  const parsedEvent = factory.interface.parseLog(event);
  const tokenAddress = parsedEvent.args.tokenAddress;

  // Get token contract instance
  const BondingCurveToken = await ethers.getContractFactory("BondingCurveToken");
  const token = BondingCurveToken.attach(tokenAddress);

  return token;
}

/**
 * Calculate expected tokens from BNB input (before fees)
 * Uses bonding curve formula: Δy = y₀ - (k / (x₀ + Δx))
 * @param {BigInt} bnbAmount - Amount of BNB to spend
 * @param {BigInt} currentBnbReserves - Current BNB reserves
 * @param {BigInt} virtualBnb - Virtual BNB reserves
 * @param {BigInt} virtualTokens - Virtual token reserves
 * @returns {BigInt} Expected tokens received
 */
function calculateExpectedTokens(bnbAmount, currentBnbReserves, virtualBnb, virtualTokens) {
  const k = virtualBnb * virtualTokens;
  const currentTotalBnb = currentBnbReserves + virtualBnb;
  const currentTokenReserves = k / currentTotalBnb;
  const newTotalBnb = currentTotalBnb + bnbAmount;
  const newTokenReserves = k / newTotalBnb;
  return currentTokenReserves - newTokenReserves;
}

/**
 * Calculate expected BNB from token input (before fees)
 * Uses bonding curve formula: Δx = x₀ - (k / (y₀ + Δy))
 * @param {BigInt} tokenAmount - Amount of tokens to sell
 * @param {BigInt} currentBnbReserves - Current BNB reserves
 * @param {BigInt} virtualBnb - Virtual BNB reserves
 * @param {BigInt} virtualTokens - Virtual token reserves
 * @returns {BigInt} Expected BNB received
 */
function calculateExpectedBNB(tokenAmount, currentBnbReserves, virtualBnb, virtualTokens) {
  const k = virtualBnb * virtualTokens;
  const currentTotalBnb = currentBnbReserves + virtualBnb;
  const currentTokenReserves = k / currentTotalBnb;
  const newTokenReserves = currentTokenReserves + tokenAmount;
  const newTotalBnb = k / newTokenReserves;
  return currentTotalBnb - newTotalBnb;
}

/**
 * Apply fee calculation to an amount
 * @param {BigInt} amount - Base amount
 * @param {number} feeBps - Fee in basis points (100 = 1%)
 * @returns {BigInt} Fee amount
 */
function calculateFee(amount, feeBps) {
  return (amount * BigInt(feeBps)) / BigInt(10000);
}

/**
 * Get token and BNB balances for an address
 * @param {Object} token - Token contract instance
 * @param {string} address - Address to check
 * @returns {Object} Balances object
 */
async function getBalances(token, address) {
  const tokenBalance = await token.balanceOf(address);
  const bnbBalance = await ethers.provider.getBalance(address);
  return { tokenBalance, bnbBalance };
}

/**
 * Get current reserves from token contract
 * @param {Object} token - Token contract instance
 * @returns {Object} Reserves object with bnbReserves and tokenReserves
 */
async function getReserves(token) {
  const [bnbReserves, tokenReserves] = await token.getCurrentReserves();
  return { bnbReserves, tokenReserves };
}

/**
 * Execute buy and return all relevant data
 * @param {Object} token - Token contract instance
 * @param {Object} buyer - Signer executing buy
 * @param {BigInt} bnbAmount - Amount of BNB to spend
 * @param {BigInt} minTokensOut - Minimum tokens expected (slippage protection)
 * @returns {Object} Transaction receipt and balances
 */
async function executeBuy(token, buyer, bnbAmount, minTokensOut = 0n) {
  const balancesBefore = await getBalances(token, buyer.address);
  const reservesBefore = await getReserves(token);

  const tx = await token.connect(buyer).buy(minTokensOut, { value: bnbAmount });
  const receipt = await tx.wait();

  const balancesAfter = await getBalances(token, buyer.address);
  const reservesAfter = await getReserves(token);

  return {
    receipt,
    balancesBefore,
    balancesAfter,
    reservesBefore,
    reservesAfter,
    tokensReceived: balancesAfter.tokenBalance - balancesBefore.tokenBalance
  };
}

/**
 * Execute sell and return all relevant data
 * @param {Object} token - Token contract instance
 * @param {Object} seller - Signer executing sell
 * @param {BigInt} tokenAmount - Amount of tokens to sell
 * @param {BigInt} minBnbOut - Minimum BNB expected (slippage protection)
 * @returns {Object} Transaction receipt and balances
 */
async function executeSell(token, seller, tokenAmount, minBnbOut = 0n) {
  const balancesBefore = await getBalances(token, seller.address);
  const reservesBefore = await getReserves(token);

  const tx = await token.connect(seller).sell(tokenAmount, minBnbOut);
  const receipt = await tx.wait();

  const balancesAfter = await getBalances(token, seller.address);
  const reservesAfter = await getReserves(token);

  return {
    receipt,
    balancesBefore,
    balancesAfter,
    reservesBefore,
    reservesAfter,
    bnbReceived: balancesAfter.bnbBalance - balancesBefore.bnbBalance
  };
}

/**
 * Mine blocks to advance time
 * @param {number} blocks - Number of blocks to mine
 */
async function mineBlocks(blocks) {
  for (let i = 0; i < blocks; i++) {
    await ethers.provider.send("evm_mine", []);
  }
}

/**
 * Increase EVM time
 * @param {number} seconds - Seconds to increase
 */
async function increaseTime(seconds) {
  await ethers.provider.send("evm_increaseTime", [seconds]);
  await ethers.provider.send("evm_mine", []);
}

/**
 * Get latest block timestamp
 * @returns {number} Current block timestamp
 */
async function getCurrentTimestamp() {
  const block = await ethers.provider.getBlock("latest");
  return block.timestamp;
}

/**
 * Constants from contracts
 */
const CONSTANTS = {
  VIRTUAL_BNB_RESERVES: ethers.parseEther("30"),
  VIRTUAL_TOKEN_RESERVES: ethers.parseUnits("1073000191", 18),
  TOTAL_TOKEN_SUPPLY: ethers.parseUnits("1000000000", 18),
  PLATFORM_FEE_BPS: 100n, // 1%
  CREATOR_FEE_BPS: 100n,  // 1%
  TOTAL_FEE_BPS: 200n,    // 2%
  GRADUATION_THRESHOLD: ethers.parseEther("50"),
  LIQUIDITY_PERCENT_BPS: 7500n, // 75%
  BURN_ADDRESS: "0x000000000000000000000000000000000000dEaD"
};

module.exports = {
  deployMocks,
  deployFactory,
  createToken,
  calculateExpectedTokens,
  calculateExpectedBNB,
  calculateFee,
  getBalances,
  getReserves,
  executeBuy,
  executeSell,
  mineBlocks,
  increaseTime,
  getCurrentTimestamp,
  CONSTANTS
};
