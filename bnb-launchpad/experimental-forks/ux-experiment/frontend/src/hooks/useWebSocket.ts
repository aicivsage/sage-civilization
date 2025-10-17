import { useEffect, useState, useCallback } from 'react';
import { io, Socket } from 'socket.io-client';
import { WS_CONFIG } from '../utils/constants';

export interface PriceData {
  address: string;
  name: string;
  symbol: string;
  price: string;
  bnbReserves: string;
  status: number;
  graduationTimestamp: string;
  timestamp: number;
}

export interface TradeEvent {
  type: 'buy' | 'sell';
  buyer?: string;
  seller?: string;
  bnbAmount?: string;
  tokensReceived?: string;
  tokensSold?: string;
  bnbReturned?: string;
  timestamp: number;
}

export interface TokenCreatedEvent {
  address: string;
  creator: string;
  name: string;
  symbol: string;
  timestamp: number;
}

export const useWebSocket = (tokenAddress: string | null) => {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [connected, setConnected] = useState(false);
  const [priceData, setPriceData] = useState<PriceData | null>(null);
  const [trades, setTrades] = useState<TradeEvent[]>([]);
  const [newTokens, setNewTokens] = useState<TokenCreatedEvent[]>([]);
  const [reconnectAttempts, setReconnectAttempts] = useState(0);

  // Initialize socket connection
  useEffect(() => {
    const newSocket = io(WS_CONFIG.URL, {
      reconnection: true,
      reconnectionAttempts: WS_CONFIG.RECONNECTION_ATTEMPTS,
      reconnectionDelay: WS_CONFIG.RECONNECTION_DELAY,
    });

    newSocket.on('connect', () => {
      setConnected(true);
      setReconnectAttempts(0);
      console.log('WebSocket connected');
    });

    newSocket.on('disconnect', () => {
      setConnected(false);
      console.log('WebSocket disconnected');
    });

    newSocket.on('reconnect_attempt', (attempt) => {
      setReconnectAttempts(attempt);
      console.log(`Reconnection attempt ${attempt}`);
    });

    newSocket.on('connect_error', (error) => {
      console.error('WebSocket connection error:', error);
    });

    setSocket(newSocket);

    return () => {
      newSocket.close();
    };
  }, []);

  // Subscribe to token updates
  useEffect(() => {
    if (!socket || !tokenAddress) return;

    console.log(`Subscribing to token: ${tokenAddress}`);
    socket.emit('subscribe', tokenAddress);

    socket.on('price_update', (data: PriceData) => {
      setPriceData(data);
    });

    socket.on('trade', (trade: TradeEvent) => {
      setTrades(prev => [trade, ...prev].slice(0, 100));
    });

    socket.on('graduation', (data: { timestamp: string }) => {
      console.log('Token graduated!', data);
      // Update price data to reflect graduation
      setPriceData(prev => prev ? { ...prev, status: 1 } : null);
    });

    return () => {
      socket.off('price_update');
      socket.off('trade');
      socket.off('graduation');
      socket.emit('unsubscribe', tokenAddress);
    };
  }, [socket, tokenAddress]);

  // Listen for new tokens created
  useEffect(() => {
    if (!socket) return;

    socket.on('token_created', (token: TokenCreatedEvent) => {
      setNewTokens(prev => [token, ...prev].slice(0, 50));
    });

    return () => {
      socket.off('token_created');
    };
  }, [socket]);

  const clearTrades = useCallback(() => {
    setTrades([]);
  }, []);

  const clearNewTokens = useCallback(() => {
    setNewTokens([]);
  }, []);

  return {
    socket,
    connected,
    reconnectAttempts,
    priceData,
    trades,
    newTokens,
    clearTrades,
    clearNewTokens,
  };
};
