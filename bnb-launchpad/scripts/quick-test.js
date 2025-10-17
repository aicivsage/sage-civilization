const { ethers } = require("hardhat");

async function main() {
  const [signer] = await ethers.getSigners();
  const tokenAddress = "0x0B7145f6c99Ec2410e9147F0055D075A3fFEFEc1";

  console.log("\n=== Quick Buy Test ===\n");
  console.log("Token:", tokenAddress);
  console.log("Buyer:", signer.address);

  // Get token contract
  const Token = await ethers.getContractFactory("BondingCurveToken");
  const token = Token.attach(tokenAddress);

  // Check status before
  const balanceBefore = await token.balanceOf(signer.address);
  const bnbReserves = await token.bnbReserves();

  console.log("\nBefore Buy:");
  console.log("  Your tokens:", ethers.formatEther(balanceBefore), "TLT");
  console.log("  Contract BNB reserves:", ethers.formatEther(bnbReserves), "BNB");

  // Buy tokens
  const buyAmount = ethers.parseEther("0.01"); // 0.01 BNB
  console.log("\n💸 Buying with", ethers.formatEther(buyAmount), "BNB...");

  const tx = await token.buy(0, { value: buyAmount });
  console.log("  Tx:", tx.hash);

  const receipt = await tx.wait();
  console.log("  Confirmed! Block:", receipt.blockNumber);
  console.log("  Gas used:", receipt.gasUsed.toString());

  // Check status after
  const balanceAfter = await token.balanceOf(signer.address);
  const bnbReservesAfter = await token.bnbReserves();
  const tokensReceived = balanceAfter - balanceBefore;

  console.log("\nAfter Buy:");
  console.log("  Your tokens:", ethers.formatEther(balanceAfter), "TLT");
  console.log("  Tokens received:", ethers.formatEther(tokensReceived), "TLT");
  console.log("  Contract BNB reserves:", ethers.formatEther(bnbReservesAfter), "BNB");

  console.log("\n✅ Buy successful!");
  console.log("\nView transaction: https://testnet.bscscan.com/tx/" + tx.hash);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("\n❌ Error:", error.message);
    process.exit(1);
  });
