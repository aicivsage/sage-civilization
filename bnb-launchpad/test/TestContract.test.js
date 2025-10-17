const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("TestContract", function () {
  let testContract;
  let owner;
  let addr1;

  beforeEach(async function () {
    [owner, addr1] = await ethers.getSigners();

    const TestContract = await ethers.getContractFactory("TestContract");
    testContract = await TestContract.deploy();
    await testContract.waitForDeployment();
  });

  describe("Deployment", function () {
    it("Should set the initial message", async function () {
      expect(await testContract.message()).to.equal("Hardhat setup successful!");
    });

    it("Should set the initial value to 0", async function () {
      expect(await testContract.value()).to.equal(0);
    });
  });

  describe("Message Updates", function () {
    it("Should update message correctly", async function () {
      const newMessage = "Updated message";
      await testContract.setMessage(newMessage);
      expect(await testContract.message()).to.equal(newMessage);
    });

    it("Should emit MessageUpdated event", async function () {
      const newMessage = "Event test";
      await expect(testContract.setMessage(newMessage))
        .to.emit(testContract, "MessageUpdated")
        .withArgs(newMessage, await ethers.provider.getBlock('latest').then(b => b.timestamp + 1));
    });
  });

  describe("Value Updates", function () {
    it("Should update value correctly", async function () {
      const newValue = 42;
      await testContract.setValue(newValue);
      expect(await testContract.value()).to.equal(newValue);
    });

    it("Should emit ValueUpdated event", async function () {
      const newValue = 100;
      await expect(testContract.setValue(newValue))
        .to.emit(testContract, "ValueUpdated");
    });
  });

  describe("GetAll Function", function () {
    it("Should return both message and value", async function () {
      const newMessage = "Test message";
      const newValue = 999;

      await testContract.setMessage(newMessage);
      await testContract.setValue(newValue);

      const [message, value] = await testContract.getAll();
      expect(message).to.equal(newMessage);
      expect(value).to.equal(newValue);
    });
  });
});
