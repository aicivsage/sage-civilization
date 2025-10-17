import React, { useState } from 'react';
import { PlusIcon, RocketLaunchIcon } from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';

interface TokenCreatorProps {
  isConnected: boolean;
  onConnect: () => void;
  onCreate: (name: string, symbol: string) => Promise<void>;
}

export const TokenCreator: React.FC<TokenCreatorProps> = ({
  isConnected,
  onConnect,
  onCreate,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [name, setName] = useState('');
  const [symbol, setSymbol] = useState('');
  const [isCreating, setIsCreating] = useState(false);

  const handleCreate = async () => {
    if (!isConnected) {
      onConnect();
      return;
    }

    if (!name || !symbol) {
      toast.error('Please enter both name and symbol');
      return;
    }

    if (name.length < 3 || name.length > 50) {
      toast.error('Token name must be between 3 and 50 characters');
      return;
    }

    if (symbol.length < 2 || symbol.length > 10) {
      toast.error('Token symbol must be between 2 and 10 characters');
      return;
    }

    setIsCreating(true);

    try {
      await onCreate(name, symbol);
      toast.success(`Token ${symbol} created successfully!`);
      setName('');
      setSymbol('');
      setIsOpen(false);
    } catch (error: any) {
      console.error('Create token error:', error);
      toast.error(error.message || 'Failed to create token');
    } finally {
      setIsCreating(false);
    }
  };

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="w-full py-3 px-4 bg-gradient-to-r from-primary to-secondary text-white
                 font-semibold rounded-lg hover:opacity-90 transition-all flex items-center
                 justify-center gap-2"
      >
        <PlusIcon className="w-5 h-5" />
        <span>Create New Token</span>
      </button>
    );
  }

  return (
    <div className="bg-dark-card rounded-xl p-6 border-2 border-primary/50">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-r from-primary to-secondary rounded-lg
                        flex items-center justify-center">
            <RocketLaunchIcon className="w-6 h-6 text-white" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-white">Launch New Token</h3>
            <p className="text-xs text-gray-400">Fair launch with bonding curve</p>
          </div>
        </div>
        <button
          onClick={() => setIsOpen(false)}
          className="text-gray-400 hover:text-white transition-colors"
        >
          ×
        </button>
      </div>

      {/* Token Name */}
      <div className="mb-4">
        <label className="block text-sm text-gray-400 mb-2">
          Token Name
        </label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="e.g., My Awesome Token"
          className="w-full px-4 py-3 bg-dark-bg text-white rounded-lg
                   focus:outline-none focus:ring-2 focus:ring-primary"
          maxLength={50}
          disabled={isCreating}
        />
        <div className="text-xs text-gray-500 mt-1">
          {name.length}/50 characters
        </div>
      </div>

      {/* Token Symbol */}
      <div className="mb-6">
        <label className="block text-sm text-gray-400 mb-2">
          Token Symbol
        </label>
        <input
          type="text"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value.toUpperCase())}
          placeholder="e.g., MAT"
          className="w-full px-4 py-3 bg-dark-bg text-white rounded-lg font-mono
                   focus:outline-none focus:ring-2 focus:ring-primary"
          maxLength={10}
          disabled={isCreating}
        />
        <div className="text-xs text-gray-500 mt-1">
          {symbol.length}/10 characters (uppercase)
        </div>
      </div>

      {/* Info Box */}
      <div className="mb-6 p-4 bg-dark-bg rounded-lg border border-gray-700">
        <h4 className="text-sm font-semibold text-white mb-2">Token Details:</h4>
        <div className="space-y-1 text-xs text-gray-400">
          <div>• Total Supply: 1,000,000,000 tokens</div>
          <div>• Initial Price: Determined by bonding curve</div>
          <div>• Trading Fee: 2% (1% platform + 1% creator)</div>
          <div>• Graduation: Automatic at 50 BNB</div>
          <div>• Creator Fee: You receive 1% of all trades!</div>
        </div>
      </div>

      {/* Create Button */}
      <button
        onClick={handleCreate}
        disabled={isCreating || !name || !symbol}
        className={`w-full py-3 px-4 text-white font-semibold rounded-lg
                 transition-all flex items-center justify-center gap-2
                 ${isCreating || !name || !symbol
                   ? 'bg-gray-600 cursor-not-allowed'
                   : 'bg-gradient-to-r from-primary to-secondary hover:opacity-90'
                 }`}
      >
        {isCreating ? (
          <>
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white" />
            <span>Creating Token...</span>
          </>
        ) : (
          <>
            <RocketLaunchIcon className="w-5 h-5" />
            <span>{isConnected ? 'Create Token' : 'Connect Wallet First'}</span>
          </>
        )}
      </button>

      {/* Warning */}
      <div className="mt-4 p-3 bg-yellow-500/10 border border-yellow-500/50 rounded-lg">
        <p className="text-xs text-yellow-500">
          ⚠️ Creating a token requires gas fees (~0.01-0.02 BNB on BSC Testnet).
          Make sure you have enough BNB in your wallet.
        </p>
      </div>
    </div>
  );
};
