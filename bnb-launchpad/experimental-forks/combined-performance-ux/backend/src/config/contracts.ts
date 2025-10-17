export const CONTRACTS = {
  factory: process.env.FACTORY_ADDRESS || '0x5FD5a0914864B4A28fA7423b8BFAf436F210CEfC',
};

export const ABIS = {
  factory: [
    'function getAllTokens() view returns (address[])',
    'function getTokenCount() view returns (uint256)',
    'function createToken(string name, string symbol) returns (address)',
    'event TokenCreated(address indexed tokenAddress, address indexed creator, string name, string symbol)',
  ],
  token: [
    // View functions
    'function name() view returns (string)',
    'function symbol() view returns (string)',
    'function decimals() view returns (uint8)',
    'function totalSupply() view returns (uint256)',
    'function balanceOf(address account) view returns (uint256)',
    'function getCurrentReserves() view returns (uint256 bnbReserves, uint256 tokenReserves)',
    'function status() view returns (uint8)',
    'function isGraduated() view returns (bool)',
    'function graduationTimestamp() view returns (uint256)',
    'function creator() view returns (address)',
    'function platformFeeRecipient() view returns (address)',
    'function calculateTokensReceived(uint256 bnbAmount) view returns (uint256)',
    'function calculateBNBReceived(uint256 tokenAmount) view returns (uint256)',
    'function pendingFees(address recipient) view returns (uint256)',
    // State-changing functions
    'function buy(uint256 minTokensOut) payable returns (uint256)',
    'function sell(uint256 tokenAmount, uint256 minBnbOut) returns (uint256)',
    'function withdrawFees() external',
    'function graduateToPancakeSwap() external',
    // Events
    'event TokensPurchased(address indexed buyer, uint256 bnbAmount, uint256 tokensReceived, uint256 bnbToReserve)',
    'event TokensSold(address indexed seller, uint256 tokensSold, uint256 bnbAmount, uint256 bnbReturned)',
    'event StatusChanged(uint8 indexed oldStatus, uint8 indexed newStatus, uint256 timestamp)',
    'event GraduationTriggered(uint256 bnbReserves, uint256 timestamp)',
    'event GraduatedToPancakeSwap(address indexed pair, uint256 bnbAmount, uint256 tokenAmount, uint256 liquidity)',
  ],
};

export const BONDING_CURVE = {
  VIRTUAL_BNB: '30', // 30 ETH virtual reserves
  VIRTUAL_TOKENS: '1073000191', // Calculated from K / VIRTUAL_BNB
  K_CONSTANT: '32190005730', // K = 30 * 1073000191
  GRADUATION_THRESHOLD: '50', // 50 BNB
  PLATFORM_FEE_BPS: '100', // 1%
  CREATOR_FEE_BPS: '100', // 1%
  TOTAL_SUPPLY: '1000000000', // 1 billion tokens
};
