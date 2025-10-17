// Create a test token through the TokenLaunchFactory

const hre = require("hardhat");
const {
  loadDeployment,
  saveDeployment,
  getContract,
  waitForTx,
  getExplorerUrl,
  parseBNB,
  formatBNB,
  verifyBalance
} = require("./utils/helpers");

async function main() {
  const networkName = hre.network.name;
  console.log("\n" + "=".repeat(60));
  console.log("CREATING TEST TOKEN");
  console.log("=".repeat(60));
  console.log(`Network: ${networkName}`);
  console.log("-".repeat(60));

  // Get deployer
  const [deployer] = await hre.ethers.getSigners();
  console.log(`Account: ${deployer.address}`);

  // Verify balance
  await verifyBalance(deployer, "0.05", hre.ethers);

  // Load factory deployment
  const networkKey = networkName === 'bscMainnet' ? 'mainnet' : 'testnet';
  const deployments = loadDeployment(networkKey);

  if (!deployments.factory) {
    throw new Error("Factory not deployed! Run deploy-factory.js first.");
  }

  console.log(`Factory Address: ${deployments.factory}`);
  console.log("-".repeat(60));

  // Get factory contract
  const factory = await getContract("TokenLaunchFactory", deployments.factory, hre.ethers);

  // Token parameters
  const tokenName = process.env.TOKEN_NAME || "Test Meme Token";
  const tokenSymbol = process.env.TOKEN_SYMBOL || "TESTMEME";

  console.log("\nToken Configuration:");
  console.log(`  Name: ${tokenName}`);
  console.log(`  Symbol: ${tokenSymbol}`);
  console.log("-".repeat(60));

  // Create token (no creation fee in current version)
  console.log("\n📦 Creating token...");
  const tx = await factory.createToken(
    tokenName,
    tokenSymbol
  );

  const receipt = await waitForTx(tx, "Token creation");

  // Find TokenCreated event
  console.log("\n🔍 Extracting token address from event...");
  let tokenAddress = null;

  for (const log of receipt.logs) {
    try {
      const parsed = factory.interface.parseLog({
        topics: [...log.topics],
        data: log.data
      });

      if (parsed && parsed.name === 'TokenCreated') {
        tokenAddress = parsed.args.tokenAddress;
        const creator = parsed.args.creator;
        const name = parsed.args.name;
        const symbol = parsed.args.symbol;

        console.log(`   Event: TokenCreated`);
        console.log(`   Token: ${tokenAddress}`);
        console.log(`   Creator: ${creator}`);
        console.log(`   Name: ${name}`);
        console.log(`   Symbol: ${symbol}`);
        break;
      }
    } catch (e) {
      // Not the event we're looking for
      continue;
    }
  }

  if (!tokenAddress) {
    throw new Error("Could not find TokenCreated event in transaction receipt");
  }

  console.log(`\n✅ Token created successfully!`);
  console.log(`   Address: ${tokenAddress}`);
  console.log(`   Explorer: ${getExplorerUrl(networkName, 'token', tokenAddress)}`);

  // Get token contract and verify
  console.log("\n🔍 Verifying token deployment...");
  const token = await getContract("BondingCurveToken", tokenAddress, hre.ethers);

  const name = await token.name();
  const symbol = await token.symbol();
  const totalSupply = await token.totalSupply();
  const factory_addr = await token.factory();
  const isGraduated = await token.isGraduated();

  console.log("   Token Details:");
  console.log(`     Name: ${name}`);
  console.log(`     Symbol: ${symbol}`);
  console.log(`     Total Supply: ${formatBNB(totalSupply, hre.ethers)}`);
  console.log(`     Factory: ${factory_addr}`);
  console.log(`     Is Graduated: ${isGraduated}`);

  // Save token address
  saveDeployment(
    networkKey,
    'testToken',
    tokenAddress,
    {
      testTokenName: name,
      testTokenSymbol: symbol,
      testTokenCreator: deployer.address,
      testTokenCreatedAt: new Date().toISOString()
    }
  );

  console.log("\n✅ Token deployment saved!");

  // Print next steps
  console.log("\n" + "=".repeat(60));
  console.log("NEXT STEPS:");
  console.log("-".repeat(60));
  console.log("1. Verify token contract on BscScan:");
  console.log(`   npx hardhat run scripts/verify-contracts.js --network ${networkName}`);
  console.log("\n2. Test buying tokens:");
  console.log(`   npx hardhat run scripts/test-buy.js --network ${networkName}`);
  console.log("\n3. Test selling tokens:");
  console.log(`   npx hardhat run scripts/test-sell.js --network ${networkName}`);
  console.log("\n4. Test graduation flow:");
  console.log(`   npx hardhat run scripts/test-graduation.js --network ${networkName}`);
  console.log("=".repeat(60) + "\n");

  return tokenAddress;
}

// Execute script
if (require.main === module) {
  main()
    .then(() => process.exit(0))
    .catch((error) => {
      console.error("\n❌ TOKEN CREATION FAILED\n");
      console.error(error);
      process.exit(1);
    });
}

module.exports = main;
