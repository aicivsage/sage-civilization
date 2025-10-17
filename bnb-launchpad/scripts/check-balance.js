const { ethers } = require("hardhat");

async function main() {
  const [signer] = await ethers.getSigners();
  const address = await signer.getAddress();
  const balance = await ethers.provider.getBalance(address);

  console.log("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
  console.log("💰 Wallet Balance Check");
  console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
  console.log("Address:", address);
  console.log("Balance:", ethers.formatEther(balance), "BNB");
  console.log("\nView on BscScan:");
  console.log("https://testnet.bscscan.com/address/" + address);
  console.log("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");

  if (balance === 0n) {
    console.log("⚠️  Balance is 0 - need to fund from faucet!");
    console.log("\nFaucets:");
    console.log("- https://faucet.quicknode.com/binance-smart-chain/bnb-testnet");
    console.log("- https://testnet.bnbchain.org/faucet-smart");
    console.log("- https://faucets.chain.link/bnb-chain-testnet\n");
  } else if (balance < ethers.parseEther("0.05")) {
    console.log("⚠️  Balance low - may need more for full testing");
    console.log("    Minimum for deployment: 0.05 BNB");
    console.log("    Recommended: 0.1+ BNB\n");
  } else {
    console.log("✅ Sufficient balance for deployment!\n");
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
