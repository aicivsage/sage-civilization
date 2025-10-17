import { ethers } from 'ethers';
import { format } from 'date-fns';

/**
 * Format an Ethereum address for display
 * @param address - Full address
 * @param chars - Number of characters to show on each side
 */
export const formatAddress = (address: string, chars: number = 4): string => {
  if (!address) return '';
  return `${address.slice(0, chars + 2)}...${address.slice(-chars)}`;
};

/**
 * Format BNB amount with decimals
 */
export const formatBNB = (amount: string | number, decimals: number = 4): string => {
  const num = typeof amount === 'string' ? parseFloat(amount) : amount;
  if (isNaN(num)) return '0';

  return num.toFixed(decimals);
};

/**
 * Format token amount with appropriate decimals
 */
export const formatTokenAmount = (
  amount: string | ethers.BigNumber,
  decimals: number = 18,
  displayDecimals: number = 2
): string => {
  try {
    const formatted = ethers.utils.formatUnits(amount, decimals);
    const num = parseFloat(formatted);

    if (num === 0) return '0';
    if (num < 0.01) return num.toExponential(2);
    if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B';
    if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M';
    if (num >= 1e3) return (num / 1e3).toFixed(2) + 'K';

    return num.toFixed(displayDecimals);
  } catch (error) {
    console.error('Error formatting token amount:', error);
    return '0';
  }
};

/**
 * Format USD value
 */
export const formatUSD = (amount: number | string): string => {
  const num = typeof amount === 'string' ? parseFloat(amount) : amount;
  if (isNaN(num)) return '$0.00';

  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(num);
};

/**
 * Format percentage change
 */
export const formatPercentage = (value: number, includeSign: boolean = true): string => {
  const sign = includeSign && value > 0 ? '+' : '';
  return `${sign}${value.toFixed(2)}%`;
};

/**
 * Format timestamp to readable date
 */
export const formatDate = (timestamp: number | string): string => {
  const time = typeof timestamp === 'string' ? parseInt(timestamp) : timestamp;
  return format(new Date(time * 1000), 'MMM dd, yyyy HH:mm');
};

/**
 * Format time ago (e.g., "2 hours ago")
 */
export const formatTimeAgo = (timestamp: number): string => {
  const seconds = Math.floor((Date.now() - timestamp) / 1000);

  if (seconds < 60) return `${seconds}s ago`;
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
  return `${Math.floor(seconds / 86400)}d ago`;
};

/**
 * Format transaction hash for BSCScan link
 */
export const getTxLink = (hash: string, isMainnet: boolean = false): string => {
  const baseUrl = isMainnet
    ? 'https://bscscan.com/tx/'
    : 'https://testnet.bscscan.com/tx/';
  return `${baseUrl}${hash}`;
};

/**
 * Format address for BSCScan link
 */
export const getAddressLink = (address: string, isMainnet: boolean = false): string => {
  const baseUrl = isMainnet
    ? 'https://bscscan.com/address/'
    : 'https://testnet.bscscan.com/address/';
  return `${baseUrl}${address}`;
};

/**
 * Parse input value to Wei
 */
export const parseInputValue = (value: string): ethers.BigNumber => {
  try {
    return ethers.utils.parseEther(value || '0');
  } catch {
    return ethers.BigNumber.from(0);
  }
};

/**
 * Validate BNB amount
 */
export const isValidBNBAmount = (amount: string): boolean => {
  try {
    const parsed = parseFloat(amount);
    return !isNaN(parsed) && parsed > 0 && parsed < 1000000;
  } catch {
    return false;
  }
};

/**
 * Calculate price impact
 */
export const calculatePriceImpact = (
  inputAmount: ethers.BigNumber,
  currentReserves: ethers.BigNumber,
  virtualReserves: ethers.BigNumber
): number => {
  try {
    const totalReserves = currentReserves.add(virtualReserves);
    const impact = inputAmount.mul(10000).div(totalReserves);
    return impact.toNumber() / 100;
  } catch {
    return 0;
  }
};
