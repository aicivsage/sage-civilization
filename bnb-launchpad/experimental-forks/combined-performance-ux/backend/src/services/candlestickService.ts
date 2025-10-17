import { ethers } from 'ethers';

export interface Candlestick {
  timestamp: number;
  open: string;
  high: string;
  low: string;
  close: string;
  volume: string;
}

export type Timeframe = '1h' | '4h' | '1d' | '1w';

export class CandlestickService {
  private priceHistory: Map<string, Array<{ price: string; timestamp: number; volume: string }>> = new Map();
  private candlesticks: Map<string, Map<Timeframe, Candlestick[]>> = new Map();

  constructor() {
    // Cleanup old data every hour
    setInterval(() => this.cleanup(), 3600000);
  }

  // Add a price point
  addPricePoint(tokenAddress: string, price: string, volume: string = '0') {
    if (!this.priceHistory.has(tokenAddress)) {
      this.priceHistory.set(tokenAddress, []);
    }

    const history = this.priceHistory.get(tokenAddress)!;
    history.push({
      price,
      timestamp: Date.now(),
      volume,
    });

    // Keep only last 7 days of raw data
    const sevenDaysAgo = Date.now() - 7 * 24 * 60 * 60 * 1000;
    const filtered = history.filter((p) => p.timestamp >= sevenDaysAgo);
    this.priceHistory.set(tokenAddress, filtered);

    // Update candlesticks
    this.updateCandlesticks(tokenAddress);
  }

  // Get candlesticks for a specific timeframe
  getCandlesticks(tokenAddress: string, timeframe: Timeframe, limit: number = 100): Candlestick[] {
    if (!this.candlesticks.has(tokenAddress)) {
      return [];
    }

    const tokenCandles = this.candlesticks.get(tokenAddress)!;
    if (!tokenCandles.has(timeframe)) {
      return [];
    }

    const candles = tokenCandles.get(timeframe)!;
    return candles.slice(-limit);
  }

  private updateCandlesticks(tokenAddress: string) {
    const history = this.priceHistory.get(tokenAddress);
    if (!history || history.length === 0) {
      return;
    }

    if (!this.candlesticks.has(tokenAddress)) {
      this.candlesticks.set(tokenAddress, new Map());
    }

    const tokenCandles = this.candlesticks.get(tokenAddress)!;

    // Generate candlesticks for each timeframe
    this.generateCandlesForTimeframe(tokenAddress, history, '1h', 3600000, tokenCandles);
    this.generateCandlesForTimeframe(tokenAddress, history, '4h', 14400000, tokenCandles);
    this.generateCandlesForTimeframe(tokenAddress, history, '1d', 86400000, tokenCandles);
    this.generateCandlesForTimeframe(tokenAddress, history, '1w', 604800000, tokenCandles);
  }

  private generateCandlesForTimeframe(
    tokenAddress: string,
    history: Array<{ price: string; timestamp: number; volume: string }>,
    timeframe: Timeframe,
    intervalMs: number,
    tokenCandles: Map<Timeframe, Candlestick[]>
  ) {
    // Get existing candles or create new array
    const existingCandles = tokenCandles.get(timeframe) || [];

    // Find the start of the current interval
    const now = Date.now();
    const currentIntervalStart = Math.floor(now / intervalMs) * intervalMs;

    // Group price points by interval
    const intervals = new Map<number, Array<{ price: string; volume: string }>>();

    for (const point of history) {
      const intervalStart = Math.floor(point.timestamp / intervalMs) * intervalMs;
      if (!intervals.has(intervalStart)) {
        intervals.set(intervalStart, []);
      }
      intervals.get(intervalStart)!.push({
        price: point.price,
        volume: point.volume,
      });
    }

    // Convert intervals to candlesticks
    const newCandles: Candlestick[] = [];

    for (const [intervalStart, points] of intervals.entries()) {
      if (points.length === 0) continue;

      const prices = points.map((p) => parseFloat(p.price));
      const volumes = points.map((p) => parseFloat(p.volume));

      const candle: Candlestick = {
        timestamp: intervalStart,
        open: points[0].price,
        high: Math.max(...prices).toString(),
        low: Math.min(...prices).toString(),
        close: points[points.length - 1].price,
        volume: volumes.reduce((a, b) => a + b, 0).toString(),
      };

      // Check if we need to update an existing candle or add a new one
      const existingIndex = existingCandles.findIndex((c) => c.timestamp === intervalStart);
      if (existingIndex >= 0) {
        // Update existing candle
        const existing = existingCandles[existingIndex];
        candle.open = existing.open; // Keep original open
        candle.high = Math.max(parseFloat(existing.high), parseFloat(candle.high)).toString();
        candle.low = Math.min(parseFloat(existing.low), parseFloat(candle.low)).toString();
        // close is already the latest
        candle.volume = (parseFloat(existing.volume) + parseFloat(candle.volume)).toString();
        existingCandles[existingIndex] = candle;
      } else {
        newCandles.push(candle);
      }
    }

    // Merge and sort
    const allCandles = [...existingCandles, ...newCandles].sort((a, b) => a.timestamp - b.timestamp);

    // Keep only reasonable amount of history
    const maxCandles = {
      '1h': 168, // 1 week
      '4h': 180, // 30 days
      '1d': 90, // 90 days
      '1w': 52, // 1 year
    };

    const limit = maxCandles[timeframe] || 100;
    const trimmed = allCandles.slice(-limit);

    tokenCandles.set(timeframe, trimmed);
  }

  private cleanup() {
    // Remove tokens with no recent activity (>24 hours)
    const oneDayAgo = Date.now() - 24 * 60 * 60 * 1000;

    for (const [tokenAddress, history] of this.priceHistory.entries()) {
      if (history.length === 0 || history[history.length - 1].timestamp < oneDayAgo) {
        this.priceHistory.delete(tokenAddress);
        this.candlesticks.delete(tokenAddress);
      }
    }
  }
}
