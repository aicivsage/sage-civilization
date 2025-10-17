// Test selling tokens back to the bonding curve

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
  console.log("TEST TOKEN SALE");
  console.log("=".repeat(60));
  console.log(`Network: ${networkName}`);
  console.log("-".repeat(60));

  // Get seller
  const [seller] = await hre.ethers.getSigners();
  console.log(`Seller: ${seller.address}`);

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

  // Check seller's token balance
  const sellerBalance = await token.balanceOf(seller.address);
  console.log(`\nSeller Token Balance: ${formatBNB(sellerBalance, hre.ethers)} tokens`);

  if (sellerBalance === 0n) {
    throw new Error("Seller has no tokens! Run test-buy.js first.");
  }

  // Get sell amount from environment or use default (50% of balance)
  const sellPercentage = parseFloat(process.env.SELL_PERCENTAGE || "50");
  const sellAmount = (sellerBalance * BigInt(Math.floor(sellPercentage * 100))) / 10000n;

  console.log(`\nSelling ${sellPercentage}% of balance: ${formatBNB(sellAmount, hre.ethers)} tokens`);

  // Get state before sell
  console.log("\n📊 State BEFORE sale:");
  const bnbReserveBefore = await token.bnbReserve();
  const tokenReserveBefore = await token.tokenReserve();
  const sellerTokenBalanceBefore = sellerBalance;
  const sellerBNBBefore = await hre.ethers.provider.getBalance(seller.address);

  console.log(`   BNB Reserve: ${formatBNB(bnbReserveBefore, hre.ethers)} BNB`);
  console.log(`   Token Reserve: ${formatBNB(tokenReserveBefore, hre.ethers)} tokens`);
  console.log(`   Seller Token Balance: ${formatBNB(sellerTokenBalanceBefore, hre.ethers)} tokens`);
  console.log(`   Seller BNB Balance: ${formatBNB(sellerBNBBefore, hre.ethers)} BNB`);

  // Calculate expected BNB
  console.log("\n💰 Calculating expected BNB return...");
  try {
    const expectedBNB = await token.calculateSellAmount(sellAmount);
    console.log(`   Expected BNB: ${formatBNB(expectedBNB, hre.ethers)}`);

    // Calculate effective price
    const effectivePrice = parseFloat(formatBNB(expectedBNB, hre.ethers)) / parseFloat(formatBNB(sellAmount, hre.ethers));
    console.log(`   Effective Price: ${effectivePrice.toFixed(10)} BNB per token`);
  } catch (error) {
    console.log(`   ⚠️  Cannot calculate: ${error.message}`);
  }

  // Approve tokens for sale
  console.log("\n🔓 Approving tokens...");
  const approveTx = await token.approve(deployments.testToken, sellAmount);
  await waitForTx(approveTx, "Token approval");

  // Execute sell
  console.log("\n💸 Executing sale...");
  const tx = await token.sell(sellAmount, 0); // minBnbOut = 0 for testing
  const receipt = await waitForTx(tx, "Token sale");

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
        if (parsed.name === 'TokenSold') {
          console.log(`     Seller: ${parsed.args.seller}`);
          console.log(`     Token Amount: ${formatBNB(parsed.args.tokenAmount, hre.ethers)} tokens`);
          console.log(`     BNB Amount: ${formatBNB(parsed.args.bnbAmount, hre.ethers)} BNB`);
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

  // Get state after sell
  console.log("\n📊 State AFTER sale:");
  const bnbReserveAfter = await token.bnbReserve();
  const tokenReserveAfter = await token.tokenReserve();
  const sellerTokenBalanceAfter = await token.balanceOf(seller.address);
  const sellerBNBAfter = await hre.ethers.provider.getBalance(seller.address);

  console.log(`   BNB Reserve: ${formatBNB(bnbReserveAfter, hre.ethers)} BNB`);
  console.log(`   Token Reserve: ${formatBNB(tokenReserveAfter, hre.ethers)} tokens`);
  console.log(`   Seller Token Balance: ${formatBNB(sellerTokenBalanceAfter, hre.ethers)} tokens`);
  console.log(`   Seller BNB Balance: ${formatBNB(sellerBNBAfter, hre.ethers)} BNB`);

  // Calculate changes
  console.log("\n📈 Changes:");
  const bnbReserveChange = bnbReserveBefore - bnbReserveAfter;
  const tokenReserveChange = tokenReserveAfter - tokenReserveBefore;
  const sellerTokenChange = sellerTokenBalanceBefore - sellerTokenBalanceAfter;
  const sellerBNBChange = sellerBNBAfter - sellerBNBBefore;

  console.log(`   BNB Reserve: -${formatBNB(bnbReserveChange, hre.ethers)} BNB`);
  console.log(`   Token Reserve: +${formatBNB(tokenReserveChange, hre.ethers)} tokens`);
  console.log(`   Seller Tokens: -${formatBNB(sellerTokenChange, hre.ethers)} tokens`);
  console.log(`   Seller BNB Received: ${formatBNB(sellerBNBChange, hre.ethers)} BNB (after gas)`);

  // Calculate net BNB (excluding gas)
  const gasUsed = receipt.gasUsed * receipt.gasPrice;
  const netBNBReceived = sellerBNBChange + gasUsed;
  console.log(`   Gas Cost: ${formatBNB(gasUsed, hre.ethers)} BNB`);
  console.log(`   Net BNB Received: ${formatBNB(netBNBReceived, hre.ethers)} BNB`);

  // Calculate effective price
  const effectivePrice = parseFloat(formatBNB(netBNBReceived, hre.ethers)) / parseFloat(formatBNB(sellerTokenChange, hre.ethers));
  console.log(`   Effective Price: ${effectivePrice.toFixed(10)} BNB per token`);

  // Check graduation progress
  const factory = await getContract("TokenLaunchFactory", deployments.factory, hre.ethers);
  const graduationThreshold = await factory.GRADUATION_THRESHOLD();
  const progressPercent = (Number(bnbReserveAfter) / Number(graduationThreshold) * 100).toFixed(2);

  console.log(`\n🎓 Graduation Progress:`);
  console.log(`   Current: ${formatBNB(bnbReserveAfter, hre.ethers)} BNB`);
  console.log(`   Target: ${formatBNB(graduationThreshold, hre.ethers)} BNB`);
  console.log(`   Progress: ${progressPercent}%`);

  console.log("\n✅ Sale test complete!");
  console.log(`   View transaction: ${getExplorerUrl(networkName, 'tx', receipt.hash)}`);

  // Print next steps
  console.log("\n" + "=".repeat(60));
  console.log("NEXT STEPS:");
  console.log("-".repeat(60));
  console.log("1. Buy more tokens:");
  console.log(`   BUY_AMOUNT=0.05 npx hardhat run scripts/test-buy.js --network ${networkName}`);
  console.log("\n2. Sell more tokens:");
  console.log(`   SELL_PERCENTAGE=25 npx hardhat run scripts/test-sell.js --network ${networkName}`);
  console.log("\n3. Continue buying to reach graduation:");
  console.log(`   BUY_AMOUNT=1.0 npx hardhat run scripts/test-buy.js --network ${networkName}`);
  console.log("=".repeat(60) + "\n");

  return receipt;
}

// Execute script
if (require.main === module) {
  main()
    .then(() => process.exit(0))
    .catch((error) => {
      console.error("\n❌ SELL TEST FAILED\n");
      console.error(error);
      process.exit(1);
    });
}

module.exports = main;
