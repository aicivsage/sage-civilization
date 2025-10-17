import { useCallback, useEffect, useState } from 'react';
import { ethers } from 'ethers';
import { CONTRACTS } from '../utils/constants';

// Minimal ABI - just the functions we need (CORRECTED TO MATCH ACTUAL CONTRACTS)
const FACTORY_ABI = [
  'function createToken(string name, string symbol) returns (address)',
  'function getAllTokens() view returns (address[])',
  'function getTokenCount() view returns (uint256)',
  'event TokenCreated(address indexed tokenAddress, address indexed creator, string name, string symbol)',
];

const TOKEN_ABI = [
  'function name() view returns (string)',
  'function symbol() view returns (string)',
  'function decimals() view returns (uint8)',
  'function totalSupply() view returns (uint256)',
  'function getCurrentReserves() view returns (uint256 bnbReserves, uint256 tokenReserves)',
  'function status() view returns (uint8)',
  'function isGraduated() view returns (bool)',
  'function graduationTimestamp() view returns (uint256)',
  'function creator() view returns (address)',
  'function buy(uint256 minTokensOut) payable returns (uint256)',
  'function sell(uint256 tokensToSell, uint256 minBnbOut) returns (uint256)',
  'function calculateTokensReceived(uint256 bnbAmount) view returns (uint256)',
  'function calculateBNBReceived(uint256 tokenAmount) view returns (uint256)',
  'function balanceOf(address account) view returns (uint256)',
  'function approve(address spender, uint256 amount) returns (bool)',
  'function allowance(address owner, address spender) view returns (uint256)',
  'function pendingFees(address recipient) view returns (uint256)',
  'function withdrawFees() external',
  'event TokensPurchased(address indexed buyer, uint256 bnbAmount, uint256 tokensReceived, uint256 bnbToReserve)',
  'event TokensSold(address indexed seller, uint256 tokensSold, uint256 bnbAmount, uint256 bnbReturned)',
  'event GraduationTriggered(uint256 bnbReserves, uint256 timestamp)',
];

export const useContract = (
  provider: ethers.providers.Web3Provider | null,
  signer: ethers.Signer | null
) => {
  const [factoryContract, setFactoryContract] = useState<ethers.Contract | null>(null);

  // Initialize factory contract
  useEffect(() => {
    if (provider) {
      const contract = new ethers.Contract(
        CONTRACTS.FACTORY,
        FACTORY_ABI,
        signer || provider
      );
      setFactoryContract(contract);
    }
  }, [provider, signer]);

  // Create a token contract instance
  const getTokenContract = useCallback(
    (tokenAddress: string) => {
      if (!provider) return null;

      return new ethers.Contract(
        tokenAddress,
        TOKEN_ABI,
        signer || provider
      );
    },
    [provider, signer]
  );

  // Create a new token
  const createToken = useCallback(
    async (name: string, symbol: string) => {
      if (!factoryContract || !signer) {
        throw new Error('Wallet not connected');
      }

      // Validate network before transaction
      if (provider) {
        const network = await provider.getNetwork();
        if (network.chainId !== 97) {
          throw new Error('Please switch to BSC Testnet (Chain ID 97) in MetaMask');
        }
      }

      const tx = await factoryContract.createToken(name, symbol, {
        gasLimit: 3000000,
      });

      const receipt = await tx.wait();

      // Extract token address from event
      const event = receipt.events?.find((e: any) => e.event === 'TokenCreated');
      const tokenAddress = event?.args?.tokenAddress;

      return { tx, receipt, tokenAddress };
    },
    [factoryContract, signer, provider]
  );

  // Get all tokens
  const getAllTokens = useCallback(async () => {
    if (!factoryContract) return [];

    try {
      const tokens = await factoryContract.getAllTokens();
      return tokens;
    } catch (error) {
      console.error('Error fetching tokens:', error);
      return [];
    }
  }, [factoryContract]);

  // Buy tokens
  const buyTokens = useCallback(
    async (tokenAddress: string, bnbAmount: string, minTokens: string = '0') => {
      if (!signer) {
        throw new Error('Wallet not connected');
      }

      // Validate network before transaction
      if (provider) {
        const network = await provider.getNetwork();
        if (network.chainId !== 97) {
          throw new Error('Please switch to BSC Testnet (Chain ID 97) in MetaMask');
        }
      }

      const tokenContract = getTokenContract(tokenAddress);
      if (!tokenContract) {
        throw new Error('Token contract not found');
      }

      const tx = await tokenContract.buy(
        ethers.utils.parseEther(minTokens),
        {
          value: ethers.utils.parseEther(bnbAmount),
          gasLimit: 500000,
        }
      );

      return await tx.wait();
    },
    [getTokenContract, signer, provider]
  );

  // Sell tokens
  const sellTokens = useCallback(
    async (tokenAddress: string, tokenAmount: string, minBNB: string = '0') => {
      if (!signer) {
        throw new Error('Wallet not connected');
      }

      // Validate network before transaction
      if (provider) {
        const network = await provider.getNetwork();
        if (network.chainId !== 97) {
          throw new Error('Please switch to BSC Testnet (Chain ID 97) in MetaMask');
        }
      }

      const tokenContract = getTokenContract(tokenAddress);
      if (!tokenContract) {
        throw new Error('Token contract not found');
      }

      const tx = await tokenContract.sell(
        ethers.utils.parseEther(tokenAmount),
        ethers.utils.parseEther(minBNB),
        {
          gasLimit: 500000,
        }
      );

      return await tx.wait();
    },
    [getTokenContract, signer, provider]
  );

  // Get token balance
  const getTokenBalance = useCallback(
    async (tokenAddress: string, account: string) => {
      const tokenContract = getTokenContract(tokenAddress);
      if (!tokenContract) return '0';

      try {
        const balance = await tokenContract.balanceOf(account);
        return ethers.utils.formatEther(balance);
      } catch (error) {
        console.error('Error fetching balance:', error);
        return '0';
      }
    },
    [getTokenContract]
  );

  // Get token info
  const getTokenInfo = useCallback(
    async (tokenAddress: string) => {
      const tokenContract = getTokenContract(tokenAddress);
      if (!tokenContract) return null;

      try {
        const [name, symbol, totalSupply, reserves, status, graduationTimestamp, isGraduated] =
          await Promise.all([
            tokenContract.name(),
            tokenContract.symbol(),
            tokenContract.totalSupply(),
            tokenContract.getCurrentReserves(),
            tokenContract.status(),
            tokenContract.graduationTimestamp(),
            tokenContract.isGraduated(),
          ]);

        return {
          name,
          symbol,
          totalSupply: ethers.utils.formatEther(totalSupply),
          bnbReserves: ethers.utils.formatEther(reserves[0]),
          tokenReserves: ethers.utils.formatEther(reserves[1]),
          status,
          isGraduated,
          graduationTimestamp: graduationTimestamp.toString(),
        };
      } catch (error) {
        console.error('Error fetching token info:', error);
        return null;
      }
    },
    [getTokenContract]
  );

  return {
    factoryContract,
    getTokenContract,
    createToken,
    getAllTokens,
    buyTokens,
    sellTokens,
    getTokenBalance,
    getTokenInfo,
  };
};
