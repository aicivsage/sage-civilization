import { ethers } from 'ethers';
import { CONTRACTS, ABIS, BONDING_CURVE } from '../config/contracts';

export class PriceService {
  private provider: ethers.providers.JsonRpcProvider;

  constructor() {
    this.provider = new ethers.providers.JsonRpcProvider(
      process.env.RPC_URL || 'https://data-seed-prebsc-1-s1.bnbchain.org:8545/'
    );
  }

  async getPrice(tokenAddress: string): Promise<string> {
    try {
      const contract = new ethers.Contract(tokenAddress, ABIS.token, this.provider);

      // getCurrentReserves() returns [bnbReserves, tokenReserves] (already includes virtual reserves)
      const reserves = await contract.getCurrentReserves();
      const bnbReserves = reserves[0];
      const tokenReserves = reserves[1];

      if (tokenReserves.isZero()) {
        return '0';
      }

      // Price = BNB reserves / Token reserves
      const price = bnbReserves.mul(ethers.utils.parseEther('1')).div(tokenReserves);

      return ethers.utils.formatEther(price);
    } catch (error) {
      console.error(`Error getting price for ${tokenAddress}:`, error);
      return '0';
    }
  }

  async getFullData(tokenAddress: string) {
    try {
      const contract = new ethers.Contract(tokenAddress, ABIS.token, this.provider);

      const [name, symbol, reserves, status, graduationTimestamp, isGraduated] = await Promise.all([
        contract.name(),
        contract.symbol(),
        contract.getCurrentReserves(),
        contract.status(),
        contract.graduationTimestamp(),
        contract.isGraduated(),
      ]);

      const price = await this.getPrice(tokenAddress);
      const bnbReserves = reserves[0];
      const tokenReserves = reserves[1];

      return {
        address: tokenAddress,
        name,
        symbol,
        price,
        bnbReserves: ethers.utils.formatEther(bnbReserves),
        tokenReserves: ethers.utils.formatEther(tokenReserves),
        status,
        isGraduated,
        graduationTimestamp: graduationTimestamp.toString(),
        timestamp: Date.now(),
      };
    } catch (error) {
      console.error(`Error getting full data for ${tokenAddress}:`, error);
      return null;
    }
  }

  async getActiveTokens(): Promise<string[]> {
    try {
      const factory = new ethers.Contract(CONTRACTS.factory, ABIS.factory, this.provider);
      const tokens = await factory.getAllTokens();
      return tokens;
    } catch (error) {
      console.error('Error getting active tokens:', error);
      return [];
    }
  }

  async getBuyQuote(tokenAddress: string, bnbAmount: string) {
    try {
      const contract = new ethers.Contract(tokenAddress, ABIS.token, this.provider);
      const bnbWei = ethers.utils.parseEther(bnbAmount);

      const tokensReceived = await contract.calculateTokensReceived(bnbWei);
      const currentPrice = await this.getPrice(tokenAddress);

      // Calculate fees (1% platform + 1% creator = 2% total)
      const platformFee = bnbWei.mul(100).div(10000); // 1%
      const creatorFee = bnbWei.mul(100).div(10000); // 1%
      const totalFee = platformFee.add(creatorFee);

      return {
        bnbAmount,
        tokensReceived: ethers.utils.formatEther(tokensReceived),
        currentPrice,
        platformFee: ethers.utils.formatEther(platformFee),
        creatorFee: ethers.utils.formatEther(creatorFee),
        totalFee: ethers.utils.formatEther(totalFee),
        priceImpact: '0', // Calculate if needed
      };
    } catch (error) {
      console.error(`Error getting buy quote for ${tokenAddress}:`, error);
      throw error;
    }
  }

  async getSellQuote(tokenAddress: string, tokenAmount: string) {
    try {
      const contract = new ethers.Contract(tokenAddress, ABIS.token, this.provider);
      const tokenWei = ethers.utils.parseEther(tokenAmount);

      const bnbReceived = await contract.calculateBNBReceived(tokenWei);
      const currentPrice = await this.getPrice(tokenAddress);

      // Fees are already deducted in calculateBNBReceived
      // But we can show them separately
      const bnbBeforeFees = bnbReceived.mul(10000).div(9800); // Reverse the 2% fee
      const platformFee = bnbBeforeFees.mul(100).div(10000); // 1%
      const creatorFee = bnbBeforeFees.mul(100).div(10000); // 1%
      const totalFee = platformFee.add(creatorFee);

      return {
        tokenAmount,
        bnbReceived: ethers.utils.formatEther(bnbReceived),
        currentPrice,
        platformFee: ethers.utils.formatEther(platformFee),
        creatorFee: ethers.utils.formatEther(creatorFee),
        totalFee: ethers.utils.formatEther(totalFee),
        priceImpact: '0', // Calculate if needed
      };
    } catch (error) {
      console.error(`Error getting sell quote for ${tokenAddress}:`, error);
      throw error;
    }
  }
}
