# Enhanced UX Fork - Detailed Implementation Plan

**Status**: READY TO BUILD
**Estimated Time**: 40-60 hours
**Risk Level**: LOW (frontend only)

---

## Phase 1: Project Setup (2 hours)

### 1.1 Initialize React Project

```bash
cd experimental-forks/enhanced-ux
npx create-react-app frontend-v2 --template typescript
cd frontend-v2
```

### 1.2 Install Dependencies

```bash
# Core
npm install ethers@5.7.2
npm install socket.io-client@4.5.4

# Charts
npm install lightweight-charts@4.0.0
npm install recharts@2.5.0

# Wallet
npm install @walletconnect/web3-provider@1.8.0
npm install @web3-react/core@8.2.0
npm install @web3-react/injected-connector@6.0.7
npm install @web3-react/walletconnect-connector@6.2.13

# UI
npm install @headlessui/react@1.7.17
npm install @heroicons/react@2.0.18
npm install framer-motion@10.16.4

# Utils
npm install date-fns@2.30.0
npm install lodash@4.17.21
npm install react-hot-toast@2.4.1

# Dev
npm install -D @types/lodash
npm install -D tailwindcss@3.3.0
npm install -D autoprefixer@10.4.16
npm install -D postcss@8.4.31
```

### 1.3 Configure Tailwind

```bash
npx tailwindcss init -p
```

**tailwind.config.js**:
```javascript
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#667eea',
        secondary: '#764ba2',
      }
    },
  },
  plugins: [],
}
```

---

## Phase 2: WebSocket Backend (8 hours)

### 2.1 Initialize Backend

```bash
cd ../backend
npm init -y
npm install express@4.18.2
npm install socket.io@4.5.4
npm install ethers@5.7.2
npm install cors@2.8.5
npm install dotenv@16.3.1

npm install -D @types/express
npm install -D @types/node
npm install -D ts-node@10.9.1
npm install -D typescript@5.2.2
npm install -D nodemon@3.0.1
```

### 2.2 Backend Structure

```
backend/
├── src/
│   ├── server.ts (Express + Socket.io setup)
│   ├── services/
│   │   ├── blockchain.ts (RPC polling)
│   │   ├── priceService.ts (Price calculations)
│   │   └── eventIndexer.ts (Event listening)
│   ├── config/
│   │   └── contracts.ts (ABIs, addresses)
│   └── types/
│       └── index.ts (TypeScript types)
├── package.json
├── tsconfig.json
└── .env
```

### 2.3 Core Backend Files

**src/server.ts**:
```typescript
import express from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';
import cors from 'cors';
import { PriceService } from './services/priceService';
import { EventIndexer } from './services/eventIndexer';

const app = express();
app.use(cors());

const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: { origin: '*' }
});

const priceService = new PriceService();
const eventIndexer = new EventIndexer(io);

// REST endpoints
app.get('/api/price/:tokenAddress', async (req, res) => {
  const price = await priceService.getPrice(req.params.tokenAddress);
  res.json({ price });
});

// WebSocket
io.on('connection', (socket) => {
  console.log('Client connected:', socket.id);

  socket.on('subscribe', (tokenAddress) => {
    socket.join(tokenAddress);
    console.log(`Client ${socket.id} subscribed to ${tokenAddress}`);
  });

  socket.on('disconnect', () => {
    console.log('Client disconnected:', socket.id);
  });
});

// Price updates every 2 seconds
setInterval(async () => {
  const tokens = await priceService.getActiveTokens();
  for (const token of tokens) {
    const data = await priceService.getFullData(token);
    io.to(token).emit('price_update', data);
  }
}, 2000);

httpServer.listen(4000, () => {
  console.log('Server running on port 4000');
});
```

**src/services/priceService.ts**:
```typescript
import { ethers } from 'ethers';
import { CONTRACTS, ABIS } from '../config/contracts';

export class PriceService {
  private provider: ethers.providers.JsonRpcProvider;

  constructor() {
    this.provider = new ethers.providers.JsonRpcProvider(
      process.env.RPC_URL || 'https://data-seed-prebsc-1-s1.bnbchain.org:8545/'
    );
  }

  async getPrice(tokenAddress: string): Promise<string> {
    const contract = new ethers.Contract(tokenAddress, ABIS.token, this.provider);

    const [bnbReserves, totalSupply] = await Promise.all([
      contract.bnbReserves(),
      contract.totalSupply()
    ]);

    const VIRTUAL_BNB = ethers.utils.parseEther('30');
    const K = ethers.utils.parseEther('32190005730');

    const currentBnbReserves = bnbReserves.add(VIRTUAL_BNB);
    const currentTokenReserves = K.div(currentBnbReserves);
    const price = currentBnbReserves.div(currentTokenReserves);

    return ethers.utils.formatEther(price);
  }

  async getFullData(tokenAddress: string) {
    const contract = new ethers.Contract(tokenAddress, ABIS.token, this.provider);

    const [name, symbol, bnbReserves, status, graduationTimestamp] = await Promise.all([
      contract.name(),
      contract.symbol(),
      contract.bnbReserves(),
      contract.status(),
      contract.graduationTimestamp()
    ]);

    const price = await this.getPrice(tokenAddress);

    return {
      address: tokenAddress,
      name,
      symbol,
      price,
      bnbReserves: ethers.utils.formatEther(bnbReserves),
      status,
      graduationTimestamp: graduationTimestamp.toString(),
      timestamp: Date.now()
    };
  }

  async getActiveTokens(): Promise<string[]> {
    const factory = new ethers.Contract(
      CONTRACTS.factory,
      ABIS.factory,
      this.provider
    );

    return await factory.getAllTokens();
  }
}
```

**src/services/eventIndexer.ts**:
```typescript
import { ethers } from 'ethers';
import { Server } from 'socket.io';
import { CONTRACTS, ABIS } from '../config/contracts';

export class EventIndexer {
  private provider: ethers.providers.JsonRpcProvider;
  private factory: ethers.Contract;

  constructor(private io: Server) {
    this.provider = new ethers.providers.JsonRpcProvider(
      process.env.RPC_URL || 'https://data-seed-prebsc-1-s1.bnbchain.org:8545/'
    );

    this.factory = new ethers.Contract(
      CONTRACTS.factory,
      ABIS.factory,
      this.provider
    );

    this.startListening();
  }

  private startListening() {
    // Listen for new tokens
    this.factory.on('TokenCreated', (tokenAddress, creator, name, symbol) => {
      this.io.emit('token_created', {
        address: tokenAddress,
        creator,
        name,
        symbol,
        timestamp: Date.now()
      });
    });

    // Listen for all tokens
    this.listenToAllTokens();
  }

  private async listenToAllTokens() {
    const tokens = await this.factory.getAllTokens();

    for (const tokenAddress of tokens) {
      const token = new ethers.Contract(tokenAddress, ABIS.token, this.provider);

      // Buy events
      token.on('TokensPurchased', (buyer, bnbAmount, tokensReceived, bnbToReserve) => {
        this.io.to(tokenAddress).emit('trade', {
          type: 'buy',
          buyer,
          bnbAmount: ethers.utils.formatEther(bnbAmount),
          tokensReceived: ethers.utils.formatEther(tokensReceived),
          timestamp: Date.now()
        });
      });

      // Sell events
      token.on('TokensSold', (seller, tokensSold, bnbAmount, bnbReturned) => {
        this.io.to(tokenAddress).emit('trade', {
          type: 'sell',
          seller,
          tokensSold: ethers.utils.formatEther(tokensSold),
          bnbReturned: ethers.utils.formatEther(bnbReturned),
          timestamp: Date.now()
        });
      });

      // Graduation
      token.on('StatusChanged', (oldStatus, newStatus, timestamp) => {
        if (newStatus === 1) { // Graduated
          this.io.to(tokenAddress).emit('graduation', {
            timestamp: timestamp.toString()
          });
        }
      });
    }
  }
}
```

---

## Phase 3: Frontend Components (20 hours)

### 3.1 Component Structure

```
src/
├── App.tsx
├── components/
│   ├── Layout/
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx (mobile menu)
│   │   └── Footer.tsx
│   ├── Wallet/
│   │   ├── WalletConnector.tsx
│   │   ├── WalletButton.tsx
│   │   └── NetworkSwitcher.tsx
│   ├── Token/
│   │   ├── TokenCreator.tsx
│   │   ├── TokenSelector.tsx
│   │   ├── TokenStats.tsx
│   │   └── TokenInfo.tsx
│   ├── Trading/
│   │   ├── BuyForm.tsx
│   │   ├── SellForm.tsx
│   │   └── TradeHistory.tsx
│   ├── Charts/
│   │   ├── PriceChart.tsx
│   │   ├── VolumeChart.tsx
│   │   ├── DepthChart.tsx
│   │   └── CandlestickChart.tsx
│   └── Notifications/
│       ├── NotificationCenter.tsx
│       └── Toast.tsx
├── hooks/
│   ├── useWebSocket.ts
│   ├── useWallet.ts
│   ├── useContract.ts
│   └── useNotifications.ts
├── services/
│   ├── websocket.ts
│   ├── blockchain.ts
│   └── storage.ts
└── utils/
    ├── formatters.ts
    ├── calculations.ts
    └── constants.ts
```

### 3.2 Key Hooks

**hooks/useWebSocket.ts**:
```typescript
import { useEffect, useState } from 'react';
import { io, Socket } from 'socket.io-client';

export const useWebSocket = (tokenAddress: string | null) => {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [priceData, setPriceData] = useState<any>(null);
  const [trades, setTrades] = useState<any[]>([]);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    const newSocket = io(process.env.REACT_APP_WS_URL || 'http://localhost:4000');

    newSocket.on('connect', () => {
      setConnected(true);
      console.log('WebSocket connected');
    });

    newSocket.on('disconnect', () => {
      setConnected(false);
      console.log('WebSocket disconnected');
    });

    setSocket(newSocket);

    return () => {
      newSocket.close();
    };
  }, []);

  useEffect(() => {
    if (!socket || !tokenAddress) return;

    socket.emit('subscribe', tokenAddress);

    socket.on('price_update', (data) => {
      setPriceData(data);
    });

    socket.on('trade', (trade) => {
      setTrades(prev => [trade, ...prev].slice(0, 50));
    });

    return () => {
      socket.off('price_update');
      socket.off('trade');
    };
  }, [socket, tokenAddress]);

  return { socket, priceData, trades, connected };
};
```

**hooks/useWallet.ts**:
```typescript
import { useWeb3React } from '@web3-react/core';
import { InjectedConnector } from '@web3-react/injected-connector';
import { WalletConnectConnector } from '@web3-react/walletconnect-connector';

const injected = new InjectedConnector({ supportedChainIds: [97, 56] });

const walletConnect = new WalletConnectConnector({
  rpc: { 97: 'https://data-seed-prebsc-1-s1.bnbchain.org:8545/' },
  qrcode: true,
});

export const useWallet = () => {
  const { activate, deactivate, account, library, chainId } = useWeb3React();

  const connectMetaMask = async () => {
    try {
      await activate(injected);
      localStorage.removeItem('walletDisconnected');
    } catch (error) {
      console.error('MetaMask connection error:', error);
    }
  };

  const connectWalletConnect = async () => {
    try {
      await activate(walletConnect);
      localStorage.removeItem('walletDisconnected');
    } catch (error) {
      console.error('WalletConnect error:', error);
    }
  };

  const disconnect = () => {
    deactivate();
    localStorage.setItem('walletDisconnected', 'true');
  };

  return {
    account,
    library,
    chainId,
    connectMetaMask,
    connectWalletConnect,
    disconnect,
    isConnected: !!account
  };
};
```

### 3.3 Main Components

**components/Charts/PriceChart.tsx**:
```typescript
import { useEffect, useRef } from 'react';
import { createChart, IChartApi } from 'lightweight-charts';

interface PriceChartProps {
  data: Array<{ time: number; value: number }>;
}

export const PriceChart: React.FC<PriceChartProps> = ({ data }) => {
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);

  useEffect(() => {
    if (!chartContainerRef.current) return;

    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: 400,
      layout: {
        background: { color: '#1a1b1e' },
        textColor: '#d1d4dc',
      },
      grid: {
        vertLines: { color: '#2B2B43' },
        horzLines: { color: '#2B2B43' },
      },
    });

    const lineSeries = chart.addLineSeries({
      color: '#667eea',
      lineWidth: 2,
    });

    lineSeries.setData(data.map(d => ({
      time: Math.floor(d.time / 1000),
      value: d.value
    })));

    chartRef.current = chart;

    const handleResize = () => {
      chart.applyOptions({
        width: chartContainerRef.current!.clientWidth
      });
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      chart.remove();
    };
  }, [data]);

  return <div ref={chartContainerRef} className="w-full" />;
};
```

---

## Phase 4: Mobile Optimization (8 hours)

### 4.1 Responsive Layout

**App.tsx**:
```typescript
function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const isMobile = useMediaQuery('(max-width: 768px)');

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Mobile Menu */}
      {isMobile && (
        <MobileSidebar
          open={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
        />
      )}

      {/* Desktop Layout */}
      <div className="flex">
        {!isMobile && <Sidebar />}

        <main className="flex-1">
          <Header onMenuClick={() => setSidebarOpen(true)} />

          <div className="p-4 md:p-6 lg:p-8">
            {/* Grid adapts to screen size */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2">
                <TokenCreator />
                <PriceChart />
              </div>

              <div>
                <TradingPanel />
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
```

### 4.2 Touch Optimizations

```typescript
// components/Trading/BuyForm.tsx
<button
  className="w-full py-4 text-lg font-semibold rounded-xl
             bg-gradient-to-r from-green-500 to-green-600
             active:scale-95 transform transition-transform
             touch-manipulation" // Prevents zoom on double-tap
  onClick={handleBuy}
>
  Buy Tokens
</button>
```

### 4.3 PWA Setup

**public/manifest.json**:
```json
{
  "short_name": "BNB Launch",
  "name": "BNB Token Launchpad",
  "icons": [
    {
      "src": "icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ],
  "start_url": ".",
  "display": "standalone",
  "theme_color": "#667eea",
  "background_color": "#1a1b1e"
}
```

**src/service-worker.ts**:
```typescript
// Workbox configuration for offline support
import { precacheAndRoute } from 'workbox-precaching';
import { registerRoute } from 'workbox-routing';
import { CacheFirst, NetworkFirst } from 'workbox-strategies';

precacheAndRoute(self.__WB_MANIFEST);

// Cache API responses
registerRoute(
  ({ url }) => url.pathname.startsWith('/api/'),
  new NetworkFirst({
    cacheName: 'api-cache',
  })
);

// Cache static assets
registerRoute(
  ({ request }) => request.destination === 'image',
  new CacheFirst({
    cacheName: 'images',
  })
);
```

---

## Phase 5: Notifications (4 hours)

### 5.1 Browser Notifications

**services/notifications.ts**:
```typescript
export class NotificationService {
  static async requestPermission() {
    if ('Notification' in window) {
      const permission = await Notification.requestPermission();
      return permission === 'granted';
    }
    return false;
  }

  static notify(title: string, options?: NotificationOptions) {
    if (Notification.permission === 'granted') {
      new Notification(title, {
        icon: '/logo192.png',
        badge: '/badge.png',
        ...options
      });
    }
  }

  static onTransactionSuccess(hash: string, type: 'buy' | 'sell') {
    this.notify(
      `Transaction ${type === 'buy' ? 'Buy' : 'Sell'} Confirmed!`,
      {
        body: `Transaction ${hash.slice(0, 10)}... completed successfully`,
        tag: hash,
      }
    );
  }

  static onGraduation(tokenName: string) {
    this.notify(
      `🎓 ${tokenName} Graduated!`,
      {
        body: `Token has reached 50 BNB and graduated to PancakeSwap`,
        tag: `graduation-${tokenName}`,
      }
    );
  }
}
```

### 5.2 Toast Notifications

```typescript
import toast from 'react-hot-toast';

export const showToast = {
  success: (message: string) => toast.success(message, {
    style: {
      background: '#10b981',
      color: '#fff',
    },
    iconTheme: {
      primary: '#fff',
      secondary: '#10b981',
    },
  }),

  error: (message: string) => toast.error(message, {
    style: {
      background: '#ef4444',
      color: '#fff',
    },
  }),

  loading: (message: string) => toast.loading(message),
};
```

---

## Phase 6: Testing & Deployment (8 hours)

### 6.1 Unit Tests

```typescript
// __tests__/hooks/useWebSocket.test.ts
import { renderHook, waitFor } from '@testing-library/react';
import { useWebSocket } from '../../hooks/useWebSocket';

describe('useWebSocket', () => {
  it('should connect and receive price updates', async () => {
    const { result } = renderHook(() =>
      useWebSocket('0x1234...'));

    await waitFor(() => {
      expect(result.current.connected).toBe(true);
    });

    // Mock price update
    mockSocket.emit('price_update', { price: '0.00000003' });

    await waitFor(() => {
      expect(result.current.priceData).toEqual({ price: '0.00000003' });
    });
  });
});
```

### 6.2 E2E Tests

```typescript
// e2e/trading.spec.ts
import { test, expect } from '@playwright/test';

test('complete buy flow', async ({ page }) => {
  await page.goto('http://localhost:3000');

  // Connect wallet
  await page.click('button:has-text("Connect Wallet")');
  await page.click('button:has-text("MetaMask")');

  // Wait for wallet connection
  await expect(page.locator('text=0x...')).toBeVisible();

  // Enter buy amount
  await page.fill('input[name="buyAmount"]', '0.01');

  // Click buy
  await page.click('button:has-text("Buy Tokens")');

  // Wait for success toast
  await expect(page.locator('text=Transaction Confirmed')).toBeVisible();
});
```

### 6.3 Deployment

**Vercel (Frontend)**:
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend-v2
vercel --prod

# Environment variables
vercel env add REACT_APP_WS_URL production
vercel env add REACT_APP_FACTORY_ADDRESS production
```

**Fly.io (Backend)**:
```toml
# fly.toml
app = "bnb-launchpad-backend"

[build]
  builder = "heroku/buildpacks:20"

[env]
  PORT = "4000"

[[services]]
  internal_port = 4000
  protocol = "tcp"

  [[services.ports]]
    port = 80
    handlers = ["http"]

  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]
```

```bash
# Deploy
fly deploy --config fly.toml
```

---

## Success Criteria

### Must Have
- [ ] Real-time price updates (<2s latency)
- [ ] Mobile responsive (works on iOS/Android)
- [ ] WalletConnect functional
- [ ] Charts render correctly
- [ ] All current features working

### Should Have
- [ ] Browser notifications (>90% delivery)
- [ ] PWA installable
- [ ] Offline support (basic)
- [ ] Lighthouse score >90

### Could Have
- [ ] Dark/light mode toggle
- [ ] Multi-language support
- [ ] Advanced order types

---

## Timeline

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| 1. Setup | 2 hours | None |
| 2. Backend | 8 hours | Phase 1 |
| 3. Frontend | 20 hours | Phase 1, 2 |
| 4. Mobile | 8 hours | Phase 3 |
| 5. Notifications | 4 hours | Phase 3 |
| 6. Testing | 8 hours | All |
| **Total** | **50 hours** | - |

**Calendar Time**: 1-2 weeks with 1 developer

---

## Next Steps

1. ✅ This plan approved
2. ⏳ Execute Phase 1 (setup)
3. ⏳ Execute Phase 2 (backend)
4. ⏳ Execute Phase 3 (frontend)
5. ⏳ Execute Phase 4 (mobile)
6. ⏳ Execute Phase 5 (notifications)
7. ⏳ Execute Phase 6 (testing & deployment)

**Status**: Ready to implement!
