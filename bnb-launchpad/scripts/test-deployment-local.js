// Test deployment scripts on local hardhat network
// This uses mock contracts instead of real PancakeSwap

const hre = require("hardhat");

async function deployMocks() {
  console.log("📦 Deploying mock contracts...");

  // Deploy MockWETH
  const MockWETH = await hre.ethers.getContractFactory("contracts/mocks/MockPancakeRouter.sol:MockWETH");
  const weth = await MockWETH.deploy();
  await weth.waitForDeployment();
  const wethAddress = await weth.getAddress();
  console.log(`   Mock WETH: ${wethAddress}`);

  // Deploy MockFactory
  const MockFactory = await hre.ethers.getContractFactory("contracts/mocks/MockPancakeRouter.sol:MockPancakeFactory");
  const factory = await MockFactory.deploy();
  await factory.waitForDeployment();
  const factoryAddress = await factory.getAddress();
  console.log(`   Mock Factory: ${factoryAddress}`);

  // Deploy MockRouter
  const MockRouter = await hre.ethers.getContractFactory("contracts/mocks/MockPancakeRouter.sol:MockPancakeRouter");
  const router = await MockRouter.deploy(wethAddress, factoryAddress);
  await router.waitForDeployment();
  const routerAddress = await router.getAddress();
  console.log(`   Mock Router: ${routerAddress}`);

  return { router: routerAddress, weth: wethAddress, factory: factoryAddress };
}

async function main() {
  console.log("\n" + "=".repeat(60));
  console.log("LOCAL DEPLOYMENT TEST");
  console.log("=".repeat(60));
  console.log("Testing deployment scripts on local hardhat network\n");

  const [deployer] = await hre.ethers.getSigners();
  console.log("Deployer:", deployer.address);
  console.log("Balance:", hre.ethers.formatEther(await hre.ethers.provider.getBalance(deployer.address)), "ETH");
  console.log("-".repeat(60));

  try {
    // Deploy mocks
    const mocks = await deployMocks();

    // Deploy factory
    console.log("\n📦 Deploying TokenLaunchFactory...");
    const TokenLaunchFactory = await hre.ethers.getContractFactory("TokenLaunchFactory");
    const factory = await TokenLaunchFactory.deploy(deployer.address, mocks.router);
    await factory.waitForDeployment();

    const factoryAddress = await factory.getAddress();
    console.log(`   Factory: ${factoryAddress}`);

    // Verify factory
    console.log("\n🔍 Verifying factory...");
    const feeRecipient = await factory.platformFeeRecipient();
    const router = await factory.pancakeRouter();
    console.log(`   Platform Fee Recipient: ${feeRecipient}`);
    console.log(`   Router: ${router}`);

    // Create token
    console.log("\n📦 Creating test token...");
    const tx = await factory.createToken(
      "Test Token",
      "TEST"
    );

    const receipt = await tx.wait();
    console.log(`   Transaction confirmed!`);

    // Find TokenCreated event
    let tokenAddress = null;
    for (const log of receipt.logs) {
      try {
        const parsed = factory.interface.parseLog({
          topics: [...log.topics],
          data: log.data
        });
        if (parsed && parsed.name === 'TokenCreated') {
          tokenAddress = parsed.args.tokenAddress;
          break;
        }
      } catch (e) {
        continue;
      }
    }

    console.log(`   Token Address: ${tokenAddress}`);

    // Get token contract
    const token = await hre.ethers.getContractAt("BondingCurveToken", tokenAddress);
    const name = await token.name();
    const symbol = await token.symbol();
    console.log(`   Token: ${name} (${symbol})`);

    // Test buy
    console.log("\n💰 Testing buy...");
    const buyAmount = hre.ethers.parseEther("0.01");
    const buyTx = await token.buy(0, { value: buyAmount }); // minTokensOut = 0 for testing
    await buyTx.wait();

    const balance = await token.balanceOf(deployer.address);
    console.log(`   Tokens received: ${hre.ethers.formatEther(balance)}`);

    // Test sell
    console.log("\n💸 Testing sell...");
    const sellAmount = balance / 2n; // Sell half
    const approveTx = await token.approve(tokenAddress, sellAmount);
    await approveTx.wait();

    const sellTx = await token.sell(sellAmount, 0); // minBnbOut = 0 for testing
    await sellTx.wait();

    const balanceAfter = await token.balanceOf(deployer.address);
    console.log(`   Remaining tokens: ${hre.ethers.formatEther(balanceAfter)}`);

    console.log("\n" + "=".repeat(60));
    console.log("✅ ALL LOCAL TESTS PASSED!");
    console.log("=".repeat(60));
    console.log("\nDeployment scripts are working correctly.");
    console.log("Ready to deploy to BSC Testnet.\n");

  } catch (error) {
    console.error("\n❌ LOCAL TEST FAILED\n");
    console.error(error);
    throw error;
  }
}

if (require.main === module) {
  main()
    .then(() => process.exit(0))
    .catch((error) => {
      process.exit(1);
    });
}

module.exports = main;
