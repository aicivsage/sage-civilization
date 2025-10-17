import express from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';
import cors from 'cors';
import dotenv from 'dotenv';
import { PriceService } from './services/priceService';
import { EventIndexer } from './services/eventIndexer';
import { CandlestickService, Timeframe } from './services/candlestickService';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 4000;
const UPDATE_INTERVAL = parseInt(process.env.UPDATE_INTERVAL || '2000');

// Middleware
app.use(cors());
app.use(express.json());

// Create HTTP server
const httpServer = createServer(app);

// Create Socket.io server
const io = new Server(httpServer, {
  cors: {
    origin: '*',
    methods: ['GET', 'POST'],
  },
});

// Services
const priceService = new PriceService();
const eventIndexer = new EventIndexer(io);
const candlestickService = new CandlestickService();

// Subscribed tokens tracker
const subscribedTokens = new Set<string>();

// REST API Endpoints
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: Date.now() });
});

app.get('/api/price/:tokenAddress', async (req, res) => {
  try {
    const { tokenAddress } = req.params;
    const price = await priceService.getPrice(tokenAddress);
    res.json({ price });
  } catch (error) {
    console.error('Error fetching price:', error);
    res.status(500).json({ error: 'Failed to fetch price' });
  }
});

app.get('/api/token/:tokenAddress', async (req, res) => {
  try {
    const { tokenAddress } = req.params;
    const data = await priceService.getFullData(tokenAddress);
    res.json(data);
  } catch (error) {
    console.error('Error fetching token data:', error);
    res.status(500).json({ error: 'Failed to fetch token data' });
  }
});

app.get('/api/tokens', async (req, res) => {
  try {
    const tokens = await priceService.getActiveTokens();
    res.json({ tokens });
  } catch (error) {
    console.error('Error fetching tokens:', error);
    res.status(500).json({ error: 'Failed to fetch tokens' });
  }
});

app.get('/api/quote/buy/:tokenAddress/:bnbAmount', async (req, res) => {
  try {
    const { tokenAddress, bnbAmount } = req.params;
    const quote = await priceService.getBuyQuote(tokenAddress, bnbAmount);
    res.json(quote);
  } catch (error) {
    console.error('Error getting buy quote:', error);
    res.status(500).json({ error: 'Failed to get buy quote' });
  }
});

app.get('/api/quote/sell/:tokenAddress/:tokenAmount', async (req, res) => {
  try {
    const { tokenAddress, tokenAmount } = req.params;
    const quote = await priceService.getSellQuote(tokenAddress, tokenAmount);
    res.json(quote);
  } catch (error) {
    console.error('Error getting sell quote:', error);
    res.status(500).json({ error: 'Failed to get sell quote' });
  }
});

app.get('/api/candles/:tokenAddress/:timeframe', async (req, res) => {
  try {
    const { tokenAddress, timeframe } = req.params;
    const limit = parseInt(req.query.limit as string) || 100;

    if (!['1h', '4h', '1d', '1w'].includes(timeframe)) {
      return res.status(400).json({ error: 'Invalid timeframe. Use: 1h, 4h, 1d, 1w' });
    }

    const candles = candlestickService.getCandlesticks(tokenAddress, timeframe as Timeframe, limit);
    res.json({ candles, timeframe, count: candles.length });
  } catch (error) {
    console.error('Error getting candlesticks:', error);
    res.status(500).json({ error: 'Failed to get candlesticks' });
  }
});

// WebSocket Connection Handling
io.on('connection', (socket) => {
  console.log(`Client connected: ${socket.id}`);

  socket.on('subscribe', (tokenAddress: string) => {
    console.log(`Client ${socket.id} subscribed to ${tokenAddress}`);
    socket.join(tokenAddress);
    subscribedTokens.add(tokenAddress);

    // Send initial data immediately
    priceService.getFullData(tokenAddress).then((data) => {
      if (data) {
        socket.emit('price_update', data);
      }
    });
  });

  socket.on('unsubscribe', (tokenAddress: string) => {
    console.log(`Client ${socket.id} unsubscribed from ${tokenAddress}`);
    socket.leave(tokenAddress);

    // Check if any other clients are still subscribed
    const room = io.sockets.adapter.rooms.get(tokenAddress);
    if (!room || room.size === 0) {
      subscribedTokens.delete(tokenAddress);
    }
  });

  socket.on('disconnect', () => {
    console.log(`Client disconnected: ${socket.id}`);
  });
});

// Price Update Loop
const updatePrices = async () => {
  if (subscribedTokens.size === 0) {
    return;
  }

  for (const tokenAddress of subscribedTokens) {
    try {
      const data = await priceService.getFullData(tokenAddress);
      if (data) {
        // Add price point to candlestick service
        candlestickService.addPricePoint(tokenAddress, data.price, '0');

        // Emit price update with candlestick data
        io.to(tokenAddress).emit('price_update', {
          ...data,
          // Include latest candle for real-time chart updates
          latestCandle: candlestickService.getCandlesticks(tokenAddress, '1h', 1)[0] || null,
        });
      }
    } catch (error) {
      console.error(`Error updating price for ${tokenAddress}:`, error);
    }
  }
};

// Start price update interval
setInterval(updatePrices, UPDATE_INTERVAL);

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully...');
  eventIndexer.cleanup();
  httpServer.close(() => {
    console.log('Server closed');
    process.exit(0);
  });
});

process.on('SIGINT', () => {
  console.log('SIGINT received, shutting down gracefully...');
  eventIndexer.cleanup();
  httpServer.close(() => {
    console.log('Server closed');
    process.exit(0);
  });
});

// Start server
httpServer.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
  console.log(`📡 WebSocket server ready`);
  console.log(`⏱️  Update interval: ${UPDATE_INTERVAL}ms`);
  console.log(`🔗 RPC URL: ${process.env.RPC_URL || 'default'}`);
});
