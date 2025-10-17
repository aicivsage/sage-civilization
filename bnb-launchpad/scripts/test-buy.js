// Test buying tokens from the bonding curve

const hre = require("hardhat");
const {
  loadDeployment,
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
  console.log("TEST TOKEN PURCHASE");
  console.log("=".repeat(60));
  console.log(`Network: ${networkName}`);
  console.log("-".repeat(60));

  // Get buyer
  const [buyer] = await hre.ethers.getSigners();
  console.log(`Buyer: ${buyer.address}`);

  // Verify balance
  await verifyBalance(buyer, "0.05", hre.ethers);

  // Load deployments
  const networkKey = networkName === 'bscMainnet' ? 'mainnet' : 'testnet';
  const deployments = loadDeployment(networkKey);

  if (!deployments.testToken) {
    throw new Error("Test token not found! Run create-test-token.js first.");
  }

  console.log(`Token Address: ${deployments.testToken}`);
  console.log("-".repeat(60));

  // Get token contract
  const token = await getContract("BondingCurveToken", deployments.testToken, hre.ethers);

  // Get token info
  const name = await token.name();
  const symbol = await token.symbol();
  console.log(`\nToken: ${name} (${symbol})`);

  // Get buy amount from environment or use default
  const buyAmountBNB = process.env.BUY_AMOUNT || "0.01";
  const buyAmount = parseBNB(buyAmountBNB, hre.ethers);

  console.log(`\nBuy Amount: ${buyAmountBNB} BNB`);

  // Get state before buy
  console.log("\n📊 State BEFORE purchase:");
  const bnbReserveBefore = await token.bnbReserve();
  const tokenReserveBefore = await token.tokenReserve();
  const buyerBalanceBefore = await token.balanceOf(buyer.address);
  const buyerBNBBefore = await hre.ethers.provider.getBalance(buyer.address);

  console.log(`   BNB Reserve: ${formatBNB(bnbReserveBefore, hre.ethers)} BNB`);
  console.log(`   Token Reserve: ${formatBNB(tokenReserveBefore, hre.ethers)} tokens`);
  console.log(`   Buyer Token Balance: ${formatBNB(buyerBalanceBefore, hre.ethers)} tokens`);
  console.log(`   Buyer BNB Balance: ${formatBNB(buyerBNBBefore, hre.ethers)} BNB`);

  // Calculate expected tokens
  console.log("\n💰 Calculating expected tokens...");
  try {
    const expectedTokens = await token.calculateBuyAmount(buyAmount);
    console.log(`   Expected tokens: ${formatBNB(expectedTokens, hre.ethers)}`);
  } catch (error) {
    console.log(`   ⚠️  Cannot calculate: ${error.message}`);
  }

  // Execute buy
  console.log("\n🛒 Executing purchase...");
  const tx = await token.buy(0, { value: buyAmount }); // minTokensOut = 0 for testing
  const receipt = await waitForTx(tx, "Token purchase");

  // Parse events
  console.log("\n📋 Transaction Events:");
  for (const log of receipt.logs) {
    try {
      const parsed = token.interface.parseLog({
        topics: [...log.topics],
        data: log.data
      });

      if (parsed) {
        console.log(`   Event: ${parsed.name}`);
        if (parsed.name === 'TokenPurchased') {
          console.log(`     Buyer: ${parsed.args.buyer}`);
          console.log(`     BNB Amount: ${formatBNB(parsed.args.bnbAmount, hre.ethers)} BNB`);
          console.log(`     Token Amount: ${formatBNB(parsed.args.tokenAmount, hre.ethers)} tokens`);
          console.log(`     Fee: ${formatBNB(parsed.args.platformFee, hre.ethers)} BNB`);
        } else if (parsed.name === 'Transfer') {
          console.log(`     From: ${parsed.args.from}`);
          console.log(`     To: ${parsed.args.to}`);
          console.log(`     Amount: ${formatBNB(parsed.args.value, hre.ethers)} tokens`);
        }
      }
    } catch (e) {
      // Not a token event
      continue;
    }
  }

  // Get state after buy
  console.log("\n📊 State AFTER purchase:");
  const bnbReserveAfter = await token.bnbReserve();
  const tokenReserveAfter = await token.tokenReserve();
  const buyerBalanceAfter = await token.balanceOf(buyer.address);
  const buyerBNBAfter = await hre.ethers.provider.getBalance(buyer.address);

  console.log(`   BNB Reserve: ${formatBNB(bnbReserveAfter, hre.ethers)} BNB`);
  console.log(`   Token Reserve: ${formatBNB(tokenReserveAfter, hre.ethers)} tokens`);
  console.log(`   Buyer Token Balance: ${formatBNB(buyerBalanceAfter, hre.ethers)} tokens`);
  console.log(`   Buyer BNB Balance: ${formatBNB(buyerBNBAfter, hre.ethers)} BNB`);

  // Calculate changes
  console.log("\n📈 Changes:");
  const bnbReserveChange = bnbReserveAfter - bnbReserveBefore;
  const tokenReserveChange = tokenReserveBefore - tokenReserveAfter; // Negative means decrease
  const buyerBalanceChange = buyerBalanceAfter - buyerBalanceBefore;
  const buyerBNBChange = buyerBNBBefore - buyerBNBAfter; // Negative means spent

  console.log(`   BNB Reserve: +${formatBNB(bnbReserveChange, hre.ethers)} BNB`);
  console.log(`   Token Reserve: -${formatBNB(tokenReserveChange, hre.ethers)} tokens`);
  console.log(`   Buyer Tokens: +${formatBNB(buyerBalanceChange, hre.ethers)} tokens`);
  console.log(`   Buyer BNB Spent: ${formatBNB(buyerBNBChange, hre.ethers)} BNB (includes gas)`);

  // Calculate effective price
  const effectivePrice = Number(buyAmountBNB) / parseFloat(formatBNB(buyerBalanceChange, hre.ethers));
  console.log(`   Effective Price: ${effectivePrice.toFixed(10)} BNB per token`);

  // Check graduation progress
  const graduationThreshold = await hre.ethers.getContractFactory("TokenLaunchFactory")
    .then(f => f.attach(deployments.factory))
    .then(f => f.GRADUATION_THRESHOLD());
  const progressPercent = (Number(bnbReserveAfter) / Number(graduationThreshold) * 100).toFixed(2);

  console.log(`\n🎓 Graduation Progress:`);
  console.log(`   Current: ${formatBNB(bnbReserveAfter, hre.ethers)} BNB`);
  console.log(`   Target: ${formatBNB(graduationThreshold, hre.ethers)} BNB`);
  console.log(`   Progress: ${progressPercent}%`);

  console.log("\n✅ Purchase test complete!");
  console.log(`   View transaction: ${getExplorerUrl(networkName, 'tx', receipt.hash)}`);

  // Print next steps
  console.log("\n" + "=".repeat(60));
  console.log("NEXT STEPS:");
  console.log("-".repeat(60));
  console.log("1. Test selling tokens:");
  console.log(`   npx hardhat run scripts/test-sell.js --network ${networkName}`);
  console.log("\n2. Continue buying to reach graduation:");
  console.log(`   BUY_AMOUNT=0.1 npx hardhat run scripts/test-buy.js --network ${networkName}`);
  console.log("\n3. Test graduation when threshold reached:");
  console.log(`   npx hardhat run scripts/test-graduation.js --network ${networkName}`);
  console.log("=".repeat(60) + "\n");

  return receipt;
}

// Execute script
if (require.main === module) {
  main()
    .then(() => process.exit(0))
    .catch((error) => {
      console.error("\n❌ BUY TEST FAILED\n");
      console.error(error);
      process.exit(1);
    });
}

module.exports = main;
