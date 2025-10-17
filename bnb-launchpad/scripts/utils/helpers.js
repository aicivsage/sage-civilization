// Helper utilities for deployment scripts

const fs = require('fs');
const path = require('path');

const DEPLOYMENTS_DIR = path.join(__dirname, '../../deployments');
const TESTNET_FILE = path.join(DEPLOYMENTS_DIR, 'testnet.json');
const MAINNET_FILE = path.join(DEPLOYMENTS_DIR, 'mainnet.json');

/**
 * Ensure deployments directory exists
 */
function ensureDeploymentsDir() {
  if (!fs.existsSync(DEPLOYMENTS_DIR)) {
    fs.mkdirSync(DEPLOYMENTS_DIR, { recursive: true });
  }
}

/**
 * Save deployment information
 * @param {string} network - Network name (testnet or mainnet)
 * @param {string} contractName - Name of the contract
 * @param {string} address - Deployed contract address
 * @param {object} extras - Additional data to save
 */
function saveDeployment(network, contractName, address, extras = {}) {
  ensureDeploymentsDir();

  const filePath = network === 'mainnet' ? MAINNET_FILE : TESTNET_FILE;

  let deployments = {};
  if (fs.existsSync(filePath)) {
    deployments = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  }

  deployments[contractName] = address;

  // Add timestamp
  if (!deployments.deployedAt) {
    deployments.deployedAt = new Date().toISOString();
  }
  deployments.lastUpdated = new Date().toISOString();

  // Add network info
  deployments.network = network === 'mainnet' ? 'bscMainnet' : 'bscTestnet';

  // Add any extra data
  Object.assign(deployments, extras);

  fs.writeFileSync(filePath, JSON.stringify(deployments, null, 2));
  console.log(`✅ Saved ${contractName} deployment: ${address}`);
}

/**
 * Load deployment information
 * @param {string} network - Network name (testnet or mainnet)
 * @returns {object} Deployment data
 */
function loadDeployment(network) {
  const filePath = network === 'mainnet' ? MAINNET_FILE : TESTNET_FILE;

  if (!fs.existsSync(filePath)) {
    console.warn(`⚠️  No deployment file found at ${filePath}`);
    return {};
  }

  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

/**
 * Get contract instance
 * @param {string} contractName - Name of the contract
 * @param {string} address - Contract address
 * @param {object} ethers - Ethers instance from hardhat
 * @returns {object} Contract instance
 */
async function getContract(contractName, address, ethers) {
  const ContractFactory = await ethers.getContractFactory(contractName);
  return ContractFactory.attach(address);
}

/**
 * Format BNB amount for display
 * @param {string|number|BigInt} amount - Amount in wei
 * @param {object} ethers - Ethers instance
 * @returns {string} Formatted BNB amount
 */
function formatBNB(amount, ethers) {
  return ethers.formatEther(amount);
}

/**
 * Parse BNB amount from string
 * @param {string} amount - Amount in BNB
 * @param {object} ethers - Ethers instance
 * @returns {BigInt} Amount in wei
 */
function parseBNB(amount, ethers) {
  return ethers.parseEther(amount);
}

/**
 * Wait for transaction with logging
 * @param {object} tx - Transaction object
 * @param {string} description - Description of what the transaction does
 * @returns {object} Transaction receipt
 */
async function waitForTx(tx, description) {
  console.log(`⏳ ${description}...`);
  console.log(`   Tx hash: ${tx.hash}`);

  const receipt = await tx.wait();

  console.log(`✅ ${description} confirmed!`);
  console.log(`   Block: ${receipt.blockNumber}`);
  console.log(`   Gas used: ${receipt.gasUsed.toString()}`);

  return receipt;
}

/**
 * Sleep for specified milliseconds
 * @param {number} ms - Milliseconds to sleep
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Get block explorer URL
 * @param {string} network - Network name
 * @param {string} type - Type (address, tx, token)
 * @param {string} value - Address or transaction hash
 * @returns {string} Block explorer URL
 */
function getExplorerUrl(network, type, value) {
  const baseUrl = network === 'mainnet'
    ? 'https://bscscan.com'
    : 'https://testnet.bscscan.com';

  const typeMap = {
    address: 'address',
    tx: 'tx',
    token: 'token'
  };

  return `${baseUrl}/${typeMap[type]}/${value}`;
}

/**
 * Print deployment summary
 * @param {object} deployments - Deployment data
 * @param {string} network - Network name
 */
function printDeploymentSummary(deployments, network) {
  console.log('\n' + '='.repeat(60));
  console.log('DEPLOYMENT SUMMARY');
  console.log('='.repeat(60));
  console.log(`Network: ${deployments.network || network}`);
  console.log(`Deployed at: ${deployments.deployedAt || 'N/A'}`);
  console.log(`Last updated: ${deployments.lastUpdated || 'N/A'}`);
  console.log('-'.repeat(60));

  const excludeKeys = ['network', 'deployedAt', 'lastUpdated', 'deployer'];

  for (const [key, value] of Object.entries(deployments)) {
    if (!excludeKeys.includes(key)) {
      console.log(`${key.padEnd(25)}: ${value}`);
      console.log(`${''.padEnd(25)}  ${getExplorerUrl(network, 'address', value)}`);
    }
  }

  if (deployments.deployer) {
    console.log('-'.repeat(60));
    console.log(`Deployer: ${deployments.deployer}`);
  }

  console.log('='.repeat(60) + '\n');
}

/**
 * Verify account has sufficient balance
 * @param {object} signer - Ethers signer
 * @param {string} minBalance - Minimum balance required (in BNB)
 * @param {object} ethers - Ethers instance
 */
async function verifyBalance(signer, minBalance, ethers) {
  const address = await signer.getAddress();
  const balance = await ethers.provider.getBalance(address);
  const balanceBNB = parseFloat(formatBNB(balance, ethers));
  const minBNB = parseFloat(minBalance);

  console.log(`Account: ${address}`);
  console.log(`Balance: ${balanceBNB.toFixed(4)} BNB`);

  if (balanceBNB < minBNB) {
    throw new Error(`Insufficient balance. Required: ${minBNB} BNB, Available: ${balanceBNB.toFixed(4)} BNB`);
  }

  console.log(`✅ Sufficient balance for deployment\n`);
}

/**
 * Find event in transaction receipt
 * @param {object} receipt - Transaction receipt
 * @param {string} eventName - Event name to find
 * @returns {object|null} Event log or null
 */
function findEvent(receipt, eventName) {
  const event = receipt.logs.find(log => {
    try {
      return log.fragment && log.fragment.name === eventName;
    } catch {
      return false;
    }
  });
  return event || null;
}

module.exports = {
  saveDeployment,
  loadDeployment,
  getContract,
  formatBNB,
  parseBNB,
  waitForTx,
  sleep,
  getExplorerUrl,
  printDeploymentSummary,
  verifyBalance,
  findEvent,
  DEPLOYMENTS_DIR,
  TESTNET_FILE,
  MAINNET_FILE
};
