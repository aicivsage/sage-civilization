import { ethers } from 'ethers';
import { Server } from 'socket.io';
import { CONTRACTS, ABIS } from '../config/contracts';

export class EventIndexer {
  private provider: ethers.providers.JsonRpcProvider;
  private factory: ethers.Contract;
  private tokenContracts: Map<string, ethers.Contract> = new Map();

  constructor(private io: Server) {
    this.provider = new ethers.providers.JsonRpcProvider(
      process.env.RPC_URL || 'https://data-seed-prebsc-1-s1.bnbchain.org:8545/'
    );

    this.factory = new ethers.Contract(CONTRACTS.factory, ABIS.factory, this.provider);

    this.startListening();
  }

  private startListening() {
    console.log('Starting event listeners...');

    // Listen for new token creations
    this.factory.on('TokenCreated', (tokenAddress, creator, name, symbol) => {
      console.log(`New token created: ${name} (${symbol}) at ${tokenAddress}`);

      this.io.emit('token_created', {
        address: tokenAddress,
        creator,
        name,
        symbol,
        timestamp: Date.now(),
      });

      // Start listening to this token's events
      this.listenToToken(tokenAddress);
    });

    // Listen to existing tokens
    this.listenToAllTokens();
  }

  private async listenToAllTokens() {
    try {
      const tokens = await this.factory.getAllTokens();
      console.log(`Found ${tokens.length} existing tokens`);

      for (const tokenAddress of tokens) {
        this.listenToToken(tokenAddress);
      }
    } catch (error) {
      console.error('Error fetching existing tokens:', error);
    }
  }

  private listenToToken(tokenAddress: string) {
    if (this.tokenContracts.has(tokenAddress)) {
      return; // Already listening
    }

    const token = new ethers.Contract(tokenAddress, ABIS.token, this.provider);
    this.tokenContracts.set(tokenAddress, token);

    // Buy events
    token.on('TokensPurchased', (buyer, bnbAmount, tokensReceived, bnbToReserve) => {
      const trade = {
        type: 'buy',
        buyer,
        bnbAmount: ethers.utils.formatEther(bnbAmount),
        tokensReceived: ethers.utils.formatEther(tokensReceived),
        timestamp: Date.now(),
      };

      console.log(`Buy event on ${tokenAddress}:`, trade);
      this.io.to(tokenAddress).emit('trade', trade);
    });

    // Sell events
    token.on('TokensSold', (seller, tokensSold, bnbAmount, bnbReturned) => {
      const trade = {
        type: 'sell',
        seller,
        tokensSold: ethers.utils.formatEther(tokensSold),
        bnbReturned: ethers.utils.formatEther(bnbReturned),
        timestamp: Date.now(),
      };

      console.log(`Sell event on ${tokenAddress}:`, trade);
      this.io.to(tokenAddress).emit('trade', trade);
    });

    // Graduation events
    token.on('StatusChanged', (oldStatus, newStatus, timestamp) => {
      if (newStatus === 1) {
        console.log(`Token graduated: ${tokenAddress}`);

        this.io.to(tokenAddress).emit('graduation', {
          timestamp: timestamp.toString(),
        });
      }
    });

    console.log(`Listening to events for token: ${tokenAddress}`);
  }

  cleanup() {
    console.log('Cleaning up event listeners...');
    this.factory.removeAllListeners();

    for (const [address, contract] of this.tokenContracts.entries()) {
      contract.removeAllListeners();
    }

    this.tokenContracts.clear();
  }
}
