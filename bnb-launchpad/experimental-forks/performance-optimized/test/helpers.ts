import { ethers } from "hardhat";

/**
 * Deploy mock contracts for testing
 */
export async function deployMocks() {
  // Deploy mock WETH
  const MockWETH = await ethers.getContractFactory("MockWETH");
  const weth = await MockWETH.deploy();
  await weth.waitForDeployment();

  // Deploy mock PancakeFactory
  const MockPancakeFactory = await ethers.getContractFactory("MockPancakeFactory");
  const factory = await MockPancakeFactory.deploy();
  await factory.waitForDeployment();

  // Deploy mock PancakeRouter
  const MockPancakeRouter = await ethers.getContractFactory("MockPancakeRouter");
  const router = await MockPancakeRouter.deploy(
    await weth.getAddress(),
    await factory.getAddress()
  );
  await router.waitForDeployment();

  return { weth, factory, router };
}
