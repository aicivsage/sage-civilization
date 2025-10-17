const hre = require("hardhat");

async function main() {
  console.log("Deploying BondingCurveFactoryOptimized to local network...");

  // Get deployer account
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying with account:", deployer.address);
  console.log("Account balance:", (await hre.ethers.provider.getBalance(deployer.address)).toString());

  // Deploy Factory with constructor parameters
  // platformFeeRecipient, creationFee, pancakeRouter
  const BondingCurveFactoryOptimized = await hre.ethers.getContractFactory("BondingCurveFactoryOptimized");
  const factory = await BondingCurveFactoryOptimized.deploy(
    deployer.address, // platformFeeRecipient
    hre.ethers.parseEther("0"), // creationFee (0 for testing)
    "0x9Ac64Cc6e4415144C455BD8E4837Fea55603e5c3" // PancakeSwap Router (BSC Testnet address, won't be used in local testing)
  );
  await factory.waitForDeployment();

  const factoryAddress = await factory.getAddress();
  console.log("\n✅ BondingCurveFactoryOptimized deployed to:", factoryAddress);

  // Create a test token
  console.log("\nCreating test token...");
  const tx = await factory.createToken("Test Token", "TEST");
  const receipt = await tx.wait();

  // Get the token address from the event
  const event = receipt.logs.find(log => {
    try {
      return factory.interface.parseLog(log).name === "TokenCreated";
    } catch {
      return false;
    }
  });

  const tokenAddress = event ? factory.interface.parseLog(event).args[0] : null;
  console.log("✅ Test token created at:", tokenAddress);

  console.log("\n📋 Configuration for .env:");
  console.log(`FACTORY_ADDRESS=${factoryAddress}`);
  console.log(`TEST_TOKEN_ADDRESS=${tokenAddress}`);
  console.log(`RPC_URL=http://localhost:8545`);
  console.log(`CHAIN_ID=31337`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
