const { ethers } = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  console.log("🔐 Generating new testnet wallet...\n");

  // Generate a random wallet
  const wallet = ethers.Wallet.createRandom();

  console.log("✅ Wallet Generated!\n");
  console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
  console.log("📍 Address:", wallet.address);
  console.log("🔑 Private Key:", wallet.privateKey);
  console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");

  console.log("⚠️  IMPORTANT: This is a TESTNET wallet only!");
  console.log("    Never use this private key on mainnet.\n");

  // Save to .env
  const envPath = path.join(__dirname, "..", ".env");
  const envContent = `# Generated Testnet Wallet
PRIVATE_KEY=${wallet.privateKey}
PLATFORM_FEE_RECIPIENT=${wallet.address}

# BscScan API Key (get free key at https://bscscan.com/apis)
BSCSCAN_API_KEY=

# Token parameters (optional)
TOKEN_NAME="Test Launch Token"
TOKEN_SYMBOL="TLT"
`;

  fs.writeFileSync(envPath, envContent);
  console.log("✅ Saved to .env file\n");

  console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
  console.log("🎯 NEXT STEPS:");
  console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
  console.log("\n1. Fund this wallet with testnet BNB:");
  console.log("   Address:", wallet.address);
  console.log("\n   📍 Faucets:");
  console.log("   - QuickNode: https://faucet.quicknode.com/binance-smart-chain/bnb-testnet");
  console.log("   - Official:  https://testnet.bnbchain.org/faucet-smart");
  console.log("   - Chainlink: https://faucets.chain.link/bnb-chain-testnet");
  console.log("\n2. Check balance:");
  console.log("   npx hardhat run scripts/check-balance.js --network bscTestnet");
  console.log("\n3. Deploy when funded:");
  console.log("   npx hardhat run scripts/deploy-factory.js --network bscTestnet");
  console.log("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
