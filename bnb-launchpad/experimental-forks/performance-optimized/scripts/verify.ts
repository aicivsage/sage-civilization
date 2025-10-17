import { run } from "hardhat";

async function main() {
  console.log("Starting contract verification...\n");

  // Update these addresses after deployment
  const FACTORY_ADDRESS = process.env.FACTORY_ADDRESS || "";
  const TOKEN_ADDRESS = process.env.TOKEN_ADDRESS || "";

  if (!FACTORY_ADDRESS) {
    throw new Error("Please set FACTORY_ADDRESS environment variable");
  }

  // Factory constructor arguments
  const PLATFORM_FEE_RECIPIENT = process.env.PLATFORM_FEE_RECIPIENT || "";
  const CREATION_FEE = process.env.CREATION_FEE || "0.01";
  const PANCAKE_ROUTER = "0xD99D1c33F9fC3444f8101754aBC46c52416550D1"; // BSC Testnet

  console.log("Verifying Factory...");
  try {
    await run("verify:verify", {
      address: FACTORY_ADDRESS,
      constructorArguments: [
        PLATFORM_FEE_RECIPIENT,
        CREATION_FEE,
        PANCAKE_ROUTER,
      ],
    });
    console.log("✅ Factory verified");
  } catch (error: any) {
    if (error.message.includes("Already Verified")) {
      console.log("✅ Factory already verified");
    } else {
      console.error("❌ Factory verification failed:", error.message);
    }
  }

  if (TOKEN_ADDRESS) {
    console.log("\nVerifying Token...");
    try {
      // Token constructor arguments (from factory deployment)
      await run("verify:verify", {
        address: TOKEN_ADDRESS,
        constructorArguments: [
          "Test Optimized Token",
          "TESTO",
          PLATFORM_FEE_RECIPIENT,
          PLATFORM_FEE_RECIPIENT,
          PANCAKE_ROUTER,
        ],
      });
      console.log("✅ Token verified");
    } catch (error: any) {
      if (error.message.includes("Already Verified")) {
        console.log("✅ Token already verified");
      } else {
        console.error("❌ Token verification failed:", error.message);
      }
    }
  }

  console.log("\nVerification complete!");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
