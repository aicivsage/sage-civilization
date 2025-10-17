const { ethers } = require("hardhat");

async function main() {
  const txHash = "0xce33734ba7f1a9ddba909b8fa0ad90312da934dc61537a9b92d18cadb23796c2";

  console.log("\n=== Transaction Details ===\n");
  console.log("Tx Hash:", txHash);

  const receipt = await ethers.provider.getTransactionReceipt(txHash);

  console.log("\nStatus:", receipt.status === 1 ? "✅ SUCCESS" : "❌ REVERTED");
  console.log("Block:", receipt.blockNumber);
  console.log("Gas Used:", receipt.gasUsed.toString());
  console.log("From:", receipt.from);
  console.log("To:", receipt.to);

  console.log("\nLogs (" + receipt.logs.length + " events):");
  for (let i = 0; i < receipt.logs.length; i++) {
    const log = receipt.logs[i];
    console.log(`\n  Event ${i + 1}:`);
    console.log("    Address:", log.address);
    console.log("    Topics:", log.topics.length);
    console.log("    Topic[0]:", log.topics[0]);
    console.log("    Data:", log.data);
  }

  // Try to decode TokenPurchase event
  const Token = await ethers.getContractFactory("BondingCurveToken");
  const iface = Token.interface;

  console.log("\n=== Decoded Events ===\n");
  for (const log of receipt.logs) {
    try {
      const parsed = iface.parseLog(log);
      if (parsed) {
        console.log("Event:", parsed.name);
        console.log("Args:", parsed.args);
      }
    } catch (e) {
      // Not a token event
    }
  }

  console.log("\nView on BscScan: https://testnet.bscscan.com/tx/" + txHash);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("\n❌ Error:", error);
    process.exit(1);
  });
