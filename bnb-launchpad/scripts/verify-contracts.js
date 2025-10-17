// Verify deployed contracts on BscScan

const hre = require("hardhat");
const {
  loadDeployment,
  getExplorerUrl,
  sleep
} = require("./utils/helpers");

async function verifyContract(address, constructorArgs, contractName) {
  console.log(`\n🔍 Verifying ${contractName}...`);
  console.log(`   Address: ${address}`);
  console.log(`   Constructor args: ${JSON.stringify(constructorArgs)}`);

  try {
    await hre.run("verify:verify", {
      address: address,
      constructorArguments: constructorArgs,
    });
    console.log(`✅ ${contractName} verified successfully!`);
    return true;
  } catch (error) {
    if (error.message.includes("Already Verified")) {
      console.log(`✅ ${contractName} already verified!`);
      return true;
    } else {
      console.error(`❌ Verification failed: ${error.message}`);
      return false;
    }
  }
}

async function main() {
  const networkName = hre.network.name;
  console.log("\n" + "=".repeat(60));
  console.log("VERIFY CONTRACTS ON BSCSCAN");
  console.log("=".repeat(60));
  console.log(`Network: ${networkName}`);
  console.log("-".repeat(60));

  // Check API key
  if (!process.env.BSCSCAN_API_KEY) {
    throw new Error("BSCSCAN_API_KEY not set in .env file");
  }

  console.log("✅ BscScan API key found");

  // Load deployments
  const networkKey = networkName === 'bscMainnet' ? 'mainnet' : 'testnet';
  const deployments = loadDeployment(networkKey);

  if (!deployments.factory) {
    throw new Error("No deployments found! Run deploy-factory.js first.");
  }

  console.log("\nDeployed contracts:");
  console.log(`  Factory: ${deployments.factory}`);
  if (deployments.testToken) {
    console.log(`  Test Token: ${deployments.testToken}`);
  }
  console.log("-".repeat(60));

  const results = {
    factory: false,
    testToken: false
  };

  // Verify Factory
  console.log("\n📝 VERIFYING TOKENLAUNCHFACTORY");
  console.log("-".repeat(60));

  const platformFeeRecipient = deployments.platformFeeRecipient;
  const pancakeRouter = deployments.pancakeRouter;

  if (!platformFeeRecipient || !pancakeRouter) {
    console.error("❌ Missing constructor args for factory!");
    console.log("   platformFeeRecipient:", platformFeeRecipient);
    console.log("   pancakeRouter:", pancakeRouter);
    throw new Error("Cannot verify factory without constructor args");
  }

  results.factory = await verifyContract(
    deployments.factory,
    [platformFeeRecipient, pancakeRouter],
    "TokenLaunchFactory"
  );

  console.log(`   View on BscScan: ${getExplorerUrl(networkKey, 'address', deployments.factory)}`);

  // Wait between verifications to avoid rate limiting
  if (deployments.testToken) {
    console.log("\n⏳ Waiting 5 seconds before next verification...");
    await sleep(5000);

    // Verify Test Token
    console.log("\n📝 VERIFYING BONDING CURVE TOKEN");
    console.log("-".repeat(60));

    // Token constructor args: name, symbol, description, image, twitter, telegram, website, factory, creator
    // These are stored in the factory's createToken call, we need to get them from the contract

    try {
      const token = await hre.ethers.getContractAt("BondingCurveToken", deployments.testToken);

      const name = await token.name();
      const symbol = await token.symbol();
      const description = await token.description();
      const image = await token.image();
      const twitter = await token.twitter();
      const telegram = await token.telegram();
      const website = await token.website();
      const factory = await token.factory();
      const creator = deployments.testTokenCreator || deployments.deployer;

      console.log("   Token info retrieved:");
      console.log(`     Name: ${name}`);
      console.log(`     Symbol: ${symbol}`);
      console.log(`     Factory: ${factory}`);
      console.log(`     Creator: ${creator}`);

      results.testToken = await verifyContract(
        deployments.testToken,
        [name, symbol, description, image, twitter, telegram, website, factory, creator],
        "BondingCurveToken"
      );

      console.log(`   View on BscScan: ${getExplorerUrl(networkKey, 'token', deployments.testToken)}`);
    } catch (error) {
      console.error(`❌ Failed to verify test token: ${error.message}`);
    }
  }

  // Print summary
  console.log("\n" + "=".repeat(60));
  console.log("VERIFICATION SUMMARY");
  console.log("=".repeat(60));
  console.log(`Factory: ${results.factory ? '✅ Verified' : '❌ Failed'}`);
  if (deployments.testToken) {
    console.log(`Test Token: ${results.testToken ? '✅ Verified' : '❌ Failed'}`);
  }
  console.log("=".repeat(60));

  // Print URLs
  console.log("\nVIEW ON BSCSCAN:");
  console.log("-".repeat(60));
  console.log(`Factory: ${getExplorerUrl(networkKey, 'address', deployments.factory)}`);
  if (deployments.testToken) {
    console.log(`Test Token: ${getExplorerUrl(networkKey, 'token', deployments.testToken)}`);
  }
  console.log("=".repeat(60) + "\n");

  const allSuccess = results.factory && (!deployments.testToken || results.testToken);

  if (!allSuccess) {
    console.log("⚠️  Some verifications failed. You can try manual verification:");
    console.log("\nManual verification commands:");
    console.log(`npx hardhat verify --network ${networkName} ${deployments.factory} "${platformFeeRecipient}" "${pancakeRouter}"`);
    if (deployments.testToken) {
      console.log(`\n# For token, you'll need to pass all constructor args manually`);
    }
  } else {
    console.log("✅ All contracts verified successfully!");
  }

  return results;
}

// Execute script
if (require.main === module) {
  main()
    .then(() => process.exit(0))
    .catch((error) => {
      console.error("\n❌ VERIFICATION FAILED\n");
      console.error(error);
      process.exit(1);
    });
}

module.exports = main;
