// Contract Addresses (BSC Testnet)
const CONFIG = {
    NETWORK: {
        chainId: '0x61', // 97 in hex
        chainIdDecimal: 97,
        name: 'BNB Smart Chain Testnet',
        rpcUrl: 'https://data-seed-prebsc-1-s1.bnbchain.org:8545/',
        blockExplorer: 'https://testnet.bscscan.com',
        nativeCurrency: {
            name: 'tBNB',
            symbol: 'tBNB',
            decimals: 18
        }
    },

    CONTRACTS: {
        factory: '0x5FD5a0914864B4A28fA7423b8BFAf436F210CEfC',
        pancakeRouter: '0xD99D1c33F9fC3444f8101754aBC46c52416550D1'
    },

    // ABIs (minimal - only functions we need)
    ABIS: {
        factory: [
            "function createToken(string name, string symbol) external returns (address)",
            "function getAllTokens() external view returns (address[] memory)",
            "function getTokenCount() external view returns (uint256)",
            "function platformFeeRecipient() external view returns (address)",
            "event TokenCreated(address indexed tokenAddress, address indexed creator, string name, string symbol)"
        ],

        token: [
            "function name() external view returns (string)",
            "function symbol() external view returns (string)",
            "function balanceOf(address account) external view returns (uint256)",
            "function totalSupply() external view returns (uint256)",
            "function bnbReserves() external view returns (uint256)",
            "function creator() external view returns (address)",
            "function platformFeeRecipient() external view returns (address)",
            "function pendingFees(address account) external view returns (uint256)",
            "function status() external view returns (uint8)",
            "function graduationTimestamp() external view returns (uint256)",
            "function buy(uint256 minTokensOut) external payable",
            "function sell(uint256 tokensToSell, uint256 minBnbOut) external",
            "function withdrawFees() external",
            "function calculateTokensReceived(uint256 bnbAmount) external view returns (uint256)",
            "function calculateBNBReceived(uint256 tokenAmount) external view returns (uint256)",
            "function getCurrentReserves() external view returns (uint256, uint256)",
            "function isGraduated() external view returns (bool)",
            "function graduationCooldownRemaining() external view returns (uint256)",
            "event TokensPurchased(address indexed buyer, uint256 bnbAmount, uint256 tokensReceived, uint256 bnbToReserve)",
            "event TokensSold(address indexed seller, uint256 tokensSold, uint256 bnbAmount, uint256 bnbReturned)",
            "event FeesWithdrawn(address indexed recipient, uint256 amount)",
            "event StatusChanged(uint8 oldStatus, uint8 newStatus, uint256 timestamp)"
        ]
    },

    CONSTANTS: {
        GRADUATION_THRESHOLD: '50', // 50 BNB
        PLATFORM_FEE_BPS: 100, // 1%
        CREATOR_FEE_BPS: 100, // 1%
        MIN_BNB_AMOUNT: '0.001', // 0.001 BNB minimum buy
        TOTAL_SUPPLY: '1073000191' // Total token supply
    }
};
