import { ethers } from "hardhat";

async function main() {
  console.log("\n=================================================");
  console.log("DEPLOYING PERFORMANCE OPTIMIZED LAUNCHPAD");
  console.log("=================================================\n");

  const [deployer] = await ethers.getSigners();

  console.log("Deploying with account:", deployer.address);
  console.log("Account balance:", ethers.formatEther(await ethers.provider.getBalance(deployer.address)), "BNB");

  // Configuration
  const CREATION_FEE = ethers.parseEther("0.01"); // 0.01 BNB to create token
  const PLATFORM_FEE_RECIPIENT = deployer.address; // Change to platform treasury
  const PANCAKE_ROUTER = "0xD99D1c33F9fC3444f8101754aBC46c52416550D1"; // BSC Testnet PancakeSwap Router

  console.log("\nConfiguration:");
  console.log("- Creation Fee:", ethers.formatEther(CREATION_FEE), "BNB");
  console.log("- Platform Fee Recipient:", PLATFORM_FEE_RECIPIENT);
  console.log("- PancakeSwap Router:", PANCAKE_ROUTER);

  // Deploy Factory
  console.log("\nDeploying BondingCurveFactoryOptimized...");
  const Factory = await ethers.getContractFactory("BondingCurveFactoryOptimized");
  const factory = await Factory.deploy(
    PLATFORM_FEE_RECIPIENT,
    CREATION_FEE,
    PANCAKE_ROUTER
  );

  await factory.waitForDeployment();
  const factoryAddress = await factory.getAddress();

  console.log("✅ Factory deployed to:", factoryAddress);

  // Deploy test token
  console.log("\nDeploying test token...");
  const tx = await factory.createToken("Test Optimized Token", "TESTO", {
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

  if (!event) {
    throw new Error("TokenCreated event not found");
  }

  const parsedEvent = factory.interface.parseLog(event);
  const tokenAddress = parsedEvent?.args[0];

  console.log("✅ Test token deployed to:", tokenAddress);

  // Get token instance
  const token = await ethers.getContractAt("BondingCurveTokenOptimized", tokenAddress);

  console.log("\n=================================================");
  console.log("DEPLOYMENT SUMMARY");
  console.log("=================================================");
  console.log("\nFactory Address:", factoryAddress);
  console.log("Test Token Address:", tokenAddress);
  console.log("\nToken Details:");
  console.log("- Name:", await token.name());
  console.log("- Symbol:", await token.symbol());
  console.log("- Total Supply:", ethers.formatEther(await token.totalSupply()));
  console.log("- Status:", (await token.status()) === 0 ? "Trading" : "Graduated");
  console.log("- Creator:", await token.creator());

  console.log("\n=================================================");
  console.log("NEXT STEPS");
  console.log("=================================================");
  console.log("\n1. Verify contracts on BscScan:");
  console.log("   npx hardhat verify --network bscTestnet", factoryAddress, PLATFORM_FEE_RECIPIENT, ethers.formatEther(CREATION_FEE), PANCAKE_ROUTER);
  console.log("\n2. Test buying tokens:");
  console.log("   - Token Address:", tokenAddress);
  console.log("   - Minimum Buy: 0.001 BNB");
  console.log("   - Maximum Buy: 10 BNB");
  console.log("\n3. Monitor events and gas usage");
  console.log("\n4. Run comprehensive test suite:");
  console.log("   npm run test");
  console.log("   npm run test:gas");
  console.log("\n=================================================\n");

  // Save deployment info
  const deploymentInfo = {
    network: "bscTestnet",
    timestamp: new Date().toISOString(),
    deployer: deployer.address,
    factory: factoryAddress,
    testToken: tokenAddress,
    config: {
      creationFee: ethers.formatEther(CREATION_FEE),
      platformFeeRecipient: PLATFORM_FEE_RECIPIENT,
      pancakeRouter: PANCAKE_ROUTER,
    },
  };

  console.log("Deployment Info:");
  console.log(JSON.stringify(deploymentInfo, null, 2));

  return deploymentInfo;
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
