import React, { useEffect, useRef, useState } from 'react';
import { createChart, IChartApi, ISeriesApi, LineStyle, CandlestickData } from 'lightweight-charts';
import { PriceData } from '../hooks/useWebSocket';
import axios from 'axios';

interface PriceChartProps {
  tokenAddress: string;
  priceData: PriceData | null;
  className?: string;
}

type Timeframe = '1h' | '4h' | '1d' | '1w';

export const PriceChart: React.FC<PriceChartProps> = ({ tokenAddress, priceData, className = '' }) => {
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const candleSeriesRef = useRef<ISeriesApi<'Candlestick'> | null>(null);
  const [timeframe, setTimeframe] = useState<Timeframe>('1h');
  const [candleData, setCandleData] = useState<CandlestickData[]>([]);
  const [loading, setLoading] = useState(false);

  // Initialize chart
  useEffect(() => {
    if (!chartContainerRef.current) return;

    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: 400,
      layout: {
        background: { color: '#2B2B43' },
        textColor: '#d1d4dc',
      },
      grid: {
        vertLines: {
          color: '#363c4e',
          style: LineStyle.Dotted,
        },
        horzLines: {
          color: '#363c4e',
          style: LineStyle.Dotted,
        },
      },
      rightPriceScale: {
        borderColor: '#485c7b',
      },
      timeScale: {
        borderColor: '#485c7b',
        timeVisible: true,
        secondsVisible: false,
      },
      crosshair: {
        mode: 1, // CrosshairMode.Normal
        vertLine: {
          width: 1,
          color: '#758696',
          style: 3, // LineStyle.Dashed
          labelBackgroundColor: '#4c5a67',
        },
        horzLine: {
          width: 1,
          color: '#758696',
          style: 3, // LineStyle.Dashed
          labelBackgroundColor: '#4c5a67',
        },
      },
    });

    const candleSeries = chart.addCandlestickSeries({
      upColor: '#26a69a',
      downColor: '#ef5350',
      borderVisible: false,
      wickUpColor: '#26a69a',
      wickDownColor: '#ef5350',
      priceFormat: {
        type: 'price',
        precision: 8,
        minMove: 0.00000001,
      },
      lastValueVisible: true,
      priceLineVisible: true,
    });

    chartRef.current = chart;
    candleSeriesRef.current = candleSeries;

    // Handle resize
    const handleResize = () => {
      if (chartContainerRef.current) {
        chart.applyOptions({
          width: chartContainerRef.current.clientWidth,
        });
      }
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      chart.remove();
    };
  }, []);

  // Fetch candlestick data when timeframe changes
  useEffect(() => {
    const fetchCandleData = async () => {
      if (!tokenAddress) return;

      setLoading(true);
      try {
        const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:4000';
        const response = await axios.get(`${API_URL}/api/candles/${tokenAddress}/${timeframe}?limit=100`);

        if (response.data && response.data.candles) {
          const candles = response.data.candles.map((c: any) => ({
            time: Math.floor(c.timestamp / 1000) as any,
            open: parseFloat(c.open),
            high: parseFloat(c.high),
            low: parseFloat(c.low),
            close: parseFloat(c.close),
          }));

          setCandleData(candles as any);

          if (candleSeriesRef.current && candles.length > 0) {
            candleSeriesRef.current.setData(candles as any);
            chartRef.current?.timeScale().fitContent();
          }
        }
      } catch (error) {
        console.error('Error fetching candle data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCandleData();
    // Refresh every minute
    const interval = setInterval(fetchCandleData, 60000);

    return () => clearInterval(interval);
  }, [tokenAddress, timeframe]);

  // Update with latest price data
  useEffect(() => {
    if (!priceData || !candleSeriesRef.current || candleData.length === 0) return;

    const latestCandle = candleData[candleData.length - 1];
    const currentTime = Math.floor(Date.now() / 1000);
    const price = parseFloat(priceData.price);

    // Determine if we should update the current candle or create a new one
    const intervalMs = {
      '1h': 3600,
      '4h': 14400,
      '1d': 86400,
      '1w': 604800,
    };

    const interval = intervalMs[timeframe];
    const currentIntervalStart = Math.floor(currentTime / interval) * interval;

    if (latestCandle && latestCandle.time === currentIntervalStart) {
      // Update existing candle
      const updatedCandle = {
        ...latestCandle,
        high: Math.max(latestCandle.high, price),
        low: Math.min(latestCandle.low, price),
        close: price,
      };

      const newCandleData = [...candleData.slice(0, -1), updatedCandle];
      setCandleData(newCandleData as any);
      candleSeriesRef.current.setData(newCandleData as any);
    } else if (!latestCandle || currentIntervalStart > latestCandle.time) {
      // Create new candle
      const newCandle = {
        time: currentIntervalStart as any,
        open: price,
        high: price,
        low: price,
        close: price,
      };

      const newCandleData = [...candleData, newCandle];
      setCandleData(newCandleData as any);
      candleSeriesRef.current.setData(newCandleData as any);
    }
  }, [priceData, timeframe, candleData]);

  // Calculate price change
  const priceChange = candleData.length >= 2
    ? ((candleData[candleData.length - 1].close - candleData[0].open) / candleData[0].open) * 100
    : 0;

  const timeframeButtons: Array<{ label: string; value: Timeframe }> = [
    { label: '1H', value: '1h' },
    { label: '4H', value: '4h' },
    { label: '1D', value: '1d' },
    { label: '1W', value: '1w' },
  ];

  return (
    <div className={`bg-dark-card rounded-xl p-4 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-white">Price Chart</h3>
          {priceData && (
            <div className="flex items-center gap-3 mt-1">
              <span className="text-2xl font-bold text-white">
                {parseFloat(priceData.price).toExponential(4)} BNB
              </span>
              <span
                className={`text-sm font-semibold ${
                  priceChange >= 0 ? 'text-green-500' : 'text-red-500'
                }`}
              >
                {priceChange >= 0 ? '+' : ''}
                {priceChange.toFixed(2)}%
              </span>
            </div>
          )}
        </div>

        <div className="flex gap-2">
          {timeframeButtons.map((btn) => (
            <button
              key={btn.value}
              onClick={() => setTimeframe(btn.value)}
              className={`px-3 py-1 text-sm transition-colors rounded ${
                timeframe === btn.value
                  ? 'text-white bg-primary'
                  : 'text-gray-400 hover:text-white hover:bg-gray-700'
              }`}
              disabled={loading}
            >
              {btn.label}
            </button>
          ))}
        </div>
      </div>

      {/* Chart Container */}
      <div className="relative">
        {loading && (
          <div className="absolute inset-0 flex items-center justify-center bg-dark-card/50 z-10 rounded">
            <div className="text-white">Loading {timeframe} candlesticks...</div>
          </div>
        )}
        <div ref={chartContainerRef} className="w-full" />
      </div>

      {/* Stats */}
      {priceData && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4 pt-4 border-t border-gray-700">
          <div>
            <div className="text-xs text-gray-400 mb-1">BNB Reserves</div>
            <div className="text-sm font-semibold text-white">
              {parseFloat(priceData.bnbReserves).toFixed(4)} BNB
            </div>
          </div>
          <div>
            <div className="text-xs text-gray-400 mb-1">Status</div>
            <div className="text-sm font-semibold text-white">
              <span className={`inline-flex items-center px-2 py-1 rounded text-xs ${
                priceData.status === 0
                  ? 'bg-green-500/20 text-green-500'
                  : 'bg-blue-500/20 text-blue-500'
              }`}>
                {priceData.status === 0 ? 'Active' : 'Graduated'}
              </span>
            </div>
          </div>
          <div>
            <div className="text-xs text-gray-400 mb-1">Progress</div>
            <div className="text-sm font-semibold text-white">
              {((parseFloat(priceData.bnbReserves) / 50) * 100).toFixed(1)}%
            </div>
          </div>
          <div>
            <div className="text-xs text-gray-400 mb-1">Candles</div>
            <div className="text-sm font-semibold text-white">
              {candleData.length} × {timeframe}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
