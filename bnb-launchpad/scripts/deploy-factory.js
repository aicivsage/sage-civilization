// Deploy TokenLaunchFactory to BSC testnet/mainnet

const hre = require("hardhat");
const {
  saveDeployment,
  loadDeployment,
  formatBNB,
  waitForTx,
  getExplorerUrl,
  printDeploymentSummary,
  verifyBalance
} = require("./utils/helpers");

// Network configurations
const NETWORK_CONFIG = {
  bscTestnet: {
    pancakeRouter: "0xD99D1c33F9fC3444f8101754aBC46c52416550D1",
    wbnb: "0xae13d989daC2f0dEbFf460aC112a837C89BAa7cd",
    chainId: 97,
    minBalance: "0.1" // Minimum BNB required for deployment
  },
  bscMainnet: {
    pancakeRouter: "0x10ED43C718714eb63d5aA57B78B54704E256024E",
    wbnb: "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
    chainId: 56,
    minBalance: "0.5" // Higher minimum for mainnet
  }
};

async function main() {
  const networkName = hre.network.name;
  console.log("\n" + "=".repeat(60));
  console.log("DEPLOYING TOKENLAUNCHFACTORY");
  console.log("=".repeat(60));
  console.log(`Network: ${networkName}`);
  console.log(`Chain ID: ${(await hre.ethers.provider.getNetwork()).chainId}`);
  console.log("-".repeat(60));

  // Get deployer
  const [deployer] = await hre.ethers.getSigners();
  console.log(`Deployer: ${deployer.address}`);

  // Verify balance
  const config = NETWORK_CONFIG[networkName] || NETWORK_CONFIG.bscTestnet;
  await verifyBalance(deployer, config.minBalance, hre.ethers);

  // Get configuration
  const platformFeeRecipient = process.env.PLATFORM_FEE_RECIPIENT || deployer.address;
  const pancakeRouter = config.pancakeRouter;

  console.log("Deployment Configuration:");
  console.log(`  Platform Fee Recipient: ${platformFeeRecipient}`);
  console.log(`  PancakeSwap Router: ${pancakeRouter}`);
  console.log(`  WBNB Address: ${config.wbnb}`);
  console.log("-".repeat(60));

  // Deploy Factory
  console.log("\n📦 Deploying TokenLaunchFactory...");
  const TokenLaunchFactory = await hre.ethers.getContractFactory("TokenLaunchFactory");

  console.log("   Sending deployment transaction...");
  const factory = await TokenLaunchFactory.deploy(platformFeeRecipient, pancakeRouter);

  console.log("   Waiting for deployment confirmation...");
  await factory.waitForDeployment();

  const factoryAddress = await factory.getAddress();

  console.log(`\n✅ TokenLaunchFactory deployed!`);
  console.log(`   Address: ${factoryAddress}`);
  console.log(`   Explorer: ${getExplorerUrl(networkName, 'address', factoryAddress)}`);

  // Verify deployment by calling view functions
  console.log("\n🔍 Verifying deployment...");
  try {
    const feeRecipient = await factory.platformFeeRecipient();
    const router = await factory.pancakeRouter();
    const tokenCount = await factory.getTokenCount();

    console.log("   Platform Fee Recipient:", feeRecipient);
    console.log("   PancakeSwap Router:", router);
    console.log("   Token Count:", tokenCount.toString());

    if (feeRecipient.toLowerCase() !== platformFeeRecipient.toLowerCase()) {
      throw new Error("Fee recipient mismatch!");
    }
    if (router.toLowerCase() !== pancakeRouter.toLowerCase()) {
      throw new Error("Router address mismatch!");
    }

    console.log("\n✅ Deployment verification passed!");
  } catch (error) {
    console.error("\n❌ Deployment verification failed!");
    throw error;
  }

  // Save deployment
  const networkKey = networkName === 'bscMainnet' ? 'mainnet' : 'testnet';
  saveDeployment(
    networkKey,
    'factory',
    factoryAddress,
    {
      deployer: deployer.address,
      platformFeeRecipient,
      pancakeRouter,
      wbnb: config.wbnb,
      chainId: config.chainId
    }
  );

  // Print summary
  const deployments = loadDeployment(networkKey);
  printDeploymentSummary(deployments, networkKey);

  // Print next steps
  console.log("NEXT STEPS:");
  console.log("-".repeat(60));
  console.log("1. Verify contract on BscScan:");
  console.log(`   npx hardhat verify --network ${networkName} ${factoryAddress} "${platformFeeRecipient}" "${pancakeRouter}"`);
  console.log("\n2. Create a test token:");
  console.log(`   npx hardhat run scripts/create-test-token.js --network ${networkName}`);
  console.log("\n3. Test buying tokens:");
  console.log(`   npx hardhat run scripts/test-buy.js --network ${networkName}`);
  console.log("=".repeat(60) + "\n");

  return factoryAddress;
}

// Execute deployment
if (require.main === module) {
  main()
    .then(() => process.exit(0))
    .catch((error) => {
      console.error("\n❌ DEPLOYMENT FAILED\n");
      console.error(error);
      process.exit(1);
    });
}

module.exports = main;
