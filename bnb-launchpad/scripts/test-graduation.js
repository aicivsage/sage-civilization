// Test the full graduation flow to PancakeSwap

const hre = require("hardhat");
const {
  loadDeployment,
  getContract,
  waitForTx,
  getExplorerUrl,
  parseBNB,
  formatBNB,
  verifyBalance,
  sleep
} = require("./utils/helpers");

async function main() {
  const networkName = hre.network.name;
  console.log("\n" + "=".repeat(60));
  console.log("TEST GRADUATION TO PANCAKESWAP");
  console.log("=".repeat(60));
  console.log(`Network: ${networkName}`);
  console.log("-".repeat(60));

  // Get account
  const [account] = await hre.ethers.getSigners();
  console.log(`Account: ${account.address}`);

  // Load deployments
  const networkKey = networkName === 'bscMainnet' ? 'mainnet' : 'testnet';
  const deployments = loadDeployment(networkKey);

  if (!deployments.testToken) {
    throw new Error("Test token not found! Run create-test-token.js first.");
  }

  console.log(`Token Address: ${deployments.testToken}`);
  console.log(`Factory Address: ${deployments.factory}`);
  console.log("-".repeat(60));

  // Get contracts
  const token = await getContract("BondingCurveToken", deployments.testToken, hre.ethers);
  const factory = await getContract("TokenLaunchFactory", deployments.factory, hre.ethers);

  // Get token info
  const name = await token.name();
  const symbol = await token.symbol();
  console.log(`\nToken: ${name} (${symbol})`);

  // Check if already graduated
  const isGraduated = await token.isGraduated();
  if (isGraduated) {
    console.log("\n⚠️  Token is already graduated!");
    const lpPair = await token.lpPair();
    console.log(`   LP Pair: ${lpPair}`);
    console.log(`   View on BscScan: ${getExplorerUrl(networkKey, 'address', lpPair)}`);
    return;
  }

  // Get graduation parameters
  const graduationThreshold = await factory.GRADUATION_THRESHOLD();
  const cooldownPeriod = await factory.GRADUATION_COOLDOWN();
  const bnbReserve = await token.bnbReserve();
  const tokenReserve = await token.tokenReserve();

  console.log("\n📊 Current State:");
  console.log(`   BNB Reserve: ${formatBNB(bnbReserve, hre.ethers)} BNB`);
  console.log(`   Token Reserve: ${formatBNB(tokenReserve, hre.ethers)} tokens`);
  console.log(`   Graduation Threshold: ${formatBNB(graduationThreshold, hre.ethers)} BNB`);
  console.log(`   Cooldown Period: ${cooldownPeriod.toString()} seconds`);

  const progressPercent = (Number(bnbReserve) / Number(graduationThreshold) * 100).toFixed(2);
  console.log(`   Progress: ${progressPercent}%`);

  // Check if threshold reached
  if (bnbReserve < graduationThreshold) {
    const needed = graduationThreshold - bnbReserve;
    console.log(`\n⚠️  Graduation threshold not reached yet!`);
    console.log(`   Still need: ${formatBNB(needed, hre.ethers)} BNB`);

    // Ask if user wants to buy up to threshold
    const autoBuy = process.env.AUTO_BUY === 'true';
    if (!autoBuy) {
      console.log(`\n   To auto-buy to threshold, run:`);
      console.log(`   AUTO_BUY=true npx hardhat run scripts/test-graduation.js --network ${networkName}`);
      return;
    }

    console.log(`\n💰 Auto-buying to reach threshold...`);

    // Verify sufficient balance
    const requiredBNB = parseFloat(formatBNB(needed, hre.ethers)) * 1.05; // 5% extra for fees
    await verifyBalance(account, requiredBNB.toString(), hre.ethers);

    // Buy in chunks to avoid single large transaction
    const chunkSize = parseBNB("5", hre.ethers); // 5 BNB per buy
    let remaining = needed;
    let buyCount = 0;

    while (remaining > 0n) {
      const buyAmount = remaining > chunkSize ? chunkSize : remaining;
      buyCount++;

      console.log(`\n   Buy #${buyCount}: ${formatBNB(buyAmount, hre.ethers)} BNB`);
      const tx = await token.buy(0, { value: buyAmount }); // minTokensOut = 0
      await waitForTx(tx, `Buy #${buyCount}`);

      // Update reserves
      const newReserve = await token.bnbReserve();
      remaining = graduationThreshold - newReserve;

      console.log(`   New reserve: ${formatBNB(newReserve, hre.ethers)} BNB`);
      console.log(`   Remaining: ${formatBNB(remaining > 0n ? remaining : 0n, hre.ethers)} BNB`);

      if (remaining > 0n && buyCount < 20) {
        // Small delay between buys
        await sleep(2000);
      }
    }

    console.log(`\n✅ Threshold reached after ${buyCount} buys!`);
  } else {
    console.log(`\n✅ Graduation threshold already reached!`);
  }

  // Check graduation timestamp
  const graduationTimestamp = await token.graduationTimestamp();
  const currentTime = Math.floor(Date.now() / 1000);

  console.log(`\n⏰ Graduation Cooldown:`);
  console.log(`   Graduation Timestamp: ${graduationTimestamp.toString()}`);
  console.log(`   Current Time: ${currentTime}`);

  if (graduationTimestamp === 0n) {
    console.log(`   ⚠️  Graduation timestamp not set yet (first time hitting threshold)`);
  } else if (currentTime < Number(graduationTimestamp) + Number(cooldownPeriod)) {
    const remaining = Number(graduationTimestamp) + Number(cooldownPeriod) - currentTime;
    console.log(`   ⏳ Cooldown remaining: ${remaining} seconds (${(remaining / 60).toFixed(1)} minutes)`);

    if (process.env.SKIP_COOLDOWN !== 'true') {
      console.log(`\n   To skip waiting, you can try graduating anyway (may fail if cooldown not complete)`);
      console.log(`   Or run: SKIP_COOLDOWN=true npx hardhat run scripts/test-graduation.js --network ${networkName}`);
      return;
    }
  } else {
    console.log(`   ✅ Cooldown period complete!`);
  }

  // Get state before graduation
  console.log("\n📊 State BEFORE graduation:");
  const totalSupply = await token.totalSupply();
  const owner = await token.owner();

  console.log(`   Total Supply: ${formatBNB(totalSupply, hre.ethers)} tokens`);
  console.log(`   Owner: ${owner}`);
  console.log(`   BNB Reserve: ${formatBNB(bnbReserve, hre.ethers)} BNB`);
  console.log(`   Token Reserve: ${formatBNB(tokenReserve, hre.ethers)} tokens`);

  // Attempt graduation
  console.log("\n🎓 Attempting graduation to PancakeSwap...");
  try {
    const tx = await token.graduateToPancakeSwap();
    const receipt = await waitForTx(tx, "Graduation");

    // Parse events
    console.log("\n📋 Transaction Events:");
    let lpPairAddress = null;

    for (const log of receipt.logs) {
      try {
        const parsed = token.interface.parseLog({
          topics: [...log.topics],
          data: log.data
        });

        if (parsed) {
          console.log(`   Event: ${parsed.name}`);
          if (parsed.name === 'GraduatedToPancakeSwap') {
            lpPairAddress = parsed.args.lpPair;
            console.log(`     LP Pair: ${lpPairAddress}`);
            console.log(`     BNB Amount: ${formatBNB(parsed.args.bnbAmount, hre.ethers)} BNB`);
            console.log(`     Token Amount: ${formatBNB(parsed.args.tokenAmount, hre.ethers)} tokens`);
          }
        }
      } catch (e) {
        // Not a token event
        continue;
      }
    }

    // Get state after graduation
    console.log("\n📊 State AFTER graduation:");
    const isGraduatedAfter = await token.isGraduated();
    const lpPair = await token.lpPair();
    const bnbReserveAfter = await token.bnbReserve();
    const tokenReserveAfter = await token.tokenReserve();
    const ownerAfter = await token.owner();

    console.log(`   Is Graduated: ${isGraduatedAfter}`);
    console.log(`   LP Pair: ${lpPair}`);
    console.log(`   BNB Reserve: ${formatBNB(bnbReserveAfter, hre.ethers)} BNB`);
    console.log(`   Token Reserve: ${formatBNB(tokenReserveAfter, hre.ethers)} tokens`);
    console.log(`   Owner: ${ownerAfter}`);

    // Verify LP tokens burned
    console.log("\n🔥 Verifying LP tokens burned...");
    if (lpPair && lpPair !== hre.ethers.ZeroAddress) {
      const pairContract = await hre.ethers.getContractAt(
        ["function balanceOf(address) view returns (uint256)", "function totalSupply() view returns (uint256)"],
        lpPair
      );

      const burnAddress = "0x000000000000000000000000000000000000dEaD";
      const lpBalance = await pairContract.balanceOf(burnAddress);
      const lpTotalSupply = await pairContract.totalSupply();

      console.log(`   LP Total Supply: ${formatBNB(lpTotalSupply, hre.ethers)}`);
      console.log(`   LP Burned: ${formatBNB(lpBalance, hre.ethers)}`);
      console.log(`   Burn %: ${(Number(lpBalance) / Number(lpTotalSupply) * 100).toFixed(2)}%`);
    }

    // Verify ownership renounced
    console.log("\n👤 Verifying ownership...");
    if (ownerAfter === hre.ethers.ZeroAddress) {
      console.log("   ✅ Ownership renounced!");
    } else {
      console.log("   ⚠️  Ownership NOT renounced: " + ownerAfter);
    }

    console.log("\n✅ Graduation test complete!");
    console.log(`   View transaction: ${getExplorerUrl(networkKey, 'tx', receipt.hash)}`);
    console.log(`   View LP pair: ${getExplorerUrl(networkKey, 'address', lpPair)}`);

    // Print PancakeSwap trading info
    console.log("\n" + "=".repeat(60));
    console.log("PANCAKESWAP TRADING INFO");
    console.log("=".repeat(60));
    console.log(`Token: ${symbol}`);
    console.log(`Address: ${deployments.testToken}`);
    console.log(`LP Pair: ${lpPair}`);
    console.log(`\nTrade on PancakeSwap:`);
    if (networkName === 'bscTestnet') {
      console.log(`https://pancakeswap.finance/?chain=bscTestnet`);
    } else {
      console.log(`https://pancakeswap.finance/swap?outputCurrency=${deployments.testToken}`);
    }
    console.log("=".repeat(60) + "\n");

  } catch (error) {
    console.error("\n❌ Graduation failed!");
    console.error("Error:", error.message);

    if (error.message.includes("Cooldown")) {
      console.log("\n   Cooldown period not complete yet. Wait and try again.");
    } else if (error.message.includes("threshold")) {
      console.log("\n   Graduation threshold not reached. Buy more tokens first.");
    }

    throw error;
  }
}

// Execute script
if (require.main === module) {
  main()
    .then(() => process.exit(0))
    .catch((error) => {
      console.error("\n❌ GRADUATION TEST FAILED\n");
      console.error(error);
      process.exit(1);
    });
}

module.exports = main;
