const { ethers } = require("hardhat");

async function main() {
  const toAddress = process.env.TO_ADDRESS || "0x756B8F288741537BD7A54d58917cc734aFa5e447";
  const amount = process.env.AMOUNT || "0.1";

  console.log("\n🚀 Sending testnet BNB...\n");
  console.log("To:", toAddress);
  console.log("Amount:", amount, "BNB");

  const [signer] = await ethers.getSigners();
  const fromAddress = await signer.getAddress();

  console.log("From:", fromAddress);

  // Check balance
  const balance = await ethers.provider.getBalance(fromAddress);
  console.log("Current balance:", ethers.formatEther(balance), "BNB");

  if (balance < ethers.parseEther(amount)) {
    console.error("\n❌ Insufficient balance!");
    process.exit(1);
  }

  // Send transaction
  console.log("\n📤 Sending...");
  const tx = await signer.sendTransaction({
    to: toAddress,
    value: ethers.parseEther(amount)
  });

  console.log("Transaction hash:", tx.hash);
  console.log("Waiting for confirmation...");

  const receipt = await tx.wait();
  console.log("✅ Confirmed in block:", receipt.blockNumber);

  // Check new balance
  const newBalance = await ethers.provider.getBalance(fromAddress);
  console.log("\nNew balance:", ethers.formatEther(newBalance), "BNB");
  console.log("\nView on BscScan:");
  console.log(`https://testnet.bscscan.com/tx/${tx.hash}`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("\n❌ Error:", error);
    process.exit(1);
  });
