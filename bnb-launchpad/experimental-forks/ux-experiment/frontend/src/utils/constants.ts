// Network Configuration
export const CHAIN_CONFIG = {
  BSC_TESTNET: {
    chainId: '0x61', // 97 in hex
    chainName: 'BSC Testnet',
    nativeCurrency: {
      name: 'BNB',
      symbol: 'BNB',
      decimals: 18,
    },
    rpcUrls: ['https://data-seed-prebsc-1-s1.bnbchain.org:8545/'],
    blockExplorerUrls: ['https://testnet.bscscan.com/'],
  },
  BSC_MAINNET: {
    chainId: '0x38', // 56 in hex
    chainName: 'BSC Mainnet',
    nativeCurrency: {
      name: 'BNB',
      symbol: 'BNB',
      decimals: 18,
    },
    rpcUrls: ['https://bsc-dataseed.binance.org/'],
    blockExplorerUrls: ['https://bscscan.com/'],
  },
};

// Contract Addresses (BSC Testnet)
export const CONTRACTS = {
  FACTORY: '0xBF9A7517d2b16318D1E24Eb66a0E4bF855841Ef0',
  PANCAKE_ROUTER: '0xD99D1c33F9fC3444f8101754aBC46c52416550D1',
  PANCAKE_FACTORY: '0x6725F303b657a9451d8BA641348b6761A6CC7a17',
};

// Bonding Curve Constants
export const BONDING_CURVE = {
  VIRTUAL_BNB: '30', // 30 BNB
  K_CONSTANT: '32190005730', // k = virtualBNB × virtualTokenSupply
  GRADUATION_THRESHOLD: '50', // 50 BNB
  INITIAL_TOKEN_SUPPLY: '1000000000', // 1 billion tokens
};

// WebSocket Configuration
export const WS_CONFIG = {
  URL: process.env.REACT_APP_WEBSOCKET_URL || process.env.REACT_APP_API_URL || 'http://localhost:4000',
  RECONNECTION_ATTEMPTS: 5,
  RECONNECTION_DELAY: 3000,
};

// UI Constants
export const UI = {
  TOAST_DURATION: 5000,
  CHART_UPDATE_INTERVAL: 2000,
  PRICE_DECIMALS: 10,
  BNB_DECIMALS: 4,
  TOKEN_DECIMALS: 2,
};

// Transaction Settings
export const TX_CONFIG = {
  GAS_LIMIT_BUFFER: 1.2, // 20% buffer
  MAX_SLIPPAGE: 0.05, // 5%
  DEADLINE_MINUTES: 20,
};

// Token Status
export enum TokenStatus {
  ACTIVE = 0,
  GRADUATED = 1,
  PAUSED = 2,
}

// Wallet Types
export enum WalletType {
  METAMASK = 'MetaMask',
  WALLET_CONNECT = 'WalletConnect',
}
