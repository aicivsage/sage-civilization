import React, { useState } from 'react';
import { ArrowUpIcon, ArrowDownIcon } from '@heroicons/react/24/outline';
import { formatBNB, formatTokenAmount, isValidBNBAmount } from '../utils/formatters';
import toast from 'react-hot-toast';

interface TradingPanelProps {
  tokenAddress: string | null;
  tokenSymbol: string;
  tokenBalance: string;
  bnbBalance: string;
  currentPrice: string;
  isConnected: boolean;
  onBuy: (amount: string) => Promise<void>;
  onSell: (amount: string) => Promise<void>;
  onConnect: () => void;
}

type TradeType = 'buy' | 'sell';

export const TradingPanel: React.FC<TradingPanelProps> = ({
  tokenAddress,
  tokenSymbol,
  tokenBalance,
  bnbBalance,
  currentPrice,
  isConnected,
  onBuy,
  onSell,
  onConnect,
}) => {
  const [tradeType, setTradeType] = useState<TradeType>('buy');
  const [amount, setAmount] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [txStage, setTxStage] = useState<string>('');

  const isBuy = tradeType === 'buy';

  // Calculate estimated output
  const estimatedOutput = () => {
    if (!amount || !currentPrice) return '0';

    const amountNum = parseFloat(amount);
    const priceNum = parseFloat(currentPrice);

    if (isNaN(amountNum) || isNaN(priceNum)) return '0';

    // CRITICAL FIX: Prevent division by zero (causes "Infinity TOKEN" bug)
    if (priceNum === 0) return '0';

    if (isBuy) {
      // BNB input → token output
      return (amountNum / priceNum).toFixed(2);
    } else {
      // Token input → BNB output
      return (amountNum * priceNum).toFixed(6);
    }
  };

  // Handle trade
  const handleTrade = async () => {
    if (!isConnected) {
      onConnect();
      return;
    }

    if (!tokenAddress) {
      toast.error('No token selected');
      return;
    }

    if (!amount || parseFloat(amount) <= 0) {
      toast.error('Please enter a valid amount');
      return;
    }

    if (isBuy && !isValidBNBAmount(amount)) {
      toast.error('Invalid BNB amount. Please enter between 0.001 and 1000 BNB');
      return;
    }

    if (!isBuy && parseFloat(amount) > parseFloat(tokenBalance)) {
      const shortage = (parseFloat(amount) - parseFloat(tokenBalance)).toFixed(2);
      toast.error(`Insufficient token balance. You need ${shortage} more ${tokenSymbol}`);
      return;
    }

    if (isBuy && parseFloat(amount) > parseFloat(bnbBalance)) {
      const shortfall = (parseFloat(amount) - parseFloat(bnbBalance)).toFixed(4);
      toast.error(`Insufficient BNB balance. You need ${shortfall} more BNB`);
      return;
    }

    setIsLoading(true);
    setTxStage('Preparing transaction...');

    try {
      if (isBuy) {
        toast.loading('Waiting for wallet confirmation...', { id: 'trade' });
        setTxStage('Awaiting wallet approval...');

        await onBuy(amount);

        toast.loading('Transaction submitted, confirming...', { id: 'trade' });
        setTxStage('Confirming on blockchain...');

        // Success
        toast.success(`Successfully bought ${estimatedOutput()} ${tokenSymbol} for ${amount} BNB!`, { id: 'trade' });
      } else {
        toast.loading('Waiting for wallet confirmation...', { id: 'trade' });
        setTxStage('Awaiting wallet approval...');

        await onSell(amount);

        toast.loading('Transaction submitted, confirming...', { id: 'trade' });
        setTxStage('Confirming on blockchain...');

        // Success
        toast.success(`Successfully sold ${amount} ${tokenSymbol} for ${estimatedOutput()} BNB!`, { id: 'trade' });
      }
      setAmount('');
    } catch (error: any) {
      console.error('Trade error:', error);

      // Parse blockchain errors for user-friendly messages
      let message = 'Transaction failed';
      if (error.message?.includes('user rejected') || error.message?.includes('User denied')) {
        message = 'Transaction cancelled in wallet';
      } else if (error.code === 'ACTION_REJECTED' || error.code === 4001) {
        message = 'Transaction rejected in wallet';
      } else if (error.message?.includes('insufficient funds')) {
        message = 'Insufficient funds for transaction + gas fees';
      } else if (error.message?.includes('execution reverted')) {
        message = 'Transaction reverted. Check slippage or liquidity';
      } else if (error.message) {
        message = error.message;
      }

      toast.error(message, { id: 'trade' });
    } finally {
      setIsLoading(false);
      setTxStage('');
    }
  };

  // Quick amount buttons
  const quickAmounts = isBuy
    ? ['0.01', '0.05', '0.1', '0.5']
    : ['25%', '50%', '75%', '100%'];

  const handleQuickAmount = (value: string) => {
    if (isBuy) {
      setAmount(value);
    } else {
      // Calculate percentage of token balance
      const percentage = parseInt(value) / 100;
      const tokenAmount = (parseFloat(tokenBalance) * percentage).toFixed(2);
      setAmount(tokenAmount);
    }
  };

  return (
    <div className="bg-dark-card rounded-xl p-6">
      {/* Trade Type Tabs */}
      <div className="flex gap-2 mb-6">
        <button
          onClick={() => setTradeType('buy')}
          className={`flex-1 py-3 rounded-lg font-semibold transition-all ${
            isBuy
              ? 'bg-gradient-to-r from-green-500 to-green-600 text-white'
              : 'bg-dark-hover text-gray-400'
          }`}
        >
          <div className="flex items-center justify-center gap-2">
            <ArrowUpIcon className="w-5 h-5" />
            <span>Buy</span>
          </div>
        </button>

        <button
          onClick={() => setTradeType('sell')}
          className={`flex-1 py-3 rounded-lg font-semibold transition-all ${
            !isBuy
              ? 'bg-gradient-to-r from-red-500 to-red-600 text-white'
              : 'bg-dark-hover text-gray-400'
          }`}
        >
          <div className="flex items-center justify-center gap-2">
            <ArrowDownIcon className="w-5 h-5" />
            <span>Sell</span>
          </div>
        </button>
      </div>

      {/* Amount Input */}
      <div className="mb-4">
        <div className="flex items-center justify-between mb-2">
          <label className="text-sm text-gray-400">
            {isBuy ? 'You Pay' : 'You Sell'}
          </label>
          <span className="text-xs text-gray-500">
            Balance: {isBuy ? formatBNB(bnbBalance, 4) : formatTokenAmount(tokenBalance, 18, 2)}{' '}
            {isBuy ? 'BNB' : tokenSymbol}
          </span>
        </div>

        <div className="relative">
          <input
            type="number"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            placeholder="0.0"
            className="w-full px-4 py-3 bg-dark-bg text-white rounded-lg text-lg
                     focus:outline-none focus:ring-2 focus:ring-primary"
            step={isBuy ? '0.01' : '1'}
            min="0"
          />
          <div className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 font-semibold">
            {isBuy ? 'BNB' : tokenSymbol}
          </div>
        </div>

        {/* Quick Amount Buttons */}
        <div className="grid grid-cols-4 gap-2 mt-2">
          {quickAmounts.map((value) => (
            <button
              key={value}
              onClick={() => handleQuickAmount(value)}
              className="px-2 py-1 text-xs bg-dark-hover text-gray-300 rounded hover:bg-dark-bg
                       transition-colors"
            >
              {value}
            </button>
          ))}
        </div>
      </div>

      {/* Estimated Output */}
      <div className="mb-6 p-4 bg-dark-bg rounded-lg">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-gray-400">
            {isBuy ? 'You Receive' : 'You Receive'}
          </span>
          <span className="text-lg font-semibold text-white">
            {estimatedOutput()} {isBuy ? tokenSymbol : 'BNB'}
          </span>
        </div>

        {currentPrice && (
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Price per token</span>
            <span>{parseFloat(currentPrice).toExponential(4)} BNB</span>
          </div>
        )}
      </div>

      {/* Trade Button */}
      <button
        onClick={handleTrade}
        disabled={isLoading || !tokenAddress}
        className={`w-full py-4 rounded-xl font-bold text-lg transition-all transform
                   active:scale-95 touch-manipulation ${
                     isBuy
                       ? 'bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700'
                       : 'bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700'
                   } text-white disabled:opacity-50 disabled:cursor-not-allowed`}
      >
        {isLoading ? (
          <div className="flex items-center justify-center gap-2">
            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
            <span>{txStage || 'Processing...'}</span>
          </div>
        ) : !isConnected ? (
          'Connect Wallet'
        ) : !tokenAddress ? (
          'Select a Token'
        ) : (
          `${isBuy ? 'Buy' : 'Sell'} ${tokenSymbol}`
        )}
      </button>

      {/* Info */}
      <div className="mt-4 p-3 bg-blue-500/10 border border-blue-500/20 rounded-lg">
        <p className="text-xs text-blue-400">
          {isBuy
            ? 'Buying tokens will increase the price based on the bonding curve'
            : 'Selling tokens will decrease the price based on the bonding curve'}
        </p>
      </div>
    </div>
  );
};
